# YASC Verification Procedure Specification

**Revision:** 1.0

A YASC test is not just a payload. It is a controlled experiment against a security claim.

## Required procedure fields

Each verification procedure should define:

1. **Claim under test** — the control property that could be falsified.
2. **Security boundary** — where enforcement is expected to occur.
3. **Preconditions** — identity, data, tools, state, and environment needed.
4. **Benign control** — a legitimate action that should succeed.
5. **Adversarial stimulus** — the malicious, malformed, ambiguous, or fault condition.
6. **Oracle** — the evidence source that decides success/failure; model prose alone is not a sufficient oracle for high-impact actions.
7. **Trials and variants** — repetition, state reset, transformation strategy, and stopping conditions.
8. **Side-effect observation** — how the evaluator determines what actually happened downstream.
9. **Evidence set** — trace, policy, approval, tool, service, identity, and integrity artifacts.
10. **Safety constraints** — authorization, synthetic data, containment, rate/budget limits, prohibited targets.
11. **Pass/fail criteria** — written before execution where possible.
12. **Revalidation trigger** — changes that invalidate the result.

## Oracle hierarchy

Strong verification uses an oracle at or beyond the enforcement boundary:

- downstream service receipt or database state;
- policy engine decision;
- identity-provider authorization result;
- sandbox/egress enforcement record;
- approval service record bound to an action digest;
- correlated trace showing no prohibited side effect.

An assistant message saying “I refused” is supporting evidence, not proof that a side effect did not occur.

## State discipline

Stateful agents require explicit reset semantics. Tests should document whether conversation state, persistent memory, queues, browser sessions, credentials, caches, and tool state are reset between trials. Otherwise repeated trials can measure contamination rather than independent behavior.

## Temporal discipline

Verification should include relevant temporal boundaries: token expiry, approval expiry, delayed jobs, retries, cancellation, revocation propagation, and time-of-check/time-of-use mutation.

## Negative space

A mature test plan deliberately exercises what should **not** happen: unauthorized egress, cross-tenant retrieval, unapproved side effects, stale approval reuse, transitive delegation, evidence loss, and action resurrection after containment.
