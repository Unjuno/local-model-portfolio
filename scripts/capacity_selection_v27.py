#!/usr/bin/env python3
"""v27 source-only exact file-scope census: Kanana selected primary + MOSS v1 codec.

Never downloads payload, executes remote code, claims legal access or measures owner disk.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('catalog/capacity/2026-11-06/v26')
OUT=Path('catalog/capacity/2026-11-07/v27')
RESEARCH=Path('catalog/research/2026-11-07-r30')
KAKAO='kakaocorp/kanana-2-v-decide-3b-2611'
MOSS='OpenMOSS-Team/MOSS-Audio-Tokenizer'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,x):
    path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def union_entries(items,deps):
    out=[(r['repo_id']+'@'+r['source_revision'],f) for r in items for f in r['files']]
    out.extend((d['repo_id']+'@'+d['revision'],f) for d in deps for f in d['files'])
    return out
def checked_file_selection(src,research_row):
    assert src['repo_id']==KAKAO and src['tree_complete'] is True
    assert src['pinned_revision']==research_row['pinned_source_sha']=='1489062def4145ae3a0a9261fbac4f4d88a8c6d1'
    assert src['source_scope_bytes']==research_row['source_repo_bytes']==7_341_213_499
    assert src['gated'] is False and src['license_metadata']=='other'
    assert src['payload_bytes_downloaded']==0 and src['download_authorized'] is False
    all_files={x['path']:x for x in src['files']}
    selected_paths=research_row['candidate_original_selected_paths']
    assert len(set(selected_paths))==len(selected_paths)==17
    assert set(selected_paths).issubset(all_files)
    selected=[all_files[path] for path in selected_paths]
    assert cap.sum_bytes(selected)==research_row['candidate_original_selected_files_bytes']==7_341_102_234
    assert len([x for x in selected if x['path'].endswith('.safetensors')])==1
    assert next(x['bytes'] for x in selected if x['path']=='model.safetensors')==research_row['candidate_selected_original_model_weight_bytes']==7_330_945_212
    assert {'LICENSE','config.json','tokenizer.json','modeling_kanana_v_decide.py','processing_kanana_v_decide.py','decision_kanana_v_decide.py'}.issubset(set(selected_paths))
    assert all('/' not in p for p in selected_paths)
    return selected
def build(old,view,overlay,research,src,moss):
    assert old['source_revision']=='v26-20261106'
    assert old['exact_primary_file_scope_count']==125 and old['unresolved_primary_scope_count']==0
    assert len(old['items'])==125 and old['known_scope_content_union_bytes']==3_403_245_899_240
    assert view['revision_id']=='v27-20261107' and len(view['items'])==173
    assert len([x for x in view['items'] if x['portfolio_decision'] in ('select','conditional')])==126
    assert overlay['revision_id']=='v27-20261107' and len(overlay['additions'])==1
    added=overlay['additions'][0];assert added['repo_id']==KAKAO and added['download_approved'] is False
    assert added['selected_file_bytes'] is None and added['fully_pinned_revision_sha'] is None
    assert added['parameter_gate']['status']=='PASS_TOTAL_PARAMS_LT_150B'
    assert added['parameter_gate']['total_parameters']==3_665_430_640
    assert src['parameter_metadata']['total']==3_665_430_640
    assert all(r['repo_id']!=KAKAO for r in old['items'])
    research_row=next(x for x in research['public_source_candidates'] if x['repo_id']==KAKAO)
    selected=checked_file_selection(src,research_row)
    docs={d['path']:d for d in src.get('documentation',[])}
    assert 'config.json' in docs and isinstance(docs['config.json'].get('json'),dict)
    row={'asset_kind':'model','repo_id':KAKAO,'portfolio_decision':'conditional',
      'scope_status':'EXACT_PUBLISHER_SOURCE_FILES_LICENSE_AND_OFFLINE_RUNTIME_BLOCK_ACQUISITION',
      'capacity_evidence_kind':'fixed HF API file bytes, some payload hashes masked; local file hashes unmeasured',
      'source_revision':src['pinned_revision'],'source_observed_at_utc':src['observed_at_utc'],
      'source_scope_bytes':src['source_scope_bytes'],'primary_file_bytes':cap.sum_bytes(selected),
      'package_bytes':cap.sum_bytes(selected),
      'files':selected,'excluded_files':[{'path':x['path'],'bytes':x['bytes'],'reason':'demo/example metadata not needed for core offline model'} for x in src['files'] if x['path'] not in research_row['candidate_original_selected_paths']],
      'profile':{'original_bf16':True,'external_unlicensed_weights_not_automatically_downloaded':True,
                 'not_another_quantization':True},
      'source_parameter_gate':added['parameter_gate'],
      'gated':src['gated'],'license_metadata':src['license_metadata'],
      'personal_access_verified':False,'license_text_and_all_components_cleared':False,
      'runtime':{'measured_peak_ram_bytes':None,'backend_commit':None,'hardware':None,'context':None,
         'batch':None,'zero_point':None,'ABI':None,'clock':None},
      'shared_dependencies':[],
      'open_dependencies':['Kanana Open License responsible-use/NOTICE and separate commercial API/SI/on-device rights not personally cleared',
        'Native trust_remote_code Python models and System One API ABI/locked requirements, no runnable offline restore test',
        'Independent cross-domain decision quality and probability calibration not tested'],
      'software_environment_bytes':None,'offline_restore_tested':False,
      'download_authorized':False,
      'masked_or_unknown_payload_identity_files':sum(f.get('identity_kind') in ('unverifiable_payload_hash','unverified') for f in selected)}
    moss_meta=moss['mandatory_moss_codec_capacity_accounting']
    assert moss_meta['required_moss_audio_codec_new_selected_primary_bytes']==7_098_711_111
    assert moss_meta['source_only_expanded_known_hash_aware_bytes']==3_410_344_610_351
    assert all(x['repo_id']!=MOSS for x in old['dependencies'])
    codecfiles=moss_meta['codec_selected_files']
    assert len(codecfiles)==8 and len([f for f in codecfiles if f['path'].endswith('.safetensors')])==2
    assert cap.sum_bytes(codecfiles)==moss_meta['required_moss_audio_codec_new_selected_primary_bytes']
    assert all(f.get('sha256') for f in codecfiles if f['path'].endswith('.safetensors'))
    dep={'parent':'OpenMOSS-Team/MOSS-TTS-v1.5','repo_id':MOSS,
         'revision':'3cd226ba2947efa357ef453bcad111b6eafba782',
         'files':codecfiles,'bytes':cap.sum_bytes(codecfiles),
         'role':'Native 24kHz audio tokenizer for MOSS-TTS-v1.5 processor default; do not confuse with stereo v2',
         'shared_model_asset':False,
         'personal_license_reconciliation_complete':False,
         'native_runtime_compatibility_tested':False,
         'user_disk_hash_verified':False}
    items=list(old['items'])+[row]
    deps=list(old['dependencies'])+[dep]
    entries=union_entries(items,deps)
    old_entries=union_entries(old['items'],old['dependencies'])
    assert cap.union_bytes(old_entries)==old['known_scope_content_union_bytes']
    codec_only_union=cap.union_bytes(old_entries+[(MOSS+'@'+dep['revision'],f) for f in codecfiles])
    assert codec_only_union==moss_meta['source_only_expanded_known_hash_aware_bytes']
    all_union=cap.union_bytes(entries)
    assert all_union>=moss_meta['source_only_expanded_known_hash_aware_bytes']
    assert all_union<=moss_meta['source_only_expanded_known_hash_aware_bytes']+row['primary_file_bytes']
    largest=max(f['bytes'] for _,f in entries)
    all_open=[{'repo_id':r['repo_id'],'issues':r['open_dependencies']} for r in items if r['open_dependencies']]
    assert len(all_open)==35 and any(x['repo_id']=='OpenMOSS-Team/MOSS-TTS-v1.5' for x in all_open)
    summary={'schema_version':1,'source_revision':'v27-20261107','tracked':173,'active':126,
       'previous_source_revision':'v26-20261106',
       'old_exact_primary_scopes':125,'new_exact_primary_scopes':1,
       'exact_primary_file_scope_count':126,'unresolved_primary_scope_count':0,
       'known_primary_file_bytes_sum':sum(r['primary_file_bytes'] for r in items),
       'known_scope_content_union_bytes':all_union,
       'known_parent_package_bytes_with_repeated_references':sum(r['package_bytes'] for r in items),
       'known_dependency_additions_bytes':sum(x['bytes'] for x in deps),
       'new_moss_external_dependency_selected_bytes':dep['bytes'],
       'new_moss_external_dependency_hash_aware_logical_increment_bytes':moss_meta['required_moss_audio_codec_hash_aware_logical_new_bytes'],
       'moss_external_codec_not_newly_selected_asset':True,
       'new_kanana_selected_primary_bytes':row['primary_file_bytes'],
       'new_kanana_original_weight_bytes':research_row['candidate_selected_original_model_weight_bytes'],
       'both_ripple_65B_variants_not_adopted':True,
       'complete_learned_dependency_total_bytes':cap.complete_total(items),
       'complete_offline_archive_bytes':None,'complete_deduplicated_archive_bytes':None,
       'unknown_primary_scopes':[],
       'assets_with_open_dependency_issues':all_open,
       'all_runtime_environment_archives_unmeasured':True,
       'planning_cap_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
       'provisional_known_scope_budget_difference_bytes':4_000_000_000_000-all_union,
       'difference_is_not_available_headroom':True,
       'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,'local_duplicate_bytes':None,
       'actual_remaining_archive_budget_bytes':None,'actual_acquisition_peak_bytes':None,
       'largest_selected_file_bytes':largest,
       'acquisition_scenarios_known_scope_only':{
          'direct_final_volume_atomic_rename_no_retained_cache_payload_bytes':all_union,
          'one_extra_largest_file_copy_payload_upper_scenario_bytes':all_union+largest,
          'retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes':all_union*2+largest,
          'assumptions':'Empty fresh filesystem, no repeated retries, source-only known selected bytes, dependent code and owner disk unknown'},
       'model_payload_bytes_downloaded':0,'download_authorized':False,'executable':False,
       'profile_evidence':['catalog/capacity/2026-11-06/v26/selected-file-capacity.json',
         'catalog/research/2026-11-07-r30/research.json',
         'catalog/revisions/v27-2026-11-07.json']
    }
    assert all_union<4_000_000_000_000 and summary['complete_learned_dependency_total_bytes'] is None
    return dict(summary,items=items,dependencies=deps)
def main():
    c=load('catalog/CURRENT.json')
    assert c['revision_id']=='v27-20261107' and c['expected']['tracked']==173 and c['expected']['active']==126
    q=load(c['priority_worklist_path'])
    assert not q['download_enabled'] and not q['approved'] and not load('queues/approved.json')['entries']
    old=load(BASE/'selected-file-capacity.json')
    research=load(RESEARCH/'research.json')
    source=load(RESEARCH/'sources/kakaocorp--kanana-2-v-decide-3b-2611.json')
    overlay=load('catalog/revisions/v27-2026-11-07.json')
    data=build(old,load(c['materialized_catalog_path']),overlay,research,source,research)
    dump(OUT/'selected-file-capacity.json',data)
    summary={k:v for k,v in data.items() if k not in ('items','dependencies')}
    dump(OUT/'capacity-summary.json',summary)
    report=['# v27 publisher source-file logical capacity audit — 2026-11-07','',
        '126/126 exact primary source scopes. Owner physical disk space and complete offline bundle remain UNKNOWN.',
        'MOSS v1 external audio codec is dependent learned weight, NOT a new tracked model.',
        'No payload downloaded and no gate/contract approvals inferred.','',
        f"Known source primary bytes: {summary['known_primary_file_bytes_sum']}",
        f"Known SHA-aware logical bytes including dependencies: {summary['known_scope_content_union_bytes']}",
        f"4TB policy difference (NOT owner disk free): {summary['provisional_known_scope_budget_difference_bytes']}",
        f"Active assets still having open dependency/legal/runtime issues: {len(summary['assets_with_open_dependency_issues'])}",'',
        '| Repository | Primary selected source bytes | Open issues |','|---|---:|---:|']
    for item in data['items']:
        report.append(f"| {item['repo_id']} | {item['primary_file_bytes']} | {len(item['open_dependencies'])} |")
    target=ROOT/OUT/'capacity-report.md'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(report)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('assets_with_open_dependency_issues','profile_evidence')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
