# R196 / v100 Shorter Formulae noise post-training

2026-11-28 JST. Parent 270aaba8371294f8f0b1d5e940b65ab58f657984. 293 prior rows unchanged; 294 tracked/238 active. ADD research-only conditional. Resolve v96 HOLD incomplete pin using immutable HF file and code metadata. Preserve 145M original plus 48h noise FT as controlled robustness pair. RASR-94M-S risk-sensitive GRPO/complexity objective and safer safetensors, 190105408 B partial source; KEEP as complementary smaller baseline. No superiority claim. Distinct learned states, not quantization. Four 89M ablations HOLD.

Publisher reports better extrapolation at equal time (~10 s author experiment) and improved noise robustness after FT; independent exact equation recovery not verified.

Search methods can outperform at 10–1000x time; no matched RASR test, exact tensor census, dependency closure. PTH loader lacks explicit weights_only. Fit does not prove physical law.

- ADD ShwayW/shorter-formulae: Resolve v96 HOLD incomplete pin using immutable HF file and code metadata. Preserve 145M original plus 48h noise FT as controlled robustness pair. RASR-94M-S risk-sensitive GRPO/complexity objective and safer safetensors, 190105408 B partial source; KEEP as complementary smaller baseline. No superiority claim. Distinct learned states, not quantization. Four 89M ablations HOLD.
- HOLD ShwayW/shorter-formulae: Distinct training results, 4318731740 B; marginal value unverified
- HOLD FoundPDE: 2610.26963; 97.50% clean, 94.43% at 2% noise, 52.09% at 10%; no verified checkpoint ID
- HOLD GAIR/SR-Scientist-30B: RL agent 30,532,122,624 params, 61,084,166,003 B source; sandbox; matched value unverified
- HOLD At1uri/kolmogorov-arnold-network-symbolic-engine: 234 params, 16,745 B; held-out general recovery unverified
- KEEP davidotte/RASR-94M-S: 94.1M risk-sensitive GRPO; 10.3 mean nodes/26s across 12 tasks author, unmatched; KEEP cheaper comparator
- KEEP IFM/K2-Horizon-0.9B: text math/code distillation
- KEEP udgamlabs/Lilavati: 94.7M text-to-program word problems
- KEEP Tabimpute/MatrixFormer: 77,998,496 params, numeric cell imputation
- KEEP Duane245/DGNO: image inverse operator

Sources: https://huggingface.co/ShwayW/shorter-formulae/blob/f2eddcf91ca8b83c1fe5f4ef683e3f3e8c96c835/README.md ; https://huggingface.co/ShwayW/shorter-formulae/tree/f2eddcf91ca8b83c1fe5f4ef683e3f3e8c96c835 ; https://arxiv.org/abs/2610.03947 ; https://github.com/ShwayW/shorter-formulae/tree/12c71c723f91175dc92317234c24e1b6dbd745ea ; https://github.com/ShwayW/shorter-formulae/blob/12c71c723f91175dc92317234c24e1b6dbd745ea/LICENSE ; https://arxiv.org/abs/2610.17994. Bounded latest 100 created/modified HF metadata; 7/30/90-day search. No observed access or license change. No independent benchmark. Full HF 5485162467 B; selected 1166430727 B; held 4318731740 B; code 7088086 B (582 blobs); combined 1173518813 B. Dependency closure and owner increment unknown. Python >=3.10, C++20, torch/scipy/sympy, PTH safety, ABI, exact census, rights, offline restore unresolved. Keep 4TB/200GB, parameter policy unchanged. No download, execution, deletion or approval.

H: noise FT improves exact recovery without material clean degradation. T: >=100 paired held-out equations per noise stratum, same HW/backend/time, report seeds/derivative/OOD errors. D: lower 95% paired CI >0 noisy recovery; clean loss <=5 percentage points. C: leakage, fit without symbolic equivalence, derivative failure. U: paired family bootstrap; not measured here.

catalog/research/2026-11-28-r196-shorter-formulae-primary-evidence.json; manifests/drafts/r196-2026-11-28-shorter-formulae-publisher-scope.candidate.json; catalog/decisions/2026-11-28-r196-shorter-formulae-formal-add.json; tests/test_r196_v100_shorter_formulae.py.

## Executed verification

Published main commit bec8a98382edb2397bbfb44481ba555967d61039; fetched from origin main into separate verification worktree files. Python unittest: 4/4 passed (old records and overlay, exact joins and all STOP, source sums, 4TB/200GB policy). CURRENT count map equals catalog counts; readiness blocking gate and first-blocker counts recomputed exactly. Historical ledger 133 verified reports, 137 records; no owner HDD rehash. No full suite or model execution claimed.
