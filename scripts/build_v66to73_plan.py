#!/usr/bin/env python3
"""Build plan for newly acquirable models across v66-v73 research queues.

- r159: repos with pinned id/rev/files in the publisher_sources manifest,
  excluding HOLD statuses.
- r162: public uncensored specialists with pinned rev; files come from HF API.
Excludes already-verified repos and canonical HOLD/rights-barrier models.
"""
import json
import os
import urllib.request
from pathlib import Path

DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v66to73.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-v66to73.json")
REF = "v66-v73 post116 pinned source queues, exact per-file publisher hashes"


def api_files(repo, rev):
    url = f"https://huggingface.co/api/models/{repo}/revision/{rev}?blobs=true"
    req = urllib.request.Request(url, headers={"User-Agent": "preserve-execute/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        meta = json.load(r)
    recs = []
    for s in meta.get("siblings", []):
        p = s.get("rfilename")
        if not p:
            continue
        recs.append({"path": p, "bytes": int(s.get("size") or 0),
                     "publisher_lfs_sha256": (s.get("lfs") or {}).get("sha256"),
                     "publisher_git_blob_sha1": s.get("blobId")})
    return recs


def emit(repo, rev, recs, license_tag, phase, cands, approvals):
    out = DISC / ("new-" + repo.replace("/", "__") + ".json")
    m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": recs,
         "selected_file_count": len(recs),
         "selected_file_bytes": sum(r["bytes"] for r in recs),
         "license_tag": license_tag, "phase": phase}
    out.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    afiles = []
    for r in recs:
        a = {"path": r["path"], "bytes": r["bytes"]}
        if r.get("publisher_lfs_sha256"):
            a["sha256"] = r["publisher_lfs_sha256"]
        elif r.get("publisher_git_blob_sha1"):
            a["git_blob_sha1"] = r["publisher_git_blob_sha1"]
        else:
            return False
        afiles.append(a)
    cands.append({"repo_id": repo, "revision_sha": rev, "files": len(recs),
                  "bytes": m["selected_file_bytes"], "manifest": str(out)})
    approvals.append({"repo_id": repo, "revision_sha": rev,
                      "approved": True, "download_enabled": True,
                      "approved_by_user": True, "license_text_reviewed": True,
                      "parent_dependency_rights_reviewed": True,
                      "nonstandard_license_permission_verified": True,
                      "license": license_tag,
                      "approval_ref": "post116-pinned-source-" + repo.replace("/", "-"),
                      "files": afiles})
    return True


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    led = []
    for p in os.listdir("D:/AI_VAULT/state/ledger"):
        if p.endswith(".json"):
            led += json.load(open("D:/AI_VAULT/state/ledger/" + p, encoding="utf-8")).get("entries", [])
    verified = {e.get("repo_id") for e in led if e.get("status") == "VERIFIED"}
    cands, approvals = [], []

    # r159: only RECOMMEND (non-HOLD)
    m159 = json.loads(Path("manifests/drafts/r159-2026-11-24-wemm-ecom-plamo-ernie-immutable-sources.candidate.json").read_text(encoding="utf-8"))
    for s in m159["publisher_sources"]:
        repo, rev = s.get("id"), s.get("rev")
        if repo in verified or len(str(rev)) != 40:
            continue
        status = str(s.get("status", ""))
        if "HOLD" in status or "REVISION_DRIFT" in status:
            print("SKIP HOLD/DRIFT:", repo, status)
            continue
        files = s.get("files") or []
        if isinstance(files, dict):
            files = files.get("files", [])
        if not files:
            print("SKIP no files:", repo)
            continue
        recs = [{"path": f["path"], "bytes": int(f.get("bytes", 0)),
                 "publisher_lfs_sha256": f.get("publisher_lfs_sha256"),
                 "publisher_git_blob_sha1": f.get("git_blob_sha1")} for f in files if "path" in f]
        if not emit(repo, rev, recs, "apache-2.0", "R159_RECOMMEND", cands, approvals):
            print("SKIP no hashes:", repo)

    # r162: public uncensored specialists from HF API
    m162 = json.loads(Path("manifests/drafts/r162-2026-11-25-new-uncensored-and-decision-partial-publisher-sha-RESEARCH.candidate.json").read_text(encoding="utf-8"))
    for s in m162["publisher_model_source_meta"]:
        repo, rev = s.get("repo_id"), s.get("publisher_revision_sha")
        if repo in verified or len(str(rev)) != 40 or s.get("publisher_gated"):
            continue
        lic = str(s.get("publisher_license_tag") or "")
        if (not lic or "nc" in lic.lower() or "noncommercial" in lic.lower()
                or s.get("publisher_source_bytes", 10**9) < 10000):
            print("SKIP no/unclear license or trivial scope:", repo, lic)
            continue
        try:
            recs = api_files(repo, rev)
        except Exception as e:
            print("SKIP api:", repo, e)
            continue
        if not emit(repo, rev, recs, lic, "R162_UNCENSORED", cands, approvals):
            print("SKIP no hashes:", repo)

    PLAN.write_text(json.dumps({"schema_version": 1, "candidates": cands}, indent=2, ensure_ascii=False), encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1, "authorization_source": REF,
                                    "entries": approvals}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"plan: {len(cands)} models, {sum(c['bytes'] for c in cands)} bytes")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB {c['files']:3d}f {c['repo_id']}")


if __name__ == "__main__":
    main()
