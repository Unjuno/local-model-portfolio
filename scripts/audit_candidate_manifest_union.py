#!/usr/bin/env python3
"""Read-only R40 cross-manifest reconciliation (metadata only).

- No downloading, writing, model loading, file deletion or user approval.
- Compares each selected source file with the archived pinned source manifest.
- Deduplicates ONLY non-null, identical publisher SHA-256 values with equal bytes.
- Does not prove full runnable dependency closure or physical disk savings.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = "catalog/research/2026-11-08-r40-cross-manifest-sha-union.json"


def read_repo_json(relative_path: str) -> dict[str, Any]:
    p = ROOT / relative_path
    if not p.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Path escapes repository")
    return json.loads(p.read_text(encoding="utf-8"))


def source_file_index(manifest_path: str) -> dict[tuple[str, str, str], tuple[int, str | None]]:
    """Map (repository, immutable revision, relative path) -> (bytes, SHA-256)."""
    x = read_repo_json(manifest_path)
    index: dict[tuple[str, str, str], tuple[int, str | None]] = {}

    def add(repo: str, rev: str, path: str, size: int, sha: str | None) -> None:
        key = (repo, rev, path)
        value = (size, sha)
        if key in index and index[key] != value:
            raise ValueError(f"Conflicting source metadata: {manifest_path} {key}")
        index[key] = value

    if manifest_path.endswith(("round21-pinned-preservation.candidate.json",
                               "r36-22-source-closure-weight-only.candidate.json")):
        for repo in x["repositories"]:
            for file in repo["files"]:
                add(repo["repo_id"], repo["revision"], file["path"],
                    file["bytes"], file.get("source_sha256"))

    elif manifest_path.endswith("round23-motion-avatar.candidate.json"):
        for package in x["packages"]:
            for file in package["weight_files"]:
                add(file["repo_id"], file["revision"], file["path"],
                    file["bytes"], file.get("source_sha256"))

    elif manifest_path.endswith("r39-backend-specific-large-sources.candidate.json"):
        for package in x["packages"]:
            for file in package["selected_files"]:
                add(package["repo_id"], package["revision"], file["path"],
                    file["bytes"], file.get("source_sha256"))

    elif manifest_path.endswith("r37-chatterbox-versioned-source-manifest.json"):
        v = x["multilingual_v3"]
        for file in v["selected_files"]:
            add(v["repo_id"], v["sha"], file["path"], file["bytes"], file.get("sha256"))

    elif manifest_path.endswith("r35-ltx-pinned-file-census.json"):
        chris = x["chris_component_alternatives"]
        repo_id = chris["source_repo_id"]
        rev = next(r["immutable_commit"] for r in x["repos"] if r["repo_id"] == repo_id)
        for file in chris["chosen_components"]:
            add(repo_id, rev, file["path"], file["bytes"], file.get("sha256"))
        stub = x["stuubs_trained_stages_and_formats"]
        for file in stub["files"]:
            add(stub["repo_id"], stub["immutable_commit"], file["file"],
                file["bytes"], file.get("sha256"))

    elif manifest_path.endswith("round19-media-evidence.candidate.json"):
        # Research-only checksum corroboration, not a selected package.
        pass

    else:
        source = x["source"]
        for file in x["files"]:
            add(source["repo_id"], source["revision_sha"], file["path"],
                file["size_bytes"], file.get("source_sha256"))
    return index


def aggregate(packages: list[dict[str, Any]]) -> dict[str, Any]:
    """Return metadata-only bytes; no inferences for missing SHA-256."""
    seen: dict[str, tuple[int, str, str, str]] = {}
    raw_bytes = 0
    repeated_bytes = 0
    repeats: list[dict[str, Any]] = []
    count = 0
    unknown_sha = 0
    for package in packages:
        for file in package["files"]:
            count += 1
            raw_bytes += file["bytes"]
            sha = file.get("source_sha256")
            if not sha:
                unknown_sha += 1
                continue
            if sha in seen:
                size, prior_package, prior_repo, prior_path = seen[sha]
                if file["bytes"] != size:
                    raise ValueError(f"SHA256 collision with different byte count: {sha}")
                repeated_bytes += size
                repeats.append({
                    "sha256": sha, "bytes": size,
                    "first_package": prior_package, "first_repo": prior_repo,
                    "first_path": prior_path, "later_package": package["package_id"],
                    "later_repo": file["repo_id"], "later_path": file["path"],
                })
            else:
                seen[sha] = (file["bytes"], package["package_id"],
                             file["repo_id"], file["path"])
    return {
        "package_count": len(packages),
        "file_references": count,
        "publisher_file_bytes_before_sha_reuse": raw_bytes,
        "publisher_sha_reusable_bytes": repeated_bytes,
        "publisher_sha_unique_bytes": raw_bytes - repeated_bytes,
        "sha_unknown_file_references": unknown_sha,
        "sha_known_distinct_file_content_count": len(seen),
        "publisher_sha_identical_repeated_files": repeats,
        "local_hash_confirmed": False,
        "physical_disk_savings_measured": False,
    }


def verify_report(report_path: str = DEFAULT_REPORT) -> dict[str, Any]:
    report = read_repo_json(report_path)
    sources = {p: source_file_index(p) for p in report["source_manifests"]}
    core = report["core_packages"]
    optional = report["optional_special_packages"]
    all_packs = core + optional
    if not all_packs or len({p["package_id"] for p in all_packs}) != len(all_packs):
        raise ValueError("Missing or duplicate package IDs")
    for package in all_packs:
        source = sources[package["origin"]]
        seen_paths: set[tuple[str, str, str]] = set()
        subtotal = 0
        for file in package["files"]:
            key = (file["repo_id"], file["revision"], file["path"])
            if key in seen_paths:
                raise ValueError(f"Duplicate path within {package['package_id']}: {key}")
            seen_paths.add(key)
            if key not in source:
                raise ValueError(f"Missing original pinned source: {package['package_id']} {key}")
            actual = (file["bytes"], file.get("source_sha256"))
            if actual != source[key]:
                raise ValueError(f"Source metadata drift: {package['package_id']} {key}")
            if file["body_downloaded"] or file["local_full_sha_verified"]:
                raise ValueError("Unverified model body marked downloaded or locally verified")
            subtotal += file["bytes"]
        if subtotal != package["total_file_bytes"] or len(seen_paths) != package["file_count"]:
            raise ValueError(f"Incorrect package file count or bytes: {package['package_id']}")
        if package["download_approved"] or package["fully_runtime_executable"]:
            raise ValueError("Research-only package represented as approved or executable")

    scenarios = [("core", core, report["core_statistics"]),
                 ("with_optional_special", all_packs,
                  report["with_optional_special_statistics"])]
    output = {}
    for name, packages, stored in scenarios:
        calc = aggregate(packages)
        field_map = {
            "package_count": "packages",
            "file_references": "source_file_references",
            "publisher_file_bytes_before_sha_reuse": "unreconciled_sum_file_bytes",
            "publisher_sha_reusable_bytes": "repeated_publisher_sha_total_bytes",
            "publisher_sha_unique_bytes": "deduplicated_publisher_hash_unique_bytes",
            "sha_unknown_file_references": "sha_unknown_file_refs",
            "sha_known_distinct_file_content_count": "sha_known_distinct_file_content_count",
        }
        for field, original in field_map.items():
            if calc[field] != stored[original]:
                raise ValueError(f"{name} drift: {field} {calc[field]} != {stored[original]}")
        if len(calc["publisher_sha_identical_repeated_files"]) != len(
                stored["sha_identical_file_overlaps"]):
            raise ValueError(f"{name} duplicate fingerprint count drift")
        output[name] = calc

    limits = read_repo_json("policies/limits.json")
    current = read_repo_json("catalog/CURRENT.json")
    queue = read_repo_json("queues/approved.json")
    if current["expected"]["tracked"] != 150 or current["expected"]["active"] != 105:
        raise ValueError("Catalog baseline changed; rebase R40 audit")
    if limits["archive_target_bytes"] != report["policy"]["user_archive_ceiling_bytes"]:
        raise ValueError("Archive policy cap drift")
    if limits["minimum_free_bytes"] != report["policy"]["minimum_physical_free_bytes"]:
        raise ValueError("Free-space floor drift")
    if queue["entries"] or not report["policy"]["not_a_final_approved_download_manifest"]:
        raise ValueError("Archive approval gate unexpectedly passed")
    return {"status": "PASS_PUBLISHER_METADATA_ONLY",
            "source_manifests": len(sources),
            "core": output["core"],
            "with_optional_special": output["with_optional_special"],
            "archive_complete": False, "download_authorized": False}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", default=DEFAULT_REPORT)
    args = p.parse_args()
    try:
        print(json.dumps(verify_report(args.report), ensure_ascii=False, indent=2))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
