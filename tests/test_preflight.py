import json
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from renderer.errors import PreflightError
from renderer.preflight import run_preflight


class PreflightV19Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "images").mkdir()
        (self.root / "images" / "cut01.png").write_bytes(b"test")
        (self.root / "images" / "end_card.png").write_bytes(b"test")
        self.edit_path = self.root / "edit.json"
        self.edit = {
            "project": {
                "id": "E001",
                "title": "test",
                "format": "shorts",
                "resolution": {"width": 1080, "height": 1920},
                "fps": 30,
            },
            "cuts": [
                {
                    "id": 1,
                    "image": "images/cut01.png",
                    "duration": 1.0,
                    "camera": {"preset": "STATIC"},
                    "text": [],
                    "actions": [],
                    "sfx": [],
                },
                {
                    "id": "end_card",
                    "type": "end_card",
                    "image": "images/end_card.png",
                    "duration": 2.0,
                    "camera": {"preset": "STATIC"},
                    "text": [{"type": "end_message", "text": "오늘은 여기까지.", "animation": "STATIC"}],
                    "actions": [],
                    "sfx": [],
                    "transition_out": {"type": "FADE_OUT"},
                },
            ],
        }
        self.approval = {
            "schema_version": 1,
            "episode_id": "E001",
            "approvals": {
                "script": {"status": "APPROVED", "reviewer": "CONTINUITY", "reviewed_at": "2026-09-14T18:00:00+09:00"},
                "assets": {"status": "APPROVED", "reviewer": "CONTINUITY", "reviewed_at": "2026-09-14T20:00:00+09:00"},
            },
        }
        self._write()

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self):
        self.edit_path.write_text(json.dumps(self.edit), encoding="utf-8")
        (self.root / "approval.json").write_text(json.dumps(self.approval), encoding="utf-8")

    def test_approved_package_passes(self):
        result = run_preflight(self.edit, self.edit_path)
        self.assertEqual(result["project_id"], "E001")
        self.assertEqual(result["cut_count"], 2)

    def test_unapproved_script_is_fatal(self):
        self.approval["approvals"]["script"]["status"] = "REJECTED"
        self._write()
        with self.assertRaisesRegex(PreflightError, "SCRIPT_APPROVED"):
            run_preflight(self.edit, self.edit_path)

    def test_dialogue_post_compositing_is_fatal(self):
        self.edit["cuts"][0]["text"] = [{"type": "dialogue", "text": "안 돼"}]
        with self.assertRaisesRegex(PreflightError, "baked into the source image"):
            run_preflight(self.edit, self.edit_path)

    def test_typewriter_is_fatal(self):
        self.edit["cuts"][0]["text"] = [{"type": "caption", "text": "test", "animation": "TYPEWRITER"}]
        with self.assertRaisesRegex(PreflightError, "TYPEWRITER is retired"):
            run_preflight(self.edit, self.edit_path)

    def test_end_card_must_be_static(self):
        self.edit["cuts"][-1]["camera"] = {"preset": "ZOOM_IN_SLOW"}
        with self.assertRaisesRegex(PreflightError, "End Card camera must be STATIC"):
            run_preflight(self.edit, self.edit_path)


if __name__ == "__main__":
    unittest.main()

