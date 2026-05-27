# Shared Quality Harness

The harness defines the artifact contract that every CFO workflow must satisfy before a final output can be published.

Use the templates in `harness/templates/` when starting a run. Use the schemas in `harness/schemas/` for static checks. Use `mcp/cfo_quality_harness_server.py` for local MCP registration, artifact IO, and final validation.

## Files

- `contract.json`: scope, audience, entities, periods, currency, materiality, rounding, required sources, final artifact type.
- `source_ledger.json`: authoritative list of Round, Round MCP Xero, bank, payroll, spreadsheet, model, and template evidence.
- `generator_output.md` or `generator_output.pptx`: draft produced by the Generator Agent.
- `numerical_qa.json`: independent recomputation of every displayed number.
- `narrative_eval.json`: evaluator signoff on claims, caveats, and audience fit.
- `cfo_quality_eval.json`: external CFO quality signoff on artifact quality, decision usefulness, board/CFO tone, and unsupported-claim discipline.
- `revision_log.md`: append-only issue and fix history.
- `final/`: final artifacts only after all gates are `PASS`.

## Fail-Closed Standard

The harness is intentionally stricter than normal AI drafting:

- no source means no fact;
- no formula means no derived number;
- no period/entity/currency means no finance number;
- no independent recomputation means no publication;
- no evaluator signoff means no final artifact.
- no external CFO quality signoff means no final artifact.

The default production scope is `connector_mode: round_only`. A workflow may publish when every claim it makes is supported by Round MCP account, balance, freshness, and transaction evidence. `connector_mode: round_with_xero` requires usable Round MCP Xero reports, accounts, invoices, and bank transactions. Optional payment, payroll, model, or template evidence can enrich the artifact, but absence of those optional sources should narrow the published scope rather than force a failed out-of-box run.

## Local Validation

From the plugin root:

```bash
python3 mcp/cfo_quality_harness_server.py --validate-run /path/to/run
```

Validation returns JSON with `hard_status`, `issues`, and `summary`.

Generate deterministic Round-only artifacts:

```bash
python3 mcp/round_only_artifact_builder.py --demo --output-root /tmp/cfo-round-demo
```

Generate from exported Round MCP responses:

```bash
python3 mcp/round_only_artifact_builder.py \
  --accounts-json /path/to/get_accounts.json \
  --transactions-json /path/to/get_bank_transactions.json \
  --output-root /tmp/cfo-round-live \
  --entity "Round MCP company" \
  --period "May 2026" \
  --currency GBP
```
