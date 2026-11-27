# R188 / v92 — MatrixFormer numerical matrix completion

2026-11-28 JST. New primary-source [research and adjudication](../../catalog/research/2026-11-28-matrixformer-tabular-specialists-primary-evidence.json) committed previously in 7456f9f4337c617d24ef8cfea59879bdbf91cdf2. Formal ADD / research-only CONDITIONAL Tabimpute/MatrixFormer; all 285 prior rows preserved including concurrent selections; 286 tracked / 230 active / 174 conditional, all STOP. 133 historical ledger reports unchanged; no new approval, payload, execution or deletion.

Independently trained numerical matrix completion (masked entries across rows and columns, no per-table task labels required); Kumo Tabular predicts designated supervised targets, Kumo Relational consumes relational graphs, Kumo Anomaly is temporal anomaly reconstruction. Keep these non-equivalent assets. Publisher release reports continuation on 250k synthetic matrices / 62,500 updates; save one original state, not two serialization formats.

Fixed release card: MissBench NRMSE 1.256252 (2,091 cases); UCI 1.285373 (3,058 cases), scaled by held-out true column SD. Author reports 77,998,496 trainable parameters, 254 tensors; HF safetensors reports 77,998,688 stored elements. No independent reproduction.

Checkpoint selection used prior MissBench/UCI monitoring; not pristine holdouts. Observed-column-SD NRMSE 4.000035 / 1.045013 differs from held-out-truth scaling. No verified matched Kumo comparison, calibrated uncertainty, or complete-row/column missingness robustness. Synthetic distribution transfer, large-window memory, data rights and runtime unverified. Paper/project-page claims are not automatically attributable to this exact checkpoint.

Five model source files 312,108,648 B; 26 code/reconstruction source blobs 218,310 B; combined 312,326,958 B. Full model repository 624,134,936 B. Alternative serialization 312,026,288 B excluded; publisher reports equal tensors. No physical storage or full dependencies measured. Exact official loader and borders trust unresolved. See [manifest](../../manifests/drafts/r188-2026-11-28-matrixformer-source.candidate.json) and [decision](../../catalog/decisions/2026-11-28-r188-matrix-completion-decisions.json). Source metadata, all comparison outcomes, limitations, license and prospective test plan preserved in the primary research record. No replacement of Kumo Tabular/Relational/Anomaly, Chronos or Toto. No acquisition authority.

Parent 7456f9f4337c617d24ef8cfea59879bdbf91cdf2. All prior main selections and gates carried forward; no force update.
