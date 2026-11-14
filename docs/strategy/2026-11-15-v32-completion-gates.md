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

## 2026-11-15 R70/R71: reconcile every active asset and resolve the RFD4 source-commit discrepancy

**Machine-readable evidence:** [R70 135-ID source-evidence join](../../catalog/research/2026-11-15-r70-v32-all135-source-evidence-reconciliation.json), [R71 seven-file RFD4 publisher identity check](../../catalog/research/2026-11-15-r71-rfd4-revision-file-identity.json). The offline standard-library validator [`scripts/validate_v32_source_evidence.py`](../../scripts/validate_v32_source_evidence.py) also checks the R71 identity comparison and R64 internal content references. **Its successful execution on the owner's full repository was not observed here; the source joins and arithmetic were independently checked during research.**

### Verified scope coverage, not final lock coverage

All **135 active IDs** are accounted for as 126 retained v27 assets with historical primary-source scope audits, eight post-v27 assets with R64 fixed candidate file lists, and one ZONOS3-Mini asset with the R48 pinned **reference** profile. This closes the *source-evidence discovery coverage* gap, not the rights/runtime/final-revision gap. The 126 older scopes must still be reconciled to v32 exact selected-file choices. In the canonical catalog, 133 selected-byte fields and 133 final-revision fields remain null.

R64 has **9 publisher repositories, 91 source-file references, 38,519,866,446 bytes**. Their exact SHA256/Git-blob identities show four repeated non-LFS source references (two matching `.gitattributes` files and matching ACE Step vocabulary/merge support pairs), totaling **4,451,775 repeated bytes**; consequently the R64 internal source identity union is **38,515,414,671 bytes**. This is *not* a cross-revision deduplicated portfolio total. It makes no claim about the physical disk or SHA of material not in the manifest.

### RFD4-Proteina revision comparison: critical primary-source correction

The canonical v32 **observed** SHA is `cf31b93509df5af854c7f6ad704f5c83c77c0698`; the R64 candidate source revision is `a06e2509c7033b010fc43614e9fd840303588502`. First-party, immutable [old API file tree](https://huggingface.co/api/models/nvidia/RFD4-Proteina/tree/cf31b93509df5af854c7f6ad704f5c83c77c0698?recursive=false) and [candidate API file tree](https://huggingface.co/api/models/nvidia/RFD4-Proteina/tree/a06e2509c7033b010fc43614e9fd840303588502?recursive=false) were compared for **all seven R64 selected files**.

| Selected file class | Exact file-OID comparison | Consequence |
| --- | --- | --- |
| `model.safetensors` | **Identical**, LFS SHA256 `5b549dd61adb2f6c6b5cb95bda13f40f5e31556b4e6c755edc0ca6f011c68fb0`, 1,742,660,596 B in both | Do **not** re-archive this trained root model twice |
| `config.json` and `LICENSE` | Identical Git blob OIDs and bytes | Reuse identical files by immutable identity |
| `README.md`, `inference.yaml`, `provenance.json`, `release-checkpoints.json` | Four different Git blob OIDs | Retain the chosen commit's matching support metadata; distinguish code/inference compatibility |
| Seven-file source subset total | Old: **1,742,695,830 B**; candidate: **1,742,698,063 B** | 2,233 B net difference, **not** a weight-model change |

**Version-trap:** The [old release-checkpoints.json](https://huggingface.co/nvidia/RFD4-Proteina/blob/cf31b93509df5af854c7f6ad704f5c83c77c0698/release-checkpoints.json) claims the prior bundle SHA `5f00cdcd...` and 435,622,721 stored parameters. Nevertheless the **actual old-commit root weight file** already has SHA `5b549dd6...`, and the [newer release-checkpoints.json](https://huggingface.co/nvidia/RFD4-Proteina/blob/a06e2509c7033b010fc43614e9fd840303588502/release-checkpoints.json) accurately records this with 435,622,465 stored parameters. **This is stale indirect publisher metadata at the older commit, not evidence that the selected root checkpoint changed between the two specified commits.** Extra `base/` and `adapter/` components appear at the candidate revision and are outside the selected seven-file subset; do not imply their training states are identical or already archived.

R71 therefore resolves the **main-weight identity question** but *does not approve* either revision as the complete legally reproducible archive. The owner still needs a deliberate pinned source choice, full compatible component/runtime selection, full rights review and physical-file verification.

### Source-byte scenario, not disk availability

The historical v27 SHA-aware union plus R64's **internally** deduplicated references plus ZONOS's reference profile sum to **3,467,277,687,891 B** (still not globally deduplicated and not a complete offline runtime). The nominal empty-4TB/200GB-floor arithmetic difference is **332,722,312,109 B**, excluding unknown external learned components, runtime packages, staging/cache, existing files and physical HDD measurements. This number is **neither certified available disk capacity nor a safe acquisition budget**.

### Variable table and dimensional check

| Symbol | Meaning (Japanese) | SI unit | Definition | Domain / assumption | Type |
| --- | --- | --- | --- | --- | --- |
| `B27` | v27既知ソースのSHA-aware容量 | byte | 3,417,685,712,585 | 過去126資産の監査範囲のみ | 非負整数スカラー |
| `BR64` | R64のファイル参照容量 | byte | 38,519,866,446 | 9repo・91ファイル、重複含む | 非負整数スカラー |
| `DR64` | R64内のSHA/Git重複容量 | byte | 4,451,775 | R64内で証拠が一致する4参照 | 非負整数スカラー |
| `BZ` | ZONOS固定リファレンスの容量 | byte | 11,076,560,635 | 必須最小構成である証明なし | 非負整数スカラー |
| `BC` | 計画容量上限 | byte | 4,000,000,000,000 | 実ドライブの測定値ではない | 非負整数スカラー |
| `BF` | 空き容量の最低床 | byte | 200,000,000,000 | 実測未知 | 非負整数スカラー |

The arithmetic-only source scenario is `B27 + BR64 - DR64 + BZ`; dimensions are byte + byte − byte + byte = byte. Its difference from the nominal safe empty-drive ceiling `BC - BF` is also in bytes. No comparison against parameter count or actual physical free space is inferred.

### H/T/D/C/U and ERROR CHECK

**H:** The two RFD4 commits have equal selected main-model bytes and SHA, but differ in support-file identities. **T:** 7/7 selected paths checked against two immutable publisher trees, 91/91 R64 references checked for duplicate SHA/Git identities, 135/135 selected asset IDs joined. **D:** PASS for RFD4 root model equality, SHA/size metadata and the 135-source coverage; FAIL/UNCERTAIN for a fully runnable lawful archive. **C:** Older release metadata was stale even while actual root weights had changed to newer payload; other optional components may have distinct training states. **U:** Publisher file metadata is not owner-local SHA verification, and runtime/rightsclearance/disk measurements remain unknown. No measured distribution supports `u_c` or `k`.

**ERROR CHECK:** selected files compared=7; identical=3, changed support=4, net size delta=2,233 B. R64 file references=91, duplicate references=4, duplicate bytes=4,451,775. v32 active=135, approved download=0. No model payloads or datasets were downloaded.

**Interdisciplinary links:** ML tensor provenance; software supply-chain commit and blob identity; long-term digital archiving and content-addressed deduplication; license and authorization governance.

**Next question:** Should the archive preserve the older RFD4 README/inference recipe as historical documentation alongside the newer selected seven-file source set, while storing the main trained weight file only once? The hashes support this as a research option; rights and runtime verification remain independent.

## 2026-11-15 R72/R73: source-file byte provenance bridge and nine historical revision reconciliations

New machine-readable proof: [R72 all 135 asset-level source-byte bridge](../../catalog/research/2026-11-15-r72-v32-active135-selected-source-byte-bridge.json); [R73 all nine historical/current source revision differences](../../catalog/research/2026-11-15-r73-nine-v27-v32-revision-payload-identity.json). Offline **manual** standard-library validator: [`scripts/validate_v32_selected_source_bridge.py`](../../scripts/validate_v32_selected_source_bridge.py). Python validator execution on the full user repository was **not performed** here; the same numeric invariants and 135-ID coverage were checked while compiling the GitHub artifact. No extra GitHub Actions trigger was enabled.

### Essential correction: full repository sizes are not chosen file sizes

The **v27 capacity file ledger was independently re-read in full** (21,383,329 characters in the API response). All 126 historical selected assets have an explicit list of their chosen files; **59,938 named file references**, each carrying a Git blob SHA1 and 50,314 also carrying a publisher SHA256 field. These references are not owner-local checksum attestations. The ledger also flags 762 masked/unknown payload identity occurrences, which cannot be silently marked verified.

| Historical v27 / 126 retained active IDs | Value | What this actually means |
| --- | ---: | --- |
| `source_scope_bytes` summed | 6,399,135,485,511 B | Wider publisher repository scopes, **not selected payload** |
| Sum of `primary_file_bytes` | **3,413,612,735,064 B** | Exactly the sum of the explicitly named selected file references |
| Parent-inclusive `package_bytes` sum | 3,569,207,077,684 B | Parent references and alternative package context; **not** final physical bytes |
| Assets where source scope differs from selected bytes | **66 / 126** | A 6.399TB full-repo plan would be incorrect |
| Broad scope less exact selected files | 2,985,522,750,447 B | Difference between unlike source scopes, **not a physically verified space saving** |

Example: `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` has historical `source_scope_bytes=1,645,270,647,302`, while its selected `primary_file_bytes=16,560,392,734`; do **not** archive all redundant quantizations and GSQ shard variants just because they exist upstream.

### Nine v27→v32 revision SHA mismatches now have publisher file-level evidence

Nine differences in observed Git commit SHAs were checked using the official Hugging Face immutable [repository-tree API](https://huggingface.co/docs/hub/api). Each previously selected file path was compared at the two revisions, checking its publisher Git blob OID and byte size; the historical file metadata also matched the old publisher tree.

| Evidence | Actual result |
| --- | ---: |
| Repositories with different commit IDs | 9 |
| Historical selected files compared | **233** |
| Selected trained weight blobs found changed | **0** |
| Selected files with unchanged identities | 221 |
| Support/configuration files changed, still present | 8 |
| Old evaluation YAML no longer at new revision | 4 |
| Old-publisher source file metadata disagreements | 0 |

Of the eight changed support files, seven are README files and one is `ibm-granite/granite-speech-5.0-2b/tokenizer_config.json`. The four absent evaluation files are `.eval_results/*.yaml` in `LiquidAI/LFM2.5-24B-A2B`; they are not trained weights. **The nine model-weight payloads can be treated as identical for the previously selected file sets, but full inference equivalence is NOT established**, especially where tokenizer configuration changed. The R73 record includes exact commit IDs, official immutable API URLs, named changed files and relevant old/new Git blob IDs. Any newly added, previously unselected model variant is outside this nine-repo comparison.

The historical 126 v27 records join the current v32 inventory as **85 matching observed revisions, 32 current catalog observed-revision blanks, and nine source-commit differences with unchanged selected weight blobs**. The blanks are missing *catalog linkage*, not proof that the publisher source was unavailable.

### Nine post-v27 assets, exact known source scopes versus final rights

The eight R64 asset-specific pinned candidate source profiles total **33,219,541,806 B**. R64 also references `ACE-Step/Ace-Step1.5` as a **distinct external dependency source** of 5,300,324,640 B; it is not a tenth new selected asset. The ninth new active asset `Zyphra/ZONOS3-Mini` has a 14-file native **reference** profile of 11,076,560,635 B, not a proven minimal, fully licensed or reproducible final configuration.

Adding the v27 historical primary selected files plus the eight R64 active candidates and the ZONOS reference gives **3,457,908,837,505 B** as a **source-file arithmetic scenario**. Adding only the specifically R64-listed external ACE dependency gives 3,463,209,162,145 B, still with other unknown dependencies. The separate R70/R71 source union scenario counts different kinds of historically deduplicated/source and dependent bytes; **do not add those two scenarios or treat either as owner disk free space**.

### Variables and dimensional check

| Symbol | Meaning (日本語) | SI unit | Definition | Domain / premise | Type |
| --- | --- | --- | --- | --- | --- |
| `P_{old}` | v27の選定一次ファイル容量 | byte | 3,413,612,735,064 | 履歴上の選定126件、許諾未完了 | 非負整数スカラー |
| `P_{R64}` | R64の新規8資産の選定ソース容量 | byte | 33,219,541,806 | 外部ACE共有repoは別勘定 | 非負整数スカラー |
| `P_Z` | ZONOS固定参考構成の容量 | byte | 11,076,560,635 | 最小実行集合を未証明 | 非負整数スカラー |
| `P_A` | ACE共有外部ソースの容量 | byte | 5,300,324,640 | 他の依存と重複の可能性 | 非負整数スカラー |
| `C` | 名目保存上限 | byte | 4,000,000,000,000 | 実HDD容量を未測定 | 非負整数スカラー |
| `F` | 必須空き容量の下限 | byte | 200,000,000,000 | 物理実測が必要 | 非負整数スカラー |

**Derivation:** Historical selected files `P_{old}` + eight new asset source profiles `P_{R64}` + ZONOS reference `P_Z` = 3,457,908,837,505 byte. A hypothetical empty, **truly 4,000,000,000,000-byte usable drive** would have the arithmetic difference `C - F - P_{old} - P_{R64} - P_Z = 342,091,162,495 byte`. This **is not measured free space**, a guaranteed maximum additional model budget, nor proof of archive fit because actual learned dependencies, runtime, staging, cache and disk occupancy are unknown. All terms and the result have byte dimension; model-parameter counts are dimensionless and cannot be substituted for byte counts.

### Completion conditions / falsification / errors

**H:** Source evidence for each of the 135 active IDs can be linked to a historical or pinned candidate file scope; all nine historical Git SHA differences can be resolved as no change to previously selected trained weight content.  
**T:** Census of 135 active IDs, 126 v27 exact selected-file source profiles and nine new selected IDs; immutable two-revision comparison for the 233 paths across the nine mismatched older repos; stop if any old file OID or byte mismatches the publisher's historical snapshot.  
**D:** PASS for source *evidence linking* and zero changed selected weight blobs in the nine checked pairs; **UNCERTAIN** for final file manifest, full rights, selected dependencies, runtime and physical space; zero acquisition approvals.  
**C:** Newer revisions may introduce optional learned components or alter inference configuration; a prior file set need not be the newly selected optimal file set. A Git blob SHA alone does not attest to a locally stored large weight.  
**U:** Time-varying Hub terms, missing local SHA measurements, implicit trained components, restricted individual Gated permissions and staging peak are dominant sources; no calibrated `u_c` and coverage factor `k` can be computed.

**ERROR CHECK:** 182 tracked; 135 active; 126 old+8 R64+1 ZONOS=135; 59,938 historical file references; 233 selected cross-revision checks; 0 changed selected trained-weight blobs in the nine pairs; v32 final selected bytes still absent 133, final revision absent 133; 0 downloads, 0 new approvals.

**Next question:** The historical SHA matches can remove nine *weight-identity* uncertainties, but the practical next bottleneck is **32 missing canonical revision links, 133 unfinished final manifests and unreviewed runtime/licensing**. Which externally required trained dependencies can be proven identical to already selected weights by SHA, rather than archived twice?
