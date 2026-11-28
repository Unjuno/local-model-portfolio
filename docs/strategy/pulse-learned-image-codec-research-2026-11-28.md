# PULSE 独立学習画像コーデック — 新規調査・比較証拠

2026-11-28 JST。正式選定候補はADD（研究限定CONDITIONAL）。並行更新により先行候補コミットはmain未反映。この独立した研究証拠を先にmainに保存する。正式カタログ、取得承認、物理資産は本証拠コミットでは変更しない。

## 新規一次資料と判断

- https://arxiv.org/abs/2609.18602
- https://huggingface.co/zhaoyangjia/PULSE/blob/26efab7d7e723929550542540294063a4c5b5aec/README.md
- https://huggingface.co/zhaoyangjia/PULSE/blob/26efab7d7e723929550542540294063a4c5b5aec/manifest.json
- https://huggingface.co/zhaoyangjia/PULSE/blob/26efab7d7e723929550542540294063a4c5b5aec/SHA256SUMS
- https://huggingface.co/zhaoyangjia/PULSE/blob/26efab7d7e723929550542540294063a4c5b5aec/LICENSE
- https://huggingface.co/api/models/zhaoyangjia/PULSE?blobs=true
- https://github.com/microsoft/GenCodec/tree/cdb5a73508b6206676aca800fe7f5b3ffc24b218/PULSE

7日/30日窓ではPRISM、FMT、ICM蒸留を調査（配布重み未確認）。90日窓で9月公開PULSEを発見。対象限定検索、過去全文重複の網羅検査ではない。

**ADD (CONDITIONAL)** zhaoyangjia/PULSE / pulse-mse。独立に学習された可変レート画像コーデックの基本MSE版。整数CDF予測・meta prior・bit-exact entropy decodingを備え、既存の超解像Phips/PULSEや潜在VAE、画像生成とは異なる実ビットストリーム符号化・復号の研究能力を補完する。原本画像の代替ではない。

原著Table 3: Pulse MSEはCLIC Professional validationでHM-16.25比PSNR BD-rate -2.9%、1088×1920 AMD EPYC 9V84単一CPUスレッドで符号化920ms・復号126ms、5.2 kMAC/pixel decoder。HEIC +25.2%、80ms、HM 0%、98ms。著者実験のみ、clock/batch未確認。

VTM-17.0は-23.4%/189ms、EVC-S -14.3%。PULSEは可逆画像ではなく、bit-exact entropyは画素一致を保証しない。画面・ゲーム・芸術画像への汎化、実HDD/ABI/完全オフライン復元、独立再現未確認。13M encoder/1.7M decoderは各経路の使用数で重複除去済み全体数ではない。

- ADD: zhaoyangjia/PULSE — 独立に学習された可変レート画像コーデックの基本MSE版。整数CDF予測・meta prior・bit-exact entropy decodingを備え、既存の超解像Phips/PULSEや潜在VAE、画像生成とは異なる実ビットストリーム符号化・復号の研究能力を補完する。原本画像の代替ではない。
- HOLD: zhaoyangjia/PULSE / pulse-s-mse — Distinct smaller architecture, +5.9% BD-rate vs HM, 77ms decode; not a mere quantization; defer until matched resource benefit established
- HOLD: zhaoyangjia/PULSE / pulse-perceptual — Separate learned perceptual objective; +45.5% PSNR BD-rate vs HM and -4.1% FID BD-rate vs MS-ILLM; fidelity tradeoff not justified for first codec research state
- HOLD: zhaoyangjia/PULSE / pulse-l-perceptual — Distinct larger perceptual state; -22.5% FID BD-rate, 420ms decode; no immediate incremental need
- KEEP: Phips/PULSE — Separate image super-resolution; not same author/model or bitstream codec
- KEEP: ostris/primal_vae — Distinct learned latent representations, no documented interoperable PULSE bitstream
- KEEP: Qwen/Qwen-Image-2.1 — Image generation/editing, not entropy coding
- HOLD: zhaoyangjia/CoD_Lite — Different ultra-low-bitrate diffusion codec; Table 3 author comparison 5.9s decode, +218.8% PSNR BD-rate; lower bitrate operating range not matched. No replacement evidence
- HOLD: PRISM — Recent paper; source weights/revision not confirmed
- HOLD: FMT lossless image codec — Recent paper; weight/code release not verified
- HOLD: Generalizable Variable-Rate Adaptation for Image Coding for Machines — Task-focused student distillation, estimated bitrate excludes coding overhead; weights not verified

入替・除外なし。原画の可逆保存を置き換えない。

## 保存容量と権利

HF revision 26efab7d7e723929550542540294063a4c5b5aec、18 source files 373,706,354 B、4 profile 12 publisher checksumsのうち8 LFS SHA一致。選定7 files 88,499,234 B、コード cdb5a73508b6206676aca800fe7f5b3ffc24b218 218 blobs 2,165,939 B、計90,665,173 B参照範囲。全依存・実機増分不明。MIT公開・ungatedの観測であり個別利用権の承認ではない。4TB/200GB床/275GB予約上限不変。PyTorch .pt信頼境界、固定C++ rANS ABI・wheelhouse未確認。重み未実行。

## 検証設計

H: 画像符号化・復号という非重複能力を提供する。T: CLIC/Kodakの許諾済みデータ100画像以上、固定CPU/clock/thread/精度/ABI、最低3反復。同PSNR・同レート比較と実ビットストリーム保存・別機種の整数エントロピー一致。D: 全画像復号成功・ビットストリーム互換・権利/依存/総数/容量/復元全ゲート成立でPASS、不一致でFAIL、未実測はUNCERTAIN。C: 既存可逆/標準codecが同条件で十分、再現不能なABI、知覚歪み。U: publisher計測のみ、クロック・バッチ・総数不明、合成不確かさ算出不可。実機評価未実施。

候補差分、manifest、テストは [候補コミット](https://github.com/Unjuno/local-model-portfolio/commit/ff39217483daa43dec263d9f7744b926c51c0483) に保存済み（mainへの反映は未成立）。
