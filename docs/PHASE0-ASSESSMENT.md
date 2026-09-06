# Venu Skill Runtime — Phase 0 Assessment

Read-only inspection performed before any implementation. Nothing under
`skills/` was modified to produce this document; all findings are grounded
in the repository content as of commit `5f4185e` (tag `v0.1.0`).

## 1. Current repository architecture

The repository is a **library of 58 prompt specifications** (Markdown with
YAML frontmatter) — not executable software. Three commits exist: a zip
upload via the GitHub web UI, an unpacked-tree push via
`PUSH_TO_GITHUB.ps1`, and a merge of the two. No CI, no license, no
`.gitignore` existed before Phase 1.

`venu-skillset-plugin-github-upload.zip` at the repo root is a byte-for-byte
packaging duplicate of the `skills/`+`benchmarks/` tree (58 `SKILL.md` files
in the zip, 58 in the working tree) — a leftover from the upload process,
not a Skill artifact. Left in place per the Phase 1 decision; not deleted.

## 2. Complete Skill inventory

| Category | Count | Structure |
|---|---|---|
| Technical/AI Skills | 47 | single `SKILL.md`, uniform "10/10 Operating Contract" template |
| Business Mastery Skills | 6 | `SKILL.md` (bespoke per-domain structure) + `references/sources.md` + `tests/cases.md` (15-item narrative checklist) |
| Cross-cutting extensions | 5 | mostly single `SKILL.md`; `aar-loop-reflexion-evolution` also has `references/`, `evaluations/`, `scripts/` |
| **Total** | **58** | matches `README.md` and (pre-Phase-1) `SKILL-REGISTRY.json` |

Two registries disagreed before Phase 1: root `SKILL-REGISTRY.json` (53
canonical + 5 cross-cutting) vs. `benchmarks/SKILL-REGISTRY-2026-09.md` (47
technical only, no business mastery, no cross-cutting). Phase 1 resolves
this — see §6.

Two real data-quality defects were found by building the loader/validator,
not previously documented anywhere in the repository:

- `skills/_cross-cutting/aar-loop-reflexion-evolution/SKILL.md` has a stray
  leading space before `description:` in its frontmatter, making the block
  **invalid YAML** (`yaml.safe_load` raises `mapping values are not allowed
  here`). Confirmed independently with a raw `yaml.safe_load` sweep across
  all 58 files before any runtime code was written.
- `skills/_cross-cutting/llm-mcp-guardrails-mastery/SKILL.md` has valid YAML,
  but its frontmatter `name:` field is
  `execution-controller-and-tool-governance` — a copy-paste leftover
  colliding with an unrelated, real Skill of that name.

Neither is corrected by Phase 1 (Skill content is treated as a source
artifact); both are recorded as structural validation findings (see §6).

## 3. Existing benchmark/evaluation system

Entirely **static text linting of the SKILL.md files themselves** — no LLM
is invoked, no tool is called, nothing runs against a real runtime. Three
scripts existed with two portability bugs:

- `run_benchmark.py` hardcoded `ROOT=Path('/mnt/data/bench')`, a foreign
  sandbox path; could not run in this repository at all.
- `unified_benchmark.py` / `run-skill-regression.py` used
  `ROOT=Path(__file__).resolve().parent` (the `benchmarks/` folder itself,
  which has no `SKILL.md` files) — both silently scanned **zero** Skills.

Fixed for portability in Phase 1 via `benchmarks/_skill_scope.py` (see §8),
without touching the check logic, the anchor/concept keyword tables, or the
documented 47-technical-skill scope.

Committed result snapshots (`benchmark_results.json`,
`unified_benchmark_results.json`) are static-quality (Tier 1) evidence only.
`benchmarks/REGRESSION-MANIFEST-235.json` (47 skills × 5 scenario classes)
has every entry at `status: "runtime-pending"` — zero behavioral cases have
ever been executed. `benchmarks/UNIFIED-BENCHMARK-FINAL-2026-09.md` already
states this limitation for itself.

**Resolved per the approved Phase 1 decisions:** the canonical behavioral
target is **265** (53 canonical Skills × 5 scenario classes), not the 235
the existing manifest currently encodes (47 × 5, technical skills only).
Extending the manifest to 265 with concrete, non-generic scenarios is
explicitly **out of scope for Phase 1** (Evaluation Engine work, a later
phase) — see `docs/ARCHITECTURE.md`'s 5-tier evidence model for how this is
represented honestly in the meantime.

## 4. Reusable components already present

Before Phase 1, exactly 4 Python files existed in the whole repository —
3 static benchmark scripts (above) and
`skills/_cross-cutting/aar-loop-reflexion-evolution/scripts/append_lesson.py`,
a small dependency-free CLI that appends structured AAR lesson entries to a
Markdown log without touching Skill/rule files — a good seed for the
"observe" stage of the Controlled Improvement Engine (a later phase).

Substantial *prose* design already maps onto the target runtime's
components (`skill-router-and-composer`, `execution-controller-and-tool-governance`,
`llm-mcp-guardrails-mastery`, `mcp-tooling-and-ai-gateway-ecosystem`,
`ai-observability-telemetry-mastery`, `agent-evaluation-security-governance`,
`aar-loop-reflexion-evolution`) — these are specifications to build from,
not code.

## 5–6. Proposed runtime architecture, directory structure, registry

See `docs/ARCHITECTURE.md` for the registry schema actually implemented in
Phase 1, and the full 15-component target architecture below (not yet
implemented beyond registry/loader/validator).

Fifteen components, split into a capability plane (proposes, never
authorizes: Registry, Loader/Validator, Router, Composer, Context/Retrieval)
and an authority plane (deterministic, outside model reasoning: Policy
Engine, Authorization, Tool/MCP Gateway, Execution Controller, Verification),
plus a cross-cutting governance loop (Observability, Evaluation Engine,
Regression Manager, Controlled Improvement Engine, Version/Provenance
Manager). "The model proposes; deterministic policy authorizes; tools
execute; validators verify" — `execution-controller-and-tool-governance`'s
own stated doctrine, now the runtime's actual design principle rather than
prose guidance.

```
venu-runtime/
  pyproject.toml
  src/venu_runtime/
    schemas/      # skill_schema.py, registry_schema.py — implemented
    loader/        # skill_loader.py, validator.py — implemented
    registry/       # registry.py, builder.py, compat.py — implemented
    router/ composer/ context/ policy/ authz/ gateway/
    execution/ verification/ observability/
    evaluation/ regression/ improvement/            # later phases
  scripts/build_registry.py     # implemented
  tests/unit/                    # implemented — 19 tests
skills/            # untouched — remains source of truth
benchmarks/         # existing scripts fixed for portability, not replaced
docs/
  PHASE0-ASSESSMENT.md   # this file
  ARCHITECTURE.md
```

## 7. Phase-by-phase implementation plan

| Phase | Scope |
|---|---|
| 0 | This inspection |
| **1 (current)** | Registry schemas, loader, validator, authoritative registry builder, benchmark portability fixes, docs, `.gitignore` |
| 2 | Router + Composer + Context layer (capability plane, no execution) |
| 3 | Policy Engine + Authorization + Tool/MCP Gateway (authority plane, sandboxed) |
| 4 | Execution Controller + Verification/Postcondition |
| 5 | Observability + Evaluation Engine — first real (not placeholder) scenarios |
| 6 | Regression Manager + scale to all 53 canonical Skills × 5 scenario classes (265) |
| 7 | Controlled Improvement Engine (observe→...→promote/rollback) |
| 8 | Hardening: security/red-team suite, docs, versioning policy |

## 8. Security/control-plane design

Implements the non-negotiable invariants as code, not prose, starting in
Phase 3 (Policy Engine/Authorization/Gateway do not exist yet). Phase 1's
contribution is narrower but load-bearing: the registry's `id` field uses
the **directory name**, never the frontmatter-declared `name`, specifically
because a Skill's own declared identity is untrusted input (proven by the
`llm-mcp-guardrails-mastery` collision above) — the first concrete instance
of "Skill text is not an authorization source" applied in code.

## 9. Runtime evaluation design — the 5-tier evidence model

See `docs/ARCHITECTURE.md` for the full definition. Summary: Tier 1
(specification quality, existing static linters) and Tier 2 (static schema
validation, this phase's loader/validator) are implemented. Tiers 3–5
(runtime behavioral evidence, security evidence, regression evidence) are
not, and no report may blend them into one number.

## 10. Controlled self-improvement design

Not implemented in Phase 1 (explicitly out of scope). Target lifecycle:
`observe → detect → generate proposal → evaluate → regression test →
security review → human approval → canary → verify → promote OR rollback`,
extending `append_lesson.py`'s existing append-only, non-authoritative
pattern for the "observe" stage.

## 11. Risks and resolved/open questions

- **265 vs. 235** — resolved per the Phase 1 decision: 265 (53 × 5) is
  authoritative. The manifest itself is not yet extended (Phase 6 work).
- **Two registries** — resolved: one authoritative generated registry
  (§6), replacing root `SKILL-REGISTRY.json` after a passing compatibility
  check, with `benchmarks/SKILL-REGISTRY-2026-09.md` marked superseded.
- **The upload zip** — left in place per the Phase 1 decision; a pending
  packaging artifact, removable only in an explicit later cleanup change.
- **Business-mastery skills' test format** — still an open question:
  15 narrative checks (`tests/cases.md`) vs. the 5-class runtime taxonomy
  are structurally different; the Phase 1 decision requires folding them
  into the same canonical evaluation schema while preserving domain-specific
  acceptance criteria, which is Evaluation Engine work (a later phase), not
  attempted here.
- **No sandboxing environment chosen yet** for the Execution Controller —
  needed before Phase 4.
- **Metadata inconsistency** — only 11 of 47 technical Skills declare a
  `metadata:` block (version/maturity/research_snapshot); none of the 6
  business-mastery Skills do. The registry records `null` rather than
  fabricating values for the rest — see `docs/ARCHITECTURE.md`.

## 12. Files created/modified in Phase 1

New: `venu-runtime/` (full package — schemas, loader, registry, tests,
`scripts/build_registry.py`, `pyproject.toml`), `benchmarks/_skill_scope.py`,
`docs/ARCHITECTURE.md`, `docs/PHASE0-ASSESSMENT.md` (this file), `.gitignore`.

Modified: `benchmarks/run_benchmark.py`, `benchmarks/unified_benchmark.py`,
`benchmarks/run-skill-regression.py` (portability fixes only — see diffs),
`benchmarks/benchmark_results.json` / `unified_benchmark_results.json`
(regenerated by re-running the now-portable scripts), root
`SKILL-REGISTRY.json` (replaced with the generated schema after a passing
compatibility check), `benchmarks/SKILL-REGISTRY-2026-09.md` (marked
superseded), `README.md` (points at `venu-runtime/` and `docs/`).

Untouched: everything under `skills/`;
`venu-skillset-plugin-github-upload.zip`.
