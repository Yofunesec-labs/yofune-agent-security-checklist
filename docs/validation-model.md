# YASC Validation Model

**Status:** v1.0 Stable Release  
**Version:** 0.2-design  
**Reference snapshot:** 2026-09-18

YASC treats validation as a structured attempt to disprove a security claim, not as a demonstration that an agent behaved correctly once.

## 1. Claim-centered verification

Every assessment should be reducible to a claim of the form:

> For system **S**, in scope **B**, control **C** prevents or contains failure path **A**, under conditions **E**, with evidence **V**.

A test is useful only when it can change confidence in that claim. Passing a conversational prompt without reaching an enforcement boundary is not sufficient evidence for a high-impact control.

## 2. Four claim layers

YASC separates four layers that are often conflated:

1. **Defined** — a policy, design, or requirement exists.
2. **Enforced** — an implementation outside mere model preference applies the control.
3. **Observed** — runtime evidence shows the enforcement point acted as designed.
4. **Adversarially verified** — representative attacks, bypass attempts, and negative tests fail to defeat the control within the assessed scope.

These layers align with YAL-1 through YAL-4. They are cumulative: an adversarial test without reproducible evidence does not justify YAL-4.

## 3. Verification modes

A complete assessment may combine several modes:

| Mode | Primary question | Typical evidence |
|---|---|---|
| Design review | Is the control specified in the architecture? | threat model, policy, design record |
| Configuration inspection | Is the enforcement configured? | IAM policy, gateway rules, sandbox config |
| Positive functional test | Can legitimate behavior still succeed? | allowed trace, expected side effect |
| Negative security test | Is prohibited behavior blocked? | denial decision, no side effect |
| Adversarial test | Can a realistic attacker bypass the intended boundary? | attack corpus, traces, attempts, outcomes |
| Fault injection | Does the system fail safely when dependencies break? | injected failures, retry/rollback logs |
| Runtime observation | Does the control operate under real workload? | telemetry, alerts, policy decisions |
| Recovery exercise | Can the organization contain and restore? | kill-switch result, revoke/rollback evidence |

No single mode is sufficient for every control.

## 4. Validation dimensions

YASC does not collapse test quality into one score. Reviewers should report these dimensions separately:

### 4.1 Enforcement independence

How independent is the control from the same model behavior it is meant to constrain?

- **Model-only:** relies primarily on prompt/model refusal.
- **Runtime-assisted:** model behavior is backed by deterministic middleware or application checks.
- **External enforcement:** identity provider, policy engine, gateway, sandbox, database policy, or downstream service enforces the decision.

For high-impact actions, external enforcement is preferred.

### 4.2 Boundary coverage

Which trust boundaries were exercised: instruction, identity, data, tool, execution, tenant, agent-to-agent, approval, or telemetry?

A test that does not cross the relevant boundary cannot establish the corresponding control claim.

### 4.3 Environmental fidelity

Record where the verification ran:

- component/unit harness;
- integration environment;
- production-like staging;
- production-safe observation or bounded probe.

A staging pass does not automatically prove production equivalence. Differences in identity, network controls, tool catalogs, model versions, feature flags, or data paths must be declared.

### 4.4 Reproducibility

The run should identify enough state to reproduce the observation: model/provider/version, prompt/config hash, policy version, tool/MCP versions, environment, input corpus, time window, and trace identifiers.

### 4.5 Adversarial strength

Record whether the test used a single known payload, payload variants, multi-turn adaptation, indirect injection, chained tools, role/identity manipulation, or attacker-controlled external content.

A larger payload list is not automatically stronger; relevance to the threat model matters more than raw count.

### 4.6 Evidence integrity

Evidence should be attributable, time-correlated, tamper-evident where warranted, and protected against retrospective editing. Hashes, signed logs, immutable storage, or controlled evidence repositories may be used according to impact.

### 4.7 Temporal freshness

Agent behavior can change after model, prompt, policy, tool, MCP server, retrieval corpus, dependency, or identity configuration changes. Assurance therefore expires or requires revalidation when material change occurs.

## 5. Positive and negative controls

Every adversarial scenario should have at least one benign control case. This distinguishes a genuine security block from an agent or tool that is simply broken.

Example:

- **Benign control:** user asks the agent to send an approved email to an allowed test recipient; action succeeds.
- **Negative test:** retrieved content asks the agent to secretly add an external recipient; policy blocks the altered action.

A system that blocks both cases has availability/usability failure, not demonstrated security correctness.

## 6. Deterministic and stochastic systems

Agent behavior may vary across repeated runs. A single pass should not be treated as proof when the path includes probabilistic model decisions.

For stochastic tests, record at minimum:

- number of trials `n`;
- number of security failures `k`;
- model/version and inference parameters where available;
- attack variant set;
- whether state was reset between trials;
- observed failure rate `k/n`.

When useful, report a confidence interval for the failure probability. If zero failures are observed, the approximate "rule of three" gives an upper 95% bound of about `3/n`; for example, 0 failures in 30 trials is not evidence that failure probability is zero — it is compatible with a true rate on the order of 10% at that confidence level.

YASC therefore discourages statements such as "100% secure" or "prompt injection proof" based on finite trials.

## 7. Metamorphic and differential testing

### Metamorphic testing

Transform the representation while preserving the security-relevant meaning:

- translation;
- encoding/decoding;
- markdown/HTML/JSON wrapping;
- split instructions across documents or turns;
- paraphrase;
- reordered benign context;
- equivalent tool argument representations.

A control should not depend on a narrow lexical signature when the underlying authorization decision is unchanged.

### Differential testing

Re-run a stable test corpus across changes to:

- model/provider/version;
- system/developer prompt;
- policy bundle;
- tool/MCP server version;
- retrieval pipeline;
- agent framework;
- sandbox/runtime;
- identity configuration.

The purpose is to detect security regressions introduced by upgrades, not to rank models generically.

## 8. Compositional and multi-step verification

Agent incidents often emerge from combinations that are safe in isolation. YASC recommends explicit chain tests covering sequences such as:

`external content -> memory write -> later retrieval -> privileged tool call`

or:

`agent A -> delegated agent B -> MCP server -> database -> external egress`.

Record the authority and trust label at each hop. A downstream component must not silently inherit more authority than the caller possessed.

## 9. Fault injection and resilience

Security validation should include failure behavior, not only attacker input. Representative injections include:

- timeout and retry;
- partial tool success;
- stale or inconsistent authorization data;
- identity-provider unavailability;
- log pipeline loss;
- MCP server replacement or version mismatch;
- sandbox resource exhaustion;
- downstream duplicate execution;
- peer-agent fan-out or loop.

Expected behavior should define fail-open versus fail-closed semantics explicitly. High-impact actions should not become more permissive because a policy or approval dependency is unavailable.

## 10. Containment latency

For kill switches and revocation, measure the time between a containment decision and the last observed prohibited action. A binary "kill switch exists" claim is weaker than evidence showing:

- when containment was invoked;
- how in-flight work was handled;
- when credentials became unusable;
- when queued tasks stopped;
- whether downstream systems continued acting;
- whether restart could restore unsafe state.

## 11. Revalidation triggers

A control should be revalidated when any of the following materially changes:

- model/provider/version or inference mode;
- system/developer prompts;
- tool or MCP inventory;
- tool schemas or authorization scopes;
- identity/delegation policy;
- retrieval sources, embedding/retrieval logic, or memory implementation;
- sandbox/egress policy;
- agent framework/orchestrator;
- approval UX or approval semantics;
- detection rules or telemetry pipeline;
- high-impact action classification;
- material incident or newly discovered attack technique.

## 12. Verdicts

YASC uses the following verdicts:

- **PASS** — stated pass criteria met within assessed scope.
- **FAIL** — prohibited behavior occurred or required evidence shows the control did not operate.
- **PARTIAL** — only part of the scope or requirement is satisfied.
- **INCONCLUSIVE** — test could not establish a valid conclusion (e.g., missing evidence, broken harness, ambiguous side effect).
- **NOT TESTED** — no verification performed.
- **NOT APPLICABLE** — applicability is explicitly justified and reviewed.

`INCONCLUSIVE` is intentionally distinct from `PASS` and `FAIL`.

## 13. Independent review

YAL-4 does not require a third-party company, but high-impact claims benefit from review by a person or team independent from the implementation owner. The reviewer should be able to reconstruct the claim, scope, run conditions, verdict, and evidence without relying on undocumented oral context.


## 14. Verification plans and security oracles

YASC v1.0 requires material assessments to define a verification plan before interpreting results. The plan records the exact scope, control/test set, environment, security oracles, trial policy, state-reset semantics, evidence policy, safety constraints, and reviewer independence.

A **security oracle** is the evidence source that determines whether the prohibited or required effect actually occurred. Strong oracles are located at or beyond the enforcing boundary: policy decisions, identity authorization results, downstream receipts, database state, sandbox/egress enforcement, action-bound approvals, or correlated evidence proving absence/presence of the side effect. Model output alone is insufficient for high-impact claims.

## 15. Temporal and stateful verification

Agent workflows frequently contain delayed queues, callbacks, retries, cached credentials, long-lived browser sessions, memory, and asynchronous workers. Verification therefore includes time-of-check/time-of-use mutation, approval expiry, credential revocation propagation, queued-action drain, restart behavior, and delayed memory activation.

For consequential actions, compare the security-relevant intent at authorization time with the action actually executed. Material differences require re-authorization.

## 16. Parser and representation differentials

Test whether validators, policy engines, agent runtimes, and downstream tools interpret the same request consistently. Include duplicate keys, null/default ambiguity, Unicode normalization/confusables, alternate encodings, unknown fields, nested structures, and canonicalization. Security should depend on the meaning of the action, not one serialization.

## 17. Coverage reporting

Coverage is reported as separate dimensions: applicable controls, planned tests, exercised trust boundaries, high-impact action classes, evidence completeness, variant coverage, environment fidelity, and change/regression coverage. YASC does not convert these dimensions into a universal security score.

## 18. v1.0 executable harness boundary

`scripts/yasc_harness.py` provides plan validation, run scaffolding, evidence manifests/integrity checks, and plan-to-run coverage. Target-specific attack execution remains an adapter responsibility so the baseline stays framework-neutral and does not imply authorization to test third parties.
