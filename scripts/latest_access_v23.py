#!/usr/bin/env python3
"""Bounded anonymous metadata and license checks. Never retrieve model payloads."""
from __future__ import annotations
import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('catalog/research/2026-11-06-latest-v23')
BASE = Path('catalog/capacity/2026-11-06')
CANDIDATES = ['pfnet/plamo-3-translate-0.8b', 'pfnet/plamo-3-translate-8b',
              'ConwayResearch/Underdog-Saluki-27B-1.0']
SHA = re.compile(r'^[0-9a-f]{40}$')
TEXT_NAMES = {'LICENSE','LICENSE.md','LICENSE.txt','LICENSE/en','LICENSE/ja','NOTICE','README.md'}


def normalized(value):
    if isinstance(value, list):
        return sorted(json.dumps(x, sort_keys=True) for x in value)
    return value


def changes(prior, live):
    pairs = {
        'revision_changed': (prior.get('pinned_revision'), live.get('sha')),
        'gated_changed': (prior.get('gated'), live.get('gated')),
        'license_metadata_changed': (prior.get('license_metadata'), (live.get('cardData') or {}).get('license')),
    }
    return {key: None if a is None or b is None else normalized(a) != normalized(b)
            for key, (a, b) in pairs.items()}


def detect_license(text):
    lower = text.lower()
    if any(x in lower for x in ('attribution-noncommercial 4.0','creativecommons.org/licenses/by-nc/4.0','cc by-nc 4.0')):
        return 'cc-by-nc-4.0'
    if 'plamo community license' in lower:
        return 'plamo-community'
    if 'apache license' in lower and 'version 2.0' in lower:
        return 'apache-2.0'
    return 'undetermined'


def validate_text_url(url):
    p = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(p.path)
    if p.scheme != 'https' or p.netloc != 'huggingface.co' or p.query or p.fragment:
        raise ValueError('only anonymous immutable HF text URLs allowed')
    if '..' in path.split('/') or '\\' in path:
        raise ValueError('path traversal blocked')
    m = re.fullmatch(r'/[\w.-]+/[\w.-]+/raw/([0-9a-f]{40})/(.+)', path)
    if not m or m.group(2) not in TEXT_NAMES:
        raise ValueError('payload or unpinned document blocked')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('text redirects must be reviewed, not followed automatically')


def text_evidence(repo, rev, name):
    url = 'https://huggingface.co/'+repo+'/raw/'+rev+'/'+name
    validate_text_url(url)
    result = {'url':url, 'repo_id':repo, 'revision':rev, 'path':name,
              'text_role':'license_terms' if name.startswith('LICENSE') else 'provenance_notice',
              'marker_is_not_legal_clearance':True}
    try:
        opener = urllib.request.build_opener(NoRedirect)
        request = urllib.request.Request(url, headers={'User-Agent':'portfolio-readonly-text/1.0'})
        with opener.open(request, timeout=20) as response:
            raw = response.read(262145)
        if len(raw)>262144:
            raise ValueError('license text exceeds safety bound')
        text = raw.decode('utf-8')
        result.update(observed_bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                      license_marker=detect_license(text), retrieved=True)
    except Exception as exc:
        result.update(retrieved=False, error=type(exc).__name__+': '+str(exc)[:180])
    return result


def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def dump(path, obj):
    p=ROOT/path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')


def audit_active(item):
    from scripts.capacity_inventory import get
    kind, repo = item['asset_kind'], item['repo_id']
    path = BASE/'sources'/(kind+'--'+repo.replace('/','--')+'.json')
    if not (ROOT/path).is_file():
        path = BASE/'followup-sources'/(repo.replace('/','--')+'.json')
    prior = load(path) if (ROOT/path).is_file() else {}
    fields = ['sha','gated','private','lastModified','cardData']
    query = urllib.parse.urlencode([('expand[]',x) for x in fields])
    url = 'https://huggingface.co/api/'+kind+'s/'+repo+'?'+query
    record = {'asset_kind':kind,'repo_id':repo,'primary_url':url,
              'prior_snapshot_path':str(path),'prior_observed_at_utc':prior.get('observed_at_utc'),
              'observed_at_utc':datetime.now(timezone.utc).isoformat(),
              'selection_changed':False,'personal_access_verified':False,
              'download_authorized':False,'specific_government_order_verified':False}
    try:
        body,_ = get(url)
        live = json.loads(body)
        if not isinstance(live,dict) or not SHA.fullmatch(live.get('sha','')):
            raise ValueError('head metadata has no valid revision SHA')
        record.update(metadata_status='OBSERVED',live_revision=live['sha'],
                      live_gated=live.get('gated'),live_private=live.get('private'),
                      live_license=(live.get('cardData') or {}).get('license'),
                      live_last_modified=live.get('lastModified'),
                      prior_revision=prior.get('pinned_revision'),prior_gated=prior.get('gated'),
                      prior_license=prior.get('license_metadata'),comparison=changes(prior,live),
                      comparison_scope='live_head_vs_previous_metadata_snapshot_not_proof_of_new_release_or_ban')
    except Exception as exc:
        record.update(metadata_status='UNRESOLVED_NOT_PROOF_OF_DELETION',
                      error=type(exc).__name__+': '+str(exc)[:180],
                      comparison={k:None for k in ('revision_changed','gated_changed','license_metadata_changed')})
    return record


def candidate(repo, view):
    from scripts.capacity_inventory import snapshot, get
    src = snapshot({'asset_kind':'model','repo_id':repo,'portfolio_decision':'research_only'})
    filename=repo.replace('/','--')+'.json'
    dump(OUT/'sources'/filename,src)
    prior=[]
    for path in (ROOT/'catalog/research').glob('*.json'):
        if repo in path.read_text(encoding='utf-8'):
            prior.append(str(path.relative_to(ROOT)))
    row={'repo_id':repo,'snapshot_path':str(OUT/'sources'/filename),
         'pinned_revision':src.get('pinned_revision'),'source_repository_bytes':src.get('source_scope_bytes'),
         'source_tree_complete':src.get('tree_complete'),'source_repo_bytes_not_selected_bytes':True,
         'prior_research_matches':prior,
         'already_in_catalog':any(x['repo_id'].casefold()==repo.casefold() for x in view['items']),
         'currently_selected':any(x['repo_id'].casefold()==repo.casefold() and x['portfolio_decision'] in ('select','conditional') for x in view['items']),
         'observed_access':src.get('gated'),'license_metadata':src.get('license_metadata'),
         'selected_file_bytes':None,'complete_dependency_bytes':None,
         'download_authorized':False,'regulation_probability':None,
         'license_text_evidence':[],'history_evidence':[]}
    rev=src.get('pinned_revision')
    if rev and SHA.fullmatch(rev):
        paths={x['path'] for x in src.get('files',[])}
        names=[x for x in ('LICENSE','LICENSE.md','LICENSE.txt','LICENSE/en','LICENSE/ja','NOTICE') if x in paths]
        row['license_text_evidence']=[text_evidence(repo,rev,name) for name in names]
    if repo.startswith('pfnet/'):
        row.update(decision='RESEARCH_PRIORITY_TRANSLATION_NO_AUTOMATIC_ADDITION',
          public_announcement_date='2026-11-05',
          announcement_date_is_not_repository_creation_date=True,
          primary_announcement='https://www.preferred.jp/en/news/pr20261105',
          primary_development='https://www.preferred.jp/en/blog/tech/plamo-3-translate-weight-release',
          preservation_value='Translation-specific SFT/DPO and distilled variants, Japanese glossary/context control; distinct from generic chat weights.',
          negative_evidence='Provider benchmarks only; 53 languages do not imply every language pair equally good; custom code and PLaMo community terms need exact review. Do not collect all sizes/formats.',
          next_action='Compare 0.8B vs 8B with already-selected multilingual and translation assets; choose a single justified representative after full file and dependency accounting.')
    else:
        row.update(decision='LICENSE_CHANGE_PRIMARY_HISTORY_REVIEW_NOT_BAN_PROOF',
          preservation_value='Potential specialized tool-use/quantization-related posttraining; distinct learned weights beyond upstream must be established.',
          negative_evidence='License metadata change is not government regulation; low bit size and vendor agent scores alone do not establish independent learned value.',
          next_action='Retain pre/post license evidence; do not infer retroactive termination of older grants or bypass new access terms.')
        try:
            body,_=get('https://huggingface.co/api/models/'+repo+'/commits/main?limit=20')
            commits=json.loads(body)
            if not isinstance(commits,list): raise ValueError('commit history not a list')
            row['history_evidence']=[{k:c.get(k) for k in ('id','date','title')} for c in commits[:20]]
            candidates=[c for c in commits[:12] if SHA.fullmatch(c.get('id','')) and c['id']!=rev]
            for commit in candidates[:5]:
                evidence=text_evidence(repo,commit['id'],'LICENSE')
                evidence['source_commit_date']=commit.get('date')
                row['license_text_evidence'].append(evidence)
                if evidence.get('license_marker')=='apache-2.0': break
        except Exception as exc:
            row['history_error']=type(exc).__name__+': '+str(exc)[:180]
    return row


def main():
    current=load('catalog/CURRENT.json');view=load(current['materialized_catalog_path'])
    assert current['revision_id']=='v23-20261106' and len(view['items'])==165
    active=[x for x in view['items'] if x['portfolio_decision'] in ('select','conditional')]
    assert len(active)==118 and not load('queues/approved.json')['entries']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records=list(pool.map(audit_active,active))
    assert len({(r['asset_kind'],r['repo_id']) for r in records})==118
    dump(OUT/'active-access-checks.json',{'source_revision':current['revision_id'],'records':records})
    reviews=[candidate(repo,view) for repo in CANDIDATES]
    dump(OUT/'candidate-decisions.json',{'date':'2026-11-06','formal_selection_changes':0,'candidates':reviews})
    summary={'date':'2026-11-06','source_revision':current['revision_id'],'tracked':165,'active':118,
             'checked':len(records),'metadata_observed':sum(x['metadata_status']=='OBSERVED' for x in records),
             'unresolved':sum(x['metadata_status']!='OBSERVED' for x in records),
             'changes':{k:[x['repo_id'] for x in records if x['comparison'][k] is True]
                        for k in ('revision_changed','gated_changed','license_metadata_changed')},
             'scope':'Current anonymous publisher metadata vs previous snapshots. Errors are not deletions; lastModified is not weight release date.',
             'comparison_coverage':{k:{'changed':sum(x['comparison'][k] is True for x in records),
                    'unchanged':sum(x['comparison'][k] is False for x in records),
                    'unknown':sum(x['comparison'][k] is None for x in records)}
                    for k in ('revision_changed','gated_changed','license_metadata_changed')},
             'candidate_reviews':len(reviews),'formal_selection_changes':0,'download_authorized':False,
             'weight_payload_bytes_downloaded':0,'owner_disk_connected':False,
             'specific_regulatory_probabilities_invented':False}
    dump(OUT/'freshness-summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
