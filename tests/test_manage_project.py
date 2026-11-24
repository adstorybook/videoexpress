import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage_project.py"


def project_fixture(status="assets_generating"):
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": "1.0",
        "project_id": "test-story",
        "title": "Test Story",
        "channel": "TheStorybook_ad",
        "settings": {"runtime_seconds": 300, "aspect_ratio": "16:9", "resolution": "1920x1080"},
        "workflow": {"status": status, "updated_at": now, "history": []},
        "script_ref": "script.md",
        "storyboard_ref": "storyboard.json",
        "characters": [],
        "scenes": [{"scene_id": "scene-01", "order": 1, "target_duration_seconds": 300,
                    "character_ids": [], "asset_ids": [], "status": "planned", "notes": ""}],
        "assets": [],
        "corrections_ref": "corrections.json",
        "qa_report_ref": None,
        "render": None,
        "publishing": {"approval_required": True, "approved": False, "youtube_video_id": None,
                       "youtube_url": None, "visibility": None, "published_at": None},
        "analytics": [],
    }


class ManageProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project_dir = self.root / "test-story"
        self.project_dir.mkdir()
        self.manifest = self.project_dir / "project.json"
        self.save_project(project_fixture())

    def tearDown(self):
        self.tmp.cleanup()

    def save_project(self, project):
        self.manifest.write_text(json.dumps(project, indent=2), encoding="utf-8")

    def load_project(self):
        return json.loads(self.manifest.read_text(encoding="utf-8"))

    def run_cli(self, *args, expect=0):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, result.stderr)
        return result

    def add_visual(self, *, asset_id="clip-01", coverage="full", status="approved"):
        self.run_cli("add-asset", self.project_dir, "--asset-id", asset_id, "--type", "video",
                     "--status", status, "--coverage", coverage, "--scene-id", "scene-01")

    def test_status_reports_stage_and_scene_progress(self):
        result = self.run_cli("status", self.project_dir, "--json")
        summary = json.loads(result.stdout)
        self.assertEqual(summary["workflow_status"], "assets_generating")
        self.assertEqual(summary["scene_count"], 1)
        self.assertEqual(summary["selected_scenes"], 0)

    def test_add_asset_registers_metadata_and_attaches_to_scene(self):
        self.add_visual(asset_id="rabbit-shot", coverage="partial", status="generated")
        project = self.load_project()
        self.assertEqual(project["scenes"][0]["asset_ids"], ["rabbit-shot"])
        self.assertEqual(project["assets"][0]["coverage"], "partial")
        self.assertEqual(project["assets"][0]["type"], "video")

    def test_duplicate_asset_id_is_rejected(self):
        self.add_visual()
        self.run_cli("add-asset", self.project_dir, "--asset-id", "clip-01", "--type", "video", expect=2)

    def test_partial_clip_cannot_mark_scene_selected(self):
        self.add_visual(coverage="partial", status="approved_partial_scene_coverage")
        self.run_cli("scene-status", self.project_dir, "scene-01", "selected", expect=2)
        self.assertEqual(self.load_project()["scenes"][0]["status"], "planned")

    def test_approved_full_clip_can_mark_scene_selected(self):
        self.add_visual(coverage="full", status="approved_full_scene_coverage")
        self.run_cli("scene-status", self.project_dir, "scene-01", "selected", "--note", "Reviewed full scene")
        scene = self.load_project()["scenes"][0]
        self.assertEqual(scene["status"], "selected")
        self.assertEqual(scene["status_history"][-1]["note"], "Reviewed full scene")

    def test_assets_ready_gate_requires_every_scene_selected(self):
        self.run_cli("set-stage", self.project_dir, "assets_ready", "--note", "All scenes ready", expect=2)
        self.assertEqual(self.load_project()["workflow"]["status"], "assets_generating")

    def test_workflow_cannot_skip_a_stage(self):
        self.run_cli("set-stage", self.project_dir, "assembly", "--note", "Skip ahead", expect=2)
        self.assertEqual(self.load_project()["workflow"]["status"], "assets_generating")

    def test_block_and_resume_returns_to_recorded_stage(self):
        self.run_cli("set-stage", self.project_dir, "blocked", "--note", "Waiting for source assets")
        self.run_cli("resume", self.project_dir, "--note", "Assets are available")
        workflow = self.load_project()["workflow"]
        self.assertEqual(workflow["status"], "assets_generating")
        self.assertNotIn("blocked_from_status", workflow)

    def test_init_creates_project_from_template_without_overwriting(self):
        template = self.root / "template"
        template.mkdir()
        template_project = project_fixture(status="idea")
        template_project["project_id"] = "replace-with-project-id"
        template_project["title"] = "Replace with story title"
        template_project["scenes"] = []
        (template / "project.json").write_text(json.dumps(template_project), encoding="utf-8")
        (template / "corrections.json").write_text(json.dumps({"project_id": "replace-with-project-id", "entries": []}), encoding="utf-8")
        (template / "qa-report.json").write_text(json.dumps({"report_id": "template", "project_id": "replace", "render_id": "replace",
            "created_at": "2026-01-01T00:00:00Z", "checks": [], "overall_status": "incomplete", "full_watch_completed": False,
            "approval": {"approved": False, "approved_by": None, "approved_at": None}}), encoding="utf-8")
        projects = self.root / "projects"
        self.run_cli("init", "new-story", "--title", "New Story", "--projects-dir", projects, "--template-dir", template)
        created = projects / "new-story"
        project = json.loads((created / "project.json").read_text(encoding="utf-8"))
        self.assertEqual(project["project_id"], "new-story")
        self.assertEqual(project["settings"]["runtime_seconds"], 300)
        self.assertEqual(project["scenes"][0]["target_duration_seconds"], 300)
        self.assertTrue((created / "script.md").exists())
        self.run_cli("init", "new-story", "--title", "Overwrite", "--projects-dir", projects, "--template-dir", template, expect=2)

    def test_export_gate_requires_full_watch_and_explicit_qa_approval(self):
        project = self.load_project()
        project["workflow"]["status"] = "review"
        project["render"] = {"render_id": "render-1", "output_ref": "exports/preview.mp4"}
        project["qa_report_ref"] = "qa-report.json"
        self.save_project(project)
        qa = {"overall_status": "pass", "full_watch_completed": False,
              "approval": {"approved": True, "approved_by": "user", "approved_at": "2026-11-24T00:00:00Z"}}
        (self.project_dir / "qa-report.json").write_text(json.dumps(qa), encoding="utf-8")
        self.run_cli("set-stage", self.project_dir, "approved", "--note", "QA approved", expect=2)
        qa["full_watch_completed"] = True
        (self.project_dir / "qa-report.json").write_text(json.dumps(qa), encoding="utf-8")
        self.run_cli("set-stage", self.project_dir, "approved", "--note", "Full review approved")
        self.assertEqual(self.load_project()["workflow"]["status"], "approved")

    def test_qa_reference_cannot_escape_project_directory(self):
        project = self.load_project()
        project["workflow"]["status"] = "review"
        project["render"] = {"output_ref": "preview.mp4"}
        project["qa_report_ref"] = "../outside.json"
        self.save_project(project)
        self.run_cli("set-stage", self.project_dir, "approved", "--note", "QA approved", expect=2)

    def test_published_stage_requires_approval_and_youtube_readback(self):
        project = self.load_project()
        project["workflow"]["status"] = "upload_pending_approval"
        project["publishing"].update({"approved": False, "youtube_video_id": "abc", "youtube_url": "https://youtu.be/abc",
                                      "published_at": "2026-11-24T00:00:00Z"})
        self.save_project(project)
        self.run_cli("set-stage", self.project_dir, "published", "--note", "Upload verified", expect=2)
        project = self.load_project()
        project["publishing"].update({"approved": True, "approved_by": "user", "approved_at": "2026-11-24T00:00:00Z", "visibility": "unlisted"})
        self.save_project(project)
        self.run_cli("set-stage", self.project_dir, "published", "--note", "User-approved upload verified")
        self.assertEqual(self.load_project()["workflow"]["status"], "published")


if __name__ == "__main__":
    unittest.main()
