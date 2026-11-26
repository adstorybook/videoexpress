"""Structural checks for the separately versioned expanded production packs."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKS = (
    ROOT / "production-packs/expanded-retellings/the-three-little-rabbits-and-the-wolfs-tail.md",
    ROOT / "production-packs/expanded-retellings/mama-nells-big-heart.md",
)
REQUIRED_FIELDS = (
    "**Target duration:**",
    "**Narration:**",
    "**Reference image prompt:**",
    "**Video prompt:**",
    "**Optional dialogue:**",
    "**Voice direction:**",
    "**Audio:**",
)


class ExpandedProductionPackTests(unittest.TestCase):
    def test_each_pack_has_fourteen_complete_scenes_and_five_minute_timing(self):
        for path in PACKS:
            with self.subTest(pack=path.name):
                content = path.read_text(encoding="utf-8")
                headings = list(re.finditer(r"^## Scene \d{2} — .+$", content, re.MULTILINE))
                self.assertEqual(len(headings), 14, "each expanded pack must have 14 scenes")

                for index, match in enumerate(headings):
                    end = headings[index + 1].start() if index + 1 < len(headings) else content.find("\n## End card", match.end())
                    if end < 0:
                        end = len(content)
                    scene = content[match.start():end]
                    for field in REQUIRED_FIELDS:
                        self.assertIn(field, scene, f"{path.name}: scene {index + 1} missing {field}")

                durations = [int(value) for value in re.findall(r"\*\*Target duration:\*\* (\d+) seconds", content)]
                self.assertEqual(len(durations), 14)
                self.assertEqual(sum(durations) + 10, 300, "14 scenes plus 5s title and 5s end card must total 300s")

    def test_packs_are_explicitly_separate_from_canonical_project_manifests(self):
        index = (ROOT / "production-packs/expanded-retellings/README.md").read_text(encoding="utf-8")
        self.assertIn("not yet adopted", index)
        self.assertIn("source-checked project drafts", index)
        for path in PACKS:
            self.assertIn("Alternate expanded retelling", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
