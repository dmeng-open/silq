# Micro-step roadmap — proposed implementation, NOT blanket authorization

**Contract:** Implement exactly ONE item per user-approved Claude Code turn, validate it, create a real Chinese learning report, update `docs/PROGRESS.md`, then STOP. Milestones are conceptual: **do not implement an entire milestone in one go**. Any step can be split smaller, but never silently combined. The planned steps below are not implemented yet.

## Milestone A — verifiable domain foundation

| ID | Single learning goal / smallest shippable behavior | Evidence to collect |
| --- | --- | --- |
| **S01** | Python 3.12+ package, Windows PowerShell setup and `pytest` smoke import | Fresh install commands, passing smoke test, learning report |
| **S02** | `Event` identity, source and timezone-aware timestamp type | Valid/invalid fixture tests; no LLM |
| **S03** | Normalize a fake calendar record into one `Event` | Exact input→output contract test |
| **S04** | Event deduplication via canonical identity and source IDs | Repeated event not duplicated |
| **S05** | Lifecycle transitions for `DISCOVERED / QUALIFIED / CANCELLED` | Reject invalid transitions |
| **S06** | `Goal` separate from `Event`, with success criteria | Event ending does not auto-close goal |
| **S07** | `ActionRequest` schema with stable idempotency key | Same request same identity, changed args new identity |
| **S08** | Pure authorization policy: low-risk vs approval-required | Non-approved external action rejected |

## Milestone B — first runnable proactive event loop (all synthetic)

| ID | Single learning goal / smallest shippable behavior | Evidence to collect |
| --- | --- | --- |
| **S09** | Injectable virtual clock and fake event feed | Advance time without sleeping |
| **S10** | Deterministic proactive eligibility decision for ONE meeting | Acts on needed prep; ignores irrelevant event |
| **S11** | Explainable decision record with confidence/reasons | Trace includes why act/ignore |
| **S12** | Minimal brief generator using mock context and templates | One user-visible brief from synthetic event |
| **S13** | One end-to-end CLI command for fake event → brief | Reproducible Windows terminal demo |
| **S14** | User approve/decline decision for one suggested action | Declined action never executes |
| **S15** | Extend same runtime to Birthday fixture via small event Skill | No separate birthday agent |
| **S16** | Tech meetup and personal visit fixtures reuse shared contracts | Scenario parity, privacy boundaries |

## Milestone C — durability, reliable actions and realistic agent reasoning

| ID | Single learning goal / smallest shippable behavior | Evidence to collect |
| --- | --- | --- |
| **S17** | Persist workflow checkpoint locally | Restart resumes correct state |
| **S18** | Replay-safe fake tool action and idempotency store | Duplicate delivery does not duplicate effect |
| **S19** | Approval-bound-to-exact-arguments and expiry | Any material action change invalidates approval |
| **S20** | Fake tool fault injection: timeout after success | Retry reconciles actual state |
| **S21** | Model protocol + mock provider; one explicit LLM-assisted planning decision | Fake mode passes deterministically; real use opt-in |
| **S22** | Grounded Evidence record with source and as-of time | Missing/contradictory source not silently accepted |
| **S23** | Context selection for one meeting from a small evidence corpus | Show selected vs irrelevant snippets |
| **S24** | Typed tool-call adapter / schema validation | Invalid arguments are rejected before execution |
| **S25** | One long-horizon follow-up path using injected clock | Waiting, new reply, and cancellation transitions tested |

## Milestone D — advanced agent engineering with measured justification

| ID | Single learning goal / smallest shippable behavior | Evidence to collect |
| --- | --- | --- |
| **S26** | Stateful scenario evaluator with environment-state success oracle | Baseline success rate on seeded scenarios |
| **S27** | Proactive false-trigger benchmark and suppression rule | Precision/recall before vs after |
| **S28** | Structured trace and replay with sensitive data redaction | Trace proves actual decisions; safe logs |
| **S29** | One read-only real Calendar connector (consented, scoped) | Contract tests + opt-in integration test |
| **S30** | One read-only Email connector OR public event feed (choose after need assessment) | Untrusted content cannot issue commands |
| **S31** | MCP adapter to expose one existing controlled tool | Contract test and access boundary |
| **S32** | Independent Verification Agent for contradictory evidence | Evaluation vs single-agent baseline |
| **S33** | Dynamic routing threshold based on complexity, latency and measured quality | Simple task stays single-agent; eval delta |
| **S34** | A2A boundary for truly independent Research Agent service (optional experiment) | Interop success and overhead measured |
| **S35** | Persistent semantic/episodic memory with provenance, expiry, edit/delete | No stale facts or unintended profile inference |
| **S36** | Retrieval + reranking improvement on known hard queries | Groundedness/latency experiment |
| **S37** | Context compaction/selection under token budget | Cost/quality regression table |
| **S38** | Model routing for simple vs complex tasks | Cost per success measured |
| **S39** | Candidate reusable Skill generated from a failure trace | Candidate version recorded; not auto-promoted |
| **S40** | Hold-out evaluation + user approval for Skill promotion/rollback | Reject regressing candidate and demonstrate rollback |

## Important delivery principles

- The **first meaningful demo** should be reachable by S13, without email/calendar OAuth, UI or multi-agent architecture.
- If a step is too broad, split it into `Sxx.a`, `Sxx.b` and reflect this in PROGRESS; do not silently do both.
- Add LangGraph only when implementing durable agent execution after comparing to existing state machine; add PostgreSQL/pgvector only if existing data/query needs justify them.
- Frontend is an optional separate track **only after** CLI correctness and evaluations; do not build a dashboard as a dependency for the first demo.
- The order of advanced steps may be changed with user approval and an ADR; prove value through baseline comparisons.
- A report per step is mandatory, including documentation-only future steps.
