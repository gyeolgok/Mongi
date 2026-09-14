from pathlib import Path
from .config import ASSETS_DIR
from .utils import require_ffmpeg, run, find_asset


def _global_sfx(edit):
    events=[]; base=0.0
    for cut in edit["cuts"]:
        for s in cut.get("sfx",[]):
            e=dict(s)
            offset=float(e.get("offset",0.0))
            if "at" in e:
                e["global_start"]=max(0.0,base+float(e["at"])+offset); e["global_end"]=None
            else:
                e["global_start"]=max(0.0,base+float(e["start"])+offset)
                e["global_end"]=max(e["global_start"],base+float(e["end"])+offset)
            events.append(e)
        base += float(cut["duration"])
    return events


def mix_audio(video_in: Path, edit: dict, out_path: Path):
    total=sum(float(c["duration"]) for c in edit["cuts"]); ffmpeg,_=require_ffmpeg(); inputs=["-i",str(video_in)]; filters=[]; bg_labels=[]; sx_labels=[]; idx=1; duck=[]
    for b in edit.get("bgm",[]):
        p=find_asset(ASSETS_DIR/"bgm",b["name"])
        if not p: continue
        start=float(b.get("start",0)); end=float(b.get("end",total)); source_start=float(b.get("source_start",0)); vol=float(b.get("volume",1.0)); fi=float(b.get("fade_in",0)); fo=float(b.get("fade_out",0)); dur=max(0,end-start)
        inputs += ["-stream_loop","-1","-i",str(p)]
        chain=f"[{idx}:a]atrim=start={source_start:.6f}:end={source_start+dur:.6f},asetpts=PTS-STARTPTS,volume={vol}"
        if fi>0: chain += f",afade=t=in:st=0:d={min(fi,dur):.6f}"
        if fo>0 and dur>0: chain += f",afade=t=out:st={max(0,dur-fo):.6f}:d={min(fo,dur):.6f}"
        if start>0: chain += f",adelay={int(round(start*1000))}|{int(round(start*1000))}"
        lab=f"bg{idx}"; filters.append(chain+f"[{lab}]"); bg_labels.append(lab); idx+=1
    sfx_events=_global_sfx(edit)
    for s in sfx_events:
        p=find_asset(ASSETS_DIR/"sfx",s["name"])
        if not p: continue
        start=float(s["global_start"]); vol=float(s.get("volume",1.0)); source_start=float(s.get("source_start",0.0)); inputs += ["-i",str(p)]
        if s.get("global_end") is not None:
            dur=max(0.0,float(s["global_end"])-start)
            chain=f"[{idx}:a]atrim=start={source_start:.6f}:end={source_start+dur:.6f},asetpts=PTS-STARTPTS,volume={vol}"
        else:
            chain=f"[{idx}:a]atrim=start={source_start:.6f},asetpts=PTS-STARTPTS,volume={vol}"
        # Millisecond-accurate delay; negative semantic timing is represented with
        # `offset` and clamped only at the beginning of the whole video.
        delay_ms=max(0,int(round(start*1000)))
        chain += f",adelay={delay_ms}|{delay_ms}"
        lab=f"sx{idx}"; filters.append(chain+f"[{lab}]"); sx_labels.append(lab)
        if s.get("duck_bgm"): duck.append((max(0,start-0.06),min(total,start+0.52)))
        idx+=1
    mix_labels=[]
    if bg_labels:
        joined="".join(f"[{x}]" for x in bg_labels); filters.append(f"{joined}amix=inputs={len(bg_labels)}:duration=longest:normalize=0[bgmix]"); bg="bgmix"
        if duck:
            expr="1"
            for a,b in duck: expr += f"*if(between(t,{a:.6f},{b:.6f}),0.42,1)"
            filters.append(f"[bgmix]volume='{expr}':eval=frame[bgduck]"); bg="bgduck"
        mix_labels.append(bg)
    mix_labels += sx_labels
    if not mix_labels:
        run([ffmpeg,"-y","-loglevel","error","-i",str(video_in),"-c:v","copy","-an",str(out_path)]); return False
    joined="".join(f"[{x}]" for x in mix_labels); filters.append(f"{joined}amix=inputs={len(mix_labels)}:duration=longest:normalize=0,atrim=0:{total:.6f}[finala]")
    run([ffmpeg,"-y","-loglevel","error"]+inputs+["-filter_complex",";".join(filters),"-map","0:v:0","-map","[finala]","-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{total:.6f}",str(out_path)]); return True
