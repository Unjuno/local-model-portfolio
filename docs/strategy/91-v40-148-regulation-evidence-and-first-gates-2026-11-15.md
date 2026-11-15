# R91｜現行v40・148有効資産の規制事実と取得前ゲートの再監査（2026-11-15）

**判断**：`main` の唯一の正本 `catalog/CURRENT.json` は v40（登録195／有効148＝SELECT53＋CONDITIONAL95）。現時点で**新規追加・除外・交換は0件**。理由は、追加候補の性能や見かけの公開状況では、ユーザー本人の利用権限、完全な学習済み依存、原本同一性、物理HDD実測という非代替的ゲートを埋められないためである。既存選定を「ダウンロード可能と確定」とは言わない。

[全148件の機械可読・第一停止要因台帳](../../catalog/research/2026-11-15-v40-148-regulatory-source-triage.json)を同日に新規作成。本記録は調査・静的メタデータ分析のみで、ウェイト取得・実行・権利同意・approved queue変更は一切行っていない。

## 1.〈本論〉— 最新の一次情報：事実と予測を分離する

| 観測事実・日付 | 一次ソース | このリポジトリへの含意 |
|---|---|---|
| 2025-05-13：米BISは2025年のAI Diffusion Rule撤回と不執行を発表 | [BIS公式](https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens) | 旧案のECCN・計算量基準を「現行の公開ウェイト全面禁止」と誤表示しない。別のEAR・制裁・契約の適用は個別に検証する。 |
| 2026-06-12：米国の輸出管理措置に対応しAnthropicはFable 5とMythos 5のアクセスを一時停止 | [Anthropic当日声明](https://www.anthropic.com/news/fable-mythos-access) | **能力を理由に利用経路が突然停止しうる実例**。しかし非公開のホスト型モデルであり、個々の公開ウェイト消失の予告とはしない。 |
| **2026-06-30に当該制限解除、07-01に復旧** | [Anthropic復旧声明](https://www.anthropic.com/news/redeploying-fable-5) | **6月の制限が現在も継続という記載は誤り**。停止と復旧の両方を記録する。 |
| 2026-08-02：EU AI ActのGPAI等の執行が開始。2026-12-02に特定の非同意性的ディープフェイク／CSAM生成システムの禁止とArticle 50(2)移行期日 | [EU当局の執行FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start)／[公式実施日程](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline) | システム・提供者義務と保存済みウェイトの利用・保管を混同しない。 |
| EUのオープンソースGPAIは一定の文書義務が条件付き免除。ただし著作権関連義務、データ要約、システミックリスクモデルの義務は残る | [EU当局FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)／[Article 53](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53) | 150Bという私的なモデル総数上限と、EUの**学習計算量10^25 FLOP**推定基準を同一視しない。 |
| 2023-12-19にLAION-5Bを停止、2024-08-30に安全フィルタ済みRe-LAION-5Bを公開 | [LAION公式](https://laion.ai/blog/relaion-5b/) | 旧データと安全フィルタ版は同一スナップショットではない。疑義のあるデータの「消える前に無差別取得」は不適切。 |
| HubのGatedは個人のアクセス申請・同意が必要 | [Hugging Face公式](https://huggingface.co/docs/hub/models-gated) | **モデルページを閲覧できることと本人が重み取得可能であることは別**。過去のGated表示は現在の本人認可の証拠にならない。 |

**事実／仮説の線引き**：T1＝悪用・権利・プライバシー等の限定的な配布・アクセス措置、T2＝高能力モデルへの対象拡大、T3＝公開ウェイト一般への広範な配布規制、の順序は**ストレステスト用のシナリオ**であり既定路線でも個別予告でもない。対立仮説は、公開ウェイトの競争・研究価値、規則の撤回、ライセンス緩和、措置の復旧である。モデル別消失確率は定量根拠がなく数値化しない。

## 2. 全148件を「最初の停止要因」で一意に再分類

| 順位ではなく排他的な第一停止要因 | 数 | 確認すべき最初の証拠 |
|---|---:|---|
| 個人のGatedアクセスと契約適合性 | 19 | 本人の承認、特定commitの条件、再配布／保存・研究利用の権利 |
| 学習済みパイプライン総パラメータ未確定 | 9 | 別学習済みtokenizer／codec／encoder／MoE全expert等を含む総数、非実行の一次メタデータ |
| 固定revision・必要な原本ファイル・外部依存未閉包 | 118 | 同じ配布元のrevision、モデル・tokenizer・adapter・音声codec・ライブラリABI、重複SHA |
| 暫定source候補は絞れているが実機HDD・staging未測定 | 2 | 実HDD総容量、空き容量、キャッシュと展開一時領域のピーク |
| **計** | **148** | 全件で取得前の別ゲートも未解消 |

根拠：[現行v40正本](../../catalog/effective-portfolio-2026-11-15-v40.json)・[148件readiness正本](../../catalog/readiness/v40-2026-11-15-r90-all148-gates.json)・[派生した148行監査](../../catalog/research/2026-11-15-v40-148-regulatory-source-triage.json)。

注意：Gatedの履歴記録は**計20件**。上表の最初の停止要因がGatedなのは19件で、残りの1件は総数未確定が先行する。総数未確定は9件。**146件で固定ファイル／最終bytes-SHAの停止条件**が残り、144件のreadinessは以前のv36からの証拠継承であり本人権限のライブ再検証ではない。実行・重み取得・権利承認・オフライン復元の成功例は0。

## 3. モデル内部構成と配布元の原本を見た個別判断

| 対象（一次モデルカード） | 今回の確定判断 | 保留するもの／重複排除方針 |
|---|---|---|
| [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts) | **独立の数値音響制御TTSとしてCONDITIONAL維持**。出版社表示は音響9.59M、Vocos13.53M、refiner17.64M又はcloning flow24.67M、外部WavLM約101MとMiniLM約22.7M。CC BY-NCとWhissle追加契約、音声同意制限を確認。 | 総学習済みcomponentの最終revision別列挙と本人Gated許可は未確認。表示値の加算だけで「完全総数を実査」としない。 |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | インド諸語等の別学習済み音声モデルとして候補維持。モデル本体のほか**Kyutai MimiとSpeechBrain ECAPA**を作者が依存指定。 | これらの学習済み依存とライセンスを含む総数未閉包につき取得準備停止。 |
| [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | 671MBのrank-128独立LoRAを原本候補として維持。最終候補sourceの一部は既存台帳で固定済み。 | **Qwen-Image-2.1基盤・encoder・VAEが必須**。派生LoRAごとに同一SHAの基盤を複製しない。Qwen Research License、研究・評価用途制限を継承。 |
| [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | **追加確定・優先度昇格はしない**。作者は2026-09-28の更新で移動・ポーズ変更への過適合を認め、LoRAを使わない再アラインメントworkflowも提示。 | ChatR系LoRAとは学習目的が異なるため同一学習重みとして削除もしない。ベースモデルと直接比較する制御実験で増分を反証する。 |
| [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | Q4言語＋F16視覚の原本候補は保持。モデル固有編集とMTP保持は別の研究価値がある。 | 政治回答の作者113問LLM judgeは一般的正確性ではない。GPQA等のBF16結果をQ4の品質と取り違えない。実重みSHA／使用権限未確認。 |
| [nvidia/Kumo-Anomaly](https://huggingface.co/blog/nvidia/kumo-anomaly) | 多変量時系列拡散異常検知の独立学習を保全対象に残す。 | NVIDIA公式紹介の「約8M」と別SDK値の食い違いは**元の全tensor数確定ではない**。9件の総数不明ゲートに残す。 |
| [GroundingPI/GroundingPI](https://huggingface.co/GroundingPI/GroundingPI) | v40の追加を維持。位置トークン原本はOCR・SAM3マスク・ロボット行動と同一能力ではない。 | 著作者Apache-2.0とKimi派生条件を区分し、独自Transformers fork/vLLM固定、実HDD・本人権利を検証する。[既存根拠](90-v40-groundingpi-original-decision.md) |
| [XiaomiRobotics/Xiaomi-Robotics-U0-4B](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B) | 既存v39の独立世界モデルとして維持。 | 外部学習済みVisionTokenizerとunsafe `torch.load`／`trust_remote_code`経路は別安全ゲート。配布元ソース固定だけでは実行安全ではない。[既存根拠](90-v39-unis4b-source-allowlist-runtime-gates.md) |

**入替保留の反証対象**：LTX-2.5の2種類の後学習派生が同条件で同一機能・品質に収束する、画像Consistency LoRAが通常のbase／Realign操作に優位を示さない、あるいは同一家族の音声モデルが特殊話者・言語制御の独立能力を示さないなら、対応するCONDITIONALをHOLDへ降格し、容量を他ドメインへ回す。ただし**異なる学習済み成果を単に同名ベースだから重複と判定することは禁止**。

**大容量の誤解に注意**：`mistralai/Mistral-Small-4-119B-2603`の公開元全repo約241.9GB、`meta-llama/Llama-4-Scout-17B-16E`約217.3GB、`openai/gpt-oss-120b`約195.8GB、`black-forest-labs/FLUX.2-dev`約177.6GB、`Qwen/Qwen3-Coder-Next`約159.4GBは、いずれも**保存対象を固定した後の増分容量ではない**。原本メタデータとして重くても、同一SHAの共有依存・量子化例外・ライセンスを検証する前に削除または全取得してはいけない。

総モデルパラメータ150Bはローカル方針。現在は**150B以上の量子化特殊版を例外審査に回す**規約だが、自動採用でも取得許可でもない。現行の2件はHOLDのまま。MoEではactiveだけでなく全expert・学習済みembedding・MTPを考慮し、原本の総構成が不明な9件は研究記録のみに留める。

## 4.〈応用・転用例〉— 保存順序・ベンチマーク・供給網への適用

**決めた順序**：①9件の総学習済み構成を静的照合する、②20件のGatedに関する本人権限と現行LICENSEを別々に確認する、③静的source候補が絞れた2件の実HDD・キャッシュ・同一SHAを評価する、④118件のpublisher固定revision・学習済み依存・原本ファイルを閉包する、⑤144件の古いアクセス観測を現行Hubで再確認する。**重みの無許可ダウンロードは常に停止**。

同じモデル系列の重複判定では、最低30入力×各3乱数シードを用意し、同一評価セット・同一backendとdtype/quantizer/zero-point・同一context・GPU/CPU/クロック／batch条件・評価者を固定することを提案する。品質差の信頼区間、能力固有タスク、実際の保存増分byteが揃わなければ統廃合の確定はしない。この設定は**提案プロトコル**でありベンチマーク実施済みではない。

学際的な意義：①AI政策・データ保護（配布権利と将来政策を分離）、②デジタルアーカイブ・ソフトウェア供給網（不変SHA、ライブラリABI、取得履歴）、③統計学・モデル評価（同一条件での非劣性・重複検証）、④計算機工学（物理容量・ピークRAM・依存閉包）。

## 5. 変数表・単位チェック

今回の静的監査で用いる**件数恒等式**：

\[
N_{\mathrm{active}}=N_{\mathrm{select}}+N_{\mathrm{conditional}}=53+95=148.
\]

| 記号 | 意味 | SI単位 | 定義と範囲／前提 | 型 |
|---|---|---|---|---|
| \(N_{\mathrm{active}}\) | 有効選定資産数 | 1（件数） | 現行v40でSELECTまたはCONDITIONAL、0〜195 | 非負整数スカラー |
| \(N_{\mathrm{select}}\) | SELECT件数 | 1（件数） | v40正本から算出、0〜195 | 非負整数スカラー |
| \(N_{\mathrm{conditional}}\) | CONDITIONAL件数 | 1（件数） | v40正本から算出、0〜195 | 非負整数スカラー |

**次元確認**：右辺の53件と95件はいずれも同じ次元1の資産件数であり、和の148件も単位整合。データセットとモデルの「登録件数」はこの式とは別の母集団なので混同しない。

## 6. H / T / D / C / U と ERROR CHECK

**H（反証可能仮説）**：公開ウェイト全面禁止確率に根拠のない数値を付けて候補数を増やすより、権利・総数・最終bundle・ディスクの第一停止要因から処理した方が、取得承認可能な独立学習成果の件数を増やせる。対象はv40 148資産、次回監査時点までに確認できた権利・hash・HDDゲートの解消数で評価する。

**T（最小検証）**：v40選定とreadinessをrepo IDで1対1で結合（n=148）、排他的第一停止要因を分類。実際の下流保存・評価では同一構成の最低30入力×3シードを候補ごとに検証し、資産単位で逐次的に権利・依存不備が出たところで停止する。

**D（合否基準）**：PASS＝148件repo ID一意、53/95区分、19＋9＋118＋2第一停止要因、権限0・ダウンロード0。FAIL＝重複・欠落・無許可取得・必要学習済みcomponent欠落。UNCERTAIN＝各個人のGated同意、政策変更の発生率、模型品質、実HDD余白、実際のoffline復元成否。

**C（破れ方）**：広域一括規制が先行する、同一基盤の微小LoRAに再現不能な独立価値が見つかる、逆に独自重みと思われたcheckpointが同一SHAコピーだった、あるいは権利条件改定により保存不可になる、という対立ケースで再分類する。

**U（不確かさ）**：一次model cardの変更、実repo版差、委託データの権利、継承されたアクセス情報の鮮度、GPU／backend差、HDDフォーマット・cache／staging不足が主要誤差源。実測分散がないため合成標準不確かさ`u_c`及び包含係数`k`での量的保証は**不能**。

**ERROR CHECK**：全195管理・148有効・53 SELECT・95 CONDITIONAL・47非有効、第一停止要因計148、Gated履歴20、未知総数9、146件のsource固定とbyte+SHA gate、取得準備PASS0、本人認可0、重みDL0、モデルコード実行0。Exa検索は2026-11-15に使用枠不足（HTTP 402）で失敗したため、一次公文書・配布元原文はWeb検索で検証。**全148件の現在の上流アクセスが独立実査済みである、とは主張しない**。

## 7.〈次に考える問い〉

**「追加するモデル名」より先に、現在の148件のうち最初に完全な原本・権利・依存・実機容量を証明できるのは何件か？** まずここがゼロから増えなければ、規制リスク対策としての保存可能性は改善しない。
