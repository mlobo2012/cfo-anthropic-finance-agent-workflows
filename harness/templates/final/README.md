# Final Artifact Directory

Only the Final Controller may write here.

Allowed final outputs:

- `final.md`
- `final.pptx`
- `final.pdf`
- `final.json`
- workflow-specific supporting appendix files

Final publication requires:

- `contract.json.hard_status == "PASS"`
- `source_ledger.json` has no blocking source gaps
- `numerical_qa.json.hard_status == "PASS"`
- `numerical_qa.unresolved_numbers` is empty
- `narrative_eval.json.hard_status == "PASS"`
- `narrative_eval.evaluator.signed_off == true`
- `cfo_quality_eval.json.hard_status == "PASS"`
- `cfo_quality_eval.evaluator.signed_off == true`
- `revision_log.md` has no open material issue
