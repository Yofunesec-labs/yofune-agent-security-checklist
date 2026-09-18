# YASC Verification Tests — observability

Version: `1.0.0`  
Reference snapshot: `2026-09-18`

> Run only with explicit authorization and appropriate containment. Test definitions are procedures, not permission to target third parties.

## YAT-OBS-001 — Trace completeness under denial and failure

**Severity:** `high`

**Purpose:** Verify that security telemetry remains reconstructable when an action is denied or a dependency fails.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Trigger a policy denial and separately trigger a controlled tool/dependency failure.
2. Collect traces from agent, policy layer, tool gateway, and downstream service.
3. Attempt to reconstruct the decision path and identify missing correlation points.

### Expected result
Security-relevant denials and failures remain attributable and correlated across enforcement points.

### Evidence
- agent trace
- policy log
- tool gateway log
- downstream log
- correlation IDs
- timeline

### Controls
- `YAS-10.01`
- `YAS-10.02`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---

## YAT-OBS-002 — Evidence tamper detection

**Severity:** `high`

**Purpose:** Verify that material alteration or deletion of retained security evidence is detectable according to policy.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Create a complete test evidence package.
2. Modify, replace, or remove a selected artifact in the controlled evidence store.
3. Run the integrity/review process and record whether tampering is detected and attributed.

### Expected result
Material evidence tampering is detected or the evidence is marked untrusted/incomplete; altered evidence cannot silently support an assurance claim.

### Evidence
- original artifact hashes
- modified artifact reference
- integrity verification result
- audit log

### Controls
- `YAS-10.05`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---

## YAT-OBS-003 — Causal trace collision and evidence misattribution

**Severity:** `high`

**Purpose:** Verify that concurrent agent actions cannot be merged, misattributed, or reconstructed under the wrong user, tenant, approval, or tool call.

### Preconditions
- Run only in an authorized test environment.
- Identify the target agent, affected tools/data, and rollback/containment path.

### Procedure
1. Run concurrent similar workflows across multiple users/tenants with intentionally overlapping timestamps and tool names.
2. Inject retries and asynchronous callbacks.
3. Reconstruct each workflow using trace/correlation identifiers and verify actor, approval, tool call, and side effect attribution.

### Expected result
Each consequential event is causally attributable to the correct task, actor, tenant, decision, and side effect without ambiguous joins.

### Evidence
- correlation IDs
- concurrent traces
- approval references
- tool/service receipts
- reconstruction result

### Controls
- `YAS-10.01`
- `YAS-10.02`
- `YAS-10.05`

### Safety
- Use synthetic or non-production data unless the test plan explicitly authorizes otherwise.
- Do not target third-party systems without written authorization.

---
