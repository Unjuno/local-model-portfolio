#!/usr/bin/env python3
"""Offline source-file capacity evidence, NOT an acquisition manifest.
No payload retrieval, remote code execution, disk access, or approval changes.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'catalog/capacity/2026-11-06'
ALT={'onnx','original','metal','variants','int8'}
WEIGHT=re.compile(r'\.(safetensors|gguf|bin|pt|pth|ckpt|onnx|h5|msgpack|nemo|npz|onnx_data)$',re.I)
MEDIA=re.compile(r'\.(png|jpg|jpeg|gif|webp|mp4|wav|flac|mp3|ogg|m4a)$',re.I)
SHARD=re.compile(r'^(.*?)([0-9]{5})-of-([0-9]{5})(\.safetensors)$')
PROFILES={
 '0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF':{'weights':['RVN-Q4_K_M-multilingual.gguf'],'note':'Existing multilingual text Q4 selection; not vision, MTP, GSQ or all quantizations.'},
 'InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF':{'r21':'interpretic-gguf','note':'R21 Q4+projector; add original provenance, not BF16 weights.'},
 'chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1':{'r21':'chatr-adapter'},
 'Qwen/Qwen-Image-2.1':{'r21':'qwen-image-base','note':'Exact R21 shared base rather than unreviewed newer HEAD.'},
 'ausboss/Qwen-Image-2.1-Consistency-LoRA':{'weights':['qwen-image-2.1-consistency.safetensors'],'note':'Step1500 only; step2000 is not claimed identical.'},
 'nvidia/Nemotron-Cascade-2-SFT-Data':{'dataset_paths':['math/math_proof.jsonl','swe/swe_agentic.jsonl']},
 'nvidia/Granary-v2':{'dataset_label_manifests':True,
   'support_paths':['.gitattributes','LICENSE','LICENSES/CC-BY-SA-4.0.txt','NOTICE','README.md'],
   'mandatory_labels':['en/people_speech/en_asr.jsonl.gz'],
   'labels_only_no_audio':True,'license_scope':{
     'all_except_people_speech':'OpenMDW-1.1',
     'en/people_speech/en_asr.jsonl.gz':'CC-BY-SA-4.0'},
   'note':'All 148 released multilingual label JSONL.gz manifests plus 5 provenance/license files; no source audio. Rights partition from pinned LICENSE and NOTICE; no audio acquisition.'},
 'BAAI/bge-m3':{'weights':['pytorch_model.bin','colbert_linear.pt','sparse_linear.pt']},
 'usezn/Galvanize-3':{'weights':['onnx/model.onnx'],'allowed_alt':['onnx'],'note':'Existing preferred CPU ONNX path; no duplicate safetensors.'},
 'mistralai/Mistral-Small-4-119B-2603':{'exclude_weight_prefixes':['consolidated-'],'note':'HF model shards only. Precision/quantization from config, never inferred from size.'},
 'facebook/sam3':{'exclude_weights':['sam3.pt']},
 'facebook/vjepa2-vitg-fpc64-384':{'weights':['original/model.pth'],'allowed_alt':['original'],'note':'Conservatively preserve native original. Smaller HF export is not assumed to contain all original training state.'},
 'black-forest-labs/FLUX.2-dev':{'diffusers':True},
 'black-forest-labs/flux-3-image-klein-base':{'diffusers':True},
 'nvidia/Cosmos-Predict2-2B-Video2World':{'diffusers':True,'note':'Single Diffusers pipeline; native resolution/fps equivalence requires review.'},
 'Lightricks/LTX-2.5':{'weights':['diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors','text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors','vae/ltx-2.5-video-vae-bf16.safetensors','vae/ltx-2.5-audio-vae-bf16.safetensors','model_patches/ltx-2.5-duration-head-bf16.safetensors','latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors'],'note':'Publisher BF16 distilled recipe; duration and spatial upscaler included; no alternate DiT formats.'},
 'ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8':{'weights':['split/diffusion_models/ltx25_uncensored_v1.1-fp8_scaled.safetensors','split/text_encoders/gemma4_12b_ltx25_uncensored-int8.safetensors','split/vae/ltx25_uncensored_audio_vae.safetensors','split/vae/ltx25_uncensored_video_vae.safetensors'],'note':'Actual tree VAE names differ from README. Modified encoder is not replaced by official encoder.'},
 'Stuubs/Stubelius_Remix_Ltx2.5':{'weights':['ltx2.5-Stubelius_remix_v1_int8_convrot.safetensors'],'note':'v1 Comfy int8 representative, not experimental Q4 or old beta checkpoints.'},
 'KlingTeam/LivePortrait':{'exclude_prefixes':['liveportrait_animals/'],'note':'Human portrait scope; animal models are not claimed identical.'},
 'ResembleAI/chatterbox':{'weights':['t3_mtl23ls_v3.safetensors','ve.pt','s3gen.pt','conds.pt'],'note':'Named multilingual v3; current upstream mtl_tts.py requires ve.pt+s3gen.pt, not guessed s3gen_v3. Runtime revision still unpinned.'},
 'WhissleAI/steer-tts':{'exclude_prefixes':['native/int8/'],'note':'Original precision including bundled native encoders; interoperability and total count remain uncertified.'}
}
OPEN={
 'nvidia/Granary-v2':['All released labels have exact metadata bytes and license partition, but repository includes NO source audio. Future audio restoration requires separate lawful source corpus selection, bytes, revision, consent and hash review.'],
 'allenai/pixmo-cap':['External image URLs; captions alone are not requested image+caption package'],
 'ibm-granite/granite-switch-4.1-30b':['Decision/Guardian aLoRA and ASR attachment revisions'],
 'OpenMOSS-Team/MOSS-TTS-v1.5':['External audio tokenizer checkpoint/version'],
 'maya-research/maya2-native':['kyutai/mimi','speechbrain/spkrec-ecapa-voxceleb'],
 'WhissleAI/steer-tts':['Full learned count and native/Python frontend/encoder compatibility'],
 'fishaudio/drama-3':['Full codec-inclusive count and matching SGLang-Omni/vLLM-Omni revision'],
 'ausboss/Qwen-Image-2.1-Consistency-LoRA':['Comfy-Org INT8-convrot versus R21 BF16 adapter mapping and count'],
 'ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8':['Full learned count, Gemma tokenizer and donor conditions'],
 'Stuubs/Stubelius_Remix_Ltx2.5':['Full learned count and official text/VAE backend compatibility'],
 'Lightricks/LTX-2.5':['Gemma tokenizer, prompt enhancer and exact runtime closure'],
 'black-forest-labs/flux-3-image-klein-base':['Prompt upsampler and tokenizer/runtime closure'],
 'briaai/Fibo-2.0-dev':['VGL preprocessing/prompt expansion dependency closure'],
 'microsoft/TRELLIS.2-4B':['External vision encoder, background-removal models, CUDA build assets'],
 'speridlabs/idol':['Native FLUX AE versus Diffusers VAE interoperability and SDK requirements'],
 'tencent/Hunyuan3D-2.1':['Conditioning encoder and ancillary segmentation/texture tools'],
 'lerobot/pi0_base':['External tokenizer/processor and robot normalization'],
 'lerobot/smolvla_base':['Backbone tokenizer/processor and embodiment configuration'],
 'nvidia/GR00T-N1.6-3B':['External processor/tokenizer and embodiment assets'],
 'nvidia/Cosmos-Predict2-2B-Video2World':['Native resolution/fps variant provenance and external preprocessing/safety components'],
 'boltz-community/boltz-2':['MSA/reference-data path for completely offline operation'],
 'microsoft/VibeVoice-1.5B':['Qwen tokenizer and original inference code version'],
 'ResembleAI/chatterbox':['Pinned inference code, Perth watermark assets and text frontend'],
 'tencent/Hy-SimulMT-30B-A3B':['Separately selected speech-output TTS and streaming scaffold'],
 'facebook/vjepa2-vitg-fpc64-384':['Original checkpoint contents and native inference/conversion code']
}
SHARED={
 'LiquidAI/LFM2.5-VL-3B-DSpark':['LiquidAI/LFM2.5-VL-3B'],
 'udgamlabs/Lilavati-Checker':['udgamlabs/Lilavati'],
 'm-a-p/SheetSage2':['m-a-p/MERT-v2-FullSong'],
 'm-a-p/YuE2-3B':['m-a-p/YuE2-Vae'],
 'chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1':['Qwen/Qwen-Image-2.1'],
 'ausboss/Qwen-Image-2.1-Consistency-LoRA':['Qwen/Qwen-Image-2.1'],
 'speridlabs/idol':['facebook/dinov3-vith16plus-pretrain-lvd1689m']
}
def sum_bytes(files):
    values=[f['bytes'] for f in files]
    if any(v is not None and (type(v) is not int or v<0) for v in values):raise ValueError('invalid byte count')
    return None if None in values else sum(values)
def union_bytes(entries):
    unique={}
    for scope,f in entries:
        sum_bytes([f])
        k=('sha256',f['sha256']) if f.get('sha256') else (('git-blob',f['git_blob_sha1']) if f.get('identity_kind')=='git_blob_sha1' and f.get('git_blob_sha1') else ('scoped-path',scope,f['path']))
        if k in unique and unique[k]!=f['bytes']:raise ValueError('content identity size conflict')
        unique[k]=f['bytes']
    return None if None in unique.values() else sum(unique.values())
def complete_total(items):
    if any(r['open_dependencies'] or r['package_bytes'] is None for r in items):return None
    return sum(r['package_bytes'] for r in items)
def check_shards(files,declared_paths=None):
    groups={}
    for f in files:
        m=SHARD.match(f['path'])
        if m:
            prefix,i,n,suffix=m.groups();groups.setdefault((prefix,int(n),suffix),[]).append(int(i))
    for (prefix,n,suffix),parts in groups.items():
        if declared_paths is not None:
            expected={x for x in declared_paths if (m:=SHARD.match(x)) and m.group(1)==prefix and int(m.group(3))==n}
            actual={f['path'] for f in files if (m:=SHARD.match(f['path'])) and m.group(1)==prefix and int(m.group(3))==n}
            if expected:
                if actual!=expected:raise ValueError('index and selected shards disagree: '+prefix)
                continue
        if sorted(parts) not in (list(range(1,n+1)),list(range(n))):raise ValueError('incomplete shards: '+prefix)
def choose_files(files,profile):
    if len({f['path'] for f in files})!=len(files):raise ValueError('duplicate path')
    available={f['path'] for f in files}
    for p in profile.get('weights',[]):
        if p not in available:raise ValueError('missing explicit weight: '+p)
    if profile.get('dataset_label_manifests'):
        support=set(profile['support_paths'])
        if not support.issubset(available):raise ValueError('missing required label provenance/license/NOTICE')
        mandatory=set(profile.get('mandatory_labels',[]))
        if not mandatory.issubset(available):raise ValueError('mandatory separately licensed People_Speech manifest missing')
        labels={p for p in available if p.endswith('.jsonl.gz')}
        if not labels:raise ValueError('missing published label manifests')
        if any(not re.fullmatch(r'[a-z]{2,3}/[a-z][a-z0-9_]+/[a-z]{2,3}_asr(?:\.part[0-9]{2})?\.jsonl\.gz',p) for p in labels):
            raise ValueError('unrecognized label filename, review license partition')
    for p in profile.get('dataset_paths',[]):
        if not any(f==p or f.startswith(p.rstrip('/')+'/') for f in available):raise ValueError('missing subset: '+p)
    selected=[];excluded=[]
    for f in files:
        p=f['path'];parts=Path(p).parts;weight=bool(WEIGHT.search(p));reason=None
        if profile.get('dataset_label_manifests'):
            if p not in set(profile['support_paths']) and p not in labels:
                reason='outside published label manifests and LICENSE/NOTICE scope'
        elif profile.get('dataset_paths') is not None:
            allowed=any(p==x or p.startswith(x.rstrip('/')+'/') for x in profile['dataset_paths'])
            support='/' not in p and (p in ('.gitattributes','README.md') or p.lower().startswith(('license','notice')))
            if not allowed and not support:reason='outside selected dataset subset'
        elif profile.get('dataset_all'):pass
        else:
            if parts[0] in ALT and parts[0] not in profile.get('allowed_alt',[]):reason='alternative packaging not selected'
            if any(p.startswith(x) for x in profile.get('exclude_prefixes',[])):reason='out of named capability scope'
            if MEDIA.search(p):reason='demonstration media not required runtime artifact'
            if weight:
                if 'weights' in profile and p not in profile['weights']:reason='not the named checkpoint/component'
                if profile.get('diffusers') and '/' not in p:reason='native packaging alternative to selected pipeline'
                if p in profile.get('exclude_weights',[]):reason='explicit alternate representation'
                if any(p.startswith(x) for x in profile.get('exclude_weight_prefixes',[])):reason='alternative weight family'
                if p in ('pytorch_model.bin','tf_model.h5','flax_model.msgpack') and any(x.startswith('model') and x.endswith('.safetensors') and '/' not in x for x in available):
                    if p not in profile.get('weights',[]):reason='alternate framework export'
        if reason:excluded.append({'path':p,'bytes':f['bytes'],'reason':reason})
        else:selected.append(f)
    check_shards(selected,profile.get("index_shards"))
    if not selected:raise ValueError('empty selection')
    return selected,excluded

def r21_files(repo):
    out=[]
    for f in repo['files']:
        h=f.get('source_sha256')
        out.append({'path':f['path'],'bytes':f['bytes'],'sha256':h,'git_blob_sha1':f.get('git_blob_sha1'),
                    'identity_kind':'lfs_payload_sha256' if h else 'git_blob_sha1','local_hash_verified':False,
                    'evidence_scope':'R21 immutable historical plan, not newly downloaded bytes'})
    return out

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    current=load('catalog/CURRENT.json');view=load(current['materialized_catalog_path']);inv=load('catalog/capacity/2026-11-06/inventory.json')
    active=[x for x in view['items'] if x['portfolio_decision'] in ('select','conditional')]
    assert current['revision_id']=='v22-20261106' and len(active)==116 and len(view['items'])==163
    assert load('queues/approved.json')['entries']==[]
    sources={(x['asset_kind'],x['repo_id']):load(x['snapshot_path']) for x in inv['items']}
    historical={r['key']:r for r in load('manifests/drafts/round21-pinned-preservation.candidate.json')['repositories']}
    rows=[];byid={};all_entries=[]
    for item in active:
        repo=item['repo_id'];src=sources[(item['asset_kind'],repo)];profile=dict(PROFILES.get(repo,{}))
        if item['asset_kind']=='dataset' and 'dataset_paths' not in profile and not profile.get('dataset_label_manifests'):profile['dataset_all']=True
        if 'r21' not in profile:
            indexes=[]
            for d in src.get('documentation',[]):
                if isinstance(d.get('json'),dict) and isinstance(d['json'].get('weight_map'),dict):
                    parent=Path(d['path']).parent
                    indexes.extend(str(parent/x) for x in d['json']['weight_map'].values() if isinstance(x,str))
            if indexes:profile['index_shards']=sorted(set(indexes))
        row={'asset_kind':item['asset_kind'],'repo_id':repo,'portfolio_decision':item['portfolio_decision'],
             'scope_status':'EXACT_NAMED_FILE_PROFILE_PENDING_RIGHTS_AND_DEPENDENCY_REVIEW',
             'capacity_evidence_kind':'computed_sum_of_publisher_exact_file_metadata_not_local_measurement',
             'source_revision':src['pinned_revision'],'source_observed_at_utc':src['observed_at_utc'],
             'source_scope_bytes':src['source_scope_bytes'],'profile':profile,'gated':src.get('gated'),'license_metadata':src.get('license_metadata'),
             'personal_access_verified':False,'license_text_and_all_components_cleared':False,'source_parameter_gate':item.get('parameter_gate'),
             'runtime':{'measured_peak_ram_bytes':None,'backend_commit':None,'hardware':None,'context':None,'batch':None,'zero_point':None,'ABI':None,
                        'source_config':[{'path':d['path'],'quantization_config':d['json'].get('quantization_config'),'torch_dtype':d['json'].get('torch_dtype')} for d in src.get('documentation',[]) if isinstance(d.get('json'),dict) and ('quantization_config' in d['json'] or 'torch_dtype' in d['json'])]},
             'shared_dependencies':SHARED.get(repo,[]),'open_dependencies':list(OPEN.get(repo,[])),
             'software_environment_bytes':None,'offline_restore_tested':False,'download_authorized':False,
             'files':[],'package_bytes':None,'primary_file_bytes':None,'excluded_files':[]}
        if 'scope_unresolved' in profile:
            row['scope_status']='UNRESOLVED_SUBSET';rows.append(row);byid[repo]=row;continue
        try:
            if 'r21' in profile:
                r=historical[profile['r21']];files=r21_files(r);row['source_revision']=r['revision']
                row['scope_evidence']='R21 exact scope kept; current HEAD not automatically substituted'
            else:files,row['excluded_files']=choose_files(src['files'],profile)
            if profile.get('dataset_label_manifests'):
                manifests=[f for f in files if f['path'].endswith('.jsonl.gz')]
                people=next(f for f in manifests if f['path']=='en/people_speech/en_asr.jsonl.gz')
                row['license_partition']={
                    'OpenMDW-1.1_manifest_count':len(manifests)-1,
                    'OpenMDW-1.1_manifest_bytes':sum_bytes(f for f in manifests if f is not people),
                    'CC-BY-SA-4.0_people_speech_manifest_count':1,
                    'CC-BY-SA-4.0_people_speech_bytes':people['bytes'],
                    'provenance_and_license_notice_bytes':sum_bytes(f for f in files if not f['path'].endswith('.jsonl.gz')),
                    'license_full_text_read_from_fixed_source':True,
                    'publisher_licenses_and_third_party_audio_not_individually_cleared':True,
                    'audio_included':False,
                    'primary_license_urls':[
                        'https://huggingface.co/datasets/nvidia/Granary-v2/raw/'+src['pinned_revision']+'/LICENSE',
                        'https://huggingface.co/datasets/nvidia/Granary-v2/raw/'+src['pinned_revision']+'/NOTICE']}
                row['scope_status']='FULL_PUBLISHED_LABEL_MANIFEST_SCOPE_EXACT_AUDIO_DEPENDENCY_UNRESOLVED'
            row['files']=files;row['primary_file_bytes']=sum_bytes(files);row['package_bytes']=row['primary_file_bytes']
            row['masked_or_unknown_payload_identity_files']=sum(f.get('identity_kind') in ('unverifiable_payload_hash','unverified') for f in files)
            if item['asset_kind']=='model' and not any(WEIGHT.search(f['path']) for f in files):raise ValueError('no weights in scope')
            all_entries.extend((repo+'@'+row['source_revision'],f) for f in files)
        except ValueError as exc:
            row.update(scope_status='UNRESOLVED_FILE_SELECTION',primary_file_bytes=None,package_bytes=None,files=[]);row['open_dependencies'].append(str(exc))
        rows.append(row);byid[repo]=row
    dependencies=[]
    r=historical['interpretic-provenance'];fs=r21_files(r)
    dependencies.append({'parent':'InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF','repo_id':r['repo_id'],'revision':r['revision'],'files':fs,'bytes':sum_bytes(fs),'role':'provenance_only'})
    flux=sources[('model','black-forest-labs/FLUX.2-dev')];fs=[f for f in flux['files'] if f['path']=='ae.safetensors']
    if len(fs)!=1:raise ValueError('Idol native AE missing')
    dependencies.append({'parent':'speridlabs/idol','repo_id':flux['repo_id'],'revision':flux['pinned_revision'],'files':fs,'bytes':sum_bytes(fs),'role':'native_runtime_required_representation_not_assumed_same_bytes'})
    for d in dependencies:
        all_entries.extend((d['repo_id']+'@'+d['revision'],f) for f in d['files']);byid[d['parent']]['package_bytes']+=d['bytes']
    for row in rows:
        for dep in row['shared_dependencies']:
            target=byid[dep];row['package_bytes']=None if row['package_bytes'] is None or target['primary_file_bytes'] is None else row['package_bytes']+target['primary_file_bytes']
        if row['repo_id']=='Stuubs/Stubelius_Remix_Ltx2.5':
            target=byid['Lightricks/LTX-2.5'];fs=[f for f in target['files'] if f['path'].startswith(('text_encoders/','vae/'))]
            row['shared_component_dependency']={'repo_id':target['repo_id'],'revision':target['source_revision'],'paths':[f['path'] for f in fs],'bytes':sum_bytes(fs),'compatibility_verified':False}
            if row['package_bytes'] is not None:row['package_bytes']+=sum_bytes(fs)
    scoped=[r for r in rows if r['primary_file_bytes'] is not None]
    unknown=[{'repo_id':r['repo_id'],'reason':r['profile'].get('scope_unresolved') or r['open_dependencies']} for r in rows if r['primary_file_bytes'] is None]
    known_dedup=union_bytes(all_entries);largest=max(f['bytes'] for _,f in all_entries)
    summary={'schema_version':1,'source_revision':current['revision_id'],'tracked':163,'active':116,
      'formal_selection_changes':{'additions':0,'hold_transitions':0,'exclusions':0},
      'exact_primary_file_scope_count':len(scoped),'unresolved_primary_scope_count':len(unknown),
      'known_primary_file_bytes_sum':sum(r['primary_file_bytes'] for r in scoped),
      'known_parent_package_bytes_sum_with_shared_repetitions':sum(r['package_bytes'] for r in rows if r['package_bytes'] is not None),
      'known_dependency_additions_bytes':sum(d['bytes'] for d in dependencies),'known_scope_content_union_bytes':known_dedup,
      'source_identity_dedup_assumption':'Content-addressed store; SHA256+size or ordinary Git blob SHA1+size only. Masked LFS uses scoped path, never pointer hash. Physical allocated bytes/local reuse unmeasured.',
      'largest_selected_file_bytes':largest,'complete_learned_dependency_total_bytes':complete_total(rows),
      'complete_offline_archive_bytes':None,'complete_deduplicated_archive_bytes':None,'unknown_primary_scopes':unknown,
      'assets_with_open_dependency_issues':[{'repo_id':r['repo_id'],'issues':r['open_dependencies']} for r in rows if r['open_dependencies']],
      'all_runtime_environment_archives_unmeasured':True,'planning_cap_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
      'provisional_known_scope_budget_difference_bytes':4_000_000_000_000-known_dedup,'difference_is_not_available_headroom':True,
      'physical_disk_capacity_bytes':None,'physical_disk_free_bytes':None,'local_duplicate_bytes':None,'actual_remaining_archive_budget_bytes':None,'actual_acquisition_peak_bytes':None,
      'acquisition_scenarios_known_scope_only':{'direct_final_volume_atomic_rename_no_retained_cache_payload_bytes':known_dedup,
        'one_extra_largest_file_copy_payload_upper_scenario_bytes':known_dedup+largest,
        'retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes':2*known_dedup+largest,
        'assumptions':'Empty store, one asset at a time, no retries/residuals, logical bytes only; filesystem allocation, environments and unresolved components excluded. Not a measured maximum.'},
      'download_authorized':False,'executable':False,'model_payload_bytes_downloaded':0,
      'profile_evidence':['catalog/capacity/2026-11-06/source-review.md','manifests/drafts/round21-pinned-preservation.candidate.json','catalog/revisions/v22-2026-11-06.json'],
      'dependencies':dependencies,'items':rows}
    dump(OUT/'selected-file-capacity.json',summary)
    compact={k:v for k,v in summary.items() if k not in ('items','dependencies')};dump(OUT/'capacity-summary.json',compact)
    report=['# v22 capacity audit — 2026-11-06','','Publisher immutable file metadata and computed totals. No model payload or owner-disk measurements. Non-executable capacity evidence, NOT an acquisition manifest.','','## Results','','```json',json.dumps(compact,ensure_ascii=False,indent=2),'```','','## All active assets','','| Asset | Primary selected bytes | Package bytes (shared dependencies repeated) | Issues |','|---|---:|---:|---|']
    for r in rows:
        issues='; '.join(r['open_dependencies']) or 'No additional learned dependency identified in this review; runtime closure NOT certified'
        report.append('| '+r['repo_id']+' | '+str(r['primary_file_bytes'])+' | '+str(r['package_bytes'])+' | '+issues+' |')
    report+=['','## Interpretation','','Missing capacity is never zero. All 116 runtime/environment archives remain unmeasured. Exact file bytes do not establish full offline closure or personal access approval.',
      'Difference from the 4TB ceiling is NOT physical free storage or safe headroom. Unknown Granary subset, external images and dependencies must be accounted for before approval.',
      'Same-size weights are not deduplicated. Source-identity reuse assumes a content-addressed layout and later local hash verification. Filesystem allocation and hardlink support are untested.',
      'Format narrowing is not deletion of a local artifact. Historic catalog decisions and approved queue are unchanged. Native checkpoint contents are not assumed redundant solely because another export is smaller.',
      'R21 checksum discrepancies remain in the historical audit. R21 Qwen base is retained for ChatR; Consistency-LoRA interoperability is not proven.',
      'Machine learning checks distinct learned outcomes; software supply chain checks versions/components; digital preservation checks offline restoration. These checks are not interchangeable.',
      '','## Next gate','','Resolve the enumerated missing dependencies and Granary subset, then run read-only preflight on the actual owner volume. No model download, cloud execution, consent or approval is enabled.']
    (OUT/'capacity-report.md').write_text('\n'.join(report)+'\n',encoding='utf-8');print(json.dumps(compact,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
