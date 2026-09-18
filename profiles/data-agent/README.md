# Yofune Data Agent Security Profile

**Profile target:** agents that query, transform, or write structured data  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-01.04`
- `YAS-03.02`
- `YAS-04.02`
- `YAS-04.03`
- `YAS-05.02`
- `YAS-05.06`
- `YAS-09.01`
- `YAS-10.02`

## Profile requirements

1. Separate read, write, DDL/admin, export, and sharing privileges.
2. Use query parameterization and constrained query APIs where feasible.
3. Enforce row/column/tenant authorization outside model reasoning.
4. Require approval for destructive writes, bulk changes, permission changes, or external exports.
5. Apply result-size and export-volume limits.
6. Mask/minimize sensitive columns before model context when full values are unnecessary.
7. Capture query text/template, bound parameters, principal, row/byte counts, and destination.
8. Test prompt-to-SQL injection, query expansion, and cross-tenant joins.
9. Use transactions/rollback or compensation for agent-driven writes where possible.
10. Prevent the agent from using higher-privilege service accounts to satisfy lower-privilege user requests.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
