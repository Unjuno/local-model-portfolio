# 第7回選定 — 小型・専門モデルの容量効率を優先（2026-10-31）

> 正本の `catalog/CURRENT.json` はv2の110件・有効94件のまま。これは7モデルの**新規レビュー用選定案**であり、重みを取得するリストではない。Hugging Faceの公開データ・公式カードとGitHub実装を使い、同じモデルの別フォーマットを重複して計上しない。

## 1. 7モデルの採否

| 正規配布元 | 今回の判定 | 公開UI容量の目安 | 異なる能力/重みとして残す理由 |
| --- | --- | ---: | --- |
| [facebook/dinov3-vits16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m) | conditional / R0 | 86.4 MB model.safetensors; Gated | 現行7B原本の代替とはせず、同じDINOv3系列を86.4MBの蒸留済み版で比較する。Gated原本の取得権と技術的再現性は未確定。 |
| [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) | select_proposed / R2 | 99.2 MB safetensors; Apache-2.0 | 99.2MB、単眼相対深度専用。通常の画像埋め込み・SAMマスクの出力と異なる。絶対距離を出すメートル深度モデルとは区別。 |
| [facebook/sam2-hiera-tiny](https://huggingface.co/facebook/sam2-hiera-tiny) | select_proposed / R2 | 156 MB safetensors; Apache-2.0; full repo 312 MB | 公式repoは約312MBだが、safetensorsと旧.ptが各約156MB。まずsafetensors一式を選ぶ。既存SAM3の文字プロンプト等を全て代替できるわけではない。 |
| [Qwen/Qwen3Guard-Gen-0.6B](https://huggingface.co/Qwen/Qwen3Guard-Gen-0.6B) | select_proposed / R1 | 1.52 GB full repo; Apache-2.0 | 1.52GBの全repo表示。後学習された安全分類を独立資産とする。名前0.6Bに対しHubは約751.6M params表示。Shieldstral/LlamaGuardとは同一ルール・データで比較が必要。 |
| [microsoft/OmniParser-v2.0](https://huggingface.co/microsoft/OmniParser-v2.0) | conditional / R1 | main 1.12 GB; MIT caption; MIT detector in refs/pr/37 ~281 MB | 公式mainにはAGPL-3.0由来の旧icon_detectがあり、MITのicon_detect_v3は現在見えるrefs/pr/37の約281MB。mainのicon_caption約1.08GBを合わせる選択を検証する。main一括をMITと扱わない。 |
| [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) | conditional / R1 | 2.48 GB full repo; CC-BY-NC-4.0 | 2.48GBの全repo表示。重みはpytorch_model.binで、実行時に安全確認が必要。v5 Transformersのtranslation pipeline非対応や非商用条件を固定する。 |
| [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | select_proposed / R2 | 2.03 GB model.safetensors; 7.92 GB full repo; Apache-2.0 | 全repo約7.92GBに対しメインのmodel.safetensors約2.03GB。動画質問応答に必要なトークナイザとProcessorを加え、ONNX/その他形式を別版として評価。 |

**推奨4件、条件付き3件。** 候補のrepo IDは現行v2、第3〜6回の過去提案と照合し、新規7件に重複はない。

## 2. 重要なモデル供給・権利の差

### DINOv3 ViT7BとViT-S

現行v2には `facebook/dinov3-vit7b16-pretrain-lvd1689m`（上流全repoの観測は26,864,283,632 B）があり、今回のViT-Sはモデルカード表示86.4MB。サイズでは約311倍の違いになるが、**ViT-Sは蒸留された別の重みであり、高精度原本の置き換えではない**。同じデータ・同じ画素数・同じ前処理・同じ評価タスクで測るまで両モデルの能力差は未確定。Gated利用条件も共通に確認する。

### OmniParserのMITとAGPL

公式[Microsoft OmniParserモデルカード](https://huggingface.co/microsoft/OmniParser-v2.0)は、`icon_detect`をAGPL-3.0、`icon_detect_v3`をMIT、`icon_caption`をMITと区別する。現時点で[mainのツリー](https://huggingface.co/microsoft/OmniParser-v2.0/tree/main)には前2種類のうち`icon_detect`しかない。作者の[GitHub案内](https://github.com/microsoft/OmniParser)は新MIT検出器を[refs/pr/37](https://huggingface.co/microsoft/OmniParser-v2.0/tree/refs%2Fpr%2F37/icon_detect_v3)から取得する手順を示す。**2つの違うrevisionを一つのmainとして誤って固定しない。**

### SAM2・SmolVLM2の不要な複数形式

[SAM2 Tinyのrepo](https://huggingface.co/facebook/sam2-hiera-tiny/tree/main)はsafetensors約156MBと旧PyTorch .pt約156MBが同梱。両形式の併存は要検証で、自動保存しない。[SmolVLM2のrepo](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct/tree/main)は約7.92GBだが、選定する主チェックポイントは約2.03GB。残余はONNXなどの別形式の可能性があり、何が必要かをファイルツリー・依存で確定する。

### NLLB-200とQwen3Guardの用途

NLLBは**文字の多言語翻訳**であり既存のリアルタイム同時翻訳モデルを置き換えるものではない。非商用CC BY-NC 4.0と旧PyTorch `.bin`を審査する。[Qwen3Guard](https://huggingface.co/Qwen/Qwen3Guard-Gen-0.6B)は小型の安全分類という用途に特化しており、Shieldstral等との違いは同じタスクの独立評価まで不確実。

## 3. 今回の権利/完全性保留3件、監視2件

| 配布元 | 判定 | 根拠 |
| --- | --- | --- |
| [facebook/watermark-anything](https://huggingface.co/facebook/watermark-anything) | HOLD | undefined |
| [depth-anything/Depth-Anything-V2-Metric-Indoor-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Indoor-Small-hf) | HOLD | undefined |
| [depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf) | HOLD | undefined |
| [microsoft/Florence-2-base](https://huggingface.co/microsoft/Florence-2-base) | WATCH | undefined |
| [google/timesfm-2.0-500m-pytorch](https://huggingface.co/google/timesfm-2.0-500m-pytorch) | WATCH | undefined |

**特にWatermark Anything**は重要な真正性技術だが、公式GitHubがMITと説明する`wam_mit.pth`とHF配布の`checkpoint.pth`のハッシュ一致・同一学習版が未確認。COCO研究版には非商用条件があり、HFのMITタグだけで全ファイルに同じ権利を適用しない。`.pth`のpickleも隔離審査が必要。近似名が異なるものを同一の重みとして自動承認しない。

## 4. 容量の考え方と単位チェック

選定案7件について、公開UIの丸められた数値から、各選定対象を混ぜたサイズ見積りを作ると**約7.733GB**となる。この数値は**一部が全repo、一部が単一チェックポイントの混合**で、正確な選択ファイル全量や必須ソフトウェアを示さず、取得可能容量の上限・下限を構成しない。現行v2の3.234TBに未加算。

最終承認時は次の容量モデルで確定する。

\[B_{\mathrm{bundle}}=B_{\mathrm{weights}}+B_{\mathrm{deps}}+B_{\mathrm{runtime}}-B_{\mathrm{shared}}\]

| 記号 | 意味（日本語） | SI単位 | 定義・前提・範囲 | 型 |
| --- | --- | --- | --- | --- |
| \(B_{\mathrm{bundle}}\) | 対象バンドルの実容量 | B | 対象資産群に必要な全ファイル量、0以上 | 非負実数スカラー |
| \(B_{\mathrm{weights}}\) | 選択した本体重みと設定 | B | 固定revの全シャード・設定、0以上 | 非負実数スカラー |
| \(B_{\mathrm{deps}}\) | 必要なEncoder/Codecなどの別重み | B | オフライン動作に必要な重み依存、0以上 | 非負実数スカラー |
| \(B_{\mathrm{runtime}}\) | 実行ソフトウェアと環境ロック | B | 必要なバイナリ・ライブラリ、0以上 | 非負実数スカラー |
| \(B_{\mathrm{shared}}\) | ハッシュ一致で共有できる重複実体 | B | 上記の合計以下、権利も両立しなければ控除不可 | 非負実数スカラー |

**次元チェック**：右辺の各項はバイトBで、左辺と同じ次元。十進GBは10^9 B、GiBは2^30 B。ラウンド表示値や同一性不明なミラーを誤って控除しない。

**実装前提**：CPU/GPU・GPUメモリ・OS/カーネル・Python ABI・CUDA/ROCm/Metal/Vulkan・driver・推論backend・コンテキスト・バッチ/並列数・重み精度とKVキャッシュをモデルごとに固定する。ピークRAMはOS+重み+KV+workplaceを含めて、512,000,000,000 B未満とする。容量に空き200GBという別条件がある。

## 5. H/T/D/C/U

| 区分 | 最小の検証ルール |
| --- | --- |
| H | 7件の小型モデルで既存ポートフォリオに足りない能力、または同一タスクの効率的な代替原本を少容量で確保できる可能性がある |
| T | まず7件の各公式モデルカード、適用LICENSE、選択ファイルと完全revを1件ずつ調査。性能評価時は同一データ・タスク・HW・クロック/電力・backend/版・精度・batch/コンテキストを事前固定し最初に比較可能な2モデルで実測。条件未充足なら逐次停止 |
| D | PASS=選択理由・正式公開元・固有能力の裏付けがある。FAIL=重複・非許諾・依存が得られない。UNCERTAIN=選択ファイルbytes/完全sha/実測精度/依存ライセンスが未知。PASSでも取得禁止は維持 |
| C | 元モデルに全ての能力が既にあり小型化で重大な精度を失う、重要な版はPruned/蒸留で再現研究価値が異なる、MIT版とAGPL版の依存関係が混在する |
| U | 上流repoの版変更・公開UIの丸め、実機環境差・非商用条件・モデル固有ライセンス・評価セット漏れ。測度の確率分布を定義していないため合成標準不確かさと包含係数kの数値は出さない |

## ERROR CHECK

- 第7回の新規候補7件：採用推奨4・条件付き3。旧Round3/4/5/6と正式台帳の新規ID重複0。
- WAMを権利が一意でないままMIT原本と決めつけない。DINOv3-SをViT7Bの完全コピーと扱わない。SmolVLM2の7.92GBを必要サイズと扱わない。
- `CURRENT.json`と`queues/approved.json`は変えていない。全候補の`selected_file_bytes=null`/未承認。