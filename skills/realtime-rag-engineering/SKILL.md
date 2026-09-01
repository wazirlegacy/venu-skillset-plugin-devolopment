---
name: realtime-rag-engineering
description: Architect, debug, and evaluate production RAG systems using the supplied Confluent guide plus independent RAG research. Cover ingestion, chunking, embeddings, semantic and structured retrieval, query decomposition, caching, freshness, validation, provenance, security, metrics, and vendor-neutral implementation choices.
metadata:
  version: "1.0"
  source_basis: "The Developer's Guide to RAG with Data Streaming + RAG research/NIST"
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

# Real-Time RAG Engineering

## Purpose

Treat RAG as a complete data-to-answer pipeline:

**data -> preparation -> indexing -> retrieval -> context assembly -> generation -> validation -> observability**

Do not reduce RAG to “put PDFs into a vector database”.

## Four-phase workflow

### 1. Data augmentation

Build a trusted external knowledge layer.

Actions:
- ingest new/changed data;
- clean and normalize;
- preserve source identity and timestamps;
- transform raw events into reusable data products;
- identify which content should be embedded;
- chunk meaningful unstructured content;
- generate embeddings;
- update the vector/semantic index.

### 2. Inference

At query time:
- interpret the question;
- retrieve relevant semantic context;
- query structured/transactional facts when exact values matter;
- apply authorization;
- assemble context with provenance/freshness metadata;
- generate an answer grounded in the selected context.

### 3. Workflows

Break complex requests into composable subproblems when that improves correctness.

A workflow can decide among:
- semantic retrieval;
- relational query;
- API;
- web search;
- cache;
- another LLM call;
- specialist agent/tool.

Avoid unnecessary chains. Every extra hop adds latency and another failure surface.

### 4. Post-processing

Before final output:
- validate factual claims against authoritative data where possible;
- enforce business rules;
- check policy/compliance constraints;
- detect unsupported or contradictory content;
- attach citations/provenance when appropriate;
- downgrade confidence or ask for clarification if validation fails.

## What to vectorize

Prefer semantic indexing when:
- content is unstructured;
- text has meaningful context;
- semi-structured records contain natural-language fields;
- research documents mix narrative and tables.

Do not blindly vectorize:
- pure identifiers;
- exact transactional aggregates;
- values whose semantics depend entirely on exact relational constraints.

For structured/unstructured mixtures, construct a semantically meaningful representation rather than embedding raw database dumps.

## Chunking

Chunk by semantic boundary where possible:
- section;
- paragraph group;
- record;
- FAQ;
- policy clause;
- logically complete unit.

Preserve metadata:
- document ID;
- source URL/path;
- version;
- date;
- heading;
- access policy;
- content type.

Avoid arbitrary chunking that destroys references or makes a chunk uninterpretable.

## Retrieval architecture

Use:
- dense semantic retrieval when meaning matters;
- lexical/exact retrieval when exact terms/identifiers matter;
- structured filtering when business truth matters;
- hybrid retrieval when both are important;
- reranking when the candidate set is large enough to justify it.

A useful pattern is:

**retrieve candidates -> apply authoritative filters -> rerank -> contextualize -> generate**

Do not assume higher embedding similarity means factual correctness.

## Query decomposition

For a compound request:
1. detect independently answerable subquestions;
2. route each to its best retrieval source/tool;
3. collect evidence;
4. reconcile contradictions;
5. assemble a final answer.

Example categories:
- current numeric value -> relational source;
- policy text -> document retrieval;
- identity/availability -> transactional/API source;
- prior answer -> cache when still valid.

## Caching

Cache only when:
- the answer is reusable;
- the underlying data is sufficiently stable;
- the cache key captures relevant user/tenant/permissions;
- TTL/invalidation rules are explicit.

Never return a cached answer that can violate current authorization or critical freshness requirements.

## Freshness

Every time-sensitive RAG system should have:
- a freshness target;
- source timestamp;
- index/update timestamp;
- stale-data threshold;
- fallback behavior.

If the freshness target is exceeded:
- signal staleness;
- use the latest confirmed snapshot only when acceptable;
- do not represent stale context as current.

## Provenance and trust

Track:
- where the source data came from;
- what transformations occurred;
- which chunks/records were retrieved;
- when they were retrieved;
- which model/version generated embeddings and output;
- what validation occurred.

NIST guidance supports documenting data origin/lineage and testing data/content flows and outputs against known ground truth.

## RAG evaluation

Evaluate separately:

### Retrieval
- recall@k / hit rate;
- relevance;
- coverage;
- stale retrieval rate;
- duplicate/noisy retrieval.

### Generation
- factuality;
- completeness;
- groundedness;
- unsupported-claim rate;
- refusal/abstention quality.

### System
- latency p50/p95/p99;
- throughput/QPS;
- token/call cost;
- cache hit rate;
- freshness;
- authorization failures.

### Business
- task success;
- resolution rate;
- user satisfaction;
- conversion/recommendation quality where applicable.

Do not use one LLM-as-judge number as the entire evaluation.

## Scientific guardrails

The original RAG paper demonstrates that retrieval-augmented systems can outperform parametric-only baselines on tested knowledge-intensive tasks. Later research also shows that poor/noisy retrieval can itself harm factual reliability. Therefore:
- RAG is not a guarantee against hallucination;
- retrieval quality must be measured;
- validation is a separate layer.

## Vendor-specific implementation note

The supplied Confluent guide describes a Stream/Connect/Process/Govern model, Kafka/Flink-style processing, vector-store integrations, and model inference inside stream processing. Retain these as concrete implementation patterns, but do not make Confluent mandatory.

## Output

For a RAG architecture request:
1. use case and data freshness;
2. data sources;
3. data preparation;
4. vector/semantic indexing;
5. structured retrieval;
6. query decomposition;
7. context assembly;
8. generation;
9. post-processing;
10. security/governance;
11. evaluation;
12. cost/latency trade-offs.


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

Define freshness SLAs; route exact structured questions to structured data and semantic questions to retrieval; monitor retrieval noise and latency.


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
