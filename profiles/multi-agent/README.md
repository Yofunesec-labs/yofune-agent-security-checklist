# Yofune Multi-Agent Security Profile

**Profile target:** systems with agent-to-agent messaging or delegation  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-03.04`
- `YAS-08.01`
- `YAS-08.02`
- `YAS-08.03`
- `YAS-08.04`
- `YAS-08.05`
- `YAS-10.02`
- `YAS-10.04`

## Profile requirements

1. Assign verifiable identities to agent workloads.
2. Authenticate message sender and destination.
3. Define typed message schemas and reject unknown control fields.
4. Preserve original source/provenance when forwarding information.
5. Constrain delegated scopes to the parent’s authority and task.
6. Limit recursion, delegation depth, retries, fan-out, compute, and financial budgets.
7. Do not automatically trust a message because it came through a trusted intermediate agent.
8. Record principal/delegation chains end-to-end.
9. Isolate shared memory and tools by tenant/workflow.
10. Use circuit breakers for repeated errors and conflicting agent loops.
11. Define quorum/human escalation for high-impact multi-agent decisions where appropriate.
12. Test spoofing, privilege amplification, taint laundering, and cascading failure.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
