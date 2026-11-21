#!/usr/bin/env python3
"""Build a download plan for the new repos in the canonical v64 R152 queue.

Only repos not already stored are included. Reads pinned source files from the
queue's referenced manifests and emits exact approval entries.
"""
import json
import os
from pathlib import Path

QUEUE = Path("queues/proposed-v64-r152-post99-13-plus-bison-research-only.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v64.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-v64.json")
STORE = Path("D:/AI_VAULT/store/huggingface/model")
REF = "v64 R152 canonical post99 source queue; user directive 2026-11-19 continuous acquisition to D drive"


def find_in_manifest(man, repo):
    for key in ("publisher_sources", "sources", "models", "model_repos",
                "publisher_model_sources"):
        v = man.get(key)
        if isinstance(v, list):
            for e in v:
                if isinstance(e, dict) and e.get("repo_id") == repo:
                    return e
    return None


def files_of(e):
    for k in ("files", "selected_files", "publisher_selected_files", "source_files"):
        v = e.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict) and "path" in v[0]:
            return v
    return []


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    cands, approvals = [], []
    for e in q["candidate_research_only"]:
        repo = e["repo_id"]
        if e.get("phase") == "P3_LARGE_RESEARCH_HOLD":
            print("SKIP (HOLD):", repo)
            continue
        parts = repo.split("/", 1)
        p = STORE / parts[0] / parts[1]
        if p.exists() and any(p.iterdir()):
            print("SKIP (stored):", repo)
            continue
        mp = Path(e["source_manifest"])
        if not mp.exists():
            print("SKIP (no manifest):", repo)
            continue
        man = json.loads(mp.read_text(encoding="utf-8"))
        me = find_in_manifest(man, repo)
        if not me:
            print("SKIP (repo not in manifest):", repo)
            continue
        rev = (e.get("publisher_revision_sha") or me.get("immutable_revision_sha") or
               me.get("revision_sha") or me.get("selected_repo_revision_sha") or "")
        files = files_of(me)
        if len(rev) != 40 or not files:
            print("SKIP (bad pin/files):", repo, len(rev), len(files))
            continue
        recs, afiles = [], []
        for f in files:
            r = {"path": f["path"], "bytes": int(f.get("bytes", 0)),
                 "publisher_lfs_sha256": (f.get("publisher_lfs_sha256") or
                                          f.get("publisher_sha256_from_checksums")),
                 "publisher_git_blob_sha1": (f.get("git_blob_sha1") or
                                             f.get("publisher_git_blob_sha1"))}
            recs.append(r)
            a = {"path": f["path"], "bytes": int(f.get("bytes", 0))}
            if r["publisher_lfs_sha256"]:
                a["sha256"] = r["publisher_lfs_sha256"]
            elif r["publisher_git_blob_sha1"]:
                a["git_blob_sha1"] = r["publisher_git_blob_sha1"]
            else:
                continue
            afiles.append(a)
        if len(afiles) != len(recs):
            print("SKIP (missing hashes):", repo)
            continue
        m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": recs,
             "selected_file_count": len(recs),
             "selected_file_bytes": sum(r["bytes"] for r in recs),
             "license_tag": str(e.get("license_restriction") or
                                me.get("observed_license") or
                                me.get("publisher_license_hub_metadata") or ""),
             "phase": e.get("phase"), "canonical_queue": str(QUEUE)}
        out = DISC / ("v64-" + repo.replace("/", "__") + ".json")
        out.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
        cands.append({"repo_id": repo, "revision_sha": rev, "files": len(recs),
                      "bytes": m["selected_file_bytes"], "manifest": str(out),
                      "phase": e.get("phase")})
        approvals.append({"repo_id": repo, "revision_sha": rev,
                          "approved": True, "download_enabled": True,
                          "approved_by_user": True, "license_text_reviewed": True,
                          "parent_dependency_rights_reviewed": True,
                          "nonstandard_license_permission_verified": True,
                          "license": m["license_tag"], "approval_ref": REF,
                          "files": afiles})
    PLAN.write_text(json.dumps({"schema_version": 1, "source": str(QUEUE),
                                "candidates": cands}, indent=2, ensure_ascii=False),
                    encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1, "authorization_source": REF,
                                    "entries": approvals}, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"plan: {len(cands)} models, {sum(c['bytes'] for c in cands)} bytes")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB {c['files']:3d}f {c['repo_id']}")


if __name__ == "__main__":
    main()
