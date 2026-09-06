"""Pydantic models describing a single parsed Venu Skill package.

These models describe what the loader extracts from a Skill directory on
disk. They are intentionally permissive about Skill content: the runtime's
job in Phase 1 is to observe and validate what already exists in
``skills/``, not to force existing Skill files into a stricter shape than
they currently have. Malformed or inconsistent frontmatter is captured as
data (``frontmatter_parse_error``, mismatched ``name``, etc.) rather than
raising -- see ``loader/validator.py`` for how that data becomes a
validation finding.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class SkillKind(str, Enum):
    """Distinguishes canonical domain Skills from cross-cutting extensions.

    Cross-cutting extensions are inheritable capability/policy modules, not
    additional domain Skills, per the Phase 0 decision. This distinction is
    load-bearing for the registry and must never be collapsed into a single
    flat list.
    """

    CANONICAL = "canonical"
    CROSS_CUTTING = "cross_cutting"


class SkillFrontmatter(BaseModel):
    """Raw fields as declared in a SKILL.md YAML frontmatter block.

    All fields are optional at this layer so that a Skill with missing or
    malformed frontmatter is still loadable -- one bad file must not abort
    loading the other 57. The validator turns absence/mismatch into
    reported findings instead.
    """

    name: str | None = None
    description: str | None = None
    metadata: dict = Field(default_factory=dict)


class SkillFile(BaseModel):
    """A single file inside a Skill package directory, tracked for provenance."""

    relative_path: str
    sha256: str
    size_bytes: int


class ParsedSkill(BaseModel):
    """Everything the loader extracts from one Skill package directory."""

    directory_name: str
    directory_path: str
    kind: SkillKind

    frontmatter: SkillFrontmatter
    frontmatter_raw: str | None = None
    frontmatter_parse_error: str | None = None

    body: str
    section_headers: list[str] = Field(default_factory=list)

    files: list[SkillFile] = Field(default_factory=list)
    skill_md_sha256: str

    loaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
