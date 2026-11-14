# Pruna全コンポーネントのヘッダー限定計数（2026-11-14）

現行正本は main の catalog/CURRENT.json。旧v9の132資産提案と現行v32の182資産・有効135件を混同しない。本変更は採否・取得承認・権利同意を変更しない。

## 実行結果：全15ファイルを計数

GitHub Actions [run 43602722632](https://github.com/Unjuno/local-model-portfolio/actions/runs/43602722632)、実装commit `181d5581f6abf9157c6c874aa9e0f492f95ecf7a` で完走。読み取ったのはヘッダーメタデータ339,304byte、要求したtensor payloadは0byte。模型をロード・実行していない。

[凍結した生の計数JSON](../../catalog/research/2026-11-14-pruna-header-census.json) はActions artifactから取得した内容をそのまま保存。JSONのSHA-256は `c84574df257007eacd23174df231baa1861186501131a955c71029230e04a809`。元artifact ZIPのSHA-256は `bc3d5422741d5f489974779540d867e6f8e242569da6445d9a08b92aec894871`。ZIP digestはアップロード時のログとも照合済み。

| 部品 | ファイル数 | テンソル数 | 保存要素数 |
|---|---:|---:|---:|
| Transformer | 7 | 638 | 33,122,992,896 |
| Text Encoder | 2 | 713 | 4,437,815,808 |
| Prompt Upsampler | 4 | 760 | 9,409,813,744 |
| Text Connector | 1 | 6 | 65,576,960 |
| VAE | 1 | 703 | 2,599,148,088 |
| 合計 | **15** | **2,820** | **49,635,347,496** |

**確認できた事実**：固定15ファイル内の保存テンソル要素は約49.635B。33.1BはTransformerだけで、他4部品を含む数字ではなかった。BF16の49,372,210,504要素とF32の263,136,992要素を、ヘッダーのshape・dtype・offsetから独立集計した。

**容量との照合**：全ファイル99,797,308,280byteからヘッダーと長さprefixの339,304byteを除いたデータ部は99,796,968,976byte。BF16要素ごと2byte、F32要素ごと4byteの集計と一致する。

**未証明**：bufferや共有重みの重複を除いた固有の学習済みパラメータ数、公開ファイル以外の必須学習済み依存の閉包、モデル全体のSHA-256、実機復元・性能、利用者の権利。本結果はこの固定された保存範囲が150B未満である証拠であり、すべての利用形態の全モデル規模・取得許可を認定するものではない。`UNVERIFIED_BLOCK_FINAL_LOCK`や承認キューを自動変更しない。

## 対象と安全な方法

R61で固定した PrunaAI/P-H3-Image のrevision `7f98acef503cf2bcfba821a78cb1cf1a9928b2df`、Transformer7・Text Encoder2・Prompt Upsampler4・Connector1・VAE1の15 Safetensorsだけを対象とする。Python標準ライブラリのみ。モデルコード・Torch・pickleをロードしない。

[Hugging Face公式のメタデータ解析](https://huggingface.co/docs/safetensors/en/metadata_parsing)に従い、先頭8byteのヘッダー長と続くJSONヘッダーだけをHTTP Rangeで取得。要求どおりの206/Content-Range/Content-Lengthでなければ本文を読まず停止する。1ヘッダー最大4MiB。匿名・HTTPS・公式Hub/CDNのみ。401/403やGated同意を回避しない。

shape各次元の積を型別集計する前に、dtype幅とdata_offsets、データ領域の連続被覆、コンポーネント内の重複テンソル名を検査。未対応のpacked量子化dtypeは失敗扱い。全15ファイルが揃わなければ総数を認定しない。実測環境はGitHub Actions Ubuntu、CPython 3.12.16、GPU推論なし。速度・品質のベンチマークではない。

| 変数 | 意味 | SI単位 | 定義・前提・範囲 | 型 |
|---|---|---|---|---|
| N | 検査対象ファイル数 | 1 | 固定15、全5部品が必要 | 整数スカラー |
| H | ヘッダーJSON長 | byte | 2以上4MiB以下 | 整数スカラー |
| P_s | 保存テンソル要素総数 | 1 | shapeの積の合計、bufferを含む49,635,347,496 | 整数スカラー |
| B | テンソルの格納領域 | byte | dtype幅とoffset整合を検査、計99,796,968,976 | 整数スカラー |

次元チェック：要素数は無次元、dtype幅はbyte/要素。積はbyteとなり格納offset差と比較可能。

H：固定15重みのヘッダーだけで保存要素総数を再現計数できる。T：匿名Range照会、全ヘッダーの整合検査、オフライン異常入力12テストと凍結証拠4テスト。D：全15ファイルを処理してHEADER_CENSUS_COMPLETE、読めないファイルがあればBLOCKED。C：metadata変更、HTTP Range未対応、packed量子化、未列挙依存。U：上流情報の真正性、bufferと学習済みの区別、権利・外部依存。統計実験ではなくu_c/kは未算定。

**ERROR CHECK**：15ファイル・5部品・2,820テンソルの合算、型別容量、artifact digestが一致。原本重み・推論・承認操作0。関連分野はモデル構造監査、HTTP/ファイル形式セキュリティ、デジタル保全。
