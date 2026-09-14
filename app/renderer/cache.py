import hashlib, json
from pathlib import Path

# Bump whenever renderer behavior changes in a way that can alter cached cut video.
# This prevents old cached cuts from surviving camera/text-renderer hotfixes.
CACHE_SCHEMA = "renderer-1.7.0-edit-lock-1.9"


def file_sig(path: Path):
    st=path.stat()
    return {"path":str(path),"size":st.st_size,"mtime_ns":st.st_mtime_ns}


def cut_cache_key(cut: dict, project: dict, referenced_files):
    payload={
        "cache_schema":CACHE_SCHEMA,
        "cut":cut,
        "project":project,
        "files":[file_sig(Path(p)) for p in referenced_files if Path(p).exists()],
    }
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]
