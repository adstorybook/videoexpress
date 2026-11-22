#!/usr/bin/env python3
"""Validate a VideoExpress project manifest and cross-reference consistency."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read JSON {path}: {exc}") from exc


def validate_project(project_path: Path, schema_path: Path) -> list[str]:
    project = load_json(project_path)
    schema = load_json(schema_path)
    errors: list[str] = []

    try:
        import jsonschema  # type: ignore
    except ImportError:
        errors.append("Missing dependency jsonschema; install with: python -m pip install -r requirements.txt")
        return errors

    try:
        jsonschema.validate(instance=project, schema=schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"Schema validation: {exc.message} (at {'/'.join(map(str, exc.absolute_path))})")
    except jsonschema.SchemaError as exc:
        errors.append(f"Invalid schema: {exc.message}")

    scenes = project.get("scenes", [])
    scene_ids = [scene.get("scene_id") for scene in scenes]
    if len(scene_ids) != len(set(scene_ids)):
        errors.append("Scene IDs must be unique.")

    orders = [scene.get("order") for scene in scenes]
    if orders != sorted(orders):
        errors.append("Scenes must be sorted by their order field.")
    if orders and orders != list(range(1, len(orders) + 1)):
        errors.append("Scene order must be contiguous starting at 1.")

    target_seconds = project.get("settings", {}).get("runtime_seconds")
    planned_seconds = sum(float(scene.get("target_duration_seconds", 0)) for scene in scenes)
    if target_seconds is not None and abs(planned_seconds - float(target_seconds)) > 1:
        errors.append(
            f"Scene durations total {planned_seconds:g}s but target runtime is {target_seconds}s "
            "(tolerance: 1s)."
        )

    characters = project.get("characters", [])
    character_ids = [character.get("character_id") for character in characters]
    if len(character_ids) != len(set(character_ids)):
        errors.append("Character IDs must be unique.")
    known_characters = set(character_ids)

    assets = project.get("assets", [])
    asset_ids = [asset.get("asset_id") for asset in assets]
    if len(asset_ids) != len(set(asset_ids)):
        errors.append("Asset IDs must be unique.")
    known_assets = set(asset_ids)

    for character in characters:
        unknown_assets = set(character.get("reference_asset_ids", [])) - known_assets
        if unknown_assets:
            errors.append(
                f"{character.get('character_id')}: unknown reference asset IDs: "
                f"{', '.join(sorted(unknown_assets))}"
            )

    for scene in scenes:
        unknown = set(scene.get("character_ids", [])) - known_characters
        if unknown:
            errors.append(f"{scene.get('scene_id')}: unknown character IDs: {', '.join(sorted(unknown))}")
        unknown_assets = set(scene.get("asset_ids", [])) - known_assets
        if unknown_assets:
            errors.append(f"{scene.get('scene_id')}: unknown asset IDs: {', '.join(sorted(unknown_assets))}")

    if not project.get("corrections_ref"):
        errors.append("A correction log reference is required so feedback can be retained.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Path to project.json")
    parser.add_argument("--schema", type=Path, default=Path("schemas/project.schema.json"))
    args = parser.parse_args()
    try:
        errors = validate_project(args.project, args.schema)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.project} passed schema and project consistency checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
