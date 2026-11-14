# Deep Research follow-up: evidence and catalog integrity audit (2026-11-14)

## Scope and repository state

- Repository: `Unjuno/local-model-portfolio`
- Baseline: `6e9389c97d24528df97e4b14a6bc772780141fd3`
- Active branch observed via GitHub branches API on 2026-11-14: **`main` only** (commit `bb4953a8bac5474108b22d9b12b7eefe5f93bc7c` at check time).
- Historical `strategy/2026-11-03-01-risk` branch no longer resolves. Existing proposal is on `main`: `catalog/proposals/01-regulation-priority.json`.
- This document is an **audit addendum**, not a new authorization to acquire any model or dataset. No download is initiated.

## Corrections to the 2026-11-14 Deep Research narrative

| Claim in research narrative | Audit decision | Reason and required verification |
| --- | --- | --- |
| Sample dataset X represents a portfolio asset | **REJECT** | It is explicitly a hypothetical example, not an asset identifier from the 132-entry catalog. Never count it in coverage or priority totals. |
| Suno hosted-service model retirement is evidence that a corresponding open-weight checkpoint was deleted | **REJECT as direct portfolio evidence** | A hosted proprietary model lifecycle and an open-weight Hub repository have different availability and rights conditions. Verify any claimed date from the provider and do not add Suno to the 132-entry catalog without an actual catalog match. |
| All 132 assets comply with the 150B hard ceiling | **REJECT** | The existing proposal contains a 150B-or-above exclusion gate and unverified parameter counts. Distinguish inventory membership from download eligibility. Any MoE must be evaluated on **total**, not activated, parameters; unknown total remains blocked. |
| A sample P0/P1/P2/P3 pie chart demonstrates the actual 132-asset distribution | **REJECT** | Illustrative percentages are not measured catalog counts. Recompute directly from the versioned JSON before reporting. |
| Model survival-study proportions can be applied as probabilities of disappearance for these 132 assets | **REJECT** | Different cohort, selection and censoring conditions; rename is not identical to deletion. No asset-level probability can be inferred without a calibrated, validated model. |
| AI Act Article 53 implies a general ban on open-weight distribution | **REJECT** | Article 53 establishes provider obligations and conditional exemptions; systemic-risk models are an exception to the open-source exemption. This is not a blanket download ban. |
| US 2025 AI Diffusion Rule proves a currently enforced blanket ban on open weights | **REJECT** | BIS announced non-enforcement and intent to rescind the rule on 2025-05-13; check subsequent official rulemaking for the current legal position. |

## Primary-source research ledger

1. **EU AI Act, Article 53 (law, observed)**: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53 . Distinguish documentation/copyright-policy obligations, free/open-source exemptions, and systemic-risk exceptions.
2. **EU AI Act, Article 93 (law, observed)**: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-93 . Conditional provider-directed corrective measures are not evidence of an order against a particular portfolio checkpoint.
3. **US BIS, May 13 2025 (agency statement, observed historical event)**: https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens . Confirm later operative law separately.
4. **LAION withdrawal/re-release (publisher, observed event)**: https://laion.ai/blog/relaion-5b/ . A dataset withdrawal is evidence of changing availability, not of a universal weight ban.
5. **Stability AI license revision (publisher, observed event)**: https://stability.ai/news-updates/license-update . Licensing can also become less restrictive.
6. **Hugging Face Gated models (platform documentation, observed mechanism)**: https://huggingface.co/docs/hub/models-gated . Gated status and an individual user's approved access are distinct facts.
7. **GEITje author-reported takedown (publisher account, historical case)**: https://goingdutch.ai/en/posts/geitje-takedown/ . Model-specific evidence only.

These links are an evidence ledger, **not** a claim that every endpoint was independently re-fetched on this date. The Exa connector returned **HTTP 402 (credit limit exceeded)** on 2026-11-14, so no new Exa verification was completed in this follow-up.

## Required per-asset decision gate

For every one of the 132 baseline IDs, retain the exact catalog ID and separate:

- **Observed facts**: source URL, checked date, revision/commit, current hosting state, publisher license, gated status, and *actual user authorization* (unknown unless proven).
- **Hypotheses**: three tightening scenarios (capability-specific, broad high-performance, broad open-weight); falsification trigger and uncertainty, without fabricated probabilities.
- **Preservation value**: uniqueness versus actual substitutes, retraining difficulty, provenance, source diversity, storage bytes, dependencies, and legal reproducibility.
- **Hard eligibility**: total parameters <150B for models, including every MoE expert; unknown totals **BLOCK**; >=150B **EXCLUDE**. The presence of an excluded record in an inventory is not a download approval.
- **Acquisition authorization**: explicit rights, source access, exact revision, capacity and checksum; **default DENY** until verified.

Priority must not be treated as permission. Keep the existing proposal's `approved=false` and `download_enabled=false` controls unless the user explicitly approves a separately verified execution plan.

## Validation protocol

**H (falsifiable hypothesis):** All 132 baseline asset identifiers have exactly one proposal record and no excluded/unknown-parameter model is download-approved.

**T (minimum test):** Parse baseline v9 JSON and current proposal JSON, compare identifier multisets (not merely counts), then inspect parameter gate and authorization flags for every matching record. Minimum sample = all 132; stop on any mismatch and mark FAIL.

**D (decision):** PASS only when exact-ID equality, uniqueness, all gates and authorization controls are satisfied; FAIL on any counterexample; UNCERTAIN when source fields or baseline are unavailable.

**C (counter-hypotheses):** Alias drift, renamed repository, untracked duplicate quantization, total-versus-active MoE parameter confusion, stale Gated metadata, or changed license terms.

**U (uncertainty):** Most material unknowns are current publisher revisions, actual gated entitlements, full dependency provenance, and true physical free storage. No combined numeric uncertainty or confidence interval is justified without measurement data.

## Next concrete work

1. Run the exact-ID automated comparison against the **current** `main` proposal and baseline.
2. Review source metadata and license snapshots for P0 assets first, then P1, with date-stamped evidence.
3. Recalculate actual priority distributions from JSON; do not reuse illustrative Deep Research charts.
4. Publish a machine-readable diff only for verified changes. Do not silently change portfolio selection or start downloads.

**Cross-disciplinary dependencies:** AI policy and export controls (legal scope); software supply-chain provenance (revision/license integrity); digital preservation (reproducibility, storage and substitute diversity).

**Question to resolve:** Which scarce model capability is genuinely non-substitutable after checking alternative first-party releases, rather than merely unusual by name?


## 2026-11-14 follow-up: executable-equivalent full inventory comparison

**Method:** Read the complete current `catalog/effective-portfolio-2026-11-03-v9.json` and `catalog/proposals/01-regulation-priority.json` from GitHub `main`, parse both as JSON, compare exact `repo_id` sets and duplicate IDs, count `priority.band` and `parameter_limit.status` for every proposal record, and check `priority.download_approved` and `priority.legally_cleared_for_acquisition` across all 132 records. This is an observed repository-data audit, not an independent upstream model-card validation.

| Integrity / decision check | Measured result | Decision |
| --- | ---: | --- |
| v9 inventory IDs | 132 | baseline |
| proposal IDs | 132 | PASS |
| missing / extra / duplicated IDs | 0 / 0 / 0 | PASS |
| priority P0 / P1 / P2 / P3 / PX | 22 / 59 / 37 / 12 / 2 | PASS; actual JSON, not illustrative percentages |
| model total-parameter PASS (<150B) | 95 | metadata eligibility only |
| model total-parameter UNVERIFIED | 12 | BLOCK |
| model total-parameter EXCLUDED (>=150B) | 2 | EXCLUDE |
| datasets, parameter threshold not applicable | 23 | other rights gates still apply |
| asset-level `download_approved=true` or `legally_cleared_for_acquisition=true` | 0 | PASS |
| proposal-level `approved` / `download_enabled` | false / false | PASS |

**Excluded (do not acquire):** `orcarouter/Qwen3.8-Flash-Next-Uncensored` (180B total recorded); `mistralai/Mistral-Large-4-1T-A52B` (1.05T total recorded). These totals are catalog assertions and were not independently remeasured in this pass.

**Twelve total-parameter verification blockers:**

1. `Plachta/Seed-VC`
2. `InstantX/InstantID`
3. `SWivid/F5-TTS`
4. `coqui/XTTS-v2`
5. `onnx-community/higgs-audio-v3-tts-4b`
6. `ByteDance/InfiniteYou`
7. `fishaudio/fish-speech-1.5`
8. `TencentARC/PhotoMaker`
9. `ACERobotics/Puffin-World`
10. `bytedance-research/Lance`
11. `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`
12. `OnomaAIResearch/Illustrious-XL-v1.1`

**Primary-source recheck, performed through public web search on 2026-11-14:**

- European Commission AI Act Service Desk, Article 53: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53 — provider obligations and conditional open-source exemption; no general prohibition on public model weights is stated.
- European Commission AI Act Service Desk, open-source FAQ: https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source — exemptions do not waive copyright policy/training-data-summary obligations, nor cover systemic-risk GPAI models.
- European Commission AI Act Service Desk, systemic-risk FAQ: https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-general-purpose-ai-model-one-systemic-risk — capability or Commission designation matters; total parameter count is not itself a legal systemic-risk determination.
- US BIS official May 13 2025 statement: https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens — describes announced non-enforcement and planned rescission; **does not independently establish the full current 2026 export-control status**.

**Interpretation:** The hard 150B cutoff is this portfolio's internal acquisition policy, not the EU AI Act systemic-risk threshold. A passing parameter gate is neither a license clearance nor a download authorization. The current catalog has no approved acquisitions.

**H/T/D/C/U result:** H = exact 132-ID equality and no unauthorized flags; T = census of all 132 records; D = PASS for ID/flag integrity, UNCERTAIN for upstream factual freshness; C = stale model cards, hidden MoE experts, dependency parameters, changed hosting/license, or misidentified repo; U = no calibrated numeric uncertainty without upstream validation and physical capacity measurement. No model weights or datasets were downloaded in this audit.
