# Product brief — silq

## Promise

**Before** an important event, silq identifies preparation needs. **During** its lifecycle, it monitors relevant changes. **After**, it tracks commitments and verifies follow-through. It acts proactively but does not invent user intent.

## User and goals

Initial user: one technical individual learning advanced agent engineering while managing real calendar events. The project must be personally usable without needing third-party business contracts or a live payment stack.

- Users see meaningful upcoming events and **why silq thinks action is useful**.
- Users can approve/decline proactive suggestions and edit goals, budgets and preferences.
- Users can see the plan, evidence, pending approvals, actions performed and next check.
- Users can stop tracking an event or revoke permissions at any time.

## Four representative journeys (synthetic test personas first)

| Event | Before | During / change | After | Guardrail |
| --- | --- | --- | --- | --- |
| Work meeting | Review prior context; open questions; agenda brief | Schedule/participants changed; replan | Extract user-supplied commitments; follow up after consent | Never send unapproved external email |
| Birthday | Ask whether to prepare; use approved preference | Gift deadline / plan change | Optional check-in and feedback | Do not assume marketing email implies preference |
| Tech meetup | Discover relevant public event; research agenda | Registration/deadline/location change | Extract notes; propose follow-up research | Web content is untrusted data |
| Hospital visit | Check public visiting policy and travel plan | Time/visiting policy changed | Optional gentle check-in | Don't infer/store patient diagnosis or read third-party health records |

## Unified experience

1. Discover an event from mock data, later calendar/email or approved feeds.
2. Qualify: relevance, confidence, consent, urgency, suppression rules.
3. Plan: create explicit user goals with success criteria; fetch cited evidence.
4. Prepare: draft briefing / tasks; request approval for external side effects.
5. Reconcile changes: cancellation, reschedule, response, new information.
6. Event occurs (only after evidence/confirmation, not just passage of time).
7. Follow up: track independent goals and prove completion.
8. Learn: update approved preferences and propose skill improvements subject to eval gates.

## MVP / non-goals

**MVP:** one synthetic meeting event and a deterministic full loop, local CLI, minimal tests and trace. Event model supports other types but no real connectors. First real connector later is **calendar read-only**; email read-only later and only if justified.

**Not MVP:** automatic email sending, gift purchases, patient health data, browser automation, complex recommendation engine, public SaaS hosting, multi-tenancy, real-time availability guarantees, always-on background operation, A2A distributed deployment.

## Success means

The demo runs on Windows from a clean checkout with fake data; every decision can be explained; external actions never happen without permission; errors can be reproduced; benchmark results are measured rather than made up. Future versions can add real integrations without rewriting Event/Goal contracts.
