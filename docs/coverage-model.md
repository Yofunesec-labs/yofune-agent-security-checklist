# YASC Verification Coverage Model

YASC v1.0 reports coverage as multiple dimensions rather than one score.

## Recommended dimensions

- **Control coverage:** applicable controls with an explicit verdict / applicable controls.
- **Test coverage:** planned verification tests with at least one valid run / planned tests.
- **Boundary coverage:** relevant trust boundaries exercised at least once.
- **High-impact action coverage:** high-impact action classes with positive and negative verification.
- **Evidence completeness:** required evidence classes present for the claim.
- **Variant coverage:** canonical, indirect, encoded/metamorphic, stateful, and temporal variants where applicable.
- **Environment fidelity:** unit, integration, staging, production-safe observation.
- **Change coverage:** security-relevant changes that have received differential/regression verification.

Coverage should be used to expose blind spots, not to imply that 100% test coverage equals 100% security.
