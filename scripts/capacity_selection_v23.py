#!/usr/bin/env python3
"""Non-executable v23 publisher-file accounting, reusing verified immutable v22 evidence."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
HIST=Path('catalog/capacity/2026-11-06')
OUT=HIST/'v23'
FOLLOW=HIST/'followup-sources'
NEW={
    'Hcompany/Holotron4-30B-A3B':{
        'source_path':FOLLOW/'Hcompany--Holotron4-30B-A3B.json',
        'expected_source_bytes':66_051_239_820,
        'expected_weight_shard_count':17,
        'expected_source_parameter_screen':33_015_598_915,
        'open_dependencies':[
            'Pinned NVIDIA Open Model Agreement parent rights and code static review',
            'Compatible NemotronH inference ABI and image/audio processor closure, offline test',
        ],
        'shared_dependencies':[],
        'file_profile':{'note':'One source-precision NemotronH checkpoint including 17 shards, index and native code; do not silently replace with existing Qwen Holo4'},
    },
    'LiquidAI/LFM2.5-24B-A2B-DSpark':{
        'source_path':FOLLOW/'LiquidAI--LFM2.5-24B-A2B-DSpark.json',
        'expected_source_bytes':656_291_264,
        'expected_weight_shard_count':0,
        'expected_source_parameter_screen':327_707_521,
        'open_dependencies':[
            'Target LiquidAI/LFM2.5-24B-A2B exact FP8 weight revision and SGLang DSpark commit/ABI require matching test',
            'LFM1.0 terms, latency and task parity on representative hardware unverified',
        ],
        'shared_dependencies':['LiquidAI/LFM2.5-24B-A2B'],
        'file_profile':{'weights':['model.safetensors'],'note':'Original learned 327.7M draft. Existing 24B target is not copied a second time; benchmark protocol retained.'},
    }
}

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def dump(path,obj):
    p=ROOT/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def verify_sources(old,view,overlay,snapshots):
    old=copy.deepcopy(old)
    assert old['source_revision']=='v22-20261106'
    assert len(old['items'])==116
    assert old['exact_primary_file_scope_count']==116 and old['unresolved_primary_scope_count']==0
    assert old['known_scope_content_union_bytes']==3_108_440_834_201
    assert len(view['items'])==165 and view['revision_id']=='v23-20261106'
    assert len(overlay['additions'])==2
    keys=lambda a:(a['asset_kind'].lower(),a['repo_id'].lower())
    prev={keys(a) for a in old['items']}
    active=[a for a in view['items'] if a['portfolio_decision'] in ('select','conditional')]
    assert len(active)==118
    assert {keys(a) for a in active}-{keys(a) for a in old['items']}=={('model',r.lower()) for r in NEW}
    assert {x['repo_id'] for x in overlay['additions']}==set(NEW)
    rows=list(old['items'])
    byid={row['repo_id']:row for row in rows}
    for item in overlay['additions']:
        key=item['repo_id']
        rule=NEW[key]
        src=snapshots[key]
        assert src['repo_id']==key and src['pinned_revision']==item['upstream_revision_sha_observed']
        assert src['source_scope_bytes']==rule['expected_source_bytes']==item['upstream_all_files_bytes_observed']
        assert src['tree_complete'] is True and src['gated'] is False
        assert src['payload_bytes_downloaded']==0 and not src['download_authorized']
        assert len({f['path'] for f in src['files']})==len(src['files'])
        assert cap.sum_bytes(src['files'])==src['source_scope_bytes']
        assert item['portfolio_decision']=='conditional' and item['download_approved'] is False
        assert item['fully_pinned_revision_sha'] is None and item['selected_file_bytes'] is None
        assert not item['license_text_reviewed'] and not item['dependencies_reviewed']
        params=src.get('parameter_metadata') or {}
        if key=='Hcompany/Holotron4-30B-A3B':
            assert params.get('total')==rule['expected_source_parameter_screen']
            shard_names=[f['path'] for f in src['files'] if f['path'].startswith('model-') and f['path'].endswith('.safetensors')]
            assert len(shard_names)==rule['expected_weight_shard_count']
            assert 'model.safetensors.index.json' in {f['path'] for f in src['files']}
        else:
            assert params.get('total')==rule['expected_source_parameter_screen']
            assert 'model.safetensors' in {f['path'] for f in src['files']}
        profile=copy.deepcopy(rule['file_profile'])
        if key=='Hcompany/Holotron4-30B-A3B':
            profile['weights']=shard_names
            index=[]
            for d in src.get('documentation',[]):
                j=d.get('json')
                if isinstance(j,dict) and isinstance(j.get('weight_map'),dict):
                    index=list(sorted(set(j['weight_map'].values())))
            # The immutable source inventory captures index file bytes but not its
            # full weight_map JSON; validate 17 contiguous shards now, and retain
            # index-map content verification as a separate final-lock requirement.
            if index:
                profile['index_shards']=index
        files,excluded=cap.choose_files(src['files'],profile)
        assert len(files)>0 and cap.sum_bytes(files) is not None
        assert any(f['path'].endswith('.safetensors') for f in files)
        assert len({f['path'] for f in files})==len(files)
        if key=='Hcompany/Holotron4-30B-A3B':
            assert sum(f['path'].startswith('model-') and f['path'].endswith('.safetensors') for f in files)==17
            if 'index_shards' in profile:
                assert set(profile['index_shards'])==set(shard_names)
            else:
                profile['index_weight_map_content_checked']=False
        if key=='LiquidAI/LFM2.5-24B-A2B-DSpark':
            assert sum(f['path'].endswith('.safetensors') for f in files)==1
        shared=rule['shared_dependencies']
        for dep in shared:assert dep in byid and byid[dep]['primary_file_bytes'] is not None
        own_bytes=cap.sum_bytes(files)
        row={
            'asset_kind':'model','repo_id':key,'portfolio_decision':'conditional',
            'scope_status':'EXACT_NAMED_PUBLISHER_FILE_SCOPE_PENDING_RIGHTS_AND_RUNTIME',
            'capacity_evidence_kind':'publisher_immutable_file_sizes_not_local_payload_or_filesystem_measurement',
            'source_revision':src['pinned_revision'],'source_observed_at_utc':src['observed_at_utc'],
            'source_scope_bytes':src['source_scope_bytes'],'profile':profile,
            'gated':src.get('gated'),'license_metadata':src.get('license_metadata'),
            'personal_access_verified':False,'license_text_and_all_components_cleared':False,
            'source_parameter_gate':item['parameter_gate'],
            'runtime':{'measured_peak_ram_bytes':None,'backend_commit':None,'hardware':None,'context':None,
                       'batch':None,'zero_point':None,'ABI':None},
            'shared_dependencies':shared,'open_dependencies':copy.deepcopy(rule['open_dependencies']),
            'software_environment_bytes':None,'offline_restore_tested':False,'download_authorized':False,
            'files':files,'package_bytes':own_bytes+sum(byid[dep]['primary_file_bytes'] for dep in shared),
            'primary_file_bytes':own_bytes,'excluded_files':excluded,
            'selected_source_model_already_in_active_catalog':bool(shared),
            'masked_or_unknown_payload_identity_files':sum(f.get('identity_kind') in ('unverified','unverifiable_payload_hash') for f in files),
        }
        if profile.get('index_weight_map_content_checked') is False:
            row['index_weight_map_content_checked']=False
            row['open_dependencies'].append('Pinned index file bytes known; weight_map content membership still requires review')
        rows.append(row);byid[key]=row
    assert len(rows)==118
    return rows

def compute_summary(old,rows):
    dependencies=old['dependencies']
    entries=[(r['repo_id']+'@'+r['source_revision'],f) for r in rows for f in r['files']]
    entries.extend((d['repo_id']+'@'+d['revision'],f) for d in dependencies for f in d['files'])
    known=cap.union_bytes(entries)
    total=cap.sum_bytes(f for r in rows for f in r['files'])
    all_largest=max(f['bytes'] for _,f in entries)
    additional=[r for r in rows if r['repo_id'] in NEW]
    summary={
        'schema_version':1,'source_revision':'v23-20261106','tracked':165,'active':118,
        'formal_selection_changes_already_in_v23':{'additions':2,'hold_transitions':0,'exclusions':0},
        'baseline_previous_source_revision':'v22-20261106',
        'baseline_primary_file_scopes':116,'new_primary_file_scopes':2,
        'exact_primary_file_scope_count':sum(x['primary_file_bytes'] is not None for x in rows),
        'unresolved_primary_scope_count':sum(x['primary_file_bytes'] is None for x in rows),
        'known_primary_file_bytes_sum':total,
        'known_parent_package_bytes_sum_with_shared_repetitions':cap.sum_bytes({'bytes':r['package_bytes']} for r in rows),
        'known_dependency_additions_bytes':cap.sum_bytes({'bytes':d['bytes']} for d in dependencies),
        'known_scope_content_union_bytes':known,
        'source_identity_dedup_assumption':old['source_identity_dedup_assumption'],
        'largest_selected_file_bytes':all_largest,
        'complete_learned_dependency_total_bytes':cap.complete_total(rows),
        'complete_offline_archive_bytes':None,'complete_deduplicated_archive_bytes':None,
        'unknown_primary_scopes':[{'repo_id':r['repo_id'],'reason':r['open_dependencies']} for r in rows if r['primary_file_bytes'] is None],
        'assets_with_open_dependency_issues':[{'repo_id':r['repo_id'],'issues':r['open_dependencies']} for r in rows if r['open_dependencies']],
        'all_runtime_environment_archives_unmeasured':True,
        'planning_cap_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
        'provisional_known_scope_budget_difference_bytes':4_000_000_000_000-known,
        'difference_is_not_available_headroom':True,
        'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,
        'local_duplicate_bytes':None,'actual_remaining_archive_budget_bytes':None,'actual_acquisition_peak_bytes':None,
        'acquisition_scenarios_known_scope_only':{
            'direct_final_volume_atomic_rename_no_retained_cache_payload_bytes':known,
            'one_extra_largest_file_copy_payload_upper_scenario_bytes':known+all_largest,
            'retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes':2*known+all_largest,
            'assumptions':'Empty store, one asset at a time, no retries/residuals. Logical bytes only; not measured maximal peak. 27 open dependencies and original audio not included.'},
        'download_authorized':False,'executable':False,'model_payload_bytes_downloaded':0,
        'new_assets_selected_primary_file_bytes_sum':sum(x['primary_file_bytes'] for x in additional),
        'new_assets_publisher_all_repo_bytes_sum':sum(x['source_scope_bytes'] for x in additional),
        'profile_evidence':[str(HIST/'capacity-summary.json'),
                            str(FOLLOW/'Hcompany--Holotron4-30B-A3B.json'),
                            str(FOLLOW/'LiquidAI--LFM2.5-24B-A2B-DSpark.json'),
                            'catalog/revisions/v23-2026-11-06.json']
    }
    assert summary['exact_primary_file_scope_count']==118
    assert summary['unresolved_primary_scope_count']==0
    assert len(summary['assets_with_open_dependency_issues'])>=25
    return summary

def main():
    current=load('catalog/CURRENT.json');view=load(current['materialized_catalog_path'])
    overlay=load('catalog/revisions/v23-2026-11-06.json')
    old=load(HIST/'selected-file-capacity.json')
    sources={repo:load(rule['source_path']) for repo,rule in NEW.items()}
    assert current['revision_id']=='v23-20261106'
    assert current['expected']['tracked']==165 and current['expected']['active']==118
    assert load('queues/approved.json')['entries']==[]
    assert load(current['priority_worklist_path'])['download_enabled'] is False
    rows=verify_sources(old,view,overlay,sources)
    summary=compute_summary(old,rows)
    out=dict(summary,items=rows,dependencies=old['dependencies'])
    dump(OUT/'selected-file-capacity.json',out)
    dump(OUT/'capacity-summary.json',summary)
    lines=['# v23 selected-file capacity audit — 2026-11-06','',
      'Publisher immutable file metadata. No model payload, runtime or user filesystem measured.',
      '## Known numbers','',
      'Primary file sum: '+str(summary['known_primary_file_bytes_sum'])+' bytes.',
      'SHA-aware logical dedup known scope: '+str(summary['known_scope_content_union_bytes'])+' bytes.',
      'Exact primary file scopes: '+str(summary['exact_primary_file_scope_count'])+'/118.',
      'Remaining external dependency issues: '+str(len(summary['assets_with_open_dependency_issues']))+'.',
      'Complete offline archive bytes: UNKNOWN. Actual disk bytes and free: UNKNOWN. Approval: 0.','',
      '| Repo ID | Selected primary bytes (source metadata) | Package including repeated references | Open dependency issues |',
      '|---|---:|---:|---|']
    for r in rows:
        lines.append('| '+r['repo_id']+' | '+str(r['primary_file_bytes'])+' | '+str(r['package_bytes'])+' | '+str(len(r['open_dependencies']))+' |')
    dump(OUT/'capacity-note.json',{'explanation':'v23 118 selected primary scopes, not all offline restore components or disk.','source_revision':'v23-20261106','user_disk_measured':False})
    p=ROOT/OUT/'capacity-report.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('assets_with_open_dependency_issues','profile_evidence')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
