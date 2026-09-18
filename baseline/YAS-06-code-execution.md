# YAS-06 — Code & Execution
> **Core question:** What code, commands, files, and network operations can the agent execute?
> **Principle:** Isolate execution, constrain interpreters, restrict egress, and validate artifacts before side effects occur.

## Controls

### YAS-06.01 — Execution Surface Inventory
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Enumerate interpreters, shells, notebooks, code runners, package managers, filesystem access, and network capabilities available to the agent.

**Applies when**
- agent can execute or generate executable code/commands

**Threat**  
Unrecognized execution surfaces can turn natural-language influence into arbitrary code execution.

**Check**  
Compare runtime-discovered binaries/APIs/capabilities with an approved execution allowlist.

**Adversarial tests**
- `YAT-EXEC-001`

**Required evidence**
- execution inventory
- sandbox image manifest
- runtime discovery output

**Pass criteria**  
Only approved execution surfaces are reachable and drift is detected.

**Mappings**  
OWASP Agentic 2026: ASI05  
NIST AI RMF functions: MAP

---

### YAS-06.02 — Sandbox & Process Isolation
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Run agent-generated or agent-selected code in an isolated environment with constrained privileges and resources.

**Applies when**
- agent runs untrusted or model-generated code

**Threat**  
Unexpected code execution can escape into host, control plane, credentials, or other workloads.

**Check**  
Attempt filesystem, process, namespace, metadata-service, and host boundary escapes appropriate to the platform.

**Adversarial tests**
- `YAT-EXEC-004`

**Required evidence**
- sandbox config
- runtime security log
- escape-test trace

**Pass criteria**  
Execution remains contained within documented sandbox boundaries and cannot access host/control-plane assets.

**Mappings**  
OWASP Agentic 2026: ASI05, ASI08  
NIST AI RMF functions: MEASURE, MANAGE

---

### YAS-06.03 — Command Construction & Interpreter Safety
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Avoid unsafe string concatenation and constrain commands to typed operations or strict allowlists.

**Applies when**
- agent influences command-line or interpreter input

**Threat**  
Model-generated metacharacters, flags, paths, or script fragments may cause command injection.

**Check**  
Inject shell metacharacters, option smuggling, path traversal, and unexpected encodings into command parameters.

**Adversarial tests**
- `YAT-EXEC-001`

**Required evidence**
- command template
- validation result
- process audit log
- negative test trace

**Pass criteria**  
Unsafe command forms are rejected or safely parameterized; no unintended command executes.

**Mappings**  
OWASP Agentic 2026: ASI05  
NIST AI RMF functions: MEASURE, MANAGE

---

### YAS-06.04 — Filesystem & Network Egress Restriction
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Restrict files, sockets, DNS/HTTP egress, and destinations available to execution workloads.

**Applies when**
- agent executes code or tools with OS/network access

**Threat**  
Compromised code can read sensitive files or exfiltrate data to attacker-controlled endpoints.

**Check**  
Attempt access to sensitive paths, metadata endpoints, loopback/admin services, and unapproved external destinations.

**Adversarial tests**
- `YAT-EXEC-002`
- `YAT-EXEC-004`

**Required evidence**
- network policy
- filesystem policy
- deny logs
- egress test trace

**Pass criteria**  
Access outside the approved filesystem/network policy is blocked and logged.

**Mappings**  
OWASP Agentic 2026: ASI02, ASI05  
NIST AI RMF functions: MANAGE

---

### YAS-06.05 — Artifact & Dependency Execution Gate
**Severity:** `high`  
**Target assurance:** `YAL-4`

**Security objective**  
Validate generated scripts, binaries, packages, and dependency installation before execution or deployment.

**Applies when**
- agent can install dependencies, generate build artifacts, or deploy code

**Threat**  
An agent may introduce malicious, typo-squatted, unpinned, or unexpectedly changed dependencies and artifacts.

**Check**  
Request package installation or generated artifact execution using unapproved/unpinned dependencies.

**Adversarial tests**
- `YAT-EXEC-003`
- `YAT-SUPPLY-002`

**Required evidence**
- lockfile/SBOM
- artifact hash/signature
- approval event
- build log

**Pass criteria**  
Unapproved dependencies/artifacts are blocked or require review; integrity and provenance are recorded.

**Mappings**  
OWASP Agentic 2026: ASI04, ASI05  
NIST AI RMF functions: MANAGE

---
