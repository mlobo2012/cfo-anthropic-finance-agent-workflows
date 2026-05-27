---
name: forecast-model-diagnostics
description: Forecast and model diagnostic workflow with source-traced drivers and formula checks.
---

# Forecast + Model Diagnostics Workflow

Use this skill to review forecasts, board models, lender models, covenant models, and operating plans.

## Scope

The diagnostic always includes a Round-only cash baseline and may include richer model sections when evidence is available:

- source data mapping;
- cash runway baseline from Round account and transaction evidence;
- model structure review, formula lineage, driver sanity checks, actuals versus forecast, and covenant sensitivity when a model and accounting evidence are present;
- unresolved model risks.

## Required Contract Fields

`contract.json` must state:

- model file path or source when model checks are requested;
- `connector_mode`;
- forecast periods;
- entities and segments in scope;
- currency and FX policy;
- actuals source, with Round as the default cash actuals source;
- key drivers;
- materiality threshold;
- tabs, sheets, or outputs to inspect;
- protected or excluded areas.

## Execution

1. Register the run with workflow `forecast_model_diagnostics`.
2. Write the contract and source ledger.
3. Save Round actuals and any supplied model evidence under `extracts/` or `workpapers/`.
4. Ask Workflow Planner for a model review plan and critical driver list.
5. Ask Generator Agent for `generator_output.md`.
6. Ask Numerical QA Agent to recompute driver outputs, formulas, forecast bridges, and variance calculations.
7. Ask Narrative Evaluator Agent to check whether diagnostic conclusions are supported.
8. Ask CFO Quality Evaluator Agent to score artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline.
9. Ask Final Controller to publish only after all critical model issues are classified and gates pass.

## Model Diagnostic Specific QA

The Numerical QA Agent must test:

- formulas are recomputed from declared inputs where accessible;
- actuals tie to Round MCP, Round MCP Xero evidence, or source extracts;
- forecast periods align with the contract;
- percentages and ratios state numerator and denominator;
- manual overrides are identified;
- circularity, hardcodes, broken references, and hidden rows are disclosed when detected;
- unresolved formula lineage is listed as a blocker for affected conclusions.

The workflow may publish a Round-only cash diagnostic without a model file. It may publish a diagnostic with unresolved model risks only if the final artifact clearly labels them as unresolved and does not present affected numbers as fact.
