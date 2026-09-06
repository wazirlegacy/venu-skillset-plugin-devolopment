"""Loads and queries a generated Venu Skill registry document."""
from __future__ import annotations

import json
from pathlib import Path

from venu_runtime.schemas.registry_schema import RegistryDocument, RegistryEntry
from venu_runtime.schemas.skill_schema import SkillKind


class Registry:
    """Read-only, in-memory view over a ``RegistryDocument``."""

    def __init__(self, document: RegistryDocument):
        self._document = document
        self._by_id = {entry.id: entry for entry in document.entries}

    @classmethod
    def load(cls, path: Path) -> "Registry":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(RegistryDocument.model_validate(data))

    @property
    def document(self) -> RegistryDocument:
        return self._document

    def get(self, skill_id: str) -> RegistryEntry | None:
        return self._by_id.get(skill_id)

    def canonical(self) -> list[RegistryEntry]:
        return [e for e in self._document.entries if e.kind is SkillKind.CANONICAL]

    def cross_cutting(self) -> list[RegistryEntry]:
        return [e for e in self._document.entries if e.kind is SkillKind.CROSS_CUTTING]

    def __len__(self) -> int:
        return len(self._document.entries)

    def __contains__(self, skill_id: str) -> bool:
        return skill_id in self._by_id
