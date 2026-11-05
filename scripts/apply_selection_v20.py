#!/usr/bin/env python3
"""Deterministic v19 -> v20 metadata-only transition. Python >=3.10, stdlib.

No network, model import, payload download, authorization or filesystem-vault access.
Only the repository files listed by --apply are changed; source snapshots are kept.
"""
from __future__ import annotations
import argparse
import copy
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REV = 'v20-20261106'
OLD = 'v19-20261106'
OVERLAY = 'catalog/revisions/v20-2026-11-06.json'
VIEW = 'catalog/effective-portfolio-2026-11-06-v20.json'
QUEUE = 'queues/proposed-v20-2026-11-06.json'
REPORT = 'docs/strategy/24-selected-cascade-4tb-v20.md'
ACTIVE = {'select', 'conditional'}

def key(row):
    return row['asset_kind'].lower(), row['repo_id'].lower()

def prepare(current, view, queue, limits, rules, overlay):
    current, view, queue, limits, rules, overlay = copy.deepcopy((current, view, queue, limits, rules, overlay))
    if current.get('revision_id') != OLD or view.get('revision_id') != OLD:
        raise ValueError('unexpected baseline: v19 required')
    items = view.get('items', [])
    if len(items) != 150 or sum(x.get('portfolio_decision') in ACTIVE for x in items) != 105:
        raise ValueError('baseline must contain 150 identities / 105 active')
    ids = {key(x) for x in items}
    if len(ids) != len(items):
        raise ValueError('duplicate baseline identity')
    if any(x.get('download_approved') is not False for x in items):
        raise ValueError('baseline approval changed: review before applying')
    if queue.get('approved') is not False or queue.get('download_enabled') is not False:
        raise ValueError('baseline queue must remain non-executable')
    old_active = {key(x) for x in items if x.get('portfolio_decision') in ACTIVE}
    if {key(x) for x in queue.get('candidates', [])} != old_active or len(queue['candidates']) != 105:
        raise ValueError('baseline queue mismatch')
    if overlay.get('revision_id') != REV or overlay.get('previous_revision_id') != OLD:
        raise ValueError('overlay revision mismatch')
    if overlay.get('archive_target_bytes') != 4_000_000_000_000 or overlay.get('minimum_free_bytes') != 200_000_000_000:
        raise ValueError('incorrect budget or changed free-space floor')
    additions = overlay.get('additions', [])
    if len(additions) != 4 or sum(x.get('portfolio_decision') in ACTIVE for x in additions) != 3:
        raise ValueError('expected three conditional additions plus one deferred format')
    reserve = 0
    rank = max(x.get('forecast_priority', {}).get('rank', 0) for x in items)
    for offset, item in enumerate(additions, 1):
        if key(item) in ids:
            raise ValueError('duplicate addition: '+item['repo_id'])
        ids.add(key(item))
        for field in ('url', 'reason_selected', 'quality_negative', 'evidence_date'):
            if not item.get(field):
                raise ValueError('missing evidence field '+field)
        if item.get('download_approved') is not False:
            raise ValueError('new entry cannot authorize acquisition')
        g = item.get('parameter_gate', {})
        if item['asset_kind'] == 'model':
            total = g.get('total_parameters')
            if isinstance(total, bool) or not isinstance(total, int) or not 0 < total < 150_000_000_000:
                raise ValueError('new model total unknown or >=150B')
            if g.get('status') != 'PASS_TOTAL_PARAMS_LT_150B':
                raise ValueError('inconsistent model size gate')
        elif item['asset_kind'] != 'dataset' or g.get('status') != 'NOT_APPLICABLE_TO_DATASET':
            raise ValueError('invalid asset kind/dataset gate')
        if item.get('portfolio_decision') in ACTIVE:
            cap = item.get('selection_budget_cap_bytes')
            if isinstance(cap, bool) or not isinstance(cap, int) or cap <= 0:
                raise ValueError('active additions require explicit planning cap')
            reserve += cap
        item.setdefault('forecast_priority', {})['rank'] = rank + offset
        item['forecast_priority']['scenario_status'] = 'HYPOTHESIS_NOT_A_RELEASE_BAN'
        items.append(item)
        if item.get('portfolio_decision') in ACTIVE:
            queue['candidates'].append({'asset_kind':item['asset_kind'], 'repo_id':item['repo_id'],
                'selection':item['portfolio_decision'], 'parameter_gate':g['status'],
                'not_authorized':True, 'download_approved':False,
                'selection_budget_cap_bytes':item['selection_budget_cap_bytes'],
                'requested_subset_paths':item.get('requested_subset_paths'),
                'full_dependency_manifest_complete':False, 'approved_lock':False})
    if reserve > overlay.get('max_new_selection_budget_bytes', 0):
        raise ValueError('new planning reservations exceed explicit cap')
    active = [x for x in items if x.get('portfolio_decision') in ACTIVE]
    if len(items) != 154 or len(active) != 108 or {key(x) for x in active} != {key(x) for x in queue['candidates']}:
        raise ValueError('result cardinality mismatch')
    if any(x.get('download_approved') is not False or x.get('not_authorized') is not True for x in queue['candidates']):
        raise ValueError('queue inadvertently authorized')
    counts = {'tracked':len(items), 'active':len(active),
              'by_tier':dict(Counter(x.get('risk_tier') for x in items)),
              'by_decision':dict(Counter(x['portfolio_decision'] for x in items)),
              'parameter_gate':dict(Counter(x.get('parameter_gate',{}).get('status') for x in items if x['asset_kind']=='model'))}
    counts['by_forecast_wave'] = {w:{'active':sum(x.get('portfolio_decision') in ACTIVE and x.get('forecast_priority',{}).get('wave')==w for x in items),
                                   'inactive':sum(x.get('portfolio_decision') not in ACTIVE and x.get('forecast_priority',{}).get('wave')==w for x in items)} for w in ('S1','S2','S3')}
    source_bytes = lambda x:x.get('resource_screen',{}).get('source_all_repo_bytes')
    counts['resource_screen'] = {'tracked':len(items), 'source_repo_bytes_unknown':sum(source_bytes(x) is None for x in items),
                                 'active_source_repo_bytes_unknown':sum(source_bytes(x) is None for x in active),
                                 'active_ge_100GB_repo_assets':sum(source_bytes(x) is not None and source_bytes(x)>=100_000_000_000 for x in active)}
    if view.get('budget'):
        view['historical_budget_v19'] = copy.deepcopy(view['budget'])
    view['budget'] = {'archive_limit_bytes':4_000_000_000_000, 'minimum_free_bytes':200_000_000_000,
        'new_active_reservation_cap_bytes':reserve, 'reservation_is_policy_cap_not_observed_bytes':True,
        'final_selected_total_bytes':None, 'final_headroom_bytes':None,
        'unknown_final_selected_asset_count':sum(x.get('selected_file_bytes') is None for x in active),
        'physical_capacity_verified':False, 'budget_status':'UNFINALIZED_DO_NOT_TREAT_MISSING_BYTES_AS_ZERO',
        'warning':'4TB is an authorized planning ceiling, not measured disk capacity or evidence the complete portfolio fits. SFT selection is bounded to two named files, not all 593GB.'}
    view['counts'].update(counts)
    view.update({'revision_id':REV,'generated_date':'2026-11-06','items':items,'read_only_derived':True,
                 'v20_note':'3 adopted conditional selections and 1 deferred duplicate format; all original 150 records preserved; no downloads.'})
    current['expected'].update(counts)
    current['expected']['historical_budget_scenario_v19'] = current['expected'].pop('budget_scenario', {})
    current['expected'].update({'archive_limit_bytes':4_000_000_000_000,'provisional_headroom_bytes':None,
                               'provisional_active_repo_bytes_plus_fineweb_sample':None,'budget_scenario':copy.deepcopy(view['budget'])})
    current['revision_id']=REV
    current['generated_date']='2026-11-06'
    current['materialized_catalog_path']=VIEW
    current['priority_worklist_path']=QUEUE
    current['ordered_overlays'].append(OVERLAY)
    current['latest_adopted_selection_path']=OVERLAY
    current['latest_selection_report_path']=REPORT
    note=' v20 adopts Cascade2 original, full RL dataset, and proof+agentic SWE SFT subset as 3 conditional selections; Orca FP8 remains deferred duplicate. Four decimal TB budget; physical space and final locks unresolved. New models must be <150B; no over-baseline promotions.'
    current['notes']=current.get('notes','')+note
    current['application_rule']=current.get('application_rule','')+note
    current['statuses']={'draft':True,'download_approved':False,'selected_file_bytes_final':False}
    queue.update({'source_revision':REV,'generated_at':'2026-11-06','approved':False,'download_enabled':False,
                  'description':'v20: 108 active selections; metadata-only, no user-approved payloads; 4TB ceiling.'})
    limits['archive_target_bytes']=4_000_000_000_000
    allocation=limits.setdefault('storage_allocation_policy',{})
    allocation.update({'confirmed_on':'2026-11-06','permitted_archive_budget_bytes':4_000_000_000_000,
        'latest_user_statement':'リポに選定して入れて行ってください4tまでいれることができます',
        'notes':'User authorized a 4,000,000,000,000-byte selection ceiling. This is not a disk measurement. Retain the 200GB free-space floor; if usable total is exactly 4TB, payload must be below 3.8TB before existing data/staging.',
        'requires_actual_formatted_volume_capacity_and_free_space_measurement':True,'free_space_floor_still_applies':True})
    rules.setdefault('hard_boundaries',{})['archive_target_bytes']=4_000_000_000_000
    rules['archive_budget_last_user_authorization']='2026-11-06'
    return dict(current=current,view=view,queue=queue,limits=limits,rules=rules)

def safe_path(root, relative):
    p=(root/relative).resolve()
    if not p.is_relative_to(root.resolve()): raise ValueError('path outside repository')
    return p

def read(root, relative):
    return json.loads(safe_path(root,relative).read_text(encoding='utf-8'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true',help='write deterministic repository metadata only')
    args=parser.parse_args()
    current=read(ROOT,'catalog/CURRENT.json')
    if current.get('revision_id')==REV:
        print('Already at v20; no writes.'); return
    approved_before=(ROOT/'queues/approved.json').read_bytes()
    if read(ROOT,'queues/approved.json').get('entries') != []:
        raise ValueError('approved queue changed; refuse automation')
    data=prepare(current,read(ROOT,current['materialized_catalog_path']),read(ROOT,current['priority_worklist_path']),
                 read(ROOT,'policies/limits.json'),read(ROOT,'policies/selection-decision-v17.json'),read(ROOT,OVERLAY))
    outputs={VIEW:json.dumps(data['view'],ensure_ascii=False,indent=2)+'\n',
             QUEUE:json.dumps(data['queue'],ensure_ascii=False,indent=2)+'\n',
             'catalog/CURRENT.json':json.dumps(data['current'],ensure_ascii=False,indent=2)+'\n',
             'policies/limits.json':json.dumps(data['limits'],ensure_ascii=False,indent=2)+'\n',
             'policies/selection-decision-v17.json':json.dumps(data['rules'],ensure_ascii=False,indent=2)+'\n'}
    audit_path='scripts/audit_selection_decisions.py'
    audit=(ROOT/audit_path).read_text(encoding='utf-8')
    old='if current.get("revision_id")!="v19-20261106": return ["unexpected CURRENT revision"]'
    new='if current.get("revision_id") not in ("v19-20261106", "v20-20261106"): return ["unexpected CURRENT revision"]'
    if audit.count(old)!=1: raise ValueError('audit source drift')
    outputs[audit_path]=audit.replace(old,new).replace('PASS v19 selection, historic v17 evidence','PASS current selection, historic v17 evidence')
    readme=(ROOT/'README.md').read_text(encoding='utf-8')
    headline='## 現行選定 v19'
    if readme.count(headline)!=1: raise ValueError('README source drift')
    intro='## 現行選定 v20（2026-11-06：4TB枠・Cascade2を正式選定）\n\n- [CURRENT](catalog/CURRENT.json)・[154資産の全件ビュー]('+VIEW+')・[108件の非実行キュー]('+QUEUE+')。\n- Cascade2原本、RLデータ、SFTの数学証明＋agentic SWE部分を3件conditionalとして正式追加。Orca27B FP8は重複のためdeferred。\n- 保存予算は十進4TB。追加3件に計165GBの計画上限を割当。約134.5GBという表示容量の合算は概算であり最終lockではない。SFT全593GBは選ばない。\n- [採用理由・負の根拠・容量管理]('+REPORT+')。実空き・全依存・権利・固定SHA未確定、ダウンロード承認0。過去節の3.8TBは旧方針で、現在の数値はpolicies/limits.jsonが正本。\n\n'
    outputs['README.md']=readme.replace(headline,intro+'## 旧版選定 v19',1)
    agents=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
    new_intro='\n## v20：このブランチの現在値\n\nCURRENTはv20・154資産／有効108件。4,000,000,000,000 byteは選定上限、200GB空き条件は維持。追加はCascade2原本、RLデータ、SFTのmath/math_proof.jsonlとswe/swe_agentic.jsonlのみ。Orca FP8はdeferred。全150旧レコードと承認キューは維持し、今回150B以上を新規採用しない。以下のv19件数・3.8TB記述は履歴。本体取得・クラウド課金・任意モデル実行は禁止のまま。\n'
    outputs['AGENTS.md']=agents.replace('# エージェント作業規約','# エージェント作業規約\n'+new_intro,1)
    selection=(ROOT/'policies/selection.md').read_text(encoding='utf-8')
    selection=selection.replace('4TBのうち3.8TBを有用な資産に割り当てる。','2026-11-06のユーザー指定により、選定予算は十進4TBとする。実測空き200GB・既存ファイル・stagingは別に確認する。')
    outputs['policies/selection.md']=selection.replace('3.8TB','4TB')
    workflow=(ROOT/'docs/workflow.md').read_text(encoding='utf-8')
    outputs['docs/workflow.md']=workflow.replace('十進3,800,000,000,000バイト','十進4,000,000,000,000バイト').replace('**3.8TBは選定の最大利用許可','**4TBは選定の最大利用許可')
    summary={'revision':REV,'tracked':154,'active':108,'archive_target_bytes':4_000_000_000_000,
             'approved_downloads':0,'changed_paths':sorted(outputs),'final_total_bytes':None,
             'scope':'static catalog transformation; no model/hardware tests'}
    outputs['catalog/preparation/2026-11-06-v20-integration-check.json']=json.dumps(summary,ensure_ascii=False,indent=2)+'\n'
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if args.apply:
        for path,text in outputs.items():
            p=safe_path(ROOT,path); p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(text,encoding='utf-8')
        if (ROOT/'queues/approved.json').read_bytes()!=approved_before:
            raise ValueError('approved queue unexpectedly changed')

if __name__=='__main__': main()
