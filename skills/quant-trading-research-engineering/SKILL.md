---
name: quant-trading-research-engineering
description: Design, backtest, validate, and compare quantitative trading systems using event-driven engines, realistic execution assumptions, statistical research hygiene, and research-to-live parity.
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

# Quant Trading Research Engineering

## Purpose
Use this skill when designing or reviewing algorithmic trading research, backtesting, execution simulation, strategy architecture, or research-to-production workflows.

## Core operating model
Treat a trading system as a pipeline, not a strategy function:
`data acquisition -> normalization -> feature/indicator computation -> signal generation -> portfolio/risk decision -> order construction -> execution simulation -> accounting -> analytics -> validation -> deployment`.
Separate these concerns so a convenient backtest shortcut never becomes an unstated live assumption.

## Backtrader pattern
Use a Cerebro-style orchestration model for composable data feeds, strategies, observers, analyzers, writers, broker simulation, commissions, slippage, and optimization. Strategies follow a lifecycle and react to engine time progression. Brokers model cash, positions and order execution. Keep analyzers on the same execution history used to produce returns.

Use built-in run/vectorization modes when they preserve intended semantics. Model realistic commissions and slippage. Multi-data and pair strategies must preserve timestamp alignment.

## NautilusTrader pattern
Prefer a deterministic, event-driven core when research must match live behavior. Model a common kernel with typed domain objects, MessageBus, Cache, Portfolio, execution algorithms and modular venue adapters. Keep strategy lifecycle and execution semantics common between backtest and live. For the event loop, process market state first, dispatch strategy callbacks, then settle queued venue commands according to the documented timestamp ordering.

Treat adapters as anti-corruption layers: raw venue protocol -> normalized events/commands -> internal model. Preserve venue-specific order types, time-in-force, precision, margin/funding and reconciliation semantics.

## Freqtrade pattern
Treat strategy feature construction and decision callbacks as different cost/causality surfaces. Explicitly test for look-ahead bias and recursive indicator issues. Hyperparameter search is a statistical experiment: define an explicit loss objective, limit the search space, record the search budget, and verify holdout/walk-forward performance.

## Research hygiene
Every backtest must declare dataset/source, timestamp convention, market universe, survivorship policy, corporate actions, fees, spread/slippage, latency/fill assumptions, leverage/funding/borrow, signal delay, train/validation/test or walk-forward scheme, parameter-search budget, and diagnostics.

## Validation hierarchy
1. Unit-test features/signals.
2. Test synthetic edge cases.
3. Prove no future information enters the feature/signal path.
4. Validate execution, fee and slippage semantics.
5. Use in-sample + holdout or rolling/walk-forward validation.
6. Stress different regimes and liquidity.
7. Compare against realistic baselines.
8. Run paper/dry-run.
9. Only then consider live execution with explicit limits and reconciliation.

## Metrics
Report return, volatility, Sharpe/Sortino with stated conventions, max drawdown and duration, turnover, exposure, concentration, expectancy, profit factor, tail loss and parameter stability. Distinguish economic edge from leverage, turnover, sample-selection, data-snooping and cost artifacts.

## Strategy procedure
Define market/horizon/venue/objective -> define observable information at decision time -> define features and timestamps -> separate entry/exit/position sizing/risk -> build minimal baseline -> add one hypothesis at a time -> measure incremental value -> robustness test -> document negative evidence.

## Anti-patterns
Never assume a profitable backtest implies live profitability; zero slippage is acceptable; close-price execution is available at the same close used to calculate a signal; broad hyperparameter search increases truth; one market regime generalizes; or model confidence is calibrated by appearance.


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

Make data timestamps, fills, fees, slippage, latency and position accounting explicit; forbid look-ahead/survivorship leakage and validate out-of-sample.


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
