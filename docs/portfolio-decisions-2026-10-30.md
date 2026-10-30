# 一括選定レビュー（2026-10-30）

> **状態：初回選定レビューのみ。ダウンロード承認ではありません。** 各ファイルの選択・全SHA・依存関係の固定は未完了。`queues/approved.json` はこの変更では触れません。

## 優先度の読み方（2026-10-30更新）

**この119件のP0/P1は「保存する価値」の一次評価であり、規制・削除・Gated化に備えた緊急取得順ではない。** 現在の分野別3.8TB枠も調整可能な仮置きであり、分野の網羅や平均配分を優先しない。

実際の選定順は[選定基準](../policies/selection.md)の「最上位原則」に従い、**モデル重みとデータセットを同じ土俵で**、確認済みの現在制限・具体的な公開変更、将来の制限シナリオ、失った場合の再現困難性を組み合わせて再順位付けする。Gatedであることだけを将来の削除予定と見なさず、高性能であることだけを規制の確証としない。データは知財・個人情報・配布許諾を先に確認し、適法な範囲に限定する。

## 評価原則

性能が高いことによる将来のアクセス条件変更は**仮説的なシナリオ**として評価する。Gated/独自ライセンス/提供者が変更可能な状態は現時点で観察できる事実。追加学習済み重みが元モデルのみから再現できないことは別の評価軸。モデルへの攻撃用機能や悪用用途は保存の推奨理由にせず、研究用の隔離保管と正当な利用条件を前提とする。

- **P0** 重要候補。Gated・権利・依存があるときは「条件」を付記し、取得許可とは扱わない。
- **P1** 次点。代表系列の網羅・容量とのトレードオフで採否を決定。
- **P2** 保留または重複が大きいもの。
- **保留** 許諾・実行可能性・容量の未解決が重大。事実不明のものを合格とはしない。

## 暫定の3.8TB部門別予算（選択ファイルの確定容量ではない）

| 区分 | 上限（GB,十進） |
| --- | ---: |
| 汎用LLM・Base・高性能 | 1460 |
| 専門ファインチューニング・無検閲 | 420 |
| 画像生成・編集 | 440 |
| 動画・ワールドモデル | 430 |
| 音声・ASR・TTS | 160 |
| OCR・分類・検索・科学 | 160 |
| データセット・知識資料 | 510 |
| 実行環境・復旧資材 | 180 |
| 部門間調整枠 | 40 |
| **合計** | **3800** |

**注意：** 下記の表示サイズは個別ファイル選定後の正確な合計ではないため、3.8TBの確定配分として加算しない。全モデルに対する必要メモリも未実測。最終承認は完全なcommit、選択ファイルのバイト数とライセンスを確認してから行う。

## 候補の一括判定

### 言語・高性能・Base

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 55.6 | 画像動画を理解するQwen系列の高精度基準重み。派生版の比較原本 |
| P0 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) | 19.3 | 小型の事前学習Base。後からSFTや量子化をやり直せる |
| P0 | [Qwen/Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | 71.9 | MoEの事前学習Base。Denseと違う再学習資料 |
| P0 | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 未確定 | 80B級コード・エージェント専用モデル。機能の独自性が高い |
| P0条件 | [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | 未確定 | 約180Bの新設計MoEと独自ライセンス。高性能化に伴う方針変更に備える |
| P1 | [Qwen/Qwen3.5-122B-A10B](https://huggingface.co/Qwen/Qwen3.5-122B-A10B) | 250 | 約125Bの別サイズMoE。容量競合があれば量子化版を検討 |
| P0 | [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) | 未確定 | Gemma系列のBase重み。Qwenと異なる学習・構造を保全 |
| P1 | [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) | 未確定 | 対話後学習を比較するためのGemma版 |
| P1 | [google/gemma-4-26B-A4B](https://huggingface.co/google/gemma-4-26B-A4B) | 未確定 | Gemma系列のMoE。31B Denseと比較する独立構成 |
| P0 | [meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | 未確定 | Meta系公開重みの30B級別系列。性能比較と移植性 |
| P0 | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | 未確定 | MXFP4の約117B MoE。保存効率と別設計の推論研究 |
| P1 | [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | 未確定 | 約21Bの小型モデル。120Bとのスケール比較 |
| P0 | [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 242 | 約119B MoE。複合能力を持つ独立ファミリー |
| P0 | [mistralai/Devstral-Small-2-24B-Instruct-2512](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512) | 51.6 | コード・ソフト開発特化の後学習済みモデル |
| P0 | [zai-org/GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash) | 62.5 | GLM系列の独立した実用モデル |
| P0条件 | [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | 未確定 | 約109Bの公式MoE原本。現在Gatedで再アクセスが保証されない |
| P0条件 | [CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | 未確定 | 多言語VLM。Gatedかつ非商用条件で別系列の能力を保全 |
| P1条件 | [MiniMaxAI/MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) | 未確定 | 約229Bの高性能候補。原本容量が大きく権利と実行可能性を確認 |
| P0 | [allenai/Olmo-3-1125-32B](https://huggingface.co/allenai/Olmo-3-1125-32B) | 64.5 | 研究公開度の高いOLMo系列。解析・再学習に有用 |
| P1 | [ByteDance-Seed/Seed-OSS-36B-Base](https://huggingface.co/ByteDance-Seed/Seed-OSS-36B-Base) | 未確定 | 36Bの別系列Base。OLMo等との重複予算次第 |
| P1 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-32B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B) | 未確定 | 32B級推論蒸留の研究資料。元モデルと異なる推論後学習 |
| P1 | [microsoft/phi-4](https://huggingface.co/microsoft/phi-4) | 未確定 | 小型Denseの別系列。個人向け比較基準 |
| 保留 | [deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) | 未確定 | 総約763B。実機RAMと原本容量の見積りが未確定で3.8TB予算への負担大 |

### 無検閲・派生

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0条件 | [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | 55.6 | 現在GatedのBF16重み。独自拒否方向編集と元版を比較 |
| P0 | [JonathanColetti/Qwen3.8-27B-Uncensored](https://huggingface.co/JonathanColetti/Qwen3.8-27B-Uncensored) | 55.6 | Heretic最適化のBF16版。Orca版とは編集方法が異なる |
| P0 | [saidutta69/LFM3-1.7B-heretic](https://huggingface.co/saidutta69/LFM3-1.7B-heretic) | 3.46 | 異種ハイブリッド構造への拒否方向編集。再現レシピも公開 |
| P1 | [AtomicChat/LFM3-1.7B-Uncensored-GGUF](https://huggingface.co/AtomicChat/LFM3-1.7B-Uncensored-GGUF) | 2.72 | 新型LFM3の量子化派生。方法と元版の照合資料 |
| P0条件 | [dphn/Dolphin3.0-Mistral-24B](https://huggingface.co/dphn/Dolphin3.0-Mistral-24B) | 未確定 | Mistral系に独自追加学習したDolphin。元版だけでは学習成果を復元できない |
| P1条件 | [dphn/Dolphin3.0-Llama3.1-8B](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B) | 未確定 | Llama系Dolphin。小容量で独自SFTを記録 |
| P2 | [HauhauCS/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF](https://huggingface.co/HauhauCS/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF) | 未確定 | 高攻撃性の別GGUF調整。最初はBF16派生2種を優先 |
| 保留 | [orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | 336 | 約180BのBF16派生。上流otherと派生Apache表示の適合性を先に検証 |

### LFM・構造多様性

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [LiquidAI/LFM3-1.7B-Base](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | 3.48 | 2026年公開のtri-hybrid事前学習Base。小型で解析しやすい |
| P0 | [LiquidAI/LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) | 3.48 | 同系列の後学習重み。Baseと挙動差を比較 |
| P0 | [LiquidAI/LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B) | 3.84 | LFMの画像理解専門モデル。構造の多様性 |
| P0 | [LiquidAI/LFM3-Audio-2B](https://huggingface.co/LiquidAI/LFM3-Audio-2B) | 4 | LFM音声エンコーダ／生成系の実装を保存 |
| P0 | [LiquidAI/LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B) | 4.33 | 音声・画像・動画入力と音声出力を統合 |
| P1 | [LiquidAI/d1-2B](https://huggingface.co/LiquidAI/d1-2B) | 3.84 | LFM由来の判断・抽出特化後学習重み |
| P1 | [LiquidAI/d1-Omni-2B](https://huggingface.co/LiquidAI/d1-Omni-2B) | 未確定 | 判断系のOmni版。利用目的が独特 |
| P0 | [answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large) | 1.58 | 分類・検索・特徴抽出向けの小型Encoder |
| P0 | [tohoku-nlp/bert-base-japanese-v3](https://huggingface.co/tohoku-nlp/bert-base-japanese-v3) | 未確定 | 日本語BERT。独自データで追加学習しやすい |
| P1 | [microsoft/deberta-v3-base](https://huggingface.co/microsoft/deberta-v3-base) | 未確定 | BERTと異なるEncoder。判別・分類性能比較 |
| P0 | [google-t5/t5-3b](https://huggingface.co/google-t5/t5-3b) | 未確定 | Encoder-Decoderの事前学習構造を保全 |
| P1 | [google/flan-t5-xxl](https://huggingface.co/google/flan-t5-xxl) | 未確定 | Instruction tuning済みEncoder-Decoderの大型比較対象 |
| P0 | [state-spaces/mamba-2.8b](https://huggingface.co/state-spaces/mamba-2.8b) | 未確定 | SSM系でAttention以外の系列を保全 |
| P0 | [RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14.4 | RWKV7の再帰型構造。Transformerと異なる推論特性 |
| P0 | [GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 未確定 | 拡散言語モデルのBase。独自生成方式 |
| P0 | [hazyresearch/ncm-checkpoints](https://huggingface.co/hazyresearch/ncm-checkpoints) | 未確定 | 次概念モデルNCMの段階的生成研究資料 |

### 専門・追加学習

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | 未確定 | 臨床領域の追加学習。監査可能なデータ・レシピ付き |
| P1 | [EPFLiGHT/Apertus-70B-MeditronFO](https://huggingface.co/EPFLiGHT/Apertus-70B-MeditronFO) | 未確定 | 約71Bの異なる医療特化基盤。大容量なので比較価値と予算を審査 |
| P0 | [OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | 66.7 | 画像と医療推論を結びつけた32B SFT。学習トレースの再現コストが大きい |
| P1条件 | [Aikyam-Lab/CURE-MED-32B](https://huggingface.co/Aikyam-Lab/CURE-MED-32B) | 4.3 | 多言語医療推論の専門アダプター。元のQwen2.5-32Bが別途必要 |
| P1条件 | [EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | 未確定 | Llama系列の医療SFT。Gatedと専門学習成果の両面で保全候補 |
| P0 | [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | 54.7 | PC操作・GUIエージェント特化。汎用会話モデルとは異なる行動能力 |
| P1 | [microsoft/AesCode-32B](https://huggingface.co/microsoft/AesCode-32B) | 66.7 | コード開発特化。独自のコード学習成果を候補に |
| P1 | [Qwen/Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | 61.1 | 高効率MoEコード特化。Coder-Nextと用途重複を比較 |
| P1 | [bigcode/starcoder2-15b](https://huggingface.co/bigcode/starcoder2-15b) | 未確定 | コード学習に特化した別系列。独自利用条件を確認 |
| P1条件 | [defog/llama-3-sqlcoder-8b](https://huggingface.co/defog/llama-3-sqlcoder-8b) | 未確定 | 自然言語からSQLへの特化SFT。基盤ライセンスも別途確認 |
| P2 | [microsoft/UserRepGen-4B](https://huggingface.co/microsoft/UserRepGen-4B) | 未確定 | ユーザー表現生成の特化モデル。研究範囲との関連を追加評価 |

### 画像生成・画像編集

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0条件 | [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | 未確定 | 高性能画像生成・編集基盤。現在Gated・独自の非商用条件 |
| P0条件 | [black-forest-labs/FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | 未確定 | 小型版とはライセンスも異なる9B。高品質生成能力 |
| P0 | [black-forest-labs/FLUX.2-klein-4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) | 23.7 | 公開利用条件が明確な別画像生成モデル |
| P0条件 | [ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | 未確定 | Ideogram系列の画像・文字表現。NF4形式で容量要確認 |
| P0条件 | [Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | 未確定 | 新しい画像生成・編集一体型。独自Researchライセンスを精査 |
| P1 | [Qwen/Qwen-Image-2512](https://huggingface.co/Qwen/Qwen-Image-2512) | 未確定 | 以前のApache系列画像生成。後から復元・調整しやすい |
| P0 | [Tongyi-MAI/Z-Image](https://huggingface.co/Tongyi-MAI/Z-Image) | 未確定 | 別構造の小型画像生成。高い保存効率 |
| P1条件 | [stabilityai/stable-diffusion-3.5-large](https://huggingface.co/stabilityai/stable-diffusion-3.5-large) | 未確定 | Stable Diffusion系の大型モデル。Gatedだが画像群の重複を確認 |

### 動画・ワールドモデル

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | 未確定 | 動画生成の小型実用系。テキスト・画像から動画 |
| P1 | [Wan-AI/Wan2.2-T2V-A14B](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B) | 126 | 高品質動画生成系。全リポジトリは126GBと大きい |
| P0条件 | [Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | 未確定 | 22B級映像と音声の同時生成。独自ライセンスと依存を要確認 |
| P0条件 | [nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | 未確定 | Gatedのworld prediction資料。動画生成と物理世界モデリングを分けて保存 |
| P1条件 | [nvidia/Cosmos-Predict2.5-14B](https://huggingface.co/nvidia/Cosmos-Predict2.5-14B) | 未確定 | 大きなworld foundation model。配布リポジトリと依存を審査 |
| P1条件 | [tencent/HunyuanVideo-1.5](https://huggingface.co/tencent/HunyuanVideo-1.5) | 未確定 | Wan・LTXと異なる動画生成系列 |
| P0 | [facebook/vjepa2-vitg-fpc64-384](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384) | 4.14 | 動画から特徴を学ぶ非生成モデル。world modelの基礎研究 |

### 視覚・OCR・分類・検索

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [deepseek-ai/DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | 6.78 | 文書OCR用の特殊視覚言語モデル |
| P0 | [PaddlePaddle/PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | 1.92 | 小容量の文書・表・式認識。別ランタイムを保全 |
| P1 | [zai-org/GLM-OCR](https://huggingface.co/zai-org/GLM-OCR) | 2.65 | 別方式の軽量OCR。比較評価 |
| P0条件 | [facebook/sam3](https://huggingface.co/facebook/sam3) | 未確定 | 画像と動画の領域分割。Gatedで別種の重要能力 |
| P1 | [tencent/WeVisDoc-4B](https://huggingface.co/tencent/WeVisDoc-4B) | 未確定 | 視覚文書処理の専門モデル |
| P1 | [google/siglip2-base-patch16-224](https://huggingface.co/google/siglip2-base-patch16-224) | 未確定 | 視覚Encoderの比較基準 |
| P0 | [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) | 未確定 | 多言語検索と埋め込み。RAG基盤 |
| P0 | [Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 未確定 | 小型Embedding。汎用LLMと異なる重要機能 |
| P0 | [Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | 未確定 | 検索結果の再評価専用。Embeddingだけでは代替できない |
| P1 | [intfloat/multilingual-e5-base](https://huggingface.co/intfloat/multilingual-e5-base) | 未確定 | 多言語Encoder。比較用の検索モデル |

### 音声・ASR・TTS

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | 1.62 | ローカル音声認識・翻訳の実用基準 |
| P0 | [Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | 4.7 | Whisperと異なる日本語対応ASR |
| P0 | [Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | 未確定 | 声質・スタイル指定のTTS専門モデル |
| P0 | [Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) | 未確定 | 声の指定・多言語音声合成の別構成 |
| P0 | [microsoft/VibeVoice-1.5B](https://huggingface.co/microsoft/VibeVoice-1.5B) | 未確定 | 長尺・複数話者TTSの専門構造 |
| P1 | [microsoft/VibeVoice-ASR-Streaming-1.5B](https://huggingface.co/microsoft/VibeVoice-ASR-Streaming-1.5B) | 未確定 | 低遅延ストリーミングASR |
| P0条件 | [nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | 67.5 | 高性能な多言語ASR・翻訳・話者分離。独自条件を精査 |
| P1条件 | [SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS) | 未確定 | 音声生成の別方式。クローン可能性ゆえ利用条件に注意 |
| P1 | [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | 未確定 | 極小TTS。CPU実行比較に有用 |
| P1条件 | [coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2) | 未確定 | 多言語音声クローン特化。独自のライセンスとコード継続性を確認 |

### 科学・時系列

| 優先 | モデル | 表示サイズ概算 GB | 保存する理由 |
| --- | --- | ---: | --- |
| P0 | [facebook/esm2_t33_650M_UR50D](https://huggingface.co/facebook/esm2_t33_650M_UR50D) | 2.61 | タンパク質配列表現。言語LLMとは独立した科学用途 |
| P0 | [autogluon/chronos-2](https://huggingface.co/autogluon/chronos-2) | 0.478 | 時系列予測の専用モデル。小容量で高い補完価値 |
| P0条件 | [google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | 8.6 | 医学特化でGated。臨床利用に適すると未検証の研究資料として保存 |

### データセット・評価

| 優先 | データセット | 表示サイズ概算 GB | 目的 |
| --- | --- | ---: | --- |
| P0 | [HuggingFaceFW/fineweb-edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | 28.5 | FineWeb-Edu 10BT標本を対象。事前学習資料の一部を保存 |
| P0 | [allenai/tulu-3-sft-mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | 未確定 | SFTの大規模混合。各元データのライセンスを別に点検 |
| P0 | [HuggingFaceH4/ultrafeedback_binarized](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized) | 未確定 | DPO/選好最適化用の比較データ |
| P0 | [llm-jp/magpie-sft-v1.0](https://huggingface.co/datasets/llm-jp/magpie-sft-v1.0) | 未確定 | 日本語指示学習データ |
| P0 | [nvidia/OpenCodeInstruct](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) | 6.86 | コード指示学習の再現データ |
| P0 | [nvidia/OpenMathInstruct-2](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) | 12.6 | 数学推論向けの追加学習データ |
| P1 | [project-numina/NuminaMath-1.5](https://huggingface.co/datasets/project-numina/NuminaMath-1.5) | 未確定 | 数学SFTの別データ系統 |
| P0 | [EPFLiGHT/fully-open-meditron](https://huggingface.co/datasets/EPFLiGHT/fully-open-meditron) | 未確定 | MeditronFO再現に関連する医療専門学習データ |
| P1条件 | [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) | 未確定 | 多言語音声データ。全量は巨大でサブセット指定必須 |
| P0 | [elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | 未確定 | 日本語評価用。学習には使用しない |
| P0 | [openai/gsm8k](https://huggingface.co/datasets/openai/gsm8k) | 未確定 | 推論能力の評価用。訓練から分離 |
| P0 | [livecodebench/code_generation_lite](https://huggingface.co/datasets/livecodebench/code_generation_lite) | 未確定 | コード生成能力の独立評価。評価汚染を防ぐ |
| P1条件 | [allenai/dolma3_mix-6T](https://huggingface.co/datasets/allenai/dolma3_mix-6T) | 未確定 | 事前学習の幅を確保。全量でなく法的に利用可能な標本 |
| P1条件 | [uonlp/CulturaX](https://huggingface.co/datasets/uonlp/CulturaX) | 未確定 | 日本語多言語コーパスのサブセット。Gated等を先に確認 |

### 実行・再学習ソフト

| 優先 | ソフト | 意義 |
| --- | --- | --- |
| P0 | llama.cpp | GGUFの量子化・CPU/GPU推論。Windows CPU/Vulkan/CUDA互換ビルドとsource commitを別々に保存 |
| P0 | transformers+tokenizers+safetensors | BF16モデル読込・画像/音声プロセッサ。対応Python wheelsをオフライン保全 |
| P0 | pytorch+CUDA/ROCm wheels | 再学習・各特殊モデルの共通基盤。Windows版とLinux版のABIを区別 |
| P0 | diffusers+ComfyUI | FLUX/Qwen-Image/Wan/LTX画像動画実行。custom nodesは精査 |
| P0 | whisper.cpp+FFmpeg | 音声デコード・ASRと入出力処理の基盤 |
| P1 | vLLM+SGLang | 分散/高速推論。実機OS GPU互換性を確認した版を保管 |
| P0 | PEFT+TRL+LLaMA-Factory+Unsloth | 独自SFT・LoRA・選好学習の再現環境とバージョン固定 |
| P0 | Podman+QEMU+OS installer+GPU drivers | 隔離された実行環境とオフライン再構築 |
| P0 | HuggingFace Hub CLI + Python wheelhouse | 権利を持つ公開モデルの取得と再現可能な依存の保存 |

## 誤認を防ぐためのルール

1. `P0`はダウンロード可能・動作保証・法的利用許可の意味ではない。
2. `P0条件`は利用条件・アカウント承認・特定のコミットと実ファイル・モデルの依存関係を先に確認する。
3. 画像・動画モデルはリポジトリ内の重複量子化版やサブディレクトリを丸ごと足し合わせない。
4. 専門SFTでは基盤重み・LoRAアダプター・学習データ・レシピを関連づける。例：CURE-MEDはアダプターと元モデルを別に管理。
5. 医療モデルや無検閲モデルは安全性が確認されたという主張ではない。保存後の実行も別許可。
6. 3〜4bit理論重み容量だけで512GB RAMに適合するとは判断しない。巨大MoEでは実効ビット率やCPU/GPU offloadを確認。
7. このレビューを`manifests/*.lock.json`の代用にしたり、`queues/approved.json`に自動追加しない。

## 第1回リスク調査の一次資料

- [Hugging Face Gated models](https://huggingface.co/docs/hub/models-gated)
- [Hugging Face Content Policy](https://huggingface.co/content-policy)
- [EU AI Act systemic risk FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-general-purpose-ai-model-one-systemic-risk)
- [Hugging Face Hub download](https://huggingface.co/docs/huggingface_hub/guides/download)

**件数：119件（モデル96、データセット14、ソフト9）。**
**優先度分布：P0: 62、P0条件: 14、P1: 26、P1条件: 13、保留: 2、P2: 2。**
