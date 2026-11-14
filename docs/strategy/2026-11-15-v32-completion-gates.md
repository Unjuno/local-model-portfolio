# v32 portfolio completion gate — 2026-11-15

**Repository:** Unjuno/local-model-portfolio; **canonical revision:** `catalog/CURRENT.json` → `v32-20261114` → `catalog/effective-portfolio-2026-11-14-v32.json`.

## Executive decision

**Research selection catalog: PRESENT AND INTERNALLY CONSISTENT. Acquisition-ready offline archive: NOT COMPLETE.** Do not describe this portfolio as fully reproducible or download-approved.

This report supersedes v9-only 132-record conclusions **for current operational planning**. The older regulation-risk proposal remains a valid historical v9-specific research artifact, not a replacement for v32.

## Exact census of current v32, read from GitHub main

| Check | Measured result | Interpretation |
| --- | ---: | --- |
| Unique inventory records | 182 / 182; no duplicate `asset_kind:repo_id` | PASS |
| Active (`select` or `conditional`) | 135 | Research selection, not download approval |
| `select` / `conditional` | 53 / 82 | PASS against CURRENT expected |
| `hold` / `deferred` / `excluded` | 28 / 13 / 6 | PASS against CURRENT expected |
| Models / datasets | 156 / 26 | PASS |
| Total-parameter PASS below baseline | 134 | Does not imply complete dependency or rights verification |
| Total-parameter UNVERIFIED | 20 | BLOCK |
| Over-150B quantized exception review | 2 | HOLD, no measured matched-runtime exception |
| Active assets without exact `selected_file_bytes` | 133 / 135 | BLOCK acquisition manifest |
| Active assets without `fully_pinned_revision_sha` | 133 / 135 | BLOCK reproducibility |
| Active assets with `license_text_reviewed=false` | 132 / 135 | BLOCK rights approval |
| Active assets with `dependencies_reviewed=false` | 133 / 135 | BLOCK complete offline reproduction |
| `download_approved=true` anywhere | 0 / 182 | No downloads authorized |

**Important:** The current v32 policy explicitly allows research into >=150B quantized exceptions only after matched measured peak RAM against a smaller reference on the same hardware/backend/context/batch, quality/speed, legal rights and explicit approval. The two >150B assets are HOLD, not active. Do not silently revert v32 to v9's absolute ban or treat an exception as pre-approved.

### The 20 parameter-gate blockers (exact current v32 IDs)

`InstantX/InstantID`, `Plachta/Seed-VC`, `SWivid/F5-TTS`, `ByteDance/InfiniteYou`, `coqui/XTTS-v2`, `fishaudio/fish-speech-1.5`, `onnx-community/higgs-audio-v3-tts-4b`, `TencentARC/PhotoMaker`, `bytedance-research/Lance`, `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`, `Stuubs/Stubelius_Remix_Ltx2.5`, `OnomaAIResearch/Illustrious-XL-v1.1`, `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`, `ACERobotics/Puffin-World`, `WhissleAI/steer-tts`, `maya-research/maya2-native`, `Louis0324/StyleStream`, `fishaudio/drama-3`, `ausboss/Qwen-Image-2.1-Consistency-LoRA`, `PrunaAI/P-H3-Image`.

Of these, **7 are marked conditional despite the total parameter gate remaining UNVERIFIED**. These are research-only and must never enter the approved download queue until resolved.

### Two over-baseline review holds

`orcarouter/Qwen3.8-Flash-Next-Uncensored` and `mistralai/Mistral-Large-4-1T-A52B`. Both have `portfolio_decision=hold`; no performance exception has been measured and accepted.

## Completion roadmap, non-compensatory

**Gate A — portfolio integrity: PASS.** Preserve 182 unique identities and expected counts; reject a new overlay that changes selection without explicit provenance and conflict checks.

**Gate B — trained weights and complete inference dependency manifest: FAIL/INCOMPLETE.** For 133 active records, exact selected-file bytes and immutable revision pins are absent; 133 active dependencies have not been fully reviewed. Do not mistake whole-repository displayed size for selected-file size, and do not sum all alternative variants as one required inference pipeline.

**Gate C — rights and access: FAIL/INCOMPLETE.** 132 active records have not had full license text reviewed. Hub license metadata and public listing are insufficient; include every external base/codec/encoder and individual Gated approval. Model-card metadata disagreement must be reconciled against the same pinned README before inferring a license change.

**Gate D — actual storage capacity: UNCERTAIN.** Policy is 4,000,000,000,000 bytes with 200,000,000,000 bytes minimum free floor; physical filesystem formatted total, free bytes, existing archive content and staging peak have not been verified. No full portfolio fit claim is justified.

**Gate E — runtime feasibility: UNCERTAIN.** Quantized exceptions require measured RAM on fixed hardware, backend, version, context length, batch and quality task, with comparison to a <150B reference. No such evidence is currently approved.

**Gate F — acquisition: BLOCK.** Zero approved assets. The research priority order does not grant rights or authorize any network transfer.

## CI decision, based on repository configuration

On 2026-11-15, 24 GitHub Actions workflow YAML files were observed. Two automatically-triggered workflows were modified to `workflow_dispatch` only: `audit-parameter-cap.yml` and `pruna-header-only-census.yml`. Most other legacy workflows target the no-longer-listed `strategy/2026-11-03-01-risk` branch and some contain write-permission and git-push steps. **Do not enable old apply workflows on main.** Their archival presence does not mean they are safe or useful to run. Prefer retaining offline Python audit scripts and a minimal manually-invoked, read-only integrity check; never automate selection commits or downloads.

## Verification protocol

**H:** The current v32 research catalog has exactly 182 unique IDs, 135 active selections, zero approved downloads, and all unresolved parameter/rights/file-manifest gates remain blocking.

**T:** Full census of all 182 `items` in the GitHub `main` effective v32 JSON; compare `CURRENT.expected`; count missing `selected_file_bytes`, `fully_pinned_revision_sha`, license and dependency reviews among the 135 active. Minimum sample: 182/182; no random sampling.

**D:** PASS for ID/count consistency and no accidental approvals; FAIL for acquisition readiness; UNCERTAIN for external metadata freshness, measured hardware performance and physical free disk space.

**C:** Potential hidden problems include stale repository metadata, missing external learned dependencies, misleading quantization size, duplicate files under different names, incorrect user rights assumptions and obsolete CI write jobs.

**U:** This is a deterministic file census, not a statistical estimate. Main uncertainties are incomplete source manifests and license evidence; no meaningful numerical combined uncertainty or confidence interval exists yet.

**Cross-disciplinary relevance:** machine learning systems (dependency and parameter census), software supply-chain security (immutable revisions and checksums), digital preservation (long-term reproducibility and deduplication), law (license/access), and storage engineering (peak capacity and staging).

**Next question:** Which of the 133 active missing manifests can be resolved first using exact publisher file trees without acquiring any weights, and which must remain held because rights or dependencies cannot be verified?

**No model or dataset payload was downloaded in this audit.**
