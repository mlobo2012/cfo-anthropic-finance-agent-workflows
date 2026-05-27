# Changelog

## 1.0.0

- Added `connector_mode` to the workflow contract with `round_only` and `round_with_xero`.
- Kept v1 on Round MCP only: Xero evidence must come through Round MCP tools or user extracts, with direct Xero MCP documented only as a future fallback.
- Added external CFO quality evaluation as a third required gate alongside numerical QA and narrative evaluation.
- Updated monthly review rules so full accounting review blocks when Round MCP cannot expose usable Xero data.

## 0.2.0

- Added a Round-only artifact builder that produces complete PASS run folders from Round MCP account and bank-transaction extracts.
- Re-scoped all five workflows so the out-of-box path works with Round MCP alone, while Xero, payment files, payroll files, board templates, and models enrich the artifacts when present.
- Updated the quality rules so missing optional sources narrow final artifact scope instead of blocking supported Round-visible claims.

## 0.1.0

- Initial Claude Code and Claude Cowork scaffold for Round MCP CFO workflows.
- Added commands, skills, shared agents, workflow templates, artifact schemas, and local quality harness MCP server.
- Added fail-closed numerical QA contract for PASS, REVISE, and BLOCKED statuses.
- Added static free-tool landing page draft under the plugin boundary.
- Replaced placeholder Round connector documentation with the Round OAuth MCP `mcp-remote` setup, expected tool list, recovery guidance, and auth material handling rules.
