# Venu Skillset Plugin Development

This repository is the version-controlled source for the Venu Skill Library,
and (as of Phase 1) the Venu Skill Runtime that loads, validates, and
registers it.

## Layout
- `skills/` — canonical Venu Skills plus `_cross-cutting/` extensions. Source
  of truth; not modified by the runtime.
- `benchmarks/` — static specification-quality checks (Tier 1 evidence only —
  see `docs/ARCHITECTURE.md`). Fixed for portability in Phase 1; check logic
  unchanged.
- `SKILL-REGISTRY.json` — the single authoritative, machine-readable
  registry, **generated** by `venu-runtime/scripts/build_registry.py` from
  `skills/`. Do not hand-edit; regenerate instead.
- `venu-runtime/` — the runtime package (registry, loader, validator so far;
  see `docs/ARCHITECTURE.md` for what's implemented vs. planned).
- `docs/` — `PHASE0-ASSESSMENT.md` (inspection findings) and
  `ARCHITECTURE.md` (registry schema, canonical/cross-cutting distinction,
  5-tier evidence model).

Canonical library: 53 Skills (47 technical/AI + 6 Business Mastery).
Cross-cutting extensions (5) are inheritable capability/policy modules, not
additional domain Skills, unless explicitly promoted later.
