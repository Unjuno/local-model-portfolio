#!/usr/bin/env python3
"""New trained decision model and MOSS codec closure v26 -> v27 catalog transition. Python >=3.10, stdlib only.
No network, vault access, model execution, payload transfer or approvals.
"""
from __future__ import annotations
import argparse
import copy
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD='v26-20261106'; REV='v27-20261107'
OVERLAY='catalog/revisions/v27-2026-11-07.json'
VIEW='catalog/effective-portfolio-2026-11-07-v27.json'
QUEUE='queues/proposed-v27-2026-11-07.json'
PLAN='catalog/preparation/2026-11-07-insurance-bundles-v27.json'
POLICY='policies/archival-insurance.json'
REPORT='docs/strategy/37-kanana-moss-archive-v27.md'
ACTIVE={'select','conditional'}
LOW='PASS_TOTAL_PARAMS_LT_150B'; UNKNOWN='UNVERIFIED_BLOCK_FINAL_LOCK'
CAP=150_000_000_000

def key(x): return x['asset_kind'].lower(),x['repo_id'].lower()
def integer(x): return isinstance(x,int) and not isinstance(x,bool)

def prepare(current,view,queue,overlay):
    c,v,q,o=copy.deepcopy((current,view,queue,overlay))
    if (c.get('revision_id'),v.get('revision_id'),q.get('source_revision'))!=(OLD,OLD,OLD):
        raise ValueError('expected v26 baseline')
    items=v.get('items',[]); ids={key(x) for x in items}
    if len(items)!=172 or len(ids)!=172 or sum(x.get('portfolio_decision') in ACTIVE for x in items)!=125:
        raise ValueError('baseline must have 172 identities and 125 active')
    if any(x.get('download_approved') is not False for x in items):
        raise ValueError('baseline download authorization changed')
    if q.get('approved') is not False or q.get('download_enabled') is not False:
        raise ValueError('baseline queue executable')
    if len(q.get('candidates',[]))!=125 or {key(x) for x in q['candidates']}!={key(x) for x in items if x['portfolio_decision'] in ACTIVE}:
        raise ValueError('baseline queue mismatch')
    if any(x.get('not_authorized') is not True or x.get('download_approved') is not False for x in q['candidates']):
        raise ValueError('baseline queue entry authorized')
    if (o.get('revision_id'),o.get('previous_revision_id'))!=(REV,OLD):
        raise ValueError('overlay revision mismatch')
    if (o.get('archive_target_bytes'),o.get('minimum_free_bytes'))!=(4_000_000_000_000,200_000_000_000):
        raise ValueError('resource policy changed')
    additions=o.get('additions',[])
    if len(additions)!=1 or any(x.get('portfolio_decision')!='conditional' for x in additions):
        raise ValueError('expected one trained decision outcome')
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
        if x.get('gated_approval_required') is True or x.get('research_only_gated_access') is True:
            if x.get('observed_access','').lower().find('gated')<0:
                raise ValueError('gated restriction not justified by source')
            entry.update(research_only=True,can_enter_approved_queue=False,
                         personal_gated_access_verification_required=True,
                         license_approval_required=True,gated_approval_required=True)
        if x.get('license_metadata','').startswith('other:') and x.get('license_text_reviewed') is False:
            entry.update(research_only=True,can_enter_approved_queue=False,
                personal_license_review_required=True,source_license_name=x['license_metadata'])
        q['candidates'].append(entry); items.append(x)
    if not integer(o.get('max_new_selection_budget_bytes')) or reserve>o['max_new_selection_budget_bytes']:
        raise ValueError('new planning caps exceed allocation')
    active=[x for x in items if x['portfolio_decision'] in ACTIVE]
    if len(items)!=173 or len(active)!=126: raise ValueError('result counts inconsistent')
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
    v['historical_budget_v26']=copy.deepcopy(v.get('budget',{}))
    budget={'archive_limit_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
      'new_active_reservation_cap_bytes':reserve,'reservation_is_policy_cap_not_observed_bytes':True,
      'final_selected_total_bytes':None,'final_headroom_bytes':None,'physical_capacity_verified':False,
      'unknown_final_selected_asset_count':sum(x.get('selected_file_bytes') is None for x in active),
      'shared_base_savings_verified':False,'budget_status':'UNFINALIZED_DO_NOT_TREAT_MISSING_BYTES_AS_ZERO'}
    v.update(revision_id=REV,generated_date='2026-11-06',items=items,budget=budget,read_only_derived=True)
    v.setdefault('counts',{}).update(counts); c['expected'].update(counts)
    c['expected']['historical_budget_scenario_v26']=c['expected'].pop('budget_scenario',{})
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
    if isinstance(c.get('capacity_audit'),dict):
        c['capacity_audit']['status']='V26_125_SOURCE_SCOPES_VERIFIED_V27_1_KANANA_UNCENSUSED_MOSS_CODEC_KNOWN'
        c['capacity_audit']['source_revision']='v26-20261106'
        c['capacity_audit']['latest_revision_scope_coverage']=125
        c['capacity_audit']['v27_new_assets_unmeasured_count']=1
        c['capacity_audit']['moss_v1_external_codec_source_evidence']='catalog/research/2026-11-07-r30/codec-capacity.json'
    v['budget']['prior_verified_v26_known_logical_dedup_bytes']=3_403_245_899_240
    v['budget']['new_v27_kanana_source_repo_bytes_not_selected_bytes']=7_341_213_499
    v['budget']['new_v27_selected_scope_preview_not_final_bytes']=7_341_102_234
    v['budget']['moss_v1_required_codec_selected_external_dependency_bytes']=7_098_711_111
    v['budget']['known_v26_plus_moss_source_only_logical_bytes']=3_410_344_610_351
    v['budget']['scenario_is_not_final_total_or_available_disk']=True
    note=' v27 adds 3.665B Kanana non-generative multimodal decision learned outcome conditional research-only. Contract separate permissions for API resale and redistribution. MOSS-TTS v1.5 original audio codec v1 7.099GB accounted as mandatory learned dependency, not v2. Ripple-65B base/instruct HOLD. Old 125 source scopes are historical; v27 recomputes 126. 4TB/200GB, >150B RAM and no downloads unchanged.'
    c['notes']=c.get('notes','')+note; c['application_rule']=c.get('application_rule','')+note
    c['statuses']={'draft':True,'download_approved':False,'selected_file_bytes_final':False}
    byid={key(x):x for x in items}
    stage=lambda x:{'S1':1,'S2':2,'S3':3}.get(x.get('forecast_priority',{}).get('wave'),3)
    q['candidates'].sort(key=lambda x:(stage(byid[key(x)]),byid[key(x)].get('forecast_priority',{}).get('rank',0)))
    q.update(source_revision=REV,generated_at='2026-11-06',approved=False,download_enabled=False,
      description='126 research archival selections including Kakao Kanana typed decision, contract-license blocked from approval; no weight access authorized.')
    work=[]
    for x in sorted(active,key=lambda x:(stage(x),x.get('forecast_priority',{}).get('rank',0))):
        blocked=x.get('parameter_gate',{}).get('status')==UNKNOWN
        work.append({'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'stage':stage(x),
          'is_new_v27':key(x) in {key(a) for a in additions},
          'next_action':'PUBLIC_METADATA_PARAMETER_CENSUS_ONLY' if blocked else 'PERSONAL_GATED_PERMISSION_AND_LICENSE_REVIEW_ONLY' if x.get('gated_approval_required') else 'KANANA_CONTRACT_LICENSE_AND_OFFLINE_RUNTIME_REVIEW_ONLY' if x.get('repo_id')=='kakaocorp/kanana-2-v-decide-3b-2611' else 'RIGHTS_REVISION_AND_DEPENDENCY_INVENTORY',
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
        print('Already v27; no changes'); return
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
    texts={p:replace_once((ROOT/p).read_text(), '("v19-20261106", "v20-20261106", "v21-20261106", "v22-20261106", "v23-20261106", "v24-20261106", "v25-20261106", "v26-20261106")',
                          '("v19-20261106", "v20-20261106", "v21-20261106", "v22-20261106", "v23-20261106", "v24-20261106", "v25-20261106", "v26-20261106", "v27-20261107")')}
    p='tests/test_catalog_v19.py'
    texts[p]=replace_once((ROOT/p).read_text(),'"v26-20261106":(172,125)','"v26-20261106":(172,125),"v27-20261107":(173,126)')
    intro="\n## 現行v27：Kakao Kanana非生成型判断モデルとMOSS必須音声Codec\n\n[CURRENT](catalog/CURRENT.json)は173資産・有効126件。Kanana 3.665Bの型付き確率判断（choice/noul/score）をBF16原本一式として条件付き研究選定。Kanana Open LicenseのNOTICE/利用条件・別途商用API/SI/端末組込権利が未確認で取得承認不可。MOSS-TTS v1.5の外部必須v1音声Codecを容量に計上、v2は混同しない。Ricursive Ripple 65Bの事前学習原本・後学習版は研究HOLD。4TB上限・最低空き200GB・150B以上量子化同等RAM・承認0を維持。[評価](docs/strategy/37-kanana-moss-archive-v27.md)・[容量](catalog/capacity/2026-11-07/v27/capacity-summary.json)。以下は履歴。\n"
    for p,title in [('README.md','# Local Model Portfolio\n'),('AGENTS.md','# エージェント作業規約\n')]:
        texts[p]=replace_once((ROOT/p).read_text(),title,title+intro)
    # Archive-insurance policy is already current in v22; do not duplicate the policy heading.
    prior={}
    for x in o['additions']:
        refs=[]
        for f in (ROOT/'catalog/research').glob('*.json'):
            raw=f.read_text(encoding='utf-8')
            if x['repo_id'] in raw or x.get('prior_research_identity',x['repo_id']) in raw:
                refs.append(str(f.relative_to(ROOT)))
        prior[x['repo_id']]=refs
    summary={'revision':REV,'tracked':173,'active':126,'new_conditional':1,
      'new_reservation_bytes':result['view']['budget']['new_active_reservation_cap_bytes'],
      'approved_downloads':0,'final_total_bytes':None,'prior_research_matches':prior,
      'full_suite_verified':False,'verification_scope':'metadata transformation; runtime and physical storage unmeasured'}
    files['catalog/preparation/2026-11-07-v27-integration-check.json']=summary
    if args.apply:
        for path,obj in files.items():
            dest=ROOT/path; dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for path,text in texts.items(): (ROOT/path).write_text(text,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
