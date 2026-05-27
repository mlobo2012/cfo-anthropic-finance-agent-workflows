# Run Artifact Tree

```text
runs/{run_id}/
  contract.json
  source_ledger.json
  generator_output.md
  generator_output.pptx
  numerical_qa.json
  narrative_eval.json
  cfo_quality_eval.json
  revision_log.md
  extracts/
    round/
    xero/
    bank/
    payroll/
    models/
  workpapers/
  templates/
  final/
```

`generator_output.md` and `generator_output.pptx` are alternatives unless the workflow contract requires both.

Only the Final Controller may write to `final/` after Numerical QA, Narrative Evaluation, and CFO Quality Evaluation all pass.
