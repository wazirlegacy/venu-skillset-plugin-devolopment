---
name: web-rag-ocr-document-intelligence
description: Build document and web ingestion systems using Firecrawl, RAGFlow/DeepDoc, Unlimited-OCR, OCR/VLM paths, and provenance-aware extraction for RAG and agents.
---
## Purpose
Build document and web ingestion systems using Firecrawl, RAGFlow/DeepDoc, Unlimited-OCR, OCR/VLM paths, and provenance-aware extraction for RAG and agents.

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

# Web, RAG, OCR and Document Intelligence

## Ingestion router
Select the parser based on input: web HTML -> web extractor; simple PDF -> text parser; scanned/complex PDF -> layout-aware parser; image -> OCR/VLM; spreadsheet -> structure-preserving parser; slides -> hierarchy/layout parser; audio/video -> transcription with timecodes.

## DeepDoc pattern
RAGFlow DeepDoc separates vision and parser concerns. Preserve page boxes/layout structures before normalized text when the document's visual structure carries meaning.

## Unlimited-OCR pattern
Baidu's current Unlimited-OCR project describes one-shot long-horizon parsing and current integrations with vLLM and ms-swift. Use it as a reference model and validate on your own corpus.

## Extraction quality
OCR is not ground truth. For high-consequence values, retain bounding boxes if available, validate formats/checksums, reconcile table totals and route uncertainty to a second parser/VLM or human review.

## Post-OCR processing
`extract -> layout reconstruction -> normalize -> remove safe boilerplate -> provenance -> semantic chunking -> indexing`.
Never chunk raw OCR indiscriminately.

## Firecrawl-style web ingestion
Acquire -> render/network handling -> parse -> structured extraction -> validate -> persist source metadata. Use explicit schemas for records and check missing fields.

## Provenance
Each chunk should carry document id/page/URL/section/extraction method and timestamps where available.

## Failure modes
Missing pages, OCR substitutions, column reordering, table drift, duplicated headers/footers, stale web content, dynamic content not captured, anti-bot failures and truncation of long documents.


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

Preserve page/region provenance through acquisition, OCR/layout parsing, indexing, retrieval, generation and citation validation.


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
