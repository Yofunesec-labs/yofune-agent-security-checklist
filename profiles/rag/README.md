# Yofune RAG Agent Security Profile

**Profile target:** RAG/search/retrieval agents  
**YASC baseline:** 1.0.0  
**Reference snapshot:** 2026-09-18

This profile supplements, and does not replace, the core YASC baseline.

## Required baseline controls

- `YAS-01.04`
- `YAS-02.02`
- `YAS-02.04`
- `YAS-05.01`
- `YAS-05.02`
- `YAS-05.04`
- `YAS-05.05`
- `YAS-05.06`
- `YAS-10.01`

## Profile requirements

1. Classify every ingestion source and preserve provenance through chunking/embedding/indexing.
2. Enforce document-level authorization before retrieved text enters model context.
3. Test semantic and exact-match cross-tenant leakage.
4. Treat retrieved instructions as untrusted content.
5. Separate retrieval relevance from trust/authorization.
6. Detect or contain poisoned documents and manipulated metadata.
7. Record source identifiers, retrieval scores, filters, and authorization decisions.
8. Minimize sensitive chunks and prevent unrelated context stuffing.
9. Support removal/revocation with index/cache propagation.
10. Use an evaluation corpus that includes indirect prompt injection in documents.
11. Keep ingestion identities distinct from query identities.
12. Define freshness/staleness behavior for security-sensitive records.

## Evidence package

A profile assessment should preserve the applicable baseline evidence plus profile-specific configuration, identity/authorization records, representative traces, negative-test results, and exception records.
