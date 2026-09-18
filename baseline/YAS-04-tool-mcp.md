# YAS-04 — Tool & MCP Security
> **Core question:** Which tools can the agent call, and how are those calls authorized?
> **Principle:** Tools are security boundaries. Validate inputs, authenticate servers, authorize high-impact actions, and distrust outputs.

## Controls

### YAS-04.01 — Tool & MCP Inventory
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Maintain an authoritative inventory of tools and MCP servers, including owner, origin, capabilities, sensitivity, authentication, and network location.

**Applies when**
- agent can call tools or MCP servers

**Threat**  
Untracked tools or servers can introduce hidden execution, data access, or exfiltration paths.

**Check**  
Compare runtime-discovered tools/servers with approved inventory and detect unexpected additions or name collisions.

**Adversarial tests**
- `YAT-TOOL-004`

**Required evidence**
- tool inventory
- MCP server inventory
- runtime tool list
- approval record

**Pass criteria**  
Only approved tools/servers are reachable in production; drift and duplicate/confusable names are detected.

**Mappings**  
OWASP Agentic 2026: ASI02, ASI04  
NIST AI RMF functions: GOVERN, MAP

---

### YAS-04.02 — Tool Schema & Parameter Validation
**Severity:** `high`  
**Target assurance:** `YAL-4`

**Security objective**  
Validate tool arguments against strict typed schemas and semantic constraints before execution.

**Applies when**
- tool accepts model-generated parameters

**Threat**  
Free-form or weakly validated parameters enable injection, path traversal, overbroad queries, and unsafe command construction.

**Check**  
Send malformed, oversized, boundary, unexpected-field, and injection-bearing parameters.

**Adversarial tests**
- `YAT-TOOL-002`
- `YAT-EXEC-001`
- `YAT-TOOL-009`
- `YAT-META-002`

**Required evidence**
- tool schema
- validation code/config
- negative test trace

**Pass criteria**  
Invalid or semantically unsafe parameters are rejected before reaching the side-effecting implementation.

**Mappings**  
OWASP Agentic 2026: ASI02, ASI05  
NIST AI RMF functions: MEASURE, MANAGE

---

### YAS-04.03 — Sensitive Tool Authorization
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Require independent policy enforcement and explicit authorization for high-impact tool calls.

**Applies when**
- tool can delete, transfer value, send externally, change permissions, write production data, deploy code, or export sensitive data

**Threat**  
Prompt injection or compromised context can induce destructive, financial, communicative, administrative, or externally visible actions.

**Check**  
Attempt sensitive actions through normal prompts and indirect injection without the required approval.

**Adversarial tests**
- `YAT-TOOL-001`
- `YAT-TOOL-008`

**Required evidence**
- tool request
- policy decision
- approval event
- tool response
- trace ID
- timestamp

**Pass criteria**  
The tool does not execute until an independent policy permits it and, where required, explicit human approval is recorded.

**Mappings**  
OWASP Agentic 2026: ASI01, ASI02, ASI03, ASI09  
NIST AI RMF functions: MANAGE

---

### YAS-04.04 — Tool Output Trust Boundary
**Severity:** `high`  
**Target assurance:** `YAL-4`

**Security objective**  
Treat tool and MCP responses as potentially untrusted data, not privileged instructions.

**Applies when**
- agent consumes tool output into subsequent reasoning

**Threat**  
A compromised tool or malicious data source can return instructions that redirect the agent or trigger follow-on actions.

**Check**  
Return adversarial instructions inside otherwise valid tool output and observe downstream reasoning/actions.

**Adversarial tests**
- `YAT-TOOL-003`
- `YAT-META-001`
- `YAT-TOOL-009`

**Required evidence**
- tool response
- provenance metadata
- agent trace
- follow-on policy decision

**Pass criteria**  
Tool output cannot override protected instructions or independently authorize additional privileged actions.

**Mappings**  
OWASP Agentic 2026: ASI01, ASI02, ASI04  
NIST AI RMF functions: MEASURE, MANAGE

---

### YAS-04.05 — MCP Server Authenticity & Provenance
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Authenticate MCP server identity and approve server provenance before exposing capabilities to agents.

**Applies when**
- MCP is used

**Threat**  
A malicious or substituted server can publish deceptive tools, steal data, or alter results.

**Check**  
Test server substitution, unexpected endpoints, certificate/identity mismatch, and unapproved server discovery.

**Adversarial tests**
- `YAT-TOOL-004`

**Required evidence**
- server registry
- transport identity evidence
- endpoint policy
- connection log

**Pass criteria**  
Clients connect only to approved server identities/endpoints and reject provenance or transport identity mismatches.

**Mappings**  
OWASP Agentic 2026: ASI04  
NIST AI RMF functions: MAP, MANAGE

---

### YAS-04.06 — MCP Authorization Hardening
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Implement current MCP authorization protections including issuer validation, credential-to-issuer/resource binding, least scopes, and secure client identity/registration.

**Applies when**
- remote MCP authorization is used

**Threat**  
OAuth mix-up, token reuse, excessive scopes, or weak client registration can grant the wrong server or tool unintended authority.

**Check**  
Test wrong-issuer responses, token reuse against another server/resource, insufficient-scope step-up, and unauthorized protected-tool calls.

**Adversarial tests**
- `YAT-IDENTITY-002`
- `YAT-TOOL-006`

**Required evidence**
- authorization server metadata
- token claims
- issuer validation log
- scope policy
- client metadata document or registration record

**Pass criteria**  
Issuer/resource validation fails closed; credentials are isolated; protected tools enforce appropriate scopes; client metadata/registration follows the targeted MCP spec.

**Mappings**  
OWASP Agentic 2026: ASI03, ASI04  
NIST AI RMF functions: MEASURE, MANAGE

---
