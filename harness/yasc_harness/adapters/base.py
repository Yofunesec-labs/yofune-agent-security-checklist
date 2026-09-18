from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol

@dataclass
class AdapterResult:
    text: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    raw: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

class AgentAdapter(Protocol):
    name: str
    def send(self, message: str, *, context: dict[str, Any] | None = None) -> AdapterResult: ...
    def reset(self) -> None: ...
    def close(self) -> None: ...

class MCPAdapter(Protocol):
    name: str
    def initialize(self) -> dict[str, Any]: ...
    def list_tools(self) -> list[dict[str, Any]]: ...
    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]: ...
    def close(self) -> None: ...
