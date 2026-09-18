from __future__ import annotations
from typing import Any
import requests
from .base import AdapterResult
from ..util import expand_env, get_path

class HTTPAgentAdapter:
    """Framework-neutral JSON-over-HTTP adapter.

    The target config defines where input text is placed and where response text,
    tool calls, and optional events can be found. This keeps the harness from
    hard-coding one agent SDK.
    """
    name = "http-agent"
    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        self.url = self.config["url"]
        self.timeout = float(self.config.get("timeout_seconds", 30))
        self.verify_tls = bool(self.config.get("verify_tls", True))
        self.session = requests.Session()
        self.session.headers.update(self.config.get("headers", {}))

    def reset(self) -> None:
        reset_url = self.config.get("reset_url")
        if reset_url:
            self.session.post(reset_url, timeout=self.timeout, verify=self.verify_tls)

    def close(self) -> None: self.session.close()

    def send(self, message: str, *, context: dict[str, Any] | None = None) -> AdapterResult:
        req_cfg = self.config.get("request", {})
        body = dict(req_cfg.get("static", {}))
        body[req_cfg.get("input_field", "message")] = message
        if context and req_cfg.get("context_field"):
            body[req_cfg["context_field"]] = context
        r = self.session.request(
            self.config.get("method", "POST"), self.url,
            json=body, timeout=self.timeout, verify=self.verify_tls,
        )
        r.raise_for_status()
        try: raw = r.json()
        except ValueError: raw = {"text": r.text}
        resp = self.config.get("response", {})
        text = get_path(raw, resp.get("text_path", "text"), "") or ""
        tool_calls = get_path(raw, resp.get("tool_calls_path", "tool_calls"), []) or []
        events = get_path(raw, resp.get("events_path", "events"), []) or []
        return AdapterResult(text=str(text), tool_calls=list(tool_calls) if isinstance(tool_calls,list) else [], events=list(events) if isinstance(events,list) else [], raw=raw, metadata={"http_status":r.status_code})
