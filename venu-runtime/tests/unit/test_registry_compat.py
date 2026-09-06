"""Tests for the legacy-vs-generated registry compatibility check.

Deliberately uses a hardcoded fixture reproducing the original (pre-Phase-1)
root SKILL-REGISTRY.json content, rather than reading the live file on disk.
Once Phase 1 replaces SKILL-REGISTRY.json with the new generated schema,
the live file will no longer have the legacy ``canonical_skills`` /
``cross_cutting_extensions`` keys this check compares against -- but this
test must keep proving the *skill set itself* has not silently drifted.
"""
from __future__ import annotations

from pathlib import Path

from venu_runtime.registry.builder import build_registry
from venu_runtime.registry.compat import compatibility_problems

REPO_ROOT = Path(__file__).resolve().parents[3]

# Verbatim snapshot of the original root SKILL-REGISTRY.json's canonical and
# cross-cutting name lists, captured during Phase 0 inspection.
LEGACY_REGISTRY_FIXTURE = {
    "canonical_skill_count": 53,
    "canonical_skills": [
        "agent-evaluation-security-governance",
        "agent-orchestration-workflows",
        "agentic-memory-architecture",
        "ai-infrastructure-vps-docker-runtime",
        "ai-trading-research-agents",
        "api-backend-engineering",
        "blender-engineering",
        "brand-fidelity-strategy",
        "commerce-trade-mastery",
        "computer-use",
        "computer-vision",
        "cybersecurity",
        "design-open-source-and-research-discovery",
        "devops-sre",
        "docker-kubernetes",
        "entrepreneurship-mastery",
        "event-driven-agent-architecture",
        "exchange-market-connectors",
        "execution-controller-and-tool-governance",
        "financial-risk",
        "git-github-engineering",
        "integrated-agentic-systems-architect",
        "integrated-ai-development-architect",
        "integrated-business-strategy",
        "legal-law-mastery",
        "linux-windows-automation",
        "llm-model-engineering-and-serving",
        "market-visual-research-and-ai-trading",
        "marketing-management-mastery",
        "mathematical-statistical-reasoning",
        "mcp-tooling-and-ai-gateway-ecosystem",
        "music-rights-metadata-governance",
        "omniroute-gateway-and-adaptive-routing",
        "python-engineering",
        "quant-trading-research-engineering",
        "rag-knowledge-memory-systems",
        "react-nextjs-engineering",
        "realtime-rag-engineering",
        "research-evidence-and-provenance",
        "risk-management-mastery",
        "skill-evaluation-and-continuous-learning",
        "skill-router-and-composer",
        "speech-audio-engineering",
        "sql-database-engineering",
        "testing-qa",
        "typescript-javascript-engineering",
        "ui-ux-engineering",
        "unity-engineering",
        "venu-universal-engineering-orchestrator",
        "vfx-motion-graphics",
        "web-intelligence-and-browser-agents",
        "web-rag-ocr-document-intelligence",
        "webar-8thwall-zappar",
    ],
    "cross_cutting_extensions": [
        "aar-loop-reflexion-evolution",
        "llm-mcp-guardrails-mastery",
        "voice-agent-systems-mastery",
        "blender-mcp-integration-mastery",
        "ai-observability-telemetry-mastery",
    ],
}


def test_generated_registry_is_compatible_with_the_legacy_fixture():
    document = build_registry(REPO_ROOT)
    problems = compatibility_problems(LEGACY_REGISTRY_FIXTURE, document)
    assert problems == []


def test_detects_a_missing_canonical_skill():
    document = build_registry(REPO_ROOT)
    broken_fixture = dict(LEGACY_REGISTRY_FIXTURE)
    broken_fixture["canonical_skills"] = LEGACY_REGISTRY_FIXTURE["canonical_skills"] + ["not-a-real-skill"]
    problems = compatibility_problems(broken_fixture, document)
    assert any("canonical skill set differs" in p for p in problems)


def test_detects_a_count_mismatch():
    document = build_registry(REPO_ROOT)
    broken_fixture = dict(LEGACY_REGISTRY_FIXTURE)
    broken_fixture["canonical_skill_count"] = 999
    problems = compatibility_problems(broken_fixture, document)
    assert any("canonical_skill_count mismatch" in p for p in problems)
