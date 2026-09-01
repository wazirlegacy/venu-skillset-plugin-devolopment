---
name: omniroute-gateway-and-adaptive-routing
description: Design, analyze, implement, debug, and evaluate OmniRoute-style AI gateways, including provider abstraction, OpenAI/Anthropic/Gemini translation, auto-combo routing, quota and health awareness, adaptive quality feedback, resilience, caching, compression, MCP/A2A, Skills, observability, and secure self-hosting. Use when a task involves multi-provider LLM gateways, intelligent model routing, failover, routing policies, provider health, quality-aware selection, MCP gateway design, or reproducing/modernizing OmniRoute architectural patterns.
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

# OmniRoute Gateway & Adaptive Routing

## Purpose

Use this skill as an engineering playbook derived from the public OmniRoute repository and its technical documentation. It captures architectural patterns and decision procedures rather than copying source code.

Treat repository-specific numbers, benchmarks, provider lists, and feature claims as versioned observations. Verify the current upstream implementation before relying on them for production work.

## Core mental model

Model the system as two planes:

1. **Data plane / request hot path**: authenticate, validate, resolve route, translate request, execute upstream, stream/return response, record minimal in-memory outcome metadata.
2. **Control / intelligence plane**: quality evaluation, historical analysis, telemetry export, routing analysis, dashboards, experiments, offline optimization.

Keep blocking I/O, expensive evaluation, and non-essential persistence out of the hot path.

## Canonical request pipeline

Use this sequence unless the target architecture explicitly differs:

```text
Client request
  -> authenticate + validate
  -> resolve model/combo
  -> select provider/account/model
  -> translate source format to target format if required
  -> execute through provider executor
  -> retry/backoff + circuit-breaker handling
  -> stream/normalize response
  -> classify outcome
  -> emit bounded routing event
  -> asynchronous persistence/telemetry/evaluation
```

The source architecture describes five conceptual stages: ROUTE, TRANSLATE, EXECUTE, STREAM, RECORD.

## Provider abstraction

Prefer a registry-driven architecture:

- normalized provider identity
- provider-specific base URL/auth metadata
- reusable default executor for compatible providers
- specialized executor only when behavior truly differs
- isolated request/response translators for protocol differences
- explicit account/session identity when multiple credentials exist

Do not create one bespoke execution stack per provider when configuration plus a shared executor is sufficient.

## Translation layer

Treat provider translation as a separate boundary. Support at minimum:

- OpenAI-style messages -> Anthropic-style request
- OpenAI-style messages -> Gemini-style request
- OpenAI Chat Completions -> Responses-style request
- system/developer role normalization
- tool schema conversion
- reasoning/thinking parameter mapping
- structured-output/schema conversion

Always define what is preserved, transformed, dropped, or approximated.

## Routing hierarchy

Distinguish these concepts:

- **candidate discovery**: which provider/model/account targets exist?
- **hard eligibility**: is a candidate allowed to execute?
- **soft scoring**: among eligible candidates, which is preferable?
- **execution strategy**: how are retries/fallbacks attempted?
- **post-outcome feedback**: what was learned from the attempt?

Hard exclusion must remain independent from soft quality preference. Typical hard exclusions include circuit breaker OPEN, exhausted quota, failed authentication, and explicit model lockout.

## Auto-routing / Auto-Combo

When designing an auto-routing mode, use a layered process:

### 1. Parse route intent

Examples:

- balanced
- coding
- reasoning
- vision
- multimodal
- fast
- cheap
- reliable
- offline/free-tier focused

Support category/tier composition when useful, such as `auto/coding:fast`.

### 2. Build candidate pool

Start from active provider connections, valid credentials, supported model capabilities, account/session availability, and policy filters.

Prefer a virtual/in-memory candidate set for per-request auto-routing when persistence is unnecessary.

### 3. Apply hard filters

Filter by:

- credential validity
- circuit-breaker state
- quota/rate-limit availability
- model lockout
- requested modality/capabilities
- policy restrictions
- session/account availability

Use fail-open only where the product's design explicitly requires routing continuity and the fallback is safe.

### 4. Score eligible candidates

A production-quality scorer can combine:

- quota headroom
- health
- inverse blended cost
- inverse latency
- task fit
- stability/error rate
- account tier
- tier affinity
- request specificity/context affinity
- session availability
- connection density / anti-concentration
- cache affinity
- reset-window affinity
- observed semantic/operational quality

Normalize configurable weights before combining scores.

A simple general form is:

```text
score(candidate) = sum_i w_i * factor_i(candidate)
```

with normalized weights `sum(w_i) = 1`.

### 5. Add exploration carefully

For discovery modes, reserve a small exploration probability/bias so unknown models can collect observations. Do not allow cold-start optimism to overwhelm established evidence.

## Adaptive quality feedback

Separate **operational quality** from **semantic quality**.

Operational quality may include:

- transport/HTTP failures
- malformed responses
- 429/rate limits
- stream interruption
- zero-output anomalies
- finish-by-length anomalies
- latency/TTFT behavior

Semantic quality should come from an evaluator/judge and must not be inferred merely from HTTP success.

Use sample-aware smoothing. A useful pattern from the source design is an EWMA plus confidence warm-up:

```text
confidence = clamp(samples / warmup_samples, 0, 1)
smoothed = neutral + confidence * (observed - neutral)
```

This prevents a handful of lucky calls from dominating provider choice.

Keep semantic evaluation off the request hot path. Feed results back asynchronously through a typed outcome/evaluation channel.

## Routing events

Define a compact typed event such as:

```text
requestId
provider
model
strategy
latency
TTFT / timing metadata
input/output tokens
cost
retry count
fallback used
outcome/status
finish reason
timestamp
```

Rules:

- no prompts, secrets, or full bodies in routing events
- bounded in-memory storage for recent explainability
- sink interface for pluggable consumers
- O(1) or near-O(1) recording on the hot path
- telemetry export asynchronously
- dropping telemetry under overload must not backpressure inference

## Resilience

Use independent layers:

```text
Timeouts
  -> retry with bounded exponential backoff
  -> circuit breaker
  -> connection cooldown / rate-limit state
  -> alternate account/provider/model
  -> emergency fallback
```

Do not conflate retryable transport failures with semantic model quality.

Circuit state should normally include a recovery/probe state such as HALF_OPEN rather than a binary open/closed model.

## Quota-aware routing

Track quota at the correct scope:

- API key / account
- provider
- model where applicable
- reset time
- current consumption
- estimated headroom

Treat quota exhaustion as a hard eligibility condition; treat remaining headroom as a soft score factor.

## Caching

Separate cache responsibilities:

- exact/signature cache for deterministic request identity
- semantic cache for approximate reuse
- prompt-cache affinity where the upstream provider benefits from reuse
- idempotency records for safe retries/replays

Never treat a cache hit as proof that two requests are semantically interchangeable without a defined equivalence policy.

## Observability

Track at minimum:

- latency p50/p95/p99
- TTFT and stream timing where applicable
- throughput
- retry/fallback counts
- rate limits
- provider/model success/failure
- token usage
- cost
- routing decisions
- quality observations
- circuit state

Provide an explainability path so an operator can answer: **why did this request use this provider/model?**

## MCP and tool gateway

When exposing the gateway through MCP:

- define tools with explicit input schemas
- attach least-privilege scopes
- separate read, write, execute, and management capabilities
- support stdio for local IDEs and an HTTP transport for remote/multi-session scenarios when required
- authenticate remote access explicitly
- keep sensitive content out of telemetry and diagnostic responses

Typical gateway MCP surfaces can include routing, health, quota, model catalog, cost, memory, skills, web retrieval, compression, and provider operations.

## Skills architecture

Distinguish two layers when emulating OmniRoute:

1. **Runtime skills/tools**: executable capabilities exposed to the model and dispatched by tool-call interception.
2. **Agent Skills catalog**: `SKILL.md`-style instructional assets discoverable by external agents.

For executable skills, use versioned identities and explicit modes such as `on`, `off`, and `auto`. Automatic injection should use relevance scoring and a hard upper bound on how many skills are injected per request.

If execution requires arbitrary code, isolate it in a sandbox with:

- dropped Linux capabilities
- resource limits
- network disabled by default
- read-only filesystem where possible
- bounded process count
- bounded output
- hard timeout
- allowlisted container images

## Compression / context economy

Treat compression as an independent subsystem, not a prompt hack.

Possible layers:

- recurring-noise removal from model context
- tool-description compression
- accessibility-tree result compression
- bounded context storage/reference handles
- cache-aware compression

Compression must preserve the semantics and anchors required for downstream tools. Never claim token savings without measuring actual payloads.

## Security boundaries

Enforce:

- secret redaction
- per-principal workspace isolation
- path traversal rejection
- private-network blocking for outbound fetches where SSRF is a risk
- redirect control
- authorization scopes
- bounded payload sizes
- rate limits
- audit trails

Never allow a convenience feature to silently bypass provider auth, filesystem boundaries, or remote-MCP authorization.

## Evaluation procedure

When asked to reproduce, extend, or modernize an OmniRoute feature:

1. Identify the exact upstream feature and version.
2. Read the relevant architecture/design document.
3. Inspect the narrowest source paths needed to validate behavior.
4. Separate documented design from inferred implementation.
5. Identify existing components to reuse before creating duplicates.
6. Define invariants and failure modes.
7. Build unit/integration tests around the invariant.
8. Benchmark only after correctness is established.
9. Record compatibility differences.
10. Re-check the current upstream repository because OmniRoute evolves quickly.

## Source and attribution discipline

This skill is based on public technical material. Do not copy large source files into outputs. Describe algorithms, interfaces, workflows, architecture, and design patterns in original engineering language; reference exact upstream files when the user needs implementation tracing.

## Output format for architecture requests

When designing a gateway or router, produce:

1. requirements and constraints
2. architecture diagram/text flow
3. data-plane vs control-plane boundary
4. provider/executor/translator design
5. candidate eligibility rules
6. scoring model
7. failure/recovery logic
8. state and persistence model
9. observability and explainability
10. MCP/tool/security boundary
11. deployment topology
12. test/evaluation plan
13. known deviations from OmniRoute


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

Separate hot-path routing from control feedback; keep hard eligibility distinct from soft quality scoring and make provider translation/telemetry observable.


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
