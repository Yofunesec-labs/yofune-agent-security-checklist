from __future__ import annotations
import json, os, re
from pathlib import Path
from typing import Any
import yaml

_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
_SECRET_KEYS = re.compile(r"(?i)(authorization|token|secret|password|api[_-]?key|cookie|credential)")
_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+\-/]+=*")


def load_data(path: str | Path) -> Any:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    return json.loads(text) if p.suffix.lower() == ".json" else yaml.safe_load(text)


def write_data(path: str | Path, obj: Any) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == ".json":
        p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        p.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def expand_env(value: Any) -> Any:
    if isinstance(value, str):
        def repl(m: re.Match[str]) -> str:
            key = m.group(1)
            if key not in os.environ:
                raise KeyError(f"environment variable not set: {key}")
            return os.environ[key]
        return _ENV_RE.sub(repl, value)
    if isinstance(value, list): return [expand_env(x) for x in value]
    if isinstance(value, dict): return {k: expand_env(v) for k, v in value.items()}
    return value


def get_path(obj: Any, path: str | None, default: Any = None) -> Any:
    if not path: return obj
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            return default
    return cur


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            out[k] = "[REDACTED]" if _SECRET_KEYS.search(str(k)) else redact(v)
        return out
    if isinstance(value, list): return [redact(x) for x in value]
    if isinstance(value, str): return _BEARER_RE.sub("Bearer [REDACTED]", value)
    return value
