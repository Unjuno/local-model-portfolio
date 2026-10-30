# 3.8TBオフラインAI：採用・保留の統合ポートフォリオ

> **更新：2026年10月30日／72件。** 具体的な採用理由・配布元への直接リンク・一次資料から確認した公開状態・サイズを記録。これは**選定台帳**であり、ダウンロード承認でもライセンス利用許可でもありません。公開停止リスクを予測確率として断定しません。

## 結論と容量監査

- **統合対象：72件**（R0 13、R1 30、R2 20、HOLD 9）。モデル・データセットの両方。
- **最優先R0の13件：上流リポジトリ内の全ファイル合計 851,771,058,386 バイト（851.771 GB）**。全13件に完全な40文字commit SHAとファイルサイズのスナップショットあり。
- **注意**：この値はリポジトリ内の全ファイル合計で、複数精度・ミラー・関連資料が同居する場合は重複する。**選ぶファイルを固定した実容量ではない**。
- Mistral Large 4は10月29日に公式重みが公開。公式FP8リポジトリ合計約**1,060.61GB**、NVFP4リポジトリ合計約**610.11GB**。実際の3bit系GGUFは配布者による424GB/493GB表示で、512GB RAMとOS/KV等の余裕を実機確認するまで**保留**。上流は[Mistral Large 4](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B)、量子化版は[Unsloth GGUF](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF)。
- [NVIDIA Foundation4D](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D)は全リポジトリ約**9.23TB**で4TB超。契約は自律走行用途等に限定され、旧版の削除義務も規定。**権利確認なしに保存しない。**
- 3.8TBのアーカイブ目標は維持。固定の分野別割当より、将来の再取得困難性・再現困難性を優先する。

## 判定基準

- **R0**：現時点でGatedなど具体的アクセス条件があり、正規の取得可能性・容量・権利を先に確認したい。Gatedは将来削除の証拠ではない。
- **R1**：いま公開中でも独自の専門ファインチューニング、独自の学習データ、Base、画像/動画/音声・ロボットなどの学習成果を失う損失が大きい。
- **R2**：基準モデル・特殊アーキテクチャ・評価データなど、差分解析・再学習のために保存する価値がある。
- **HOLD**：権利・プライバシー・アーキテクチャの互換性・512GB推論条件・4TB物理容量など未解決で、取得承認しない。

## 最新モデル・データの追加（初回65件から7件）

| リンク | 判断 | 何を失うため保存するか | ソース全量（GB） |
| --- | --- | --- | ---: |
| [mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | HOLD / hold | 10月29日に公開された約1Tの画像対応MoE。サイバー防御・コード・エージェント能力の独立重みは失われると復元困難。ただし公式FP8全repo1.06TB、NVFP4でも610GBで、3-4bitの512GB RAM上限適合は未検証。 | 1060.613 |
| [tencent/Hy-SimulMT-30B-A3B](https://huggingface.co/tencent/Hy-SimulMT-30B-A3B) | R1 / conditional | 低遅延の中国語・英語同時翻訳に専門学習した約30B MoE。独立したストリーミング翻訳重みが失われると同じ品質を元ASRからは復元できない。 | 60.858 |
| [Nanbeige/Nanbeige4.3-33B-Base](https://huggingface.co/Nanbeige/Nanbeige4.3-33B-Base) | R1 / select | 10月25日前後に公開された新しい33B級事前学習Base。エージェント教師モデルの出発点となる独自重みで、post-trainedから逆算再現できない。 | 66.241 |
| [Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | R1 / conditional | 33B級Baseから後学習したコード・長期エージェント教師モデル。学習過程・元データがなければ完全再現できない。 | 66.260 |
| [ibm-granite/granite-switch-4.1-30b](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | R1 / select | 4.1.1で改訂された約30Bのモジュラーモデル。Decision aLoRA・Guardian aLoRA・日本語含む7言語音声Encoderという独特の専門部品の組合せを保存する。 | 59.991 |
| [nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D) | HOLD / hold | 自律走行向け実空間データと注釈は収集・再現困難で重要だが、ファイル全量が9.23TBでHDD容量を超える。 | 9225.410 |
| [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) | R1 / conditional | 48言語・16コーパスの音声を再ラベル化した、数十万時間分のASR・翻訳・音声QA向け学習資料。専門的なラベル生成をそのまま再現するのは困難。 | 111.560 |

## 最優先13件：リポジトリの正確な容量と版（取得対象の選択は未了）

| モデルまたはデータ | 取得元全ファイルのバイト数 | 完全commit SHA | 参照 |
| --- | ---: | --- | --- |
| [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | 55,586,066,230 | `0f639a9bde23fe229a7b064b40a5153c5bec0b48` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-1.json) |
| [black-forest-labs/flux-3-image-klein-base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | 43,229,095,576 | `3f7fa5ee22ca1d5a5cc095ac7cc96e6a173b4c86` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-1.json) |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | 177,640,374,395 | `26afe3a78bb242c0a8bb181dcc8937bb16e5c66c` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-reference-and-datasets.json) |
| [ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | 16,117,791,323 | `f664347839e0a87bc495f5c9483cc0014b8e344e` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-1.json) |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | 217,315,708,790 | `14d516bdff6ac06cec40678529222f193386189c` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-1.json) |
| [facebook/dinov3-vit7b16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | 26,864,283,632 | `b80367753773648a6793235ab9c65cdbb029506f` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-1.json) |
| [facebook/sam3](https://huggingface.co/facebook/sam3) | 6,895,093,624 | `3c879f39826c281e95690f02c7821c4de09afae7` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-2.json) |
| [nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | 38,139,108,598 | `f50c09f5d8ab133a90cac3f4886a6471e9ba3f18` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-2.json) |
| [CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | 66,297,944,724 | `0554d66834922fc0f2e5f47a12f78464f4a98533` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-2.json) |
| [google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | 8,639,644,263 | `290cda5eeccbee130f987c4ad74a59ae6f196408` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-2.json) |
| [black-forest-labs/FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | 52,888,736,795 | `92196c8e11f7b6cf2b7493e037d8c5345c559216` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-2.json) |
| [EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | 141,116,879,850 | `1ec3a7ee2355e384149df2e4dd42fed41e7fd08f` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-r0-gated-2.json) |
| [StephaneBah/AfroRadVoice-FR](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | 1,040,330,586 | `eb9200abd571ac4a6616e0ab89501747acb57a2b` | [ファイル台帳](https://github.com/Unjuno/local-model-portfolio/blob/main/catalog/snapshots/2026-10-30-reference-and-datasets.json) |

## 採用理由・根拠を含む全候補

この表は選定の意思決定を可視化したものであり、Gated条件の受諾やダウンロード実行を自動許可しない。リポジトリからの取得・実行は別工程。

### R0（13件）

| 資産 | 判断 | これを選ぶ理由 | 現時点の制約・不確実性 |
| --- | --- | --- | --- |
| [MODEL: orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | conditional | OrcaRouterによる27B級BF16拒否方向編集版。公式の元重みと並べれば編集後の振る舞いと差分を比較でき、第三者配布物そのものの再現は保証されない。 | 現在Gated。将来の公開停止は仮説。元のQwenと単純量子化版ではこの改変済みチェックポイントを代替できない。 |
| [MODEL: black-forest-labs/flux-3-image-klein-base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | conditional | FLUX 3 Kleinの蒸留前Base。高品質生成能力と追加学習の出発点を保存するためで、API利用だけでは内部解析ができない。 | 現在Gatedかつ独自ライセンス。外部エンコーダーなどの依存は未確定。 |
| [MODEL: black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | conditional | 独立した32B級画像生成・画像編集の重み。人物・物体の参照編集などをモデル一式として再現したい。 | 現在Gated、独自非商用ライセンス。リモートエンコーダー依存を別途解消する必要あり。 |
| [MODEL: ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | conditional | Ideogram系の独立画像生成能力、特に画像内テキスト表現の比較に価値がある。FLUXやQwen-Imageだけでは同一の学習済み重みを復元できない。 | 現在Gatedと独自利用条件。NF4形式でありBF16原本とは異なる。 |
| [MODEL: meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | conditional | Meta Llama 4の約109B MoE。QwenやMistralとは異なる学習済みパラメータと設計を研究用に保全する。 | 現在Gated、Llama独自ライセンス。公式配布条件と約512GBピークメモリ制約を確認。 |
| [MODEL: facebook/dinov3-vit7b16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | conditional | 約6.7Bの巨大な自己教師あり視覚Encoder。画像生成とは違う汎用表現学習を再現なしで確保する価値がある。 | 現在Gated・独自ライセンス。事前学習画像の配布権と重みのライセンスは別。 |
| [MODEL: facebook/sam3](https://huggingface.co/facebook/sam3) | conditional | 単なる画像生成では代替しづらいプロンプトによる領域分割能力を保全する。小容量で異なる画像・動画系機能を確保できる。 | 現在Gated、独自の配布条件。実行コードとモデル重みを分けて監査。 |
| [MODEL: nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | conditional | 動画から次の世界状態を予測する世界モデル。汎用言語LLMや一般動画生成器とは異なる学習成果を保存する。 | 現在GatedとNVIDIA独自条件。必要モデル部品と利用目的は未確定。 |
| [MODEL: CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | conditional | 約33Bの多言語・視覚言語モデル。主要英語中心VLMと異なる言語データ由来の能力を保存する。 | 現在Gated、CC-BY-NC。非商用利用の範囲と依存が必要。 |
| [MODEL: google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | conditional | 4B級の医療画像・テキスト特化モデル。専門後学習済み重みは汎用Gemmaから容易に復元できない。 | 現在Gated、Google独自の利用条件。臨床利用の安全性は検証されていない。 |
| [MODEL: black-forest-labs/FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | conditional | FLUX2の9B版という別実装・別重み。画像編集系で大規模devとの特性差を保全できる。 | 現在Gated、独自条件。FLUX3と類似用途なので残余予算で重複審査。 |
| [MODEL: EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | conditional | Llama 3.1由来の70B級医療特化重み。一般のLlamaを残しても専門学習成果はそのまま戻らない。 | 現在Gated、Llama3.1ライセンス。医療モデルであり検証抜き臨床利用不可。 |
| [DATA: StephaneBah/AfroRadVoice-FR](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | conditional | 放射線医療分野の仏語音声と注釈。少数の専門家が作った音声データは再録音・再注釈が難しい。 | 現在Gated。患者・話者の同意、医療音声の利用範囲と匿名性を優先確認。 |

### R1（30件）

| 資産 | 判断 | これを選ぶ理由 | 現時点の制約・不確実性 |
| --- | --- | --- | --- |
| [MODEL: OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | select | 医療画像・推論を対象に独自の多数の学習トレースでSFTした約33Bモデル。Qwen3-VLの元重みだけから再構成できない。 | 現在公開。医療という分野だけで将来の規制を断定しないが再学習資源は重い。 |
| [MODEL: EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | select | 臨床質問・ガイドライン用SFTを施した32B。公開されたMeditronコーパスとレシピを含めて再学習の検証に使える。 | 現在公開・Apache 2.0。独自専門学習が失われた場合の損失を優先する。 |
| [MODEL: EPFLiGHT/Apertus-70B-MeditronFO](https://huggingface.co/EPFLiGHT/Apertus-70B-MeditronFO) | select | OLMoとは異なるApertus 70Bの医学専門調整重み。独自系列の比較で臨床言語の適応差を研究できる。 | 現在公開。70Bなので原本容量と他の医療特化版との重複を精査する。 |
| [MODEL: HuggingFaceBio/Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | select | DNA配列と自然言語を共同学習した約14.8B特殊モデル。独自DNAトークナイザーと学習工程が必要で、Qwen3-14Bだけでは同じ重みを戻せない。 | 現在公開。バイオ能力による提供条件変更は仮説。 |
| [MODEL: microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | select | PC画面を見て操作する27B級GUIエージェントの学習成果。一般会話モデルの重みだけでは行動ポリシーを再現できない。 | 現在公開・MIT。自律操作の提供方針変更は将来シナリオであり実行は別許可。 |
| [MODEL: nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B) | conditional | 人型ロボットVLA制御に特化した約3.3B。実機と合成の操作データを学習した重みで汎用視覚モデルと代替できない。 | 現在公開。NVIDIA独自ライセンス本文と推論依存を精査。 |
| [MODEL: lerobot/pi0_base](https://huggingface.co/lerobot/pi0_base) | conditional | 視覚・言語・行動を統合するπ0系のBase。行動生成のアーキテクチャとロボット学習の比較に価値がある。 | 現在公開。Gemma系ライセンスと元モデル由来の制約を確認。 |
| [MODEL: Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | select | 約80Bのコード・エージェント専用学習済み重み。汎用Qwenを保存しても専用のコード学習成果は自明に戻らない。 | 現在公開。高性能コードAIの将来配布制限は推論。 |
| [MODEL: mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | select | 約119Bの独立したMistral MoE。別系列の高性能言語・マルチモーダル能力と学習成果を保全する。 | 現在公開・Apache 2.0。全repo約242GBは概算、選択ファイルの正確なバイト数未確定。 |
| [MODEL: openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | select | 約117BのMoEとMXFP4形式。QwenやMistralと異なる公開重みの表現・推論実装を比較できる。 | 現在公開・Apache 2.0。量子化済み配布形式をBF16の未配布原本と誤記しない。 |
| [MODEL: Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | conditional | 22B級の動画と音声を統合した生成モデル。独自の映像・音声同期学習を再学習し直すコストが高い。 | 現在公開、ライセンスother。複数checkpointを全取得せず原本と必要な依存だけ選ぶ。 |
| [MODEL: Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | select | 5B級のテキスト・画像からの動画生成。異なる動画生成系列を小さめの容量で保存できる。 | 現在公開・Apache 2.0。VAEやテキストエンコーダー等の依存を含む容量は未確定。 |
| [MODEL: Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | conditional | 約7Bの画像生成・編集モデル。WanやFLUXとは別の学習済みパラメータで独立の研究価値がある。 | 現在公開、ライセンスother。利用条件の本文確認が必要。 |
| [MODEL: nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | conditional | 約34Bの音声認識・翻訳専用MoE。Whisperと異なる大規模音声後学習を保全したい。 | 現在公開・ライセンスother、配布表示約67.5GB。話者情報とモデルコードの利用条件を確認。 |
| [MODEL: Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | select | 声質指定や音声生成に特化したQwenの1.7B級重み。一般LLMやASRでは同じ合成能力を代替できない。 | 現在公開・Apache 2.0。話者同意など利用面の制約とモデル保存を分離する。 |
| [MODEL: microsoft/VibeVoice-1.5B](https://huggingface.co/microsoft/VibeVoice-1.5B) | select | 長尺・複数話者の音声生成に特化した別アーキテクチャ。Qwen TTSと比較可能。 | 現在公開・MIT。音声複製の悪用問題による将来の公開変更は仮説。 |
| [MODEL: LiquidAI/LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B) | conditional | 画像・音声などを統合するLFMのOmniモデル。小容量で独自の非Transformer成分を持つ音声対話を保全できる。 | 現在公開、LFM独自ライセンス。カスタムコードの実行は別許可。 |
| [MODEL: deepseek-ai/DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | select | 文書の文字・構造理解に特化した3.4B。一般VLMとは異なるOCR専用学習成果を保存できる。 | 現在公開・Apache 2.0。実行に必要なカスタム依存は別に検証。 |
| [DATA: IFM/SFT-Reasoning](https://huggingface.co/datasets/IFM/SFT-Reasoning) | conditional | 約4080万行の推論・指示学習データ。IFM K2系列に結びつくSFT工程を再現・比較するために不可欠。 | 現在公開・Apache 2.0のHub表示、repo全体約159GB。素材の権利・個人データ検査を要する。 |
| [DATA: EPFLiGHT/fully-open-meditron](https://huggingface.co/datasets/EPFLiGHT/fully-open-meditron) | select | 専門家監修の医療ガイドライン・QAなどを含む学習データ。MeditronFOの学習成果を説明する資料としてモデルと対にする。 | 現在公開・Apache 2.0。医学の専門性とデータのプライバシー・二次配布条件を分けて精査。 |
| [DATA: CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | select | 多言語人手注釈・再注釈の指示データ。少数言語の品質を後から同水準で確保するには人手のコストがかかる。 | 現在公開・Apache 2.0。各言語の元データ条件を確認する。 |
| [DATA: laion/emotional-roleplay-finetuning-dataset](https://huggingface.co/datasets/laion/emotional-roleplay-finetuning-dataset) | conditional | 感情表現音声と注釈の対を用いるTTS向け専門調整データ。音声だけでなく注釈の再収集が難しい。 | 現在公開・CC-BY-4.0の表示、全repo約6.67GB。声の権利・同意を確認してから取り込む。 |
| [DATA: allenai/pixmo-cap](https://huggingface.co/datasets/allenai/pixmo-cap) | conditional | 人手の詳細な画像キャプション。画像と説明の組み合わせは自動では同一に再構築できない。 | 現在公開・ODC-BY。原画像は外部URLがあり画像素材の権利が別。 |
| [DATA: nvidia/OpenCodeInstruct](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) | select | コード指示学習用の専門データ。コードモデルの追加学習を再現するため重みと対で保全する。 | 現在公開・CC-BY-4.0、表示約6.86GB。元コード由来のライセンスを再確認。 |
| [DATA: nvidia/OpenMathInstruct-2](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) | select | 数学推論向けSFTデータ。問題と解答・推論過程の組を再収集するコストが高い。 | 現在公開・CC-BY-4.0、表示約12.6GB。評価セットの混入を確認。 |
| [MODEL: tencent/Hy-SimulMT-30B-A3B](https://huggingface.co/tencent/Hy-SimulMT-30B-A3B) | conditional | 低遅延の中国語・英語同時翻訳に専門学習した約30B MoE。独立したストリーミング翻訳重みが失われると同じ品質を元ASRからは復元できない。 | 現在公開・Apache 2.0。声の複製に関する将来条件変更は仮説。声の生成と音声出力には別TTSが必要なので完全オフラインは依存選定後。 |
| [MODEL: Nanbeige/Nanbeige4.3-33B-Base](https://huggingface.co/Nanbeige/Nanbeige4.3-33B-Base) | select | 10月25日前後に公開された新しい33B級事前学習Base。エージェント教師モデルの出発点となる独自重みで、post-trainedから逆算再現できない。 | 現在公開・Apache 2.0。高度なエージェント能力への将来制限は仮説。trust_remote_code前提を推論環境と隔離して扱う。 |
| [MODEL: Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | conditional | 33B級Baseから後学習したコード・長期エージェント教師モデル。学習過程・元データがなければ完全再現できない。 | 現在公開・Apache 2.0。Baseとの高精度2本保存は約132.5GBで容量競合があるため重複査定。 |
| [MODEL: ibm-granite/granite-switch-4.1-30b](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | select | 4.1.1で改訂された約30Bのモジュラーモデル。Decision aLoRA・Guardian aLoRA・日本語含む7言語音声Encoderという独特の専門部品の組合せを保存する。 | 現在公開・Apache 2.0。公開停止予告なし。アダプターやEncoderの改訂後、旧版を再取得できなくなる可能性があるため版固定の価値がある。 |
| [DATA: nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) | conditional | 48言語・16コーパスの音声を再ラベル化した、数十万時間分のASR・翻訳・音声QA向け学習資料。専門的なラベル生成をそのまま再現するのは困難。 | 現在公開。元コーパスごとのライセンスが混在するため許諾されたsplitのみ選択。全repo111.56GB。 |

### R2（20件）

| 資産 | 判断 | これを選ぶ理由 | 現時点の制約・不確実性 |
| --- | --- | --- | --- |
| [MODEL: Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | select | Qwen系列の約27.8B公式マルチモーダル重み。Orca等の無検閲派生と重み差分・性能差を測定する比較原本として不可欠。 | 現在公開・Apache 2.0。消失リスクの高いGated派生より緊急度は低いが対応付ける。 |
| [MODEL: google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) | select | Gemma系列31Bの事前学習基準重み。Qwenとは異なる系列のBaseの選択肢を維持する。 | 現在公開・Apache 2.0。後学習ITは優先的には重複を避ける。 |
| [MODEL: Qwen/Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | select | 約36BのMoE事前学習Base。元重みがあれば新しいSFT・LoRA実験をやり直せる。 | 現在公開・Apache 2.0。派生量子化全件の重複保存はしない。 |
| [MODEL: allenai/Olmo-3-1125-32B](https://huggingface.co/allenai/Olmo-3-1125-32B) | select | AllenAIによる公開度の高い32B級系列。学習過程と検証可能性を別系統の比較対象として残す。 | 現在公開・Apache 2.0。名前だけでBaseとは断定せず学習段階を検証。 |
| [MODEL: LiquidAI/LFM3-1.7B-Base](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | conditional | 独特のハイブリッド構造を持つ小型事前学習Base。Attention以外の系列を解析・追加学習する原本になる。 | 現在公開、LFM独自ライセンス。動作にカスタムコードが必要か確認。 |
| [MODEL: RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | select | RWKV7の再帰型言語モデル。通常Transformerと異なる推論計算・状態保持を比較できる。 | 現在公開・Apache 2.0。ランタイムの対応版を保管。 |
| [MODEL: GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | select | トークン逐次生成ではない拡散言語モデルのBase。生成方式の多様性を保全する。 | 現在公開・Apache 2.0。専用デコードコードも必要。 |
| [MODEL: state-spaces/mamba-2.8b](https://huggingface.co/state-spaces/mamba-2.8b) | select | SSM系の基礎重み。Self-Attention以外のモデルを長期保存するための代表。 | 現在公開・Apache 2.0。専用ランタイムと固定する。 |
| [MODEL: facebook/vjepa2-vitg-fpc64-384](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384) | select | 動画から表現を学習する非生成型モデル。動画生成器にはない動画特徴抽出・世界理解の能力を確保する。 | 現在公開・Apache 2.0。動作環境・事前処理を保存。 |
| [MODEL: PaddlePaddle/PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | select | 小型かつ異なるOCR/文書解析実装。大きなDeepSeek-OCRが動かない環境でも推論と比較ができる。 | 現在公開・Apache 2.0。Paddle依存を別管理。 |
| [MODEL: openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | select | 小容量で汎用多言語ASRを確保する実用基準。高価な専門音声モデルとの比較に使う。 | 現在公開・MIT。消失リスクはGated音声データより低い。 |
| [MODEL: Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | select | Whisperとは異なる音声認識系統を低容量で確保し多言語比較に使う。 | 現在公開・Apache 2.0。言語別性能を実測で確認。 |
| [MODEL: answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large) | select | 分類・検索用のEncoder-only原本を確保し、LLM以外のファインチューニングを可能にする。 | 現在公開・Apache 2.0。生成モデルでは代替しづらい効率を比較。 |
| [MODEL: BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) | select | 埋め込み・多言語検索の専門モデル。大規模生成モデルと異なるretrievalタスクを保存する。 | 現在公開・MIT。研究価値はあるが配布停止の兆候は未確認。 |
| [DATA: HuggingFaceFW/fineweb-edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | conditional | 事前学習の教師なしテキストを部分保存し、モデルの再学習可能性を維持する。 | 巨大な多版・多構成dataset。例示した28.5GBを全体容量とせず許諾されたsubsetを選ぶ。 |
| [DATA: allenai/tulu-3-sft-mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | conditional | 汎用指示学習を再現するための混合データ。専門SFTとの差分対照として必要。 | 現在公開・ODC-BYメタデータ。元の各構成データの利用条件を再確認。 |
| [DATA: HuggingFaceH4/ultrafeedback_binarized](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized) | select | DPO等の選好学習比較データ。後学習の再現可能性と拒否挙動の解析に必要。 | 現在公開・MIT。元の比較データセットと学習/評価の汚染を点検。 |
| [DATA: llm-jp/magpie-sft-v1.0](https://huggingface.co/datasets/llm-jp/magpie-sft-v1.0) | select | 日本語SFTデータ。英語中心データで代用できない日本語分布を保存する。 | 現在公開・Apache 2.0。学習/評価セットを分ける。 |
| [DATA: elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | select | 日本語の独立評価用。保存する日本語モデルの品質を将来も比較するため不可欠。 | 現在公開・CC-BY-SA。絶対に学習用と混在させず評価専用で保管。 |
| [DATA: lerobot/aloha_sim_insertion_human](https://huggingface.co/datasets/lerobot/aloha_sim_insertion_human) | select | ロボット操作デモデータ。GR00Tやπ0の制御研究で行動を追跡できる。 | 現在公開・MIT。モデルの具体的な学習データと同一ではないことを明記する。 |

### HOLD（9件）

| 資産 | 判断 | これを選ぶ理由 | 現時点の制約・不確実性 |
| --- | --- | --- | --- |
| [DATA: bigcode/the-stack-v2](https://huggingface.co/datasets/bigcode/the-stack-v2) | hold | 大規模コード事前学習データ。ソースライセンス・帰属・削除履歴を含む研究価値は高い。 | 現在Gated。一括取得にはSoftware Heritage/INRIAとの別途契約、削除要求後の利用可能版への追随義務が明示される。 |
| [DATA: bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata) | hold | 別時代の多言語コード学習データ。出典付きの大量コードとして再現価値が高い。 | 現在Gated。元コードの権利と有効版の更新義務があり、永久保存条件は未確認。 |
| [DATA: amphion/Emilia-Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset) | hold | 多数話者音声と注釈からなるTTS学習データ。再取得・再注釈のコストが高い。 | 現在Gated。HubのCC-BY-4.0表示と本体に関する同意画面のCC-BY-NCが不一致。 |
| [DATA: lmsys/lmsys-chat-1m](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | hold | 大規模な人間-LLM対話ログ。再収集が難しい研究資産。 | 現在Gated。個人情報・同意・権利条件が未確認のため無条件保存不可。 |
| [DATA: laion/relaion2B-en-research](https://huggingface.co/datasets/laion/relaion2B-en-research) | hold | 大規模画像・文章ペアを含む学習用資料。入手可能性と権利情報が重要。 | 現在Gated、既存表示約481GB。各画像の権利と収集目的・削除要求への対応が未検証。 |
| [DATA: allenai/WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M) | hold | 実際のユーザー対話記録に基づくSFT候補で貴重な自然発話分布を含む。 | 現在公開でも会話ログのプライバシーと同意について詳細確認なしでは取り込まない。 |
| [MODEL: orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | hold | 約180B級MoEの拒否方向編集済みBF16原本。小さなLLMでは比較できない改変研究価値がある。 | 現在Gated、上流Qwen3.8-Flash-Nextのlicense metadata otherと派生のApache表示が異なる。原本約336GBを無条件取得しない。 |
| [MODEL: mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | hold | 10月29日に公開された約1Tの画像対応MoE。サイバー防御・コード・エージェント能力の独立重みは失われると復元困難。ただし公式FP8全repo1.06TB、NVFP4でも610GBで、3-4bitの512GB RAM上限適合は未検証。 | 現在公開・独自Mistral Ecosystemライセンス。高性能による提供変更は仮説。Unsloth約3bit GGUFは424/493GBとの自己表示で、OS・KV・mmprojの追加メモリを含む実測が必要。 |
| [DATA: nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D) | hold | 自律走行向け実空間データと注釈は収集・再現困難で重要だが、ファイル全量が9.23TBでHDD容量を超える。 | 現在Gated・NVIDIA独自契約。NVIDIA技術を用いた自律走行開発等に用途限定、権利者による旧版削除要求の規定あり。長期アーカイブと契約の適合が確認できないため取得不可。 |

## 未実施と次の具体的作業

- 現在の**モデルダウンロード承認キューは空**。原本重み・音声・データセットの取得は行っていない。
- 13件の上流メタデータに完全commit SHAとファイルサイズはあるが、**選択対象の確定・実機RAM試験・権利条件の最終確認**が必要。
- データセットのSource Licensesとプライバシー/削除条件を優先確認する。データ権利が未解決のHOLDは明確に除外。
- 3.8TB予算は、重複表現・外部エンコーダー・依存コードを除いた実際の選択ファイルのバイト数で再計算する。

## 一次資料

- [Hugging Face Content Policy](https://huggingface.co/content-policy)
- [Hugging Face Gated Models](https://huggingface.co/docs/hub/models-gated)
- [Mistral Large 4 official release blog (2026-10-29)](https://huggingface.co/blog/mistral-large4)
- [The Stack v2 dataset access conditions](https://huggingface.co/datasets/bigcode/the-stack-v2)
- [NVIDIA Foundation4D dataset license conditions](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D)
