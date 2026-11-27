#!/usr/bin/env python3
"""Execution agent: acquire pinned publisher source files, verify, and ledger.

Safety properties (no exceptions):
  * Only HTTP GET to huggingface.co resolve endpoints. No import/exec of payload.
  * Pinned revision only (40-char commit); never 'main'/'latest'.
  * Skip gated repos and licenses that are unknown/restrictive (record HOLD).
  * Skip files already present with matching publisher hash (dedupe).
  * Resume via .part + Range, with retry/backoff on transient errors.
  * Enforce a minimum free-space floor on the destination drive.
  * Write machine-readable receipts + ledger; keep local state outside public git.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STORE = Path("D:/AI_VAULT/store/huggingface/model")
STATE = Path("D:/AI_VAULT/state")
LEDGER = STATE / "ledger" / "acquisition-ledger.json"
LOG = STATE / "logs" / "preserve_execute.log"
MIN_FREE = 200_000_000_000
# Tags are only initial screens; any transfer requires an explicit approved manifest.
# Nonstandard, source-available and restricted licenses require an individual act review.
PERMISSIVE = {"apache-2.0", "mit", "bsd-2-clause", "bsd-3-clause", "cc0-1.0"}
CHUNK = 1024 * 1024
REV_KEYS = ("repo_revision_sha", "source_revision_sha", "revision_sha",
            "source_revision", "immutable_revision", "first_party_repo_sha",
            "source_commit", "revision")



APPROVED_QUEUE = Path(__file__).resolve().parents[1] / "queues" / "approved.json"


def approval_for(task, approval_path=None):
    """Find a human-approved exact pinned model+file scope. Fail closed.

    This gate is administrative, not cryptographic proof of who gave consent.
    An external user authorization process must update queues/approved.json.
    """
    repo, rev = task.get("repo_id", ""), task.get("rev", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        return None
    if not re.fullmatch(r"[0-9a-f]{40}", rev):
        return None
    paths = []
    for f in task.get("files", []):
        p = f.get("path") or f.get("rfilename")
        size = f.get("bytes") or f.get("size_bytes") or f.get("size")
        if not isinstance(p, str) or not p or p.startswith("/") or "\\" in p:
            return None
        if any(x in ("", ".", "..") for x in p.split("/")):
            return None
        try:
            n = int(size)
        except (TypeError, ValueError):
            return None
        if n <= 0:
            return None
        sha = f.get("sha256") or f.get("publisher_lfs_sha256") or f.get("publisher_sha256") or f.get("source_sha256") or f.get("lfs_sha256")
        blob = f.get("git_blob_sha1") or f.get("publisher_git_blob_sha1") or f.get("git_blob_id") or f.get("blobId") or f.get("sha1")
        if isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha):
            fingerprint = ("sha256", sha)
        elif isinstance(blob, str) and re.fullmatch(r"[0-9a-f]{40}", blob):
            fingerprint = ("git-blob-sha1", blob)
        else:
            return None
        paths.append((p, n, fingerprint))
    if not paths or len({p for p, _, _ in paths}) != len(paths):
        return None
    try:
        with open(approval_path or APPROVED_QUEUE, encoding="utf-8") as stream:
            approved = json.load(stream)
    except (OSError, json.JSONDecodeError):
        return None
    # A previous v73 plan builder forged signed approval from source/licence tags.
    # Reject the WHOLE stale synthetic file, even if a row approval_ref was edited.
    source = str(approved.get("authorization_source") or "").lower()
    if "v73 effective portfolio pinned candidate sources" in source:
        return None
    for entry in approved.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("repo_id") != repo or entry.get("revision_sha") != rev:
            continue
        if not all(entry.get(k) is True for k in (
                "approved", "download_enabled", "approved_by_user",
                "license_text_reviewed", "parent_dependency_rights_reviewed")):
            continue
        if not isinstance(entry.get("approval_ref"), str) or not entry["approval_ref"].strip():
            continue
        # Prior automated plan builders falsely used a dated, general chat
        # directive to assert *individual* owner signoff and license review.
        # Old local approved-*.json files can remain on disk. Reject their
        # synthetic references even if every boolean in them is true.
        review_ref = entry["approval_ref"].lower()
        if ("user directive 2026-11-19" in review_ref
                or "canonical post96 source queue" in review_ref
                or "canonical 21-source queue" in review_ref
                or "v64 r152 canonical post99 source queue" in review_ref
                or "v65-post112-exact-source-files-" in review_ref
                or "v65 post112 pinned source queues" in review_ref
                or review_ref.startswith("v73-pinned-candidate-")
                or "v73 effective portfolio pinned candidate sources" in review_ref):
            continue
        allowed = entry.get("files")
        if not isinstance(allowed, list) or len(allowed) != len(paths):
            continue
        seen = []
        for f in allowed:
            if not isinstance(f, dict):
                break
            p = f.get("path")
            try:
                n = int(f.get("bytes"))
            except (ValueError, TypeError):
                break
            sha = f.get("sha256") or f.get("publisher_lfs_sha256")
            blob = f.get("git_blob_sha1") or f.get("publisher_git_blob_sha1")
            # A size-only or wildcard approval is never sufficient.
            if not ((isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha))
                    or (isinstance(blob, str) and re.fullmatch(r"[0-9a-f]{40}", blob))):
                break
            if isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha):
                fingerprint = ("sha256", sha)
            elif isinstance(blob, str) and re.fullmatch(r"[0-9a-f]{40}", blob):
                fingerprint = ("git-blob-sha1", blob)
            else:
                break
            seen.append((p, n, fingerprint))
        if len(seen) != len(paths) or sorted(seen) != sorted(paths):
            continue
        return entry
    return None

def now():
    return datetime.now(timezone.utc).isoformat()


def log(msg):
    line = f"{now()} {msg}"
    print(line, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        # Logging must never abort an acquisition; stdout still records progress.
        pass


def free_bytes(path):
    return shutil.disk_usage(str(path)).free


def api_model(repo, rev, repo_type="model"):
    seg = "datasets" if repo_type == "dataset" else "models"
    url = f"https://huggingface.co/api/{seg}/{repo}/revision/{rev}?blobs=true"
    req = urllib.request.Request(url, headers={"User-Agent": "preserve-execute/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def http_fetch(url, dest, expected_size):
    """Download to dest.part with resume; raise on failure."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    have = part.stat().st_size if part.exists() else 0
    if have and expected_size and have > expected_size:
        part.unlink()
        have = 0
    for attempt in range(8):
        try:
            have = part.stat().st_size if part.exists() else 0
            if have and expected_size and have >= expected_size:
                # A partial at/over full size is unusable; restart cleanly.
                part.unlink()
                have = 0
            headers = {"User-Agent": "preserve-execute/1.0"}
            if have:
                headers["Range"] = f"bytes={have}-"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=180) as r:
                if have and r.status == 200:  # server ignored Range -> restart
                    have = 0
                    if part.exists():
                        part.unlink()
                mode = "ab" if have else "wb"
                with open(part, mode) as f:
                    while True:
                        chunk = r.read(CHUNK)
                        if not chunk:
                            break
                        f.write(chunk)
                        have += len(chunk)
            if expected_size and part.stat().st_size != expected_size:
                raise IOError(f"size mismatch {part.stat().st_size} != {expected_size}")
            os.replace(part, dest)
            return
        except Exception as e:
            code = getattr(e, "code", None)
            msg = str(e)
            # Corrupt partial / unsatisfiable range: discard and restart from zero.
            # Transient Errno 22 / Permission denied on the external drive must
            # NOT discard an otherwise valid partial download.
            reset = code == 416 or "size mismatch" in msg
            if reset:
                try:
                    if part.exists():
                        part.unlink()
                except Exception:
                    pass
                have = 0
            log(f"  retry {attempt+1}/8 (reset={reset}): {type(e).__name__}: {e}")
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError(f"download failed: {url}")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(CHUNK), b""):
            h.update(c)
    return h.hexdigest()


def git_blob_sha1_file(path):
    size = path.stat().st_size
    h = hashlib.sha1()
    h.update(b"blob " + str(size).encode() + b"\0")
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(CHUNK), b""):
            h.update(c)
    return h.hexdigest()


def normalize_files(container):
    """Find a list of file dicts in a model record."""
    for k in ("selected_files", "files", "all_source_files",
              "selected_archival_scope", "source_files"):
        v = container.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict) and "path" in v[0]:
            return v
        if isinstance(v, dict):
            for kk in ("files", "selected_files"):
                if isinstance(v.get(kk), list) and v[kk] and "path" in v[kk][0]:
                    return v[kk]
    return []


def file_record(f, siblings):
    path = f.get("path") or f.get("rfilename")
    size = int(f.get("bytes") or f.get("size_bytes") or f.get("size") or 0)
    s256 = (f.get("publisher_lfs_sha256") or f.get("lfs_sha256") or
            f.get("publisher_sha256") or f.get("source_sha256") or f.get("sha256"))
    s1 = (f.get("publisher_git_blob_sha1") or f.get("git_blob_sha1") or
          f.get("git_blob_id") or f.get("blobId") or f.get("sha1"))
    # Fall back to Hugging Face API sibling metadata (publisher-provided).
    sib = siblings.get(path, {})
    if not s256:
        s256 = (sib.get("lfs") or {}).get("sha256")
    if not s1:
        s1 = sib.get("blobId")
    return {"path": path, "bytes": size,
            "sha256": s256.lower() if isinstance(s256, str) else None,
            "sha1": s1.lower() if isinstance(s1, str) else None}


def extract_tasks(m):
    reps = []
    for k in ("models", "repositories", "entries"):
        if isinstance(m.get(k), list):
            reps.extend(x for x in m[k] if isinstance(x, dict))
    if not reps and (m.get("repo_id") or m.get("repo") or
                     (m.get("source") or {}).get("repo_id")):
        reps.append(m)
    tasks = []
    for x in reps:
        repo = x.get("repo_id") or x.get("repo") or (x.get("source") or {}).get("repo_id")
        if not repo:
            continue
        rev = ""
        for k in REV_KEYS:
            v = x.get(k)
            if isinstance(v, str) and len(v) == 40:
                rev = v
                break
        if not rev:
            src = x.get("source") or {}
            for k in REV_KEYS:
                v = src.get(k)
                if isinstance(v, str) and len(v) == 40:
                    rev = v
                    break
        files = normalize_files(x)
        if not files:
            continue
        lic = (x.get("model_license_metadata") or x.get("model_license_tag") or
               x.get("license_metadata") or x.get("license_tag") or
               x.get("publisher_license_tag") or x.get("license") or "")
        if isinstance(lic, dict):
            lic = json.dumps(lic)
        lic = str(lic).lower()
        gated = bool(x.get("gated") or x.get("hub_metadata_gated") or
                     x.get("current_hub_gated")) or (x.get("gated") == "auto")
        rtype = x.get("repo_type") or x.get("asset_kind") or m.get("repo_type") or "model"
        if rtype not in ("model", "dataset"):
            rtype = "model"
        tasks.append({"repo_id": repo, "rev": rev, "files": files,
                      "license": lic, "gated_hint": gated, "repo_type": rtype,
                      "group": x.get("priority_group") or x.get("group") or ""})
    return tasks


def verify_file(path, rec):
    if rec.get("sha256"):
        got = sha256_file(path)
        return (got == rec["sha256"], "sha256-vs-publisher", rec["sha256"])
    if rec.get("sha1"):
        got = git_blob_sha1_file(path)
        return (got == rec["sha1"], "git-blob-sha1-vs-publisher", rec["sha1"])
    return (False, "NO_PUBLISHER_HASH", None)


def process_task(task, source, dry=False):
    repo, rev = task["repo_id"], task["rev"]
    log(f"=== {repo} @ {rev or 'NO PIN'} :: {len(task['files'])} files [{task['group']}] ===")
    res = {"repo_id": repo, "revision_sha": rev, "source": source,
           "group": task["group"], "started_at": now(), "files": [],
           "dry_run": bool(dry)}
    if not re.fullmatch(r"[0-9a-f]{40}", rev):
        res["status"] = "HOLD_NO_PINNED_REVISION"
        return res
    approved = approval_for(task)
    if not dry and approved is None:
        res["status"] = "HOLD_NO_EXPLICIT_APPROVED_MANIFEST"
        log("  HOLD: not in exact user-approved immutable file queue")
        return res
    try:
        meta = api_model(repo, rev, task.get("repo_type", "model"))
    except Exception as e:
        res["status"] = f"FAIL_API_{type(e).__name__}"
        res["error"] = str(e)
        log(f"  FAIL API: {e}")
        return res
    if meta.get("gated") or meta.get("private") or meta.get("disabled") or task["gated_hint"]:
        res["status"] = "HOLD_GATED_OR_PRIVATE"
        log(f"  HOLD: gated={meta.get('gated')} private={meta.get('private')}")
        return res
    lic = ((meta.get("cardData") or {}).get("license") or task["license"] or "").lower()
    if (not lic or (lic not in PERMISSIVE
            and not (approved and approved.get("nonstandard_license_permission_verified") is True))):
        res["status"] = "HOLD_LICENSE_REVIEW_REQUIRED"
        log(f"  HOLD: publisher license {lic!r} requires explicit reviewed rights")
        return res
    res["license"] = lic or "unspecified"

    siblings = {}
    for s in meta.get("siblings", []):
        rp = s.get("rfilename")
        if rp:
            siblings[rp] = s
    recs = [file_record(f, siblings) for f in task["files"]]
    if any(r["bytes"] <= 0 or not (r.get("sha256") or r.get("sha1")) for r in recs):
        res["status"] = "HOLD_INCOMPLETE_SOURCE_SIZE_OR_HASH"
        return res
    need = sum(r["bytes"] for r in recs)
    free = free_bytes(STORE)
    if not dry and free - need < MIN_FREE:
        res["status"] = "HOLD_CAPACITY_200GB_FLOOR"
        return res

    base = STORE / repo.split("/", 1)[0] / repo.split("/", 1)[1] / rev
    ok = 0
    for r in recs:
        rel = r["path"]
        target = (base / rel).resolve()
        if not target.is_relative_to(base.resolve()):
            res["files"].append({"path": rel, "status": "SKIP_UNSAFE_PATH"})
            continue
        out = {"path": rel, "bytes": r["bytes"]}
        if target.exists():
            v, method, exp = verify_file(target, r)
            if v and (not r["bytes"] or target.stat().st_size == r["bytes"]):
                out.update(status="DEDUP_VERIFIED", method=method)
                ok += 1
                res["files"].append(out)
                log(f"  DEDUP {rel}")
                continue
        if dry:
            out.update(status="DRY_RUN_SKIP")
            res["files"].append(out)
            continue
        host_seg = ("datasets/" if task.get("repo_type") == "dataset" else "")
        url = f"https://huggingface.co/{host_seg}{repo}/resolve/{rev}/{rel}"
        try:
            http_fetch(url, target, r["bytes"])
            v, method, exp = verify_file(target, r)
            out.update(status="VERIFIED" if v else "HASH_MISMATCH",
                       method=method, sha256=sha256_file(target))
            if v:
                ok += 1
            log(f"  {'VERIFIED' if v else 'HASH_MISMATCH'} {rel} [{method}]")
        except Exception as e:
            out.update(status=f"FAIL_{type(e).__name__}", error=str(e))
            log(f"  FAIL {rel}: {type(e).__name__}: {e}")
        res["files"].append(out)

    total = len(recs)
    res["verified"], res["total"], res["bytes"] = ok, total, need
    res["finished_at"] = now()
    res["free_bytes_after"] = free_bytes(STORE)
    res["status"] = "VERIFIED" if ok == total else ("PARTIAL" if ok else "FAILED")
    log(f"  RESULT {res['status']} {ok}/{total} free={res['free_bytes_after']}")
    return res


def append_ledger(results, ledger_path=None):
    ledger_path = Path(ledger_path) if ledger_path else LEDGER
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    data = {"schema_version": 1, "updated_at": now(), "entries": []}
    if ledger_path.exists():
        try:
            with open(ledger_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    data.setdefault("entries", []).extend(r for r in results if not r.get("dry_run"))
    data["updated_at"] = now()
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--small-first", action="store_true",
                    help="process smallest models first (small model validation wave)")
    ap.add_argument("--ledger", default=None, help="override local ledger path")
    args = ap.parse_args()
    results = []
    for mp in args.manifests:
        try:
            with open(mp, encoding="utf-8") as f:
                m = json.load(f)
            tasks = extract_tasks(m)
            if args.small_first:
                tasks.sort(key=lambda t: sum(int(f.get("bytes") or f.get("size_bytes")
                                                  or f.get("size") or 0)
                                             for f in t["files"]))
            log(f"SOURCE {mp} -> {len(tasks)} task(s)")
            for t in tasks:
                results.append(process_task(t, mp, args.dry_run))
        except Exception as e:
            log(f"FATAL {mp}: {type(e).__name__}: {e}")
            results.append({"source": mp, "status": "FATAL", "error": str(e)})
    if results:
        append_ledger(results, args.ledger)
    summary = {r.get("repo_id", r.get("source")): r.get("status") for r in results}
    log("SUMMARY " + json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
