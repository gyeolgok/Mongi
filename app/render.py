import argparse, os, shutil, sys
from pathlib import Path
from renderer.config import OUTPUT_DIR, CACHE_DIR
from renderer.errors import PreflightError, MongiRendererError
from renderer.preflight import run_preflight
from renderer.utils import load_json, require_ffmpeg
from renderer.versioning import next_output_path
from renderer.compositor import render_cut, assemble_video
from renderer.audio import mix_audio
from renderer.validate import validate_output
from renderer.text_render import choose_font


def open_folder(path: Path):
    try:
        if sys.platform.startswith("win"): os.startfile(str(path))
        elif sys.platform=="darwin": os.system(f'open "{path}"')
        else: os.system(f'xdg-open "{path}" >/dev/null 2>&1 &')
    except Exception: pass


def main():
    ap=argparse.ArgumentParser(description="Mongi Renderer V1")
    ap.add_argument("edit_json",help="Path to edit.json")
    ap.add_argument("--preflight-only",action="store_true")
    ap.add_argument("--force",action="store_true",help="Ignore cut cache")
    ap.add_argument("--open-output",action="store_true",help="Open output folder when done")
    args=ap.parse_args(); edit_path=Path(args.edit_json).resolve()
    print("Mongi Renderer V1.6.9\n")
    try:
        require_ffmpeg(); edit=load_json(edit_path); result=run_preflight(edit,edit_path)
    except PreflightError as e:
        print(f"✗ Preflight failed: {e}"); return 1
    print(f"[{result['project_id']}]\n✓ edit.json\n✓ Assets / structure\n✓ Preflight ({result['cut_count']} cuts, {result['total_duration']:.2f}s)")
    font=choose_font()
    if font: print(f"✓ Font: {font.name}")
    else: print("! WARNING: no project/system Korean font found; Pillow fallback will be used")
    for w in result["warnings"]: print(f"! WARNING: {w}")
    if args.preflight_only: print("\nDONE (preflight only)"); return 0
    project=edit["project"]; out=next_output_path(OUTPUT_DIR,result["project_id"]); tmp_dir=CACHE_DIR/"_final"; tmp_dir.mkdir(parents=True,exist_ok=True)
    visual=tmp_dir/f"{result['project_id']}_visual.mp4"; mixed=tmp_dir/f"{result['project_id']}_mixed.mp4"
    try:
        print("\nRendering...")
        cut_files=[]
        for cut in edit["cuts"]:
            p,cached=render_cut(cut,edit_path,project,force=args.force); cut_files.append(p)
            cut_id = cut.get('id', '?')
            try:
                cut_label = f"{int(cut_id):02d}"
            except (TypeError, ValueError):
                cut_label = str(cut_id)
            print(f"✓ Cut {cut_label} [{'cached' if cached else 'rendered'}]")
        assemble_video(cut_files,edit["cuts"],project,visual); print("✓ Video assembly")
        has_audio=mix_audio(visual,edit,mixed); print("✓ Audio mix" if has_audio else "✓ Audio mix [no audio assets used]")
        shutil.copy2(mixed,out); print("✓ Final encode")
        v=validate_output(out,project,result["total_duration"]); print(f"✓ Validation {v['resolution']} / {v['fps']:.2f}fps / {v['duration']:.2f}s / audio={'yes' if v['audio'] else 'no'}")
    except MongiRendererError as e:
        print(f"\n✗ Render failed: {e}"); return 2
    print(f"\nDONE\n{out}")
    if args.open_output: open_folder(OUTPUT_DIR)
    return 0

if __name__=="__main__": sys.exit(main())
