# AIオフライン保存ポートフォリオ（現行版）

**調査日：2026年10月30日／全97資産。** モデルとデータを同じ基準で、正規の再取得が難しくなる恐れ・学習成果の独自性・小容量での業務代替可能性に基づいて選ぶ。これは選定台帳であり、ダウンロード承認・実行許可・ライセンス確認完了ではありません。

## 最新の25件：小型モデル・専門業務の代替可能性

実際の産業への影響と将来の規制は**仮説**です。性能数値が配布者によるものは第三者による独立検証を行っていません。

| 配布元モデル・データセット | 上流全ファイル GB | どういう価値があり、何を代替し得るか | 条件・限界 |
| --- | ---: | --- | --- |
| [lightonai/LightOnOCR-3-0.8B](https://huggingface.co/lightonai/LightOnOCR-3-0.8B) | 1.738 | **採用理由：** 文書OCR・表・数式・図表・ページ領域検出を0.8B級で統合した専用重み。以前は複数のOCR/レイアウト認識工程を組み合わせた作業の一部を単体で担える。 **仕事：** 文書電子化・フォーム処理・経理入力などの前処理を小型でローカル化する可能性。企業業務全体の自動化や精度優位は未実証。 | 2026年10月の新モデル。Apache 2.0公開。作者の比較評価は独立再試験前で、将来の産業影響・規制は仮説。 |
| [lightonai/LightOnOCR-3-4B](https://huggingface.co/lightonai/LightOnOCR-3-4B) | 9.110 | **採用理由：** LightOnOCR-3の4B高精度系チェックポイント。0.8B版と違う精度・コスト特性を保全し、複雑な文書解析の再学習成果を比較できる。 **仕事：** 法律・製造・医療文書など複雑なレイアウト解析パイプラインの一部を置換する可能性。小型版と重複が多い。 | 現在公開・Apache 2.0。4Bが常に優れるという一般化は禁止。0.8Bとの別重み保存の必要性を予算と実測で判断。 |
| [ibm-granite/granite-speech-5.0-470m-turboctc](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) | 0.949 | **採用理由：** 日本語を含む7言語に対応する470Mの高速CTC音声認識器。多言語句読点付き文字起こしを低メモリで再現する原本として有用。 **仕事：** 有料文字起こし・議事録・字幕工程の音声→テキスト部分をオンデバイスで置換する可能性。 | 2026年10月21日更新・Apache 2.0。IBMの精度数値は公開評価条件での報告で、日本語の実使用品質は未測定。 |
| [ibm-granite/granite-speech-5.0-2b](https://huggingface.co/ibm-granite/granite-speech-5.0-2b) | 5.050 | **採用理由：** 約2.3Bの多言語ASR・双方向音声翻訳とキーワードバイアスに特化した重み。日本語の専門語を含む音声処理に使える。 **仕事：** 翻訳・会議文字起こしAPIの一部を自前で動かす可能性。470M版にはない翻訳・長文処理の能力がある。 | 2026年10月公開・Apache 2.0。TTS音声合成は別モデル、IBM公表ベンチは実測未検証。 |
| [nvidia/nemotron-labs-unified-asr-0.6b](https://huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b) | 2.509 | **採用理由：** 約0.6Bの欧州25言語対応ASR。オフラインとストリーミングを同一重みで扱い、低遅延処理を比較できる。 **仕事：** ライブ字幕・多言語会議ソフトの認識エンジン部分に利用可能性。 | 2026年10月27日公開。Hub licenseはother。160msは作者のアルゴリズム上の最短遅延で、端末実測ではない。日本語非対応。 |
| [qvac/TranscribePsy-250M-EU](https://huggingface.co/qvac/TranscribePsy-250M-EU) | 2.039 | **採用理由：** わずか254Mの欧州多言語音声認識重み。端末内の処理を優先し、同系の0.6Bモデルより小さな教師蒸留成果を保存できる。 **仕事：** 携帯端末の音声入力・字幕・オフライン文字起こしの部品。 | 2026年10月公開・Apache 2.0。手機での高速性は配布者による6機種評価。日本語は対象外で、GGUF/CoreML版は別リポジトリ。 |
| [black-forest-labs/flux-3-image-klein](https://huggingface.co/black-forest-labs/flux-3-image-klein) | 43.318 | **採用理由：** FLUX.3 Image Kleinの蒸留済み5.6B画像生成・編集重み。Baseと違い少ステップ推論に最適化されており、蒸留済みの学習成果はBaseからの単純変換で復元できない。 **仕事：** 画像編集・商品画像・レイアウト制御のクラウドAPI代替に寄与する可能性。 | 2026年10月公開、現在Gated・独自FLUXライセンス。必要なprompt upsamplerとQwen3-VL-4BテキストEncoderは別部品。 |
| [bytedance-research/Lance](https://huggingface.co/bytedance-research/Lance) | 30.857 | **採用理由：** 約3Bで画像/動画の理解・生成・編集を統合した独特のマルチタスク研究モデル。複数機能を小容量にまとめた学習レシピと原本の保存価値が高い。 **仕事：** 動画編集や画像生成と理解を一体化した試作業務の研究基盤。 | 2026年5月公開・Apache 2.0。配布者自身が研究プロジェクトと説明し、品質や速度は商用成熟を保証しない。 |
| [PerceptronAI/Isaac-0.2-2B-Preview](https://huggingface.co/PerceptronAI/Isaac-0.2-2B-Preview) | 10.285 | **採用理由：** 約2.57BのVLM。Focusツールによる拡大確認・複雑OCR・画面理解を兼ね備え、汎用LLMより小型で視覚作業に特化する。 **仕事：** 産業検査・文書処理・GUI視覚解析の一部を省メモリで代替する可能性。 | 現在公開だがCC-BY-NC-4.0。性能が10倍大きいモデル以上という表現は配布者の主張で、評価条件を固定した独立検証は未了。 |
| [ACERobotics/Puffin-World](https://huggingface.co/ACERobotics/Puffin-World) | 67.016 | **採用理由：** 画像から重力・深度・見た目を統合した3D世界状態を推論・生成する独自世界モデル。RGB動画生成器だけでは同じ幾何表現を復元できない。 **仕事：** 3Dシミュレーション・ロボット検証・画像からの仮想環境復元の研究用途。 | 現在公開・NTU S-Lab独自ライセンス。約67GBは全repo容量。構成要素が複数で、実際の性能は研究段階。 |
| [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16.237 | **採用理由：** 約4Bの画像→3Dメッシュ・物理ベース材質生成重み。通常の画像・動画生成とは違い編集可能な3D形状が出力できるため、失うと再学習負担が大きい。 **仕事：** 3Dアセット制作・商品設計の初期形状作成・ゲーム用モデルの原案生成を補助する可能性。 | 現在公開・HubライセンスMIT。工業設計精度・商用アセットの権利適合は未検証で、工程全体の代替を断定しない。 |
| [tencent/Hunyuan3D-2.1](https://huggingface.co/tencent/Hunyuan3D-2.1) | 14.910 | **採用理由：** 画像から材質を伴う3Dアセットを生成する独立系列。TRELLIS2とは異なるパイプラインと学習済み形状生成能力を保全する。 **仕事：** 3Dモデリング・商品可視化・ゲーム素材制作の前処理を支援できる可能性。 | 現在公開・ライセンスother。TRELLIS2と重複するためライセンス・品質・所要GPU/容量を比較してから採否を絞る。 |
| [Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | 32.900 | **採用理由：** 6B級の蒸留済み高速画像生成モデル。8 NFEを標準とする小型で独自の生成品質・レイアウト学習を保全できる。 **仕事：** 広告用画像・商品イメージ・制作素材のAPI依存を減らす可能性。 | 現在公開・Apache 2.0。H800上sub-secondは作者の測定条件に限定、CPUや一般GPUで保証しない。 |
| [autogluon/chronos-2](https://huggingface.co/autogluon/chronos-2) | 0.478 | **採用理由：** 約120Mのゼロショット時系列予測モデル。Encoder-onlyで共変量・複数時系列を扱い、LLMとは別の意思決定機能を小容量で保全する。 **仕事：** 需要予測・在庫予測・運用データの予測サービスの一部をローカル化する可能性。 | 現在公開・Apache 2.0。GPU性能数値は特定の測定条件に依存し、金融運用の優位は証明していない。 |
| [Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | 2.498 | **採用理由：** 0.6B級の10言語対応音声合成・話し方制御モデル。日本語音声を含み、汎用LLMでは持たない音声生成機能を小容量で保存できる。 **仕事：** ナレーション・アクセシビリティ・字幕読み上げのAPI代替に寄与する可能性。 | 現在公開・Apache 2.0。話者同意と著作権を守る。97msの配布者報告はエンドツーエンド性能の一般保証ではない。 |
| [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 0.915 | **採用理由：** 約450MのVLA Base。画像・状態・言語から連続ロボット動作を出す軽量学習済み重みで、ロボット特化Fine-tuneの土台になる。 **仕事：** 小規模ロボットの研究・操作学習を専用大型モデルなしで試せる可能性。 | 現在公開・Apache 2.0。実機の安全性・転移精度や産業での動作保証は未検証。 |
| [Qwen/Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct) | 4.267 | **採用理由：** 約2.13Bの小型VLM。画像・画面の読解や簡易なGUI認識を軽量に実装する基準原本として有用。 **仕事：** 画像検索・フォーム読解・画面補助AIのローカル実装に使える可能性。 | 現在公開・Apache 2.0。同じQwen系列の27Bに比べ能力は限定されるが、容量と推論メモリが小さい。 |
| [Wigtn/Qwen3-VL-2B-WigtnOCR](https://huggingface.co/Wigtn/Qwen3-VL-2B-WigtnOCR) | 4.290 | **採用理由：** 30B教師からの擬似ラベル蒸留で、韓国政府文書のレイアウト・表を2Bへ適応した専門OCR。単なる元Qwen3-VL-2B重みではこの調整を復元できない。 **仕事：** 韓国語公文書・業務帳票のOCR/構造抽出を小規模サーバーで処理する可能性。 | 現在公開。OmniDocBench等の比較は作者報告で、特化データの汚染・著作権・他言語への転用は未検証。 |
| [tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | 60.144 | **採用理由：** 約30B総数/約3Bアクティブの長期エージェント記憶書き込み専門MoE。メモリ更新方針を専門的な蒸留・強化学習で学んでいる。 **仕事：** 長期チャット・業務支援エージェントのメモリ管理基盤を汎用LLM呼出しから専用モデルへ置換する可能性。 | 現在公開・Apache 2.0。外部Memory frameworkの実装が前提で、端末での効果・コスト削減は独立検証前。 |
| [Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 1.207 | **採用理由：** 約0.6Bの多言語埋め込みモデル。汎用会話モデルとは別の意味検索用の表現学習済み重みで、RAGの基盤を小容量で保存できる。 **仕事：** 検索インデックス・社内文書の意味検索のAPI依存を減らす可能性。 | 現在公開・Apache 2.0。生成LLMでは代用しにくいが、BGE-M3など既存候補との冗長度は比較する。 |
| [Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | 1.207 | **採用理由：** 約0.6Bの検索結果再順位付け専門モデル。Embedding単独では行わない問い合わせと候補文書の関連度判定を軽量に行う。 **仕事：** 検索品質向上の外部Reranker APIを置換する可能性。 | 現在公開・Apache 2.0。再順位付けは検索全体の代替ではなく、遅延・候補件数に依存。 |
| [facebook/esm2_t33_650M_UR50D](https://huggingface.co/facebook/esm2_t33_650M_UR50D) | 7.824 | **採用理由：** 約650Mのタンパク質配列Encoder。汎用自然言語LLMでは保持しない生物配列の学習済み表現をオフラインで利用できる。 **仕事：** バイオインフォマティクスの特徴抽出・候補分子解析を支援する可能性。 | 現在公開・MIT。予測された特徴は実験的なタンパク質機能の保証ではない。 |
| [google/siglip2-base-patch16-224](https://huggingface.co/google/siglip2-base-patch16-224) | 1.539 | **採用理由：** 約375Mの視覚Encoder。画像検索・分類と多言語画像テキスト類似度の構成要素として小容量で価値がある。 **仕事：** メディア検索・画像分類パイプラインの一部を軽量に構築できる可能性。 | 現在公開・Apache 2.0。大型VLMの生成能力を持たず、独立した視覚特徴抽出用。 |
| [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | 1.770 | **採用理由：** 0.8B級の汎用後学習モデル。最小構成のCPU/端末推論や、他の専用モデルの統合評価用の小型基準として保存する。 **仕事：** 単純な分類・事務補助・オフライン対話などで大規模クラウドLLMへの依存を一部下げる可能性。 | 現在公開・Apache 2.0。これは事前学習直後のBaseと確認されていないためBaseとは呼ばず、品質の制約を明示。 |
| [Wigtn/KoGovDoc-Bench](https://huggingface.co/datasets/Wigtn/KoGovDoc-Bench) | 0.112 | **採用理由：** 韓国政府文書のレイアウト・OCR/検索評価用の専門注釈データ。WigtnOCRの蒸留成果を独立検証する参照データで、再注釈が困難。 **仕事：** 文書自動化・公文書検索の現実的な性能評価を維持する研究資料。 | 現在公開・HubライセンスApache 2.0。原画像・行政文書の著作権と個人情報、モデル評価汚染は別途確認。 |

## リスクと容量の現在地

| 区分 | 件数 | 完全な改訂SHAと上流全ファイル容量が確認できた数 | 既知の上流全ファイル合計 GB |
| --- | ---: | ---: | ---: |
| R0 | 14 | 14/14 | 895.089 |
| R1 | 47 | 47/47 | 2103.209 |
| R2 | 27 | 26/27（残りはFineWebサブセット） | 369.399 GB（部分合計） |
| HOLD | 9 | 取得対象外 | 除外 |

R0は既にGated等の制限がある候補。R1は専門SFT・別系列・実用性の高い小型モデル・希少データ。R2は比較用原本と軽量実用基盤。HOLDは権利・プライバシー・実行メモリ/容量など未解決。

**FineWeb-Eduは全repoを容量計画に含めない。** `sample/10BT` 14ファイルの合計 **28,518,193,415バイト（28.518GB）**を別に確定し、[厳密なファイル一覧とrevision](../catalog/snapshots/2026-10-30-fineweb-edu-10bt-subset.json)に記録した。残るR2はそのサブセットの扱いだけで、原repo全量の容量は未計上。

**現時点の監査済み上流全repo容量の部分合計は3,367.697GB。** FineWeb-Eduの10BTを加えると **3,396.215GB** だが、これはソフト・外部依存・一時領域が未確定のため、3.8TBに必ず収まると保証するものではない。原本や形式を選び、重複を除いた実容量で判断する。

**重要：** 上流の全ファイル容量は、同一チェックポイントの別精度、別形式や補助資料を含む場合があり、これらの合計は**HDDへ選んで保存する容量ではありません**。3.8TBへの収容と512GB実メモリへの適合は、実ファイルと依存物を選んだ後に判定します。利用許諾のないGated資産は取得しません。

## 全97件：何をなぜ選んだか、リンク、制限

### R0（14件）

| 直接リンク | 採用判断 | 採用理由 | 取得上の課題・将来の不確実性 |
| --- | --- | --- | --- |
| [MODEL orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | conditional | OrcaRouterによる27B級BF16拒否方向編集版。公式の元重みと並べれば編集後の振る舞いと差分を比較でき、第三者配布物そのものの再現は保証されない。 | gated。現在Gated。将来の公開停止は仮説。元のQwenと単純量子化版ではこの改変済みチェックポイントを代替できない。 |
| [MODEL black-forest-labs/flux-3-image-klein-base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | conditional | FLUX 3 Kleinの蒸留前Base。高品質生成能力と追加学習の出発点を保存するためで、API利用だけでは内部解析ができない。 | gated。現在Gatedかつ独自ライセンス。外部エンコーダーなどの依存は未確定。 |
| [MODEL black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | conditional | 独立した32B級画像生成・画像編集の重み。人物・物体の参照編集などをモデル一式として再現したい。 | gated。現在Gated、独自非商用ライセンス。リモートエンコーダー依存を別途解消する必要あり。 |
| [MODEL ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | conditional | Ideogram系の独立画像生成能力、特に画像内テキスト表現の比較に価値がある。FLUXやQwen-Imageだけでは同一の学習済み重みを復元できない。 | gated。現在Gatedと独自利用条件。NF4形式でありBF16原本とは異なる。 |
| [MODEL meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | conditional | Meta Llama 4の約109B MoE。QwenやMistralとは異なる学習済みパラメータと設計を研究用に保全する。 | gated。現在Gated、Llama独自ライセンス。公式配布条件と約512GBピークメモリ制約を確認。 |
| [MODEL facebook/dinov3-vit7b16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | conditional | 約6.7Bの巨大な自己教師あり視覚Encoder。画像生成とは違う汎用表現学習を再現なしで確保する価値がある。 | gated。現在Gated・独自ライセンス。事前学習画像の配布権と重みのライセンスは別。 |
| [MODEL facebook/sam3](https://huggingface.co/facebook/sam3) | conditional | 単なる画像生成では代替しづらいプロンプトによる領域分割能力を保全する。小容量で異なる画像・動画系機能を確保できる。 | gated。現在Gated、独自の配布条件。実行コードとモデル重みを分けて監査。 |
| [MODEL nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | conditional | 動画から次の世界状態を予測する世界モデル。汎用言語LLMや一般動画生成器とは異なる学習成果を保存する。 | gated。現在GatedとNVIDIA独自条件。必要モデル部品と利用目的は未確定。 |
| [MODEL CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | conditional | 約33Bの多言語・視覚言語モデル。主要英語中心VLMと異なる言語データ由来の能力を保存する。 | gated。現在Gated、CC-BY-NC。非商用利用の範囲と依存が必要。 |
| [MODEL google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | conditional | 4B級の医療画像・テキスト特化モデル。専門後学習済み重みは汎用Gemmaから容易に復元できない。 | gated。現在Gated、Google独自の利用条件。臨床利用の安全性は検証されていない。 |
| [MODEL black-forest-labs/FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | conditional | FLUX2の9B版という別実装・別重み。画像編集系で大規模devとの特性差を保全できる。 | gated。現在Gated、独自条件。FLUX3と類似用途なので残余予算で重複審査。 |
| [MODEL EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | conditional | Llama 3.1由来の70B級医療特化重み。一般のLlamaを残しても専門学習成果はそのまま戻らない。 | gated。現在Gated、Llama3.1ライセンス。医療モデルであり検証抜き臨床利用不可。 |
| [DATA StephaneBah/AfroRadVoice-FR](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | conditional | 放射線医療分野の仏語音声と注釈。少数の専門家が作った音声データは再録音・再注釈が難しい。 | gated。現在Gated。患者・話者の同意、医療音声の利用範囲と匿名性を優先確認。 |
| [MODEL black-forest-labs/flux-3-image-klein](https://huggingface.co/black-forest-labs/flux-3-image-klein) | conditional | FLUX.3 Image Kleinの蒸留済み5.6B画像生成・編集重み。Baseと違い少ステップ推論に最適化されており、蒸留済みの学習成果はBaseからの単純変換で復元できない。 | gated。2026年10月公開、現在Gated・独自FLUXライセンス。必要なprompt upsamplerとQwen3-VL-4BテキストEncoderは別部品。 |

### R1（47件）

| 直接リンク | 採用判断 | 採用理由 | 取得上の課題・将来の不確実性 |
| --- | --- | --- | --- |
| [MODEL OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | select | 医療画像・推論を対象に独自の多数の学習トレースでSFTした約33Bモデル。Qwen3-VLの元重みだけから再構成できない。 | public。現在公開。医療という分野だけで将来の規制を断定しないが再学習資源は重い。 |
| [MODEL EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | select | 臨床質問・ガイドライン用SFTを施した32B。公開されたMeditronコーパスとレシピを含めて再学習の検証に使える。 | public。現在公開・Apache 2.0。独自専門学習が失われた場合の損失を優先する。 |
| [MODEL EPFLiGHT/Apertus-70B-MeditronFO](https://huggingface.co/EPFLiGHT/Apertus-70B-MeditronFO) | select | OLMoとは異なるApertus 70Bの医学専門調整重み。独自系列の比較で臨床言語の適応差を研究できる。 | public。現在公開。70Bなので原本容量と他の医療特化版との重複を精査する。 |
| [MODEL HuggingFaceBio/Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | select | DNA配列と自然言語を共同学習した約14.8B特殊モデル。独自DNAトークナイザーと学習工程が必要で、Qwen3-14Bだけでは同じ重みを戻せない。 | public。現在公開。バイオ能力による提供条件変更は仮説。 |
| [MODEL microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | select | PC画面を見て操作する27B級GUIエージェントの学習成果。一般会話モデルの重みだけでは行動ポリシーを再現できない。 | public。現在公開・MIT。自律操作の提供方針変更は将来シナリオであり実行は別許可。 |
| [MODEL nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B) | conditional | 人型ロボットVLA制御に特化した約3.3B。実機と合成の操作データを学習した重みで汎用視覚モデルと代替できない。 | public。現在公開。NVIDIA独自ライセンス本文と推論依存を精査。 |
| [MODEL lerobot/pi0_base](https://huggingface.co/lerobot/pi0_base) | conditional | 視覚・言語・行動を統合するπ0系のBase。行動生成のアーキテクチャとロボット学習の比較に価値がある。 | public。現在公開。Gemma系ライセンスと元モデル由来の制約を確認。 |
| [MODEL Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | select | 約80Bのコード・エージェント専用学習済み重み。汎用Qwenを保存しても専用のコード学習成果は自明に戻らない。 | public。現在公開。高性能コードAIの将来配布制限は推論。 |
| [MODEL mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | select | 約119Bの独立したMistral MoE。別系列の高性能言語・マルチモーダル能力と学習成果を保全する。 | public。現在公開・Apache 2.0。全repo約242GBは概算、選択ファイルの正確なバイト数未確定。 |
| [MODEL openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | select | 約117BのMoEとMXFP4形式。QwenやMistralと異なる公開重みの表現・推論実装を比較できる。 | public。現在公開・Apache 2.0。量子化済み配布形式をBF16の未配布原本と誤記しない。 |
| [MODEL Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | conditional | 22B級の動画と音声を統合した生成モデル。独自の映像・音声同期学習を再学習し直すコストが高い。 | public。現在公開、ライセンスother。複数checkpointを全取得せず原本と必要な依存だけ選ぶ。 |
| [MODEL Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | select | 5B級のテキスト・画像からの動画生成。異なる動画生成系列を小さめの容量で保存できる。 | public。現在公開・Apache 2.0。VAEやテキストエンコーダー等の依存を含む容量は未確定。 |
| [MODEL Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | conditional | 約7Bの画像生成・編集モデル。WanやFLUXとは別の学習済みパラメータで独立の研究価値がある。 | public。現在公開、ライセンスother。利用条件の本文確認が必要。 |
| [MODEL nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | conditional | 約34Bの音声認識・翻訳専用MoE。Whisperと異なる大規模音声後学習を保全したい。 | public。現在公開・ライセンスother、配布表示約67.5GB。話者情報とモデルコードの利用条件を確認。 |
| [MODEL Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | select | 声質指定や音声生成に特化したQwenの1.7B級重み。一般LLMやASRでは同じ合成能力を代替できない。 | public。現在公開・Apache 2.0。話者同意など利用面の制約とモデル保存を分離する。 |
| [MODEL microsoft/VibeVoice-1.5B](https://huggingface.co/microsoft/VibeVoice-1.5B) | select | 長尺・複数話者の音声生成に特化した別アーキテクチャ。Qwen TTSと比較可能。 | public。現在公開・MIT。音声複製の悪用問題による将来の公開変更は仮説。 |
| [MODEL LiquidAI/LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B) | conditional | 画像・音声などを統合するLFMのOmniモデル。小容量で独自の非Transformer成分を持つ音声対話を保全できる。 | public。現在公開、LFM独自ライセンス。カスタムコードの実行は別許可。 |
| [MODEL deepseek-ai/DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | select | 文書の文字・構造理解に特化した3.4B。一般VLMとは異なるOCR専用学習成果を保存できる。 | public。現在公開・Apache 2.0。実行に必要なカスタム依存は別に検証。 |
| [DATA IFM/SFT-Reasoning](https://huggingface.co/datasets/IFM/SFT-Reasoning) | conditional | 約4080万行の推論・指示学習データ。IFM K2系列に結びつくSFT工程を再現・比較するために不可欠。 | public。現在公開・Apache 2.0のHub表示、repo全体約159GB。素材の権利・個人データ検査を要する。 |
| [DATA EPFLiGHT/fully-open-meditron](https://huggingface.co/datasets/EPFLiGHT/fully-open-meditron) | select | 専門家監修の医療ガイドライン・QAなどを含む学習データ。MeditronFOの学習成果を説明する資料としてモデルと対にする。 | public。現在公開・Apache 2.0。医学の専門性とデータのプライバシー・二次配布条件を分けて精査。 |
| [DATA CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | select | 多言語人手注釈・再注釈の指示データ。少数言語の品質を後から同水準で確保するには人手のコストがかかる。 | public。現在公開・Apache 2.0。各言語の元データ条件を確認する。 |
| [DATA laion/emotional-roleplay-finetuning-dataset](https://huggingface.co/datasets/laion/emotional-roleplay-finetuning-dataset) | conditional | 感情表現音声と注釈の対を用いるTTS向け専門調整データ。音声だけでなく注釈の再収集が難しい。 | public。現在公開・CC-BY-4.0の表示、全repo約6.67GB。声の権利・同意を確認してから取り込む。 |
| [DATA allenai/pixmo-cap](https://huggingface.co/datasets/allenai/pixmo-cap) | conditional | 人手の詳細な画像キャプション。画像と説明の組み合わせは自動では同一に再構築できない。 | public。現在公開・ODC-BY。原画像は外部URLがあり画像素材の権利が別。 |
| [DATA nvidia/OpenCodeInstruct](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) | select | コード指示学習用の専門データ。コードモデルの追加学習を再現するため重みと対で保全する。 | public。現在公開・CC-BY-4.0、表示約6.86GB。元コード由来のライセンスを再確認。 |
| [DATA nvidia/OpenMathInstruct-2](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) | select | 数学推論向けSFTデータ。問題と解答・推論過程の組を再収集するコストが高い。 | public。現在公開・CC-BY-4.0、表示約12.6GB。評価セットの混入を確認。 |
| [MODEL tencent/Hy-SimulMT-30B-A3B](https://huggingface.co/tencent/Hy-SimulMT-30B-A3B) | conditional | 低遅延の中国語・英語同時翻訳に専門学習した約30B MoE。独立したストリーミング翻訳重みが失われると同じ品質を元ASRからは復元できない。 | public。現在公開・Apache 2.0。声の複製に関する将来条件変更は仮説。声の生成と音声出力には別TTSが必要なので完全オフラインは依存選定後。 |
| [MODEL Nanbeige/Nanbeige4.3-33B-Base](https://huggingface.co/Nanbeige/Nanbeige4.3-33B-Base) | select | 10月25日前後に公開された新しい33B級事前学習Base。エージェント教師モデルの出発点となる独自重みで、post-trainedから逆算再現できない。 | public。現在公開・Apache 2.0。高度なエージェント能力への将来制限は仮説。trust_remote_code前提を推論環境と隔離して扱う。 |
| [MODEL Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | conditional | 33B級Baseから後学習したコード・長期エージェント教師モデル。学習過程・元データがなければ完全再現できない。 | public。現在公開・Apache 2.0。Baseとの高精度2本保存は約132.5GBで容量競合があるため重複査定。 |
| [MODEL ibm-granite/granite-switch-4.1-30b](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | select | 4.1.1で改訂された約30Bのモジュラーモデル。Decision aLoRA・Guardian aLoRA・日本語含む7言語音声Encoderという独特の専門部品の組合せを保存する。 | public。現在公開・Apache 2.0。公開停止予告なし。アダプターやEncoderの改訂後、旧版を再取得できなくなる可能性があるため版固定の価値がある。 |
| [DATA nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) | conditional | 48言語・16コーパスの音声を再ラベル化した、数十万時間分のASR・翻訳・音声QA向け学習資料。専門的なラベル生成をそのまま再現するのは困難。 | public。現在公開。元コーパスごとのライセンスが混在するため許諾されたsplitのみ選択。全repo111.56GB。 |
| [MODEL lightonai/LightOnOCR-3-0.8B](https://huggingface.co/lightonai/LightOnOCR-3-0.8B) | select | 文書OCR・表・数式・図表・ページ領域検出を0.8B級で統合した専用重み。以前は複数のOCR/レイアウト認識工程を組み合わせた作業の一部を単体で担える。 | public。2026年10月の新モデル。Apache 2.0公開。作者の比較評価は独立再試験前で、将来の産業影響・規制は仮説。 |
| [MODEL lightonai/LightOnOCR-3-4B](https://huggingface.co/lightonai/LightOnOCR-3-4B) | conditional | LightOnOCR-3の4B高精度系チェックポイント。0.8B版と違う精度・コスト特性を保全し、複雑な文書解析の再学習成果を比較できる。 | public。現在公開・Apache 2.0。4Bが常に優れるという一般化は禁止。0.8Bとの別重み保存の必要性を予算と実測で判断。 |
| [MODEL ibm-granite/granite-speech-5.0-470m-turboctc](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) | select | 日本語を含む7言語に対応する470Mの高速CTC音声認識器。多言語句読点付き文字起こしを低メモリで再現する原本として有用。 | public。2026年10月21日更新・Apache 2.0。IBMの精度数値は公開評価条件での報告で、日本語の実使用品質は未測定。 |
| [MODEL ibm-granite/granite-speech-5.0-2b](https://huggingface.co/ibm-granite/granite-speech-5.0-2b) | select | 約2.3Bの多言語ASR・双方向音声翻訳とキーワードバイアスに特化した重み。日本語の専門語を含む音声処理に使える。 | public。2026年10月公開・Apache 2.0。TTS音声合成は別モデル、IBM公表ベンチは実測未検証。 |
| [MODEL bytedance-research/Lance](https://huggingface.co/bytedance-research/Lance) | conditional | 約3Bで画像/動画の理解・生成・編集を統合した独特のマルチタスク研究モデル。複数機能を小容量にまとめた学習レシピと原本の保存価値が高い。 | public。2026年5月公開・Apache 2.0。配布者自身が研究プロジェクトと説明し、品質や速度は商用成熟を保証しない。 |
| [MODEL PerceptronAI/Isaac-0.2-2B-Preview](https://huggingface.co/PerceptronAI/Isaac-0.2-2B-Preview) | conditional | 約2.57BのVLM。Focusツールによる拡大確認・複雑OCR・画面理解を兼ね備え、汎用LLMより小型で視覚作業に特化する。 | public。現在公開だがCC-BY-NC-4.0。性能が10倍大きいモデル以上という表現は配布者の主張で、評価条件を固定した独立検証は未了。 |
| [MODEL ACERobotics/Puffin-World](https://huggingface.co/ACERobotics/Puffin-World) | conditional | 画像から重力・深度・見た目を統合した3D世界状態を推論・生成する独自世界モデル。RGB動画生成器だけでは同じ幾何表現を復元できない。 | public。現在公開・NTU S-Lab独自ライセンス。約67GBは全repo容量。構成要素が複数で、実際の性能は研究段階。 |
| [MODEL microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | select | 約4Bの画像→3Dメッシュ・物理ベース材質生成重み。通常の画像・動画生成とは違い編集可能な3D形状が出力できるため、失うと再学習負担が大きい。 | public。現在公開・HubライセンスMIT。工業設計精度・商用アセットの権利適合は未検証で、工程全体の代替を断定しない。 |
| [MODEL tencent/Hunyuan3D-2.1](https://huggingface.co/tencent/Hunyuan3D-2.1) | conditional | 画像から材質を伴う3Dアセットを生成する独立系列。TRELLIS2とは異なるパイプラインと学習済み形状生成能力を保全する。 | public。現在公開・ライセンスother。TRELLIS2と重複するためライセンス・品質・所要GPU/容量を比較してから採否を絞る。 |
| [MODEL Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | select | 6B級の蒸留済み高速画像生成モデル。8 NFEを標準とする小型で独自の生成品質・レイアウト学習を保全できる。 | public。現在公開・Apache 2.0。H800上sub-secondは作者の測定条件に限定、CPUや一般GPUで保証しない。 |
| [MODEL autogluon/chronos-2](https://huggingface.co/autogluon/chronos-2) | select | 約120Mのゼロショット時系列予測モデル。Encoder-onlyで共変量・複数時系列を扱い、LLMとは別の意思決定機能を小容量で保全する。 | public。現在公開・Apache 2.0。GPU性能数値は特定の測定条件に依存し、金融運用の優位は証明していない。 |
| [MODEL Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | select | 0.6B級の10言語対応音声合成・話し方制御モデル。日本語音声を含み、汎用LLMでは持たない音声生成機能を小容量で保存できる。 | public。現在公開・Apache 2.0。話者同意と著作権を守る。97msの配布者報告はエンドツーエンド性能の一般保証ではない。 |
| [MODEL lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | select | 約450MのVLA Base。画像・状態・言語から連続ロボット動作を出す軽量学習済み重みで、ロボット特化Fine-tuneの土台になる。 | public。現在公開・Apache 2.0。実機の安全性・転移精度や産業での動作保証は未検証。 |
| [MODEL Wigtn/Qwen3-VL-2B-WigtnOCR](https://huggingface.co/Wigtn/Qwen3-VL-2B-WigtnOCR) | conditional | 30B教師からの擬似ラベル蒸留で、韓国政府文書のレイアウト・表を2Bへ適応した専門OCR。単なる元Qwen3-VL-2B重みではこの調整を復元できない。 | public。現在公開。OmniDocBench等の比較は作者報告で、特化データの汚染・著作権・他言語への転用は未検証。 |
| [MODEL tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | select | 約30B総数/約3Bアクティブの長期エージェント記憶書き込み専門MoE。メモリ更新方針を専門的な蒸留・強化学習で学んでいる。 | public。現在公開・Apache 2.0。外部Memory frameworkの実装が前提で、端末での効果・コスト削減は独立検証前。 |
| [MODEL facebook/esm2_t33_650M_UR50D](https://huggingface.co/facebook/esm2_t33_650M_UR50D) | select | 約650Mのタンパク質配列Encoder。汎用自然言語LLMでは保持しない生物配列の学習済み表現をオフラインで利用できる。 | public。現在公開・MIT。予測された特徴は実験的なタンパク質機能の保証ではない。 |
| [DATA Wigtn/KoGovDoc-Bench](https://huggingface.co/datasets/Wigtn/KoGovDoc-Bench) | conditional | 韓国政府文書のレイアウト・OCR/検索評価用の専門注釈データ。WigtnOCRの蒸留成果を独立検証する参照データで、再注釈が困難。 | public。現在公開・HubライセンスApache 2.0。原画像・行政文書の著作権と個人情報、モデル評価汚染は別途確認。 |

### R2（27件）

| 直接リンク | 採用判断 | 採用理由 | 取得上の課題・将来の不確実性 |
| --- | --- | --- | --- |
| [MODEL Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | select | Qwen系列の約27.8B公式マルチモーダル重み。Orca等の無検閲派生と重み差分・性能差を測定する比較原本として不可欠。 | public。現在公開・Apache 2.0。消失リスクの高いGated派生より緊急度は低いが対応付ける。 |
| [MODEL google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) | select | Gemma系列31Bの事前学習基準重み。Qwenとは異なる系列のBaseの選択肢を維持する。 | public。現在公開・Apache 2.0。後学習ITは優先的には重複を避ける。 |
| [MODEL Qwen/Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | select | 約36BのMoE事前学習Base。元重みがあれば新しいSFT・LoRA実験をやり直せる。 | public。現在公開・Apache 2.0。派生量子化全件の重複保存はしない。 |
| [MODEL allenai/Olmo-3-1125-32B](https://huggingface.co/allenai/Olmo-3-1125-32B) | select | AllenAIによる公開度の高い32B級系列。学習過程と検証可能性を別系統の比較対象として残す。 | public。現在公開・Apache 2.0。名前だけでBaseとは断定せず学習段階を検証。 |
| [MODEL LiquidAI/LFM3-1.7B-Base](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | conditional | 独特のハイブリッド構造を持つ小型事前学習Base。Attention以外の系列を解析・追加学習する原本になる。 | public。現在公開、LFM独自ライセンス。動作にカスタムコードが必要か確認。 |
| [MODEL RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | select | RWKV7の再帰型言語モデル。通常Transformerと異なる推論計算・状態保持を比較できる。 | public。現在公開・Apache 2.0。ランタイムの対応版を保管。 |
| [MODEL GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | select | トークン逐次生成ではない拡散言語モデルのBase。生成方式の多様性を保全する。 | public。現在公開・Apache 2.0。専用デコードコードも必要。 |
| [MODEL state-spaces/mamba-2.8b](https://huggingface.co/state-spaces/mamba-2.8b) | select | SSM系の基礎重み。Self-Attention以外のモデルを長期保存するための代表。 | public。現在公開・Apache 2.0。専用ランタイムと固定する。 |
| [MODEL facebook/vjepa2-vitg-fpc64-384](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384) | select | 動画から表現を学習する非生成型モデル。動画生成器にはない動画特徴抽出・世界理解の能力を確保する。 | public。現在公開・Apache 2.0。動作環境・事前処理を保存。 |
| [MODEL PaddlePaddle/PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | select | 小型かつ異なるOCR/文書解析実装。大きなDeepSeek-OCRが動かない環境でも推論と比較ができる。 | public。現在公開・Apache 2.0。Paddle依存を別管理。 |
| [MODEL openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | select | 小容量で汎用多言語ASRを確保する実用基準。高価な専門音声モデルとの比較に使う。 | public。現在公開・MIT。消失リスクはGated音声データより低い。 |
| [MODEL Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | select | Whisperとは異なる音声認識系統を低容量で確保し多言語比較に使う。 | public。現在公開・Apache 2.0。言語別性能を実測で確認。 |
| [MODEL answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large) | select | 分類・検索用のEncoder-only原本を確保し、LLM以外のファインチューニングを可能にする。 | public。現在公開・Apache 2.0。生成モデルでは代替しづらい効率を比較。 |
| [MODEL BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) | select | 埋め込み・多言語検索の専門モデル。大規模生成モデルと異なるretrievalタスクを保存する。 | public。現在公開・MIT。研究価値はあるが配布停止の兆候は未確認。 |
| [DATA HuggingFaceFW/fineweb-edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | conditional | 事前学習の教師なしテキストを部分保存し、モデルの再学習可能性を維持する。 | public。巨大な多版・多構成dataset。例示した28.5GBを全体容量とせず許諾されたsubsetを選ぶ。 |
| [DATA allenai/tulu-3-sft-mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | conditional | 汎用指示学習を再現するための混合データ。専門SFTとの差分対照として必要。 | public。現在公開・ODC-BYメタデータ。元の各構成データの利用条件を再確認。 |
| [DATA HuggingFaceH4/ultrafeedback_binarized](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized) | select | DPO等の選好学習比較データ。後学習の再現可能性と拒否挙動の解析に必要。 | public。現在公開・MIT。元の比較データセットと学習/評価の汚染を点検。 |
| [DATA llm-jp/magpie-sft-v1.0](https://huggingface.co/datasets/llm-jp/magpie-sft-v1.0) | select | 日本語SFTデータ。英語中心データで代用できない日本語分布を保存する。 | public。現在公開・Apache 2.0。学習/評価セットを分ける。 |
| [DATA elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | select | 日本語の独立評価用。保存する日本語モデルの品質を将来も比較するため不可欠。 | public。現在公開・CC-BY-SA。絶対に学習用と混在させず評価専用で保管。 |
| [DATA lerobot/aloha_sim_insertion_human](https://huggingface.co/datasets/lerobot/aloha_sim_insertion_human) | select | ロボット操作デモデータ。GR00Tやπ0の制御研究で行動を追跡できる。 | public。現在公開・MIT。モデルの具体的な学習データと同一ではないことを明記する。 |
| [MODEL nvidia/nemotron-labs-unified-asr-0.6b](https://huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b) | conditional | 約0.6Bの欧州25言語対応ASR。オフラインとストリーミングを同一重みで扱い、低遅延処理を比較できる。 | public。2026年10月27日公開。Hub licenseはother。160msは作者のアルゴリズム上の最短遅延で、端末実測ではない。日本語非対応。 |
| [MODEL qvac/TranscribePsy-250M-EU](https://huggingface.co/qvac/TranscribePsy-250M-EU) | conditional | わずか254Mの欧州多言語音声認識重み。端末内の処理を優先し、同系の0.6Bモデルより小さな教師蒸留成果を保存できる。 | public。2026年10月公開・Apache 2.0。手機での高速性は配布者による6機種評価。日本語は対象外で、GGUF/CoreML版は別リポジトリ。 |
| [MODEL Qwen/Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct) | select | 約2.13Bの小型VLM。画像・画面の読解や簡易なGUI認識を軽量に実装する基準原本として有用。 | public。現在公開・Apache 2.0。同じQwen系列の27Bに比べ能力は限定されるが、容量と推論メモリが小さい。 |
| [MODEL Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | select | 約0.6Bの多言語埋め込みモデル。汎用会話モデルとは別の意味検索用の表現学習済み重みで、RAGの基盤を小容量で保存できる。 | public。現在公開・Apache 2.0。生成LLMでは代用しにくいが、BGE-M3など既存候補との冗長度は比較する。 |
| [MODEL Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | select | 約0.6Bの検索結果再順位付け専門モデル。Embedding単独では行わない問い合わせと候補文書の関連度判定を軽量に行う。 | public。現在公開・Apache 2.0。再順位付けは検索全体の代替ではなく、遅延・候補件数に依存。 |
| [MODEL google/siglip2-base-patch16-224](https://huggingface.co/google/siglip2-base-patch16-224) | select | 約375Mの視覚Encoder。画像検索・分類と多言語画像テキスト類似度の構成要素として小容量で価値がある。 | public。現在公開・Apache 2.0。大型VLMの生成能力を持たず、独立した視覚特徴抽出用。 |
| [MODEL Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | select | 0.8B級の汎用後学習モデル。最小構成のCPU/端末推論や、他の専用モデルの統合評価用の小型基準として保存する。 | public。現在公開・Apache 2.0。これは事前学習直後のBaseと確認されていないためBaseとは呼ばず、品質の制約を明示。 |

### HOLD（9件）

| 直接リンク | 採用判断 | 採用理由 | 取得上の課題・将来の不確実性 |
| --- | --- | --- | --- |
| [DATA bigcode/the-stack-v2](https://huggingface.co/datasets/bigcode/the-stack-v2) | hold | 大規模コード事前学習データ。ソースライセンス・帰属・削除履歴を含む研究価値は高い。 | gated。現在Gated。一括取得にはSoftware Heritage/INRIAとの別途契約、削除要求後の利用可能版への追随義務が明示される。 |
| [DATA bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata) | hold | 別時代の多言語コード学習データ。出典付きの大量コードとして再現価値が高い。 | gated。現在Gated。元コードの権利と有効版の更新義務があり、永久保存条件は未確認。 |
| [DATA amphion/Emilia-Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset) | hold | 多数話者音声と注釈からなるTTS学習データ。再取得・再注釈のコストが高い。 | gated。現在Gated。HubのCC-BY-4.0表示と本体に関する同意画面のCC-BY-NCが不一致。 |
| [DATA lmsys/lmsys-chat-1m](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | hold | 大規模な人間-LLM対話ログ。再収集が難しい研究資産。 | gated。現在Gated。個人情報・同意・権利条件が未確認のため無条件保存不可。 |
| [DATA laion/relaion2B-en-research](https://huggingface.co/datasets/laion/relaion2B-en-research) | hold | 大規模画像・文章ペアを含む学習用資料。入手可能性と権利情報が重要。 | gated。現在Gated、既存表示約481GB。各画像の権利と収集目的・削除要求への対応が未検証。 |
| [DATA allenai/WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M) | hold | 実際のユーザー対話記録に基づくSFT候補で貴重な自然発話分布を含む。 | public。現在公開でも会話ログのプライバシーと同意について詳細確認なしでは取り込まない。 |
| [MODEL orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | hold | 約180B級MoEの拒否方向編集済みBF16原本。小さなLLMでは比較できない改変研究価値がある。 | gated。現在Gated、上流Qwen3.8-Flash-Nextのlicense metadata otherと派生のApache表示が異なる。原本約336GBを無条件取得しない。 |
| [MODEL mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | hold | 10月29日に公開された約1Tの画像対応MoE。サイバー防御・コード・エージェント能力の独立重みは失われると復元困難。ただし公式FP8全repo1.06TB、NVFP4でも610GBで、3-4bitの512GB RAM上限適合は未検証。 | public。現在公開・独自Mistral Ecosystemライセンス。高性能による提供変更は仮説。Unsloth約3bit GGUFは424/493GBとの自己表示で、OS・KV・mmprojの追加メモリを含む実測が必要。 |
| [DATA nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D) | hold | 自律走行向け実空間データと注釈は収集・再現困難で重要だが、ファイル全量が9.23TBでHDD容量を超える。 | gated。現在Gated・NVIDIA独自契約。NVIDIA技術を用いた自律走行開発等に用途限定、権利者による旧版削除要求の規定あり。長期アーカイブと契約の適合が確認できないため取得不可。 |

## 上流の完全SHAとファイルサイズの一次情報

- [今回の小型OCR・音声・FLUX3](../catalog/snapshots/2026-10-30-disruptive-compact-1.json)
- [画像・動画・3D・ロボティクス・時系列](../catalog/snapshots/2026-10-30-disruptive-compact-2.json)
- [小型TTS・視覚・エージェント記憶・検索](../catalog/snapshots/2026-10-30-disruptive-compact-3.json)
- [科学モデル・文書評価データ](../catalog/snapshots/2026-10-30-disruptive-compact-4.json)
- [従来のGatedモデル・各R1のファイル監査はGitHubのsnapshotsディレクトリ](../catalog/snapshots/)

## 厳密な取り扱い

- **事実**：Hugging Face Hubに現在表示されるアクセス状態、ライセンスメタデータ、版・ファイル容量。
- **配布者主張**：OCR精度、音声WER、画像生成速度、GUI理解等。比較条件や独立性に留意する。
- **推論**：クラウドサービスや人手作業の代替可能性、経済的影響、将来の配布条件変更。
- **未確認**：選択ファイルの最終セットと合計容量、各依存コードとライセンス、RAM実測、データの個人情報・元素材の権利。
- **実行状態**：取得承認キューは空。モデルやデータ本体はダウンロードしていません。

## 一次資料

- [LightOnOCR-3公開記事](https://huggingface.co/blog/lightonai/lightonocr-3)
- [IBM Granite Speech 5.0公式記事](https://huggingface.co/blog/ibm-granite/granite-speech-5)
- [FLUX.3のDiffusers統合と測定](https://huggingface.co/blog/flux-3)
- [QVACの端末別測定](https://huggingface.co/blog/qvac/transcribepsy-250m)
- [Hugging Face利用ポリシー](https://huggingface.co/content-policy)
