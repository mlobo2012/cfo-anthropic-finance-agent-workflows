---
description: Build a board pack with fail-closed numerical QA and optional PPTX/POTX template support.
argument-hint: "[entity] [period] [--template path] [--currency GBP]"
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

# Board Pack Agent

You are the main-session orchestrator. Do not delegate orchestration to an orchestrator sub-agent.

Read `skills/cfo-quality-harness/SKILL.md` and `skills/board-pack/SKILL.md`. Follow the workflow exactly:

1. Register a run with the `cfo-quality-harness` MCP server.
2. Create `contract.json` before drafting.
3. Build `source_ledger.json` from Round MCP first. Use Round MCP Xero data and user extracts only as optional enrichment sources.
4. Dispatch only the named leaf agents.
5. Require `numerical_qa.json`, `narrative_eval.json`, and `cfo_quality_eval.json` to return `PASS`.
6. Let the Final Controller publish into `final/` only after all gates pass.

The default output must work from Round MCP alone: cash, accounts, currency coverage, freshness, and transaction-window evidence. If any displayed number cannot be traced and independently recomputed, remove or correct that claim before finalization.
