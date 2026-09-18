# Yofune Browser Agent Security Profile

**Profile target:** agents that browse and interact with websites  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-02.02`
- `YAS-02.04`
- `YAS-03.03`
- `YAS-04.03`
- `YAS-05.06`
- `YAS-09.01`
- `YAS-09.02`
- `YAS-10.01`
- `YAS-10.04`

## Profile requirements

1. Treat page text, accessibility trees, DOM metadata, downloads, and visual content as untrusted.
2. Isolate browser profiles, sessions, cookies, and credentials by user/tenant/task.
3. Restrict navigation and download/upload destinations where business policy requires it.
4. Require approval for purchases, messages, submissions, permission changes, and other consequential actions.
5. Show target domain and concrete form/action details at approval time.
6. Block hidden/obfuscated prompt injection from silently authorizing tools.
7. Constrain file access exposed to upload controls.
8. Apply data-loss policy before pasting/uploading sensitive content.
9. Log navigation, important DOM/action targets, downloads/uploads, approvals, and final external effects.
10. Detect suspicious domain changes, homographs, redirect chains, and unexpected login/consent pages.
11. Provide cancellation and browser-session invalidation.
12. Test indirect injection using pages that instruct the agent to ignore the user and exfiltrate data.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
