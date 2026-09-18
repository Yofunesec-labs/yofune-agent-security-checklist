# YASC Conformance and Claim Rules

**Revision:** 1.0  
**Status:** v1.0 Stable Release

YASC conformance is a **bounded statement about an identified system state and scope**. It is not a universal claim that an agent is safe, and v1.0 is not a commercial certification program.

## 1. Three claim types

YASC distinguishes:

1. **Control conformance** — one named control meets its pass criteria in a stated scope.
2. **Profile conformance** — all applicable mandatory controls in a named profile have an explicit status, with exclusions justified.
3. **Baseline assessment** — the complete core baseline has been assessed for applicability and status, including unresolved gaps.

A claim must name the YASC version, system/version, environment, scope, applicable profiles, control results, achieved YAL, known gaps, and revalidation triggers.

## 2. Status and assurance are different

`PASS` answers whether the stated pass criteria were met. `YAL` answers how strong the supporting evidence is. A control can be implemented correctly but only supported by YAL-2 evidence; conversely, extensive adversarial testing cannot turn a failed control into a pass.

## 3. No hidden averaging

YASC does not permit a failed critical control to be averaged away by many lower-impact passes. Reports should preserve per-control status. Organizations may create their own risk summaries, but those summaries are not YASC conformance labels.

## 4. Required claim boundary

A reviewer should be able to identify:

- the exact application and model baseline;
- identities/tenants and high-impact actions included;
- tools, MCP servers, memory/retrieval systems, and execution surfaces included;
- environments and data classes exercised;
- explicit exclusions;
- test corpus/version and trial policy;
- evidence location and integrity metadata;
- validity window and material-change triggers.

## 5. Recommended wording

Use bounded language such as:

> Within the stated staging scope and recorded system baseline, control YAS-04.03 met its pass criteria and achieved YAL-4 based on the referenced verification runs and assurance case.

Avoid wording such as “YASC certified secure,” “prompt-injection proof,” or “fully compliant” unless a future governance program defines and authorizes those claims.

## 6. Independence disclosure

Every externally shared claim should disclose whether the work was self-reviewed, independently reviewed within the same organization, or reviewed by an independent external party. Independence strengthens governance, but does not replace technical evidence.
