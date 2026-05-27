# CFO Anthropic Finance Agent Workflows

[![License](https://img.shields.io/badge/License-Apache%202.0%20%2B%20Commons%20Clause-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-111111.svg)](https://docs.anthropic.com/en/docs/claude-code)

Finance workflows for Claude that help CFOs and finance teams turn Round MCP data into board packs, monthly finance reviews, cash briefs, payment readiness packs, and forecast diagnostics. The plugin is designed to be useful even when only Round is connected: it starts with verified cash, account, currency, freshness, and bank-transaction evidence, then adds Xero accounting sections only when Xero is connected inside Round.

> **Important finance disclaimer**
>
> This plugin is not financial, accounting, tax, investment, audit, or legal advice. It does not approve payments, release payroll, move money, post journals, file accounts, or replace a qualified finance professional. It prepares evidence-backed drafts and workpapers for human review. AI Heroes is not affiliated with, endorsed by, or sponsored by Anthropic, Round, or Xero.

## Built By AI Heroes

This plugin is built by [AI Heroes](https://www.ai-heroes.co), a specialist AI implementation studio that builds practical Claude, Cowork, MCP, and workflow automation systems for operators, finance teams, agencies, and SMBs.

## Who This Is For

This is for people who want Claude to help with finance work without making up numbers:

| User | What it helps with |
|---|---|
| CFOs and finance directors | Fast cash summaries, board-ready narrative, risks, actions, and open questions. |
| Fractional CFOs | Repeatable finance packs across clients while preserving evidence discipline. |
| Founders and operators | A clearer view of cash, runway, and what needs human review. |
| Finance teams | Month-end commentary, payment readiness checks, and forecast diagnostic workpapers. |
| Board and investor prep teams | Cleaner liquidity stories with visible source limits. |

## What It Can Produce

| Workflow | Use it when you need | Default evidence |
|---|---|---|
| `/board-pack` | A board or investor pack with cash position, liquidity story, risks, and decisions. | Round accounts and bank transactions. |
| `/monthly-financial-review` | A month-end CFO memo explaining what changed and what needs action. | Round treasury review by default; full P&L and balance sheet only with Xero through Round. |
| `/cfo-cash-brief` | A same-day or weekly cash brief. | Round cash, account coverage, freshness, and supported movement. |
| `/payment-payroll-readiness` | A funding and control checklist before payments or payroll. | Round funding baseline; approval and release checks need user files or supported sources. |
| `/forecast-model-diagnostics` | A pressure test of runway, forecast assumptions, model outputs, and actuals tie-out. | Round cash baseline; model and accounting checks need supplied files or Xero through Round. |

## The Simple Version

1. Install the plugin in Claude Code or Claude Cowork.
2. Connect Round when Claude asks you to sign in.
3. Ask for a CFO pack, cash brief, monthly review, payment readiness check, or forecast diagnostic.
4. Claude creates a controlled draft.
5. The workflow blocks anything it cannot support with source evidence.

## How The Evidence Rules Work

The plugin uses three quality gates before a final artifact can be published:

| Gate | What it checks |
|---|---|
| Numerical QA | Every displayed number must tie to a source or formula and recompute cleanly. |
| Narrative Evaluation | Every claim must be supported by audited numbers or named source evidence. |
| CFO Quality Evaluation | The output must be useful, direct, CFO-ready, and disciplined about unsupported claims. |

If the workflow cannot prove a number, it removes the claim or blocks the affected section. That is the point of the plugin.

## Round And Xero

Round is the required connector.

Xero is optional. For full monthly review, connect Xero inside Round first. This plugin does **not** ask for separate Xero MCP credentials in v1.

| Mode | What it means |
|---|---|
| `round_only` | The default. Produces treasury-focused reviews from Round cash, account, currency, freshness, and transaction evidence. |
| `round_with_xero` | Adds P&L, balance sheet, invoice, account, and bank-transaction context when Round MCP exposes usable Xero data. |

Round MCP Xero bank transactions can support cash movement and reconciliation. They are not P&L or management-account evidence by themselves.

## Install In Claude Code

Use these commands inside Claude Code. This is a custom AI Heroes GitHub marketplace, not Anthropic's official marketplace.

```text
/plugin marketplace add mlobo2012/cfo-anthropic-finance-agent-workflows
/plugin install cfo-anthropic-finance-agent-workflows@ai-heroes-cfo-finance-agent-workflows
/reload-plugins
```

After install, try:

```text
/cfo-cash-brief "Acme Ltd" "May 2026" --currency GBP
```

The first Round-backed run may open a browser sign-in flow for Round MCP. Complete the sign-in, then return to Claude.

## Install In Claude Cowork Or Claude Desktop

1. Open this repository's **Releases** page.
2. Download `cfo-anthropic-finance-agent-workflows-claude-cowork-v1.0.0.zip`.
3. Open Claude Cowork or Claude Desktop.
4. Go to the plugin upload area.
5. Upload the zip file.
6. Start a new chat and ask for one of the finance workflows.

If you do not see a plugin upload option, update Claude Desktop or Claude Cowork first.

## First Useful Prompts

Copy one of these into Claude after installation:

```text
/cfo-cash-brief "Company name" "today" --currency GBP
```

```text
/monthly-financial-review "Company name" "May 2026" --currency GBP
```

```text
/board-pack "Company name" "May 2026" --currency GBP
```

```text
/payment-payroll-readiness "Company name" "2026-06-28" --currency GBP
```

```text
/forecast-model-diagnostics "Company name" "FY2026" --currency GBP
```

## Use Cases In Plain English

### 1. Board Pack

Use this when you need to explain the cash story to a board or investor group. The workflow can draft the liquidity position, movement, risks, and decisions needed. If you provide a PowerPoint template, the pack can respect locked and editable sections.

### 2. Monthly Financial Review

Use this after month end. With Round only, the workflow gives a treasury review. With Xero connected inside Round, it can add P&L, balance sheet, invoice, AR/AP, and close commentary.

### 3. CFO Cash Brief

Use this before a cash meeting. It tells you current cash, account coverage, freshness, visible movement, and decisions. It does not present runway unless the supporting movement or burn evidence exists.

### 4. Payment And Payroll Readiness

Use this before a payment or payroll run. It confirms the Round-visible funding baseline, then separates what is ready from what still needs human approval. It does not release money.

### 5. Forecast And Model Diagnostics

Use this before a runway number goes to the board. The workflow tests the Round cash baseline, then inspects model assumptions, actuals, formulas, and unresolved risks when files are supplied.

## What The Plugin Will Not Do

- It will not move money.
- It will not approve payments or payroll.
- It will not invent P&L or balance sheet values from bank transactions.
- It will not ask for separate Xero MCP credentials in v1.
- It will not publish a final artifact when numbers, claims, or source evidence do not pass the gates.

## MCP Connectors

The plugin ships with two MCP entries:

| MCP server | Purpose |
|---|---|
| `round-mcp` | Required live connector for Round MCP. |
| `cfo-quality-harness` | Local evidence harness that stores and validates workflow artifacts. |

Expected Round MCP tools include:

- `get_user_data`
- `get_accounts`
- `get_bank_transactions`
- `get_xero_profit_and_loss_report`
- `get_xero_balance_sheet_report`
- `get_xero_accounts`
- `get_xero_invoices`
- `get_xero_bank_transactions`

## File Structure

```text
.claude-plugin/
  plugin.json
  marketplace.json
.mcp.json
commands/
agents/
skills/
harness/
mcp/
workflows/
CONNECTORS.md
SETUP.md
```

## For Developers

You can validate the deterministic Round-only demo builder locally:

```bash
python3 mcp/round_only_artifact_builder.py --demo --output-root /tmp/cfo-round-demo
```

You can validate a generated run folder:

```bash
python3 mcp/cfo_quality_harness_server.py --validate-run /path/to/run
```

## Getting The Most Out Of This Plugin

If you need help with setup, want it customised to your firm's workflows, or just want to talk through what's possible — reach out to AI Heroes. We're building these tools to be as valuable as possible and your input drives that.

[Talk to AI Heroes](https://www.ai-heroes.co/contact)

## License

[Apache 2.0 + Commons Clause](LICENSE) - free for private and internal business use. Commercial resale is not permitted.
