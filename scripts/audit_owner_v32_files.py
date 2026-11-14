#!/usr/bin/env python3
"""Verify already-owned v32 source files; no downloads, model code, or approval.

Python >=3.10 / stdlib. Explicit --asset-id only; no automatic 3+TB scan.
A matching hash proves only local file/source identity, not legal rights or runtime.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HEX40 = re.compile(r"^[a-f0-9]{40}$")
HEX64 = re.compile(r"^[a-f0-9]{64}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def load(root: Path, path: str) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def safe_relative(path: str) -> bool:
    return (isinstance(path, str) and bool(path) and "\\" not in path
            and ":" not in path and "\x00" not in path
            and all(part not in ("", ".", "..") for part in path.split("/")))


def normalized(path: str, n: int, sha: str | None, blob: str | None,
               *, kind: str | None = None) -> dict:
    if not safe_relative(path) or type(n) is not int or n < 0:
        raise ValueError("unsafe relative path or file size: " + repr(path))
    if sha is not None and not HEX64.fullmatch(sha):
        raise ValueError("invalid publisher SHA256: " + path)
    if blob is not None and not HEX40.fullmatch(blob):
        raise ValueError("invalid Git blob SHA1: " + path)
    # Git-LFS pointer SHA1 must not be compared to a raw weight payload.
    normal_git = kind == "git_blob_sha1" or (kind is None and sha is None)
    return {"path": path, "bytes": n, "sha256": sha,
            "git_blob_sha1": blob if normal_git else None}


def build_index(catalog: dict, v27: dict, r64: dict, r48: dict) -> dict:
    active = [x for x in catalog["items"] if x["portfolio_decision"] in ("select", "conditional")]
    if catalog["revision_id"] != "v32-20261114" or len(active) != 135:
        raise ValueError("requires the frozen v32 135-active source inventory")
    active_keys = {(x["asset_kind"], x["repo_id"]) for x in active}
    if len(active_keys) != 135:
        raise ValueError("duplicate formal asset ID")
    index: dict[str, dict] = {}

    def put(kind: str, repo: str, rev: str, files: list[dict], origin: str) -> None:
        if not REPO.fullmatch(repo) or not isinstance(rev, str) or not HEX40.fullmatch(rev):
            raise ValueError("unverified publisher repo revision: " + repo)
        if (kind, repo) not in active_keys or repo in index:
            raise ValueError("non-active or duplicate source repo: " + repo)
        if not files or len({f["path"] for f in files}) != len(files):
            raise ValueError("missing or duplicate file paths: " + repo)
        index[repo] = {"kind": kind, "repo_id": repo, "revision": rev,
                       "files": files, "evidence": origin}

    for row in v27["items"]:
        selected = [normalized(f["path"], f["bytes"], f.get("sha256"),
                               f.get("git_blob_sha1"), kind=f.get("identity_kind"))
                    for f in row["files"]]
        put(row["asset_kind"], row["repo_id"], row["source_revision"],
            selected, "V27_PUBLISHER_SOURCE_HISTORY")
    for row in r64["repositories"]:
        kind = row.get("repo_type", "model")
        if (kind, row["repo_id"]) not in active_keys:
            continue  # ACE-Step extra shared dependency is not a 136th asset.
        selected = [normalized(f["path"], f["bytes"], f.get("source_sha256"),
                               f.get("git_blob_sha1"))
                    for f in row["files"]]
        put(kind, row["repo_id"], row["revision"], selected, "R64_FIXED_SOURCE_SUBSET")
    z = next(s for s in r48["sources"] if s["repo_id"] == "Zyphra/ZONOS3-Mini")
    profile = next(p for p in r48["profiles"] if p["id"] == "zonos_native_keep2_reference_scope")
    if len(set(profile["file_indices"])) != 14 or len(profile["file_indices"]) != 14:
        raise ValueError("bad ZONOS14 file selection")
    selected = []
    for i in profile["file_indices"]:
        source_index, path, size, kind, digest = r48["files"][i]
        if source_index != 0 or kind not in ("G", "L"):
            raise ValueError("bad ZONOS source record")
        selected.append(normalized(path, size, digest if kind == "L" else None,
                                   digest if kind == "G" else None,
                                   kind="git_blob_sha1" if kind == "G" else "lfs_sha256"))
    if sum(f["bytes"] for f in selected) != profile["known_scope_bytes"]:
        raise ValueError("ZONOS selected byte mismatch")
    put("model", "Zyphra/ZONOS3-Mini", z["revision"], selected,
        "R48_REFERENCE_NOT_COMPLETE_RUNTIME")
    if len(index) != 135 or set(index) != {x["repo_id"] for x in active}:
        raise ValueError("incomplete 135-source inventory")
    return index


def local_source_file(root: Path, rel: str) -> Path:
    if not safe_relative(rel):
        raise ValueError("unsafe selected path")
    if not root.is_dir():
        raise FileNotFoundError("owner source directory absent")
    path = root
    for component in rel.split("/"):
        path = path / component
        if path.is_symlink():
            raise ValueError("symlink source path (even internal symlink)")
    if not path.resolve(strict=False).is_relative_to(root.resolve(strict=True)):
        raise ValueError("path escapes owner source")
    return path


def check_file(root: Path, f: dict) -> str:
    try:
        p = local_source_file(root, f["path"])
    except FileNotFoundError:
        return "MISSING"
    except (OSError, ValueError):
        return "UNSAFE_PATH"
    try:
        if not p.is_file():
            return "MISSING"
        if p.stat().st_size != f["bytes"]:
            return "BAD_SIZE"
        expected_sha, expected_blob = f.get("sha256"), f.get("git_blob_sha1")
        if expected_sha is None and expected_blob is None:
            return "PUBLISHER_HASH_UNKNOWN"
        h = hashlib.sha256() if expected_sha else hashlib.sha1()
        if not expected_sha:
            h.update(b"blob " + str(f["bytes"]).encode("ascii") + b"\0")
        with p.open("rb") as stream:
            while True:
                block = stream.read(4 * 1024 * 1024)
                if not block:
                    break
                h.update(block)
        return "MATCHED" if h.hexdigest() == (expected_sha or expected_blob) else "BAD_HASH"
    except OSError:
        return "READ_ERROR"


def inspect_asset(archive: Path, asset: dict, source_root: Path | None = None) -> dict:
    loc = (source_root if source_root is not None else
           archive / "store" / "huggingface" / asset["kind"] / asset["repo_id"] / asset["revision"])
    counts: dict[str, int] = {}
    for file in asset["files"]:
        code = check_file(loc, file)
        counts[code] = counts.get(code, 0) + 1
    matched = counts.get("MATCHED", 0) == len(asset["files"])
    return {"repo_id": asset["repo_id"], "source_file_references": len(asset["files"]),
            "source": asset["evidence"], "checks": counts,
            "all_selected_file_hashes_match": matched,
            "legal_acquisition_rights_passed": False, "offline_reconstruction_test_passed": False,
            "status": "SOURCE_HASHES_MATCH_ONLY" if matched else "INCOMPLETE_OR_UNKNOWN"}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog-root", type=Path, default=ROOT)
    p.add_argument("--archive-root", type=Path, required=True,
                   help="Existing owner archive root; never created by this program")
    p.add_argument("--asset-id", action="append", required=True,
                   help="Exact one v32 active HF repo ID; repeat explicitly if desired")
    p.add_argument("--source-root", action="append", default=[], metavar="REPO_ID=LOCAL_DIR",
                   help="Already-owned local repo dir, useful for existing HF cache layout; repeat")
    args = p.parse_args()
    idx = build_index(
        load(args.catalog_root, "catalog/effective-portfolio-2026-11-14-v32.json"),
        load(args.catalog_root, "catalog/capacity/2026-11-07/v27/selected-file-capacity.json"),
        load(args.catalog_root, "manifests/drafts/r64-eight-source-scopes.candidate.json"),
        load(args.catalog_root, "catalog/research/2026-11-12-r48-pinned-scopes.json")
    )
    if not args.archive_root.is_dir():
        raise ValueError("owner archive root is absent; do not create or download")
    if len(set(args.asset_id)) != len(args.asset_id) or any(k not in idx for k in args.asset_id):
        raise ValueError("non-active/unknown or repeated asset ID")
    overrides: dict[str, Path] = {}
    for spec in args.source_root:
        if "=" not in spec:
            raise ValueError("--source-root requires REPO_ID=LOCAL_DIR")
        repo, directory = spec.split("=", 1)
        if repo in overrides or repo not in args.asset_id or not directory:
            raise ValueError("duplicate, unselected or empty --source-root")
        overrides[repo] = Path(directory)
    rows = [inspect_asset(args.archive_root, idx[k], overrides.get(k))
            for k in args.asset_id]
    print(json.dumps({"schema_version":1,"scope":"LOCAL_FILES_ONLY",
                      "network_used":False, "downloads_authorized":False,
                      "models_executed":False,"files_modified":False,
                      "physical_4TB_capacity_gate":"NOT_VERIFIED",
                      "legal_and_gate_entitlement":"NOT_VERIFIED",
                      "results":rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
