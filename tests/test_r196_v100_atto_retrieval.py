import json
from pathlib import Path
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def test_r196_atto():
    old=load("catalog/effective-portfolio-2026-11-28-v99.json")["items"]
    rows=load("catalog/effective-portfolio-2026-11-28-v100.json")["items"]
    assert rows[:293]==old and len(rows)==295
    assert len({x["repo_id"].lower() for x in rows})==295
    active={x["repo_id"] for x in rows if x["portfolio_decision"] in ("select","conditional")}
    cond={x["repo_id"] for x in rows if x["portfolio_decision"]=="conditional"}
    assert len(active)==239 and len(cond)==183
    for p,k,s in [("queues/proposed-v100-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v100.json","items",active),("catalog/readiness/v100-2026-11-28-r196-all239-gates.json","records",active),("catalog/access/2026-11-28-v100-conditional-hub-gates.json","entries",cond)]:
        a=load(p)[k]; assert len(a)==len(s) and {x["repo_id"] for x in a}==s
    m=load("manifests/drafts/r196-2026-11-28-atto-retrieval-originals.candidate.json")
    f=[x for s in m["source_models"][:2] for x in s["source_files"]]
    assert len(f)==22 and sum(x["bytes"] for x in f)==3931097
    assert sum({x["publisher_lfs_sha256"] or x["git_blob_sha"]:x["bytes"] for x in f}.values())==3918055
    assert len({x["publisher_lfs_sha256"] for x in f if x["publisher_lfs_sha256"]})==2
    assert not m["download_approved"] and m["owner_incremental_bytes"] is None
    assert all(x["download_approved"] is False and not x.get("ready_to_acquire") for x in load("catalog/readiness/v100-2026-11-28-r196-all239-gates.json")["records"])
    assert load("catalog/revisions/v100-2026-11-28.json")["additions"]==rows[-2:]
