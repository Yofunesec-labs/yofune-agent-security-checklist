from __future__ import annotations

import importlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any


def obj_get(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def to_plain(value: Any, *, depth: int = 0) -> Any:
    """Best-effort conversion of SDK/framework objects to evidence-safe JSON-ish data."""
    if depth > 8:
        return repr(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): to_plain(v, depth=depth + 1) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_plain(v, depth=depth + 1) for v in value]
    if is_dataclass(value):
        return to_plain(asdict(value), depth=depth + 1)
    for method in ("model_dump", "to_dict", "dict"):
        fn = getattr(value, method, None)
        if callable(fn):
            try:
                return to_plain(fn(), depth=depth + 1)
            except Exception:
                pass
    if hasattr(value, "__dict__"):
        try:
            return {
                k: to_plain(v, depth=depth + 1)
                for k, v in vars(value).items()
                if not k.startswith("_")
            }
        except Exception:
            pass
    return repr(value)


def parse_json_arguments(value: Any) -> Any:
    if not isinstance(value, str):
        return to_plain(value)
    try:
        return json.loads(value)
    except Exception:
        return value


def import_symbol(spec: str) -> Any:
    if ":" not in spec:
        raise ValueError("import path must use 'module:object' syntax")
    module_name, symbol_path = spec.split(":", 1)
    module = importlib.import_module(module_name)
    obj: Any = module
    for part in symbol_path.split("."):
        obj = getattr(obj, part)
    return obj


def text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            typ = obj_get(item, "type")
            if typ in {"text", "output_text", "input_text"}:
                text = obj_get(item, "text", "")
                if text:
                    parts.append(str(text))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    if content is None:
        return ""
    return str(content)


def tool_calls_from_message(message: Any) -> list[dict[str, Any]]:
    calls = obj_get(message, "tool_calls", []) or []
    out: list[dict[str, Any]] = []
    for call in calls:
        fn = obj_get(call, "function")
        if fn is not None:
            out.append({
                "id": obj_get(call, "id"),
                "name": obj_get(fn, "name", ""),
                "arguments": parse_json_arguments(obj_get(fn, "arguments", {})),
            })
        else:
            out.append({
                "id": obj_get(call, "id"),
                "name": obj_get(call, "name", ""),
                "arguments": to_plain(obj_get(call, "args", obj_get(call, "input", {}))),
            })
    return out
