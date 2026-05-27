---
name: payment-payroll-readiness
description: Payment and payroll readiness workflow with approvals, funding, duplicates, and cutoff checks.
---

# Payment + Payroll Readiness Workflow

Use this skill before reviewing supplier payments, payroll funding, or mixed payment runs. The out-of-box mode publishes a Round-only funding baseline from account and bank-transaction evidence. Payment files, payroll files, approvals, beneficiary changes, duplicate checks, and cutoffs are optional enrichment sources unless a future authenticated Round discovery exposes additional tools.

## Scope

The pack always includes a Round-only funding baseline and may include richer control checks when evidence is available:

- Round cash coverage baseline;
- Round transaction-window context;
- payment run summary, payroll funding summary, approval state, beneficiary and bank detail change risks, duplicate payment checks, cutoff and value date checks when source files or future tools are present;
- exceptions and hold recommendations.

## Required Contract Fields

`contract.json` must state:

- payment date and payroll date;
- `connector_mode`;
- entities and bank accounts in scope;
- currency;
- approval matrix when approval checks are in scope;
- payment file source when payment-file checks are in scope;
- payroll file source when payroll checks are in scope;
- duplicate detection policy when duplicate checks are in scope;
- beneficiary change lookback period when beneficiary checks are in scope;
- cutoff rules when cutoff checks are in scope;
- final action options.

## Execution

1. Register the run with workflow `payment_payroll_readiness`.
2. Write the contract and source ledger.
3. Fetch verified Round account and bank-transaction evidence, then ingest Round MCP Xero, payment run, payroll, approval, beneficiary, duplicate-check, and cutoff extracts when those checks are in scope.
4. Ask Workflow Planner for a readiness checklist and exception taxonomy.
5. Ask Generator Agent for `generator_output.md`.
6. Ask Numerical QA Agent to recompute payment totals, payroll totals, funding coverage, and duplicate checks.
7. Ask Narrative Evaluator Agent to check action wording, exception handling, and approval caveats.
8. Ask CFO Quality Evaluator Agent to score artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline.
9. Ask Final Controller to publish only when all required approvals and evaluator gates pass.

## Readiness Specific QA

The Numerical QA Agent must test:

- payment file total equals line item total and approval total;
- payroll funding total equals payroll source or declared payroll funding extract;
- available cash covers approved payments and payroll after restrictions;
- duplicate candidates are listed, cleared, or held;
- beneficiary changes are traced to source evidence;
- cutoff rules match bank or Round evidence;
- exception totals foot to the payment or payroll population.

If approval, payment-file, payroll, beneficiary-change, duplicate-check, or cutoff evidence is missing, the final pack must say those checks were not assessed. It is `BLOCKED` only if it attempts to publish a release, approval, duplicate-clearance, beneficiary-clearance, or cutoff claim without that evidence.
