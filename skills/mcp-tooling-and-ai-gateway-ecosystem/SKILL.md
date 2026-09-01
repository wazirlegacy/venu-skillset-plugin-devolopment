---
name: mcp-tooling-and-ai-gateway-ecosystem
description: Design interoperable tool ecosystems using MCP, A2A, public APIs, n8n/Dify/Langflow tool surfaces, Hermes, OmniRoute, and curated MCP/server catalogs.
---
## Purpose
Design interoperable tool ecosystems using MCP, A2A, public APIs, n8n/Dify/Langflow tool surfaces, Hermes, OmniRoute, and curated MCP/server catalogs.

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

# MCP, Tooling and AI Gateway Ecosystem

## MCP mental model
MCP clients discover and call tools/resources/prompts exposed by servers. The critical contract is accurate capability metadata, not just transport.

Every tool should define stable name, exact description, typed inputs/outputs, side effects, permissions, authentication and failure semantics.

## Transport
Use local stdio or remote HTTP/streaming transports as appropriate. Keep the trust boundary explicit.

## Catalogs
`awesome-mcp-servers` and similar lists are discovery indexes, not security guarantees. Verify repository origin, maintainer activity, license, scopes, secret/filesystem/network access and side effects before enabling a server.

## Public APIs
Use `public-apis` as a discovery map. Verify current endpoint docs, auth, limits, data license, uptime, commercial terms and privacy before integration.

## AI gateway pattern
`client -> auth/policy -> routing -> provider adapter -> inference -> telemetry`.
Useful controls include model routing, fallbacks, rate limits, caching, cost budgets, health checks, audit logs and protocol translation.

## OmniRoute
The name currently refers to multiple public projects. Do not assume a single canonical implementation. Some current OmniRoute repositories describe OpenAI-compatible multi-provider gateways with routing/fallbacks plus MCP/A2A and optional memory/skills/eval surfaces. Exact-repository selection is mandatory before using project-specific behavior.

## Hermes interoperability
Hermes provides a reference for Skills + MCP composition, external server catalogs, per-server filtering, and exposing Hermes capabilities via MCP to other agents.

## A2A vs MCP
Use MCP for fine-grained tool/resource interaction. Use A2A when the remote entity is an independent agent/service with its own capabilities and task lifecycle.

## Security
Least privilege, allowlists, input/output validation, sandboxing, quotas, human approval for sensitive effects and immutable audit logs. Never give a model unrestricted shell/filesystem/trading authority by default.

## Tool-selection evaluation
Test near-neighbor tools, ambiguous descriptions, missing permissions and malformed outputs. Correct tool implementation does not guarantee correct tool selection.


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

Keep MCP tools narrow, scoped and auditable; separate discovery from execution and follow current transport/auth semantics.


## Research anchors — verified/current snapshot 2026-09-01

Primary sources to re-check when implementation decisions depend on changing behavior:
- Agent Skills specification: https://agentskills.io/specification
- MCP specification update (2026-07-28): https://blog.modelcontextprotocol.io/posts/2026-07-28/
- NIST AI RMF GenAI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Top 10:2025: https://owasp.org/Top10/
- OpenTelemetry signals/semantic conventions: https://opentelemetry.io/docs/concepts/signals/
- DORA 2025: https://dora.dev/research/2025/dora-report/


## Unified execution workflow
1. Frame the task, inputs, outputs, constraints, environment, versions, success criteria, trust boundaries, and irreversible side effects.
2. Choose the simplest architecture and implementation mechanism that satisfies the stated requirements; identify dependencies and assumptions.
3. Define contracts, invariants, state ownership, security boundaries, failure classes, and observability before consequential execution.
4. Implement a smallest testable path, then add integration, adversarial, recovery, and performance coverage appropriate to the risk.
5. Verify outputs and postconditions against authoritative state; do not treat process completion, model confidence, or HTTP success as proof of correctness.
6. Record versions, source/provenance, measurements, failures, and unresolved risks; preserve a regression case for every material defect.
7. Re-check changing external dependencies at execution time and provide rollback/migration guidance for production changes.

## Integration

Combine this Skill with other Venu Skills when a task crosses domains. Use the minimum sufficient Skill set, explicit precedence, shared contracts, and the Skill router/composer; do not silently blend incompatible assumptions.
