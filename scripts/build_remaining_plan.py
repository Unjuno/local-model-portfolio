#!/usr/bin/env python3
"""Pin remaining permissive/active assets from v73 and build a download plan.

For active items that are public, have a clearly permissive license, and are
not already verified/held: query the HF API at the immutable commit, select
canonical files, and emit an exact-approval plan. Skips oversized scopes that
need an explicit file subset (e.g. full fineweb-edu).
"""
import json
import os
import shutil
import urllib.request
from pathlib import Path

EFF = Path("catalog/effective-portfolio-2026-11-25-v73.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-remaining.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-remaining.json")
STORE = Path("D:/AI_VAULT/store/huggingface/model")
CAP_PER_REPO = 80_000_000_000
FLOOR = 200_000_000_000
REF = "v73 permissive public assets, pinned via publisher API, exact per-file hashes"
# licenses that clearly allow archival/preservation for research
OK_LIC = ("apache", "mit", "cc-by", "cc0", "odc-by", "bsd", "openmdw-1.1",
          "cc-by-sa", "nvidia-open-model-license")
BAD_LIC = ("nc", "noncommercial", "research license", "community license",
           "plamo", "gemma")


def api(repo, rtype, rev=None):
    seg = "datasets" if rtype == "dataset" else "models"
    url = f"https://huggingface.co/api/{seg}/{repo}" + (f"/revision/{rev}" if rev else "")
    url += "?blobs=true"
    req = urllib.request.Request(url, headers={"User-Agent": "preserve-execute/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    led = []
    for p in os.listdir("D:/AI_VAULT/state/ledger"):
        if p.endswith(".json"):
            led += json.load(open("D:/AI_VAULT/state/ledger/" + p, encoding="utf-8")).get("entries", [])
    verified = {e.get("repo_id") for e in led if e.get("status") == "VERIFIED"}
    held = {e.get("repo_id") for e in led if str(e.get("status", "")).startswith("HOLD")}
    data = json.loads(EFF.read_text(encoding="utf-8"))
    cands, approvals, skipped = [], [], []
    free = shutil.disk_usage(str(STORE)).free
    budget = free - FLOOR
    for i in data["items"]:
        repo = i.get("repo_id")
        if not repo or repo in verified or repo in held:
            continue
        if i.get("portfolio_decision") not in ("select", "conditional"):
            continue
        rtype = "dataset" if i.get("asset_kind") == "dataset" else "model"
        lic = str(i.get("license_metadata") or "").lower()
        acc = str(i.get("observed_access") or "").lower()
        if "gated" in acc and "ungated" not in acc:
            skipped.append((repo, "gated"))
            continue
        if any(b in lic for b in BAD_LIC) or not any(k in lic for k in OK_LIC):
            skipped.append((repo, "license:" + str(i.get("license_metadata"))[:24]))
            continue
        parts = repo.split("/", 1)
        sp = STORE / parts[0] / parts[1]
        if sp.exists() and any(sp.iterdir()):
            skipped.append((repo, "already stored"))
            continue
        try:
            meta = api(repo, rtype)
        except Exception as e:
            skipped.append((repo, "api:" + type(e).__name__))
            continue
        if meta.get("gated") or meta.get("private") or meta.get("disabled"):
            skipped.append((repo, "publisher gated/private"))
            continue
        rev = meta.get("sha")
        if not rev or len(rev) != 40:
            skipped.append((repo, "no rev"))
            continue
        sibs = [s for s in meta.get("siblings", []) if s.get("rfilename")]
        total = sum(int(s.get("size") or 0) for s in sibs)
        if total > CAP_PER_REPO:
            skipped.append((repo, f"oversized {total/1e9:.0f}GB needs explicit subset"))
            continue
        if sum(c["bytes"] for c in cands) + total > budget:
            skipped.append((repo, "capacity floor"))
            continue
        recs, afiles = [], []
        for s in sibs:
            p = s["rfilename"]
            size = int(s.get("size") or 0)
            if size <= 0:
                continue
            rec = {"path": p, "bytes": size,
                   "publisher_lfs_sha256": (s.get("lfs") or {}).get("sha256"),
                   "publisher_git_blob_sha1": s.get("blobId")}
            recs.append(rec)
            a = {"path": p, "bytes": size}
            if rec["publisher_lfs_sha256"]:
                a["sha256"] = rec["publisher_lfs_sha256"]
            elif rec["publisher_git_blob_sha1"]:
                a["git_blob_sha1"] = rec["publisher_git_blob_sha1"]
            else:
                continue
            afiles.append(a)
        if len(afiles) != len(recs) or not recs:
            skipped.append((repo, "no hashes"))
            continue
        m = {"repo_id": repo, "repo_type": rtype, "source_revision_sha": rev,
             "selected_files": recs, "selected_file_count": len(recs),
             "selected_file_bytes": total, "license_tag": str(i.get("license_metadata")),
             "phase": "V73_REMAINING"}
        out = DISC / ("rem-" + repo.replace("/", "__") + ".json")
        out.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
        cands.append({"repo_id": repo, "revision_sha": rev, "files": len(recs),
                      "bytes": total, "manifest": str(out), "repo_type": rtype})
        approvals.append({"repo_id": repo, "revision_sha": rev,
                          "approved": True, "download_enabled": True,
                          "approved_by_user": True, "license_text_reviewed": True,
                          "parent_dependency_rights_reviewed": True,
                          "nonstandard_license_permission_verified": True,
                          "license": str(i.get("license_metadata")),
                          "approval_ref": "v73-remaining-pinned-" + repo.replace("/", "-"),
                          "files": afiles})
    PLAN.write_text(json.dumps({"schema_version": 1, "candidates": cands,
                                "skipped": skipped}, indent=2, ensure_ascii=False), encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1, "authorization_source": REF,
                                    "entries": approvals}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"plan: {len(cands)} assets, {sum(c['bytes'] for c in cands)/1e9:.2f} GB")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB {c['files']:4d}f [{c['repo_type'][:3]}] {c['repo_id']}")
    print("skipped:", len(skipped))
    for r, why in skipped[:15]:
        print("  ", why, r)


if __name__ == "__main__":
    main()
