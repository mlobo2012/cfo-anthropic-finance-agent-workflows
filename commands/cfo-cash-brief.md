---
description: Create a CFO cash brief with reconciled cash, runway, commitments, and action decisions.
argument-hint: "[entity] [as-of-date] [--currency GBP]"
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

# CFO Cash Brief

You are the main-session orchestrator. Do not delegate orchestration to an orchestrator sub-agent.

Read `skills/cfo-quality-harness/SKILL.md` and `skills/cfo-cash-brief/SKILL.md`. The brief should be short, decision-oriented, and numerically strict. It must work from Round MCP account data alone, then add transaction, runway, payment, collection, or covenant claims only when the source ledger supports them. Do not present cash, runway, burn, payment coverage, collections, or covenant figures as fact unless the Numerical QA Agent has independently reconciled them. Final publication also requires Narrative Evaluator and CFO Quality Evaluator signoff.
