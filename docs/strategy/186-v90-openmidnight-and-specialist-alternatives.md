# R186 v90 — OpenMidnight independent pathology representation
2026-11-28 JST. Initial main v86; integrate on v89-20261128, parent 1150996c7f5b23a476276b6ffb6c78066e7d9298; all parallel additions preserved.
## ADD conditional research-only
medarc/OpenMidnight-1.1 57efe1ad969958190f245aa87ee3a8e5d5db7e54. DINOv2-initialized independent histopathology pretraining on about 12k TCGA slides (320 H100 GPU-hours); complete tile encoder, not a quantization. Complements general DINOv3 and generative MedGemma, distinct from biomedical image-text BiomedCLIP, DGNO inverse imaging and TATR geometry.
Positive: Author THUNDER: 16 classification and 4 segmentation tasks, mean segmentation Dice 69.7%, overall rank 4/14. Negative: Single-run comparisons and prior KDE sign issue; no matched device test versus incumbents, no WSI diagnostic head, clinical external validation not established. New squash preprocessing changes inference without changing learned weights.
Publisher F32 stored elements 1,134,774,272; RGB224 full squash, 1536-dim CLS. Separate WSI aggregation head not included; tile encoder needs no external learned parent. timm 1.0.30/PyTorch; device ABI, latency and RAM untested.
Seven immutable publisher files 4539168331 B, six small Git blobs independently verified; LFS weight hash publisher metadata only. Same weight SHA in four revisions, updated config changes preprocessing; no observed license restriction change. Apache-2.0 tag and text observed; owner acts/data rights and clinical validation unresolved.
## Alternatives and decisions
- HOLD ai-hhmi/lmd-vitl-p8-simmim-lvd: 3D ViT-L, 8nm isotropic microscopy, 8^3 patch, 3D RoPE; inflated DINOv3 and independently pretrained 100k SimMIM steps on 243 volumes. Other input windows untested; decoder/optimizer excluded; compare scratch, affinity and CellMap; inherited DINOv3 rights and pinned code closure unresolved. https://huggingface.co/ai-hhmi/lmd-vitl-p8-simmim-lvd
- HOLD eremeev-d/graphpfn-1.3: Independent graph-task adaptation; author reports competitive graph ICL/fine-tuning. Parent revision, full learned total, dependencies and redistribution rights unresolved; .pt code safety unverified. KEEP Kumo-Relational/Tabular; not direct substitutes. https://huggingface.co/eremeev-d/graphpfn-1.3
- HOLD inclusionAI/Ming-Image-0.2-Design: Design-specific generated visual layouts; preliminary publisher AA ranking. 6B denotes DiT only; separate MLLM, connector, MLP, VAE; no matched layout/text fidelity or complete cost comparison to Qwen-Image-2.1/Fibo2.0. KEEP both. https://huggingface.co/inclusionAI/Ming-Image-0.2-Design
KEEP all 283 prior rows, including briaai/Fibo-2.0-dev, briaai/Fibo-2.0-edit-turbo, Qwen/Qwen-Image-2.1, google/medgemma-4b-it, microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224, facebook/dinov3-vit7b16-pretrain-lvd1689m, facebook/dinov3-vith16plus-pretrain-lvd1689m, nvidia/Kumo-Relational, nvidia/Kumo-Tabular, Duane245/DGNO, microsoft/table-transformer-structure-recognition-v1.1-all, hanyuyuan/STSF-TPLS-weights. No replacement proof. Reject separate entries for same learned weight revisions, no physical deletion.
## Sources and state
https://huggingface.co/medarc/OpenMidnight-1.1/blob/57efe1ad969958190f245aa87ee3a8e5d5db7e54/README.md

https://huggingface.co/medarc/OpenMidnight-1.1/blob/57efe1ad969958190f245aa87ee3a8e5d5db7e54/config.json

https://huggingface.co/medarc/OpenMidnight-1.1/blob/57efe1ad969958190f245aa87ee3a8e5d5db7e54/provenance.json

https://huggingface.co/medarc/OpenMidnight-1.1/blob/57efe1ad969958190f245aa87ee3a8e5d5db7e54/LICENSE

https://huggingface.co/api/models/medarc/OpenMidnight-1.1/revision/57efe1ad969958190f245aa87ee3a8e5d5db7e54

https://arxiv.org/abs/2611.00064

https://github.com/MedARC-AI/OpenMidnight
catalog/research/2026-11-28-r186-pathology-graph-microscopy-design-evidence.json / manifests/drafts/r186-2026-11-28-openmidnight-source-frozen.candidate.json / catalog/decisions/2026-11-28-r186-pathology-specialist-formal-selection.json.
284 tracked, 228 active, 172 conditional, 56 select; all STOP. Publisher reference +4539168331 B, actual complete archive increment unknown. 4 TB cap, 200 GB free floor unchanged; no payload transfers or approvals. Precommit exact row preservation and queue/readiness/access joins checked; full suite not run. Nonexhaustive research search.
