# R193 / v97 — BiSCI 分光圧縮撮像復元

2026-11-28 JST. Base f98d89c9e8ff68e8b4f862533c7fcd63f44c023d v96-20261128; concurrent additions preserved. Four novel repo IDs absent from v93 rows and prior research/strategy/decision/manifest grep. HF spectral/compression 50 each sorted lastModified, bounded 7/30/90-day web specialist search plus older work. No exhaustive survey or restriction-change claim.

ADD CaiYuanhao/BiSCI simulation BiSRNet only, research-only CONDITIONAL/R2. Independent binarization-aware BiSRNet trained for 28-band CASSI simulated coded measurements to spectral cubes, not post-training quantization. DGNO fluorescence defocus, STSF direct mask, TerraFM representation, PULSE upsampling and primal_vae generative latent are not same-output substitutes. Simulation BiSRNet alone, not all 12 checkpoints.

NeurIPS 2023 Table 1 ten KAIST simulation scenes: BiSRNet 29.76 dB / 0.837 SSIM vs BTM 27.21 / 0.716 and BBCU 26.51 / 0.673. CAVE training; adaptive spectral redistribution and differentiable sign surrogate.

TSA-Net full precision 31.46 dB / 0.894 better. 36K params and 1.18G OPs normalized binary cost, not complete learned scalar census or measured latency. No matched owner runtime, binary kernel or RAM verified. Real HF weight 2835887 B vs GitHub 2873024 B, HOLD; equal simulation size is not parity proof.

HF d7c8aaac7c5180dd6334edc602120b43afa5817c created 2026-11-10, public ungated, card Apache-2.0. GitHub code 9905f65e87036411758e53cdca87b8a425df523f, MIT LICENSE.txt, pinned requirements. No proof HF weight equals earlier GitHub weight. 2023 original training, not 2026 new architecture. Selected 3 HF refs 2854346 B, 29 GitHub code/README/license/requirements refs 301186 B; combined 3155532 B source reference only; dependency/physical incremental bytes null. No model weights or code executed/downloaded. See manifests/drafts/r193-2026-11-28-bisci-simulation-source.candidate.json.

HOLD real profile, LiMoDeNet (CC-BY-NC, 0.69M backbone not full, modern restoration baselines stronger), TerraCodec FlexTEC (two ~901MB variants, rate-quality and decoder closure unresolved), STELLAR (semantic/spatial representation, scale and decoder tradeoff unresolved). KEEP DGNO, STSF, TerraFM, PULSE, primal_vae. No matched replacement evidence. See catalog/research/2026-11-28-r193-spectral-compressive-imaging-evidence.json and catalog/decisions/2026-11-28-r193-bisci-formal-add.json.

291 tracked, 235 active (56 SELECT, 179 CONDITIONAL); 32 active unknown parameter totals; all 235 STOP. 133 prior reported verified acquisitions unchanged, not local rehash. Archive 4TB, 200GB free floor, 150B baseline and matched RAM exception unchanged. Owner rights, dataset/mask dependency closure, local storage, safe .pth inspection, ABI and matched owner hardware runtime unverified. Independently reproduce KAIST PSNR/SSIM with fixed mask, full-precision comparator and actual peak RAM/latency/clock/backend before acquisition. No approval.

Primary sources:
- https://huggingface.co/CaiYuanhao/BiSCI/blob/d7c8aaac7c5180dd6334edc602120b43afa5817c/README.md
- https://huggingface.co/api/models/CaiYuanhao/BiSCI/revision/d7c8aaac7c5180dd6334edc602120b43afa5817c?blobs=true
- https://arxiv.org/abs/2305.10299
- https://proceedings.neurips.cc/paper_files/paper/2023/hash/788e086c07b8d6fa6b279df56e512312-Abstract-Conference.html
- https://github.com/caiyuanhao1998/BiSCI/tree/9905f65e87036411758e53cdca87b8a425df523f
- https://api.github.com/repos/caiyuanhao1998/BiSCI/git/trees/9905f65e87036411758e53cdca87b8a425df523f?recursive=1
