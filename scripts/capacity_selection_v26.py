#!/usr/bin/env python3
"""v26 offline publisher metadata file census. Never download or execute model payloads."""
from __future__ import annotations
import json
from pathlib import Path
from scripts import capacity_selection as cap
ROOT=Path(__file__).resolve().parents[1]
HIST=Path('catalog/capacity/2026-11-06/v25')
OUT=Path('catalog/capacity/2026-11-06/v26')
R27=Path('catalog/research/2026-11-06-round27/sources')
R25=Path('catalog/research/2026-11-06-release-insurance/sources')
SUBS={
 'nvidia/Cosmos3-Nano-Sim-Auto':(R25/'nvidia--Cosmos3-Nano-Sim-Auto.json','e289a50a4049614eaa62c9edc10b1e8d6cc1a6c1',32_364_133_043,15_157_324_096),
 'gradium/phonon-31m-en':(R27/'gradium--phonon-31m-en.json','92741c5b07d085ff840e26fea8ce43110b87852f',223_333_254,41_096_035),
 'gradium/phonon-40m-multilingual':(R27/'gradium--phonon-40m-multilingual.json','1537ce46c64f42903e0d608b132ccb073dac46d2',257_581_010,50_539_363),
}
VOICE=(R27/'gradium--phonon-voices.json','0ee17205f254b5abc43b266c8a0f215565c352f7',69_292_384)
QWEN=(R27/'Qwen--Qwen2.5-1.5B.json','8faed761d45a263340a0528343f099c05c9a4323',3_098_972_223)
QWEN_METADATA={'LICENSE','README.md','config.json','generation_config.json','merges.txt','tokenizer.json','tokenizer_config.json','vocab.json','.gitattributes'}
def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def dump(path,obj):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def verified_source(src,repo,rev,bytes_expected,gate=None):
    assert src['repo_id']==repo and src['pinned_revision']==rev
    assert src['tree_complete'] is True and src['source_scope_bytes']==bytes_expected
    assert src['download_authorized'] is False and src['payload_bytes_downloaded']==0
    if gate is not None:assert src['gated']==gate
    assert len({f['path'] for f in src['files']})==len(src['files'])
    assert cap.sum_bytes(src['files'])==bytes_expected

def choose_phonon(src,repo):
    names={'model.safetensors','default-voice.safetensors'}
    files=[x for x in src['files'] if x['path'] not in ('model.q8.gguf','model.q4k.gguf')]
    assert names.issubset({x['path'] for x in files})
    assert len([x for x in files if x['path'].endswith('.safetensors')])==2
    assert not any(x['path'].endswith('.gguf') for x in files)
    assert 'processor_config.json' in {x['path'] for x in files}
    assert 'chat_template.jinja' in {x['path'] for x in files}
    expect=103_745_734 if repo.endswith('31m-en') else 122_629_650
    assert cap.sum_bytes(files)==expect
    return files
def chose_externals(voice_src,qwen_src):
    verified_source(voice_src,'gradium/phonon-voices',VOICE[1],VOICE[2],False)
    assert voice_src['license_metadata']=='apache-2.0'
    voices=[x for x in voice_src['files'] if x['path'].startswith('voices/') and x['path'].endswith('.safetensors')]
    assert len(voices)==102
    assert cap.sum_bytes(voices)==26_125_872
    support=[x for x in voice_src['files'] if x['path'] in {'README.md','.gitattributes','voices.jsonl'}]
    assert len(support)==3
    vf=voices+support
    assert cap.sum_bytes(vf)==26_183_423
    verified_source(qwen_src,'Qwen/Qwen2.5-1.5B',QWEN[1],QWEN[2],False)
    assert qwen_src['license_metadata']=='apache-2.0'
    qf=[x for x in qwen_src['files'] if x['path'] in QWEN_METADATA]
    assert len(qf)==9 and cap.sum_bytes(qf)==11_505_079
    assert not any(x['path'].endswith('.safetensors') for x in qf)
    return vf,qf

def build(old,view,overlay,source,voice_src,qwen_src):
    assert old['source_revision']=='v25-20261106' and len(old['items'])==122
    assert old['exact_primary_file_scope_count']==122 and old['unresolved_primary_scope_count']==0
    assert old['known_scope_content_union_bytes']==3_372_065_984_104
    assert view['revision_id']=='v26-20261106' and len(view['items'])==172
    assert len(overlay['additions'])==3 and {x['repo_id'] for x in overlay['additions']}==set(SUBS)
    assert len({x['repo_id'].lower() for x in old['items']})==122
    assert not {x['repo_id'] for x in old['items']}.intersection(SUBS)
    old_bi=next(x for x in old['items'] if x['repo_id']=='nvidia/Cosmos3-Nano-Sim-Bimanual')
    vae='vae/diffusion_pytorch_model.safetensors'
    old_vae=next(x for x in old_bi['files'] if x['path']==vae)
    vf,qf=chose_externals(voice_src,qwen_src)
    rows=list(old['items'])
    for item in overlay['additions']:
        repo=item['repo_id'];src=source[repo]
        snap,rev,bytes_expected,param=SUBS[repo]
        verified_source(src,repo,rev,bytes_expected)
        assert item['upstream_revision_sha_observed']==rev
        assert item['upstream_all_files_bytes_observed']==bytes_expected
        assert item['parameter_gate']['status']=='PASS_TOTAL_PARAMS_LT_150B'
        assert item['parameter_gate']['total_parameters']==param==src['parameter_metadata']['total']
        assert item['download_approved'] is False and item['fully_pinned_revision_sha'] is None
        assert item['selected_file_bytes'] is None and item['license_text_reviewed'] is False
        if repo=='nvidia/Cosmos3-Nano-Sim-Auto':
            files=list(src['files'])
            cap.check_shards(files)
            assert len(files)==45
            bypath={x['path']:x for x in files}
            assert {'lidar_vae/diffusion_pytorch_model.safetensors',
                    'vae/diffusion_pytorch_model.safetensors',
                    'model.safetensors.index.json',
                    'transformer/diffusion_pytorch_model.safetensors.index.json'}.issubset(bypath)
            assert bypath[vae]['sha256']==old_vae['sha256'] and bypath[vae]['bytes']==old_vae['bytes']==1_409_400_600
            bimap={x['path']:x for x in old_bi['files'] if x['path'].startswith('transformer/') and x['path'].endswith('.safetensors')}
            distinct=[p for p,x in bypath.items() if p.startswith('transformer/') and p.endswith('.safetensors')
                      and p in bimap and x.get('sha256') and bimap[p].get('sha256') and x['sha256']!=bimap[p]['sha256']]
            assert len(distinct)==6
            # Verify the exact publisher weight_map, not naive count-only file stem.
            for d in src.get('documentation',[]):
                if d['path']=='transformer/diffusion_pytorch_model.safetensors.index.json' and isinstance(d.get('json'),dict):
                    mapped=set(d['json']['weight_map'].values())
                    assert mapped=={x.split('/',1)[1] for x in distinct}
                    break
            else:raise AssertionError('Sim-Auto pinned transformer weight map missing')
            issues=['Pinned Cosmos Framework, FA4/CUDA and rolling history ABI not audited',
                    'WSM reference camera rig, LiDAR controls and reference files from Transfer-Auto missing/uncleared',
                    'OpenMDW plus source AV datasets and independent physics-quality evaluation pending']
            shared=['nvidia/Cosmos3-Nano-Sim-Bimanual:same-sha256-1.409GB-vae']
        else:
            files=choose_phonon(src,repo)
            issues=['Audio decoder-only inference + Gradium ptts/Transformers version and voice rights not verified',
                    'Upstream speaker codec is not published; only precomputed latents can be preserved',
                    'gradium/phonon-voices 102 latent file set requires license and attribution review']
            shared=['gradium/phonon-voices@'+VOICE[1]]
            if repo.endswith('multilingual'):
                assert src['gated']=='auto' and item.get('gated_approval_required') is True
                issues+=['GATED: authenticated personal access unverified, no automatic payload acquisition',
                         'CC BY-NC4.0 prohibits commercial use without separate authorization']
                assert all(x['path']!='model.q8.gguf' for x in files)
            else:
                assert src['gated'] is False
        sz=cap.sum_bytes(files)
        row={'asset_kind':'model','repo_id':repo,'portfolio_decision':'conditional',
            'scope_status':'EXACT_SOURCE_FILES_BUT_GATED_ACCESS_BLOCKED' if item.get('gated_approval_required') else 'EXACT_SOURCE_FILES_PENDING_RUNTIME_AND_RIGHTS',
            'capacity_evidence_kind':'publisher fixed file metadata; no local payload hashes',
            'source_revision':rev,'source_observed_at_utc':src['observed_at_utc'],
            'source_scope_bytes':bytes_expected,'primary_file_bytes':sz,
            'package_bytes':sz+(cap.sum_bytes(vf) if repo.startswith('gradium/') else 0),
            'files':files,'excluded_files':[{'path':x['path'],'bytes':x['bytes'],'reason':'alternate quant serialization'} for x in src['files'] if x not in files],
            'profile':{'one_original_BF16':repo.startswith('gradium/'),'alternative_GGUF_duplicates_excluded':repo.startswith('gradium/')},
            'source_parameter_gate':item['parameter_gate'],
            'gated':src['gated'],'license_metadata':src['license_metadata'],
            'personal_access_verified':False,'license_text_and_all_components_cleared':False,
            'runtime':{'measured_peak_ram_bytes':None,'backend_commit':None,'hardware':None,'context':None,'batch':None,'zero_point':None,'ABI':None},
            'shared_dependencies':shared,'open_dependencies':issues,
            'software_environment_bytes':None,'offline_restore_tested':False,
            'download_authorized':False,
            'masked_or_unknown_payload_identity_files':sum(x.get('identity_kind') in ('unverifiable_payload_hash','unverified') for x in files)}
        rows.append(row)
    assert len(rows)==125
    dependencies=list(old['dependencies'])+[
        {'parent':'gradium/phonon-31m-en & gradium/phonon-40m-multilingual',
         'repo_id':'gradium/phonon-voices','revision':VOICE[1],'files':vf,
         'bytes':cap.sum_bytes(vf),'role':'102 precomputed voice latents and index, no voice encoder',
         'shared_model_asset':False,'personal_license_reconciliation_complete':False,'user_disk_hash_verified':False},
        {'parent':'microsoft/VibeVoice-1.5B',
         'repo_id':'Qwen/Qwen2.5-1.5B','revision':QWEN[1],'files':qf,
         'bytes':cap.sum_bytes(qf),'role':'tokenizer/config source only; excludes full 1.5B Qwen weights',
         'original_conversion_code_version':'huggingface/transformers@640a08a597034221ca1c4fc0c129cf0118179225 (HF discussion proposal, not publisher runtime confirmation)',
         'personal_license_reconciliation_complete':False,'user_disk_hash_verified':False}
    ]
    entries=[(r['repo_id']+'@'+r['source_revision'],f) for r in rows for f in r['files']]
    entries.extend((d['repo_id']+'@'+d['revision'],f) for d in dependencies for f in d['files'])
    known=cap.union_bytes(entries)
    largest=max(f['bytes'] for _,f in entries)
    all_open=[{'repo_id':r['repo_id'],'issues':r['open_dependencies']} for r in rows if r['open_dependencies']]
    summary={
      'schema_version':1,'source_revision':'v26-20261106','tracked':172,'active':125,
      'previous_source_revision':'v25-20261106','old_scopes_exact':122,'new_scopes_exact':3,
      'exact_primary_file_scope_count':125,'unresolved_primary_scope_count':0,
      'known_primary_file_bytes_sum':sum(r['primary_file_bytes'] for r in rows),
      'known_scope_content_union_bytes':known,
      'known_parent_package_bytes_with_repeated_references':sum(r['package_bytes'] for r in rows),
      'known_dependency_additions_bytes':sum(d['bytes'] for d in dependencies),
      'complete_learned_dependency_total_bytes':cap.complete_total(rows),
      'complete_offline_archive_bytes':None,'complete_deduplicated_archive_bytes':None,
      'unknown_primary_scopes':[],
      'assets_with_open_dependency_issues':all_open,
      'all_runtime_environment_archives_unmeasured':True,
      'planning_cap_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
      'provisional_known_scope_budget_difference_bytes':4_000_000_000_000-known,
      'difference_is_not_available_headroom':True,
      'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,'local_duplicate_bytes':None,
      'actual_remaining_archive_budget_bytes':None,'actual_acquisition_peak_bytes':None,
      'largest_selected_file_bytes':largest,
      'acquisition_scenarios_known_scope_only':{
         'direct_final_volume_atomic_rename_no_retained_cache_payload_bytes':known,
         'one_extra_largest_file_copy_payload_upper_scenario_bytes':known+largest,
         'retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes':known*2+largest,
         'assumptions':'Empty store, no retries, logical bytes only; 34+ external dependency issues, hardware runtimes, physical filesystem unknown.'},
      'new_selected_primary_bytes_sum':sum(r['primary_file_bytes'] for r in rows if r['repo_id'] in SUBS),
      'source_repo_bytes_of_three_new_items_sum':sum(r['source_scope_bytes'] for r in rows if r['repo_id'] in SUBS),
      'new_shared_voices_source_selected_bytes':cap.sum_bytes(vf),
      'new_vibevoice_qwen_tokenizer_only_bytes':cap.sum_bytes(qf),
      'nvidia_Cosmos_common_vae_sha256':old_vae['sha256'],
      'nvidia_Cosmos_common_vae_bytes':old_vae['bytes'],
      'gated_model_source_payload_digest_masked_and_unverified':True,
      'download_authorized':False,'executable':False,'model_payload_bytes_downloaded':0,
      'profile_evidence':['catalog/capacity/2026-11-06/v25/selected-file-capacity.json','catalog/research/2026-11-06-round27/research.json','catalog/revisions/v26-2026-11-06.json']
    }
    assert summary['exact_primary_file_scope_count']==125 and summary['unresolved_primary_scope_count']==0
    assert known<4_000_000_000_000 and cap.complete_total(rows) is None
    return dict(summary,items=rows,dependencies=dependencies)

def main():
    c=load('catalog/CURRENT.json')
    assert c['revision_id']=='v26-20261106' and c['expected']['tracked']==172 and c['expected']['active']==125
    view=load(c['materialized_catalog_path'])
    overlay=load('catalog/revisions/v26-2026-11-06.json')
    q=load(c['priority_worklist_path'])
    assert not q['download_enabled'] and not q['approved'] and not load('queues/approved.json')['entries']
    old=load(HIST/'selected-file-capacity.json')
    src={k:load(row[0]) for k,row in SUBS.items()}
    voices=load(VOICE[0]); qwen=load(QWEN[0])
    data=build(old,view,overlay,src,voices,qwen)
    dump(OUT/'selected-file-capacity.json',data)
    compact={k:v for k,v in data.items() if k not in ('items','dependencies')}
    dump(OUT/'capacity-summary.json',compact)
    report=['# v26 selected-file primary capacity census (metadata only)','',
       'Fixed publisher metadata, not model downloads, not hardware measurements.','',
       f"Active file scopes: {compact['exact_primary_file_scope_count']}/125",
       f"Known logical SHA-sensitive dedup bytes: {compact['known_scope_content_union_bytes']}",
       f"Fully offline archived bytes: UNKNOWN; physical free disk: UNKNOWN.",
       f"New external voices + VibeVoice tokenizer file bytes: {compact['new_shared_voices_source_selected_bytes']} + {compact['new_vibevoice_qwen_tokenizer_only_bytes']}.",
       f"Assets with unresolved dependency issues: {len(all_open) if (all_open:=compact['assets_with_open_dependency_issues']) else 0}.",
       'Gated 40M multilingual has no automatic personal entitlement. Zero weight downloads.','',
       '| Asset | Selected primary bytes | Source revision | Open issues |',
       '|---|---:|---|---|']
    for row in data['items']:
        report.append(f"| {row['repo_id']} | {row['primary_file_bytes']} | {row['source_revision']} | {len(row['open_dependencies'])} |")
    target=ROOT/OUT/'capacity-report.md';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(report)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in compact.items() if k not in ('assets_with_open_dependency_issues','profile_evidence')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
