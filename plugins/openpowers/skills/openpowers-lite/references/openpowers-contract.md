# OpenPowers Contract

OpenPowers is a composition rule, not a new specification framework.

## Ownership

| Layer | Owns | Must not own |
| --- | --- | --- |
| OpenSpec | Product behavior, capability specs, change proposals, archival history | Agent execution habits |
| Superpowers Lite | Execution discipline, TDD pressure, review posture, verification gates | Product requirements or accepted behavior |
| AGENTS.md | When the agent must use OpenSpec or OpenPowers Lite in a repository | Detailed product specs |
| OpenPowers plugin | Thin adaptation rules and verification helpers | Forked upstream prompts or duplicated specs |

## Allowed Local Glue

- A short `AGENTS.md` policy that tells agents when to use OpenSpec.
- A Codex skill that reminds agents how to execute safely.
- Verification scripts that check the contract.
- Upstream lock/report files that make upgrades reviewable.

## Forbidden Drift

- A second product spec tree under `.openpowers/`, `.superpowers/`, or plugin folders.
- Copied upstream OpenSpec or Superpowers prompt bodies.
- Silent edits to local workflow rules during update checks.
- Claims that tests or OpenSpec validation passed without actually running them.
