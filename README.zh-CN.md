# OpenPowers

语言：[English](README.md) | [简体中文](README.zh-CN.md)

OpenPowers 是一个开箱即用的 **OpenSpec + Superpowers Lite** Codex 插件/仓库模板。

它不是把两套完整流程硬拼成一个更大的框架。它的契约刻意保持很小：

- **OpenSpec owns WHAT**：产品规格、变更提案、任务、验证和归档历史。
- **Superpowers Lite guards HOW**：规划纪律、TDD 压力、review 姿态和 verification 证据。
- **AGENTS.md decides WHEN**：每个仓库自行定义 agent 什么时候必须使用 OpenSpec 和 OpenPowers Lite。

OpenPowers 让 OpenSpec 始终作为唯一产品规格源头。本地规则只是薄胶水层，因此 OpenSpec 和 Superpowers 上游可以持续演进，而不需要 fork。

## 仓库结构

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

## 安装插件

从本地 clone 安装：

```bash
git clone git@github.com:YuLinXi/openPowers.git
cd openPowers
codex plugin marketplace add .
codex plugin add openpowers@openpowers
```

从 GitHub 安装：

```bash
codex plugin marketplace add YuLinXi/openPowers --ref main
codex plugin add openpowers@openpowers
```

安装后开启一个新的 Codex 线程，让 `openpowers-lite` skill 生效。

## 在 OpenSpec 项目中使用

1. 按照 OpenSpec 上游说明，在目标项目中安装或更新 OpenSpec。
2. 将 `templates/AGENTS.openpowers.md` 复制或改写到目标仓库的 `AGENTS.md`。
3. 产品规格只保存在 OpenSpec 自己的 proposal/spec 结构中。不要创建 `.openpowers/specs` 或 `.superpowers/specs`。
4. 让 Codex 从一个明确命名的 OpenSpec change 开始工作，例如：

   ```text
   Use OpenPowers Lite to implement OpenSpec change add-team-invites.
   ```

5. 要求最终报告包含 OpenSpec 来源、改动的代码/文档、验证命令、未验证范围和残余风险。

## 推荐开发工作流

在 OpenSpec 项目中处理产品行为变更时，推荐使用这条流程：

1. **判断请求类型**
   判断请求是否会改变产品行为、API 行为、领域规则、权限、数据模型语义或已接受的边界情况。如果会，就进入 OpenSpec 流程。

2. **选择或创建 OpenSpec change**
   使用目标项目的 OpenSpec 工作流找到控制本次工作的 proposal/task/spec。如果不存在，就先创建 OpenSpec change，再进入实现。需求只能写在 OpenSpec 中。

3. **从 WHAT 规划到 HOW**
   复述 OpenSpec 来源，指出模糊点，并选择最小可行实现路径。OpenPowers Lite 只塑造执行纪律，不添加第二份产品规格。

4. **在可行时先写失败检查**
   添加或更新能捕获 OpenSpec 行为边界的最小测试。只有文档变更、纯机械改动或无法形成有意义测试的场景，才跳过 TDD。

5. **用聚焦 diff 实现**
   只修改所选 OpenSpec change 所需的文件。避免顺手重构、无关格式化和不必要的新抽象，除非当前变更确实需要。

6. **对照 OpenSpec delta 做 review**
   检查 diff 是否满足 OpenSpec 变更、测试是否覆盖关键行为，以及是否引入了 OpenSpec 之外的重复产品规格源。

7. **验证并归档**
   运行相关项目测试和 OpenSpec validation。变更被接受后，通过 OpenSpec archive 归档，让 OpenSpec 继续作为产品事实的历史来源。

给 Codex 的推荐提示词：

```text
Use OpenPowers Lite to implement OpenSpec change <change-id>. Keep OpenSpec as the only product spec source, use TDD where practical, and report verification evidence.
```

## 工作流命令与 Skill 映射

终端命令用于读取 OpenSpec 状态、做验证和运行项目测试。AI chat 命令用于生成 OpenSpec artifacts、实现和归档。`openpowers-lite` 是本插件提供的 Codex skill；`/opsx:*` 命令来自目标项目中 OpenSpec 生成的集成。

| 阶段 | 如何使用 | 命令 | 触发的 skill 或 chat 命令 | 完成标准 |
| --- | --- | --- | --- | --- |
| 0. 初始化 | 在目标项目安装 OpenSpec，并在 Codex 安装本插件。 | `npm install -g @fission-ai/openspec@latest`<br>`openspec init`<br>`codex plugin marketplace add YuLinXi/openPowers --ref main`<br>`codex plugin add openpowers@openpowers` | 开一个新的 Codex 线程，让 `openpowers-lite` 可以被发现。 | 存在 `openspec/`，`/opsx:*` 命令可识别，Codex 能触发 `openpowers-lite`。 |
| 1. 判断请求类型 | 判断请求是否必须进入 OpenSpec。 | 通常不需要命令。可选上下文检查：<br>`openspec list --json`<br>`openspec list --specs --json` | `Use OpenPowers Lite to classify this request against AGENTS.md.` | 行为变更进入 OpenSpec；杂务或机械改动可以不新建 spec。 |
| 2. 探索 | 在创建 artifact 前澄清模糊需求。 | `openspec list --specs`<br>`openspec show <spec-id> --type spec` | `/opsx:explore`，并补充 `Use OpenPowers Lite to keep OpenSpec as the WHAT source.` | 模糊点已记录，下一步明确为停止、propose，或选择已有 change。 |
| 3. 提案 | 创建或更新 OpenSpec change。 | 可选脚手架：<br>`openspec new change <change-id>`<br>查看状态：<br>`openspec status --change <change-id>` | `/opsx:propose <change-id>` 或 `Use OpenPowers Lite to draft/review OpenSpec change <change-id>.` | proposal、delta specs、design 和 tasks 已足够可审查，可以进入实现。 |
| 4. 规划 | 将 OpenSpec artifacts 转成实现计划。 | `openspec show <change-id> --json`<br>`openspec status --change <change-id> --json`<br>`openspec instructions apply --change <change-id> --json` | `Use OpenPowers Lite to plan implementation for <change-id>.` | 已明确 OpenSpec 来源、风险和第一个测试目标。 |
| 5. TDD 实现 | 先写最小有用失败检查，再实现。 | 项目相关命令，例如：<br>`npm test`<br>`pytest`<br>`go test ./...`<br>`cargo test` | `/opsx:apply <change-id>`，并补充 `Use OpenPowers Lite; keep the diff scoped and use TDD where practical.` | 选定行为可工作，diff 聚焦，测试覆盖关键边界。 |
| 6. 同步与 review | 将实际改动与 OpenSpec tasks/specs 对齐。 | `git diff`<br>`openspec status --change <change-id>`<br>`openspec show <change-id>` | 启用时使用 `/opsx:sync <change-id>`，并补充 `Use OpenPowers Lite to review against the OpenSpec delta.` | tasks/specs 反映现实，且没有引入 OpenSpec 之外的重复产品规格源。 |
| 7. 验证 | 证明实现和 spec 结构都正确。 | `openspec validate <change-id> --strict`<br>`openspec validate --all --strict`<br>相关项目 test/lint/type/build 命令 | 启用时使用 `/opsx:verify <change-id>`，并补充 `Use OpenPowers Lite to produce verification evidence.` | OpenSpec validation 和相关项目检查通过；如果失败，必须诚实报告。 |
| 8. 归档 | 将已接受工作写入 OpenSpec 历史。 | `openspec archive <change-id> --yes`<br>仅工具类变更：<br>`openspec archive <change-id> --skip-specs --yes` | `/opsx:archive <change-id>` 或 `Use OpenPowers Lite to confirm archive readiness.` | delta specs 已合并或明确跳过，change 已归档。 |
| 9. 升级工作流规则 | 刷新上游追踪，但不静默改变本地规则。 | `python3 scripts/openpowers_lite.py upgrade-check`<br>`python3 scripts/openpowers_lite.py upgrade-check --write-lock` | `Use OpenPowers Lite to review an OpenSpec/Superpowers upstream update.` | 生成 `.openpowers/upgrade-report.md`、`.openpowers/UPGRADE_CHANGELOG.md` 和可审查 diff。 |

如果目标项目无法识别 `/opsx:*` 命令，运行：

```bash
openspec init
openspec update
```

然后重启 AI 工具或开启新线程。OpenSpec 上游命令细节见官方 [getting started guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md) 和 [CLI reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)。

## 验证本仓库

运行本地检查：

```bash
python3 scripts/openpowers_lite.py verify
python3 -m unittest discover -s tests -p 'test_*.py'
python3 /Users/yumengyuan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/openpowers
python3 /Users/yumengyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/openpowers/skills/openpowers-lite
```

上面的 validator 路径适用于当前开发机器，并且需要 `PyYAML`。在其他机器上，请运行 Codex skill 安装位置中的等价 validator；或者在审查仓库后，通过 `codex plugin add` 做安装验证。

## 升级上游

OpenPowers 通过 `.openpowers/upstreams.json` 和 `.openpowers/upstreams.lock.json` 追踪上游引用。

只生成审计报告，不修改 lock：

```bash
python3 scripts/openpowers_lite.py upgrade-check
```

生成可审查的 lock/changelog diff：

```bash
python3 scripts/openpowers_lite.py upgrade-check --write-lock
git diff -- .openpowers
```

当团队需要自动化升级证据时，创建分支、提交和 PR：

```bash
python3 scripts/openpowers_lite.py upgrade-check \
  --write-lock \
  --branch chore/openpowers-upstream-refresh \
  --commit "chore: refresh openpowers upstream lock" \
  --pr
```

升级命令只更新审计文件。它不会 vendor 上游 prompt、大量复制规则、重写 OpenSpec specs，也不会静默改变本地工作流规则。

## 设计边界

OpenPowers 明确不是：

- OpenSpec fork；
- Superpowers fork；
- 第二套产品规格系统；
- 从任一上游复制而来的大型 prompt 包；
- 会在没有审查的情况下静默改写本地规则的隐藏自动更新器。

如果这个仓库以后需要更强的能力，只在 diff 可审查且 OpenSpec 仍是唯一产品事实源的前提下添加。
