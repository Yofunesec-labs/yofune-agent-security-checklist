# Contributing to YASC

Thank you for helping improve an evidence-driven baseline for agent security.

## Contribution types

- **Control proposal** — new or changed control objective, threat, check, evidence, or pass criteria.
- **Verification test** — reproducible adversarial or assurance test with safe preconditions and expected result.
- **Profile change** — context-specific requirement for MCP, RAG, coding, browser, data, customer service, multi-agent, or enterprise copilot systems.
- **Crosswalk correction** — framework mapping supported by a dated primary source.
- **Editorial fix** — clarity, examples, links, formatting, or generated-output issues.

## Process

```text
Issue → Proposal → Technical discussion → Yofune editorial review → Draft → Public review → Release
```

1. Open an issue using the closest template.
2. State the threat/failure mode and why existing controls do not cover it.
3. For a control change, update `schema/controls.yaml`; generated files should be rebuilt with `make generate`.
4. For a test, update `schema/tests.yaml` and link it to one or more controls.
5. Add primary references for external-framework mapping changes.
6. Run `make check` before opening a PR.

## Control design rules

A control must be testable and evidence-bearing. Avoid vague requirements such as “use secure AI practices.” Prefer language that identifies an enforcement point and a falsifiable pass condition.

Every control should support: **Control → Threat → Test → Evidence → Pass Criteria**.

## Safety

Verification tests must be designed for systems you own or are explicitly authorized to test. Use synthetic/non-production data by default. Do not contribute payloads whose only practical purpose is unauthorized exploitation of third-party systems.

## Editorial authority

Community review is welcomed; final editorial decisions and release signing remain with **Yofune Security Research**.
