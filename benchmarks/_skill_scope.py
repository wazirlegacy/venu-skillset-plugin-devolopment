#!/usr/bin/env python3
"""Shared, portable skill-discovery scope for the static benchmark scripts.

Phase 1 portability fix -- what was broken and why
----------------------------------------------------
Before this fix, each benchmark script resolved its scan root differently,
and none of them worked from a fresh checkout of this repository:

* ``run_benchmark.py`` hardcoded ``ROOT = Path('/mnt/data/bench')``, a
  foreign absolute path from whatever sandbox originally produced it. It
  could not run in this repository at all (``ROOT.iterdir()`` would raise
  ``FileNotFoundError``).
* ``unified_benchmark.py`` and ``run-skill-regression.py`` both used
  ``ROOT = Path(__file__).resolve().parent``, i.e. the ``benchmarks/``
  folder itself. That folder contains no ``SKILL.md`` files (they live in
  ``../skills/``), so both scripts would silently scan zero Skills and
  report a trivially "passing" empty result instead of failing loudly.

This module fixes both problems by resolving paths relative to the
repository root (``benchmarks/..``), which is portable to any checkout
location, and by centralizing the skill-name scope so the three scripts
cannot drift from each other.

Scope note (documented per the Phase 1 decision requiring this to be
explained, not silently changed)
-----------------------------------------------------------------------
The benchmark scripts' own companion documents -- EVALUATION-MATRIX-2026-09.md,
SKILL-REGISTRY-2026-09.md, REGRESSION-MANIFEST-235.json, and
UNIFIED-BENCHMARK-FINAL-2026-09.md -- all consistently describe the scope
as "47 technical/AI Skills," and the per-skill ``anchors``/``concepts``
keyword tables embedded in ``run_benchmark.py`` and ``unified_benchmark.py``
contain exactly those same 47 names (verified to match exactly during this
fix). The 6 Business Mastery Skills use a different, intentionally looser
template (see ``skills/*/tests/cases.md``, a 15-item narrative checklist)
and are not covered by this structural "10/10 Operating Contract" checker.
The 5 cross-cutting extensions are similarly out of scope.

This fix therefore restores the scripts to their evidenced original scope
of exactly 47 technical/AI Skills -- it does not narrow OR widen that
scope. Extending structural scoring to Business Mastery or cross-cutting
Skills would require new anchor/concept keyword definitions for each and is
left as a deliberate, separate decision for a later phase, not something a
portability fix should do silently.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
OUTPUT_DIR = Path(__file__).resolve().parent

# The 6 Business Mastery Skill directory names. Also duplicated in
# venu-runtime/src/venu_runtime/registry/builder.py -- intentionally, so
# that these stand-alone scripts keep zero dependency on the venu_runtime
# package. Keep both lists in sync if the canonical skill set changes.
BUSINESS_MASTERY_SKILLS = frozenset(
    {
        "commerce-trade-mastery",
        "entrepreneurship-mastery",
        "integrated-business-strategy",
        "legal-law-mastery",
        "marketing-management-mastery",
        "risk-management-mastery",
    }
)


def discover_technical_skill_dirs() -> list[Path]:
    """Return the 47 technical-skill directories, sorted.

    Portable to any checkout location: resolved relative to this file
    rather than a hardcoded absolute path or the wrong working directory.
    """
    return sorted(
        p
        for p in SKILLS_ROOT.iterdir()
        if p.is_dir()
        and p.name not in BUSINESS_MASTERY_SKILLS
        and p.name != "_cross-cutting"
        and (p / "SKILL.md").exists()
    )
