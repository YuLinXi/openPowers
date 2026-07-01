---
name: openpowers-lite
description: "Use when working on an OpenSpec-driven codebase that wants lightweight Superpowers-style execution discipline: planning from OpenSpec proposals/tasks, TDD implementation, review, verification, archiving, or upstream workflow-rule upgrades. This skill enforces that OpenSpec is the only product specification source while Superpowers Lite only guards execution process."
---

# OpenPowers Lite

OpenPowers Lite is a thin workflow guard for OpenSpec projects.

Core invariants:

- OpenSpec owns WHAT.
- Superpowers Lite guards HOW.
- AGENTS.md decides WHEN.
- Do not create product specifications outside OpenSpec.
- Do not copy upstream OpenSpec or Superpowers prompt bodies into local rules.

## Workflow

1. Locate the controlling OpenSpec change before implementation.
   Use existing OpenSpec commands and files in the target repo, such as `openspec list`, `openspec show`, `openspec validate`, `openspec archive`, `specs/`, or `changes/`, according to that repo's OpenSpec installation.
2. If the user asks for a product or behavior change and there is no OpenSpec proposal/task, stop and ask whether to create or select one. Do not invent a parallel spec in README, issues, Superpowers notes, or OpenPowers files.
3. Execute with Superpowers Lite discipline:
   - restate the selected OpenSpec source;
   - identify ambiguous requirements before coding;
   - prefer the smallest correct change;
   - use TDD when a behavior boundary is testable;
   - keep diffs scoped to the selected OpenSpec change;
   - run relevant tests, lint, type checks, builds, and OpenSpec validation.
4. During review, check behavior against the OpenSpec delta first, then check test coverage, verification evidence, and unrelated drift.
5. During archive, verify implementation and OpenSpec validation before marking work complete.

## Upgrade Rules

For upstream OpenSpec or Superpowers updates, read `references/upgrade-policy.md`.

Never silently rewrite local workflow files. Any automated upgrade must leave reviewable evidence: a branch or diff, an upgrade report, and a changelog entry. Prefer the repository script:

```bash
python3 scripts/openpowers_lite.py upgrade-check --write-lock
```

Use `--branch`, `--commit`, and `--pr` only when the user explicitly wants automation to create Git history or a GitHub PR.

## Output Contract

When finishing work, report:

- the OpenSpec proposal/task/spec source used;
- what code or docs changed;
- which tests and OpenSpec validation commands ran;
- what was not verified;
- residual risks or follow-up work.

If no OpenSpec source controlled the change, say that clearly and do not claim the work is spec-complete.
