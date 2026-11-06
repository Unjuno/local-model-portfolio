# v22 capacity audit — 2026-11-06

Publisher immutable file metadata and computed totals. No model payload or owner-disk measurements. Non-executable capacity evidence, NOT an acquisition manifest.

## Results

```json
{
  "schema_version": 1,
  "source_revision": "v22-20261106",
  "tracked": 163,
  "active": 116,
  "formal_selection_changes": {
    "additions": 0,
    "hold_transitions": 0,
    "exclusions": 0
  },
  "exact_primary_file_scope_count": 114,
  "unresolved_primary_scope_count": 2,
  "known_primary_file_bytes_sum": 2933166075842,
  "known_parent_package_bytes_sum_with_shared_repetitions": 3040745255366,
  "known_dependency_additions_bytes": 336241419,
  "known_scope_content_union_bytes": 2931606771845,
  "source_identity_dedup_assumption": "Content-addressed store; SHA256+size or ordinary Git blob SHA1+size only. Masked LFS uses scoped path, never pointer hash. Physical allocated bytes/local reuse unmeasured.",
  "largest_selected_file_bytes": 55942929173,
  "complete_learned_dependency_total_bytes": null,
  "complete_offline_archive_bytes": null,
  "complete_deduplicated_archive_bytes": null,
  "unknown_primary_scopes": [
    {
      "repo_id": "openai/gpt-oss-120b",
      "reason": [
        "incomplete shards: model-"
      ]
    },
    {
      "repo_id": "nvidia/Granary-v2",
      "reason": "Permitted per-corpus label subset not determined; full repository is not automatically selected."
    }
  ],
  "assets_with_open_dependency_issues": [
    {
      "repo_id": "microsoft/VibeVoice-1.5B",
      "issues": [
        "Qwen tokenizer and original inference code version"
      ]
    },
    {
      "repo_id": "OpenMOSS-Team/MOSS-TTS-v1.5",
      "issues": [
        "External audio tokenizer checkpoint/version"
      ]
    },
    {
      "repo_id": "ResembleAI/chatterbox",
      "issues": [
        "Pinned inference code, Perth watermark assets and text frontend"
      ]
    },
    {
      "repo_id": "black-forest-labs/flux-3-image-klein-base",
      "issues": [
        "Prompt upsampler and tokenizer/runtime closure"
      ]
    },
    {
      "repo_id": "briaai/Fibo-2.0-dev",
      "issues": [
        "VGL preprocessing/prompt expansion dependency closure"
      ]
    },
    {
      "repo_id": "Lightricks/LTX-2.5",
      "issues": [
        "Gemma tokenizer, prompt enhancer and exact runtime closure"
      ]
    },
    {
      "repo_id": "ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8",
      "issues": [
        "Full learned count, Gemma tokenizer and donor conditions"
      ]
    },
    {
      "repo_id": "Stuubs/Stubelius_Remix_Ltx2.5",
      "issues": [
        "Full learned count and official text/VAE backend compatibility"
      ]
    },
    {
      "repo_id": "ibm-granite/granite-switch-4.1-30b",
      "issues": [
        "Decision/Guardian aLoRA and ASR attachment revisions"
      ]
    },
    {
      "repo_id": "openai/gpt-oss-120b",
      "issues": [
        "incomplete shards: model-"
      ]
    },
    {
      "repo_id": "boltz-community/boltz-2",
      "issues": [
        "MSA/reference-data path for completely offline operation"
      ]
    },
    {
      "repo_id": "nvidia/Cosmos-Predict2-2B-Video2World",
      "issues": [
        "Native resolution/fps variant provenance and external preprocessing/safety components"
      ]
    },
    {
      "repo_id": "lerobot/pi0_base",
      "issues": [
        "External tokenizer/processor and robot normalization"
      ]
    },
    {
      "repo_id": "lerobot/smolvla_base",
      "issues": [
        "Backbone tokenizer/processor and embodiment configuration"
      ]
    },
    {
      "repo_id": "microsoft/TRELLIS.2-4B",
      "issues": [
        "External vision encoder, background-removal models, CUDA build assets"
      ]
    },
    {
      "repo_id": "nvidia/GR00T-N1.6-3B",
      "issues": [
        "External processor/tokenizer and embodiment assets"
      ]
    },
    {
      "repo_id": "speridlabs/idol",
      "issues": [
        "Native FLUX AE versus Diffusers VAE interoperability and SDK requirements"
      ]
    },
    {
      "repo_id": "tencent/Hunyuan3D-2.1",
      "issues": [
        "Conditioning encoder and ancillary segmentation/texture tools"
      ]
    },
    {
      "repo_id": "nvidia/Granary-v2",
      "issues": [
        "Per-corpus permitted subset and external source-audio scope"
      ]
    },
    {
      "repo_id": "allenai/pixmo-cap",
      "issues": [
        "External image URLs; captions alone are not requested image+caption package"
      ]
    },
    {
      "repo_id": "facebook/vjepa2-vitg-fpc64-384",
      "issues": [
        "Original checkpoint contents and native inference/conversion code"
      ]
    },
    {
      "repo_id": "tencent/Hy-SimulMT-30B-A3B",
      "issues": [
        "Separately selected speech-output TTS and streaming scaffold"
      ]
    },
    {
      "repo_id": "WhissleAI/steer-tts",
      "issues": [
        "Full learned count and native/Python frontend/encoder compatibility"
      ]
    },
    {
      "repo_id": "maya-research/maya2-native",
      "issues": [
        "kyutai/mimi",
        "speechbrain/spkrec-ecapa-voxceleb"
      ]
    },
    {
      "repo_id": "fishaudio/drama-3",
      "issues": [
        "Full codec-inclusive count and matching SGLang-Omni/vLLM-Omni revision"
      ]
    },
    {
      "repo_id": "ausboss/Qwen-Image-2.1-Consistency-LoRA",
      "issues": [
        "Comfy-Org INT8-convrot versus R21 BF16 adapter mapping and count"
      ]
    }
  ],
  "all_runtime_environment_archives_unmeasured": true,
  "planning_cap_bytes": 4000000000000,
  "minimum_free_bytes": 200000000000,
  "provisional_known_scope_budget_difference_bytes": 1068393228155,
  "difference_is_not_available_headroom": true,
  "physical_disk_capacity_bytes": null,
  "physical_disk_free_bytes": null,
  "local_duplicate_bytes": null,
  "actual_remaining_archive_budget_bytes": null,
  "actual_acquisition_peak_bytes": null,
  "acquisition_scenarios_known_scope_only": {
    "direct_final_volume_atomic_rename_no_retained_cache_payload_bytes": 2931606771845,
    "one_extra_largest_file_copy_payload_upper_scenario_bytes": 2987549701018,
    "retained_full_cache_plus_final_plus_one_staging_file_payload_upper_scenario_bytes": 5919156472863,
    "assumptions": "Empty store, one asset at a time, no retries/residuals, logical bytes only; filesystem allocation, environments and unresolved components excluded. Not a measured maximum."
  },
  "download_authorized": false,
  "executable": false,
  "model_payload_bytes_downloaded": 0,
  "profile_evidence": [
    "catalog/capacity/2026-11-06/source-review.md",
    "manifests/drafts/round21-pinned-preservation.candidate.json",
    "catalog/revisions/v22-2026-11-06.json"
  ]
}
```

## All active assets

| Asset | Primary selected bytes | Package bytes (shared dependencies repeated) | Issues |
|---|---:|---:|---|
| orcarouter/Qwen3.8-27B-Uncensored | 55586066230 | 55586066230 | No additional learned dependency identified in this review; runtime closure NOT certified |
| InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF | 17738327225 | 17738357352 | No additional learned dependency identified in this review; runtime closure NOT certified |
| 0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF | 16560392734 | 16560392734 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2 | 53120711400 | 53120711400 | No additional learned dependency identified in this review; runtime closure NOT certified |
| LiquidAI/LFM2.5-24B-A2B | 47962796250 | 47962796250 | No additional learned dependency identified in this review; runtime closure NOT certified |
| usezn/Galvanize-3 | 597573024 | 597573024 | No additional learned dependency identified in this review; runtime closure NOT certified |
| microsoft/Fara1.5-27B | 54743814229 | 54743814229 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-Coder-Next | 159376351965 | 159376351965 | No additional learned dependency identified in this review; runtime closure NOT certified |
| tencent/Hy-Memory-30B-A3B | 60143172163 | 60143172163 | No additional learned dependency identified in this review; runtime closure NOT certified |
| LiquidAI/LFM3-1.7B | 3475686813 | 3475686813 | No additional learned dependency identified in this review; runtime closure NOT certified |
| KlingTeam/LivePortrait | 658957150 | 658957150 | No additional learned dependency identified in this review; runtime closure NOT certified |
| chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1 | 671173375 | 33802789787 | No additional learned dependency identified in this review; runtime closure NOT certified |
| microsoft/VibeVoice-1.5B | 5408337065 | 5408337065 | Qwen tokenizer and original inference code version |
| OpenMOSS-Team/MOSS-TTS-v1.5 | 16995761910 | 16995761910 | External audio tokenizer checkpoint/version |
| Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice | 2498388392 | 2498388392 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-TTS-12Hz-1.7B-Base | 4544229700 | 4544229700 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign | 4520163832 | 4520163832 | No additional learned dependency identified in this review; runtime closure NOT certified |
| ResembleAI/chatterbox | 3209057119 | 3209057119 | Pinned inference code, Perth watermark assets and text frontend |
| Edge0/Audio8-TTS-Realistic-Air | 2565494726 | 2565494726 | No additional learned dependency identified in this review; runtime closure NOT certified |
| black-forest-labs/flux-3-image-klein-base | 20300554474 | 20300554474 | Prompt upsampler and tokenizer/runtime closure |
| black-forest-labs/FLUX.2-dev | 112823045100 | 112823045100 | No additional learned dependency identified in this review; runtime closure NOT certified |
| briaai/Fibo-2.0-dev | 25479156514 | 25479156514 | VGL preprocessing/prompt expansion dependency closure |
| ideogram-ai/ideogram-4-nf4 | 16106834204 | 16106834204 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Lightricks/LTX-2.5 | 71118789776 | 71118789776 | Gemma tokenizer, prompt enhancer and exact runtime closure |
| ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8 | 36468384300 | 36468384300 | Full learned count, Gemma tokenizer and donor conditions |
| Stuubs/Stubelius_Remix_Ltx2.5 | 21504132027 | 49605080095 | Full learned count and official text/VAE backend compatibility |
| kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers | 26670725000 | 26670725000 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen-Image-2.1 | 33131616412 | 33131616412 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Tongyi-MAI/Z-Image-Turbo | 32864088840 | 32864088840 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Wan-AI/Wan2.2-TI2V-5B | 34201539556 | 34201539556 | No additional learned dependency identified in this review; runtime closure NOT certified |
| StephaneBah/AfroRadVoice-FR | 1040330586 | 1040330586 | No additional learned dependency identified in this review; runtime closure NOT certified |
| CohereLabs/aya-vision-32b | 66296141864 | 66296141864 | No additional learned dependency identified in this review; runtime closure NOT certified |
| meta-llama/Llama-4-Scout-17B-16E | 217315708790 | 217315708790 | No additional learned dependency identified in this review; runtime closure NOT certified |
| allenai/Olmo-3-1125-32B | 64476874755 | 64476874755 | No additional learned dependency identified in this review; runtime closure NOT certified |
| IFM/K2-Horizon-0.9B | 2161772471 | 2161772471 | No additional learned dependency identified in this review; runtime closure NOT certified |
| google/gemma-4-31B | 62578664883 | 62578664883 | No additional learned dependency identified in this review; runtime closure NOT certified |
| ibm-granite/granite-switch-4.1-30b | 59991296229 | 59991296229 | Decision/Guardian aLoRA and ASR attachment revisions |
| LiquidAI/LFM3-Omni-2B | 4499443673 | 4499443673 | No additional learned dependency identified in this review; runtime closure NOT certified |
| mistralai/Mistral-Small-4-119B-2603 | 120960168209 | 120960168209 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Nanbeige/Nanbeige4.3-33B | 66259307131 | 66259307131 | No additional learned dependency identified in this review; runtime closure NOT certified |
| nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB | 6180517517 | 6180517517 | No additional learned dependency identified in this review; runtime closure NOT certified |
| LiquidAI/LFM2.5-VL-3B | 6265014358 | 6265014358 | No additional learned dependency identified in this review; runtime closure NOT certified |
| LiquidAI/LFM2.5-VL-3B-DSpark | 558964083 | 6823978441 | No additional learned dependency identified in this review; runtime closure NOT certified |
| openai/gpt-oss-120b | None | None | incomplete shards: model- |
| Qwen/Qwen3-Omni-30B-A3B-Instruct | 70530595574 | 70530595574 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3.5-35B-A3B-Base | 71926986405 | 71926986405 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3.8-27B | 55586114907 | 55586114907 | No additional learned dependency identified in this review; runtime closure NOT certified |
| udgamlabs/Lilavati | 190656047 | 190656047 | No additional learned dependency identified in this review; runtime closure NOT certified |
| udgamlabs/Lilavati-Checker | 190649144 | 381305191 | No additional learned dependency identified in this review; runtime closure NOT certified |
| EPFLiGHT/Meditron3-70B | 141116879850 | 141116879850 | No additional learned dependency identified in this review; runtime closure NOT certified |
| google/medgemma-4b-it | 8639644263 | 8639644263 | No additional learned dependency identified in this review; runtime closure NOT certified |
| boltz-community/boltz-2 | 6204364262 | 6204364262 | MSA/reference-data path for completely offline operation |
| EPFLiGHT/fully-open-meditron | 511345597 | 511345597 | No additional learned dependency identified in this review; runtime closure NOT certified |
| EPFLiGHT/OLMo-2-32B-MeditronFO | 64477464469 | 64477464469 | No additional learned dependency identified in this review; runtime closure NOT certified |
| facebook/esm2_t33_650M_UR50D | 2609510572 | 2609510572 | No additional learned dependency identified in this review; runtime closure NOT certified |
| HuggingFaceBio/Carbon-X | 29655678789 | 29655678789 | No additional learned dependency identified in this review; runtime closure NOT certified |
| IFM/SFT-Reasoning | 158563572761 | 158563572761 | No additional learned dependency identified in this review; runtime closure NOT certified |
| OctoMed/OctoMed-32B | 66726453842 | 66726453842 | No additional learned dependency identified in this review; runtime closure NOT certified |
| nvidia/Cosmos-Predict2-2B-Video2World | 14661005052 | 14661005052 | Native resolution/fps variant provenance and external preprocessing/safety components |
| lerobot/pi0_base | 14005628513 | 14005628513 | External tokenizer/processor and robot normalization |
| lerobot/smolvla_base | 906731641 | 906731641 | Backbone tokenizer/processor and embodiment configuration |
| microsoft/TRELLIS.2-4B | 16237485044 | 16237485044 | External vision encoder, background-removal models, CUDA build assets |
| nvidia/GR00T-N1.6-3B | 6573788038 | 6573788038 | External processor/tokenizer and embodiment assets |
| speridlabs/idol | 3078990585 | 6777659556 | Native FLUX AE versus Diffusers VAE interoperability and SDK requirements |
| tencent/Hunyuan3D-2.1 | 14909683275 | 14909683275 | Conditioning encoder and ancillary segmentation/texture tools |
| laion/emotional-roleplay-finetuning-dataset | 6667420582 | 6667420582 | No additional learned dependency identified in this review; runtime closure NOT certified |
| m-a-p/MERT-v2-FullSong | 2529878111 | 2529878111 | No additional learned dependency identified in this review; runtime closure NOT certified |
| m-a-p/SheetSage2 | 231081591 | 2760959702 | No additional learned dependency identified in this review; runtime closure NOT certified |
| m-a-p/YuE2-3B | 7264394226 | 7795145244 | No additional learned dependency identified in this review; runtime closure NOT certified |
| m-a-p/YuE2-Vae | 530751018 | 530751018 | No additional learned dependency identified in this review; runtime closure NOT certified |
| nvidia/Granary-v2 | None | None | Per-corpus permitted subset and external source-audio scope |
| nvidia/OpenCodeInstruct | 6861119940 | 6861119940 | No additional learned dependency identified in this review; runtime closure NOT certified |
| nvidia/OpenMathInstruct-2 | 12628474179 | 12628474179 | No additional learned dependency identified in this review; runtime closure NOT certified |
| facebook/dinov3-vit7b16-pretrain-lvd1689m | 26864283632 | 26864283632 | No additional learned dependency identified in this review; runtime closure NOT certified |
| facebook/dinov3-vith16plus-pretrain-lvd1689m | 3362457679 | 3362457679 | No additional learned dependency identified in this review; runtime closure NOT certified |
| facebook/sam3 | 3445031383 | 3445031383 | No additional learned dependency identified in this review; runtime closure NOT certified |
| allenai/pixmo-cap | 1101532176 | 1101532176 | External image URLs; captions alone are not requested image+caption package |
| allenai/tulu-3-sft-mixture | 1412964994 | 1412964994 | No additional learned dependency identified in this review; runtime closure NOT certified |
| answerdotai/ModernBERT-large | 1585710451 | 1585710451 | No additional learned dependency identified in this review; runtime closure NOT certified |
| autogluon/chronos-2 | 477940832 | 477940832 | No additional learned dependency identified in this review; runtime closure NOT certified |
| BAAI/bge-m3 | 2295443588 | 2295443588 | No additional learned dependency identified in this review; runtime closure NOT certified |
| CohereLabs/aya_dataset | 140160376 | 140160376 | No additional learned dependency identified in this review; runtime closure NOT certified |
| deepseek-ai/DeepSeek-OCR-2 | 6789165316 | 6789165316 | No additional learned dependency identified in this review; runtime closure NOT certified |
| elyza/ELYZA-tasks-100 | 7788480 | 7788480 | No additional learned dependency identified in this review; runtime closure NOT certified |
| facebook/vjepa2-vitg-fpc64-384 | 16464857277 | 16464857277 | Original checkpoint contents and native inference/conversion code |
| google/siglip2-base-patch16-224 | 1539458338 | 1539458338 | No additional learned dependency identified in this review; runtime closure NOT certified |
| GSAI-ML/iLLaDA-8B-Base | 16512918618 | 16512918618 | No additional learned dependency identified in this review; runtime closure NOT certified |
| HuggingFaceFW/fineweb-edu | 28518222076 | 28518222076 | No additional learned dependency identified in this review; runtime closure NOT certified |
| HuggingFaceH4/ultrafeedback_binarized | 649980296 | 649980296 | No additional learned dependency identified in this review; runtime closure NOT certified |
| ibm-granite/granite-speech-5.0-2b | 5047717206 | 5047717206 | No additional learned dependency identified in this review; runtime closure NOT certified |
| ibm-granite/granite-speech-5.0-470m-turboctc | 948033277 | 948033277 | No additional learned dependency identified in this review; runtime closure NOT certified |
| lerobot/aloha_sim_insertion_human | 91348537 | 91348537 | No additional learned dependency identified in this review; runtime closure NOT certified |
| lightonai/LightOnOCR-3-0.8B | 1736123523 | 1736123523 | No additional learned dependency identified in this review; runtime closure NOT certified |
| LiquidAI/d1-omni-600M | 2353572356 | 2353572356 | No additional learned dependency identified in this review; runtime closure NOT certified |
| LiquidAI/LFM3-1.7B-Base | 3475641783 | 3475641783 | No additional learned dependency identified in this review; runtime closure NOT certified |
| llm-jp/magpie-sft-v1.0 | 284157816 | 284157816 | No additional learned dependency identified in this review; runtime closure NOT certified |
| openai/whisper-large-v3-turbo | 1622466054 | 1622466054 | No additional learned dependency identified in this review; runtime closure NOT certified |
| PaddlePaddle/PaddleOCR-VL-1.5 | 1930468959 | 1930468959 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-ASR-1.7B | 4703114308 | 4703114308 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-Embedding-0.6B | 1207489041 | 1207489041 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-Reranker-0.6B | 1207488344 | 1207488344 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3-VL-2B-Instruct | 4266648961 | 4266648961 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Qwen/Qwen3.5-0.8B | 1769980465 | 1769980465 | No additional learned dependency identified in this review; runtime closure NOT certified |
| RWKV/RWKV7-7.2B-20260805 | 14402000339 | 14402000339 | No additional learned dependency identified in this review; runtime closure NOT certified |
| tencent/Hy-SimulMT-30B-A3B | 60803459351 | 60803459351 | Separately selected speech-output TTS and streaming scaffold |
| nvidia/Nemotron-Cascade-2-30B-A3B | 63176817785 | 63176817785 | No additional learned dependency identified in this review; runtime closure NOT certified |
| nvidia/Nemotron-Cascade-2-RL-data | 2859999928 | 2859999928 | No additional learned dependency identified in this review; runtime closure NOT certified |
| nvidia/Nemotron-Cascade-2-SFT-Data | 68397032645 | 68397032645 | No additional learned dependency identified in this review; runtime closure NOT certified |
| Hcompany/Holo4-27B | 54736673609 | 54736673609 | No additional learned dependency identified in this review; runtime closure NOT certified |
| WhissleAI/steer-tts | 767336820 | 767336820 | Full learned count and native/Python frontend/encoder compatibility |
| maya-research/maya2-native | 5021124225 | 5021124225 | kyutai/mimi; speechbrain/spkrec-ecapa-voxceleb |
| Hcompany/trajectories | 2741330342 | 2741330342 | No additional learned dependency identified in this review; runtime closure NOT certified |
| DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU | 55589894040 | 55589894040 | No additional learned dependency identified in this review; runtime closure NOT certified |
| fishaudio/drama-3 | 41502571262 | 41502571262 | Full codec-inclusive count and matching SGLang-Omni/vLLM-Omni revision |
| PrentisAI/GroundGUI-8B | 17550250270 | 17550250270 | No additional learned dependency identified in this review; runtime closure NOT certified |
| ausboss/Qwen-Image-2.1-Consistency-LoRA | 159544753 | 33291161165 | Comfy-Org INT8-convrot versus R21 BF16 adapter mapping and count |

## Interpretation

Missing capacity is never zero. All 116 runtime/environment archives remain unmeasured. Exact file bytes do not establish full offline closure or personal access approval.
Difference from the 4TB ceiling is NOT physical free storage or safe headroom. Unknown Granary subset, external images and dependencies must be accounted for before approval.
Same-size weights are not deduplicated. Source-identity reuse assumes a content-addressed layout and later local hash verification. Filesystem allocation and hardlink support are untested.
Format narrowing is not deletion of a local artifact. Historic catalog decisions and approved queue are unchanged. Native checkpoint contents are not assumed redundant solely because another export is smaller.
R21 checksum discrepancies remain in the historical audit. R21 Qwen base is retained for ChatR; Consistency-LoRA interoperability is not proven.
Machine learning checks distinct learned outcomes; software supply chain checks versions/components; digital preservation checks offline restoration. These checks are not interchangeable.

## Next gate

Resolve the enumerated missing dependencies and Granary subset, then run read-only preflight on the actual owner volume. No model download, cloud execution, consent or approval is enabled.
