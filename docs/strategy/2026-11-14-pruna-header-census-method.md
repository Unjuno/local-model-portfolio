# Pruna全コンポーネントのヘッダー限定計数（2026-11-14）

現行正本は main の catalog/CURRENT.json。旧v9の132資産提案と現行v32の182資産・有効135件を混同しない。本変更は選定・取得承認・権利同意を一切変更しない。

## 対象と方法

R61で固定した PrunaAI/P-H3-Image のrevision `7f98acef503cf2bcfba821a78cb1cf1a9928b2df`、Transformer7・Text Encoder2・Prompt Upsampler4・Connector1・VAE1の15 Safetensorsだけを対象とする。実行器はPython標準ライブラリのみで、モデルコード・Torch・pickleをロードしない。

[Hugging Face公式のメタデータ解析](https://huggingface.co/docs/safetensors/en/metadata_parsing)に従い、各ファイル先頭8byteのヘッダー長、続くJSONヘッダーのみをHTTP Rangeで取得する。要求と一致する206/Content-Range/Content-Lengthが得られない場合は本文を読まず停止する。1ヘッダー最大4MiB。匿名・HTTPS・公式Hub/CDN以外へのリダイレクトを拒否し、401/403やGated同意を回避しない。

shape各次元の積を型別に集計する前に、dtype幅とdata_offsets、データ領域全体の連続被覆、コンポーネント内の重複テンソル名を検査する。未対応のpacked量子化dtypeは失敗扱い。全15ファイルが揃わなければ総数を認定しない。

## 数値の意味と限界

結果は「保存テンソル要素数」であり、bufferや共有重みの重複を含み得る。独立した学習済みパラメータ数の完全一致、学習済み外部依存の閉包、全重みSHA256、本人の権利、完全オフライン復元を証明するものではない。検証が成功してもカタログのPASS昇格や取得承認を自動的に行わない。

| 変数 | 意味 | SI単位 | 定義・前提・範囲 | 型 |
|---|---|---|---|---|
| N | 検査対象ファイル数 | 1 | 固定15、全5部品が必要 | 整数スカラー |
| H | ヘッダーJSON長 | byte | 2以上4MiB以下 | 整数スカラー |
| P_s | 保存テンソル要素総数 | 1 | shapeの積を全対象について合算、buffer含む | 整数スカラー |
| B | テンソルの格納領域 | byte | 要素数とdtype幅でoffset整合を検査 | 整数スカラー |

次元チェック：要素数は無次元、dtype幅はbyte/要素。積はbyteとなり格納offset差と比較できる。

H：固定15重みのヘッダーだけで保存要素総数を再現計数できる。T：匿名Range照会とオフライン異常入力テスト。D：全ファイル・offset・dtype整合でHEADER_CENSUS_COMPLETE、一つでも失敗すればBLOCKED。C：metadata変更、HTTP Range未対応、packed量子化、未列挙依存。U：上流情報の真正性、bufferと学習済みの区別、権利・外部依存。統計実験ではなくu_c/kは未算定。

関連分野：モデル構造監査、HTTP/ファイル形式セキュリティ、デジタル保全。実行結果はGitHub Actionsログとartifactに保存し、結果確認後に研究台帳へ記録する。
