from __future__ import annotations

import os
from typing import Any

import requests

from .base import AdapterResult
from .common import obj_get, to_plain
from ..util import expand_env


class AnthropicMessagesAdapter:
    """Anthropic Messages API adapter that observes client-side tool_use blocks."""

    name = "anthropic-messages"

    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        self.model = self.config["model"]
        self.timeout = float(self.config.get("timeout_seconds", 60))
        self.verify_tls = bool(self.config.get("verify_tls", True))
        base_url = self.config.get("base_url", "https://api.anthropic.com/v1").rstrip("/")
        self.url = self.config.get("url", f"{base_url}/messages")
        api_key = self.config.get("api_key") or os.getenv(self.config.get("api_key_env", "ANTHROPIC_API_KEY"))
        if not api_key:
            raise ValueError("anthropic-messages adapter requires api_key or ANTHROPIC_API_KEY")
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "anthropic-version": self.config.get("anthropic_version", "2023-06-01"),
            "content-type": "application/json",
            **self.config.get("headers", {}),
        })

    def reset(self) -> None:
        return None

    def close(self) -> None:
        self.session.close()

    def send(self, message: str, *, context: dict[str, Any] | None = None) -> AdapterResult:
        body: dict[str, Any] = {
            "model": self.model,
            "max_tokens": int(self.config.get("max_tokens", 1024)),
            "messages": [{"role": "user", "content": message}],
        }
        for key in ("system", "tools", "tool_choice", "temperature", "top_p", "stop_sequences", "thinking"):
            if key in self.config:
                body[key] = self.config[key]
        body.update(self.config.get("request", {}))
        response = self.session.post(self.url, json=body, timeout=self.timeout, verify=self.verify_tls)
        response.raise_for_status()
        raw = response.json()

        text_parts: list[str] = []
        tool_calls: list[dict[str, Any]] = []
        events: list[dict[str, Any]] = []
        for block in raw.get("content", []) or []:
            typ = obj_get(block, "type")
            events.append({"type": typ or "content_block", "block": to_plain(block)})
            if typ == "text" and obj_get(block, "text"):
                text_parts.append(str(obj_get(block, "text")))
            elif typ == "tool_use":
                tool_calls.append({
                    "id": obj_get(block, "id"),
                    "name": obj_get(block, "name", ""),
                    "arguments": to_plain(obj_get(block, "input", {})),
                })

        return AdapterResult(
            text="\n".join(text_parts),
            tool_calls=tool_calls,
            events=events,
            raw=raw,
            metadata={
                "provider": "anthropic",
                "api": "messages",
                "message_id": raw.get("id"),
                "model": raw.get("model", self.model),
                "stop_reason": raw.get("stop_reason"),
                "usage": raw.get("usage"),
                "http_status": response.status_code,
            },
        )
