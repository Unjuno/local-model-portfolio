#!/usr/bin/env python3
"""Discover remaining acquirable models and build pinned source manifests.

Filters the canonical effective portfolio to active, public, permissively
licensed models that are not yet stored locally. For each candidate it reads
the Hugging Face API at the current fixed commit, selects canonical weight +
runtime files (excluding duplicate quantizations/media), and writes a pinned
manifest that preserve_execute.py can consume.

No payload is downloaded here. Capacity is planned against a 200 GB floor.
"""
import json
import re
import urllib.request
from pathlib import Path

PORTFOLIO = Path("catalog/effective-portfolio-2026-11-18-v48.json")
STORE = Path("D:/AI_VAULT/store/huggingface/model")
OUTDIR = Path("D:/AI_VAULT/state/discovered")
PLAN = Path("D:/AI_VAULT/state/discovered/plan.json")
MIN_FREE = 200_000_000_000

PERMISSIVE = {
    "apache-2.0", "mit", "bsd-3-clause", "cc0-1.0", "cc-by-4.0",
    "openmdw-1.1",
    "apache-2.0 (publisher tag and README; standalone LICENSE absent)",
    "apache-2.0_weights;mit_code_reported",
    "apache-2.0_weights;mit_code_reported".lower(),
    "apache-2.0_model_and_code_metadata",
    "mit_publisher_tag_and_code_mit",
}
WEIGHT_EXT = (".safetensors", ".bin", ".pt", ".pth", ".ckpt", ".msgpack", ".h5", ".npz")
KEEP_NAMES = {
    "config.json", "generation_config.json", "tokenizer.json",
    "tokenizer_config.json", "special_tokens_map.json", "vocab.json",
    "merges.txt", "preprocessor_config.json", "processor_config.json",
    "added_tokens.json", "normalizer.json", "chat_template.jinja",
    "model_index.json", "scheduler_config.json", "LICENSE", "LICENSE.txt",
    "README.md", "config.yaml",
}
EXCLUDE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".wav",
               ".mp3", ".flac", ".svg", ".gguf", ".onnx", ".zip", ".tar",
               ".gz", ".pdf", ".exe", ".pyc")


def api(repo, rev=None):
    url = (f"https://huggingface.co/api/models/{repo}" if not rev else
           f"https://huggingface.co/api/models/{repo}/revision/{rev}")
    url += "?blobs=true"
    req = urllib.request.Request(url, headers={"User-Agent": "discover/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def already_stored(repo):
    owner, name = repo.split("/", 1)
    p = STORE / owner / name
    return p.exists() and any(p.iterdir())


def is_gated(access):
    a = str(access).lower()
    return "gated" in a and "ungated" not in a


def select_files(siblings):
    has_safetensors = any(s["rfilename"].endswith(".safetensors") for s in siblings)
    out = []
    for s in siblings:
        p = s["rfilename"]
        low = p.lower()
        if any(low.endswith(e) for e in EXCLUDE_EXT):
            continue
        name = p.rsplit("/", 1)[-1]
        is_weight = low.endswith(WEIGHT_EXT)
        if is_weight and has_safetensors and low.endswith((".bin", ".pt", ".pth", ".ckpt")):
            continue  # duplicate legacy format when canonical safetensors exists
        if is_weight and has_safetensors and low.endswith(".npz"):
            continue
        if not is_weight and name not in KEEP_NAMES and not low.endswith(".json"):
            continue
        size = int(s.get("size") or 0)
        if size > 60_000_000_000:
            continue
        lfs = (s.get("lfs") or {}).get("sha256")
        rec = {"path": p, "bytes": size,
               "publisher_lfs_sha256": lfs,
               "publisher_git_blob_sha1": s.get("blobId")}
        out.append(rec)
    return out


def main():
    d = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    active = [i for i in d["items"]
              if i.get("asset_kind") == "model"
              and i.get("portfolio_decision") in ("select", "conditional")]
    OUTDIR.mkdir(parents=True, exist_ok=True)
    candidates, skipped = [], {"gated": [], "license": [], "stored": [], "api": [], "empty": []}
    for it in active:
        repo = it.get("repo_id")
        if not repo or "/" not in repo:
            continue
        if is_gated(it.get("observed_access")):
            skipped["gated"].append(repo)
            continue
        lic = str(it.get("license_metadata") or "").lower()
        if lic not in PERMISSIVE:
            skipped["license"].append(repo)
            continue
        if already_stored(repo):
            skipped["stored"].append(repo)
            continue
        try:
            meta = api(repo)
        except Exception:
            skipped["api"].append(repo)
            continue
        if meta.get("gated") or meta.get("private") or meta.get("disabled"):
            skipped["gated"].append(repo)
            continue
        rev = meta.get("sha")
        if not rev or len(rev) != 40:
            skipped["api"].append(repo)
            continue
        files = select_files(meta.get("siblings", []))
        if not files:
            skipped["empty"].append(repo)
            continue
        total = sum(f["bytes"] for f in files)
        manifest = {
            "repo_id": repo, "source_revision_sha": rev,
            "selected_files": files, "selected_file_count": len(files),
            "selected_file_bytes": total,
            "license_tag": lic, "discovered_from": str(PORTFOLIO),
        }
        fn = OUTDIR / (repo.replace("/", "__") + ".json")
        fn.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        candidates.append({"repo_id": repo, "revision_sha": rev,
                           "files": len(files), "bytes": total,
                           "manifest": str(fn), "license": lic})
    free = __import__("shutil").disk_usage(str(STORE)).free
    plan = {"generated_at": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc).isoformat(),
            "free_bytes": free, "floor": MIN_FREE,
            "candidates": candidates, "skipped": {k: v for k, v in skipped.items()}}
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"candidates={len(candidates)} planned_bytes={sum(c['bytes'] for c in candidates)}")
    print("skipped:", {k: len(v) for k, v in skipped.items()})
    for c in sorted(candidates, key=lambda x: x["bytes"]):
        print(f"  {c['bytes']/1e9:8.3f} GB  {c['files']:4d} files  {c['repo_id']}")


if __name__ == "__main__":
    main()
