# OpenPowers

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

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

## Recommended Development Workflow

Use this workflow for product behavior changes in an OpenSpec project:

1. **Classify the request**
   Decide whether the request changes product behavior, API behavior, domain rules, permissions, data model semantics, or accepted edge cases. If yes, route it through OpenSpec.

2. **Select or create the OpenSpec change**
   Use the target project's OpenSpec workflow to find the controlling proposal/task/spec. If none exists, create an OpenSpec change before implementation. Keep requirements in OpenSpec only.

3. **Plan from WHAT to HOW**
   Restate the OpenSpec source, identify ambiguity, and choose the smallest implementation path. OpenPowers Lite should shape execution discipline, not add another product spec.

4. **Write the first failing check when practical**
   Add or update the narrowest test that captures the OpenSpec behavior boundary. Skip TDD only when the change is documentation-only, purely mechanical, or not meaningfully testable.

5. **Implement in a scoped diff**
   Change only the files needed for the selected OpenSpec change. Avoid opportunistic refactors, unrelated formatting, and new abstractions unless the current change genuinely needs them.

6. **Review against the OpenSpec delta**
   Check that the diff satisfies the OpenSpec change, that tests cover the important behavior, and that no duplicate product-spec source was introduced outside OpenSpec.

7. **Verify and archive**
   Run the relevant project tests plus OpenSpec validation. After the change is accepted, archive it through OpenSpec so OpenSpec remains the historical source of product truth.

For Codex, a good working prompt is:

```text
Use OpenPowers Lite to implement OpenSpec change <change-id>. Keep OpenSpec as the only product spec source, use TDD where practical, and report verification evidence.
```

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
