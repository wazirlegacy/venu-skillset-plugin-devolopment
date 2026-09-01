---
name: blender-mcp-integration-mastery
description: High-assurance Blender MCP integration and agent workflow skill. Use for connecting AI agents to Blender, inspecting scenes, validating Blender/API versions, executing bounded Blender operations, rendering/visual verification, asset workflows, recovery, telemetry, and MCP-aware tool orchestration.
---

# Blender MCP Integration Mastery

## Purpose
Provide a portable, evidence-driven workflow for AI-assisted Blender work through MCP, while preserving the universal Venu security and provenance contract.

## Core operating model
Treat Blender automation as two layers:

1. Agent/client + MCP server
2. Blender add-on / live Blender process

Prefer an explicit inspect → plan → execute → verify workflow.

## Mandatory workflow
1. Identify Blender version, MCP server version, add-on version, client, transport, endpoint and execution mode.
2. Inspect current scene/file state before mutation.
3. Consult the relevant Blender API/manual documentation before using uncertain APIs or operators.
4. Choose the narrowest tool capable of the task.
5. For consequential mutation, make the change bounded, explicit and recoverable.
6. Execute small, idempotent steps.
7. Verify state using structured summaries and visual evidence where appropriate.
8. Verify postconditions.
9. Record version/provenance and relevant telemetry.
10. On failure, classify root cause before changing the Skill or workflow.

## Tool hierarchy
Prefer structured inspection and documentation tools before arbitrary code execution.

Typical tool families:
- scene/object summaries
- blend-file summaries
- Blender API/manual search
- screenshots / viewport inspection
- render-to-path / thumbnail rendering
- targeted UI navigation
- execute_blender_code for bounded operations

Arbitrary Python execution is a powerful destructive capability. Treat it as high-risk and apply Venu's LLM/MCP guardrails, authorization and sandbox policies.

## Version awareness
Never assume Blender API compatibility.
Check:
- Blender version
- add-on/protocol version
- MCP server version
- active execution mode
- relevant API documentation

When behavior differs by Blender release, state the exact version boundary.

## Official vs community implementations
Keep vendor/source provenance explicit.

Community implementation researched:
ahujasid/blender-mcp

Official first-party Blender implementation researched:
Blender Lab / blender_mcp

Do not silently merge their behaviors or claim equivalence.

## Security
For arbitrary code execution:
- require explicit authorized scope
- constrain filesystem/network access
- never expose credentials to Blender Python
- avoid public network binding for local execution bridges
- validate URLs and downloaded assets
- protect against path traversal and malicious archives
- preserve auditability
- verify postconditions

The official Blender MCP documentation warns that its server executes LLM-generated code in Blender without a sandbox; therefore treat direct code execution as a privileged operation and prefer isolation for sensitive projects.

## Reliability
Design for:
- socket disconnects
- timeouts
- stale add-ons
- version mismatch
- background/headless differences
- event-loop stalls
- partial execution
- duplicate calls
- concurrent tool calls

Serialize operations when a transport requires response ordering.

Fail fast on unrecoverable transport states, then reconnect only under bounded retry policy.

## Visual verification
For visual tasks:
inspect scene → mutate → screenshot/render → compare against acceptance criteria.

Do not treat successful Python execution as proof that the visual result is correct.

## Asset workflows
External assets must be treated as untrusted inputs.
Validate:
- origin
- expected type
- archive safety
- path traversal
- file size
- import format
- Blender compatibility

Keep optional vendor asset services isolated from the core Blender workflow.

## Observability and trajectory
Capture:
- user goal
- tool name
- parameters
- pre-state
- action
- post-state
- outcome
- duration
- Blender/MCP versions
- errors
- verification result

Telemetry never grants authorization.

## High-value inherited capabilities
This Skill inherits:
- Venu universal LLM/MCP guardrails
- Blender engineering
- Python engineering
- MCP tooling and gateway architecture
- execution-controller/tool governance
- testing/QA
- DevOps/SRE
- event-driven architecture
- AI observability/telemetry
- skill evaluation/continuous learning
- research evidence/provenance

## Research-derived distinctions

### ahujasid community implementation
Strengths:
- broad ecosystem integrations
- Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin and Hunyuan3D workflows
- screenshots and scene inspection
- telemetry and trajectory capture
- add-on/server version handshake
- persistent socket connection
- concurrent-call serialization
- security regression tests such as archive path-traversal checks

Source repository:
https://github.com/ahujasid/blender-mcp

### Blender Lab official implementation
Strengths:
- first-party Blender integration
- Blender 5.1+ support
- structured scene/object and blend-file inspection
- bundled Blender API/manual documentation
- screenshots, navigation and rendering tools
- background/CLI variants for several inspection operations
- smaller, clearer first-party integration surface

Source:
https://www.blender.org/lab/mcp-server/
https://projects.blender.org/lab/blender_mcp

The official Blender page explicitly warns that the MCP server can execute LLM-generated Blender code without guards. Design Venu integrations with stronger external guardrails and isolation rather than weakening this warning.

## Recommended Venu strategy
Use a provider-neutral Blender adapter with two source profiles:

OFFICIAL:
Blender Lab / blender_mcp

COMMUNITY:
ahujasid/blender-mcp

Expose common capabilities through a normalized interface, while retaining source-specific extensions.

Recommended common interface:
- inspect_scene
- inspect_object
- inspect_blendfile
- search_api_docs
- search_manual_docs
- screenshot
- render
- execute_bounded_code
- navigate_ui
- check_health
- check_version
- recover_connection

Never hide source/version differences behind false compatibility.

## Evolution rule
When a Blender MCP failure is observed:
1. capture trace
2. determine whether failure is Skill/model/tool/environment/version related
3. research current authoritative documentation
4. create candidate improvement
5. create regression test
6. run prior regression suite
7. run new test
8. promote only after required approval

## Quality boundary
This Skill is a release-grade specification, not empirical proof of perfect runtime behavior.
