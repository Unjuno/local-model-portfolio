#!/usr/bin/env python3
"""Deterministic v20 -> v21 metadata transition; Python >=3.10, stdlib only.
No network, model execution, weight downloads, vault access, or approvals.
"""
from __future__ import annotations
import argparse
import copy
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD='v20-20261106'
REV='v21-20261106'
OVERLAY='catalog/revisions/v21-2026-11-06.json'
VIEW='catalog/effective-portfolio-2026-11-06-v21.json'
QUEUE='queues/proposed-v21-2026-11-06.json'
REPORT='docs/strategy/26-risk-evidence-selection-v21.md'
ACTIVE={'select','conditional'}
LOW='PASS_TOTAL_PARAMS_LT_150B'
UNKNOWN='UNVERIFIED_BLOCK_FINAL_LOCK'
REVIEW='OVER_150B_QUANT_REVIEW_REQUIRED'
CAP=150_000_000_000

def key(x): return x['asset_kind'].lower(),x['repo_id'].lower()
def integer(x): return isinstance(x,int) and not isinstance(x,bool)

def prepare(current,view,queue,overlay):
    c,v,q,o=copy.deepcopy((current,view,queue,overlay))
    if c.get('revision_id')!=OLD or v.get('revision_id')!=OLD or q.get('source_revision')!=OLD:
        raise ValueError('expected immutable v20 baseline')
    items=v.get('items',[])
    if len(items)!=154 or sum(x.get('portfolio_decision') in ACTIVE for x in items)!=108:
        raise ValueError('baseline counts must be 154/108')
    ids={key(x) for x in items}
    if len(ids)!=154 or any(x.get('download_approved') is not False for x in items):
        raise ValueError('duplicate baseline or changed authorization')
    if q.get('approved') is not False or q.get('download_enabled') is not False:
        raise ValueError('queue must be nonexecutable')
    if {key(x) for x in q.get('candidates',[])}!={key(x) for x in items if x['portfolio_decision'] in ACTIVE} or len(q['candidates'])!=108:
        raise ValueError('baseline queue mismatch')
    if o.get('revision_id')!=REV or o.get('previous_revision_id')!=OLD:
        raise ValueError('overlay revision mismatch')
    if o.get('archive_target_bytes')!=4_000_000_000_000 or o.get('minimum_free_bytes')!=200_000_000_000:
        raise ValueError('budget changed unexpectedly')
    additions=o.get('additions',[])
    if len(additions)!=5 or sum(x.get('portfolio_decision') in ACTIVE for x in additions)!=4:
        raise ValueError('expected four conditional and one HOLD')
    rank=max(x.get('forecast_priority',{}).get('rank',0) for x in items)
    reserve=0
    for i,x in enumerate(additions,1):
        if key(x) in ids: raise ValueError('duplicate asset '+x['repo_id'])
        ids.add(key(x))
        for name in ('url','reason_selected','quality_negative','evidence_date'):
            if not isinstance(x.get(name),str) or not x[name].strip(): raise ValueError('missing '+name)
        if not x['url'].startswith('https://'): raise ValueError('primary https URL required')
        if x.get('download_approved') is not False or x.get('fully_pinned_revision_sha') is not None or x.get('selected_file_bytes') is not None:
            raise ValueError('unreviewed input fabricates approval or pin')
        risk=x.get('restriction_assessment',{})
        if risk.get('probability') is not None or not risk.get('observed') or not risk.get('scenario'):
            raise ValueError('risk observation/scenario missing or probability invented')
        g=x.get('parameter_gate',{}); n=g.get('total_parameters'); status=g.get('status')
        active=x.get('portfolio_decision') in ACTIVE
        if x['asset_kind']=='dataset':
            if status!='NOT_APPLICABLE_TO_DATASET': raise ValueError('dataset model gate')
        elif x['asset_kind']=='model':
            if n is None:
                if status!=UNKNOWN: raise ValueError('unknown total must block lock')
                if active and not (x['portfolio_decision']=='conditional' and x.get('research_only_unknown_total_allow_conditional') is True and g.get('research_screening_exception')=='CONDITIONAL_RESEARCH_ONLY_NON_EXECUTABLE'):
                    raise ValueError('unknown total lacks research-only marker')
            elif not integer(n) or n<=0: raise ValueError('invalid total')
            elif n<CAP and status!=LOW: raise ValueError('invalid below-baseline status')
            elif n>=CAP:
                if active:
                    if status!='OVER_150B_QUANT_RUNTIME_VERIFIED':
                        raise ValueError('oversized active lacks verified status')
                    from scripts.check_parameter_cutoff import verified_quant_exception
                    if not verified_quant_exception(x):
                        raise ValueError('oversized active requires measured matched-memory exception')
                elif status not in (REVIEW,'OVER_150B_QUANT_RUNTIME_VERIFIED'):
                    raise ValueError('oversized research must have a review status')
        else: raise ValueError('unknown asset kind')
        x.setdefault('forecast_priority',{})['rank']=rank+i
        if active:
            b=x.get('selection_budget_cap_bytes')
            if not integer(b) or b<=0: raise ValueError('active addition missing planning cap')
            reserve+=b
            entry={'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'selection':x['portfolio_decision'],
                   'parameter_gate':status,'not_authorized':True,'download_approved':False,
                   'approved_lock':False,'selection_budget_cap_bytes':b}
            if status==UNKNOWN:
                entry.update(research_only=True,can_enter_approved_queue=False,requires_total_parameter_confirmation=True)
            q['candidates'].append(entry)
        items.append(x)
    if not integer(o.get('max_new_selection_budget_bytes')) or reserve>o['max_new_selection_budget_bytes']:
        raise ValueError('new reservations exceed cap')
    active=[x for x in items if x['portfolio_decision'] in ACTIVE]
    if len(items)!=159 or len(active)!=112: raise ValueError('result count mismatch')
    counts={'tracked':len(items),'active':len(active),'models':sum(x['asset_kind']=='model' for x in items),
            'datasets':sum(x['asset_kind']=='dataset' for x in items),
            'by_tier':dict(Counter(x['risk_tier'] for x in items)),
            'by_decision':dict(Counter(x['portfolio_decision'] for x in items)),
            'parameter_gate':dict(Counter(x['parameter_gate']['status'] for x in items if x['asset_kind']=='model'))}
    counts['by_forecast_wave']={w:{'active':sum(x in active and x.get('forecast_priority',{}).get('wave')==w for x in items),
                                  'inactive':sum(x not in active and x.get('forecast_priority',{}).get('wave')==w for x in items)} for w in ('S1','S2','S3')}
    size=lambda x:x.get('resource_screen',{}).get('source_all_repo_bytes')
    counts['resource_screen']={'tracked':len(items),'source_repo_bytes_unknown':sum(size(x) is None for x in items),
          'active_source_repo_bytes_unknown':sum(size(x) is None for x in active),
          'active_ge_100GB_repo_assets':sum(size(x) is not None and size(x)>=100_000_000_000 for x in active)}
    v['historical_budget_v20']=copy.deepcopy(v.get('budget',{}))
    v['budget']={'archive_limit_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
       'new_active_reservation_cap_bytes':reserve,'reservation_is_policy_cap_not_observed_bytes':True,
       'final_selected_total_bytes':None,'final_headroom_bytes':None,'physical_capacity_verified':False,
       'unknown_final_selected_asset_count':sum(x.get('selected_file_bytes') is None for x in active),
       'budget_status':'UNFINALIZED_DO_NOT_TREAT_MISSING_BYTES_AS_ZERO'}
    v.update(revision_id=REV,generated_date='2026-11-06',items=items,read_only_derived=True)
    v.setdefault('counts',{}).update(counts)
    c['expected'].update(counts)
    c['expected']['historical_budget_scenario_v20']=c['expected'].pop('budget_scenario',{})
    c['expected'].update(archive_limit_bytes=4_000_000_000_000,provisional_headroom_bytes=None,
                        provisional_active_repo_bytes_plus_fineweb_sample=None,budget_scenario=copy.deepcopy(v['budget']))
    pe=c['expected'].setdefault('parameter_evidence_review',{})
    pe.update(remaining_unknown=counts['parameter_gate'].get(UNKNOWN,0),
              remaining_active_unknown=sum(x['asset_kind']=='model' and x['parameter_gate']['status']==UNKNOWN for x in active),
              revision_note='v21 unknown totals remain blocked; published Holo4 size is screening, not full tensor certification.')
    c.update(revision_id=REV,generated_date='2026-11-06',materialized_catalog_path=VIEW,
             priority_worklist_path=QUEUE,latest_adopted_selection_path=OVERLAY,latest_selection_report_path=REPORT)
    c['ordered_overlays'].append(OVERLAY)
    note=' v21 adds Holo4-27B, SteerTTS, Maya2 Native and released Hcompany evaluation trajectories as conditional; StyleStream public subset HOLD. Model-specific imminent takedown unconfirmed; no new model/weight download authorization. Unknown full audio totals block preparation. Existing over150B matched-memory policy unchanged.'
    c['notes']=c.get('notes','')+note; c['application_rule']=c.get('application_rule','')+note
    c['statuses']={'draft':True,'download_approved':False,'selected_file_bytes_final':False}
    byid={key(x):x for x in items}
    q['candidates'].sort(key=lambda x:({'S1':0,'S2':1,'S3':2}.get(byid[key(x)].get('forecast_priority',{}).get('wave'),3),byid[key(x)].get('forecast_priority',{}).get('rank',0)))
    q.update(source_revision=REV,generated_at='2026-11-06',approved=False,download_enabled=False,
             description='112 active research selections; S1-first investigation only; no download authorization')
    return {'current':c,'view':v,'queue':q}

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def one(text,old,new):
    if text.count(old)!=1: raise ValueError('source patch anchor changed: '+old[:60])
    return text.replace(old,new)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--apply',action='store_true'); args=parser.parse_args()
    c=load('catalog/CURRENT.json')
    if c['revision_id']==REV:
        print('Already v21; refusing a second materialization.'); return
    v=load(c['materialized_catalog_path']); q=load(c['priority_worklist_path']); o=load(OVERLAY)
    if load('queues/approved.json')['entries']!=[]: raise ValueError('approval queue changed')
    result=prepare(c,v,q,o)
    files={'catalog/CURRENT.json':result['current'],VIEW:result['view'],QUEUE:result['queue']}
    # Preserve v20 historical checks; use CURRENT's own counts for current invariants.
    p='scripts/audit_selection_decisions.py'
    audit=one((ROOT/p).read_text(), '("v19-20261106", "v20-20261106")', '("v19-20261106", "v20-20261106", "v21-20261106")')
    tp='tests/test_quantized_memory_research.py'; test=(ROOT/tp).read_text()
    test=one(test,'        self.assertEqual(c["revision_id"],"v20-20261106")\n        self.assertEqual(len(v["items"]),154)\n        self.assertEqual(c["expected"]["active"],108)\n        self.assertEqual(len(q["candidates"]),108)',
       '        self.assertEqual(v["revision_id"],c["revision_id"])\n        self.assertEqual(len(v["items"]),c["expected"]["tracked"])\n        self.assertEqual(len(q["candidates"]),c["expected"]["active"])\n        historical=load("catalog/effective-portfolio-2026-11-06-v20.json")\n        self.assertEqual(len(historical["items"]),154)\n        self.assertEqual(sum(x["portfolio_decision"] in ("select","conditional") for x in historical["items"]),108)')
    hp='tests/test_catalog_v19.py'
    historical=one((ROOT/hp).read_text(), '"v20-20261106":(154,108)', '"v20-20261106":(154,108),"v21-20261106":(159,112)')
    intro='\n## 現行v21：配布制限の証拠と独自能力による追加選定\n\n[CURRENT](catalog/CURRENT.json)・[159資産](catalog/effective-portfolio-2026-11-06-v21.json)・[112件の非実行キュー](queues/proposed-v21-2026-11-06.json)。Holo4-27B、SteerTTS、Maya2 Native、Hcompany公開評価軌跡を4件conditionalに追加。StyleStreamは一部非公開・総数未確定のためHOLD。追加計画枠92GBは実測容量ではない。4TB上限、実空き200GB、150B超の量子化同等RAM規則、取得承認0は維持。[判断と一次出典](docs/strategy/26-risk-evidence-selection-v21.md)。以下のv20以前の件数は履歴。\n'
    texts={p:audit,tp:test,hp:historical,'README.md':one((ROOT/'README.md').read_text(),'# Local Model Portfolio\n','# Local Model Portfolio\n'+intro),
           'AGENTS.md':one((ROOT/'AGENTS.md').read_text(),'# エージェント作業規約\n','# エージェント作業規約\n'+intro)}
    # Scan all previous research files; do not treat a prior HOLD as fresh discovery.
    prior={}
    for x in o['additions']:
        matches=[]
        for f in (ROOT/'catalog/research').glob('*.json'):
            if x['repo_id'] in f.read_text(encoding='utf-8'): matches.append(str(f.relative_to(ROOT)))
        prior[x['repo_id']]=matches
    summary={'revision':REV,'tracked':159,'active':112,'new_conditional':4,'new_hold':1,
       'new_reservation_bytes':result['view']['budget']['new_active_reservation_cap_bytes'],
       'final_total_bytes':None,'approved_downloads':0,'prior_research_matches':prior,
       'verification_scope':'metadata transformation; full CI tests recorded separately'}
    if args.apply:
        for path,obj in files.items():
            dest=ROOT/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for path,content in texts.items(): (ROOT/path).write_text(content,encoding='utf-8')
        dest=ROOT/'catalog/preparation/2026-11-06-v21-integration-check.json'
        dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
