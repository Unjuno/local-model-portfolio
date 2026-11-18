# R114｜無検閲27Bの原本性監査：逆向き親タグ・同一トークナイザー・容量交換案

2026-11-19 JST、`Unjuno/local-model-portfolio`。**最新正本v48（201登録・154有効）は変更しない。** Hugging Faceと既存の[配布元固定原本2系列](https://github.com/Unjuno/local-model-portfolio/blob/main/manifests/drafts/r113-v48-two-uncensored-original-fp16-parents.candidate.json)を照合し、GGUFとの原本交換が本当に妥当か検証した。全ファイルと判定を[機械可読JSON](../../catalog/decisions/2026-11-19-r114-uncensored-original-lineage-swap.json)に収録。

## 1.〈本論〉— 元モデルだと主張する前に確かめること

無検閲など拒否抑制後学習の重みは、公式ベースと異なる学習結果であれば保存価値がある。ただし**量子化前の原本／GGUFへの実変換経路／同じRVN版の学習結果**は、Hugging Faceのタグだけで確定できない。特に`0bserverx`はマスター原本に誤認すると別の学習済み成果を失う危険がある。

| 現在v48で選定したGGUF | 追加で見つかったSafetensorsルート | GGUF (GB) | root (GB) | 置換時の純増 (GB) | 調査判定 |
|---|---|---:|---:|---:|---|
| [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](undefined) | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | 17.738 | 55.586 | 37.848 | 原本を調査優先。権利・容量確認待ち |
| [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](undefined) | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored) | 17.177 | 53.811 | 36.634 | 原本性の証拠不足。RVN維持 |

- **`InterpreticAI/Qwen3.8-27B-Uncensored-v2`**：配布元が付けた親タグは `Qwen/Qwen3.8-27B`、GGUF側の親タグは `InterpreticAI/Qwen3.8-27B-Uncensored-v2`。現行の`InterpreticAI/Qwen3.8-27B-Uncensored-v2`は総数公称 27.781B、アーキテクチャ`qwen3_5`、原本ルート undefinedファイル／学習済み重み18 shards。<underline>配布者タグの由来表明と、変換前後の同一性を示すバイナリ証拠は別物</underline>。
- **`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored`**：配布元が付けた親タグは `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`、GGUF側の親タグは `Qwen/Qwen3.8-27B`。現行の`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored`は総数公称 26.896B、アーキテクチャ`qwen3_5_text`、原本ルート undefinedファイル／学習済み重み13 shards。<underline>配布者タグの由来表明と、変換前後の同一性を示すバイナリ証拠は別物</underline>。

**Interpretic**：[現行GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)のモデルカードは、[公式Safetensors版](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)を`base_model:quantized`として明示。従ってSafetensorsルートは長期の再量子化が可能な保全原本の**第一候補**。ただし固定版の全必要VLM構成、権利、完全SHA、量子化した同一チェックポイントとの変換同一性は未検証。GGUF資産を**今削除しない**。

**0bserverx**：[Safetensors版](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored)のモデルカードは`base_model:0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`を**finetune親として記載**する。ところが[GGUF版](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)は`base_model:quantized:Qwen/Qwen3.8-27B`。親の向きが単純な「Safetensors→GGUF」と整合しない。**単なるタグ誤記の可能性もあり、これだけで逆量子化を行ったとは証明しない。** Safetensorsは`qwen3_5_text`、公称26.896Bだが、既存選定はRVN-Q4_K_M-multilingual + vision `mmproj`。原本ルートがRVN編集後の完全同一学習結果だという根拠は現段階でない。**原本への機械的交換を停止し、現在のRVN Q4を保持する。**

### 1.1 SHA比較で本当に分かったこと

二つのSafetensorsルート合計58ファイルから、Publisher LFS SHA-256の参照が**33件**、異なるハッシュが**32個**。同じSHA-256は`tokenizer.json` **1ファイルのみ、12,809,320byte**で一致した。**重みshardのSHA一致は0**。これは同じトークナイザー原本を共有する可能性を支持するが、モデルの重み全体や独立学習結果が同一とは意味しない。

コンテンツアドレス保存を仮定した重複tokenizerの**理論的な1コピー分**12,809,320byteは記録できる。ただしディレクトリ構造・復元pathを2件とも維持する必要があり、実HDDでのdedup実施を確認したわけではない。

## 2.〈応用・転用例〉— 同じ能力に二重容量を費やさない

15件の[現行固定source-only研究キュー](https://github.com/Unjuno/local-model-portfolio/blob/main/queues/proposed-v48-r113-source-pinned-15.json)は **212,023,095,122byte**。無検閲のGGUF 2件を原本2件に置き換える場合と両方保存する場合を、**排他的なケース**として比較する。

| 代替案 | publisher source bytes | 判断 |
|---|---:|---|
| 現在の15件（両GGUF維持） | 212,023,095,122 | 基準（研究キューのみ） |
| InterpreticのみSafetensorsへ交換 | 249,870,824,696 | **推奨する条件付き再審査** |
| 0bserverxのみSafetensorsへ交換 | 248,657,330,337 | **系譜不整合により停止** |
| 両方Safetensorsへ交換 | 286,505,059,911 | 現時点では根拠不足 |
| 両GGUFと両Safetensorsを二重保存 | 321,420,079,414 | **原則非推奨：独立学習差が未確認** |

元の15件に対して両系列のsource交換は **74,481,964,789byte純増**。これは約74.482GBであり、かつ完全offline依存・キャッシュ・取得ステージを除く。先行R111で品質増分未証明のため後回しにしていたPantheon/DavidAUのsource約108,711,479,306byteは、**取得順を後ろにしただけ**で正式に選定解除していない。したがって「すでに108.711GBの空き容量が増えた」と主張することは誤り。既存4TBの実空きと、物理的な取捨選択に関するユーザー承認が必要。

**次に採否を確定する条件：** Interpreticは固定原本のLICENSE正文・親の有効条件・同一学習結果への変換履歴・必要なprocessorやmmprojと推論runtimeを閉包し、個別の実HDD条件を満たす場合のみ原本マスターへ交換。0bserverxは**RVN版とrootの同一性証明**、Safetensorsへの変換経路、作者の由来記録、テキスト専用とvision機能の差を確認するまでGGUFのまま。

## 3. 現在の規制事実・推論・不確実性

- **観測事実**：Hugging Faceの公開状態・作者による`base_model`注記・固定revisionとLFS SHA/byte。著作権、親モデル、利用目的のライセンスは個別に検証が必要。
- **推論**：同じ学習結果と証明できれば、原本Safetensorsは別量子化を将来再作成できるので保全マスターとして有利。ただし今回の0bserverxについて、この推論の前提がまだ成立しない。
- **将来仮説**：無検閲→高性能→公開モデル全般の規制という段階論。モデル別削除日や規制確率の根拠はない。公開済み重みの無許可取得を正当化しない。

今回Exa検索は**402クレジット上限エラー**。Hugging Face接続先の一次モデルカードとGitHubに固定されたPublisherメタデータを用い、Exaによる新規検索成果があったとは主張しない。

## 4. 変数表・算術と次元チェック

| 記号 | 意味（日本語） | SI単位 | 定義・前提 | 定義域／範囲 | 型 |
|---|---|---|---|---|---|
| `B_G` | 対象GGUF2原本のpublisher容量 | byte | 34,915,019,503、既存選定の内数 | 0以上 | 非負整数スカラー |
| `B_F` | Safetensors2原本のpublisher容量 | byte | 109,396,984,292、まだ選定外 | 0以上 | 非負整数スカラー |
| `B_15` | 現行15件の論理publisher候補容量 | byte | 212,023,095,122、全offline量ではない | 0以上 | 非負整数スカラー |
| `B_Δ` | 両モデルのsource交換による差分 | byte | `B_F-B_G`、仮想差分 | 整数 | 整数スカラー |
| `D_tok` | 同一tokenizer SHA分の重複容量 | byte | 12,809,320、物理未確認 | 0以上 | 非負整数スカラー |
| `F_owner` | 所有者4TB媒体の実空き容量 | byte | 現時点未観測（null） | 未知／0以上 | 整数またはnull |
| `B_stage` | 取得中のピーク作業用容量 | byte | CLI/cache/FS依存、未観測 | 未知／0以上 | 整数またはnull |

計算：`B_Δ = 109,396,984,292 - 34,915,019,503 = 74,481,964,789 byte`。**次元チェックPASS**：同じbyte単位のみを差し引いた。原本の学習済み全総数と量子化バイトを直接比較しない。MoE全expert、MTP/embeddings、150B境界／現行厳格な量子化例外は`policies/limits.json`の独立条件。

## 5. H/T/D/C/U、ERROR CHECK

- **H**：正しい同一学習成果のSafetensors原本をマスター保存する方が、GGUFだけの保存より将来の量子化変換・研究再利用を保持できる。
- **T**：2組の由来関係と固定root58ファイル、既存GGUF9ファイル、SHA重複を照合（n_min＝2）。原本・量子化版の実比較には本人の適法な取得、固定HW/driver/backend/context/batch、32件以上の対応入力、モデル変換履歴が必要。権利・由来不整合が1件でもあれば交換処理を止める。
- **D**：sourceメタデータ・算術整合はPASS。原本マスターへの実交換の判定は現時点UNCERTAIN。無許可取得・誤った学習版・本人HDD不足・ライセンス不適合があればFAIL。
- **C**：0bserverxのSafetensorsがGGUFから復元された別重み、またはRVNではない旧学習成果の可能性。Interpreticにも処理系依存や異なるcheckpoint更新の可能性。
- **U**：配布者タグの誤記、学習結果の識別不可、実ディスク空き、外部コード/ライセンス、品質比較バイアス。分布・反復測定がないため合成標準不確かさ `u_c` と包含係数 `k` は数値化しない。

### ERROR CHECK

- 2原本root：32 + 26 = 58ファイル、18+13 learned weight shards、source合計109,396,984,292byte。
- Publisher SHA-256：33参照・32一意、重複は同一tokenizerのみ。学習済み重みshardの重複SHAは確認されていない。
- 現行v48：201資産／154有効を変更しない。`CURRENT.json`、`queues/approved.json`、HDD、モデル本体を変更せず、専用ブランチのR114研究JSONと文書だけを追加。
- **本体ダウンロード・実行・本人許諾・オフライン復元は0件**。主題は原本交換判断の正確性。

## 6.〈次に考える問い〉

**0bserverxのGGUFとSafetensors原本が同じRVN学習成果かどうかを証明できるまで、現在の量子化原本を維持しつつ、Interpreticの元Safetensorsだけを原本マスターとして準備する方が、容量あたりの情報損失を最小化できるか。**

