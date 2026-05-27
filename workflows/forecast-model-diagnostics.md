# Workflow Template: Forecast + Model Diagnostics

## Contract Defaults

- `workflow`: `forecast_model_diagnostics`
- `connector_mode`: `round_only` by default; `round_with_xero` only when Round MCP exposes usable Xero data
- `output.audience`: `CFO`
- `output.artifact_type`: `md`
- Required sources: Round `get_accounts` for the out-of-box cash diagnostic. Round `get_bank_transactions` enriches runway and movement checks when rows are returned. Forecast model, Round MCP Xero ledger evidence, driver source files, and scenario assumptions are optional enrichment sources when model diagnostics are requested.

## Required Sections

1. Diagnostic conclusion
2. Round cash actuals
3. Source data lineage
4. Cash runway baseline when transaction rows exist
5. Optional model structure, driver, formula, and integrity checks
6. Forecast versus actuals when model and accounting evidence exist
7. Unresolved model risks

## Numeric QA Focus

- Formula recomputation
- Driver inputs
- Actuals tie-out
- Forecast bridges
- Sensitivity outputs
- Hardcodes and overrides

## Final Artifact

`final/final.md`

## Blockers

- Round account evidence missing.
- Model file missing when model checks are requested.
- Formula lineage cannot be inspected for a material output when model checks are requested.
- Actuals do not tie to Round MCP, Round MCP Xero evidence, or source extracts.
- A critical driver has no source evidence when driver claims are included.
