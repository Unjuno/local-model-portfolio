#!/usr/bin/env python3
"""Read-only v47 R111 acquisition-plan preflight. Python >=3.10, stdlib only.

Does NOT download/execute model code, install packages, approve queues, or
change user data. Publisher metadata checks are not local hashes or legal grants.
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
QUEUE = ROOT / "queues/proposed-v47-r110-source-pinned-14.json"
DECISIONS = ROOT / "catalog/decisions/2026-11-18-r111-preservation-tranche-and-swap-audit.json"
APPROVED = ROOT / "queues/approved.json"
LIMITS = ROOT / "policies/limits.json"
CANDIDATES = ROOT / "catalog/CURRENT.json"
REQUIRED_COUNTS = (14, 173, 72, 211999468264)
REQUIRED_GROUP_BYTES = {"A": 47030749353, "B": 671173375,
                        "C": 108711479306, "D": 55586066230}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_path(rel):
    if not isinstance(rel, str) or not rel or "\\" in rel or ":" in rel or "\x00" in rel:
        return False
    p = PurePosixPath(rel)
    return not p.is_absolute() and all(x not in ("", ".", "..") for x in rel.split("/"))


def source_sha(f):
    a, b = f.get("sha256"), f.get("publisher_lfs_sha256")
    if a is not None and b is not None and a != b:
        raise ValueError("Conflicting publisher SHA-256 fields")
    return a or b


def validate(q, d, approved, limits, current):
    errors, result, observed_sha = [], [], {}
    records = q.get("entries", [])
    groups = d.get("groups", {})
    revision = str(current.get("revision_id",""))
    try:
        revision_number = int(revision.split("-",1)[0].lstrip("v"))
    except ValueError:
        revision_number = -1
    if revision_number < 47 or "catalog/revisions/v47-2026-11-18.json" not in current.get("ordered_overlays",[]):
        errors.append("Not v47 canonical revision or valid later descendant")
    historical = read_json(ROOT / "catalog/effective-portfolio-2026-11-18-v47.json")
    if (len(historical["items"]) != 200 or
            sum(x["portfolio_decision"] in ("select","conditional")
                for x in historical["items"]) != 153):
        errors.append("200/153 v47 active invariants violated")
    if q.get("model_count") != 14 or len(records) != 14:
        errors.append("R110 expected 14 model records")
    if approved.get("entries") != []:
        errors.append("Explicit approved queue must remain empty")
    if q.get("authorization", {}).get("approved") is not False:
        errors.append("Source plan unexpectedly authorized")
    if limits.get("archive_target_bytes") != 4000000000000 or limits.get("minimum_free_bytes") != 200000000000:
        errors.append("4TB/200GB official archive policy changed")
    lane_lookup = {}
    for lane, ids in groups.items():
        for rid in ids:
            if rid in lane_lookup:
                errors.append("Duplicate repo in R111 lanes: " + rid)
            lane_lookup[rid] = lane
    if set(lane_lookup) != {r.get("repo_id") for r in records}:
        errors.append("R111 lane membership != R110 model IDs")
    ids = set()
    file_count = sha_count = total = 0
    totals = {name: 0 for name in REQUIRED_GROUP_BYTES}
    for item in records:
        rid, rev = item.get("repo_id"), item.get("source_revision")
        if not isinstance(rid, str) or rid.count("/") != 1 or rid in ids:
            errors.append("Duplicate or invalid repo ID: " + str(rid))
            continue
        ids.add(rid)
        lane = lane_lookup.get(rid)
        if lane not in totals:
            errors.append("Unknown R111 selection lane: " + str(lane))
            continue
        if not isinstance(rev, str) or not re.fullmatch("[0-9a-f]{40}", rev):
            errors.append("Invalid commit: " + rid)
        if item.get("download_approved") is not False:
            errors.append("Unapproved model became approved: " + rid)
        files = item.get("files")
        if not isinstance(files, list) or not files:
            errors.append("No selected files: " + rid)
            continue
        seen, subtotal, sha_here = set(), 0, 0
        for f in files:
            rel, n = f.get("path"), f.get("bytes")
            if not safe_path(rel) or rel in seen:
                errors.append("Unsafe or duplicate file path: " + rid + " / " + str(rel))
                continue
            seen.add(rel)
            if type(n) is not int or n <= 0:
                errors.append("Invalid byte value: " + rel)
                continue
            subtotal += n
            try:
                sha = source_sha(f)
            except ValueError:
                errors.append("Conflicting SHA fields: " + rel)
                sha = None
            if sha is not None:
                if not isinstance(sha, str) or re.fullmatch("[0-9a-f]{64}", sha) is None:
                    errors.append("Invalid publisher SHA: " + rel)
                else:
                    sha_here += 1
                    old = observed_sha.get(sha)
                    if old is not None and old != n:
                        errors.append("Same SHA / different file sizes")
                    observed_sha[sha] = n
            if re.search(r"\.(gguf|safetensors|pt|pth|onnx|bin|npz)$", rel, re.I) and sha is None:
                errors.append("Unhashed binary data: " + rid + " / " + rel)
            blob = f.get("git_blob_sha1")
            if blob is not None and (not isinstance(blob, str) or not re.fullmatch("[0-9a-f]{40}", blob)):
                errors.append("Invalid Git blob: " + rel)
        if subtotal != item.get("source_bytes") or len(files) != item.get("source_file_count"):
            errors.append("R110 model subtotal or file count drift: " + rid)
        total += subtotal
        file_count += len(files)
        sha_count += sha_here
        totals[lane] += subtotal
        result.append({"repo_id": rid, "revision": rev, "lane": lane,
                       "files": files, "bytes": subtotal, "gated": bool(item.get("gated"))})
    if (len(result), file_count, sha_count, total) != REQUIRED_COUNTS:
        errors.append("R110 14/173/72/211999468264 totals mismatch")
    if totals != REQUIRED_GROUP_BYTES:
        errors.append("R111 A/B/C/D group source sums mismatch")
    if q.get("total_publisher_source_bytes") != total or q.get("source_file_count") != file_count:
        errors.append("R110 proposal metadata header mismatch")
    if q.get("publisher_sha256_entries") != sha_count:
        errors.append("R110 proposal hash metadata header mismatch")
    return errors, result


def local_file(archive_root, r, rel):
    path = archive_root
    for s in (r["repo_id"] + "/" + r["revision"] + "/" + rel).split("/"):
        path = path / s
        if path.is_symlink():
            raise ValueError("Symlink in local archive path")
    return path


def fingerprint(path, n, f):
    if not path.is_file() or path.stat().st_size != n:
        return False
    sha = source_sha(f)
    git_blob = f.get("git_blob_sha1")
    if sha:
        h = hashlib.sha256()
    elif git_blob:
        h = hashlib.sha1()
        h.update(b"blob " + str(n).encode() + b"\0")
    else:
        return False
    with path.open("rb") as fh:
        for data in iter(lambda: fh.read(4 * 1024 * 1024), b""):
            h.update(data)
    return h.hexdigest() == (sha or git_blob)


def run(args):
    q, d, approved, limits, current = (read_json(p) for p in
        (args.queue, args.decisions, args.approved, args.limits, args.current))
    errors, rows = validate(q, d, approved, limits, current)
    if errors:
        return {"status": "FAIL_METADATA", "errors": errors[:30], "download_approved": False}
    selection = set(args.repo_id or [])
    if args.lane:
        selection |= set(d["groups"][args.lane])
    if args.repo_id or args.lane:
        rows = [r for r in rows if r["repo_id"] in selection]
    if args.repo_id and not set(args.repo_id).issubset({r["repo_id"] for r in rows}):
        return {"status": "FAIL_UNKNOWN_MODEL", "download_approved": False}
    source_bytes = sum(r["bytes"] for r in rows)
    stage_bytes = max((f["bytes"] for r in rows for f in r["files"]), default=0)
    report = {"status": "PASS_PUBLISHER_METADATA_ONLY", "canonical_revision": "v47-20261118",
              "requested_models": len(rows), "historical_selected_source_bytes": source_bytes,
              "max_selected_file_bytes": stage_bytes,
              "download_approved": False, "network_used": False, "models_executed": False,
              "legal_rights_verified": False, "offline_restore_verified": False,
              "note": "The 14-model group is already part of v47; no duplicate 4TB reservation."}
    if args.archive_root:
        root = Path(args.archive_root).expanduser()
        if not root.is_dir():
            report["disk"] = {"status": "FAIL_NO_ARCHIVE_DIRECTORY"}
        else:
            u = shutil.disk_usage(root)
            needed = source_bytes + stage_bytes + limits["minimum_free_bytes"]
            report["disk"] = {
                "status": "PASS_CAPACITY_PROVISIONAL" if u.free >= needed else "FAIL_CAPACITY",
                "actual_free_bytes": u.free, "filesystem_total_bytes": u.total,
                "selected_source_bytes": source_bytes, "single_largest_file_stage_bytes": stage_bytes,
                "minimum_policy_free_bytes": limits["minimum_free_bytes"],
                "conservative_required_free_bytes": needed,
                "runtime_wheelhouse_and_parent_weights_not_accounted": True
            }
            if args.verify_existing:
                found = checked = 0
                for r in rows:
                    for f in r["files"]:
                        try:
                            path = local_file(root, r, f["path"])
                            if path.exists():
                                found += 1
                                if fingerprint(path, f["bytes"], f):
                                    checked += 1
                        except (OSError, ValueError):
                            pass
                report["hash_verification"] = {
                    "found": found, "matched": checked,
                    "expected": sum(len(r["files"]) for r in rows),
                    "all_matched": checked == sum(len(r["files"]) for r in rows)
                }
    if args.show_dry_run:
        commands = []
        for row in rows:
            flags = ["hf", "download", row["repo_id"], "--revision", row["revision"]]
            for f in row["files"]:
                flags.extend(["--include", f["path"]])
            flags.extend(["--dry-run", "--max-workers", "1"])
            commands.append(" ".join(shlex.quote(x) for x in flags))
        report["commands_not_executed"] = commands
    return report


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--queue", type=Path, default=QUEUE)
    a.add_argument("--decisions", type=Path, default=DECISIONS)
    a.add_argument("--current", type=Path, default=CANDIDATES)
    a.add_argument("--approved", type=Path, default=APPROVED)
    a.add_argument("--limits", type=Path, default=LIMITS)
    a.add_argument("--lane", choices=tuple(REQUIRED_GROUP_BYTES))
    a.add_argument("--repo-id", action="append")
    a.add_argument("--archive-root")
    a.add_argument("--verify-existing", action="store_true")
    a.add_argument("--show-dry-run", action="store_true")
    opts = a.parse_args(argv)
    try:
        result = run(opts)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as err:
        result = {"status": "FAIL", "reason": str(err), "download_approved": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS_PUBLISHER_METADATA_ONLY" else 2


if __name__ == "__main__":
    sys.exit(main())
