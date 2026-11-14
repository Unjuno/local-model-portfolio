#!/usr/bin/env python3
"""Read-only v32 capacity audit. Python >=3.10, stdlib only, no network/write/model execution."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def j(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def verify(report_root: Path | None = None):
    """Verify immutable source arithmetic; optionally override historical report root in tests."""
    v27 = j('catalog/capacity/2026-11-07/v27/capacity-summary.json')
    old_markdown = ((ROOT if report_root is None else Path(report_root)) / 'catalog/capacity/2026-11-07/v27/capacity-report.md').read_text(encoding='utf-8')
    old = {}
    for line in old_markdown.splitlines():
        m = re.fullmatch(r'\|\s*([^|]+/[^|]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', line.strip())
        if m:
            rid = m[1].strip()
            if rid in old: raise ValueError('duplicate old ID ' + rid)
            old[rid] = int(m[2])
    if len(old) != 126 or sum(old.values()) != v27['known_primary_file_bytes_sum']:
        raise ValueError('v27 historical capacity mismatch')
    catalog = j('catalog/effective-portfolio-2026-11-14-v32.json')
    active = [x for x in catalog['items'] if x['portfolio_decision'] in ('select', 'conditional')]
    ids = [x['repo_id'] for x in active]
    if catalog['revision_id'] != 'v32-20261114' or len(active) != 135 or len(set(ids)) != 135 or not set(old) <= set(ids):
        raise ValueError('v32 IDs/cohorts invalid')
    r64 = j('manifests/drafts/r64-eight-source-scopes.candidate.json')
    r48 = j('catalog/research/2026-11-12-r48-pinned-scopes.json')
    r62 = j('catalog/research/2026-11-14-r62-ace-exact-source-scope-and-kumo-tag.json')
    r73 = j('catalog/capacity/2026-11-15/v32/135-primary-file-source-reconciliation.json')
    byrepo = {x['repo_id']: x for x in r64['repositories']}
    for r in r64['repositories']:
        if sum(f['bytes'] for f in r['files']) != r['selected_bytes'] or len(r['files']) != r['file_count']:
            raise ValueError('R64 file scope mismatched ' + r['repo_id'])
    prof = next(x for x in r48['profiles'] if x['id'] == 'zonos_native_keep2_reference_scope')
    zonos = sum(r48['files'][i][2] for i in prof['file_indices'])
    if zonos != prof['known_scope_bytes'] or len(prof['file_indices']) != 14:
        raise ValueError('ZONOS profile mismatch')
    evidence = {(x['asset_kind'], x['repo_id']): x for x in r73['rows']}
    if len(evidence) != 135: raise ValueError('R73 missing or duplicate rows')
    primary = 0
    for x in active:
        rid = x['repo_id']
        size = old[rid] if rid in old else (zonos if rid == 'Zyphra/ZONOS3-Mini' else byrepo[rid]['selected_bytes'])
        row = evidence[(x['asset_kind'], rid)]
        if row['primary_source_reference_bytes'] != size or row['download_approved'] is not False:
            raise ValueError('R73 source/approval mismatch ' + rid)
        primary += size
    extra = byrepo['ACE-Step/Ace-Step1.5']
    if extra['repo_id'] in ids: raise ValueError('ACE dependency misclassified as active asset')
    reuse = r62['QWEN_REUSE']['reused_occurrences']
    lookup = {f['path']: f for f in extra['files']}
    for f in reuse:
        ref = lookup[f['path']]
        if (ref['bytes'], ref.get('source_sha256'), ref.get('git_blob_sha1')) != (f['bytes'], f.get('sha256'), f.get('git_blob_sha1')):
            raise ValueError('Qwen SHA reuse mismatch ' + f['path'])
    dedup = sum(f['bytes'] for f in reuse)
    raw = v27['known_scope_content_union_bytes'] + primary - sum(old.values()) + extra['selected_bytes']
    adjusted = raw - dedup
    s = r73['summary']
    if (primary, raw, adjusted, dedup) != (s['primary_selected_source_bytes_simple_sum'],s['source_only_additive_scenario_bytes_not_final_archive'],s['v32_publisher_SHA_adjusted_source_only_scenario_bytes'],s['R62_publisher_SHA_reused_bytes']):
        raise ValueError('R73 scenario arithmetic mismatch')
    if j('queues/approved.json')['entries'] or s['owner_physical_disk_free_bytes'] is not None:
        raise ValueError('owner approval/physical disk gate was not preserved')
    return {'status':'PASS_SOURCE_SCOPE_ONLY','active':135,'old':126,'new':9,'primary_bytes':primary,'publisher_SHA_reused_bytes':dedup,'adjusted_source_scenario_bytes':adjusted,'physical_capacity_verified':False,'download_approved':False}

if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
