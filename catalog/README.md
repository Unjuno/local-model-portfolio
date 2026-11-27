## 現行 v75 / R171（2026-11-28）

266登録・210有効（SELECT 56、CONDITIONAL 154）。Qwen3-OmniをHOLD、独立した小型動画点追跡モデルRoboTrackerを研究限定CONDITIONALへ追加。全210取得STOP、既取得報告133件保存、取得承認・重量DL・物理削除0。[監査](../docs/strategy/171-v75-dependency-aware-composition-exchange.md)。以下の旧版記録は履歴。

## 履歴 v74 / R169（2026-11-27）

[CURRENT](CURRENT.json)：265登録・210有効。Llama 4 Scoutのみ正式HOLD、264行不変、既取得報告133件を保存。追加・交換・除外・重量DL・承認・物理削除0。[監査](../docs/strategy/169-v74-portfolio-composition-and-ledger-reconciliation.md)。

---

## R158／現行v67（2026-11-24）：独立日本語TTS2モデルを追加

[CURRENT](CURRENT.json)：**248登録／199有効**、旧246件不変。[32file／51,265,149,668byteのPublisher原本SHA](../manifests/drafts/r158-2026-11-24-aratako-trained-and-studio-distilled-publisher-originals.candidate.json)、[全199 STOP](readiness/v67-2026-11-24-r158-all199-gates.json)、[研究/ライセンス](../docs/strategy/158-v67-aratako-japanese-drama3-and-studio-distilled-12gb-tts.md)参照。Aratako35.9B BF16/FP8 LoRA日本語FTとStudio別学習small KL蒸留を別登録、Q4/Q5 GGUF形式重複は非採用。所有者実媒体SHA・ライセンス・CUDA ABI未検証、承認0・新規DL0。

---

## v65 R154／112取得台帳の全IDを正式目録へ照合

[正式CURRENT](CURRENT.json) は240登録・192有効。Timestral5M/WeMM-video2bは既存112 VERIFIED原本、Hereticの2小型LoRAを条件付き、Cartwheel3制御policyを第三者権利でHOLD。[監査](audits/2026-11-22-r154-all112-ledger-and-new-source-delta.json)、[8INT8差分](research/2026-11-22-r154-pico-eight-int8-extra-publisher-sha.json)、[判断報告](../docs/strategy/154-v65-post112-backfill-small-heretic-and-robot-rights.md)。承認0。

---

# 資産台帳

## R150最新運用照合／2026-11-22（正式v63 235/188は変更なし）

[235件全カタログの取得報告statusマップ](audits/2026-11-22-r150-all235-completion-status.json)、[RFD4中心モデルSHA同一・別推論variant](research/2026-11-22-r150-rfd4-core-weight-same-auxiliary-diff.json)、[研究報告](../docs/strategy/150-completion-audit-rfd4-and-historical-ci-recovery.md)。現在の99取得報告・1 Gated HOLDはowner現物実証ではない。旧テスト固有版の混同とNTFSパス解釈を修正、66x Pythonテストは**691 PASS**、全188件は引き続き個別権利・オフライン復元未確証で新取得STOP。正本そのものは[CURRENT](CURRENT.json)のv63。

---

## 現行v63／R148（2026-11-22）：取得済み99件のID整合と不正自動承認防止

[CURRENT](CURRENT.json)：**235登録／188有効、SELECT55／CONDITIONAL133**。[取得台帳99件差分とRFD4重み相違](research/2026-11-22-r148-ledger99-immutable-revision-drift.json)、[既保存4source49ファイル追加](../manifests/drafts/r148-2026-11-22-ledger99-four-untracked-trained-sources.candidate.json)、[研究・安全判断](../docs/strategy/148-v63-reconcile-99-acquisitions-and-block-implicit-approval.md)。全188アクティブは[取得STOP](readiness/v63-2026-11-22-r148-all188-gates.json)。Publisher SHAと所有者D現物の独立再ハッシュは分ける。再ダウンロード・追加承認0。

---

## 現行v62・2026-11-22（v61以前は履歴）

[CURRENT](CURRENT.json) →**231登録／184有効**、[Aurora2＋Mirage＋LFM3-VL親・Heretic改変原本](../docs/strategy/146-v62-rare-small-uncensored-vision-dual-master-selection.md)をCONDITIONAL4件追加。[新4repoの58 source file SHA](../manifests/drafts/r146-2026-11-22-aurora-mirage-lfm3-paired-source.candidate.json)、[全184STOP](readiness/v62-2026-11-22-r146-all184-gates.json)。旧227全て維持。publisher sourceのみ、owner HDD実測なし、今回重みDL/承認0。

---

## 現行v61・2026-11-22（v60以下は履歴）

[CURRENT](CURRENT.json)で**227登録・180有効**。FastFrames-S／MOSS-VL-Realtime／Cosmos3-Nano-Sim-Transferの3独立学習成果をCONDITIONAL追加。旧224件不変更。[判断・権利・固定コード](../docs/strategy/144-v61-video-realtime-world-model-source-selection.md)／[70ファイル／55.386GB source](../manifests/drafts/r144-2026-11-22-video-world-and-streaming-publisher-sources.candidate.json)／[177から180へ拡張した停止ゲート](readiness/v61-2026-11-22-r144-all180-gates.json)。owner HDD実測なし、取得承認0、危険コード未実行。

---

## 現行v60・2026-11-22（過去のv42などの「現行」は歴史）

唯一の正本：[CURRENT](CURRENT.json)→**224登録／177有効**。[本次選定](../docs/strategy/143-v60-three-small-originals-and-regulatory-triage.md)、[新3件immutable59files](../manifests/drafts/r143-2026-11-22-three-specialists-originals.candidate.json)、[全177STOP](readiness/v60-2026-11-22-r143-all177-gates.json)。旧221件の判断保持。取得承認0、所有者HDD・実行コード・本人権利未検証。

---

## 現行正本（main・v42／2026-11-15）

[CURRENT](CURRENT.json)→[全195資産・有効148](effective-portfolio-2026-11-15-v42.json)（SELECT53／CONDITIONAL95）。[正式v42の停止条件](../docs/strategy/94-v42-ltx-parent-gates-interim-export-policy.md)／[追加の一次証拠](research/2026-11-15-r93-hf-ltx-parent-gated-china-interim-kimi-review.json)／[148件キュー](../queues/proposed-v42-2026-11-15.json)／[95件アクセス](access/2026-11-15-v42-conditional-hub-gates.json)／[148件停止](readiness/v42-2026-11-15-r94-all148-gates.json)。3件LTX原本・権利監査の追記のみ、承認0。


## 旧v41（履歴・2026-11-15）

[CURRENT](CURRENT.json)→[195件／148有効](effective-portfolio-2026-11-15-v41.json)、SELECT53／CONDITIONAL95。[v41二訂正](../docs/strategy/92-v41-source-and-license-corrections.md)／[5ファイルLoRA](../manifests/drafts/v40-qwen-image21-step1500.candidate.json)／[148候補](../queues/proposed-v41-2026-11-15.json)／[95アクセス](access/2026-11-15-v41-conditional-hub-gates.json)／[148停止](readiness/v41-2026-11-15-r92-all148-gates.json)。承認0、全件採否変化なし。


## 旧v40（履歴・2026-11-15）

[CURRENT](CURRENT.json)→[全195登録（169モデル・26データ）／有効148](effective-portfolio-2026-11-15-v40.json)、SELECT53／CONDITIONAL95、HOLD28、DEFERRED13、EXCLUDED6。[v40の差分](revisions/v40-2026-11-15.json)／[学習済み原本の採否](../docs/strategy/90-v40-groundingpi-original-decision.md)／[28ファイルsource](../manifests/drafts/v39-groundingpi-source28.candidate.json)／[148件研究キュー](../queues/proposed-v40-2026-11-15.json)／[148依存](preparation/2026-11-15-insurance-bundles-v40.json)／[95アクセス](access/2026-11-15-v40-conditional-hub-gates.json)／[148停止ゲート](readiness/v40-2026-11-15-r90-all148-gates.json)。取得承認0、HDD/localSHA/実行未確認。旧v39の194件はそのまま保持。


## 旧版v38（履歴・2026-11-15）

[CURRENT](CURRENT.json)→[全193資産：167モデル・26データセット](effective-portfolio-2026-11-15-v38.json)、**SELECT53・CONDITIONAL93・HOLD28・DEFERRED13・EXCLUDED6／有効146件**。[v38追加2件の正式差分](revisions/v38-2026-11-15.json)／[一次重み原本と役割比較](../docs/strategy/86-v38-risk-aware-original-model-selection-2026-11-15.md)／[非実行146件の候補](../queues/proposed-v38-2026-11-15.json)／[依存準備146件](preparation/2026-11-15-insurance-bundles-v38.json)／[全146件停止条件](readiness/v38-2026-11-15-r86-all146-selection-gates.json)。Haru original BF16とGated Praxis DROID（全17 BF16 shard）をそれぞれ1モデルとして保存研究選定。Qwen3.5-2BはPraxisの外部依存、Wan2.2 VAEは既存資産の共有ファイル。実取得・HDD/本人権利・復元未確認、承認0。

## 旧版v33（履歴）


[CURRENT](CURRENT.json)→[全185資産：159モデル・26データセット](effective-portfolio-2026-11-15-v33.json)、**SELECT53・CONDITIONAL85・HOLD28・DEFERRED13・EXCLUDED6**。[公式重み・モデル内部に基づく3件追加採否](revisions/v33-2026-11-15.json)／[選定根拠と4件の非採用](../docs/strategy/77-v33-weight-content-selection-and-alternatives-2026-11-15.md)／[有効138件の非実行候補](../queues/proposed-v33-2026-11-15.json)／[138件の依存準備](preparation/2026-11-15-insurance-bundles-v33.json)。旧v32の182件は全件維持。取得承認0、Kumo学習済み総数・Perplexity個別アクセス権は未確定。

## 旧版v32（main・2026-11-14、履歴）

**R57現在の保存準備成果**：[公開元の固定ファイル23件と容量・SHA](research/2026-11-14-r57-v32-frozen-source-scopes.json)／[非実行の候補スコープ](../manifests/drafts/r57-v32-three-source-scopes.candidate.json)／[権利と重複の判断](../docs/strategy/57-v32-source-identity-and-packaging-audit.md)。182件の正式採否は変更なし。

v32当時は[履歴全件](effective-portfolio-2026-11-14-v32.json)が正本だった。**182資産（モデル156／データ26）、SELECT53、CONDITIONAL82、HOLD28、DEFERRED13、EXCLUDED6**。[全件](effective-portfolio-2026-11-14-v32.json)／[非実行135件取得候補](../queues/proposed-v32-2026-11-14.json)／[135件の依存](preparation/2026-11-14-insurance-bundles-v32.json)／[CONDITIONAL82件の公開メタデータ](access/2026-11-14-v32-conditional-hub-gates.json)／[追加採否](revisions/v32-2026-11-14.json)。

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
