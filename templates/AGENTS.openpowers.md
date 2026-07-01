# AGENTS.md

Use this template in repositories that adopt OpenPowers.

## Core Rule

OpenSpec owns WHAT. Superpowers Lite guards HOW. AGENTS.md decides WHEN.

## When To Use OpenSpec

Use OpenSpec before coding when a request changes product behavior, public API behavior, user workflows, domain rules, permissions, data model semantics, or accepted edge cases.

Do not require OpenSpec for typo fixes, formatting-only changes, dependency chores, mechanical refactors with no behavior change, or exploratory code reading.

## When To Use OpenPowers Lite

Use OpenPowers Lite whenever an OpenSpec change is being proposed, implemented, reviewed, verified, or archived.

The agent must:

- identify the controlling OpenSpec proposal/task/spec;
- ask before proceeding if no controlling OpenSpec change exists;
- keep product requirements in OpenSpec only;
- use TDD where the behavior boundary is testable;
- keep diffs scoped to the selected OpenSpec change;
- run relevant tests and OpenSpec validation before claiming completion.

## Forbidden

- Do not create product specs under `.openpowers/`, `.superpowers/`, docs-only files, or issue comments as an alternative to OpenSpec.
- Do not copy large upstream prompt bodies into this repository.
- Do not silently change local workflow rules during upgrade checks.

## Final Report

Every completed OpenSpec task must report:

- OpenSpec source used;
- files changed;
- tests, lint, type checks, builds, and OpenSpec validation run;
- areas not verified;
- residual risk or follow-up work.
