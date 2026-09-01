---
name: integrated-ai-development-architect
description: Combine trading engines, exchange APIs, research agents, LLM runtimes, RAG/memory, browser intelligence, MCP, workflows, evaluation, and infrastructure into coherent production-oriented AI systems.
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

# Integrated AI Development Architect

## Purpose
Cross-domain architecture skill for systems spanning the user's trading, agent, RAG, model, MCP, web and infrastructure research.

## Layer map
1. Data plane — exchanges, OpenBB, APIs, websites, documents, OCR, streams.
2. Knowledge plane — RAGFlow/LlamaIndex/Supermemory-style retrieval and memory.
3. Reasoning plane — LangChain/LangGraph, Dify, Langflow, TradingAgents, Hermes.
4. Tool plane — CCXT, browser-use, MCP, public APIs, n8n tools.
5. Model plane — hosted models, Transformers, vLLM, llama.cpp, Ollama-compatible endpoints.
6. Execution plane — NautilusTrader/Freqtrade/Backtrader or domain engines.
7. Control plane — policies, approvals, checkpoints, observability, evaluation.
8. Runtime plane — Docker/VPS/cloud/queues/databases/caches.

## Architecture loop
`goal -> constraints -> decomposition -> data plane -> reasoning/tool plane -> control plane -> persistence -> evaluation -> deployment`.

## Decision questions
Is the workload batch/interactive/streaming/event-driven? What consistency is required? Which parts must be deterministic? What state must persist? Is the model doing interpretation or control? What changes continuously? Which side effects are reversible? What is the smallest trusted interface?

## Trading + AI reference
`market events -> normalized connector -> research/feature data -> RAG/context -> specialist agents -> debate -> risk gate -> execution engine -> venue -> reconciliation -> decision memory`.
Never let an LLM be the accounting system or matching engine; use deterministic services for financial state/risk enforcement.

## Web + RAG reference
`URL/event -> acquisition -> parsing/OCR -> structure reconstruction -> chunk/index -> hybrid retrieval -> agent reasoning -> citation validation -> answer`.

## Agent automation reference
`trigger -> orchestrator -> agent state -> tool discovery -> deterministic execution -> approval -> result -> checkpoint/event -> notification`.

## Memory policy
Separate session state, durable facts, event history, user/project memory and derived knowledge. Retain provenance and temporal precedence.

## Model choice
Use smaller models for extraction/routing, stronger reasoning models for synthesis, local models for privacy/air-gapped use, optimized serving for throughput and multimodal paths for complex documents.

## Production gates
Unit tests, integration tests, failure recovery, security, freshness, retrieval quality, agent behavior and end-to-end scenario tests.

## Anti-patterns
One giant agent, unbounded tools, unvalidated model-generated SQL, raw browser automation where an API exists, blindly vectorizing identifiers/numbers, LLM-controlled irreversible financial actions without gates, no provenance, no replay/checkpoint, or dependence on one vendor's changing capability set.


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

Use explicit subsystem contracts, decision records and dependency direction; optimize jointly for correctness, security, cost, latency and operability.


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
