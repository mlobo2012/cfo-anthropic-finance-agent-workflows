# CFO Quality Harness MCP

`cfo_quality_harness_server.py` is a no-dependency local stdio MCP server for Claude Desktop and Cowork.

It owns host-side run artifact persistence:

- `register_run`
- `write_json_artifact`
- `read_json_artifact`
- `write_text_artifact`
- `read_text_artifact`
- `write_base64_artifact`
- `list_artifacts`
- `validate_run`

Default data root:

- macOS: `~/Library/Application Support/cfo-anthropic-finance-agent-workflows/v1`
- Linux: `~/.local/share/cfo-anthropic-finance-agent-workflows/v1`
- Other platforms: `~/.cfo-anthropic-finance-agent-workflows/v1`

Override for development:

```bash
CFO_ROUND_PLUGIN_DATA_ROOT=/tmp/cfo-round-runs python3 mcp/cfo_quality_harness_server.py --validate-run /tmp/cfo-round-runs/runs/example
```

The server deliberately blocks writes to `final/` unless `validate_run` would return `PASS` before the final artifact is written. A pre-final `PASS` requires `contract.json`, `source_ledger.json`, `numerical_qa.json`, `narrative_eval.json`, `cfo_quality_eval.json`, and `revision_log.md` to pass.

`round_only_artifact_builder.py` is the deterministic Round-only baseline generator. It is used for smoke tests, demo artifacts, and local validation from exported Round MCP responses:

```bash
python3 mcp/round_only_artifact_builder.py --demo --output-root /tmp/cfo-round-demo
```

For live validation, pass actual Round MCP response files:

```bash
python3 mcp/round_only_artifact_builder.py \
  --accounts-json /path/to/get_accounts.json \
  --transactions-json /path/to/get_bank_transactions.json \
  --output-root /tmp/cfo-round-live \
  --entity "Round MCP company" \
  --period "May 2026"
```
