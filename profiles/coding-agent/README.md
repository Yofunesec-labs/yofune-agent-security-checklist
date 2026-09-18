# Yofune Coding Agent Security Profile

**Profile target:** agents that read/write code or execute developer tooling  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-02.02`
- `YAS-03.02`
- `YAS-04.03`
- `YAS-04.04`
- `YAS-05.04`
- `YAS-06.01`
- `YAS-06.02`
- `YAS-06.03`
- `YAS-06.04`
- `YAS-06.05`
- `YAS-07.02`
- `YAS-07.05`
- `YAS-09.01`
- `YAS-10.04`

## Profile requirements

1. Treat repository content, issues, comments, READMEs, generated files, and dependency metadata as untrusted instructions.
2. Run code/tests/builds in an isolated sandbox with no ambient production credentials.
3. Restrict network egress and protect cloud/CI metadata endpoints.
4. Use parameterized command execution; do not concatenate model text into shell commands.
5. Gate package installation and dependency changes with provenance and policy.
6. Require explicit approval for pushes, merges, releases, deployments, secret changes, and destructive operations.
7. Separate read-only repository access from write/admin scopes.
8. Prevent project content from writing durable global agent instructions/memory without validation.
9. Scan generated patches/artifacts for secrets and unexpected binary/executable additions.
10. Pin or approve toolchains, compilers, package registries, and MCP coding servers.
11. Capture command, cwd, environment class, files changed, network destinations, and exit status.
12. Support immediate cancellation and credential revocation.
13. Test path traversal, symlink, workspace escape, and command injection.
14. Do not allow an agent to self-approve security-sensitive changes it generated.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
