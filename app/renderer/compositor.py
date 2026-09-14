import math, shutil
from PIL import Image, ImageDraw
from pathlib import Path
from .config import CACHE_DIR, TEMP_DIR, ASSETS_DIR, DEFAULT_TRANSITION_DURATION
from .utils import require_ffmpeg, run, resolve_project_path
from .text_render import render_text_overlay, semantic_position
from .cache import cut_cache_key


def _fit_filter(w,h):
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"


def _camera_filter(preset,w,h,duration,fps):
    d=max(duration,0.001)
    if preset=="STATIC": return "null"
    if preset=="ZOOM_IN_SLOW":
        # FFmpeg zoompan quantizes crop coordinates to the source pixel grid.
        # At 1080x1920 that produces a visible micro-jitter during slow zooms.
        # Supersample 4x first so the same rounding error becomes sub-pixel after
        # the final downsample. Keep the optical center mathematically fixed.
        sw, sh = w*4, h*4
        frames=max(1,int(round(fps*d))-1)
        return (
            f"scale={sw}:{sh}:flags=lanczos,"
            f"zoompan=z='min(1.05,1+0.05*on/{frames})':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s={w}x{h}:fps={fps}"
        )
    if preset=="ZOOM_OUT_SLOW":
        sw, sh = w*4, h*4
        frames=max(1,int(round(fps*d))-1)
        return (
            f"scale={sw}:{sh}:flags=lanczos,"
            f"zoompan=z='max(1.0,1.05-0.05*on/{frames})':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s={w}x{h}:fps={fps}"
        )
    if preset in {"PAN_LEFT","PAN_RIGHT","PAN_UP","PAN_DOWN","SHAKE_LIGHT"}:
        sw=int(w*1.06); sh=int(h*1.06)
        if preset=="PAN_LEFT": x=f"{sw-w}*(1-t/{d})"; y=f"({sh-h})/2"
        elif preset=="PAN_RIGHT": x=f"({sw-w})*t/{d}"; y=f"({sh-h})/2"
        elif preset=="PAN_UP": x=f"({sw-w})/2"; y=f"{sh-h}*(1-t/{d})"
        elif preset=="PAN_DOWN": x=f"({sw-w})/2"; y=f"({sh-h})*t/{d}"
        else:
            x=f"({sw-w})/2 + 4*sin(35*t)"; y=f"({sh-h})/2 + 4*cos(31*t)"
        return f"scale={sw}:{sh},crop={w}:{h}:x='{x}':y='{y}'"
    if preset=="PUNCH_ZOOM":
        return f"zoompan=z='if(lt(on,{int(fps*0.12)}),1+0.10*on/{max(1,int(fps*0.12))},1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={fps}"
    return "null"



def _render_segment(image,duration,out,w,h,fps):
    ffmpeg,_=require_ffmpeg()
    run([ffmpeg,"-y","-loglevel","error","-loop","1","-i",str(image),"-vf",_fit_filter(w,h),"-t",f"{duration:.6f}","-r",str(fps),"-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(out)])


def _concat_segments(parts,out):
    ffmpeg,_=require_ffmpeg()
    lst=out.with_suffix(".txt")
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts),encoding="utf-8")
    run([ffmpeg,"-y","-loglevel","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(out)])
    lst.unlink(missing_ok=True)

def _timeline(cut, project_dir: Path):
    base=resolve_project_path(project_dir,cut["image"])
    actions=sorted([a for a in cut.get("actions",[]) if a.get("type") in {"IMAGE_SWAP","IMAGE_SEQUENCE"}],key=lambda a:float(a.get("at",0)))
    out=[]; pos=0.0; current=base
    for a in actions:
        at=float(a.get("at",0))
        if at>pos+1e-9: out.append({"image":current,"duration":at-pos,"transition":"CUT"})
        if a["type"]=="IMAGE_SWAP":
            img=resolve_project_path(project_dir,a["image"]); dur=float(a["duration"])
            out.append({"image":img,"duration":dur,"transition":a.get("transition","CUT")})
            pos=at+dur
            current=base if a.get("return_to_base",True) else img
        else:
            frames=a["frames"]; repeat=int(a.get("repeat",1)); first=True; last=current
            for _ in range(repeat):
                for f in frames:
                    img=resolve_project_path(project_dir,f["image"]); last=img
                    out.append({"image":img,"duration":float(f["duration"]),"transition":"CUT" if not first else a.get("transition","CUT")})
                    first=False
            pos=at+sum(float(f["duration"]) for f in frames)*repeat
            current=base if a.get("return_to_base",True) else last
    if pos<float(cut["duration"])-1e-9:
        out.append({"image":current,"duration":float(cut["duration"])-pos,"transition":"CUT"})
    return out


def _assemble_segments(parts, entries, out):
    ffmpeg,_=require_ffmpeg()
    if not any(e.get("transition")=="CROSSFADE" for e in entries[1:]):
        return _concat_segments(parts,out)
    inputs=[]
    for p in parts: inputs += ["-i",str(p)]
    filters=[]; current="0:v"; total=float(entries[0]["duration"])
    for i in range(1,len(parts)):
        if entries[i].get("transition")=="CROSSFADE":
            td=min(0.08,float(entries[i-1]["duration"])/2,float(entries[i]["duration"])/2)
            pad=f"apad{i}"; o=f"axf{i}"
            filters.append(f"[{current}]tpad=stop_mode=clone:stop_duration={td:.6f}[{pad}]")
            filters.append(f"[{pad}][{i}:v]xfade=transition=fade:duration={td:.6f}:offset={total:.6f}[{o}]")
            current=o
        else:
            o=f"acat{i}"; filters.append(f"[{current}][{i}:v]concat=n=2:v=1:a=0[{o}]"); current=o
        total += float(entries[i]["duration"])
    run([ffmpeg,"-y","-loglevel","error"]+inputs+["-filter_complex",";".join(filters),"-map",f"[{current}]","-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(out)])


def _cursor_sprite(path: Path, size: int = 64, clicked: bool = False):
    size=max(16,int(size))
    im=Image.new("RGBA",(size,size),(0,0,0,0)); d=ImageDraw.Draw(im)
    # Familiar OS-like arrow cursor: white fill, dark outline. Hotspot is near (2,2).
    pts=[(2,2),(2,int(size*0.72)),(int(size*0.22),int(size*0.55)),(int(size*0.36),int(size*0.86)),(int(size*0.48),int(size*0.80)),(int(size*0.34),int(size*0.50)),(int(size*0.62),int(size*0.50))]
    d.polygon(pts,fill=(255,255,255,255),outline=(50,42,38,255))
    # Pillow polygon outline can be thin; reinforce edges with a line loop.
    d.line(pts+[pts[0]],fill=(50,42,38,255),width=max(2,size//28),joint="curve")
    if clicked:
        r=max(5,size//9); cx=int(size*0.76); cy=int(size*0.22)
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(50,42,38,220),width=max(2,size//32))
    im.save(path)


def _ease_expr(kind: str, p: str):
    # p is clamped 0..1 by caller. Expressions are FFmpeg-compatible.
    if kind=="linear": return p
    if kind=="ease_in": return f"({p})*({p})"
    if kind=="ease_in_out": return f"if(lt({p},0.5),2*({p})*({p}),1-pow(-2*({p})+2,2)/2)"
    return f"1-pow(1-({p}),2)"  # ease_out


def _apply_cursor_actions(cut, work: Path, inputs, chain: str, last: str, input_idx: int):
    stage=0
    for a in sorted(cut.get("actions",[]), key=lambda x: float(x.get("at",0))):
        typ=a.get("type")
        if typ not in {"CURSOR_MOVE","CURSOR_CLICK"}: continue
        start=float(a.get("at",0)); size=int(a.get("size",64)); sprite=work/f"cursor_{stage:02d}.png"
        if typ=="CURSOR_MOVE":
            _cursor_sprite(sprite,size,False)
            p0=a.get("from",a.get("start")); p1=a.get("to",a.get("end")); dur=float(a.get("duration",0.3)); end=start+dur
            # Position is cursor hotspot; overlay x/y use that same top-left hotspot convention.
            prog=f"min(1,max(0,(t-{start:.6f})/{dur:.6f}))"; e=_ease_expr(str(a.get("easing","ease_out")),prog)
            x=f"{float(p0[0]):.6f}+({float(p1[0])-float(p0[0]):.6f})*({e})"
            y=f"{float(p0[1]):.6f}+({float(p1[1])-float(p0[1]):.6f})*({e})"
        else:
            _cursor_sprite(sprite,size,True)
            pos=a.get("position",a.get("at_position",a.get("to"))); dur=float(a.get("duration",0.16)); end=start+dur
            x=f"{float(pos[0]):.6f}"; y=f"{float(pos[1]):.6f}"
        inputs += ["-loop","1","-i",str(sprite)]
        nxt=f"vcur{stage}"
        chain += f";[{last}][{input_idx}:v]overlay=x='{x}':y='{y}':enable='between(t,{start:.6f},{end:.6f})'[{nxt}]"
        last=nxt; input_idx+=1; stage+=1
    return inputs,chain,last,input_idx

def render_cut(cut, edit_path: Path, project: dict, *, force=False):
    project_dir=edit_path.parent.resolve(); cid=str(cut["id"])
    w=int(project["resolution"]["width"]); h=int(project["resolution"]["height"]); fps=int(project["fps"])
    TEMP_DIR.mkdir(parents=True,exist_ok=True); cut_cache_dir=CACHE_DIR/project["id"]/f"cut_{cid}"; cut_cache_dir.mkdir(parents=True,exist_ok=True)
    refs=[resolve_project_path(project_dir,cut["image"])]
    for a in cut.get("actions",[]):
        if a["type"]=="IMAGE_SWAP": refs.append(resolve_project_path(project_dir,a["image"]))
        elif a["type"]=="IMAGE_SEQUENCE": refs += [resolve_project_path(project_dir,f["image"]) for f in a["frames"]]
    key=cut_cache_key(cut,project,refs); cached=cut_cache_dir/f"{key}.mp4"
    if cached.exists() and not force: return cached,True
    work=TEMP_DIR/f"{project['id']}_cut{cid}"; shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True)
    entries=_timeline(cut,project_dir); parts=[]
    for i,e in enumerate(entries):
        p=work/f"seg_{i:03d}.mp4"; _render_segment(e["image"],e["duration"],p,w,h,fps); parts.append(p)
    raw=work/"raw.mp4"; _assemble_segments(parts,entries,raw)
    ffmpeg,_=require_ffmpeg(); inputs=["-i",str(raw)]; chain="[0:v]"+_camera_filter((cut.get("camera") or {}).get("preset","STATIC"),w,h,float(cut["duration"]),fps)+"[v0]"
    last="v0"
    input_idx=1
    inputs,chain,last,input_idx=_apply_cursor_actions(cut,work,inputs,chain,last,input_idx)
    text_stage=0
    for i,t in enumerate(cut.get("text",[])):
        start=float(t.get("appear_at",0)); end=float(t.get("disappear_at") if t.get("disappear_at") is not None else cut["duration"])
        animation=str(t.get("animation","")).upper()
        if animation=="TYPEWRITER":
            full_text=str(t.get("text",""))
            cps=max(1.0,float(t.get("chars_per_second",12.0)))
            # Build the final box first so the bubble never resizes while typing.
            final_ov=work/f"text_{i:02d}_final.png"
            ow,oh=render_text_overlay(t,w,h,final_ov)
            x,y=semantic_position(t,ow,oh,w,h)
            visible_chars=[n for n,ch in enumerate(full_text,1) if ch!="\n"]
            if not visible_chars:
                continue
            # One static overlay per revealed character. This is deterministic and
            # keeps all typography in Pillow rather than relying on FFmpeg fonts.
            reveal_count=0
            for pos,ch in enumerate(full_text,1):
                if ch=="\n":
                    continue
                reveal_count+=1
                partial=dict(t)
                partial["text"]=full_text[:pos]
                partial["width"]=ow; partial["height"]=oh
                ov=work/f"text_{i:02d}_{reveal_count:03d}.png"
                render_text_overlay(partial,w,h,ov)
                inputs += ["-loop","1","-i",str(ov)]
                seg_start=start+(reveal_count-1)/cps
                seg_end=min(end,start+reveal_count/cps)
                # Last revealed state remains until disappear_at/cut end.
                if reveal_count==len(visible_chars): seg_end=end
                if seg_start>=end: break
                nxt=f"vtxt{text_stage}"; text_stage+=1
                chain += f";[{last}][{input_idx}:v]overlay={x}:{y}:enable='between(t,{seg_start:.6f},{seg_end:.6f})'[{nxt}]"
                last=nxt; input_idx+=1
        else:
            ov=work/f"text_{i:02d}.png"; ow,oh=render_text_overlay(t,w,h,ov); x,y=semantic_position(t,ow,oh,w,h)
            inputs += ["-loop","1","-i",str(ov)]
            nxt=f"vtxt{text_stage}"; text_stage+=1
            chain += f";[{last}][{input_idx}:v]overlay={x}:{y}:enable='between(t,{start:.6f},{end:.6f})'[{nxt}]"
            last=nxt; input_idx+=1
    tr=(cut.get("transition_out") or {}).get("type","CUT"); td=float((cut.get("transition_out") or {}).get("duration",DEFAULT_TRANSITION_DURATION)); td=min(td,float(cut["duration"])/2)
    if tr=="FADE_OUT": chain += f";[{last}]fade=t=out:st={max(0,float(cut['duration'])-td):.6f}:d={td:.6f}[vf]"; last="vf"
    elif tr=="FADE_IN": chain += f";[{last}]fade=t=in:st=0:d={td:.6f}[vf]"; last="vf"
    elif tr=="FLASH": chain += f";[{last}]fade=t=out:st={max(0,float(cut['duration'])-td):.6f}:d={td/2:.6f}:color=white,fade=t=in:st={max(0,float(cut['duration'])-td/2):.6f}:d={td/2:.6f}:color=white[vf]"; last="vf"
    cmd=[ffmpeg,"-y","-loglevel","error"]+inputs+["-filter_complex",chain,"-map",f"[{last}]","-t",f"{float(cut['duration']):.6f}","-r",str(fps),"-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(cached)]
    run(cmd)
    return cached,False


def assemble_video(cut_files, cuts, project, out_path):
    ffmpeg,_=require_ffmpeg()
    w=int(project["resolution"]["width"]); h=int(project["resolution"]["height"]); fps=int(project["fps"])

    # Fast path: no crossfades. Keep the existing stream-copy concat behavior.
    if all((c.get("transition_out") or {}).get("type","CUT")!="CROSSFADE" for c in cuts[:-1]):
        lst=out_path.with_suffix(".concat.txt")
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in cut_files),encoding="utf-8")
        run([ffmpeg,"-y","-loglevel","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(out_path)])
        lst.unlink(missing_ok=True)
        return

    # FFmpeg 9 is strict about xfade input frame-rate/timebase metadata. A mixed
    # filter graph (concat -> xfade) can silently convert concat output to AVTB
    # (1/1000000), even when all source MP4s are 1/fps. Therefore transitions
    # are assembled sequentially through real intermediate CFR MP4 files.
    # Every stage is re-encoded with video_track_timescale=fps, so the next
    # xfade always receives two direct 1/fps CFR file inputs.
    work=out_path.parent/f".{out_path.stem}_seq_assembly"
    shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True,exist_ok=True)

    def normalize(src: Path, dst: Path):
        run([ffmpeg,"-y","-loglevel","error","-i",str(src),
             "-vf",f"scale={w}:{h},setsar=1,fps={fps},format=yuv420p",
             "-r",str(fps),"-an","-c:v","libx264","-pix_fmt","yuv420p",
             "-preset","veryfast","-video_track_timescale",str(fps),str(dst)])

    normalized=[]
    for i,p in enumerate(cut_files):
        np=work/f"src_{i:03d}.mp4"
        normalize(Path(p),np)
        normalized.append(np)

    current=normalized[0]
    total=float(cuts[0]["duration"])

    for i in range(1,len(normalized)):
        nxt=normalized[i]
        stage=work/f"stage_{i:03d}.mp4"
        prev_tr=(cuts[i-1].get("transition_out") or {}).get("type","CUT")

        if prev_tr=="CROSSFADE":
            td=float((cuts[i-1].get("transition_out") or {}).get("duration",DEFAULT_TRANSITION_DURATION))
            td=min(td,float(cuts[i-1]["duration"])/2,float(cuts[i]["duration"])/2)
            # Preserve locked total duration: clone-pad outgoing video by td,
            # then start xfade at the exact pre-transition accumulated length.
            filt=(f"[0:v]tpad=stop_mode=clone:stop_duration={td:.6f}[pad];"
                  f"[pad][1:v]xfade=transition=fade:duration={td:.6f}:offset={total:.6f}[out]")
            run([ffmpeg,"-y","-loglevel","error","-i",str(current),"-i",str(nxt),
                 "-filter_complex",filt,"-map","[out]","-r",str(fps),"-an",
                 "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",
                 "-video_track_timescale",str(fps),str(stage)])
        else:
            # Encode the concat result as a real 1/fps CFR file. Do not leave a
            # concat filter output in-memory for a later xfade.
            run([ffmpeg,"-y","-loglevel","error","-i",str(current),"-i",str(nxt),
                 "-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0[out]",
                 "-map","[out]","-r",str(fps),"-an","-c:v","libx264",
                 "-pix_fmt","yuv420p","-preset","veryfast",
                 "-video_track_timescale",str(fps),str(stage)])

        current=stage
        total += float(cuts[i]["duration"])

    shutil.copy2(current,out_path)
    shutil.rmtree(work,ignore_errors=True)
