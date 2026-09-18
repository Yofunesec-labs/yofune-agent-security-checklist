# YASC Roadmap

## v0.1 — Initial Public Draft

- 10 domains / 52 controls
- 31 initial verification tests
- 8 security profiles
- YAL assurance model
- machine-readable baseline and interactive checklist

## v0.2 — Verification & Whitepaper Expansion

- 52 controls / 46 verification tests
- complete technical whitepaper
- stochastic-agent verification guidance
- metamorphic, differential, compositional, fault-injection, and containment testing
- verification-run and assurance-case artifacts
- evidence-quality/freshness model
- provenance/originality policy

## v0.5 — Public Review & Interoperability

- 58 verification tests
- Verification Plan, Evidence Manifest, and bounded Conformance Claim formats
- evidence integrity and multidimensional coverage model
- branded English/Chinese whitepapers
- framework-neutral harness utilities and CI integration design

## v1.0 — Stable Baseline + Executable Reference Harness (current)

- stable released identifiers and deprecation policy
- Agent adapters: deterministic mock + configurable JSON-over-HTTP
- MCP adapters: stdio + HTTP JSON-RPC transports
- execution-scenario registry for all 58 YAT IDs
- actual Test Runner with repeated trials and assertions
- Evidence Collector with redaction, SHA-256 manifests, and integrity verification
- per-control assessment builder
- branded HTML/PDF Assessment Report Generator
- CI Security Gate for coverage, severity, inconclusive, integrity, and freshness policy
- reusable GitHub composite action and self-test workflow
- formally versioned branded technical whitepapers
- signed/checksummed release artifact workflow

## v1.1+ — Ecosystem & Adapter Expansion

Directional research areas include:

- first-party adapters for widely used agent frameworks where stable interfaces justify maintenance;
- richer MCP authorization and identity verification fixtures;
- pluggable target-specific assertion/oracle packages;
- evidence attestation/signing profiles;
- regression corpus management and differential result visualization;
- optional independent-assessor workflow and review disposition records;
- KUROSHIO integration that emits the vendor-neutral YASC run/evidence formats.

The roadmap is directional. Security-relevant upstream changes can cause reprioritization without silently changing released identifiers.
