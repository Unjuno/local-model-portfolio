# Local Model Portfolio

**R74保存容量安全策（11月15日）**：v27原本全59,938ファイルを再検査し、[全135資産の公開元revision・SHAカバレッジ（R73）](docs/strategy/73-v32-135-publisher-file-identity-audit.md)を確定。Gated17資産・762ペイロードファイル・約785GBは配布元SHA未確定。さらに[66配布元・1,425ファイルの完全選択allowlist（R74）](manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)を作り、不要なrepo全量取得につながる観測差分約2.986TBを分離（[判断と容量比較](docs/strategy/74-v32-66-overfetch-prevention-2026-11-15.md)）。**研究・非実行であり、権利/依存/実機/取得承認は未完了**。

**R69固定runtime監査（11月15日）**：[IBM TTM R3の公式モデルSHA一致・公式granite-tsfmコードcommit・Python/PyTorch依存の具体的な範囲・不足しているimport経路](docs/strategy/69-ibm-ttm-r3-offline-runtime-evidence.md)／[機械可読証拠](catalog/research/2026-11-15-r69-ibm-ttm-r3-publisher-runtime-pin.json)。R68で有効135件の先頭調査ゲートを一意に整理（[監査結果](docs/strategy/68-v32-135-next-gate-triage-2026-11-15.md)／[全件JSON](catalog/readiness/v32-2026-11-15-r68-135-actionable-triage.json)）。**保存・実行・承認は未実施**。

**R64完成準備（11月15日）**：[全135件の取得ゲート台帳](catalog/readiness/v32-2026-11-15-r64-all-active.json)／[8資産91ファイルの取得前マニフェスト](manifests/drafts/r64-eight-source-scopes.candidate.json)／[実HDD読み取り専用監査手順](docs/strategy/65-v32-owner-offline-preflight.md)。保存完了を示すものではなく、承認済みダウンロード0件。

将来もAIをローカルで利用・比較・解析・追加学習できるよう、モデル、データ、実行環境を選び、保存するためのポートフォリオです。

**目的は、リポジトリをHDDに配置し、エージェントが承認済みの取得指示に従って保存・検証できる状態を作ることです。** 人気ランキングでも、重みをGitHubへ再配布する場所でもありません。

**運用の正本は `main` の `catalog/CURRENT.json`。新たな調査ブランチは作らずmain一本で更新します。**

**R61（11月14日）**：[Pruna P-H3高精度原本44ファイルとComfy圧縮カーブ形式・正確な容量比較](docs/strategy/61-pruna-original-vs-curve-and-precise-capacity.md)。原本の公開ソース部分 99,840,428,064 byte、完全同一SHAのmetadata重複を除いた固有部分 99,828,998,036 byte。ComfyのBF16/INT8/W4A8は別学習モデルと数えず、権利・実機・runtimeは未検証。取得承認0。


**R60（11月14日）**：[Pruna P-H3／MiniMax H3 Image原本のLICENSE比較・SHA重複・容量監査](docs/strategy/60-pruna-minimax-h3-licensing-and-format-audit.md)。Pruna15重み約99.8GB、MiniMax Image一形式約135.3GB。MiniMax H3動画とImageでText Encoder14ファイル約66.7GBを共有するが、両者は現行v32選定外。Pruna条件付き維持、原本HOLD、取得承認0。


**R57固定ファイル監査（11月14日）**：[3専門モデルの正確なソース部分23ファイル・6,191,586,316バイト](docs/strategy/57-v32-source-identity-and-packaging-audit.md)／[機械可読の公開元SHA・容量](catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json)／[非実行の取得前候補](manifests/drafts/r57-v32-three-source-scopes.candidate.json)。外部依存・権利・実機容量は未確定、取得承認0。

**現行の正本**：[v32／182資産（モデル156・データ26）](catalog/effective-portfolio-2026-11-14-v32.json)。SELECT53・CONDITIONAL82・HOLD28・DEFERRED13・EXCLUDED6、[有効135件の取得前キュー](queues/proposed-v32-2026-11-14.json)と[同135件の依存準備](catalog/preparation/2026-11-14-insurance-bundles-v32.json)が対応。[今回のDSpine/Nemotron/RFD4選定](docs/strategy/56-v32-small-specialist-selection-2026-11-14.md)。**すべて未承認で、本体DLは未実施。**

**歴史資料v31の選定構成**：[v31の179資産](catalog/effective-portfolio-2026-11-13-v31.json)（SELECT53・CONDITIONAL79・HOLD28・DEFERRED13・EXCLUDED6）／[132件の承認前キュー](queues/proposed-v31-2026-11-13.json)／[132件の依存準備](catalog/preparation/2026-11-13-insurance-bundles-v31.json)。[Gated監査](catalog/access/2026-11-13-v31-conditional-hub-gates.json)は条件付き79件のみ対象。正式取得承認は0件。**


## 旧版v31（2026-11-13・履歴）：楽曲生成能力の空白を補うACE-Step 1.5 XL Turbo

[CURRENT](catalog/CURRENT.json)は**179資産／有効132件**。現行178件にMERT音楽解析はあるがopen music generatorが欠けていたため、[ACE-Step/acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo)を独立8-step蒸留DiTとして**CONDITIONAL研究1件**追加。HF F32原本約20GBと音楽LM1.7B/Qwen Embedding/VAEの外部学習済み依存を分離。XL Baseは全タスク機能の別学習状態だが過剰収集回避のためHOLD。提供リンクのACE Music v1はサービス提供中、重み公開は確認できず、ACE Music公式は**v1 Flashの2026年末公開計画**だけを明記。購入/Cloud利用/取得承認を自動開始しない。4TB・200GB実空き床、未知20・150B超例外2、承認0は維持。[R53選定根拠](docs/strategy/53-ace-music-promise-and-ace-step-gap-v31.md)。以下v30以前は履歴。

## 旧版v30（2026-11-12）：Alpamayo 2 Edgeの独立運転VLA原本を条件付き追加

[CURRENT](catalog/CURRENT.json)は**178資産／有効131件**。新規条件付き研究`nvidia/Alpamayo2-Edge`は2,651,163,378総学習済みパラメータ、公開BF16二シャードの計約5.302GBを含む12ファイルの別後学習成果。既存Cosmos Sim-Autoの動画・LiDARシミュレーションでは生成できない64姿勢の運転軌道とChain-of-Causation説明を出す。原重み・ライセンス全文・固定runtimeコードが公開され、重み2シャードの旧/新revision SHA一致を監査。日本国内を含む用途での権利・別Gatedデータ、実機のLinux/H100以外での性能・自動運転安全性は未確認。モデル本体取得/実行・承認0、177旧資産・除外6・4TBと空き200GBを維持。[R50と採否](docs/strategy/50-alpamayo-edge-distinct-driving-policy.md)。以下v29以前は履歴。

## 旧版v29（2026-11-12）：ZONOS3-MiniとLingBot-Touch-Tinyの独立能力2件

[CURRENT](catalog/CURRENT.json)は**177資産／有効130件**（旧175件維持、研究用CONDITIONAL2件追加）。Zyphra ZONOS3-Miniの公開標準TTS・ZAC-1音声Codecと、Robbyant LingBot-Touch-Tinyの磁気／圧抵抗／視触覚JEPAの原本。ZONOS3公開repoには別形式が多いためPyTorch原本一構成に絞り、非公開の音声編集LoRAを取得対象としない。LingBot Smallは実ロボット評価根拠が不足して別HOLD。Alpamayo2 Edge／Praxis DROID／Simons297M／PAN2は研究HOLD。4TB・200GB物理空き・150B以上同等RAM実測・総数不明20モデルの取得STOP・承認0を維持。[原論文・取得ゲート](docs/strategy/47-nov12-distinct-modality-selection.md)。以下はv28以前の履歴。

## 旧版v28（2026-11-12）：小型独立学習BotPsyとIBM TTM R3

[CURRENT](catalog/CURRENT.json)は**175資産／有効128件**。新たに`qvac/BotPsy-0.8B`と`ibm-granite/granite-timeseries-ttm-r3`を独立学習成果としてCONDITIONAL研究採用。従来173件、6件EXCLUDED、HOLD28、4TB上限、200GB最低空き、150B超の同条件RAM例外とゼロ取得承認は維持。以前のv28-r1大型3モデル提案は未採用の研究候補。[評価と停止条件](docs/strategy/46-botpsy-ttm-v28-selection.md)。以下は履歴。

## 旧版v27：Kakao Kanana非生成型判断モデルとMOSS必須音声Codec

[CURRENT](catalog/CURRENT.json)は173資産・有効126件。Kanana 3.665Bの型付き確率判断（choice/noul/score）をBF16原本一式として条件付き研究選定。Kanana Open LicenseのNOTICE/利用条件・別途商用API/SI/端末組込権利が未確認で取得承認不可。MOSS-TTS v1.5の外部必須v1音声Codecを容量に計上、v2は混同しない。Ricursive Ripple 65Bの事前学習原本・後学習版は研究HOLD。4TB上限・最低空き200GB・150B以上量子化同等RAM・承認0を維持。[評価](docs/strategy/37-kanana-moss-archive-v27.md)・[容量](catalog/capacity/2026-11-07/v27/capacity-summary.json)。以下は履歴。

## 旧版v26：Cosmos Sim-AutoとPhononの独立学習成果3件

[CURRENT](catalog/CURRENT.json)は172資産・有効125件。車載WSM+LiDARのCosmos3 Nano Sim-Autoと音声Phononの英語31M・多言語40M原本を条件付き選定。40Mは現在Gated＋CC BY-NC4.0なので本人権限確認まで研究専用で取得不可。Phononの話者コーデック自体は未公開であり、既存の潜在話者のみ記録。BaIDU ERNIE5.5 Flash Base 280Bは総150B超の同等RAM未実測で研究HOLD。v25の旧169資産不変、外部依存に声の潜在とCosmos共通VAEを記録。4TB・200GB空き・同等RAM・取得承認0を維持。[詳細](docs/strategy/33-phonon-cosmos-ernie-risk-v26.md)・[容量](catalog/capacity/2026-11-06/v26/capacity-summary.json)。以下の版は履歴。

## 旧版v25：地域制限付き画像モデルの学習成果を条件付き研究選定

[CURRENT](catalog/CURRENT.json)は169資産・有効122件。PrunaAI/P-H3-Imageの8-step DMD蒸留・テキスト蒸留・専用VAE・学習済みプロンプト補完を別学習成果として1件conditional研究選定。MiniMax H3 Community License地域制限と総パラメータ未確定のため**最終取得ロック不可**。同一能力のComfy 4bitは二重採用せず。Maya2用Mimi/ECAPAの固定容量は別依存調査記録に記載。旧168資産を保持、v24の121件一次ファイル範囲は確定済み。4TB上限・実空き200GB・量子化後の同等RAM条件・取得承認0は維持。[根拠](docs/strategy/32-restricted-image-and-maya-dependencies-v25.md)・[容量](catalog/capacity/2026-11-06/v25/capacity-summary.json)。下のv24以前の数値は履歴。

## 旧版v24：2026年11月5日公開の独立学習成果3件

[CURRENT](catalog/CURRENT.json)は168資産・有効121件。PFN PLaMo3 Translate 31B教師と0.8B蒸留生徒、NVIDIA Cosmos3 Nano Sim-Bimanual行動条件付き世界モデルを3件追加。旧165資産不変。v23の118一次ファイル容量は監査済み、v24の新3件は別途容量再検証。4TB上限、実空き200GB、150B超量子化同等RAM審査、ダウンロード承認0は不変。[今回の選定根拠](docs/strategy/31-new-translation-and-robotics-selection-v24.md)・[容量台帳](catalog/capacity/2026-11-06/v24/capacity-summary.json)。下の記録は履歴。

## v23容量・公開状態の再照合（2026-11-06）

[118件の容量台帳](catalog/capacity/2026-11-06/v23/capacity-summary.json)・[最新公開状態](catalog/research/2026-11-06-latest-v23/freshness-summary.json)・[判断と限界](docs/strategy/30-v23-capacity-latest-check.md)。原本の固定選定と上流の現在版を区別。完全復元依存・保存先実空き・取得承認は別工程。

## 旧版v23：容量監査に基づく独自学習成果2件の追加

[CURRENT](catalog/CURRENT.json)は165資産・有効118件。v22の116件の一次ファイル範囲が確定した後、Hcompany/Holotron4-30B-A3BのNemotron後学習原本とLiquidAI/LFM2.5-24B-A2B-DSparkの学習済み投機ドラフターを条件付き選定。既存163件は不変。新2件の配布元全repo公称バイトは66,707,531,084であり最終採用ファイルや実ディスク必要量ではない。4TB上限、200GB実空き床、150B以上の量子化同等RAM条件、取得承認0件を維持。[選定根拠](docs/strategy/29-bounded-specialized-selection-v23.md)・[v22容量監査](catalog/capacity/2026-11-06/capacity-summary.json)。下のv22以前は履歴。

## 容量監査（2026-11-06）：全116件の固定ファイル一覧

[容量集計](catalog/capacity/2026-11-06/capacity-summary.json)・[全件表](catalog/capacity/2026-11-06/capacity-report.md)・[ファイル別証拠](catalog/capacity/2026-11-06/selected-file-capacity.json)。配布庫全量と選択形式を分離し、共有依存の繰り返しを除く。確定小計は配布元metadataの計算であり実ディスク使用量ではない。完全復元に必要な依存・実行環境、Granaryの許可subset、実機空き容量は未確定。v22の163管理／116有効、取得承認0を維持。

## 旧版v22：学習成果を失わないための保険

[CURRENT](catalog/CURRENT.json)は163資産・有効116件。規制予測は先に確保する順番であり、保全対象をそこだけに限定しない。[保険方針](policies/archival-insurance.json)・[116件の段階別準備表](catalog/preparation/2026-11-06-insurance-bundles-v22.json)・[採用理由](docs/strategy/27-insurance-first-selection-v22.md)。Drama3公開元原本、DavidAU独自後学習、GroundGUI定位、Consistency LoRA差分を4件conditionalとして追加。全159旧レコード、4TB枠、200GB空き、150B超の量子化同等RAM条件を維持。追加計画枠156GBは実測容量ではない。取得承認0。以下v21以前の件数は履歴。

## 旧版v21：配布制限の証拠と独自能力による追加選定

[CURRENT](catalog/CURRENT.json)・[159資産](catalog/effective-portfolio-2026-11-06-v21.json)・[112件の非実行キュー](queues/proposed-v21-2026-11-06.json)。Holo4-27B、SteerTTS、Maya2 Native、Hcompany公開評価軌跡を4件conditionalに追加。StyleStreamは一部非公開・総数未確定のためHOLD。追加計画枠92GBは実測容量ではない。4TB上限、実空き200GB、150B超の量子化同等RAM規則、取得承認0は維持。[判断と一次出典](docs/strategy/26-risk-evidence-selection-v21.md)。以下のv20以前の件数は履歴。

将来もAIをローカルで利用・比較・解析・追加学習できるよう、モデル、データ、実行環境を選び、保存するためのポートフォリオです。

**目的は、リポジトリをHDDに配置し、エージェントが承認済みの取得指示に従って保存・検証できる状態を作ることです。** 人気ランキングでも、重みをGitHubへ再配布する場所でもありません。

## 2026-11-06追補：150B超も量子化後に同等RAMなら選定対象

**150Bは絶対除外ではない。** 同条件で測定した150B未満の固定比較モデルに対して、量子化版の実行ピークRAMが同等以下であれば、総150B以上でも選定可能とする。MoEは全expert・PLE・MTP・外部学習済み部品の総数を記録。両者ピーク512GB未満、品質・速度・4TB選定予算・実空き200GB・固定SHA・正規権利・承認は独立ゲートであり、重量ファイルの大きさをピークRAMとみなさない。

[同等RAMの検証規則](docs/strategy/25-quantized-equivalent-memory-2026-11-06.md)・[大型量子化4候補の非実行調査](catalog/research/2026-11-06-over150b-memory-equivalence.json)。**既存154資産／有効108件は不変**。現行の超150B原本2件はHOLD、重み取得／クラウド課金／実行の許可は0。

## 旧版選定 v20（2026-11-06：4TB枠・Cascade2を正式選定）

- [CURRENT](catalog/CURRENT.json)・[154資産の全件ビュー](catalog/effective-portfolio-2026-11-06-v20.json)・[108件の非実行キュー](queues/proposed-v20-2026-11-06.json)。
- Cascade2原本、RLデータ、SFTの数学証明＋agentic SWE部分を3件conditionalとして正式追加。Orca27B FP8は重複のためdeferred。
- 保存予算は十進4TB。追加3件に計165GBの計画上限を割当。約134.5GBという表示容量の合算は概算であり最終lockではない。SFT全593GBは選ばない。
- [採用理由・負の根拠・容量管理](docs/strategy/24-selected-cascade-4tb-v20.md)。実空き・全依存・権利・固定SHA未確定、ダウンロード承認0。過去節の3.8TBは旧方針で、現在の数値はpolicies/limits.jsonが正本。

## 旧版選定 v19（2026-11-06：規制シナリオ下の超高効率小型モデル）

- **[CURRENT](catalog/CURRENT.json)**・[v19全150資産](catalog/effective-portfolio-2026-11-06-v19.json)・[取得未許可の105件キュー](queues/proposed-v19-2026-11-06.json)。
- **新規6件CONDITIONAL**：IFM K2-Horizon 0.9B（公開総数約1.078B、名称と相違）、Liquid LFM3-1.7B（既存Baseとは別のagent後学習）、Liquid LFM2.5-VL-3B＋DSparkドラフター、Udgam Labs Lilavati＋Checker 95M×2（sandbox付きプログラム推論）。
- **主重み6個の元LFSファイルSHAとbyteを確認**：合計12,799,213,698 byte（約12.799GB）。**全ファイルの固定コミット・tokenizer/LICENSE/補助コード・ハード・取得後のハッシュ・容量は未完了**。ダウンロード許可は0件。
- **[R26調査と中国規制の一次資料](docs/strategy/23-small-frontier-regulation-2026-11-06.md)**、[代替案込み台帳](catalog/research/2026-11-06-small-model-r26.json)、[超小型高性能の判定基準](policies/small-model-advancement-evidence.md)。
- 「人間を超えたら一律にモデル重みを禁止する」正式閾値は未確認。2026-04-30 CACは危険な公開モデル/データの管理不備を取締り対象と明記。2026-10-16商務部・科技部は技術輸出管理の改訂案と暫定登録を公表、**既に公知・オープンソースの技術を管理対象から除く方針**も示した。**規制の事実と将来予測を区別**。

## R25 保存準備の完成度と実機事前診断（2026-11-05）

- **[完成度チェックリスト](catalog/preparation/2026-11-05-completion-readiness.json)**：重点2構成の16確認項目中8件に証拠あり（項目数50%。作業量・HDD保存完了率ではない）。実機の保存率は**不明**。
- **[読み取り専用のHDD検査ツール](scripts/archive_preflight.py)**：R21固定版の47ファイルを対象に、HDD空き、既存ファイルのSHA256/Git blob、重複容量をチェック。ユーザーが実機パスを指定し、`--hash`で全ファイル同一性を確認するまで基盤を「保存済み」としない。
- **[検証手順と限界](docs/strategy/21-archive-readiness-r25.md)**：stagingと既存容量を与えない場合は`UNCERTAIN`。PASSでもダウンロード承認とは別。Remote Desktop Commanderに接続PCがないため今回の実機状態は未測定。
- 正式カタログv18の144資産／有効99件、Nanbeige維持、指定除外6件は**変更なし**。approvedキュー0。

## 旧版選定 v18（2026-11-05：R21/R22固定保存証拠から2件を条件付き採用）

- 正本：[CURRENT](catalog/CURRENT.json)／[v18全144資産](catalog/effective-portfolio-2026-11-05-v18.json)／[非実行選定キュー99件](queues/proposed-v18-2026-11-05.json)。
- **新規条件付き2資産**：ChatR LabsのQwen-Image-2.1専用rank128 LoRA（基盤重複取得禁止）、Interpretic Qwen3.8-27B Uncensored v2 Q4＋vision projector（元BF16重みの重複取得禁止）。どちらもR21/R22で完全保存構成のtensor数・固定byte・選択SHAを監査済み。独立の生成品質とユーザー実機ランタイムは未検証。
- R21固定候補構成は2パッケージ計**51,541,147,139バイト**。ChatRの基盤を既存と同一と実機ハッシュ検証できた場合だけLoRA関連約0.671GBに増分削減できる。
- [新規選定・誤差・中止条件](docs/strategy/20-promote-pinned-packages-v18.md)を参照。**最終取得承認0・実機操作0・Torrent0**。

## 旧版v17の履歴（2026-11-04：個人非商用研究のライセンス判断改訂）

[CURRENT v17](catalog/CURRENT.json)／[142資産のv17ビュー](catalog/effective-portfolio-2026-11-04-v17.json)／[研究候補97件](queues/proposed-v17-2026-11-04.json)。`license:unknown`は研究候補の自動除外理由ではない。LTX2.5のChrisColeTechとStuubsを研究専用conditionalに変更。取得許可0、全学習済み総数不明のままfinal lock不可。[新しい行為別権利ルール](policies/personal-research-rights-v17.json)／[監査報告](docs/strategy/13-personal-research-license-screening.md)。

## 旧版v16の履歴（2026-11-04：無検閲SFT・成人向け動画と採否判定規則）

- **[現在の正本](catalog/CURRENT.json)**／[全142資産のv16ビュー](catalog/effective-portfolio-2026-11-04-v16.json)／[有効95件の非実行候補キュー](queues/proposed-v16-2026-11-04.json)。
- **[採否判定規則](policies/selection-decision-v16.json)**／[判断手順と一次資料](docs/strategy/12-v16-model-judgment-research.md)／[5件の調査判定台帳](catalog/research/2026-11-04-v16-candidate-decisions.json)。厳格な権利・品質・独自性・総数・容量・実機RAMの独立ゲートで評価。低拒否だけでは採用しない。
- **3モデル追加**：Gemma4 MoEベースのPantheon RP/SFTを**conditional**（RP第三者評価に強み、一般文章は弱い）。LTX2.5成人向け派生のChrisColeTech・Stuubsは**HOLD**（権利・全依存・比較品質不足）。Civitai CyberRealistic v10とJonathanColetti無検閲27Bは比較台帳のみ。
- **承認済みダウンロード0**。HDD、旧キュー、Torrent、本人Gated認証を変更していない。

## 旧版v15の履歴（2026-11-04：モデル5件追加・Pirate Face調査）

- **正本**：[CURRENT](catalog/CURRENT.json)・[v15 全139資産](catalog/effective-portfolio-2026-11-04-v15.json)・[提案キュー94件](queues/proposed-v15-2026-11-04.json)。有効94、HOLD27、除外6。
- **新規**：Galvanize-3（select）、Audio8 Air・LTX2.5・Kandinsky6 Lite（conditional）、Opus Moderation4 Neo（HOLD）。旧Audio8とLTX2.3を重複評価のためHOLDへ。
- **代替配布**：[Pirate Face/Civitai一次調査](docs/strategy/11-additions-pirateface-civitai.md)。Pirate Faceに2原本revisionを確認したがSeeder0、Civitai画像v10は有料アクセスや配布権利未確認。torrentは自動利用しない。
- **承認**：現時点0件。HDD・実機・量子化品質・ライセンス/本人Gated許可・版固定の独立ゲートは維持。

## 旧版v14の履歴（2026-11-04：Nanbeige維持・6件除外）

- **正本**：[CURRENT v12](catalog/CURRENT.json)／[全134資産のv12ビュー](catalog/effective-portfolio-2026-11-04-v14.json)／[量子化例外調査キュー](queues/proposed-v14-2026-11-04.json)。有効選定は92件、150B超の量子化候補2件は**HOLD**、総数不明12件は取得準備停止。
- **150Bは絶対上限ではない**：総パラメータ数の原則目安。1.05T Mistral Large 4／180B OrcaRouter Flash Nextは公式/量子化配布元を確認したが、ユーザー環境のRAMと品質・速度・権利の実証がないため未採用。MoEは全expertの総数を使用。
- **上限**：OS・KV・依存込み実行ピーク<512GB（十進）、400GB超は個別審査。完全manifest・固定revision・ライセンス本文・本人Gated許可・選択byte・実機測定・明示承認がない限りダウンロードは不可。
- **検証資料**：[v12レポート](docs/strategy/08-quantized-over150-exceptions.md)／[標準ライブラリの静的チェック](scripts/check_parameter_cutoff.py)。旧v8-v11の「150B以上を必ず除外」は**歴史的な方針であり失効**した。README以下の旧版見出しは履歴として残す。

- **[v13最新性能調査](docs/strategy/09-current-hf-uncensored-performance.md)**：2026年Qwen3.8-27Bの別編集方式で、実在公開GGUFをconditional追加。別途Gated再現可能NVFP4をHOLD追加。性能の負の証拠も記載し、旧GGUFに自動回帰しない。

- **[v14選定変更](docs/strategy/10-user-pruning-nanbeige.md)**：Nanbeige4.3-33Bをselectへ昇格、直前の低優先6件をexcludedに変更。実ファイルは削除せず、選定候補キューから除外。

## 旧版v9の履歴（現行版はv14）

- **[未確認25モデルの一次資料監査](docs/parameter-audit-v9-2026-11-03.md)**：13件で配布者が示す名前付きモデル/主要構成部品の規模を確認、12件は総数の根拠不足として引き続き保留（うち有効選定7件）。現在の109モデルは **95件がパラメータゲート通過・2件が150B以上で除外・12件が未確認**。
- **[CURRENT v9](catalog/CURRENT.json)**／[132件の現在ビュー](catalog/effective-portfolio-2026-11-03-v9.json)／[25件の新規証拠](catalog/revisions/v9-2026-11-03.json)／[非実行の提案キュー](queues/proposed-v9-2026-11-03.json)。
- **[読み取り専用の150B検査](scripts/check_parameter_cutoff.py)**と[単体テスト](tests/test_parameter_cutoff.py)、[CIワークフロー](.github/workflows/audit-parameter-cap.yml)を追加・更新。予測S1→S2→S3、HDD3.8TB上限/空き200GB、推論RAM<512GBは変更なし。
- **主モデルのパラメータ数が150B未満でも、補助Encoder・VAE・Codecの権利/容量・最終ファイルと実機実行条件は別ゲート**。未確認の主モデル総数は0扱いせず、最終lock停止。**ダウンロード承認は0件です**。

## 旧版v8（2026-11-03、履歴）

- **[Exa深掘り調査と109モデルの150B判定](docs/parameter-cutoff-v8-2026-11-03.md)**：総150B未満82件、150B以上2件、総数未確認25件。以前HOLDだったOrcaRouter Qwen3.8 Flash Next Uncensored（約180B）を新規EXCLUDEDに変更。Mistral Large 4（約1.05T）の除外を維持。
- **[CURRENT v8](catalog/CURRENT.json)**／[現行132件の確定選定ビュー](catalog/effective-portfolio-2026-11-03-v8.json)／[v8総数監査](catalog/revisions/v8-2026-11-03.json)／[承認前v8キュー](queues/proposed-v8-2026-11-03.json)。
- **[読み取り専用の総数ゲート検査](scripts/check_parameter_cutoff.py)と[境界値・MoEの単体テスト](tests/test_parameter_cutoff.py)** を150Bに更新。GPU 8GBで実験的に動くかどうかは150Bを超える除外規則の例外にならない。ユーザー実機でのテスト・モデル実行は未実施。
- 3.8TB保存予算と200GB空き安全余白、512GB未満の推論RAM上限、規制予測S1→S2→S3は維持。**本体ダウンロード承認0件・モデル実行0件。**

## 旧版v7（2026-11-03、履歴）

- **[総パラメータ250B上限の復活と109モデル監査](docs/parameter-cutoff-v7-2026-11-03.md)**。83件は250B未満、25件は総数未確認で最終取得lock不可、Mistral Large 4（約1.05T）1件は厳格除外。**総パラメータは活性MoE数ではなく全expertを含む**。
- **[旧版v7](catalog/revisions/v7-2026-11-03.json)**／[132件の旧ビュー](catalog/effective-portfolio-2026-11-03-v7.json)／[v7全モデルパラメータゲート](catalog/revisions/v7-2026-11-03.json)／[v7の承認前作業キュー](queues/proposed-v7-2026-11-03.json)。
- 当時は250Bゲートを新設。現在の[検査スクリプト](scripts/check_parameter_cutoff.py)と[単体テスト](tests/test_parameter_cutoff.py)はv8の150B基準に更新済み（実機実行は未確認）。
- 規制のS1→S2→S3シナリオ、実行コスパ、HDD3.8TB上限、推論RAM512GB未満の追加条件は維持。ただし**250Bの除外条件が先**。ダウンロード承認0件、実機モデル実行0件。

## 旧版v6（2026-11-03、履歴）

- **[132件の全件コスパ監査](docs/resource-cost-screen-v6-2026-11-03.md)**。5GB未満38件、5〜15GB 18件、15〜50GB 17件、50GB以上31件、容量未確定28件（全て上流repoの値）。有効105件のうち100GB以上が9件・計約1.559TB。
- **[CURRENT v6](catalog/CURRENT.json)**／[全132件の予測順位とリソース判定](catalog/effective-portfolio-2026-11-03-v6.json)／[v6資源評価の差分](catalog/revisions/v6-2026-11-03.json)／[保存と実行を分けたv6作業キュー](queues/proposed-v6-2026-11-03.json)。
- **Qwen3-Coder-Next 8GB VRAM検証は、RTX3070Ti laptop + RAM32GB + SSDからFP8 expert streaming（約1.8 token/s）の第三者単独報告**。元重み約159GBが8GBに収まることや高速な実用性を保証するものではない。モデル実行コードのインストール・改変はしない。
- S1→S2→S3の規制予測順位は維持し、大型でも希少な原本はアーカイブ候補に残す。小型でも依存やRAMが未知なら実機実行可能としない。**モデル取得承認0件。**

## 旧版 v5（2026-11-03、履歴）

- **[v5の保存判断と規制連鎖シナリオ](docs/selected-portfolio-v5-2026-11-03.md)**：132件をS1（先行的な悪用/合成/権利リスクの制限）→S2（高性能AI一般）→S3（オープンウェイト全体）の仮説に従って優先順位付け。**S1に45件**（有効27・保留/延期18）。予測上の段階は法律の施行予定や確率ではない。
- **[CURRENT v5](catalog/CURRENT.json)**／[全132件・順位付きビュー](catalog/effective-portfolio-2026-11-03-v5.json)／[v5差分](catalog/revisions/v5-2026-11-03.json)／[S1→S2→S3調査提案キュー](queues/proposed-v5-2026-11-03.json)。
- **[規制予測と権利確認を区別する判定規約](policies/capability-access-risk.md)**：予測リスクが保存優先度の主軸。現在のGated・許諾・同意・法令は独立した必須取得ゲート。
- **旧初回3件の小容量マニフェスト案はダウンローダー安全試験用**。規制予測上の優先保存対象とは別。すべて未承認。

**モデル・データ本体のダウンロード承認は0件です。** 予測だけでアクセス制限を回避したり、権利不明の重みを取得しない。

## 旧版v4（2026-11-03、履歴）

- **[v4当時の選定：132件、うち有効105件](docs/selected-portfolio-v4-2026-11-03.md)**（select 54 / conditional 51、延期12、保留15）。旧v3の130件に、[Idol単一画像→3DGSモデル](https://huggingface.co/speridlabs/idol)と必要な[手動GatedのDINOv3 ViT-H+](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m)を条件付きで追加。
- **[現行ポインタ](catalog/CURRENT.json)**／[132件の機械可読ビュー](catalog/effective-portfolio-2026-11-03.json)／[v4の追加差分](catalog/revisions/v4-2026-11-03.json)。
- **[高性能・悪用・将来の配布制限の検証規範](policies/capability-access-risk.md)**：確認済みのGated等と、将来の規制に関する仮説を明確に分ける。高性能だけでは規制予定としない。
- **[Idolの固定コミット・コア7ファイル（約3.079GB）の承認前取得案](manifests/drafts/idol-core-2026-11-03.candidate.json)**。DINOv3とFLUX.2 VAEは別依存として権利/固定版を検証するまで取得しない。

**全資産のダウンロード承認は引き続き0件です。** 所有・研究・実行・再配布の承認を混同しません。

## 旧版 v3 の選定（2026-11-02／履歴）

- **[v3当時の130件の選定・延期・保留の判断](docs/selected-portfolio-v3-2026-11-02.md)**：有効103件（select 54 / conditional 49）、延期12件、保留15件。11件の特化モデルを有効選定し、既存の重複懸念2件を延期。
- **[CURRENT.json：v4正本への参照](catalog/CURRENT.json)**／[確定した選定130件の機械可読ビュー](catalog/effective-portfolio-2026-11-02.json)／[v3差分](catalog/revisions/v3-2026-11-02.json)。この選定は**ダウンロード承認ではない**。
- **[取得前固定案3件・5,130,218,354バイト](manifests/drafts/README.md)**：Qwen3.5-0.8B、LightOnOCR-3-0.8B、Whisper-large-v3-turbo。完全な40文字コミットとファイルごとの整数バイト/取得元SHA-256（存在する場合）を記録。権利・実機RAM・依存・HDD確認が終わるまで利用不可。
- **[Pirate Face等の代替配布元の扱いと追加20候補の評価](docs/specialized-candidate-triage-2026-11-02.md)**。合法性、同意、元の完全ファイルSHA-256照合、seeding禁止を取得と独立して審査。

- **[4TB HDDの3.8TB利用方針と残余枠の再選定](docs/storage-budget-policy-2026-11-02.md)**：3.8TBは選定上の上限。ユーザー申告の実用容量は約3.8TBだが、総容量・空き容量・TB/TiB単位は未確認。仮に実容量が十進3.8TBなら200GBの安全空きを残すため保存上限は約3.6TB以下。v3計画との差518GBを物理的な空き容量として扱わず、実機計測と依存・作業領域を確認してから追加選定する。

**現段階ではダウンローダー未実装・取得承認キュー0件・本体取得0件です。** 未承認の保存やモデル実行を開始しない。

## 旧版の採用ポートフォリオ（2026-10-30／履歴）

- **[初稿：97件の採用・条件付き・保留判断と、各モデル/データのリンク・選定理由](docs/selected-portfolio-current.md)**
- **[機械可読の初稿選定台帳（97件）](catalog/selected-portfolio-2026-10-30.json)**
- **[小型・高効率モデル25件の上流ファイル容量・SHA監査](catalog/snapshots/2026-10-30-disruptive-compact-1.json)**（続きは [2](catalog/snapshots/2026-10-30-disruptive-compact-2.json)、[3](catalog/snapshots/2026-10-30-disruptive-compact-3.json)、[4](catalog/snapshots/2026-10-30-disruptive-compact-4.json)）

**優先対象は、規制・配布条件変更による再取得困難性だけではありません。** 小型で既存のOCR・ASR・画像制作・3Dアセット・ロボット・時系列・検索サービスの一部を代替し得る独自モデル、専門ファインチューニング重み、貴重なデータも選定対象です。実際の産業への影響や規制の予測は仮説として区別します。

## 過去の採用候補レビュー（72件の時点／履歴）

- **[採用候補72件を優先順に整理した一覧（理由・リンク付き）](docs/selected-portfolio-2026-10-30.md)**
- **[機械可読の採用判断・リスク区分・確認事項](catalog/selected-portfolio-2026-10-30.json)**
- **[最優先Gated・最新公開モデルの改訂IDとバイト単位ファイル台帳](catalog/snapshots/2026-10-30-r0-gated-1.json)**（残りの台帳は [その2](catalog/snapshots/2026-10-30-r0-gated-2.json)・[参照モデルとデータ](catalog/snapshots/2026-10-30-reference-and-datasets.json)・[最新公開モデル](catalog/snapshots/2026-10-30-new-releases.json)・[最新データ](catalog/snapshots/2026-10-30-new-datasets.json)）

R0は現在Gatedなどの制限が確認され、まず取得条件を調べるもの（13件）。R1は専門学習などの復元困難性を重視したもの（30件）。R2は比較原本・構造多様性・データ基盤（20件）。HOLDは権利・個人情報・ライセンス矛盾・実行容量の未解決（9件）。**採用選定とダウンロード許可は別**であり、正確なファイル合計容量・完全コミット・必要な権利条件がそろうまで取得キューは空のままです。

**2026年10月30日の更新：最優先13件の上流全ファイル容量は合計851,771,058,386バイト。** 全13件に40文字の改訂IDと各ファイルの上流サイズを記録しました。これは選択後の取得容量ではありません。また10月29日公開のMistral Large 4など7件を調査対象に加えています。現時点のダウンロード承認は0件です。

## 最新の一括選定レビュー（2026-10-30）

- [分類別の採否・根拠・暫定3.8TB予算（119資産）](docs/portfolio-decisions-2026-10-30.md)
- [機械可読の全件レビュー（モデル96・データセット14・ソフト9）](catalog/review-2026-10-30.json)
- [消失・アクセス制限リスクの継続調査（監視29件・うち既存119件外18件）](docs/risk-watch-2026-10-30.md)
- [リスク監視の機械可読データ](catalog/risk-watch-2026-10-30.json)

このレビューは保存優先度の**一括判定**であり、取得ファイルの完全なバイト数、モデルの動作保証、ライセンス許諾、実行承認を示すものではありません。取得キューは空のままで、ダウンロードは未開始です。

## 現在地

**整理用の構成・記録形式・作業手順を用意した段階です。ダウンローダーは未実装、確定した取得マニフェストは0件、取得承認キューは空です。** クローンだけではモデルは取得されません。

以前の会話・表にある概算容量や「採用」は、固定したファイル一覧へのダウンロード承認と区別します。モデル本体の取得、HDDへの配置、実機検証はこの変更では行っていません。

## 役割を分ける

| 場所 | 記録するもの |
| --- | --- |
| [policies/selection.md](policies/selection.md) | なぜ保存するか、採用・除外の基準 |
| [policies/limits.json](policies/limits.json) | 4TBの選定計画上限、最低実空き200GB、推論RAMの条件 |
| [catalog/](catalog/README.md) | 資産ごとの用途、構造、由来、選定理由、未確認事項 |
| [manifests/](manifests/README.md) | 確定した取得元・コミット・ファイル名・バイト数 |
| [queues/approved.json](queues/approved.json) | ユーザーが取得を承認したマニフェストと処理順 |
| [AGENTS.md](AGENTS.md) | エージェントの作業範囲・停止条件 |
| [docs/workflow.md](docs/workflow.md) | HDD配置、承認、取得、検証の手順 |
| [config/local.example.json](config/local.example.json) | 公開しない実機設定のひな形 |

実データと進捗はGitの外の `AI_VAULT/store/` と `AI_VAULT/state/` に置きます。

## 固定する条件

- 現行の選定計画上限は **4,000,000,000,000バイト**。実際のHDDは **200,000,000,000バイト以上の空き**を維持し、既存ファイル・cache/staging・フォーマット後容量を別に検査する。既存ファイル・一時領域も考慮します。
- **現行ポリシーでは150Bを原則目安とし、超過モデルは高品質な量子化版のピークRAM<512GB実測・権利・速度を満たした場合だけ個別審査**し、150B未満の候補についても3〜4ビット量子化を前提とした**推定ピークRAMが512GB以上のモデルを除外**。400GB以下を推奨、400GB超512GB未満は要個別審査とします。未知・未検証は取得承認しません。推定には重みだけでなくOS・推論エンジン・KVキャッシュ・作業領域を含め、バックエンド・コンテキスト長・バッチ等を固定します。
- 将来の規制を断定せず、再取得困難性・研究価値・用途の多様性を優先します。保存の判断に「将来削除される確証」は要求しません。
- **保存の承認と実行の承認を分離**します。疑わしいモデルは研究資料として保管できても、自動ロードしません。
- 1件ずつ確認し、元重み・派生版・量子化版を区別します。未知の容量やハッシュを埋め合わせません。

## 最初に検討した1件（履歴）

[現行のv31選定台帳](catalog/effective-portfolio-2026-11-13-v31.json)にはQwen3.8-27B公式原本が登録されています。会話での選定は引き継ぎますが、現在の配布元、ファイル一覧、利用条件、依存関係の再確認が済むまで取得キューには入れません。

LFM3、BERT、T5、画像、OCR、音声・TTS、動画、ワールドモデル等は、同じ記録形式で順次追加します。モデル名を分類の大項目にはしません。
