"""Stable historical baseline of 116 verified receipts under a growing ledger.

A later acquisition must not rewrite, omit, or replace the original reported
source identity/revision/count/hash evidence. This is a report-invariance check,
NOT a rehash of the owner's actual archive or proof of authorized transfer.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "catalog/audits/2026-11-27-r168-133-receipts-original117-signedness-and-historical-integrity.json"
PRIOR_HOLD_ID = "orcarouter/Qwen3.8-27B-Uncensored"


def core_digest(row, keys):
    value = {key: row.get(key) for key in keys}
    content = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def historical_116_ids():
    return frozenset(audit()["prior117_digest_by_repo_id"]) - {PRIOR_HOLD_ID}


def historical_116_receipts(ledger, *, validate=True):
    """Recover original 116 VERIFIED rows by immutable repo identity, not order."""
    manifest = audit()
    old = manifest["prior117_digest_by_repo_id"]
    lookup = {x["repo_id"]: x for x in ledger["models"]}
    if len(lookup) != len(ledger["models"]):
        raise ValueError("duplicate acquisition ledger repo IDs")
    if set(old) - set(lookup):
        raise ValueError("original 117 acquisition rows were removed")
    if validate:
        for repo, hashed in old.items():
            if core_digest(lookup[repo], manifest["core_fields_in_sha256"]) != hashed:
                raise ValueError("historic publisher/local receipt field changed: " + repo)
    result = [lookup[repo] for repo in sorted(set(old) - {PRIOR_HOLD_ID})]
    if len(result) != 116 or any(x["status"] != "VERIFIED" for x in result):
        raise ValueError("original 116 receipts changed verification status")
    if lookup[PRIOR_HOLD_ID]["status"] != "HOLD_GATED_OR_PRIVATE":
        raise ValueError("prior HOLD was silently converted without review")
    if (sum(x["files_verified"] for x in result),
            sum(x["source_bytes"] for x in result)) != (1758, 2021784002725):
        raise ValueError("original 116 reported file/byte totals changed")
    return result


def historical_117_ledger(ledger):
    """Historical test view, exact old 117 source identities, never new receipts.

    The current ledger must retain *all* 117 original rows byte/revision/hash
    intact; this function does NOT rewrite the actual acquisition ledger.
    """
    historical_116_receipts(ledger)
    manifest = audit()
    keys = set(manifest["prior117_digest_by_repo_id"])
    old = [x for x in ledger["models"] if x["repo_id"] in keys]
    if len(old) != 117:
        raise ValueError("history must contain original 117 unique source receipts")
    view = dict(ledger)
    view["models"] = old
    view["summary"] = dict(ledger["summary"])
    view["summary"].update({
        "models_total": 117,
        "models_verified": 116,
        "models_held": 1,
        "files_verified_total": 1758,
        "bytes_verified_total": 2021784002725
    })
    view["historical_snapshot_only"] = True
    view["prior_commit_verified_source_reference"] = manifest["prior_immutable_reference_commit"]
    return view


def current_133_reported_or_more(ledger):
    summary = ledger["summary"]
    historical_116_receipts(ledger)
    return (summary["models_verified"] >= 133 and
            summary["files_verified_total"] >= 2095 and
            summary["bytes_verified_total"] >= 2451205481822)
