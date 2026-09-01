from pathlib import Path
import re, json, statistics, hashlib
ROOT=Path(__file__).resolve().parent
skills=sorted([p for p in ROOT.iterdir() if p.is_dir() and (p/"SKILL.md").exists()])
headers=[r'^## Purpose\s*$',r'^## Evidence posture\s*$',r'^## Operating workflow\s*$',r'^## Quality gates\s*$',r'^## Integration\s*$',r'^## 10/10 Operating Contract(?: — mandatory quality bar)?\s*$',r'^### Task framing\s*$',r'^### Evidence discipline\s*$',r'^### Architecture discipline\s*$',r'^### Deterministic controls\s*$',r'^### Verification\s*$',r'^### Postconditions\s*$',r'^### Security\s*$',r'^### Reliability and observability\s*$',r'^### Performance\s*$',r'^### Provenance and uncertainty\s*$',r'^### Skill composition\s*$',r'^### Completion report\s*$',r'^## 10/10 acceptance rule\s*$',r'^## 10/10 Domain Specialization\s*$',r'^## Research anchors(?: — verified/current snapshot 2026-09-01)?\s*$']
concepts={
'agent-evaluation-security-governance':['evaluation','authorization','audit','adversarial'], 'agent-orchestration-workflows':['LangGraph','n8n','Dify','Langflow','tool'], 'agentic-memory-architecture':['memory','temporal','retrieval','CDC'], 'ai-infrastructure-vps-docker-runtime':['Docker','VPS','queue','worker'], 'ai-trading-research-agents':['TradingAgents','point-in-time','risk','portfolio'], 'api-backend-engineering':['API','OpenAPI','authentication','idempot'], 'blender-engineering':['Blender','bpy','Geometry Nodes','BMesh'], 'brand-fidelity-strategy':['User-friendly','Accessible','Dependable','Personal','Meaningful','Salient'], 'computer-use':['screen','action','observation','permission'], 'computer-vision':['OpenCV','detection','segmentation','tracking'], 'cybersecurity':['OWASP','least privilege','threat','secret'], 'design-open-source-and-research-discovery':['OpenDesign','curat','license'], 'devops-sre':['SLO','error budget','OpenTelemetry','rollback'], 'docker-kubernetes':['Docker','Kubernetes','RBAC','seccomp','probe'], 'event-driven-agent-architecture':['event','idempot','replay','dead-letter','schema'], 'exchange-market-connectors':['CCXT','rate limit','WebSocket','adapter'], 'execution-controller-and-tool-governance':['authorization','postcondition','sandbox','tool'], 'financial-risk':['VaR','Expected Shortfall','drawdown','stress','liquidity'], 'git-github-engineering':['Git','GitHub','branch','CI'], 'integrated-agentic-systems-architect':['signal','retrieve','reason','validate'], 'integrated-ai-development-architect':['architecture','LLM','RAG','MCP'], 'linux-windows-automation':['Linux','Windows','PowerShell','privilege'], 'llm-model-engineering-and-serving':['Transformer','quantization','vLLM','llama.cpp'], 'market-visual-research-and-ai-trading':['TradingView','chart','BullGPT','scenario'], 'mathematical-statistical-reasoning':['probability','validation','uncertainty','calibration'], 'mcp-tooling-and-ai-gateway-ecosystem':['MCP','tool','A2A','gateway'], 'music-rights-metadata-governance':['ISRC','ISWC','DDEX','ownership'], 'omniroute-gateway-and-adaptive-routing':['OmniRoute','routing','provider','fallback','quality'], 'python-engineering':['Python','typing','async','packaging'], 'quant-trading-research-engineering':['Backtrader','NautilusTrader','backtest','slippage'], 'rag-knowledge-memory-systems':['RAG','LlamaIndex','RAGFlow','retrieval'], 'react-nextjs-engineering':['React','Next.js','Server Component','App Router'], 'realtime-rag-engineering':['real-time','RAG','freshness','provenance'], 'research-evidence-and-provenance':['primary source','provenance','citation','version'], 'skill-evaluation-and-continuous-learning':['regression','evaluation','benchmark','failure','learning'], 'skill-router-and-composer':['router','compose','dependency','conflict'], 'speech-audio-engineering':['speech','audio','Whisper','sampling'], 'sql-database-engineering':['SQL','PostgreSQL','MVCC','EXPLAIN'], 'testing-qa':['unit','integration','property','regression'], 'typescript-javascript-engineering':['TypeScript','JavaScript','ESM','CJS'], 'ui-ux-engineering':['UI','UX','Figma','accessibility'], 'unity-engineering':['Unity','C#','Addressables','Input System'], 'venu-universal-engineering-orchestrator':['orchestrator','routing','execution','validation'], 'vfx-motion-graphics':['After Effects','VFX','motion','expression'], 'web-intelligence-and-browser-agents':['browser','Firecrawl','session','web'], 'web-rag-ocr-document-intelligence':['OCR','document','DeepDoc','layout','RAG'], 'webar-8thwall-zappar':['WebAR','8th Wall','Zappar','tracking']
}
def has_any(t,arr): return any(a.lower() in t.lower() for a in arr)
rows=[]
for p in skills:
 t=(p/'SKILL.md').read_text(encoding='utf-8',errors='replace')
 neg=False
 for line in t.splitlines():
  if re.search(r'\bguarantee(?:s|d)?\s+(?:profit|correctness|security|accuracy|safety)\b',line,re.I):
   low=line.lower();
   if not any(n in low for n in ['never ','not ','no ','without ','do not ','does not ','cannot ']): neg=True
 tests={
  'metadata':bool(re.search(r'^---\n',t) and re.search(r'^name:\s*'+re.escape(p.name)+r'\s*$',t,re.M) and re.search(r'^description:\s*.{20,}$',t,re.M)),
  'happy_path':all(re.search(h,t,re.M|re.I) for h in headers[:4]) and bool(re.search(r'^\s*\d+\.\s+',t,re.M)),
  'ambiguous_input': all(x.lower() in t.lower() for x in ['Task framing','constraints','assumptions']),
  'adversarial_security': all(x in t.lower() for x in ['security','failure']) and any(x in t.lower() for x in ['adversarial','attack','abuse','malformed','least privilege']),
  'composition': all(re.search(h,t,re.M|re.I) for h in [r'^## Integration\s*$',r'^### Skill composition\s*$']),
  'version_recovery_provenance': all(x in t.lower() for x in ['version','recovery','rollback','provenance and uncertainty']),
  'quality_contract': all(re.search(h,t,re.M|re.I) for h in headers[5:]),
  'research_sources': len(re.findall(r'https?://',t))>=5 and bool(re.search(r'^## Research anchors',t,re.M)),
  'domain_specificity': sum(1 for a in concepts[p.name] if a.lower() in t.lower())>=max(3,int(0.75*len(concepts[p.name]))),
  'no_placeholders':not any(x in t.lower() for x in ['todo','tbd','fill in','placeholder']),
  'no_unsafe_positive_guarantee':not neg,
 }
 rows.append({'skill':p.name,'score':round(10*sum(tests.values())/len(tests),2),'passed':sum(tests.values()),'total':len(tests),'tests':tests,'sha256':hashlib.sha256(t.encode()).hexdigest()})
summary={'skills_tested':len(rows),'tests_per_skill':len(rows[0]['tests']),'total_tests':len(rows)*len(rows[0]['tests']),'passed_tests':sum(r['passed'] for r in rows),'failed_tests':sum(r['total']-r['passed'] for r in rows),'avg_score':round(statistics.mean(r['score'] for r in rows),2),'min_score':min(r['score'] for r in rows),'max_score':max(r['score'] for r in rows),'skills_at_10':sum(r['score']==10 for r in rows)}
Path(ROOT/'unified_benchmark_results.json').write_text(json.dumps({'summary':summary,'results':rows},indent=2))
print(json.dumps(summary,indent=2))
for r in rows:
 if r['score']<10: print(r['skill'],r['score'],[k for k,v in r['tests'].items() if not v])
