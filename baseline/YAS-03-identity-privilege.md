# YAS-03 — Identity & Privilege
> **Core question:** Under whose identity does the agent act, and with what authority?
> **Principle:** Use dedicated identities, least privilege, constrained delegation, and short-lived credentials.

## Controls

### YAS-03.01 — Dedicated Agent Identity
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Give production agents attributable workload identities rather than shared human or application credentials.

**Applies when**
- agent accesses authenticated systems

**Threat**  
Shared identities prevent attribution and allow agents to inherit authority intended for people or unrelated services.

**Check**  
Inspect credentials used for tool and service calls and correlate them to a specific agent workload.

**Adversarial tests**
- `YAT-IDENTITY-001`

**Required evidence**
- identity record
- token claims
- service logs
- ownership record

**Pass criteria**  
Production actions use attributable agent/workload identities; shared secrets are not the default identity mechanism.

**Mappings**  
OWASP Agentic 2026: ASI03  
NIST AI RMF functions: GOVERN, MANAGE

---

### YAS-03.02 — Least Privilege
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Limit each agent and tool to the minimum permissions, resources, operations, and data scope required.

**Applies when**
- agent can access protected data or perform authenticated actions

**Threat**  
Compromise or goal hijack causes disproportionate impact when the agent holds broad standing authority.

**Check**  
Enumerate effective permissions and attempt representative actions outside the documented task scope.

**Adversarial tests**
- `YAT-TOOL-006`
- `YAT-IDENTITY-004`

**Required evidence**
- effective permission export
- deny trace
- role/policy definition
- exception approval

**Pass criteria**  
Out-of-scope actions are denied at an enforcement point independent of model judgment.

**Mappings**  
OWASP Agentic 2026: ASI02, ASI03  
NIST AI RMF functions: MAP, MANAGE

---

### YAS-03.03 — Credential Isolation
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Isolate credentials by agent, environment, tenant, and target service; never expose raw secrets to untrusted context.

**Applies when**
- agent uses tokens, API keys, certificates, or delegated credentials

**Threat**  
Credentials can leak through prompts, memory, logs, tool outputs, or be reused by the wrong agent or tenant.

**Check**  
Attempt credential reuse across agents/tenants and inspect prompts, logs, traces, and memory for secret material.

**Adversarial tests**
- `YAT-IDENTITY-001`
- `YAT-IDENTITY-004`

**Required evidence**
- secret manager policy
- token claims
- redacted trace
- negative test result

**Pass criteria**  
Credentials are scoped and non-exportable where possible; cross-context reuse fails; secret values are absent from model-visible context.

**Mappings**  
OWASP Agentic 2026: ASI03, ASI06  
NIST AI RMF functions: MANAGE

---

### YAS-03.04 — Delegation & Impersonation Control
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Constrain on-behalf-of delegation and prevent an agent from silently impersonating a human or higher-privilege principal.

**Applies when**
- agent acts on behalf of users or other agents

**Threat**  
Confused-deputy flows can turn user intent into broader delegated authority.

**Check**  
Test delegation chains, principal switching, and requests where agent and user authority differ.

**Adversarial tests**
- `YAT-IDENTITY-003`
- `YAT-MULTI-002`
- `YAT-APPROVAL-003`
- `YAT-IDENTITY-005`

**Required evidence**
- delegation token/claims
- policy decision
- principal chain
- audit log

**Pass criteria**  
The acting agent, represented user, delegated scopes, and target resource are all explicit and validated.

**Mappings**  
OWASP Agentic 2026: ASI03, ASI07  
NIST AI RMF functions: MAP, MANAGE

---

### YAS-03.05 — Credential Lifetime, Rotation & Revocation
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Use bounded credential lifetimes with rotation and rapid revocation for agent access.

**Applies when**
- agent has reusable authenticated access

**Threat**  
Long-lived credentials prolong compromise and undermine containment.

**Check**  
Validate expiry enforcement, token refresh boundaries, rotation behavior, and emergency revocation.

**Adversarial tests**
- `YAT-IDENTITY-002`
- `YAT-IR-001`
- `YAT-IDENTITY-006`
- `YAT-RESILIENCE-004`

**Required evidence**
- credential policy
- expiry test
- revocation trace
- rotation log

**Pass criteria**  
Expired/revoked credentials fail closed; rotation does not widen scope; emergency revocation meets the documented response objective.

**Mappings**  
OWASP Agentic 2026: ASI03, ASI08  
NIST AI RMF functions: MANAGE

---
