# Verification Methodology

## Scope → Attack → Control → Verify → Evidence → Assurance Claim

YASC treats verification as a structured attempt to disprove a bounded security claim. It is not limited to jailbreak prompting and it does not treat one successful refusal as proof of security.

### 1. Scope
Inventory the agent, principals, tools, data, memory, execution, external content, peer agents, environments, and high-impact actions. Draw trust boundaries before testing.

### 2. Attack
Choose realistic failure paths that challenge authorization and trust assumptions, not just model wording. Include direct/indirect injection, privilege misuse, poisoned context, tool chaining, execution escape, delegation abuse, approval replay, dependency drift, and cascading failure.

### 3. Control
Identify the enforcement point. A model refusal is useful defense in depth but should not be the only barrier protecting a high-impact resource.

### 4. Verify
Combine the verification modes appropriate to the claim: design review, configuration inspection, positive functional testing, negative testing, adversarial testing, fault injection, runtime observation, and recovery exercises.

For stochastic paths, use repeated trials and record `n`, security failures `k`, state-reset behavior, version state, and the attack variant set. Do not infer a zero failure probability from zero observed failures.

### 5. Evidence
Preserve enough evidence for an independent reviewer to distinguish “defined,” “enforced,” “observed,” and “adversarially verified.” Prefer observable policy/tool/approval/side-effect evidence; hidden model chain-of-thought is not required.

### 6. Assurance Claim
Bind the conclusion to an explicit scope, achieved YAL, evidence, assumptions, known gaps, residual risk, assessment date, and revalidation triggers.

## Test quality dimensions

Report these dimensions separately instead of collapsing them into one score:

- enforcement independence;
- boundary coverage;
- environmental fidelity;
- reproducibility;
- adversarial strength;
- evidence integrity;
- temporal freshness.

## Pass/fail discipline

Use `PASS`, `FAIL`, `PARTIAL`, `INCONCLUSIVE`, `NOT TESTED`, and `NOT APPLICABLE`. A broken harness or missing evidence is `INCONCLUSIVE`, not `PASS`.

## Revalidation

Re-run mapped verification when material model, prompt, policy, tool/MCP, identity, retrieval/memory, sandbox, approval, telemetry, or dependency state changes.

## Safe testing

Use isolated or bounded environments, synthetic accounts/data, explicit authorization, rate/resource limits, and rollback/containment plans. Verification must not become uncontrolled exploitation.

See [`validation-model.md`](validation-model.md), [`evidence-model.md`](evidence-model.md), and [`assurance-case.md`](assurance-case.md) for the full model.
