import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import validate_project

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "project.schema.json"
RABBITS = ROOT / "projects" / "the-clever-little-rabbits" / "project.json"


class ProjectManifestTests(unittest.TestCase):
    def test_seed_projects_validate(self):
        for path in (
            RABBITS,
            ROOT / "projects" / "mother-magpie" / "project.json",
        ):
            with self.subTest(project=path):
                self.assertEqual(validate_project(path, SCHEMA), [])

    def validate_mutation(self, mutation):
        project = json.loads(RABBITS.read_text(encoding="utf-8"))
        mutation(project)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory) / "invalid-project.json"
            temporary.write_text(json.dumps(project), encoding="utf-8")
            return validate_project(temporary, SCHEMA)

    def test_unknown_character_is_detected(self):
        errors = self.validate_mutation(
            lambda project: project["scenes"][0]["character_ids"].append("not-in-character-bible")
        )
        self.assertTrue(any("unknown character IDs" in error for error in errors))

    def test_duplicate_character_id_is_detected(self):
        def mutate(project):
            project["characters"][1]["character_id"] = project["characters"][0]["character_id"]

        errors = self.validate_mutation(mutate)
        self.assertTrue(any("Character IDs must be unique" in error for error in errors))

    def test_duplicate_asset_id_is_detected(self):
        def mutate(project):
            duplicate = copy.deepcopy(project["assets"][0])
            project["assets"].append(duplicate)

        errors = self.validate_mutation(mutate)
        self.assertTrue(any("Asset IDs must be unique" in error for error in errors))

    def test_scene_unknown_asset_is_detected(self):
        errors = self.validate_mutation(
            lambda project: project["scenes"][0]["asset_ids"].append("missing-scene-asset")
        )
        self.assertTrue(any("unknown asset IDs" in error for error in errors))

    def test_character_unknown_reference_asset_is_detected(self):
        errors = self.validate_mutation(
            lambda project: project["characters"][0]["reference_asset_ids"].append("missing-reference")
        )
        self.assertTrue(any("unknown reference asset IDs" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
