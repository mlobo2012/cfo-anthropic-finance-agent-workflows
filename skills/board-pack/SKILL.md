---
name: board-pack
description: Board pack workflow with editable PPTX/POTX support and fail-closed finance QA.
---

# Board Pack Workflow

Use this skill for board decks, investor packs, finance committee packs, and monthly board updates.

## Scope

The board pack always includes a Round-only baseline and may include richer sections when evidence is available:

- executive summary from Round-visible cash/account evidence;
- cash and liquidity;
- account coverage and source freshness;
- bank-transaction movement when Round returns rows for the selected window;
- trading performance, working capital, forecast versus actual, risks, and decisions when Round MCP Xero data, model files, or user extracts are present;
- appendix workpapers; and
- editable PPTX output from a user `.pptx` or `.potx` template.

## Required Contract Fields

`contract.json` must state:

- board meeting date;
- `connector_mode`;
- reporting period and comparison periods;
- legal entities and consolidation scope;
- presentation currency and rounding policy;
- required sections and excluded sections;
- materiality threshold;
- Round MCP source requirements and optional enrichment sources;
- template path when applicable;
- locked slides and editable slides;
- final artifact format: `pptx`, `md`, or both.

## Execution

1. Register the run with workflow `board_pack`.
2. Write `contract.json`.
3. Save source extracts under `extracts/` and declare them in `source_ledger.json`.
4. Ask Workflow Planner to create a slide-by-slide production plan.
5. Ask Generator Agent to draft `generator_output.md` and, when requested, `generator_output.pptx`.
6. Ask Numerical QA Agent to recompute every displayed metric, KPI, variance, bridge, and cash figure.
7. Ask Narrative Evaluator Agent to check board-readiness, claim support, and unresolved caveats.
8. Ask CFO Quality Evaluator Agent to score artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline.
9. Ask Final Controller to publish only if all three evaluator gates are `PASS`.

## Board Pack Specific QA

The Numerical QA Agent must test:

- opening cash plus net cash movement equals closing cash;
- P&L variances match ledger or management accounts extracts when those sections are in scope;
- KPI definitions match the contract;
- bridge charts reconcile from start value to end value;
- any percentage point movement is not confused with percent movement;
- all FX translations state rate source and period;
- every slide number exists in `numerical_qa.displayed_numbers`.

## Template Rules

User templates belong in `templates/`. Do not overwrite the source template. Generated PPTX files are drafts until final approval. If no template or deck writer is available, publish the Round-only Markdown board pack and record PPTX as out of scope rather than blocking the baseline.
