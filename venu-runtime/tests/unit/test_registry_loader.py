from __future__ import annotations

from pathlib import Path

from venu_runtime.registry.builder import build_registry
from venu_runtime.registry.registry import Registry

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_round_trips_through_json(tmp_path):
    document = build_registry(REPO_ROOT)
    out = tmp_path / "registry.json"
    out.write_text(document.model_dump_json(indent=2), encoding="utf-8")

    registry = Registry.load(out)
    assert len(registry) == 58
    assert len(registry.canonical()) == 53
    assert len(registry.cross_cutting()) == 5

    entry = registry.get("python-engineering")
    assert entry is not None
    assert entry.description

    assert registry.get("not-a-real-skill") is None
    assert "python-engineering" in registry
    assert "not-a-real-skill" not in registry
