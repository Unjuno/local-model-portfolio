#!/usr/bin/env python3
"""Fail-closed, read-only verification of the 66 R74 historical selected-file allowlists.

No HTTP, model execution, installation, filesystem modifications, or downloads.
All byte counts refer to *publisher metadata*, not existing HDD contents.
Python >=3.10, standard library only.
"""
from __future__ import annotations

from collections import Counter
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json"
SOURCE = "catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json"
APPROVAL = "queues/approved.json"
HEX40 = re.compile(r"[a-f0-9]{40}")
HEX64 = re.compile(r"[a-f0-9]{64}")
GLOB = re.compile(r"[*?\[\]\\]")

def load(root: Path = ROOT) -> tuple[dict, dict, dict]:
    """Read repository-local evidence without network access or side effects."""
    return tuple(
        json.loads((root / p).read_text(encoding="utf-8"))
        for p in (MANIFEST, SOURCE, APPROVAL)
    )

def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def safe_filename(name: object) -> bool:
    """Explicit relative paths only; no globbing or traversal."""
    return (
        isinstance(name, str) and bool(name)
        and "\x00" not in name
        and ":" not in name
        and not name.startswith("/")
        and not GLOB.search(name)
        and all(part not in ("", ".", "..") for part in name.split("/"))
    )

def validate(
    draft: dict,
    source: dict,
    approvals: dict,
) -> dict:
    """Validate R74 file identities against the independent 135-row R73 index."""
    need(approvals.get("entries") == [], "approved queue is not empty")
    need(draft.get("source_catalog_revision") == "v32-20261114", "wrong R74 catalog")
    need(source.get("portfolio_revision") == "v32-20261114", "wrong R73 catalog")
    need(draft.get("historical_source_blob_sha") == source.get("input_blob_sha", {}).get("historical")
         and draft.get("historical_source_path") == source.get("input_paths", {}).get("historical"),
         "historical source blob provenance mismatch")
    for key in ("executable", "approved_manifest", "download_authorized",
                "auto_execute", "auto_seed", "allow_full_repo_download"):
        need(draft.get(key) is False, "unsafe draft flag: " + key)
    for key in ("requires_owner_specific_hub_entitlement",
                "requires_canonical_license_text_review",
                "requires_full_learned_runtime_dependencies",
                "requires_owner_disk_and_local_sha",
                "requires_final_selected_revision_review"):
        need(draft.get(key) is True, "missing required hard gate: " + key)
    summary = draft.get("summary", {})
    for key in ("fully_lawfully_downloadable_assets_confirmed",
                "owner_approved_downloads"):
        need(summary.get(key) == 0, "unsafe approval signal: " + key)

    coverage = source.get("records")
    need(isinstance(coverage, list) and len(coverage) == 135, "R73 must cover 135")
    reference = {}
    for row in coverage:
        key = (row.get("asset_kind"), row.get("repo_id"))
        need(key not in reference, "duplicate R73 identity: " + str(key))
        reference[key] = row

    records = draft.get("records")
    need(isinstance(records, list) and len(records) == 66, "R74 must contain 66")
    seen = set()
    count = Counter()
    observed_sum = selected_sum = excess_sum = max_excess = 0
    unattributed_excess = []
    for row in records:
        key = (row.get("asset_kind"), row.get("repo_id"))
        need(key not in seen, "duplicate R74 asset: " + str(key))
        seen.add(key)
        need(key in reference, "R74 source absent in R73: " + str(key))
        rid = row["repo_id"]
        need(row.get("asset_kind") in ("model", "dataset"), "bad asset kind: " + rid)
        need(isinstance(rid, str) and "/" in rid, "invalid repo ID: " + str(rid))
        revision = row.get("revision_sha")
        need(isinstance(revision, str) and HEX40.fullmatch(revision) is not None,
             "unfixed revision: " + rid)
        selected = row.get("selected_file_bytes")
        observed = row.get("observed_publisher_repo_scope_bytes")
        extra = row.get("excluded_repo_scope_bytes")
        need(all(type(n) is int and n > 0 for n in (selected, observed, extra)),
             "invalid source bytes: " + rid)
        need(observed - selected == extra, "unexplained byte arithmetic: " + rid)
        for field in ("complete_file_allowlist_for_profile",):
            need(row.get(field) is True, "allowlist not complete: " + rid)
        for field in ("allowlist_is_full_runtime_package",
                      "publisher_access_entitlement_verified",
                      "licensed_for_owner_use_verified", "local_sha_verified",
                      "download_approved", "full_repo_snapshot_approved"):
            need(row.get(field) is False, "unexpectedly approved: " + rid + " " + field)

        files = row.get("files")
        need(isinstance(files, list) and len(files) > 0, "empty file list: " + rid)
        need(row.get("selected_file_count") == len(files), "wrong file count: " + rid)
        paths = set()
        size = masked = 0
        for f in files:
            name = f.get("path")
            need(safe_filename(name), "unsafe filename: " + rid + " " + str(name))
            need(name not in paths, "duplicate filename: " + rid + " " + name)
            paths.add(name)
            n = f.get("bytes")
            need(type(n) is int and n >= 0, "invalid file bytes: " + rid + " " + name)
            sha1 = f.get("git_blob_sha1_reference")
            need(isinstance(sha1, str) and HEX40.fullmatch(sha1) is not None,
                 "bad Git blob identity: " + rid + " " + name)
            kind = f.get("identity_kind")
            if n == 0:
                need(kind == "git_blob_sha1" and sha1 == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
                     "invalid zero-byte Git blob identity: " + rid + " " + name)
            sha256 = f.get("publisher_payload_sha256")
            unknown = f.get("publisher_payload_sha256_unverified")
            if kind == "lfs_payload_sha256":
                need(isinstance(sha256, str) and HEX64.fullmatch(sha256) is not None
                     and unknown is False,
                     "bad LFS payload identity: " + rid + " " + name)
            elif kind == "git_blob_sha1":
                need(sha256 is None and unknown is False,
                     "Git blob must not be mislabelled as payload SHA: " + rid + " " + name)
            elif kind == "unverifiable_payload_hash":
                need(sha256 is None and unknown is True,
                     "masked payload must remain blocked: " + rid + " " + name)
                masked += 1
            else:
                raise ValueError("unrecognized hash identity kind: " + str(kind))
            count[kind] += 1
            size += n

        need(size == selected, "selected byte total mismatch: " + rid)
        original = reference[key]
        for actual, expected, label in (
            (revision, original.get("source_revision"), "revision"),
            (selected, original.get("selected_file_bytes"), "selected bytes"),
            (len(files), original.get("selected_file_count"), "selected files"),
            (masked, original.get("masked_payload_file_count"), "masked hashes"),
            (observed, original.get("observed_upstream_repo_scope_bytes"), "repo bytes"),
        ):
            need(actual == expected, "R73/R74 mismatch: " + rid + " " + label)

        excluded_files = row.get("source_excluded_file_count")
        need(type(excluded_files) is int and excluded_files >= 0,
             "bad excluded file count: " + rid)
        if excluded_files == 0:
            # An observed positive byte difference without a named excluded file
            # is an evidence-quality issue, not proof of a particular extra file.
            unattributed_excess.append({"repo_id": rid, "unattributed_bytes": extra})
        observed_sum += observed
        selected_sum += selected
        excess_sum += extra
        max_excess = max(max_excess, extra)

    need(len(seen) == summary.get("repos_with_extra_upstream_scope"),
         "R74 summary repo count mismatch")
    need(sum(count.values()) == summary.get("selected_file_refs"),
         "R74 summary file count mismatch")
    need(count["unverifiable_payload_hash"] == summary.get("unverified_sha256_file_refs"),
         "R74 summary masked-hash count mismatch")
    need(excess_sum == summary.get("observed_upstream_extra_bytes_sum"),
         "R74 summary overfetch bytes mismatch")
    need(max_excess == summary.get("max_single_repo_extra_bytes"),
         "R74 summary max excess mismatch")
    return {
        "status": "PASS_METADATA_CROSSCHECK_ONLY",
        "asset_count": len(seen),
        "file_refs": sum(count.values()),
        "hash_identity_counts": dict(sorted(count.items())),
        "observed_scope_bytes": observed_sum,
        "selected_scope_bytes": selected_sum,
        "overfetch_scope_difference_bytes": excess_sum,
        "unattributed_excess": unattributed_excess,
        "full_runtime_closed": False,
        "owner_disk_verified": False,
        "approved_download": False,
        "download_performed": False,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root")
    args = parser.parse_args()
    print(json.dumps(validate(*load(args.root)), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
