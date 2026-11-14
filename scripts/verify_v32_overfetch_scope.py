#!/usr/bin/env python3
"""Read-only validator for the R74 v32 exact-file selection candidate.

Python >=3.10; stdlib only. Does not use the network, download, execute
model code, accept licenses, or modify the approved queue.
This does not establish lawful acquisition or complete offline restoration.
"""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = "manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json"
IDENTITIES = "catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json"
APPROVED = "queues/approved.json"

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
REPO_ID = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
UNSAFE_GLOB = set("*?[]")


def _fail(message: str) -> None:
    raise ValueError(message)


def _safe_literal_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    if any(ch in value for ch in UNSAFE_GLOB) or "\\" in value or ":" in value:
        return False
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return False
    return not PurePosixPath(value).is_absolute()


def validate(allowlist: dict, identities: dict, approved: dict) -> dict:
    """Validate immutable evidence against R73; never construct a download command."""
    for flag in (
        "executable", "approved_manifest", "download_authorized",
        "auto_execute", "auto_seed", "allow_full_repo_download",
    ):
        if allowlist.get(flag) is not False:
            _fail("candidate must be non-executable: " + flag)
    if approved.get("entries") != []:
        _fail("approved queue not empty")
    if allowlist.get("source_catalog_revision") != "v32-20261114":
        _fail("unexpected catalog revision")
    if identities.get("portfolio_revision") != "v32-20261114":
        _fail("unexpected identity-ledger revision")

    source_rows = identities.get("records")
    rows = allowlist.get("records")
    if not isinstance(rows, list) or not isinstance(source_rows, list):
        _fail("records missing")
    identity_by_key = {}
    for row in source_rows:
        key = (row["asset_kind"], row["repo_id"])
        if key in identity_by_key:
            _fail("duplicate R73 asset: " + str(key))
        identity_by_key[key] = row

    seen_keys = set()
    selected_files = 0
    selected_bytes = 0
    excess_bytes = 0
    unknown_payload_sha256 = 0
    identity_kinds = {"lfs_payload_sha256": 0, "git_blob_sha1": 0,
                      "unverifiable_payload_hash": 0}
    scope_delta_without_excluded_files = []

    for row in rows:
        key = (row.get("asset_kind"), row.get("repo_id"))
        if key in seen_keys:
            _fail("duplicate candidate asset: " + str(key))
        seen_keys.add(key)
        if key not in identity_by_key:
            _fail("candidate missing from R73: " + str(key))
        if key[0] not in ("model", "dataset") or not isinstance(key[1], str):
            _fail("invalid asset type or id")
        if not REPO_ID.fullmatch(key[1]):
            _fail("unsafe Hugging Face repository id: " + key[1])
        if not isinstance(row.get("revision_sha"), str) or not HEX40.fullmatch(row["revision_sha"]):
            _fail("invalid immutable revision: " + key[1])

        for flag in (
            "download_approved", "full_repo_snapshot_approved",
            "publisher_access_entitlement_verified",
            "licensed_for_owner_use_verified", "local_sha_verified",
            "allowlist_is_full_runtime_package",
        ):
            if row.get(flag) is not False:
                _fail("unverified entitlement, execution or restore: " + key[1] + " " + flag)
        if row.get("complete_file_allowlist_for_profile") is not True:
            _fail("incomplete selected-source profile: " + key[1])

        source = identity_by_key[key]
        if (row["revision_sha"] != source["source_revision"]
                or row["selected_file_bytes"] != source["selected_file_bytes"]
                or row["selected_file_count"] != source["selected_file_count"]
                or row["observed_publisher_repo_scope_bytes"]
                    != source["observed_upstream_repo_scope_bytes"]):
            _fail("R73 immutable source identity mismatch: " + key[1])

        files = row.get("files")
        if not isinstance(files, list) or not files:
            _fail("empty selection: " + key[1])
        seen_paths = set()
        row_bytes = 0
        row_unknown = 0
        for f in files:
            path = f.get("path")
            if not _safe_literal_path(path):
                _fail("unsafe/glob file path: " + str(path))
            if path in seen_paths:
                _fail("duplicate literal file path: " + key[1] + " " + path)
            seen_paths.add(path)
            n = f.get("bytes")
            if type(n) is not int or n <= 0:
                _fail("invalid file byte size: " + key[1] + " " + path)
            row_bytes += n
            sha = f.get("publisher_payload_sha256")
            git_blob = f.get("git_blob_sha1_reference")
            if not isinstance(git_blob, str) or not HEX40.fullmatch(git_blob):
                _fail("invalid published Git blob pointer: " + key[1] + " " + path)
            identity = f.get("identity_kind")
            if identity not in identity_kinds:
                _fail("unsupported source identity kind: " + key[1] + " " + path)
            identity_kinds[identity] += 1
            is_masked = f.get("publisher_payload_sha256_unverified")
            if identity == "lfs_payload_sha256":
                if not isinstance(sha, str) or not HEX64.fullmatch(sha) or is_masked is not False:
                    _fail("invalid publisher payload SHA: " + key[1] + " " + path)
            elif identity == "git_blob_sha1":
                if sha is not None or is_masked is not False:
                    _fail("Git blob is not a verified payload SHA: " + key[1] + " " + path)
            else:
                if sha is not None or is_masked is not True:
                    _fail("masked payload must stay unverified: " + key[1] + " " + path)
                row_unknown += 1

        if row_bytes != row["selected_file_bytes"] or len(files) != row["selected_file_count"]:
            _fail("source selection byte/count mismatch: " + key[1])
        if row_unknown != source["masked_payload_file_count"]:
            _fail("R73 masked payload count mismatch: " + key[1])
        observed = row["observed_publisher_repo_scope_bytes"]
        delta = observed - row_bytes
        if delta <= 0 or delta != row.get("excluded_repo_scope_bytes"):
            _fail("overfetch byte delta mismatch: " + key[1])
        excluded_count = row.get("source_excluded_file_count")
        if type(excluded_count) is not int or excluded_count < 0:
            _fail("invalid excluded file count: " + key[1])
        if excluded_count == 0:
            scope_delta_without_excluded_files.append({
                "repo_id": key[1],
                "observed_scope_delta_bytes": delta,
                "source_excluded_file_count": 0,
                "finding": "UNEXPLAINED_SOURCE_SCOPE_DELTA_NOT_INFERRED_FILES",
            })
        selected_files += len(files)
        selected_bytes += row_bytes
        unknown_payload_sha256 += row_unknown
        excess_bytes += delta

    s = allowlist.get("summary", {})
    if (len(rows), selected_files, unknown_payload_sha256, excess_bytes) != (
        s.get("repos_with_extra_upstream_scope"),
        s.get("selected_file_refs"),
        s.get("unverified_sha256_file_refs"),
        s.get("observed_upstream_extra_bytes_sum"),
    ):
        _fail("R74 summary mismatch")
    if (len(rows), selected_files, unknown_payload_sha256, excess_bytes) != (
        66, 1425, 80, 2_985_522_750_447
    ):
        _fail("unexpected R74 evidence baseline; review intentionally")
    if identity_kinds != {
        "lfs_payload_sha256": 491, "git_blob_sha1": 854,
        "unverifiable_payload_hash": 80
    }:
        _fail("unexpected publisher hash-identity distribution")

    return {
        "status": "PASS_PUBLISHER_SOURCE_SCOPE_ONLY",
        "download_authorized": False,
        "source_allowlist_repos": len(rows),
        "selected_file_refs": selected_files,
        "selected_file_bytes": selected_bytes,
        "observed_extra_source_bytes": excess_bytes,
        "masked_payload_sha256_refs": unknown_payload_sha256,
        "published_identity_kinds": identity_kinds,
        "scope_delta_without_excluded_files": scope_delta_without_excluded_files,
        "safe_as_download_authorization": False,
        "full_dependency_closure_verified": False,
        "owner_HDD_verified": False,
    }


def verify(root: Path = ROOT) -> dict:
    root = Path(root)
    return validate(
        json.loads((root / ALLOWLIST).read_text(encoding="utf-8")),
        json.loads((root / IDENTITIES).read_text(encoding="utf-8")),
        json.loads((root / APPROVED).read_text(encoding="utf-8")),
    )


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
