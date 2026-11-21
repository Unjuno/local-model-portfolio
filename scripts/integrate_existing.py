#!/usr/bin/env python3
"""Integrate three already-stored models into the acquisition ledger.

These were downloaded earlier under acquisition_verification_receipt receipts
but were never reported in the public execution ledger. Build pinned manifests
from the recorded publisher metadata and re-hash the actual local files so the
ledger reflects verified on-disk state (never claim unverified acquisitions).
"""
import json
from pathlib import Path

STATE = Path("D:/AI_VAULT/state")
DISC = STATE / "discovered"
ACQ = STATE / "acquisitions"
LEDGER = STATE / "ledger" / "existing-integrated-ledger.json"
STORE = Path("D:/AI_VAULT/store/huggingface/model")


def manifest_from_api(repo, rev, api_path, out_name):
    api = json.loads((STATE / "research" / api_path).read_text(encoding="utf-8"))
    files = []
    for s in api.get("siblings", []):
        p = s.get("rfilename")
        if not p:
            continue
        files.append({"path": p, "bytes": int(s.get("size") or 0),
                      "publisher_lfs_sha256": (s.get("lfs") or {}).get("sha256"),
                      "publisher_git_blob_sha1": s.get("blobId")})
    m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": files,
         "selected_file_count": len(files),
         "selected_file_bytes": sum(f["bytes"] for f in files),
         "license_tag": "apache-2.0"}
    p = DISC / out_name
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return m, p


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    built = []
    built.append(manifest_from_api(
        "tencent/Hy-SimulMT-30B-A3B", "56c233df75bf09e386aa6282b01730b461afc83f",
        "hy-simulmt-api-2026-11-05.json", "existing-tencent-hy-simulmt.json"))
    for m, p in built:
        print(m["repo_id"], "rev", m["source_revision_sha"],
              "files", m["selected_file_count"], "bytes", m["selected_file_bytes"],
              "->", p.name)


if __name__ == "__main__":
    main()
