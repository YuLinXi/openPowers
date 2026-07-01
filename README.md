# OpenPowers

OpenPowers is an out-of-the-box **OpenSpec + Superpowers Lite** Codex plugin/repository template.

It does not merge two full workflows into a larger framework. The contract is deliberately small:

- **OpenSpec owns WHAT**: product specs, proposals, tasks, validation, and archive history.
- **Superpowers Lite guards HOW**: planning discipline, TDD pressure, review posture, and verification evidence.
- **AGENTS.md decides WHEN**: each repository says when agents must use OpenSpec and OpenPowers Lite.

OpenPowers keeps OpenSpec as the only product-spec source. Local rules are thin glue so upstream OpenSpec and Superpowers can keep evolving without a hard fork.

## Repository Layout

```text
.
├── .agents/plugins/marketplace.json
├── .openpowers/
│   ├── upstreams.json
│   ├── upstreams.lock.json
│   ├── upgrade-report.md
│   └── UPGRADE_CHANGELOG.md
├── plugins/openpowers/
│   ├── .codex-plugin/plugin.json
│   └── skills/openpowers-lite/
├── scripts/openpowers_lite.py
├── templates/AGENTS.openpowers.md
└── tests/
```

## Install the Plugin

From a local clone:

```bash
git clone git@github.com:YuLinXi/openPowers.git
cd openPowers
codex plugin marketplace add .
codex plugin add openpowers@openpowers
```

From GitHub:

```bash
codex plugin marketplace add YuLinXi/openPowers --ref main
codex plugin add openpowers@openpowers
```

Start a new Codex thread after installing so the `openpowers-lite` skill is available.

## Use in an OpenSpec Project

1. Install or update OpenSpec in the target project using the upstream OpenSpec instructions.
2. Copy or adapt `templates/AGENTS.openpowers.md` into the target repository's `AGENTS.md`.
3. Keep product specs in OpenSpec's own proposal/spec structure. Do not create `.openpowers/specs` or `.superpowers/specs`.
4. Ask Codex to work from a named OpenSpec change, for example:

   ```text
   Use OpenPowers Lite to implement OpenSpec change add-team-invites.
   ```

5. Require final reports to include the OpenSpec source, code/docs changed, validation commands, unverified areas, and residual risk.

## Verify This Repository

Run the local checks:

```bash
python3 scripts/openpowers_lite.py verify
python3 -m unittest discover -s tests -p 'test_*.py'
python3 /Users/yumengyuan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/openpowers
python3 /Users/yumengyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/openpowers/skills/openpowers-lite
```

The validator paths above are for this development machine and require `PyYAML`. On another machine, run the equivalent validator scripts from your Codex skill installation, or rely on `codex plugin add` after reviewing the repository.

## Upgrade Upstreams

OpenPowers tracks upstream refs in `.openpowers/upstreams.json` and `.openpowers/upstreams.lock.json`.

Create an audit report without changing the lock:

```bash
python3 scripts/openpowers_lite.py upgrade-check
```

Create a reviewable lock/changelog diff:

```bash
python3 scripts/openpowers_lite.py upgrade-check --write-lock
git diff -- .openpowers
```

Create a branch, commit, and PR when a team wants automated upgrade evidence:

```bash
python3 scripts/openpowers_lite.py upgrade-check \
  --write-lock \
  --branch chore/openpowers-upstream-refresh \
  --commit "chore: refresh openpowers upstream lock" \
  --pr
```

The upgrade command updates audit files only. It does not vendor upstream prompt bodies, rewrite OpenSpec specs, or silently change local workflow rules.

## Design Boundary

OpenPowers is intentionally not:

- an OpenSpec fork;
- a Superpowers fork;
- a second product-spec system;
- a large prompt pack copied from either upstream;
- a hidden auto-updater that changes local rules without review.

If this repository needs stronger behavior later, add it only when the diff remains reviewable and OpenSpec stays the single source of product truth.
