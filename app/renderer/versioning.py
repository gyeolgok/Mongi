from pathlib import Path


def next_output_path(output_dir: Path, project_id: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    first = output_dir / f"{project_id}.mp4"
    if not first.exists():
        return first
    i = 2
    while True:
        p = output_dir / f"{project_id}_v{i}.mp4"
        if not p.exists():
            return p
        i += 1
