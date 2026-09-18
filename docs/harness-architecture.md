# YASC 1.0 Verification Harness Architecture

## Purpose

YASC 1.0 adds an executable reference implementation for the verification lifecycle while keeping the baseline vendor-neutral. The harness is deliberately split into six trust-relevant components:

```text
Verification Plan
       |
       v
Scenario Registry ---> Target-specific Scenario
       |                       |
       v                       v
 Test Runner --------> Agent / MCP Adapter
       |                       |
       +----------+------------+
                  v
           Evidence Collector
                  |
                  v
        Verification Run + Manifest
                  |
          +-------+--------+
          v                v
    Assessment         CI Security Gate
          |                |
          +-------+--------+
                  v
             HTML / PDF
```

### Adapter boundary

Adapters translate a target framework into a small YASC execution interface. They do not decide whether a result passes. Keeping transport/integration separate from security oracles avoids coupling YASC to one agent framework.

**Agent adapters** expose `send`, `reset`, and `close`. v1.0 includes a deterministic mock, a field-mapped JSON-over-HTTP adapter, direct OpenAI Responses API and Anthropic Messages API adapters, an in-process LangGraph adapter, and an in-process CrewAI adapter. Provider adapters observe proposed tool calls but do not execute them.

**MCP adapters** expose discovery/legacy initialization, list-tools, call-tool, and close operations. The stdio and HTTP clients support both the modern `2026-07-28` protocol era (`server/discover`, per-request `_meta`, stateless HTTP routing headers) and legacy initialize/session behavior. `mode: auto` negotiates between them. The stdio modern probe uses a disposable sibling process so old servers that stall before `initialize` cannot poison the main connection.

Configuration examples and framework notes are in [`docs/adapters.md`](adapters.md).

### Scenario boundary

A YAT test defines purpose, procedure, expected result, evidence, control mapping, and safety constraints. An **execution scenario** binds that normative test to concrete target actions and machine-checkable assertions.

YASC does not label a test "automated" merely because it can send a prompt. Tests involving tenant boundaries, identity revocation, memory lifecycle, queue cancellation, network egress, kill switches, retry behavior, or supply-chain rollback need real target fixtures and observability. The built-in registry therefore leaves these as guided until a target-specific scenario exists.

### Evidence boundary

The Evidence Collector records requests, target responses, assertion outcomes, and runner errors. Structured evidence is redacted for common secret fields before persistence. Each run produces a SHA-256 evidence manifest. Integrity proves that the collected bytes have not changed after hashing; it does not prove that the target telemetry itself was truthful.

### Gate boundary

The CI gate evaluates engineering policy such as:

- minimum planned-test coverage;
- specific required tests;
- failures at configured severities;
- maximum inconclusive results;
- evidence-manifest integrity;
- maximum evidence age.

The gate never averages a critical failure into an aggregate score.

## Supported assertions in 1.0

The reference runner includes reusable assertions for:

- no tool calls / presence of tool calls;
- text regular-expression match / non-match;
- MCP tool-name uniqueness;
- conservative confusable-name collision checks;
- structured path equality.

Teams can add new target-specific assertions without changing control IDs or YAT semantics.

## Evidence and secret handling

The harness applies default structured redaction for keys containing authorization, token, secret, password, API key, cookie, or credential, and masks bearer tokens found in string values. This is a guardrail, not a complete DLP system. Assessment owners remain responsible for evidence classification, redaction review, storage, and retention.

## Safety model

The reference repository only auto-runs synthetic probes against a deterministic mock target in CI. Real targets must be explicitly configured by the operator. YASC test definitions require authorization and containment; the harness does not grant permission to test third-party or production systems.
