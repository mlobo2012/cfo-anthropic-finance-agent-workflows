# Setup

This plugin is designed for Claude Desktop, Claude Cowork, and Claude Code development runs.

## Prerequisites

- Python 3.10 or newer available as `python3` on `PATH`.
- Node.js and `npx` available on `PATH` for `mcp-remote`.
- Round user access approved for OAuth through the Round MCP server.
- For full monthly review, Xero connected inside Round first.
- Optional for editable deck generation: local presentation tooling such as Claude Presentations artifact support, `python-pptx`, or another approved PPTX writer. Without that tooling, board-pack runs should publish Markdown workpapers and treat PPTX generation as blocked.

## 1. Configure Round MCP

The bundled `.mcp.json` uses the real Round OAuth MCP server through `mcp-remote`.

Round server:

```text
https://mcp.roundtreasury.com/mcp
```

Exact command:

```bash
MCP_REMOTE_CONFIG_DIR="${HOME}/.config/cfo-anthropic-finance-agent-workflows/round-mcp-auth" \
  npx -y mcp-remote https://mcp.roundtreasury.com/mcp 3334 \
    --host 127.0.0.1 \
    --transport http-only \
    --auth-timeout 600
```

The bundled MCP server entry is:

```json
"command": "npx",
"args": [
  "-y",
  "mcp-remote",
  "https://mcp.roundtreasury.com/mcp",
  "3334",
  "--host",
  "127.0.0.1",
  "--transport",
  "http-only",
  "--auth-timeout",
  "600"
],
"env": {
  "MCP_REMOTE_CONFIG_DIR": "${HOME}/.config/cfo-anthropic-finance-agent-workflows/round-mcp-auth"
}
```

No Round API key environment variables are required for this connector. Authentication happens through the OAuth browser flow managed by `mcp-remote`. Do not configure separate Xero MCP credentials for v1.

The bundled `PATH` in `.mcp.json` includes common macOS and Linux binary locations so `npx` can be found by desktop runtimes. Adjust it locally if your Node.js install lives elsewhere.

Never commit or print auth material. This includes `.context/mcp-auth-round-fresh`, the `MCP_REMOTE_CONFIG_DIR` contents, code verifiers, access tokens, refresh tokens, callback URLs, consent URLs, screenshots of auth pages, and raw Round balances.

Minimum probe before production use:

1. Start the Round MCP server entry from `.mcp.json`.
2. Complete the OAuth browser flow.
3. Call `get_user_data`.
4. Call `get_accounts`.
5. Fetch Round accounts and one bounded bank-transaction window for a known period.
6. Save the minimal extract under `runs/{run_id}/extracts/` and register it in `source_ledger.json`.

Expected Round tools:

- `get_user_data`
- `get_accounts`
- `get_bank_transactions`
- `get_xero_profit_and_loss_report`
- `get_xero_balance_sheet_report`
- `get_xero_accounts`
- `get_xero_invoices`
- `get_xero_bank_transactions`

If OAuth returns `Invalid state parameter`, close stale auth tabs, restart a fresh `mcp-remote` client flow, keep the callback process alive until auth completes, and do not reuse old Clerk or OAuth links.

Xero report, invoice, account, and bank-transaction tools require an active Xero connection inside Round. Round direct feeds into Xero can keep Xero bank data current, but full CFO review still requires Round MCP access to Xero reports, invoices, accounts, and bank transactions.

The plugin's default `connector_mode` is `round_only`, so Xero errors should narrow the artifact scope rather than block a cash/account/transaction artifact. Use `connector_mode: round_with_xero` only when the Round MCP Xero tools return usable data. If the user explicitly asks for a full Xero-backed monthly review and Round MCP does not expose usable Xero data, block the full accounting sections and tell the user to verify the Round-Xero connection. Do not ask for separate Xero MCP credentials in v1.

Cash and payment-readiness workflows can publish a Round-only baseline from `get_accounts` alone. A successful `get_bank_transactions` call with zero rows is a factual result for that selected window; the artifact may state that no rows were returned, but it must not infer movement drivers, payment timing, collections, burn, or duplicate status from absent rows.

## 2. Install In Claude Desktop Or Cowork

From the plugin root:

```bash
zip -r ~/Downloads/cfo-anthropic-finance-agent-workflows-v1.0.0.zip \
  .claude-plugin .mcp.json commands agents skills harness workflows mcp \
  README.md CONNECTORS.md SETUP.md CHANGELOG.md LICENSE \
  -x "*.DS_Store" "*/__pycache__/*" "*.pyc" "tests/*"
```

Then upload the zip in Claude Desktop or Claude Cowork through the plugin upload flow.

The zip root must contain:

```text
.claude-plugin/plugin.json
.mcp.json
commands/
skills/
agents/
```

Do not zip a parent folder around the plugin.

## 3. Use In Claude Code

Claude Code can use the same command and skill files during development:

1. Open this plugin directory in the repository.
2. Read `README.md` and the workflow skill you want to test.
3. Run the local harness directly when needed:

```bash
python3 mcp/cfo_quality_harness_server.py --validate-run /path/to/run
```

Claude Code is useful for local smoke tests. Do not bypass the Cowork-safe artifact pattern when moving to Cowork.

## 4. Run Artifact Storage

Default harness data root:

```text
~/Library/Application Support/cfo-anthropic-finance-agent-workflows/v1
```

Development override:

```bash
export CFO_ROUND_PLUGIN_DATA_ROOT="/tmp/cfo-round-runs"
```

Each run uses:

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
  workpapers/
  templates/
  final/
```

## 5. User PPTX/POTX Board Templates

For board pack runs:

1. Put the source `.pptx` or `.potx` file in `runs/{run_id}/templates/`.
2. Record the filename in `contract.json.output.template_path`.
3. List locked slides or sections in `contract.json.output.locked_sections`.
4. List editable slides or sections in `contract.json.output.editable_sections`.
5. Keep the source template unchanged.
6. Write generated drafts as `generator_output.pptx`.
7. Move the final deck to `final/final.pptx` only after all gates pass.

Template evidence should include:

- template filename;
- template source owner;
- date received;
- known brand constraints;
- slides that must not be edited;
- required output filename.

## 6. Production Readiness Checklist

- Round MCP `mcp-remote` command, OAuth flow, and user access confirmed.
- Round-only artifact generation confirmed with account and bank-transaction evidence.
- Xero connected inside Round and Round MCP Xero tools confirmed when `round_with_xero` claims are requested.
- Harness MCP starts under Claude Desktop or Cowork.
- `register_run` creates a run folder.
- `validate_run` returns `PASS` for a complete Round-only baseline run.
- Incomplete or contradictory source-ledger runs still return `BLOCKED`.
- Final writes are blocked until pre-final validation passes.
- Numerical QA, Narrative Evaluation, and CFO Quality Evaluation all pass before publication.
- Board template rules are captured in `contract.json`.
