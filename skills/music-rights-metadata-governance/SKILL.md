---
name: music-rights-metadata-governance
description: Validate, reconcile, and govern music composition and sound-recording metadata for distribution, rights management, royalty matching, and catalog scalability. Use ISRC/ISWC/IPI concepts, ownership splits, identifier integrity, maturity assessment, and audit-ready workflows. This is operational guidance, not legal advice.
metadata:
  version: "1.0"
  source_basis: "The Invisible Infrastructure of the Music Industry + IFPI/CISAC/DDEX verification"
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

# Music Rights & Metadata Governance

## Purpose

Treat music metadata as an operational and financial-control layer connecting:
- compositions;
- sound recordings;
- contributors;
- rights holders;
- territories;
- usage;
- royalties;
- distribution systems.

The supplied source emphasizes that metadata failures often appear as delayed, misallocated, disputed, or unmatched revenue rather than obvious software failures.

## First principle: separate the right layers

### Composition / musical work

Model the underlying work separately from a particular recording.

Typical source fields:
- work title;
- ISWC;
- songwriters/contributors;
- IPI/CAE identifiers;
- publisher(s);
- ownership splits;
- registrations with relevant rights organizations.

The source connects this layer to publishing revenue streams such as performance, mechanical, and synchronization uses.

### Sound recording / master

Model the specific recorded performance separately.

Typical source fields:
- ISRC;
- main artist;
- featured artists;
- performer roles;
- producer credits;
- label/distributor;
- UPC/product identifier;
- release date;
- territory data;
- version information.

The source emphasizes that recording metadata determines how a recording is identified, distributed, credited, and monetized across systems.

## Identifier discipline

Use these conceptual rules:

- **ISRC** identifies a particular sound recording or music video; it does not identify the underlying composition or a product.
- **ISWC** identifies a musical work.
- **IPI/CAE** identifies a rights-holder/creator-party identity in the relevant rights ecosystem.

Verify current implementation rules with the authoritative standards before assigning or changing identifiers.

IFPI states that an existing ISRC should be retained for the same recording and should not be reassigned merely because distribution crosses formats or countries. CISAC describes ISWC as a globally unique identifier for musical works. DDEX provides machine-readable standards for musical-work and recording-rights communication.

## End-to-end validation workflow

### 1. Ingest

Collect source metadata from the authoritative upstream systems.

Record:
- source;
- timestamp;
- territory;
- version;
- confidence;
- change reason.

### 2. Normalize

Normalize:
- names;
- titles;
- whitespace/punctuation where appropriate;
- dates;
- territory codes;
- identifier syntax.

Do not “normalize” away distinctions that have legal or business meaning.

### 3. Resolve entities

Match:
- recording -> ISRC;
- recording -> composition/work;
- contributor -> IPI/CAE;
- work -> publisher/rightsholder;
- product/release -> its components.

Use exact identifiers first. When identifiers are missing, use controlled fuzzy matching and assign confidence rather than silently merging records.

### 4. Validate ownership

For each work/right layer:
- ensure all required parties exist;
- check that shares are defined;
- check total allocation;
- detect conflicting claims;
- distinguish unknown from zero;
- retain effective dates/territories.

The supplied source stresses that undefined/disputed splits can stop automated allocation. For systems that require 100% ownership allocation, reject or hold records that do not reconcile to the required total.

### 5. Cross-system reconciliation

Compare publishing/master/catalog/distributor/DSP-facing records.

Flag:
- same recording with conflicting identifiers;
- recording with no work relationship when one is expected;
- duplicate works;
- duplicate recordings;
- contributor mismatches;
- ownership conflicts;
- territory conflicts;
- stale versions;
- missing required metadata.

### 6. Release gate

Before distribution:
- validate identifiers;
- validate contributors;
- validate ownership/splits;
- validate release/territory data;
- validate recording-to-work mapping;
- persist an auditable snapshot.

### 7. Continuous integrity monitoring

After release:
- detect upstream changes;
- monitor failed matches;
- reconcile incoming usage reports;
- reprocess changes idempotently;
- preserve correction history;
- escalate unresolved conflicts.

## Maturity model

Use the source's four-level model diagnostically:

**Level 1 — Reactive**
- fix issues after they occur;
- dispersed data;
- little/no validation;
- high matching and suspension risk.

**Level 2 — Operational**
- pre-release steps;
- basic identifier tracking;
- partial centralization;
- manual reconciliation.

**Level 3 — Structured**
- centralized catalog;
- standardized split workflow;
- validation checkpoints;
- fewer post-release corrections.

**Level 4 — Data-Driven Scalability**
- publishing + master integration;
- automated validation;
- continuous integrity monitoring;
- audit/version control;
- cross-territory synchronization.

When scoring maturity, report both the level and the evidence that supports it.

## Conflict-resolution policy

Never silently choose a rights holder when authoritative data conflicts.

Use:
1. preserve all conflicting claims;
2. identify source authority and effective date;
3. classify the conflict;
4. request/locate authoritative evidence;
5. prevent irreversible downstream allocation until resolved where required;
6. log the resolution.

## Output

For catalog audits, return:
- identity coverage;
- missing/invalid fields;
- identifier conflicts;
- work/recording linkage failures;
- split validation results;
- territory/version issues;
- severity;
- recommended remediation;
- maturity level;
- audit trail requirements.

## Guardrails

- This is data/operations guidance, not legal advice.
- Do not invent rights ownership.
- Do not infer legal entitlement from metadata alone.
- Verify current standards and territory-specific rules before implementing.
- Ignore promotional CTAs from the source.


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

Keep work and recording identity distinct; validate identifiers, splits, territories and dates independently and maintain audit history.


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
