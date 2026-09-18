# Governance

## Roles

- **Maintainers** — approve releases, control identifiers, and editorial policy.
- **Reviewers** — review controls, tests, mappings, and profiles in their area of expertise.
- **Contributors** — submit issues, evidence, tests, corrections, and proposals.
- **Research acknowledgements** — credited for material research contributions even when they are not repository maintainers.

## Identifier stability

Released `YAS-*` and `YAT-*` identifiers are never silently reassigned. Deprecated items remain discoverable with migration notes.

## Release policy

- **Major** (`v1 → v2`): material risk-model or structural change.
- **Minor** (`v1.1 → v1.2`): new controls, profiles, or meaningful verification capability.
- **Patch** (`v1.1.1`): wording, links, non-semantic schema fixes, and mapping corrections.

Every release includes a reference snapshot date and the external versions reviewed at that date.

## Decision principle

The baseline remains vendor-neutral. Product-specific automation may implement YASC, but core control language must not require a Yofune product.
