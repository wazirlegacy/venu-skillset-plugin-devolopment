"""Regression tests proving the benchmarks/ static-check scripts are
portable (run correctly from a fresh checkout) after the Phase 1 fix.

Before the fix:
  - run_benchmark.py hardcoded ROOT=Path('/mnt/data/bench'), a foreign
    sandbox path; it could not run in this repository at all.
  - unified_benchmark.py and run-skill-regression.py used
    ROOT=Path(__file__).resolve().parent (the benchmarks/ folder itself),
    which contains no SKILL.md files, so they silently scanned zero Skills.

After the fix, all three resolve skills/ relative to the repository root
(via benchmarks/_skill_scope.py) and scan exactly the 47 technical/AI
Skills they were originally designed for.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"


def _run(script_name: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BENCHMARKS_DIR / script_name)],
        cwd=BENCHMARKS_DIR,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_run_skill_regression_finds_47_skills_and_passes():
    result = _run("run-skill-regression.py")
    assert "47 skills checked" in result.stdout, result.stdout
    assert result.returncode == 0, result.stdout + result.stderr


def test_run_benchmark_scans_47_skills_and_is_reproducible():
    result = _run("run_benchmark.py")
    assert result.returncode == 0, result.stderr
    data = json.loads((BENCHMARKS_DIR / "benchmark_results.json").read_text(encoding="utf-8"))
    assert data["skills_tested"] == 47
    assert len(data["scores"]) == 47


def test_unified_benchmark_scans_47_skills_and_is_reproducible():
    result = _run("unified_benchmark.py")
    assert result.returncode == 0, result.stderr
    data = json.loads((BENCHMARKS_DIR / "unified_benchmark_results.json").read_text(encoding="utf-8"))
    assert data["summary"]["skills_tested"] == 47
    assert len(data["results"]) == 47


def test_scripts_run_correctly_regardless_of_current_working_directory(tmp_path):
    """The old ROOT=Path(__file__).resolve().parent bug was invisible unless
    you happened to invoke the script from a different cwd. Prove the fix
    does not depend on cwd by running from an unrelated directory.
    """
    result = subprocess.run(
        [sys.executable, str(BENCHMARKS_DIR / "run-skill-regression.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert "47 skills checked" in result.stdout, result.stdout
    assert result.returncode == 0, result.stdout + result.stderr
