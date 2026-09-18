# Yofune Customer Service Agent Security Profile

**Profile target:** customer-facing support and service agents  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-02.01`
- `YAS-03.04`
- `YAS-05.02`
- `YAS-05.06`
- `YAS-09.01`
- `YAS-09.05`
- `YAS-10.01`

## Profile requirements

1. Authenticate the customer before exposing account-specific data or actions.
2. Bind delegated authority to the authenticated customer, not the agent service account.
3. Keep knowledge-base content and customer text separate from privileged policy.
4. Require stronger approval/authentication for refunds, account changes, identity changes, or sensitive disclosure.
5. Minimize customer data in prompts, logs, and long-term memory.
6. Prevent one customer conversation from influencing another customer through shared memory.
7. Make escalation to a human clear and preserve case context/evidence.
8. Do not let persuasive agent language substitute for policy or verified account facts.
9. Log outbound messages and account-changing actions with traceability.
10. Test jailbreaks asking the agent to reveal other customers, policies, internal prompts, or perform unauthorized concessions.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
