# YASC v1.0.0 Release

**Release date:** 2026-09-18  
**Reference snapshot:** 2026-09-18  
**Maintainer:** Yofune Security Research  
**Publisher:** Chengdu Yofune Ariake Technology Co., Ltd.  
**Website:** https://yofunesec.com/  
**Contact:** contact@yofunesec.com

YASC v1.0.0 is the first stable baseline release. The 10-domain / 52-control identifier set remains stable from the public-draft series, while the reference implementation now closes the loop from plan to execution to evidence to CI decision.

## Release contents

- 52 core controls / 58 verification tests / 8 security profiles.
- Machine-readable YAML and JSON Schemas.
- English and Chinese branded technical whitepapers.
- Interactive static checklist.
- Installable `yasc` Verification Harness.
- Agent HTTP adapter and deterministic mock adapter.
- MCP stdio/HTTP adapters.
- Evidence Collector and SHA-256 manifests.
- Actual Test Runner and scenario registry.
- Per-control assessment builder.
- HTML/PDF Assessment Report Generator.
- CI Security Gate and GitHub Action integration.

## Claim boundary

A YASC test PASS or CI gate PASS is a bounded result for the declared system state, scope, environment, test set, and evidence. This release is not a commercial certification program and does not authorize unqualified claims that an agent is universally secure.
