# YASC 1.0 CI Security Gate

The CI Security Gate turns a bounded Verification Plan into a repeatable pipeline decision.

## Policy example

```yaml
security_gate:
  minimum_test_coverage: 1.0
  fail_on_severities: [critical, high]
  maximum_inconclusive: 0
  require_evidence_integrity: true
  maximum_evidence_age_hours: 24
  required_tests:
    - YAT-INJECTION-001
    - YAT-TOOL-001
```

## Evaluation order

1. Load the Verification Plan and all `verification-run` artifacts.
2. Measure planned test coverage.
3. Check required-test presence.
4. Fail on configured-severity test failures.
5. Enforce the inconclusive-result ceiling.
6. Optionally re-hash every evidence-manifest artifact.
7. Optionally reject stale/undated evidence.
8. Emit a machine-readable gate result and process exit code.

## What a gate PASS means

A PASS means the configured CI policy was met for the exact plan, target state, scenarios, environment, and evidence set. It does not mean the system is certified secure, free of vulnerabilities, or safe outside the evaluated scope.

## GitHub Actions

The repository includes a self-test workflow and a reusable composite action under `.github/actions/yasc-security-gate`. Teams can point the action at their own plan, target, scenario, and policy files. Secrets should be supplied through GitHub Actions secrets/environment variables and referenced from target YAML with `${ENV_VAR}` placeholders.

A recommended deployment pattern is:

- pull request: synthetic/integration target; block merge on gate failure;
- release candidate: staging target plus broader target-specific scenarios;
- production: continuous evidence/telemetry checks and production-safe probes only.
