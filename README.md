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

## Workflow Command and Skill Map

Use terminal commands for OpenSpec state, validation, and project tests. Use AI chat commands for OpenSpec artifact work and implementation. `openpowers-lite` is the Codex skill from this plugin; `/opsx:*` commands come from the OpenSpec integration generated in the target project.

| Stage | How to use it | Commands | Skill or chat trigger | Done when |
| --- | --- | --- | --- | --- |
| 0. Bootstrap | Install OpenSpec in the target project and install this plugin in Codex. | `npm install -g @fission-ai/openspec@latest`<br>`openspec init`<br>`codex plugin marketplace add YuLinXi/openPowers --ref main`<br>`codex plugin add openpowers@openpowers` | Start a new Codex thread so `openpowers-lite` is discoverable. | `openspec/` exists, `/opsx:*` commands are recognized, and Codex can trigger `openpowers-lite`. |
| 1. Classify | Decide whether the request needs OpenSpec. | Usually none. Optional context checks:<br>`openspec list --json`<br>`openspec list --specs --json` | `Use OpenPowers Lite to classify this request against AGENTS.md.` | Behavior changes go to OpenSpec; chores or mechanical edits can proceed without a new spec. |
| 2. Explore | Clarify fuzzy requirements before creating artifacts. | `openspec list --specs`<br>`openspec show <spec-id> --type spec` | `/opsx:explore` plus `Use OpenPowers Lite to keep OpenSpec as the WHAT source.` | Ambiguity is captured, and the next step is either stop, propose, or select an existing change. |
| 3. Propose | Create or update the OpenSpec change. | Optional scaffold:<br>`openspec new change <change-id>`<br>Status:<br>`openspec status --change <change-id>` | `/opsx:propose <change-id>` or `Use OpenPowers Lite to draft/review OpenSpec change <change-id>.` | Proposal, delta specs, design, and tasks are reviewed enough for implementation. |
| 4. Plan | Turn OpenSpec artifacts into an implementation plan. | `openspec show <change-id> --json`<br>`openspec status --change <change-id> --json`<br>`openspec instructions apply --change <change-id> --json` | `Use OpenPowers Lite to plan implementation for <change-id>.` | The OpenSpec source is named, risks are explicit, and the first test target is known. |
| 5. Implement with TDD | Write the smallest useful failing check, then implement. | Project-specific commands, for example:<br>`npm test`<br>`pytest`<br>`go test ./...`<br>`cargo test` | `/opsx:apply <change-id>` plus `Use OpenPowers Lite; keep the diff scoped and use TDD where practical.` | The selected behavior works, the diff is scoped, and tests cover the important boundary. |
| 6. Sync and review | Reconcile what changed with OpenSpec tasks and specs. | `git diff`<br>`openspec status --change <change-id>`<br>`openspec show <change-id>` | `/opsx:sync <change-id>` when enabled, plus `Use OpenPowers Lite to review against the OpenSpec delta.` | Tasks and specs reflect reality, and no duplicate product-spec source was introduced. |
| 7. Verify | Prove the implementation and spec structure. | `openspec validate <change-id> --strict`<br>`openspec validate --all --strict`<br>Relevant project test/lint/type/build commands | `/opsx:verify <change-id>` when enabled, plus `Use OpenPowers Lite to produce verification evidence.` | OpenSpec validation and relevant project checks pass, or failures are reported honestly. |
| 8. Archive | Move accepted work into OpenSpec history. | `openspec archive <change-id> --yes`<br>For tooling-only changes:<br>`openspec archive <change-id> --skip-specs --yes` | `/opsx:archive <change-id>` or `Use OpenPowers Lite to confirm archive readiness.` | Delta specs are merged or intentionally skipped, and the change is archived. |
| 9. Upgrade workflow rules | Refresh upstream tracking without silently changing local rules. | `python3 scripts/openpowers_lite.py upgrade-check`<br>`python3 scripts/openpowers_lite.py upgrade-check --write-lock` | `Use OpenPowers Lite to review an OpenSpec/Superpowers upstream update.` | `.openpowers/upgrade-report.md`, `.openpowers/UPGRADE_CHANGELOG.md`, and a reviewable diff exist. |

If `/opsx:*` commands are not recognized in the target project, run:

```bash
openspec init
openspec update
```

Then restart the AI tool or start a new thread. See the OpenSpec [getting started guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md) and [CLI reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md) for the upstream command details.

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
