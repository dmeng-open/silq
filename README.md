# silq

**silq — A proactive, event-centered personal agent.**

Discover meaningful events, help people prepare, coordinate permitted actions, and follow through. The same Event/Goal/Action lifecycle supports work meetings, birthdays, tech events, and personal visits.

> **Status: design-only starter repository.** This package contains Claude Code/pstack instructions and project design docs, not a working agent. Implement capabilities incrementally and only report measured results.

## What makes this project special?

The engineering goal is an **evaluated agent runtime**, not another calendar summary application. Over time silq will demonstrate proactive decisions, context/evidence retrieval, layered memory, durable execution, dynamic planning, conditional multi-agent collaboration, MCP/A2A integration, risk-based approvals, trace-based evaluation, model routing, and gated skill improvement.

The user experience is intentionally narrow: **event → preparation → event occurrence → follow-up → verified outcome**. If an event is cancelled or a goal is declined, silq should safely stop/replan.

## How to start on Windows

1. Extract this starter into a directory such as `C:\dev\silq` (copy the **contents** into your repository root).
2. Open **PowerShell** in that directory; launch Claude Code:

   ```powershell
   Set-Location C:\dev\silq
   claude
   ```

3. pstack is already installed by you; within Claude Code, check `/` for its available command names. **Do not reinstall pstack.**
4. **Start each development task with the installed pstack entry command.** For the typical Claude Code plugin, send this as **one prompt**:

   ```text
   /pstack:poteto-mode 请阅读 CLAUDE.md、docs/PROGRESS.md 和 docs/ROADMAP.md。严格遵守小步学习约定；现在只实现 S01。先说清计划，再执行真实测试，生成详细中文学习报告并更新 PROGRESS.md。完成后立即停止，等待我确认 S02。不要自行推进后续步骤。
   ```

   If your installation exposes `/poteto-mode` instead, use the actual command shown in Claude Code's `/` menu. Do **not** stack `/pstack:poteto-mode /silq-next` as two slash commands. `/silq-next` remains an optional standalone helper. See `docs/PROMPTS.md` for examples.

5. Read `docs/learning/S01-*.md` after the first step. Ordinary questions don't need the prefix. Explicitly approve S02 before starting another pstack development task.

For a source-code explanation without edits, invoke `/silq-explain` and name a file/concept.

## Repository map

```text
CLAUDE.md                         Claude's project-level constraints
.claude/skills/silq-next/         One-step implementation and report protocol
.claude/skills/silq-explain/      Read-only learning/tutoring protocol
docs/PRODUCT.md                   User journeys and MVP boundaries
docs/ARCHITECTURE.md              Target architecture and design principles
docs/ROADMAP.md                   Atomic development steps
docs/PROGRESS.md                  Resume point, completion state
docs/LEARNING-CONTRACT.md         Teaching quality requirements
docs/EVALUATION.md                Testing and benchmark strategy
docs/SECURITY.md                  Permissions, privacy, prompt injection
docs/templates/LEARNING_REPORT_TEMPLATE.md
docs/learning/                   One Chinese report per completed step
docs/decisions/                  Architectural decision records
```

## Scope discipline

**First working slice:** deterministic synthetic calendar event → agent-like preparation decision → generated brief → verification. Real email/calendar integrations, persistent memory, agent collaboration, and self-improvement are later milestones and must be benchmarked, not assumed.

## Documentation order

1. `CLAUDE.md`
2. `docs/PROGRESS.md`
3. `docs/ROADMAP.md`
4. `docs/PRODUCT.md`
5. `docs/ARCHITECTURE.md`

## Safety

Never commit `.env`, OAuth tokens, raw personal emails, medical details or payment credentials. No automatic external actions until a policy+approval+idempotency path exists. See `docs/SECURITY.md`.
