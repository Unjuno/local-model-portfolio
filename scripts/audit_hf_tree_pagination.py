#!/usr/bin/env python3
"""Read-only, fail-closed HF immutable file-tree pagination audit.

This tool fetches ONLY JSON metadata from the public model API. It never
fetches LFS payloads, uses no authentication, and never executes model code.

Usage:
    python scripts/audit_hf_tree_pagination.py publisher/model <40-hex-commit> --summary-only
"""
from __future__ import annotations
import argparse
import json
import re
import urllib.parse
import urllib.request
from typing import Callable

REPO_RE = re.compile(r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$")
REV_RE = re.compile(r"^[a-f0-9]{40}$")
NEXT_RE = re.compile(r'<([^>]+)>\s*;\s*rel="next"')


def next_page(link: str | None, repo: str, revision: str) -> str | None:
    """Return only the expected API host+repo+revision next cursor URL."""
    if not link:
        return None
    matches = NEXT_RE.findall(link)
    if len(matches) != 1:
        raise ValueError("Missing or ambiguous rel=next pagination")
    url = matches[0]
    parsed = urllib.parse.urlsplit(url)
    root = f"/api/models/{repo}/tree/{revision}"
    if parsed.scheme != "https" or parsed.netloc != "huggingface.co" or parsed.path != root:
        raise ValueError("Unexpected pagination origin/path; refusing to follow")
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=False)
    if not params.get("cursor"):
        raise ValueError("Pagination next URL lacks cursor")
    return url


def list_all_immutable_files(
    repo: str,
    revision: str,
    opener: Callable[[str], tuple[list[dict], str | None]] | None = None,
    max_pages: int = 512,
) -> dict:
    if not REPO_RE.fullmatch(repo) or not REV_RE.fullmatch(revision):
        raise ValueError("Provide an exact publisher/model and immutable 40-hex SHA")
    def http_opener(url: str) -> tuple[list[dict], str | None]:
        request = urllib.request.Request(url, headers={"User-Agent": "local-model-portfolio-readonly-tree-audit"})
        with urllib.request.urlopen(request, timeout=35) as response:
            body = json.load(response)
            link = response.headers.get("Link")
        if not isinstance(body, list):
            raise ValueError("Publisher response must be a JSON array")
        return body, link

    opener = opener or http_opener
    url = f"https://huggingface.co/api/models/{repo}/tree/{revision}?recursive=true&expand=true"
    encountered = set()
    pages = 0
    paths = set()
    files = []
    while url:
        if pages >= max_pages:
            raise ValueError("Unexpectedly many pagination pages")
        if url in encountered:
            raise ValueError("Repeated cursor detected")
        encountered.add(url)
        page, link = opener(url)
        if not isinstance(page, list):
            raise ValueError("Invalid page payload")
        pages += 1
        for obj in page:
            if not isinstance(obj, dict):
                raise ValueError("Malformed tree entry")
            if obj.get("type") != "file":
                continue
            path = obj.get("path")
            if not isinstance(path, str) or path.startswith("/") or ".." in path.split("/"):
                raise ValueError("Unsafe file path")
            if path in paths:
                raise ValueError("Duplicate file path in paginated tree")
            paths.add(path)
            oid = obj.get("oid")
            if not isinstance(oid, str) or not re.fullmatch(r"[a-f0-9]{40}", oid):
                oid = None
            digest = obj.get("lfs", {}).get("oid")
            sha = digest if isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest) else None
            masked = digest is not None and sha is None
            size = obj.get("size")
            if not isinstance(size, int) or size < 0:
                raise ValueError("Missing or invalid size")
            files.append({"path": path, "bytes": size, "git_blob_sha1": oid,
                          "publisher_lfs_sha256": sha, "publisher_digest_masked": masked})
        url = next_page(link, repo, revision)
    return {
        "repo_id": repo, "revision_sha": revision, "metadata_only": True,
        "pages_fetched": pages, "file_count": len(files),
        "source_bytes": sum(x["bytes"] for x in files),
        "lfs_sha256_available": sum(x["publisher_lfs_sha256"] is not None for x in files),
        "lfs_masked": sum(x["publisher_digest_masked"] for x in files),
        "files": files,
    }


def main() -> None:
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("repo_id")
    a.add_argument("revision_sha")
    a.add_argument("--summary-only", action="store_true")
    opt = a.parse_args()
    result = list_all_immutable_files(opt.repo_id, opt.revision_sha)
    if opt.summary_only:
        result.pop("files", None)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
