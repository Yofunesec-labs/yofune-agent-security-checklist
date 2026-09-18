# Yofune Agent Security Checklist (YASC) v1.0.0

**Release date:** 2026-09-18  
**Reference snapshot:** 2026-09-18  
**Status:** Stable Baseline  
**Maintainer:** Yofune Security Research  
**Publisher:** Chengdu Yofune Ariake Technology Co., Ltd.  
**Website:** https://yofunesec.com/  
**Contact:** contact@yofunesec.com

YASC v1.0.0 is the first stable release of the Yofune evidence-driven Agent Security baseline and its open verification framework. It keeps the 10-domain / 52-control baseline stable while completing the path from a security claim to executable verification, evidence, assessment reporting, and a CI decision.

## What ships in v1.0.0

### Stable security baseline

- 10 security domains.
- 52 core controls with objective, threat, applicability, verification, evidence, pass criteria, and external mappings.
- 58 reusable YAT verification tests.
- 8 architecture/security profiles: MCP, RAG, coding, browser, data, customer service, multi-agent, and enterprise copilot.
- YAL-0 through YAL-4 assurance taxonomy.
- Versioned crosswalks to OWASP Agentic Top 10 2026, NIST AI RMF / AI 600-1, and selected MITRE ATLAS technique families.

### Executable YASC Verification Harness

The `yasc` CLI now supports the complete reference workflow:

```text
Verification Plan
      ↓
Target Adapter
      ↓
Scenario Test Runner
      ↓
Evidence Collector
      ↓
Verification Run + Evidence Manifest
      ↓
Assessment Builder
      ↓
HTML / PDF Assessment Report
      ↓
CI Security Gate
```

The harness produces hashed evidence, machine-readable runs, bounded per-control assurance, and CI exit codes suitable for merge/release gates.

### Real target adapters

v1.0.0 includes:

- `http-agent` — framework-neutral JSON-over-HTTP mapping.
- `openai-responses` — OpenAI Responses API, including observation of `function_call` output items.
- `anthropic-messages` — Anthropic Messages API, including observation of `tool_use` blocks.
- `langgraph` — in-process LangGraph/LangChain runnable import with `.invoke()` and thread reset support.
- `crewai` — in-process CrewAI Crew/factory import with `.kickoff(inputs=...)`.
- `mcp-stdio` — MCP over stdio.
- `mcp-http` — MCP over HTTP / streamable responses.

Provider adapters observe proposed tool calls but do **not** execute them. This is deliberate: adversarial verification should not create a side effect merely because the model attempted one.

### MCP 2026-07-28 + legacy interoperability

The MCP adapters support both protocol eras:

- modern `2026-07-28`: `server/discover`, per-request `_meta`, stateless request routing, `MCP-Protocol-Version`, `Mcp-Method`, and `Mcp-Name` headers;
- legacy through `2025-11-25`: `initialize` / `notifications/initialized` and legacy session behavior.

`mode: auto` probes the modern protocol and falls back to legacy. The stdio probe uses a disposable sibling process so an old server that exits or stalls before `initialize` cannot corrupt the main verification connection.

### Evidence and reporting

- per-run JSONL event evidence;
- common-secret redaction guardrails;
- SHA-256 evidence manifests and integrity verification;
- machine-readable assessment artifacts;
- branded Yofune HTML/PDF Assessment Report;
- English and Chinese technical whitepapers.

### CI Security Gate

The reusable GitHub Action and `yasc gate` can enforce:

- minimum planned-test coverage;
- required tests;
- severity-based failures;
- maximum inconclusive results;
- evidence hash integrity;
- evidence freshness.

A gate PASS remains a bounded engineering decision for the declared plan, target state, evidence and policy. It is not a universal security certification.

## GitHub Pages

The repository ships a GitHub Pages workflow for the interactive control checklist and release downloads. Pages is rebuilt from the repository source of truth and includes the v1.0.0 whitepapers and release notes.

## Release assets

- `yasc-v1.0.0.zip` — complete repository source release.
- `yasc-v1.0.0.sha256` — SHA-256 checksum.
- `YASC-Technical-Whitepaper-v1.0.0.pdf` — English technical whitepaper.
- `YASC-Technical-Whitepaper-v1.0.0.zh-CN.pdf` — Chinese technical whitepaper.
- `YASC-Sample-Assessment-Report-v1.0.0.pdf` — sample generated assessment report.

## Claim boundary

YASC v1.0.0 is an open security baseline and verification framework, not a commercial certification program. `PASS`, `YAL-4`, or a CI gate PASS must always be interpreted with the recorded scope, system version, model/prompt/policy/tool state, test selection, evidence set, validity window, exclusions, and revalidation triggers.

## Upgrade notes from v0.5

- Core control IDs remain stable.
- Verification catalog remains at 58 tests.
- Harness changes are additive at the target-adapter layer.
- MCP raw clients were corrected for the `2026-07-28` stateless/discovery protocol era and retain legacy fallback.
- Existing `mock-agent`, `http-agent`, `mcp-stdio`, and `mcp-http` target files remain supported; MCP targets can explicitly set `mode: legacy` when required.

## Verification performed for this release

Repository CI exercises:

- secure deterministic Agent flow → gate must PASS;
- intentionally insecure Agent flow → gate must FAIL;
- modern MCP stdio discovery/list/call fixture;
- modern MCP HTTP discovery/list/call fixture;
- legacy MCP HTTP fallback;
- OpenAI Responses request/response parsing against a local API fixture;
- Anthropic Messages request/response parsing against a local API fixture;
- LangGraph import/invoke adapter fixture;
- CrewAI import/kickoff adapter fixture;
- report generation, evidence integrity, schema validation, and repository generation tests.

For implementation details see `docs/adapters.md`, `docs/harness-architecture.md`, and `docs/ci-security-gate.md`.
