#!/usr/bin/env python3
"""Produce source-only v73 reviews. NEVER assert human consent or license approval.

R168/2026-11-27: older version generated approved-v73.json with true
approved_by_user/license_text_reviewed flags from model-card tags and file
metadata. A model card, repo path, or chat directive cannot authorize copying.
This version only writes UNAPPROVED reviews under discovered/ and never writes
D:/AI_VAULT/state/approved-v73.json. Existing old synthetic files (if any)
are not deleted here; preserve_execute.approval_for rejects their identifiers.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EFF = ROOT / "catalog/effective-portfolio-2026-11-25-v73.json"
LEDGER_DIR = Path("D:/AI_VAULT/state/ledger")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v73-candidates-UNAPPROVED.json"
REVIEW = DISC / "review-v73-candidates-UNAPPROVED.json"
REF = None

# These restrictions are *not* waived by model-card metadata alone.
EXCLUDE = {
    "ausboss/Qwen-Image-2.1-Consistency-LoRA": "Qwen Research License: per-act rights unresolved",
    "ngocthien/tihon-tts": "CC BY-NC 4.0 and third-party voice rights",
    "GroundingPI/GroundingPI": "training derivative rights unresolved"
}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def immutable_scope(files):
    """Return strict, non-executable publisher source metadata or None."""
    if not isinstance(files, list) or not files:
        return None
    result = []
    seen = set()
    for x in files:
        if not isinstance(x, dict):
            return None
        name, n = x.get("path"), x.get("bytes")
        if (not isinstance(name, str) or not name or name.startswith("/")
                or "\\" in name or any(z in ("", ".", "..") for z in name.split("/"))
                or name in seen or type(n) is not int or n <= 0):
            return None
        seen.add(name)
        sha = x.get("sha256") or x.get("publisher_lfs_sha256")
        blob = x.get("git_blob_sha1") or x.get("publisher_git_blob_sha1")
        if sha and not (isinstance(sha, str) and HEX64.fullmatch(sha)):
            return None
        if blob and not (isinstance(blob, str) and HEX40.fullmatch(blob)):
            return None
        if not sha and not blob:
            return None
        result.append({
            "path": name, "bytes": n,
            "sha256": sha or None, "git_blob_sha1": blob or None,
            "owner_local_SHA_verified": False
        })
    return result


def main():
    if not LEDGER_DIR.is_dir():
        raise ValueError("owner ledger directory not available; no plan may imply acquisition rights")
    if not EFF.is_file():
        raise ValueError("v73 exact materialized catalog unavailable")
    verified = set()
    for path in LEDGER_DIR.glob("*.json"):
        if path.is_symlink():
            raise ValueError("symlinked owner ledger not accepted")
        obj = json.loads(path.read_text(encoding="utf-8"))
        for row in obj.get("entries", []):
            if row.get("status") == "VERIFIED":
                verified.add(row.get("repo_id"))
    catalog = json.loads(EFF.read_text(encoding="utf-8"))
    if catalog.get("revision_id") != "v73-20261125":
        raise ValueError("stale v73 input; fail closed")
    candidates, templates, rejected = [], [], []
    for item in catalog.get("items", []):
        repo = item.get("repo_id")
        if repo in verified or item.get("portfolio_decision") not in ("select", "conditional"):
            continue
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            continue
        if repo in EXCLUDE:
            rejected.append({"repo_id": repo, "reason": EXCLUDE[repo]})
            continue
        rev = item.get("upstream_revision_sha_observed")
        if not isinstance(rev, str) or not HEX40.fullmatch(rev):
            continue
        allowed = immutable_scope(item.get("candidate_selected_source_files"))
        if allowed is None:
            continue
        access = (item.get("observed_access") or "").lower()
        if "gated" in access and "ungated" not in access:
            continue
        lic = str(item.get("license_metadata") or "")
        # Pre-screen only; a permissive *tag* does not prove the intended act.
        if not any(x in lic.lower() for x in ("apache", "mit", "bsd", "cc0")):
            continue
        if any(x in lic.lower() for x in ("noncommercial", "research license", "cc-by-nc")):
            continue
        entry = {
            "repo_id": repo, "source_revision_sha": rev,
            "selected_files": allowed,
            "selected_file_count": len(allowed),
            "selected_file_bytes": sum(x["bytes"] for x in allowed),
            "observed_license_metadata": lic,
            "publisher_scope_only": True,
            "download_enabled": False,
            "approved": False,
            "owner_rights_verified": False,
            "complete_offline_restore_verified": False,
            "source_status": "PUBLISHER_METADATA_ONLY_UNAPPROVED"
        }
        candidates.append(entry)
        templates.append({
            "repo_id": repo, "revision_sha": rev, "files": allowed,
            "approved": False, "download_enabled": False,
            "approved_by_user": False,
            "license_text_reviewed": False,
            "parent_dependency_rights_reviewed": False,
            "nonstandard_license_permission_verified": False,
            "approval_ref": None,
            "source": "machine-generated review template, not user approval"
        })
    result = {
        "schema_version": 1, "kind": "V73_SOURCE_ONLY_RESEARCH_UNAPPROVED",
        "catalog_revision": "v73-20261125", "approved": False,
        "download_enabled": False, "owner_download_approvals_added": 0,
        "excluded": EXCLUDE, "rights_review_held": rejected,
        "candidates": candidates,
        "warning": "No license metadata can establish user consent or intended-use rights"
    }
    review = {
        "schema_version": 1, "kind": "UNAPPROVED_OWNER_REVIEW_TEMPLATE",
        "authorization_source": None, "approved": False,
        "download_enabled": False, "entries": templates,
        "warning": "Cannot be used for acquisition without a distinct owner approval process"
    }
    DISC.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v73 source review: {len(candidates)} sources, {sum(x['selected_file_bytes'] for x in candidates)} reference bytes, 0 approvals, 0 model downloads")


if __name__ == "__main__":
    main()
