"""Compatibility checking between the generated registry and the legacy
flat-format root ``SKILL-REGISTRY.json`` this project replaces.

Kept as a pure function (no file I/O) so it stays testable even after the
live ``SKILL-REGISTRY.json`` on disk has already been replaced with the new
schema -- see ``tests/unit/test_registry_compat.py``, which exercises this
against a fixed synthetic legacy-format fixture rather than reading
whatever is currently on disk.
"""
from __future__ import annotations

from venu_runtime.schemas.registry_schema import RegistryDocument
from venu_runtime.schemas.skill_schema import SkillKind


def compatibility_problems(existing_legacy: dict, generated: RegistryDocument) -> list[str]:
    """Compare a legacy-format registry dict against a generated document.

    Returns an empty list if the generated registry covers exactly the same
    canonical and cross-cutting skill id sets as the legacy document -- the
    signal that it is safe to replace the legacy file.
    """
    problems: list[str] = []

    existing_canonical = set(existing_legacy.get("canonical_skills", []))
    existing_cross_cutting = set(existing_legacy.get("cross_cutting_extensions", []))

    generated_canonical = {e.id for e in generated.entries if e.kind is SkillKind.CANONICAL}
    generated_cross_cutting = {e.id for e in generated.entries if e.kind is SkillKind.CROSS_CUTTING}

    if existing_canonical != generated_canonical:
        problems.append(
            "canonical skill set differs: "
            f"missing={sorted(existing_canonical - generated_canonical)} "
            f"extra={sorted(generated_canonical - existing_canonical)}"
        )
    if existing_cross_cutting != generated_cross_cutting:
        problems.append(
            "cross-cutting extension set differs: "
            f"missing={sorted(existing_cross_cutting - generated_cross_cutting)} "
            f"extra={sorted(generated_cross_cutting - existing_cross_cutting)}"
        )

    expected_canonical_count = existing_legacy.get("canonical_skill_count")
    if expected_canonical_count is not None and expected_canonical_count != len(generated_canonical):
        problems.append(
            f"canonical_skill_count mismatch: existing={expected_canonical_count} "
            f"generated={len(generated_canonical)}"
        )
    return problems
