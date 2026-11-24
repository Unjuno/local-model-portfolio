#!/usr/bin/env python3
"""R159: fail-closed, metadata-only source review for the post-116 portfolio.

Never infers rights or human download approval from HF licenses, previous chat,
or an acquisition ledger. Never writes 'approved-v65.json' or downloads weights.
Legacy v65 generated 'approved_by_user: true' without a human act; do not reuse.
"""
import json
import re
from pathlib import Path

QUEUE = Path("queues/proposed-v66-r159-after116-novel-decision-models-UNAPPROVED.json")
SOURCE = Path("manifests/drafts/r159-2026-11-24-ive-ivonnet-ccore-immutable-publisher-source.candidate.json")
LEDGER = Path("catalog/execution/2026-11-19-acquisition-ledger.json")
CURRENT = Path("catalog/CURRENT.json")
DISC = Path("D:/AI_VAULT/state/discovered")
PLAN = DISC / "plan-v66-r159-RESEARCH-ONLY.json"
APPROVAL = DISC / "review-v66-r159-UNAPPROVED.json"
EXPECTED = ("illuin/Ivonnet-0.8B", "illuin/IVE-4B")
EXPECTED_FILES = 44
EXPECTED_BYTES = 10831209292


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _valid_hex(value, count):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{" + str(count) + "}", value) is not None


def _file(f):
    path = f["path"]
    if (not isinstance(path, str) or not path or path.startswith("/")
            or "\\" in path or any(x in ("", ".", "..") for x in path.split("/"))):
        raise ValueError("unsafe source path")
    size = f.get("bytes")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("invalid source size")
    git = f.get("git_blob_sha1")
    sha = f.get("publisher_lfs_sha256")
    if not _valid_hex(git, 40) or (sha is not None and not _valid_hex(sha, 64)):
        raise ValueError("missing or invalid publisher immutable fingerprint")
    return {
        "path": path, "bytes": size, "git_blob_sha1": git,
        "sha256": sha, "owner_local_sha_verified": False
    }


def main():
    queue, source, ledger, current = read(QUEUE), read(SOURCE), read(LEDGER), read(CURRENT)
    if current["revision_id"] != "v66-20261124":
        raise ValueError("canonical selection changed: refresh model research")
    if (current["expected"]["tracked"], current["expected"]["active"]) != (246, 197):
        raise ValueError("unexpected canonical counts")
    if (ledger["summary"]["models_verified"], ledger["summary"]["files_verified_total"],
            ledger["summary"]["bytes_verified_total"]) != (116, 1758, 2021784002725):
        raise ValueError("updated acquisition ledger requires fresh reconciliation")
    verified = {x["repo_id"]: x for x in ledger["models"] if x["status"] == "VERIFIED"}
    if len(verified) != 116:
        raise ValueError("duplicate or missing receipt identities")
    if tuple(r["repo_id"] for r in queue["research_selection_rows"]) != EXPECTED:
        raise ValueError("unrecognized candidates, fail closed")
    if queue["download_enabled"] or queue["approved_by_user"] or queue["approved_entries"] != 0:
        raise ValueError("research queue cannot authorize downloads")
    src = {x["repo_id"]: x for x in source["publisher_sources"]}
    if set(src) != set(EXPECTED) | {"ccore/CCORE-Web-Coder-4B"}:
        raise ValueError("unexpected model source scope")
    candidates, owner_review, scratch = [], [], []
    for r in queue["research_selection_rows"]:
        repo, rev = r["repo_id"], r["frozen_revision_sha"]
        if repo in verified or r["download_approved"] or r["explicit_owner_licensed_act_verified"]:
            raise ValueError("repo already downloaded or falsely authorized")
        entry = src[repo]
        if entry["research_selection"] != "RESEARCH_CONDITIONAL_NOT_CANONICAL":
            raise ValueError("source is not selected for research")
        if not _valid_hex(rev, 40) or rev != entry["publisher_revision_sha"]:
            raise ValueError("immutable revision mismatch")
        if entry["model_card_license_tag"] != "apache-2.0" or entry["observed_gated"] is not False:
            raise ValueError("license metadata/gating requires individual inspection")
        files = [_file(x) for x in entry["publisher_source_files"]]
        paths = {x["path"] for x in files}
        if (len(files) != len(paths) or len(files) != r["publisher_source_file_count"]
                or sum(f["bytes"] for f in files) != r["publisher_original_source_bytes"]
                or r["publisher_original_source_bytes"] != entry["publisher_full_bytes"]):
            raise ValueError("publisher file scope changed")
        if not {"readout.safetensors", "decision_config.json", "source/pyproject.toml", "tokenizer.json"}.issubset(paths):
            raise ValueError("cannot restore decision model without readout, tokenizer and runtime source")
        output = DISC / ("v65-r159-" + repo.replace("/", "__") + ".json")
        scratch.append((output, {
            "schema_version": 1, "repo_id": repo, "source_revision_sha": rev,
            "selected_file_count": len(files), "selected_file_bytes": entry["publisher_full_bytes"],
            "selected_files": files, "research_only": True, "download_approved": False,
            "owner_license_rights_verified": False, "owner_live_sha_verified": False
        }))
        candidates.append({
            "repo_id": repo, "revision_sha": rev, "selected_file_count": len(files),
            "selected_file_bytes": entry["publisher_full_bytes"], "manifest_path": str(output),
            "source_status": "PUBLISHER_ONLY_NOT_ACQUISITION_APPROVAL", "download_approved": False
        })
        owner_review.append({
            "repo_id": repo, "revision_sha": rev, "approved": False, "download_enabled": False,
            "approved_by_user": False, "license_text_reviewed": False,
            "parent_dependency_rights_reviewed": False, "nonstandard_license_permission_verified": False,
            "approval_ref": None, "files": files,
            "note": "A review template, not a signed human authorization."
        })
    if len(candidates) != 2 or sum(c["selected_file_count"] for c in candidates) != EXPECTED_FILES or sum(c["selected_file_bytes"] for c in candidates) != EXPECTED_BYTES:
        raise ValueError("new selected model scope changed")
    plan = {
        "schema_version": 1, "source": str(QUEUE), "catalog_revision": "v66-20261124",
        "ledger116_reported_only": True, "approved": False, "download_enabled": False,
        "candidate_repo_count": len(candidates), "publisher_reference_bytes": EXPECTED_BYTES,
        "candidates": candidates, "warning": "No source/license/owner authorization implied"
    }
    approval = {
        "schema_version": 1, "kind": "UNAPPROVED_OWNER_REVIEW_TEMPLATE_ONLY",
        "authorization_source": None, "approved": False, "download_enabled": False,
        "entries": owner_review
    }
    DISC.mkdir(parents=True, exist_ok=True)
    for path, data in scratch:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    APPROVAL.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R159 source review only: 2 models, 44 publisher files, 10831209292 byte; 0 approvals, 0 weight downloads")


if __name__ == "__main__":
    main()
