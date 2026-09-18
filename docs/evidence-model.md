# YASC Evidence Model

Security claims become durable only when another reviewer can reconstruct what happened.

## Minimum Evidence Set (MES)

For a verification run, collect as applicable:

1. **Claim and scope** — control ID, system, environment, tenant/test account, included and excluded components.
2. **Version state** — YASC version, model/provider/version, prompt/config hash, policy version, tool/MCP versions, application build.
3. **Stimulus** — test ID, payload/corpus reference, preconditions, user/agent identity, relevant external content.
4. **Decision path** — agent plan or available decision trace, policy decision, authorization result, approval event.
5. **Action path** — tool/MCP request, downstream API/database/shell request, response, side effect.
6. **Telemetry** — trace ID, correlated event IDs, timestamps, alerts, containment events.
7. **Outcome** — pass/fail/partial/inconclusive, unexpected effects, cleanup/rollback status.
8. **Integrity metadata** — hashes, signer/collector, collection time, storage location, redaction record.

Not every control needs every artifact. The minimum set should be sufficient to support the specific claim.

## Evidence classes

YASC recognizes several evidence classes without ranking them as substitutes for one another:

- **E-DESIGN** — architecture, policy, data-flow, threat model.
- **E-CONFIG** — IAM policy, gateway rule, policy-as-code, sandbox profile, deployment config.
- **E-RUNTIME** — trace, log, audit event, policy decision, tool call, approval event.
- **E-TEST** — test definition, payload, run record, expected/actual result.
- **E-SIDE-EFFECT** — downstream system state proving an action did or did not occur.
- **E-INTEGRITY** — hashes, signatures, immutable log references, custody record.
- **E-REVIEW** — reviewer sign-off, exception, residual-risk acceptance.

## Evidence quality rules

Evidence should be:

- **attributable** — tied to the relevant system and principal;
- **correlatable** — events across components can be linked;
- **time-bounded** — collection and event times are known;
- **versioned** — material configuration is identifiable;
- **minimized** — unnecessary secrets and personal data are not collected;
- **integrity-protected** — alteration is detectable where material;
- **retained appropriately** — long enough for audit/incident use, not indefinitely by default;
- **reproducible** — another reviewer can repeat or independently inspect the basis of the conclusion.

## Evidence freshness

Evidence is not permanent. Treat a material change as a potential invalidation event. Assessments should carry:

- `assessed_at`;
- `valid_through` when an organization uses time-based expiry;
- `change_triggers`;
- `last_revalidated_at`;
- links to the versions/configuration to which evidence applies.

## Privacy and sensitive reasoning

YASC does not require storage of hidden model chain-of-thought. Security evidence should prefer observable inputs, policy decisions, tool calls, approvals, outputs, and system traces. Where a product exposes internal plans or summaries, collect only what is authorized and necessary. Redact secrets and personal data without destroying the evidence needed to validate the claim.


## v1.0 — Evidence manifests and collectors

The repository defines `schema/evidence-manifest.schema.json` and `templates/evidence-manifest.yaml`. A manifest records SHA-256, artifact size, type, path, source component, trace ID, sensitivity, collection time, and redaction notes. It supports integrity review without pretending that a hash proves the original source was truthful.

## Causal integrity

Evidence quality includes **causal attribution**, not only completeness. Concurrent tasks, retries, callbacks, and shared tools can create trace collisions. High-impact verification should demonstrate that the final side effect can be tied to the correct user/task, tenant, policy decision, approval, and tool call.

## Evidence minimization

Collect the smallest evidence set that permits independent reconstruction. Secret values, personal data, and unrelated customer content should be omitted or redacted when the security claim can still be evaluated. Redaction should preserve identifiers/digests and the fields that determine policy/action semantics.
