---
name: devops-sre
description: Design reliable operations using CI/CD, SLOs, SLIs, error budgets, observability, incidents, capacity, backups and safe deployment.
---

# DevOps / SRE

## Purpose
Design reliable operations using CI/CD, SLOs, SLIs, error budgets, observability, incidents, capacity, backups and safe deployment.

## Evidence posture
Ground recommendations in current primary/official documentation where available. Distinguish documented behavior from inference, benchmark claims, and product marketing. Record version assumptions.

## Research synthesis
Define user-centric SLIs/SLOs and error budgets; instrument traces/metrics/logs; propagate context carefully; deploy progressively with rollback; rehearse backup/restore and incident response.

## Operating workflow
1. Define the problem, inputs, outputs, constraints, runtime/version, and threat or failure model.
2. Select architecture and mechanisms appropriate to the workload rather than blindly copying a framework pattern.
3. Establish contracts, invariants, state ownership, error handling, security boundaries, and observability.
4. Implement the smallest testable path, then add integration and failure-path behavior.
5. Measure correctness, performance, reliability, usability, and cost with representative data.
6. Harden for edge cases, partial failure, recovery, and version changes.
7. Document reproducible setup and verify the final artifact end-to-end.

## Quality gates
- Do not invent undocumented APIs or hidden model behavior.
- Preserve provenance for important external data.
- Test failure modes and rollback paths.
- Keep credentials, personal data, and irreversible actions behind explicit controls.
- Prefer deterministic control around probabilistic systems.

## Integration
Combine with the existing Venu AI/agent/RAG/gateway Skills when the task crosses domains. This skill describes methods and architecture; it does not imply that tools or permissions are currently available.


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

Define SLIs/SLOs/error budgets, instrument traces/metrics/logs, automate progressive delivery/rollback and correlate operational metrics with product outcomes.


## Research anchors — verified/current snapshot 2026-09-01

Primary sources to re-check when implementation decisions depend on changing behavior:
- Agent Skills specification: https://agentskills.io/specification
- MCP specification update (2026-07-28): https://blog.modelcontextprotocol.io/posts/2026-07-28/
- NIST AI RMF GenAI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Top 10:2025: https://owasp.org/Top10/
- OpenTelemetry signals/semantic conventions: https://opentelemetry.io/docs/concepts/signals/
- DORA 2025: https://dora.dev/research/2025/dora-report/
