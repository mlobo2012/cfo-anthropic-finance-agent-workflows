#!/usr/bin/env python3
import argparse
import base64
import datetime as dt
import json
import os
import platform
import re
import shutil
import sys
import uuid
from pathlib import Path


PLUGIN_NAME = "cfo-anthropic-finance-agent-workflows"
VALID_HARD_STATUSES = {"PASS", "REVISE", "BLOCKED"}
VALID_NUMERICAL_STATUSES = {"PASS", "BLOCKED"}
VALID_WORKFLOWS = {
    "board_pack",
    "monthly_financial_review",
    "cfo_cash_brief",
    "payment_payroll_readiness",
    "forecast_model_diagnostics",
}
NAMESPACES = {
    "root": "",
    "extracts": "extracts",
    "workpapers": "workpapers",
    "templates": "templates",
    "final": "final",
}
ROOT_JSON_FILES = {
    "contract.json",
    "source_ledger.json",
    "numerical_qa.json",
    "narrative_eval.json",
    "cfo_quality_eval.json",
}
ROOT_TEXT_FILES = {
    "generator_output.md",
    "revision_log.md",
}
ROOT_BINARY_FILES = {
    "generator_output.pptx",
}
REQUIRED_PREFINAL_FILES = [
    "contract.json",
    "source_ledger.json",
    "numerical_qa.json",
    "narrative_eval.json",
    "cfo_quality_eval.json",
    "revision_log.md",
]


class HarnessError(Exception):
    pass


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_data_root():
    override = os.environ.get("CFO_ROUND_PLUGIN_DATA_ROOT")
    if override:
        return Path(override).expanduser()
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / PLUGIN_NAME / "v1"
    if system == "Linux":
        return Path.home() / ".local" / "share" / PLUGIN_NAME / "v1"
    return Path.home() / f".{PLUGIN_NAME}" / "v1"


def slug(value):
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value).strip().lower())
    return value.strip("-") or "run"


def ensure_run_id(run_id):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id or ""):
        raise HarnessError("run_id contains unsupported characters")
    return run_id


def safe_join(base, relative_path):
    base = Path(base).resolve()
    target = (base / relative_path).resolve()
    if base != target and base not in target.parents:
        raise HarnessError("path traversal is not allowed")
    return target


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise HarnessError(f"missing JSON artifact: {path}")
    except json.JSONDecodeError as exc:
        raise HarnessError(f"invalid JSON artifact {path}: {exc}")


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_dir(data_root, run_id):
    return Path(data_root) / "runs" / ensure_run_id(run_id)


def load_template(plugin_root, name):
    path = Path(plugin_root) / "harness" / "templates" / name
    if name.endswith(".json"):
        return read_json(path)
    return path.read_text(encoding="utf-8")


def seed_run_templates(plugin_root, path, run_id, workflow, entity, period, currency):
    contract = load_template(plugin_root, "contract.json")
    contract["run_id"] = run_id
    contract["workflow"] = workflow
    contract["created_at"] = utc_now()
    if entity:
        contract["entity_scope"][0]["entity"] = entity
    if period:
        contract["period"]["primary"] = period
    if currency:
        contract["currency"]["presentation"] = currency
        contract["currency"]["source_currencies"] = [currency]
        contract["materiality"]["currency"] = currency
    write_json(path / "contract.json", contract)

    source_ledger = load_template(plugin_root, "source_ledger.json")
    source_ledger["run_id"] = run_id
    if entity:
        source_ledger["sources"][0]["entity"] = entity
    if period:
        source_ledger["sources"][0]["period"] = period
    if currency:
        source_ledger["sources"][0]["currency"] = currency
    write_json(path / "source_ledger.json", source_ledger)

    numerical_qa = load_template(plugin_root, "numerical_qa.json")
    numerical_qa["run_id"] = run_id
    if entity:
        numerical_qa["displayed_numbers"][0]["entity"] = entity
    if period:
        numerical_qa["displayed_numbers"][0]["period"] = period
    if currency:
        numerical_qa["displayed_numbers"][0]["currency"] = currency
    write_json(path / "numerical_qa.json", numerical_qa)

    narrative_eval = load_template(plugin_root, "narrative_eval.json")
    narrative_eval["run_id"] = run_id
    write_json(path / "narrative_eval.json", narrative_eval)

    cfo_quality_eval = load_template(plugin_root, "cfo_quality_eval.json")
    cfo_quality_eval["run_id"] = run_id
    write_json(path / "cfo_quality_eval.json", cfo_quality_eval)

    revision_log = load_template(plugin_root, "revision_log.md")
    revision_log = revision_log.replace("Run ID:", f"Run ID: {run_id}")
    revision_log = revision_log.replace("Workflow:", f"Workflow: {workflow}")
    write_text(path / "revision_log.md", revision_log)

    final_readme = Path(plugin_root) / "harness" / "templates" / "final" / "README.md"
    if final_readme.exists():
        shutil.copyfile(final_readme, path / "final" / "README.md")


class Harness:
    def __init__(self, plugin_root, data_root):
        self.plugin_root = Path(plugin_root).resolve()
        self.data_root = Path(data_root).expanduser().resolve()
        self.data_root.mkdir(parents=True, exist_ok=True)

    def register_run(self, arguments):
        workflow = arguments.get("workflow")
        if workflow not in VALID_WORKFLOWS:
            raise HarnessError(f"workflow must be one of: {', '.join(sorted(VALID_WORKFLOWS))}")
        entity = arguments.get("entity", "")
        period = arguments.get("period", "")
        currency = arguments.get("currency", "GBP")
        requested_by = arguments.get("requested_by", "")
        run_id = arguments.get("run_id") or f"{dt.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}-{slug(workflow)}-{uuid.uuid4().hex[:8]}"
        ensure_run_id(run_id)
        path = run_dir(self.data_root, run_id)
        if path.exists():
            raise HarnessError(f"run already exists: {run_id}")

        for child in ["extracts", "workpapers", "templates", "final"]:
            (path / child).mkdir(parents=True, exist_ok=True)
        for child in ["round", "xero", "bank", "payroll", "models"]:
            (path / "extracts" / child).mkdir(parents=True, exist_ok=True)

        seed_run_templates(self.plugin_root, path, run_id, workflow, entity, period, currency)

        state = {
            "run_id": run_id,
            "workflow": workflow,
            "entity": entity,
            "period": period,
            "currency": currency,
            "requested_by": requested_by,
            "created_at": utc_now(),
            "hard_status": "BLOCKED",
            "run_dir": str(path),
        }
        write_json(path / "state.json", state)
        return {
            "run_id": run_id,
            "run_dir": str(path),
            "state_path": str(path / "state.json"),
            "artifacts": self.artifact_paths(path),
        }

    def artifact_paths(self, path):
        return {
            "contract": str(path / "contract.json"),
            "source_ledger": str(path / "source_ledger.json"),
            "generator_output_md": str(path / "generator_output.md"),
            "generator_output_pptx": str(path / "generator_output.pptx"),
            "numerical_qa": str(path / "numerical_qa.json"),
            "narrative_eval": str(path / "narrative_eval.json"),
            "cfo_quality_eval": str(path / "cfo_quality_eval.json"),
            "revision_log": str(path / "revision_log.md"),
            "extracts": str(path / "extracts"),
            "workpapers": str(path / "workpapers"),
            "templates": str(path / "templates"),
            "final": str(path / "final"),
        }

    def artifact_path(self, run_id, namespace, relative_path):
        if namespace not in NAMESPACES:
            raise HarnessError(f"unknown namespace: {namespace}")
        base = run_dir(self.data_root, run_id)
        if not base.exists():
            raise HarnessError(f"unknown run_id: {run_id}")
        if namespace == "root":
            if relative_path not in ROOT_JSON_FILES | ROOT_TEXT_FILES | ROOT_BINARY_FILES | {"state.json"}:
                raise HarnessError("root namespace only allows declared run artifact files")
        target_base = base / NAMESPACES[namespace]
        return safe_join(target_base, relative_path)

    def write_json_artifact(self, arguments):
        run_id = arguments["run_id"]
        namespace = arguments.get("namespace", "root")
        relative_path = arguments["relative_path"]
        content = arguments["content"]
        if isinstance(content, str):
            content = json.loads(content)
        path = self.artifact_path(run_id, namespace, relative_path)
        if namespace == "final":
            self.require_prefinal_pass(run_id)
        write_json(path, content)
        return {"path": str(path), "bytes": path.stat().st_size}

    def read_json_artifact(self, arguments):
        path = self.artifact_path(arguments["run_id"], arguments.get("namespace", "root"), arguments["relative_path"])
        return {"path": str(path), "content": read_json(path)}

    def write_text_artifact(self, arguments):
        run_id = arguments["run_id"]
        namespace = arguments.get("namespace", "root")
        relative_path = arguments["relative_path"]
        content = arguments["content"]
        path = self.artifact_path(run_id, namespace, relative_path)
        if namespace == "final":
            self.require_prefinal_pass(run_id)
        write_text(path, content)
        return {"path": str(path), "bytes": path.stat().st_size}

    def write_base64_artifact(self, arguments):
        run_id = arguments["run_id"]
        namespace = arguments.get("namespace", "root")
        relative_path = arguments["relative_path"]
        content_base64 = arguments["content_base64"]
        path = self.artifact_path(run_id, namespace, relative_path)
        if namespace == "final":
            self.require_prefinal_pass(run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode(content_base64))
        return {"path": str(path), "bytes": path.stat().st_size}

    def read_text_artifact(self, arguments):
        path = self.artifact_path(arguments["run_id"], arguments.get("namespace", "root"), arguments["relative_path"])
        return {"path": str(path), "content": Path(path).read_text(encoding="utf-8")}

    def list_artifacts(self, arguments):
        run_id = arguments["run_id"]
        namespace = arguments.get("namespace", "root")
        base = self.artifact_path(run_id, namespace, ".") if namespace != "root" else run_dir(self.data_root, run_id)
        items = []
        for item in sorted(Path(base).rglob("*")):
            if item.is_file():
                items.append(str(item.relative_to(base)))
        return {"run_id": run_id, "namespace": namespace, "files": items}

    def validate_run(self, arguments):
        if "run_dir" in arguments and arguments["run_dir"]:
            path = Path(arguments["run_dir"]).expanduser().resolve()
        else:
            run_id = arguments.get("run_id")
            if not run_id:
                raise HarnessError("validate_run requires either run_dir or run_id")
            path = run_dir(self.data_root, run_id)
        phase = arguments.get("phase", "pre_final")
        require_final = phase == "post_final"
        return validate_run_dir(path, require_final=require_final)

    def require_prefinal_pass(self, run_id):
        result = validate_run_dir(run_dir(self.data_root, run_id), require_final=False)
        if result["hard_status"] != "PASS":
            raise HarnessError("final writes require PASS pre-final validation: " + "; ".join(result["issues"][:5]))


def add_issue(issues, status, message):
    issues.append({"status": status, "message": message})


def worst_status(issues):
    statuses = [issue["status"] for issue in issues]
    if "BLOCKED" in statuses:
        return "BLOCKED"
    if "REVISE" in statuses:
        return "REVISE"
    return "PASS"


def validate_required_number_fields(number):
    missing = []
    for field in ["number_id", "label", "displayed_value", "unit", "period", "entity", "recomputed_value", "variance", "rounding", "match_type", "status"]:
        if field not in number or number[field] in ("", None):
            missing.append(field)
    if not number.get("source_ref") and not number.get("formula"):
        missing.append("source_ref_or_formula")
    if number.get("unit") == "currency" and not number.get("currency"):
        missing.append("currency")
    rounding = number.get("rounding")
    if not isinstance(rounding, dict) or rounding.get("policy") in ("", None) or "difference" not in rounding:
        missing.append("rounding.policy_and_difference")
    return missing


def source_missing_fields(source):
    missing = []
    for field in [
        "source_ref",
        "system",
        "period",
        "entity",
        "currency",
        "extract_path",
        "source_hash_sha256",
        "source_as_of",
        "fetched_at",
    ]:
        if not source.get(field):
            missing.append(field)
    if "row_count" not in source or source.get("row_count") is None:
        missing.append("row_count")
    return missing


def revision_log_has_open_blocker(text):
    for line in text.splitlines():
        normalized = line.strip().upper()
        if normalized.startswith("| ISSUE") or normalized.startswith("| ---"):
            continue
        if ("| BLOCKED |" in normalized or "| REVISE |" in normalized) and "| TRUE |" in normalized:
            return True
    return False


def validate_run_dir(path, require_final=False):
    path = Path(path).expanduser().resolve()
    issues = []
    if not path.exists():
        return {
            "hard_status": "BLOCKED",
            "issues": [f"run directory does not exist: {path}"],
            "summary": {},
        }

    for name in REQUIRED_PREFINAL_FILES:
        if not (path / name).exists():
            add_issue(issues, "BLOCKED", f"missing required artifact: {name}")

    generator_md = path / "generator_output.md"
    generator_pptx = path / "generator_output.pptx"
    if not generator_md.exists() and not generator_pptx.exists():
        add_issue(issues, "REVISE", "missing generator output draft")

    parsed = {}
    for name in ROOT_JSON_FILES:
        file_path = path / name
        if file_path.exists():
            try:
                parsed[name] = read_json(file_path)
            except HarnessError as exc:
                add_issue(issues, "BLOCKED", str(exc))

    contract = parsed.get("contract.json", {})
    if contract.get("hard_status") != "PASS":
        add_issue(issues, contract.get("hard_status", "BLOCKED") if contract.get("hard_status") in VALID_HARD_STATUSES else "BLOCKED", "contract is not PASS")
    if contract.get("workflow") not in VALID_WORKFLOWS:
        add_issue(issues, "BLOCKED", "contract workflow is missing or unsupported")
    if contract.get("connector_mode") not in {"round_only", "round_with_xero"}:
        add_issue(issues, "BLOCKED", "contract connector_mode must be round_only or round_with_xero")
    quality_gates = contract.get("quality_gates", {})
    for gate in ["numerical_qa_required", "narrative_eval_required", "cfo_quality_eval_required", "final_controller_required"]:
        if quality_gates.get(gate) is not True:
            add_issue(issues, "BLOCKED", f"contract quality gate must be true: {gate}")
    max_revision_loops = quality_gates.get("max_revision_loops")
    if type(max_revision_loops) is not int or max_revision_loops > 3 or max_revision_loops < 0:
        add_issue(issues, "BLOCKED", "contract quality_gates.max_revision_loops must be an integer from 0 to 3")

    source_ledger = parsed.get("source_ledger.json", {})
    if source_ledger.get("hard_status") != "PASS":
        add_issue(issues, source_ledger.get("hard_status", "BLOCKED") if source_ledger.get("hard_status") in VALID_HARD_STATUSES else "BLOCKED", "source ledger is not PASS")
    for source in source_ledger.get("sources", []):
        if source.get("status") != "READY":
            add_issue(issues, "BLOCKED", f"source is not READY: {source.get('source_ref', '<missing source_ref>')}")
        missing_source_fields = source_missing_fields(source)
        if missing_source_fields:
            add_issue(issues, "BLOCKED", f"source missing fields: {source.get('source_ref', '<missing source_ref>')}: {', '.join(missing_source_fields)}")
    for gap in source_ledger.get("open_gaps", []):
        if gap.get("blocks_final"):
            add_issue(issues, "BLOCKED", f"blocking source gap: {gap.get('gap_id', '<missing gap_id>')}")

    numerical_qa = parsed.get("numerical_qa.json", {})
    if numerical_qa.get("hard_status") not in VALID_NUMERICAL_STATUSES:
        add_issue(issues, "BLOCKED", "numerical QA hard_status must be PASS or BLOCKED")
    if numerical_qa.get("hard_status") != "PASS":
        add_issue(issues, "BLOCKED", "numerical QA is not PASS")
    displayed_numbers = numerical_qa.get("displayed_numbers", [])
    if not displayed_numbers:
        add_issue(issues, "BLOCKED", "numerical QA has no displayed_numbers")
    source_refs = {source.get("source_ref") for source in source_ledger.get("sources", []) if source.get("source_ref")}
    for number in displayed_numbers:
        number_id = number.get("number_id", "<missing number_id>")
        missing = validate_required_number_fields(number)
        if missing:
            add_issue(issues, "BLOCKED", f"number {number_id} missing fields: {', '.join(missing)}")
        if number.get("status") != "PASS":
            add_issue(issues, "BLOCKED", f"number is not PASS: {number_id}")
        if number.get("status") not in VALID_NUMERICAL_STATUSES:
            add_issue(issues, "BLOCKED", f"number status must be PASS or BLOCKED: {number_id}")
        if number.get("source_ref") and number.get("source_ref") not in source_refs:
            add_issue(issues, "BLOCKED", f"number references unknown source_ref: {number_id}: {number.get('source_ref')}")
    if numerical_qa.get("unresolved_numbers"):
        add_issue(issues, "BLOCKED", "numerical QA has unresolved_numbers")

    narrative_eval = parsed.get("narrative_eval.json", {})
    if narrative_eval.get("hard_status") != "PASS":
        add_issue(issues, narrative_eval.get("hard_status", "BLOCKED") if narrative_eval.get("hard_status") in VALID_HARD_STATUSES else "BLOCKED", "narrative evaluation is not PASS")
    evaluator = narrative_eval.get("evaluator", {})
    if evaluator.get("signed_off") is not True:
        add_issue(issues, "BLOCKED", "narrative evaluator has not signed off")
    for claim in narrative_eval.get("claims", []):
        if claim.get("status") != "PASS":
            add_issue(issues, claim.get("status", "BLOCKED") if claim.get("status") in VALID_HARD_STATUSES else "BLOCKED", f"claim is not PASS: {claim.get('claim_id', '<missing claim_id>')}")

    cfo_quality_eval = parsed.get("cfo_quality_eval.json", {})
    if cfo_quality_eval.get("hard_status") != "PASS":
        add_issue(issues, cfo_quality_eval.get("hard_status", "BLOCKED") if cfo_quality_eval.get("hard_status") in VALID_HARD_STATUSES else "BLOCKED", "CFO quality evaluation is not PASS")
    cfo_evaluator = cfo_quality_eval.get("evaluator", {})
    if cfo_evaluator.get("signed_off") is not True:
        add_issue(issues, "BLOCKED", "CFO quality evaluator has not signed off")
    revision_loop = cfo_quality_eval.get("revision_loop")
    if type(revision_loop) is not int or revision_loop < 0 or revision_loop > 3:
        add_issue(issues, "BLOCKED", "CFO quality revision_loop must be an integer from 0 to 3")
    score_statuses = cfo_quality_eval.get("scores", {})
    for score_name in ["artifact_quality", "decision_usefulness", "board_cfo_tone", "unsupported_claim_discipline"]:
        score = score_statuses.get(score_name, {})
        if score.get("status") != "PASS":
            add_issue(issues, score.get("status", "BLOCKED") if score.get("status") in VALID_HARD_STATUSES else "BLOCKED", f"CFO quality score is not PASS: {score_name}")
        score_value = score.get("score")
        if type(score_value) is not int or score_value < 1 or score_value > 5:
            add_issue(issues, "BLOCKED", f"CFO quality score must be 1-5: {score_name}")
    for finding in cfo_quality_eval.get("findings", []):
        if finding.get("blocks_final") and finding.get("status") != "PASS":
            add_issue(issues, finding.get("status", "BLOCKED") if finding.get("status") in VALID_HARD_STATUSES else "BLOCKED", f"CFO quality finding blocks final: {finding.get('finding_id', '<missing finding_id>')}")

    revision_log = path / "revision_log.md"
    if revision_log.exists() and revision_log_has_open_blocker(revision_log.read_text(encoding="utf-8")):
        add_issue(issues, "BLOCKED", "revision_log.md has an open blocking issue")

    final_dir = path / "final"
    final_files = []
    if final_dir.exists():
        final_files = [str(item.relative_to(final_dir)) for item in final_dir.rglob("*") if item.is_file() and item.name != "README.md"]
    if require_final and not final_files:
        add_issue(issues, "BLOCKED", "post_final validation requires a final artifact")

    issue_messages = [issue["message"] for issue in issues]
    return {
        "hard_status": worst_status(issues),
        "issues": issue_messages,
        "summary": {
            "run_dir": str(path),
            "displayed_number_count": len(displayed_numbers),
            "final_file_count": len(final_files),
            "issue_count": len(issues),
        },
    }


def tool_definitions():
    return [
        {
            "name": "register_run",
            "description": "Create a CFO workflow run folder and seed required fail-closed artifacts.",
            "inputSchema": {
                "type": "object",
                "required": ["workflow"],
                "properties": {
                    "workflow": {"type": "string", "enum": sorted(VALID_WORKFLOWS)},
                    "entity": {"type": "string"},
                    "period": {"type": "string"},
                    "currency": {"type": "string", "default": "GBP"},
                    "requested_by": {"type": "string"},
                    "run_id": {"type": "string"},
                },
            },
        },
        {
            "name": "write_json_artifact",
            "description": "Write a JSON artifact inside a run namespace.",
            "inputSchema": artifact_write_schema("object"),
        },
        {
            "name": "read_json_artifact",
            "description": "Read a JSON artifact from a run namespace.",
            "inputSchema": artifact_read_schema(),
        },
        {
            "name": "write_text_artifact",
            "description": "Write a text artifact inside a run namespace.",
            "inputSchema": artifact_write_schema("string"),
        },
        {
            "name": "read_text_artifact",
            "description": "Read a text artifact from a run namespace.",
            "inputSchema": artifact_read_schema(),
        },
        {
            "name": "write_base64_artifact",
            "description": "Write a binary artifact, such as a PPTX or POTX, from base64 content.",
            "inputSchema": {
                "type": "object",
                "required": ["run_id", "relative_path", "content_base64"],
                "properties": {
                    "run_id": {"type": "string"},
                    "namespace": {"type": "string", "enum": sorted(NAMESPACES), "default": "root"},
                    "relative_path": {"type": "string"},
                    "content_base64": {"type": "string"},
                },
            },
        },
        {
            "name": "list_artifacts",
            "description": "List files for a run namespace.",
            "inputSchema": {
                "type": "object",
                "required": ["run_id"],
                "properties": {
                    "run_id": {"type": "string"},
                    "namespace": {"type": "string", "enum": sorted(NAMESPACES), "default": "root"},
                },
            },
        },
        {
            "name": "validate_run",
            "description": "Validate a CFO workflow run folder against fail-closed finalization rules.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "run_id": {"type": "string"},
                    "run_dir": {"type": "string"},
                    "phase": {"type": "string", "enum": ["pre_final", "post_final"], "default": "pre_final"},
                },
            },
        },
    ]


def artifact_read_schema():
    return {
        "type": "object",
        "required": ["run_id", "relative_path"],
        "properties": {
            "run_id": {"type": "string"},
            "namespace": {"type": "string", "enum": sorted(NAMESPACES), "default": "root"},
            "relative_path": {"type": "string"},
        },
    }


def artifact_write_schema(content_type):
    return {
        "type": "object",
        "required": ["run_id", "relative_path", "content"],
        "properties": {
            "run_id": {"type": "string"},
            "namespace": {"type": "string", "enum": sorted(NAMESPACES), "default": "root"},
            "relative_path": {"type": "string"},
            "content": {"type": content_type},
        },
    }


class McpServer:
    def __init__(self, harness):
        self.harness = harness

    def handle(self, request):
        method = request.get("method")
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "cfo-quality-harness", "version": "0.1.0"},
            }
        if method == "tools/list":
            return {"tools": tool_definitions()}
        if method == "tools/call":
            params = request.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments") or {}
            result = self.call_tool(name, arguments)
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2, sort_keys=True)}],
                "structuredContent": result,
            }
        raise HarnessError(f"unsupported method: {method}")

    def call_tool(self, name, arguments):
        tools = {
            "register_run": self.harness.register_run,
            "write_json_artifact": self.harness.write_json_artifact,
            "read_json_artifact": self.harness.read_json_artifact,
            "write_text_artifact": self.harness.write_text_artifact,
            "read_text_artifact": self.harness.read_text_artifact,
            "write_base64_artifact": self.harness.write_base64_artifact,
            "list_artifacts": self.harness.list_artifacts,
            "validate_run": self.harness.validate_run,
        }
        if name not in tools:
            raise HarnessError(f"unknown tool: {name}")
        return tools[name](arguments)


def run_stdio(server):
    for line in sys.stdin:
        if not line.strip():
            continue
        response_id = None
        try:
            request = json.loads(line)
            response_id = request.get("id")
            if request.get("method", "").startswith("notifications/"):
                continue
            result = server.handle(request)
            if response_id is not None:
                send({"jsonrpc": "2.0", "id": response_id, "result": result})
        except Exception as exc:
            if response_id is not None:
                send({
                    "jsonrpc": "2.0",
                    "id": response_id,
                    "error": {"code": -32000, "message": str(exc)},
                })


def send(payload):
    sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="CFO quality harness MCP server")
    parser.add_argument("--plugin-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--data-root", default=str(default_data_root()))
    parser.add_argument("--validate-run")
    parser.add_argument("--phase", default="pre_final", choices=["pre_final", "post_final"])
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.validate_run:
        result = validate_run_dir(args.validate_run, require_final=args.phase == "post_final")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["hard_status"] == "PASS" else 1
    harness = Harness(args.plugin_root, args.data_root)
    run_stdio(McpServer(harness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
