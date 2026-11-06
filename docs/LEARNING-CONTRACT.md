# Learning contract — the most important project deliverable

The purpose of silq is **to learn and demonstrate agent engineering**. Claude/pstack is an instructor and implementer, not an autopilot team that ships large chunks without explanation.

## Per-turn sequence (one step only)

1. Read `CLAUDE.md`, `docs/PROGRESS.md`, the corresponding roadmap step, and touched source/tests.
2. Explain a **small concrete change** in Chinese: learning objective, inputs/outputs, boundary, verification and what is explicitly OUT of scope.
3. Use the installed pstack workflow **only within this step**: read/think, TDD if appropriate, implement minimum, verify, focused code review.
4. Write `docs/learning/SXX-<slug>.md` using the template. Explanation must quote **actual** code snippets and annotate file path + line number. Do not fill a hypothetical implementation into a completed report.
5. Update progress with a real, reproducible verification summary and exactly one next step.
6. Respond in Chinese with implementation summary, report path, one key insight, one learning exercise, and **stop for approval**.

## Learning report quality gate

Every report must answer:

1. **Why now?** What one agent-engineering problem did this step solve?
2. **Mental model:** what are inputs, outputs, persistent state and failure modes? Include a tiny text diagram where appropriate.
3. **Code walkthrough:** show exact module path + actual function/class names, 2–3 small excerpts and explain important lines/branches; show line numbers or an explicitly identified code revision.
4. **Design decision:** compare at least one plausible alternative and the trade-off.
5. **Verification:** commands in Windows PowerShell, actual output, tests/negative cases. If commands weren't run, say so and why.
6. **Pitfall:** describe a realistic failure mode and how it is (or isn't yet) prevented.
7. **What is NOT built yet?** No marketing-style claims.

Do not merely write an API usage tutorial. Connect each concept to an invariant and observable behavior in this repository.

## Report file naming and truthfulness

One file per completed roadmap step, e.g. `docs/learning/S01-python-env-and-smoke-test.md`, in UTF-8 Chinese (English API names intact). Report must be readable without chat history. Use real paths/line references; keep excerpts short. If code/tests fail, create a **BLOCKED report**, identify blocker, and do not mark step complete.

## Scope and interaction gate

- One roadmap step **per turn**, not one phase.
- The user's approval is required before advancing `docs/PROGRESS.md` to new active work.
- Do not generate placeholder reports for future steps.
- Avoid running independent parallel work streams, autopilot, or overnight jobs: they undermine the one-step teaching loop.
- Technical research and clarification are fine, but any additional implementation is a **new step requiring approval**.
