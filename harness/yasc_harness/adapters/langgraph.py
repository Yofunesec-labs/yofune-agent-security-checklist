from __future__ import annotations

import copy
import uuid
from typing import Any

from .base import AdapterResult
from .common import import_symbol, obj_get, text_from_content, tool_calls_from_message, to_plain
from ..util import expand_env, get_path


class LangGraphAdapter:
    """Adapter for an in-process LangGraph/LangChain runnable exposing .invoke()."""

    name = "langgraph"

    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        symbol = import_symbol(self.config["graph"])
        if self.config.get("factory", False):
            symbol = symbol()
        self.graph = symbol
        if not hasattr(self.graph, "invoke"):
            raise TypeError("langgraph adapter target must expose invoke(input, config=...)")
        self.base_invoke_config = copy.deepcopy(self.config.get("invoke_config", {}))
        self.thread_id_mode = self.config.get("thread_id")
        self.invoke_config = copy.deepcopy(self.base_invoke_config)
        self.reset()

    def reset(self) -> None:
        self.invoke_config = copy.deepcopy(self.base_invoke_config)
        if self.thread_id_mode == "auto":
            self.invoke_config.setdefault("configurable", {})["thread_id"] = f"yasc-{uuid.uuid4()}"
        elif self.thread_id_mode:
            self.invoke_config.setdefault("configurable", {})["thread_id"] = str(self.thread_id_mode)

    def close(self) -> None:
        close = getattr(self.graph, "close", None)
        if callable(close):
            close()

    def _input(self, message: str, context: dict[str, Any] | None) -> Any:
        mode = self.config.get("input_mode", "messages")
        if mode == "string":
            return message
        if mode == "mapping":
            data = copy.deepcopy(self.config.get("input", {}))
            data[self.config.get("input_field", "message")] = message
            if context and self.config.get("context_field"):
                data[self.config["context_field"]] = context
            return data
        key = self.config.get("messages_field", "messages")
        return {key: [{"role": "user", "content": message}]}

    def send(self, message: str, *, context: dict[str, Any] | None = None) -> AdapterResult:
        result = self.graph.invoke(self._input(message, context), config=self.invoke_config or None)
        plain = to_plain(result)
        output_cfg = self.config.get("response", {})
        text = ""
        tool_calls: list[dict[str, Any]] = []
        events: list[dict[str, Any]] = []

        text_path = output_cfg.get("text_path")
        if text_path:
            text = str(get_path(plain, text_path, "") or "")
        messages_path = output_cfg.get("messages_path", self.config.get("messages_field", "messages"))
        messages = get_path(result if isinstance(result, dict) else plain, messages_path, [])
        if isinstance(messages, list) and messages:
            last = messages[-1]
            if not text:
                text = text_from_content(obj_get(last, "content", ""))
            tool_calls = tool_calls_from_message(last)
            events = [{"type": "message", "message": to_plain(m)} for m in messages]
        if not text and isinstance(result, str):
            text = result

        return AdapterResult(
            text=text,
            tool_calls=tool_calls,
            events=events,
            raw=plain,
            metadata={
                "framework": "langgraph",
                "graph": self.config["graph"],
                "thread_id": get_path(self.invoke_config, "configurable.thread_id"),
            },
        )
