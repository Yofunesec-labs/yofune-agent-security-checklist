# Adoption Guide

## Phase 1 — Scope and inventory
Start with YAS-01. Register agents, dependencies, data flows, identities, tools/MCP servers, memory, execution surfaces, and high-impact actions. Produce a trust-boundary map.

## Phase 2 — Baseline design and enforcement
Assess applicable controls at YAL-1/YAL-2. Move critical authorization, tenant, execution, and egress decisions outside model preference. Record non-applicable controls with rationale instead of deleting them.

## Phase 3 — Observability and evidence
Raise critical paths toward YAL-3 by correlating task intent, identity, policy, tool/action, approval, downstream side effect, and containment evidence. Adopt the Minimum Evidence Set in `evidence-model.md`.

## Phase 4 — Adversarial and resilience verification
Use `schema/tests.yaml` / `verification-tests/` to target high-impact controls for YAL-4. Include benign control cases, repeated trials for stochastic paths, approval replay/parameter drift, memory persistence, supply-chain drift, failure injection, duplicate-side-effect testing, and kill-switch races.

## Phase 5 — Assurance cases
For consequential claims, create `templates/assurance-case.yaml`. Bind the conclusion to scope, versions, verification runs, evidence, assumptions, known gaps, residual risk, and revalidation triggers.

## Phase 6 — Continuous assurance
Run selected tests in pre-production/CI, maintain a stable security regression corpus, monitor dependency/protocol drift, and re-assess when agent capabilities or authority change. Treat material changes as possible invalidation of prior assurance.

## Suggested assessment output

Report per control:

- applicability;
- status: pass / fail / partial / not tested / not applicable;
- achieved YAL;
- verification-run references;
- evidence references and integrity status;
- known gaps / residual risk;
- owner and remediation date;
- revalidation trigger/date.

Avoid one aggregate score as the primary conclusion.
