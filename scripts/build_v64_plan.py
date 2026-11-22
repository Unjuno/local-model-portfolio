#!/usr/bin/env python3
"""R156 fail-closed static source review from the post-112 Pico INT8 and Toto4M delta.

Does NOT create an approved*.json file or infer owner/license approvals. No
network, model execution, model downloads, or change to the owner model store.
Do not run historical R152 as a new download queue: 13 of 14 scopes are
already reported VERIFIED in the acquisition ledger.
"""
import json
from pathlib import Path

QUEUE = Path("queues/proposed-v65-r156-toto4m-pico8-UNAPPROVED.json")
SOURCE = Path("manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json")
LEDGER = Path("catalog/execution/2026-11-19-acquisition-ledger.json")
HISTORICAL_QUEUE = Path("queues/proposed-v64-r152-post99-13-plus-bison-research-only.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v65-r156-RESEARCH-ONLY.json"
APPROVAL = DISC / "review-v65-r156-UNAPPROVED.json"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _identity_file(f):
    p = f["path"]
    if (not p or p.startswith("/") or "\\" in p or
            any(part in ("", ".", "..") for part in p.split("/"))):
        raise ValueError("unsafe source path")
    if not isinstance(f["bytes"], int) or f["bytes"] <= 0:
        raise ValueError("invalid source size")
    h = f.get("publisher_lfs_sha256")
    g = f.get("publisher_git_blob_sha1")
    if h is not None and (len(h) != 64 or
                          any(c not in "0123456789abcdef" for c in h)):
        raise ValueError("invalid publisher LFS SHA")
    if not isinstance(g, str) or len(g) != 40 or any(c not in "0123456789abcdef" for c in g):
        raise ValueError("missing publisher Git blob ID")
    return {"path": p, "bytes": f["bytes"],
            "sha256": h, "git_blob_sha1": g}


def main():
    q = load(QUEUE)
    m = load(SOURCE)
    l = load(LEDGER)
    old = load(HISTORICAL_QUEUE)
    if q.get("legacy_14_source_reconciliation",{}).get("matched_previous_candidate_count") != 13:
        raise ValueError("stale post112 queue/expected dedup not satisfied")
    if (l["summary"]["models_verified"] != 112 or
            l["summary"]["files_verified_total"] != 1714 or
            l["summary"]["bytes_verified_total"] != 2020548143087):
        raise ValueError("ledger changed; refresh research and recheck")
    verified = {x["repo_id"]: x for x in l["models"] if x["status"] == "VERIFIED"}
    if len(verified) != 112:
        raise ValueError("duplicate receipt repo IDs")
    previous = old["candidate_research_only"]
    verified_previous = [x for x in previous
                         if x["repo_id"] in verified
                         and x["publisher_revision_sha"] == verified[x["repo_id"]]["revision_sha"]
                         and x["selected_file_count"] == verified[x["repo_id"]]["files_verified"]
                         and x["publisher_reference_bytes"] == verified[x["repo_id"]]["source_bytes"]]
    if len(previous) != 14 or len(verified_previous) != 13:
        raise ValueError("old R152 source/ledger SHA or count diverged; stop")
    if "Datadog/Toto-2.0-4m" in verified:
        raise ValueError("new Toto source is already VERIFIED; refresh before planning")
    sources = {x["repo_id"]: x for x in m["model_sources"]}
    sdelta = m["same_repo_complementary_trained_scope"]
    srepo = sdelta["repo_id"]
    assert srepo == "KittenML/kitten-tts-2-pico"
    if (verified[srepo]["revision_sha"] != sdelta["immutable_revision_sha"] or
            verified[srepo]["files_verified"] != 33):
        raise ValueError("Pico original scope changed")
    scratch = []
    review = []
    for x in q["research_priority_order"]:
        repo = x["repo_id"]
        if repo == srepo:
            files = sdelta["additional_files"]
            rev = sdelta["immutable_revision_sha"]
            status = "SAME_REPO_8_QAD_DELTA_ONLY"
        else:
            if repo in verified:
                raise ValueError("unexpected new repo is already acquired")
            model = sources[repo]
            rev = model["immutable_revision_sha"]
            files = model["file_scope"]
            status = "FIRST_TIME_PUBLISHER_FULL_SOURCE"
        if (len(rev) != 40 or
                sum(y["bytes"] for y in files) != x["publisher_reference_bytes"]):
            raise ValueError("source size or revision scope mismatch")
        items = [_identity_file(f) for f in files]
        if len({f["path"] for f in items}) != len(items):
            raise ValueError("duplicate path in selected scope")
        safe_name = repo.replace("/", "__")
        target = DISC / ("v65-r156-" + safe_name + ".json")
        extracted = {"repo_id": repo, "revision_sha": rev, "repo_type": "model",
                     "selected_files": items, "selected_file_count": len(items),
                     "selected_file_bytes": sum(f["bytes"] for f in items),
                     "source_status": status, "research_only": True,
                     "download_approved": False, "download_enabled": False,
                     "owner_local_sha_verified": False}
        scratch.append((target, extracted))
        review.append({"repo_id": repo, "revision_sha": rev,
                       "approved": False, "approved_by_user": False,
                       "download_enabled": False,
                       "license_text_reviewed": False,
                       "parent_dependency_rights_reviewed": False,
                       "nonstandard_license_permission_verified": False,
                       "approval_ref": None, "files": items,
                       "research_only": True})
    payload = {"schema_version": 1, "catalog_revision": "v65-20261122",
               "source": str(QUEUE), "candidates": [{"repo_id": x["repo_id"], "phase": x["phase"],
                  "selected_file_bytes":x["publisher_reference_bytes"],
                  "research_only":True,"download_approved":False} for x in q["research_priority_order"]],
               "download_enabled": False, "approved": False,
               "historical_13_matched_receipts_skipped": True,
               "owner_license_rights_verified": False}
    if sum(x["selected_file_bytes"] for x in payload["candidates"]) != 81355672:
        raise ValueError("new candidate totals changed")
    DISC.mkdir(parents=True, exist_ok=True)
    for path, data in scratch:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PLAN.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    APPROVAL.write_text(json.dumps({"schema_version":1,"kind":"UNAPPROVED_OWNER_REVIEW_TEMPLATE_ONLY",
                                    "entries":review,"approved":False,"download_enabled":False},
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R156 source research only: 2 scopes, 81355672 publisher reference bytes; previous 13 already archived; approvals=0")


if __name__ == "__main__":
    main()
