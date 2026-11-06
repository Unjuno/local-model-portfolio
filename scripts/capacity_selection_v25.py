#!/usr/bin/env python3
"""Non-executable v25 Pruna original Diffusers file accounting."""
from __future__ import annotations
import json
from pathlib import Path
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('catalog/capacity/2026-11-06/v24')
OUT=Path('catalog/capacity/2026-11-06/v25')
R=Path('catalog/research/2026-11-06-insurance-r26')

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,obj):
    x=ROOT/p;x.parent.mkdir(parents=True,exist_ok=True)
    x.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def audit(old,view,overlay,research,source):
    assert old['source_revision']=='v24-20261106' and len(old['items'])==121
    assert old['exact_primary_file_scope_count']==121 and old['unresolved_primary_scope_count']==0
    assert old['known_scope_content_union_bytes']==3_272_248_434_044
    assert view['revision_id']=='v25-20261106' and len(view['items'])==169
    a=overlay['additions']
    assert len(a)==1 and a[0]['repo_id']=='PrunaAI/P-H3-Image'
    item=a[0]
    assert item['parameter_gate']['status']=='UNVERIFIED_BLOCK_FINAL_LOCK'
    assert item['parameter_gate']['total_parameters'] is None
    assert item['research_only_unknown_total_allow_conditional'] is True
    assert item['download_approved'] is False and item['fully_pinned_revision_sha'] is None
    assert source['pinned_revision']==item['upstream_revision_sha_observed']
    assert source['source_scope_bytes']==item['upstream_all_files_bytes_observed']==99_845_388_933
    assert source['gated'] is False and source['tree_complete'] is True
    assert source['payload_bytes_downloaded']==0 and source['download_authorized'] is False
    r=next(x for x in research['Pruna_candidates'] if x['repo_id']=='PrunaAI/P-H3-Image')
    profile=r['candidate_full_diffusers_profile']
    paths=profile['selected_file_paths']
    all_source={f['path']:f for f in source['files']}
    assert len(set(paths))==len(paths) and set(paths).issubset(all_source)
    files=[all_source[p] for p in paths]
    assert cap.sum_bytes(files)==profile['selected_file_bytes']==99_840_428_064
    cap.check_shards(files)
    for dirname,n,prefix in [
      ('prompt_upsampler',4,'model-'),
      ('text_encoder',2,'model-'),
      ('transformer',7,'diffusion_pytorch_model-')]:
        keys={f['path'].split('/',1)[1] for f in files if f['path'].startswith(dirname+'/'+prefix) and f['path'].endswith('.safetensors')}
        assert len(keys)==n
        index=dirname+'/model.safetensors.index.json' if dirname!='transformer' else 'transformer/diffusion_pytorch_model.safetensors.index.json'
        assert index in set(paths)
        docs=[d for d in source.get('documentation',[]) if d['path']==index and isinstance(d.get('json'),dict)]
        assert len(docs)==1 and set(docs[0]['json']['weight_map'].values())==keys
    assert {'text_connector/diffusion_pytorch_model.safetensors','vae/diffusion_pytorch_model.safetensors',
            'LICENSE','NOTICE','LICENSE-APACHE'}.issubset(set(paths))
    new={
      'asset_kind':'model','repo_id':'PrunaAI/P-H3-Image','portfolio_decision':'conditional',
      'scope_status':'EXACT_DIFFUSERS_BF16_SOURCE_FILES_RESEARCH_ONLY_UNVERIFIED_FULL_PARAM_AND_LICENSE',
      'capacity_evidence_kind':'publisher immutable HF file sizes not local payload hashes',
      'source_revision':source['pinned_revision'],'source_observed_at_utc':source['observed_at_utc'],
      'source_scope_bytes':source['source_scope_bytes'],'primary_file_bytes':cap.sum_bytes(files),
      'package_bytes':cap.sum_bytes(files),'files':files,'excluded_files':profile['excluded_file_paths'],
      'profile':{'kind':'one 8-step BF16 Diffusers original; Comfy 4bit is non-adopted same trained result'},
      'source_parameter_gate':item['parameter_gate'],'gated':source['gated'],
      'license_metadata':source['license_metadata'],
      'personal_access_verified':False,'license_text_and_all_components_cleared':False,
      'runtime':{'measured_peak_ram_bytes':None,'backend_commit':None,'hardware':None,
         'context':None,'batch':None,'zero_point':None,'ABI':None},
      'shared_dependencies':[],
      'open_dependencies':[
        'MiniMax H3 Community License region and contractual subject review, hosting/reuse/redistribution compliance',
        'Complete learned pipeline tensor-element count including upsampler, distilled encoder, connector, image decoder and main transformer',
        'Reproducible pinned Modular Diffusers API, tokenizer and usage package compatibility, image quality/VRAM tests',
        'Derivative parent attribution and NOTICE obligations; no inferred permanent redistribution entitlement'],
      'software_environment_bytes':None,'offline_restore_tested':False,
      'download_authorized':False,
      'masked_or_unknown_payload_identity_files':sum(f.get('identity_kind') in ('unverifiable_payload_hash','unverified') for f in files)
    }
    rows=list(old['items'])+[new]
    assert len(rows)==122
    deps=old['dependencies']
    entries=[(x['repo_id']+'@'+x['source_revision'],f) for x in rows for f in x['files']]
    entries.extend((x['repo_id']+'@'+x['revision'],f) for x in deps for f in x['files'])
    unique=cap.union_bytes(entries)
    largest=max(f['bytes'] for _,f in entries)
    external=research['maya2_dependencies']
    assert len(external)==2 and sum(x['source_bytes'] for x in external)==473790793
    summary={
     'schema_version':1,'source_revision':'v25-20261106','tracked':169,'active':122,
     'old_exact_scopes':121,'new_exact_scopes':1,
     'exact_primary_file_scope_count':122,'unresolved_primary_scope_count':0,
     'known_primary_file_bytes_sum':sum(x['primary_file_bytes'] for x in rows),
     'known_scope_content_union_bytes':unique,
     'known_parent_package_bytes_with_repeated_references':sum(x['package_bytes'] for x in rows),
     'known_dependency_additions_bytes_from_v24':old['known_dependency_additions_bytes'],
     'complete_learned_dependency_total_bytes':cap.complete_total(rows),
     'complete_offline_archive_bytes':None,'complete_deduplicated_archive_bytes':None,
     'unknown_primary_scopes':[],
     'assets_with_open_dependency_issues':[{'repo_id':x['repo_id'],'issues':x['open_dependencies']} for x in rows if x['open_dependencies']],
     'all_runtime_environment_archives_unmeasured':True,
     'planning_cap_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
     'provisional_known_scope_budget_difference_bytes':4_000_000_000_000-unique,
     'difference_is_not_available_headroom':True,
     'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,
     'local_duplicate_bytes':None,'actual_remaining_archive_budget_bytes':None,
     'actual_acquisition_peak_bytes':None,'largest_selected_file_bytes':largest,
     'acquisition_scenarios_known_scope_only':{
         'direct_final_volume_atomic_rename_no_retained_cache_payload_bytes':unique,
         'one_extra_largest_file_copy_payload_upper_scenario_bytes':unique+largest,
         'retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes':2*unique+largest,
         'assumptions':'Empty store, no retries, payload bytes only, external learned dependencies not included.'},
     'maya2_external_two_repo_publisher_bytes_reported_not_double_counted':473790793,
     'maya2_external_two_repo_pinned_metadata_only':True,
     'download_authorized':False,'executable':False,'model_payload_bytes_downloaded':0,
     'profile_evidence':['catalog/capacity/2026-11-06/v24/selected-file-capacity.json',
                        'catalog/research/2026-11-06-insurance-r26/research.json',
                        'catalog/revisions/v25-2026-11-06.json'],
    }
    assert unique<4_000_000_000_000
    return dict(summary,items=rows,dependencies=deps)

def main():
    c=load('catalog/CURRENT.json')
    assert c['revision_id']=='v25-20261106'
    assert c['expected']['tracked']==169 and c['expected']['active']==122
    q=load(c['priority_worklist_path'])
    assert not q['download_enabled'] and not q['approved'] and not load('queues/approved.json')['entries']
    data=audit(load(BASE/'selected-file-capacity.json'),load(c['materialized_catalog_path']),
       load('catalog/revisions/v25-2026-11-06.json'),
       load(R/'research.json'),load(R/'sources/PrunaAI--P-H3-Image.json'))
    dump(OUT/'selected-file-capacity.json',data)
    summary={k:v for k,v in data.items() if k not in ('items','dependencies')}
    dump(OUT/'capacity-summary.json',summary)
    lines=['# v25 selected-file source metadata audit — 2026-11-06','',
        '122/122 primary publisher file scopes. No user disk, no model payload, no granted acquisition rights.','',
        'Total known primary bytes: '+str(summary['known_primary_file_bytes_sum']),
        'SHA-aware logical dedup: '+str(summary['known_scope_content_union_bytes']),
        'External/rights/runtime issues: '+str(len(summary['assets_with_open_dependency_issues'])),'',
        '| Repository | Primary bytes | Pending external/rights issues |',
        '|---|---:|---|']
    for row in data['items']:
        lines.append('| '+row['repo_id']+' | '+str(row['primary_file_bytes'])+' | '+str(len(row['open_dependencies']))+' |')
    p=ROOT/OUT/'capacity-report.md';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('assets_with_open_dependency_issues','profile_evidence')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
