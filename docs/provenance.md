# Provenance, Originality, and External Basis

YASC is designed as an engineering baseline built on established public security knowledge. It does **not** claim to have invented the underlying classes of risk such as least privilege, prompt injection, supply-chain risk, sandboxing, audit logging, or human approval.

## External foundations

The 2026 reference snapshot uses, among others:

- OWASP Top 10 for Agentic Applications 2026 for agentic risk categories.
- OWASP Agent Control Standard (ACS) for runtime inspectability, traceability, instrumentation, and policy-control concepts.
- OWASP AI Red Teaming materials for the distinction between meaningful adversarial testing and jailbreak-only exercises.
- Model Context Protocol 2026-07-28 materials for protocol-specific authorization and identity requirements.
- NIST AI RMF 1.0 and NIST AI 600-1 for governance, mapping, measurement, and management context.
- NIST SP 800-218/800-218A for secure software-development lifecycle context.
- MITRE ATLAS for adversary tactics/techniques and threat-informed testing.
- ISO/IEC 42001:2023 as an external management-system reference; YASC does not reproduce its normative text.

## YASC contribution

YASC's intended contribution is the engineering synthesis:

1. stable agent-security control identifiers;
2. explicit links from threat to control to reusable verification test;
3. evidence requirements and pass criteria per control;
4. YAL assurance claims tied to evidence depth;
5. scenario-specific security profiles;
6. machine-readable control, test, assessment, verification-run, and assurance-case formats;
7. bounded, reproducible verification for stochastic agent systems;
8. continuous revalidation triggers and evidence freshness;
9. vendor-neutral artifacts that can be consumed by security tooling.

## Editorial rule

External identifiers are used as mappings and references. YASC control prose should be independently written. Where a direct quotation is ever necessary, it must be clearly marked, attributed, and compatible with the source license.

YASC does not claim certification, endorsement, or full equivalence with mapped frameworks.
