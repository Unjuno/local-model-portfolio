#!/usr/bin/env python3
"""Source-only research: Pruna P-H3 and Maya2 necessary weights. No model payload."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts.latest_access_v23 import text_evidence
from scripts.capacity_selection import choose_files

ROOT=Path(__file__).resolve().parents[1]
OUT=Path('catalog/research/2026-11-06-insurance-r26')
SOURCES=('PrunaAI/P-H3-Image','PrunaAI/P-H3-Image-Comfy')
MAYA_DEPS={
 'kyutai/mimi':('catalog/capacity/2026-11-06/followup-sources/kyutai--mimi.json',
                '89091b3e466eb6a9d11e537bf26b144f194978f7',384657055,'cc-by-4.0'),
 'speechbrain/spkrec-ecapa-voxceleb':('catalog/capacity/2026-11-06/followup-sources/speechbrain--spkrec-ecapa-voxceleb.json',
                '0f99f2d0ebe89ac095bcc5903c4dd8f72b367286',89133738,'apache-2.0'),
}
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def validate_dep(repo,source):
    path,rev,bytes_expected,license_expected=MAYA_DEPS[repo]
    assert source['repo_id']==repo and source['tree_complete'] is True
    assert source['pinned_revision']==rev and source['source_scope_bytes']==bytes_expected
    assert source['license_metadata']==license_expected
    assert source['gated'] is False and source['payload_bytes_downloaded']==0
    assert exact_sum(f['bytes'] for f in source['files'])==bytes_expected
    selected=[f for f in source['files'] if f['path'].endswith(('.safetensors','.ckpt','.pth','.bin'))]
    assert len(selected)>0
    return {'repo_id':repo,'parent':'maya-research/maya2-native',
      'revision_observed':rev,'source_bytes':bytes_expected,
      'weight_bytes':exact_sum(f['bytes'] for f in selected),
      'weight_files':[{'path':f['path'],'bytes':f['bytes'],'sha256':f.get('sha256'),'git_blob_sha1':f.get('git_blob_sha1')} for f in selected],
      'license_metadata':license_expected,'source_snapshot':path,'is_required_by_creator_card':True,
      'not_included_in_maya2_primary_files':True,'personal_license_reviewed':False,
      'download_approved':False,'locally_hashed':False,'saved_to_owner_disk':False,
      'source_url':'https://huggingface.co/'+repo}
def summarize_pruna(repo,source):
    assert source['repo_id']==repo and source['tree_complete'] is True
    assert source['gated'] is False and source['payload_bytes_downloaded']==0
    assert isinstance(source['pinned_revision'],str) and len(source['pinned_revision'])==40
    assert exact_sum(f['bytes'] for f in source['files'])==source['source_scope_bytes']
    files=source['files']
    paths={f['path'] for f in files}
    assert 'LICENSE' in paths, 'copyright terms missing from source'
    names=[n for n in ('LICENSE','NOTICE') if n in paths]
    license_evidence=[text_evidence(repo,source['pinned_revision'],name) for name in names]
    assert len(license_evidence)>0 and all(x.get('retrieved') for x in license_evidence)
    row={'repo_id':repo,'decision':'RESEARCH_REQUIRES_LICENSE_AND_SELECTED_FILE_CLOSURE',
       'observed_gated':source['gated'],'license_tag':source['license_metadata'],
       'pinned_source_revision':source['pinned_revision'],
       'source_repository_bytes':source['source_scope_bytes'],
       'source_file_count':len(files),
       'publisher_safetensors_total_parameters':(source.get('parameter_metadata') or {}).get('total'),
       'source_url':'https://huggingface.co/'+repo,
       'license_evidence':license_evidence,
       'license_territorial_exclusions':['European Union','United Kingdom','Republic of Korea','United States'],
       'license_terms_need_personal_legal_review':True,
       'model_derivative_based_on':'MiniMaxAI/MiniMax-H3',
       'download_authorized':False,'model_payload_bytes_downloaded':0,
       'exact_selected_primary_bytes':None,'all_learned_dependencies_verified':False,
       'user_disk_measured':False,'source_tree_complete':True,
       'licensing_not_a_government_takedown':True,
       'upstream_model_reuse_not_automatically_required_for_full_finetuned_checkpoint':True,
       'specific_2026_regulation_probability':None,
       'weights_and_components':[{'path':f['path'],'bytes':f['bytes']} for f in files if f['path'].endswith('.safetensors')],
       'interesting_paths':[f['path'] for f in files if any(k in f['path'] for k in ('vae','text_encoder','upsampler','transformer','LICENSE','NOTICE','model_index'))][:85],
       'novel_trained_components':['8-step DMD distilled image diffusion','4B distilled text encoder','new single-frame decoder','Qwen3.5-based prompt upsampler'],
       'publisher_cautions':['limited geography; must not bypass legal terms','4-bit quality/composition differences','bf16 Diffusers model card 33B vs creator blog 20B optimized backbone claim; count closure needed'],
       'source_source_scope_not_selected_scope':True,
       'prior_model_not_in_active_selection':True,
    }
    if repo.endswith('P-H3-Image') and not repo.endswith('-Comfy'):
        profile={'diffusers':True}
        chosen,excluded=choose_files(files,profile)
        row['candidate_full_diffusers_profile']={
            'selected_file_bytes':exact_sum(f['bytes'] for f in chosen),
            'selected_file_count':len(chosen),
            'excluded_file_paths':[f['path'] for f in excluded],
            'weights_file_count':sum(f['path'].endswith('.safetensors') for f in chosen),
            'selected_file_paths':[f['path'] for f in chosen],
            'is_executable_manifest':False,
        }
        assert row['candidate_full_diffusers_profile']['weights_file_count']>1
        assert row['candidate_full_diffusers_profile']['selected_file_bytes']>10000000000
    return row
def main():
    c=load('catalog/CURRENT.json');v=load(c['materialized_catalog_path'])
    assert c['revision_id']=='v24-20261106' and c['expected']['tracked']==168 and c['expected']['active']==121
    assert len(v['items'])==168 and not load('queues/approved.json')['entries']
    selected={x['repo_id'].lower() for x in v['items']}
    assert all(x.lower() not in selected for x in SOURCES)
    snaps={}
    for repo in SOURCES:
        src=snapshot({'asset_kind':'model','repo_id':repo,'portfolio_decision':'research_only'})
        dump(ROOT/OUT/'sources'/(repo.replace('/','--')+'.json'),src)
        snaps[repo]=src
        print('Pruna source:',repo,src.get('pinned_revision'),src.get('source_scope_bytes'),src.get('error'))
    decisions=[summarize_pruna(r,snaps[r]) for r in SOURCES]
    dependencies=[validate_dep(r,load(x[0])) for r,x in MAYA_DEPS.items()]
    row={
       'schema_version':1,'review_date':'2026-11-06','baseline':'v24-20261106',
       'current_tracked':168,'current_active':121,
       'selection_changes':0,'download_authorized':False,'user_disk_measured':False,
       'primary_research_urls':[
          'https://www.pruna.ai/blog/oss-p-h3-image-launch',
          'https://huggingface.co/PrunaAI/P-H3-Image',
          'https://huggingface.co/PrunaAI/P-H3-Image-Comfy',
          'https://huggingface.co/maya-research/maya2-native',
          'https://huggingface.co/PrunaAI/P-H3-Image/blob/main/LICENSE'],
       'license_determination':'TERRITORY_RESTRICTED_COMMUNITY_LICENSE_NOT_A_GOVERNMENT_BAN; NO_LEGAL_CLEARANCE',
       'Pruna_candidates':decisions,'maya2_dependencies':dependencies,
       'maya2_external_publisher_repo_sum_bytes':sum(x['source_bytes'] for x in dependencies),
       'maya2_external_repo_bytes_are_not_new_full_portfolio_total':True,
       'independent_runtime_verified':False,
       'next_action':'Select one original learned checkpoint (Diffusers) only if immutable scope < risk-adjusted 4TB reserve and all licenses reviewed; keep Comfy 4-bit as optional runtime variant, do not select both',
    }
    dump(ROOT/OUT/'research.json',row)
    print(json.dumps({k:v for k,v in row.items() if k not in ('Pruna_candidates','maya2_dependencies')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
