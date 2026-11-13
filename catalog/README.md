# 資産台帳

## 現行正本（main・v32／2026-11-14）

[CURRENT.json](CURRENT.json)がv32を指定する。**182資産（モデル156／データ26）、SELECT53、CONDITIONAL82、HOLD28、DEFERRED13、EXCLUDED6**。[全件](effective-portfolio-2026-11-14-v32.json)／[非実行135件取得候補](../queues/proposed-v32-2026-11-14.json)／[135件の依存](preparation/2026-11-14-insurance-bundles-v32.json)／[CONDITIONAL82件の公開メタデータ](access/2026-11-14-v32-conditional-hub-gates.json)／[追加採否](revisions/v32-2026-11-14.json)。

**旧v31の179資産はすべて採否を変えず保持**。v32にDSpine・NVIDIA Diarization・RFD4の独立学習済み原本を3件追加。これらを通常の別精度コピーとみなさない。新しい3件も取得許可0。

## 旧版v31の正本（2026-11-13・履歴）

[CURRENT.json](CURRENT.json)が選定正本。[v31全179資産](effective-portfolio-2026-11-13-v31.json)はモデル153・データ26、SELECT53・CONDITIONAL79・HOLD28・DEFERRED13・EXCLUDED6。旧v19の150件を保持し29件を追加。

- [v31承認前の132件キュー](../queues/proposed-v31-2026-11-13.json)
- [v31依存・保全準備132件](preparation/2026-11-13-insurance-bundles-v31.json)
- [条件付き79件のGated再監査](access/2026-11-13-v31-conditional-hub-gates.json)：Gated17件、他の100件は当該監査の対象外
- [v31全件監査](audits/2026-11-13-v31-portfolio-assessment.json)

**採否選定はダウンロード承認ではない。取得承認キューは0件。容量上限は十進4TB、HDDの実空き200GBは別条件。以下のv3〜v9で「現行」「最新版」と書かれている箇所は当時の履歴であり現在値ではない。**


1つの論理的な資産につき1 JSON。モデル、データ、ランタイム、知識資料を同じ原則で管理する。
サブフォルダーは models、datasets、software、knowledge を用途に応じて作る。初回一括レビューは[119件](review-2026-10-30.json)で固定し、その後のリスク監視候補は[別台帳](risk-watch-2026-10-30.json)で重複を管理する。追加候補の個別JSONは models と datasets に置く。

## 分類を混ぜない

| 軸 | 例 |
| --- | --- |
| asset_kind | model / dataset / software / knowledge |
| tasks | text-generation / classification / OCR / ASR / TTS / video-generation 等の複数タグ |
| modalities | 入力と出力をそれぞれ text / image / audio / video / spatial 等で記録 |
| family | BERT / T5 / Qwen / LFM 等の系統名 |
| architecture | encoder-only / encoder-decoder / decoder-only / SSM / recurrent / hybrid 等 |
| parameter_layout | dense / MoE / hybrid。上の構造と別に記録 |
| training_stage | pretrained / post-trained / unknown |
| modifications | instruction-tuning / weight-edit / distillation / quantization 等 |
| source_relation | official / derivative / conversion / mirror / unknown |
| representations | safetensors等の形式とBF16等の精度を別々に記録 |

LFM3はモデルファミリーであり、音声や画像などの用途と並列の大分類ではない。複数用途でも保存先を複製しない。

## 選ぶ理由と出典URL（採用ゲート）

[採用基準](../policies/selection.md)に従い、**モデルとデータセットの全候補に、正確な直接リンクと個別の保存理由を必須**とする。理由は「人気」「性能が高い」「規制されそう」だけでは不足。「固有の能力・専門学習成果」「消えたら失うもの」「元モデルから再現できるか」「代替候補との差」を具体化する。

ファイルごとの既存フィールドは次のように対応する。

| 台帳 | 配布元リンク | 選定理由 |
| --- | --- | --- |
| `review-2026-10-30.json` | `items[].evidence_url` | `items[].reason` |
| `risk-watch-2026-10-30.json` | `items[].evidence_url` | `items[].why_preserve` |
| 個別資産 `models/*.json`・`datasets/*.json` | `source.url` または `evidence[].url`（直接リンク） | `selection.reason` |

**根拠の区別：** 実際のGated・公開停止・利用条件は`verified`相当の事実として一次資料URL・確認日を記録し、高性能・悪用可能性・配布方針変化は仮説として明示する。既存の`reason`は一次レビューの採用理由であり、**規制リスクの独立検証済み根拠ではない**。根拠のない理由を事実として補完しない。

**候補から採用への進行：** URL・具体的な保存理由・現在の権利/配布条件・リスク事実と仮説の分離が不十分なら`candidate`または`held`。十分な判断資料がある資産のみ選定する。ただし選定とダウンロードの承認は別。コミットSHA・選択バイト数・ハッシュの確定は後段のマニフェストで行う。情報のない欄は「未確認」と記録する。

## 必須の記録

asset_id、asset_kind、source、selection、review、facts、evidence、representations_requested、dependencies、manifest_pathを持つ。
不明はnullまたはunknown、未確認リストは空にしない。モデルはfacts.total_parametersに総数を整数で記録してもよいが、総数だけで除外しない。選定審査には3〜4ビット時の推定ピークRAM（重み・KVキャッシュ・実装オーバーヘッド・OSを含む）、前提のバックエンド・コンテキスト長・バッチ・量子化方式、根拠を追加する。見積未確定の場合は取得承認しない。
sourceは取得元の指定であり、存在確認が済んだという証明ではない。

evidenceには、確認日時、URL、対象リビジョン、確認内容、fact / publisher_claim / inferenceを記録する。秘密情報は書かない。

## 選定と取得を分離

- selection.state: candidate / selected / held / excluded。selectedは「保存したい」という選定判断。
- review.state: unchecked / reviewed / blocked。未確認のファイル容量やライセンスが残れば取得準備は完了しない。
- manifest_path: 固定した取得定義がなければnull。
- 実際の取得許可は queues/approved.json、取得・照合・実行の結果はHDDのstateに記録する。

この台帳にDownloadedやTestedを手入力して、実ファイルの検証記録の代わりにしない。


## 旧版v9の正本（2026-11-03・履歴）

- 2026-11-03時点の旧選定は**v9**。[effective-portfolio-2026-11-03-v9.json](effective-portfolio-2026-11-03-v9.json)に132件の選定・規制予測順位・コスパ監査・150Bゲートを統合。
- [revisions/v9-2026-11-03.json](revisions/v9-2026-11-03.json)は、旧v8で総数未確認だった25モデルを全件監査。13件に一次資料で確認した**モデル本体/主要コンポーネントの概数**を記録、12件は総数未確認としてロック停止。当時のモデル109件は **95通過・2除外・12未確認**。
- [検証方法](../docs/parameter-audit-v9-2026-11-03.md)、[非実行提案キュー](../queues/proposed-v9-2026-11-03.json)、[静的検査のCI](../.github/workflows/audit-parameter-cap.yml)。この確認はモデル実行・Gated同意・ダウンロード許可ではない。

## 旧版v8の正本（2026-11-03、履歴）

- [CURRENT.json](CURRENT.json) はv8で**総パラメータ150B以上のモデルのハード除外**を適用。すべてのMoE expertと独立した学習済みembedding/MTPを含める。主モデル125Bだけを使った過小判定は不可。
- [effective-portfolio-2026-11-03-v8.json](effective-portfolio-2026-11-03-v8.json) は**132資産（有効105、BACKLOG12、HOLD13、EXCLUDED2）**の現在ビュー。
- [revisions/v8-2026-11-03.json](revisions/v8-2026-11-03.json) が109モデルの全件ゲート。82件が150B未満、2件は除外、25件は総数未確認で最終lockを保留。
- [深掘り調査・一次資料](../docs/parameter-cutoff-v8-2026-11-03.md)と[取得承認前の審査順](../queues/proposed-v8-2026-11-03.json)を参照。規制予測S1→S2→S3とリソース費用を維持しつつ**150B除外条件を先に適用**する。

## 旧版v7の正本（2026-11-03、履歴）

- [CURRENT.json](CURRENT.json) は、baseからv6までの全履歴を保ったうえで、[v7 250Bハード上限](revisions/v7-2026-11-03.json)を適用する。
- [effective-portfolio-2026-11-03-v7.json](effective-portfolio-2026-11-03-v7.json) は追跡132件・有効105件・BACKLOG12件・HOLD14件・EXCLUDED1件の最新ビュー。
- [109モデルの一次データ照合](../docs/parameter-cutoff-v7-2026-11-03.md)では83件通過、Mistral Large 4を除外、25件未確認。250Bが不明なら取得用最終lock不可。
- [承認前の作業キュー](../queues/proposed-v7-2026-11-03.json)は予測S1/S2/S3・実行コスパの二軸を保つが、250Bハード除外と権利・容量チェックを超えない。

## 旧版v6の正本（2026-11-03、履歴）

- [CURRENT.json](CURRENT.json) にv6の「**全132件に対する容量/8GB実行可能性の証拠区分**」を追加。**規制シナリオS1→S2→S3の優先順位は変えない。**
- [effective-portfolio-2026-11-03-v6.json](effective-portfolio-2026-11-03-v6.json) は現行の132件の予測順位・リソース判定付き閲覧ビュー。モデル性能の実測結果や取得承認を示さない。
- [revisions/v6-2026-11-03.json](revisions/v6-2026-11-03.json) は増分容量/実行モード/オフロードの証拠区分であり、[コスパ監査](../docs/resource-cost-screen-v6-2026-11-03.md)と[二系統の作業案](../queues/proposed-v6-2026-11-03.json)を対応づける。

## 旧版v5の正本（2026-11-03、履歴）

- [CURRENT.json](CURRENT.json) が、immutable base97+v2〜v4の選定判断と、v5の**予測順位付け操作132件**を指定する。
- [effective-portfolio-2026-11-03-v5.json](effective-portfolio-2026-11-03-v5.json) は全132件をS1→S2→S3で並べた閲覧専用ビュー。有効105、延期12、保留15。**予測順位はダウンロード承認ではない**。
- [revisions/v5-2026-11-03.json](revisions/v5-2026-11-03.json) は採否・容量・権利条件を変えず、順位と予測の理由をすべての資産に付与した新しい正本の差分。
- [予測優先度の説明](../docs/selected-portfolio-v5-2026-11-03.md)と[調査キュー](../queues/proposed-v5-2026-11-03.json)を参照。以前のR0/R1/R2は**履歴分類**、現行の調査順位はv5のS1/S2/S3。

## 旧版v4の正本（2026-11-03、履歴）

- [CURRENT.json](CURRENT.json) が最新版の差分順序を指定する。[effective-portfolio-2026-11-03.json](effective-portfolio-2026-11-03.json) は**132件・有効105件の閲覧専用実体化ビュー**。
- [revisions/v4-2026-11-03.json](revisions/v4-2026-11-03.json) にIdolとgated DINOv3 ViT-H+の2件を、URL・固定版・容量根拠・権利ゲート付きで追加した。取得承認ではない。
- 前版[effective-portfolio-2026-11-02.json](effective-portfolio-2026-11-02.json)はv3履歴である。

## 旧版v3の正本（2026-11-02、履歴）

- [CURRENT.json](CURRENT.json)が正本のリビジョン・差分順序を指定する。
- [effective-portfolio-2026-11-02.json](effective-portfolio-2026-11-02.json) は初稿97件・v2差分・v3差分を反映した**閲覧専用の実体化ビュー**。重複管理対象は130件、有効選定103件。取得承認ではない。
- [revisions/v3-2026-11-02.json](revisions/v3-2026-11-02.json) は新規20件を採用/延期/保留に判定した唯一の差分。旧台帳のURL、判断理由は削除しない。
