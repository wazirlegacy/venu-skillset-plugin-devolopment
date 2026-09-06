from __future__ import annotations

from pathlib import Path

from venu_runtime.registry.builder import build_registry
from venu_runtime.schemas.registry_schema import ValidationStatus
from venu_runtime.schemas.skill_schema import SkillKind

REPO_ROOT = Path(__file__).resolve().parents[3]


def _document():
    return build_registry(REPO_ROOT)


def test_counts_match_the_documented_58_skill_library():
    document = _document()
    assert document.canonical_count == 53
    assert document.cross_cutting_count == 5
    assert document.total_count == 58


def test_category_split_matches_47_technical_plus_6_business_mastery():
    document = _document()
    categories = {}
    for entry in document.entries:
        categories[entry.category] = categories.get(entry.category, 0) + 1
    assert categories["technical"] == 47
    assert categories["business_mastery"] == 6
    assert categories["cross_cutting"] == 5


def test_entry_id_is_always_the_directory_name_not_the_frontmatter_name():
    """Directory name is the authoritative identifier even when a Skill's
    own frontmatter 'name' field is wrong (see the llm-mcp-guardrails-mastery
    copy-paste bug) -- the registry must not inherit that bug.
    """
    document = _document()
    guardrails = next(e for e in document.entries if e.id == "llm-mcp-guardrails-mastery")
    assert guardrails.id == "llm-mcp-guardrails-mastery"
    assert guardrails.validation_status == ValidationStatus.WARNING


def test_known_bad_yaml_skill_is_flagged_fail_but_still_present():
    document = _document()
    aar = next(e for e in document.entries if e.id == "aar-loop-reflexion-evolution")
    assert aar.kind == SkillKind.CROSS_CUTTING
    assert aar.validation_status == ValidationStatus.FAIL
    assert any("YAML" in f for f in aar.validation_findings)


def test_no_entry_ids_are_duplicated():
    document = _document()
    ids = [e.id for e in document.entries]
    assert len(ids) == len(set(ids))
