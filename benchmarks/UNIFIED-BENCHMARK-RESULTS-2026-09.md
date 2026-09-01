# Venu Unified 47-Skill Benchmark

Research snapshot: 2026-09-01

## Result

- Skills tested: 47
- Contract tests per Skill: 11
- Total automated checks: 517
- Passed: 517
- Failed: 0
- Skill scores: 47/47 at 10.0/10.0
- Mean score: 10.0/10.0

## What was tested

1. Metadata/identity contract.
2. Happy-path capability/workflow contract.
3. Ambiguous-input and constraint handling.
4. Adversarial/failure/security handling.
5. Cross-Skill composition.
6. Version-change/recovery/provenance handling.
7. Required 10/10 quality-contract sections.
8. Research/provenance anchors.
9. Domain-specific conceptual anchors.
10. Placeholder/unfinished-content checks.
11. Unsafe positive guarantee-claim check.

## Upgrade event

The first run produced 517 checks with 490 passed and 27 failed. Failures clustered around legacy Skills that used different section headings and omitted a standardized operating workflow/domain-specialization block. The benchmark was used as the trigger for deterministic upgrades: missing canonical sections were added, explicit numbered workflows were added where needed, and domain specialization was filled with skill-specific controls. A false-positive checker for negative guarantee warnings was corrected so safety disclaimers are not misclassified.

## Regression policy

Every future Skill change should rerun the same 517 checks. Any new failure becomes a regression record before release. A behavioral runtime suite should additionally execute the five scenario classes against a real agent runtime and retain traces, outputs, tool calls, and postcondition evidence.

## Limitation

This benchmark verifies the Skill repository's written contracts and knowledge anchors. It does not execute the 47 Skills inside ChatGPT's native Skill runtime or prove real-world solution quality. That requires an external agent/runtime harness with controlled tasks and judges.
