# YASC 1.0 Adapter Guide

YASC keeps security oracles and evidence semantics separate from framework transport. The adapter layer only turns a real target into the small interface consumed by execution scenarios.

## Supported Agent adapters

| Adapter | Target type | Integration model | Side-effect policy |
|---|---|---|---|
| Mock | `mock-agent` | deterministic repository fixture | synthetic only |
| Generic HTTP | `http-agent` | configurable JSON request/response mapping | target-defined |
| OpenAI Responses | `openai-responses` | HTTPS `/v1/responses` | function calls are observed, not executed by YASC |
| Anthropic Messages | `anthropic-messages` | HTTPS `/v1/messages` | `tool_use` blocks are observed, not executed by YASC |
| LangGraph | `langgraph` | import a local compiled graph/runnable and call `.invoke()` | graph-defined |
| CrewAI | `crewai` | import a Crew/factory and call `.kickoff(inputs=...)` | crew-defined |

The OpenAI and Anthropic adapters use the provider HTTP APIs directly so the harness does not require either provider SDK. Credentials are supplied through environment variables or target YAML placeholders and are not written into evidence artifacts.

### OpenAI Responses API

```yaml
target:
  schema_version: "1.0"
  name: OpenAI Agent
  model: "${OPENAI_MODEL}"
  agent:
    type: openai-responses
    model: "${OPENAI_MODEL}"
    api_key: "${OPENAI_API_KEY}"
    instructions: "Target system prompt"
    store: false
    tools:
      - type: function
        name: send_email
        description: Send email
        parameters:
          type: object
          properties:
            to: {type: string}
          required: [to]
```

YASC records `function_call` output items as proposed tool calls. It deliberately does not execute them. This makes adversarial scenarios safe by default and lets the scenario oracle decide whether proposing the call itself is a failure.

### Anthropic Messages API

```yaml
target:
  schema_version: "1.0"
  name: Anthropic Agent
  model: "${ANTHROPIC_MODEL}"
  agent:
    type: anthropic-messages
    model: "${ANTHROPIC_MODEL}"
    api_key: "${ANTHROPIC_API_KEY}"
    system: "Target system prompt"
    max_tokens: 1024
    tools: []
```

The adapter records text and client-side `tool_use` blocks. It does not submit tool results or execute tools.

### LangGraph

```yaml
agent:
  type: langgraph
  graph: "myapp.agent:graph"
  factory: false
  input_mode: messages
  thread_id: auto
  response:
    messages_path: messages
```

The import target must expose `.invoke(input, config=...)`. `thread_id: auto` generates a new thread identifier when the runner resets state between trials. The adapter understands ordinary LangChain/LangGraph message objects with `content` and `tool_calls` fields.

### CrewAI

```yaml
agent:
  type: crewai
  crew: "myapp.crew:create_crew"
  factory: true
  input_key: prompt
  inputs: {}
```

The target must resolve to a Crew, a factory returning a Crew, or a CrewBase-style object exposing `.crew()`. YASC calls `.kickoff(inputs=...)` and captures the returned raw output and task outputs. Framework-specific tool traces can be mapped through `response.tool_calls_path` when the application exposes them.

## MCP adapters

YASC supports `mcp-stdio` and `mcp-http` with two protocol eras:

- **Modern `2026-07-28`**: `server/discover`, stateless requests, per-request `_meta`, and HTTP `MCP-Protocol-Version` / `Mcp-Method` / `Mcp-Name` headers.
- **Legacy through `2025-11-25`**: `initialize` / `notifications/initialized`, optional `Mcp-Session-Id`, and the legacy session model.

`mode: auto` probes modern discovery and falls back to legacy. For stdio, the probe runs in a disposable sibling process so a legacy server that exits or stalls on a pre-initialize request cannot corrupt the main verification connection.

```yaml
mcp:
  type: mcp-http
  url: https://mcp.example.com/mcp
  mode: auto
  protocol_version: "2026-07-28"
  headers:
    Authorization: "Bearer ${MCP_TOKEN}"
```

YASC exposes `server/discover`/legacy initialization, `tools/list`, and `tools/call`. Multi-round-trip input-required flows are preserved as returned evidence; v1.0 does not synthesize human answers to those requests.

## Trust boundary

Adapters are part of the evidence collection path, not part of the target's security control. A malicious or incorrectly configured adapter can distort observations. Material assessments should therefore record adapter version/configuration, protect target configuration, and independently review high-impact findings.
