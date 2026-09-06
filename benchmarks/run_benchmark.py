from pathlib import Path
import re, json, statistics, hashlib

# Phase 1 portability fix: ROOT was hardcoded to '/mnt/data/bench', a
# foreign sandbox path from wherever this script was originally authored --
# it could not run in this repository at all. Discovery/output paths now
# come from _skill_scope.py, resolved relative to this repository. See that
# module's docstring for the full before/after and the documented 47-skill
# scope this restores (not a narrowing or widening of the original scope).
from _skill_scope import discover_technical_skill_dirs, OUTPUT_DIR
skills=discover_technical_skill_dirs()
required_sections=[
    '## Purpose','## Evidence posture','## Operating workflow','## Quality gates','## Integration',
    '## 10/10 Operating Contract','### Task framing','### Evidence discipline','### Architecture discipline',
    '### Deterministic controls','### Verification','### Postconditions','### Security',
    '### Reliability and observability','### Performance','### Provenance and uncertainty','### Skill composition',
    '### Completion report','## 10/10 acceptance rule','## 10/10 Domain Specialization','## Research anchors'
]
base_checks={
    'frontmatter': lambda t: bool(re.search(r'^---\n(?s:.*?)\n---\n',t)),
    'name': lambda t: bool(re.search(r'^name:\s*[^\n]+',t,re.M)),
    'description': lambda t: bool(re.search(r'^description:\s*[^\n]+',t,re.M)),
    'workflow_numbered': lambda t: len(re.findall(r'^\d+\. ',t,re.M))>=5,
    'source_urls': lambda t: len(re.findall(r'https?://',t))>=5,
    'quality_contract': lambda t: all(s in t for s in required_sections),
    'size_reasonable': lambda t: len(t)<30000,
}
# domain-specific anchors; multiple acceptable tokens per skill
anchors={
'agent-evaluation-security-governance':['evaluation','security','authorization','adversarial','audit'],
'agent-orchestration-workflows':['LangGraph','n8n','Dify','Langflow','tool'],
'agentic-memory-architecture':['memory','temporal','retrieval','semantic','CDC'],
'ai-infrastructure-vps-docker-runtime':['Docker','VPS','container','queue','observability'],
'ai-trading-research-agents':['TradingAgents','risk','point-in-time','debate','portfolio'],
'api-backend-engineering':['API','REST','OpenAPI','authentication','idempot'],
'blender-engineering':['Blender','bpy','Geometry Nodes','BMesh','headless'],
'brand-fidelity-strategy':['User-friendly','Accessible','Dependable','Personal','Meaningful','Salient'],
'computer-use':['computer-use','screen','action','observation','permission'],
'computer-vision':['OpenCV','vision','detection','segmentation','tracking'],
'cybersecurity':['OWASP','least privilege','threat','input validation','supply-chain'],
'design-open-source-and-research-discovery':['OpenDesign','curat','license','resource','design system'],
'devops-sre':['SLO','SLI','error budget','OpenTelemetry','deployment'],
'docker-kubernetes':['Docker','Kubernetes','RBAC','seccomp','probe'],
'event-driven-agent-architecture':['event','idempot','replay','dead-letter','schema'],
'exchange-market-connectors':['CCXT','exchange','rate limit','WebSocket','adapter'],
'execution-controller-and-tool-governance':['authorization','policy','postcondition','tool','sandbox'],
'financial-risk':['VaR','Expected Shortfall','drawdown','stress','liquidity'],
'git-github-engineering':['Git','GitHub','branch','commit','CI'],
'integrated-agentic-systems-architect':['signal','context','retrieve','reason','validate'],
'integrated-ai-development-architect':['architecture','LLM','RAG','MCP','deployment'],
'linux-windows-automation':['Linux','Windows','PowerShell','shell','privilege'],
'llm-model-engineering-and-serving':['Transformer','quantization','vLLM','llama.cpp','inference'],
'market-visual-research-and-ai-trading':['TradingView','chart','BullGPT','technical','scenario'],
'mathematical-statistical-reasoning':['probability','statistical','validation','uncertainty','calibration'],
'mcp-tooling-and-ai-gateway-ecosystem':['MCP','tool','A2A','gateway','authorization'],
'music-rights-metadata-governance':['ISRC','ISWC','DDEX','ownership','metadata'],
'omniroute-gateway-and-adaptive-routing':['OmniRoute','routing','provider','fallback','quality'],
'python-engineering':['Python','typing','async','packaging','pytest'],
'quant-trading-research-engineering':['Backtrader','NautilusTrader','backtest','slippage','optimization'],
'rag-knowledge-memory-systems':['RAG','LlamaIndex','RAGFlow','memory','retrieval'],
'react-nextjs-engineering':['React','Next.js','Server Component','Client Component','App Router'],
'realtime-rag-engineering':['real-time','RAG','freshness','retrieval','provenance'],
'research-evidence-and-provenance':['primary','provenance','vendor','citation','version'],
'skill-evaluation-and-continuous-learning':['regression','evaluation','benchmark','failure','learning'],
'skill-router-and-composer':['router','compose','dependency','conflict','Skill'],
'speech-audio-engineering':['speech','audio','Whisper','sampling','latency'],
'sql-database-engineering':['SQL','PostgreSQL','MVCC','EXPLAIN','transaction'],
'testing-qa':['unit','integration','property','regression','E2E'],
'typescript-javascript-engineering':['TypeScript','JavaScript','ESM','CJS','type'],
'ui-ux-engineering':['UI','UX','Figma','accessibility','design system'],
'unity-engineering':['Unity','C#','Addressables','Input System','asset'],
'venu-universal-engineering-orchestrator':['orchestrator','Skill router','execution','validation','memory'],
'vfx-motion-graphics':['After Effects','VFX','motion','expression','composit'],
'web-intelligence-and-browser-agents':['browser','Firecrawl','session','web','provenance'],
'web-rag-ocr-document-intelligence':['OCR','document','DeepDoc','layout','RAG'],
'webar-8thwall-zappar':['WebAR','8th Wall','Zappar','tracking','AR'],
}
results=[]
for p in skills:
    t=(p/'SKILL.md').read_text(encoding='utf-8',errors='replace')
    checks={k:bool(fn(t)) for k,fn in base_checks.items()}
    ak=anchors.get(p.name,[])
    checks['domain_anchors']=sum(1 for a in ak if a.lower() in t.lower())>=max(3, min(5,len(ak)))
    checks['no_placeholder']=not any(x in t.lower() for x in ['todo','tbd','fill in','placeholder'])
    checks['no_absolute_guarantee']=not re.search(r'\bguarantee(?:d|s)?\b',t,re.I)
    score=10*sum(checks.values())/len(checks)
    results.append({'skill':p.name,'score':round(score,2),'checks':checks,'sha256':hashlib.sha256(t.encode()).hexdigest(),'chars':len(t)})

out={'skills_tested':len(results),'scores':results,'avg':round(statistics.mean(r['score'] for r in results),2),'min':min(r['score'] for r in results),'max':max(r['score'] for r in results),'failures':[r for r in results if r['score']<10]}
(OUTPUT_DIR/'benchmark_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'skills_tested':out['skills_tested'],'avg':out['avg'],'min':out['min'],'max':out['max'],'fail_count':len(out['failures'])},indent=2))
for r in out['failures']:
    print(r['skill'], r['score'], [k for k,v in r['checks'].items() if not v])
