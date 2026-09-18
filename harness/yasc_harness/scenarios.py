from __future__ import annotations
from pathlib import Path
from typing import Any
from .util import load_data, expand_env

def load_scenarios(paths: list[str | Path]) -> dict[str,dict[str,Any]]:
    out: dict[str,dict[str,Any]]={}
    for path in paths:
        doc=expand_env(load_data(path))
        items=doc.get('scenarios',[]) if isinstance(doc,dict) else []
        for s in items:
            sid=s['test_id']
            if sid in out: raise ValueError(f'duplicate execution scenario for {sid}')
            out[sid]=s
    return out
