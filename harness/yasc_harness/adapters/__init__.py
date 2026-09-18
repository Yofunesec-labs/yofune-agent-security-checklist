from __future__ import annotations
from typing import Any
from .mock import MockAgentAdapter
from .http_agent import HTTPAgentAdapter
from .openai_responses import OpenAIResponsesAdapter
from .anthropic_messages import AnthropicMessagesAdapter
from .langgraph import LangGraphAdapter
from .crewai import CrewAIAdapter
from .mcp import make_mcp_adapter


def make_agent_adapter(config: dict[str, Any]):
    typ=config.get("type")
    if typ=="mock-agent": return MockAgentAdapter(config)
    if typ=="http-agent": return HTTPAgentAdapter(config)
    if typ=="openai-responses": return OpenAIResponsesAdapter(config)
    if typ=="anthropic-messages": return AnthropicMessagesAdapter(config)
    if typ=="langgraph": return LangGraphAdapter(config)
    if typ=="crewai": return CrewAIAdapter(config)
    raise ValueError(f"unsupported agent adapter type: {typ}")

__all__=["make_agent_adapter","make_mcp_adapter"]
