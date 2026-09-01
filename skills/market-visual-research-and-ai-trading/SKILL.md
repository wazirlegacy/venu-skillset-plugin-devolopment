---
name: market-visual-research-and-ai-trading
description: Apply TradingView-style charting and alert concepts, BullGPT-style visual chart analysis workflows, and Latent Box-style curated research discovery. Use for chart interpretation, Pine Script strategy/alert design, technical-analysis research, visual trading-plan structuring, and curated AI/creative resource discovery. Do not claim hidden/proprietary model internals that sources do not disclose.
---
## Purpose
Apply TradingView-style charting and alert concepts, BullGPT-style visual chart analysis workflows, and Latent Box-style curated research discovery. Use for chart interpretation, Pine Script strategy/alert design, technical-analysis research, visual trading-plan structuring, and curated AI/creative resource discovery. Do not claim hidden/proprietary model internals that sources do not disclose.

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

# Market Visual Research and AI Trading

## Source-grounded operating model

### TradingView
Treat TradingView as a charting, scripting, strategy-simulation, and alerting environment.
Use:
- Pine Script indicators for calculations/visualization.
- Pine Script strategies for historical/realtime simulation and broker-emulator order modeling.
- Strategy Tester for simulated performance review.
- `alert()` for dynamic script events; `alertcondition()` for indicator alert conditions; strategy order-fill events for simulated fills.
- Webhooks as an external HTTP POST bridge from alerts.
- Explicitly account for realtime-only alert triggering and the fact that an alert stores a server-side mirror of the script/settings at creation time.
- Flag repainting, lookahead bias, synthetic/non-standard chart issues, intrabar assumptions, costs/slippage, and parameter changes.

### BullGPT
Treat BullGPT as a published product workflow, not as proof of a disclosed proprietary model.
Its public workflow:
1. User supplies a chart screenshot.
2. System analyzes chart structure and reported technical/contextual features.
3. Output is organized as a trade plan with entry, stop-loss, take-profit, key levels, and scenario probabilities.
4. Product publicly states support for support/resistance, Fibonacci, RSI, macro context, and adaptation to scalper/swing style after repeated analyses.
5. Never present the reported “7 seconds”, trader counts, profitability testimonials, or scenario probabilities as independently validated performance.
6. Never claim the exact hidden vision model, weights, prompt, feature extraction implementation, or proprietary scoring unless a primary source actually discloses it.

### Latent Box
Treat Latent Box as a curated discovery methodology rather than a search-engine replacement:
1. Identify the user's domain and intended outcome.
2. Search curated collections by category.
3. Prefer high-signal resources over exhaustive lists.
4. Record why each resource is relevant.
5. Distinguish official sources, open-source repositories, papers, products, and community resources.
6. Track freshness and licensing.
7. Preserve useful cross-disciplinary links across AI, art, design, web, dev, game, visualization, and related collections.

## Combined workflow

For a chart-analysis or trading-research task:
- Establish instrument, timeframe, market session, data provenance, and whether analysis is historical or realtime.
- Extract observable structure before forming a conclusion.
- Separate facts, technical-analysis heuristics, model outputs, and speculative interpretations.
- Build scenarios rather than pretending certainty.
- For automated execution, require a deterministic signal contract, risk limits, confirmation rules, and a separately tested execution layer.
- Backtest with realistic assumptions and inspect lookahead/repainting risks.
- For TradingView integration, prefer alert/webhook interfaces over assuming Pine Script can directly place live broker-panel orders.
- For visual chart analysis, request the screenshot or structured OHLCV/context when needed; do not infer invisible values from an image.

## Safety / quality gates

Never state that a pattern guarantees profit.
Never convert marketing testimonials into evidence.
Never use a probability as if it were a calibrated statistical forecast unless calibration/evaluation data are available.
For automated trading, include:
- position sizing
- stop/exit logic
- transaction costs
- slippage
- maximum exposure
- kill switch
- monitoring
- replay/backtest validation


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

Observation precedes interpretation; flag repainting/lookahead/simulated-fill risks and separate product claims from calibrated evidence.


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
