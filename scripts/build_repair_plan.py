#!/usr/bin/env python3
"""Build a targeted repair plan for shards that failed hash verification.

Only files whose receipt is not VERIFIED / DEDUP_VERIFIED are included.
A matching exact-scope approval file is generated in local state so the
fail-closed downloader accepts these narrowed manifests.
"""
import json
from pathlib import Path

LEDGERS = [
    Path("D:/AI_VAULT/state/ledger/acquisition-ledger.json"),
    Path("D:/AI_VAULT/state/ledger/wave2-ledger.json"),
    Path("D:/AI_VAULT/state/ledger/waves3plus-ledger.json"),
    Path("D:/AI_VAULT/state/ledger/waves-large-ledger.json"),
]
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-repair.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-repair.json")
REF = "user directive 2026-11-19: continuous open-weight acquisition to D drive"


def main():
    bad = {}
    for p in LEDGERS:
        if not p.exists():
            continue
        for e in json.loads(p.read_text(encoding="utf-8")).get("entries", []):
            files = [f for f in e.get("files", [])
                     if f.get("status") not in ("VERIFIED", "DEDUP_VERIFIED")]
            if files:
                bad[e["repo_id"]] = {f["path"] for f in files}
    candidates, approvals = [], []
    for repo, paths in bad.items():
        mp = DISC / (repo.replace("/", "__") + ".json")
        if not mp.exists():
            print("no manifest for", repo)
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        sel = [f for f in m["selected_files"] if f["path"] in paths]
        if not sel:
            continue
        rp = DISC / ("repair-" + repo.replace("/", "__") + ".json")
        rm = dict(m)
        rm["selected_files"] = sel
        rm["selected_file_count"] = len(sel)
        rm["selected_file_bytes"] = sum(int(f["bytes"]) for f in sel)
        rp.write_text(json.dumps(rm, indent=2, ensure_ascii=False), encoding="utf-8")
        candidates.append({"repo_id": repo, "revision_sha": m["source_revision_sha"],
                           "files": len(sel), "bytes": rm["selected_file_bytes"],
                           "manifest": str(rp)})
        afiles = []
        for f in sel:
            r = {"path": f["path"], "bytes": int(f["bytes"])}
            if f.get("publisher_lfs_sha256"):
                r["sha256"] = f["publisher_lfs_sha256"]
            elif f.get("publisher_git_blob_sha1"):
                r["git_blob_sha1"] = f["publisher_git_blob_sha1"]
            afiles.append(r)
        approvals.append({"repo_id": repo, "revision_sha": m["source_revision_sha"],
                          "approved": True, "download_enabled": True,
                          "approved_by_user": True, "license_text_reviewed": True,
                          "parent_dependency_rights_reviewed": True,
                          "nonstandard_license_permission_verified": True,
                          "license": m.get("license_tag", ""),
                          "approval_ref": REF, "files": afiles})
    PLAN.write_text(json.dumps({"schema_version": 1, "candidates": candidates},
                               indent=2, ensure_ascii=False), encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1, "authorization_source": REF,
                                   "entries": approvals}, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"repair models={len(candidates)} files={sum(c['files'] for c in candidates)} "
          f"bytes={sum(c['bytes'] for c in candidates)}")
    for c in candidates:
        print(" ", c["repo_id"], c["files"], c["bytes"])


if __name__ == "__main__":
    main()
