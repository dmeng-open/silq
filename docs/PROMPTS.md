# Claude Code + pstack prompt recipes (Windows)

Use the command **available in your installation**, typically `/pstack:poteto-mode` in Claude Code. Some distributions offer `/poteto-mode`. Find the actual command in the `/` menu. For each **new development task**, explicit invocation is safer than assuming that `CLAUDE.md` automatically runs it. Some distributions have sticky/automatic routing; that behavior varies.

## First development task (S01)

```text
/pstack:poteto-mode 请阅读 CLAUDE.md、docs/PROGRESS.md、docs/ROADMAP.md 和 docs/LEARNING-CONTRACT.md。严格只完成 S01，不做 S02。先说明学习目标、涉及文件及验证计划。使用 pstack 的严谨开发流程，在 Windows PowerShell 真正运行测试；完成后生成 docs/learning/S01-python-env-and-smoke-test.md 中文学习报告，更新 PROGRESS.md，然后立即停止，等待我批准下一个步骤。
```

## Every later approved micro-step

```text
/pstack:poteto-mode 我批准开始 docs/PROGRESS.md 中的下一个微步骤。遵守 CLAUDE.md，只做一个步骤；先说明计划；实施最小改动并真实验证；解释关键代码；写对应 docs/learning/SXX-*.md 学习报告；更新 PROGRESS.md；然后停止，等待我确认。
```

## Fix a bug within the current step

```text
/pstack:poteto-mode 我在当前 SXX 步骤发现问题：[错误与复现命令]。只调查并修复此问题，先复现、再做最小修改及测试。记录报告更正并更新 PROGRESS.md；不得开始下一个步骤。
```

## Discuss a design decision (read only)

```text
/pstack:poteto-mode 只调查，不改代码。针对 silq 的 [具体设计问题]，给出两个方案的可靠性、复杂度和可验证性对比，并推荐一个方案。等待我确认后再实现。
```

## Ask a learning question (no prefix necessary)

```text
请只解释 SXX 学习报告里 [函数/概念] 的执行流程，展示一个输入输出例子及一个练习。不修改文件。
```

## Rules

- Do not stack two slash commands (`/pstack:poteto-mode /silq-next`) in one message; after one slash command use ordinary text.
- Prefix is recommended for new engineering tasks, not required for all Q&A.
- Disable/avoid overnight, autopilot, or auto-merge behavior that would bypass approval after every micro-step.
- Record real verification evidence; never claim tests passed without running them.
