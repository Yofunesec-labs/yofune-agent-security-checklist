from __future__ import annotations

import os
from typing import Any

import requests

from .base import AdapterResult
from .common import obj_get, parse_json_arguments, to_plain
from ..util import expand_env


class OpenAIResponsesAdapter:
    """OpenAI Responses API adapter.

    The harness intentionally observes function calls instead of executing them. This is
    safer for adversarial verification and lets scenarios assert on proposed side effects.
    """

    name = "openai-responses"

    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        self.model = self.config["model"]
        self.timeout = float(self.config.get("timeout_seconds", 60))
        self.verify_tls = bool(self.config.get("verify_tls", True))
        base_url = self.config.get("base_url", "https://api.openai.com/v1").rstrip("/")
        self.url = self.config.get("url", f"{base_url}/responses")
        api_key = self.config.get("api_key") or os.getenv(self.config.get("api_key_env", "OPENAI_API_KEY"))
        if not api_key:
            raise ValueError("openai-responses adapter requires api_key or OPENAI_API_KEY")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **self.config.get("headers", {}),
        })
        if self.config.get("organization"):
            self.session.headers["OpenAI-Organization"] = self.config["organization"]
        if self.config.get("project"):
            self.session.headers["OpenAI-Project"] = self.config["project"]
        self.previous_response_id: str | None = None

    def reset(self) -> None:
        self.previous_response_id = None

    def close(self) -> None:
        self.session.close()

    def send(self, message: str, *, context: dict[str, Any] | None = None) -> AdapterResult:
        body: dict[str, Any] = {
            "model": self.model,
            "input": message,
            "store": bool(self.config.get("store", False)),
        }
        for key in ("instructions", "tools", "tool_choice", "max_output_tokens", "reasoning", "text", "include"):
            if key in self.config:
                body[key] = self.config[key]
        body.update(self.config.get("request", {}))
        if self.config.get("conversation") and self.previous_response_id:
            body["previous_response_id"] = self.previous_response_id
        if context and self.config.get("context_as_metadata"):
            metadata = dict(body.get("metadata", {}))
            for key, value in context.items():
                if isinstance(value, (str, int, float, bool)):
                    metadata[str(key)] = str(value)[:512]
            body["metadata"] = metadata

        response = self.session.post(self.url, json=body, timeout=self.timeout, verify=self.verify_tls)
        response.raise_for_status()
        raw = response.json()
        if self.config.get("conversation"):
            self.previous_response_id = raw.get("id")

        text = raw.get("output_text", "") or ""
        tool_calls: list[dict[str, Any]] = []
        events: list[dict[str, Any]] = []
        text_parts: list[str] = []
        for item in raw.get("output", []) or []:
            typ = obj_get(item, "type")
            events.append({"type": typ or "output_item", "item": to_plain(item)})
            if typ == "function_call":
                tool_calls.append({
                    "id": obj_get(item, "call_id", obj_get(item, "id")),
                    "name": obj_get(item, "name", ""),
                    "arguments": parse_json_arguments(obj_get(item, "arguments", "{}")),
                })
            elif typ == "message":
                for part in obj_get(item, "content", []) or []:
                    if obj_get(part, "type") == "output_text" and obj_get(part, "text"):
                        text_parts.append(str(obj_get(part, "text")))
        if not text and text_parts:
            text = "\n".join(text_parts)

        return AdapterResult(
            text=str(text),
            tool_calls=tool_calls,
            events=events,
            raw=raw,
            metadata={
                "provider": "openai",
                "api": "responses",
                "response_id": raw.get("id"),
                "model": raw.get("model", self.model),
                "status": raw.get("status"),
                "usage": raw.get("usage"),
                "http_status": response.status_code,
            },
        )
