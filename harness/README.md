# YASC Verification Harness 1.0

The YASC Verification Harness turns the YASC control/test catalog into an executable, evidence-producing verification workflow. It stays framework-neutral: target-specific behavior lives behind adapters and scenario files, while run records, evidence manifests, assessment logic, reports, and gates use the same YASC data model.

## What is executable in 1.0

- **Agent adapters**: deterministic mock, configurable JSON-over-HTTP, OpenAI Responses API, Anthropic Messages API, in-process LangGraph, and in-process CrewAI.
- **MCP adapters**: stdio and HTTP clients with modern `2026-07-28` discovery/stateless behavior plus legacy handshake fallback, `tools/list`, and `tools/call`.
- **Evidence Collector**: per-run JSONL events, structured artifacts, default secret redaction, SHA-256 manifests, and integrity verification.
- **Test Runner**: executes scenario steps/assertions against a target, repeats trials, resets state when configured, and emits `verification-run` artifacts.
- **Assessment Builder**: derives bounded per-control status and provisional assurance from the tests explicitly included in a verification plan.
- **HTML/PDF Report Generator**: branded Yofune assessment report with gate status, coverage, test outcomes, controls, and evidence references.
- **CI Security Gate**: enforces minimum coverage, required tests, severity-based failure policy, maximum inconclusive runs, evidence integrity, and evidence freshness.

YASC does **not** pretend that all 58 catalog tests are universally automatable. The built-in scenario registry marks tests that need target-specific fixtures, identities, memory, failure injection, queues, or side-effect telemetry as `guided`. A target team can convert any of those tests into an executable scenario without changing the YAT definition.

## Install

```bash
python -m pip install -e .[pdf]
yasc summary
```

Or run directly from the repository:

```bash
python scripts/yasc_harness.py summary
```

## End-to-end smoke verification

```bash
yasc plan-check examples/plans/smoke.yaml
yasc target-check examples/targets/mock-secure.yaml

yasc run \
  --plan examples/plans/smoke.yaml \
  --target examples/targets/mock-secure.yaml \
  --out build/yasc/runs \
  --evidence build/yasc/evidence \
  --summary build/yasc/run-summary.json

yasc assess \
  --plan examples/plans/smoke.yaml \
  --runs build/yasc/runs \
  --out build/yasc/assessment.json

yasc gate \
  --plan examples/plans/smoke.yaml \
  --runs build/yasc/runs \
  --policy examples/gate-policy.yaml \
  --out build/yasc/gate.json

yasc report \
  --plan examples/plans/smoke.yaml \
  --runs build/yasc/runs \
  --gate-result build/yasc/gate.json \
  --html build/yasc/assessment.html \
  --pdf build/yasc/assessment.pdf
```

The corresponding insecure mock target is expected to fail the gate:

```bash
yasc run --plan examples/plans/smoke.yaml --target examples/targets/mock-insecure.yaml --out build/insecure/runs --evidence build/insecure/evidence
yasc gate --plan examples/plans/smoke.yaml --runs build/insecure/runs --policy examples/gate-policy.yaml
# exits 10
```


## Provider and framework adapters

YASC 1.0 ships real target adapters rather than requiring every framework to be wrapped behind the generic HTTP shape:

- `openai-responses` calls the OpenAI Responses API and records text/function-call output without executing the function.
- `anthropic-messages` calls the Anthropic Messages API and records text/`tool_use` blocks without executing the tool.
- `langgraph` imports a local graph/runnable (`module:object`) and calls `.invoke()`, with optional automatic thread IDs for state reset.
- `crewai` imports a Crew/factory and calls `.kickoff(inputs=...)`.
- `mcp-stdio` and `mcp-http` negotiate modern `2026-07-28` discovery or fall back to the legacy initialize era.

See [`docs/adapters.md`](../docs/adapters.md) and the sample target files under `examples/targets/`.

## HTTP Agent adapter

The adapter is intentionally field-mapped rather than SDK-specific:

```yaml
target:
  schema_version: "1.0"
  name: Example Agent
  agent:
    type: http-agent
    url: https://agent.example/api/run
    headers:
      Authorization: "Bearer ${YASC_AGENT_TOKEN}"
    request:
      input_field: message
    response:
      text_path: output.text
      tool_calls_path: trace.tool_calls
      events_path: trace.events
```

Environment placeholders are resolved at runtime. Evidence redaction removes common secret-key fields and bearer tokens before artifacts are written.

## MCP adapter

A repository-local stdio fixture is provided so the transport can be tested without external services:

```bash
yasc mcp-list --target examples/targets/mcp-stdio.yaml
yasc mcp-call --target examples/targets/mcp-stdio.yaml --name echo --arguments '{"text":"hello"}'
```

For a real MCP server, configure either `mcp-stdio` or `mcp-http`. Do not run destructive tools against production unless the verification plan explicitly authorizes and contains them.

## Target-specific scenarios

Generate a starting point for any YAT test:

```bash
yasc scenario-init YAT-MEMORY-001 --out local/memory-poisoning.yaml
```

Then replace the placeholder step with authorized target-specific actions and assertions. Scenario definitions are separate from the normative YAT catalog: automation can evolve without silently changing the meaning of the test.

## Security gate semantics

A gate failure is a pipeline decision, not a universal statement that the system is unsafe. A passing gate means only that the configured plan/policy conditions were satisfied for the evidence available in that run.

Exit codes used by the CLI include:

- `0`: command/gate succeeded;
- `2`: schema or argument validation failure;
- `3`: evidence-integrity verification failure;
- `10`: CI security gate failed;
- `20`: test execution completed with one or more failing tests when `--exit-nonzero-on-fail` is used.

See [`docs/harness-architecture.md`](../docs/harness-architecture.md) and [`docs/ci-security-gate.md`](../docs/ci-security-gate.md).
