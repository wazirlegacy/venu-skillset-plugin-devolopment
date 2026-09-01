---
name: agentic-memory-architecture
description: Design memory, retrieval, state, temporal context, and data architecture for reliable agentic AI systems. Use the supplied O'Reilly Agentic AI Data Architectures report plus independent RAG/agent research and current database documentation. Apply semantic, transactional, temporal, and event-oriented patterns with explicit consistency and latency trade-offs.
metadata:
  version: "1.0"
  source_basis: "Agentic AI Data Architectures (O'Reilly/PingCAP) + independent verification"
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

# Agentic Memory Architecture

## Purpose

Design the data/memory substrate that lets an agent preserve:
- facts;
- context;
- intentions;
- task progress;
- historical state;
- feedback;
- semantic associations.

The core question is not simply “which vector database?” It is:

**What information must remain true, what information must remain retrievable, and what information must remain temporally coherent?**

## Agent anatomy

Use the source's operational decomposition:

1. Persona / job function.
2. Perception.
3. Reasoning and decision-making.
4. Memory.
5. Planning.
6. Action.
7. Learning.
8. Coordination/collaboration.
9. Tool interface.

Treat memory and tools as architecture components, not prompt text.

## Memory taxonomy

### Working / short-term memory
Current task context, active constraints, intermediate decisions.

Use for:
- conversation continuity;
- immediate planning;
- tool results.

### Long-term memory
Durable facts worth carrying across sessions.

Possible representations:
- structured records for explicit facts;
- vector memory for semantic recall;
- hybrid stores for both.

### Episodic memory
Time-bound event/session details.

Use for:
- “continue where we left off”;
- multistep task state;
- recent decisions and unresolved work.

### Temporal memory

Use when the question depends on what was true **at a particular time**.

Store:
- valid time;
- transaction/system time where relevant;
- source/version;
- retrieval timestamp.

Never collapse historical state into the current state when temporal fidelity matters.

## Retrieval patterns

### Semantic-transactional join

Combine semantic similarity with authoritative relational filters.

Example:
- retrieve semantically similar cases;
- only accept rows satisfying current account/status/territory constraints.

This reduces the risk of returning semantically relevant but operationally invalid context.

### Contextual fact augmentation

Retrieve semantic context and attach structured facts:
- account size;
- renewal date;
- region;
- status;
- inventory quantity.

This is preferred when meaning and exact facts both matter.

### Probabilistic join

When identity is uncertain:
- compute similarity features;
- produce a confidence score;
- keep candidate matches visible;
- require thresholded acceptance or human review.

Never silently convert a fuzzy match into a fact.

### Sliding-window context

Combine:
- recent event stream;
- longer historical aggregates.

Use for:
- anomaly detection;
- fraud;
- operations;
- real-time personalization.

Prefer incremental updates and bounded windows rather than repeatedly scanning all history.

### Microbatch refresh

When true streaming is unnecessary but freshness matters:

1. define freshness target;
2. trigger small batches;
3. ingest only changes since watermark;
4. apply a small safety delay where race conditions are possible;
5. validate/dedupe/transform;
6. merge atomically;
7. advance watermark and emit monitoring metrics;
8. expose timestamped results.

On failure:
- keep last successful watermark;
- retry with exponential backoff;
- use idempotent merge/upsert;
- mark data stale when freshness target is exceeded.

### Incremental fact synchronization

When semantic indexes depend on transactional data:
1. emit row-level changes/CDC;
2. re-embed changed records;
3. update the semantic index;
4. query semantic and transactional truth together;
5. retain version/timestamp linkage.

This avoids a vector index silently diverging from authoritative state.

## Architecture selection

Choose among:
- relational/transactional store;
- vector store;
- event log/stream;
- document/content store;
- distributed SQL;
- hybrid architecture.

Base the choice on:
- data semantics;
- consistency requirements;
- freshness;
- scale;
- latency;
- write rate;
- retrieval mode;
- failure/replay requirements;
- governance;
- cost.

Do not assume distributed SQL is always the best answer. The supplied report makes a strong case for it, but the choice remains workload-dependent.

## Distributed SQL: source-derived implementation pattern

The O'Reilly report describes distributed SQL as:
- SQL/relational semantics;
- ACID transactions;
- horizontal distribution;
- partitioning and replication;
- consensus such as Raft.

Current TiDB documentation independently describes TiDB as a distributed SQL database with horizontal scalability, strong consistency/high availability, and a TiDB/TiKV/PD architecture. TiDB documentation also describes TiFlash for HTAP and Multi-Raft replication.

When discussing TiDB, distinguish:
- **general architectural principle**;
- **TiDB-specific mechanism**.

For example, TiDB's Region sharding, Multi-Raft, TiKV/TiFlash roles, and resource controls are implementation details, not universal requirements.

## Reliability architecture

Design for:
- idempotency;
- replay;
- checkpoints/watermarks;
- stale-data detection;
- versioned data;
- partial failure;
- observability;
- authorization;
- auditability.

Prefer infrastructure-level guarantees for invariants rather than asking every application to reimplement them.

## Latency reasoning

Break latency into:
- average/happy path;
- tail latency;
- cold/cache-miss;
- cross-node;
- index update/maintenance.

When optimizing:
1. reduce unnecessary round trips;
2. colocate frequently joined data when practical;
3. parallelize independent reads;
4. use caching when correctness permits;
5. avoid adding orchestration layers without measuring their effect;
6. define p50/p95/p99 targets where relevant.

## Output

For an architecture request produce:
1. Requirements and constraints.
2. Data taxonomy.
3. Memory model.
4. Retrieval patterns.
5. Consistency/freshness policy.
6. Failure/replay plan.
7. Latency plan.
8. Governance/security.
9. Technology options and trade-offs.
10. Test/evaluation plan.

## Guardrails

- Memory is not automatically safe because it is useful; apply retention/access rules.
- Do not persist sensitive information merely because it may be useful later.
- Avoid anthropomorphic claims about “learning” unless a specific mechanism exists.
- Do not copy vendor-specific architecture into a vendor-neutral design without labeling it.
- When current product capabilities matter, verify with current primary documentation.


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

Define memory semantics, temporal validity and authority before storage selection; support stale-data signaling, idempotency and replay.


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
