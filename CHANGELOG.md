# Changelog

All notable changes are documented here. YASC uses semantic versioning for the baseline and profiles.

## [1.0.0] - 2026-09-18

### Added
- Installable `yasc-verification-harness` Python package and `yasc` CLI.
- Configurable JSON-over-HTTP Agent adapter plus deterministic secure/insecure mock targets.
- MCP stdio and HTTP adapters with modern `server/discover` / legacy initialize negotiation, `tools/list`, and `tools/call` operations.
- Execution-scenario schema and registry covering all 58 YAT IDs; generic-safe probes are automated and target-dependent tests are explicitly guided.
- Actual Test Runner with repeated trials, adapter state reset, executable assertions, and machine-readable Verification Run output.
- Evidence Collector with structured event capture, default secret/bearer-token redaction, SHA-256 manifests, and integrity verification.
- Per-control Assessment Builder that derives bounded status/assurance only from tests included in the Verification Plan.
- Yofune-branded HTML/PDF Assessment Report Generator.
- CI Security Gate supporting minimum coverage, required tests, severity blocking, maximum inconclusive runs, evidence integrity, and evidence freshness.
- Reusable GitHub composite action and repository self-test workflow proving a secure synthetic target passes and an intentionally insecure target is rejected.
- Target, execution-scenario, and CI gate JSON Schemas/templates; local MCP stdio fixture; end-to-end smoke examples.
- Harness architecture and CI gate technical documentation.
- Direct OpenAI Responses API and Anthropic Messages API target adapters with safe observation of proposed tool calls.
- In-process LangGraph `.invoke()` and CrewAI `.kickoff()` target adapters.
- MCP `2026-07-28` modern discovery/stateless request support with legacy handshake fallback; stdio auto-probe isolation and modern HTTP routing headers.
- GitHub Release workflow that publishes v1.0.0 assets from the tagged source after full validation/security-gate checks.
- GitHub Pages release/download page generated from the repository source of truth.

### Changed
- Promoted YASC metadata from Public Draft to v1.0 Stable Release while retaining bounded, non-certification claim language.
- Technical whitepapers updated with executable Harness, Adapter, Evidence Collector, Test Runner, Assessment Report, and CI Gate architecture.
- Repository tests expanded to cover the executable reference stack.

## [0.5.0-draft] - 2026-09-18

### Added
- Yofune-branded English and Chinese technical whitepapers with supplied logo, website, contact email, and publisher identity.
- 12 new verification tests (58 total) covering capability attenuation, revocation propagation, TOCTOU action mutation, schema/parser confusion, context compaction privilege laundering, deleted-memory resurrection, transitive peer trust, approval expiry, causal trace collision, queued-action drain, downgrade/rollback integrity, and Unicode/confusable metamorphic variants.
- Verification Plan, Evidence Manifest, and Public-draft Conformance Claim schemas/templates.
- Verification procedure specification, evidence integrity/chain-of-custody guidance, conformance rules, and multidimensional coverage model.
- Framework-neutral `scripts/yasc_harness.py` for plan validation, run scaffolding, evidence hashing/integrity checks, and coverage reporting.
- Branded interactive checklist header/footer and repository brand assets.

### Changed
- Method lifecycle expanded to Scope → Attack → Control → Verify → Evidence → Assurance → Revalidate.
- Whitepaper strengthened around security oracles, asynchronous/temporal verification, TOCTOU, parser differentials, causal evidence attribution, independence disclosure, and release gates.
- Generated baseline/test playbooks now derive directly from machine-readable YAML to reduce documentation drift.

## [0.2.0-draft] - 2026-09-18

### Added
- Full technical whitepaper and Chinese review edition.
- 15 new verification tests (46 total), covering approval integrity, supply-chain drift, observability, resilience, differential regression, and metamorphic transformations.
- Verification-run and assurance-case JSON Schemas/templates.
- Validation model covering stochastic trials, fault injection, environment fidelity, evidence integrity, containment latency, and revalidation triggers.
- Evidence model and provenance/originality policy.

### Changed
- Replaced the earlier marketing-style tagline with descriptive positioning: a verifiable security baseline for AI agents.
- Expanded methodology from Scope → Attack → Control → Verify → Evidence to include bounded Assurance Claims.
- Updated reference snapshot with OWASP red-teaming guidance, NIST SP 800-218A/AIRC, and ISO/IEC 42001 context.

## [0.1.0-draft] - 2026-09-18

### Added
- Public-draft baseline with 52 controls across 10 domains.
- Yofune Assurance Levels YAL-0 through YAL-4.
- 31 verification-test definitions.
- Eight scenario security profiles.
- Machine-readable YAML source, JSON Schema, generators, validation, CI, and static interactive checklist.
- Dated external-framework reference snapshot and initial crosswalks.
