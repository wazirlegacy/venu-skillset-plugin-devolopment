---
name: brand-fidelity-strategy
description: Diagnose and improve customer-brand relationships using the M+ Brand Fidelity framework from the supplied Material report, while separating proprietary source claims from independent evidence. Use for brand strategy, CX/product experience diagnosis, customer loyalty, positioning, consumer insight, and intervention roadmaps.
metadata:
  version: "1.0"
  source_basis: "M+ Brand Fidelity 2026 Intelligent Growth Report"
  evidence_policy: "Source-derived proprietary framework; independently corroborate causal claims when stakes matter."
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

# Brand Fidelity Strategy

## Purpose

Use the supplied M+ Brand Fidelity framework as a structured diagnostic model for how a brand performs for customers both **in the moment** and **over time**.

Do not present the proprietary M+ framework as a universal scientific law. Preserve its six-attribute vocabulary when the user asks for an M+ analysis. For causal or quantitative claims, distinguish:
- **M+ source claim**: directly reported by Material;
- **independent evidence**: supported by outside research;
- **synthesis**: an analytical recommendation generated from the framework.

## The six attributes

Assess each independently:

1. **User-friendly** — Does the brand meet needs easily and reliably?
2. **Accessible** — Is the brand there when the customer needs it?
3. **Dependable** — Does it consistently provide a good experience?
4. **Personal** — Does it understand the customer's unique needs?
5. **Meaningful** — Does it play a significant role in the customer's life?
6. **Salient** — When the customer has a need in the category, is this the brand they turn to?

Use the source wording as the semantic anchor, but avoid long verbatim reproduction.

## Diagnostic workflow

### Step 1 — Define the category and customer job

Identify:
- category;
- target segment;
- primary need/job;
- relevant context and channel;
- important competitors/substitutes;
- time horizon.

Do not score a brand without defining the comparison context.

### Step 2 — Separate “moment” from “time”

Analyze two layers:

**In-the-moment**
- availability/access;
- friction;
- task completion;
- reliability;
- contextual responsiveness.

**Over-time**
- habit;
- trust;
- identity relevance;
- emotional significance;
- top-of-mind choice;
- accumulated relationship value.

A strong score in one layer does not automatically imply strength in the other.

### Step 3 — Score or qualitatively assess the six attributes

When numeric input is available:
- preserve the supplied scale;
- if using the M+ scale, individual attributes are 1–5;
- the source report states that the overall score is the unweighted aggregate of six ratings, rescaled to 0–100.

If using an adapted scale, label it **M+-inspired**, not an official M+ score.

### Step 4 — Find the limiting attributes

Look for:
- the lowest absolute scores;
- the largest competitive gaps;
- contradictions across attributes;
- moment-vs-time disconnects.

Do not simply optimize the lowest number. A low score may be strategically less important than a moderate score that blocks the customer journey or weakens another attribute.

### Step 5 — Link diagnosis to intervention

Map each gap to a controllable lever:

- User-friendly -> simplify flows, reduce friction, improve information architecture.
- Accessible -> improve availability, channel reach, support, discoverability.
- Dependable -> reliability, consistency, service recovery, operational quality.
- Personal -> personalization, preferences, context, identity-relevant experiences.
- Meaningful -> purpose, utility beyond transaction, emotional/cultural relevance.
- Salient -> distinctive positioning, memory structures, category cues, strong reason to choose.

Treat these as hypotheses to test, not guaranteed causal recipes.

### Step 6 — Create a high-fidelity growth roadmap

Use three phases inspired by the supplied report:

**Understanding**
- assess current state;
- combine customer/brand/CX evidence;
- map customer journeys;
- identify disconnects and opportunity areas.

**Co-Creation**
- ideate against prime gaps;
- prototype;
- test with customers;
- iterate and prioritize.

**Vision, Action + Impact**
- align people/process/technology;
- define investment pathways;
- sequence activation;
- define measurable business outcomes.

## Evidence discipline

The M+ report states that its study covered nearly 24,000 consumers and hundreds of global brands across 30 industries and reports business associations for high-fidelity brands.

When quoting its numerical claims (for example, 2x, 2.5x, or 3x relationships), call them **Material-reported findings** and do not imply independent replication. The supplied report describes a proprietary Economic Evaluation Model, not an open methodology sufficient for external reproduction.

Independent research supports the broader construct of attachment/relationship quality as a predictor of customer behavior. One longitudinal study of 2,284 US customers across durable-product categories found brand attachment to be a stronger long-term predictor of more difficult loyalty behaviors than satisfaction, with stated limits on generalizability. Use this as supporting context, not as validation of the M+ score.

## Industry pattern use

The report includes category-specific examples for retail, consumer technology, entertainment, and travel. Use them as case illustrations, not universal laws.

For a category diagnosis, ask:
- Which attributes are structurally strong?
- Which relational dimensions are underdelivered?
- Which cultural/macro shifts change the meaning of those attributes?
- Which customer behavior should change if the intervention succeeds?

## Output format

For strategic assessments, prefer:

1. Context and customer job
2. Six-attribute diagnostic
3. Moment vs over-time analysis
4. Evidence and confidence
5. Priority gaps
6. Intervention hypotheses
7. Test plan
8. Business metrics
9. Risks/assumptions

Avoid generic “improve customer experience” recommendations. Every recommendation must map back to an observable customer behavior or journey failure.

## Guardrails

- Never fabricate an official M+ score.
- Never imply an adapted score is Material's score.
- Never convert correlation or vendor-reported association into causation.
- Do not retain marketing CTAs from the source.
- When current market trends are material, verify them with current external research.


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

Use the six relational dimensions as a diagnostic framework, then validate interventions with behavioral/business experiments.


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
