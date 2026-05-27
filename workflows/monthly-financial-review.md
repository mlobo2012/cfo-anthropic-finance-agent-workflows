# Workflow Template: Monthly Financial Review

## Contract Defaults

- `workflow`: `monthly_financial_review`
- `connector_mode`: `round_only` by default; `round_with_xero` only when Round MCP exposes usable Xero data
- `output.audience`: `CFO`
- `output.artifact_type`: `md`
- Required sources: Round `get_accounts` for the out-of-box treasury review. Round `get_bank_transactions` enriches movement. In `round_with_xero`, use Round MCP `get_xero_profit_and_loss_report`, `get_xero_balance_sheet_report`, `get_xero_accounts`, `get_xero_invoices`, and `get_xero_bank_transactions`.

## Required Sections

1. One-page conclusion
2. Round cash position
3. Account and currency coverage
4. Cash movement when transaction rows exist
5. Optional P&L, balance sheet, working capital, and close sections when evidence exists
6. Risks, actions, and close gaps

## Numeric QA Focus

- Current period values
- Comparative values
- Variance calculations
- Subtotals and control totals
- Aging buckets
- Cash movement versus bank or Round data
- Xero bank transactions are used for cash movement/reconciliation, not as P&L or balance-sheet evidence

## Final Artifact

`final/final.md`

## Blockers

- Missing Round account evidence.
- Unclear consolidation scope.
- Source period mismatch.
- `round_with_xero` requested but Round MCP does not expose usable Xero report, account, invoice, or bank-transaction data.
- Round cash and Round MCP Xero cash or bank-transaction evidence mismatch above materiality without a reconciliation note.
- Material variance explanation lacks supporting evidence when variance commentary is included.

## Full Review Rule

For full monthly review, connect Xero inside Round first. If the Round MCP Xero tools return data, produce P&L, balance sheet, cash movement, AR/AP or invoice context, risks, and actions. If Xero is connected in Xero but Round MCP cannot return usable Xero data, block the full accounting sections and tell the user to verify the Round-Xero connection. Do not ask for separate Xero MCP credentials in v1.

Round/Xero cash mismatches above materiality must block affected sections or be carried as an explicit reconciliation note in `source_ledger.json` and the final review.
