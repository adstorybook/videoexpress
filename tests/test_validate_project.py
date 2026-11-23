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


if __name__ == "__main__":
    unittest.main()
