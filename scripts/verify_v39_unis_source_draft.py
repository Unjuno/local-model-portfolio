"""Static fail-closed verification for Xiaomi UNIS4B/VQ immutable-source candidate.

No network, model import, pickle unmarshal, or downloaded code execution.
The result certifies a source-metadata allowlist, NOT authorized acquisition.
"""
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PATH = ROOT / "catalog/research/2026-11-15-r89-xiaomi-u0-4b-immutable-selected-source.json"
DRAFT_PATH = ROOT / "manifests/drafts/v39-unis4b-and-vq-source.candidate.json"
REPO_IDS = ("XiaomiRobotics/Xiaomi-Robotics-U0-4B", "BAAI/Emu3.5-VisionTokenizer")
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA64 = re.compile(r"[0-9a-f]{64}\Z")
UNSAFE_WEIGHT_SUFFIXES = (".ckpt", ".pkl", ".pickle", ".pth", ".pt")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _valid_path(p):
    _require(isinstance(p, str) and p and "\\" not in p, "invalid path string")
    parts = PurePosixPath(p).parts
    _require(not p.startswith("/") and ":" not in p and all(x not in (".", "..") for x in parts),
             "absolute, drive or traversal path")
    _require(p == str(PurePosixPath(p)), "noncanonical path")
    _require(not p.lower().endswith(UNSAFE_WEIGHT_SUFFIXES), "unreviewed pickle checkpoint")
    return p


def validate(research, draft):
    _require(draft["manifest_kind"] == "NON_EXECUTABLE_IMMUTABLE_SOURCE_SCOPE_CANDIDATE", "wrong artifact")
    _require(draft["source_catalog_revision"] == "v39-20261115", "wrong revision")
    _require(not any(draft[x] for x in ("approved", "download_enabled", "download_authorized",
                "offline_restore_verified", "model_payload_downloaded", "owner_drive_verified",
                "owner_permission_verified", "auto_download_allowed", "materialize_local_files")),
             "unsafe approval or execution state")
    risk = draft["execution_risk"]
    _require(not risk["deserialization_from_untrusted_source_permitted"], "pickle execution enabled")
    _require(not risk["trust_remote_code_execution_permitted"], "remote code allowed")
    _require(not risk["run_model_to_validate_manifest"], "model run enabled")
    _require(risk["safe_safetensors_source_does_not_prove_safe_runtime"], "runtime risk incorrectly waived")

    _require(tuple(x["repo_id"] for x in research["repos"]) == REPO_IDS, "research repo IDs drift")
    _require(tuple(x["repo_id"] for x in draft["repos"]) == REPO_IDS, "draft repo IDs drift")
    _require(draft["source_repo_count"] == len(REPO_IDS), "repo count")
    _require(SHA40.fullmatch(draft["required_code"]["commit"]), "source-code commit is mutable")
    _require(not draft["required_code"]["code_source_contents_reviewed_for_runtime_security"],
             "unreviewed code claimed safe")

    total_n = total_bytes = weights = 0
    for source_repo, repo in zip(research["repos"], draft["repos"]):
        _require(repo["immutable_revision_sha"] == source_repo["revision"], "revision mismatch")
        _require(bool(SHA40.fullmatch(repo["immutable_revision_sha"])), "invalid immutable revision")
        _require(repo["source_metadata_url"] == source_repo["publisher_api_url"], "source URL changed")
        _require(repo["license_tag_metadata_only"] == source_repo["license_tag"], "license label drift")
        _require(repo["observed_public_ungated"] == (not source_repo["gated"] and not source_repo["private"]),
                 "access status mismatch")
        expected = {x["path"]: x for x in source_repo["selected_files"]}
        actual = {x["path"]: x for x in repo["files"]}
        _require(len(expected) == len(source_repo["selected_files"]) == len(actual) == len(repo["files"]),
                 "duplicate/missing files")
        _require(set(expected) == set(actual), "selected source allowlist differs")
        count_bytes = 0
        for name, rec in actual.items():
            _valid_path(name)
            src = expected[name]
            _require(rec["bytes"] == src["bytes"] and isinstance(rec["bytes"], int) and rec["bytes"] >= 0,
                     "source bytes mismatch")
            _require(rec["publisher_git_blob_sha1"] == src["publisher_git_blob_sha1"],
                     "publisher git blob hash changed")
            _require(rec["publisher_lfs_sha256"] == src["publisher_lfs_sha256"],
                     "publisher LFS hash changed")
            _require(rec["execute_during_acquisition"] is False and rec["local_sha256_verified"] is False,
                     "unsafe execute/local hash claim")
            if name.endswith(".safetensors"):
                _require(isinstance(rec["publisher_lfs_sha256"], str) and
                         SHA64.fullmatch(rec["publisher_lfs_sha256"]), "missing weight source sha256")
                weights += 1
            count_bytes += rec["bytes"]
        _require(repo["source_file_bytes"] == source_repo["selected_bytes"] == count_bytes,
                 "repository source byte mismatch")
        _require(repo["source_file_count"] == len(actual), "repository file count wrong")
        _require(set(x["path"] for x in repo["explicitly_excluded_alternates"]) ==
                 set(x["path"] for x in source_repo["unselected"]), "alternative exclusion drift")
        total_n += len(actual)
        total_bytes += count_bytes
    _require(total_n == research["total_source_selected_file_count"] ==
             draft["source_file_count"] == 18, "total file count")
    _require(total_bytes == research["total_source_selected_bytes"] ==
             draft["source_selected_file_bytes"] == 11_991_440_188, "total selected source bytes")
    _require(weights == 3, "expected 3 safetensors original trained checkpoints")
    _require(draft["selected_source_bytes_are_not_final_offline_bundle_size"],
             "selected source falsely treated as complete runtime bundle")
    return {"source_repos": len(REPO_IDS), "files": total_n,
            "source_bytes": total_bytes, "safetensors_checkpoints": weights,
            "download_approved": False}


def main():
    source = json.loads(RESEARCH_PATH.read_text(encoding="utf-8"))
    draft = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    result = validate(source, draft)
    print(json.dumps({"status": "PASS_SOURCE_METADATA_ONLY_NOT_DOWNLOAD_READY", **result},
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
