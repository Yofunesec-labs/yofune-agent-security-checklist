# YAS-10 — Detection, Response & Containment
> **Core question:** Can unsafe behavior be detected, reconstructed, and stopped?
> **Principle:** Capture correlated evidence, detect policy violations, preserve audit integrity, and provide a tested kill switch.

## Controls

### YAS-10.01 — Security Event Telemetry
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Record security-relevant agent events across prompts, policy decisions, tool calls, identity, memory, retrieval, execution, and approvals.

**Applies when**
- agent runs outside a disposable local-only sandbox

**Threat**  
Without telemetry, harmful behavior cannot be detected, investigated, or proven.

**Check**  
Trigger representative security events and verify they produce structured, attributable telemetry.

**Adversarial tests**
- `YAT-IR-002`
- `YAT-OBS-001`
- `YAT-OBS-003`

**Required evidence**
- event schema
- sample logs
- coverage test result

**Pass criteria**  
Required event classes are logged with actor, target, decision, outcome, timestamp, and correlation identifier.

**Mappings**  
OWASP Agentic 2026: ASI08, ASI10  
NIST AI RMF functions: MEASURE, MANAGE

---

### YAS-10.02 — Trace Correlation & Evidence Completeness
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Correlate end-to-end evidence from user/task intent through model/plan, policy, tools, approvals, and side effects.

**Applies when**
- agent has multiple components or side-effecting steps

**Threat**  
Fragmented logs make it impossible to prove why an action occurred or which control made a decision.

**Check**  
Execute a multi-step scenario and reconstruct it using trace identifiers without privileged ad hoc data gathering.

**Adversarial tests**
- `YAT-IR-002`
- `YAT-TOOL-007`
- `YAT-OBS-001`
- `YAT-OBS-003`

**Required evidence**
- trace ID
- prompt/context references
- policy log
- tool log
- approval log
- side-effect receipt

**Pass criteria**  
Investigators can reconstruct the security-relevant chain from one trace/case identifier with documented gaps.

**Mappings**  
OWASP Agentic 2026: ASI08, ASI10  
NIST AI RMF functions: MEASURE

---

### YAS-10.03 — Policy Violation & Anomaly Detection
**Severity:** `high`  
**Target assurance:** `YAL-4`

**Security objective**  
Detect denied/bypassed controls, unusual tool use, privilege changes, repeated injections, exfiltration patterns, and abnormal agent behavior.

**Applies when**
- production agent can access sensitive data or side-effecting capabilities

**Threat**  
Controls may fail silently while harmful behavior appears operationally successful.

**Check**  
Generate known policy violations and abnormal sequences to measure detection coverage and alert quality.

**Adversarial tests**
- `YAT-IR-003`
- `YAT-RESILIENCE-001`
- `YAT-DIFF-001`

**Required evidence**
- detection rule
- alert
- trace link
- response ticket

**Pass criteria**  
Defined high-severity events produce actionable detections with bounded latency and sufficient investigation context.

**Mappings**  
OWASP Agentic 2026: ASI02, ASI03, ASI08, ASI10  
NIST AI RMF functions: MEASURE, MANAGE

---

### YAS-10.04 — Containment & Kill Switch
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Provide a tested mechanism to stop agent actions, revoke authority, disable tools, and isolate affected workloads.

**Applies when**
- agent has autonomous or high-impact capabilities

**Threat**  
A compromised or runaway agent may continue acting faster than manual investigation can respond.

**Check**  
Trigger containment during active workflows and verify new actions fail after the containment point.

**Adversarial tests**
- `YAT-IR-001`
- `YAT-RESILIENCE-002`
- `YAT-RESILIENCE-003`
- `YAT-IDENTITY-006`
- `YAT-RESILIENCE-004`

**Required evidence**
- containment procedure
- kill-switch event
- revocation log
- post-containment deny trace

**Pass criteria**  
The documented kill switch reliably halts or isolates affected capabilities and revokes relevant credentials within the response objective.

**Mappings**  
OWASP Agentic 2026: ASI08, ASI10  
NIST AI RMF functions: MANAGE

---

### YAS-10.05 — Incident Evidence Retention & Integrity
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Preserve security evidence with retention, access control, integrity protection, and time synchronization appropriate to investigations.

**Applies when**
- agent operates in production or regulated/sensitive environments

**Threat**  
Attackers or ordinary log rotation may erase or alter the evidence needed to determine impact.

**Check**  
Attempt unauthorized log modification/deletion and verify retention/time consistency across components.

**Adversarial tests**
- `YAT-IR-004`
- `YAT-OBS-002`
- `YAT-OBS-003`

**Required evidence**
- retention policy
- WORM/tamper-evidence setting
- access logs
- time-sync evidence

**Pass criteria**  
Security evidence is access-controlled, integrity-protected or tamper-evident, retained per policy, and time-correlatable.

**Mappings**  
OWASP Agentic 2026: ASI08, ASI10  
NIST AI RMF functions: GOVERN, MEASURE, MANAGE

---
