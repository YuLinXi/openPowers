# Upgrade Policy

OpenPowers supports upstream movement without forking OpenSpec or Superpowers.

## Tracked Upstreams

The tracked upstreams live in `.openpowers/upstreams.json`; resolved refs live in `.openpowers/upstreams.lock.json`.

## Rules

- Upgrade checks may fetch upstream metadata.
- Upgrade checks must not silently rewrite local workflow rules.
- Any lock refresh must produce `.openpowers/upgrade-report.md` and `.openpowers/UPGRADE_CHANGELOG.md`.
- Shared changes should be committed on a branch and opened as a PR.
- Local rule changes must be explained in `CHANGELOG.md`.

## Command

```bash
python3 scripts/openpowers_lite.py upgrade-check --write-lock
```
