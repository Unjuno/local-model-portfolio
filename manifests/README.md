# 確定した取得指示

このディレクトリには、調査後に固定した `*.lock.json` だけを置く。現在は0件。
モデル名やURLの一覧は取得指示ではない。全量子化版を暗黙に取得しない。

## Hugging Face取得定義の契約

| 項目 | 内容 |
| --- | --- |
| schema_version | 1 |
| asset_id | catalogのID |
| source | provider、repo_type、repo_id、完全な固定commit SHA |
| files | 空でない配列。各要素にpath、size_bytes、source_sha256 |
| total_bytes | 選択したファイルのsize_bytesの合計 |
| dependencies | 必要な別マニフェストとそのSHA-256。依存の確認が済んで初めて空にできる |
| license_review | 本文の出典、対象版、確認結果。取得者の私的情報は含めない |
| resolved_at | 一覧を確定した日時 |

source_sha256は、配布元が完全なファイルのSHA-256を提供している場合だけ値を入れる。得られない場合はnullとし、後でローカル計算値を取得記録に残す。
size_bytesに概算・nullは不可。Hugging Faceのrevisionは短縮SHA、main、latestではなく完全なコミットSHA。
filesのpathはリポジトリ相対パス。Windowsで保存できること、親参照・絶対パス・大小文字衝突がないことを確認する。

## 版と保存先

標準保存先は `store/huggingface/<repo_type>/<owner>/<repo>/<commit>/`。リポジトリ内のパスを維持する。
同一版の複数取得定義が同じファイルを要求しても一つだけ保存し、予算集計も重複を除く。
別repo IDの同名ファイルや同じサイズだけで重複と判断しない。
他プロバイダーの実行資材は、その取得元に適した不変の版・URL・ファイル検証方法を別途定義する。未対応プロバイダーを推測で実行しない。

## 承認キュー

queues/approved.jsonのentriesにはasset_id、manifest_path、manifest_sha256、order、user_approved_at、execution_allowed=falseを記録する。
manifest_sha256は承認対象JSONそのもののバイト列のSHA-256。改行を含む変更で承認対象が変わる。
マニフェストや依存を変更したら再承認。選定済みでも未ロックならキューへ入れない。

## 完了判定

取得後にファイル件数、サイズ、SHA-256を確認する。配布元照合の有無も別に記録する。
ハッシュ一致は、実行可能性、無害性、モデルの能力を保証する判定ではない。

一次資料: [固定版・ファイル選択・local_dir](https://huggingface.co/docs/huggingface_hub/guides/download)。使用クライアントの版も取得記録に残す。
