#!/usr/bin/env python3
"""Build a public-safe, machine-readable acquisition ledger from local receipts.

Local absolute paths, usernames and credentials are never written to the repo.
Only publisher identity (repo_id/revision), file counts, byte totals, hashes and
statuses are exported. Unacquired/held models are recorded as such, never as
acquired.
"""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

LOCAL = Path("D:/AI_VAULT/state/ledger/acquisition-ledger.json")
LOCAL_WAVE2 = Path("D:/AI_VAULT/state/ledger/wave2-ledger.json")
LOCAL_CONT = Path("D:/AI_VAULT/state/ledger/waves3plus-ledger.json")
LOCAL_LARGE = Path("D:/AI_VAULT/state/ledger/waves-large-ledger.json")
LOCAL_OCT = Path("D:/AI_VAULT/state/ledger/octomed-ledger.json")
LOCAL_REPAIR = Path("D:/AI_VAULT/state/ledger/waves3plus-ledger.json")
LOCAL_INTEGRATE = Path("D:/AI_VAULT/state/ledger/existing-integrated-ledger.json")
LOCAL_EXCLUDED = Path("D:/AI_VAULT/state/ledger/excluded-rights-ledger.json")
OUT = Path("catalog/execution/2026-11-19-acquisition-ledger.json")
MD = Path("docs/strategy/114-v48-execution-acquisition-results-2026-11-19.md")


def sanitize_source(value):
    """Never export local absolute paths into the public repository."""
    if not value:
        return None
    s = str(value).replace("\\", "/")
    if "AI_VAULT" in s or s.lower().startswith("d:/"):
        return "local-discovered/" + s.rsplit("/", 1)[-1]
    return s


def main():
    all_entries = []
    for p in (LOCAL, LOCAL_WAVE2, LOCAL_CONT, LOCAL_LARGE, LOCAL_OCT,
              LOCAL_INTEGRATE, LOCAL_EXCLUDED):
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            all_entries.extend(d.get("entries", []))
    # Merge receipts for the same exact publisher identity. Repair receipts
    # contain only the fixed shards, so union every file path and prefer the
    # verified version of each path. The full scope comes from the largest
    # receipt, preventing a narrow repair from undercounting a model.
    grouped = {}
    for e in all_entries:
        key = (e.get("repo_id"), e.get("revision_sha"))
        grouped.setdefault(key, []).append(e)

    good = {"VERIFIED", "DEDUP_VERIFIED"}
    entries = []
    for (repo, rev), group in grouped.items():
        files = {}
        for e in group:
            for f in e.get("files", []):
                p = f.get("path")
                if not p:
                    continue
                old = files.get(p)
                if old is None or (f.get("status") in good and
                                   old.get("status") not in good):
                    files[p] = f
        expected = max((int(e.get("total") or 0) for e in group), default=0)
        verified_count = sum(1 for f in files.values() if f.get("status") in good)
        holds = [str(e.get("status")) for e in group
                 if str(e.get("status", "")).startswith("HOLD")]
        # A verified receipt always supersedes a stale HOLD from a blocked attempt.
        if expected and verified_count >= expected:
            status = "VERIFIED"
        elif verified_count:
            status = "PARTIAL"
        elif holds:
            status = holds[0]
        else:
            status = max((str(e.get("status")) for e in group), default="FAILED")
        base = max(group, key=lambda e: (int(e.get("total") or 0),
                                         str(e.get("finished_at", ""))))
        methods = Counter(f.get("method") for f in files.values() if f.get("method"))
        statuses = Counter(f.get("status") for f in files.values())
        entries.append({
            "repo_id": repo,
            "revision_sha": rev,
            "source_manifest": sanitize_source(base.get("source")),
            "priority_group": base.get("group"),
            "status": status,
            "license": base.get("license"),
            "hold_reason": next((e.get("hold_reason") for e in group
                                 if e.get("hold_reason")), None),
            "files_total": expected or len(files),
            "files_verified": verified_count,
            "source_bytes": max((int(e.get("bytes") or 0) for e in group), default=0),
            "verification_methods": dict(methods),
            "file_status_counts": dict(statuses),
            "weight_files_sha256": [
                {"path": f["path"], "sha256": f["sha256"]}
                for f in files.values()
                if f.get("method") == "sha256-vs-publisher" and f.get("sha256")
            ],
            "started_at": base.get("started_at"),
            "finished_at": base.get("finished_at"),
            "free_bytes_after": base.get("free_bytes_after"),
        })
    summary = {
        "models_total": len(entries),
        "models_verified": sum(1 for e in entries if e["status"] == "VERIFIED"),
        "models_partial": sum(1 for e in entries if e["status"] == "PARTIAL"),
        "models_failed": sum(1 for e in entries if e["status"] == "FAILED"),
        "models_held": sum(1 for e in entries if str(e["status"]).startswith("HOLD")),
        "files_verified_total": sum(e["files_verified"] or 0 for e in entries),
        "bytes_verified_total": sum(e["source_bytes"] or 0 for e in entries
                                    if e["status"] in ("VERIFIED", "PARTIAL")),
        "minimum_free_bytes_observed": min(
            (e["free_bytes_after"] for e in entries if e.get("free_bytes_after") is not None),
            default=None),
        "minimum_free_floor_bytes": 200_000_000_000,
    }
    summary["free_floor_maintained"] = bool(
        summary["minimum_free_bytes_observed"] is not None and
        summary["minimum_free_bytes_observed"] >= summary["minimum_free_floor_bytes"])
    out = {
        "schema_version": 1,
        "ledger_id": "2026-11-19-v48-execution",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_revision": "v48-20261118",
        "source_plan": "queues/proposed-v48-r113-source-pinned-15.json",
        "policy": {
            "pinned_revision_only": True,
            "publisher_hash_verification": True,
            "dedupe_by_hash": True,
            "resume_partial_downloads": True,
            "model_code_executed": False,
            "gated_without_entitlement": "HOLD",
            "unclear_license": "HOLD",
        },
        "summary": summary,
        "models": entries,
        "notes": [
            "Local absolute paths, usernames and credentials are intentionally omitted.",
            "A HOLD entry means no payload was acquired for that model.",
            "Publisher LFS SHA-256 compared for weight files; ordinary Git blobs "
            "compared by Git blob SHA-1; 'size-only' means no publisher hash existed.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md = [
        "# v48 Acquisition Execution Results (2026-11-19)",
        "",
        "Results of executing the unified pinned-source plan "
        "`queues/proposed-v48-r113-source-pinned-15.json` from canonical "
        "`catalog/CURRENT.json` (v48-20261118).",
        "",
        f"- Models: {summary['models_total']} "
        f"(verified {summary['models_verified']}, partial {summary['models_partial']}, "
        f"failed {summary['models_failed']}, held {summary['models_held']})",
        f"- Verified files: {summary['files_verified_total']}",
        f"- Verified source bytes: {summary['bytes_verified_total']}",
        f"- Minimum observed free bytes: {summary['minimum_free_bytes_observed']} "
        f"(200 GB floor maintained: {summary['free_floor_maintained']})",
        "",
        "| repo_id | revision | status | verified files | license |",
        "| --- | --- | --- | --- | --- |",
    ]
    for e in entries:
        md.append(f"| `{e['repo_id']}` | `{e['revision_sha']}` | {e['status']} | "
                  f"{e['files_verified']}/{e['files_total']} | {e['license']} |")
    md += [
        "",
        "Weight files were compared against publisher LFS SHA-256; ordinary Git blobs "
        "were compared by Git blob SHA-1. 'size-only' means no publisher hash existed.",
        "Gated models without verified owner entitlement were recorded as HOLD and no "
        "payload was acquired for them.",
        "No model code, pickle payload or weights were imported or executed.",
        "Local absolute paths, usernames and credentials are not exported to the repo.",
        "",
    ]
    MD.parent.mkdir(parents=True, exist_ok=True)
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {OUT} and {MD}: {summary}")


if __name__ == "__main__":
    main()
