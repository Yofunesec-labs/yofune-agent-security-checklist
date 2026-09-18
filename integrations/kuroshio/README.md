# KUROSHIO Integration Contract (Draft)

The YASC baseline is vendor-neutral. This directory defines an optional adapter shape for tools such as KUROSHIO to emit evidence without changing baseline semantics.

## Input
A runner selects one or more `YAT-*` tests and supplies a scoped target configuration outside this repository.

## Result envelope

```json
{
  "schema": "yasc-result/1.0",
  "test_id": "YAT-TOOL-001",
  "controls": ["YAS-04.03", "YAS-09.01"],
  "target": {"agent": "example-agent", "environment": "staging"},
  "started_at": "2026-09-18T00:00:00Z",
  "finished_at": "2026-09-18T00:00:03Z",
  "outcome": "pass",
  "trace_id": "...",
  "evidence": [
    {"type": "policy_decision", "ref": "..."},
    {"type": "tool_call", "ref": "..."},
    {"type": "approval_event", "ref": "..."}
  ],
  "notes": ""
}
```

## Rules

- The runner must not redefine `YAS-*` pass criteria.
- Evidence references should be immutable or integrity-verifiable where practical.
- Secrets and sensitive payloads should be redacted from exported evidence while preserving reviewability.
- Automated `pass` means the test's expected result was observed for the stated scope; it does not imply whole-agent certification.
