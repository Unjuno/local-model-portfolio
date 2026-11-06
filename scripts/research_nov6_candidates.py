#!/usr/bin/env python3
"""Bounded Nov 6 2026 primary release review. Anonymous metadata ONLY, no payload."""
from __future__ import annotations
import json
from pathlib import Path

from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts.latest_access_v23 import text_evidence
from scripts.capacity_selection import choose_files, sum_bytes, check_shards

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('catalog/research/2026-11-06-release-insurance')
PREVIOUS = Path('catalog/research/2026-11-06-latest-v23/sources')
SCOPE = (
    'pfnet/plamo-3-translate-31b',
    'nvidia/Cosmos3-Nano-Sim-Bimanual',
    'nvidia/Cosmos3-Nano-Sim-Auto',
    'orcarouter/GLM-5.3-Flash-Uncensored-GGUF',
)
SOURCE_URLS = {
    'pfnet/plamo-3-translate-31b':[
        'https://www.preferred.jp/en/news/pr20261105',
        'https://www.preferred.jp/en/blog/tech/plamo-3-translate-weight-release',
        'https://huggingface.co/pfnet/plamo-3-translate-31b',
    ],
    'nvidia/Cosmos3-Nano-Sim-Bimanual':[
        'https://huggingface.co/blog/nvidia/cosmos-interactive-world-simulation',
        'https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Bimanual',
        'https://nvidia.github.io/cosmos-framework/inference_bimanual/',
    ],
    'nvidia/Cosmos3-Nano-Sim-Auto':[
        'https://huggingface.co/blog/nvidia/cosmos-interactive-world-simulation',
        'https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto',
    ],
    'orcarouter/GLM-5.3-Flash-Uncensored-GGUF':[
        'https://huggingface.co/orcarouter/GLM-5.3-Flash-Uncensored-GGUF',
        'https://huggingface.co/orcarouter/GLM-5.3-Flash-Uncensored-FP8',
    ],
}
POSITIVE = {
    SCOPE[0]:'31B translation-specialized final SFT/DPO teacher, distinct from general chat and later 0.8B student distillation.',
    SCOPE[1]:'Independent causal-distilled action-conditioned bimanual robotics video model (YAM/AgiBot and camera navigation), 59 values padded to 64.',
    SCOPE[2]:'Independent 4-step distillation of Transfer-Auto for rolling multi-camera+LiDAR driving observations; do not call it a duplicate of Sim-Bimanual.',
    SCOPE[3]:'Abliterated >320B MoE for research on refusal controls and vision; GGUF removes native 7B-class MTP while preserving separate mmproj.',
}
NEGATIVE = {
    SCOPE[0]:'Provider benchmark only; PLaMo community license needs exact private-commercial distinction; different-size teacher vs student requires explicit preservation reason.',
    SCOPE[1]:'No hardware memory or offline runtime measured; Cosmos Framework custom actions, encoders, video codecs and OpenMDW license boundaries require closure.',
    SCOPE[2]:'Potential significant duplication with Sim-Bimanual and older Cosmos; multi-view+LiDAR runtime, conditioning inputs, HD maps and memory unknown.',
    SCOPE[3]:'Gated access not personally verified; upstream license, all-experts total ~321B, matched <150B reference RAM and GGUF MTP loss unverified; Q4 ~193GB is not peak RAM.',
}
DECISION = {
    SCOPE[0]:'CONDITIONAL_SELECTION_EVALUATION_AFTER_EXACT_BYTES',
    SCOPE[1]:'CONDITIONAL_SELECTION_EVALUATION_AFTER_EXACT_BYTES',
    SCOPE[2]:'HOLD_COMPARATIVE_RESEARCH_NOT_AUTOMATIC_FOUR_COSMOS_COPIES',
    SCOPE[3]:'S1_RESEARCH_ONLY_GATED_OVERSIZED_QUANT_EXCEPTION_NOT_PROVEN',
}
def path(repo):
    return OUT / 'sources' / (repo.replace('/','--')+'.json')

def load(p):
    return json.loads((ROOT/p).read_text(encoding='utf-8'))

def candidate(src, repo):
    row={
        'repo_id':repo,
        'snapshot_path':str(path(repo)),
        'evidence_scope':'anonymous HF metadata + specific named small text files, no weights',
        'source_revision_observed':src.get('pinned_revision'),
        'source_revision_is_not_final_acquisition_lock':True,
        'source_repo_bytes':src.get('source_scope_bytes'),
        'source_repo_bytes_are_not_verified_selected_bytes':True,
        'source_file_count':src.get('file_count'),
        'tree_complete':src.get('tree_complete'),
        'observed_access':src.get('gated'),
        'license_metadata':src.get('license_metadata'),
        'parameter_total_publisher_display':(src.get('parameter_metadata') or {}).get('total'),
        'previous_active_catalog_present':False,
        'decision':DECISION[repo],
        'positive':POSITIVE[repo],
        'negative':NEGATIVE[repo],
        'source_urls':SOURCE_URLS[repo],
        'specific_model_takedown_verified':False,
        'distribution_restriction_scenario':'HYPOTHESIS',
        'regulatory_probability':None,
        'selected_file_bytes':None,
        'final_offline_dependency_bytes':None,
        'reference_ram_memory_proven':False,
        'software_runtime_pinned':False,
        'local_file_hash_verified':False,
        'user_access_verified':False,
        'user_disk_bytes_measured':False,
        'download_authorized':False,
        'legal_clearance_for_acquisition':False,
        'license_text_evidence':[],
        'technical_file_profile':None,
    }
    if src.get('tree_complete') and src.get('pinned_revision'):
        paths={f['path'] for f in src['files']}
        names=[x for x in ('LICENSE','LICENSE.md','LICENSE/en','LICENSE/ja','NOTICE') if x in paths]
        row['license_text_evidence']=[text_evidence(repo,src['pinned_revision'],x) for x in names]
        if repo==SCOPE[0]:
            files,excluded=choose_files(src['files'],{})
            row['technical_file_profile']={
                'type':'single_BF16_checkpoint_all_shards',
                'candidate_selected_primary_bytes':sum_bytes(files),
                'candidate_file_count':len(files),
                'excluded_demo_or_alternates':excluded,
                'selected_files_are_not_user_download_approval':True,
                'weights_shards_count':sum(f['path'].startswith('model-') and f['path'].endswith('.safetensors') for f in files),
            }
    return row

def main():
    current=load('catalog/CURRENT.json')
    assert current['revision_id']=='v23-20261106'
    v=load(current['materialized_catalog_path'])
    assert len(v['items'])==165 and current['expected']['active']==118
    assert not load('queues/approved.json')['entries']
    active={x['repo_id'].casefold() for x in v['items']}
    assert not any(x.casefold() in active for x in SCOPE)
    snapshots={}
    for repo in SCOPE:
        s=snapshot({'asset_kind':'model','repo_id':repo,'portfolio_decision':'research_only'})
        dump(ROOT/path(repo),s)
        snapshots[repo]=s
        print('SOURCE',repo,s.get('pinned_revision'),s.get('source_scope_bytes'),'ERROR',s.get('error'))
    saved=load(PREVIOUS/'pfnet--plamo-3-translate-0.8b.json')
    assert saved['repo_id']=='pfnet/plamo-3-translate-0.8b'
    assert saved['tree_complete'] and saved['source_scope_bytes']==1_785_576_024
    decisions=[candidate(snapshots[x],x) for x in SCOPE]
    for r in decisions:
        r['previous_active_catalog_present']=r['repo_id'].casefold() in active
    summary={
        'date':'2026-11-06',
        'review':'RELEASE_RESEARCH_BEFORE_ANY_FORMAL_SELECTION',
        'base_revision':'v23-20261106',
        'base_tracked':165,'base_active':118,
        'new_repos_reviewed':len(SCOPE),
        'existing_0_8b_distilled_student_snapshot':str(PREVIOUS/'pfnet--plamo-3-translate-0.8b.json'),
        'existing_0_8b_source_bytes':saved['source_scope_bytes'],
        'individual_source_tree_complete':{r['repo_id']:r['tree_complete'] for r in decisions},
        'file_bytes_in_current_active_catalog_changed':False,
        'non_executable':True,'download_authorized':False,
        'model_payload_bytes_downloaded':0,'owner_disk_measured':False,
        'new_formal_selections':0,
        'primary_development_date':'2026-11-05',
        'decisions':decisions,
    }
    dump(ROOT/OUT/'candidate-review.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='decisions'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
