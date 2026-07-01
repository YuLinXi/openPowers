# Upgrade Policy

Use this policy when refreshing OpenSpec, Superpowers, or OpenPowers workflow rules.

## Required Evidence

Every automated upgrade must create reviewable evidence:

- a visible Git diff or branch;
- `.openpowers/upgrade-report.md`;
- `.openpowers/UPGRADE_CHANGELOG.md`;
- an updated `.openpowers/upstreams.lock.json` when upstream refs changed;
- a PR when the workflow is used by a team or shared repository.

## Safe Procedure

1. Start from a clean worktree or a dedicated upgrade branch.
2. Run:

   ```bash
   python3 scripts/openpowers_lite.py upgrade-check --write-lock
   ```

3. Review `git diff -- .openpowers plugins/openpowers AGENTS.md templates README.md`.
4. If local rules changed, explain the reason in `CHANGELOG.md`.
5. Run:

   ```bash
python3 scripts/openpowers_lite.py verify
python3 -m unittest discover -s tests -p 'test_*.py'
```

6. Open a PR before installing the changed plugin broadly.

## Automation Options

Use these only when the user asks for Git automation:

```bash
python3 scripts/openpowers_lite.py upgrade-check \
  --write-lock \
  --branch chore/openpowers-upstream-refresh \
  --commit "chore: refresh openpowers upstream lock" \
  --pr
```

The command updates audit files only. It does not vendor upstream prompt bodies and does not rewrite OpenSpec product specs.
