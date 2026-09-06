"""Structural/loadability validation for a parsed Venu Skill.

This is deliberately narrow: it checks whether a Skill package is
well-formed enough for the runtime to load and register it (Tier 2 --
static schema validation, see docs/ARCHITECTURE.md). It does not re-check
the full "10/10 Operating Contract" content bar -- that remains the job of
the existing static benchmark scripts in ``benchmarks/`` (Tier 1 --
specification quality), which were fixed for portability rather than
duplicated here. Keeping these two checks separate avoids two different
parts of the runtime disagreeing about what "valid" means for the same
file.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from venu_runtime.schemas.skill_schema import ParsedSkill


@dataclass
class ValidationResult:
    status: str  # "pass" | "warning" | "fail"
    findings: list[str] = field(default_factory=list)


def validate_skill(skill: ParsedSkill) -> ValidationResult:
    findings: list[str] = []
    status = "pass"

    if skill.frontmatter_parse_error:
        findings.append(f"frontmatter: {skill.frontmatter_parse_error}")
        status = "fail"

    if not skill.frontmatter.name:
        findings.append("frontmatter missing required 'name' field")
        status = "fail"
    if not skill.frontmatter.description:
        findings.append("frontmatter missing required 'description' field")
        status = "fail"

    if skill.frontmatter.name and skill.frontmatter.name != skill.directory_name:
        findings.append(
            f"frontmatter name '{skill.frontmatter.name}' does not match "
            f"directory name '{skill.directory_name}'"
        )
        if status == "pass":
            status = "warning"

    if not skill.body.strip():
        findings.append("Skill body is empty after the frontmatter block")
        status = "fail"

    return ValidationResult(status=status, findings=findings)
