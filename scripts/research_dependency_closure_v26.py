#!/usr/bin/env python3
"""Evidence-only v26 restoration dependency audit (2026-11-07).

No model weight download, no auth, no execution, no approved queue edits.
Fetches only anonymous public Hugging Face repository trees and small text metadata.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
OUT=Path('catalog/research/2026-11-07-dependency-readiness')
SOURCE=Path('catalog/capacity/2026-11-06/sources')
R27=Path('catalog/research/2026-11-06-round27/sources')
MOSS_PARENT=SOURCE/'model--OpenMOSS-Team--MOSS-TTS-v1.5.json'
LTX_PARENT=SOURCE/'model--Lightricks--LTX-2.5.json'
VIBE_PARENT=SOURCE/'model--microsoft--VibeVoice-1.5B.json'
CODECS=['OpenMOSS-Team/MOSS-Audio-Tokenizer','OpenMOSS-Team/MOSS-Audio-Tokenizer-v2']
CODE_SHA={
 'OpenMOSS/MOSS-TTS':'934d6826b084c46a0d033402174d5f8ac4ed2519',
 'Lightricks/LTX-2':'4f521619ae0029e8fbb64d555030c2b121a33b4f',
 'microsoft/VibeVoice':'16fb2cb1217c9934a886e1948ffb06120caa2df5',
 'huggingface/transformers':'640a08a597034221ca1c4fc0c129cf0118179225',
}
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha_ok(s):return isinstance(s,str) and len(s)==40 and all(ch in '0123456789abcdef' for ch in s)
def source_summary(repo,src):
    assert src['repo_id']==repo and src['asset_kind']=='model'
    assert src.get('payload_bytes_downloaded')==0 and src.get('download_authorized') is False
    assert src['tree_complete'] is True and src['gated'] is False
    assert sha_ok(src['pinned_revision'])
    files=src['files']
    assert len({f['path'] for f in files})==len(files)
    assert exact_sum(x['bytes'] for x in files)==src['source_scope_bytes']
    names={f['path'] for f in files}
    weight_files=[f for f in files if f['path'].endswith('.safetensors')]
    assert weight_files and 'model.safetensors.index.json' in names
    shard_names={f['path'] for f in weight_files if f['path'].startswith('model-')}
    docs=[d for d in src.get('documentation',[]) if d.get('path')=='model.safetensors.index.json' and isinstance(d.get('json'),dict)]
    assert len(docs)==1
    assert set(docs[0]['json']['weight_map'].values())==shard_names
    must=['config.json','README.md','model.safetensors.index.json']
    for fn in ('configuration_moss_audio_tokenizer.py','modeling_moss_audio_tokenizer.py','LICENSE'):
        if fn in names:must.append(fn)
    assert set(must).issubset(names)
    keep=[f for f in files if f['path'] in must or f in weight_files or f['path'] in ('__init__.py','NOTICE')]
    return {
       'repo_id':repo,'fixed_source_sha_observed':src['pinned_revision'],
       'source_repository_bytes':src['source_scope_bytes'],
       'source_file_count':len(files),'model_weight_file_count':len(weight_files),
       'model_weights_bytes':exact_sum(f['bytes'] for f in weight_files),
       'candidate_complete_self_hosted_repo_subset_bytes':exact_sum(f['bytes'] for f in keep),
       'candidate_files':[{'path':f['path'],'bytes':f['bytes'],'sha256':f['sha256'],'identity_kind':f['identity_kind']} for f in keep],
       'source_license_metadata':src['license_metadata'],
       'all_index_shards_present':True,'metadata_only':True,'personal_access_approved':False,
       'runtime_reconstruction_verified':False,
       'source_path':str(OUT/'sources'/(repo.replace('/','--')+'.json')),
    }
def check_parent_models(moss,ltx,vibe):
    assert moss['repo_id']=='OpenMOSS-Team/MOSS-TTS-v1.5'
    assert moss['pinned_revision']=='cdd3b911b1585e3f2dbc7775ef10f9926f58850a'
    assert moss['source_scope_bytes']==16_995_761_910
    assert vibe['repo_id']=='microsoft/VibeVoice-1.5B'
    assert vibe['pinned_revision']=='c00898d257e6b46004e3e2866a47534085fb685a'
    assert vibe['source_scope_bytes']==5_408_491_036
    assert ltx['repo_id']=='Lightricks/LTX-2.5' and ltx['gated']=='auto'
    assert ltx['pinned_revision']=='49b093a39c19169a8a81721dcc541e07e945232f'
    assert ltx['source_scope_bytes']==200_853_702_264
    p=cap.PROFILES['Lightricks/LTX-2.5']
    selected,excluded=cap.choose_files(ltx['files'],p)
    assert cap.sum_bytes(selected)==71_118_789_776
    bf16=[f for f in selected if f['path'].endswith('.safetensors')]
    assert len(bf16)==6
    assert all(not f['path'].endswith('int8-convrot.safetensors') for f in bf16)
    assert any('gemma4-12b-with-proj' in f['path'] for f in bf16)
    assert any('duration-head' in f['path'] for f in bf16)
    qsrc=load(R27/'Qwen--Qwen2.5-1.5B.json')
    assert qsrc['pinned_revision']=='8faed761d45a263340a0528343f099c05c9a4323'
    qpaths={'.gitattributes','LICENSE','README.md','config.json','generation_config.json',
            'merges.txt','tokenizer.json','tokenizer_config.json','vocab.json'}
    qfiles=[f for f in qsrc['files'] if f['path'] in qpaths]
    assert len(qfiles)==9 and cap.sum_bytes(qfiles)==11_505_079
    assert all(not f['path'].endswith('.safetensors') for f in qfiles)
    return {
       'moss_tts':{'fixed_sha':moss['pinned_revision'],'publisher_repo_bytes':moss['source_scope_bytes'],
                   'codec_fallback_repo_from_pinned_processing_source':'OpenMOSS-Team/MOSS-Audio-Tokenizer',
                   'codec_path_override_possible':True,
                   'source_code_url':'https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5/raw/'+moss['pinned_revision']+'/processing_moss_tts.py',
                   'processor_source_verified_by_read_only_2026_11_07':True,
                   'codec_is_not_in_moss_tts_parent_file_tree':True},
       'ltx_2_5':{'fixed_sha':ltx['pinned_revision'],'gated':'auto',
          'preselected_original_BF16_bytes':cap.sum_bytes(selected),
          'six_native_split_weight_file_bytes':cap.sum_bytes(bf16),
          'selected_weight_files':[{'path':f['path'],'bytes':f['bytes'],'sha256_visible':bool(f.get('sha256'))} for f in bf16],
          'prompt_enhancer':{'repo':'Comfy-Org/gemma-4','file':'gemma4_e2b_it_bf16.safetensors',
            'required_for_minimal_native_distilled_video':False,'required_if_using_optional_enhanced_prompts':True,
            'bytes':None,'source_url':'https://docs.ltx.io/open-source-model/usage-guides/text-to-video'},
          'native_runtime_candidate_git_sha':CODE_SHA['Lightricks/LTX-2'],
          'native_runtime_source_verified_but_compatibility_not_tested':True,
          'publisher_rights_or_download_approval_verified':False},
       'vibevoice':{'fixed_sha':vibe['pinned_revision'],
          'qwen_tokenizer_candidate_source_sha':qsrc['pinned_revision'],
          'qwen_tokenizer_nine_source_files_bytes':cap.sum_bytes(qfiles),
          'qwen_full_weights_required_for_tokenizer_only':False,
          'transformers_merged_vibevoice_PR_SHA':CODE_SHA['huggingface/transformers'],
          'microsoft_source_code_candidate_sha':CODE_SHA['microsoft/VibeVoice'],
          'native_conversion_same_tensor_shapes_reported_by_community_not_independently_run':True,
          'official_microsoft_model_HF_repo_confirmed':False,
          'source_community_proposal':'https://huggingface.co/microsoft/VibeVoice-1.5B/discussions/54',
          'output_restore_validated':False}
    }
def main():
    current=load('catalog/CURRENT.json')
    assert current['revision_id']=='v26-20261106' and current['expected']['tracked']==172
    assert current['expected']['active']==125
    assert load('queues/approved.json')['entries']==[]
    capacity=load('catalog/capacity/2026-11-06/v26/capacity-summary.json')
    assert capacity['known_scope_content_union_bytes']==3_403_245_899_240
    assert len(capacity['assets_with_open_dependency_issues'])==34
    parents=check_parent_models(load(MOSS_PARENT),load(LTX_PARENT),load(VIBE_PARENT))
    result=[]
    for repo in CODECS:
        src=snapshot({'asset_kind':'model','repo_id':repo,'portfolio_decision':'research_only'})
        dump(ROOT/OUT/'sources'/(repo.replace('/','--')+'.json'),src)
        row=source_summary(repo,src)
        result.append(row)
        print('CODEC',repo,row['fixed_source_sha_observed'],row['source_repository_bytes'])
    obj={
       'schema_version':1,'observed_at':'2026-11-07',
       'baseline_revision':'v26-20261106','current_assets':172,'current_active':125,
       'baseline_known_logical_dedup_bytes':3_403_245_899_240,
       'initial_assets_with_open_dependencies':34,
       'formal_selections_added':0,'formal_selections_removed':0,'capacity_catalog_changed':False,
       'codec_source_snapshots':result,
       'moss_v1_5_required_audio_codec_repo':CODECS[0],
       'moss_local_transformer_v1_5_uses_different_stereo_v2_codec':True,
       'moss_v2_codec_is_not_default_v1_5_dependency':True,
       'parents':parents,'verified_code_source_git_commit_shas':CODE_SHA,
       'codec_file_bytes_not_added_to_125_primary_file_total':True,
       'no_new_publisher_cache_or_sha256_verified_on_owner_disk':True,
       'missing_work':['owner disk space & expected peak staging','authenticated gate license rights',
                       'exact runtime ABI and environment capture','component load and offline playback experiments'],
       'download_approved':False,'model_payload_bytes_downloaded':0,'owner_disk_measured':False,
       'full_offline_total_bytes':None,'provisional_codec_gross_byte_upper_scenario':result[0]['source_repository_bytes'],
       'provisional_codec_is_not_verified_dedup_increment':True,
    }
    dump(ROOT/OUT/'audit.json',obj)
    print(json.dumps({k:v for k,v in obj.items() if k not in ('codec_source_snapshots','parents')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
