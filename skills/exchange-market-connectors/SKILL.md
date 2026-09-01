---
name: exchange-market-connectors
description: Design robust exchange and broker connectors using CCXT-style unified interfaces, capability detection, rate limiting, async streaming, normalization, retries, reconciliation, and venue-specific semantics.
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

# Exchange Market Connectors

## Purpose
Use for exchange/broker API integration, market-data ingestion, order placement, connector design, multi-venue routing, and AI-agent access to market APIs.

## CCXT architecture
Think in three layers:
1. Unified API for common operations.
2. Exchange-specific implementation: declarative endpoints, parsers, capability metadata and params.
3. Transport/runtime: REST/WebSocket, auth, throttling, retries and error translation.

CCXT's exchange-specific API is declarative: endpoint definitions in an exchange's `.api` surface are used to create implicit API methods. Unified methods are only the common subset. Capability discovery (`has`) and market metadata must precede assumptions about support.

## Connector contract
Normalize market ids, symbols, assets, precision, limits, product type, fees, order types, TIF, post-only/reduce-only semantics, leverage/funding, ids and timestamps. Preserve raw venue payloads and provenance.

## Rate limiting
Rate limits are control logic. Track endpoint costs/weights, shared budgets, burst behavior, public/private quotas and retry state. Back off on transient failures. Avoid retry storms and quota bans.

## REST/WebSocket
Use REST for snapshots, history, account reads and recovery. Use WebSockets for live feeds/orders when available. For stateful order books, design snapshot-plus-delta recovery and sequence validation.

## Order lifecycle
`intent -> validated request -> signed transport -> acknowledgement -> working -> partial fills -> terminal state -> reconciliation`.
Keep client ids, venue ids, fill ids and timestamps. For an unknown write outcome, reconcile before resubmitting. Do not blindly retry an order that might already exist.

## Multi-venue routing
Separate trade intent from venue choice. Consider fees, liquidity, spread, latency, inventory, venue health and execution constraints. Maintain a venue-health signal and explicit failover policy.

## AI-facing tools
Expose narrow high-level tools rather than arbitrary raw endpoints. Example tools: get_market, get_order_book, get_account_state, create_order, cancel_order, reconcile. Every write tool needs a schema, side-effect declaration, authorization policy, dry-run behavior and postcondition validation.

## Security
Never put API keys in prompts/logs/source control. Separate read-only market access from trade authority. Require approval for irreversible/high-consequence actions unless a prior policy explicitly grants authority.

## Failure tests
Timeouts, duplicate events, out-of-order messages, reconnect, clock drift, maintenance, delisting, precision mismatch, insufficient balance, reject, partial fill, unknown status and rate-limit exhaustion.


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

Normalize heterogeneous venue semantics behind an adapter layer; use endpoint-aware throttling, idempotency and order-state reconciliation.


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
