import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import bootstrap


class BootstrapLockVersionTest(unittest.TestCase):
    def test_consolidated_suffix_is_supported(self):
        path = Path("Mongi-Shorts-Edit-Lock-V1.9-Consolidated.md")
        self.assertEqual(bootstrap._version_key(path), (1, 9))


if __name__ == "__main__":
    unittest.main()

