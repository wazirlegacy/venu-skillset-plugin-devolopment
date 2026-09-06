from __future__ import annotations

from pathlib import Path

from venu_runtime.loader.skill_loader import load_skill
from venu_runtime.schemas.skill_schema import SkillKind

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"


def test_loads_a_well_formed_canonical_skill():
    parsed = load_skill(SKILLS_ROOT / "python-engineering", SkillKind.CANONICAL)
    assert parsed.frontmatter.name == "python-engineering"
    assert parsed.frontmatter.description
    assert parsed.frontmatter_parse_error is None
    assert parsed.body.strip()
    assert any(f.relative_path == "SKILL.md" for f in parsed.files)


def test_tolerates_invalid_yaml_frontmatter_via_fallback_extraction():
    """skills/_cross-cutting/aar-loop-reflexion-evolution/SKILL.md has a
    stray leading space before 'description:' in its frontmatter, making it
    invalid YAML. The loader must not raise, and must still recover name and
    description via the regex fallback.
    """
    parsed = load_skill(
        SKILLS_ROOT / "_cross-cutting" / "aar-loop-reflexion-evolution",
        SkillKind.CROSS_CUTTING,
    )
    assert parsed.frontmatter_parse_error is not None
    assert "YAML" in parsed.frontmatter_parse_error
    assert parsed.frontmatter.name == "aar-loop-reflexion-evolution"
    assert parsed.frontmatter.description


def test_records_frontmatter_name_mismatch_without_correcting_it():
    """skills/_cross-cutting/llm-mcp-guardrails-mastery/SKILL.md declares
    name: execution-controller-and-tool-governance -- a copy-paste leftover.
    The loader must record this verbatim, not silently fix it.
    """
    parsed = load_skill(
        SKILLS_ROOT / "_cross-cutting" / "llm-mcp-guardrails-mastery",
        SkillKind.CROSS_CUTTING,
    )
    assert parsed.frontmatter_parse_error is None
    assert parsed.frontmatter.name == "execution-controller-and-tool-governance"
    assert parsed.directory_name == "llm-mcp-guardrails-mastery"
