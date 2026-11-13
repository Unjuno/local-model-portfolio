#!/usr/bin/env python3
"""R30 independent posttraining release and mandatory MOSS codec dependency closure.

Public HF source tree metadata only. NEVER fetch model tensors, run remote Python,
assume personal gate approval, authorize downloads, or measure owner's disk.
"""
from __future__ import annotations
from pathlib import Path
import json
from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts.latest_access_v23 import text_evidence
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
OUT=Path('catalog/research/2026-11-07-r30')
KAKAO='kakaocorp/kanana-2-v-decide-3b-2611'
RIPPLE_BASE='ricursiveAI/Ripple-65B-Base-Preview'
RIPPLE_INSTRUCT='ricursiveAI/Ripple-65B-Preview'
REPOS=[KAKAO,RIPPLE_BASE,RIPPLE_INSTRUCT]
MOSS='OpenMOSS-Team/MOSS-Audio-Tokenizer'
MOSS_SOURCE=Path('catalog/research/2026-11-07-dependency-readiness/sources/OpenMOSS-Team--MOSS-Audio-Tokenizer.json')
MOSS_AUDIT=Path('catalog/research/2026-11-07-dependency-readiness/audit.json')
V26=Path('catalog/capacity/2026-11-06/v26/selected-file-capacity.json')
SRC_DIR=OUT/'sources'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def must(condition,msg):
    if not condition:raise ValueError(msg)
def sha(v):
    return isinstance(v,str) and len(v)==40 and all(ch in '0123456789abcdef' for ch in v)
def identity_scope(row):
    return row['repo_id']+'@'+row['source_revision']
def accounted_entries(data):
    entries=[(identity_scope(r),f) for r in data['items'] for f in r['files']]
    entries += [(d['repo_id']+'@'+d['revision'],f) for d in data['dependencies'] for f in d['files']]
    return entries
def codec_accounting(old,snapshot_codec,audit_codec):
    must(old['source_revision']=='v26-20261106' and len(old['items'])==125,'v26 baseline changed')
    must(old['known_scope_content_union_bytes']==3_403_245_899_240,'v26 content sum changed')
    must(snapshot_codec['pinned_revision']=='3cd226ba2947efa357ef453bcad111b6eafba782','MOSS v1 source changed')
    must(snapshot_codec['repo_id']==MOSS and snapshot_codec['tree_complete'] is True,'wrong codec')
    r=next((r for r in audit_codec['codec_source_snapshots'] if r['repo_id']==MOSS),None)
    must(r is not None and r['candidate_complete_self_hosted_repo_subset_bytes']==7_098_711_111,'codec choice changed')
    files={f['path']:f for f in snapshot_codec['files']}
    selected=[files[f['path']] for f in r['candidate_files']]
    must(len(selected)==8 and len(set(f['path'] for f in selected))==8,'expected exactly 8 files')
    must(cap.sum_bytes(selected)==7_098_711_111,'codec subset bytes changed')
    must(len([f for f in selected if f['path'].endswith('.safetensors')])==2,'two shard source required')
    must(all(f['sha256'] for f in selected if f['path'].endswith('.safetensors')),'no strong weight hashes')
    old_entries=accounted_entries(old)
    baseline=cap.union_bytes(old_entries)
    must(baseline==old['known_scope_content_union_bytes'],'baseline inconsistent with source rows')
    new_entries=old_entries+[(MOSS+'@'+snapshot_codec['pinned_revision'],f) for f in selected]
    expanded=cap.union_bytes(new_entries)
    must(expanded>=baseline and expanded<=baseline+cap.sum_bytes(selected),'invalid union')
    # Without user disk proof, this is a publisher-hash-aware *logical* increment only.
    return {
      'source_revision':'v26-20261106',
      'baseline_exact_primary_asset_count':125,
      'baseline_known_hash_aware_logical_bytes':baseline,
      'required_moss_audio_codec_new_selected_primary_bytes':cap.sum_bytes(selected),
      'required_moss_audio_codec_hash_aware_logical_new_bytes':expanded-baseline,
      'source_only_expanded_known_hash_aware_bytes':expanded,
      'codec_source_ref':str(MOSS_SOURCE),
      'codec_full_repo_bytes':snapshot_codec['source_scope_bytes'],
      'codec_selected_files':[{'path':f['path'],'bytes':f['bytes'],
          'sha256':f.get('sha256'),'git_blob_sha1':f.get('git_blob_sha1'),
          'identity_kind':f.get('identity_kind')} for f in selected],
      'source_license_metadata':snapshot_codec['license_metadata'],
      'license_original_text_verified':False,
      'executable_manifest':False,
      'model_payload_bytes_downloaded':0,
      'model_payload_sha256_measured_locally':False,
      'disk_real_free_bytes':None,
      'download_time_peak_bytes':None,
      'complete_offline_archive_bytes':None,
      'source_dependency_completeness_improved_but_restoration_not_proven':True,
      'open_parent_asset_count_still_unresolved':34,
      'owner_disk_unsafe_to_infer':True,
    }
def classify(repo,src):
    must(src['repo_id']==repo and src['asset_kind']=='model','wrong source identity')
    must(src['tree_complete'] is True and src['payload_bytes_downloaded']==0 and src['download_authorized'] is False,'metadata source incomplete')
    must(sha(src['pinned_revision']),'invalid fixed revision')
    must(src['source_scope_bytes']==exact_sum(f['bytes'] for f in src['files']),'source file bytes mismatch')
    license_names=[n for n in ('LICENSE','LICENSE.md','LICENSE.txt','NOTICE') if n in {f['path'] for f in src['files']}]
    must(license_names,'missing source licensing')
    texts=[text_evidence(repo,src['pinned_revision'],n) for n in license_names]
    must(all(e['retrieved'] and len(e['sha256'])==64 for e in texts),'fixed license evidence unavailable')
    item={
       'repo_id':repo,'pinned_source_sha':src['pinned_revision'],
       'source_tree_complete':True,'source_repo_bytes':src['source_scope_bytes'],
       'source_repo_file_count':len(src['files']),
       'source_all_files_not_selected_files':True,
       'source_gated':src['gated'],'source_license_metadata':src['license_metadata'],
       'source_license_text_evidence':texts,'source_snapshot':str(SRC_DIR/(repo.replace('/','--')+'.json')),
       'total_safetensors_elements_publisher':(src.get('parameter_metadata') or {}).get('total'),
       'personal_access_verified':False,'download_approved':False,'source_payload_downloaded_bytes':0,
       'hardware_peak_ram_measured_bytes':None,'source_only_evidence_not_execution':True,
       'forecast_regulation_probability':None,
       'source_card_url':'https://huggingface.co/'+repo,
    }
    names={f['path'] for f in src['files']}
    if repo==KAKAO:
        must(src['gated'] is False,'Kanana unexpectedly gated')
        must(src['license_metadata']=='other','Kanana licence unexpectedly changed')
        must('model.safetensors' in names and 'tokenizer.json' in names and 'config.json' in names,'single full source model missing')
        must({'decision_kanana_v_decide.py','modeling_kanana_v_decide.py',
              'processing_kanana_v_decide.py','image_processing_kanana_v.py','LICENSE'}.issubset(names),'original custom decision/vision code missing')
        must(src['source_scope_bytes']<12_000_000_000,'unexpected giant weight capacity')
        # Original model weights are required; demos/images are not essential reconstruction dependencies.
        selected=[f for f in src['files'] if '/' not in f['path'] or f['path'].startswith('tokenizer/')]
        must(len(selected)>10 and any(f['path']=='model.safetensors' for f in selected),'selection empty')
        item.update(
          decision='CONDITIONAL_ARCHIVAL_SELECTION_REVIEW_UNAPPROVED',
          creator_announcement_date='2026-11-06',
          creator_announcement_url='https://www.kakaocorp.com/page/detail/12193',
          independently_trained_outcome='3.665B multimodal typed-decision probability embedding model adapted from Kanana-2-v-3b; NOT text-generative model, not quantization of another selected checkpoint',
          baseline_comparison=['microsoft/VibeVoice-1.5B','Hcompany/Holotron4-30B-A3B','nvidia/GR00T-N1.6-3B'],
          quantitative_negative_evidence='Creator results on own Korean 15909-question Decision Bench 72.50 and public Decision Index 61.34/Vision 61.12; no independent benchmark or measured owner GPU. Not a general text-generation model, vision only still images, up to 10.',
          reported_h200_latency='Developer claims <=0.04 sec per decision on single H200, batch/clock/backend not stated and performance NOT an independent benchmark',
          legal_critical_terms=['Kanana Open License (not Apache)', 'redistribution attribution/NOTICE and Powered by Kanana', 'separate commercial license for resold API/hosted access, SI/on-prem or on-device distribution', 'responsible-use guidelines incorporated'],
          candidate_original_selected_files_bytes=exact_sum(f['bytes'] for f in selected),
          candidate_original_selected_paths=[f['path'] for f in selected],
          candidate_selected_original_model_weight_bytes=next(f['bytes'] for f in selected if f['path']=='model.safetensors'),
          candidate_selection_is_not_approved_manifest=True,
          source_parameter_count_excludes_unverified_runtime_dependency=False,
          model_config_and_remote_code_execution_not_tested=True,
          required_pretrain_original_checkpoint_for_inference=False,
          all_code_dependencies_pinned_and_tested=False,
          falsification_condition='Return HOLD if licensed use unacceptable, missing inferred learned component, not materially different from existing trained weights, or actual 4TB/200GB floor unmet.',
       )
    else:
        must(src['gated'] is False and src['license_metadata']=='apache-2.0','Ripple license/gate changed')
        must(src['source_scope_bytes']>50_000_000_000,'Ripple source unexpectedly tiny')
        item.update(decision='RESEARCH_HOLD_CAPACITY_AND_DUPLICATE_COMPARISON',
         independently_trained_outcome='Ricursive 65B dense pretrained-from-scratch 12T tokens, pretrain-only base and BF16 instruction-tuned are two different learned stages',
         training_provenance='https://www.ricursive.com/ripple',
         preview_not_same_as_pretrain=repo==RIPPLE_INSTRUCT,
         research_negative_evidence='Developer agentic coding claims only; owner RAM+backend+long-context and independent quality unknown. Repo source bulk >50GB; do not add BF16, base and NVFP4 as duplicate default formats.',
         next_gate='Compare v26 general code models, pin runnable environment, verify smallest credible preservation of base vs post-train, then complete 4TB/200GB physical preflight.');
    return item
def main():
    c=load('catalog/CURRENT.json')
    must(c['revision_id']=='v26-20261106' and c['expected']['tracked']==172 and c['expected']['active']==125,'v26 changed; manual rebase needed')
    v=load(c['materialized_catalog_path'])
    must(len(v['items'])==172,'v26 view changed')
    previous={x['repo_id'].casefold() for x in v['items']}
    must(all(repo.casefold() not in previous for repo in REPOS),'already classified repository in CURRENT')
    must(load('queues/approved.json')['entries']==[],'approved queue nonempty')
    old=load(V26)
    moss_snapshot=load(MOSS_SOURCE)
    moss_audit=load(MOSS_AUDIT)
    codec=codec_accounting(old,moss_snapshot,moss_audit)
    data=[]
    for repo in REPOS:
        src=snapshot({'asset_kind':'model','repo_id':repo,'portfolio_decision':'research_only'})
        dump(ROOT/SRC_DIR/(repo.replace('/','--')+'.json'),src)
        if src.get('error'):raise ValueError(repo+': '+src['error'])
        record=classify(repo,src)
        data.append(record)
        print('CANDIDATE',repo,'sha',record['pinned_source_sha'],'bytes',record['source_repo_bytes'],flush=True)
    output={'schema_version':1,'observed_on':'2026-11-07','baseline_revision':'v26-20261106',
       'previous_tracked':172,'previous_active':125,
       'public_source_candidates':data,'mandatory_moss_codec_capacity_accounting':codec,
       'new_formal_selected_assets':0,'newly_approved_downloads':0,
       'model_payload_bytes_downloaded':0,'local_raid_or_hdd_tested':False,
       'main_branch_modified':False,
       'recommendation':'Select one Kanana trained BF16 model conditional research-only, keep Ripple Base/IT as research HOLD until capacity and quality comparison. Preserve MOSS original codec and do not replace it with v2.'
    }
    dump(ROOT/OUT/'research.json',output)
    dump(ROOT/OUT/'codec-capacity.json',codec)
    print('SUMMARY',json.dumps({
        'kanana_selected_source_bytes':data[0]['candidate_original_selected_files_bytes'],
        'moss_selected_source_bytes':codec['required_moss_audio_codec_new_selected_primary_bytes'],
        'moss_increment':codec['required_moss_audio_codec_hash_aware_logical_new_bytes'],
        'known_with_moss':codec['source_only_expanded_known_hash_aware_bytes'],
        'download_authorized':False},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
