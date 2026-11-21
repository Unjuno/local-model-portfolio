"""Generate UNAPPROVED owner-review records only; no standing grants.\n\nHistorical continuous-acquisition instructions do not prove that each license,\ntrained dependency, exact source file or owner act is authorized. Existing\napproved-session.json is never touched. No transfers or model code runs.\n"""
import json
from pathlib import Path

PLAN = Path("D:/AI_VAULT/state/discovered/plan.json")
OUT = Path("D:/AI_VAULT/state/review-session-UNAPPROVED.json")
REF = "user directive 2026-11-19: continuous open-weight acquisition to D drive"


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    entries = []
    for c in plan["candidates"]:
        m = json.loads(Path(c["manifest"]).read_text(encoding="utf-8"))
        files = []
        for f in m["selected_files"]:
            rec = {"path": f["path"], "bytes": int(f["bytes"])}
            if f.get("publisher_lfs_sha256"):
                rec["sha256"] = f["publisher_lfs_sha256"]
            elif f.get("publisher_git_blob_sha1"):
                rec["git_blob_sha1"] = f["publisher_git_blob_sha1"]
            else:
                break
            files.append(rec)
        if len(files) != len(m["selected_files"]):
            continue
        lic = str(c.get("license") or "").lower()
        entries.append({
            "repo_id": m["repo_id"], "revision_sha": m["source_revision_sha"],
            "approved": False, "download_enabled": False, "approved_by_user": False,
            "license_text_reviewed": False,
            "parent_dependency_rights_reviewed": False,
            "nonstandard_license_permission_verified": False,
            "license": lic, "approval_ref": None, "files": files,
        })
    OUT.write_text(json.dumps({"schema_version": 1, "authorization_source": "UNAPPROVED_RESEARCH_SOURCE_REVIEW_ONLY",
                               "entries": entries}, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"wrote {OUT}: {len(entries)} exact pinned UNAPPROVED review entries")


if __name__ == "__main__":
    main()
