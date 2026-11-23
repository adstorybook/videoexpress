import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage_corrections.py"


class CorrectionManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = Path(self.tmp.name) / "corrections.json"

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, expect=0):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.log), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, result.stderr)
        return result

    def test_add_creates_proposed_project_entry(self):
        out = self.run_cli("add", "--project-id", "rabbits", "--category", "voice", "--issue", "Narration too fast", "--requested-change", "Slow by 10 percent")
        self.assertIn("status proposed", out.stdout)
        data = json.loads(self.log.read_text())
        entry = data["entries"][0]
        self.assertEqual(entry["status"], "proposed")
        self.assertEqual(entry["project_id"], "rabbits")
        self.assertFalse(entry["reuse_as_rule"])

    def test_channel_rule_is_hidden_until_explicit_approval(self):
        add = self.run_cli("add", "--scope", "channel", "--category", "pacing", "--issue", "Narration rushed", "--requested-change", "Use slower delivery", "--reuse-as-rule", "--rule-text", "Narrate 10% slower")
        correction_id = add.stdout.split()[1]
        self.assertEqual(json.loads(self.run_cli("rules").stdout), [])
        self.run_cli("approve", correction_id, "--approved-by", "user")
        rules = json.loads(self.run_cli("rules").stdout)
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["rule"], "Narrate 10% slower")

    def test_applied_change_does_not_remove_an_approved_channel_rule(self):
        add = self.run_cli("add", "--scope", "channel", "--category", "pacing", "--issue", "Delivery too quick", "--requested-change", "Slow delivery", "--reuse-as-rule", "--rule-text", "Use calmer pace")
        correction_id = add.stdout.split()[1]
        self.run_cli("approve", correction_id, "--approved-by", "user")
        self.run_cli("mark-applied", correction_id, "--applied-change", "Applied in current scene")
        entry = json.loads(self.log.read_text())["entries"][0]
        self.assertEqual(entry["status"], "approved")
        self.assertEqual(len(json.loads(self.run_cli("rules").stdout)), 1)

    def test_reusable_rule_requires_channel_scope_and_text(self):
        self.run_cli("add", "--project-id", "rabbits", "--category", "visual_style", "--issue", "Wrong style", "--requested-change", "Fix style", "--reuse-as-rule", "--rule-text", "Use approved style", expect=2)
        self.assertFalse(self.log.exists())

    def test_mark_applied_and_approve_state(self):
        add = self.run_cli("add", "--project-id", "rabbits", "--category", "editing", "--issue", "Timing mismatch", "--requested-change", "Shorten scene")
        correction_id = add.stdout.split()[1]
        self.run_cli("mark-applied", correction_id, "--applied-change", "Trimmed by 4 seconds")
        self.run_cli("approve", correction_id, "--approved-by", "user")
        entry = json.loads(self.log.read_text())["entries"][0]
        self.assertEqual(entry["status"], "approved")
        self.assertEqual(entry["applied_change"], "Trimmed by 4 seconds")
        self.assertTrue(entry["approved_at"])

    def test_rejected_correction_does_not_become_reusable(self):
        add = self.run_cli("add", "--scope", "channel", "--category", "visual_style", "--issue", "Style mismatch", "--requested-change", "Use consistent lighting", "--reuse-as-rule", "--rule-text", "Use approved soft lighting")
        correction_id = add.stdout.split()[1]
        self.run_cli("reject", correction_id, "--reason", "Only for this scene")
        self.assertEqual(json.loads(self.run_cli("rules").stdout), [])
        entry = json.loads(self.log.read_text())["entries"][0]
        self.assertEqual(entry["status"], "rejected")
        self.assertIn("Only for this scene", entry["notes"])

    def test_approval_requires_explicit_approver(self):
        add = self.run_cli("add", "--project-id", "rabbits", "--category", "caption", "--issue", "Typo", "--requested-change", "Correct text")
        correction_id = add.stdout.split()[1]
        self.run_cli("approve", correction_id, expect=2)
        entry = json.loads(self.log.read_text())["entries"][0]
        self.assertEqual(entry["status"], "proposed")


if __name__ == "__main__":
    unittest.main()
