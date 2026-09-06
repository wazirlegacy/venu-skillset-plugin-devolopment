"""Builds the single authoritative Venu Skill registry by scanning the
``skills/`` directory on disk.

Read-only: nothing under ``skills/`` is modified by this process. Callers
(the CLI in ``scripts/build_registry.py``) decide whether and where to
persist the resulting ``RegistryDocument``.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from venu_runtime.loader.skill_loader import load_skill
from venu_runtime.loader.validator import validate_skill
from venu_runtime.schemas.registry_schema import (
    BenchmarkStatus,
    RegistryDocument,
    RegistryEntry,
    RiskTier,
    ValidationStatus,
)
from venu_runtime.schemas.skill_schema import SkillKind

# The 6 Business Mastery Skill directory names, used to split "canonical"
# into the "technical" / "business_mastery" categories the repository's own
# README.md and (pre-Phase-1) SKILL-REGISTRY.json already document:
# 53 canonical = 47 technical + 6 Business Mastery.
#
# This is intentionally duplicated in benchmarks/_skill_scope.py rather than
# imported from it, so the benchmarks/ scripts keep zero dependency on this
# package and remain runnable stand-alone (see docs/PHASE1-CHECKPOINT.md).
# Keep both lists in sync if the canonical skill set changes.
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

CROSS_CUTTING_DIRNAME = "_cross-cutting"

_VALIDATION_STATUS_MAP = {
    "pass": ValidationStatus.PASS,
    "warning": ValidationStatus.WARNING,
    "fail": ValidationStatus.FAIL,
}


def _git_commit(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return None


def _category_for(directory_name: str, kind: SkillKind) -> str:
    if kind is SkillKind.CROSS_CUTTING:
        return "cross_cutting"
    if directory_name in BUSINESS_MASTERY_SKILLS:
        return "business_mastery"
    return "technical"


def _load_static_benchmark(path: Path) -> dict[str, dict]:
    """Best-effort load of benchmarks/unified_benchmark_results.json.

    Returns {} on any problem (missing file, bad JSON, unexpected shape) --
    a missing or stale Tier 1 report must never prevent the registry (Tier 2)
    from building.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {row["skill"]: row for row in data.get("results", [])}
    except Exception:
        return {}


def build_registry(repo_root: Path, static_benchmark_path: Path | None = None) -> RegistryDocument:
    """Scan repo_root/skills and build the authoritative registry document."""
    skills_root = repo_root / "skills"
    commit = _git_commit(repo_root)

    static_results: dict[str, dict] = {}
    if static_benchmark_path is not None and static_benchmark_path.exists():
        static_results = _load_static_benchmark(static_benchmark_path)

    entries: list[RegistryEntry] = []

    canonical_dirs = sorted(
        p
        for p in skills_root.iterdir()
        if p.is_dir() and p.name != CROSS_CUTTING_DIRNAME and (p / "SKILL.md").exists()
    )
    for directory in canonical_dirs:
        entries.append(_build_entry(directory, SkillKind.CANONICAL, repo_root, commit, static_results))

    cross_cutting_root = skills_root / CROSS_CUTTING_DIRNAME
    if cross_cutting_root.is_dir():
        cross_cutting_dirs = sorted(
            p for p in cross_cutting_root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
        )
        for directory in cross_cutting_dirs:
            entries.append(
                _build_entry(directory, SkillKind.CROSS_CUTTING, repo_root, commit, static_results)
            )

    canonical_count = sum(1 for e in entries if e.kind is SkillKind.CANONICAL)
    cross_cutting_count = sum(1 for e in entries if e.kind is SkillKind.CROSS_CUTTING)

    return RegistryDocument(
        canonical_count=canonical_count,
        cross_cutting_count=cross_cutting_count,
        total_count=len(entries),
        entries=entries,
    )


def _build_entry(
    directory: Path,
    kind: SkillKind,
    repo_root: Path,
    commit: str | None,
    static_results: dict[str, dict],
) -> RegistryEntry:
    parsed = load_skill(directory, kind)
    validation = validate_skill(parsed)

    benchmark_row = static_results.get(parsed.directory_name)
    if benchmark_row is not None:
        benchmark_status = BenchmarkStatus(
            static_checks_available=True,
            static_checks_passed=benchmark_row.get("passed"),
            static_checks_total=benchmark_row.get("total"),
        )
    else:
        benchmark_status = BenchmarkStatus(static_checks_available=False)

    return RegistryEntry(
        id=parsed.directory_name,
        version=(parsed.frontmatter.metadata or {}).get("version"),
        kind=kind,
        category=_category_for(parsed.directory_name, kind),
        maturity=(parsed.frontmatter.metadata or {}).get("maturity"),
        description=parsed.frontmatter.description or "",
        declared_tool_scopes=[],
        cross_cutting_dependencies=[],
        risk_tier=RiskTier.UNCLASSIFIED,
        benchmark_status=benchmark_status,
        provenance={
            "source_repository": "wazirlegacy/venu-skillset-plugin-devolopment",
            "source_commit": commit,
            "relative_path": str(directory.relative_to(repo_root)),
        },
        source_hash=parsed.skill_md_sha256,
        validation_status=_VALIDATION_STATUS_MAP[validation.status],
        validation_findings=validation.findings,
    )
