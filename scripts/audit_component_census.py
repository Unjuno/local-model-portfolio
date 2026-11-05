#!/usr/bin/env python3
"""Read-only R22 evidence validation. Python 3.10+, stdlib; no network or weights."""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
DTYPE_BYTES={'BF16':2,'F16':2,'F32':4}

def verify_support_bytes(data: bytes, record: dict[str, Any]) -> str:
    """Validate resolved metadata. An LFS pointer's Git SHA is not its content SHA."""
    size=record.get('bytes')
    if type(size) is not int or len(data)!=size: raise ValueError('metadata byte count differs')
    sha=record.get('source_sha256')
    if sha:
        if not re.fullmatch(r'[0-9a-f]{64}',sha) or hashlib.sha256(data).hexdigest()!=sha:
            raise ValueError('source SHA-256 mismatch')
        return 'source_sha256'
    expected=record.get('git_blob_sha1')
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if not isinstance(expected,str) or not re.fullmatch(r'[0-9a-f]{40}',expected) or blob!=expected:
        raise ValueError('Git blob mismatch')
    return 'git_blob_sha1'

def audit(e: dict[str, Any], p: dict[str, Any]) -> list[str]:
    """Check exported census against pinned R21 identity and arithmetic, not model quality."""
    errors=[]
    for k in ('download_authorized','auto_execute','auto_seed','user_disk_changed','formal_catalog_changed'):
        if e.get(k) is not False: errors.append(f'{k} must remain false')
    if e.get('weight_data_bytes_read')!=0: errors.append('weight data unexpectedly read')
    refs={(r['key'],f['path']):(r,f) for r in p['repositories'] for f in r['files']}
    expected_weights={k for k,(_,f) in refs.items() if f['role']=='weight'}
    rows=e.get('weight_headers',[])
    keys=[(r.get('repository_key'),r.get('path')) for r in rows]
    if set(keys)!=expected_weights or len(keys)!=len(set(keys)): errors.append('weight file inventory differs')
    components=Counter()
    for row in rows:
        key=(row.get('repository_key'),row.get('path'))
        if key not in refs: errors.append(f'unknown weight {key}'); continue
        repo,ref=refs[key]
        for k,expected in [('revision',repo['revision']),('repo_id',repo['repo_id']),('file_bytes',ref['bytes']),('source_sha256',ref['source_sha256'])]:
            if row.get(k)!=expected: errors.append(f'{key}: {k} differs from pinned source')
        if row.get('full_weight_hash_verified') is not False or row.get('weight_data_bytes_read')!=0:
            errors.append(f'{key}: metadata read cannot prove full payload identity')
        if not isinstance(row.get('metadata_sha256'),str) or not re.fullmatch('[0-9a-f]{64}',row['metadata_sha256']):
            errors.append(f'{key}: invalid header digest')
        counts=row.get('scalars_by_dtype',{})
        if not counts or any(type(v) is not int or v<=0 for v in counts.values()):
            errors.append(f'{key}: invalid scalar counts'); continue
        total=sum(counts.values())
        if row.get('scalar_total')!=total: errors.append(f'{key}: scalar sum mismatch')
        components[row['component']]+=total
        if row.get('format')=='safetensors':
            if any(k not in DTYPE_BYTES for k in counts): errors.append(f'{key}: dtype'); continue
            payload=sum(DTYPE_BYTES[k]*v for k,v in counts.items())
            if row.get('header_json_bytes',-9)+8!=row.get('metadata_bytes') or row.get('metadata_bytes')!=row.get('tensor_data_start'):
                errors.append(f'{key}: header offsets')
            if payload+row.get('tensor_data_start',0)!=row['file_bytes']: errors.append(f'{key}: shape/dtype/file length differs')
        elif row.get('format')=='gguf-v3':
            if set(counts)-{'0','1','12','14'}: errors.append(f'{key}: unsupported quant type'); continue
            payload=4*counts.get('0',0)+2*counts.get('1',0)
            for q,b in [('12',144),('14',210)]:
                if counts.get(q,0)%256: errors.append(f'{key}: quant block alignment')
                payload+=(counts.get(q,0)//256)*b
            start=((row['metadata_bytes']+31)//32)*32
            if start!=row['tensor_data_start']: errors.append(f'{key}: tensor region alignment')
            padding=row['file_bytes']-start-payload
            if not 0<=padding<=31*row['tensor_count']: errors.append(f'{key}: quant size/padding inconsistent')
        else: errors.append(f'{key}: unknown format')
    if dict(components)!=e.get('component_scalars'): errors.append('component totals differ')
    for key,package in e.get('packages',{}).items():
        if any(x not in components for x in package['components']): errors.append(f'{key}: missing component')
        total=sum(components.get(x,0) for x in package['components'])
        if total!=package.get('serialized_scalar_total') or not 0<total<150_000_000_000: errors.append(f'{key}: total/150B test')
        if package.get('actual_user_peak_ram_bytes') is not None: errors.append(f'{key}: fabricated hardware measurement')
    supports=e.get('support_verification',{}); ss=supports.get('files',[])
    sk=[(r['repository_key'],r['path']) for r in ss]
    expected_support={k for k,(_,f) in refs.items() if f['role']!='weight'}
    if set(sk)!=expected_support or len(sk)!=len(set(sk)): errors.append('support inventory differs')
    if len(ss)!=supports.get('count') or sum(x['bytes'] for x in ss)!=supports.get('verified_bytes'): errors.append('support arithmetic differs')
    for row in ss:
        key=(row['repository_key'],row['path'])
        if key not in refs: continue
        _,ref=refs[key]
        kind='source_sha256' if ref.get('source_sha256') else 'git_blob_sha1'
        if row['bytes']!=ref['bytes'] or row.get('verified_against')!=kind or row.get('identity_matches') is not True: errors.append(f'{key}: support identity')
        if not re.fullmatch('[0-9a-f]{64}',row.get('observed_sha256','')): errors.append(f'{key}: observed hash')
        if kind=='source_sha256' and row['observed_sha256']!=ref['source_sha256']: errors.append(f'{key}: source hash mismatch')
    pairs=e.get('adapter_compatibility',{})
    if pairs.get('pairs')!=224 or pairs.get('matched_pairs')!=224 or pairs.get('unmatched_pairs')!=0: errors.append('adapter target mismatch')
    conflicts=e.get('publisher_checksum_discrepancies',[])
    if {x.get('path') for x in conflicts}!={'README.md','inference.py'}: errors.append('publisher checksum discrepancies lost')
    smap={(x['repository_key'],x['path']):x for x in ss}
    for row in conflicts:
        actual=smap.get((row['repository_key'],row['path']),{}).get('observed_sha256')
        if actual!=row.get('observed_sha256') or row.get('publisher_sha256')==actual: errors.append('checksum discrepancy incorrectly resolved')
    return errors

if __name__=='__main__':
    try:
        e=json.loads((ROOT/'catalog/preparation/2026-11-05-component-census.json').read_text())
        p=json.loads((ROOT/e['source_manifest']).read_text())
        problems=audit(e,p)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        problems=[f'Invalid or missing evidence: {exc}']
    for problem in problems: print('FAIL:',problem)
    if problems: raise SystemExit(1)
    print('PASS R22: ten weight headers, 37 support identities, two checksum discrepancies retained; no payload approval.')
