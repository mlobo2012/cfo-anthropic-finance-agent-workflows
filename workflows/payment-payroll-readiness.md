# Workflow Template: Payment + Payroll Readiness

## Contract Defaults

- `workflow`: `payment_payroll_readiness`
- `connector_mode`: `round_only` by default; `round_with_xero` only when Round MCP exposes usable Xero data
- `output.audience`: `Payments approver`
- `output.artifact_type`: `md`
- Required sources: Round `get_accounts` for the out-of-box funding baseline. Round `get_bank_transactions` enriches duplicate and timing context when rows are returned. Round MCP Xero invoice/bank evidence, payment file, approval matrix, beneficiary-change evidence, payroll funding file, duplicate-check workpaper, and cutoff evidence are optional enrichment sources when those checks are in scope.

## Required Sections

1. Readiness decision
2. Round-visible funding baseline
3. Transaction-window context
4. Optional approvals
5. Optional payment and payroll exceptions
6. Optional duplicate and beneficiary risk
7. Human review instructions

## Numeric QA Focus

- Payment file total
- Approved payment total
- Payroll funding total
- Available cash coverage
- Duplicate candidates
- Exception totals

## Final Artifact

`final/final.md`

## Blockers

- Round account evidence missing.
- Approval evidence missing when approval clearance is claimed.
- User-supplied payment, payroll, beneficiary-change, cutoff, or duplicate-check extract missing when those checks are claimed.
- Payment total does not equal line item total when payment files are in scope.
- Payroll source not available when payroll clearance is claimed.
- Beneficiary change evidence missing for changed payees when beneficiary clearance is claimed.
- Cash coverage is insufficient or unverified.
