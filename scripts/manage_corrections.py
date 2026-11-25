#!/usr/bin/env python3
"""Manage project/channel correction records without promoting unapproved feedback."""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

CATEGORIES = {
    "voice", "pronunciation", "pacing", "emotion", "character_continuity",
    "visual_style", "prompt", "editing", "music", "sound_effect", "caption",
    "story", "branding", "technical", "other",
}
STATUSES = {"proposed", "approved", "rejected", "applied", "verified"}
ENTRY_KEYS = {
    "correction_id", "date", "scope", "project_id", "category", "scene_id",
    "timecode", "issue", "requested_change", "applied_change", "evidence_ref",
    "status", "approved_by", "approved_at", "reuse_as_rule", "rule_text", "notes",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_log(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": "1.0", "project_id": None, "entries": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read correction log {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ValueError("Correction log must be a JSON object with an entries array.")
    ids = [entry.get("correction_id") for entry in data["entries"] if isinstance(entry, dict)]
    if len(ids) != len(set(ids)):
        raise ValueError("Correction log contains duplicate correction_id values.")
    for entry in data["entries"]:
        if not isinstance(entry, dict):
            raise ValueError("Every correction entry must be a JSON object.")
        validate_entry(entry)
    return data


def save_log(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def validate_entry(entry: dict[str, Any]) -> None:
    missing = [key for key in ("correction_id", "date", "scope", "category", "issue", "requested_change", "status") if not entry.get(key)]
    if missing:
        raise ValueError("Correction entry missing required fields: " + ", ".join(missing))
    unknown = set(entry) - ENTRY_KEYS
    if unknown:
        raise ValueError("Unknown correction fields: " + ", ".join(sorted(unknown)))
    try:
        date.fromisoformat(entry["date"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Correction date must use YYYY-MM-DD.") from exc
    if entry["scope"] not in {"project", "channel"}:
        raise ValueError("Scope must be project or channel.")
    if entry["category"] not in CATEGORIES:
        raise ValueError(f"Category must be one of: {', '.join(sorted(CATEGORIES))}.")
    if entry["status"] not in STATUSES:
        raise ValueError(f"Status must be one of: {', '.join(sorted(STATUSES))}.")
    if entry.get("reuse_as_rule") and (entry["scope"] != "channel" or not entry.get("rule_text")):
        raise ValueError("A reusable rule must be channel-scoped and include rule_text.")
    if entry.get("status") in {"approved", "verified"} and (not entry.get("approved_by") or not entry.get("approved_at")):
        raise ValueError("Approved/verified corrections require approved_by and approved_at.")


def add_entry(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    project_id = args.project_id or data.get("project_id")
    if args.scope == "project" and not project_id:
        raise ValueError("Project-scoped entries require --project-id or a project_id in the log.")
    if args.scope == "channel" and args.reuse_as_rule and not args.rule_text:
        raise ValueError("--reuse-as-rule requires --rule-text.")
    entry = {
        "correction_id": "corr-" + uuid.uuid4().hex[:12],
        "date": args.date or date.today().isoformat(),
        "scope": args.scope,
        "project_id": project_id if args.scope == "project" else None,
        "category": args.category,
        "scene_id": args.scene_id,
        "timecode": args.timecode,
        "issue": args.issue,
        "requested_change": args.requested_change,
        "applied_change": None,
        "evidence_ref": args.evidence_ref,
        "status": "proposed",
        "approved_by": None,
        "approved_at": None,
        "reuse_as_rule": bool(args.reuse_as_rule),
        "rule_text": args.rule_text,
        "notes": args.notes or "",
    }
    validate_entry(entry)
    data.setdefault("entries", []).append(entry)
    if args.scope == "project" and not data.get("project_id"):
        data["project_id"] = project_id
    return entry


def find_entry(data: dict[str, Any], correction_id: str) -> dict[str, Any]:
    for entry in data.get("entries", []):
        if entry.get("correction_id") == correction_id:
            return entry
    raise ValueError(f"Correction not found: {correction_id}")


def approve_entry(entry: dict[str, Any], approved_by: str) -> None:
    if entry["status"] not in {"proposed", "applied"}:
        raise ValueError(f"Only proposed/applied corrections can be approved (current: {entry['status']}).")
    if entry.get("reuse_as_rule") and (entry.get("scope") != "channel" or not entry.get("rule_text")):
        raise ValueError("Reusable rules must be channel-scoped and have rule_text.")
    entry["status"] = "approved"
    entry["approved_by"] = approved_by
    entry["approved_at"] = utc_now()


def mark_applied(entry: dict[str, Any], applied_change: str) -> None:
    if entry["status"] not in {"proposed", "approved"}:
        raise ValueError(f"Only proposed/approved corrections can be marked applied (current: {entry['status']}).")
    entry["applied_change"] = applied_change
    # Keep an explicit approval intact; an approved rule remains reusable.
    if entry["status"] == "proposed":
        entry["status"] = "applied"


def reject_entry(entry: dict[str, Any], reason: str) -> None:
    if entry["status"] not in {"proposed", "applied"}:
        raise ValueError(f"Only proposed/applied corrections can be rejected (current: {entry['status']}).")
    entry["status"] = "rejected"
    entry["notes"] = (entry.get("notes", "") + ("\n" if entry.get("notes") else "") + "Rejected: " + reason).strip()


def effective_rules(data: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"correction_id": entry["correction_id"], "category": entry["category"], "rule": entry["rule_text"]}
        for entry in data.get("entries", [])
        if entry.get("scope") == "channel"
        and entry.get("reuse_as_rule") is True
        and entry.get("status") in {"approved", "verified"}
        and entry.get("rule_text")
    ]


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("log", type=Path, help="Path to corrections.json")
    sub = p.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Record new feedback as proposed (never auto-approved)")
    add.add_argument("--scope", choices=["project", "channel"], default="project")
    add.add_argument("--project-id")
    add.add_argument("--category", choices=sorted(CATEGORIES), required=True)
    add.add_argument("--issue", required=True)
    add.add_argument("--requested-change", required=True)
    add.add_argument("--date")
    add.add_argument("--scene-id")
    add.add_argument("--timecode")
    add.add_argument("--evidence-ref")
    add.add_argument("--reuse-as-rule", action="store_true")
    add.add_argument("--rule-text")
    add.add_argument("--notes", default="")
    approve = sub.add_parser("approve", help="Explicitly approve a correction for reuse")
    approve.add_argument("correction_id")
    approve.add_argument("--approved-by", required=True, help="Name/role of the approver; must be supplied explicitly")
    applied = sub.add_parser("mark-applied", help="Record a correction applied to a project")
    applied.add_argument("correction_id")
    applied.add_argument("--applied-change", required=True)
    reject = sub.add_parser("reject", help="Reject a proposed correction and record why")
    reject.add_argument("correction_id")
    reject.add_argument("--reason", required=True)
    listing = sub.add_parser("list", help="Print the correction log")
    listing.add_argument("--status", choices=sorted(STATUSES))
    sub.add_parser("rules", help="Print only approved reusable channel rules")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        data = load_log(args.log)
        if args.command == "add":
            entry = add_entry(data, args)
            save_log(args.log, data)
            print(f"Added {entry['correction_id']} with status proposed.")
        elif args.command == "approve":
            entry = find_entry(data, args.correction_id)
            approve_entry(entry, args.approved_by)
            validate_entry(entry)
            save_log(args.log, data)
            print(f"Approved {entry['correction_id']}; reusable channel rules are now eligible if flagged.")
        elif args.command == "mark-applied":
            entry = find_entry(data, args.correction_id)
            mark_applied(entry, args.applied_change)
            validate_entry(entry)
            save_log(args.log, data)
            print(f"Marked {entry['correction_id']} applied.")
        elif args.command == "reject":
            entry = find_entry(data, args.correction_id)
            reject_entry(entry, args.reason)
            validate_entry(entry)
            save_log(args.log, data)
            print(f"Rejected {entry['correction_id']}.")
        elif args.command == "list":
            entries = data.get("entries", [])
            if args.status:
                entries = [entry for entry in entries if entry.get("status") == args.status]
            print(json.dumps(entries, ensure_ascii=False, indent=2))
        elif args.command == "rules":
            print(json.dumps(effective_rules(data), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
