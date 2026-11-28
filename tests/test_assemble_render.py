import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.assemble_render import (
    assemble,
    build_ffmpeg_command,
    load_plan,
    prepare_inputs,
)
from scripts.inspect_render import probe_media


class AssemblyPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.manifest = self.base / "project.json"
        self.manifest.write_text(json.dumps({
            "project_id": "test-film",
            "title": "Test Film",
            "settings": {"runtime_seconds": 4, "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_rate": 24}
        }), encoding="utf-8")
        self.clip_a = self.base / "clip a.mp4"
        self.clip_b = self.base / "clip-b.mp4"
        self.audio = self.base / "voice.wav"
        for path in (self.clip_a, self.clip_b, self.audio):
            path.write_bytes(b"test")
        self.plan_path = self.base / "plan.json"
        self.plan = {
            "project_manifest": "project.json",
            "output": "out.mp4",
            "clips": [
                {"path": "clip a.mp4", "duration_seconds": 2},
                {"path": "clip-b.mp4", "duration_seconds": 2}
            ],
            "audio_tracks": [
                {"path": "voice.wav", "gain": 1, "start_seconds": 0.25, "label": "narration"}
            ]
        }
        self.plan_path.write_text(json.dumps(self.plan), encoding="utf-8")

    def test_schema_validates_plan_shape(self):
        plan, base = load_plan(self.plan_path)
        self.assertEqual(plan["clips"][0]["path"], "clip a.mp4")
        self.assertEqual(base, self.base.resolve())

    @patch("scripts.assemble_render.probe_media")
    def test_prepares_paths_duration_and_target_settings(self, probe):
        probe.return_value = {"video_stream": {"codec_type": "video"}, "duration_seconds": 3.0}
        prepared = prepare_inputs(self.plan, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=False, allow_silent_preview=False, duration_tolerance=0.01)
        self.assertEqual(prepared["duration"], 4)
        self.assertEqual(prepared["width"], 1920)
        self.assertEqual(prepared["height"], 1080)
        self.assertEqual(prepared["audio_tracks"][0]["start"], 0.25)

    @patch("scripts.assemble_render.probe_media")
    def test_short_assembly_requires_explicit_preview_flag(self, probe):
        probe.return_value = {"video_stream": {"codec_type": "video"}, "duration_seconds": 3.0}
        short = {**self.plan, "clips": [{"path": "clip a.mp4", "duration_seconds": 2}]}
        with self.assertRaisesRegex(ValueError, "allow-partial-preview"):
            prepare_inputs(short, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=False, allow_silent_preview=False, duration_tolerance=0.01)
        prepared = prepare_inputs(short, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=True, allow_silent_preview=False, duration_tolerance=0.01)
        self.assertEqual(prepared["duration"], 2)

    @patch("scripts.assemble_render.probe_media")
    def test_silent_output_requires_explicit_preview_flag(self, probe):
        probe.return_value = {"video_stream": {"codec_type": "video"}, "duration_seconds": 3.0}
        silent = {**self.plan, "audio_tracks": []}
        with self.assertRaisesRegex(ValueError, "allow-silent-preview"):
            prepare_inputs(silent, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=False, allow_silent_preview=False, duration_tolerance=0.01)
        prepared = prepare_inputs(silent, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=False, allow_silent_preview=True, duration_tolerance=0.01)
        self.assertEqual(prepared["audio_tracks"], [])

    @patch("scripts.assemble_render.probe_media")
    def test_trim_cannot_exceed_source_clip(self, probe):
        probe.return_value = {"video_stream": {"codec_type": "video"}, "duration_seconds": 3.0}
        bad = {**self.plan, "clips": [{"path": "clip a.mp4", "start_seconds": 2, "duration_seconds": 2}, {"path": "clip-b.mp4", "duration_seconds": 2}]}
        with self.assertRaisesRegex(ValueError, "only 1s remaining"):
            prepare_inputs(bad, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=True, allow_silent_preview=False, duration_tolerance=0.01)

    @patch("scripts.assemble_render.probe_media")
    def test_builds_safe_concat_and_audio_command(self, probe):
        probe.return_value = {"video_stream": {"codec_type": "video"}, "duration_seconds": 3.0}
        prepared = prepare_inputs(self.plan, self.base, self.base / "out.mp4", ffprobe="ffprobe", allow_partial_preview=False, allow_silent_preview=False, duration_tolerance=0.01)
        command = build_ffmpeg_command(prepared, self.base / "out.mp4", "/usr/bin/ffmpeg")
        rendered = " ".join(command)
        self.assertIn("concat=n=2:v=1:a=0", rendered)
        self.assertIn("adelay=delays=250:all=1", rendered)
        self.assertIn("anull[aout]", rendered)
        self.assertIn("-n", command)
        self.assertIn("libx264", command)
        self.assertIn("-map", command)

    def test_existing_output_is_never_overwritten(self):
        output = self.base / "out.mp4"
        output.write_bytes(b"keep")
        with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
            assemble(self.plan_path, output, dry_run=True)
        self.assertEqual(output.read_bytes(), b"keep")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/FFprobe not installed")
class RealFfmpegSmokeTests(unittest.TestCase):
    def test_assembles_real_clips_and_mixes_voice_and_looped_music(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            for name, color in (("one.mp4", "red"), ("two.mp4", "blue")):
                path = base / name
                subprocess.run([
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", f"color=c={color}:s=640x360:r=24:d=2", "-an", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-y", str(path)
                ], check=True, capture_output=True)
            audio = base / "voice.wav"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                "-i", "sine=frequency=440:duration=4", "-c:a", "pcm_s16le", "-y", str(audio)
            ], check=True, capture_output=True)
            music = base / "music.wav"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                "-i", "sine=frequency=220:duration=1", "-c:a", "pcm_s16le", "-y", str(music)
            ], check=True, capture_output=True)
            manifest = base / "project.json"
            manifest.write_text(json.dumps({
                "project_id": "smoke-film",
                "title": "Smoke Test Film",
                "settings": {"runtime_seconds": 4, "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_rate": 24}
            }), encoding="utf-8")
            plan = base / "plan.json"
            plan.write_text(json.dumps({
                "project_manifest": "project.json",
                "clips": [{"path": "one.mp4"}, {"path": "two.mp4"}],
                "audio_tracks": [
                    {"path": "voice.wav", "gain": 0.8},
                    {"path": "music.wav", "gain": 0.08, "start_seconds": 0.25, "loop": True}
                ]
            }), encoding="utf-8")
            output = base / "assembled.mp4"
            code, message = assemble(plan, output)
            self.assertEqual(code, 0, message)
            media = probe_media(output)
            self.assertEqual(media["width"], 1920)
            self.assertEqual(media["height"], 1080)
            self.assertGreater(media["audio_stream_count"], 0)
            self.assertAlmostEqual(media["duration_seconds"], 4, delta=0.15)
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
