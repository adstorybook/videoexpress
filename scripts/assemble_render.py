#!/usr/bin/env python3
"""Assemble ordered video clips and optional audio tracks into a draft MP4.

This local FFmpeg utility never uploads or publishes media. It refuses to overwrite
inputs or an existing output. Partial and silent previews require explicit flags.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts.inspect_render import load_project, probe_media

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "assembly-plan.schema.json"


def _finite_number(value: Any, field: str, *, minimum: float = 0.0, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number.")
    result = float(value)
    if not math.isfinite(result) or result < minimum or (maximum is not None and result > maximum):
        bound = f" between {minimum:g} and {maximum:g}" if maximum is not None else f" at least {minimum:g}"
        raise ValueError(f"{field} must be{bound}.")
    return result


def _resolve(base: Path, value: str, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty path string.")
    path = Path(value).expanduser()
    return (path if path.is_absolute() else base / path).resolve()


def load_plan(path: Path, schema_path: Path = DEFAULT_SCHEMA) -> tuple[dict[str, Any], Path]:
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read assembly plan {path}: {exc}") from exc
    if not isinstance(plan, dict):
        raise ValueError("Assembly plan must contain a JSON object.")
    try:
        import jsonschema  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Missing dependency jsonschema; install with: python -m pip install -r requirements.txt") from exc
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=plan, schema=schema)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read assembly-plan schema {schema_path}: {exc}") from exc
    except jsonschema.ValidationError as exc:
        location = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        raise ValueError(f"Assembly plan validation failed at {location}: {exc.message}") from exc
    except jsonschema.SchemaError as exc:
        raise RuntimeError(f"Invalid assembly-plan schema: {exc.message}") from exc
    return plan, path.resolve().parent


def _probe_clip(path: Path, ffprobe: str) -> float:
    media = probe_media(path, ffprobe=ffprobe)
    if media.get("video_stream") is None:
        raise ValueError(f"Clip has no video stream: {path}")
    duration = media.get("duration_seconds")
    if duration is None or not math.isfinite(float(duration)) or float(duration) <= 0:
        raise ValueError(f"Could not determine a positive duration for clip: {path}")
    return float(duration)


def prepare_inputs(
    plan: dict[str, Any],
    base: Path,
    output: Path,
    *,
    ffprobe: str,
    allow_partial_preview: bool,
    allow_silent_preview: bool,
    duration_tolerance: float,
) -> dict[str, Any]:
    manifest_path = _resolve(base, plan["project_manifest"], "project_manifest")
    project = load_project(manifest_path)
    settings = project.get("settings") or {}
    target_duration = _finite_number(settings.get("runtime_seconds", 300), "project runtime", minimum=0.001)
    resolution = str(settings.get("resolution") or "1920x1080")
    try:
        width_text, height_text = resolution.lower().split("x", 1)
        width, height = int(width_text), int(height_text)
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"Unsupported project resolution {resolution!r}; expected WIDTHxHEIGHT.") from exc
    if width <= 0 or height <= 0:
        raise ValueError("Project resolution must be positive.")
    aspect = str(settings.get("aspect_ratio") or "16:9")
    try:
        ratio_width, ratio_height = (int(part) for part in aspect.split(":", 1))
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Unsupported project aspect ratio {aspect!r}; expected WIDTH:HEIGHT.") from exc
    if ratio_width <= 0 or ratio_height <= 0 or not math.isclose(width / height, ratio_width / ratio_height, abs_tol=0.005):
        raise ValueError(f"Project resolution {resolution} does not match aspect ratio {aspect}.")
    frame_rate = _finite_number(settings.get("frame_rate") or 24, "frame_rate", minimum=1, maximum=120)

    clips: list[dict[str, Any]] = []
    for index, item in enumerate(plan["clips"], start=1):
        clip_path = _resolve(base, item["path"], f"clips[{index - 1}].path")
        actual_duration = _probe_clip(clip_path, ffprobe)
        start = _finite_number(item.get("start_seconds", 0), f"clips[{index - 1}].start_seconds")
        if start >= actual_duration:
            raise ValueError(f"Clip trim start {start:g}s is beyond its {actual_duration:g}s duration: {clip_path}")
        remaining = actual_duration - start
        duration = _finite_number(item["duration_seconds"], f"clips[{index - 1}].duration_seconds", minimum=0.001) if "duration_seconds" in item else remaining
        if duration > remaining + 0.001:
            raise ValueError(f"Requested {duration:g}s from clip with only {remaining:g}s remaining: {clip_path}")
        clips.append({"path": clip_path, "start": start, "duration": min(duration, remaining)})

    total_duration = sum(item["duration"] for item in clips)
    if total_duration > target_duration + duration_tolerance:
        raise ValueError(f"Assembled clips total {total_duration:.3f}s, exceeding project target {target_duration:.3f}s.")
    if not allow_partial_preview and abs(total_duration - target_duration) > duration_tolerance:
        raise ValueError(
            f"Clip total is {total_duration:.3f}s; project target is {target_duration:.3f}s "
            f"(tolerance ±{duration_tolerance:g}s). Use --allow-partial-preview only for a draft preview."
        )

    audio_tracks: list[dict[str, Any]] = []
    for index, item in enumerate(plan.get("audio_tracks", [])):
        audio_path = _resolve(base, item["path"], f"audio_tracks[{index}].path")
        if not audio_path.is_file():
            raise ValueError(f"Audio track does not exist or is not a regular file: {audio_path}")
        start = _finite_number(item.get("start_seconds", 0), f"audio_tracks[{index}].start_seconds")
        if start >= total_duration:
            raise ValueError(f"Audio track starts at {start:g}s, after the {total_duration:.3f}s output ends: {audio_path}")
        gain = _finite_number(item.get("gain", 1), f"audio_tracks[{index}].gain", minimum=0, maximum=2)
        audio_tracks.append({"path": audio_path, "start": start, "gain": gain, "loop": bool(item.get("loop", False)), "label": item.get("label", f"track-{index + 1}")})

    if not audio_tracks and not allow_silent_preview:
        raise ValueError("At least one audio track is required. Use --allow-silent-preview only for a silent draft.")

    if output == manifest_path:
        raise ValueError("Output path must not overwrite the project manifest.")
    if output in {item["path"] for item in clips} or output in {item["path"] for item in audio_tracks}:
        raise ValueError("Output path must not overwrite any source media.")

    return {
        "project": project,
        "manifest_path": manifest_path,
        "target_duration": target_duration,
        "duration": total_duration,
        "width": width,
        "height": height,
        "frame_rate": frame_rate,
        "clips": clips,
        "audio_tracks": audio_tracks,
    }


def build_ffmpeg_command(
    prepared: dict[str, Any], output: Path, ffmpeg_path: str
) -> list[str]:
    clips = prepared["clips"]
    audio_tracks = prepared["audio_tracks"]
    width, height = prepared["width"], prepared["height"]
    fps = prepared["frame_rate"]
    duration = prepared["duration"]

    command = [ffmpeg_path, "-hide_banner", "-nostdin", "-n"]
    for clip in clips:
        command.extend(["-i", str(clip["path"])])
    for track in audio_tracks:
        if track["loop"]:
            command.extend(["-stream_loop", "-1"])
        command.extend(["-i", str(track["path"])])

    filters: list[str] = []
    video_labels: list[str] = []
    for index, clip in enumerate(clips):
        label = f"v{index}"
        video_labels.append(f"[{label}]")
        filters.append(
            f"[{index}:v:0]trim=start={clip['start']:.6f}:duration={clip['duration']:.6f},"
            f"setpts=PTS-STARTPTS,scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"fps={fps:g},setsar=1,format=yuv420p[{label}]"
        )
    filters.append(f"{''.join(video_labels)}concat=n={len(clips)}:v=1:a=0[vout]")

    if audio_tracks:
        audio_labels: list[str] = []
        clip_input_count = len(clips)
        for index, track in enumerate(audio_tracks):
            input_index = clip_input_count + index
            label = f"a{index}"
            audio_labels.append(f"[{label}]")
            delay_ms = round(track["start"] * 1000)
            chain = f"[{input_index}:a:0]volume={track['gain']:.6f}"
            if delay_ms:
                chain += f",adelay=delays={delay_ms}:all=1"
            chain += f",apad,atrim=duration={duration:.6f},asetpts=PTS-STARTPTS[{label}]"
            filters.append(chain)
        if len(audio_labels) == 1:
            filters.append(f"{audio_labels[0]}anull[aout]")
        else:
            filters.append(
                f"{''.join(audio_labels)}amix=inputs={len(audio_labels)}:duration=longest:"
                "dropout_transition=0:normalize=0,alimiter=limit=0.95[aout]"
            )

    command.extend(["-filter_complex", ";".join(filters), "-map", "[vout]"])
    if audio_tracks:
        command.extend(["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"])
    command.extend([
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", f"{fps:g}", "-t", f"{duration:.6f}", "-movflags", "+faststart", str(output),
    ])
    return command


def assemble(
    plan_path: Path,
    output_override: Path | None = None,
    *,
    ffmpeg: str = "ffmpeg",
    ffprobe: str = "ffprobe",
    timeout: int = 3600,
    allow_partial_preview: bool = False,
    allow_silent_preview: bool = False,
    duration_tolerance: float = 1.0,
    dry_run: bool = False,
) -> tuple[int, str]:
    plan_path = plan_path.resolve()
    plan, base = load_plan(plan_path)
    output_value = output_override or (Path(plan["output"]) if plan.get("output") else None)
    if output_value is None:
        raise ValueError("Provide an output path in the plan or with --output.")
    output = output_value.expanduser()
    if not output.is_absolute():
        output = (Path.cwd() / output).resolve() if output_override is not None else (base / output).resolve()
    else:
        output = output.resolve()
    if output.suffix.lower() != ".mp4":
        raise ValueError("Output filename must end in .mp4.")
    if output.exists():
        raise ValueError(f"Refusing to overwrite existing output: {output}")
    if output == plan_path:
        raise ValueError("Output path must not overwrite the assembly plan.")
    if timeout <= 0:
        raise ValueError("Timeout must be positive.")
    if duration_tolerance < 0 or not math.isfinite(duration_tolerance):
        raise ValueError("Duration tolerance must be a finite non-negative number.")

    prepared = prepare_inputs(
        plan, base, output, ffprobe=ffprobe,
        allow_partial_preview=allow_partial_preview,
        allow_silent_preview=allow_silent_preview,
        duration_tolerance=duration_tolerance,
    )
    ffmpeg_path = shutil.which(ffmpeg)
    if ffmpeg_path is None:
        raise RuntimeError(f"ffmpeg was not found ({ffmpeg!r}). Install FFmpeg and ensure ffmpeg is on PATH.")
    command = build_ffmpeg_command(prepared, output, ffmpeg_path)
    if dry_run:
        return 0, shlex.join(command)

    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"ffmpeg timed out after {timeout} seconds.") from exc
    except OSError as exc:
        raise RuntimeError(f"Could not start ffmpeg: {exc}") from exc
    if completed.returncode != 0:
        detail = completed.stderr.strip()[-3000:] or f"exit code {completed.returncode}"
        raise RuntimeError(f"ffmpeg assembly failed: {detail}")
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("ffmpeg reported success but did not create a non-empty MP4.")
    return 0, f"Draft MP4 assembled: {output} ({output.stat().st_size} bytes, {prepared['duration']:.3f}s). Run scripts/inspect_render.py next; human review is still required."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Assembly plan JSON")
    parser.add_argument("--output", type=Path, help="Override output MP4 path")
    parser.add_argument("--ffmpeg", default="ffmpeg", help="FFmpeg executable name/path")
    parser.add_argument("--ffprobe", default="ffprobe", help="FFprobe executable name/path")
    parser.add_argument("--timeout", type=int, default=3600, help="Assembly timeout in seconds")
    parser.add_argument("--duration-tolerance", type=float, default=1.0, help="Allowed difference from project runtime")
    parser.add_argument("--allow-partial-preview", action="store_true", help="Allow a shorter-than-target draft preview")
    parser.add_argument("--allow-silent-preview", action="store_true", help="Allow a preview with no audio tracks")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print the FFmpeg command without assembling")
    args = parser.parse_args(argv)
    try:
        code, message = assemble(
            args.plan, args.output, ffmpeg=args.ffmpeg, ffprobe=args.ffprobe,
            timeout=args.timeout, allow_partial_preview=args.allow_partial_preview,
            allow_silent_preview=args.allow_silent_preview,
            duration_tolerance=args.duration_tolerance, dry_run=args.dry_run,
        )
        print(message)
        return code
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
