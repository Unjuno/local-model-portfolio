# R192 / v96: independent symbolic regression

2026-11-28 JST; parent d776ac7f5ebf19640624f560b701b31be90c420c. ADD davidotte/RASR-94M-S research-only CONDITIONAL, 289 prior rows preserved. No approval, model download, execution or deletion.

Bounded 7/30/90-day search; no sufficiently verified seven-day weight release, 30-day card activity not exact dates; October papers within 90 days. Full HF tree and connector search unavailable. Sources:
- https://huggingface.co/davidotte/RASR-94M-S
- https://huggingface.co/davidotte/RASR-94M-S/commit/b764ebf857a20509de7ba86fa0dc90757b89f3e7
- https://huggingface.co/davidotte/RASR-94M-S/blob/b764ebf857a20509de7ba86fa0dc90757b89f3e7/model.safetensors
- https://arxiv.org/abs/2610.17994
- https://github.com/automl/rasr/tree/f7bdf878a46f0a691d55146d7b4cf1ddac605db7

Alternating row/feature attention encoder and prefix expression decoder; ~62M synthetic datasets with TabICLv2 prior, then risk-sensitive GRPO. S penalty 0.5, M 0.15, L 0.05. Author reports 10.3 mean nodes, 26s mean across 12 SRBench 2.0 black-box tasks. Hardware/clock/batch independent verification absent. S may sacrifice fit, up to 11 finite features, no missing values, restricted operators; Feynman exact recovery not universally superior. Exact tensor census unknown, nominal 94.1M. No inference of unique physical law. KEEP MatrixFormer (numeric cell completion), Kumo-Tabular (target prediction), Lilavati/checker (text-to-program), TinyCast (time-series forecast). HOLD distinct RASR L/M/base; not quantizations, matched marginal value and immutable scope pending. HOLD Shorter Formulae (https://arxiv.org/abs/2610.03947; 145M base/noise FT, four 89M ablations, equal-time extrapolation advantage but search methods can outperform with more time, .pth and incomplete pin); Flash-ANSR (https://arxiv.org/abs/2602.08885; 120M F32, unmatched comparisons).

Pinned weight b764ebf857a20509de7ba86fa0dc90757b89f3e7 / LFS SHA256 ada6f12950507c70e86ee0c1b94783de6c6852e10c76214bb0c0f52a5e78acfa, 188351066 B; root code f7bdf878a46f0a691d55146d7b4cf1ddac605db7, 120 blobs 1754342 B; gitlinks excluded from sum. Known partial 190105408 B; complete archive/owner increment unknown, not reservation. MIT card and pinned source LICENSE, training data and per-act rights not established. Python 3.12–3.13, torch >=2.6, simplipy==0.2.14, triton, torchtitan. Local path loader supports safetensors/config; snapshot_download nonlocal and SimpliPyEngine.load(install=True) including workers, block until engine install and wheelhouse audited. No verified license or access change; no risk-based acquisition rank. Owner HDD not rehashed. 4TB/200GB floor/RAM limits unchanged.

Preflight validation: compare old rows exactly and sidecar identities, all STOP, publisher byte sum, approved queue empty. Regression test added; actual test execution status separate, not presumed.
