# Connectors

This plugin expects one required connector class and optional enrichment sources:

- Required: Round MCP for live finance workflow data.
- Optional: Xero evidence exposed through Round MCP, plus ledger, bank, payroll, board-template, and model evidence when the user asks for claims beyond Round-visible cash/account/transaction data.

Do not add official Xero MCP to `.mcp.json` for v1. Direct Xero MCP is a documented future fallback only if Round's Xero tool coverage is insufficient.

The quality harness treats connectors as evidence providers, not as final authorities. A connector result becomes usable only after it is written to `source_ledger.json` with period, entity, currency, extract path, hash, row count, and reconciliation status. Missing optional connectors narrow the final artifact scope; they do not block the Round-only baseline.

## Round MCP

`.mcp.json` includes the real Round OAuth MCP bridge through `mcp-remote`.

Round server:

```text
https://mcp.roundtreasury.com/mcp
```

MCP server configuration:

```json
{
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
}
```

Equivalent shell command:

```bash
MCP_REMOTE_CONFIG_DIR="${HOME}/.config/cfo-anthropic-finance-agent-workflows/round-mcp-auth" \
  npx -y mcp-remote https://mcp.roundtreasury.com/mcp 3334 \
    --host 127.0.0.1 \
    --transport http-only \
    --auth-timeout 600
```

Round authentication is OAuth-based. Do not configure `ROUND_API_KEY`, `ROUND_TENANT_ID`, `XERO_TENANT_ID`, Xero client credentials, or a separate Round base URL for this connector.

The auth cache is intentionally outside the plugin package:

```bash
export MCP_REMOTE_CONFIG_DIR="${HOME}/.config/cfo-anthropic-finance-agent-workflows/round-mcp-auth"
```

Do not commit, paste, print, screenshot, or upload any auth cache, callback URL, consent URL, code verifier, access token, refresh token, or raw Round balance. In this workspace, never commit or print anything from `.context/mcp-auth-round-fresh`.

Recommended operational probe after OAuth completes:

1. Call `get_user_data`.
2. Call `get_accounts`.
3. Fetch one bounded, low-volume finance dataset such as `get_bank_transactions` for a narrow period or a small Xero report.
4. Save only the minimal extract needed under `runs/{run_id}/extracts/`.
5. Register the extract in `source_ledger.json` with freshness, period, entity, currency, row count, and reconciliation status.

Do not use a large context dump, raw balance dump, screenshot, consent URL, or callback URL as a health check.

If the OAuth browser flow shows `Invalid state parameter`, close stale auth tabs, restart a fresh `mcp-remote` client flow, keep the callback process alive until auth completes, and do not reuse old Clerk or OAuth links.

## Expected Round Tool Coverage

The Round MCP server is expected to expose these exact tools:

- `get_user_data`
- `get_accounts`
- `get_bank_transactions`
- `get_xero_profit_and_loss_report`
- `get_xero_balance_sheet_report`
- `get_xero_accounts`
- `get_xero_invoices`
- `get_xero_bank_transactions`

Map these tools to the workflow evidence needs:

- Account and cash-position evidence by entity, account, date, and currency. This is the minimum required source for the out-of-box baseline.
- Bank transactions and movement evidence. Zero returned rows are valid evidence that no rows were returned for the selected window, but not evidence of payment coverage, collections, burn, or duplicate status.
- Payment run state, approvals, beneficiary changes, payroll funding, duplicate risks, cutoff metadata, treasury commitments, debt, covenant, and facility data only when supplied as user extracts or exposed by future authenticated tool discovery.
- Accounts receivable and accounts payable aging when Xero or an accounting extract is available.
- Xero P&L, balance sheet, accounts, invoices, bank transactions, and tracking context through Round MCP when the user asks for accounting-backed sections.
- Audit metadata: fetched_at, source system id, tenant id, row count, and immutable extract identifier where available.

Do not treat Round MCP Xero bank transactions as P&L, balance-sheet, or management-account evidence. They support cash movement and reconciliation only unless the relevant Xero report/accounting source is also present.

The verified Round MCP tool list does not currently include live payment approval, payroll, beneficiary-change, debt, covenant, or facility tools. Those evidence needs are optional enrichments. If absent, the final artifact must state that the relevant checks were not assessed and must not publish approval, release, payroll, beneficiary-clearance, duplicate-clearance, covenant, debt, or facility claims as fact.

The Xero tools require an active Xero connection in Round. For full monthly review, connect Xero inside Round first. Round direct feeds into Xero help keep Xero bank data current, but full CFO review still requires Round MCP access to Xero reports, accounts, invoices, and bank transactions.

If `get_xero_profit_and_loss_report`, `get_xero_balance_sheet_report`, `get_xero_accounts`, `get_xero_invoices`, or `get_xero_bank_transactions` returns usable data for the connected company, `connector_mode: round_with_xero` may produce full P&L, balance sheet, cash movement, AR/AP or invoice context, risks, and actions. If Xero is connected in Xero but Round MCP does not expose usable Xero data, block the full accounting review and tell the user to verify the Round-Xero connection. Do not ask for separate Xero MCP credentials in v1.

In the default `connector_mode: round_only` baseline, omit the Xero-backed section and publish only supported Round claims. If the contract explicitly requires Xero-backed claims, record the tool result as `UNRESOLVED` and block those unsupported claims from final publication.

A successful `get_bank_transactions` call with zero rows proves only that the connector returned no transactions for the requested account/window. It does not prove cash movement, payment coverage, collections, or payroll readiness.

## Xero And Ledger Extracts

Acceptable Xero evidence in v1:

- Xero data returned through Round MCP.
- Xero exports saved under `extracts/`.

Direct Xero MCP results are not part of the v1 packaged connector path. Treat direct Xero MCP only as a future fallback outside this build.

Each source entry must state:

- `system`: `Xero`, `Round`, `Bank`, `Payroll`, `Spreadsheet`, or another named system.
- `source_ref`: stable identifier used by numeric assertions.
- `period`: close month, forecast period, payment date, or payroll date.
- `entity`: legal entity or group.
- `currency`: source currency.
- `extract_path`: path inside the run folder.
- `source_hash_sha256`: hash of the saved extract when file based.
- `source_as_of`: source-system as-of timestamp or snapshot timestamp.
- `fetched_at`: timestamp when the connector or extract was read.
- `row_count`: number of source rows or records.
- `status`: `READY`, `PARTIAL`, or `UNRESOLVED`.

## User-Supplied Files

User files are allowed, but must be treated as source evidence with explicit provenance:

- Board templates: `.pptx` or `.potx` in `templates/`.
- Trial balances, GL dumps, and working papers: `extracts/`.
- Forecast models: `extracts/` or `workpapers/`.
- Payroll files and bank files: `extracts/` with access controls outside the plugin.

Do not paste sensitive payroll or bank data into visible final artifacts unless the contract explicitly requires it and the evaluator signs off.

## Connector Failure Policy

- Missing required Round account connector: `BLOCKED`.
- Optional connector unavailable: omit dependent claims and record the scope limit.
- Connector reachable but period unavailable: omit dependent claims unless the contract explicitly requires them.
- Connector result conflicts with another source: `BLOCKED` for affected claims until the mismatch is investigated and a reconciled source ledger is written.
- Round/Xero cash mismatch above contract materiality: `BLOCKED` for full-review cash/accounting sections unless the source ledger records a reconciliation note and the final artifact names the mismatch.
- Connector result has no period, entity, or currency metadata for a displayed number: `BLOCKED` for that number.
- Connector result is stale relative to contract freshness rules for a displayed number: `BLOCKED` for that number.
