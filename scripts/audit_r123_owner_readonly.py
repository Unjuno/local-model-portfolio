#!/usr/bin/env python3
"""Read-only verifier for R123 source file reuse on an owner's archive volume.

No network, downloads, publisher code execution, file writes, or approvals.
Python >= 3.10, stdlib only. A historic ledger SHA match is never a local PASS.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sys

DEFAULT_MANIFEST = "catalog/decisions/2026-11-20-r123-v52-delta-aware-17-source-preservation.json"
FLOOR_BYTES = 200_000_000_000
CHUNK = 4 * 1024 * 1024
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REV = re.compile(r"^[a-f0-9]{40}$")
SHA = re.compile(r"^[a-f0-9]{64}$")
BLOB = re.compile(r"^[a-f0-9]{40}$")
WINDOWS_BAD = re.compile(r'[<>:"|?*\\\x00-\x1f]')
RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}


def safe_rel(name: str) -> tuple[str, ...]:
    if not isinstance(name, str) or not name or WINDOWS_BAD.search(name):
        raise ValueError("Unsafe Windows path")
    p = PurePosixPath(name)
    if p.is_absolute() or str(p) != name or any(x in ("", ".", "..") for x in name.split("/")):
        raise ValueError("Unsafe relative path")
    for part in p.parts:
        if part.rstrip(" .") != part or part.split(".", 1)[0].upper() in RESERVED:
            raise ValueError("Nonportable Windows path")
    return p.parts


def locations(root: Path, repo_id: str, revision: str, rel: str, repo_type: str) -> list[Path]:
    if not REPO.fullmatch(repo_id) or not REV.fullmatch(revision):
        raise ValueError("Invalid immutable source identifier")
    if repo_type not in ("model", "dataset"):
        raise ValueError("Unsupported repository type")
    author, name = repo_id.split("/", 1)
    leaf = safe_rel(rel)
    prefixes = [root / ("datasets" if repo_type == "dataset" else "models") / author / name,
                root / author / name,
                root / "downloads" / author / name,
                root / ("datasets" if repo_type == "dataset" else "models") / name]
    result = []
    for p in prefixes:
        result.append(p.joinpath(*leaf))
        result.append((p / revision).joinpath(*leaf))
    return list(dict.fromkeys(result))


def no_symlink_between(root: Path, path: Path) -> bool:
    try:
        if not path.resolve(strict=False).is_relative_to(root.resolve(strict=True)):
            return False
    except (ValueError, OSError):
        return False
    cursor = path
    while cursor != root:
        if cursor.is_symlink():
            return False
        cursor = cursor.parent
    return not root.is_symlink()


def fingerprint(path: Path, expected_bytes: int, sha256: str | None, git_blob_sha1: str | None) -> tuple[bool, str]:
    if type(expected_bytes) is not int or expected_bytes < 0:
        raise ValueError("Invalid expected bytes")
    if sha256 is not None and not SHA.fullmatch(sha256):
        raise ValueError("Invalid SHA256")
    if git_blob_sha1 is not None and not BLOB.fullmatch(git_blob_sha1):
        raise ValueError("Invalid Git blob SHA1")
    if not sha256 and not git_blob_sha1:
        raise ValueError("Publisher integrity evidence is missing")
    if not path.is_file() or path.is_symlink():
        return False, "NOT_REGULAR"
    if path.stat().st_size != expected_bytes:
        return False, "SIZE_MISMATCH"
    digest = hashlib.sha256() if sha256 else hashlib.sha1()
    if not sha256:
        digest.update(f"blob {expected_bytes}\0".encode("ascii"))
    with path.open("rb") as stream:
        while block := stream.read(CHUNK):
            digest.update(block)
    if path.stat().st_size != expected_bytes:
        return False, "CHANGED_WHILE_READING"
    expect = sha256 or git_blob_sha1
    return (digest.hexdigest() == expect, "VERIFIED" if digest.hexdigest() == expect else "HASH_MISMATCH")


def audit(manifest: dict, root: Path, *, check_all: bool = False, only_repos: set[str] | None = None) -> dict:
    if manifest.get("canonical_revision") != "v52-20261119":
        raise ValueError("Not canonical v52 R123")
    sources = manifest.get("source_repositories")
    if not isinstance(sources, list) or len(sources) != 17:
        raise ValueError("Expected 17 immutable source repositories")
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Archive root does not exist or is a symlink")
    root = root.resolve(strict=True)
    result = []
    for source in sources:
        repo_id = source["repo_id"]
        if only_repos is not None and repo_id not in only_repos:
            continue
        for item in source["source_files"]:
            if not check_all and not item["prior_61_reported_content_hash_match"]:
                continue
            checked = []
            for location in locations(root, repo_id, source["source_revision"], item["path"], source["repository_type"]):
                if not location.exists() and not location.is_symlink():
                    continue
                if not no_symlink_between(root, location):
                    checked.append((str(location), "UNSAFE_SYMLINK_OR_ESCAPE"))
                    continue
                try:
                    ok, status = fingerprint(location, item["bytes"], item.get("sha256"), item.get("git_blob_sha1"))
                except (OSError, ValueError) as error:
                    status, ok = "READ_ERROR:" + type(error).__name__, False
                checked.append((str(location), status))
            state = ("UNLOCATED_IN_KNOWN_LAYOUTS" if not checked else
                     "CONFLICT" if any(x[1] != "VERIFIED" for x in checked) else "VERIFIED_ON_OWNER_VOLUME")
            result.append({"repo_id": repo_id, "path": item["path"], "bytes": item["bytes"],
                           "historical_sha_match": bool(item["prior_61_reported_content_hash_match"]),
                           "state": state, "locations": checked})
    counts = {state: sum(x["state"] == state for x in result) for state in
              ("VERIFIED_ON_OWNER_VOLUME", "UNLOCATED_IN_KNOWN_LAYOUTS", "CONFLICT")}
    free = shutil.disk_usage(root).free
    return {"mode": "ALL" if check_all else "HISTORICAL_SHA_MATCHES_ONLY",
            "file_count": len(result), "status_counts": counts,
            "verified_bytes_on_this_volume": sum(x["bytes"] for x in result if x["state"] == "VERIFIED_ON_OWNER_VOLUME"),
            "free_bytes_at_audit_time": free, "minimum_free_floor_bytes": FLOOR_BYTES,
            "passes_free_floor_at_audit_time": free >= FLOOR_BYTES,
            "no_downloads_performed": True, "not_a_full_offline_model_restore": True,
            "results": result}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", default=DEFAULT_MANIFEST)
    p.add_argument("--root", required=True, help="Mounted archive directory, e.g. D:\\AI-Models")
    p.add_argument("--check-all", action="store_true", help="Hash all selected files (373 total); default only 20 historical matches")
    p.add_argument("--repo-id", action="append", help="Restrict to one or several source repo IDs")
    args = p.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    result = audit(manifest, Path(args.root), check_all=args.check_all,
                   only_repos=set(args.repo_id) if args.repo_id else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["status_counts"]["CONFLICT"] else 0


if __name__ == "__main__":
    sys.exit(main())
