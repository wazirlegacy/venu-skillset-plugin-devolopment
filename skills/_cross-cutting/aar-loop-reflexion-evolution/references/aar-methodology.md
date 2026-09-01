# AAR Loop, Reflexion & Evidence-Driven Evolution — Research Reference

Research snapshot: 2026-09-01

## 1. After Action Review

The U.S. Army's AAR method emphasizes reviewing the standard/intent, establishing what happened from factual and chronological evidence, analyzing why outcomes differed, and identifying lessons/recommendations. Current Army training material says AARs should be conducted immediately after learning events, remain nonjudgmental, and use supporting longitudinal data when changes to training are made.

Primary/current Army references:
- https://adminpubs.tradoc.army.mil/pamphlets/TP350-70-14.pdf
- https://api.army.mil/e2/c/downloads/2025/07/25/5ffd4949/no-25-761-home-station-training-handbook-jul-25.pdf

Historical doctrinal reference used to understand the four-question format:
- TC 25-20, A Leader's Guide to After Action Reviews, 1993.

Design implication for AI agents: separate the debrief from blame, establish the intended standard, reconstruct observed events, analyze causal gaps, and carry concrete lessons into subsequent work. Do not mistake a facilitator's narrative for evidence.

## 2. Reflexion

Shinn et al. (2023) introduced Reflexion, which uses verbal feedback and an episodic memory buffer rather than weight updates to improve subsequent attempts. The core pattern is: attempt -> feedback -> verbal reflection -> store reflection -> next attempt.

Source:
- https://arxiv.org/abs/2303.11366

Engineering implication: useful feedback can improve later decisions without retraining model weights, but the feedback signal and memory quality determine whether the loop helps.

## 3. Self-Refine

Self-Refine uses iterative self-feedback and refinement and reported substantial gains across multiple tasks in its original experiments.

Source:
- https://arxiv.org/abs/2303.17651

Engineering implication: iterative refinement is a useful technique, but should be measured rather than assumed to help.

## 4. Limits of intrinsic self-reflection

Evidence is mixed. Li, Yang, and Ettinger (2024) found self-reflection can help on some tasks but hurt on others, depending on initial accuracy and task difficulty.

Source:
- https://arxiv.org/abs/2404.09129

A 2026 study, "Reflection or Re-Generation? Why LLM Revision Fails Where Human Revision Succeeds," reports cases where LLM revision provides near-zero information gain on objective tasks and negative information gain on some subjective tasks, arguing that self-conditioned revision can resemble regeneration without external information.

Source:
- https://arxiv.org/abs/2607.28908

Engineering implication: Venu must never treat self-reflection text as proof. Preserve the original result, require evidence, and evaluate whether reflection actually improved the measured outcome.

## 5. Positive and managed reflection

Research also indicates that reflection can be weaker when an agent initially succeeds or when models are smaller, and that retaining useful positive experiences alongside failures can improve the reflection context in some environments.

Source:
- https://openreview.net/pdf?id=YwqlQubiiv

Engineering implication: AAR should record both sustainments and corrective lessons, while controlling memory growth and scope.

## 6. Evaluation and observability

Modern agent evaluation guidance emphasizes measuring agents over realistic multi-turn/tool-use behavior rather than relying only on static outputs. OpenAI's Agents SDK provides traces for LLM generations, tool calls, handoffs, guardrails and custom events; Anthropic's 2026 evaluation guidance emphasizes that agent evaluations should make behavioral changes visible before production and should combine evaluation strategies suited to complex agent behavior.

Sources:
- https://github.com/openai/openai-agents-python/blob/main/docs/tracing.md
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Engineering implication: an AAR should consume traces, tool outputs, artifacts, test results, and authoritative state whenever those are available.

## 7. Guardrails and authorization

OpenAI's current agent guidance recommends layered guardrails, deterministic protections, output validation, risk-based pauses, and human intervention for high-risk actions. Tool guardrails can validate calls before and after execution, and tripwires can halt execution on a violation.

Sources:
- https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- https://github.com/openai/openai-agents-python/blob/main/docs/guardrails.md

Engineering implication: reflection must never bypass authorization. AAR can propose a control change, but policy layers remain the authorization boundary.

## 8. Venu synthesis

The Venu AAR implementation therefore uses:

attempt -> observable trace -> four-question AAR -> evidence reconciliation -> root cause -> concrete lesson -> regression test -> candidate improvement -> independent evaluation -> approval -> durable versioned memory.

The synthesis intentionally rejects the assumption that reflection equals learning. The test is behavioral improvement on subsequent attempts.
