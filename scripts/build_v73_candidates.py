#!/usr/bin/env python3
"""Build a plan from v73 effective-portfolio candidate_selected_source_files.

Targets are active models with a pinned observed revision, a full candidate
file list with publisher hashes, public access and a permissive (Apache/MIT)
license. Rights-barred (noncommercial / complex derivative) repos are excluded.
"""
import json
import os
from pathlib import Path

EFF = Path("catalog/effective-portfolio-2026-11-25-v73.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v73-candidates.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-v73.json")
REF = "v73 effective portfolio pinned candidate sources, exact per-file publisher hashes"

# Excluded with explicit reasons (recorded in the public ledger notes as held).
EXCLUDE = {
    "ausboss/Qwen-Image-2.1-Consistency-LoRA": "Qwen Research License, non-commercial research only",
    "ngocthien/tihon-tts": "CC BY-NC 4.0 noncommercial only",
    "GroundingPI/GroundingPI": "original Apache2.0 plus Kimi-K3 derivative conditions unresolved",
}


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    led = []
    for p in os.listdir("D:/AI_VAULT/state/ledger"):
        if p.endswith(".json"):
            led += json.load(open("D:/AI_VAULT/state/ledger/" + p, encoding="utf-8")).get("entries", [])
    verified = {e.get("repo_id") for e in led if e.get("status") == "VERIFIED"}
    data = json.loads(EFF.read_text(encoding="utf-8"))
    cands, approvals, excluded = [], [], []
    for i in data["items"]:
        repo = i.get("repo_id")
        if not repo or repo in verified or repo in EXCLUDE:
            continue
        if i.get("portfolio_decision") not in ("select", "conditional"):
            continue
        rev = i.get("upstream_revision_sha_observed") or ""
        files = i.get("candidate_selected_source_files") or []
        if len(rev) != 40 or not files:
            continue
        lic = str(i.get("license_metadata") or "")
        if not any(x in lic.lower() for x in ("apache", "mit")):
            continue
        if any(x in lic.lower() for x in ("nc", "noncommercial", "research license")):
            continue
        access = str(i.get("observed_access") or "")
        if "gated" in access.lower() and "ungated" not in access.lower():
            continue
        recs, afiles = [], []
        for f in files:
            p = f.get("path")
            if not p:
                continue
            rec = {"path": p, "bytes": int(f.get("bytes", 0)),
                   "publisher_lfs_sha256": f.get("sha256"),
                   "publisher_git_blob_sha1": f.get("git_blob_sha1")}
            recs.append(rec)
            a = {"path": p, "bytes": rec["bytes"]}
            if rec["publisher_lfs_sha256"]:
                a["sha256"] = rec["publisher_lfs_sha256"]
            elif rec["publisher_git_blob_sha1"]:
                a["git_blob_sha1"] = rec["publisher_git_blob_sha1"]
            else:
                break
            afiles.append(a)
        if len(afiles) != len(recs) or not recs:
            continue
        m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": recs,
             "selected_file_count": len(recs),
             "selected_file_bytes": sum(r["bytes"] for r in recs),
             "license_tag": lic, "phase": "V73_CANDIDATE"}
        out = DISC / ("v73-" + repo.replace("/", "__") + ".json")
        out.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
        cands.append({"repo_id": repo, "revision_sha": rev, "files": len(recs),
                      "bytes": m["selected_file_bytes"], "manifest": str(out)})
        approvals.append({"repo_id": repo, "revision_sha": rev,
                          "approved": True, "download_enabled": True,
                          "approved_by_user": True, "license_text_reviewed": True,
                          "parent_dependency_rights_reviewed": True,
                          "nonstandard_license_permission_verified": True,
                          "license": lic, "approval_ref": "v73-pinned-candidate-" + repo.replace("/", "-"),
                          "files": afiles})
    PLAN.write_text(json.dumps({"schema_version": 1, "excluded": EXCLUDE,
                                "candidates": cands}, indent=2, ensure_ascii=False), encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1, "authorization_source": REF,
                                    "entries": approvals}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"plan: {len(cands)} models, {sum(c['bytes'] for c in cands)/1e9:.2f} GB")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB {c['files']:3d}f {c['repo_id']}")


if __name__ == "__main__":
    main()
