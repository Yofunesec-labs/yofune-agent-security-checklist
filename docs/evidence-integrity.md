# YASC Evidence Integrity and Chain of Custody

**Revision:** 1.0

YASC evidence should allow another reviewer to reconstruct not only the output, but the security-relevant causal chain.

## Evidence classes

- **Input evidence:** prompts, documents, retrieved content, peer messages, payload/variant identifiers.
- **Identity evidence:** principal, delegation chain, credential metadata, tenant/environment.
- **Decision evidence:** policy, authorization, approval, schema validation, sandbox/egress decisions.
- **Execution evidence:** tool/MCP request and response, command, queue event, worker execution.
- **Side-effect evidence:** downstream receipt, resource version, database record, sent-message ID, deployment/event result.
- **Containment evidence:** cancellation, revocation, kill-switch, queue drain, rollback/compensation.
- **Integrity evidence:** hashes, collection time, source component, access controls, time synchronization, redaction record.

## Minimum evidence principle

Collect enough evidence to support the claim, but avoid indiscriminate capture of secrets, personal data, model internals, or unrelated customer content. Evidence minimization and evidence sufficiency must be balanced explicitly.

## Artifact integrity

For high-impact claims, preserve a manifest containing SHA-256 hashes, sizes, logical artifact types, trace identifiers, and collection metadata. Hashes do not prove that a source system told the truth, but they make later modification of the collected artifact detectable.

## Redaction

Redaction must preserve decision-relevant fields. A reviewer should be able to see what resource, identity class, policy result, action digest, timestamp, and outcome were involved even when sensitive values are removed.

## Time

Distributed evidence is difficult to reconstruct when clocks diverge. Production-grade verification should record time synchronization assumptions and prefer monotonic/correlation data in addition to wall-clock timestamps.
