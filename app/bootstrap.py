from __future__ import annotations
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "app" / "requirements.txt"
DOCS = ROOT / "docs"
LOCK_GLOB = "Mongi-Shorts-Edit-Lock-V*.md"
LOCK_RE = re.compile(
    r"^Mongi-Shorts-Edit-Lock-V(\d+(?:\.\d+)*)(?:-[^.]+)?\.md$",
    re.IGNORECASE,
)


def _install_requirements() -> bool:
    print("! Missing Python dependency: Pillow")
    print("  Installing app/requirements.txt ...")
    try:
        rc = subprocess.call([sys.executable, "-m", "pip", "install", "-r", str(REQ)])
        return rc == 0
    except Exception as exc:
        print(f"✗ Dependency install failed: {exc}")
        return False


def _version_key(path: Path):
    m = LOCK_RE.match(path.name)
    if not m:
        return None
    try:
        return tuple(int(x) for x in m.group(1).split("."))
    except ValueError:
        return None


def _find_latest_edit_lock():
    valid = []
    for path in DOCS.glob(LOCK_GLOB):
        key = _version_key(path)
        if key is not None:
            valid.append((key, path))
    if not valid:
        return None, []
    valid.sort(key=lambda item: item[0])
    return valid[-1][1], [p for _, p in valid]


def main() -> int:
    print("Mongi Renderer V1.7.0 - Startup Check")

    if importlib.util.find_spec("PIL") is None:
        if not _install_requirements() or importlib.util.find_spec("PIL") is None:
            print("✗ Pillow is still unavailable. Run setup_windows.bat once.")
            return 2
    print("✓ Python dependency: Pillow")

    missing_tools = [name for name in ("ffmpeg", "ffprobe") if shutil.which(name) is None]
    if missing_tools:
        print(f"✗ Missing external tool(s): {', '.join(missing_tools)}")
        print("  Run setup_windows.bat once, then reopen render.bat.")
        return 3
    print("✓ FFmpeg / ffprobe")

    latest_lock, locks = _find_latest_edit_lock()
    if latest_lock is None:
        print(f"✗ No Mongi Shorts Edit Lock found in docs/ ({LOCK_GLOB})")
        return 4

    version = LOCK_RE.match(latest_lock.name).group(1)
    print(f"✓ Local Edit Lock: V{version} ({latest_lock.name})")
    if len(locks) > 1:
        older = [p.name for p in locks if p != latest_lock]
        print("! INFO: older Edit Lock copies ignored: " + ", ".join(older))

    required_audio = [
        ROOT / "assets" / "bgm_segments.json",
        ROOT / "assets" / "bgm_sources.json",
        ROOT / "docs" / "AUDIO_LIBRARY.md",
    ]
    missing_audio = [str(p.relative_to(ROOT)) for p in required_audio if not p.exists()]
    if missing_audio:
        print("✗ Audio V1 metadata missing: " + ", ".join(missing_audio))
        return 5
    print("✓ Audio V1 metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
