# R195 / v99 — SeisLM 地震波形専門表現

2026-11-28 JST. Integrated latest v98-20261128 at b7a02ae7526af15ea86175fccf61a17d56f4b77b, preserving all 292 prior rows, including concurrent research. 293 registered, 237 active, 56 SELECT, 181 CONDITIONAL, all acquisition STOP. 133 historical verified receipts untouched.

## Evidence
Independent contrastively pretrained seismic waveform encoder, not another generic time-series forecasting model or a quantization. Three-component ground-motion representation for low-label downstream geophysics. Preserve compact Base only; Large does not justify marginal bytes without matched evidence. No existing selected model establishes same-task replacement.

Publisher 11,359,568 FP32 parameters including original pretraining heads; 6-layer Wav2Vec2-derived transformer hidden 240, 3 ZNE channels, 100 Hz, 3001 samples -> 749 x 240 features. Original eight-corpus pretraining (ETHZ/GEOFON/STEAD/MLAAPDE/InstanceCounts/Iquique/PNW/OBST2024); paper reports low-label downstream transfer. Publisher synthetic 8-field regression exact on CPU and NVIDIA GB10 with Python 3.12.3/PyTorch 2.14.1+cu130; not independent performance or hardware latency.

Bare encoder lacks trained phase/event head; no earthquake-warning efficacy established. No automatic resampling or missing-channel filling; training optimizer omitted, dataset snapshots/rights and exact recreation unresolved. SeisMoLLM reports SeisLM deficiencies; later objective-comparison preprint reports downstream tradeoffs. Independent matched transfer, memory/clock/batch and runtime ABI unverified; wheel code unreviewed.

Fixed revision 13a3dcd6ae56c39f5b0750b817c8788a7fc3c99b; public 2026-10-15 MIT grant. 45,633,248 B full source; 45,546,712 B candidate seven files (FP32 weight, config, preprocessing, manifest, license, card and wheel 0.2.1). Complete dependencies and owner actual bytes unknown. No model/wheel execution or download approval. Secondary 2026-10-03 report did not establish public license; fixed 2026-10-15 publisher release explicitly MIT for weights. Not proof of prior prohibition or change in legal terms.

## Decisions
- ADD ltlltl2006/seislm-base: Independent contrastively pretrained seismic waveform encoder, not another generic time-series forecasting model or a quantization. Three-component ground-motion representation for low-label downstream geophysics. Preserve compact Base only; Large does not justify marginal bytes without matched evidence. No existing selected model establishes same-task replacement.
- KEEP autogluon/chronos-2: Generic multivariate forecasting; does not provide pretrained seismic phase representation.
- KEEP mistralai/Timestral-5M: Compact forecasting outcome; different target.
- KEEP raws-labs/tinycast: Very small univariate forecast model; complementary.
- KEEP MBZUAI/TerraFM: Satellite remote-sensing representation, different physical modality.
- KEEP Duane245/DGNO: Fluorescence inverse problem, distinct measured input and output.
- KEEP hanyuyuan/STSF-TPLS-weights: Coded imaging segmentation; not ground-motion waveform representation.
- HOLD ltlltl2006/seislm-large: 90,683,648 parameters, 362,760,728 B weight; 0ac6158dbfd139591f57d3064a893e667387106f; same family, marginal benefit insufficiently established.
- HOLD YuYu1015/YuYu1015-PhaseNet-50Hz-268k-v1: 268,443 params claimed; 1,114,631 B weights; 372d89ef726217cafea3895da3811e9e20534088. No verified training lineage or comparable quantitative evaluation; PT trust unresolved.
- HOLD SeisProcBench/SPBench-Model: Multiple seismic processing checkpoints; per-state training and closure not established. README at 68603de6c74cb02fe179b1064241ea346bff27eb.
- HOLD SeisDFE: 7B seismic foundation model for geological interpretation; 2026-11-16 arXiv:2611.20745; fixed released weights not confirmed.

## Sources and validation
7/30/90-day web queries, newest HF sample 100, SeisLM 2, seismic 16 keyword results, older primary papers. Not exhaustive.
- https://huggingface.co/ltlltl2006/seislm-base/blob/13a3dcd6ae56c39f5b0750b817c8788a7fc3c99b/README.md
- https://huggingface.co/api/models/ltlltl2006/seislm-base/revision/13a3dcd6ae56c39f5b0750b817c8788a7fc3c99b?blobs=true
- https://huggingface.co/ltlltl2006/seislm-base/blob/13a3dcd6ae56c39f5b0750b817c8788a7fc3c99b/LICENSE
- https://huggingface.co/ltlltl2006/seislm-base/blob/13a3dcd6ae56c39f5b0750b817c8788a7fc3c99b/manifest.json
- https://huggingface.co/ltlltl2006/seislm-base/blob/13a3dcd6ae56c39f5b0750b817c8788a7fc3c99b/config.json
- https://arxiv.org/abs/2410.15765
- https://github.com/liutianlin0121/seisLM
- https://doi.org/10.1029/2025GL118505
- https://arxiv.org/abs/2610.38003
- https://fossettlab.org/models/seislm/
- https://huggingface.co/ltlltl2006/seislm-large/blob/0ac6158dbfd139591f57d3064a893e667387106f/README.md
- https://huggingface.co/YuYu1015/YuYu1015-PhaseNet-50Hz-268k-v1/blob/372d89ef726217cafea3895da3811e9e20534088/README.md
- https://huggingface.co/SeisProcBench/SPBench-Model/blob/68603de6c74cb02fe179b1064241ea346bff27eb/README.md
- https://arxiv.org/abs/2611.20745

Metadata-only regression tests/test_r195_v99_seislm_specialist.py. No owner rights, local SHA, measured memory, final dependency closure, or operational efficacy inferred. Existing scripts/build_v93_plan.py constructs approval flags from metadata; not executed or changed. Separate review required.
