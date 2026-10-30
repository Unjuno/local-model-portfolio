# AI保存ポートフォリオ：採用候補の統合判定（2026-10-30）

> **ここで選定を進める。** 119件の一次レビューと29件のリスク調査から、**「何を・なぜ・どこから保存するか」を具体的に比較して選んだ一覧**。取得承認は含まず、ユーザーの4TB HDDには何も保存していない。現在Gatedでも、今後削除される確証とは扱わない。

## 採用の順序

**R0：現時点で取得条件が制約されているもの。** 正規アクセスの有無・ライセンス・別契約・容量を最優先で確認する。

**R1：公開中でも独自の学習成果やデータを再現しづらいもの。** 専門SFT、医療、科学、コード・GUIエージェント、動画・音声など。

**R2：比較原本・構造多様性・学習/評価基盤。** R0/R1に必要な元モデルは順番を繰り上げる。

**HOLD：重要だが権利・個人情報・ライセンス不一致が未解決。** 『先に取得しておく』ことは許可しない。

## 4TB制約を確認する方法

- 保存ターゲットは3,800GB（十進）、最低空きは200GB（十進）。**用途別の固定割当は廃止し、消失リスクの高い資産へ優先配分**。
- 量子化3〜4bitでのピーク推論RAMが512GB（十進）未満となるか、backend・コンテキスト・KVキャッシュ・OS・実装オーバーヘッドを含めて評価する。モデルの総パラメータ数では一律除外しない。
- 下記の『表示容量』は参考。**モデルやデータセットごとのダウンロードファイル選定とバイト単位の実容量集計が未完了なので、3.8TBに収まったとは主張しない**。Gated重みはモデルカード、付属物、依存実装を別に確認する。
- ライセンス/Gatedへの同意、個人情報、学習データの権利は取得・再配布と区別して確認する。**現時点で取得キューは空**。

## 件数：65資産

R0 13件、R1 25件、R2 20件、HOLD 7件。採用候補 33件、条件付き 25件、権利等で保留 7件。

## R0：既にGated等の具体的制限がある／供給元が限られるため先に権利・取得可能性を調べる。将来削除の予告ではない。

| 順 | モデル・データセット | 保存する具体的理由 | 現時点の状態 / 課題 |
| ---: | --- | --- | --- |
| 1 | [MODEL: orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | OrcaRouterによる27B級BF16拒否方向編集版。公式の元重みと並べれば編集後の振る舞いと差分を比較でき、第三者配布物そのものの再現は保証されない。 | 現在Gated。将来の公開停止は仮説。元のQwenと単純量子化版ではこの改変済みチェックポイントを代替できない。 |
| 2 | [MODEL: black-forest-labs/flux-3-image-klein-base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | FLUX 3 Kleinの蒸留前Base。高品質生成能力と追加学習の出発点を保存するためで、API利用だけでは内部解析ができない。 | 現在Gatedかつ独自ライセンス。外部エンコーダーなどの依存は未確定。 |
| 3 | [MODEL: black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | 独立した32B級画像生成・画像編集の重み。人物・物体の参照編集などをモデル一式として再現したい。 | 現在Gated、独自非商用ライセンス。リモートエンコーダー依存を別途解消する必要あり。 |
| 4 | [MODEL: ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | Ideogram系の独立画像生成能力、特に画像内テキスト表現の比較に価値がある。FLUXやQwen-Imageだけでは同一の学習済み重みを復元できない。 | 現在Gatedと独自利用条件。NF4形式でありBF16原本とは異なる。 |
| 5 | [MODEL: meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | Meta Llama 4の約109B MoE。QwenやMistralとは異なる学習済みパラメータと設計を研究用に保全する。 | 現在Gated、Llama独自ライセンス。公式配布条件と約512GBピークメモリ制約を確認。 |
| 6 | [MODEL: facebook/dinov3-vit7b16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | 約6.7Bの巨大な自己教師あり視覚Encoder。画像生成とは違う汎用表現学習を再現なしで確保する価値がある。 | 現在Gated・独自ライセンス。事前学習画像の配布権と重みのライセンスは別。 |
| 7 | [MODEL: facebook/sam3](https://huggingface.co/facebook/sam3) | 単なる画像生成では代替しづらいプロンプトによる領域分割能力を保全する。小容量で異なる画像・動画系機能を確保できる。 | 現在Gated、独自の配布条件。実行コードとモデル重みを分けて監査。 |
| 8 | [MODEL: nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | 動画から次の世界状態を予測する世界モデル。汎用言語LLMや一般動画生成器とは異なる学習成果を保存する。 | 現在GatedとNVIDIA独自条件。必要モデル部品と利用目的は未確定。 |
| 9 | [MODEL: CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | 約33Bの多言語・視覚言語モデル。主要英語中心VLMと異なる言語データ由来の能力を保存する。 | 現在Gated、CC-BY-NC。非商用利用の範囲と依存が必要。 |
| 10 | [MODEL: google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | 4B級の医療画像・テキスト特化モデル。専門後学習済み重みは汎用Gemmaから容易に復元できない。 | 現在Gated、Google独自の利用条件。臨床利用の安全性は検証されていない。 |
| 11 | [MODEL: black-forest-labs/FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | FLUX2の9B版という別実装・別重み。画像編集系で大規模devとの特性差を保全できる。 | 現在Gated、独自条件。FLUX3と類似用途なので残余予算で重複審査。 |
| 12 | [MODEL: EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | Llama 3.1由来の70B級医療特化重み。一般のLlamaを残しても専門学習成果はそのまま戻らない。 | 現在Gated、Llama3.1ライセンス。医療モデルであり検証抜き臨床利用不可。 |
| 13 | [DATA: StephaneBah/AfroRadVoice-FR](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | 放射線医療分野の仏語音声と注釈。少数の専門家が作った音声データは再録音・再注釈が難しい。 | 現在Gated。患者・話者の同意、医療音声の利用範囲と匿名性を優先確認。 |

## R1：現在公開でも専門SFT・独自データ・特殊能力などの再現が難しいため保存候補として優先する。

| 順 | モデル・データセット | 保存する具体的理由 | 現時点の状態 / 課題 |
| ---: | --- | --- | --- |
| 14 | [MODEL: OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | 医療画像・推論を対象に独自の多数の学習トレースでSFTした約33Bモデル。Qwen3-VLの元重みだけから再構成できない。 | 現在公開。医療という分野だけで将来の規制を断定しないが再学習資源は重い。 |
| 15 | [MODEL: EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | 臨床質問・ガイドライン用SFTを施した32B。公開されたMeditronコーパスとレシピを含めて再学習の検証に使える。 | 現在公開・Apache 2.0。独自専門学習が失われた場合の損失を優先する。 |
| 16 | [MODEL: EPFLiGHT/Apertus-70B-MeditronFO](https://huggingface.co/EPFLiGHT/Apertus-70B-MeditronFO) | OLMoとは異なるApertus 70Bの医学専門調整重み。独自系列の比較で臨床言語の適応差を研究できる。 | 現在公開。70Bなので原本容量と他の医療特化版との重複を精査する。 |
| 17 | [MODEL: HuggingFaceBio/Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | DNA配列と自然言語を共同学習した約14.8B特殊モデル。独自DNAトークナイザーと学習工程が必要で、Qwen3-14Bだけでは同じ重みを戻せない。 | 現在公開。バイオ能力による提供条件変更は仮説。 |
| 18 | [MODEL: microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | PC画面を見て操作する27B級GUIエージェントの学習成果。一般会話モデルの重みだけでは行動ポリシーを再現できない。 | 現在公開・MIT。自律操作の提供方針変更は将来シナリオであり実行は別許可。 |
| 19 | [MODEL: nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B) | 人型ロボットVLA制御に特化した約3.3B。実機と合成の操作データを学習した重みで汎用視覚モデルと代替できない。 | 現在公開。NVIDIA独自ライセンス本文と推論依存を精査。 |
| 20 | [MODEL: lerobot/pi0_base](https://huggingface.co/lerobot/pi0_base) | 視覚・言語・行動を統合するπ0系のBase。行動生成のアーキテクチャとロボット学習の比較に価値がある。 | 現在公開。Gemma系ライセンスと元モデル由来の制約を確認。 |
| 21 | [MODEL: Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 約80Bのコード・エージェント専用学習済み重み。汎用Qwenを保存しても専用のコード学習成果は自明に戻らない。 | 現在公開。高性能コードAIの将来配布制限は推論。 |
| 22 | [MODEL: mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 約119Bの独立したMistral MoE。別系列の高性能言語・マルチモーダル能力と学習成果を保全する。 | 現在公開・Apache 2.0。全repo約242GBは概算、選択ファイルの正確なバイト数未確定。 |
| 23 | [MODEL: openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | 約117BのMoEとMXFP4形式。QwenやMistralと異なる公開重みの表現・推論実装を比較できる。 | 現在公開・Apache 2.0。量子化済み配布形式をBF16の未配布原本と誤記しない。 |
| 24 | [MODEL: Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | 22B級の動画と音声を統合した生成モデル。独自の映像・音声同期学習を再学習し直すコストが高い。 | 現在公開、ライセンスother。複数checkpointを全取得せず原本と必要な依存だけ選ぶ。 |
| 25 | [MODEL: Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | 5B級のテキスト・画像からの動画生成。異なる動画生成系列を小さめの容量で保存できる。 | 現在公開・Apache 2.0。VAEやテキストエンコーダー等の依存を含む容量は未確定。 |
| 26 | [MODEL: Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | 約7Bの画像生成・編集モデル。WanやFLUXとは別の学習済みパラメータで独立の研究価値がある。 | 現在公開、ライセンスother。利用条件の本文確認が必要。 |
| 27 | [MODEL: nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | 約34Bの音声認識・翻訳専用MoE。Whisperと異なる大規模音声後学習を保全したい。 | 現在公開・ライセンスother、配布表示約67.5GB。話者情報とモデルコードの利用条件を確認。 |
| 28 | [MODEL: Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | 声質指定や音声生成に特化したQwenの1.7B級重み。一般LLMやASRでは同じ合成能力を代替できない。 | 現在公開・Apache 2.0。話者同意など利用面の制約とモデル保存を分離する。 |
| 29 | [MODEL: microsoft/VibeVoice-1.5B](https://huggingface.co/microsoft/VibeVoice-1.5B) | 長尺・複数話者の音声生成に特化した別アーキテクチャ。Qwen TTSと比較可能。 | 現在公開・MIT。音声複製の悪用問題による将来の公開変更は仮説。 |
| 30 | [MODEL: LiquidAI/LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B) | 画像・音声などを統合するLFMのOmniモデル。小容量で独自の非Transformer成分を持つ音声対話を保全できる。 | 現在公開、LFM独自ライセンス。カスタムコードの実行は別許可。 |
| 31 | [MODEL: deepseek-ai/DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | 文書の文字・構造理解に特化した3.4B。一般VLMとは異なるOCR専用学習成果を保存できる。 | 現在公開・Apache 2.0。実行に必要なカスタム依存は別に検証。 |
| 32 | [DATA: IFM/SFT-Reasoning](https://huggingface.co/datasets/IFM/SFT-Reasoning) | 約4080万行の推論・指示学習データ。IFM K2系列に結びつくSFT工程を再現・比較するために不可欠。 | 現在公開・Apache 2.0のHub表示、repo全体約159GB。素材の権利・個人データ検査を要する。 |
| 33 | [DATA: EPFLiGHT/fully-open-meditron](https://huggingface.co/datasets/EPFLiGHT/fully-open-meditron) | 専門家監修の医療ガイドライン・QAなどを含む学習データ。MeditronFOの学習成果を説明する資料としてモデルと対にする。 | 現在公開・Apache 2.0。医学の専門性とデータのプライバシー・二次配布条件を分けて精査。 |
| 34 | [DATA: CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 多言語人手注釈・再注釈の指示データ。少数言語の品質を後から同水準で確保するには人手のコストがかかる。 | 現在公開・Apache 2.0。各言語の元データ条件を確認する。 |
| 35 | [DATA: laion/emotional-roleplay-finetuning-dataset](https://huggingface.co/datasets/laion/emotional-roleplay-finetuning-dataset) | 感情表現音声と注釈の対を用いるTTS向け専門調整データ。音声だけでなく注釈の再収集が難しい。 | 現在公開・CC-BY-4.0の表示、全repo約6.67GB。声の権利・同意を確認してから取り込む。 |
| 36 | [DATA: allenai/pixmo-cap](https://huggingface.co/datasets/allenai/pixmo-cap) | 人手の詳細な画像キャプション。画像と説明の組み合わせは自動では同一に再構築できない。 | 現在公開・ODC-BY。原画像は外部URLがあり画像素材の権利が別。 |
| 37 | [DATA: nvidia/OpenCodeInstruct](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) | コード指示学習用の専門データ。コードモデルの追加学習を再現するため重みと対で保全する。 | 現在公開・CC-BY-4.0、表示約6.86GB。元コード由来のライセンスを再確認。 |
| 38 | [DATA: nvidia/OpenMathInstruct-2](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) | 数学推論向けSFTデータ。問題と解答・推論過程の組を再収集するコストが高い。 | 現在公開・CC-BY-4.0、表示約12.6GB。評価セットの混入を確認。 |

## R2：後からでも再入手しやすい可能性があるが比較原本や再学習基盤として有用。

| 順 | モデル・データセット | 保存する具体的理由 | 現時点の状態 / 課題 |
| ---: | --- | --- | --- |
| 39 | [MODEL: Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | Qwen系列の約27.8B公式マルチモーダル重み。Orca等の無検閲派生と重み差分・性能差を測定する比較原本として不可欠。 | 現在公開・Apache 2.0。消失リスクの高いGated派生より緊急度は低いが対応付ける。 |
| 40 | [MODEL: google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) | Gemma系列31Bの事前学習基準重み。Qwenとは異なる系列のBaseの選択肢を維持する。 | 現在公開・Apache 2.0。後学習ITは優先的には重複を避ける。 |
| 41 | [MODEL: Qwen/Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | 約36BのMoE事前学習Base。元重みがあれば新しいSFT・LoRA実験をやり直せる。 | 現在公開・Apache 2.0。派生量子化全件の重複保存はしない。 |
| 42 | [MODEL: allenai/Olmo-3-1125-32B](https://huggingface.co/allenai/Olmo-3-1125-32B) | AllenAIによる公開度の高い32B級系列。学習過程と検証可能性を別系統の比較対象として残す。 | 現在公開・Apache 2.0。名前だけでBaseとは断定せず学習段階を検証。 |
| 43 | [MODEL: LiquidAI/LFM3-1.7B-Base](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | 独特のハイブリッド構造を持つ小型事前学習Base。Attention以外の系列を解析・追加学習する原本になる。 | 現在公開、LFM独自ライセンス。動作にカスタムコードが必要か確認。 |
| 44 | [MODEL: RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | RWKV7の再帰型言語モデル。通常Transformerと異なる推論計算・状態保持を比較できる。 | 現在公開・Apache 2.0。ランタイムの対応版を保管。 |
| 45 | [MODEL: GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | トークン逐次生成ではない拡散言語モデルのBase。生成方式の多様性を保全する。 | 現在公開・Apache 2.0。専用デコードコードも必要。 |
| 46 | [MODEL: state-spaces/mamba-2.8b](https://huggingface.co/state-spaces/mamba-2.8b) | SSM系の基礎重み。Self-Attention以外のモデルを長期保存するための代表。 | 現在公開・Apache 2.0。専用ランタイムと固定する。 |
| 47 | [MODEL: facebook/vjepa2-vitg-fpc64-384](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384) | 動画から表現を学習する非生成型モデル。動画生成器にはない動画特徴抽出・世界理解の能力を確保する。 | 現在公開・Apache 2.0。動作環境・事前処理を保存。 |
| 48 | [MODEL: PaddlePaddle/PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | 小型かつ異なるOCR/文書解析実装。大きなDeepSeek-OCRが動かない環境でも推論と比較ができる。 | 現在公開・Apache 2.0。Paddle依存を別管理。 |
| 49 | [MODEL: openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | 小容量で汎用多言語ASRを確保する実用基準。高価な専門音声モデルとの比較に使う。 | 現在公開・MIT。消失リスクはGated音声データより低い。 |
| 50 | [MODEL: Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | Whisperとは異なる音声認識系統を低容量で確保し多言語比較に使う。 | 現在公開・Apache 2.0。言語別性能を実測で確認。 |
| 51 | [MODEL: answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large) | 分類・検索用のEncoder-only原本を確保し、LLM以外のファインチューニングを可能にする。 | 現在公開・Apache 2.0。生成モデルでは代替しづらい効率を比較。 |
| 52 | [MODEL: BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) | 埋め込み・多言語検索の専門モデル。大規模生成モデルと異なるretrievalタスクを保存する。 | 現在公開・MIT。研究価値はあるが配布停止の兆候は未確認。 |
| 53 | [DATA: HuggingFaceFW/fineweb-edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | 事前学習の教師なしテキストを部分保存し、モデルの再学習可能性を維持する。 | 巨大な多版・多構成dataset。例示した28.5GBを全体容量とせず許諾されたsubsetを選ぶ。 |
| 54 | [DATA: allenai/tulu-3-sft-mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | 汎用指示学習を再現するための混合データ。専門SFTとの差分対照として必要。 | 現在公開・ODC-BYメタデータ。元の各構成データの利用条件を再確認。 |
| 55 | [DATA: HuggingFaceH4/ultrafeedback_binarized](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized) | DPO等の選好学習比較データ。後学習の再現可能性と拒否挙動の解析に必要。 | 現在公開・MIT。元の比較データセットと学習/評価の汚染を点検。 |
| 56 | [DATA: llm-jp/magpie-sft-v1.0](https://huggingface.co/datasets/llm-jp/magpie-sft-v1.0) | 日本語SFTデータ。英語中心データで代用できない日本語分布を保存する。 | 現在公開・Apache 2.0。学習/評価セットを分ける。 |
| 57 | [DATA: elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | 日本語の独立評価用。保存する日本語モデルの品質を将来も比較するため不可欠。 | 現在公開・CC-BY-SA。絶対に学習用と混在させず評価専用で保管。 |
| 58 | [DATA: lerobot/aloha_sim_insertion_human](https://huggingface.co/datasets/lerobot/aloha_sim_insertion_human) | ロボット操作デモデータ。GR00Tやπ0の制御研究で行動を追跡できる。 | 現在公開・MIT。モデルの具体的な学習データと同一ではないことを明記する。 |

## HOLD：権利・プライバシー・ライセンス矛盾が解消するまでダウンロードしない。

| 順 | モデル・データセット | 保存する具体的理由 | 現時点の状態 / 課題 |
| ---: | --- | --- | --- |
| 59 | [DATA: bigcode/the-stack-v2](https://huggingface.co/datasets/bigcode/the-stack-v2) | 大規模コード事前学習データ。ソースライセンス・帰属・削除履歴を含む研究価値は高い。 | 現在Gated。一括取得にはSoftware Heritage/INRIAとの別途契約、削除要求後の利用可能版への追随義務が明示される。 |
| 60 | [DATA: bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata) | 別時代の多言語コード学習データ。出典付きの大量コードとして再現価値が高い。 | 現在Gated。元コードの権利と有効版の更新義務があり、永久保存条件は未確認。 |
| 61 | [DATA: amphion/Emilia-Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset) | 多数話者音声と注釈からなるTTS学習データ。再取得・再注釈のコストが高い。 | 現在Gated。HubのCC-BY-4.0表示と本体に関する同意画面のCC-BY-NCが不一致。 |
| 62 | [DATA: lmsys/lmsys-chat-1m](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | 大規模な人間-LLM対話ログ。再収集が難しい研究資産。 | 現在Gated。個人情報・同意・権利条件が未確認のため無条件保存不可。 |
| 63 | [DATA: laion/relaion2B-en-research](https://huggingface.co/datasets/laion/relaion2B-en-research) | 大規模画像・文章ペアを含む学習用資料。入手可能性と権利情報が重要。 | 現在Gated、既存表示約481GB。各画像の権利と収集目的・削除要求への対応が未検証。 |
| 64 | [DATA: allenai/WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M) | 実際のユーザー対話記録に基づくSFT候補で貴重な自然発話分布を含む。 | 現在公開でも会話ログのプライバシーと同意について詳細確認なしでは取り込まない。 |
| 65 | [MODEL: orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | 約180B級MoEの拒否方向編集済みBF16原本。小さなLLMでは比較できない改変研究価値がある。 | 現在Gated、上流Qwen3.8-Flash-Nextのlicense metadata otherと派生のApache表示が異なる。原本約336GBを無条件取得しない。 |

## 差分・未解決事項

- すべての採用候補について配布元の直接リンクと『なぜ選んだか』を記述し、単純な人気順を採用理由にしない。
- R0の多くはGatedで、利用権限を持っていても利用条件・ファイル全件・推論実装の確認が必要。
- 特にThe Stack v2では一括取得の別契約と削除要請後の版更新、EmiliaではHub表示と同意条件のライセンス差異、LMSYS/WildChatでは個人情報・同意を解決しない限り承認不可。
- 初回119件とリスク監視29件のいずれの台帳も消さず、統合した優先採用結果を別ファイルとして保持する。モデル・データの実体はGitHubには置かない。

## 一次資料

- [Hugging Face Content Policy](https://huggingface.co/content-policy) — 公開制限と禁止対象の基本規定
- [Gated models](https://huggingface.co/docs/hub/models-gated) — 権限付き配布の公式説明
- [The Stack v2 dataset](https://huggingface.co/datasets/bigcode/the-stack-v2) — 一括利用の個別契約と削除要求に関する記載
- [Emilia Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset) — 同意条件のライセンス
- [Hugging Face Hub files/download](https://huggingface.co/docs/huggingface_hub/guides/download) — 取得内容と改訂版の固定

**正確なファイル一覧・ライセンス本文・保管条件の確認は続行が必要。取得承認マニフェスト0件、実データ取得0件。**
