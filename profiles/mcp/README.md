# Yofune MCP Security Profile

**Profile target:** Model Context Protocol 2026-07-28  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-01.02`
- `YAS-01.03`
- `YAS-03.01`
- `YAS-03.02`
- `YAS-03.03`
- `YAS-03.04`
- `YAS-03.05`
- `YAS-04.01`
- `YAS-04.02`
- `YAS-04.03`
- `YAS-04.04`
- `YAS-04.05`
- `YAS-04.06`
- `YAS-07.02`
- `YAS-10.01`
- `YAS-10.04`

## Profile requirements

1. Inventory every MCP server, endpoint, owner, origin, transport, tool list, and sensitivity classification.
2. Authenticate server identity and restrict connections to approved endpoints/origins.
3. For OAuth deployments, validate authorization issuer responses and bind credentials to the correct issuer/resource.
4. Use least scopes; handle insufficient-scope step-up intentionally rather than granting broad standing scope.
5. Prefer the client identity/registration mechanism required by the targeted specification; for 2026-07-28 review CIMD/client metadata adoption and any compatibility fallback.
6. Isolate credentials per server/resource and prevent model-visible exposure of bearer material.
7. Authorize sensitive tools independently from model reasoning; per-server or per-tool authorization must match risk.
8. Validate tool schemas and semantic constraints before side effects.
9. Treat tool output as untrusted content; never promote it to privileged instruction solely because it came from MCP.
10. Detect tool-name collisions, server substitution, unexpected tool-list changes, and unapproved capability drift.
11. Apply egress/data policy to tool chaining and cross-server data movement.
12. Record server identity, tool name, parameters (with safe redaction), auth decision, scope, result, trace ID, and timestamp.
13. Provide rapid server disablement, token revocation, and tool kill-switch controls.
14. Track MCP specification/SDK changes as a supply-chain/security review trigger.
15. Document enterprise identity/delegation assumptions separately; agent identity is an active area of MCP roadmap work.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
