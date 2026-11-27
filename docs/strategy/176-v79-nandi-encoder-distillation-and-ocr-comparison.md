# R176 / v79 — 多言語エンコーダの教師・蒸留生徒とOCR代替比較 (2026-11-28 JST)

基準は main 9150271f16198163c67242b767c627f37e7662fc（並行R172–R175の研究と正式選定をすべて保持）。現行方針は AGENTS.md 冒頭、policies/selection.md、selection-decision-v17.json、limits.json。旧270行および133 VERIFIED報告の取得台帳は変更しない。新規技術証拠を条件付き正式選定に反映し、実取得は全件STOP。

## 新規探索範囲と一次証拠
直近7日（11/21–28）発表・更新、30日（10/29–11/28）更新、90日（8/30–11/28）公開に着目した限定的な探索であり、全モデルの網羅ではない。Hugging Face検索・公開API、開発元発表、GitHub・arXiv情報を調査。R159で既出の重み編集の帰無結果や既選定WeMM-Ecomは新規成果として数えない。並行R172研究の候補とも重複しない。

- [NandiBERT 開発元発表](https://huggingface.co/blog/FrontiersMind/introducing-nandibert) 11/24。両repo作成11/18、更新11/26。
- [150M 固定カード](https://huggingface.co/FrontiersMind/NandiBERT-150M/tree/a6fc1adcc36a9bbecf8bddcb0af30d922d5b0eac)、[450M 固定カード](https://huggingface.co/FrontiersMind/NandiBERT-450M/tree/87dd9607b1878509939f3eaf328de7f9d13e352f)。
- [Xiaomi-OCR-0 固定カード](https://huggingface.co/xiaomi-research/Xiaomi-OCR-0/tree/bbd8cf8d21f256b3644b44cb860f3a7cecb93c30)、[arXiv:2609.36136](https://arxiv.org/abs/2609.36136)（本文の取得は確認できず、評価はカード由来）。
- [Surya OCR 2.5 固定カードとLICENSE](https://huggingface.co/datalab-to/surya-ocr-2.5/tree/00c843e9cae45611dca0a6dc2c9bbbf2dadaaed3)。
- 比較元：[ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large)、[LightOnOCR-3-0.8B](https://huggingface.co/lightonai/LightOnOCR-3-0.8B)。

公開HF APIのモデル情報および固定revisionのrecursive tree（expand=true）を終端まで確認。各候補1ページ、4候補95ファイル、総4,732,113,070 Bの配布元メタデータ。Git blob OIDとLFS SHA256を区別。モデル重みや未審査コードを取得・実行せず、公開README/config/LICENSEのみ閲覧。比較2repoのメタデータも別枠記録。公開状態とライセンスタグは観測事実であり、規制予測やアクセス変更の実証ではない。

## ADD CONDITIONAL: NandiBERT
双方向エンコーダ、28層、100352語彙、factorized embeddings、GQA、QK norm、SwiGLU。開発元の450Mは1.1T tokenで一から学習、150Mは枝刈りと500B token蒸留。教師は生徒の推論時依存ではない。名前は公称エンコーダ規模で、保存BF16 MLM headを含む総要素はHF metadata上223,742,464／548,471,808。正確な独立テンソル検査ではない。150M最大context 16384、450M 32768。英語、13インド諸語、アラビア語、インドネシア語、マレー語の17言語、日本語非対象。両者は別学習済み重みであり単純量子化ではない。教師の高品質と長文、生徒の小規模適応・蒸留比較という異なる価値。事前学習コーパス・学習再実行の完全再現は未証明。

| モデル | 作者Indic 7課題平均 | 作者英語10課題平均 | 負の証拠 |
|---|---:|---:|---|
| 150M | 67.37 vs IndicBERT-v2 66.57 | 62.20 vs ModernBERT-base 60.69 | slot filling 54 vs 58.1、QA 46 vs 48.3、UltraBERT-150M 64.59 |
| 450M | 73.23 vs IndicBERT-v2 65.93 | 63.34 vs ModernBERT-large 61.02 | GLUE 89.9 vs 90.4、SQuAD2 89.7 vs 89.8、UltraBERT-380M 66.79 |

数値は固定モデルカードの作者報告、別々の比較条件を横断して優越を断定しない。150Mのブログ記述とカード表に差があるためカードを採用。3 seedとされるが分散、独立再現、対象HW、速度・メモリ実測なし。既存SELECT ModernBERT-largeは英語対照としてKEEP（総repo 7,861,097,894 Bには代替形式が混在、native単独1,583,544,840 B）。BGE-M3、Qwen3-Embedding-0.6Bは検索用学習済みモデルであり、MLMのNandiBERTはそのまま代替できずKEEP。

配布元タグApache-2.0・カードからライセンスへのリンクあり、repo内LICENSEなし。コードと学習データの権利、本人の各利用行為は未確認。Transformers 5.x、独自nandi_encoder、150M configは5.20.2、450Mは詳細version未記載。trust_remote_codeを要するため、コードレビュー、固定依存wheel、オフライン復元、CPU/GPU実測前は実行・取得不可。設定・tokenizer・コードの固定参照は依存完全閉包を意味しない。

## HOLD 研究のみ: OCR
Xiaomi-OCR-0（9/29 repo作成、10/29更新）はQwen3.5-0.8B-BaseからOCR向け継続学習・RL、873,438,784 BF16保存要素、28ファイル1,773,852,874 B。作者のOCR中心5課題平均83.2 vs Qwen3.5-0.8B 72.9、4B 84.9。OmniDocBench 96.83 vs TeleOCR 96.87、Wild 87.94 vs 88.53。Real5はPaddleOCR 1.6との比較であり現行1.5との比較と混同しない。Apache-2.0タグ、LICENSEなし。独立学習成果だが既存専門OCRに対する必要性未実証。

Surya OCR 2.5（10/25 repo作成、10/29更新）、689,356,864 BF16保存要素、47ファイル1,395,290,275 B。作者OmniParseBench 85.9 vs 2.0の83.3、日本語80.5 vs78.8、英語90.3 vs94.3、old scans math 78.6 vs79.0。行列geometry機能なし。改変OpenRAIL-M本文は売上・資金調達5M USD条件と個人・研究例外を含み、complementary materialsに同じ許諾は及ばない。権利条件・依存閉包・旧モデルとの差を検証するまで保留。

現行LightOnOCR-3-0.8B、PaddleOCR-VL-1.5、DeepSeek-OCR-2はKEEP。既存と揃えた同一ベンチマーク不足のため新OCR2候補は正式カタログに追加しない。通常量子化は独立学習成果に数えない。新規REPLACE・EXCLUDEなし。

## 容量、依存、承認
Nandi 150M 10 refs 456,755,592 B、450M 10 refs 1,106,214,329 B。合計1,562,969,921 B。重みLFS SHAは別。4つの補助ファイル（.gitattributes、banner、tokenization code、tokenizer.json）Git blob一致9,194,667 B、2repo論理source union 1,553,775,254 B。現物の重複排除やハードリンク節約とは区別。既知有効source-repo proxyは旧3,932,833,343,922 Bから3,934,396,313,843 B（未確定49資産を含まない、量子化等の代替ファイル含有）。完全依存込み増分・現物占有・staging・空きはnull。4TB選定上限、200GB実空き床、150B原則、権利、正規アクセス、明示承認は不変。予算余裕を実証しない。モデル重みDL・新承認・物理削除0。

## 次の検証（提案・未実行）
H: 教師・生徒は既存英語対照にないIndic分類/NER性能、圧縮に伴う精度・latencyの差を持つ。T: 適法な独立holdout・3 seedで同一fine-tune設定、7 Indic/10 English tasks、CPU/GPU/OS/driver/backend固定、context 512/4096、batch 1/8、各30反復。D: 比較前に閾値合意、paired bootstrap区間と中央値/peak RAMを報告、追加価値または圧縮便益が未確認ならUNCERTAIN。C: tokenizer差・データ漏洩・タスク重み付けや著者評価条件差。U: seed間分散、サンプル偏り、測定誤差未算定。OCRは同じ許可済みページを各日本語、数式、古いスキャン、KIE strataで100件を目標に対比較、誤り類型と区間、ライセンス条件を別評価。実行は権利と取得明示承認以降。

## 正式差分
v78から272登録／216有効（SELECT56、CONDITIONAL160、HOLD37、BACKLOG13、EXCLUDED6）。既存270行と台帳不変。CURRENT、overlay、materialized、active worklist、access、readiness、preparation、estimatesを同期。R172–R175の並行研究を上書きしない。全216有効はSTOP。検証は標準ライブラリ回帰テストおよびread-only整合監査に限る。

追加統合時に未知総数の集計値を正本の各行から再計算した。既存候補の判定・ゲートは変更していない。
