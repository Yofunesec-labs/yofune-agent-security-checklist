<p align="center">
  <img src="assets/brand/yofune-mark-web.png" alt="Yofune" width="150">
</p>

<p align="center"><strong>Chengdu Yofune Ariake Technology Co., Ltd.</strong><br>
<a href="https://yofunesec.com/">yofunesec.com</a> · <a href="mailto:contact@yofunesec.com">contact@yofunesec.com</a></p>

# Yofune Agent Security Checklist (YASC)

> **A verifiable security baseline for AI agents.**  
> Controls, reproducible verification, evidence, and bounded assurance claims.

[![Status: v1.0 Stable](https://img.shields.io/badge/status-v1.0%20stable-2ea44f)](#status)
[![Controls](https://img.shields.io/badge/controls-52-blue)](schema/controls.yaml)
[![Tests](https://img.shields.io/badge/verification%20tests-58-blue)](schema/tests.yaml)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE.md)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-lightgrey)](LICENSE.md)

**YASC** turns agent-security risks into controls that can be **checked, tested, evidenced, and independently reviewed**. It is not another risk-ranking list. The repository is the source of truth; PDFs, websites, spreadsheets, and product integrations are release artifacts generated from the same data.

中文说明：[`README.zh-CN.md`](README.zh-CN.md)

## Status

**v1.0.0 — Stable Baseline + Executable Reference Harness**  
Reference snapshot: **2026-09-18**

The v1.0 release contains:

- **10 security domains** and **52 controls**.
- **58 reusable verification tests** with expected results and evidence requirements.
- **Yofune Assurance Levels (YAL-0…YAL-4)** plus machine-readable verification plans/runs, evidence manifests, assurance cases, and bounded conformance claims.
- Security profiles for MCP, RAG, coding, browser, data, customer-service, multi-agent, and enterprise-copilot systems.
- Crosswalks to OWASP Agentic Top 10 2026, NIST AI RMF / NIST AI 600-1, and selected MITRE ATLAS technique families.
- Machine-readable YAML + JSON Schema, generated Markdown/CSV/JSON, an interactive static checklist, CI validation, and an executable framework-neutral verification harness.
- **Agent/MCP adapters, Evidence Collector, Test Runner, assessment builder, branded HTML/PDF report generator, and CI Security Gate.**


## Technical Whitepaper

- **English PDF:** [`whitepaper/YASC-Technical-Whitepaper-v1.0.0.pdf`](whitepaper/YASC-Technical-Whitepaper-v1.0.0.pdf)
- **English DOCX:** [`whitepaper/YASC-Technical-Whitepaper-v1.0.0.docx`](whitepaper/YASC-Technical-Whitepaper-v1.0.0.docx)
- **Chinese review PDF:** [`whitepaper/YASC-Technical-Whitepaper-v1.0.0.zh-CN.pdf`](whitepaper/YASC-Technical-Whitepaper-v1.0.0.zh-CN.pdf)
- **Chinese review DOCX:** [`whitepaper/YASC-Technical-Whitepaper-v1.0.0.zh-CN.docx`](whitepaper/YASC-Technical-Whitepaper-v1.0.0.zh-CN.docx)
- **Authoritative Markdown:** [`docs/whitepaper.md`](docs/whitepaper.md)
- **Validation model:** [`docs/validation-model.md`](docs/validation-model.md)
- **Evidence model:** [`docs/evidence-model.md`](docs/evidence-model.md)
- **Assurance cases:** [`docs/assurance-case.md`](docs/assurance-case.md)
- **Provenance and originality policy:** [`docs/provenance.md`](docs/provenance.md)

The whitepaper treats assurance as a bounded claim tied to system state, verification runs, evidence, known gaps, and revalidation triggers. It also defines guidance for stochastic testing, metamorphic/differential testing, fault injection, containment testing, and evidence freshness.

## v1.0 Executable Verification Stack

YASC v1.0 adds a claim-centered verification workflow:

- `verification-plan` — fixes scope, tests, oracles, trial policy, evidence policy, safety constraints, and reviewer independence before execution;
- `verification-run` — records a concrete test execution against an exact system state;
- `evidence-manifest` — hashes collected evidence and records provenance/integrity metadata;
- `assurance-case` — explains which evidence supports a bounded security claim and what remains outside it;
- `conformance-claim` — a bounded, non-certification format for sharing scoped control/profile/baseline results;
- `scripts/yasc_harness.py` / `yasc` — executable CLI for adapters, test execution, evidence collection, assessment, reports, and CI gating.
- `harness/yasc_harness/adapters/` — OpenAI Responses, Anthropic Messages, LangGraph, CrewAI, generic HTTP, MCP stdio/HTTP, and deterministic mock adapters.
- `harness/scenarios/core.yaml` — executable/guided scenario registry for all 58 YAT tests.
- `.github/actions/yasc-security-gate/` — reusable CI gate integration.

See [`docs/test-procedure.md`](docs/test-procedure.md), [`docs/evidence-integrity.md`](docs/evidence-integrity.md), [`docs/conformance.md`](docs/conformance.md), and [`docs/coverage-model.md`](docs/coverage-model.md).

Implementation details: [`harness/README.md`](harness/README.md), [`docs/harness-architecture.md`](docs/harness-architecture.md), [`docs/adapters.md`](docs/adapters.md), and [`docs/ci-security-gate.md`](docs/ci-security-gate.md).

Release/publishing workflow: [`releases/v1.0.0/RELEASE_NOTES.md`](releases/v1.0.0/RELEASE_NOTES.md) and [`PUBLISHING.md`](PUBLISHING.md). An authenticated GitHub CLI can publish the prepared `main` + `v1.0.0` refs with `./scripts/publish_github.sh OWNER/yofune-agent-security-checklist --public`.

## The Method

```text
Scope  →  Attack  →  Control  →  Verify  →  Evidence  →  Assurance  →  Revalidate
```

Every control answers five questions:

1. **Scope** — when does this control apply?
2. **Attack** — what failure or adversarial path does it address?
3. **Control** — what must the system enforce?
4. **Verify** — how do we test that enforcement?
5. **Evidence** — what proves the control actually operated?

## Assurance Levels

| Level | Meaning |
|---|---|
| **YAL-0** | Unknown — no usable evidence |
| **YAL-1** | Defined — policy/design exists |
| **YAL-2** | Enforced — control is implemented |
| **YAL-3** | Observed — logs/traces show it operating |
| **YAL-4** | Adversarially Verified — active testing shows resistance to representative attacks |

YASC deliberately avoids a single “security score.” A high aggregate score can hide one catastrophic control failure. Report control status and assurance level instead.

## Domains

| Domain | Core question |
|---|---|
| [YAS-01 — Agent Inventory & Boundary](baseline/YAS-01-inventory-boundary.md) | What can the agent access, trust, change, and affect? |
| [YAS-02 — Goal & Instruction Integrity](baseline/YAS-02-goal-instruction-integrity.md) | Who can change the agent’s goals or instructions? |
| [YAS-03 — Identity & Privilege](baseline/YAS-03-identity-privilege.md) | Under whose identity does the agent act, and with what authority? |
| [YAS-04 — Tool & MCP Security](baseline/YAS-04-tool-mcp.md) | Which tools can the agent call, and how are those calls authorized? |
| [YAS-05 — Data, RAG & Memory](baseline/YAS-05-data-rag-memory.md) | What information does the agent trust now and later? |
| [YAS-06 — Code & Execution](baseline/YAS-06-code-execution.md) | What code, commands, files, and network operations can the agent execute? |
| [YAS-07 — Agentic Supply Chain](baseline/YAS-07-supply-chain.md) | Can models, tools, skills, servers, packages, or data dependencies be trusted? |
| [YAS-08 — Multi-Agent Communication](baseline/YAS-08-multi-agent.md) | Can agents authenticate each other and limit delegated authority? |
| [YAS-09 — Human Control & Approval](baseline/YAS-09-human-control.md) | When must a person decide, and what exactly are they approving? |
| [YAS-10 — Detection, Response & Containment](baseline/YAS-10-detection-response.md) | Can unsafe behavior be detected, reconstructed, and stopped? |


## Repository Layout

```text
yofune-agent-security-checklist/
├── baseline/              # Human-readable baseline controls
├── profiles/              # Scenario-specific security profiles
├── verification-tests/    # Test playbooks by attack family
├── crosswalk/             # Framework mappings
├── schema/                # Machine-readable source of truth
├── harness/               # Executable Agent/MCP verification package and scenarios
├── examples/              # Safe targets, plans, policies, and MCP fixture
├── scripts/               # Validation, generation, and repository CLI wrappers
├── site/                  # Interactive static checklist
├── docs/                  # Methodology, trust model, adoption guide, whitepaper source
├── references/            # Versioned reference snapshot
├── releases/              # Release manifests
└── .github/               # CI, Pages, issue/PR templates
```

## Quick Start

Validate the standard and launch the interactive checklist:

```bash
python -m pip install -r requirements-dev.txt
make check
python -m http.server 8000 -d site
```

Run the executable verification reference flow:

```bash
python -m pip install -e ".[pdf]"
make harness-smoke
make harness-mcp-smoke
```

Real target examples are included for OpenAI Responses, Anthropic Messages, LangGraph, CrewAI, generic HTTP agents, and MCP. Provider adapters observe proposed tool calls but do not execute them; target-side tool execution remains outside the harness by design. Provider model IDs are supplied through `${OPENAI_MODEL}` / `${ANTHROPIC_MODEL}` so living provider model names are not hard-coded into the standard.

Or use the CLI directly:

```bash
yasc run --plan examples/plans/smoke.yaml --target examples/targets/mock-secure.yaml \
  --out build/yasc/runs --evidence build/yasc/evidence
yasc gate --plan examples/plans/smoke.yaml --runs build/yasc/runs \
  --policy examples/gate-policy.yaml --out build/yasc/gate.json
yasc report --plan examples/plans/smoke.yaml --runs build/yasc/runs \
  --gate-result build/yasc/gate.json --html build/yasc/assessment.html --pdf build/yasc/assessment.pdf
```

Open `http://localhost:8000` for the interactive checklist. The smoke flow also produces a branded Yofune assessment report and hashed evidence package. The MCP smoke flow initializes a repository-local MCP server, discovers its tools through the real stdio adapter, records evidence, and enforces a critical-severity CI gate without invoking a tool.

## Control Example

```yaml
id: YAS-04.03
title: Sensitive Tool Authorization
severity: critical
target_assurance: YAL-4
adversarial_tests:
  - YAT-TOOL-001
evidence:
  - tool request
  - policy decision
  - approval event
  - tool response
  - trace ID
  - timestamp
mappings:
  owasp_agentic_2026: [ASI01, ASI02, ASI03, ASI09]
```

The authoritative record is [`schema/controls.yaml`](schema/controls.yaml).

Assessment artifacts include [`templates/assessment.yaml`](templates/assessment.yaml), [`templates/verification-plan.yaml`](templates/verification-plan.yaml), [`templates/verification-run.yaml`](templates/verification-run.yaml), [`templates/evidence-manifest.yaml`](templates/evidence-manifest.yaml), [`templates/evidence-package.md`](templates/evidence-package.md), [`templates/assurance-case.yaml`](templates/assurance-case.yaml), and [`templates/conformance-claim.yaml`](templates/conformance-claim.yaml), with JSON Schemas under [`schema/`](schema/). Optional product adapters can emit the vendor-neutral result envelope documented under [`integrations/`](integrations/kuroshio/README.md).

## Profiles

Profiles add context-specific requirements without destabilizing the core baseline:

- [MCP Security Profile](profiles/mcp/README.md) — target spec `2026-07-28`.
- [RAG Agent Security Profile](profiles/rag/README.md).
- [Coding Agent Security Profile](profiles/coding-agent/README.md).
- [Browser Agent Security Profile](profiles/browser-agent/README.md).
- [Data Agent Security Profile](profiles/data-agent/README.md).
- [Customer Service Agent Security Profile](profiles/customer-service-agent/README.md).
- [Multi-Agent Security Profile](profiles/multi-agent/README.md).
- [Enterprise Copilot Security Profile](profiles/enterprise-copilot/README.md).

## Reference Snapshot

This version is reviewed against a dated snapshot rather than claiming permanent alignment with living standards. See [`references/snapshot-2026-09-18.md`](references/snapshot-2026-09-18.md).

Key external references include:

- OWASP Top 10 for Agentic Applications 2026.
- OWASP Agent Control Standard (ACS), published 2026-09-01.
- Model Context Protocol specification `2026-07-28` and its authorization hardening.
- NIST AI RMF 1.0 and NIST AI 600-1 Generative AI Profile.
- MITRE ATLAS as a living AI adversary tactics/techniques knowledge base.

Mappings are **cross-references, not claims of certification or endorsement**.

## Contributing

Issues, control proposals, test cases, evidence patterns, and profile improvements are welcome. Changes flow through proposal → technical discussion → editorial review → public review → release. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`GOVERNANCE.md`](GOVERNANCE.md).

## Licensing

- Documentation and narrative control text: **CC BY 4.0**.
- Code, schemas, test definitions, generators, and site assets: **Apache-2.0**.

See [`LICENSE.md`](LICENSE.md). Third-party framework names and mappings remain subject to their respective owners and licenses.

## Maintainer

**Maintained by Yofune Security Research.**  
Published by **Chengdu Yofune Ariake Technology Co., Ltd.**  
https://yofunesec.com/ · contact@yofunesec.com
