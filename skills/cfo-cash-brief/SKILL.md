---
name: cfo-cash-brief
description: CFO cash brief workflow for liquidity, runway, commitments, and near-term actions.
---

# CFO Cash Brief Workflow

Use this skill for same-day or weekly cash briefs where CFOs need a concise decision pack.

## Scope

The brief always includes a Round-only cash baseline and may include richer sections when evidence is available:

- cash by bank, entity, and currency;
- available cash after restricted balances;
- bank-transaction movement when Round returns rows for the selected window;
- near-term payments and payroll from user-supplied extracts or verified future tools;
- expected collections from Round MCP Xero invoices, bank transactions, or user-supplied extracts;
- runway or liquidity headroom when transaction or burn evidence supports it;
- debt, covenant, or facility constraints from user-supplied extracts;
- immediate decisions.

## Required Contract Fields

`contract.json` must state:

- as-of date and time zone;
- `connector_mode`;
- cash freshness requirement;
- bank accounts and entities in scope;
- currency and FX policy;
- payment horizon;
- payroll horizon;
- runway definition when runway is requested;
- restricted cash treatment.

## Execution

1. Register the run with workflow `cfo_cash_brief`.
2. Write the contract and source ledger.
3. Fetch bounded Round account and bank-transaction evidence. Fetch relevant Round MCP Xero evidence and ingest user extracts only when those claims are in scope.
4. Ask Workflow Planner for a short decision-first brief structure.
5. Ask Generator Agent for `generator_output.md`.
6. Ask Numerical QA Agent to recompute cash, available cash, runway, and coverage figures.
7. Ask Narrative Evaluator Agent to check whether decisions follow from reconciled evidence.
8. Ask CFO Quality Evaluator Agent to score artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline.
9. Ask Final Controller to publish only after all gates `PASS`.

## Cash Brief Specific QA

The Numerical QA Agent must test:

- bank account balances tie to Round or bank extract as of the contract timestamp;
- restricted cash is excluded when the contract says it is unavailable;
- payment and payroll deductions are not double counted;
- expected collections are separated from confirmed cash;
- runway formulas declare burn basis and period;
- FX conversions state source rate and timestamp;
- liquidity headroom ties to facility and covenant source evidence when those claims are included.

If same-day Round cash data is stale, remove same-day wording or block the affected claim. Do not block the baseline for optional sources that are not in scope.
