"""Read-only, metadata-only check of CURRENT and its active sidecars."""
import argparse
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH_GATES = {
    "EXPLICIT_ACQUISITION_AUTHORIZATION",
    "EXPLICIT_NEW_ACQUISITION_AUTHORIZATION_IF_SCOPE_CHANGES",
}
def audit(root=ROOT):
    def read(path):
        return json.loads((root / path).read_text(encoding="utf-8"))
    def key(row):
        return row["asset_kind"], row["repo_id"]
    def index(rows):
        indexed = {key(row): row for row in rows}
        if len(indexed) != len(rows):
            raise ValueError("duplicate asset key")
        return indexed
    c = read("catalog/CURRENT.json")
    p = read(c["materialized_catalog_path"])
    rows = index(p["items"])
    active = {k: v for k, v in rows.items() if v["portfolio_decision"] in ("select", "conditional")}
    conditional = {k for k, v in active.items() if v["portfolio_decision"] == "conditional"}
    models = [v for v in active.values() if v["asset_kind"] == "model"]
    decisions = collections.Counter(v["portfolio_decision"] for v in rows.values())
    r = read(c["latest_active_readiness_audit"]["summary_path"])
    q = read(c["priority_worklist_path"])
    d = read(c["insurance_preparation_worklist_path"])
    a = read(c["latest_conditional_access_audit"]["path"])
    ready = index(r["records"])
    errors = []
    def check(condition, label):
        if not condition:
            errors.append(label)
    check(c["revision_id"] == p["revision_id"] == r["catalog_revision"], "revision mismatch")
    for obj in (q, d, a):
        check(obj["source_revision"] == c["revision_id"], "sidecar revision mismatch")
    check(len(rows) == c["expected"]["tracked"] and len(active) == c["expected"]["active"], "tracked/active mismatch")
    check(decisions == c["expected"]["by_decision"], "decision totals mismatch")
    check(set(ready) == set(active) == set(index(q["candidates"])) == set(index(d["items"])), "active membership mismatch")
    check(set(index(a["entries"])) == conditional, "conditional access membership mismatch")
    check(all(ready[k]["decision"] == active[k]["portfolio_decision"] for k in set(ready)&set(active)), "readiness decision mismatch")
    check(all(v.get("selection") == active[k]["portfolio_decision"] for k,v in index(q["candidates"]).items() if k in active), "proposed decision mismatch")
    check(all(not v["download_approved"] and not v["ready_to_acquire"] and v["final_selected_file_bytes"] is None for v in ready.values()), "unexpected readiness/authorization")
    check(all(v["first_blocker"] in v["blocking_gates"] for v in ready.values()), "first blocker not in list")
    check(all(AUTH_GATES.intersection(v["blocking_gates"]) for v in ready.values()), "missing explicit authorization gate")
    check(collections.Counter(g for v in ready.values() for g in v["blocking_gates"]) == r["summary"]["blocking_gate_counts"], "blocking gate counts mismatch")
    check(collections.Counter(v["first_blocker"] for v in ready.values()) == r["summary"]["first_blocker_counts"], "first blocker counts mismatch")
    check(read("queues/approved.json")["entries"] == [], "approved queue not empty; review explicitly")
    ledger = read(c["latest_reported_ledger_summary"]["path"])
    verified = [v for v in ledger["models"] if v["status"] == "VERIFIED"]
    by_repo = {v["repo_id"]: v for v in verified}
    check(len(by_repo) == len(verified), "duplicate verified receipt repo")
    receipt_keys = {k for k in rows if k[1] in by_repo}
    bases = [v for v in models if v.get("group") == "言語・高性能・Base"]
    known_base_bytes = sum(v["upstream_all_files_bytes_observed"] for v in bases if isinstance(v.get("upstream_all_files_bytes_observed"), int))
    checks = {
        "tracked": len(rows), "active": len(active), "decisions": dict(decisions),
        "active_models": len(models), "active_datasets": len(active)-len(models),
        "active_group_missing": sum(not v.get("group") for v in active.values()),
        "tracked_group_missing": sum(not v.get("group") for v in rows.values()),
        "active_models_with_positive_and_negative_fields": sum(bool(v.get("quality_positive")) and bool(v.get("quality_negative")) for v in models),
        "explicit_base_group_including_coding": len(bases),
        "base_group_known_full_repo_reference_bytes": known_base_bytes,
        "base_group_reported_receipts": sum(v["repo_id"] in by_repo for v in bases),
        "base_group_reported_receipt_bytes": sum(by_repo[v["repo_id"]]["source_bytes"] for v in bases if v["repo_id"] in by_repo),
        "verified_receipts": len(verified),
        "verified_receipt_files": sum(v["files_verified"] for v in verified),
        "verified_receipt_reference_bytes": sum(v["source_bytes"] for v in verified),
        "registered_verified_receipts": len(receipt_keys),
        "active_verified_receipts": len(receipt_keys & set(active)),
        "active_without_verified_receipt": len(set(active)-receipt_keys),
        "unregistered_verified_receipts": len(set(by_repo)-{k[1] for k in rows}),
        "active_final_lock_bytes_unknown": sum(v["final_selected_file_bytes"] is None for v in ready.values()),
        "active_parameter_unknown": sum(v.get("parameter_gate",{}).get("status") == "UNVERIFIED_BLOCK_FINAL_LOCK" for v in models),
        "active_first_blocker_count": sum(r["summary"]["first_blocker_counts"].values()),
        "approved_queue_entries": len(read("queues/approved.json")["entries"]),
    }
    for metric, key_name in (("verified_receipts","models_verified"),("verified_receipt_files","files_verified_total"),("verified_receipt_reference_bytes","bytes_verified_total")):
        check(checks[metric] == ledger["summary"][key_name], "receipt summary mismatch: "+metric)
    return {"revision": c["revision_id"], "scope": "metadata-only; not owner disk, performance, rights or restoration proof", "metrics": checks, "errors": errors, "physical_deletion_authorized": False, "acquisition_authorized": False}
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(bool(result["errors"]))
