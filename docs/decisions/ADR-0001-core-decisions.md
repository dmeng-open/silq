# ADR-0001 — Start with domain invariants and a synthetic vertical slice

- **Status:** Accepted as initial teaching plan; revise with measured evidence
- **Date:** 2026-11-06

## Context

silq aims to cover frontier agent engineering concepts, but is built by one engineer who wants to learn every layer. Starting with many microservices and real OAuth integrations would hide core logic, make failures expensive, and reduce learning quality.

## Decision

1. **Python-first** for agent runtime; thin UI only after terminal workflows are correct.
2. **Synthetic Event data and deterministic fake tools first**, live calendar/email later.
3. Separate **Event**, **Goal**, **Action** with explicit identities and lifecycle invariants.
4. **Single-agent baseline** before independent Research/Verification roles; justify routing with evaluations.
5. **Test-first, one micro-step then Chinese learning report** with user approval before next step.
6. **Policy enforced outside the LLM**; external side effects gated by exact approval and idempotency.
7. **Measured optimization**: only adopt persistent memory, MCP/A2A, model router and self-improving skills when there is an observable problem and an eval baseline.

## Consequences

Advantages: small reproducible increments, faster recovery from wrong assumptions, safer demos, cleaner explanations. Costs: initially less flashy UI and no real email/calendar connectivity. This is intentional, not a missing feature.

## Alternatives not selected yet

Full Next.js app first; event-specific agents from day 1; PostgreSQL/Kafka/Kubernetes from day 1; continuous autonomous self-modifying code; real checkout APIs. Revisit on evidence, not popularity.
