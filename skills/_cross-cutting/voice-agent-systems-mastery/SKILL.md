---
name: voice-agent-systems-mastery
description: High-assurance real-time voice-agent architecture, conversational UX, orchestration, telephony, multilingual behavior, deployment, resilience, observability, compliance, evaluation, and continuous improvement.
---

# Voice Agent Systems Mastery

Use this Skill when designing, reviewing, debugging, evaluating, or operating real-time voice agents.

## Core model
Treat a voice agent as a distributed, event-driven real-time system, not a text chatbot with audio attached.

Canonical loop:

`Listen -> Understand -> Reason -> Respond -> Speak -> Listen`

The stages overlap. Partial speech, end-of-turn signals, reasoning, synthesis, playback, interruption, and cancellation are concurrent events.

## Architecture
Separate:
- Core conversational layer: audio transport, streaming STT/CSR, reasoning/LLM, TTS, orchestration/runtime.
- Operational layer: memory/context, integrations/tools, observability/telemetry, compliance/security, scaling, deployment, governance.

Keep orchestration as the source of truth for session state. Do not duplicate turn detection or state machines across independent layers unless explicitly synchronized.

## Conversational control
- Treat timing, turn-taking, interruption, and cancellation as first-class control signals.
- Barge-in must cancel playback immediately and return control to listening.
- Speculative reasoning is allowed only when safely cancellable; discard stale drafts when user intent changes.
- Use concise acknowledgments when downstream work creates silence.
- Never let predictive preparation become an irreversible action before the turn is confirmed.

## Reliability
Design for graceful degradation:
- low-confidence recognition -> clarify rather than act on uncertain input;
- reasoning/retrieval failure -> acknowledge, retry within policy, or escalate;
- synthesis failure -> safe fallback voice/audio or text/channel fallback;
- connection failure -> bounded reconnect with exponential backoff and session-state restoration;
- recovery failure -> human handoff where appropriate;
- deployments -> gradual rollout, connection draining, and clean completion of active sessions.

## Multilingual behavior
Language detection is a probabilistic routing signal, not a destructive hard gate. Preserve context and persona across language switches. Localize persona, politeness, acknowledgments, clarification, error handling, and knowledge grounding; translation alone is insufficient. Unsupported languages must fail gracefully.

## Telephony and multimodal
Keep call transfer, termination, DTMF, media-stream closure, and human handoff explicit. Preserve context on handoff. Separate AI-assist and AI-speaking channels and require authorization before AI speech enters a human-controlled channel.

## Evaluation
Use both quantitative and qualitative evaluation. Prefer distributions over single pass/fail examples because speech, LLM reasoning, and orchestration are probabilistic.

Measure at minimum:
- end-of-turn to first-audio latency;
- interruption/barge-in success;
- missed-response/stall rate;
- clipped-response rate;
- recognition confidence/error distribution;
- task success and intent alignment;
- abandonment during silence;
- tail latency under load.

Use replay, probabilistic regression, load/stress tests, fault injection, turn-level diagnostics, and representative-call regression suites.

## Safety and governance
Apply the universal LLM/MCP guardrail contract. Voice output is an irreversible user-facing side effect: validate sensitive/high-impact content before speech. Use layered input moderation, reasoning controls, output filtering, authentication/consent, regional routing, secure transport, minimization/redaction, restricted audit access, and immutable/versioned audit records where required.

## Continuous improvement
Start with a constrained workflow, instrument it, gather human/user feedback, review transferred interactions, tune prompts/turn handling/domain vocabulary, validate against regression suites, then expand scope deliberately.

Do not treat vendor-specific claims as universal facts. Preserve provenance and re-verify volatile product behavior.
