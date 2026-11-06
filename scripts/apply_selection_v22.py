#!/usr/bin/env python3
"""Insurance-first v21 -> v22 catalog transition. Python >=3.10, stdlib only.
No network, vault access, model execution, payload transfer or approvals.
"""
from __future__ import annotations
import argparse
import copy
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD='v21-20261106'; REV='v22-20261106'
OVERLAY='catalog/revisions/v22-2026-11-06.json'
VIEW='catalog/effective-portfolio-2026-11-06-v22.json'
QUEUE='queues/proposed-v22-2026-11-06.json'
PLAN='catalog/preparation/2026-11-06-insurance-bundles-v22.json'
POLICY='policies/archival-insurance.json'
REPORT='docs/strategy/27-insurance-first-selection-v22.md'
ACTIVE={'select','conditional'}
LOW='PASS_TOTAL_PARAMS_LT_150B'; UNKNOWN='UNVERIFIED_BLOCK_FINAL_LOCK'
CAP=150_000_000_000

def key(x): return x['asset_kind'].lower(),x['repo_id'].lower()
def integer(x): return isinstance(x,int) and not isinstance(x,bool)

def prepare(current,view,queue,overlay):
    c,v,q,o=copy.deepcopy((current,view,queue,overlay))
    if (c.get('revision_id'),v.get('revision_id'),q.get('source_revision'))!=(OLD,OLD,OLD):
        raise ValueError('expected v21 baseline')
    items=v.get('items',[]); ids={key(x) for x in items}
    if len(items)!=159 or len(ids)!=159 or sum(x.get('portfolio_decision') in ACTIVE for x in items)!=112:
        raise ValueError('baseline must have 159 identities and 112 active')
    if any(x.get('download_approved') is not False for x in items):
        raise ValueError('baseline download authorization changed')
    if q.get('approved') is not False or q.get('download_enabled') is not False:
        raise ValueError('baseline queue executable')
    if len(q.get('candidates',[]))!=112 or {key(x) for x in q['candidates']}!={key(x) for x in items if x['portfolio_decision'] in ACTIVE}:
        raise ValueError('baseline queue mismatch')
    if any(x.get('not_authorized') is not True or x.get('download_approved') is not False for x in q['candidates']):
        raise ValueError('baseline queue entry authorized')
    if (o.get('revision_id'),o.get('previous_revision_id'))!=(REV,OLD):
        raise ValueError('overlay revision mismatch')
    if (o.get('archive_target_bytes'),o.get('minimum_free_bytes'))!=(4_000_000_000_000,200_000_000_000):
        raise ValueError('resource policy changed')
    additions=o.get('additions',[])
    if len(additions)!=4 or any(x.get('portfolio_decision')!='conditional' for x in additions):
        raise ValueError('expected four conditional archival selections')
    reserve=0; rank=max(x.get('forecast_priority',{}).get('rank',0) for x in items)
    for offset,x in enumerate(additions,1):
        if key(x) in ids: raise ValueError('duplicate asset '+x['repo_id'])
        ids.add(key(x))
        for field in ('url','reason_selected','quality_negative','evidence_date'):
            if not isinstance(x.get(field),str) or not x[field].strip(): raise ValueError('missing '+field)
        if not x['url'].startswith('https://'): raise ValueError('https primary URL required')
        if x.get('download_approved') is not False or x.get('fully_pinned_revision_sha') is not None or x.get('selected_file_bytes') is not None:
            raise ValueError('approval or final pin/bytes fabricated')
        risk=x.get('restriction_assessment',{})
        if risk.get('probability') is not None or not risk.get('observed') or not risk.get('scenario'):
            raise ValueError('restriction fact/scenario invalid')
        b=x.get('preservation_bundle',{})
        if not b.get('learned_outcome') or not isinstance(b.get('must_preserve'),list) or not b['must_preserve']:
            raise ValueError('preservation bundle absent')
        g=x.get('parameter_gate',{}); n=g.get('total_parameters'); status=g.get('status')
        if x['asset_kind']=='dataset':
            if status!='NOT_APPLICABLE_TO_DATASET': raise ValueError('dataset gate invalid')
        elif x['asset_kind']=='model':
            if n is None:
                if status!=UNKNOWN or x.get('research_only_unknown_total_allow_conditional') is not True or g.get('research_screening_exception')!='CONDITIONAL_RESEARCH_ONLY_NON_EXECUTABLE':
                    raise ValueError('unknown total must remain research-only and blocked')
            elif not integer(n) or n<=0: raise ValueError('invalid total parameter count')
            elif n<CAP:
                if status!=LOW: raise ValueError('incorrect below-baseline screen')
            else:
                if status!='OVER_150B_QUANT_RUNTIME_VERIFIED': raise ValueError('oversized candidate lacks measured exception')
                from scripts.check_parameter_cutoff import verified_quant_exception
                if not verified_quant_exception(x): raise ValueError('matched-memory evidence incomplete')
        else: raise ValueError('invalid asset kind')
        cap=x.get('selection_budget_cap_bytes')
        if not integer(cap) or cap<=0: raise ValueError('planning cap absent')
        reserve+=cap; x.setdefault('forecast_priority',{})['rank']=rank+offset
        entry={'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'selection':'conditional',
               'parameter_gate':status,'not_authorized':True,'download_approved':False,
               'approved_lock':False,'selection_budget_cap_bytes':cap}
        if status==UNKNOWN:
            entry.update(research_only=True,can_enter_approved_queue=False,requires_total_parameter_confirmation=True)
        q['candidates'].append(entry); items.append(x)
    if not integer(o.get('max_new_selection_budget_bytes')) or reserve>o['max_new_selection_budget_bytes']:
        raise ValueError('new planning caps exceed allocation')
    active=[x for x in items if x['portfolio_decision'] in ACTIVE]
    if len(items)!=163 or len(active)!=116: raise ValueError('result counts inconsistent')
    counts={'tracked':len(items),'active':len(active),
      'models':sum(x['asset_kind']=='model' for x in items),'datasets':sum(x['asset_kind']=='dataset' for x in items),
      'by_tier':dict(Counter(x['risk_tier'] for x in items)),
      'by_decision':dict(Counter(x['portfolio_decision'] for x in items)),
      'parameter_gate':dict(Counter(x['parameter_gate']['status'] for x in items if x['asset_kind']=='model'))}
    counts['by_forecast_wave']={w:{'active':sum(x['portfolio_decision'] in ACTIVE and x.get('forecast_priority',{}).get('wave')==w for x in items),
      'inactive':sum(x['portfolio_decision'] not in ACTIVE and x.get('forecast_priority',{}).get('wave')==w for x in items)} for w in ('S1','S2','S3')}
    size=lambda x:x.get('resource_screen',{}).get('source_all_repo_bytes')
    counts['resource_screen']={'tracked':len(items),'source_repo_bytes_unknown':sum(size(x) is None for x in items),
      'active_source_repo_bytes_unknown':sum(size(x) is None for x in active),
      'active_ge_100GB_repo_assets':sum(size(x) is not None and size(x)>=100_000_000_000 for x in active)}
    v['historical_budget_v21']=copy.deepcopy(v.get('budget',{}))
    budget={'archive_limit_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
      'new_active_reservation_cap_bytes':reserve,'reservation_is_policy_cap_not_observed_bytes':True,
      'final_selected_total_bytes':None,'final_headroom_bytes':None,'physical_capacity_verified':False,
      'unknown_final_selected_asset_count':sum(x.get('selected_file_bytes') is None for x in active),
      'shared_base_savings_verified':False,'budget_status':'UNFINALIZED_DO_NOT_TREAT_MISSING_BYTES_AS_ZERO'}
    v.update(revision_id=REV,generated_date='2026-11-06',items=items,budget=budget,read_only_derived=True)
    v.setdefault('counts',{}).update(counts); c['expected'].update(counts)
    c['expected']['historical_budget_scenario_v21']=c['expected'].pop('budget_scenario',{})
    c['expected'].update(archive_limit_bytes=4_000_000_000_000,budget_scenario=copy.deepcopy(budget),
                         provisional_headroom_bytes=None,provisional_active_repo_bytes_plus_fineweb_sample=None)
    c['expected'].setdefault('parameter_evidence_review',{}).update(
      remaining_unknown=counts['parameter_gate'].get(UNKNOWN,0),
      remaining_active_unknown=sum(x['asset_kind']=='model' and x['parameter_gate']['status']==UNKNOWN for x in active),
      revision_note='Insurance selection is not a complete tensor census or runtime certification.')
    c.update(revision_id=REV,generated_date='2026-11-06',materialized_catalog_path=VIEW,
      priority_worklist_path=QUEUE,latest_adopted_selection_path=OVERLAY,latest_selection_report_path=REPORT,
      archival_insurance_policy_path=POLICY,insurance_preparation_worklist_path=PLAN)
    c['ordered_overlays'].append(OVERLAY)
    note=' v22 insurance-first: preserve learned outcomes if public distribution disappears; risk forecasts order work, not blanket eligibility. Four prior-researched artifacts adopted conditionally; no original item removed, no payload approval, unknown totals remain blocked.'
    c['notes']=c.get('notes','')+note; c['application_rule']=c.get('application_rule','')+note
    c['statuses']={'draft':True,'download_approved':False,'selected_file_bytes_final':False}
    byid={key(x):x for x in items}
    stage=lambda x:{'S1':1,'S2':2,'S3':3}.get(x.get('forecast_priority',{}).get('wave'),3)
    q['candidates'].sort(key=lambda x:(stage(byid[key(x)]),byid[key(x)].get('forecast_priority',{}).get('rank',0)))
    q.update(source_revision=REV,generated_at='2026-11-06',approved=False,download_enabled=False,
      description='116 archival research selections; hypothetical early restriction orders preparation, not acquisition permission.')
    work=[]
    for x in sorted(active,key=lambda x:(stage(x),x.get('forecast_priority',{}).get('rank',0))):
        blocked=x.get('parameter_gate',{}).get('status')==UNKNOWN
        work.append({'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'stage':stage(x),
          'is_new_v22':key(x) in {key(a) for a in additions},
          'next_action':'PUBLIC_METADATA_PARAMETER_CENSUS_ONLY' if blocked else 'RIGHTS_REVISION_AND_DEPENDENCY_INVENTORY',
          'preservation_bundle':x.get('preservation_bundle',{
             'must_preserve':['selected learned/data artifacts','configuration and applicable tokenizer/processor',
                              'necessary learned dependencies','source/license notices','compatible runtime metadata'],
             'fixed_manifest_complete':False}),
          'selected_bytes':x.get('selected_file_bytes'),'download_approved':False,'not_authorized':True})
    plan={'schema_version':1,'source_revision':REV,'policy_path':POLICY,'download_enabled':False,
      'scope':'Preparation worklist, NOT downloader manifest; unknown totals allow public metadata census only',
      'critical_dependencies_travel_with_parent':True,'shared_dependency_hash_reuse_verified':False,
      'stage_meaning':{'1':'hypothetical early-restriction capabilities','2':'general/frontier/specialist learned outcomes','3':'broad baseline/data/reproduction insurance'},
      'priority_does_not_establish_ban_probability':True,'items':work}
    return {'current':c,'view':v,'queue':q,'plan':plan}

def load(path):
    target=(ROOT/path).resolve()
    if not target.is_relative_to(ROOT): raise ValueError('path outside repository')
    return json.loads(target.read_text(encoding='utf-8'))

def replace_once(text,old,new):
    if text.count(old)!=1: raise ValueError('patch anchor changed: '+old[:70])
    return text.replace(old,new)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--apply',action='store_true'); args=ap.parse_args()
    c=load('catalog/CURRENT.json')
    if c['revision_id']==REV:
        print('Already v22; no changes'); return
    if load('queues/approved.json')['entries']: raise ValueError('approved queue changed')
    limits=load('policies/limits.json')
    if (limits['archive_target_bytes'],limits['minimum_free_bytes'])!=(4_000_000_000_000,200_000_000_000):
        raise ValueError('limits changed')
    o=load(OVERLAY); result=prepare(c,load(c['materialized_catalog_path']),load(c['priority_worklist_path']),o)
    files={'catalog/CURRENT.json':result['current'],VIEW:result['view'],QUEUE:result['queue'],PLAN:result['plan']}
    rules=load('policies/selection-decision-v17.json')
    rules['objective']='Insure against loss of public distribution by preserving valuable learned outcomes and their dependencies. Early-restriction scenarios order preparation but are not the sole eligibility test; daily-use optimization is separate.'
    rules['archival_insurance_policy_path']=POLICY
    rules['conditional_minimum_quality']='Credible evidence of a distinct learned mechanism or research value, with negative evidence recorded; neither imminent-ban proof nor overall benchmark superiority is required for conditional archival selection. Acquisition and existing oversized runtime gates remain separate.'
    files['policies/selection-decision-v17.json']=rules
    p='scripts/audit_selection_decisions.py'
    texts={p:replace_once((ROOT/p).read_text(), '("v19-20261106", "v20-20261106", "v21-20261106")',
                          '("v19-20261106", "v20-20261106", "v21-20261106", "v22-20261106")')}
    p='tests/test_catalog_v19.py'
    texts[p]=replace_once((ROOT/p).read_text(),'"v21-20261106":(159,112)','"v21-20261106":(159,112),"v22-20261106":(163,116)')
    intro='\n## 現行v22：学習成果を失わないための保険\n\n[CURRENT](catalog/CURRENT.json)は163資産・有効116件。規制予測は先に確保する順番であり、保全対象をそこだけに限定しない。[保険方針](policies/archival-insurance.json)・[116件の段階別準備表](catalog/preparation/2026-11-06-insurance-bundles-v22.json)・[採用理由](docs/strategy/27-insurance-first-selection-v22.md)。Drama3公開元原本、DavidAU独自後学習、GroundGUI定位、Consistency LoRA差分を4件conditionalとして追加。全159旧レコード、4TB枠、200GB空き、150B超の量子化同等RAM条件を維持。追加計画枠156GBは実測容量ではない。取得承認0。以下v21以前の件数は履歴。\n'
    for p,title in [('README.md','# Local Model Portfolio\n'),('AGENTS.md','# エージェント作業規約\n')]:
        texts[p]=replace_once((ROOT/p).read_text(),title,title+intro)
    p='policies/selection.md'; text=(ROOT/p).read_text()
    text=replace_once(text,'# 選定基準\n','# 選定基準\n\n## 最上位目的：学習成果を失わないための保険\n\n公開配布経路全般が失われるストレスケースに備え、再構築しにくい重み・データ・再現部品を保全する。実際に全面禁止が決まったとは主張しない。**何を残すかは学習成果の価値、何から先に確保するかは先行制限シナリオと現在の配布状態で決める。** 削除予告の不在、最新ベンチの順位、日常利用の速度だけで独自成果を候補から落とさない。形式だけの重複は増やさず、基盤とadapter、codec、tokenizer、設定、利用条件、runtimeを一組で残す。[機械可読方針](archival-insurance.json)。既存の4TB・150B超量子化RAM・正規アクセス・取得承認条件は変えない。\n')
    text=text.replace('## 最上位原則：モデルもデータも消失・制限リスク順に選ぶ','## 確保の順序：先行制限シナリオから段階的に広げる')
    text=text.replace('**v5保存優先度（強い順）**','**段階的な準備順（v5のS波は仮説として使用）**')
    texts[p]=text
    prior={}
    for x in o['additions']:
        refs=[]
        for f in (ROOT/'catalog/research').glob('*.json'):
            raw=f.read_text(encoding='utf-8')
            if x['repo_id'] in raw or x.get('prior_research_identity',x['repo_id']) in raw:
                refs.append(str(f.relative_to(ROOT)))
        prior[x['repo_id']]=refs
    summary={'revision':REV,'tracked':163,'active':116,'new_conditional':4,
      'new_reservation_bytes':result['view']['budget']['new_active_reservation_cap_bytes'],
      'approved_downloads':0,'final_total_bytes':None,'prior_research_matches':prior,
      'full_suite_verified':False,'verification_scope':'metadata transformation; runtime and physical storage unmeasured'}
    files['catalog/preparation/2026-11-06-v22-integration-check.json']=summary
    if args.apply:
        for path,obj in files.items():
            dest=ROOT/path; dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for path,text in texts.items(): (ROOT/path).write_text(text,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
