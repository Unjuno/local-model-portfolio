#!/usr/bin/env python3
"""Build an accurate interim progress ledger from per-process execution logs.

Only models with a completed RESULT line are counted as acquired. A model that
logged a HOLD line without a RESULT is recorded as held (no payload acquired).
In-progress models are omitted so no unacquired model is reported as acquired.

Usage:
  python scripts/build_progress_ledger.py <log1> [<log2> ...]
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("state/execution/2026-11-19-progress.json")
START = re.compile(r"=== (\S+) @ (\S+) :: (\d+) files \[([^\]]*)\] ===")
RESULT = re.compile(r"RESULT (\S+) (\d+)/(\d+) free=(\d+)")
HOLD = re.compile(r"HOLD: gated|HOLD license|HOLD: no pinned")


def parse(path):
    current, models = None, {}
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        m = START.search(line)
        if m:
            current = {"repo_id": m.group(1), "revision_sha": m.group(2),
                       "files_total_declared": int(m.group(3)),
                       "group": m.group(4), "status": "IN_PROGRESS"}
            models[(m.group(1), m.group(2))] = current
            continue
        if current is None:
            continue
        m = RESULT.search(line)
        if m and current["status"] == "IN_PROGRESS":
            current.update(status=m.group(1), files_verified=int(m.group(2)),
                           files_total=int(m.group(3)),
                           free_bytes_after=int(m.group(4)))
        elif HOLD.search(line) and current["status"] == "IN_PROGRESS":
            current["status"] = "HOLD_GATED_OR_PRIVATE"
    return models


def main():
    logs = sys.argv[1:]
    if not logs:
        print("usage: build_progress_ledger.py <log> [<log> ...]", file=sys.stderr)
        return 2
    merged = {}
    for p in logs:
        for key, v in parse(p).items():
            old = merged.get(key)
            if old is None or (v["status"] == "VERIFIED" and old["status"] != "VERIFIED"):
                merged[key] = v
    entries = [{
        "repo_id": v["repo_id"], "revision_sha": v["revision_sha"],
        "group": v["group"], "status": v["status"],
        "files_verified": v.get("files_verified"),
        "files_total": v.get("files_total", v["files_total_declared"]),
        "free_bytes_after": v.get("free_bytes_after"),
    } for v in merged.values() if v["status"] != "IN_PROGRESS"]
    entries.sort(key=lambda e: (e["status"] != "VERIFIED", e["repo_id"]))
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "models_completed": len(entries),
        "models_verified": sum(1 for e in entries if e["status"] == "VERIFIED"),
        "models_partial": sum(1 for e in entries if e["status"] == "PARTIAL"),
        "models_held": sum(1 for e in entries if e["status"].startswith("HOLD")),
        "files_verified": sum(e["files_verified"] or 0 for e in entries),
        "minimum_free_bytes": min((e["free_bytes_after"] for e in entries
                                   if e.get("free_bytes_after")), default=None),
        "free_floor_bytes": 200_000_000_000,
    }
    summary["free_floor_maintained"] = bool(
        summary["minimum_free_bytes"] and
        summary["minimum_free_bytes"] >= summary["free_floor_bytes"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"schema_version": 1, "summary": summary,
                               "models": entries}, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
