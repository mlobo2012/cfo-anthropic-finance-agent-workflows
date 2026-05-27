# Workflow Template: Board Pack

## Contract Defaults

- `workflow`: `board_pack`
- `connector_mode`: `round_only` by default; `round_with_xero` only when Round MCP exposes usable Xero data
- `output.audience`: `Board`
- `output.artifact_type`: `pptx` or `multiple`
- `rounding.policy`: agree with board template, usually nearest 1000 or nearest 1 for ratios
- Required sources: Round `get_accounts` for the out-of-box baseline. Round `get_bank_transactions` enriches movement sections when rows are returned. Round MCP Xero P&L/balance-sheet evidence, management accounts, KPI workbook, forecast, and board template are optional enrichment sources.

## Required Sections

1. Executive summary
2. Cash and liquidity
3. Account and currency coverage
4. Movement summary when Round transaction rows exist
5. Decisions required
6. Optional financial performance, forecast, and appendix sections when evidence exists

## Numeric QA Focus

- P&L and variance tables
- Cash rollforward
- KPI definitions
- Forecast bridges
- Working capital movement
- Percent versus percentage point wording

## Final Artifact

`final/final.pptx` when a deck is requested. `final/final.md` may accompany it as speaker notes or workpaper summary.

## Blockers

- No Round account evidence for cash slides.
- Round MCP Xero or management accounts do not tie to displayed financials when those sections are included.
- Bridge chart endpoints do not reconcile.
