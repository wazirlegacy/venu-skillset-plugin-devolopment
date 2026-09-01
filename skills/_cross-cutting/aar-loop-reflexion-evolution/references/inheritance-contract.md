# Venu AAR Inheritance Contract

The AAR capability is a cross-cutting learning layer for the Venu Skill ecosystem.

## It inherits from

- Venu All-Skills Quality Standard
- execution-controller-and-tool-governance
- llm-mcp-guardrails-mastery
- skill-evaluation-and-continuous-learning
- agentic-memory-architecture
- research-evidence-and-provenance
- skill-router-and-composer

## Inheritance rule

AAR can add learning controls but cannot weaken inherited security, authorization, provenance, privacy, testing, or release requirements.

## Behavior

Every material AAR lesson should be classified as one of:

- observation only
- memory candidate
- regression candidate
- Skill change candidate
- policy/rule candidate
- research refresh candidate

Durable changes require evidence and versioning. High-consequence changes require explicit authorization.

## Runtime integration

Recommended event hooks:

- task.completed
- task.failed
- tool.error
- tool.postcondition_failed
- evaluation.completed
- evaluation.regression
- deployment.completed
- incident.closed
- user.feedback_received

The runtime should emit an immutable AAR record before allowing a candidate improvement to progress to promotion.
