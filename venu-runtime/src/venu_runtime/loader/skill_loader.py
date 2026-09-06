"""Loads a single Venu Skill package (a directory containing SKILL.md) from
disk into a ``ParsedSkill``.

This loader is intentionally tolerant: a malformed Skill (bad frontmatter
YAML, a mismatched ``name`` field) is still loaded, with the problem
recorded on the model, rather than raising and aborting the whole registry
build over one file. Turning that recorded problem into a pass/warning/fail
verdict is a separate concern -- see ``validator.py``.

Two real data-quality issues in the current repository exercise this
tolerance directly:

* ``skills/_cross-cutting/aar-loop-reflexion-evolution/SKILL.md`` has a
  stray leading space before ``description:`` in its frontmatter, which
  makes the block invalid YAML. This loader falls back to a line-based
  regex extraction so the Skill still loads with its name/description
  intact, and records the YAML error for the validator to surface.
* ``skills/_cross-cutting/llm-mcp-guardrails-mastery/SKILL.md`` has valid
  YAML, but its frontmatter ``name:`` field is
  ``execution-controller-and-tool-governance`` -- a copy-paste leftover
  from another Skill's template. This loader does not "correct" it; it
  records the frontmatter value as declared, separately from the
  authoritative directory-derived identifier used everywhere else in the
  registry (see ``registry/builder.py``).
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

from venu_runtime.schemas.skill_schema import (
    ParsedSkill,
    SkillFile,
    SkillFrontmatter,
    SkillKind,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
SECTION_HEADER_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.M)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _extract_frontmatter(text: str) -> tuple[SkillFrontmatter, str | None, str | None]:
    """Returns (frontmatter, raw_frontmatter_text, parse_error)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return (
            SkillFrontmatter(),
            None,
            "no frontmatter block found (expected '---' delimited YAML at file start)",
        )

    raw = match.group(1)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        name_match = re.search(r"^\s*name:\s*(.+)$", raw, re.M)
        desc_match = re.search(r"^\s*description:\s*(.+)$", raw, re.M)
        fallback = SkillFrontmatter(
            name=name_match.group(1).strip() if name_match else None,
            description=desc_match.group(1).strip() if desc_match else None,
        )
        return fallback, raw, f"YAML parse error: {exc}"

    if not isinstance(data, dict):
        return (
            SkillFrontmatter(),
            raw,
            f"frontmatter did not parse to a mapping (got {type(data).__name__})",
        )

    return (
        SkillFrontmatter(
            name=data.get("name"),
            description=data.get("description"),
            metadata=data.get("metadata") or {},
        ),
        raw,
        None,
    )


def load_skill(directory: Path, kind: SkillKind) -> ParsedSkill:
    """Load one Skill package directory into a ``ParsedSkill``.

    Raises FileNotFoundError if ``directory/SKILL.md`` does not exist --
    that is a caller error (the directory should have been filtered by the
    caller), not a Skill-content problem for the validator to report.
    """
    skill_md_path = directory / "SKILL.md"
    raw_bytes = skill_md_path.read_bytes()
    text = raw_bytes.decode("utf-8", errors="replace")

    frontmatter, frontmatter_raw, parse_error = _extract_frontmatter(text)

    body = FRONTMATTER_RE.sub("", text, count=1)
    section_headers = [
        f"{hashes} {title.strip()}" for hashes, title in SECTION_HEADER_RE.findall(body)
    ]

    files: list[SkillFile] = []
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            files.append(
                SkillFile(
                    relative_path=str(path.relative_to(directory)),
                    sha256=_sha256_bytes(data),
                    size_bytes=len(data),
                )
            )

    return ParsedSkill(
        directory_name=directory.name,
        directory_path=str(directory),
        kind=kind,
        frontmatter=frontmatter,
        frontmatter_raw=frontmatter_raw,
        frontmatter_parse_error=parse_error,
        body=body,
        section_headers=section_headers,
        files=files,
        skill_md_sha256=_sha256_bytes(raw_bytes),
    )
