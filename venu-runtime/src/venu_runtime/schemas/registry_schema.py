"""Pydantic models for the single authoritative Venu Skill registry.

Replaces the two independent, drifting registry sources identified in
docs/PHASE0-ASSESSMENT.md (root ``SKILL-REGISTRY.json`` and
``benchmarks/SKILL-REGISTRY-2026-09.md``) with one generated document. See
``registry/builder.py`` for how this is populated and
``registry/compat.py`` for the compatibility check gating the replacement.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field

from venu_runtime.schemas.skill_schema import SkillKind


class ValidationStatus(str, Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


class RiskTier(str, Enum):
    """Placeholder classification pending the Policy Engine (a later phase).

    Phase 1 does not compute this from real risk analysis: no Skill in the
    current repository declares a risk tier or tool scope, and no
    authorization/execution layer exists yet to enforce one. Every entry is
    UNCLASSIFIED until the Policy Engine assigns a real tier from declared
    tool scopes and content review. This field exists now so the schema
    does not need a breaking change when that lands.
    """

    UNCLASSIFIED = "unclassified"


class BenchmarkStatus(BaseModel):
    """Tier 1 (specification quality) evidence only.

    This block reflects the existing static SKILL.md content checks in
    ``benchmarks/`` -- frontmatter/section/URL/placeholder linting. It is
    NOT Tier 3 runtime behavioral evidence and must never be read as proof
    that an LLM using the Skill produces correct results. See
    docs/ARCHITECTURE.md for the full 5-tier evidence model.
    """

    tier: str = "specification_quality"
    static_checks_available: bool = False
    static_checks_passed: int | None = None
    static_checks_total: int | None = None
    runtime_cases_pending: int = 5  # 5 scenario classes per Skill; all runtime-pending until a later phase


class RegistryEntry(BaseModel):
    id: str  # directory name -- authoritative identifier; see ARCHITECTURE.md on why not frontmatter `name`
    version: str | None = None
    kind: SkillKind
    category: str  # "technical" | "business_mastery" | "cross_cutting" -- see ARCHITECTURE.md
    maturity: str | None = None
    description: str

    declared_tool_scopes: list[str] = Field(default_factory=list)
    cross_cutting_dependencies: list[str] = Field(default_factory=list)

    risk_tier: RiskTier = RiskTier.UNCLASSIFIED
    benchmark_status: BenchmarkStatus = Field(default_factory=BenchmarkStatus)

    provenance: dict
    source_hash: str
    validation_status: ValidationStatus
    validation_findings: list[str] = Field(default_factory=list)


class RegistryDocument(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    generator: str = "venu_runtime.registry.builder"
    repository: str = "wazirlegacy/venu-skillset-plugin-devolopment"

    canonical_count: int
    cross_cutting_count: int
    total_count: int

    entries: list[RegistryEntry]
