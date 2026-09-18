# YASC Assurance Cases

An **assurance case** is a structured argument that connects a security claim to controls, verification results, evidence, assumptions, and known gaps.

YASC uses assurance cases to avoid a common failure mode: a team has dozens of logs and test screenshots but cannot explain what security claim they prove.

## Structure

A YASC assurance case contains:

- **Claim** — the security property being asserted.
- **Scope** — systems, versions, identities, tenants, environments, and action types covered.
- **Control** — the YAS control(s) intended to enforce the property.
- **Threat/failure path** — how the property could fail.
- **Verification** — tests and inspection activities performed.
- **Evidence** — artifacts supporting the result.
- **Assumptions** — dependencies that must remain true.
- **Known gaps** — untested paths, exclusions, and limitations.
- **Residual risk** — remaining risk after controls and verification.
- **Assurance level** — YAL achieved for the bounded claim.
- **Freshness/revalidation** — conditions that cause the claim to expire.

## Example

> **Claim:** An email-sending agent cannot add an unapproved external recipient to a message authorized by a human.
>
> **Controls:** YAS-02.05, YAS-04.03, YAS-09.02, YAS-09.03.
>
> **Verification:** indirect injection, parameter drift after approval, and approval replay tests.
>
> **Evidence:** approval object hash, tool request, policy decision, email gateway log, trace ID, test run record.
>
> **Known gap:** mobile approval client was not included.
>
> **Assurance:** YAL-4 for the assessed web approval path; no claim is made for the excluded mobile path.

The important property is boundedness: YASC assurance applies to an explicit system state and scope, not to an abstract product forever.


## v1.0 claim linkage

An assurance case should reference the verification plan, individual verification runs, and evidence manifest. Externally shared claims should also disclose reviewer independence and the validity/revalidation boundary. The machine-readable bounded conformance format is defined in `schema/conformance-claim.schema.json`.
