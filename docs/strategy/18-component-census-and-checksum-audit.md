# R22：2構成の全テンソル集計・LoRA適合・チェックサム不一致の処理

確認日：2026-11-05。基準main：`6a3dfb7e8a469610a741abba15b68a01db4e3ef4`。

## 完了したこと

新モデル探索は行わず、R21の固定された4repo・47ファイルだけを検証した。**重み10ファイルのヘッダー、補助37ファイルの実内容、画像LoRA全224組の形状**を検証した。現在の準備順位台帳から「構成別総数の未確定」を解消し、チェックサムの不一致を新しい注意事項として追加した。CURRENT・正式カタログ・承認キュー・実機ストレージには変更なし。

[検証証拠JSON](../../catalog/preparation/2026-11-05-component-census.json)、[準備順位](../../catalog/preparation/2026-11-05-priority-packages.json)、[読み取り専用検査](../../scripts/audit_component_census.py)を参照。R21のファイル計画は過去の観測記録として変更しない。今回の値は別の版を検証したものではなく、その固定版に対する追加検証。

## 1. 実際に数えた構成

| パッケージ | 構成 | 保存テンソルの要素数 | 格納型 |
|---|---|---:|---|
| ChatR画像 | 基盤DiT全2シャード | 7,115,124,736 | BF16 |
| 同上 | マルチモーダルencoder全4シャード | 8,767,123,696 | BF16 |
| 同上 | VAE | 337,740,404 | F32 |
| 同上 | 未マージLoRA | 335,544,320 | BF16 |
| **ChatR合計** | **基盤・encoder・VAE・LoRA一式** | **16,555,533,156** | 混合 |
| Interpretic | 言語GGUF・MTPを含む保存構成 | 27,320,697,856 | Q4_K、Q6_K、F32 |
| 同上 | 視覚projector/encoder GGUF | 460,730,096 | F16、F32 |
| **Interpretic合計** | **言語＋視覚** | **27,781,427,952** | 混合 |

Interpretic合計は公開BF16原本のHub総数に一致する。ただし**総要素数一致は、量子化前後の数値・性能・全tensor名対応の同一性の証明ではない**。`Q4_K_M`は全要素が4bitという意味ではなく、今回の言語ファイルにもQ6_KとF32が含まれる。

**数値の意味**：上表は固定ファイルのtensor形状を全数集計した正確な「保存テンソル要素数」。学習されない浮動小数点buffer、同一パラメータの重複保存、未マージLoRAを含み得るため、固有の学習可能パラメータ数と無条件に等置しない。この保存構成の学習済み要素数に対する保守的な上限として150B未満を確認できる。LoRAをマージした別モデルのparameter数にLoRA分を二重加算しない。元の7.115Bという主DiTだけの値を画像パイプラインの総数としない。

### 手法と単位

[Hugging Face公式メタデータ取得法](https://huggingface.co/docs/safetensors/metadata_parsing)に沿い、公開固定版へHTTP Rangeを指定。206とContent-Rangeの一致、取得長上限を確認し、全モデルの値配列を取得しない。safetensorsは8byte長情報とJSONヘッダーだけを読み、shape積・dtype幅・data_offsetsの差・最終ファイル長・シャード間key重複を検査した。GGUF v3は[形式仕様](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)に沿ってmetadataとtensor descriptorを解析し、未解析項目の最小必要長を超えて先読みしない。いずれも**tensorデータ領域の読取りは0byte**。ヘッダーハッシュは全ファイルSHA-256の代用ではない。

全保存要素数は各tensorのshape積の総和で算定する。バイト整合性検査では、safetensorsの非圧縮値領域の要素数にdtypeのbyte幅を掛け、ヘッダー長を加えたものが配布ファイル長と一致する。量子化GGUFはblock単位の格納幅とalignmentを別扱いにする。

| 記号／フィールド | 意味 | 単位(SI) | 定義 | 範囲／前提 | 型 |
|---|---|---|---|---|---|
| `scalar_total` | 全保存要素数 | 1（個数） | 全tensorの各軸サイズの積を合計 | 非負整数、固定版・全シャード | 整数スカラー |
| `scalars_by_dtype` | 型別の要素数 | 1（個数） | BF16/F32またはGGML型別の集計 | 論理要素数、packed配列数ではない | 整数値の辞書 |
| `file_bytes` | 配布ファイル長 | byte（情報量） | 公開固定版のContent-Range総長 | 正整数 | 整数スカラー |
| `metadata_bytes` | 読み取ったヘッダー領域 | byte（情報量） | 値配列の直前まで。GGUF paddingは別 | ファイル長未満 | 整数スカラー |
| `tensor_data_start` | 値領域先頭offset | byte（情報量） | ヘッダー長とalignmentから算定 | 正整数 | 整数スカラー |
| `actual_user_peak_ram_bytes` | ユーザー環境の推論メモリ | byte（情報量） | 実測値のみ | 未測定なのでnull | 整数／欠損 |

単位チェック：要素数とbyteを同一視せず、BF16/F16は2byte、F32は4byteを用いる。量子化ではblock幅を適用。51.541GBは保存モデル・資料の容量であり、推論メモリでも一時領域込み容量でもない。

## 2. LoRA適合性

BF16アダプターの448テンソルをA/Bの224組へ整理。`transformer.`プレフィックスを明示的に対応付け、全組でrank128と基盤行列の入力・出力次元が一致、欠落0組だった。対応先名集合のSHA-256は`45d8ec819f8c804473caf3b7fd00f646753a0aca91cd08b213f1098a8e30d580`。

これは**静的な名前・shape適合**。Diffusersが全キーを実際に適用すること、学習データの品質、生成画像の優越、NSFW概念の被覆を保証しない。推論は未実行。

## 3. 発見したチェックサム問題

固定adapter版 `aa213272180d6ad0d03f5fb3d597f0f0322647c5` の[SHA256SUMS](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/blob/aa213272180d6ad0d03f5fb3d597f0f0322647c5/SHA256SUMS)と、実際のテキスト2件の値が一致しなかった。

| ファイル | 作者SHA256SUMSに記された値 | 今回読み取った実内容のSHA-256 |
|---|---|---|
| README.md | `262c5b85bb418cf55014840e3ff8c8ec6ec8d7860812b6975de282652bea78d2` | `a9cf63e5fd38129321ed17b553c875313581cab5af8235470750e08aacbde51b` |
| inference.py | `5b9a81bcdc9c8dc66441ac1188f35ef97a37f275a2a64453dffb31c56ac0a673` | `3a7ddd31b6a45af8f6f594ef39643164b4f4b26308ea3a9193f18afbe27fd6a4` |

**両ファイルの内容は固定コミットのGit blob SHA-1には一致する。** LICENSE・Notice・requirementsの作者SHA-256も一致。重みの作者SHA-256はLFSポインターと一致するが、全重みのローカル計算は未実施。したがって、ここから重み破損や悪意を断定しない。チェックサム一覧が更新されていない可能性はあるが、原因の確定ではない。原本SHA256SUMSを勝手に修正せず、双方の値を残し、無条件に`sha256sum -c`全成功と記録しない。

37補助ファイル（16,061,059byte）の内容を隔離された取得環境で取得し、36件は通常Git blob（`blob <長さ>\0`付き）のSHA-1、LFS管理のtokenizer1件は内容SHA-256と照合し一致した。LFS pointerのGit blob IDを解決後のtokenizer内容に当てる誤りは検出し、型別に使い分けた。`inference.py`はテキストとしてのみ扱い、実行していない。**補助ファイルを読んだ事実を「一切ダウンロードなし」とは表現しない。モデル本体の取得とユーザーのHDD変更は0件。**

## 4. 次の実行に必要なことと停止境界

R21計画の容量は変更なし：ChatR33,802,789,787byte、Interpretic17,738,357,352byte、合計51,541,147,139byte。既存基盤の再利用は実機ハッシュ確認まで仮定しない。

残るのは、(1)対応runtime・バイナリ依存・実機RAM/速度、(2)保存先の実空き・一時領域、(3)全重み取得後SHA-256、(4)利用目的に応じた品質検証、(5)正式カタログへの昇格と最終承認。既存の研究選定を根拠に自動取得・シード・実行しない。規制時期やモデル削除の確率は追加していない。

H：固定された構成が150B未満で、全LoRA対象に静的適合する。T：10ヘッダー・全224組・37補助ファイルを全数検査、標本抽出なし。D：構成・byte整合はPASS、同梱チェックサム2件は不一致を明記、実機品質はUNCERTAIN。C：依存漏れ、shape偽装、版変更、コードが想定キーを使わない場合に判定が破れる。U：標本誤差の問題ではなく、trainable/buffer定義、未測定runtime、配布元そのものの信頼性が主な限界。合成u_c・拡張係数kの数値は根拠がないため作らない。

関連分野は機械学習（LoRA・量子化）、ソフトウェア供給網（固定版・ハッシュ・依存）、デジタル保存（重複排除・再現性）。これらを別々に合格判定し、メタデータが正しいだけでモデル品質が証明されたことにしない。

## ERROR CHECK

`python scripts/audit_component_census.py` と `python -m unittest discover -s tests -p test_preparation_round22.py -v` で読み取り専用検査。全重みhashや実機性能を実測済みにした場合、要素数の取り違え、欠落ファイル、224組未適合、チェックサム不一致を消した場合はFAILとなる。CURRENT・approved・Nanbeige・既存6除外は無変更。
