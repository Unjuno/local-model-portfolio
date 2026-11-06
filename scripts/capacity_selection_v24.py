#!/usr/bin/env python3
"""Offline immutable source-file accounting for v24; no payload, model load or disk measurement."""
from __future__ import annotations
import json
from pathlib import Path
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('catalog/capacity/2026-11-06/v23')
OUT=Path('catalog/capacity/2026-11-06/v24')
RESEARCH=Path('catalog/research/2026-11-06-release-insurance/sources')
OLD=Path('catalog/research/2026-11-06-latest-v23/sources')
RULES={
 'pfnet/plamo-3-translate-31b':{
    'path':RESEARCH/'pfnet--plamo-3-translate-31b.json',
    'expected_sha':'01eac57bf80ef8114decd998f8f3a803ba795557',
    'expected_repo_bytes':63_519_912_375,
    'expected_primary_bytes':63_518_748_101,
    'expected_params':31_757_456_384,
    'format':'Original BF16 / 14 shards, not another quantization of 0.8B',
    'dependencies':['PLaMo Community License/commercial registration and redistribution attribution review',
                    'PFN custom modeling_plamo.py and tokenization_plamo.py runtime dependency and 32,768 token context evaluation'],
    'reuse':[],
 },
 'pfnet/plamo-3-translate-0.8b':{
    'path':OLD/'pfnet--plamo-3-translate-0.8b.json',
    'expected_sha':'cc8e88169807d5a272e8ff06db12eb0129b67f81',
    'expected_repo_bytes':1_785_576_024,
    'expected_primary_bytes':None,
    'expected_params':890_344_960,
    'format':'Original BF16 distilled 0.8B student, not teacher quantization',
    'dependencies':['PLaMo Community License, English/Japanese terms and redistribution duties',
                    'Custom tokenizer and 31B teacher provenance; teacher not a runtime necessity'],
    'reuse':[],
 },
 'nvidia/Cosmos3-Nano-Sim-Bimanual':{
    'path':RESEARCH/'nvidia--Cosmos3-Nano-Sim-Bimanual.json',
    'expected_sha':'a9e3adf6235f56f0082be7a96e497348c286c472',
    'expected_repo_bytes':31_830_399_442,
    'expected_primary_bytes':31_830_399_442,
    'expected_params':15_173_136_576,
    'format':'Original causal-distilled action-video model with six transformer shards, VAE, action schema and training examples',
    'dependencies':['Pinned NVIDIA Cosmos Framework runtime and vLLM-Omni ABI, Linux/CUDA configuration',
                    'OpenMDW-1.1 license and third-party action/video rights, schema-5 control validation'],
    'reuse':[],
 },
}
def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def dump(path,value):
    p=ROOT/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def build(old,view,overlay,sources):
    assert old['source_revision']=='v23-20261106'
    assert len(old['items'])==118 and old['known_scope_content_union_bytes']==3_175_147_816_831
    assert old['exact_primary_file_scope_count']==118 and old['unresolved_primary_scope_count']==0
    assert view['revision_id']=='v24-20261106' and len(view['items'])==168
    assert len(overlay['additions'])==3 and {x['repo_id'] for x in overlay['additions']}==set(RULES)
    original={x['repo_id'] for x in old['items']}
    assert not original.intersection(RULES)
    rows=list(old['items'])
    for item in overlay['additions']:
        repo=item['repo_id'];rule=RULES[repo];src=sources[repo]
        assert src['repo_id']==repo and src['tree_complete'] is True
        assert src['pinned_revision']==rule['expected_sha']==item['upstream_revision_sha_observed']
        assert src['source_scope_bytes']==rule['expected_repo_bytes']==item['upstream_all_files_bytes_observed']
        assert src['gated'] is False and src['payload_bytes_downloaded']==0 and src['download_authorized'] is False
        assert src['parameter_metadata']['total']==rule['expected_params']==item['parameter_gate']['total_parameters']
        assert not item['download_approved'] and item['fully_pinned_revision_sha'] is None
        assert item['selected_file_bytes'] is None and item['license_text_reviewed'] is False
        names={f['path'] for f in src['files']}
        assert len(names)==len(src['files'])
        assert cap.sum_bytes(src['files'])==src['source_scope_bytes']
        if repo.startswith('pfnet/'):
            files,excluded=cap.choose_files(src['files'],{})
            assert 'tokenizer.jsonl' in {f['path'] for f in files}
            assert 'modeling_plamo.py' in {f['path'] for f in files}
            assert 'tokenization_plamo.py' in {f['path'] for f in files}
            assert {'LICENSE/en','LICENSE/ja'}.issubset({f['path'] for f in files})
            if repo.endswith('31b'):
                sh={f['path'] for f in files if f['path'].startswith('model-') and f['path'].endswith('.safetensors')}
                assert len(sh)==14 and 'model.safetensors.index.json' in {f['path'] for f in files}
                for d in src.get('documentation',[]):
                    if d['path']=='model.safetensors.index.json' and isinstance(d.get('json'),dict):
                        assert set(d['json']['weight_map'].values())==sh
                        break
                else:raise AssertionError('31B source index must match all shards')
            else:
                assert sum(f['path'].endswith('.safetensors') for f in files)==1
        else:
            files=src['files'][:]  # all 91: original weights, VAE, action schema and reproducibility examples
            excluded=[]
            cap.check_shards(files)
            assert len(files)==91
            assert len([f for f in files if f['path'].startswith('transformer/') and f['path'].endswith('.safetensors')])==6
            assert 'vae/diffusion_pytorch_model.safetensors' in names
            assert 'model.safetensors.index.json' in names and 'transformer/diffusion_pytorch_model.safetensors.index.json' in names
            assert 'cosmos3_nano_sim_bimanual_action_sources/action_schema.json' in names
            assert 'cosmos3_nano_sim_bimanual_artifact.json' in names
            assert 'examples/training/SHA256SUMS' in names
        sz=cap.sum_bytes(files)
        if rule['expected_primary_bytes'] is not None:assert sz==rule['expected_primary_bytes']
        rows.append({
            'asset_kind':'model','repo_id':repo,'portfolio_decision':'conditional',
            'scope_status':'COMPLETE_PUBLISHER_PRIMARY_FILE_SET_PENDING_USER_RIGHTS_RUNTIME',
            'capacity_evidence_kind':'immutable_publisher_API_bytes_no_local_payload_or_local_hash',
            'source_revision':src['pinned_revision'],'source_observed_at_utc':src['observed_at_utc'],
            'source_scope_bytes':src['source_scope_bytes'],'primary_file_bytes':sz,
            'package_bytes':sz,'files':files,'excluded_files':excluded,
            'profile':{'format':rule['format'],'source_file_count':len(src['files'])},
            'source_parameter_gate':item['parameter_gate'],
            'gated':src['gated'],'license_metadata':src['license_metadata'],
            'personal_access_verified':False,'license_text_and_all_components_cleared':False,
            'runtime':{'measured_peak_ram_bytes':None,'backend_commit':None,
                       'hardware':None,'context':None,'batch':None,'zero_point':None,'ABI':None},
            'open_dependencies':rule['dependencies'],
            'shared_dependencies':rule['reuse'],
            'software_environment_bytes':None,'offline_restore_tested':False,
            'download_authorized':False,
            'masked_or_unknown_payload_identity_files':sum(f.get('identity_kind') in ('unverifiable_payload_hash','unverified') for f in files),
        })
    assert len(rows)==121
    assert len({x['repo_id'].lower() for x in rows})==121
    others=old['dependencies']
    entries=[(x['repo_id']+'@'+x['source_revision'],f) for x in rows for f in x['files']]
    entries.extend((x['repo_id']+'@'+x['revision'],f) for x in others for f in x['files'])
    known=cap.union_bytes(entries)
    largest=max(f['bytes'] for _,f in entries)
    summary={
        'schema_version':1,'source_revision':'v24-20261106','tracked':168,'active':121,
        'previous_revision':'v23-20261106','old_file_scopes_exact':118,'new_file_scopes_exact':3,
        'exact_primary_file_scope_count':sum(x['primary_file_bytes'] is not None for x in rows),
        'unresolved_primary_scope_count':sum(x['primary_file_bytes'] is None for x in rows),
        'known_primary_file_bytes_sum':sum(x['primary_file_bytes'] for x in rows),
        'known_scope_content_union_bytes':known,
        'known_parent_package_bytes_with_shared_repetitions':sum(x['package_bytes'] for x in rows),
        'known_dependency_additions_bytes':old['known_dependency_additions_bytes'],
        'source_identity_dedup_assumption':old['source_identity_dedup_assumption'],
        'largest_selected_file_bytes':largest,
        'new_selected_primary_bytes_sum':sum(x['primary_file_bytes'] for x in rows if x['repo_id'] in RULES),
        'new_source_repos_all_bytes_sum':sum(x['source_scope_bytes'] for x in rows if x['repo_id'] in RULES),
        'complete_learned_dependency_total_bytes':cap.complete_total(rows),
        'complete_offline_archive_bytes':None,'complete_deduplicated_archive_bytes':None,
        'unknown_primary_scopes':[],
        'assets_with_open_dependency_issues':[{'repo_id':x['repo_id'],'issues':x['open_dependencies']} for x in rows if x['open_dependencies']],
        'all_runtime_environment_archives_unmeasured':True,
        'planning_cap_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
        'provisional_known_scope_budget_difference_bytes':4_000_000_000_000-known,
        'difference_is_not_available_headroom':True,
        'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,
        'local_duplicate_bytes':None,'actual_remaining_archive_budget_bytes':None,
        'actual_acquisition_peak_bytes':None,
        'acquisition_scenarios_known_scope_only':{
            'direct_final_volume_atomic_rename_no_retained_cache_payload_bytes':known,
            'one_extra_largest_file_copy_payload_upper_scenario_bytes':known+largest,
            'retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes':known*2+largest,
            'assumptions':'Empty store, no retries; logical bytes only. External learned dependencies/permissions and owner disks unknown.'},
        'download_authorized':False,'executable':False,'model_payload_bytes_downloaded':0,
        'profile_evidence':['catalog/capacity/2026-11-06/v23/selected-file-capacity.json',
          'catalog/research/2026-11-06-release-insurance/candidate-review.json',
          'catalog/research/2026-11-06-latest-v23/candidate-decisions.json'],
    }
    assert summary['exact_primary_file_scope_count']==121
    assert summary['unresolved_primary_scope_count']==0
    assert known<4_000_000_000_000
    return dict(summary,items=rows,dependencies=others)

def main():
    c=load('catalog/CURRENT.json')
    assert c['revision_id']=='v24-20261106' and c['expected']['active']==121
    v=load(c['materialized_catalog_path'])
    q=load(c['priority_worklist_path'])
    assert not q['approved'] and not q['download_enabled']
    assert not load('queues/approved.json')['entries']
    previous=load(BASE/'selected-file-capacity.json')
    overlay=load('catalog/revisions/v24-2026-11-06.json')
    source={k:load(r['path']) for k,r in RULES.items()}
    out=build(previous,v,overlay,source)
    dump(OUT/'selected-file-capacity.json',out)
    compact={k:v for k,v in out.items() if k not in ('items','dependencies')}
    dump(OUT/'capacity-summary.json',compact)
    lines=['# v24 primary-file capacity census — 2026-11-06','',
      'Immutable public source-file metadata; no owner payload, disk, runtime or permission measurement.',
      'Primary file scopes: 121/121; unknown primary: 0.',
      'Primary selected bytes: '+str(compact['known_primary_file_bytes_sum']),
      'Known logical content-dedup bytes: '+str(compact['known_scope_content_union_bytes']),
      'Full offline archive, owner disk, and local duplicates: UNKNOWN.',
      'External dependency open assets: '+str(len(compact['assets_with_open_dependency_issues'])), '',
      '| Repo ID | Primary chosen bytes | Open dependency issues |',
      '|---|---:|---:|']
    for a in out['items']:
        lines.append('| '+a['repo_id']+' | '+str(a['primary_file_bytes'])+' | '+str(len(a['open_dependencies']))+' |')
    target=ROOT/OUT/'capacity-report.md';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in compact.items() if k not in ('assets_with_open_dependency_issues','profile_evidence')},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
