# AGENTS.md

This repository builds and maintains the OpenPowers plugin.

## Operating Contract

- OpenSpec owns WHAT.
- Superpowers Lite guards HOW.
- AGENTS.md decides WHEN.
- OpenSpec is the only product specification source.
- OpenPowers must stay a thin glue layer. Do not vendor large upstream prompt bodies.
- Automated upgrade work must create reviewable evidence: diff, changelog, and PR when shared.

## When Editing This Repository

- Keep plugin code under `plugins/openpowers/`.
- Keep reusable checks in `scripts/openpowers_lite.py` and cover behavior with `python3 -m unittest`.
- Keep product-spec examples out of this repo unless they are clearly marked as OpenSpec-owned examples.
- Do not create `.openpowers/specs`, `.superpowers/specs`, or plugin-local product spec directories.
- Update `README.md`, `templates/AGENTS.openpowers.md`, and `CHANGELOG.md` when behavior or installation steps change.

## Required Validation

Before claiming completion, run the relevant subset:

```bash
python3 scripts/openpowers_lite.py verify
python3 -m unittest discover -s tests -p 'test_*.py'
python3 /Users/yumengyuan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/openpowers
python3 /Users/yumengyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/openpowers/skills/openpowers-lite
```

If a validator path is unavailable on another machine, state that clearly and run the closest available check.
