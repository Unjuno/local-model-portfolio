#!/usr/bin/env python3
"""Immutable read-only Chatterbox / Perth supply-chain archival census.

Fetch GitHub commit trees and small source/license text only, NEVER pretrained
tensor payloads, remote Python execution, user disks, approved queues or billing.
"""
from __future__ import annotations
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request

from scripts import capacity_selection as cap

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("catalog/research/2026-11-07-chatterbox-perth")
REV = "v27-20261107"
CHAT = ("resemble-ai/chatterbox", "ab55923c27757c90cfcc407baa57dc25a7d25217")
PERTH = ("resemble-ai/Perth", "ff1c8ac55a976971245cdd53c18d6131ca00d993")
CKPT = "src/perth/perth_net/pretrained/implicit/perth_net_250000.pth.tar"
LIMIT = 1_500_000

def must(x, why):
    if not x:
        raise ValueError(why)

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def save(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def request_public_github(url):
    must(url.startswith("https://api.github.com/repos/resemble-ai/"), "only publisher code metadata allowed")
    must(not any(x in url for x in ("/releases/assets", "/zipball", "/tarball", "/git/blobs/")), "binary endpoint blocked")
    headers = {"User-Agent": "local-model-portfolio-code-audit/2026-11-07",
               "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token := os.environ.get("GITHUB_TOKEN", ""):
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as response:
        payload = response.read(LIMIT + 1)
    must(len(payload) <= LIMIT, "public code response too large")
    return json.loads(payload.decode("utf-8"))

def get_tree(pair):
    repo, sha = pair
    must(re.fullmatch(r"[0-9a-f]{40}", sha), "invalid commit SHA")
    obj = request_public_github(f"https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1")
    must(obj.get("truncated") is False, "incomplete source tree")
    rows = obj["tree"]
    files = [{"path": r["path"], "bytes": r["size"], "git_blob_sha1": r["sha"],
              "identity_kind": "git_blob_sha1", "local_hash_verified": False}
             for r in rows if r["type"] == "blob"]
    must(len(files) == len({f["path"] for f in files}), "duplicate paths")
    must(len(files) >= 30 and all(isinstance(f["bytes"], int) and f["bytes"] >= 0 for f in files),
         "unexpected source code tree")
    return sorted(files, key=lambda f: f["path"])

def get_text(pair, path, maximum=100_000):
    repo, sha = pair
    must(path in {
        "README.md", "LICENSE", "pyproject.toml",
        "src/chatterbox/mtl_tts.py",
        "src/perth/config.py", "src/perth/__init__.py",
        "src/perth/perth_net/perth_net_implicit/perth_watermarker.py",
    }, "unexpected text read")
    obj = request_public_github(f"https://api.github.com/repos/{repo}/contents/{path}?ref={sha}")
    must(obj["type"] == "file" and obj["encoding"] == "base64", "not a short text file")
    raw = base64.b64decode(obj["content"])
    must(len(raw) <= maximum and len(raw) == obj["size"], "unexpected source content size")
    return raw.decode("utf-8")

def entry_scope_pair(pair):
    return "github:"+pair[0]+"@"+pair[1]

def source_only_dedup(base, chat_files, perth_files):
    must(base["source_revision"] == REV and base["exact_primary_file_scope_count"] == 126,
         "v27 census mismatch")
    must(base["known_scope_content_union_bytes"] == 3_417_685_712_585, "v27 total changed")
    entries = [(x["repo_id"]+"@"+x["source_revision"], f)
               for x in base["items"] for f in x["files"]]
    entries += [(x["repo_id"]+"@"+x["revision"], f)
                for x in base["dependencies"] for f in x["files"]]
    must(cap.union_bytes(entries) == base["known_scope_content_union_bytes"],
         "v27 selected source scope no longer matches baseline")
    seen = {(x["repo_id"],x["source_revision"]) for x in base["items"]}
    must(("ResembleAI/chatterbox",next(x["source_revision"] for x in base["items"]
         if x["repo_id"] == "ResembleAI/chatterbox")) in seen,"Chatterbox not selected")
    chat = next(x for x in base["items"] if x["repo_id"] == "ResembleAI/chatterbox")
    paths = {f["path"] for f in chat["files"]}
    must({"t3_mtl23ls_v3.safetensors","s3gen.pt","ve.pt",
          "grapheme_mtl_merged_expanded_v1.json"}.issubset(paths),
         "Chatterbox v3 selected weights and its tokenizer incomplete")
    old = cap.union_bytes(entries)
    extra = [(entry_scope_pair(CHAT), x) for x in chat_files] + [(entry_scope_pair(PERTH),x) for x in perth_files]
    new = cap.union_bytes(entries+extra)
    must(new >= old and new <= old+cap.sum_bytes(chat_files)+cap.sum_bytes(perth_files),
         "archive bound wrong")
    return {
        "baseline_known_logical_bytes": old,
        "new_publisher_code_tree_gross_bytes": cap.sum_bytes(chat_files)+cap.sum_bytes(perth_files),
        "hash_identity_aware_new_bytes": new-old,
        "research_scenario_logical_bytes": new,
        "minimum_4TB_difference_scenario_bytes":4_000_000_000_000-new,
        "matched_chatterbox_model_revision":chat["source_revision"],
        "selected_chatterbox_files_count":len(chat["files"]),
        "selected_chatterbox_weights_v3":True,
        "source_only_not_complete_offline_bytes":True,
        "original_126_primary_file_scopes_unchanged":True,
        "model_payloads_downloaded":0,
        "physical_owner_disk_free_bytes":None,
        "acquisition_peak_bytes":None,
        "full_offline_archive_bytes":None,
    }

def audit_source_strings(ch,per):
    must("As of August 2026, Chatterbox is retired research" in ch["README.md"],"retired notice missing")
    must("MIT License" in ch["LICENSE"],"chatterbox code MIT license missing")
    must("MIT License" in per["LICENSE"],"Perth source MIT license missing")
    must("resemble-perth @ git+https://github.com/resemble-ai/Perth.git@master" in ch["pyproject.toml"],
         "unpinned Perth provenance changed")
    must('transformers==5.2.0' in ch["pyproject.toml"],"Transformer ABI revised")
    must('torch==2.6.0' in ch["pyproject.toml"],"Torch ABI revised")
    must('torchaudio==2.6.0' in ch["pyproject.toml"],"Torchaudio ABI revised")
    text=ch["src/chatterbox/mtl_tts.py"]
    must('DEFAULT_MULTILINGUAL_T3_MODEL = "t3_mtl23ls_v2.safetensors"' in text,
         "default T3 model version changed")
    must('"v3": "t3_mtl23ls_v3.safetensors"' in text,
         "explicit v3 T3 checkpoint support missing")
    must('ckpt_dir / "s3gen.pt"' in text,"paired S3Gen loader changed")
    must("perth.PerthImplicitWatermarker()" in text and "apply_watermark" in text,
         "Perth acoustic watermark integration changed")
    must('revision="main"' in text, "recovery revision no longer unpinned")
    must('"perth_net", "pretrained"' in per["src/perth/config.py"],
         "local default neural watermark model dir changed")
    must("PerthNet.load(run_name, models_dir)" in per["src/perth/perth_net/perth_net_implicit/perth_watermarker.py"],
         "watermarker load path changed")
    must("except ImportError:" in per["src/perth/__init__.py"]
         and "PerthImplicitWatermarker = None" in per["src/perth/__init__.py"],
         "upstream silent import-error behaviour changed")
    return {
        "publisher_retired_notice_confirmed":True,
        "perth_package_installed_from_MUTABLE_master":True,
        "default_multilingual_t3_v2_but_selected_v3":True,
        "explicit_t3_model_v3_required_for_selected_archive":True,
        "default_s3gen_pt_required_by_this_loader":True,
        "perth_implicit_checkpoint_path_required":True,
        "perth_importerror_caught_and_watermarker_may_be_None":True,
        "runtime_dependencies_from_pinned_pyproject":{
           "python":">=3.10 (official README tested 3.11 on Debian 11)",
           "torch_for_python_under_3_14":"2.6.0",
           "torchaudio_for_python_under_3_14":"2.6.0",
           "transformers":"5.2.0",
           "diffusers":"0.29.0",
           "perth":"mutable master; freeze ff1c8ac55a976971245cdd53c18d6131ca00d993 instead",
           "pip_wheel_lock_and_transitive_deps_verified":False,
        },
        "watermark_checkpoint_license_provenance_independent_legal_review":True,
        "gpu_runtime_tested":False,
    }

def main():
    c=read_json("catalog/CURRENT.json")
    must(c["revision_id"] == REV and c["expected"]["tracked"] == 173
         and c["expected"]["active"] == 126,"current catalog drift")
    must(read_json("queues/approved.json")["entries"] == [], "approval state changed")
    old=read_json("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
    chat_files=get_tree(CHAT)
    perth_files=get_tree(PERTH)
    ckpt=next((x for x in perth_files if x["path"]==CKPT),None)
    must(ckpt and ckpt["bytes"] == 37_429_684
         and ckpt["git_blob_sha1"] == "22fbc47e03a4df700425819e9b5a1f81304f3a60",
         "learned watermark model changed, stop and re-review")
    must(cap.sum_bytes(chat_files) == 1_870_627, "Chatterbox code source tree changed")
    must(cap.sum_bytes(perth_files) == 38_066_448, "Perth code+model tree changed")
    ch={p:get_text(CHAT,p) for p in ("README.md","LICENSE","pyproject.toml","src/chatterbox/mtl_tts.py")}
    per={p:get_text(PERTH,p) for p in ("LICENSE","pyproject.toml","src/perth/config.py",
                                     "src/perth/__init__.py",
                                     "src/perth/perth_net/perth_net_implicit/perth_watermarker.py")}
    strings=audit_source_strings(ch,per)
    bytecalc=source_only_dedup(old,chat_files,perth_files)
    record={
     "schema_version":1,"source_revision":REV,
     "observed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
     "method":"publisher GitHub API immutable code trees and short source/license text; v27 local capacity union",
     "chatterbox_source":{"repo_id":CHAT[0],"commit_sha":CHAT[1],
        "file_count":len(chat_files),"gross_source_blobs_bytes":cap.sum_bytes(chat_files),
        "files":chat_files,"retired_public_maintenance_policy_since":"2026-08",
        "license_id":"MIT","source_code_only_not_model_hf_repo":True},
     "perth_source":{"repo_id":PERTH[0],"commit_sha":PERTH[1],
        "file_count":len(perth_files),"gross_source_blobs_bytes":cap.sum_bytes(perth_files),
        "files":perth_files,"license_id":"MIT",
        "learned_watermark_checkpoint":{"path":CKPT,"bytes":ckpt["bytes"],
          "git_blob_sha1":ckpt["git_blob_sha1"],"sha256_locally_verified":False,
          "license_coverage_of_checkpoint_separately_confirmed":False}},
     "read_only_code_findings":strings,
     "v27_research_capacity_addendum":bytecalc,
     "new_models_selected":0,"model_downloads_approved":0,"model_payload_downloaded_bytes":0,
     "owner_disk_measured":False,
     "unresolved_asset_count_still":35,
     "open_questions":[
        "Checkpoint copyright/training provenance of Perth beyond MIT code; publisher clarification still pending",
        "Native Chatterbox explicitly v3 pairing and Perkins checkpoint load not executed offline",
        "Python 3.11 / Debian11 / torch2.6.0 / transformers5.2.0 binary ABI for user target not evaluated",
        "Transitive package wheels, sound libraries, CUDA backend and license notices not captured",
        "Source code Python checkout footprint not necessarily equal to Git blob bytes; Git objects, packaging overhead and temporary files unknown",
        "GitHub blob SHA1 is provenance identity, not measured checkpoint SHA256",
     ],
     "evidence_urls":[
       f"https://github.com/{CHAT[0]}/tree/{CHAT[1]}",
       f"https://github.com/{PERTH[0]}/tree/{PERTH[1]}",
       "https://github.com/resemble-ai/Perth/issues/22",
       "https://github.com/resemble-ai/Perth/issues/23"
     ],
     "no_downloader_manifest":True,"executed_model_runtime":False,
    }
    save(OUT/"audit.json",record)
    print(json.dumps({
     "revision":REV,"chatterbox_source_blob_bytes":record["chatterbox_source"]["gross_source_blobs_bytes"],
     "perth_source_blob_bytes":record["perth_source"]["gross_source_blobs_bytes"],
     "perth_model_weight_bytes":ckpt["bytes"],
     "source_only_logical_scenario_bytes":bytecalc["research_scenario_logical_bytes"],
     "hash_aware_code_dependency_increment_bytes":bytecalc["hash_identity_aware_new_bytes"],
     "archive_is_complete":False,"weight_downloads":0},indent=2))
if __name__=="__main__":
    main()
