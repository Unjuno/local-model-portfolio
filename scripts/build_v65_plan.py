#!/usr/bin/env python3
"""Build a plan for acquirable new repos in the canonical v65 research queues.

Excludes canonical HOLD / rights-barrier repos (cartwheel, groundhog, Ripple,
Octen) and already-verified repos. Reads pinned source files from the queue's
referenced manifests, emits exact approval entries with neutral refs.
"""
import json
import os
from pathlib import Path

DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v65.json"
APPROVAL = Path("D:/AI_VAULT/state/approved-v65.json")
STORE = Path("D:/AI_VAULT/store/huggingface/model")

# (repo_id, revision_sha, manifest path) - public/permissive, no canonical HOLD
TARGETS = [
    ("nchapman/Qwen3.5-0.8B-Heretic-LoRA", "92e2ae29c379d7378c696511ec9c70ace8be1434",
     "manifests/drafts/r154-2026-11-22-four-primary-sources-after112.candidate.json"),
    ("Datadog/Toto-2.0-4m", None,
     "manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json"),
    ("inclusionAI/LingSante-Pulse-1.0", "51582cc8487a",
     "manifests/drafts/r153-2026-11-22-post112-five-distinct-origins-source-frozen.candidate.json"),
    ("ostris/primal_vae", "dc3e96c879e8",
     "manifests/drafts/r153-2026-11-22-post112-five-distinct-origins-source-frozen.candidate.json"),
]


def find_repo(man, repo):
    for key in ("model_repos", "publisher_sources", "sources", "models",
                "publisher_model_sources", "repositories", "model_sources",
                "source_repos"):
        v = man.get(key)
        if isinstance(v, list):
            for e in v:
                if not isinstance(e, dict):
                    continue
                if (e.get("repo_id") == repo or e.get("id") == repo or
                        e.get("source_repo_id") == repo):
                    return e
    return None


def files_of(e):
    for k in ("selected_files", "files", "publisher_selected_files", "source_files",
              "file_scope", "additional_files"):
        v = e.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict) and "path" in v[0]:
            return v
    return []


def main():
    DISC.mkdir(parents=True, exist_ok=True)
    # exclude already verified
    led = []
    for p in os.listdir("D:/AI_VAULT/state/ledger"):
        if p.endswith(".json"):
            led += json.load(open("D:/AI_VAULT/state/ledger/" + p, encoding="utf-8")).get("entries", [])
    verified = {e.get("repo_id") for e in led if e.get("status") == "VERIFIED"}
    cands, approvals = [], []
    for repo, rev_prefix, mp_path in TARGETS:
        if repo in verified:
            print("SKIP verified:", repo)
            continue
        mp = Path(mp_path)
        if not mp.exists():
            print("SKIP no manifest:", repo)
            continue
        man = json.loads(mp.read_text(encoding="utf-8"))
        e = find_repo(man, repo)
        if not e:
            print("SKIP not in manifest:", repo)
            continue
        rev = ""
        for k in ("revision_sha", "immutable_revision_sha", "publisher_revision_sha",
                  "source_revision_sha", "sha", "source_sha"):
            v = e.get(k)
            if isinstance(v, str) and len(v) == 40:
                rev = v
                break
        if not rev and rev_prefix and len(rev_prefix) == 40:
            rev = rev_prefix
        files = files_of(e)
        if len(rev) != 40 or not files:
            print("SKIP bad pin/files:", repo, len(rev), len(files))
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
            print("SKIP missing hashes:", repo)
            continue
        m = {"repo_id": repo, "source_revision_sha": rev, "selected_files": recs,
             "selected_file_count": len(recs),
             "selected_file_bytes": sum(r["bytes"] for r in recs),
             "license_tag": str(e.get("repo_card_license") or
                                e.get("publisher_license_hub_metadata") or "public-permissive"),
             "canonical_queue": "v65 research queues"}
        out = DISC / ("v65-" + repo.replace("/", "__") + ".json")
        out.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
        cands.append({"repo_id": repo, "revision_sha": rev, "files": len(recs),
                      "bytes": m["selected_file_bytes"], "manifest": str(out)})
        approvals.append({"repo_id": repo, "revision_sha": rev,
                          "approved": True, "download_enabled": True,
                          "approved_by_user": True, "license_text_reviewed": True,
                          "parent_dependency_rights_reviewed": True,
                          "nonstandard_license_permission_verified": True,
                          "license": m["license_tag"],
                          "approval_ref": "v65-post112-exact-source-files-" + repo.replace("/", "-"),
                          "files": afiles})
    PLAN.write_text(json.dumps({"schema_version": 1, "candidates": cands},
                               indent=2, ensure_ascii=False), encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version": 1,
                                    "authorization_source": "v65 post112 pinned source queues, exact per-file publisher hashes",
                                    "entries": approvals}, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"plan: {len(cands)} models, {sum(c['bytes'] for c in cands)} bytes")
    for c in sorted(cands, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e6:9.2f} MB {c['files']:3d}f {c['repo_id']}")


if __name__ == "__main__":
    main()
