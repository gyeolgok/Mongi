import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from package_import import PackageError, inspect_package


class PackageApprovalTest(unittest.TestCase):
    def test_approval_json_is_required(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "E001.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("edit.json", json.dumps({"project": {"id": "E001"}}))
            with self.assertRaisesRegex(PackageError, "approval.json"):
                inspect_package(archive)


if __name__ == "__main__":
    unittest.main()

