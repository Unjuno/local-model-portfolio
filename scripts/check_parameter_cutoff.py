#!/usr/bin/env python3
"""Read-only v12 portfolio audit: 150B baseline + measured quantized exceptions.

Python >=3.10, standard library only; never downloads weights or runs models.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 150_000_000_000
PEAK_LIMIT = 512_000_000_000
LOW = "PASS_TOTAL_PARAMS_LT_150B"
UNKNOWN = "UNVERIFIED_BLOCK_FINAL_LOCK"
REVIEW = "OVER_150B_QUANT_REVIEW_REQUIRED"
VERIFIED = "OVER_150B_QUANT_RUNTIME_VERIFIED"


def load_json(root: Path, relative: str) -> dict[str, Any]:
    if not isinstance(relative, str) or not relative:
        raise ValueError("missing path")
    clean = relative.replace("\\", "/")
    parts = Path(clean).parts
    if Path(clean).is_absolute() or ".." in parts or clean.startswith("/") or ":" in clean:
        raise ValueError(f"unsafe path: {relative!r}")
    target = (root / clean).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"outside repository: {relative}")
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {relative}")
    return data


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def verified_quant_exception(item: dict[str, Any], peak_limit: int = PEAK_LIMIT) -> bool:
    q = item.get("quantized_exception")
    if not isinstance(q, dict) or q.get("status") != "VERIFIED":
        return False
    required_text = ("quantized_repo_id", "source_url", "source_revision_sha",
                     "backend_and_version", "hardware_record", "quantization_variant")
    if any(not isinstance(q.get(k), str) or not q[k].strip() for k in required_text):
        return False
    if not re.fullmatch(r"[0-9a-f]{40}", q["source_revision_sha"]):
        return False
    integers = ("total_model_parameters", "complete_selected_file_bytes",
                "measured_peak_host_ram_plus_vram_bytes", "context_tokens",
                "batch_size", "throughput_trials", "independent_quality_n")
    if any(not is_int(q.get(k)) or q[k] <= 0 for k in integers):
        return False
    if q["total_model_parameters"] != item.get("parameter_gate", {}).get("total_parameters"):
        return False
    if q["measured_peak_host_ram_plus_vram_bytes"] >= peak_limit:
        return False
    if q["throughput_trials"] < 30 or q["independent_quality_n"] < 30:
        return False
    if not isinstance(q.get("throughput_median_tokens_per_second"), (int, float)) or isinstance(q.get("throughput_median_tokens_per_second"), bool):
        return False
    if not isinstance(q.get("minimum_acceptable_tokens_per_second"), (int, float)) or isinstance(q.get("minimum_acceptable_tokens_per_second"), bool):
        return False
    if q["minimum_acceptable_tokens_per_second"] <= 0 or q["throughput_median_tokens_per_second"] < q["minimum_acceptable_tokens_per_second"]:
        return False
    checks = ("measured_user_hardware", "task_quality_pass", "license_text_reviewed",
              "dependencies_reviewed", "personal_gated_access_verified")
    if any(q.get(k) is not True for k in checks):
        return False
    return True


def validate_model(item: dict[str, Any], threshold: int = BASELINE) -> list[str]:
    errors: list[str] = []
    g = item.get("parameter_gate") or {}
    n, status = g.get("total_parameters"), g.get("status")
    rid = item.get("repo_id", "unknown")
    active = item.get("portfolio_decision") in ("select", "conditional")
    if not is_int(threshold) or threshold <= 0:
        raise ValueError("invalid baseline")
    if n is None:
        if status != UNKNOWN:
            errors.append(f"{rid}: unknown total must block acquisition")
        if active:
            errors.append(f"{rid}: unknown total cannot be active")
        return errors
    if not is_int(n) or n < 0:
        return [f"{rid}: invalid total parameters"]
    if n < threshold:
        if status != LOW:
            errors.append(f"{rid}: below baseline needs {LOW}")
    else:
        if status not in (REVIEW, VERIFIED):
            errors.append(f"{rid}: >=150B needs explicit quantized review/verified gate")
        if status == REVIEW and active:
            errors.append(f"{rid}: review-only oversized source cannot be active")
        if status == VERIFIED and not verified_quant_exception(item):
            errors.append(f"{rid}: oversized runtime exception evidence incomplete")
        if active and status != VERIFIED:
            errors.append(f"{rid}: oversized active without verified exception")
    return errors


def audit(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    policy = load_json(root, "policies/limits.json")
    rule = policy.get("total_parameter_policy") or {}
    if rule.get("baseline_model_total_parameters") != BASELINE:
        return ["baseline must be 150B"]
    if rule.get("mode") != "BASELINE_WITH_QUANTIZED_RUNTIME_EXCEPTION":
        return ["quantized exception mode absent"]
    if rule.get("hard_peak_ram_bytes_exclusive") != PEAK_LIMIT:
        return ["peak RAM limit must be <512e9 byte"]
    current = load_json(root, "catalog/CURRENT.json")
    portfolio = load_json(root, current["materialized_catalog_path"])
    items = portfolio.get("items")
    if not isinstance(items, list):
        return ["missing items"]
    ids: set[tuple[str, str]] = set()
    models: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            errors.append("non-object portfolio entry")
            continue
        kind, rid = item.get("asset_kind"), item.get("repo_id")
        if not isinstance(kind, str) or not isinstance(rid, str):
            errors.append("missing kind/repo ID")
            continue
        key = (kind.lower(), rid.lower())
        if key in ids:
            errors.append(f"duplicate: {key}")
        ids.add(key)
        if kind == "model":
            errors.extend(validate_model(item))
            models[rid.lower()] = item
        elif kind == "dataset":
            if item.get("parameter_gate", {}).get("status") != "NOT_APPLICABLE_TO_DATASET":
                errors.append(f"dataset gate invalid: {rid}")
        else:
            errors.append(f"unexpected type: {rid}")
    expected = current.get("expected") or {}
    if len(items) != expected.get("tracked"):
        errors.append("asset count mismatch")
    if portfolio.get("revision_id") != current.get("revision_id"):
        errors.append("materialization revision mismatch")
    active = [i for i in items if i.get("portfolio_decision") in ("select", "conditional")]
    if len(active) != expected.get("active"):
        errors.append("active count mismatch")
    from collections import Counter
    counts = Counter(i.get("portfolio_decision") for i in items)
    for k, n in (expected.get("by_decision") or {}).items():
        if counts[k] != n:
            errors.append(f"decision {k} mismatch")
    statuses = Counter(i.get("parameter_gate", {}).get("status") for i in items if i.get("asset_kind") == "model")
    for k, n in (expected.get("parameter_gate") or {}).items():
        if statuses[k] != n:
            errors.append(f"gate {k} mismatch")
    qpath = current.get("priority_worklist_path")
    queue = load_json(root, qpath)
    if queue.get("source_revision") != current.get("revision_id") or queue.get("approved") is not False or queue.get("download_enabled") is not False:
        errors.append("queue revision or authorization incorrect")
    candidates = queue.get("candidates")
    if not isinstance(candidates, list):
        errors.append("queue candidate list absent")
    else:
        active_ids = {(i.get("asset_kind"), i.get("repo_id")) for i in active}
        candidate_ids = {(i.get("asset_kind"), i.get("repo_id")) for i in candidates}
        if active_ids != candidate_ids or len(candidates) != len(active):
            errors.append("queue must exactly match active selection")
        if any(c.get("download_approved") is not False or c.get("not_authorized") is not True for c in candidates):
            errors.append("queue item accidentally authorized")
    if len(queue.get("over_baseline_quantized_research") or []) != statuses[REVIEW]:
        errors.append("oversized quantized research list mismatch")
    approved = load_json(root, "queues/approved.json")
    entries = approved.get("entries")
    if not isinstance(entries, list):
        return errors + ["approved queue invalid"]
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("malformed approved entry")
            continue
        path = entry.get("manifest_path")
        try:
            if not isinstance(path, str) or not path.startswith("manifests/") or not path.endswith(".lock.json"):
                raise ValueError("invalid lock path")
            manifest = load_json(root, path)
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
            continue
        source = manifest.get("source") or {}
        if source.get("repo_type") == "dataset":
            continue
        rid = source.get("repo_id")
        if not isinstance(rid, str):
            errors.append(f"{path}: missing repo id")
            continue
        model = models.get(rid.lower())
        if model is not None and model.get("portfolio_decision") in ("select", "conditional") and model.get("parameter_gate", {}).get("status") == LOW:
            continue
        parents = [m for m in models.values() if m.get("portfolio_decision") in ("select", "conditional")
                   and m.get("parameter_gate", {}).get("status") == VERIFIED
                   and verified_quant_exception(m) and m.get("quantized_exception", {}).get("quantized_repo_id", "").lower() == rid.lower()]
        if len(parents) != 1:
            errors.append(f"{path}: no eligible exact quantized model identity: {rid}")
    return errors


if __name__ == "__main__":
    problems = audit()
    if problems:
        print("FAIL: v12 baseline/quantized runtime audit")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    print("PASS: v12 150B baseline; over-baseline quantized cases HOLD unless verified; queue read-only.")
