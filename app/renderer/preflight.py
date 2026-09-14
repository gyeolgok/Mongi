from pathlib import Path
from .config import (
    SUPPORTED_CAMERA, SUPPORTED_TRANSITIONS, SUPPORTED_TEXT_TYPES,
    SUPPORTED_ACTION_TYPES, SUPPORTED_ACTION_TRANSITIONS, ASSETS_DIR,
    OFFICIAL_UI_CLICK_SFX,
)
from .errors import PreflightError
from .utils import resolve_project_path, find_asset


LEGACY_SFX_KEYS = {"scroll", "discover", "flop", "success", "pop_soft"}


def _cursor_click_times(cut):
    return [float(a.get("at", 0.0)) for a in cut.get("actions", []) if a.get("type") == "CURSOR_CLICK"]

def _has_synced_official_click_sfx(cut, click_at, tolerance=0.10):
    for item in cut.get("sfx", []):
        if item.get("name") != OFFICIAL_UI_CLICK_SFX:
            continue
        if "at" in item and abs(float(item.get("at", 0.0)) - click_at) <= tolerance:
            return True
    return False


def _num(v, name, min_value=None):
    if not isinstance(v, (int, float)):
        raise PreflightError(f"{name} must be a number")
    if min_value is not None and v < min_value:
        raise PreflightError(f"{name} must be >= {min_value}")


def run_preflight(edit: dict, edit_path: Path):
    warnings=[]
    project_dir=edit_path.parent.resolve()
    project=edit.get("project")
    if not isinstance(project,dict): raise PreflightError("Missing object: project")
    for key in ("id","title","format","resolution","fps"):
        if key not in project: raise PreflightError(f"Missing project.{key}")
    res=project["resolution"]
    if not isinstance(res,dict) or "width" not in res or "height" not in res: raise PreflightError("project.resolution must contain width and height")
    _num(res["width"],"project.resolution.width",1); _num(res["height"],"project.resolution.height",1); _num(project["fps"],"project.fps",1)
    cuts=edit.get("cuts")
    if not isinstance(cuts,list) or not cuts: raise PreflightError("cuts must be a non-empty array")

    # Edit Lock V1.6+ mandatory End Card contract. The final cut must be the
    # explicit End Card and contain one non-empty end_message.
    final_cut = cuts[-1]
    if not isinstance(final_cut, dict) or final_cut.get("type") != "end_card":
        raise PreflightError("Final cut must be type:end_card (Edit Lock V1.6+)")
    end_messages = [t for t in final_cut.get("text", []) if isinstance(t, dict) and t.get("type") == "end_message"]
    if not end_messages:
        raise PreflightError("Final End Card requires an end_message text item")
    if not any(str(t.get("text", "")).strip() for t in end_messages):
        raise PreflightError("Final End Card end_message must not be empty")
    seen=set(); total=0.0
    for idx,cut in enumerate(cuts):
        pfx=f"cuts[{idx}]"
        if not isinstance(cut,dict): raise PreflightError(f"{pfx} must be an object")
        for k in ("id","image","duration"):
            if k not in cut: raise PreflightError(f"Missing {pfx}.{k}")
        if cut["id"] in seen: raise PreflightError(f"Duplicate cut id: {cut['id']}")
        seen.add(cut["id"]); _num(cut["duration"],f"{pfx}.duration",0.01); total+=float(cut["duration"])
        ip=resolve_project_path(project_dir,cut["image"])
        if not ip.exists(): raise PreflightError(f"Missing cut image: {ip}")
        camera=(cut.get("camera") or {}).get("preset","STATIC")
        if camera not in SUPPORTED_CAMERA: raise PreflightError(f"Unsupported camera preset in cut {cut['id']}: {camera}")
        transition=(cut.get("transition_out") or {}).get("type","CUT")
        if transition not in SUPPORTED_TRANSITIONS: raise PreflightError(f"Unsupported transition in cut {cut['id']}: {transition}")
        occupied=[]
        for t in cut.get("text",[]):
            if t.get("type") not in SUPPORTED_TEXT_TYPES: raise PreflightError(f"Unsupported text type in cut {cut['id']}: {t.get('type')}")
            if t.get("type") == "end_message" and cut.get("type") != "end_card":
                raise PreflightError(f"end_message is only allowed in an end_card cut (cut {cut['id']})")
            if cut.get("type") == "end_card" and t.get("type") != "end_message":
                warnings.append(f"Non-end_message text '{t.get('type')}' in End Card cut {cut['id']} — verify this is intentional")
            if not str(t.get("text","")).strip(): warnings.append(f"Empty text item in cut {cut['id']}")
            a=t.get("appear_at",0.0); d=t.get("disappear_at")
            _num(a,f"cut {cut['id']} text.appear_at",0)
            anim=str(t.get("animation","")).upper()
            if anim=="TYPEWRITER":
                _num(t.get("chars_per_second",12),f"cut {cut['id']} text.chars_per_second",1)
            if a>cut["duration"]: raise PreflightError(f"Text appear_at exceeds cut duration in cut {cut['id']}")
            if d is not None:
                _num(d,f"cut {cut['id']} text.disappear_at",0)
                if d>cut["duration"] or d<a: raise PreflightError(f"Invalid text disappear_at in cut {cut['id']}")
        for action in sorted(cut.get("actions",[]), key=lambda x: float(x.get("at",0))):
            typ=action.get("type")
            if typ not in SUPPORTED_ACTION_TYPES: raise PreflightError(f"Unsupported action type in cut {cut['id']}: {typ}")
            at=action.get("at",0.0); _num(at,f"cut {cut['id']} action.at",0)
            if typ=="IMAGE_SWAP":
                if "image" not in action: raise PreflightError(f"IMAGE_SWAP missing image in cut {cut['id']}")
                path=resolve_project_path(project_dir,action["image"])
                if not path.exists(): raise PreflightError(f"Missing action image: {path}")
                dur=float(action.get("duration",0.0)); _num(dur,f"cut {cut['id']} action.duration",0.01)
                tr=action.get("transition","CUT")
                if tr not in SUPPORTED_ACTION_TRANSITIONS: raise PreflightError(f"Unsupported action transition in cut {cut['id']}: {tr}")
                end=at+dur
                timeline_action=True
            elif typ=="IMAGE_SEQUENCE":
                frames=action.get("frames")
                if not isinstance(frames,list) or not frames: raise PreflightError(f"IMAGE_SEQUENCE requires frames in cut {cut['id']}")
                seq=0.0
                for f in frames:
                    if "image" not in f: raise PreflightError(f"Sequence frame missing image in cut {cut['id']}")
                    path=resolve_project_path(project_dir,f["image"])
                    if not path.exists(): raise PreflightError(f"Missing sequence frame: {path}")
                    _num(f.get("duration"),f"cut {cut['id']} frame.duration",0.01); seq+=float(f["duration"])
                repeat=int(action.get("repeat",1))
                if repeat<1: raise PreflightError(f"IMAGE_SEQUENCE repeat must be >= 1 in cut {cut['id']}")
                end=at+seq*repeat
                timeline_action=True
            elif typ=="CURSOR_MOVE":
                start_pos=action.get("from", action.get("start"))
                end_pos=action.get("to", action.get("end"))
                if not (isinstance(start_pos,list) and len(start_pos)==2 and isinstance(end_pos,list) and len(end_pos)==2):
                    raise PreflightError(f"CURSOR_MOVE requires from:[x,y] and to:[x,y] in cut {cut['id']}")
                for label,pos in (("from",start_pos),("to",end_pos)):
                    _num(pos[0],f"cut {cut['id']} CURSOR_MOVE {label}.x",0); _num(pos[1],f"cut {cut['id']} CURSOR_MOVE {label}.y",0)
                dur=float(action.get("duration",0.0)); _num(dur,f"cut {cut['id']} CURSOR_MOVE duration",0.01)
                easing=str(action.get("easing","ease_out"))
                if easing not in {"linear","ease_in","ease_out","ease_in_out"}: raise PreflightError(f"Unsupported CURSOR_MOVE easing in cut {cut['id']}: {easing}")
                _num(action.get("size",64),f"cut {cut['id']} CURSOR_MOVE size",8)
                end=at+dur
                timeline_action=False
            elif typ=="CURSOR_CLICK":
                pos=action.get("position", action.get("at_position", action.get("to")))
                if not (isinstance(pos,list) and len(pos)==2): raise PreflightError(f"CURSOR_CLICK requires position:[x,y] in cut {cut['id']}")
                _num(pos[0],f"cut {cut['id']} CURSOR_CLICK x",0); _num(pos[1],f"cut {cut['id']} CURSOR_CLICK y",0)
                dur=float(action.get("duration",0.16)); _num(dur,f"cut {cut['id']} CURSOR_CLICK duration",0.04)
                _num(action.get("size",64),f"cut {cut['id']} CURSOR_CLICK size",8)
                end=at+dur
                timeline_action=False
            if end>cut["duration"]+1e-9: raise PreflightError(f"Action exceeds cut duration in cut {cut['id']}")
            # Cursor actions are overlays, so they may coexist with image timeline actions.
            if timeline_action:
                for s,e in occupied:
                    if max(s,at) < min(e,end)-1e-9: raise PreflightError(f"Overlapping image actions are not supported in V1 (cut {cut['id']})")
                occupied.append((at,end))
        for sfx in cut.get("sfx",[]):
            name=sfx.get("name")
            if not name: raise PreflightError(f"SFX missing name in cut {cut['id']}")
            if not find_asset(ASSETS_DIR/"sfx",name):
                if name in LEGACY_SFX_KEYS:
                    warnings.append(f"LEGACY SFX KEY '{name}' (cut {cut['id']}) — no Audio V1 asset; skipped. Remap in production package.")
                else:
                    warnings.append(f"Missing SFX asset for '{name}' (cut {cut['id']}) — skipped")
            if "offset" in sfx:
                _num(sfx["offset"],f"cut {cut['id']} sfx.offset")
            if "source_start" in sfx:
                _num(sfx["source_start"],f"cut {cut['id']} sfx.source_start",0)
            if "at" in sfx:
                _num(sfx["at"],f"cut {cut['id']} sfx.at",0)
                if sfx["at"]>cut["duration"]: raise PreflightError(f"SFX at exceeds cut duration in cut {cut['id']}")
            elif "start" in sfx:
                _num(sfx["start"],f"cut {cut['id']} sfx.start",0); _num(sfx.get("end"),f"cut {cut['id']} sfx.end",0)
                if sfx["end"]>cut["duration"] or sfx["end"]<=sfx["start"]: raise PreflightError(f"Invalid SFX interval in cut {cut['id']}")
            else: raise PreflightError(f"SFX requires at or start/end in cut {cut['id']}")
        for click_at in _cursor_click_times(cut):
            if not _has_synced_official_click_sfx(cut, click_at):
                warnings.append(
                    f"CURSOR_CLICK at {click_at:.2f}s in cut {cut['id']} has no synced '{OFFICIAL_UI_CLICK_SFX}' timeline SFX (±0.10s). "
                    "If an audible click is intended, add the official Audio V1 key; do not substitute an alias."
                )
    for bgm in edit.get("bgm",[]):
        name=bgm.get("name")
        if not name: raise PreflightError("BGM item missing name")
        if not find_asset(ASSETS_DIR/"bgm",name): warnings.append(f"Missing BGM asset for '{name}' — skipped")
    return {"project_id":project["id"],"total_duration":total,"cut_count":len(cuts),"warnings":warnings}
