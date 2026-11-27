#!/usr/bin/env python3
"""Inspect an exported VideoExpress MP4 and emit a schema-compatible QA report.

This performs metadata and checksum checks only. It never marks a render watched
or approved; a human must review the complete export before release.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


def _parse_fraction(value: str | None) -> float | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    try:
        result = float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None
    return result if math.isfinite(result) and result > 0 else None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_project(path: Path) -> dict[str, Any]:
    try:
        project = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read project manifest {path}: {exc}") from exc
    if not isinstance(project, dict):
        raise ValueError(f"Project manifest must contain a JSON object: {path}")
    return project


def probe_media(path: Path, ffprobe: str = "ffprobe", timeout: int = 60) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Video file does not exist or is not a regular file: {path}")

    executable = shutil.which(ffprobe)
    if executable is None:
        raise RuntimeError(
            f"ffprobe was not found ({ffprobe!r}). Install FFmpeg and ensure ffprobe is on PATH."
        )

    command = [
        executable,
        "-v", "error",
        "-show_entries",
        "format=duration,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,duration",
        "-of", "json",
        str(path),
    ]
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"ffprobe timed out after {timeout} seconds.") from exc
    except OSError as exc:
        raise RuntimeError(f"Could not start ffprobe: {exc}") from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit code {completed.returncode}"
        raise RuntimeError(f"ffprobe failed: {detail}")
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("ffprobe returned invalid JSON.") from exc

    streams = data.get("streams")
    if not isinstance(streams, list):
        raise RuntimeError("ffprobe response did not contain a streams array.")
    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    video = video_streams[0] if video_streams else {}

    format_info = data.get("format") or {}
    duration_value = format_info.get("duration")
    if duration_value in (None, "N/A") and video:
        duration_value = video.get("duration")
    try:
        duration = float(duration_value) if duration_value not in (None, "N/A") else None
    except (TypeError, ValueError):
        duration = None
    if duration is not None and (not math.isfinite(duration) or duration < 0):
        duration = None

    width = video.get("width")
    height = video.get("height")
    try:
        width = int(width) if width is not None else None
        height = int(height) if height is not None else None
    except (TypeError, ValueError):
        width, height = None, None

    fps = _parse_fraction(video.get("avg_frame_rate")) or _parse_fraction(video.get("r_frame_rate"))
    format_name = str(format_info.get("format_name") or "")
    return {
        "format_name": format_name,
        "duration_seconds": duration,
        "video_stream": video or None,
        "audio_stream_count": len(audio_streams),
        "width": width,
        "height": height,
        "video_codec": video.get("codec_name"),
        "frame_rate": fps,
    }


def _parse_resolution(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", 1)
        width, height = int(width_text), int(height_text)
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"Unsupported manifest resolution {value!r}; expected WIDTHxHEIGHT.") from exc
    if width <= 0 or height <= 0:
        raise ValueError(f"Manifest resolution must be positive: {value!r}")
    return width, height


def _parse_aspect_ratio(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.split(":", 1)
        width, height = int(width_text), int(height_text)
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"Unsupported aspect ratio {value!r}; expected WIDTH:HEIGHT.") from exc
    if width <= 0 or height <= 0:
        raise ValueError(f"Aspect ratio must be positive: {value!r}")
    return width, height


def _actual_aspect_ratio(width: int | None, height: int | None) -> str:
    if not width or not height:
        return "unknown"
    divisor = math.gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def _check(check_id: str, passed: bool, notes: str, evidence_ref: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "result": "pass" if passed else "fail",
        "notes": notes,
        "timecode": None,
        "evidence_ref": evidence_ref,
    }


def build_report(
    project: dict[str, Any],
    video_path: Path,
    media: dict[str, Any],
    checksum: str,
    duration_tolerance: float = 1.0,
    require_audio: bool = True,
) -> dict[str, Any]:
    settings = project.get("settings") or {}
    project_id = str(project.get("project_id") or "unknown-project")
    target_duration = float(settings.get("runtime_seconds") or 300)
    target_width, target_height = _parse_resolution(str(settings.get("resolution") or "1920x1080"))
    target_ratio = _parse_aspect_ratio(str(settings.get("aspect_ratio") or "16:9"))

    actual_width, actual_height = media.get("width"), media.get("height")
    actual_duration = media.get("duration_seconds")
    actual_ratio = _actual_aspect_ratio(actual_width, actual_height)
    ratio_ok = bool(actual_width and actual_height) and math.isclose(
        actual_width / actual_height,
        target_ratio[0] / target_ratio[1],
        rel_tol=0,
        abs_tol=0.005,
    )
    runtime_ok = actual_duration is not None and abs(actual_duration - target_duration) <= duration_tolerance
    resolution_ok = actual_width == target_width and actual_height == target_height
    audio_ok = media.get("audio_stream_count", 0) > 0
    format_names = media.get("format_name", "").lower().split(",")
    mp4_ok = "mp4" in format_names
    video_ok = media.get("video_stream") is not None

    evidence = video_path.as_posix()
    checks = [
        _check("mp4_container", mp4_ok, f"Container format reported by ffprobe: {media.get('format_name') or 'unknown'}.", evidence),
        _check("video_stream_present", video_ok, "A video stream is present." if video_ok else "No video stream was detected.", evidence),
        _check("runtime", runtime_ok, f"Measured {actual_duration!s}s; target {target_duration:g}s ± {duration_tolerance:g}s.", evidence),
        _check("resolution", resolution_ok, f"Measured {actual_width}x{actual_height}; target {target_width}x{target_height}.", evidence),
        _check("aspect_ratio", ratio_ok, f"Measured {actual_ratio}; target {target_ratio[0]}:{target_ratio[1]}.", evidence),
        _check("audio_stream_present", audio_ok or not require_audio, f"Detected {media.get('audio_stream_count', 0)} audio stream(s)." if audio_ok else "No audio stream detected; audio is required." if require_audio else "No audio stream detected; allowed by configuration.", evidence),
        _check("sha256_checksum", bool(checksum), f"SHA-256: {checksum}.", evidence),
    ]
    has_failure = any(item["result"] == "fail" for item in checks)
    overall_status = "fail" if has_failure else "incomplete"

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    render_id = f"render-{checksum[:12]}" if checksum else "render-unidentified"
    frame_rate = media.get("frame_rate")
    return {
        "report_id": f"{project_id}-qa-{checksum[:12]}",
        "project_id": project_id,
        "render_id": render_id,
        "created_at": created_at,
        "reviewer": "Automated ffprobe inspection",
        "checks": checks,
        "overall_status": overall_status,
        "full_watch_completed": False,
        "approval": {
            "approved": False,
            "approved_by": None,
            "approved_at": None,
            "notes": "Automated metadata inspection only. A human must watch the complete export and approve it separately.",
        },
        "export": {
            "container": media.get("format_name") or "unknown",
            "codec": media.get("video_codec") or "unknown",
            "resolution": f"{actual_width}x{actual_height}" if actual_width and actual_height else "unknown",
            "aspect_ratio": actual_ratio,
            "frame_rate": float(frame_rate or 0),
            "duration_seconds": float(actual_duration or 0),
            "file_ref": evidence,
            "checksum": checksum,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Project manifest JSON path")
    parser.add_argument("video", type=Path, help="Exported MP4 file to inspect")
    parser.add_argument("--ffprobe", default="ffprobe", help="ffprobe executable name/path (default: ffprobe)")
    parser.add_argument("--duration-tolerance", type=float, default=1.0, help="Allowed runtime difference in seconds (default: 1)")
    parser.add_argument("--allow-missing-audio", action="store_true", help="Do not fail if the export has no audio stream")
    parser.add_argument("--output", type=Path, help="Optional path to write the QA report; stdout is used otherwise")
    args = parser.parse_args(argv)

    try:
        if args.duration_tolerance < 0:
            raise ValueError("--duration-tolerance cannot be negative.")
        project = load_project(args.project)
        media = probe_media(args.video, args.ffprobe)
        checksum = _sha256(args.video)
        report = build_report(
            project,
            args.video,
            media,
            checksum,
            duration_tolerance=args.duration_tolerance,
            require_audio=not args.allow_missing_audio,
        )
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"QA report written to {args.output}")
        else:
            sys.stdout.write(rendered)
        return 1 if report["overall_status"] == "fail" else 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
