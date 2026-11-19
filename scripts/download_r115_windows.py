#!/usr/bin/env python3
"""R115 immutable-source downloader for Windows D: (also works with --root on WSL).

Usage:
  py -3 -m pip install --upgrade huggingface_hub
  py -3 scripts/download_r115_windows.py                    # read-only PLAN
  py -3 scripts/download_r115_windows.py --dry-run          # read-only PLAN
  py -3 scripts/download_r115_windows.py --execute --max-models 1 --approval-file "owner-approved.json"
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v49-r119-next7-public-source-entries.json --dry-run
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v49-r119-next7-public-source-entries.json --execute --approval-file "owner-approved-r119.json"
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v50-r122-deduplicated-next15-sources.json --dry-run
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v50-r122-deduplicated-next15-sources.json --execute --approval-file "owner-approved-r122.json"
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v52-r125-ledger61-delta-next15.json --dry-run
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v52-r125-ledger61-delta-next15.json --execute --approval-file "owner-approved-r125.json"
  py -3 scripts/download_r115_windows.py --execute --recover-prior
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v54-r128-first-four-delta-source.json --dry-run
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v54-r128-first-four-delta-source.json --execute --approval-file owner-approved-r128.json
  py -3 scripts/download_r115_windows.py --manifest queues/proposed-v53-r126-aion-bf16-first-public-source.json --dry-run

Transfers require BOTH an explicit --execute invocation on the owner's Windows
system AND --approval-file containing separately approved exact source scopes.
A general chat/download-intent flag does NOT replace the repository's
require_user_approved_manifest policy. No unapproved model transfer is made.
Each file must have publisher integrity evidence, and local capacity/rights
preflight must pass. No interactive per-model prompt is generated.

The script never loads model files, executes publisher code, deletes files,
accepts gated terms, or publishes artifacts. Previously reported exact scopes
are not re-downloaded if unlocated unless --recover-prior is set.
A model is 'verified' only if
every selected file matches its publisher hash and size.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import time
from datetime import datetime, timezone

DEFAULT_MANIFEST = "queues/proposed-v48-r115-master-sources-16.json"
DEFAULT_ROOT = r"D:\AI-Models"
REPO_PATTERN = re.compile(r"^[\w.-]+/[\w.-]+$")
REV_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA1_PATTERN = re.compile(r"^[0-9a-f]{40}$")
CHUNK = 4 * 1024 * 1024


def validate_relpath(name: str) -> tuple[str, ...]:
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError(f"Unsafe repository path: {name!r}")
    posix = PurePosixPath(name)
    parts = posix.parts
    windows_forbidden = re.compile(r'[<>:"\\|?*\x00-\x1f]')
    windows_reserved = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", re.I)
    if (posix.is_absolute() or not parts
            or any(part in (".", "..") or windows_forbidden.search(part)
                   or windows_reserved.search(part) or part.endswith((".", " ")) for part in parts)):
        raise ValueError(f"Unsafe repository path: {name!r}")
    if name != str(posix):
        raise ValueError(f"Non-canonical repository path: {name!r}")
    return parts


def validate_manifest(manifest: dict) -> list[dict]:
    profiles = {
        "R115_CONSOLIDATED_CORRECTED_ARCHIVE_SOURCE_AND_UNATTENDED_PREFLIGHT":
            (16, 10, {"apache-2.0"}),
        "R119_CONSOLIDATED_CORRECTED_UNREPORTED_FIRST_WAVE":
            (7, 7, {"apache-2.0", "mit"}),
        "R122_V50_DEDUPLICATED_NEXT_WAVE_15_UNAPPROVED_SOURCE_SCOPES":
            (15, 15, {"apache-2.0", "mit", "cc-by-sa-4.0"}),
        "R125_V52_LEDGER61_DELTA_15_SOURCES_NO_AUTO_DOWNLOAD":
            (15, 15, {"apache-2.0", "mit", "cc-by-sa-4.0"}),
        "R126_V53_MICROSOFT_AION_ONE_ORIGINAL_SOURCE_NO_AUTO_DOWNLOAD":
            (1, 1, {"mit"}),
        "R128_V54_P0_FIRST_FOUR_UNAPPROVED_PUBLISHER_SOURCES":
            (4, 4, {"cc-by-sa-4.0", "apache-2.0", "mit"}),
    }
    if manifest.get("kind") not in profiles:
        raise ValueError("Unsupported fixed-publisher source manifest")
    expected_entries, expected_eligible, accepted_licenses = profiles[manifest["kind"]]
    items = manifest.get("entries")
    if not isinstance(items, list) or len(items) != expected_entries:
        raise ValueError(f"Expected {expected_entries} source entries")
    output = []
    seen_repos = set()
    for model in items:
        source = model.get("source_repo_id")
        revision = model.get("source_revision")
        repo_type = model.get("repository_type", "model")
        if repo_type not in ("model", "dataset"):
            raise ValueError(f"Invalid HF repo type: {source}: {repo_type}")
        if manifest.get("kind") in (
            "R122_V50_DEDUPLICATED_NEXT_WAVE_15_UNAPPROVED_SOURCE_SCOPES",
            "R125_V52_LEDGER61_DELTA_15_SOURCES_NO_AUTO_DOWNLOAD"
        ) and "repository_type" not in model:
            raise ValueError(f"Next-wave source missing explicit repository_type: {source}")
        if not isinstance(source, str) or not REPO_PATTERN.fullmatch(source):
            raise ValueError("Invalid repo ID")
        if not isinstance(revision, str) or not REV_PATTERN.fullmatch(revision):
            raise ValueError(f"Missing fixed revision: {source}")
        if source in seen_repos:
            raise ValueError(f"Duplicate source model: {source}")
        seen_repos.add(source)
        files = model.get("files")
        if not isinstance(files, list) or not files:
            raise ValueError(f"Empty file scope: {source}")
        seen_files = set()
        casefolded_files = set()
        size_sum = 0
        for item in files:
            path = item["path"]
            validate_relpath(path)
            if path in seen_files or path.casefold() in casefolded_files:
                raise ValueError(f"Duplicate or casefold-colliding source path: {source}/{path}")
            seen_files.add(path)
            casefolded_files.add(path.casefold())
            size = item.get("bytes")
            if type(size) is not int or size < 0:
                raise ValueError(f"Invalid expected size: {source}/{path}")
            sha256, gitsha = item.get("sha256"), item.get("git_blob_sha1")
            if sha256 is not None and (not isinstance(sha256, str) or
                                      not SHA256_PATTERN.fullmatch(sha256)):
                raise ValueError(f"Invalid publisher SHA256: {source}/{path}")
            if gitsha is not None and (not isinstance(gitsha, str) or
                                      not GIT_SHA1_PATTERN.fullmatch(gitsha)):
                raise ValueError(f"Invalid publisher blob SHA1: {source}/{path}")
            if not sha256 and not gitsha and model.get(
                    "eligible_for_unattended_archive_after_local_preflight"):
                raise ValueError(f"No publisher integrity evidence: {source}/{path}")
            size_sum += size
        if size_sum != model.get("source_bytes"):
            raise ValueError(f"Publisher source size mismatch: {source}")
        if model.get("eligible_for_unattended_archive_after_local_preflight"):
            observed_license = model.get("license_metadata")
            license_tag = observed_license
            if observed_license == "apache-2.0 author/model card no standalone LICENSE":
                # The publisher card advertises Apache-2.0, but this repo does not
                # contain standalone license text. Approval still needs rights review.
                license_tag = "apache-2.0"
            if model.get("gated") or license_tag not in accepted_licenses:
                raise ValueError(f"Unexpected gated access or unsupported license: {source}")
            if model.get("acquisition_decision") != "GO_AFTER_LOCAL_PREFLIGHT":
                raise ValueError(f"Unexpected first-wave decision: {source}")
            if license_tag != observed_license:
                validated = dict(model)
                validated["license_metadata"] = license_tag
                validated["original_license_metadata"] = observed_license
                validated["license_text_in_repo_verified"] = False
                output.append(validated)
            else:
                output.append(model)
    if len(output) != expected_eligible:
        raise ValueError(f"Expected exactly {expected_eligible} locally-preflighted candidates")
    if manifest["kind"] == "R122_V50_DEDUPLICATED_NEXT_WAVE_15_UNAPPROVED_SOURCE_SCOPES":
        file_count = sum(len(item["files"]) for item in output)
        lfs_count = sum(sum(f.get("sha256") is not None for f in item["files"]) for item in output)
        all_bytes = sum(item["source_bytes"] for item in output)
        if (file_count, lfs_count, all_bytes) != (332, 135, 374_701_109_177):
            raise ValueError("R122 immutable publisher source totals changed")
        if (manifest.get("file_count"), manifest.get("publisher_sha256_file_count"),
                manifest.get("total_candidate_source_bytes")) != (file_count, lfs_count, all_bytes):
            raise ValueError("R122 proposed queue header differs from actual source files")
        datasets = [x["source_repo_id"] for x in output if x.get("repository_type") == "dataset"]
        if set(datasets) != {"elyza/ELYZA-tasks-100", "CohereLabs/aya_dataset"}:
            raise ValueError("R122 exact dataset scope changed")
    if manifest["kind"] == "R125_V52_LEDGER61_DELTA_15_SOURCES_NO_AUTO_DOWNLOAD":
        nfiles = sum(len(x["files"]) for x in output)
        nshas = sum(sum(f.get("sha256") is not None for f in x["files"]) for x in output)
        nbytes = sum(x["source_bytes"] for x in output)
        if (nfiles, nshas, nbytes) != (287, 118, 327_549_073_014):
            raise ValueError("R125 static source totals drift")
        if (manifest.get("file_count"), manifest.get("publisher_sha256_file_count"),
                manifest.get("total_candidate_source_bytes")) != (nfiles, nshas, nbytes):
            raise ValueError("R125 header/source identity mismatch")
        supplements = {
            "RWKV/RWKV7-7.2B-20260805": (7, 337813, 3),
            "GSAI-ML/iLLaDA-8B-Base": (4, 28506, 5),
            "microsoft/TRELLIS.2-4B": (1, 1519, 9),
        }
        observed = set()
        for model in output:
            repo = model["source_repo_id"]
            req = model.get("prerequisite_weight_files", [])
            supplement = model.get("source_mode") == "INFERRED_MISSING_SIDECARS_WEIGHT_SHA_PRECHECK_REQUIRED"
            if supplement:
                observed.add(repo)
                if repo not in supplements:
                    raise ValueError("Unexpected R125 supplementary source")
                n, nbytes_expected, npr = supplements[repo]
                if (len(model["files"]), model["source_bytes"], len(req)) != (n, nbytes_expected, npr):
                    raise ValueError("R125 supplement scope drift")
                if model.get("prior_reported_scope", {}).get("source_revision") != model["source_revision"]:
                    raise ValueError("R125 prerequisite source revision mismatch")
                if (not req or len({f.get("path") for f in req}) != len(req)
                        or set(f.get("path") for f in req) & set(f["path"] for f in model["files"])):
                    raise ValueError("R125 prerequisite paths must be unique and disjoint")
                for file in req:
                    validate_relpath(file.get("path"))
                    if (type(file.get("bytes")) is not int or file["bytes"] < 1
                            or not isinstance(file.get("sha256"), str)
                            or not SHA256_PATTERN.fullmatch(file["sha256"])):
                        raise ValueError("R125 existing-weight prerequisite must have full publisher SHA256")
            elif req or model.get("source_mode") != "FULL_SOURCE_UNREPORTED_OR_DISTINCT_PRECISION_SCOPE":
                raise ValueError("R125 full source has unexpected prerequisites or source mode")
        if observed != set(supplements):
            raise ValueError("R125 missing exactly three nonredundant supplementary scopes")
        dataset_ids = {x["source_repo_id"] for x in output
                       if x.get("repository_type") == "dataset"}
        if dataset_ids != {"elyza/ELYZA-tasks-100", "CohereLabs/aya_dataset"}:
            raise ValueError("R125 exact dataset scope mismatch")
    if manifest["kind"] == "R126_V53_MICROSOFT_AION_ONE_ORIGINAL_SOURCE_NO_AUTO_DOWNLOAD":
        model = output[0]
        if (model["source_repo_id"] != "microsoft/Aion-1.0-Instruct-2.3B"
                or model["source_revision"] != "28902cbfd9f4e0347d6c853aa1301f5d559b2fc0"
                or model["source_bytes"] != 4_593_276_272
                or len(model["files"]) != 11
                or sum(f.get("sha256") is not None for f in model["files"]) != 2
                or manifest.get("total_candidate_source_bytes") != 4_593_276_272
                or manifest.get("file_count") != 11
                or manifest.get("publisher_sha256_file_count") != 2):
            raise ValueError("R126 Aion source exact publisher manifest drift")
    if manifest["kind"] == "R128_V54_P0_FIRST_FOUR_UNAPPROVED_PUBLISHER_SOURCES":
        expected_ids = (
            "elyza/ELYZA-tasks-100", "CohereLabs/aya_dataset",
            "Reson8/Rumble-2-Flash", "microsoft/Aion-1.0-Instruct-2.3B"
        )
        records = sorted(output, key=lambda item: item["order"])
        if tuple(x["source_repo_id"] for x in records) != expected_ids:
            raise ValueError("R128 source identities or ordered priority drift")
        if tuple(x.get("repository_type") for x in records) != (
                "dataset", "dataset", "model", "model"):
            raise ValueError("R128 model/dataset Hub namespace drift")
        nfiles = sum(len(x["files"]) for x in output)
        nshas = sum(sum(f.get("sha256") is not None for f in x["files"]) for x in output)
        nbytes = sum(x["source_bytes"] for x in output)
        if (nfiles, nshas, nbytes) != (101, 9, 6_127_042_272):
            raise ValueError("R128 immutable first four source totals drift")
        if (manifest.get("file_count"),
            manifest.get("publisher_sha256_file_count"),
            manifest.get("total_candidate_source_bytes")) != (nfiles, nshas, nbytes):
            raise ValueError("R128 manifest header/file set mismatch")

    return sorted(output, key=lambda item: item["order"])


def file_hashes(path: Path) -> tuple[int, str, str]:
    size = path.stat().st_size
    sha = hashlib.sha256()
    gitblob = hashlib.sha1()
    gitblob.update(f"blob {size}\0".encode("ascii"))
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(CHUNK)
            if not chunk:
                break
            sha.update(chunk)
            gitblob.update(chunk)
    return size, sha.hexdigest(), gitblob.hexdigest()


def verify_file(path: Path, item: dict) -> tuple[bool, str, str | None]:
    if not path.is_file() or path.is_symlink():
        return False, "not_regular_file", None
    try:
        if path.stat().st_size != item["bytes"]:
            return False, "size_mismatch", None
        size, actual_sha256, actual_gitsha = file_hashes(path)
        if size != item["bytes"]:
            return False, "size_changed_during_read", actual_sha256
        # LFS git blob SHAs refer to the *pointer*, not the resolved content.
        if item.get("sha256"):
            match = actual_sha256 == item["sha256"]
            return match, "verified_publisher_lfs_sha256" if match else "sha256_mismatch", actual_sha256
        match = actual_gitsha == item["git_blob_sha1"]
        return match, "verified_publisher_git_blob_sha1" if match else "git_blob_sha1_mismatch", actual_sha256
    except OSError as exc:
        return False, "filesystem_error:" + str(exc), None


def append_log(log_path: Path, payload: dict) -> None:
    payload = dict(payload)
    payload["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def check_destination(root: Path, destination: Path) -> None:
    anchor = root.resolve(strict=True)
    resolved = destination.resolve(strict=False)
    if not resolved.is_relative_to(anchor):
        raise ValueError(f"Destination escapes archive root: {destination}")
    cursor = destination
    while cursor != root:
        if cursor.is_symlink():
            raise ValueError(f"Symlink inside destination is unsupported: {cursor}")
        cursor = cursor.parent


def get_free_bytes(root: Path) -> int:
    return shutil.disk_usage(root).free


def conservative_staging_bytes(largest_file_bytes: int) -> int:
    """Reserve cache/temp copies in addition to final destination file bytes.

    Hugging Face may stage a full LFS object or another complete copy, even
    when the final file is written into local_dir. This is deliberately stricter
    than the old largest_file_bytes // 4 approximation and remains only a
    planning bound, not proof that actual disk/codec/runtime staging fits.
    """
    if type(largest_file_bytes) is not int or largest_file_bytes < 0:
        raise ValueError("Invalid largest publisher file size")
    return max(2_000_000_000, 2 * largest_file_bytes)


def select_existing_destination(root: Path, repo: str, files: list[dict],
                                repository_type: str = "model") -> Path:
    """Prefer previously saved publisher content. Keep datasets out of the model namespace."""
    author, name = repo.split("/", 1)
    if repository_type == "dataset":
        candidates = [root / "datasets" / author / name,
                      root / "downloads" / "datasets" / author / name,
                      root / "dataset" / author / name]
    elif repository_type == "model":
        candidates = [root / "models" / author / name,
                      root / author / name,
                      root / "downloads" / author / name,
                      root / "models" / name,
                      root / name]
    else:
        raise ValueError("Invalid repository_type for destination selection")
    best = candidates[0]
    best_matches = 0
    for candidate in candidates:
        try:
            check_destination(root, candidate)
        except ValueError:
            continue
        matches = 0
        for spec in files:
            fp = candidate.joinpath(*validate_relpath(spec["path"]))
            try:
                if fp.is_file() and not fp.is_symlink() and fp.stat().st_size == spec["bytes"]:
                    matches += 1
            except OSError:
                pass
        if matches > best_matches:
            best, best_matches = candidate, matches
    return best


def inspect_existing_weight_prerequisites(root: Path, destination: Path,
                                          prerequisites: list[dict]) -> list[tuple[str, str]]:
    """Read-only publisher-SHA check of already archived model weights.

    The function never downloads or executes weight/pickle content. Rejection
    requires no network call. Never convert a metadata-only claim into an
    actual offline-restore verification.
    """
    invalid = []
    for item in prerequisites:
        path = destination.joinpath(*validate_relpath(item["path"]))
        check_destination(root, path)
        ok, reason, _ = verify_file(path, item)
        if not ok:
            invalid.append((item["path"], reason))
    return invalid


def source_fingerprint(model: dict) -> str:
    """Hash immutable source revision and the selected files/bytes/publisher hashes."""
    selected = {
        "source_repo_id": model["source_repo_id"],
        "source_revision": model["source_revision"],
        "files": sorted(({
            "path": item["path"], "bytes": item["bytes"],
            "sha256": item.get("sha256"),
            "git_blob_sha1": item.get("git_blob_sha1"),
        } for item in model["files"]), key=lambda item: item["path"]),
    }
    if model.get("repository_type", "model") == "dataset":
        selected["repository_type"] = "dataset"  # Prevent model/dataset namespace approval collision.
    if model.get("prerequisite_weight_files"):
        # Protect prerequisite weight identities under the same explicit user approval.
        selected["source_mode"] = model.get("source_mode")
        selected["prerequisite_weight_files"] = sorted(({
            "path": item["path"], "bytes": item["bytes"],
            "sha256": item["sha256"], "git_blob_sha1": item.get("git_blob_sha1"),
        } for item in model["prerequisite_weight_files"]), key=lambda item: item["path"])
    canonical = json.dumps(selected, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def hub_download_selected(hub_download, model: dict, filename: str, destination: Path):
    """Download a single pinned file, keeping dataset and model Hub namespaces distinct."""
    repository_type = model.get("repository_type", "model")
    if repository_type not in ("model", "dataset"):
        raise ValueError("Invalid Hub source repository type")
    return hub_download(repo_id=model["source_repo_id"], filename=filename,
                        revision=model["source_revision"], local_dir=str(destination),
                        repo_type=repository_type)


def assert_explicit_approved_sources(models: list[dict], approval_file: Path) -> None:
    """Fail closed before creating directories/caches or contacting the Hub."""
    if not approval_file.is_file():
        raise ValueError(f"Approved queue not present: {approval_file}")
    approvals = json.loads(approval_file.read_text(encoding="utf-8"))
    if not isinstance(approvals, dict) or approvals.get("schema_version") != 1:
        raise ValueError("Invalid approved queue schema")
    entries = approvals.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("No explicitly approved source manifests in queues/approved.json")
    approved = {}
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("Invalid approval record")
        repo = item.get("source_repo_id")
        if not isinstance(repo, str) or not REPO_PATTERN.fullmatch(repo) or repo in approved:
            raise ValueError("Duplicate or invalid approved source repo")
        approved[repo] = item
    for model in models:
        repo = model["source_repo_id"]
        entry = approved.get(repo)
        expected = source_fingerprint(model)
        if not entry or any((
            entry.get("approved") is not True,
            entry.get("user_explicit_manifest_consent") is not True,
            entry.get("license_and_parent_rights_reviewed") is not True,
            entry.get("owner_archive_volume_verified") is not True,
            entry.get("source_revision") != model["source_revision"],
            entry.get("source_scope_sha256") != expected,
        )):
            raise ValueError(f"Missing exact, rights-checked user-approved manifest: {repo}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--dry-run", action="store_true", help="Explicit read-only planning mode")
    parser.add_argument("--execute", action="store_true", help="Download frozen eligible public sources after owner D-drive preflight")
    parser.add_argument("--approval-file", default=None,
                        help="Required with --execute: exact source-scope, rights-checked owner approval JSON")
    parser.add_argument("--recover-prior", action="store_true",
                        help="Allow reacquisition of a previously VERIFIED-reported scope if missing locally")
    parser.add_argument("--max-models", type=int, default=0,
                        help="Process first N eligible models, 0 = all")
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()
    if args.max_models < 0 or args.retries < 1:
        parser.error("max-models must be >=0 and retries >=1")

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected = validate_manifest(manifest)
    if args.max_models:
        selected = selected[:args.max_models]
    if args.execute and args.dry_run:
        parser.error("--execute and --dry-run are mutually exclusive")
    if args.execute:
        if not (manifest.get("user_general_download_intent_recorded") is True and
                manifest.get("all_go_files_have_publisher_hash") is True):
            parser.error("Publisher-fixed source or user download intent missing")
        if args.approval_file is None:
            parser.error("--execute requires --approval-file with owner-approved exact source scopes")
        try:
            assert_explicit_approved_sources(selected, Path(args.approval_file))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parser.error("Execution not authorized: " + str(exc))

    root = Path(args.root)
    if os.name == "nt" and root.drive.upper() != "D:":
        parser.error("This manifest defaults to D:; pass an explicit D: archive root")
    if not root.anchor or not Path(root.anchor).is_dir():
        parser.error(f"Archive drive not mounted or accessible: {root.anchor}")
    if root.is_symlink():
        parser.error("Archive root cannot be a symlink")
    if not root.is_dir():
        if not args.execute:
            print(f"[DRY RUN] Would create {root}")
        else:
            root.mkdir(parents=True, exist_ok=True)
    disk_probe = root if root.exists() else Path(root.anchor)
    floor = int(manifest["required_free_floor_bytes"])
    if floor < 200_000_000_000:
        raise ValueError("Archive safety floor below policy")

    if not args.execute:
        for model in selected:
            print("PLAN", model["source_repo_id"], model["source_revision"],
                  model["source_bytes"], "bytes", len(model["files"]), "files",
                  "SOURCE_SCOPE_SHA256", source_fingerprint(model))
        print("FREE_BYTES", get_free_bytes(disk_probe), "FLOOR_BYTES", floor)
        return 0

    # Keep all Hugging Face temporary assets and state on D:, never C:.
    cache_root = root / ".hf-home"
    cache_root.mkdir(exist_ok=True)
    os.environ["HF_HOME"] = str(cache_root)
    os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "60")
    from huggingface_hub import hf_hub_download

    log_dir = root / "logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / "r115-download-ledger.jsonl"
    failed = 0
    completed = 0
    for model in selected:
        repo = model["source_repo_id"]
        revision = model["source_revision"]
        prereqs = model.get("prerequisite_weight_files", [])
        destination = select_existing_destination(root, repo, model["files"] + prereqs,
                                                  model.get("repository_type", "model"))
        check_destination(root, destination)
        if prereqs:
            invalid = inspect_existing_weight_prerequisites(root, destination, prereqs)
            if invalid:
                print("SKIP_PREREQUISITE_SHA", repo, len(invalid), "weight(s) not verified")
                append_log(log_path, dict(repo=repo, revision=revision,
                                          status="supplement_prerequisite_unverified",
                                          failures=invalid[:10], action="no_transfer"))
                failed += 1
                continue
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status="supplement_prerequisite_weight_sha_verified",
                                      files=len(prereqs)))
        file_state = []
        collision = False
        for spec in model["files"]:
            path = destination.joinpath(*validate_relpath(spec["path"]))
            check_destination(root, path)
            if path.exists() or path.is_symlink():
                ok, status, digest = verify_file(path, spec)
                if ok:
                    append_log(log_path, dict(repo=repo, revision=revision,
                                              path=spec["path"], status="already_verified",
                                              sha256=digest, bytes=spec["bytes"]))
                else:
                    collision = True
                    append_log(log_path, dict(repo=repo, revision=revision,
                                              path=spec["path"], status="existing_conflict",
                                              reason=status))
                file_state.append((spec, ok))
            else:
                file_state.append((spec, False))
        if collision:
            print("SKIP_CONFLICT", repo, "existing files are never overwritten")
            failed += 1
            continue
        pending = [spec for spec, ok in file_state if not ok]
        if not pending:
            completed += 1
            print("SUPPLEMENT_ALREADY_VERIFIED" if prereqs else "VERIFIED_ALREADY", repo)
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status=("supplement_verified" if prereqs else "model_verified"),
                                      files=len(model["files"])))
            continue
        # The GitHub execution ledger claims some scopes have already been
        # verified. Do not re-download those automatically if their physical
        # files are not located below this archive root.
        if model.get("prior_ledger", {}).get("reported_verified_scope_match") and not args.recover_prior:
            print("SKIP_PRIOR_REPORTED_UNLOCATED", repo, len(pending), "file(s)")
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status="prior_report_not_physically_reverified",
                                      missing_file_count=len(pending),
                                      action="skip_duplicate_new_download"))
            failed += 1
            continue
        remaining_bytes = sum(x["bytes"] for x in pending)
        largest = max(x["bytes"] for x in pending)
        # Conservative headroom for concurrent temporary file and FS metadata.
        overhead_bytes = conservative_staging_bytes(largest)
        if get_free_bytes(root) < floor + remaining_bytes + overhead_bytes:
            print("SKIP_CAPACITY", repo, "required_bytes",
                  floor + remaining_bytes + overhead_bytes)
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status="skipped_insufficient_free_space",
                                      required_bytes=floor + remaining_bytes + overhead_bytes,
                                      observed_free_bytes=get_free_bytes(root)))
            failed += 1
            continue
        destination.mkdir(parents=True, exist_ok=True)
        model_failed = False
        for spec in pending:
            relpath = spec["path"]
            path = destination.joinpath(*validate_relpath(relpath))
            if get_free_bytes(root) < floor + spec["bytes"] + overhead_bytes:
                model_failed = True
                append_log(log_path, dict(repo=repo, revision=revision,
                                          path=relpath, status="skipped_capacity_mid_model"))
                break
            last_error = ""
            for attempt in range(args.retries):
                try:
                    hub_download_selected(hf_hub_download, model, relpath, destination)
                    ok, verified_how, digest = verify_file(path, spec)
                    if not ok:
                        last_error = f"hash verification failed: {verified_how}"
                        break  # Do not automatically overwrite a mismatching file.
                    append_log(log_path, dict(repo=repo, revision=revision,
                                              path=relpath, status="file_verified",
                                              sha256=digest, bytes=spec["bytes"]))
                    print("OK", repo, relpath)
                    last_error = ""
                    break
                except Exception as exc:
                    last_error = type(exc).__name__ + ": " + str(exc)
                    if attempt + 1 < args.retries:
                        time.sleep(min(2 ** attempt, 8))
            if last_error:
                model_failed = True
                print("FAILED", repo, relpath, last_error)
                append_log(log_path, dict(repo=repo, revision=revision,
                                          path=relpath, status="download_failed",
                                          reason=last_error))
                break
        if not model_failed:
            # Recheck all listed files, not just those freshly downloaded.
            model_failed = not all(verify_file(destination.joinpath(
                *validate_relpath(spec["path"])), spec)[0] for spec in model["files"])
        if model_failed:
            failed += 1
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status="model_incomplete"))
        else:
            completed += 1
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status=("supplement_verified" if prereqs else "model_verified"),
                                      files=len(model["files"]), bytes=model["source_bytes"]))
            print("SUPPLEMENT_VERIFIED" if prereqs else "MODEL_VERIFIED", repo, model["source_bytes"])
    print("DONE", "verified_models", completed, "incomplete_or_skipped", failed,
          "free_bytes", get_free_bytes(root), "ledger", log_path)
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
