from __future__ import annotations

from pathlib import Path

from venu_runtime.loader.skill_loader import load_skill
from venu_runtime.loader.validator import validate_skill
from venu_runtime.schemas.skill_schema import SkillKind

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"


def test_well_formed_skill_passes():
    parsed = load_skill(SKILLS_ROOT / "python-engineering", SkillKind.CANONICAL)
    result = validate_skill(parsed)
    assert result.status == "pass"
    assert result.findings == []


def test_invalid_yaml_frontmatter_fails():
    parsed = load_skill(
        SKILLS_ROOT / "_cross-cutting" / "aar-loop-reflexion-evolution",
        SkillKind.CROSS_CUTTING,
    )
    result = validate_skill(parsed)
    assert result.status == "fail"
    assert any("YAML" in f for f in result.findings)


def test_name_mismatch_is_a_warning_not_a_failure():
    parsed = load_skill(
        SKILLS_ROOT / "_cross-cutting" / "llm-mcp-guardrails-mastery",
        SkillKind.CROSS_CUTTING,
    )
    result = validate_skill(parsed)
    assert result.status == "warning"
    assert any("does not match directory name" in f for f in result.findings)
