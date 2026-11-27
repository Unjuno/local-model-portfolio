# R189 / v93: TinyCast computed-period probabilistic forecaster

Parent bdca4b104afb12f7f86caf8c091aaae6d06a6a40. 287登録・231有効（SELECT 56、CONDITIONAL 175）。TinyCast独立学習14.65万パラメータを研究限定CONDITIONAL追加。既存286行・133取得報告不変。配布元候補モデル＋コード3,408,694 B、依存込み・owner増分未確定。全231取得STOP、承認・重みDL・実行・物理削除0。

[Source manifest](../../manifests/drafts/r189-2026-11-28-tinycast-forecast-originals.candidate.json) / [research](../../catalog/research/2026-11-28-tinycast-forecast-primary-evidence.json) / [decision](../../catalog/decisions/2026-11-28-r189-tinycast-formal-add.json) / [overlay](../../catalog/revisions/v93-2026-11-28.json) / [readiness](../../catalog/readiness/v93-2026-11-28-r189-all231-gates.json).

Preserve original compact attention-free learned quantile forecasting using computed periodicity and tied convolutional network; ~35x fewer parameters than selected Timestral-5M, separate low-resource research operating point. Not a quantization of incumbent; no evidence to replace multivariate/covariate forecasters.

Positive: Publisher GIFT-Eval 97 configs nGMASE 0.7738, nWQL/CRPS column 0.5454, nMSIS 0.5541 with BF16 autocast, flip symmetry and period alignment; 146505 unique F32 parameters, attention-free spectral period detection and dilated causal convolution. Paper reports Cortex-M7 INT8 4.08 s, 731 KB RAM; hardware clock/batch and independent replay not verified here.

Negative: TinyCast nGMASE 0.7738 worse than separate Timestral-5M 0.705, Toto-2.0-4m 0.757, Hirondel 0.7003; these are not matched comparisons. Univariate, 2048 context, nine quantiles; default inference does not reproduce table; training distributed launcher absent, no matched host/MCU ABI, clock, RAM or independent evaluation. No claim of superiority.

HOLD Hirondel-7M (31,632,157 B) and Aalborg Chronos-2 (477,936,515 B). KEEP Timestral-5M, Toto-4M, Chronos-2 and CTSM1.5. No matched evidence to remove assets.

Fixed HF 9635a27b66a73fedd6e88120c72c7f91427d216e; code 628c0bec8425240d5f12155add1d1d5bc2d92471; full HF 720,964 B; candidate 613,278 B; 201 code-tree blobs 2,795,416 B; total 3,408,694 B. Publisher source only; dependencies/owner bytes null, act rights and access not verified. No execution, weights fetched, downloads authorized or model files deleted.

Bounded HF latest 100 plus web 7/30/90-day and relevant earlier research. Rebased on concurrent main; latest-version sidecars used even when inherited pointer stale. Prior rows and current active/conditional joins validated. Independent model evaluation not run.
