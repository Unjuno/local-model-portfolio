#!/usr/bin/env python3
"""Read-only v46/R108 source-file and 4TB-storage preflight (Python >=3.10).

No network calls, no model loading, no downloads and no permission changes.
A PASS here confirms publisher metadata consistency, not authorization to acquire.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/drafts/r107-v45-12-original-sources-file-freeze.candidate.json"
PROPOSED = ROOT / "queues/proposed-v46-r108-source-pinned-12.json"
APPROVED = ROOT / "queues/approved.json"
LIMITS = ROOT / "policies/limits.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value or ":" in value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and all(s not in ("", ".", "..") for s in value.split("/"))


def validate(manifest, queue, approved, policy):
    errors, rows, sha_by_key = [], [], {}
    models = manifest.get("selected_models", [])
    entries = queue.get("entries", [])
    if manifest.get("count") != 12 or len(models) != 12 or len(entries) != 12:
        errors.append("Expected exactly 12 models and queue entries")
    if approved.get("entries") != []:
        errors.append("Approved queue changed: no automated acquisition is allowed")
    by_queue = {entry.get("repo_id"): entry for entry in entries}
    if len(by_queue) != len(entries):
        errors.append("Duplicate queue repository ID")
    ids = set()
    total = file_count = sha_count = 0
    for model in models:
        rid = model.get("repo_id")
        rev = model.get("immutable_revision")
        if not isinstance(rid, str) or rid in ids or rid.count("/") != 1:
            errors.append("Missing or duplicate model ID: " + str(rid))
            continue
        ids.add(rid)
        if not isinstance(rev, str) or not re.fullmatch(r"[0-9a-f]{40}", rev):
            errors.append("Invalid immutable revision: " + rid)
        if model.get("download_approved") is not False or model.get("payload_downloaded") is not False:
            errors.append("Unsafe acquired/approved claim: " + rid)
        files = model.get("selected_original_files", [])
        if not isinstance(files, list) or not files:
            errors.append("Missing selected files: " + rid)
            continue
        file_ids = set()
        sub_total = sub_sha = 0
        queue_row = by_queue.get(rid, {})
        qfiles = {f.get("path"): f for f in queue_row.get("files", [])}
        if len(qfiles) != len(files) or queue_row.get("source_revision") != rev:
            errors.append("Queue source/revision drift: " + rid)
        for f in files:
            rel, n = f.get("path"), f.get("source_bytes")
            sha, blob = f.get("source_sha256"), f.get("source_git_blob_sha1")
            if not safe_path(rel) or rel in file_ids:
                errors.append("Unsafe/duplicate file path: " + rid + " " + str(rel))
                continue
            file_ids.add(rel)
            if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
                errors.append("Invalid source bytes: " + rid + " " + rel)
                continue
            sub_total += n
            if not isinstance(blob, str) or not re.fullmatch(r"[0-9a-f]{40}", blob):
                errors.append("Missing git blob identity: " + rid + " " + rel)
            if sha is not None:
                if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
                    errors.append("Invalid LFS SHA256: " + rid + " " + rel)
                else:
                    sub_sha += 1
                    fingerprint = sha_by_key.get(sha)
                    if fingerprint is not None and fingerprint != n:
                        errors.append("Same LFS hash with different byte count")
                    sha_by_key[sha] = n
            if re.search(r"\.(gguf|safetensors|pt|pth|onnx|bin)$", rel, re.I) and sha is None:
                errors.append("Learned binary without publisher SHA256: " + rid + " " + rel)
            q = qfiles.get(rel)
            if q is None or q.get("bytes") != n or q.get("sha256") != sha:
                errors.append("Queue file differs from frozen source: " + rid + " " + rel)
        if sub_total != model.get("selected_source_bytes") or len(files) != model.get("selected_file_count"):
            errors.append("Source byte/file-count mismatch: " + rid)
        if sub_sha < model.get("selected_learned_weight_count", 0):
            errors.append("Not all learned weights have SHA256: " + rid)
        if queue_row.get("download_approved") is not False:
            errors.append("Proposed queue incorrectly approved: " + rid)
        rows.append({"repo_id": rid, "revision": rev, "bytes": sub_total,
                     "files": files, "publisher_sha256_files": sub_sha,
                     "gated": bool(model.get("gated_state"))})
        total += sub_total
        file_count += len(files)
        sha_count += sub_sha
    if set(by_queue) != ids:
        errors.append("Queue and frozen model-ID sets differ")
    if (total != 206683452429 or file_count != 131 or sha_count != 50
            or manifest.get("aggregate_selected_source_bytes") != total
            or queue.get("total_publisher_source_bytes") != total
            or queue.get("source_file_count") != file_count
            or queue.get("publisher_sha256_entries") != sha_count):
        errors.append("Aggregate source metadata differs from R108 verified baseline")
    if policy.get("archive_target_bytes") != 4000000000000:
        errors.append("Unexpected policy archive ceiling")
    if policy.get("minimum_free_bytes") != 200000000000:
        errors.append("Unexpected policy minimum free-space floor")
    return errors, rows


def get_local(root, row, rel):
    # Never follow a symlink from the selected archive root through any file path.
    base = root / row["repo_id"] / row["revision"]
    p = base
    for part in rel.split("/"):
        p = p / part
        if p.is_symlink():
            raise ValueError("Symlink in local source path")
    return p


def verify_file(path, n, sha, git_blob):
    if not path.is_file() or path.stat().st_size != n:
        return False
    if sha:
        h = hashlib.sha256()
    else:
        h = hashlib.sha1()
        h.update(b"blob " + str(n).encode("ascii") + b"\x00")
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest() == (sha or git_blob)


def run(args):
    manifest, queue, approval, policy = (load(x) for x in
        (args.manifest, args.queue, args.approved, args.limits))
    errors, rows = validate(manifest, queue, approval, policy)
    if errors:
        return {"status": "FAIL_METADATA", "errors": errors[:30], "download_approved": False}
    requested = set(args.repo_id or [])
    if requested and requested - {r["repo_id"] for r in rows}:
        return {"status": "FAIL_UNKNOWN_REPOSITORY", "unknown": sorted(requested - {r["repo_id"] for r in rows}),
                "download_approved": False}
    selected = [r for r in rows if not requested or r["repo_id"] in requested]
    selected_bytes = sum(r["bytes"] for r in selected)
    largest_file = max((f["source_bytes"] for r in selected for f in r["files"]), default=0)
    out = {"status": "PASS_SOURCE_METADATA_ONLY",
           "canonical_revision": "v46-20261118", "model_count": len(selected),
           "candidate_source_bytes": selected_bytes, "max_single_file_bytes": largest_file,
           "download_approved": False, "network_used": False, "model_code_executed": False,
           "runtime_or_license_approval": False,
           "warnings": [
               "These 12 are already selected assets, not extra bytes to add to v46 archive estimates.",
               "Manufacturer metadata and source hashes are not local file hashes or a tested offline restoration.",
               "A physical disk/free-space check does not establish owner licensing or Gated entitlement.",
               "Peak staging and runtime wheelhouse can exceed one-file temporary-copy allowance."
           ]}
    if args.archive_root:
        root = Path(args.archive_root).expanduser()
        if not root.exists() or not root.is_dir():
            out["disk"] = {"status": "FAIL_NOT_EXISTING_DIRECTORY"}
        else:
            disk = shutil.disk_usage(root)
            floor = policy["minimum_free_bytes"]
            # Conservative assuming all chosen files are currently absent.
            required = selected_bytes + largest_file + floor
            out["disk"] = {
                "status": "PASS_CAPACITY_PROVISIONAL" if disk.free >= required else "FAIL_CAPACITY",
                "path": str(root.resolve()), "filesystem_total_bytes": disk.total,
                "filesystem_free_bytes": disk.free, "minimum_floor_bytes": floor,
                "all_source_bytes_as_new": selected_bytes, "one_largest_file_staging_reserve": largest_file,
                "conservative_required_free_bytes": required,
                "actual_runtime_dependencies_known": False
            }
            if args.verify_existing:
                found = good = 0
                for row in selected:
                    for f in row["files"]:
                        try:
                            target = get_local(root, row, f["path"])
                            if target.exists():
                                found += 1
                                if verify_file(target, f["source_bytes"], f.get("source_sha256"),
                                               f.get("source_git_blob_sha1")):
                                    good += 1
                        except (OSError, ValueError):
                            pass
                out["local_hashes"] = {"found": found, "verified": good,
                                       "expected": sum(len(r["files"]) for r in selected),
                                       "complete": good == sum(len(r["files"]) for r in selected)}
    if args.show_dry_run:
        # Commands are OUTPUT ONLY; shell quoting prevents filename interpretation.
        commands = []
        for row in selected:
            parts = ["hf", "download", row["repo_id"], "--revision", row["revision"]]
            for f in row["files"]:
                parts.extend(["--include", f["path"]])
            parts.extend(["--dry-run", "--max-workers", "1"])
            commands.append(" ".join(shlex.quote(s) for s in parts))
        out["dry_run_commands_NOT_EXECUTED"] = commands
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--queue", type=Path, default=PROPOSED)
    p.add_argument("--approved", type=Path, default=APPROVED)
    p.add_argument("--limits", type=Path, default=LIMITS)
    p.add_argument("--repo-id", action="append", help="Select one or more exact IDs; omit for all 12")
    p.add_argument("--archive-root", help="Existing physical archive root on the owner's computer")
    p.add_argument("--verify-existing", action="store_true",
                   help="Hash currently stored files under archive_root/repo_id/revision/path")
    p.add_argument("--show-dry-run", action="store_true", help="Print commands only; never run")
    args = p.parse_args(argv)
    try:
        result = run(args)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as e:
        result = {"status": "FAIL", "reason": str(e), "download_approved": False}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS_SOURCE_METADATA_ONLY" else 2


if __name__ == "__main__":
    sys.exit(main())
