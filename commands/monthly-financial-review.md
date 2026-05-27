---
description: Produce a monthly financial review with reconciled numbers and evaluator signoff.
argument-hint: "[entity] [month] [--currency GBP]"
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

# Monthly Financial Review

You are the main-session orchestrator. Do not delegate orchestration to an orchestrator sub-agent.

Read `skills/cfo-quality-harness/SKILL.md` and `skills/monthly-financial-review/SKILL.md`. The default monthly review is `connector_mode: round_only`, a Round-only treasury review. Use `connector_mode: round_with_xero` only when Xero is connected inside Round and Round MCP exposes usable Xero reports, accounts, invoices, and bank transactions. Do not ask for separate Xero MCP credentials in v1.

If `round_with_xero` returns usable data, produce the full review with P&L, balance sheet, cash movement, AR/AP or invoice context, risks, and actions. If Xero is connected in Xero but Round MCP does not expose usable Xero data, block the full accounting review and tell the user to verify the Round-Xero connection.

The monthly review is not final until:

- every displayed cash, account, movement, P&L, balance sheet, working capital, and KPI number has source/formula/period/unit/entity/currency metadata;
- independent recomputation matches Round MCP, Round MCP Xero tools, or declared source extracts;
- unresolved numbers are excluded from factual claims; and
- the Narrative Evaluator, CFO Quality Evaluator, and Final Controller sign off.
