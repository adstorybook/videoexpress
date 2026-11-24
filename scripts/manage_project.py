#!/usr/bin/env python3
"""Initialize VideoExpress projects and safely track workflow/scene state."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKFLOW_STATUSES = {
    "idea", "script_draft", "script_approved", "storyboard_draft", "storyboard_approved",
    "assets_generating", "assets_ready", "assembly", "render_preview", "review", "approved",
    "export_ready", "upload_pending_approval", "published", "analytics", "blocked",
}
NEXT_STAGE = {
    "idea": "script_draft",
    "script_draft": "script_approved",
    "script_approved": "storyboard_draft",
    "storyboard_draft": "storyboard_approved",
    "storyboard_approved": "assets_generating",
    "assets_generating": "assets_ready",
    "assets_ready": "assembly",
    "assembly": "render_preview",
    "render_preview": "review",
    "review": "approved",
    "approved": "export_ready",
    "export_ready": "upload_pending_approval",
    "upload_pending_approval": "published",
    "published": "analytics",
}
SCENE_STATUSES = {
    "planned", "prompt_approved", "generating", "generated", "selected", "rejected", "needs_correction",
}
ASSET_TYPES = {"image", "video", "voice", "music", "sfx", "caption", "thumbnail", "other"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}.")
    return value


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def project_paths(value: str | Path) -> tuple[Path, Path]:
    path = Path(value)
    manifest = path / "project.json" if path.is_dir() else path
    if manifest.name != "project.json":
        raise ValueError("Pass a project directory or its project.json file.")
    return manifest, manifest.parent


def load_project(value: str | Path) -> tuple[dict[str, Any], Path, Path]:
    manifest, directory = project_paths(value)
    project = read_json(manifest)
    if not isinstance(project.get("workflow"), dict):
        raise ValueError("Project manifest must contain a workflow object.")
    if not isinstance(project.get("scenes"), list):
        raise ValueError("Project manifest must contain a scenes array.")
    if not isinstance(project.get("assets", []), list):
        raise ValueError("Project assets must be an array.")
    return project, manifest, directory


def save_project(project: dict[str, Any], manifest: Path) -> None:
    write_json_atomic(manifest, project)


def find_scene(project: dict[str, Any], scene_id: str) -> dict[str, Any]:
    for scene in project.get("scenes", []):
        if scene.get("scene_id") == scene_id:
            return scene
    raise ValueError(f"Scene not found: {scene_id}")


def find_asset(project: dict[str, Any], asset_id: str) -> dict[str, Any]:
    for asset in project.get("assets", []):
        if asset.get("asset_id") == asset_id:
            return asset
    raise ValueError(f"Asset not found: {asset_id}")


def append_history(project: dict[str, Any], status: str, note: str, actor: str) -> None:
    now = utc_now()
    workflow = project["workflow"]
    workflow["status"] = status
    workflow["updated_at"] = now
    workflow.setdefault("history", []).append({"status": status, "at": now, "note": note, "actor": actor})


def is_approved_full_visual(asset: dict[str, Any]) -> bool:
    if asset.get("type") not in {"image", "video"}:
        return False
    coverage = asset.get("coverage")
    status = str(asset.get("status", "")).lower()
    if coverage in {"partial", "reference"} or "partial" in status or "reference" in status:
        return False
    approved = "approved" in status or "selected" in status
    return approved and (coverage in {None, "full"})


def require_scene_visual(project: dict[str, Any], scene: dict[str, Any], *, selected: bool) -> None:
    linked_ids = scene.get("asset_ids", [])
    if not linked_ids:
        raise ValueError(f"{scene.get('scene_id')}: add at least one visual asset before marking it generated/selected.")
    assets = [find_asset(project, asset_id) for asset_id in linked_ids]
    visuals = [asset for asset in assets if asset.get("type") in {"image", "video"}]
    if not visuals:
        raise ValueError(f"{scene.get('scene_id')}: linked assets contain no image/video coverage.")
    if selected and not any(is_approved_full_visual(asset) for asset in visuals):
        raise ValueError(
            f"{scene.get('scene_id')}: selection requires an approved full-coverage image/video asset; "
            "partial clips and character-reference images do not complete a scene."
        )


def safe_project_file(project_dir: Path, relative_ref: str) -> Path:
    candidate = (project_dir / relative_ref).resolve()
    root = project_dir.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("Referenced QA file must stay inside the project directory.")
    return candidate


def require_qa_approval(project: dict[str, Any], project_dir: Path) -> None:
    reference = project.get("qa_report_ref")
    if not reference:
        raise ValueError("A QA report reference is required before approval/export.")
    report_path = safe_project_file(project_dir, reference)
    if not report_path.is_file():
        raise ValueError(f"QA report file does not exist: {reference}")
    report = read_json(report_path)
    approval = report.get("approval", {})
    if report.get("overall_status") != "pass":
        raise ValueError("QA report overall_status must be 'pass'.")
    if report.get("full_watch_completed") is not True:
        raise ValueError("QA report must confirm a complete end-to-end watch.")
    if approval.get("approved") is not True or not approval.get("approved_by") or not approval.get("approved_at"):
        raise ValueError("QA report requires explicit approval metadata before export.")


def initialize_project(args: argparse.Namespace) -> int:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        raise ValueError("Project slug must use lowercase letters, numbers, and single hyphens.")
    template_dir = args.template_dir
    projects_dir = args.projects_dir
    template_project = read_json(template_dir / "project.json")
    template_corrections = read_json(template_dir / "corrections.json")
    template_qa = read_json(template_dir / "qa-report.json")
    target = projects_dir / args.slug
    if target.exists():
        raise ValueError(f"Project already exists; refusing to overwrite: {target}")

    now = utc_now()
    project = template_project
    project.update({
        "project_id": args.slug,
        "title": args.title,
        "channel": args.channel,
        "source_story_ref": args.source_story_ref,
        "script_ref": "script.md",
        "storyboard_ref": "storyboard.json",
        "corrections_ref": "corrections.json",
        "qa_report_ref": None,
        "settings": {**project.get("settings", {}), "runtime_seconds": args.runtime_seconds},
        "workflow": {
            "status": "idea",
            "updated_at": now,
            "history": [{"status": "idea", "at": now, "note": "Project initialized from the reusable template.", "actor": "manage_project.py"}],
        },
        "characters": [],
        "assets": [],
        "scenes": [{
            "scene_id": "scene-01",
            "order": 1,
            "target_duration_seconds": args.runtime_seconds,
            "narration_ref": "script.md#scene-01",
            "visual_prompt": None,
            "character_ids": [],
            "asset_ids": [],
            "status": "planned",
            "beat": "Replace this placeholder with the first approved story beat.",
            "notes": "Template placeholder; do not generate until replaced with an approved storyboard.",
        }],
        "render": None,
        "publishing": {
            "approval_required": True,
            "approved": False,
            "youtube_video_id": None,
            "youtube_url": None,
            "visibility": None,
            "published_at": None,
        },
        "analytics": [],
    })
    if isinstance(project.get("brief"), dict):
        project["brief"]["format"] = (
            f"{args.runtime_seconds // 60}-minute animated story film"
            if args.runtime_seconds % 60 == 0
            else f"{args.runtime_seconds}-second animated story film"
        )
    corrections = template_corrections
    corrections["project_id"] = args.slug
    qa_report = template_qa
    qa_report["report_id"] = f"qa-{args.slug}-pending"
    qa_report["project_id"] = args.slug
    qa_report["render_id"] = "pending-render"
    qa_report["created_at"] = now
    qa_report["full_watch_completed"] = False
    qa_report["overall_status"] = "incomplete"
    qa_report["approval"] = {"approved": False, "approved_by": None, "approved_at": None, "notes": "Awaiting a completed render and explicit user review."}
    if isinstance(qa_report.get("export"), dict):
        qa_report["export"]["duration_seconds"] = 0
        qa_report["export"]["file_ref"] = None
        qa_report["export"]["checksum"] = None

    projects_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{args.slug}.", dir=projects_dir) as temp_name:
        staging = Path(temp_name) / args.slug
        staging.mkdir()
        write_json_atomic(staging / "project.json", project)
        write_json_atomic(staging / "corrections.json", corrections)
        write_json_atomic(staging / "qa-report.json", qa_report)
        write_json_atomic(staging / "storyboard.json", {
            "project_id": args.slug,
            "approval_status": "draft_pending_user_review",
            "scenes": [{"scene_id": "scene-01", "order": 1, "duration_seconds": args.runtime_seconds,
                        "beat": "Replace this placeholder with the first approved story beat.",
                        "characters": [], "visual_prompt": None, "narration_ref": "script.md#scene-01"}],
        })
        (staging / "script.md").write_text(
            f"# {args.title}\n\nDraft pending. Replace this note with the approved source-faithful script before production.\n",
            encoding="utf-8",
        )
        os.replace(staging, target)
    print(f"Initialized project: {target}")
    return 0


def show_status(args: argparse.Namespace) -> int:
    project, _, _ = load_project(args.project)
    counts = Counter(scene.get("status", "unknown") for scene in project["scenes"])
    total = len(project["scenes"])
    selected = counts.get("selected", 0)
    result = {
        "project_id": project.get("project_id"),
        "title": project.get("title"),
        "workflow_status": project["workflow"].get("status"),
        "runtime_target_seconds": project.get("settings", {}).get("runtime_seconds"),
        "scene_count": total,
        "selected_scenes": selected,
        "scene_status_counts": dict(sorted(counts.items())),
        "asset_count": len(project.get("assets", [])),
        "blocked_from_status": project["workflow"].get("blocked_from_status"),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['title']} ({result['project_id']})")
        print(f"Workflow: {result['workflow_status']}")
        print(f"Runtime target: {result['runtime_target_seconds']} seconds")
        print(f"Scenes: {selected}/{total} selected; statuses: {dict(sorted(counts.items()))}")
        print(f"Registered assets: {result['asset_count']}")
        if result["blocked_from_status"]:
            print(f"Blocked at: {result['blocked_from_status']}")
    return 0


def update_scene_status(args: argparse.Namespace) -> int:
    project, manifest, _ = load_project(args.project)
    scene = find_scene(project, args.scene_id)
    previous = scene.get("status", "planned")
    if previous == args.status:
        raise ValueError(f"{args.scene_id} is already {args.status}.")
    if args.status in {"generated", "selected"}:
        require_scene_visual(project, scene, selected=args.status == "selected")
    now = utc_now()
    scene.setdefault("status_history", []).append({
        "from": previous, "to": args.status, "at": now, "actor": args.actor, "note": args.note,
    })
    scene["status"] = args.status
    if args.note:
        scene["notes"] = (str(scene.get("notes", "")).rstrip() + ("\n" if scene.get("notes") else "") + args.note)
    save_project(project, manifest)
    print(f"Updated {args.scene_id}: {previous} -> {args.status}")
    return 0


def add_asset(args: argparse.Namespace) -> int:
    project, manifest, _ = load_project(args.project)
    if any(asset.get("asset_id") == args.asset_id for asset in project.get("assets", [])):
        raise ValueError(f"Asset ID already exists: {args.asset_id}")
    scene = find_scene(project, args.scene_id) if args.scene_id else None
    asset: dict[str, Any] = {
        "asset_id": args.asset_id,
        "type": args.type,
        "status": args.status,
        "coverage": args.coverage,
        "created_at": utc_now(),
    }
    optional = {
        "provider": args.provider, "model": args.model, "prompt": args.prompt,
        "source_uri": args.source_uri, "storage_ref": args.storage_ref,
        "checksum": args.checksum, "rights_note": args.rights_note,
        "duration_seconds": args.duration_seconds, "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio, "frame_rate": args.frame_rate,
    }
    asset.update({key: value for key, value in optional.items() if value is not None})
    project.setdefault("assets", []).append(asset)
    if scene is not None:
        scene.setdefault("asset_ids", [])
        if args.asset_id not in scene["asset_ids"]:
            scene["asset_ids"].append(args.asset_id)
    save_project(project, manifest)
    target = f" and attached to {args.scene_id}" if scene else ""
    print(f"Recorded asset {args.asset_id}{target}.")
    return 0


def attach_asset(args: argparse.Namespace) -> int:
    project, manifest, _ = load_project(args.project)
    scene = find_scene(project, args.scene_id)
    find_asset(project, args.asset_id)
    scene.setdefault("asset_ids", [])
    if args.asset_id in scene["asset_ids"]:
        raise ValueError(f"Asset {args.asset_id} is already attached to {args.scene_id}.")
    scene["asset_ids"].append(args.asset_id)
    save_project(project, manifest)
    print(f"Attached {args.asset_id} to {args.scene_id}.")
    return 0


def stage_gate(project: dict[str, Any], project_dir: Path, target: str) -> None:
    if target in {"assets_ready", "assembly"}:
        scenes = project.get("scenes", [])
        if not scenes or any(scene.get("status") != "selected" for scene in scenes):
            raise ValueError("Every scene must have approved full-coverage assets and status 'selected' before assembly.")
    if target == "review":
        render = project.get("render") or {}
        if not render.get("output_ref"):
            raise ValueError("A render.output_ref is required before review.")
    if target in {"approved", "export_ready", "upload_pending_approval"}:
        if not (project.get("render") or {}).get("output_ref"):
            raise ValueError("A render.output_ref is required before approval/export/publishing preparation.")
        require_qa_approval(project, project_dir)
    if target == "upload_pending_approval":
        publishing = project.get("publishing") or {}
        if publishing.get("approval_required") is not True or publishing.get("approved") is True:
            raise ValueError("Publishing must remain approval-gated and unapproved while awaiting user approval.")
    if target == "published":
        publishing = project.get("publishing") or {}
        required = ("youtube_video_id", "youtube_url", "published_at")
        if publishing.get("approved") is not True:
            raise ValueError("Explicit publishing.approved=true is required before recording publication.")
        approval_fields = ("approved_by", "approved_at")
        missing_approval = [key for key in approval_fields if not publishing.get(key)]
        if missing_approval:
            raise ValueError("Publishing approval must include: " + ", ".join(missing_approval))
        missing = [key for key in required + ("visibility",) if not publishing.get(key)]
        if missing:
            raise ValueError("Verified YouTube readback is missing: " + ", ".join(missing))
    if target == "analytics":
        if not (project.get("publishing") or {}).get("youtube_video_id"):
            raise ValueError("A published YouTube video ID is required before analytics.")


def set_stage(args: argparse.Namespace) -> int:
    project, manifest, project_dir = load_project(args.project)
    current = project["workflow"].get("status")
    if current not in WORKFLOW_STATUSES:
        raise ValueError(f"Unknown current workflow status: {current}")
    target = args.status
    if target == "blocked":
        if current in {"published", "analytics", "blocked"}:
            raise ValueError(f"Cannot mark a project {current} as blocked.")
        project["workflow"]["blocked_from_status"] = current
    else:
        if current == "blocked":
            raise ValueError("Project is blocked; use the resume command after resolving the blocker.")
        expected = NEXT_STAGE.get(current)
        if target != expected:
            raise ValueError(f"Invalid stage transition {current} -> {target}; expected {expected or 'no next stage'}.")
        stage_gate(project, project_dir, target)
    append_history(project, target, args.note, args.actor)
    save_project(project, manifest)
    print(f"Workflow stage updated: {current} -> {target}")
    return 0


def resume_stage(args: argparse.Namespace) -> int:
    project, manifest, _ = load_project(args.project)
    workflow = project["workflow"]
    if workflow.get("status") != "blocked":
        raise ValueError("Project is not blocked.")
    target = workflow.get("blocked_from_status")
    if target not in WORKFLOW_STATUSES - {"blocked"}:
        raise ValueError("No valid blocked_from_status is recorded; cannot resume safely.")
    workflow.pop("blocked_from_status", None)
    append_history(project, target, args.note, args.actor)
    save_project(project, manifest)
    print(f"Resumed workflow at: {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a new project from the repository template")
    init.add_argument("slug")
    init.add_argument("--title", required=True)
    init.add_argument("--channel", default="TheStorybook_ad")
    init.add_argument("--runtime-seconds", type=int, default=300)
    init.add_argument("--source-story-ref")
    init.add_argument("--projects-dir", type=Path, default=Path("projects"))
    init.add_argument("--template-dir", type=Path, default=Path("projects/_template"))
    init.set_defaults(func=initialize_project)

    status = sub.add_parser("status", help="Show workflow and scene progress")
    status.add_argument("project", type=Path)
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=show_status)

    scene = sub.add_parser("scene-status", help="Record a scene status transition")
    scene.add_argument("project", type=Path)
    scene.add_argument("scene_id")
    scene.add_argument("status", choices=sorted(SCENE_STATUSES))
    scene.add_argument("--note", default="")
    scene.add_argument("--actor", default="operator")
    scene.set_defaults(func=update_scene_status)

    asset = sub.add_parser("add-asset", help="Register an asset and optionally attach it to a scene")
    asset.add_argument("project", type=Path)
    asset.add_argument("--asset-id", required=True)
    asset.add_argument("--type", choices=sorted(ASSET_TYPES), required=True)
    asset.add_argument("--status", default="generated")
    asset.add_argument("--coverage", choices=["full", "partial", "reference"], default="partial")
    asset.add_argument("--scene-id")
    for option in ("provider", "model", "prompt", "source-uri", "storage-ref", "checksum", "rights-note", "resolution", "aspect-ratio"):
        asset.add_argument("--" + option)
    asset.add_argument("--duration-seconds", type=float)
    asset.add_argument("--frame-rate", type=float)
    asset.set_defaults(func=add_asset)

    attach = sub.add_parser("attach-asset", help="Attach an already registered asset to a scene")
    attach.add_argument("project", type=Path)
    attach.add_argument("scene_id")
    attach.add_argument("asset_id")
    attach.set_defaults(func=attach_asset)

    stage = sub.add_parser("set-stage", help="Advance one workflow stage or mark it blocked")
    stage.add_argument("project", type=Path)
    stage.add_argument("status", choices=sorted(WORKFLOW_STATUSES))
    stage.add_argument("--note", required=True)
    stage.add_argument("--actor", default="operator")
    stage.set_defaults(func=set_stage)

    resume = sub.add_parser("resume", help="Resume a blocked project at its recorded stage")
    resume.add_argument("project", type=Path)
    resume.add_argument("--note", required=True)
    resume.add_argument("--actor", default="operator")
    resume.set_defaults(func=resume_stage)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
