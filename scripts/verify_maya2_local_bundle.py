#!/usr/bin/env python3
"""Read-only Maya2 source-closure verification against pinned R59 metadata.

No network, model imports, unpickling, subprocesses or downloads. Checks files,
not runtime compatibility or legal rights. Rejects mutable symlinked file trees.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

EXPECTED = (
    "maya-research/maya2-native",
    "kyutai/mimi",
    "speechbrain/spkrec-ecapa-voxceleb",
)
DEFAULT_MANIFEST = (Path(__file__).resolve().parents[1] /
    "catalog/research/2026-11-14-r59-maya2-drama3-cross-repo-components.json")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CHUNK_BYTES = 4 * 1024 * 1024


class VerificationError(ValueError):
    """A required source file, manifest property or digest is invalid."""


def _nonnegative_int(n: Any) -> bool:
    return type(n) is int and n >= 0


def _selected_path(root: Path, rel: Any) -> Path:
    if not isinstance(rel, str) or not rel or "\\" in rel or "\x00" in rel:
        raise VerificationError(f"invalid manifest source path: {rel!r}")
    path = PurePosixPath(rel)
    if path.is_absolute() or any(part in (".", "..") for part in rel.split("/")) or path.as_posix() != rel:
        raise VerificationError(f"unsafe source path: {rel!r}")
    q = root
    for part in path.parts:
        q = q / part
        if q.is_symlink():
            raise VerificationError(f"symlink source entry not allowed: {rel}")
    try:
        if not q.is_file() or not stat.S_ISREG(q.stat().st_mode):
            raise VerificationError(f"missing regular source file: {rel}")
        q.relative_to(root)
    except (OSError, ValueError) as exc:
        raise VerificationError(f"source file escapes materialized root: {rel}") from exc
    return q


def _hash_file(path: Path, expected_size: int, lfs_sha: str | None, git_blob_sha: str | None) -> dict:
    if not _nonnegative_int(expected_size):
        raise VerificationError(f"invalid expected size: {path}")
    try:
        actual_size = path.stat().st_size
        if actual_size != expected_size:
            raise VerificationError(f"size mismatch for {path}: expected {expected_size}, observed {actual_size}")
        if lfs_sha is not None:
            if not isinstance(lfs_sha, str) or not HEX64.fullmatch(lfs_sha):
                raise VerificationError(f"invalid publisher SHA256: {path}")
            digest = hashlib.sha256()
            label, expected_hash = "SHA256", lfs_sha
        else:
            if not isinstance(git_blob_sha, str) or not HEX40.fullmatch(git_blob_sha):
                raise VerificationError(f"missing publisher Git blob SHA1: {path}")
            digest = hashlib.sha1()
            digest.update(f"blob {expected_size}\0".encode("ascii"))
            label, expected_hash = "Git blob SHA1", git_blob_sha
        with path.open("rb") as f:
            while chunk := f.read(CHUNK_BYTES):
                digest.update(chunk)
        got = digest.hexdigest()
        if got != expected_hash:
            raise VerificationError(f"{label} mismatch for {path}: expected {expected_hash}, got {got}")
        return {"size_bytes": expected_size, "hash_type": label, "hash_match": True, "hash_value": got}
    except OSError as exc:
        raise VerificationError(f"file inaccessible during verification: {path}: {exc}") from exc


def verify_bundle(manifest: Mapping[str, Any], roots: Mapping[str, str | Path]) -> dict:
    """Verify exactly the three R59 Maya2/Mimi/ECAPA source subsets.

    A fourth R59 source (Drama 3) is deliberately excluded. No model is run.
    """
    if not isinstance(manifest, dict) or manifest.get("formal_portfolio_revision") != "v32-20261114":
        raise VerificationError("expected the versioned v32 R59 source manifest")
    entries = manifest.get("source_scopes")
    if not isinstance(entries, list):
        raise VerificationError("missing source_scopes in manifest")
    if not isinstance(roots, Mapping) or set(roots) != set(EXPECTED):
        raise VerificationError("three explicitly mapped Maya2/Mimi/ECAPA source roots required")
    scopes: dict[str, dict] = {}
    for row in entries:
        if not isinstance(row, dict):
            raise VerificationError("invalid source scope record")
        rid = row.get("repo_id")
        if rid in EXPECTED:
            if rid in scopes:
                raise VerificationError(f"duplicate source scope: {rid}")
            scopes[rid] = row
    if set(scopes) != set(EXPECTED):
        raise VerificationError("Maya2/Mimi/ECAPA source manifests must all be present")
    out, total_files, total_bytes = [], 0, 0
    for repo in EXPECTED:
        row = scopes[repo]
        revision = row.get("immutable_revision_sha")
        if not isinstance(revision, str) or not HEX40.fullmatch(revision):
            raise VerificationError(f"source commit SHA is not pinned: {repo}")
        paths = row.get("files")
        if not isinstance(paths, list) or not paths:
            raise VerificationError(f"no files selected for {repo}")
        if row.get("selected_path_count") != len(paths):
            raise VerificationError(f"source file count inconsistent: {repo}")
        if not _nonnegative_int(row.get("selected_bytes")):
            raise VerificationError(f"invalid source byte total: {repo}")
        root = Path(roots[repo]).expanduser()
        if root.is_symlink() or not root.is_dir():
            raise VerificationError(f"source root must be a real directory (no symlink): {root}")
        root = root.resolve(strict=True)
        seen: set[str] = set()
        files = []
        checked_bytes = 0
        for item in paths:
            if not isinstance(item, dict):
                raise VerificationError(f"invalid source file entry: {repo}")
            name = item.get("path")
            q = _selected_path(root, name)
            if name in seen:
                raise VerificationError(f"duplicate source file: {repo}/{name}")
            seen.add(name)
            expected_bytes = item.get("size_bytes")
            verified = _hash_file(q, expected_bytes, item.get("publisher_lfs_sha256"), item.get("publisher_git_blob_sha1"))
            files.append({"path": name, **verified})
            checked_bytes += expected_bytes
        if checked_bytes != row["selected_bytes"]:
            raise VerificationError(f"source scope byte sum inconsistent: {repo}")
        out.append({"repo_id": repo, "pinned_publisher_revision": revision,
                    "verified_source_files": len(files), "verified_source_bytes": checked_bytes,
                    "files": files})
        total_files += len(files)
        total_bytes += checked_bytes
    return {
        "status": "SOURCE_FILES_MATCH_UPSTREAM_METADATA",
        "portfolio_revision": "v32-20261114",
        "repository_count": len(out), "file_count": total_files,
        "source_total_bytes": total_bytes, "repositories": out,
        "local_file_hashes_verified": True,
        "publisher_source_revision_filenames_attested": True,
        "download_authorized": False,
        "license_cleared_for_user": False,
        "safe_to_execute_model_code": False,
        "full_offline_runtime_verified": False,
        "tensor_payloads_loaded": False,
        "outstanding_gates": ["legal rights and user access", "Maya2 PyTorch/CUDA/Triton/Transformers ABI",
                              "all expected runtime model modes and model-code security", "physical free-space reserve"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--maya-root", type=Path, required=True)
    parser.add_argument("--mimi-root", type=Path, required=True)
    parser.add_argument("--ecapa-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = verify_bundle(manifest, dict(zip(EXPECTED, (args.maya_root, args.mimi_root, args.ecapa_root))))
        print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 0
    except (VerificationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "download_authorized": False, "error": str(exc)},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
