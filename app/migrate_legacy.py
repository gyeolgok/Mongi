from pathlib import Path
import shutil, sys
ROOT=Path(__file__).resolve().parents[1]

def merge(src:Path,dst:Path):
    if not src.exists(): return 0
    n=0
    for p in src.rglob('*'):
        rel=p.relative_to(src); q=dst/rel
        if p.is_dir(): q.mkdir(parents=True,exist_ok=True)
        else:
            q.parent.mkdir(parents=True,exist_ok=True)
            if not q.exists(): shutil.copy2(p,q); n+=1
    return n

def main():
    if len(sys.argv)<2: print('Old folder path required'); return 1
    old=Path(sys.argv[1].strip('"')).resolve()
    if not old.exists(): print(f'Not found: {old}'); return 1
    count=0
    for name in ('assets','projects','output'):
        count+=merge(old/name,ROOT/name)
    print(f'✓ Migrated {count} files. Existing files were preserved.')
    return 0
if __name__=='__main__': raise SystemExit(main())
