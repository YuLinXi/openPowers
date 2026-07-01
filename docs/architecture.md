# Architecture

OpenPowers is a thin Codex plugin plus repository template for OpenSpec projects.

## Layers

| Layer | Responsibility |
| --- | --- |
| OpenSpec | Product behavior, proposed changes, tasks, validation, archive history |
| Superpowers Lite | Execution discipline: clarify, test first when useful, review, verify |
| AGENTS.md | Repository-specific trigger policy |
| OpenPowers | Small glue rules, installable Codex skill, verification and upgrade scripts |

## Data Flow

1. A user requests a behavior change.
2. `AGENTS.md` determines whether OpenSpec is required.
3. OpenSpec provides the proposal/spec/task source.
4. OpenPowers Lite tells the agent how to execute and verify the work.
5. OpenSpec validation and project tests prove the result.
6. OpenSpec archive records the accepted WHAT after implementation.

No OpenPowers file becomes a product-spec source.
