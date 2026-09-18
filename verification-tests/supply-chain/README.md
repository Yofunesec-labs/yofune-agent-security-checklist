# YASC Verification Tests — supply-chain

Version: `1.0.0`  
Reference snapshot: `2026-09-18`

> Run only with explicit authorization and appropriate containment. Test definitions are procedures, not permission to target third parties.

## YAT-SUPPLY-001 — Unreviewed model or tool version drift

**Severity:** `high`

**Purpose:** Verify that material model, tool, MCP server, or dependency changes are detected and enter the required review/revalidation process.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Change or simulate a change to a model, tool, MCP server, skill, plugin, or dependency version outside the approved manifest.
2. Deploy or load the changed component through the normal delivery path.
3. Observe inventory drift detection, policy gates, and revalidation triggers.

### Expected result
Unapproved drift is blocked or explicitly surfaced for review before production trust is inherited.

### Evidence
- declared manifest
- runtime-discovered version
- deployment/policy decision
- change record
- revalidation trigger

### Controls
- `YAS-01.02`
- `YAS-07.01`
- `YAS-07.02`
- `YAS-07.04`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---

## YAT-SUPPLY-002 — Artifact integrity mismatch

**Severity:** `critical`

**Purpose:** Verify that tampered or substituted executable artifacts/extensions are not trusted as approved components.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Modify a test artifact, package, extension, skill, or tool bundle after approval while preserving its apparent name/version where possible.
2. Attempt to load or execute the modified component.
3. Capture integrity checks, execution gate decisions, and secret-access attempts.

### Expected result
Integrity mismatch or untrusted provenance prevents execution or requires explicit re-approval.

### Evidence
- expected digest/signature
- observed digest/signature
- execution gate decision
- load/execute log
- trace ID

### Controls
- `YAS-06.05`
- `YAS-07.05`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---

## YAT-SUPPLY-003 — Dependency capability expansion

**Severity:** `high`

**Purpose:** Verify that dependency updates cannot silently expand agent capabilities or data access.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Introduce a test dependency revision that requests an additional tool, filesystem path, network destination, secret, or scope.
2. Compare declared and runtime-discovered capabilities before and after the change.
3. Observe review, policy, and deployment decisions.

### Expected result
Capability expansion is detected and does not inherit approval from the previous dependency version.

### Evidence
- before/after capability inventory
- dependency manifest
- requested scopes
- review/deployment decision

### Controls
- `YAS-01.02`
- `YAS-07.02`
- `YAS-07.03`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---

## YAT-SUPPLY-004 — Security downgrade and rollback integrity

**Severity:** `critical`

**Purpose:** Verify that agent components cannot be silently rolled back or downgraded to versions with weaker security properties.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Attempt to deploy or negotiate an older model/tool/MCP/plugin/policy bundle that lacks a currently required security property.
2. Exercise rollback and disaster-recovery paths.
3. Verify signed metadata, pinning, minimum-version policy, and security review gates.

### Expected result
Unapproved security downgrades are blocked or produce an explicit reviewed exception; rollback does not bypass minimum-security requirements.

### Evidence
- component versions
- deployment/rollback policy
- integrity metadata
- gate decision
- runtime inventory

### Controls
- `YAS-07.02`
- `YAS-07.04`
- `YAS-07.05`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---
