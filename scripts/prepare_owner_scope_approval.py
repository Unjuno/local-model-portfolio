#!/usr/bin/env python3
"""Make an unapproved, exact-source-scope owner review template. Python >=3.10.

Read-only without --output. Never downloads, approves, or executes model files.
To authorize later, the actual owner must confirm EACH source's intended acts,
rights, current D: volume and files, then consciously mark the booleans true.
The downloader validates the exact revision + source_scope_sha256 on transfer.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sys

from download_r115_windows import validate_manifest, source_fingerprint

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "queues/proposed-v54-r128-first-four-delta-source.json"


def prepare(manifest_path: Path, root: Path) -> dict:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected = validate_manifest(data)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("The intended existing owner archive root must be an actual directory")
    if os.name == "nt" and root.drive.upper() != "D:":
        raise ValueError("This portfolio requires an explicitly identified D: archive root")
    usage = shutil.disk_usage(root)
    publisher_bytes = sum(model["source_bytes"] for model in selected)
    max_file = max(f["bytes"] for e in selected for f in e["files"])
    floor = data.get("required_free_floor_bytes")
    if type(floor) is not int or floor < 200_000_000_000:
        raise ValueError("The manifest reduced the 200 GB safety floor")
    # This is a planning envelope only. The actual downloader rechecks disk
    # and staging before EACH file. Real cache overhead may be higher.
    conservative_required_bytes = floor + publisher_bytes + 2 * max_file
    template = {
        "schema_version": 1,
        "kind": "OWNER_EXACT_SCOPE_REVIEW_TEMPLATE_ALL_FALSE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_manifest": str(manifest_path),
        "source_kind": data["kind"],
        "owner_intended_archive_root": str(root.resolve()),
        "owner_disk_observation": {
            "total_bytes": usage.total,
            "free_bytes": usage.free,
            "publisher_source_bytes_if_all_new": publisher_bytes,
            "maximum_single_source_file_bytes": max_file,
            "staging_envelope_bytes": 2 * max_file,
            "minimum_free_floor_bytes": floor,
            "conservative_required_free_bytes": conservative_required_bytes,
            "capacity_preflight_pass": usage.free >= conservative_required_bytes,
            "not_a_full_offline_dependency_closure": True
        },
        "entries": [
            {
                "source_repo_id": e["source_repo_id"],
                "repository_type": e.get("repository_type", "model"),
                "source_revision": e["source_revision"],
                "source_scope_sha256": source_fingerprint(e),
                "source_bytes_for_review": e["source_bytes"],
                "selected_file_count_for_review": len(e["files"]),
                "license_metadata_for_review": e["license_metadata"],
                "approved": False,
                "user_explicit_manifest_consent": False,
                "license_and_parent_rights_reviewed": False,
                "owner_archive_volume_verified": False
            }
            for e in selected
        ],
        "review_instructions": [
            "Template entries are NOT approved; no file transfer is authorized by generating this file.",
            "Review intended uses and rights/license text of EACH publisher and dataset, including attribution.",
            "Confirm current D: free space and cache/staging; the owner must mark volume verified, not the tool.",
            "Confirm all filename/revision/file-hash scopes and required runtime/parent learned dependencies.",
            "Only then mark the four approval booleans true for selected entries and provide the reviewed file to --execute --approval-file.",
            "Store approvals on the owner's D drive, not in the public GitHub repository."
        ]
    }
    return template


def write_template(value: dict, root: Path, output: Path) -> None:
    root_dir = root.resolve(strict=True)
    if not output.is_absolute():
        raise ValueError("Require an absolute --output path on the approved owner volume")
    if not output.resolve(strict=False).is_relative_to(root_dir):
        raise ValueError("Do not write owner approvals outside the selected archive volume")
    if output.is_symlink() or output.exists():
        raise FileExistsError("Refusing to overwrite any existing owner approval file")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.parent.resolve(strict=True).is_relative_to(root_dir) is False:
        raise ValueError("Output directory symlink escaped the archive volume")
    with output.open("x", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, help="Optional absolute filename inside owner archive; exclusive create")
    args = ap.parse_args(argv)
    result = prepare(args.manifest, args.root)
    if args.output is not None:
        write_template(result, args.root, args.output)
        print(json.dumps({"status":"UNAPPROVED_TEMPLATE_WRITTEN", "file":str(args.output),
                          "source_count":len(result["entries"]),
                          "capacity_preflight_pass":result["owner_disk_observation"]["capacity_preflight_pass"]}))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
