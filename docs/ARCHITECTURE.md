# Target architecture (design intent — NOT implemented)

> This is a map, not permission to scaffold everything now. Only implement a module when its roadmap step is approved. Keep an explicit distinction between live code and planned boundaries.

## Core system

```text
Synthetic Fixture / (later) Calendar, Email, Public Event Source
           |
      Event Adapter
           |
    Canonical Event Store ---> Evidence Store (source, timestamp, trust)
           |
   Proactive Decision Gate <---- User Preferences / Opt-in / Cooldowns
           |
      Goal & Plan Manager <---- Provenance-aware Memory
           |
        Task Router -------> Optional specialized Research/Verifier
           |
  Policy + Approval Gate (non-LLM enforcement)
           |
  Durable Action Executor ----> Fake tools first, then MCP connectors
           |
   State Reconciliation / Follow-up
           |
        Traces + Evaluation ----> Skill candidate -> held-out tests -> user approval
```

## Domain invariants (teach, test, then implement)

- **Event != Goal != Action.** An event may create several goals; an event being over does not close unresolved goals.
- Events have stable IDs, source references, timezone-aware event times, cancellation/reschedule semantics, and dedupe rules.
- Goals have user intent, explicit success criteria, owner, expiry and states; no inferred goal is authorized to create external side effects.
- Action requests have idempotency key, parameters, risk level, authorization scope and execution record. Approval binds to **exact** action arguments and expires on meaningful change.
- Facts from sources have provenance and timestamps. Conflicting sources must be reconciled, not merged by vibes.
- External data is never treated as a system instruction. Policies execute in trusted deterministic code.
- Resuming a workflow may rerun a node, but must not duplicate an external side effect.

## State machine — conceptual

`DISCOVERED -> QUALIFIED -> PREPARING -> READY -> OCCURRED -> FOLLOWING_UP -> CLOSED`

Terminal/exception states: `DECLINED`, `CANCELLED`, `PAUSED`, `FAILED`. Replanning can occur from active stages. There is no silent auto-close because an event timestamp passed. Actual implementation is developed in small, tested steps.

## Proposed Python package boundaries (create incrementally)

```text
src/silq/
  domain/             # Event, Goal, Action and pure lifecycle transitions
  runtime/            # Planning, checkpoint/resume, tool execution
  proactive/          # Candidate detection, prioritization, suppression
  context/            # Evidence retrieval, provenance, memory
  integrations/       # Fake and real connectors; MCP later
  evaluation/         # Scenario runner, deterministic state validators
  observability/      # Structured events, traces, cost stats
```

Do NOT create folders before the roadmap step needs them. Start with a single module; extract later if justified by tests and complexity.

## Agent strategy

- Baseline: deterministic state transitions + **single** planner with fake model interface.
- Add a verifier only once evidence conflicts need independent judgment.
- Add dynamic routing only after measuring baseline and giving each agent a non-overlapping role.
- Treat A2A as an **interoperability experiment**, not required for local function calls. MCP is useful only where tool integration exists.
- Keep model-free deterministic business rules for safety and execution invariants.

## Data and infrastructure evolution

1. In-memory fakes for domain behavior and benchmark scenarios.
2. SQLite persistence for local development (if needed); transactional outbox/idempotency when actions exist.
3. PostgreSQL only if the features justify concurrent workers or real deployment.
4. Add LangGraph durable checkpoint workflow after verifying desired retry and replay semantics; avoid double orchestration layers.
5. Add search, reranking, pgvector and context compression after collecting retrieval failure cases.
6. Add A2A, model routing and eval-gated skills as **separate measured experiments**.

## Key engineering demonstrations

- **Proactive:** act-vs-ignore choices and false interruption rate.
- **Context:** cited sources, recency, uncertainty and contradictions.
- **Runtime:** crash/restart tests, idempotent side effects, approval continuity.
- **Optimization:** baseline vs new routing/memory/skill with independent evaluation.
- **Security:** malicious instructions inside an email or event description never bypass policy.

See `docs/decisions/ADR-0001-core-decisions.md` for why this is deliberately incremental.
