---
name: cfo-quality-harness
description: Shared fail-closed operating model for Round MCP CFO workflows.
---

# CFO Quality Harness

This skill is mandatory for every workflow in this plugin.

## Core Rule

Reliability is the product feature. The default product path is a Round-only baseline that works out of the box from Round MCP account and transaction evidence. A final memo, board pack, cash brief, payment readiness pack, payroll readiness pack, or model diagnostic may only be published when the run artifacts prove:

- the workflow contract is explicit;
- the source ledger is complete for the requested scope;
- every displayed number is independently recomputed;
- unresolved numbers are disclosed in workpapers, not presented as fact;
- narrative claims are supported by audited numbers or source references; and
- external CFO quality review passes for artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline; and
- the Final Controller signs off.

If source evidence, formula lineage, freshness, or numeric reconciliation fails for a claim the artifact wants to publish, use `BLOCKED` for that claim and remove or correct it before final release. Use `REVISE` only for narrative, slide, template, or copy issues after every displayed number reconciles. If all published claims reconcile and evaluator signoff exists, use `PASS`.

Missing optional Xero, payment-file, payroll, model, or board-template evidence should narrow the artifact's scope, not block the Round-only baseline. Do not publish unsupported claims about omitted systems.

## Required Run Artifacts

Every run folder must contain:

```text
contract.json
source_ledger.json
generator_output.md or generator_output.pptx
numerical_qa.json
narrative_eval.json
cfo_quality_eval.json
revision_log.md
final/
```

Additional evidence belongs in:

```text
extracts/
workpapers/
templates/
```

## Agent Sequence

The main session orchestrates. Leaf agents do focused work only.

1. Workflow Planner: turns the user request into `contract.json`, source needs, artifact names, and gate criteria.
2. Generator Agent: drafts the memo, pack, brief, readiness pack, or diagnostic. It must tag every displayed number with a stable `number_id`.
3. Numerical QA Agent: independently recomputes every displayed number from Round MCP, Round MCP Xero tools, or source extracts and writes `numerical_qa.json`.
4. Narrative Evaluator Agent: checks claims, tone, audience fit, caveats, and whether every claim is supported.
5. CFO Quality Evaluator Agent: scores artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline in `cfo_quality_eval.json`.
6. Final Controller: reads all artifacts, validates hard statuses, writes final outputs only when gates pass.

Do not let the Generator Agent certify its own numbers. Do not let the Narrative Evaluator override numeric QA.

## Numeric Evidence Minimum

Each displayed number must have:

- `number_id`
- `label`
- `displayed_value`
- `normalised_value`
- `unit`
- `period`
- `entity`
- `currency` for monetary values
- `source_ref` or `formula`
- `source_value` or `component_values`
- `recomputed_value`
- `variance`
- `rounding.policy`
- `rounding.difference`
- `match_type`
- `status`

Allowed `match_type` values:

- `exact`
- `documented_rounding`
- `formula_recompute`

Do not use approximate agreement without a declared rounding policy. "Looks close" is `BLOCKED`.

## Status Rules

`PASS` requires all of the following:

- all required artifacts exist;
- all source entries required by the contract are `READY`;
- every displayed number is `PASS`;
- `unresolved_numbers` is empty;
- `narrative_eval.json` is `PASS`;
- `narrative_eval.evaluator.signed_off` is `true`; and
- `cfo_quality_eval.json` is `PASS`;
- `cfo_quality_eval.evaluator.signed_off` is `true`; and
- Final Controller writes a final artifact.

`REVISE` applies when:

- numerical QA is already `PASS`;
- the narrative, slide structure, template fidelity, or wording needs correction; and
- a correction can be made without new source access or changed finance numbers.

`BLOCKED` applies when:

- a source required for a displayed number is missing or stale;
- a number has no traceable source or formula;
- a formula cannot be recomputed;
- a displayed number does not reconcile exactly or by documented rounding;
- Round and Round MCP Xero evidence disagree beyond documented rounding and the difference is unresolved;
- the evaluator refuses signoff; or
- the user asks to publish despite unresolved evidence.

## Revision Loop

When a gate returns `REVISE`:

1. Write the issue to `revision_log.md`.
2. Send the draft back to the Generator Agent with exact required changes.
3. Rerun Numerical QA on changed numbers.
4. Rerun Narrative Evaluator on changed claims.
5. Do not final-publish from a previous pass after edits.

Use no more than three revision loops. If the Narrative Evaluator or CFO Quality Evaluator still returns `REVISE` after the third loop, set the run to `BLOCKED` and report the evaluator findings.

When a gate returns `BLOCKED`, stop and tell the user exactly which source, formula, or signoff is missing.

## Harness MCP Usage

Use `cfo-quality-harness` MCP tools from the main session:

- `register_run`
- `write_json_artifact`
- `write_text_artifact`
- `write_base64_artifact`
- `read_json_artifact`
- `read_text_artifact`
- `list_artifacts`
- `validate_run`

Cowork leaf agents should return concise summaries and artifact payloads for the main session to persist through MCP. Do not ask leaf agents to write arbitrary host paths directly.
