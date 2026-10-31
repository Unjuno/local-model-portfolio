# 第6回：モデル・データ・ランタイムの追加選定（2026-10-31）

> **すべてドラフト提案。`catalog/CURRENT.json`への適用、Gated同意、モデル/データ本体の取得、実行、インストールは行っていない。**

## 1. 今回の結論

第6回ではモデル11件とデータセット3件の計14件を具体的な採用審査対象に追加した。5件は保存価値を明示して採用を推奨し、9件は条件付き採用案。前回第5回の11件とv3の旧候補、現行v2の110件との**repo ID重複を避けている**。

今回は**生成専用モデルに偏らない**よう、プロンプト注入防御、文字/画像安全分類、音声の真正性、形式数学のLean4証明、分子複合体の構造/親和性、ロボット方策、音声翻訳、非英語音声・安全研究・生体学習データを広げた。カテゴリーだけで配布が制限されると断定していない。

## 2. 新規14件の具体的な選定理由

| 優先 | 種別 | 公式配布先 | 選定案 | 失うと何が残らないか |
| --- | --- | --- | --- | --- |
| R0 | モデル | [meta-llama/Llama-Prompt-Guard-2-86M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) | conditional | プロンプトインジェクション・指示系の攻撃検出に特化した分類済み重み。現在の拒否方向編集モデルや汎用LLMでは同じ防御器を再現できない。 |
| R0 | モデル | [meta-llama/Llama-Guard-4-12B](https://huggingface.co/meta-llama/Llama-Guard-4-12B) | conditional | 文字と画像の安全判定向けの後学習済みVLM。Prompt Guard 2の入力攻撃検出と異なる目的。Llama4 Scout事前学習重みだけでは同一の後学習済み判別器を復元できない。 |
| R0 | モデル | [google/shieldgemma-2-4b-it](https://huggingface.co/google/shieldgemma-2-4b-it) | conditional | 画像の危険内容の分類向け専門後学習済み重み。既存画像生成器やMedGemmaの医療画像判定とは目的・訓練が異なる。 |
| R0 | モデル | [protectai/deberta-v3-base-prompt-injection-v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2) | select_proposed | プロンプトインジェクション検出の小型後学習重み。配布者カードはプロジェクト保守終了を明記、GitHubのprotectai/llm-guardもarchivedで、古い判別器とコードの再現可能性に実際の保守リスクがある。 |
| R1 | モデル | [mistralai/Shieldstral-1.0-3B](https://huggingface.co/mistralai/Shieldstral-1.0-3B) | select_proposed | 自然言語で定義した安全ポリシーに合わせて文字・画像を分類する3Bの独自後学習済みモデル。固定カテゴリのGuardと対比できる。 |
| R1 | モデル | [facebook/audioseal](https://huggingface.co/facebook/audioseal) | select_proposed | 埋め込み式音声電子透かしの生成器と専用検出器。既存の音声合成モデルだけでは原発行モデル由来の透かし検証を代替できない。 |
| R1 | モデル | [nii-yamagishilab/hubert-xlarge-anti-deepfake](https://huggingface.co/nii-yamagishilab/hubert-xlarge-anti-deepfake) | conditional | 音声のディープフェイク検出に特化して後学習したHuBERT系判別器。AudioSealの方式依存透かしとは検出原理が異なり比較原本に価値。 |
| R1 | モデル | [Goedel-LM/Goedel-Prover-V2-8B](https://huggingface.co/Goedel-LM/Goedel-Prover-V2-8B) | select_proposed | Lean4の形式証明を生成する8Bの専門後学習済み重み。現在の汎用推論モデルや数学質問データセットとは異なり形式証明の正否を検証できる。 |
| R1 | モデル | [boltz-community/boltz-2](https://huggingface.co/boltz-community/boltz-2) | conditional | 分子複合体3D構造と結合親和性を同時に扱う学習済み重み。既存のESM2配列Encoder・Evo2核酸モデル・医療対話LLMでは代替しにくい。 |
| R1 | モデル | [lerobot/pi05_base](https://huggingface.co/lerobot/pi05_base) | conditional | π0.5ロボットVLAの後学習済み原本。既存pi0_base・GR00T N1.6と異なりロボット多環境の汎化を志向したモデル。 |
| R2 | モデル | [facebook/seamless-m4t-v2-large](https://huggingface.co/facebook/seamless-m4t-v2-large) | conditional | 音声と文字の多言語変換を単一系列で扱う専門音声翻訳の完成原本。既存のASR専用モデルやSimulMTは同一の音声出力重みでない。 |
| R0 | データ | [allenai/wildguardmix](https://huggingface.co/datasets/allenai/wildguardmix) | conditional | プロンプトの危険性・拒否評価等を伴う人手/合成の安全性データ。防御器と評価データを別に保全しなければ将来比較できない。 |
| R1 | データ | [arcinstitute/opengenome2](https://huggingface.co/datasets/arcinstitute/opengenome2) | conditional | Evo2の学習に使われた生命全般の巨大なDNA資料。モデル重みでは代替できない事前学習データとドメイン多様性を記録する。 |
| R2 | データ | [google/fleurs](https://huggingface.co/datasets/google/fleurs) | select_proposed | 102言語の並列音声・文字による評価/学習の原本。既存の英語・日本語中心音声群を補い、比較用の低資源言語を固定できる。 |

上記の`select_proposed`は**保存する価値があると判断した選定**であり、リビジョン・必要なサイズ・完全な許諾に関する取得ゲートの通過とは異なる。

## 3. 配布制限・再現困難性・不確かさ

### meta-llama/Llama-Prompt-Guard-2-86M

**観測・利用条件：** Gatedが現実のアクセス条件。提供終了予定は未確認。公式モデル名の86MとHub metadataの278.8Mが一致せず、実ファイル/パラメータを監査する。 **主な未解決事項：** Meta公式利用条件、攻撃分類の偽陰性/偽陽性、tokenizer、比較対象22M版の違いを固定。 **出典：** [一次資料1](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)、[一次資料2](https://github.com/meta-llama/PurpleLlama)。

### meta-llama/Llama-Guard-4-12B

**観測・利用条件：** Gated・独自ライセンスの観測。公開停止予定や高い規制確率の証拠はない。既存Llama 4 Scoutの元重みと比較。 **主な未解決事項：** Meta使用条件・視覚プロセッサ、Llama4派生制限、12Bフル重み、評価データ別の誤判定を確認。 **出典：** [一次資料1](https://huggingface.co/meta-llama/Llama-Guard-4-12B)、[一次資料2](https://huggingface.co/blog/llama-guard-4)。

### google/shieldgemma-2-4b-it

**観測・利用条件：** Gated + Gemma条件。Google公開カードは画像とポリシー文による分類を説明。LlamaGuard4との重複は要評価。 **主な未解決事項：** Gemmaの利用同意、画像前処理、商用条件、危害カテゴリの誤検知、ポリシー依存性能を確認。 **出典：** [一次資料1](https://huggingface.co/google/shieldgemma-2-4b-it)、[一次資料2](https://ai.google.dev/gemma/docs/shieldgemma/model_card_2)。

### protectai/deberta-v3-base-prompt-injection-v2

**観測・利用条件：** 公開モデルであり重み削除予定は未確認。2026-07までに保守終了の事実あり。英語の入力分類のみ、jailbreak検出ではない。 **主な未解決事項：** 元DeBERTa・tokenizer・LLM-Guardの固定版、分類閾値、英語範囲・誤陽性、アーカイブ版の依存SBoMを確認。 **出典：** [一次資料1](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)、[一次資料2](https://github.com/protectai/llm-guard)。

### mistralai/Shieldstral-1.0-3B

**観測・利用条件：** 公開Apache-2.0、Gatedや提供停止の証拠はない。Bench数値は提供者報告でありユーザー環境の独立検証ではない。 **主な未解決事項：** Ministral3とPixtral encoder等の依存、実装固定、32k学習文脈と256k理論文脈を区別、誤検知/言語差を再評価。 **出典：** [一次資料1](https://huggingface.co/mistralai/Shieldstral-1.0-3B)。

### facebook/audioseal

**観測・利用条件：** 公開MIT。公式カードは透かし検出器が特定の埋め込み方式を対象とすることを示す。一般のAI音声/声紋認証の万能検出器ではない。 **主な未解決事項：** generator・detectorの双方、YAMLカード・Pythonライブラリ・固定版、編集耐性の独立評価と誤陽性を確認。 **出典：** [一次資料1](https://huggingface.co/facebook/audioseal)、[一次資料2](https://github.com/facebookresearch/audioseal)。

### nii-yamagishilab/hubert-xlarge-anti-deepfake

**観測・利用条件：** 公開・非商用の配布元条件。実行に旧fairseq環境が必要で、github/facebookresearch/fairseqはarchived。2025-10公式カードで固定バージョンとweights_only=Falseを要求する事例がある。 **主な未解決事項：** コードを無条件に実行しない。fairseq 862efab...とPython3.9・依存wheelの隔離、pickle検査、本人同意ある評価音声、精度汎化と商用可否を確認。 **出典：** [一次資料1](https://huggingface.co/nii-yamagishilab/hubert-xlarge-anti-deepfake)、[一次資料2](https://github.com/facebookresearch/fairseq)。

### Goedel-LM/Goedel-Prover-V2-8B

**観測・利用条件：** 公開Apache-2.0。配布停止予定はなし。作者ベンチのMiniF2Fなどは独立再測定でない。 **主な未解決事項：** Lean4・mathlib4・コンパイラ版、tokenizer、証明探索時間/試行数/定理集合とライセンスを固定。 **出典：** [一次資料1](https://huggingface.co/Goedel-LM/Goedel-Prover-V2-8B)、[一次資料2](https://github.com/leanprover/lean4)、[一次資料3](https://github.com/leanprover-community/mathlib4)。

### boltz-community/boltz-2

**観測・利用条件：** 公開MIT。公式HFカードは情報量が乏しいが、MITの公式jwohlwend/boltz実装とconf/affチェックポイントを別途照合済み。過去v3で規制根拠不足を理由に見送ったが今回の専門学習・再現性の観点で再評価。 **主な未解決事項：** conf/aff ckpt・mols.tar、オフラインMSA入力、NVIDIA-BioNeMo等の別ランタイム差、pickle/危険なコードロードの隔離、選択サイズ。 **出典：** [一次資料1](https://huggingface.co/boltz-community/boltz-2)、[一次資料2](https://github.com/jwohlwend/boltz)。

### lerobot/pi05_base

**観測・利用条件：** 公開・Gemma条件。公式カードは流れマッチングの行動ヘッド以外の原研究要素が未公開と明記。完全再現可能だと主張しない。 **主な未解決事項：** LeRobot実装・Gemma由来の権利、pre/postprocessor、データ正規化、未公開RL部の不在、N1.7との重複。 **出典：** [一次資料1](https://huggingface.co/lerobot/pi05_base)、[一次資料2](https://github.com/huggingface/lerobot)。

### facebook/seamless-m4t-v2-large

**観測・利用条件：** 公開・非商用条件。現行の提供停止兆候は確認できず緊急度は低い。 **主な未解決事項：** speech encoder/decoder、音響codec/推論器、対応言語・入力出力形式、他翻訳系との重複と非商用利用範囲。 **出典：** [一次資料1](https://huggingface.co/facebook/seamless-m4t-v2-large)。

### allenai/wildguardmix

**観測・利用条件：** Gatedが観測事実。攻撃的・不快な文面が含まれ、配布条件・個人情報・データ由来を精査するまで無断取得しない。 **主な未解決事項：** Hugging Face利用規約同意、学習/評価の分離、二次配布可否、特定サブセットと完全SHA。 **出典：** [一次資料1](https://huggingface.co/datasets/allenai/wildguardmix)、[一次資料2](https://arxiv.org/abs/2406.18495)。

### arcinstitute/opengenome2

**観測・利用条件：** 公開Apache-2.0表示。約9兆塩基対を収録との提供者説明があり、全量を3.8TBに収容できるとは言えない。原データの由来・データ依存を確認。 **主な未解決事項：** 全量取得は非推奨。代表生物・形式（fasta/jsonl）・権利のある部分集合を特定してサイズとSHAを精算する。 **出典：** [一次資料1](https://huggingface.co/datasets/arcinstitute/opengenome2)、[一次資料2](https://github.com/ArcInstitute/evo2)。

### google/fleurs

**観測・利用条件：** 公開CC-BY-4.0。現在の配布制限や公開停止予定なし。多数の言語を同時に保存できるか、音声の元素材利用条件は確認が必要。 **主な未解決事項：** 言語・train/dev/testの選択とリーク防止、speaker同意/権利、データ容量・ファイルSHA・メタデータ変換を固定。 **出典：** [一次資料1](https://huggingface.co/datasets/google/fleurs)。


**重要な区別：** 供給停止という意味で実際の事実があるのは、例えばProtect AI LLM-GuardのGitHub Archived、旧fairseqのArchived、以前確認したMicrosoft VibeVoice-TTSのコード撤去など。GatedのMeta/Googleモデルについて、特定の将来規制や公開削除が予定されていることは確認していない。

**モデル同士の機能差：** Prompt Guard 2は攻撃的入力の分類、LlamaGuard4はテキスト/画像の安全分類、ShieldGemma2は画像安全分類、Shieldstralは自然言語の規則に応じた分類。AudioSealは**AudioSealの透かし**を検出し、HuBERT AntiDeepfakeは別の合成音声判別器。これらは完全に同一のモデルではないが、同一用途内の冗長性を比較してから選ぶ。

**ハード・安全：** Goedel-Proverの形式証明はLean4/mathlib4が必要。Boltz2はオフラインMSA・mols.tar・conf/aff重みが必要。HuBERT AntiDeepfakeは旧fairseqと安全でないpickleロード回避が必要。pi0.5は元論文の全要素が公開済みではない。

## 4. 選ばなかった9件

| 公式配布先 | 判定 | 根拠 |
| --- | --- | --- |
| [lab260/Spectra-AASIST3](https://huggingface.co/lab260/Spectra-AASIST3) | watch_only | 公開Apache-2.0、論文未公開との配布者記載あり。音声鑑定の性能・汎化は独立試験と追試が必要。 |
| [nvidia/NVIDIA-Nemotron-Parse-2.0](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0) | watch_compared_with_existing_OCR | 公開OpenMDW1.1の構造化文書抽出器。LightOnOCR3/PaddleOCR-VL/DeepSeekOCR2との重複、chart parsing固有の差を計測してから採用。 |
| [dots-studio/dots.ocr](https://huggingface.co/dots-studio/dots.ocr) | watch_compared_with_existing_OCR | 公開MITの文書レイアウト解析器。trust_remote_codeを要求する記載があり、隔離実行・既存OCR比較が先。 |
| [facebook/nllb-200-3.3B](https://huggingface.co/facebook/nllb-200-3.3B) | watch_with_existing_translation | 公開CC-BY-NCの200言語機械翻訳。Seamlessと既存Hy-SimulMTと優先度/保存容量が競合。 |
| [InstaDeepAI/nucleotide-transformer-2.5b-multi-species](https://huggingface.co/InstaDeepAI/nucleotide-transformer-2.5b-multi-species) | watch_with_evo2 | 公開CC-BY-NC-SA。Evo2との固有性と研究利用条件を比較し、重複優先保存を避ける。 |
| [mozilla-foundation/common_voice_17_0](https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0) | hold_supplier_migrated | 2025-10からMozilla Data Collectiveが専属配布先と配布者カードが明示。旧HFファイルの取得可能性/音声の本人同意/再配布条件を確認するまで取得を計画しない。 |
| [SpeechAntiSpoofingBenchmarks/ASVspoof2021_DF](https://huggingface.co/datasets/SpeechAntiSpoofingBenchmarks/ASVspoof2021_DF) | hold_legal | 公開だが独自ライセンス。評価音声の元素材権利と許諾を独立に確認。モデル保存のため無断でミラーしない。 |
| [princeton-nlp/SWE-bench](https://huggingface.co/datasets/princeton-nlp/SWE-bench) | watch_software_evaluation | 公開ソフトウェア課題評価。第三者GitHubコードとIssue/PRの利用条件、正規再現用依存イメージが必要。 |
| [nvidia/PhysicalAI-Robotics-Open-H-Embodiment](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment) | hold_legal | CC-BY-4.0表示でも医療ロボット/映像含有データ。元データ・人体・施設等の権利と利用目的を確認するまでは収集しない。 |

**Mozilla Common Voice**は配布者自身が2025-10以降の提供先をMozilla Data Collectiveに変更したことを説明している。これは重要な提供経路の変更記録だが、HFの旧版重み/データが合法的に取得可能である保証ではない。本人の声を含む音声データの権利は別に確認する。

## 5. ソフトウェア20件と知識4カテゴリの独立選定

これまで正本に独立したソフトウェアが0件であり、モデルだけを保存しても実行再現性が欠ける。今回[ソフトウェア20件と知識4カテゴリのレビューJSON](../catalog/reviews/runtime-and-knowledge-selections-2026-10-31.json)を作成した。公式GitHubのライセンスメタデータは確認したが、**実行器/ABI/ドライバー/全wheelを確定したという意味ではない**。

| 状態 | ソフトウェア |
| --- | --- |
| core（7件） | [huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub)、[huggingface/xet-core](https://github.com/huggingface/xet-core)、[huggingface/transformers](https://github.com/huggingface/transformers)、[huggingface/diffusers](https://github.com/huggingface/diffusers)、[vllm-project/vllm](https://github.com/vllm-project/vllm)、[ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)、[microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |
| conditional_core（1件） | [pytorch/pytorch](https://github.com/pytorch/pytorch) |
| family_specific（10件） | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni)、[sgl-project/sglang](https://github.com/sgl-project/sglang)、[leanprover/lean4](https://github.com/leanprover/lean4)、[leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4)、[jwohlwend/boltz](https://github.com/jwohlwend/boltz)、[huggingface/lerobot](https://github.com/huggingface/lerobot)、[NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)、[facebookresearch/audioseal](https://github.com/facebookresearch/audioseal)、[mistralai/mistral-common](https://github.com/mistralai/mistral-common)、[NVIDIA/PhysicsNeMo](https://github.com/NVIDIA/PhysicsNeMo) |
| archived_high_preservation_priority（2件） | [protectai/llm-guard](https://github.com/protectai/llm-guard)、[facebookresearch/fairseq](https://github.com/facebookresearch/fairseq) |

保存するべき知識資料4カテゴリ：ライセンス本文/版、モデルカード/ファイル出所、OS・Python ABI・GPU/driver・wheelと動作テストの完全な環境ロック、論文・モデル生成過程・評価条件。これは仕様上の選定であり、現時点では資材そのものをコピーしていない。

## 6. 容量・承認を別の段階に維持

現行v2は110件追跡・94件有効、暫定選定容量は3.234067678260TB（十進）。計画上の枠3.8TBとの差0.565932321740TBは**確定した実空き領域ではない**。新規14件・20ソフトウェアの正確なファイル容量は未確定のため、予算内へ入ると保証しない。

取得前の絶対条件は、(1)正規の同意と利用権限、(2)モデルと実行器それぞれの完全commit、(3)選択全ファイル・必要codecとtokenizer、(4)正確なバイト数と上流ハッシュ、(5)Python ABI・OS・GPU/CPU/ドライバー・backendとバッチ/コンテキスト、(6)最大推論RAM512GB未満（3–4bit適用可能な場合）、(7)HDD空き200GB以上、(8)ユーザーの固定マニフェスト承認。モデルをロードして確認することも別許可とする。

## 7. H/T/D/C/U

| 記号 | 実施規則 |
| --- | --- |
| H | 未保全の防御/真正性/形式証明/生命科学/多言語などの学習成果を追加すると、後に再取得不能になった際の研究選択肢の損失を抑えられる可能性がある。規制確率の数字は主張しない |
| T | 各候補の公式HFカード/現行利用条件/構成、代替ミラー/既存重み、必要実行器とデータ権利を順番に照合。必要情報が不足した時点で個別審査を停止 |
| D | PASS=一次資料・直接リンク・独自価値・比較理由のある選定。FAIL=重複/存在不明/権利不適合。UNCERTAIN=容量/完全rev/依存/権利が不明な取得計画 |
| C | 実際には同じモデルの量子化版/ミラー、提供者がGatedを維持して削除しない、公開原本から同じ能力を再構築できる、研究データに利用不可の第三者権利がある |
| U | ライセンス変更、モデルの公開更新、学習データ権利、HW/backend、プロバイダ評価のバイアス。合成標準不確かさや包含係数は統計モデル未定義のため数値化しない |

## ERROR CHECK

- 追加新規ID：モデル11件、データ3件、合計14件。ソフトウェア20件は別資産種別であり、モデルの件数に混ぜない。
- 現行v2や以前の第5回選定と同じrepo IDは**この第6回新規に二重計上しない**。Boltz2のみ、以前見送った候補の明示的な再評価。
- 不明なライセンス、取得ファイル容量、完全rev、実機RAMは不明のまま。Gated/非商用/安全性の特別条件を回避しない。
- `queues/approved.json`と`catalog/CURRENT.json`は編集しない。個別モデルの政府による将来配布停止は確認していない。