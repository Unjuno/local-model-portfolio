# v9：150B上限に関する未確認25モデルの一次資料監査（2026-11-03）

## 監査結論

既存v8の109モデルのうち、総パラメータが未確認だった25件について、Hugging Face配布者カード、開発元GitHub、技術論文、公式ベンダードキュメントを優先して追加調査した。

- **13件は、配布元が示す特定の公開モデルまたは主要な実行部品のパラメータ数が150B未満であることを確認**。150BハードゲートをPASSへ更新。ただし元重みの全テンソル厳密集計や依存モデルの許諾、実行時RAM、取得バイト数の審査は未完了。
- **12件は、公式資料に一部の主モデル/活性パラメータ数があっても、総数・対応revision・必要な外部学習済みコンポーネントの範囲が決まらないためUNCERTAINのまま**。このうち有効選定は7件。
- 150B以上と確認済みの2件（OrcaRouter Qwen3.8 Flash Next ~180B、Mistral Large 4 ~1.05T）のEXCLUDED状態は維持。**有効105件・管理132件**は不変。
- **総パラメータゲートの現在値：95 PASS / 2 FAIL / 12 UNCERTAIN（モデル109件）**。他にデータセット23件は150B制約の対象外。
- ダウンロード承認0件、ユーザーPCでのモデル実行・インストール0件、全重量ファイルの未取得状態を維持。

## 新たに150B未満のモデル規模を確認した13件

| 配布元モデル | 出典に記載された規模（概数を含む） | 元情報の適用範囲と残る課題 |
| --- | ---: | --- |
| [KlingTeam/LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | 130.09M | Five modules, sum of first-party table: 0.84+28.12+55.37+45.53+0.23 million; excludes independent face detector/InsightFace. |
| [ResembleAI/chatterbox](https://github.com/resemble-ai/chatterbox) | 500.00M | Publisher-listed latest multilingual/core Chatterbox variant 500M; repo/family may contain variants, count applies per named model, not sum of all files. |
| [Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | 22.000B | Full developer model checkpoint named ltx-2.3-22b-dev and distilled versions; separate text encoders/upscalers are dependencies. |
| [Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | 5.000B | Publisher official TI2V-5B checkpoint (distinct from A14B family variants). |
| [nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB](https://docs.nvidia.com/nemo/automodel/model-coverage/vision-language-models/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB-BF16) | 8.000B | NVIDIA NeMo table explicitly says Total parameters 8B, 4B effective, with GGUF variant maintaining same original model parameter count. |
| [boltz-community/boltz-2](https://build.nvidia.com/mit/boltz2/modelcard) | 1.000B | NVIDIA NIM model card for original Boltz-2 architecture lists 1 billion model parameters; original group MIT Jameel Clinic Boltz-2. |
| [nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | 2.000B | NVIDIA official diffusion transformer 2B Video2World variant; repo includes six same-model video variants. |
| [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | 4.000B | Microsoft published 4-billion-parameter flow-matching transformer (one named model); VAE/pipeline components separately dependency-locked. |
| [speridlabs/idol](https://github.com/speridlabs/idol-sdk) | 1.800B | Publisher's full inference request component table sums approximately 1.80B, including local DiT/decoders/BiRefNet plus gated DINOv3 and FLUX.2 VAE. |
| [tencent/Hunyuan3D-2.1](https://huggingface.co/spaces/tencent/Hunyuan3D-2.1/blob/main/README.md) | 5.300B | Publisher model zoo: Shape-v2-1 3.3B plus Paint-v2-1 2B. Total major shape/texture checkpoints ~5.3B. |
| [BAAI/bge-m3](https://bge-model.com/bge/bge_m3.html) | 569.00M | First-party BGE documentation explicitly lists BGE-M3 569M parameters. |
| [Edge0/Audio8-TTS-Realistic-0.6b](https://huggingface.co/Edge0/Audio8-TTS-Preview-0.6b/discussions/2) | 938.59M | Same published DualAR family main model 601,159,424 and bundled codec 337,428,866 (user calculation explicitly acknowledged by publisher on Preview variant). The Realistic variant documents same base architecture; exact Realistic variant tensor census is still pending. |
| [nvidia/nemotron-labs-unified-asr-0.6b](https://huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b) | 600.00M | NVIDIA original model card architecture lists 600M parameters for Unified FastConformer-RNNT. |

**厳密性への注意：** 「F5-TTSの335Mメインモデル」のような主モデルだけの数や、「Lanceの3B active」のような**活性数のみ**は、包括的な150B以下の証明に採用しなかった。13件の数値も公開者の**概数/モジュール合算値**を含むため、モデル内全テンソルの正確な再計算完了と誤記しない。**モデル本体のゲートと、依存する別モデル/codec/encoderのゲートを分けて固定すること**が最終取得の必須条件。

## 引き続き12件を保留した理由と解消すべき作業

| 配布元モデル | 現時点で確定できない点 | 次の検証 |
| --- | --- | --- |
| [InstantX/InstantID](https://github.com/instantX-research/InstantID) | Official repo exposes IdentityNet ControlNet + IP adapter and uses InsightFace + SDXL; no complete first-party numerical parameter census for these parts. | Enumerate fixed checkpoint metadata (ControlNet/IP-Adapter) and external FaceAnalysis; count tensors when permitted, but do not execute pickle. |
| [Plachta/Seed-VC](https://github.com/plachtaa/seed-vc) | Official table quotes 25M, 98M, 200M main variants and 67M CFM +90M AR; XLSR/Whisper encoder and BigVGAN/HIFT remain outside main figures. | Select one concrete version and account for all learned encoder/vocoder checkpoints; published main numbers alone not a complete original pipeline total. |
| [SWivid/F5-TTS](https://github.com/SWivid/F5-TTS/issues/14) | Developer confirmed base model approximately 335M, but codec/vocoder dependencies and precise selected variant unresolved. | Pin official F5 base variant and separate neural vocoder dependencies before marking full inference stack validated. |
| [ByteDance/InfiniteYou](https://huggingface.co/ByteDance/InfiniteYou) | Official model card confirms InfuseNet plug-in and FLUX.1-dev parent, but no total trainable component count. | Locate adapter config and published architecture; parent FLUX.1-dev is separately licensed and must be reviewed. |
| [coqui/XTTS-v2](https://arxiv.org/html/2406.04904v1) | Official paper describes a 443M GPT2 component and multiple other trained components; a secondary analysis sums 13+443+26=482M but omits some encoder counts. | Count remaining Perceiver/speaker encoders and match actual 2.0.3-era checkpoint; independent license review mandatory. |
| [fishaudio/fish-speech-1.5](https://huggingface.co/fishaudio/fish-speech-1.5) | Original version 1.5 has training/release docs, but official source inspected does not specify precise end-to-end parameter count. | Obtain version 1.5 config and count all tensor metadata in snapshot; do not substitute newer S2/Drama model sizes. |
| [onnx-community/higgs-audio-v3-tts-4b](https://huggingface.co/onnx-community/higgs-audio-v3-tts-4b) | Derived ONNX model card says 4B autoregressive backbone, but separate codec/export parts and provenance need verification. | Check upstream bosonai official release and ONNX components/quantization before full-asset count and license eligibility. |
| [TencentARC/PhotoMaker](https://github.com/TencentARC/PhotoMaker) | Official PhotoMaker repository documents SDXL/ID-adapter workflow, not complete numeric parameter census. | Count published adapter modules and parent components, inspect licensing. |
| [bytedance-research/Lance](http://arxiv.org/abs/2605.18678) | Official technical report calls 3B 'activated' parameters and describes dual-stream MoE. That is NOT proof total learned weights <150B. | Derive total experts and module dimensions from official config or safetensors metadata; block until verified. |
| [OnomaAIResearch/Illustrious-XL-v1.1](https://arxiv.org/html/2409.19946) | Original Illustrious SDXL-family paper names 2.6B UNet and 817M encoder from earlier release, not an exact v1.1 full checkpoint total. | Verify v1.1 exact checkpoint and remaining text/VAE components without assuming v0.1 totals identical. |
| [microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) | Microsoft official card documents PubMedBERT+ViT-B/16 and a legacy serialized checkpoint, but no exact total published in the checked primary page; third-party tensor-count 197.1M is insufficient for formal pass. | Inspect open_clip_config.json and safe tensor shapes without importing untrusted .bin; verify licensed checkpoint content. |
| [ACERobotics/Puffin-World](https://arxiv.org/abs/2609.04196) | Publisher paper specifies three checkpoint variants assembled from Qwen2.5-7B/1.5B, Qwen3.5-0.8B, C-RADIO and SD3.5-Medium 2.5B/Large 8.1B. Missing complete joint per-variant trained component total. | Choose exact Base/Pro/Caption and enumerate Qwen+vision+diffusion+connector parameters with named revisions. |

### 重要な反例：主パラメータ数だけでは総数にならない

- [Lance](http://arxiv.org/abs/2605.18678)：公式論文は「3B activated」と説明する一方、複数expertの合計総数が未確認。MoEでは活性数を150B上限に代入しない。
- [Seed-VC](https://github.com/plachtaa/seed-vc)：公式READMEは25M、98M、200Mなどの生成本体を記すが、XLSR/Whisper、vocoder等は別重み。デプロイ全体の選択版を固定する必要。
- [F5-TTS](https://github.com/SWivid/F5-TTS/issues/14)：開発者が約335Mのベースを確認したが、別の音響復号器を含む実装に適用範囲を拡張しない。
- [Audio8 TTS](https://huggingface.co/Edge0/Audio8-TTS-Preview-0.6b/discussions/2)：主モデル約601Mにcodec約337Mを加えた全体約939Mを開発者が議論で認めている。**ただしRealistic版とPreview版の正確なrevision別テンソル数比較はまだ必要**。
- [Idol](https://github.com/speridlabs/idol-sdk)：公式のFull Requestは約1.8Bで、DINOv3・FLUX.2 VAEを含むが、後者には別途Gated/権利の審査が必要。

## ダウンロードを止めている未完了ゲート（全132件の現行ビューで確認）

2026-11-03の現行v9ビューでは、**選択ファイルの確定バイト数が記入された資産0/132、最終取得用の固定revision SHA記入0/132、ライセンス本文確認済み0/132、依存審査済み0/132、ダウンロード承認0件**。これは「ファイルが存在しない」のではなく、**選択して取得するバイト列を正式に承認できる状態がまだ一件もない**という意味。

すでにQwen3.5-0.8B・LightOnOCR-3-0.8B・Whisper-large-v3-turbo・Idolの4件には**過去の保存スナップショットから作った未承認の固定ファイル候補JSON**がある。ただし`manifests/drafts/*.candidate.json`であり、権利/依存/RAM/HDDを解決した`*.lock.json`や承認キューではない。この4件を現行ビューの正式な`selected_file_bytes`や`fully_pinned_revision_sha`が確定したと誤って数えない。

したがって、パラメータ監査の **95 PASS** を「95モデルをダウンロード可能」と読み替えてはいけない。ユーザーが実際のHDDへ取得できる状態にするには、上記ゲートを別々に満たす作業が必要。

## 取得前に必要な追加監査

- 有効な未確認7件の公式version/configと全重みファイルを、モデルをロードせず**静的にテンソル形状から数える**。安全形式のsafetensorsならヘッダ等の検証を優先。pickle/ONNXは構造を検査してもロードや任意コード実行を避ける。
- すでに150B未満と判定したモデルも、実際のrevision・全シャード・tokenizer・画像/音声エンコーダー・codec・依存・ライセンス正文を固定する。
- 3.8TBの論理保存枠、200GBの物理安全余白、512GB未満の想定推論RAMと実装前提（backend/量子化zero-point/KV/バッチ/context/SSD）を別途照合する。
- 150B以上の2モデルに将来の保存枠を割り当てない。ライセンス/同意・最終lock/ユーザー承認なしにいかなるモデルも取得しない。

## H / T / D / C / U

- **H**：公開者が明記するモデルパラメータ数と全コンポーネントの分離により、厳密なハード上限を突破するモデルを一件も取得対象に残さず監査できる。
- **T**：旧未確認25件を公式一次資料で確認（今回n=25）。全132件の台帳で109モデルの状態を一意に照合し、残り12件のうち有効7件をrevision固定で再調査する。ソース資料は[機械可読v9監査差分](../catalog/revisions/v9-2026-11-03.json)に格納。
- **D**：PASS＝証拠のある名前付きモデル本体・合算した主要構成部品が150B未満であり、別途の全依存・権利・選択バイト条件を満たして最終承認。FAIL＝150B以上または未承認の取得。UNCERTAIN＝主モデル数しか分からない・MoE活性数しか分からない・必要な部品が不明。今回は13件のパラメータスクリーンをPASS、12件UNCERTAIN。ただしすべてのダウンロード準備は未完了。
- **C**：メーカー公表の「0.6B」「3B」は主モデル/活性数であり、codecや複数expertの総数が追加される。元の配布者資料が後日改訂される可能性もある。
- **U**：公表値の丸め、部品単位の計測範囲、複数チェックポイント、派生版と元版の相違、非定型重みの取り扱いが主要不確かさ。重みを入手せずに厳密な全テンソル数と合成標準不確かさ`u_c`を数値化することは不可。`k`は未適用。150Bへの近接疑義が生じた場合はUNCERTAINに戻す。

## Source-of-truth

[CURRENT v9](../catalog/CURRENT.json)／[132資産の実体化ビュー](../catalog/effective-portfolio-2026-11-03-v9.json)／[v9監査オーバーレイ](../catalog/revisions/v9-2026-11-03.json)／[取得前キュー](../queues/proposed-v9-2026-11-03.json)／[前版v8調査](parameter-cutoff-v8-2026-11-03.md)。

**実際のモデル本体ダウンロード・実行は禁止のまま。**
