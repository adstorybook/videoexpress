import copy
import json
import unittest
from pathlib import Path

from scripts.validate_project import validate_project

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "project.schema.json"


class ProjectManifestTests(unittest.TestCase):
    def test_seed_projects_validate(self):
        for path in (
            ROOT / "projects" / "the-clever-little-rabbits" / "project.json",
            ROOT / "projects" / "mother-magpie" / "project.json",
        ):
            with self.subTest(project=path):
                self.assertEqual(validate_project(path, SCHEMA), [])

    def test_unknown_character_is_detected(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        project["scenes"][0]["character_ids"].append("not-in-character-bible")
        temporary = ROOT / "tests" / "_invalid-project-fixture.json"
        try:
            temporary.write_text(json.dumps(project), encoding="utf-8")
            errors = validate_project(temporary, SCHEMA)
            self.assertTrue(any("unknown character IDs" in error for error in errors))
        finally:
            temporary.unlink(missing_ok=True)

    def test_unknown_asset_reference_is_detected(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        project["scenes"][0]["asset_ids"].append("missing-asset")
        temporary = ROOT / "tests" / "_invalid-project-fixture.json"
        try:
            temporary.write_text(json.dumps(project), encoding="utf-8")
            errors = validate_project(temporary, SCHEMA)
            self.assertTrue(any("unknown asset IDs" in error for error in errors))
        finally:
            temporary.unlink(missing_ok=True)

    def test_unknown_character_reference_asset_is_detected(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        project["characters"][-1]["reference_asset_ids"].append("missing-reference")
        temporary = ROOT / "tests" / "_invalid-project-fixture.json"
        try:
            temporary.write_text(json.dumps(project), encoding="utf-8")
            errors = validate_project(temporary, SCHEMA)
            self.assertTrue(any("unknown reference asset IDs" in error for error in errors))
        finally:
            temporary.unlink(missing_ok=True)

    def test_character_reference_must_be_image(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        wolf_reference = next(
            asset for asset in project["assets"]
            if asset["asset_id"] == "wolf-character-reference-001"
        )
        wolf_reference["type"] = "video"
        temporary = ROOT / "tests" / "_invalid-project-fixture.json"
        try:
            temporary.write_text(json.dumps(project), encoding="utf-8")
            errors = validate_project(temporary, SCHEMA)
            self.assertTrue(any("must be an image asset" in error for error in errors))
        finally:
            temporary.unlink(missing_ok=True)

    def test_duplicate_asset_id_is_detected(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        project["assets"].append(copy.deepcopy(project["assets"][0]))
        temporary = ROOT / "tests" / "_invalid-project-fixture.json"
        try:
            temporary.write_text(json.dumps(project), encoding="utf-8")
            errors = validate_project(temporary, SCHEMA)
            self.assertTrue(any("Asset IDs must be unique" in error for error in errors))
        finally:
            temporary.unlink(missing_ok=True)


    def test_rabbit_opening_clip_remains_full_hd_partial_reference(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        opening = next(
            asset for asset in project["assets"]
            if asset["asset_id"] == "rabbit-opening-clip-001"
        )
        self.assertEqual(opening["type"], "video")
        self.assertIn("partial", opening["status"])
        self.assertGreaterEqual(opening["duration_seconds"], 5.5)
        self.assertLessEqual(opening["duration_seconds"], 6.5)
        self.assertEqual(opening["resolution"], "1920x1080")
        self.assertEqual(opening["aspect_ratio"], "16:9")

    def test_rabbit_departure_and_wolf_arrival_scene_mapping(self):
        source = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"
        project = json.loads(source.read_text(encoding="utf-8"))
        scenes = {scene["scene_id"]: set(scene["asset_ids"]) for scene in project["scenes"]}
        self.assertIn("rabbit-scene2-departure-001", scenes["scene-02"])
        self.assertNotIn("rabbit-scene2-departure-001", scenes["scene-03"])
        self.assertIn("rabbit-scene3-wolf-arrival-001", scenes["scene-03"])
        self.assertNotIn("rabbit-scene3-wolf-arrival-001", scenes["scene-02"])

if __name__ == "__main__":
    unittest.main()
