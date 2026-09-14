from pathlib import Path
from .utils import ffprobe_json
from .errors import MongiRendererError


def validate_output(path: Path, project: dict, expected_duration: float, tolerance=0.18):
    data=ffprobe_json(path); streams=data.get("streams",[])
    v=next((s for s in streams if s.get("codec_type")=="video"),None)
    if not v: raise MongiRendererError("Validation failed: no video stream")
    w=int(project["resolution"]["width"]); h=int(project["resolution"]["height"])
    if int(v.get("width",0))!=w or int(v.get("height",0))!=h: raise MongiRendererError(f"Validation failed: resolution {v.get('width')}x{v.get('height')} != {w}x{h}")
    dur=float(data.get("format",{}).get("duration") or 0)
    if abs(dur-expected_duration)>tolerance: raise MongiRendererError(f"Validation failed: duration {dur:.3f}s != expected {expected_duration:.3f}s")
    fr=v.get("avg_frame_rate","0/1"); num,den=fr.split("/"); fps=float(num)/float(den) if float(den) else 0
    if abs(fps-float(project["fps"]))>0.1: raise MongiRendererError(f"Validation failed: fps {fps:.3f} != {project['fps']}")
    return {"duration":dur,"fps":fps,"resolution":f"{w}x{h}","audio":any(s.get("codec_type")=="audio" for s in streams)}
