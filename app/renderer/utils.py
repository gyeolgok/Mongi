import json
import shutil
import subprocess
from pathlib import Path
from .errors import PreflightError, MongiRendererError


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise PreflightError(f"edit.json not found: {path}")
    except json.JSONDecodeError as e:
        raise PreflightError(f"Invalid JSON: line {e.lineno}, column {e.colno}: {e.msg}")


def require_ffmpeg():
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg:
        raise PreflightError("FFmpeg not found on PATH")
    if not ffprobe:
        raise PreflightError("ffprobe not found on PATH")
    return ffmpeg, ffprobe


def resolve_project_path(project_dir: Path, value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (project_dir / p).resolve()


def run(cmd, *, capture=False, check=True):
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE if capture else None)
    if check and p.returncode != 0:
        tail = (p.stderr or "")[-4000:] if capture else ""
        raise MongiRendererError(f"Command failed ({p.returncode}): {' '.join(map(str, cmd))}\n{tail}")
    return p


def ffprobe_json(path: Path):
    _, ffprobe = require_ffmpeg()
    p = run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture=True)
    return json.loads(p.stdout)


def find_asset(folder: Path, name: str):
    matches = sorted(folder.glob(f"{name}.*"))
    return matches[0] if matches else None
