#!/usr/bin/env python3
"""Convert pre-existing acquisition receipts into ledger receipts.

These two models were downloaded and hash-verified earlier under separate
acquisition_verification_receipt records, but were never in the execution
ledger. We take the verified file counts/bytes from those receipts and re-hash
the actual on-disk files against the publisher metadata captured in research.
"""
import hashlib
import json
from pathlib import Path

STATE = Path("D:/AI_VAULT/state")
ACQ = STATE / "acquisitions"
RES = STATE / "research"
LEDGER = STATE / "ledger" / "existing-integrated-ledger.json"
STORE = Path("D:/AI_VAULT/store/huggingface/model")
CHUNK = 1024 * 1024


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(CHUNK), b""):
            h.update(c)
    return h.hexdigest()


def from_api(api_path, repo, rev, receipt_path, dest_suffix):
    api = json.loads((RES / api_path).read_text(encoding="utf-8"))
    receipt = json.loads((ACQ / receipt_path).read_text(encoding="utf-8"))
    base = STORE / Path(dest_suffix)
    files = []
    ok = 0
    total = 0
    for s in api.get("siblings", []):
        p = s.get("rfilename")
        if not p:
            continue
        f = base / p
        size = int(s.get("size") or 0)
        total += size
        if not f.exists():
            files.append({"path": p, "bytes": size, "status": "MISSING"})
            continue
        lfs = (s.get("lfs") or {}).get("sha256")
        blob = s.get("blobId")
        method = "sha256-vs-publisher" if lfs else (
            "git-blob-sha1-vs-publisher" if blob else "size-only")
        if lfs:
            good = sha256_file(f) == lfs.lower()
        elif blob:
            h = hashlib.sha1()
            h.update(b"blob " + str(f.stat().st_size).encode() + b"\0")
            with open(f, "rb") as fh:
                for c in iter(lambda: fh.read(CHUNK), b""):
                    h.update(c)
            good = h.hexdigest() == blob.lower()
        else:
            good = f.stat().st_size == size
        if good:
            ok += 1
        files.append({"path": p, "bytes": size, "status": "VERIFIED" if good else "HASH_MISMATCH",
                      "method": method})
    return {
        "repo_id": repo, "revision_sha": rev,
        "source": "pre-existing-acquisition-receipt/" + receipt_path,
        "status": "VERIFIED" if ok == len(files) else "PARTIAL",
        "verified": ok, "total": len(files), "bytes": total,
        "license": "apache-2.0", "group": "PRE_EXISTING",
        "files": files,
        "receipt_files_verified": receipt.get("files_verified") or receipt.get("verified_files"),
        "started_at": receipt.get("verified_at"), "finished_at": receipt.get("verified_at"),
        "dry_run": False,
    }


def main():
    entries = [
        from_api("wan22-ti2v5b-api-2026-11-05.json", "Wan-AI/Wan2.2-TI2V-5B",
                 "921dbaf3f1674a56f47e83fb80a34bac8a8f203e",
                 "wan22-ti2v-5b-2026-11-05.json",
                 "Wan-AI/Wan2.2-TI2V-5B/921dbaf3f1674a56f47e83fb80a34bac8a8f203e"),
        from_api("z-image-turbo-api.json", "Tongyi-MAI/Z-Image-Turbo",
                 "f332072aa78be7aecdf3ee76d5c247082da564a6",
                 "z-image-turbo-2026-11-04.json",
                 "Tongyi-MAI/Z-Image-Turbo/f332072aa78be7aecdf3ee76d5c247082da564a6"),
    ]
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps({"schema_version": 1, "entries": entries},
                                 indent=2, ensure_ascii=False), encoding="utf-8")
    for e in entries:
        print(e["status"], f"{e['verified']}/{e['total']}", e["repo_id"])


if __name__ == "__main__":
    main()
