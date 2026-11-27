import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess

from scripts.inspect_render import build_report, probe_media


ROOT = Path(__file__).resolve().parents[1]
PROJECT = {
    "project_id": "clever-little-rabbits",
    "settings": {"runtime_seconds": 300, "resolution": "1920x1080", "aspect_ratio": "16:9"},
}


class RenderInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.video = Path(self.temp.name) / "preview.mp4"
        self.video.write_bytes(b"fake video bytes")

    def ffprobe_json(self, *, duration="300.0", width=1920, height=1080, audio=True, format_name="mov,mp4,m4a,3gp,3g2,mj2"):
        streams = [{
            "index": 0,
            "codec_type": "video",
            "codec_name": "h264",
            "width": width,
            "height": height,
            "avg_frame_rate": "24/1",
            "r_frame_rate": "24/1",
            "duration": duration,
        }]
        if audio:
            streams.append({"index": 1, "codec_type": "audio", "codec_name": "aac"})
        return {"format": {"duration": duration, "format_name": format_name}, "streams": streams}

    @patch("scripts.inspect_render.shutil.which", return_value="/usr/bin/ffprobe")
    @patch("scripts.inspect_render.subprocess.run")
    def test_probe_and_report_pass_technical_checks_but_never_approve(self, run, _which):
        run.return_value = CompletedProcess([], 0, json.dumps(self.ffprobe_json()), "")
        media = probe_media(self.video)
        report = build_report(PROJECT, self.video, media, "a" * 64)
        self.assertEqual(report["overall_status"], "incomplete")
        self.assertFalse(report["full_watch_completed"])
        self.assertFalse(report["approval"]["approved"])
        self.assertTrue(all(c["result"] == "pass" for c in report["checks"]))
        self.assertEqual(report["export"]["resolution"], "1920x1080")
        self.assertEqual(report["export"]["aspect_ratio"], "16:9")
        import jsonschema
        qa_schema = json.loads((ROOT / "schemas" / "qa-report.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(report, qa_schema)

    @patch("scripts.inspect_render.shutil.which", return_value="/usr/bin/ffprobe")
    @patch("scripts.inspect_render.subprocess.run")
    def test_wrong_resolution_and_runtime_fail(self, run, _which):
        run.return_value = CompletedProcess([], 0, json.dumps(self.ffprobe_json(duration="250", width=1280, height=720)), "")
        media = probe_media(self.video)
        report = build_report(PROJECT, self.video, media, "b" * 64)
        failed = {c["check_id"] for c in report["checks"] if c["result"] == "fail"}
        self.assertEqual(report["overall_status"], "fail")
        self.assertIn("runtime", failed)
        self.assertIn("resolution", failed)

    @patch("scripts.inspect_render.shutil.which", return_value="/usr/bin/ffprobe")
    @patch("scripts.inspect_render.subprocess.run")
    def test_missing_audio_fails_by_default(self, run, _which):
        run.return_value = CompletedProcess([], 0, json.dumps(self.ffprobe_json(audio=False)), "")
        media = probe_media(self.video)
        report = build_report(PROJECT, self.video, media, "c" * 64)
        self.assertIn("audio_stream_present", {c["check_id"] for c in report["checks"] if c["result"] == "fail"})

    @patch("scripts.inspect_render.shutil.which", return_value=None)
    def test_missing_ffprobe_has_actionable_error(self, _which):
        with self.assertRaisesRegex(RuntimeError, "Install FFmpeg"):
            probe_media(self.video)

    @patch("scripts.inspect_render.shutil.which", return_value="/usr/bin/ffprobe")
    @patch("scripts.inspect_render.subprocess.run")
    def test_invalid_ffprobe_json_is_rejected(self, run, _which):
        run.return_value = CompletedProcess([], 0, "not-json", "")
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            probe_media(self.video)

    def test_missing_video_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            probe_media(Path(self.temp.name) / "missing.mp4")


if __name__ == "__main__":
    unittest.main()
