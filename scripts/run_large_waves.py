#!/usr/bin/env python3
"""Parallel worker for the largest discovered models (descending size).

Safe to overlap with run_discovered_waves.py: already-stored files are
deduped by publisher hash, so a model downloaded by either worker is reused.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import preserve_execute as pe

PLAN = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("D:/AI_VAULT/state/discovered/plan.json")
LEDGER = Path("D:/AI_VAULT/state/ledger/waves-large-ledger.json")
TOP_N = 12


def main():
    approval = Path("D:/AI_VAULT/state/approved-session.json")
    if approval.exists():
        pe.APPROVED_QUEUE = approval
        pe.log(f"using local session approvals: {approval}")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    cands = sorted(plan["candidates"], key=lambda c: c["bytes"], reverse=True)[:TOP_N]
    pe.log(f"PARALLEL LARGE RUN: {len(cands)} models, "
           f"{sum(c['bytes'] for c in cands)} bytes planned")
    for c in cands:
        for attempt in range(12):
            try:
                m = json.loads(Path(c["manifest"]).read_text(encoding="utf-8"))
                for task in pe.extract_tasks(m):
                    res = [pe.process_task(task, c["manifest"], False)]
                    pe.append_ledger(res, str(LEDGER))
                break
            except Exception as e:
                pe.log(f"retry {c['repo_id']} {attempt+1}/12: {type(e).__name__}: {e}")
                time.sleep(45)
    pe.log("PARALLEL LARGE RUN COMPLETE")


if __name__ == "__main__":
    main()
