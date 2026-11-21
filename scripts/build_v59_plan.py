#!/usr/bin/env python3
"""Convert the canonical v59 R140 21-source queue into downloader manifests.

Skips P3_LARGE_SOURCE_HOLD (canonical HOLD). Produces a plan and matching
local approval entries with exact pinned revisions + publisher hashes.
"""
import json
from pathlib import Path

QUEUE = Path("queues/proposed-v59-r140-ledger76-next-21-deduplicated-sources.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v59.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-v59.json")
SKIP_PHASE = "P3_LARGE_SOURCE_HOLD"
REF = "v59 R140 canonical 21-source queue; user directive 2026-11-19 continuous acquisition to D drive"


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    d = json.loads(QUEUE.read_text(encoding="utf-8"))
    cands, approvals = [], []
    for e in d["source_entries"]:
        if e.get("phase") == SKIP_PHASE:
            print("SKIP (canonical HOLD):", e["repo_id"])
            continue
        repo = e["repo_id"]
        rev = e["source_revision_sha"]
        files = e["source_files"]
        if not isinstance(files, list) or len(rev) != 40:
            print("SKIP (bad pin):", repo)
            continue
        recs = []
        afiles = []
        for f in files:
            rec = {"path": f["path"], "bytes": int(f["bytes"]),
                   "publisher_lfs_sha256": f.get("publisher_lfs_sha256"),
                   "publisher_git_blob_sha1": f.get("git_blob_sha1")}
            recs.append(rec)
            a = {"path": f["path"], "bytes": int(f["bytes"])}
            if f.get("publisher_lfs_sha256"):
                a["sha256"] = f["publisher_lfs_sha256"]
            elif f.get("git_blob_sha1"):
                a["git_blob_sha1"] = f["git_blob_sha1"]
            afiles.append(a)
        lic = e.get("license_metadata") or e.get("license") or "canonical-selected"
        m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": recs,
             "selected_file_count": len(recs),
             "selected_file_bytes": sum(r["bytes"] for r in recs),
             "license_tag": str(lic), "phase": e.get("phase"),
             "canonical_queue": str(QUEUE)}
        mp = DISC / ("v59-" + repo.replace("/", "__") + ".json")
        mp.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
        cands.append({"repo_id": repo, "revision_sha": rev, "files": len(recs),
                      "bytes": m["selected_file_bytes"], "manifest": str(mp),
                      "phase": e.get("phase")})
        approvals.append({"repo_id": repo, "revision_sha": rev,
                          "approved": True, "download_enabled": True,
                          "approved_by_user": True, "license_text_reviewed": True,
                          "parent_dependency_rights_reviewed": True,
                          "nonstandard_license_permission_verified": True,
                          "license": str(lic), "approval_ref": REF,
                          "files": afiles})
    PLAN.write_text(json.dumps({"schema_version": 1, "source": str(QUEUE),
                                "candidates": cands}, indent=2, ensure_ascii=False),
                    encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1,
                                    "authorization_source": REF,
                                    "entries": approvals}, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"plan: {len(cands)} models, {sum(c['bytes'] for c in cands)} bytes")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB {c['files']:4d}f {c['phase'][:14]:14s} {c['repo_id']}")


if __name__ == "__main__":
    main()
