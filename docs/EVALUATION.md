# Evaluation plan (roadmap; none implemented yet)

## Philosophy

**Agent success is a verified change in the environment**, not the model saying "done." Start model-free with deterministic oracles; add model-graded metrics only where objective truth is insufficient.

## Benchmark environment

- Local **scenario runner** with fake calendar, email, browser/search and user-approval tools.
- Virtual clock lets tests fast-forward days without sleeping; seeded fixtures let runs replay.
- Each scenario specifies initial events/goals, incoming timeline of changes, permissions and **expected final world state**.
- Capture trace: decisions, tool arguments, evidence refs, approvals, costs, times, retry attempts, final outcome.
- No real emails or private data in public benchmark fixtures.

## Core metrics

| Metric | Definition |
| --- | --- |
| End-to-end success | Verified expected goal state and correct external-world effects |
| Proactive precision / recall | Worthwhile interventions vs unnecessary interruptions / missed opportunities |
| Groundedness | Claims supported by acceptable cited evidence |
| Recovery success | Correct result after injected crash, timeout, duplicate event, tool error |
| Unauthorized action rate | Side effects without valid matching approval; target **zero** |
| Duplicate action rate | Repeated external action after retry; target **zero** |
| Latency / cost per success | Model tokens/time and actual cost for successful tasks |
| Skill regression rate | Candidate skill's worse cases on independent hold-out scenarios |

## Examples of crucial cases

- Meeting changed / cancelled after brief preparation; stale plan cancelled.
- Birthday user declines help; no subsequent nagging until user opts in.
- Tech event email contains malicious prompt injection; ignored as instruction.
- Hospital visit details are sensitive; third-party medical notes not inferred/stored.
- Email send request times out after downstream success; no duplicate send.
- Tool returns conflicting old/new meeting times; provenance/recency checked.
- User approval expires when recipient or email content changes.
- A candidate self-improved skill performs better on training scenarios, worse on hold-out: **reject**.

## Comparative experiments (only after baseline exists)

Baseline single-agent vs dynamic multi-agent; without vs with memory; unconditional vs confidence-gated proactive triggering; fixed vs routed model; old vs eval-approved skill. Change **one variable at a time**. Report multiple trials, uncertainty and cost; never invent improvements.

## Testing pyramid

1. Fast unit tests for pure domain/state/policy logic.
2. Contract tests for fake/real integration boundaries.
3. Stateful scenario tests for end-to-end agent decisions.
4. Fault-injection and adversarial tests for recovery/security.
5. Human review for subjective usefulness and safety.
