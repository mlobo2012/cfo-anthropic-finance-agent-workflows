---
description: Build a payment and payroll readiness pack with approvals, funding, exceptions, and duplicate checks.
argument-hint: "[entity] [payment-date] [--payroll-date date] [--currency GBP]"
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

# Payment + Payroll Readiness

You are the main-session orchestrator. Do not delegate orchestration to an orchestrator sub-agent.

Read `skills/cfo-quality-harness/SKILL.md` and `skills/payment-payroll-readiness/SKILL.md`. This workflow must publish a Round-only funding baseline from account and transaction-window evidence, then add payment-file, payroll, approval, duplicate-check, beneficiary, and cutoff checks only when those sources exist. It must not imply that Round MCP can approve, release, or change payments. The Final Controller may publish only after every claim included in the readiness pack reconciles and the Narrative Evaluator plus CFO Quality Evaluator sign off.
