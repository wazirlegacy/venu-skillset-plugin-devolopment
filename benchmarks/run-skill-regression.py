#!/usr/bin/env python3
"""Strict repository-level regression benchmark for Venu Skills."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parent
skills=sorted([p for p in ROOT.iterdir() if p.is_dir() and (p/"SKILL.md").exists()])
required=[
 r'^## Purpose\s*$',r'^## Evidence posture\s*$',r'^## Operating workflow\s*$',r'^## Quality gates\s*$',r'^## Integration\s*$',
 r'^## 10/10 Operating Contract(?: — mandatory quality bar)?\s*$',r'^### Task framing\s*$',r'^### Evidence discipline\s*$',r'^### Architecture discipline\s*$',
 r'^### Deterministic controls\s*$',r'^### Verification\s*$',r'^### Postconditions\s*$',r'^### Security\s*$',r'^### Reliability and observability\s*$',
 r'^### Performance\s*$',r'^### Provenance and uncertainty\s*$',r'^### Skill composition\s*$',r'^### Completion report\s*$',
 r'^## 10/10 acceptance rule\s*$',r'^## 10/10 Domain Specialization\s*$',r'^## Research anchors(?: — verified/current snapshot 2026-09-01)?\s*$'
]
failed=[]
for p in skills:
 t=(p/"SKILL.md").read_text(encoding="utf-8",errors="replace")
 def H(rx): return bool(re.search(rx,t,re.M|re.I))
 checks=[
  ("metadata",bool(re.search(r'^---\n',t) and re.search(r'^name:\s*'+re.escape(p.name)+r'\s*$',t,re.M) and re.search(r'^description:\s*.{20,}$',t,re.M))),
  ("required_sections",all(H(x) for x in required)),
  ("workflow",len(re.findall(r'^\s*\d+\.\s+',t,re.M))>=5),
  ("source_urls",len(re.findall(r'https?://',t))>=5),
  ("no_placeholders",not any(x in t.lower() for x in ['todo','tbd','fill in','placeholder']))
 ]
 if not all(v for _,v in checks): failed.append((p.name,[k for k,v in checks if not v]))
print(f"{len(skills)} skills checked; failures={len(failed)}")
for n,b in failed: print(n,b)
sys.exit(1 if failed else 0)
