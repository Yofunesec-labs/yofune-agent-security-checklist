from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FakeAIMessage:
    content: str
    tool_calls: list


class FakeGraph:
    def invoke(self, input, config=None):
        message = input['messages'][-1]['content'] if isinstance(input, dict) else str(input)
        calls = []
        text = f"LangGraph received: {message}"
        if 'CALL_TOOL' in message:
            calls = [{'id': 'lg-call-1', 'name': 'safe_lookup', 'args': {'q': 'demo'}}]
            text = ''
        return {'messages': [FakeAIMessage(content=text, tool_calls=calls)], 'config_seen': config}


graph = FakeGraph()


@dataclass
class FakeTaskOutput:
    raw: str


@dataclass
class FakeCrewOutput:
    raw: str
    tasks_output: list


class FakeCrew:
    def kickoff(self, inputs=None):
        inputs = inputs or {}
        return FakeCrewOutput(
            raw=f"CrewAI received: {inputs.get('prompt', '')}",
            tasks_output=[FakeTaskOutput(raw='task complete')],
        )


def create_crew():
    return FakeCrew()
