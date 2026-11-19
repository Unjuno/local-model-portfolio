#!/usr/bin/env python3
"""R115 immutable-source downloader for Windows D: (also works with --root on WSL).

Usage:
  py -3 -m pip install --upgrade huggingface_hub
  py -3 scripts/download_r115_windows.py
  py -3 scripts/download_r115_windows.py --dry-run
  py -3 scripts/download_r115_windows.py --max-models 1

The script never loads model files, executes publisher code, deletes files,
accepts gated terms, or publishes artifacts. A model is 'verified' only if
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
    if posix.is_absolute() or not parts or any(part in (".", "..") for part in parts):
        raise ValueError(f"Unsafe repository path: {name!r}")
    if name != str(posix):
        raise ValueError(f"Non-canonical repository path: {name!r}")
    return parts


def validate_manifest(manifest: dict) -> list[dict]:
    if manifest.get("kind") != "R115_CONSOLIDATED_CORRECTED_ARCHIVE_SOURCE_AND_UNATTENDED_PREFLIGHT":
        raise ValueError("Not an R115 master-source manifest")
    items = manifest.get("entries")
    if not isinstance(items, list) or len(items) != 16:
        raise ValueError("Expected 16 candidate entries")
    output = []
    seen_repos = set()
    for model in items:
        source = model.get("source_repo_id")
        revision = model.get("source_revision")
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
        size_sum = 0
        for item in files:
            path = item["path"]
            validate_relpath(path)
            if path in seen_files:
                raise ValueError(f"Duplicate source path: {source}/{path}")
            seen_files.add(path)
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
            if model.get("gated") or model.get("license_metadata") != "apache-2.0":
                raise ValueError(f"Unexpected access/license for first-wave: {source}")
            if model.get("acquisition_decision") != "GO_AFTER_LOCAL_PREFLIGHT":
                raise ValueError(f"Unexpected first-wave decision: {source}")
            output.append(model)
    if len(output) != 10:
        raise ValueError("Expected exactly 10 locally-preflighted candidates")
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--dry-run", action="store_true")
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

    root = Path(args.root)
    if os.name == "nt" and root.drive.upper() != "D:":
        parser.error("This manifest defaults to D:; pass an explicit D: archive root")
    if not root.anchor or not Path(root.anchor).is_dir():
        parser.error(f"Archive drive not mounted or accessible: {root.anchor}")
    if not root.is_dir():
        if args.dry_run:
            print(f"[DRY RUN] Would create {root}")
        else:
            root.mkdir(parents=True, exist_ok=True)
    disk_probe = root if root.exists() else Path(root.anchor)
    floor = int(manifest["required_free_floor_bytes"])
    if floor < 200_000_000_000:
        raise ValueError("Archive safety floor below policy")

    if args.dry_run:
        for model in selected:
            print("PLAN", model["source_repo_id"], model["source_revision"],
                  model["source_bytes"], "bytes", len(model["files"]), "files")
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
        author, short_name = repo.split("/", 1)
        destination = root / "models" / author / short_name
        check_destination(root, destination)
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
            print("VERIFIED_ALREADY", repo)
            append_log(log_path, dict(repo=repo, revision=revision,
                                      status="model_verified", files=len(model["files"])))
            continue
        remaining_bytes = sum(x["bytes"] for x in pending)
        largest = max(x["bytes"] for x in pending)
        # Conservative headroom for concurrent temporary file and FS metadata.
        overhead_bytes = max(2_000_000_000, largest // 4)
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
                    hf_hub_download(repo_id=repo, filename=relpath,
                                    revision=revision, local_dir=str(destination))
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
                                      status="model_verified", files=len(model["files"]),
                                      bytes=model["source_bytes"]))
            print("MODEL_VERIFIED", repo, model["source_bytes"])
    print("DONE", "verified_models", completed, "incomplete_or_skipped", failed,
          "free_bytes", get_free_bytes(root), "ledger", log_path)
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
