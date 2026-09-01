#!/usr/bin/env python3
"""Append a structured AAR lesson without external dependencies.

This implementation is intentionally conservative: it appends evidence fields,
keeps historical entries, and does not edit Skill/rule files. Promotion is a
separate, approval-gated operation in the Venu runtime.
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re

HEADER = """# Lessons\n\nStructured AAR lessons. Durable changes must be reviewed and regression-tested separately.\n"""


def load(path: Path) -> str:
    if not path.exists():
        return HEADER
    text = path.read_text(encoding="utf-8")
    return text if text.strip() else HEADER


def add(args: argparse.Namespace) -> None:
    path = Path(args.file)
    text = load(path)
    date = dt.date.today().isoformat()
    entry = [f"## {date} -- {args.lesson}"]
    for label, value in (("Expected", args.expected), ("Actual", args.actual), ("Why", args.why),
                         ("Evidence", args.evidence), ("Confidence", args.confidence),
                         ("Scope", args.scope), ("tags", args.tags)):
        if value:
            entry.append(f"- {label}: {value}")
    path.write_text(text.rstrip() + "\n\n" + "\n".join(entry) + "\n", encoding="utf-8")
    print(f"Wrote lesson to {path}")


def list_lessons(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        print(f"No lessons file at {path}")
        return
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=## )", text)
    for block in blocks:
        block = block.strip()
        if not block.startswith("## "):
            continue
        if args.tag and re.search(rf"^[- ]tags:\s*.*\b{re.escape(args.tag)}\b", block, re.I | re.M) is None:
            continue
        print(block)
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="LESSONS.md")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--tag")
    parser.add_argument("--lesson")
    parser.add_argument("--expected")
    parser.add_argument("--actual")
    parser.add_argument("--why")
    parser.add_argument("--evidence")
    parser.add_argument("--confidence")
    parser.add_argument("--scope")
    parser.add_argument("--tags")
    args = parser.parse_args()
    if args.list:
        list_lessons(args)
    else:
        if not args.lesson:
            parser.error("--lesson is required unless using --list")
        add(args)


if __name__ == "__main__":
    main()
