from __future__ import annotations

import copy
from typing import Any

from .base import AdapterResult
from .common import import_symbol, obj_get, to_plain
from ..util import expand_env, get_path


class CrewAIAdapter:
    """Adapter for an in-process CrewAI Crew (or factory/CrewBase wrapper)."""

    name = "crewai"

    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        symbol = import_symbol(self.config["crew"])
        obj = symbol() if self.config.get("factory", True) and callable(symbol) else symbol
        if not hasattr(obj, "kickoff") and callable(getattr(obj, "crew", None)):
            obj = obj.crew()
        if not hasattr(obj, "kickoff"):
            raise TypeError("crewai adapter target must expose kickoff(inputs=...)")
        self.crew = obj

    def reset(self) -> None:
        # CrewAI object lifecycle is application-defined. A reset factory can recreate it.
        reset = getattr(self.crew, "reset", None)
        if callable(reset):
            reset()

    def close(self) -> None:
        close = getattr(self.crew, "close", None)
        if callable(close):
            close()

    def send(self, message: str, *, context: dict[str, Any] | None = None) -> AdapterResult:
        inputs = copy.deepcopy(self.config.get("inputs", {}))
        inputs[self.config.get("input_key", "prompt")] = message
        if context and self.config.get("context_key"):
            inputs[self.config["context_key"]] = context
        result = self.crew.kickoff(inputs=inputs)
        plain = to_plain(result)
        response_cfg = self.config.get("response", {})
        text_path = response_cfg.get("text_path")
        text = str(get_path(plain, text_path, "") or "") if text_path else ""
        if not text:
            raw_text = obj_get(result, "raw")
            text = str(raw_text) if raw_text is not None else str(result)
        tool_calls = get_path(plain, response_cfg.get("tool_calls_path"), []) if response_cfg.get("tool_calls_path") else []
        if not isinstance(tool_calls, list):
            tool_calls = []
        tasks_output = obj_get(result, "tasks_output", []) or []
        events = [{"type": "task_output", "task": to_plain(x)} for x in tasks_output]
        return AdapterResult(
            text=text,
            tool_calls=[to_plain(x) for x in tool_calls],
            events=events,
            raw=plain,
            metadata={
                "framework": "crewai",
                "crew": self.config["crew"],
                "tasks": len(tasks_output) if isinstance(tasks_output, list) else None,
            },
        )
