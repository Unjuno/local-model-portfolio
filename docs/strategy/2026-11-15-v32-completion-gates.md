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


## R70–R71 latest evidence integration — 2026-11-15

### Source-evidence coverage is now *mapped* for 135/135, not acquisition-ready

[Deterministic R70 join](../../catalog/research/2026-11-15-r70-v32-all135-source-evidence-reconciliation.json) matches the 126 active identities surviving from v27 with the **nine** new v28–v32 active identities: eight official-source R64 candidate scopes plus one R48 ZONOS3-Mini reference profile. The historical 126 coverage is grounded in [v27's source-capacity summary](../../catalog/capacity/2026-11-07/v27/capacity-summary.json), not freshly re-verified as a 2026-11-15 owner-side byte-identical acquisition manifest.

| Evidence category | Current active identities | Evidence quality |
| --- | ---: | --- |
| v27 historical selected-source scope | 126 | Historical publisher source census, revalidation required |
| R64 pinned source candidate, 9 source repositories / 91 files | 8 | Exact publisher revision/file bytes/digests; one external ACE-Step repository included in nine |
| R48 ZONOS3-Mini native keep2 reference profile, 14 files | 1 | Fixed research subset, **not proven minimal or runnable** |
| No source evidence found | 0 | Source-evidence join coverage only |
| Canonical final revision **still missing** | 133 | Separate hard gate |
| Canonical selected-file byte total **still missing** | 133 | Separate hard gate |
| Fully licensed, local-SHA verified and approved model archive | 0 | No model downloads authorized |

[Offline-only source-evidence validator](../../scripts/validate_v32_source_evidence.py) checks exact join coverage, hash shapes, file byte arithmetic, RFD4 version relation, scope counts, and zero approvals. It does **not** run automatically in GitHub Actions and was not executed against an owner HDD during this research turn. The cross-file join itself was computed and checked against GitHub JSON sources, including 91 R64 file references.

### Updated nominal 4TB *source-only* arithmetic, not an actual free-space statement

| Term | Decimal bytes | Evidence |
| --- | ---: | --- |
| Historical v27 SHA-aware union | 3,417,685,712,585 | v27 source summary |
| R64 eight assets + ACE-Step external source, 9 repo raw reference sum | 38,519,866,446 | Publisher-pinned R64 candidate; possible overlaps |
| ZONOS3-Mini fixed keep2 reference selection | 11,076,560,635 | Publisher-pinned R48 profile; incomplete runtime |
| **Illustrative source-reference sum** | **3,467,282,139,666** | Addition across three cohorts, without cross-cohort deduplication |
| Hypothetical empty 4TB disk, retaining 200GB free, arithmetic difference | **332,717,860,334** | Not owner-measured free disk |

This sum **is neither a final minimum nor a final upper bound**. Cross-cohort duplicate hashes could decrease unique bytes, whereas external codecs, trained dependents, exact runtime environments, cache/staging and existing owner files can increase actual disk needs. Alternative model variants must not be double-counted as mandatory inference components. The 4TB figure is a policy capacity ceiling, not a measurement of formatted usable bytes.

**Variables and dimensional check**

| Symbol | Japanese meaning | SI unit | Definition, range, assumptions | Type |
| --- | --- | --- | --- | --- |
| `V` | v27の過去ソース容量 | byte | 3,417,685,712,585; SHA-aware union | nonnegative integer scalar |
| `R` | R64の公開ソース参照和 | byte | 38,519,866,446; nine repos, duplicates possible | nonnegative integer scalar |
| `Z` | ZONOS3-Mini参考構成容量 | byte | 11,076,560,635; nonminimal profile | nonnegative integer scalar |
| `S` | 3コホートの算術ソース合計 | byte | `S=V+R+Z`; NOT a finalized archive | nonnegative integer scalar |
| `C` | nominal保存計画上限 | byte | 4,000,000,000,000; actual disk unmeasured | nonnegative integer scalar |
| `F` | 最小空き容量の方針値 | byte | 200,000,000,000 | nonnegative integer scalar |
| `D` | 仮想空ドライブ上の算術差 | byte | `D=C-F-S`; 332,717,860,334; not actual free space | signed integer scalar |

**Unit check:** `V`, `R`, `Z`, `S`, `C`, `F`, and `D` are all byte quantities, so addition/subtraction is dimensionally valid. Parameter counts and inference RAM are separate measurements.

### R71 resolved the RFD4 *main weight* ambiguity but not runtime equivalence

Official [old-revision API](https://huggingface.co/api/models/nvidia/RFD4-Proteina/revision/cf31b93509df5af854c7f6ad704f5c83c77c0698?blobs=true) and [R64 candidate-revision API](https://huggingface.co/api/models/nvidia/RFD4-Proteina/revision/a06e2509c7033b010fc43614e9fd840303588502?blobs=true) were compared for **all seven R64 selected paths**. The `model.safetensors` main weight is identical at **1,742,660,596 bytes** and the same publisher SHA256 `5b549dd61adb2f6c6b5cb95bda13f40f5e31556b4e6c755edc0ca6f011c68fb0`. `LICENSE` and `config.json` also match by Git blob SHA1. Four other files (`README.md`, `inference.yaml`, `provenance.json`, `release-checkpoints.json`) differ.

**Decision:** Preserve a single unique content object for the main weight *if later lawfully acquired and locally hash-verified*, but retain distinct source revisions and their differing support documents. Model-specific rights, environment and use-case reproducibility remain BLOCK/UNCERTAIN. [R71 complete comparison JSON](../../catalog/research/2026-11-15-r71-rfd4-two-revision-source-diff.json).

### H/T/D/C/U and self-check

**H:** Every current v32 active ID has a traceable historical or pinned candidate source-scope evidence reference; a difference between repository revisions does not necessarily imply different trained weights.

**T:** Compare all 135 active IDs with v27 126 scope IDs, R64 8 active IDs / 9 source repos and ZONOS 1 reference profile. Independently compare RFD4's two source revisions on seven exact selected paths, n_min=135 assets and seven path comparisons.

**D:** SOURCE_EVIDENCE_COVERAGE=PASS (126+8+1=135); RFD4_MAIN_WEIGHT_DIGEST=PASS; RFD4_ALL_SELECTED_PATHS_IDENTICAL=FAIL (3 identical, 4 differing); ACQUISITION_READY=FAIL/UNCERTAIN with 0 approvals.

**C:** Contrary outcomes would result from stale publisher metadata, misidentified dependency repo, altered raw checkpoint, hidden learned codecs, or a license/access mismatch that blocks lawful acquisition.

**U:** Numeric combined `u_c` and coverage factor `k` are not estimable because underlying legal permissions, owner filesystem capacity, runtime dependencies and local physical hashes remain unmeasured; no fabricated risk probability.

**ERROR CHECK:** Current inventory 182, active 135, source-evidence cohorts 126/8/1, one R64 extra external repo, RFD4 7 selected paths=3 identical+4 changed, canonical final pins missing 133, approvals 0. **No source-weight download or local file validation performed.**
