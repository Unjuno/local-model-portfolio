#!/usr/bin/env python3
"""Continuously acquire all discovered pinned models, smallest first.

Writes each model's receipt to the ledger immediately after completion so
progress is always observable, even if the process is interrupted.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import preserve_execute as pe

PLAN = Path("D:/AI_VAULT/state/discovered/plan.json")
LEDGER = Path("D:/AI_VAULT/state/ledger/waves3plus-ledger.json")


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    cands = sorted(plan["candidates"], key=lambda c: c["bytes"])
    pe.log(f"CONTINUOUS RUN: {len(cands)} models, "
           f"{sum(c['bytes'] for c in cands)} bytes planned")
    for c in cands:
        try:
            m = json.loads(Path(c["manifest"]).read_text(encoding="utf-8"))
            for task in pe.extract_tasks(m):
                res = [pe.process_task(task, c["manifest"], False)]
                pe.append_ledger(res, str(LEDGER))
        except Exception as e:
            pe.log(f"FATAL {c['repo_id']}: {type(e).__name__}: {e}")
    pe.log("CONTINUOUS RUN COMPLETE")


if __name__ == "__main__":
    main()
