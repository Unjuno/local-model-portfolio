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
OUT = Path("state/execution/2026-11-19-acquisition-ledger.json")


def main():
    all_entries = []
    for p in (LOCAL, LOCAL_WAVE2):
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            all_entries.extend(d.get("entries", []))
    entries = []
    for e in all_entries:
        files = e.get("files", [])
        methods = Counter(f.get("method") for f in files if f.get("method"))
        statuses = Counter(f.get("status") for f in files)
        entries.append({
            "repo_id": e.get("repo_id"),
            "revision_sha": e.get("revision_sha"),
            "source_manifest": e.get("source"),
            "priority_group": e.get("group"),
            "status": e.get("status"),
            "license": e.get("license"),
            "files_total": e.get("total"),
            "files_verified": e.get("verified"),
            "source_bytes": e.get("bytes"),
            "verification_methods": dict(methods),
            "file_status_counts": dict(statuses),
            "weight_files_sha256": [
                {"path": f["path"], "sha256": f["sha256"]}
                for f in files
                if f.get("method") == "sha256-vs-publisher" and f.get("sha256")
            ],
            "started_at": e.get("started_at"),
            "finished_at": e.get("finished_at"),
            "free_bytes_after": e.get("free_bytes_after"),
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
        "# v48 取得実行実績（2026-11-19）",
        "",
        "正本 `catalog/CURRENT.json` (v48-20261118) の統一ソース計画 "
        "`queues/proposed-v48-r113-source-pinned-15.json` に基づく実行結果。",
        "",
        f"- モデル数: {summary['models_total']}（検証済み {summary['models_verified']}、"
        f"部分 {summary['models_partial']}、失敗 {summary['models_failed']}、保留 {summary['models_held']}）",
        f"- 検証済みファイル: {summary['files_verified_total']}",
        f"- 検証済みソースバイト: {summary['bytes_verified_total']}",
        f"- 観測された最小空き: {summary['minimum_free_bytes_observed']} byte"
        f"（200GB床維持: {summary['free_floor_maintained']}）",
        "",
        "| repo_id | revision | 状態 | 検証ファイル | ライセンス |",
        "| --- | --- | --- | --- | --- |",
    ]
    for e in entries:
        md.append(f"| `{e['repo_id']}` | `{e['revision_sha']}` | {e['status']} | "
                  f"{e['files_verified']}/{e['files_total']} | {e['license']} |")
    md += [
        "",
        "重みファイルは出版社 LFS SHA-256 と照合し、通常 Git blob は Git blob SHA-1 で照合した。",
        "Gated で本人権限が確認できないモデルは HOLD とし、ペイロードを取得していない。",
        "モデルコードの import / pickle / 推論は一切実行していない。",
        "ローカル絶対パス・ユーザー名・認証情報は公開リポジトリへ書き出していない。",
        "",
    ]
    MD = Path("docs/strategy/114-v48-execution-acquisition-results-2026-11-19.md")
    MD.parent.mkdir(parents=True, exist_ok=True)
    MD.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {OUT} and {MD}: {summary}")


if __name__ == "__main__":
    main()
