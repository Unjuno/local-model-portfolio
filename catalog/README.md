# 資産台帳

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
