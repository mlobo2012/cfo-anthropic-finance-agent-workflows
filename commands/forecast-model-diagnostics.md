---
description: Diagnose forecasts and finance models with source-traced drivers, formulas, and unresolved risks.
argument-hint: "[entity] [forecast-period] [--model path] [--currency GBP]"
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__cfo-quality-harness__*
  - mcp__round-mcp__*
---

# Forecast + Model Diagnostics

You are the main-session orchestrator. Do not delegate orchestration to an orchestrator sub-agent.

Read `skills/cfo-quality-harness/SKILL.md` and `skills/forecast-model-diagnostics/SKILL.md`. The default diagnostic is a Round-only cash runway baseline. Treat any supplied model as evidence to inspect, not truth to repeat. Recompute key drivers, compare against Round MCP, Round MCP Xero tools, or source extracts, and publish only claims whose formula lineage, source reconciliation, narrative support, and CFO quality review are resolved.
