# R194 / v98 — PULSE learned image codec

2026-11-28 JST。基準 main 77c1a27d981fb807d485522039b0d5f4e551ff8e。291→292登録、235→236 active、179→180 conditional、SELECT 56。既存全行と133 VERIFIED報告維持。全STOP。先行独立研究 [証拠](../../docs/strategy/pulse-learned-image-codec-research-2026-11-28.md) を正式選定へ統合。取得承認・重量DL・削除0。

ADD zhaoyangjia/PULSE pulse-mse。独立に学習された可変レート画像コーデックの基本MSE版。整数CDF予測・meta prior・bit-exact entropy decodingを備え、既存の超解像Phips/PULSEや潜在VAE、画像生成とは異なる実ビットストリーム符号化・復号の研究能力を補完する。原本画像の代替ではない。

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

配布元7ファイル88,499,234 B + 固定コード218 blobs 2,165,939 B = 90,665,173 B。HF全18ファイル373,706,354 B。12 publisher checksums、8 LFS一致。依存込み・実機増分・権利・正確な総数・ABI・復元未確認。4TB/200GB/275GB不変。

一次資料・実験設計は上記証拠および [研究](../../catalog/research/2026-11-28-pulse-learned-image-codec-primary-evidence.json)、[候補manifest](../../manifests/drafts/r194-2026-11-28-pulse-codec-original.candidate.json)、[採否](../../catalog/decisions/2026-11-28-r194-pulse-codec-formal-add.json)。JS preflight実施、Python回帰テスト追加（未実行）。
