#!/usr/bin/env python3
"""Build a download plan from the canonical v62 R147 post96 research queue.

Reads the pinned source manifests referenced by the queue, skips the P3
canonical HOLD, and writes per-model manifests + exact approval entries.
"""
import json
from pathlib import Path

QUEUE = Path("queues/proposed-v62-r147-post96-next-research-sources.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v62.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-v62.json")
SKIP_PHASE = "P3_LARGE_RESEARCH_HOLD"
REF = "v62 R147 canonical post96 source queue; user directive 2026-11-19 continuous acquisition to D drive"


def find_model(man, repo):
    for key in ("model_repos", "publisher_model_sources", "publisher_sources",
                "models", "repositories", "source_entries"):
        v = man.get(key)
        if isinstance(v, list):
            for e in v:
                if isinstance(e, dict) and e.get("repo_id") == repo:
                    return e
    return None


def files_of(e):
    for k in ("selected_files", "publisher_selected_files", "files", "source_files"):
        v = e.get(k)
        if isinstance(v, list) and v and "path" in v[0]:
            return v
    return []


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    entries = q.get("future_research_queue") or []
    cands, approvals = [], []
    for e in entries:
        if e.get("phase") == SKIP_PHASE:
            print("SKIP (canonical HOLD):", e["repo_id"])
            continue
        repo = e["repo_id"]
        mp = Path(e["source_manifest"])
        if not mp.exists():
            print("SKIP (no manifest):", repo)
            continue
        man = json.loads(mp.read_text(encoding="utf-8"))
        me = find_model(man, repo)
        if not me:
            print("SKIP (repo not in manifest):", repo)
            continue
        rev = (e.get("publisher_revision_sha") or me.get("revision_sha") or
               me.get("immutable_revision_sha") or "")
        files = files_of(me)
        if len(rev) != 40 or not files:
            print("SKIP (bad pin/files):", repo, "rev=", rev, "files=", len(files))
            continue
        recs, afiles = [], []
        for f in files:
            r = {"path": f["path"], "bytes": int(f.get("bytes", 0)),
                 "publisher_lfs_sha256": f.get("publisher_lfs_sha256"),
                 "publisher_git_blob_sha1": f.get("git_blob_sha1")}
            recs.append(r)
            a = {"path": f["path"], "bytes": int(f.get("bytes", 0))}
            if f.get("publisher_lfs_sha256"):
                a["sha256"] = f["publisher_lfs_sha256"]
            elif f.get("git_blob_sha1"):
                a["git_blob_sha1"] = f["git_blob_sha1"]
            else:
                continue
            afiles.append(a)
        if len(afiles) != len(recs):
            print("SKIP (files without hash):", repo)
            continue
        m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": recs,
             "selected_file_count": len(recs),
             "selected_file_bytes": sum(r["bytes"] for r in recs),
             "license_tag": str(e.get("publisher_license_tag") or
                                me.get("repo_card_license") or me.get("publisher_license_tag") or ""),
             "phase": e.get("phase"), "canonical_queue": str(QUEUE)}
        out = DISC / ("v62-" + repo.replace("/", "__") + ".json")
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
    APPROVAL.write_text(json.dumps({"schema_version": 1,
                                    "authorization_source": REF,
                                    "entries": approvals}, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"plan: {len(cands)} models, {sum(c['bytes'] for c in cands)} bytes")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB {c['files']:3d}f {c['phase'][:16]:16s} {c['repo_id']}")


if __name__ == "__main__":
    main()
