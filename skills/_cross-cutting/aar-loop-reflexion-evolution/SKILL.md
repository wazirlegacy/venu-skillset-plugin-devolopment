---
name: aar-loop-reflexion-evolution
 description: Run evidence-grounded After Action Reviews over completed agent tasks or sessions, distinguish expected from actual behavior, identify causal gaps, extract concrete checkable lessons, and convert validated lessons into approved skill/rule/regression improvements. Use after meaningful tasks, failures, surprises, recoveries, releases, or at explicit user request for an AAR, review, learning, or fix.
metadata:
  version: "2.0"
  maturity: "10-of-10-target"
  research_snapshot: "2026-09-01"
  inherits: "aar-loop concepts + Reflexion/self-refinement research + Venu evaluation/evolution + Venu guardrails"
---

# AAR Loop, Reflexion & Evidence-Driven Evolution

## Purpose

Convert completed agent work into durable, checkable improvement without pretending that self-reflection is automatically correct. The Skill combines the four-question After Action Review method with evidence capture, causal analysis, controlled memory, regression testing, and approval-gated Skill evolution.

## Core doctrine

The model may reflect and propose. Evidence, deterministic checks, and authorization decide what becomes durable.

Never treat a model's self-critique as ground truth. Reflection is a hypothesis about why something happened unless supported by execution traces, tool results, tests, authoritative state, user correction, or other independent evidence.

Never silently rewrite a released Skill, policy, rule, memory store, or production configuration because of an AAR.

## When to run

Run an AAR when:

- the user explicitly requests an AAR, review, lesson, or learning pass;
- a task fails, partially fails, surprises the agent, or requires a workaround;
- an external system reports success but verification disagrees;
- a tool call is rejected, times out, or causes an unexpected side effect;
- a release, deployment, migration, or consequential decision completes;
- a repeated mistake appears;
- a successful pattern is important enough to preserve;
- an evaluation case finishes and the result is informative.

A clean run may still yield a positive sustainment lesson. Do not manufacture a failure or a lesson just to fill the template.

## AAR modes

### Micro AAR
Use for low-risk, short tasks. Capture the four questions plus zero to three lessons.

### Standard AAR
Use for normal engineering, research, business, design, or operational work. Include evidence, root cause, lesson quality, and improvement disposition.

### Incident AAR
Use for failures, security events, data loss, unexpected side effects, or material operational deviations. Preserve chronology, evidence, containment, root cause, contributing factors, and corrective actions. Do not destroy or rewrite incident evidence.

### Release AAR
Use after deploys, migrations, launches, or production changes. Verify the real resulting state rather than trusting command exit codes, dashboards, or agent claims alone.

### Evolution AAR
Use when the goal is to improve a Skill, rule, workflow, evaluation, or memory policy. Requires regression coverage and explicit promotion rules.

## The four questions

Ask and answer in order:

1. What was supposed to happen?
2. What actually happened?
3. Why was there a difference?
4. What should we sustain, change, or test next time?

For question 1, establish the intended objective, constraints, acceptance criteria, and relevant standard.

For question 2, describe observable events chronologically. Include partial completion, silent failures, retries, tool behavior, and workarounds.

For question 3, distinguish observed mechanism from hypothesis. Prefer causal evidence over statements about care, intent, or personality.

For question 4, produce specific changes that another agent could execute without guessing.

## Evidence hierarchy

Prefer, in order where available:

1. Deterministic test or authoritative external state.
2. Tool output, execution trace, artifact diff, or system log.
3. Independent evaluator or second-agent assessment.
4. User correction or explicit acceptance criteria.
5. Model self-report or self-reflection.
6. Unverified inference.

When evidence conflicts, preserve the conflict and state what remains unresolved.

## Lesson quality gate

A lesson must be concrete, testable, and transferable.

Good:

- "After a deployment, verify the running version of every touched service against the build identifier; do not treat the deployment command's exit code as proof of service state."
- "When an API accepts partial batches, verify the persisted item count and retry only the missing records with bounded exponential backoff."

Reject or rewrite vague lessons such as:

- "Be more careful."
- "Improve the code."
- "Check things better."
- "Communicate clearly."

A durable lesson should normally name a condition, object/tool, observable signal, and action or decision rule.

## Positive and negative learning

Capture both failure-prevention lessons and successful patterns.

Positive lesson requirements:

- identify what worked;
- explain why it likely worked using evidence;
- identify the context where it is valid;
- avoid over-generalizing from one success.

Negative lesson requirements:

- identify the failure or gap;
- identify mechanism and contributing factors;
- state the prevention or recovery rule;
- create a regression test when recurrence is plausible.

## Root-cause analysis

Do not equate symptom with cause.

Classify the primary cause as one or more of:

SKILL_DEFECT
MODEL_DEFECT
TOOL_DEFECT
DATA_DEFECT
TEST_DEFECT
ENVIRONMENT_DEFECT
KNOWLEDGE_DEFECT
OUTDATED_KNOWLEDGE
ROUTING_DEFECT
PERMISSION_DEFECT
WORKFLOW_DEFECT
HUMAN_INPUT_DEFECT
EXTERNAL_SYSTEM_DEFECT
UNKNOWN

If evidence is insufficient, use UNKNOWN and specify what evidence would disambiguate it.

## Causal chain

When useful, represent:

trigger -> decision -> action -> system response -> observed outcome -> gap -> contributing factors -> corrective control

For high-consequence failures, identify both the direct cause and latent/systemic contributors.

## From lesson to durable change

For each lesson decide:

CONTEXT_ONLY

or

DURABLE_CHANGE_REQUIRED

A durable change may target:

- a Skill instruction;
- a Skill reference;
- a policy/rule file;
- a routing rule;
- a tool contract;
- a test/evaluation case;
- a memory policy;
- an operational checklist;
- a monitoring rule.

A fix plan must name the exact target and the exact intended edit or new test.

## Approval policy

Default: proposal first, then approval.

Apply without a new approval only when the current instruction explicitly authorizes application, such as an unambiguous "apply the fix" or equivalent request, and the target is within that authorization scope.

Even when application is authorized, do not bypass mandatory security, legal, financial, destructive-action, or production-change gates.

## Regression-first evolution

Every material change proposed from an AAR should have a regression case unless the change is demonstrably context-only.

Evolution sequence:

observe -> AAR -> evidence check -> root cause -> lesson -> proposed fix -> regression test -> candidate version -> evaluation -> security checks -> compare -> approval -> promote -> record

Never use a generated regression test merely to make the candidate pass. The test must encode the actual invariant or failure mode.

## Reflection reliability controls

Self-reflection can improve performance, but evidence also shows that reflection is not uniformly beneficial. It can act like re-generation, amplify errors, or degrade performance on some tasks.

Therefore:

- trigger reflection based on task value/risk rather than blindly every turn;
- prefer external feedback when available;
- compare pre- and post-reflection results;
- retain the original output for auditability;
- do not accept a reflection-derived change solely because the model sounds confident;
- detect repeated reflection loops with no measurable improvement;
- use independent evaluation for consequential changes.

## Memory policy

A lesson becomes durable memory only when it clears the configured confidence and specificity threshold.

Store at minimum:

- lesson ID;
- date/time;
- task/session ID when available;
- expected;
- actual;
- why;
- lesson;
- evidence references;
- confidence;
- tags;
- scope;
- affected Skill/rule;
- fix status;
- regression test ID;
- source/provenance;
- supersession status.

Do not store secrets, credentials, private tokens, or unnecessary personal data.

## Deduplication and contradiction handling

Before writing a lesson:

1. search existing lessons;
2. detect semantic duplicates;
3. detect contradictions;
4. merge or supersede only with provenance;
5. preserve historical entries for auditability.

Do not delete a prior lesson merely because a newer lesson differs. Mark it superseded, scoped, or disproven with evidence.

## Confidence model

Use separate dimensions rather than one opaque score:

- evidence strength;
- causal confidence;
- generalization confidence;
- action confidence.

A high-confidence fix requires strong evidence that the proposed change addresses the causal mechanism and will not create unacceptable regressions.

## Stop conditions

Stop the reflection loop when:

- the lesson is specific and tested;
- new iterations produce no meaningful information gain;
- the same failure repeats without new evidence;
- the candidate change has plateaued;
- a safety/permission boundary is reached;
- required evidence is unavailable.

Do not create endless self-critique text.

## Output contract

For a completed AAR, report:

1. Objective/expected outcome.
2. Actual outcome.
3. Evidence-backed gap analysis.
4. Root cause and confidence.
5. Sustainments.
6. Lessons.
7. Fix plan, if needed.
8. Regression test, if created.
9. Applied/proposed/rejected status.
10. Known uncertainty and follow-up.

## Integration with Venu

This Skill composes with:

- `skill-evaluation-and-continuous-learning` for benchmark execution and feedback;
- `agentic-memory-architecture` for durable memory policy;
- `execution-controller-and-tool-governance` for authorization and side-effect control;
- `llm-mcp-guardrails-mastery` for prompt-injection, tool, MCP, identity, and privilege defenses;
- `skill-router-and-composer` for cross-Skill routing;
- `research-evidence-and-provenance` for evidence verification.

The AAR layer never weakens any of these controls.

## Scientific/evidence posture

This Skill is derived from the AAR method and research on verbal reflection and iterative refinement. Results from reflection methods are task-, model-, and feedback-dependent. Treat reflection as an intervention to evaluate, not as a guarantee of learning.

## 10/10 acceptance rule

A release-ready AAR implementation is:

- evidence-grounded;
- specific and reproducible;
- causally cautious;
- auditable;
- regression-backed for material changes;
- approval-aware;
- memory-safe;
- composable with Venu guardrails;
- resistant to reflection loops and self-confirming errors.
