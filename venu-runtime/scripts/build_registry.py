#!/usr/bin/env python3
"""CLI entrypoint: build the authoritative Venu Skill registry and,
optionally, write it to disk after a compatibility check against the
existing root ``SKILL-REGISTRY.json``.

Usage:
    python3 scripts/build_registry.py               # scan + report only
    python3 scripts/build_registry.py --write        # scan, verify, write

Without --write, this prints a summary and the compatibility-check result
but touches no file. This mirrors the Phase 0 decision that the generated
registry "may replace the duplicated root registry after compatibility has
been verified" -- verification is a visible, separate step, not an
automatic side effect of building.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from venu_runtime.registry.builder import build_registry  # noqa: E402
from venu_runtime.registry.compat import compatibility_problems  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root (default: parent of venu-runtime/)",
    )
    parser.add_argument("--write", action="store_true", help="Write the generated registry to --out")
    parser.add_argument("--out", default=None, help="Output path (default: SKILL-REGISTRY.json at repo root)")
    parser.add_argument(
        "--static-benchmark",
        default=None,
        help="Path to unified_benchmark_results.json (default: benchmarks/unified_benchmark_results.json)",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root) if args.repo_root else Path(__file__).resolve().parents[2]
    out_path = Path(args.out) if args.out else repo_root / "SKILL-REGISTRY.json"
    static_benchmark_path = (
        Path(args.static_benchmark)
        if args.static_benchmark
        else repo_root / "benchmarks" / "unified_benchmark_results.json"
    )

    document = build_registry(repo_root, static_benchmark_path=static_benchmark_path)

    print(
        f"Scanned skills: {document.total_count} "
        f"(canonical={document.canonical_count}, cross_cutting={document.cross_cutting_count})"
    )

    fail = [e for e in document.entries if e.validation_status.value == "fail"]
    warn = [e for e in document.entries if e.validation_status.value == "warning"]
    passed = document.total_count - len(fail) - len(warn)
    print(f"Validation: pass={passed} warning={len(warn)} fail={len(fail)}")
    for entry in warn + fail:
        print(f"  [{entry.validation_status.value}] {entry.id}: {'; '.join(entry.validation_findings)}")

    existing_path = repo_root / "SKILL-REGISTRY.json"
    problems: list[str] = []
    if existing_path.exists():
        existing = json.loads(existing_path.read_text(encoding="utf-8"))
        problems = compatibility_problems(existing, document)
    else:
        problems = ["existing SKILL-REGISTRY.json not found -- nothing to compare against"]

    if problems:
        print("\nCompatibility check FAILED against existing SKILL-REGISTRY.json:")
        for problem in problems:
            print(f"  - {problem}")
    else:
        print(
            "\nCompatibility check PASSED: generated registry covers the same "
            "canonical + cross-cutting skill id sets as the existing root registry."
        )

    if args.write:
        if problems:
            print("\nRefusing to write: compatibility check failed. Resolve the mismatch and re-run.")
            return 1
        out_path.write_text(document.model_dump_json(indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
