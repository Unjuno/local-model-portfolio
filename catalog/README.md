# 資産台帳

1つの論理的な資産につき1 JSON。モデル、データ、ランタイム、知識資料を同じ原則で管理する。
サブフォルダーは models、datasets、software、knowledge を必要になったときに作る。今は models に最初の1件だけ置く。

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

## 必須の記録

asset_id、asset_kind、source、selection、review、facts、evidence、representations_requested、dependencies、manifest_pathを持つ。
不明はnullまたはunknown、未確認リストは空にしない。モデルはfacts.total_parametersに総数を整数で記録し、量子化前の規模を確認する。
sourceは取得元の指定であり、存在確認が済んだという証明ではない。

evidenceには、確認日時、URL、対象リビジョン、確認内容、fact / publisher_claim / inferenceを記録する。秘密情報は書かない。

## 選定と取得を分離

- selection.state: candidate / selected / held / excluded。selectedは「保存したい」という選定判断。
- review.state: unchecked / reviewed / blocked。未確認のファイル容量やライセンスが残れば取得準備は完了しない。
- manifest_path: 固定した取得定義がなければnull。
- 実際の取得許可は queues/approved.json、取得・照合・実行の結果はHDDのstateに記録する。

この台帳にDownloadedやTestedを手入力して、実ファイルの検証記録の代わりにしない。
