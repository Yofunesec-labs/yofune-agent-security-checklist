# Yofune Enterprise Copilot Security Profile

**Profile target:** enterprise copilots connected to SaaS, documents, messaging, and business systems  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-01.02`
- `YAS-03.01`
- `YAS-03.02`
- `YAS-03.04`
- `YAS-04.03`
- `YAS-05.02`
- `YAS-05.06`
- `YAS-09.01`
- `YAS-10.01`
- `YAS-10.04`

## Profile requirements

1. Use enterprise/workload identity and preserve the represented user principal.
2. Intersect agent capability with user authorization; never widen access through the copilot service identity.
3. Inventory every connected SaaS/data source and classify read/write/export capability.
4. Apply tenant and document ACLs before data enters model context.
5. Separate personal and enterprise identities/sessions to avoid cross-account data flow.
6. Require approval for external send, sharing, permission changes, destructive edits, and administrative actions.
7. Apply DLP/egress policy to generated messages, files, and tool calls.
8. Keep connector/tool output untrusted for instruction purposes.
9. Record connector, principal, resource, action, policy decision, and outcome.
10. Provide centralized connector disablement and token revocation.
11. Test indirect injection from email/docs/tickets that tries to trigger another connector.
12. Review enterprise MCP/connector authorization against the current protocol and identity roadmap.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
