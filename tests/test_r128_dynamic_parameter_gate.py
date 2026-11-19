"""R128: offline dynamic catalog parameter-gate consistency checks.

Python 3.10+ standard library. No networking, models, or remote code execution.
Loads CURRENT.json's materialized path and rejects header drift independently
of whether current revision is v48, v54, or a later snapshot.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PARAMETER_STATES = (
    "PASS_TOTAL_PARAMS_LT_150B",
    "OVER_150B_QUANT_REVIEW_REQUIRED",
    "UNVERIFIED_BLOCK_FINAL_LOCK",
)


def parameter_audit(root: Path = ROOT) -> list[str]:
    current = json.loads((root / "catalog" / "CURRENT.json").read_text(encoding="utf-8"))
    p = Path(current["materialized_catalog_path"])
    if p.is_absolute() or ".." in p.parts:
        return ["invalid materialized catalog path"]
    materialized = json.loads((root / p).read_text(encoding="utf-8"))
    errors: list[str] = []
    if current["revision_id"] != materialized["revision_id"]:
        errors.append("CURRENT revision differs from materialized revision")
    items = materialized["items"]
    observed = Counter(
        x.get("parameter_gate", {}).get("status", "<MISSING>")
        for x in items if x.get("asset_kind") == "model"
    )
    model_n = sum(x.get("asset_kind") == "model" for x in items)
    if sum(observed.values()) != model_n:
        errors.append("unaccounted model gate")
    for state in PARAMETER_STATES:
        n = observed.get(state, 0)
        if current.get("expected", {}).get("parameter_gate", {}).get(state) != n:
            errors.append(f"CURRENT expected {state} does not match actual {n}")
        if materialized.get("counts", {}).get("parameter_gate", {}).get(state) != n:
            errors.append(f"materialized header {state} does not match actual {n}")
    if any(state not in PARAMETER_STATES for state in observed):
        errors.append("unexpected parameter gate status")
    limit = 150_000_000_000
    for item in items:
        if item.get("asset_kind") != "model":
            continue
        total = item.get("parameter_gate", {}).get("total_parameters")
        decision = item.get("portfolio_decision")
        if total is not None and total >= limit and decision in ("select", "conditional"):
            errors.append(f"over-cap model marked active: {item['repo_id']}")
        if total is None and item.get("download_approved") is True:
            errors.append(f"unknown-total model download approved: {item['repo_id']}")
    return errors


class R128ParameterGateTests(unittest.TestCase):
    def test_branch_current_consistency(self) -> None:
        self.assertEqual(parameter_audit(), [])

    def test_missing_one_pass_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog").mkdir()
            current = {"revision_id": "vT", "materialized_catalog_path": "catalog/snapshot.json",
                       "expected": {"parameter_gate": {
                           "PASS_TOTAL_PARAMS_LT_150B": 2,
                           "OVER_150B_QUANT_REVIEW_REQUIRED": 0,
                           "UNVERIFIED_BLOCK_FINAL_LOCK": 0}}}
            item = {"repo_id": "p/model", "asset_kind": "model", "portfolio_decision": "select",
                    "parameter_gate": {"status": "PASS_TOTAL_PARAMS_LT_150B",
                                       "total_parameters": 100}}
            mat = {"revision_id": "vT", "items": [item],
                   "counts": {"parameter_gate": {
                       "PASS_TOTAL_PARAMS_LT_150B": 1,
                       "OVER_150B_QUANT_REVIEW_REQUIRED": 0,
                       "UNVERIFIED_BLOCK_FINAL_LOCK": 0}}}
            (root / "catalog" / "CURRENT.json").write_text(json.dumps(current))
            (root / "catalog" / "snapshot.json").write_text(json.dumps(mat))
            self.assertIn("CURRENT expected PASS_TOTAL_PARAMS_LT_150B does not match actual 1",
                          parameter_audit(root))


if __name__ == "__main__":
    unittest.main()
