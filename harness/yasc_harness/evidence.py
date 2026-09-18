from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .util import redact, write_data

def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

class EvidenceCollector:
    """Collects per-run evidence with default secret redaction and SHA-256 integrity metadata."""
    def __init__(self, root: str | Path, run_id: str, *, sensitivity: str='confidential'):
        self.root=Path(root); self.run_id=run_id; self.dir=self.root/run_id; self.dir.mkdir(parents=True,exist_ok=True)
        self.sensitivity=sensitivity; self.events_path=self.dir/'events.jsonl'; self._event_count=0

    def event(self, event_type: str, data: Any) -> None:
        record={'time':utcnow(),'type':event_type,'data':redact(data)}
        with self.events_path.open('a',encoding='utf-8') as f: f.write(json.dumps(record,ensure_ascii=False)+'\n')
        self._event_count+=1

    def artifact_json(self, name: str, obj: Any) -> Path:
        p=self.dir/name
        if p.suffix.lower() not in {'.json','.yaml','.yml'}: p=p.with_suffix('.json')
        write_data(p,redact(obj)); return p

    def artifact_text(self, name: str, text: str) -> Path:
        p=self.dir/name; p.write_text(str(redact(text)),encoding='utf-8'); return p

    def finalize(self, *, case_id: str | None=None, collector: str='YASC Verification Harness') -> dict[str, Any]:
        files=[p for p in sorted(self.dir.rglob('*')) if p.is_file() and p.name!='evidence-manifest.yaml']
        arts=[]
        for i,p in enumerate(files,1):
            arts.append({'artifact_id':f'EV-{i:03d}','type':p.suffix.lstrip('.') or 'file','path':p.relative_to(self.dir).as_posix(),'sha256':sha256(p),'size_bytes':p.stat().st_size,'sensitivity':self.sensitivity,'redaction':'automatic secret-key/bearer-token redaction applied where structured'})
        manifest={'evidence_manifest':{'schema_version':'1.0','manifest_id':f'YEM-{self.run_id}','generated_at':utcnow(),'case_id':case_id or self.run_id,'collector':collector,'hash_algorithm':'sha256','artifacts':arts}}
        write_data(self.dir/'evidence-manifest.yaml',manifest)
        return manifest
