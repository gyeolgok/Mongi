from __future__ import annotations
import json, shutil, tempfile, zipfile
from datetime import datetime
from pathlib import Path

IMG_EXT={'.png','.jpg','.jpeg','.webp'}

class PackageError(RuntimeError): pass

def _safe_extract(zf: zipfile.ZipFile, dest: Path):
    root=dest.resolve()
    for info in zf.infolist():
        target=(dest/info.filename).resolve()
        if root not in target.parents and target != root:
            raise PackageError(f'Unsafe ZIP path: {info.filename}')
    zf.extractall(dest)

def inspect_package(zip_path: Path):
    zip_path=zip_path.resolve()
    if not zip_path.exists(): raise PackageError(f'Package not found: {zip_path}')
    if zip_path.suffix.lower()!='.zip': raise PackageError('Input package must be .zip')
    with tempfile.TemporaryDirectory(prefix='mongi_pkg_') as td:
        stage=Path(td)
        with zipfile.ZipFile(zip_path,'r') as zf: _safe_extract(zf,stage)
        edit=stage/'edit.json'
        if not edit.exists(): raise PackageError('ZIP root must contain edit.json')
        approval=stage/'approval.json'
        if not approval.exists(): raise PackageError('ZIP root must contain approval.json')
        try: data=json.loads(edit.read_text(encoding='utf-8-sig'))
        except Exception as e: raise PackageError(f'Invalid edit.json: {e}')
        try: json.loads(approval.read_text(encoding='utf-8-sig'))
        except Exception as e: raise PackageError(f'Invalid approval.json: {e}')
        pid=str(data.get('project',{}).get('id','')).strip()
        if not pid: raise PackageError('edit.json project.id is required')
        return pid,data

def import_package(zip_path: Path, root: Path):
    root=root.resolve(); zip_path=zip_path.resolve()
    pid,_=inspect_package(zip_path)
    projects=root/'projects'; projects.mkdir(parents=True,exist_ok=True)
    target=projects/pid
    history=projects/'_history'/pid
    with tempfile.TemporaryDirectory(prefix='mongi_pkg_') as td:
        stage=Path(td)
        with zipfile.ZipFile(zip_path,'r') as zf: _safe_extract(zf,stage)
        # re-read after extraction
        edit=stage/'edit.json'
        data=json.loads(edit.read_text(encoding='utf-8-sig'))
        # Required package directories may be empty, but paths referenced by edit.json must exist later via preflight.
        (stage/'images').mkdir(exist_ok=True)
        (stage/'actions').mkdir(exist_ok=True)
        if target.exists():
            stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
            backup=history/stamp
            backup.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(target,backup)
        if target.exists(): shutil.rmtree(target)
        shutil.copytree(stage,target)
        pkg_dir=target/'_package'
        pkg_dir.mkdir(exist_ok=True)
        shutil.copy2(zip_path,pkg_dir/zip_path.name)
    return pid,target,target/'edit.json'

def find_inbox_packages(root: Path):
    inbox=root/'inbox'; inbox.mkdir(parents=True,exist_ok=True)
    return sorted(inbox.glob('*.zip'), key=lambda p:(p.stat().st_mtime_ns,p.name))
