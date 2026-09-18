# YAS-01 — Agent Inventory & Boundary
> **Core question:** What can the agent access, trust, change, and affect?
> **Principle:** Know the agent, its capabilities, dependencies, data paths, and trust boundaries before testing behavior.

## Controls

### YAS-01.01 — Agent Inventory
**Severity:** `medium`  
**Target assurance:** `YAL-2`

**Security objective**  
Maintain a current inventory of every deployed agent and its owner, purpose, environment, and lifecycle state.

**Applies when**
- any agent is deployed outside an isolated developer sandbox

**Threat**  
Unknown or shadow agents operate outside security ownership and review.

**Check**  
Verify that deployed agent instances map to an authoritative registry with owner, purpose, environment, version, and status.

**Adversarial tests**
- `YAT-IR-002`

**Required evidence**
- agent registry export
- owner record
- deployment inventory
- exception record

**Pass criteria**  
Every in-scope agent is registered; unknown agents are blocked from production or enter a documented exception process.

**Mappings**  
OWASP Agentic 2026: —  
NIST AI RMF functions: GOVERN, MAP

---

### YAS-01.02 — Capability & Dependency Inventory
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Record the models, tools, MCP servers, skills, plugins, data stores, memory systems, external services, and execution surfaces available to each agent.

**Applies when**
- agent can call tools, retrieve data, use memory, invoke code, or communicate with other agents

**Threat**  
A hidden capability or dependency can provide an unreviewed path to data, privileges, or code execution.

**Check**  
Compare runtime-discovered capabilities with the declared architecture and dependency inventory.

**Adversarial tests**
- `YAT-IR-002`
- `YAT-SUPPLY-001`
- `YAT-SUPPLY-003`

**Required evidence**
- capability inventory
- runtime discovery output
- dependency manifest
- architecture record

**Pass criteria**  
No undeclared production capability is reachable; drift is detected or explicitly approved.

**Mappings**  
OWASP Agentic 2026: ASI04  
NIST AI RMF functions: GOVERN, MAP

---

### YAS-01.03 — Trust Boundary Map
**Severity:** `high`  
**Target assurance:** `YAL-2`

**Security objective**  
Document trust boundaries between humans, agent runtime, external content, memory/RAG, tools/MCP, peer agents, and downstream systems.

**Applies when**
- agent consumes any external or multi-source input

**Threat**  
Security decisions fail when untrusted content silently crosses into trusted instruction, data, identity, or privilege planes.

**Check**  
Review the architecture for explicit identity, data, instruction, privilege, trust, and evidence boundaries.

**Adversarial tests**
- `YAT-INJECTION-002`
- `YAT-MULTI-001`

**Required evidence**
- trust-boundary diagram
- data-flow diagram
- control-point inventory

**Pass criteria**  
All meaningful trust crossings are identified with an enforcing component and owner.

**Mappings**  
OWASP Agentic 2026: ASI01, ASI02, ASI06, ASI07  
NIST AI RMF functions: MAP

---

### YAS-01.04 — Data Classification & Flow
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Classify sensitive data the agent can read, derive, store, transmit, or expose and map allowed destinations.

**Applies when**
- agent processes confidential, personal, regulated, proprietary, or credential data

**Threat**  
The agent may exfiltrate or over-share data because data sensitivity and destination policy are implicit.

**Check**  
Trace representative sensitive records from source through prompts, context, memory, logs, tools, and external calls.

**Adversarial tests**
- `YAT-TOOL-005`
- `YAT-EXEC-002`

**Required evidence**
- data classification policy
- flow trace
- DLP/policy logs
- egress policy

**Pass criteria**  
Sensitive data has explicit handling rules, permitted destinations, and enforcement at relevant egress points.

**Mappings**  
OWASP Agentic 2026: ASI02, ASI03, ASI06  
NIST AI RMF functions: MAP, MANAGE

---

### YAS-01.05 — Environment & Tenant Boundary
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Prevent agent state, credentials, memory, files, and retrieved data from crossing environment or tenant boundaries.

**Applies when**
- multi-tenant, multi-user, or multi-environment deployment exists

**Threat**  
A shared runtime or retrieval layer can leak one tenant’s data or authority into another tenant or environment.

**Check**  
Attempt cross-tenant and cross-environment retrieval, memory access, credential use, and tool execution.

**Adversarial tests**
- `YAT-IDENTITY-004`
- `YAT-MEMORY-003`

**Required evidence**
- isolation configuration
- authorization decision
- negative test trace
- tenant-scoped logs

**Pass criteria**  
Cross-boundary access is denied by technical controls and produces attributable security telemetry.

**Mappings**  
OWASP Agentic 2026: ASI03, ASI06, ASI08  
NIST AI RMF functions: MAP, MEASURE, MANAGE

---
