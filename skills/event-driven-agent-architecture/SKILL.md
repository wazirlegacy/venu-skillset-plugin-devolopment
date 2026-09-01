---
name: event-driven-agent-architecture
description: Design resilient event-driven single-agent and multi-agent systems using the supplied Confluent guide plus independent event-driven architecture references. Cover agent anatomy, EDA, Orchestrator-Worker, Hierarchical, Blackboard, Market-Based patterns, event contracts, replay, idempotency, DLQs, observability, governance, and trade-offs.
metadata:
  version: "1.0"
  source_basis: "A Guide to Event-Driven Design for Agents and Multi-Agent Systems + EDA verification"
---
## Evidence posture
Ground recommendations in current primary sources, official documentation, standards, primary repositories/tests, and peer-reviewed research where applicable. Separate documented behavior from inference, vendor claims, benchmarks, and speculation; record version/date assumptions.

## Operating workflow
1. Frame the objective, inputs, outputs, constraints, environment, versions, success criteria, trust boundaries, and irreversible side effects.
2. Select the simplest architecture and mechanisms that satisfy the requirements; state assumptions and dependencies.
3. Define interfaces/contracts, state ownership, invariants, error/failure classes, security controls, observability, and rollback/recovery.
4. Implement a smallest testable path, then add integration, adversarial, regression, recovery, and performance coverage appropriate to risk.
5. Verify outputs and postconditions against authoritative state and record evidence, measurements, and unresolved risks.
6. Re-check fast-changing dependencies and versions before production decisions.

## Quality gates
- No invented APIs, undocumented guarantees, or silent assumptions.
- Validate important inputs, outputs, permissions, side effects, provenance, and postconditions.
- Test failure, abuse, recovery, rollback, and version-change paths.
- Protect secrets and irreversible operations behind explicit controls.
- Prefer deterministic controls for high-consequence decisions.

Combine this Skill with other Venu Skills when a task crosses domains; use the minimum sufficient Skill set, explicit precedence, shared contracts, and the Skill router/composer rather than blending incompatible assumptions.

# Event-Driven Agent Architecture

## Purpose

Use event-driven architecture (EDA) when agents need:
- asynchronous work;
- loose coupling;
- dynamic fan-out/fan-in;
- real-time event reaction;
- replay/recovery;
- independent scaling;
- multi-agent coordination.

Do not choose EDA only because it is fashionable. Compare it with synchronous request/response and hybrid designs.

## Agent anatomy

Model an agent as:
1. persona/job function;
2. perception;
3. reasoning/decision;
4. memory;
5. planning;
6. action;
7. learning/feedback;
8. coordination;
9. tool interface.

Every external action should have:
- an explicit intent;
- authorization;
- an execution handler;
- a result/event;
- outcome validation.

## Event model

A useful minimum event envelope:

```text
event_id
event_type
schema_version
occurred_at
source
subject/key
correlation_id
causation_id
tenant/security_context
payload
```

Use immutable identifiers and schema versions. Keep business payload separate from routing/observability metadata.

## Architecture loop

Use:

**Input -> Process -> Output**

Input:
- command;
- state change;
- external event;
- timer;
- agent result.

Process:
- validate;
- retrieve context;
- reason;
- call tools;
- update state;
- emit result.

Output:
- new event;
- external side effect;
- status update.

## Design pattern 1 — Orchestrator-Worker

Use when a central planner should decompose work but execution can scale horizontally.

Event-driven form:
1. orchestrator publishes work events;
2. workers consume through a consumer group;
3. partition/key routing preserves per-entity ordering where needed;
4. workers publish results;
5. orchestrator correlates results.

Benefits:
- dynamic worker count;
- replay/recovery;
- independent scaling.

Failure controls:
- idempotency keys;
- offsets/checkpoints;
- retry policy;
- dead-letter route.

## Design pattern 2 — Hierarchical Agents

Use when complex goals naturally decompose into nested domains.

Event-driven form:
- top-level agent publishes objective;
- mid-tier agents consume and decompose;
- lower-tier agents execute;
- results propagate upward through events.

Each non-leaf node can behave as an orchestrator for its subtree.

Avoid deep hierarchies unless the decomposition creates real specialization. Too many layers increase latency and observability burden.

## Design pattern 3 — Blackboard

Use when multiple agents need shared asynchronous context.

Implementation idea:
- shared event stream/topic or durable state layer;
- agents publish findings/updates;
- other agents subscribe or retrieve relevant state.

Treat the blackboard as shared knowledge, not as an uncontrolled command bus.

Use:
- event IDs;
- versioning;
- conflict handling;
- access controls;
- retention rules.

## Design pattern 4 — Market-Based

Use when agents should compete/negotiate for tasks or resources:
- bids/offers;
- matching;
- allocation;
- decentralized optimization.

A shared event log can replace direct peer-to-peer connections and reduce interaction complexity.

Require explicit:
- bid schema;
- valuation/priority rule;
- winner selection;
- timeout;
- compensation/rollback where applicable.

## Reliability

### Idempotency
Every event-driven action that can be retried should have an idempotency strategy.

Examples:
- operation ID table;
- transactional outbox/inbox;
- deterministic state transition;
- dedupe key.

### Replay
Store enough event history and checkpoint state to reproduce or restore progress.

### Dead-letter handling
Route unprocessable events to a controlled failure path with:
- original event;
- error category;
- retry count;
- timestamps;
- correlation IDs.

### Ordering
Do not assume global order. Define the ordering key only where business semantics require it.

### At-least-once reality
Design actions so duplicate delivery is safe unless the platform explicitly guarantees stronger semantics and the application uses them correctly.

## Event contracts

Define:
- schema;
- versioning;
- compatibility rules;
- required vs optional fields;
- ownership;
- privacy classification;
- retention;
- consumer expectations.

Treat schemas as product interfaces.

## Observability

Track:
- event throughput;
- consumer lag;
- processing latency;
- retries;
- DLQ rate;
- duplicate rate;
- replay count;
- state divergence;
- agent action outcomes;
- tool failure rates;
- decision trace/correlation IDs.

Agentic systems require both system telemetry and decision/audit telemetry.

## Security/governance

Before a tool action:
- authenticate;
- authorize;
- check data classification;
- enforce tenant/field permissions;
- record the decision and result.

Never let event-driven decoupling become a bypass for authorization.

## When not to use EDA

Prefer synchronous or hybrid architectures when:
- the interaction is simple and request-scoped;
- the caller must receive an immediate deterministic acknowledgement;
- event indirection would obscure a simple business flow;
- ordering/transaction semantics are easiest to express in one transaction;
- operational teams cannot yet support event observability.

The right answer is often hybrid:
- synchronous request for user-facing command;
- event-driven background work;
- synchronous status query or streamed progress.

## Output

For an EDA design:
1. business events;
2. agents and responsibilities;
3. event schemas;
4. topics/queues/streams;
5. partitioning/keys;
6. state stores;
7. orchestration pattern;
8. retries/idempotency/DLQ;
9. replay/recovery;
10. observability;
11. security/governance;
12. latency/cost trade-offs.

## Vendor-specific implementation note

The supplied Confluent guide describes Kafka-style event streaming, consumer groups, offsets/replay, Flink stream processing, and managed governance. Keep these as implementation examples rather than universal requirements.


## 10/10 Operating Contract — mandatory quality bar

This skill is a production-grade, evidence-aware capability. Apply this contract on every non-trivial task.

### Task framing
Identify the objective, inputs/outputs, environment and versions, constraints, success metrics, cost/latency limits, trust boundaries, and irreversible side effects before acting.

### Evidence discipline
Prefer current official documentation/specifications, primary repositories/tests, standards bodies and peer-reviewed research. Clearly distinguish documented behavior, measured results, vendor/project claims, inference and speculation. Re-check fast-changing facts at execution time.

### Architecture discipline
Define interfaces, state ownership, lifecycle, invariants, failure modes, security boundaries, observability, performance budgets, and rollback/migration paths. Choose the simplest architecture that satisfies the requirements.

### Deterministic controls
Probabilistic models, agents and heuristics may propose. Deterministic policy layers must authorize high-consequence actions, validate schemas and postconditions, enforce quotas/limits, protect secrets, and control filesystem/network/financial side effects.

### Verification
Use appropriate unit, property/invariant, integration/contract, end-to-end, adversarial, regression and performance tests. A successful build, HTTP 200, or model confidence is not proof of correctness.

### Postconditions
For every consequential action, verify the authoritative resulting state independently. When a tool or external system reports acceptance, confirm the actual effect.

### Security
Apply least privilege, explicit trust boundaries, secret isolation/redaction, secure defaults, input/output validation, supply-chain hygiene, rate limits, resource limits, safe logging and safe failure. Design for zero trust when crossing trust boundaries.

### Reliability and observability
Define timeouts, bounded retries/backoff, idempotency, failure classification, structured logs, metrics, traces, correlation IDs, health signals and recovery/rollback. Use dead-letter/replay/checkpointing where justified by the workload.

### Performance
Define the metric and baseline first. Measure representative workloads; do not optimize solely from intuition or benchmark headlines.

### Provenance and uncertainty
Record source/version/time, transformations, assumptions and uncertainty for important recommendations/data. Preserve temporal validity where facts change.

### Skill composition
For cross-domain work, identify the minimum sufficient Skills, dependencies, precedence and shared contracts. Resolve conflicts explicitly; do not silently blend incompatible assumptions.

### Completion report
For substantial work, report what changed, what was verified, tests and results, known limitations, version assumptions, rollback path and unresolved risks.

## 10/10 acceptance rule
A Skill is release-ready when its instructions are actionable, its important claims are traceable, its failure/security boundaries are explicit, its workflow is testable, and its outputs compose cleanly with the other Venu Skills.


## 10/10 Domain Specialization

Use EDA when decoupling/replay/fan-out justify it; define event schemas, ordering, partitions, idempotency and dead-letter/replay semantics.


## Research anchors — verified/current snapshot 2026-09-01

Primary sources to re-check when implementation decisions depend on changing behavior:
- Agent Skills specification: https://agentskills.io/specification
- MCP specification update (2026-07-28): https://blog.modelcontextprotocol.io/posts/2026-07-28/
- NIST AI RMF GenAI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Top 10:2025: https://owasp.org/Top10/
- OpenTelemetry signals/semantic conventions: https://opentelemetry.io/docs/concepts/signals/
- DORA 2025: https://dora.dev/research/2025/dora-report/

## Integration

Combine this Skill with other Venu Skills when a task crosses domains. Use the minimum sufficient Skill set, explicit precedence, shared contracts, and the Skill router/composer; do not silently blend incompatible assumptions.
