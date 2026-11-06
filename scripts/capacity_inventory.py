#!/usr/bin/env python3
"""Bounded, anonymous Hugging Face metadata census. Never download model payloads.

This is evidence collection, not an executable acquisition manifest. Repository
sizes do not establish selected dependency closure, runtime RAM or disk capacity.
"""
from __future__ import annotations
import concurrent.futures
import hashlib
import json
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'catalog/capacity/2026-11-06'
SHA = re.compile(r'^[0-9a-f]{40}$')
SAFE_DOC = re.compile(r'(^|/)(README\.md|config\.json|model_index\.json|[^/]+\.index\.json)$')
MAX_BODY = 8_000_000
MAX_PAGES = 160

def exact_sum(values):
    values = list(values)
    for value in values:
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError('invalid byte count')
    return None if None in values else sum(values)

def validate_url(url):
    p = urllib.parse.urlsplit(url)
    decoded = urllib.parse.unquote(p.path)
    if p.scheme != 'https' or p.netloc != 'huggingface.co' or p.fragment or '..' in decoded.split('/'):
        raise ValueError('untrusted metadata URL')
    api = re.match(r'^/api/(models|datasets)/[\w.-]+/[\w.-]+(?:/|$)', decoded)
    raw = re.match(r'^/(?:datasets/)?[\w.-]+/[\w.-]+/raw/[0-9a-f]{40}/(.+)$', decoded)
    if api:
        if '/resolve/' in decoded: raise ValueError('payload URL')
        return
    if raw and SAFE_DOC.search(raw.group(1)):
        return
    raise ValueError('only repository metadata and named small text documents allowed')

class MetadataRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def get(url, limit=MAX_BODY):
    validate_url(url)
    opener = urllib.request.build_opener(MetadataRedirect)
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent':'portfolio-metadata-census/1.0','Accept':'application/json,text/plain'})
            with opener.open(request, timeout=25) as response:
                body = response.read(limit + 1)
                if len(body) > limit: raise ValueError('metadata response exceeds byte limit')
                return body, response.headers.get('Link','')
        except urllib.error.HTTPError as exc:
            if exc.code in (429,500,502,503,504) and attempt < 2:
                time.sleep(2 ** attempt * 2)
                continue
            raise
        except (TimeoutError, urllib.error.URLError):
            if attempt == 2: raise
            time.sleep(2 ** attempt)

def normalize_file(row):
    path = row['path']
    if not path or path.startswith('/') or '\\' in path or '..' in PurePosixPath(path).parts:
        raise ValueError('unsafe repository path')
    lfs = row.get('lfs') or {}
    size = row.get('size')
    exact_sum([size, lfs.get('size')])
    if lfs.get('size') is not None:
        if size is not None and size != lfs['size']: raise ValueError('LFS size mismatch')
        size = lfs['size']
    digest = lfs.get('oid') or lfs.get('sha256')
    if digest and not re.fullmatch('[0-9a-f]{64}',digest): raise ValueError('invalid LFS SHA256')
    return {'path':path,'bytes':size,'sha256':digest,'git_blob_sha1':row.get('oid'),
            'identity_kind':'lfs_payload_sha256' if digest else 'git_blob_sha1' if row.get('oid') else 'unverified',
            'local_hash_verified':False}

def deduplicated_bytes(entries):
    unique = {}
    for scope, f in entries:
        size = f['bytes']
        exact_sum([size])
        identity = ('sha256',f['sha256']) if f.get('sha256') else (
            ('git-blob-sha1',f['git_blob_sha1']) if f.get('git_blob_sha1') else ('path',scope,f['path']))
        if identity in unique and unique[identity] != size: raise ValueError('same digest, different size')
        unique[identity] = size
    return exact_sum(unique.values())

def tree(kind, repo, rev, subpath='', recursive=True):
    url = f'https://huggingface.co/api/{kind}s/{repo}/tree/{rev}'
    if subpath: url += '/' + urllib.parse.quote(subpath, safe='/')
    url += '?recursive=' + ('true' if recursive else 'false') + '&expand=false&limit=1000'
    rows, seen = [], set()
    for _ in range(MAX_PAGES):
        if url in seen: raise ValueError('pagination loop')
        seen.add(url)
        body, link = get(url)
        page = json.loads(body)
        if not isinstance(page,list): raise ValueError('tree response is not a list')
        rows.extend(normalize_file(r) for r in page if r.get('type') == 'file')
        next_url = re.search(r'<([^>]+)>;\s*rel="next"',link)
        if not next_url:
            if len({r['path'] for r in rows}) != len(rows): raise ValueError('duplicate tree paths')
            return rows
        url = next_url.group(1)
        validate_url(url)
    raise ValueError('pagination limit reached; tree incomplete')

def documents(kind, repo, rev, files):
    names = [f['path'] for f in files if SAFE_DOC.search(f['path']) and f['bytes'] is not None and f['bytes'] <= 250_000]
    names.sort(key=lambda p:(p != 'README.md', '/' in p, p))
    docs = []
    prefix = 'datasets/' if kind == 'dataset' else ''
    for path in names[:24]:
        url = f'https://huggingface.co/{prefix}{repo}/raw/{rev}/{urllib.parse.quote(path, safe="/")}'
        try:
            body,_ = get(url,250_000)
            text = body.decode('utf-8')
            doc = {'path':path,'url':url,'observed_bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
            if path.endswith('.json'): doc['json'] = json.loads(text)
            else:
                doc['repo_reference_leads_not_verified_dependencies'] = sorted(set(re.findall(r'(?:huggingface\.co/|["\'])([\w.-]+/[\w.-]+)',text)))
                doc['card_text_archived'] = False
            docs.append(doc)
        except Exception as exc:
            docs.append({'path':path,'url':url,'error':type(exc).__name__+': '+str(exc)[:180]})
    return docs

def snapshot(item):
    kind,repo = item['asset_kind'],item['repo_id']
    result = {'asset_kind':kind,'repo_id':repo,'portfolio_decision':item['portfolio_decision'],
              'observed_at_utc':datetime.now(timezone.utc).isoformat(),
              'evidence_kind':'anonymous_publisher_api_metadata_not_local_payload_measurement',
              'download_authorized':False,'payload_bytes_downloaded':0,
              'tree_complete':False,'files':[], 'source_scope_bytes':None,
              'selected_files_bytes':None,'complete_dependency_bytes':None,
              'runtime_peak_ram_bytes':None,'local_reuse_verified':False,
              'prior_observed_access':item.get('observed_access'),
              'prior_revision':item.get('upstream_revision_sha_observed'),
              'requested_artifact':item.get('requested_artifact'),
              'required_dependencies_note':item.get('required_dependencies_note'),
              'parameter_gate_status':item.get('parameter_gate',{}).get('status')}
    try:
        if not re.fullmatch(r'[\w.-]+/[\w.-]+',repo): raise ValueError('unsupported repository identity')
        url=f'https://huggingface.co/api/{kind}s/{repo}'
        body,_=get(url)
        info=json.loads(body)
        head=info.get('sha')
        if not isinstance(head,str) or not SHA.fullmatch(head): raise ValueError('missing immutable head SHA')
        rev=item.get('fully_pinned_revision_sha') or head
        if not SHA.fullmatch(rev): raise ValueError('invalid pinned revision')
        result.update(source_api_url=url,head_revision_observed=head,pinned_revision=rev,
                      pinned_revision_origin='existing_explicit_pin' if item.get('fully_pinned_revision_sha') else 'head_observed_for_capacity_only_not_selection_approval',
                      gated=info.get('gated'),private=info.get('private'),
                      license_metadata=(info.get('cardData') or {}).get('license'),
                      metadata_sha256=hashlib.sha256(body).hexdigest(),
                      last_modified=info.get('lastModified'),
                      architecture_metadata=info.get('config'),
                      parameter_metadata=info.get('safetensors'))
        subpath='sample/10BT' if repo=='HuggingFaceFW/fineweb-edu' else ''
        result['source_scope']=subpath or 'repository_all_files_not_selection'
        files=tree(kind,repo,rev,subpath)
        if subpath:
            roots=tree(kind,repo,rev,recursive=False)
            files.extend(f for f in roots if f['path'] not in {x['path'] for x in files})
        files.sort(key=lambda f:f['path'])
        result.update(files=files,tree_complete=True,source_scope_bytes=exact_sum(f['bytes'] for f in files),
                      file_count=len(files),documentation=documents(kind,repo,rev,files))
        result['metadata_change_requires_review']=bool(result['prior_revision'] and result['prior_revision']!=rev)
    except Exception as exc:
        result['error']=type(exc).__name__+': '+str(exc)[:300]
    return result

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def history_index():
    records=[]
    def walk(obj,path):
        if isinstance(obj,dict):
            if isinstance(obj.get('repo_id'),str):
                keep={k:v for k,v in obj.items() if k in ('repo_id','decision','portfolio_decision','reason','why_not_add','reversal_condition','negative_evidence','next_validation')}
                if len(keep)>1: records.append({'source_path':path,**keep})
            for v in obj.values(): walk(v,path)
        elif isinstance(obj,list):
            for v in obj: walk(v,path)
    for p in sorted((ROOT/'catalog/research').glob('*.json')):
        walk(json.loads(p.read_text(encoding='utf-8')),str(p.relative_to(ROOT)))
    return records

def main():
    current=json.loads((ROOT/'catalog/CURRENT.json').read_text())
    view=json.loads((ROOT/current['materialized_catalog_path']).read_text())
    limits=json.loads((ROOT/'policies/limits.json').read_text())
    assert current['revision_id']=='v22-20261106' and len(view['items'])==163
    assert limits['archive_target_bytes']==4_000_000_000_000 and limits['minimum_free_bytes']==200_000_000_000
    active=[x for x in view['items'] if x['portfolio_decision'] in ('select','conditional')]
    assert len(active)==116 and len({(x['asset_kind'],x['repo_id'].casefold()) for x in active})==116
    baseline={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('catalog/CURRENT.json',current['materialized_catalog_path'],current['priority_worklist_path'],'queues/approved.json','policies/limits.json')}
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        tasks={pool.submit(snapshot,x):x for x in active}
        for task in concurrent.futures.as_completed(tasks):
            r=task.result()
            path=OUT/'sources'/(r['asset_kind']+'--'+r['repo_id'].replace('/','--')+'.json')
            dump(path,r)
            rows.append({k:v for k,v in r.items() if k not in ('files','documentation','architecture_metadata','parameter_metadata')})
            rows[-1]['snapshot_path']=str(path.relative_to(ROOT))
            print(json.dumps({'repo':r['repo_id'],'files':r.get('file_count'),'bytes':r['source_scope_bytes'],'error':r.get('error')},ensure_ascii=False),flush=True)
    rows.sort(key=lambda r:(r['asset_kind'],r['repo_id']))
    summary={'schema_version':1,'source_revision':current['revision_id'],'tracked':163,'active':116,
             'generated_at_utc':datetime.now(timezone.utc).isoformat(),
             'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             'complete_tree_count':sum(r['tree_complete'] for r in rows),
             'failed_or_incomplete_count':sum(not r['tree_complete'] for r in rows),
             'known_source_scope_bytes_sum_not_selected_capacity':sum(r['source_scope_bytes'] for r in rows if r['source_scope_bytes'] is not None),
             'final_selected_bytes':None,'final_deduplicated_bytes':None,'peak_acquisition_bytes':None,
             'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,'local_duplicate_bytes':None,
             'physical_measurement_status':'NO_CONNECTED_OWNER_DEVICE; CI filesystem is not the archive',
             'download_enabled':False,'payload_bytes_downloaded':0,'baseline_sha256':baseline,'items':rows}
    dump(OUT/'inventory.json',summary)
    dump(OUT/'prior-research-index.json',history_index())
    for p,h in baseline.items(): assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    print('SUMMARY',json.dumps({k:v for k,v in summary.items() if k not in ('items','baseline_sha256')},ensure_ascii=False),flush=True)

if __name__=='__main__': main()
