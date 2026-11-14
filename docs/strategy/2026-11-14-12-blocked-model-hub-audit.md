# 2026-11-14: Twelve blocked-model upstream metadata audit

## Purpose and method

This is a **read-only research addendum** for `Unjuno/local-model-portfolio` on `main`. The current proposal `catalog/proposals/01-regulation-priority.json` flags the following **12** models as `UNVERIFIED_BLOCK_FINAL_LOCK`. On 2026-11-14, each repository ID was looked up using the Hugging Face Hub repository-details connector. Seed-VC and F5-TTS were also cross-checked against public publisher repository pages and the original Seed-VC author GitHub project. These are observations about listing metadata, **not** independent tensor counts, exact commit pins, or license clearances.

**Decision: all 12 remain blocked.** No acquisition, checkpoint download, parameter-gate promotion, or change to the 132-asset proposal was authorized.

| Catalog repo ID | Hub-reported license metadata | Distinct follow-up / unresolved gate |
| --- | --- | --- |
| `Plachta/Seed-VC` | GPL-3.0 | Author source lists several VC/SVC checkpoints with 25M, 98M, 200M, and 67M CFM + 90M AR **component** parameters; external encoders and vocoders, exact checkpoint selection and full dependency totals unresolved. Author GitHub repository archived in 2025, while Hub listing still exists. |
| `InstantX/InstantID` | Apache-2.0 | Adapter/identity modules plus external image-generation backbone; count complete intended dependency graph. |
| `SWivid/F5-TTS` | CC-BY-NC-4.0 | Noncommercial terms; multiple checkpoints and vocoder; confirm exact revision and total dependency scope. |
| `coqui/XTTS-v2` | other | Custom license requires full-text review; total component parameters unresolved. |
| `onnx-community/higgs-audio-v3-tts-4b` | other | ONNX community conversion, base `bosonai/higgs-tts-3-4b`; verify conversion provenance, quantization and total dependency scope, not just “4b” in name. |
| `ByteDance/InfiniteYou` | CC-BY-NC-4.0 | Depends on FLUX.1-dev backbone; do not infer license clearance from adapter license. |
| `fishaudio/fish-speech-1.5` | CC-BY-NC-SA-4.0 | Noncommercial/share-alike terms; full text and dual-AR components unresolved. |
| `TencentARC/PhotoMaker` | Apache-2.0 | Image-ID conditioning components and SD backbone dependency must be scoped. |
| `ACERobotics/Puffin-World` | other | World model and external assets; publisher terms, model total and exact manifest unresolved. |
| `bytedance-research/Lance` | Apache-2.0 | Hub declares Qwen2.5-VL-3B-Instruct base; multimodal generation components and aggregate dependency scope unresolved. |
| `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` | MIT | Multimodal text+vision architecture; count both towers and dependency weights. |
| `OnomaAIResearch/Illustrious-XL-v1.1` | other | Custom terms; exact checkpoint, VAE/text encoders and tensor count unresolved. |

## First-party references

Hub repository pages (listing existence and metadata, not user-specific authorization):

- https://huggingface.co/Plachta/Seed-VC
- https://huggingface.co/InstantX/InstantID
- https://huggingface.co/SWivid/F5-TTS
- https://huggingface.co/coqui/XTTS-v2
- https://huggingface.co/onnx-community/higgs-audio-v3-tts-4b
- https://huggingface.co/ByteDance/InfiniteYou
- https://huggingface.co/fishaudio/fish-speech-1.5
- https://huggingface.co/TencentARC/PhotoMaker
- https://huggingface.co/ACERobotics/Puffin-World
- https://huggingface.co/bytedance-research/Lance
- https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224
- https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.1
- Seed-VC author GitHub repository: https://github.com/Plachtaa/seed-vc
- F5-TTS author GitHub repository: https://github.com/SWivid/F5-TTS

**Important evidence distinction:** A repository being listed publicly does not prove every blob is accessible, that gated approval exists, or that the entire intended checkpoint graph is legally redistributable. A license tag is not a substitute for the governing license text and dependency licenses. Seed-VC source-component counts are **not** a verified aggregate for the archived portfolio asset. “Other” is not a grant of rights.

## Next tests and stopping criteria

**H:** Each of the 12 blocked records can eventually be resolved into a fixed exact revision, complete dependency graph, total tensor count, and verified rights scope without crossing the hard 150B threshold.

**T:** For each ID, retrieve first-party model card and revision-specific file manifest, identify the exact intended artifact, list all required trained dependencies, inspect tensor headers or authoritative model configuration without downloading full weights, and read the applicable license text. Verify each of the 12 individually; stop a record on any missing dependency or ambiguous rights condition.

**D:** PASS for a record only if complete intended model total is confirmed <150B **and** source/rights/dependency/capacity checks pass. FAIL for >=150B. UNCERTAIN/BLOCK for unknown total or rights. No pass is an automatic download approval.

**C:** Adapter-only parameter counts misreported as full models, model-name size mistaken for aggregate parameters, inactive MoE experts excluded, publisher licensing mismatched with base-model licensing, or stale repository revisions.

**U:** No numerical confidence or combined uncertainty is defensible before tensor and dependency inventories exist. Dominant errors are incomplete checkpoint scope, third-party dependencies, ambiguous custom terms, and mutable Hub metadata.

**Disciplines:** digital preservation (reproducible manifests), software supply-chain engineering (revision and license provenance), and ML systems (total-parameter accounting and dependency graphs).

**Question:** For an adapter-dependent asset, should preservation scope include only the unique adapter plus a separately preserved, legally licensed base, or a complete independent checkpoint? Answer requires a reproducibility and rights comparison, not just file-size optimization.
