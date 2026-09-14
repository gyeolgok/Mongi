from __future__ import annotations
import subprocess, sys, shutil
from pathlib import Path
from package_import import find_inbox_packages, import_package, PackageError

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'app'

def main():
    packages=find_inbox_packages(ROOT)
    if not packages:
        print('Mongi Renderer V1.7.0')
        print('\n✗ inbox/에 에피소드 ZIP이 없습니다.')
        print('  제작실에서 받은 E01_assets.zip 같은 파일을 inbox/에 넣고 다시 실행하세요.')
        return 1
    failed=0
    for pkg in packages:
        print(f'\n=== {pkg.name} ===')
        try:
            pid,project_dir,edit=import_package(pkg,ROOT)
            print(f'✓ Package imported -> projects/{pid}')
            cmd=[sys.executable,str(APP/'render.py'),str(edit),'--open-output']
            rc=subprocess.call(cmd,cwd=str(ROOT))
            if rc!=0:
                failed+=1; print(f'✗ Render failed: {pkg.name}')
                continue
            done=ROOT/'inbox'/'processed'; done.mkdir(parents=True,exist_ok=True)
            dst=done/pkg.name
            if dst.exists():
                stem,suf=pkg.stem,pkg.suffix; i=2
                while (done/f'{stem}_v{i}{suf}').exists(): i+=1
                dst=done/f'{stem}_v{i}{suf}'
            shutil.move(str(pkg),str(dst))
            print(f'✓ Package archived -> inbox/processed/{dst.name}')
        except PackageError as e:
            failed+=1; print(f'✗ Package error: {e}')
    return 2 if failed else 0

if __name__=='__main__': raise SystemExit(main())
