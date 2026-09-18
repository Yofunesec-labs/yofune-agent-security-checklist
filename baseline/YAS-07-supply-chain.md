# YAS-07 — Agentic Supply Chain
> **Core question:** Can models, tools, skills, servers, packages, or data dependencies be trusted?
> **Principle:** Track provenance, pin dependencies, inventory components, and review changes across the agentic stack.

## Controls

### YAS-07.01 — Model & Provider Provenance
**Severity:** `high`  
**Target assurance:** `YAL-2`

**Security objective**  
Record model/provider identity, version, deployment mode, security-relevant settings, and change history.

**Applies when**
- agent depends on hosted or self-hosted models

**Threat**  
Untracked model/provider changes can alter behavior, retention, tool use, or security assumptions.

**Check**  
Compare deployed model configuration and provider endpoint with approved records.

**Adversarial tests**
- `YAT-IR-002`
- `YAT-SUPPLY-001`
- `YAT-DIFF-001`

**Required evidence**
- model inventory
- provider contract/config
- deployment manifest
- change log

**Pass criteria**  
Model/provider changes are attributable, reviewed, and detectable.

**Mappings**  
OWASP Agentic 2026: ASI04  
NIST AI RMF functions: GOVERN, MAP

---

### YAS-07.02 — Tool, MCP, Skill & Plugin Dependency Pinning
**Severity:** `high`  
**Target assurance:** `YAL-3`

**Security objective**  
Pin or otherwise constrain versions and origins of agent extensions and review updates before promotion.

**Applies when**
- agent loads external tools, MCP servers, skills, plugins, or packages

**Threat**  
A compromised or silently changed extension can gain trusted access through the agent.

**Check**  
Introduce an unexpected version/source or mutate a dependency reference in a controlled environment.

**Adversarial tests**
- `YAT-TOOL-004`
- `YAT-EXEC-003`
- `YAT-SUPPLY-001`
- `YAT-SUPPLY-003`
- `YAT-SUPPLY-004`

**Required evidence**
- lockfile/manifest
- registry policy
- integrity verification
- change approval

**Pass criteria**  
Production resolves only approved sources/versions and detects integrity drift.

**Mappings**  
OWASP Agentic 2026: ASI04  
NIST AI RMF functions: MANAGE

---

### YAS-07.03 — AIBOM/SBOM & Component Traceability
**Severity:** `medium`  
**Target assurance:** `YAL-2`

**Security objective**  
Maintain machine-readable component inventories covering models, software, tools, MCP servers, data dependencies, and critical runtime services.

**Applies when**
- production agent has third-party or versioned components

**Threat**  
Incident response and exposure analysis are delayed when affected components cannot be enumerated.

**Check**  
Verify that a named component/version can be traced to all affected agent deployments.

**Adversarial tests**
- `YAT-IR-002`
- `YAT-SUPPLY-003`

**Required evidence**
- AIBOM/SBOM
- deployment mapping
- component ownership

**Pass criteria**  
Component inventory is current enough to answer exposure queries and is tied to deployments/releases.

**Mappings**  
OWASP Agentic 2026: ASI04  
NIST AI RMF functions: GOVERN, MAP

---

### YAS-07.04 — Security Update & Review Lifecycle
**Severity:** `high`  
**Target assurance:** `YAL-2`

**Security objective**  
Monitor security-relevant changes to protocols, models, SDKs, dependencies, and threat frameworks and review their impact.

**Applies when**
- agent relies on actively evolving external components or standards

**Threat**  
A previously acceptable configuration may become unsafe as protocols and dependencies evolve.

**Check**  
Inspect whether significant upstream security changes trigger documented review and regression tests.

**Adversarial tests**
- `YAT-IR-002`
- `YAT-SUPPLY-001`
- `YAT-DIFF-001`
- `YAT-SUPPLY-004`

**Required evidence**
- dependency alerts
- review record
- regression result
- risk acceptance

**Pass criteria**  
Critical upstream changes have an owner, review outcome, and tracked remediation or accepted risk.

**Mappings**  
OWASP Agentic 2026: ASI04  
NIST AI RMF functions: GOVERN, MANAGE

---

### YAS-07.05 — Extension Integrity & Secret Hygiene
**Severity:** `critical`  
**Target assurance:** `YAL-4`

**Security objective**  
Verify extension artifacts/configuration and prevent embedded credentials or unauthorized secret access.

**Applies when**
- agent loads executable extensions or third-party configuration

**Threat**  
Malicious packages, skills, or server configs can tamper with behavior or harvest credentials.

**Check**  
Scan extensions for integrity drift, embedded secrets, unexpected network destinations, and secret access.

**Adversarial tests**
- `YAT-EXEC-003`
- `YAT-IDENTITY-001`
- `YAT-SUPPLY-002`
- `YAT-SUPPLY-004`

**Required evidence**
- artifact hash/signature
- secret scan
- runtime secret access log
- network manifest

**Pass criteria**  
Integrity failures or secret leakage are blocked; extensions receive only explicitly required secret access.

**Mappings**  
OWASP Agentic 2026: ASI03, ASI04  
NIST AI RMF functions: MEASURE, MANAGE

---
