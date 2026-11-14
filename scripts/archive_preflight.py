#!/usr/bin/env python3
"""Offline, read-only R21 archive probe. Python >=3.10; stdlib only.

Does not download, install, execute models, write, delete or authorize files.
--hash streams each mapped local file (can take time on HDD).
This scan is not atomic if a different process changes the filesystem.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "manifests/drafts/round21-pinned-preservation.candidate.json"
# The repository policy is authoritative. Never silently restore an outdated
# archival cap when the owner has revised policies/limits.json.
_LIMITS = json.loads((ROOT / "policies" / "limits.json").read_text(encoding="utf-8"))
DEFAULT_ARCHIVE_TARGET = _LIMITS["archive_target_bytes"]
DEFAULT_FREE_FLOOR = _LIMITS["minimum_free_bytes"]

def _safe_relative_path(value: str) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        return False
    pp = PurePosixPath(value)
    return not pp.is_absolute() and all(x not in ("", ".", "..") for x in value.split("/"))

def audit_source_manifest(plan: dict[str, Any]) -> list[str]:
    errors = []
    if not isinstance(plan, dict):
        return ["manifest not an object"]
    for flag in ("executable", "approved_manifest", "download_authorized", "auto_execute", "auto_seed"):
        if plan.get(flag) is not False:
            errors.append("non-executable flag violated: " + flag)
    repos, packages = plan.get("repositories"), plan.get("packages")
    if not isinstance(repos, list) or not isinstance(packages, list):
        return errors + ["repositories/packages must be arrays"]
    keys, ids, by_key = set(), set(), {}
    for r in repos:
        if not isinstance(r, dict):
            errors.append("repo not object")
            continue
        key, rid, rev = r.get("key"), r.get("repo_id"), r.get("revision")
        if not isinstance(key, str) or not key or key in keys:
            errors.append("duplicate/invalid repo key")
        else:
            keys.add(key)
            by_key[key] = r
        if not isinstance(rid, str) or rid in ids or not rid:
            errors.append("duplicate/invalid repo id")
        else:
            ids.add(rid)
        if not isinstance(rev, str) or not re.fullmatch("[0-9a-f]{40}", rev):
            errors.append("invalid revision: " + str(key))
        files = r.get("files")
        if not isinstance(files, list) or not files:
            errors.append("empty file list: " + str(key))
            continue
        paths, total = set(), 0
        for f in files:
            if not isinstance(f, dict):
                errors.append("bad file in " + str(key))
                continue
            path, n, sha, blob = f.get("path"), f.get("bytes"), f.get("source_sha256"), f.get("git_blob_sha1")
            if not _safe_relative_path(path):
                errors.append("unsafe source path: " + str(path))
            if path in paths:
                errors.append("duplicate source path: " + str(path))
            paths.add(path)
            if not isinstance(n, int) or isinstance(n, bool) or n < 1:
                errors.append("invalid byte size: " + str(path))
            else:
                total += n
            if not isinstance(blob, str) or not re.fullmatch("[0-9a-f]{40}", blob):
                errors.append("invalid blob id: " + str(path))
            if sha is not None and (not isinstance(sha, str) or not re.fullmatch("[0-9a-f]{64}", sha)):
                errors.append("invalid payload SHA256: " + str(path))
            if f.get("role") == "weight" and not isinstance(sha, str):
                errors.append("weight without source SHA256: " + str(path))
        if r.get("file_count") != len(files) or r.get("selected_bytes") != total:
            errors.append("repo count or byte mismatch: " + str(key))
    all_refs, package_keys = set(), set()
    for p in packages:
        if not isinstance(p, dict):
            errors.append("package not object")
            continue
        k, refs = p.get("key"), p.get("repository_keys")
        if not isinstance(k, str) or k in package_keys:
            errors.append("duplicate package")
        package_keys.add(k)
        if not isinstance(refs, list) or not refs or len(set(refs)) != len(refs):
            errors.append("bad repo refs: " + str(k))
            continue
        if any(ref not in by_key for ref in refs):
            errors.append("unknown repo ref: " + str(k))
            continue
        if p.get("selected_model_and_support_bytes") != sum(by_key[ref]["selected_bytes"] for ref in refs):
            errors.append("package byte mismatch: " + str(k))
        all_refs.update(refs)
    if all_refs != keys:
        errors.append("unused repo or missing package mapping")
    return errors

def _safe_target(srcroot: Path, rel: str) -> Path:
    if not _safe_relative_path(rel):
        raise ValueError("unsafe path")
    root = srcroot.resolve(strict=True)
    candidate = root
    for component in rel.split("/"):
        candidate = candidate / component
        # Reject symlinks even when the target remains inside the archive:
        # checking only .resolve().is_relative_to(root) silently followed them.
        if candidate.is_symlink():
            raise ValueError("symlink within source file path")
    p = candidate.resolve(strict=False)
    if not p.is_relative_to(root):
        raise ValueError("symlink/junction escaped source root")
    return p

def _fingerprint_file(path: Path, size: int, source_sha256: str | None, git_blob_sha1: str | None) -> bool:
    """Compare payload SHA256, or the ordinary Git blob content SHA1 (not LFS pointer SHA1)."""
    try:
        if not path.is_file() or path.stat().st_size != size:
            return False
        h = hashlib.sha256() if source_sha256 is not None else hashlib.sha1()
        if source_sha256 is None:
            h.update(b"blob " + str(size).encode("ascii") + b"\0")
        with path.open("rb") as fh:
            while True:
                data = fh.read(4 * 1024 * 1024)
                if not data:
                    break
                h.update(data)
        return h.hexdigest() == (source_sha256 if source_sha256 is not None else git_blob_sha1)
    except (OSError, ValueError):
        return False

def inspect_archive(plan: dict[str, Any], archive_root: Path,
                    source_roots: dict[str, Path], *, hash_existing: bool = False,
                    staging_reserve_bytes: int | None = None,
                    existing_archive_bytes: int | None = None,
                    archive_target_bytes: int = DEFAULT_ARCHIVE_TARGET,
                    free_floor_bytes: int = DEFAULT_FREE_FLOOR) -> dict[str, Any]:
    """Only inspects; passing point-in-time storage math never approves acquisition."""
    problems = audit_source_manifest(plan)
    if problems:
        raise ValueError("invalid pinned manifest: " + "; ".join(problems[:12]))
    root = Path(archive_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("archive root must be an existing directory")
    for name, value in (("staging reserve", staging_reserve_bytes), ("existing archive", existing_archive_bytes)):
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            raise ValueError(name + " must be a nonnegative integer byte count")
    for name, value in (("archive target", archive_target_bytes), ("free floor", free_floor_bytes)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(name + " invalid")
    known_keys = {r["key"] for r in plan["repositories"]}
    if set(source_roots) - known_keys:
        raise ValueError("unknown source root keys")
    roots = {k: Path(v).resolve(strict=False) for k, v in source_roots.items()}
    if len({str(v) for v in roots.values()}) != len(roots):
        raise ValueError("duplicate source root mappings")
    result = {
        "schema_version": 1,
        "status": "READ_ONLY_EVIDENCE_NOT_ACQUISITION",
        "download_authorized": False, "model_executed": False,
        "data_changed": False, "network_used": False,
        "archive_root": str(root), "hash_existing": hash_existing,
        "source_roots": {}, "capacity": {},
        "limitations": [
            "Filesystem path and st_dev are not a confirmed physical disk serial number.",
            "Matching file hashes does not authorize downloading, executing or redistributing weights.",
            "Point-in-time disk values can change due to concurrent downloads.",
            "No full device survey, runtime benchmark, signed environment lock or owner approval performed."
        ]
    }
    confirmed_existing = 0
    for r in plan["repositories"]:
        key, selected = r["key"], r["selected_bytes"]
        mapped = roots.get(key)
        if mapped is None:
            result["source_roots"][key] = {"status": "UNMAPPED", "selected_bytes": selected,
                                           "inside_archive": False, "verified_files": 0, "matched_bytes": 0}
            continue
        try:
            same_volume = mapped.stat().st_dev == root.stat().st_dev
        except OSError:
            same_volume = False
        inside = bool(mapped.is_relative_to(root) and same_volume)
        if not mapped.is_dir():
            result["source_roots"][key] = {"status": "NOT_A_DIRECTORY", "selected_bytes": selected,
                                           "inside_archive": inside, "verified_files": 0, "matched_bytes": 0}
            continue
        verified, found, fully_matches, unsafe = 0, 0, True, False
        for f in r["files"]:
            try:
                path = _safe_target(mapped, f["path"])
            except (ValueError, OSError):
                unsafe, fully_matches = True, False
                break
            try:
                exists = path.is_file() and path.stat().st_size == f["bytes"]
            except OSError:
                exists = False
            if not exists:
                fully_matches = False
                continue
            found += 1
            if not hash_existing:
                continue
            if _fingerprint_file(path, f["bytes"], f.get("source_sha256"), f.get("git_blob_sha1")):
                verified += 1
            else:
                fully_matches = False
        status = ("UNSAFE_PATH" if unsafe else
                  "MISMATCH" if hash_existing and not fully_matches else
                  "FULLY_MATCHED" if hash_existing and verified == len(r["files"]) else
                  "SIZE_ONLY_UNVERIFIED" if not hash_existing and found == len(r["files"]) else
                  "PARTIAL_OR_MISSING")
        if status == "FULLY_MATCHED" and inside:
            confirmed_existing += selected
        result["source_roots"][key] = {
            "status": status, "selected_bytes": selected, "inside_archive": inside,
            "verified_files": verified, "matched_bytes": selected if status == "FULLY_MATCHED" else 0,
            "files_present_at_expected_size": found, "files_required": len(r["files"])
        }
    full = sum(r["selected_bytes"] for r in plan["repositories"])
    by_packages = sum(p["selected_model_and_support_bytes"] for p in plan["packages"])
    if full != by_packages:
        raise ValueError("overlapping package references double counted")
    incremental = full - confirmed_existing
    usage = shutil.disk_usage(root)
    physical = ("UNCERTAIN" if staging_reserve_bytes is None else
                "PASS" if usage.free - incremental - staging_reserve_bytes >= free_floor_bytes else "FAIL")
    budget = ("UNCERTAIN" if existing_archive_bytes is None else
              "PASS" if existing_archive_bytes + incremental <= archive_target_bytes else "FAIL")
    result["capacity"] = {
        "pinned_selected_bytes": full,
        "confirmed_reused_bytes": confirmed_existing,
        "new_payload_bytes_after_verified_reuse": incremental,
        "observed_disk_total_bytes": usage.total,
        "observed_disk_used_bytes": usage.used,
        "observed_disk_free_bytes": usage.free,
        "free_floor_bytes": free_floor_bytes,
        "staging_reserve_bytes": staging_reserve_bytes,
        "existing_archive_bytes": existing_archive_bytes,
        "archive_target_bytes": archive_target_bytes,
        "physical_gate": physical,
        "archive_budget_gate": budget,
        "overall_gate": ("PASS_POINT_IN_TIME_ONLY" if physical == "PASS" and budget == "PASS" else
                         "FAIL" if physical == "FAIL" or budget == "FAIL" else "UNCERTAIN"),
        "final_manifest_approved": False,
        "real_download_permitted": False
    }
    return result

def _source_root_spec(spec: str) -> tuple[str, Path]:
    if "=" not in spec:
        raise ValueError("--source-root requires key=/path")
    key, path = spec.split("=", 1)
    if not key or not path:
        raise ValueError("invalid --source-root")
    return key, Path(path)

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive-root", type=Path, required=True, help="Existing archive directory (read-only)")
    ap.add_argument("--source-root", action="append", default=[], metavar="KEY=PATH",
                    help="Existing repository root; repeat for each repo")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--hash", action="store_true", help="Verify every mapped file checksum; may be slow on HDD")
    ap.add_argument("--staging-reserve-bytes", type=int, default=None,
                    help="Explicit reserve for temporary/cache use, omitted means UNCERTAIN")
    ap.add_argument("--existing-archive-bytes", type=int, default=None,
                    help="Measured current archive budget use, omitted means UNCERTAIN")
    args = ap.parse_args(argv)
    try:
        roots = dict(_source_root_spec(x) for x in args.source_root)
        if len(roots) != len(args.source_root):
            raise ValueError("duplicate source root key")
        plan = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = inspect_archive(plan, args.archive_root, roots,
                                 hash_existing=args.hash,
                                 staging_reserve_bytes=args.staging_reserve_bytes,
                                 existing_archive_bytes=args.existing_archive_bytes)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status":"ERROR_NOT_AUTHORIZED","download_authorized":False,
                          "reason":str(exc)},ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
