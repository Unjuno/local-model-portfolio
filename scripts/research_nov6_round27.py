#!/usr/bin/env python3
"""Bounded read-only Nov 6 research: original Phonon, voices, ERNIE base and VibeVoice tokenizer.

Only anonymous HF repository JSON, public source-tree metadata and named small
license texts. No model payload, execution, login, cloud spending or download authorization.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts.latest_access_v23 import text_evidence

ROOT=Path(__file__).resolve().parents[1]
OUT=Path('catalog/research/2026-11-06-round27')
CANDIDATES=(
    'gradium/phonon-31m-en',
    'gradium/phonon-40m-multilingual',
    'gradium/phonon-voices',
    'baidu/ERNIE-5.5-Flash-Base',
    'Qwen/Qwen2.5-1.5B',
)
TOK_FIXED='8faed761d45a263340a0528343f099c05c9a4323'

def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))
def path(repo):
    return OUT/'sources'/(repo.replace('/','--')+'.json')

def report(repo,source):
    files=source.get('files') or []
    named={x['path'] for x in files}
    full=source.get('tree_complete') is True and source.get('source_scope_bytes') is not None
    license_doc=[]
    if source.get('pinned_revision') and full:
        for name in ('LICENSE','LICENSE.md','LICENSE.txt','NOTICE'):
            if name in named:
                license_doc.append(text_evidence(repo,source['pinned_revision'],name))
    w=[f for f in files if f['path'].endswith(('.safetensors','.gguf','.ckpt','.bin','.pt','.pth'))]
    if full:assert exact_sum(f['bytes'] for f in files)==source['source_scope_bytes']
    row={
        'repo_id':repo,'snapshot':str(path(repo)),
        'source_revision':source.get('pinned_revision'),
        'fixed_version_is_selection_approval':False,
        'tree_complete':source.get('tree_complete'),
        'source_scope_bytes':source.get('source_scope_bytes'),
        'source_is_not_selected_file_bytes':True,
        'file_count':source.get('file_count'),
        'gated':source.get('gated'),
        'license_metadata':source.get('license_metadata'),
        'full_weights_not_downloaded':True,
        'download_authorized':False,
        'personal_access_verified':False,
        'licensed_to_user_verified':False,
        'param_total_publisher_display':(source.get('parameter_metadata') or {}).get('total'),
        'weighted_files':[{'path':f['path'],'bytes':f['bytes'],'sha256':f.get('sha256'),
                           'identity_kind':f.get('identity_kind')} for f in w],
        'license_evidence':license_doc,
        'observation_error':source.get('error'),
        'measured_peak_runtime_memory':None,
        'legal_clearance':False,
        'next_action':None,
    }
    if repo=='gradium/phonon-31m-en':
        row.update(decision='HIGH_VALUE_RESEARCH_AND_CONDITIONAL_SELECTION_REVIEW',
            independent_learned_outcome='Original English 31M Phonon flow-latent TTS; decoder-only PocketTTS/Mimi lineage, not another serialization of existing high-B TTS.',
            all_component_total_note='HF safetensors displayed total includes decoder audio tokenizer ~10M; creator distinguishes base 30.8M vs processor decoder 10.3M.',
            must_preserve=['preferred original precision and matching voice latent', 'checkpoint processor and audio tokenizer decoder',
                           'gradium/phonon-voices selected precomputed voices', 'gradium-ai/xn-ptts runtime commit',
                           'Apache 2.0 license + rights for voice latents'],
            primary_urls=['https://gradium.ai/blog/phonon-closer-look',
                          'https://huggingface.co/gradium/phonon-31m-en',
                          'https://huggingface.co/docs/transformers/model_doc/gradium_phonon_tts'],
            next_action='Choose one complete source checkpoint (not source plus every GGUF); verify internal decoder and default voice, exact selected bytes and runtime commit.')
    elif repo=='gradium/phonon-40m-multilingual':
        row.update(decision='S1_GATED_RESEARCH_NOT_ACQUISITION_AUTHORIZED',
            independent_learned_outcome='Additional 40M multilingual English/French/German/Spanish/Portuguese voice TTS learned checkpoint, distinct from 31M English model',
            primary_urls=['https://gradium.ai/blog/phonon-closer-look',
                          'https://huggingface.co/gradium/phonon-40m-multilingual'],
            must_preserve=['a complete multilingual learned checkpoint and internal decoder',
                           'precomputed voice latents and language normalization',
                           'license and pinned native runtime'],
            next_action='Observe actual gate and CC BY-NC terms; do not treat anonymous file listing as personal rights. Pin selected source weights before formal adoption.')
    elif repo=='gradium/phonon-voices':
        row.update(decision='SHARED_DEPENDENCY_CANDIDATE_NOT_NEW_AUTONOMOUS_MODEL',
            independent_learned_outcome='Precomputed speaker-latent vectors; creator did not publish upstream speaker encoder required to make arbitrary new voice latents.',
            primary_urls=['https://huggingface.co/gradium/phonon-voices',
                          'https://huggingface.co/docs/transformers/model_doc/gradium_phonon_tts'],
            must_preserve=['voice .safetensors and mapping metadata', 'source voice-specific license and consent policies'],
            next_action='Select full voice collection if inexpensive and rights verified. Preserve voices with Phonon original checkpoint, no claims that cloning from raw audio works offline.')
    elif repo=='baidu/ERNIE-5.5-Flash-Base':
        row.update(decision='S1_OVERSIZED_RESTRICTED_REGION_RESEARCH_ONLY',
            independent_learned_outcome='Pre-training-only 280B-class sparse MoE after 33.5T tokens, no SFT/DPO; expensive unique base to reconstruct',
            primary_urls=['https://huggingface.co/baidu/ERNIE-5.5-Flash-Base',
                          'https://ernie.baidu.com/release/ernie-5-5-flash-base/'],
            license_territory_excludes=['European Union','United Kingdom','South Korea'],
            verified_government_ban=False,
            size_rule='total experts >=150B; source FP8 file bytes and active 14B are NOT verified 150B reference RAM equivalence',
            next_action='Review fixed LICENSE and commercial threshold. Look for legitimate quantizer and measured same-condition <=150B reference peak with task fidelity before active selection.')
    elif repo=='Qwen/Qwen2.5-1.5B':
        row.update(decision='VIBEVOICE_TOKENIZER_SOURCE_LOCK_ONLY',
            independent_learned_outcome='Tokenizer provenance, NOT a reason to copy all Qwen2.5 pretrained weights',
            primary_urls=['https://huggingface.co/microsoft/VibeVoice-1.5B/discussions/54',
                          'https://huggingface.co/Qwen/Qwen2.5-1.5B'],
            subset_paths=['tokenizer.json','tokenizer_config.json','vocab.json','merges.txt','special_tokens_map.json','added_tokens.json',
                          'generation_config.json','config.json'],
            required_commit=TOK_FIXED,
            next_action='Verify pinned revision and exact tokenizer paths. Also pin canonical Transformers converter implementation; only relevant config/tokenizer source files required for VibeVoice, not 1.5B full weights.')
    return row

def main():
    c=load('catalog/CURRENT.json')
    v=load(c['materialized_catalog_path'])
    assert c['revision_id']=='v25-20261106' and c['expected']['tracked']==169 and c['expected']['active']==122
    assert len(v['items'])==169
    assert not load('queues/approved.json')['entries']
    active={x['repo_id'].casefold() for x in v['items']}
    assert not any(name.casefold() in active for name in CANDIDATES)
    records=[]
    for repo in CANDIDATES:
        src=snapshot({'asset_kind':'model','repo_id':repo,'portfolio_decision':'research_only',
                      **({'fully_pinned_revision_sha':TOK_FIXED} if repo=='Qwen/Qwen2.5-1.5B' else {})})
        dump(ROOT/path(repo),src)
        records.append(report(repo,src))
        print(repo,'pinned',src.get('pinned_revision'),'bytes',src.get('source_scope_bytes'),'error',src.get('error'))
    old=load('catalog/research/2026-11-06-release-insurance/sources/nvidia--Cosmos3-Nano-Sim-Auto.json')
    bimanual=load('catalog/research/2026-11-06-release-insurance/sources/nvidia--Cosmos3-Nano-Sim-Bimanual.json')
    assert old['tree_complete'] and old['pinned_revision']=='e289a50a4049614eaa62c9edc10b1e8d6cc1a6c1'
    assert old['source_scope_bytes']==32_364_133_043
    vae='vae/diffusion_pytorch_model.safetensors'
    def weightmap(s):return {f['path']:f for f in s['files'] if f['path'].endswith('.safetensors')}
    ow=weightmap(old); bw=weightmap(bimanual)
    assert ow[vae]['sha256'] and ow[vae]['sha256']==bw[vae]['sha256']
    changed=[p for p in ow if p.startswith('transformer/') and p in bw
             and ow[p]['sha256'] and bw[p]['sha256'] and ow[p]['sha256']!=bw[p]['sha256']]
    assert len(changed)==6, '6 post-trained transformer shards should differ from Bimanual'
    research={
        'schema_version':1,'date':'2026-11-06','source_revision':'v25-20261106',
        'current_tracked':169,'current_active':122,'catalog_changed':False,
        'current_known_dedup_bytes':3_372_065_984_104,
        'records':records,
        'cosmos_sim_auto_comparison':{
            'repo_id':old['repo_id'],'pinned_revision':old['pinned_revision'],
            'source_scope_bytes':old['source_scope_bytes'],'gated':old['gated'],'license_tag':old['license_metadata'],
            'shared_VAE_with_Bimanual_sha256':ow[vae]['sha256'],
            'shared_VAE_bytes':ow[vae]['bytes'],
            'changed_6_transformer_shards':changed,
            'developer_docs':'https://nvidia.github.io/cosmos-framework/inference_sim_auto/',
            'creator_model_card':'https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto',
            'difference':'Causal 4-step distillation of multi-camera+LiDAR WSM-driven driving model; distinct from Bimanual robot-manipulation action-model.',
            'negative':'Full offline Cosmos runtime, initial reference rig and WSM input files and independent driving physics/quality validation missing.',
            'decision':'S1_CONDITIONAL_EVALUATION_DISTINCT_LEARNING_ALREADY_PINNED',
            'formal_selection':False,'download_authorized':False,
        },
        'download_authorized':False,'weight_payloads_downloaded':0,'paid_compute_authorized':False,
        'owner_disk_measured':False,'regulation_probabilities':None,
        'license_or_gated_status_is_not_government_takedown':True,
    }
    dump(ROOT/OUT/'research.json',research)
    print('METADATA_ONLY',json.dumps({x['repo_id']:(x['tree_complete'],x['source_scope_bytes']) for x in records},sort_keys=True))
if __name__=='__main__':main()
