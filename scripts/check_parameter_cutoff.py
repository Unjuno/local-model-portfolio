#!/usr/bin/env python3
"""Read-only portfolio parameter gate. Never downloads, loads weights, or executes models.

Python >=3.10, standard library only.
Usage: python scripts/check_parameter_cutoff.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(root: Path, relative: str) -> dict[str, Any]:
    # Forbid arbitrary absolute, parent-relative, and out-of-tree references.
    if not isinstance(relative, str) or not relative:
        raise ValueError("missing file path")
    clean = relative.replace("\\", "/")
    parts = Path(clean).parts
    if Path(clean).is_absolute() or ".." in parts or clean.startswith("/") or ":" in clean:
        raise ValueError(f"unsafe path: {relative!r}")
    target = (root / clean).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"outside repository: {relative!r}")
    result = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError(f"expected JSON object: {relative!r}")
    return result


def validate_model(item: dict[str, Any], threshold: int) -> list[str]:
    errors: list[str] = []
    gate = item.get("parameter_gate") or {}
    count = gate.get("total_parameters")
    state = gate.get("status")
    repo_id = item.get("repo_id", "<no repo_id>")
    if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold <= 0:
        raise ValueError("invalid parameter threshold")
    if count is None:
        if state != "UNVERIFIED_BLOCK_FINAL_LOCK":
            errors.append(f"{repo_id}: unknown model total must block final lock")
        return errors
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        return [f"{repo_id}: invalid total parameter value"]
    if count >= threshold:
        if state != "EXCLUDED_TOTAL_PARAMS_GE_250B":
            errors.append(f"{repo_id}: >=250B must have excluded parameter gate")
        if item.get("risk_tier") != "EXCLUDED" or item.get("portfolio_decision") != "excluded":
            errors.append(f"{repo_id}: >=250B must be EXCLUDED/excluded in portfolio")
    else:
        if state != "PASS_TOTAL_PARAMS_LT_250B":
            errors.append(f"{repo_id}: known <250B must have PASS parameter gate")
    return errors


def audit(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    policy = load_json(root, "policies/limits.json")
    rule = policy.get("total_parameter_policy") or {}
    threshold = rule.get("cutoff_model_total_parameters_inclusive")
    if threshold != 250_000_000_000:
        return ["policies/limits.json: hard inclusive threshold must be exactly 250B"]
    current = load_json(root, "catalog/CURRENT.json")
    portfolio = load_json(root, current["materialized_catalog_path"])
    items = portfolio.get("items")
    if not isinstance(items, list):
        return ["effective portfolio missing items"]
    ids: set[tuple[str, str]] = set()
    model_index: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            errors.append("invalid portfolio item object")
            continue
        kind, repo_id = item.get("asset_kind"), item.get("repo_id")
        if not isinstance(kind, str) or not isinstance(repo_id, str):
            errors.append("portfolio item missing kind/id")
            continue
        key = (kind.lower(), repo_id.lower())
        if key in ids:
            errors.append(f"duplicate asset: {kind}/{repo_id}")
        ids.add(key)
        if kind == "model":
            errors += validate_model(item, threshold)
            if repo_id.lower() in model_index:
                errors.append(f"duplicate model repo_id: {repo_id}")
            model_index[repo_id.lower()] = item
        elif kind == "dataset":
            if item.get("parameter_gate", {}).get("status") != "NOT_APPLICABLE_TO_DATASET":
                errors.append(f"dataset should be parameter-exempt: {repo_id}")
        else:
            errors.append(f"unknown asset kind {kind!r}: {repo_id}")
    expected = current.get("expected", {})
    if len(items) != expected.get("tracked"):
        errors.append("tracked item count differs from CURRENT")
    if sum(1 for i in items if i.get("risk_tier") in ("R0", "R1", "R2")) != expected.get("active"):
        errors.append("active item count differs from CURRENT")
    if sum(1 for i in items if i.get("portfolio_decision") == "excluded") != expected.get("by_decision", {}).get("excluded"):
        errors.append("excluded item count differs from CURRENT")
    # A proposed queue is read-only: it is never an execution authorization.
    approved = load_json(root, "queues/approved.json")
    entries = approved.get("entries")
    if not isinstance(entries, list):
        return errors + ["approved queue has invalid entries"]
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("invalid approved entry")
            continue
        path = entry.get("manifest_path")
        try:
            if not isinstance(path, str) or not path.startswith("manifests/") or not path.endswith(".lock.json"):
                raise ValueError("approved manifest must be a pinned .lock.json")
            manifest = load_json(root, path)
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"invalid approved manifest: {exc}")
            continue
        source = manifest.get("source") or {}
        if source.get("repo_type") == "dataset":
            continue
        repo_id = source.get("repo_id")
        if not isinstance(repo_id, str):
            errors.append(f"{path}: model repo_id absent")
            continue
        matched = model_index.get(repo_id.lower())
        if matched is None:
            errors.append(f"{path}: approved model not in screened portfolio: {repo_id}")
        elif matched["parameter_gate"]["status"] != "PASS_TOTAL_PARAMS_LT_250B":
            errors.append(f"{path}: blocked parameter total (unknown or >=250B): {repo_id}")
    return errors


if __name__ == "__main__":
    problems = audit()
    if problems:
        print("FAIL: hard 250B parameter-policy violations:")
        for problem in problems:
            print(" - " + problem)
        raise SystemExit(1)
    print("PASS: total-parameter gate enforced; all tracked >=250B models excluded; approved queue checked.")
