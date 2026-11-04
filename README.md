# Local Model Portfolio

将来もAIをローカルで利用・比較・解析・追加学習できるよう、モデル、データ、実行環境を選び、保存するためのポートフォリオです。

**目的は、リポジトリをHDDに配置し、エージェントが承認済みの取得指示に従って保存・検証できる状態を作ることです。** 人気ランキングでも、重みをGitHubへ再配布する場所でもありません。

## 現行選定 v14（2026-11-04：Nanbeige維持・6件除外）

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
| [policies/limits.json](policies/limits.json) | 3.8TBの保存予算、空き容量、推定推論RAM上限 |
| [catalog/](catalog/README.md) | 資産ごとの用途、構造、由来、選定理由、未確認事項 |
| [manifests/](manifests/README.md) | 確定した取得元・コミット・ファイル名・バイト数 |
| [queues/approved.json](queues/approved.json) | ユーザーが取得を承認したマニフェストと処理順 |
| [AGENTS.md](AGENTS.md) | エージェントの作業範囲・停止条件 |
| [docs/workflow.md](docs/workflow.md) | HDD配置、承認、取得、検証の手順 |
| [config/local.example.json](config/local.example.json) | 公開しない実機設定のひな形 |

実データと進捗はGitの外の `AI_VAULT/store/` と `AI_VAULT/state/` に置きます。

## 固定する条件

- 4TB HDDの保存目標は **3,800,000,000,000バイト**。空きは原則 **200,000,000,000バイト以上**。既存ファイル・一時領域も考慮します。
- **現行v12では150Bを原則目安とし、超過モデルは高品質な量子化版のピークRAM<512GB実測・権利・速度を満たした場合だけ個別審査**し、150B未満の候補についても3〜4ビット量子化を前提とした**推定ピークRAMが512GB以上のモデルを除外**。400GB以下を推奨、400GB超512GB未満は要個別審査とします。未知・未検証は取得承認しません。推定には重みだけでなくOS・推論エンジン・KVキャッシュ・作業領域を含め、バックエンド・コンテキスト長・バッチ等を固定します。
- 将来の規制を断定せず、再取得困難性・研究価値・用途の多様性を優先します。保存の判断に「将来削除される確証」は要求しません。
- **保存の承認と実行の承認を分離**します。疑わしいモデルは研究資料として保管できても、自動ロードしません。
- 1件ずつ確認し、元重み・派生版・量子化版を区別します。未知の容量やハッシュを埋め合わせません。

## 最初の1件

[Qwen公式版の台帳](catalog/models/qwen3.8-27b-official.json)を用意しました。会話での選定は引き継ぎますが、現在の配布元、ファイル一覧、利用条件、依存関係の再確認が済むまで取得キューには入れません。

LFM3、BERT、T5、画像、OCR、音声・TTS、動画、ワールドモデル等は、同じ記録形式で順次追加します。モデル名を分類の大項目にはしません。
