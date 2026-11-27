# R180 v83 — 独立CPU音声修復 (2026-11-28 JST)
並行更新 v82 (14bb5bdc80b7fa5c51596f66560ffcb11f65c1c0) を統合。Inworld SAVA/Voice IsolatorおよびPAWP 300K TTSを含む旧276行を維持。ADD 1、277登録/221有効/SELECT56/CONDITIONAL165、全221 STOP。133取得報告保持。重みDL・承認・実行・削除0。

HF 6タスク（各最大25）、7/30/90日とarXiv・開発元の限定探索。網羅性やアクセス条件変更は未立証。

ADD [ai-sage/GigaEdge-Enhance](https://huggingface.co/ai-sage/GigaEdge-Enhance/blob/f1553bd1859bcef52d0037a0ebe4d17da293548e/README.md) — [論文v4](https://arxiv.org/html/2611.13243v4)・[固定実装](https://github.com/salute-developers/giga-edge-enhance/tree/d55d693be6c73df4804f296687e4e4bbb5783938)。11/25 UTC公開・更新、MITタグ/本文確認。hybrid48 FP32、fast8 INT8は別学習履歴、内製データ・訓練・量子化・変換手段未公開。C++17/ONNX Runtime、32ms窓、16ms hop、Hanning、1 thread。quality48は公開checkpointと論文評価の差によりHOLD、TFLiteは同profile別exportで独立学習ではない。

配布者評価（886 EARS-WHAMv2 pairs、normalization/AEC off、16ms hop）:
| 指標 | noisy | hybrid48 | DPDFNet2 HR |
|---|---:|---:|---:|
| DNSMOS P808 | 2.68 | 3.44 | 3.66 |
| PESQ-WB | 1.23 | 1.90 | 2.21 |
| SI-SDR dB | 5.35 | 13.03 | 14.69 |

共有stream 56.00±1.00 vs 17.33±0.58（3 searches、10秒測定、20秒入力反復、16ms chunks、WSL2/ORT、CPU SKU/clock未抽出）。RNNoise 1088.67±30.09。fast8 ESTOI .64→.72、PESQ-NB 1.85→2.28、SI-SDR 5.32→10.99 dB。8/48kHz直接比較不可。生成修復は原音保存・同意・WERで評価。

v81 [Inworld Voice Isolator](https://huggingface.co/inworld/voice-isolator/blob/9b0285b3fe8403aa8e2f1dbb2165a80a4294c970/README.md) は48kHz mono, offline 64M/realtime 58.2M、重み489040928 B、VIBE 5502項目77条件、復元生成なし。GigaEdgeは8kHz narrowband/CPU生成修復、11MB源候補。異なる学習成果と小容量の追加価値は残るが、同一データ・HWでの優位性は未立証。双方CONDITIONAL維持、置換なし。SAVAはEOT、Whisper/GraniteはASR、Mimiはcodec。

- HOLD [kandinskylab/KVAE-Audio-Stereo](https://huggingface.co/kandinskylab/KVAE-Audio-Stereo) cfbe57c806e11cfd1358893688282955fadc3e13: 48kHz stereo continuous latent, 960 samples/step,128 channels; internal claim only, no matched public stereo score; three exports not separate outcomes. 重み参考 669099176 B。
- HOLD [WhiteYC/PixelMatte](https://huggingface.co/WhiteYC/PixelMatte) 556b2ab6a67390412c35e4ee2dee431c49feed57: HiDream-8B and PRX-7B fine-tunes; alpha not binary segmentation; no VAE/text encoder. Trimaps, census and matched evidence unresolved. 重み参考 29231160232 B。
- HOLD [nums-ai/causilo-1.5](https://huggingface.co/nums-ai/causilo-1.5) c2109e225b6cad0e827acf2e454c82fc550f5e7e: Separate classifier/regressor; publisher top Elo nine tasks, 1.5.1 TabArena pending, no matched comparison; rights/census unresolved. 重み参考 2208604548 B。
- HOLD [sathiskumarjothi0/Beveridge-Large-C](https://huggingface.co/sathiskumarjothi0/Beveridge-Large-C) 7cb0d24cce8572b8803a738c083b2419cdc40a8a: Decision network; publisher operations 93.04%, typed decisions 75.85%, rules 85.60%; independent calibration and matched comparisons absent. 重み参考 1592939676 B。
- HOLD [Ceva-IP/DPDFNet](https://huggingface.co/Ceva-IP/DPDFNet) revision未固定: DPDFNet2 HR better quality in GigaEdge study; HOLD pending exact source and rights closure.
- HOLD [google/timesfm-3.0-pytorch](https://huggingface.co/google/timesfm-3.0-pytorch) 297aa8f81ab7e152fa70c00de64e2da596d50572: 11/27 update; already compared R177; no evidence of distinct training or changed terms. 重み参考 1322898824 B。
PAWP 300KはTTSであり波形修復と異なる。KEEP inworld/voice-isolator, inworld/sava, openai/whisper-large-v3-turbo, ibm-granite/granite-speech-5.0-470m-turboctc, kyutai/mimi, facebook/sam3, nvidia/Kumo-Tabular, answerdotai/ModernBERT-large, internlm/Intern-Decision-0.8B, illuin/Ivonnet-0.8B。

全13file 39967596 B、5 LFS SHA。候補7file 11058505 B、2 ONNX/2 config/3 metadata、LFS SHA2。SDK/ORT依存閉包、正確な学習数、権利・owner HDD/SHA/復元未確認、実増分null。4TB/200GB空き条件・既存ゲート維持。
[証拠/H-T-D-C-U](../../catalog/research/2026-11-28-r179-speech-enhancement-specialist-evidence.json) / [manifest](../../manifests/drafts/r180-2026-11-28-gigaedge-two-profile-source.candidate.json) / [overlay](../../catalog/revisions/v83-2026-11-28.json) / [全221 STOP](../../catalog/readiness/v83-2026-11-28-r180-all221-gates.json)。作業環境ディスク満杯のためclone不可、GitデータAPIで更新、全回帰suite未実行。実験は未実行。
