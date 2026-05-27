# Workflow Template: CFO Cash Brief

## Contract Defaults

- `workflow`: `cfo_cash_brief`
- `connector_mode`: `round_only` by default; `round_with_xero` only when Round MCP exposes usable Xero data
- `output.audience`: `CFO`
- `output.artifact_type`: `md`
- Required sources: Round `get_accounts` for the out-of-box cash baseline. Round `get_bank_transactions` enriches movement and runway when rows are returned. Round MCP Xero evidence and user-supplied extracts for payments, payroll, collections, facilities, covenants, or commitments are optional enrichment sources when those claims are in scope.

## Required Sections

1. Cash position
2. Round transaction-window result
3. Liquidity headroom from Round-visible cash
4. Runway or coverage when transaction/burn evidence supports it
5. Decisions today
6. Optional items not assessed

## Numeric QA Focus

- As-of cash balance
- Restricted cash treatment
- Payment and payroll deductions from user-supplied extracts or verified future tools
- Confirmed versus expected receipts from Round MCP Xero invoices, bank transactions, or user extracts
- Runway formula
- FX rates

## Final Artifact

`final/final.md`

## Blockers

- Cash data stale beyond contract freshness.
- Missing bank or Round source for a material account.
- Missing user extract for payment, payroll, facility, covenant, commitment, or collection evidence only if the brief tries to claim those items.
- Runway formula not declared.
- Expected cash treated as confirmed cash.
