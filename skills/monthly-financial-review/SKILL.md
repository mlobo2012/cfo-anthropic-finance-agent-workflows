---
name: monthly-financial-review
description: Monthly finance review workflow with reconciled management accounts and commentary.
---

# Monthly Financial Review Workflow

Use this skill for month-end review memos, management accounts commentary, and CFO review packs.

## Scope

The review always includes a Round-only treasury baseline. The contract must declare one connector mode:

- `round_only`: default treasury review from Round MCP accounts and bank transactions.
- `round_with_xero`: full monthly review using Xero evidence exposed through Round MCP.

Full monthly review requires Xero to be connected inside Round first. Do not ask for separate Xero MCP credentials in v1.

The review may include:

- Round cash position, account coverage, currency coverage, and freshness;
- Round bank-transaction movement when rows are returned for the selected window;
- P&L performance, gross margin, cost movement, balance sheet movement, AR/AP or invoice context, working capital, covenant, or board KPI metrics when Round MCP Xero tools or user extracts are present;
- risks, actions, and open close items.

Round MCP Xero bank transactions can support cash movement and reconciliation. They are not P&L or management-account evidence by themselves.

## Required Contract Fields

`contract.json` must state:

- close month;
- `connector_mode`;
- comparison periods;
- entity and consolidation scope;
- management reporting currency;
- rounding policy;
- materiality threshold for variance commentary;
- required Round source systems and optional enrichment sources;
- close cutoff date and freshness rule;
- output audience.

## Execution

1. Register the run with workflow `monthly_financial_review`.
2. Build the contract and source ledger before drafting.
3. Fetch or ingest Round data first. If `connector_mode` is `round_with_xero`, fetch Xero reports, accounts, invoices, and bank transactions through Round MCP.
4. Ask Workflow Planner for a review outline and source map.
5. Ask Generator Agent for `generator_output.md`.
6. Ask Numerical QA Agent to recompute P&L, balance sheet, cash, working capital, and KPI numbers.
7. Ask Narrative Evaluator Agent to challenge all causal claims and action recommendations.
8. Ask Final Controller to write the final review only after `PASS`.

## Monthly Review Specific QA

The Numerical QA Agent must test:

- current period values match the declared Round or ledger extract;
- comparative values use the correct prior month, prior quarter, or prior year;
- all variances calculate from the normalised values, not displayed rounded values;
- subtotal relationships foot and cross-foot;
- percentages state numerator and denominator;
- cash movement ties to bank or Round cash evidence;
- Round cash and Round MCP Xero bank/cash balances reconcile within contract materiality when both are included;
- working capital aging buckets foot to the relevant control total when working capital is in scope.

Unsupported variance explanations are omitted from a Round-only baseline. They are narrative failures only if the artifact tries to publish them as fact.

## Round-Xero Failure Rule

If `round_with_xero` is requested and the Round MCP Xero tools return usable data, produce the full monthly review with P&L, balance sheet, cash movement, AR/AP or invoice context, risks, and actions.

If Xero is connected in Xero but Round MCP does not expose usable Xero data, block the full accounting review and tell the user to verify the Round-Xero connection. Do not request direct Xero MCP credentials in v1.

If Round cash and Round MCP Xero cash or bank-transaction evidence disagree above materiality, block the affected full-review sections unless the source ledger includes a clear reconciliation note and the final artifact names the mismatch.
