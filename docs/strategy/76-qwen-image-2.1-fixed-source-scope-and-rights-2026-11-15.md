# R76｜Qwen-Image-2.1の除外ファイル1件と349 byteの観測差を公式APIで再確定

監査日：2026-11-15。正本v32／`main`。**研究専用、モデル取得・実行・利用規約への同意・許可キュー変更なし。**

[固定revisionの全ファイル・byte・blob証拠を機械可読化](../../catalog/research/2026-11-15-r76-qwen-image-2.1-fixed-source-overfetch-resolution.json)。入力は[R74旧66配布元allowlist](../../manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)、一次参照は[Hugging Face固定commitのAPI](https://huggingface.co/api/models/Qwen/Qwen-Image-2.1/revision/790c92633540aa0cb11d9abf19eb46d861714758?blobs=true)。

## 1.〈本論〉— 保存スコープの確定

| 対象（同じSHA） | 件数／byte | 判定 |
|---|---:|---|
| 固定revision `790c92633540aa0cb11d9abf19eb46d861714758` の公式ファイル一覧 | 28件／33,134,949,212 byte | 当日公開元APIの表示値 |
| R74で固定した推論用・補助ファイル範囲 | **27件／33,131,616,412 byte** | **27/27 ファイルのpath、size、Git blob SHAが公式APIと一致** |
| R74採用済みファイルのLFS payload SHA256 | 8件／8件一致 | 公開元メタデータ照合、ローカル実物のSHA計算ではない |
| 公式API上の選択外ファイル | **1件／3,332,800 byte** | `assets/qr.png` |
| R74旧全repo観測総量 | 33,134,949,561 byte | 当日公式APIの全ファイル和より349 byte大きい |
| R74旧「選択外差分」 | 3,333,149 byte | うち3,332,800 byteがQR画像、残り349 byteは集計差 |
| R74旧`source_excluded_file_count` | 0件 | 実際の固定版には選択外QR画像が1件存在 |

選択外の`assets/qr.png`の公開元[LFS SHA256](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/790c92633540aa0cb11d9abf19eb46d861714758/assets/qr.png)は`9b1c6d8996a3560f12060affd070575dd8a3938462b15233c0dc15b2604a9243`、容量3,332,800 byte。公式[README](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/790c92633540aa0cb11d9abf19eb46d861714758/README.md)のWeChatリンク先として説明される。公式[model_index.json](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/790c92633540aa0cb11d9abf19eb46d861714758/model_index.json)の実行モジュールはprocessor、scheduler、text_encoder、transformer、VAEであり、QR画像はその列挙に含まれない。

**結論：** R74の選択27ファイルと重みのSHA記録は変更不要。旧観測の3,333,149 byte差のうち3,332,800 byteを単一の画像へ対応付けた。残349 byteは当日APIと旧repo容量の集計方式・観測差であり、**追加ファイルと断定しない**。履歴R74を根拠なく上書きせず、このR76を最新版の訂正根拠とする。

### ライセンス本文から確定した条件

対象revisionの[公式LICENSE全文](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/790c92633540aa0cb11d9abf19eb46d861714758/LICENSE)を確認。名称は**Qwen Research License Agreement（2026-09-20）**、メタデータは`license:other / license_name:qwen-research`。第1条(i)・第2条(a)(b)は使用・複製等を**非商用の研究または評価用途**に制限し、商用は別途ライセンスが必要。第3条は再配布時のライセンス本文とNOTICE/変更通知条件、第4条は適用輸出法令等を規定する。

これは**条文の確認**であり、特定所有者の用途適合、事前の同意、法域別適法性を自動承認したわけではない。LFSや派生LoRAの正規取得・再配布は別ゲート。AI生成物の権利一般をこの記録から一律推論しない。

## 2.〈応用・転用例〉— 4TB保存枠への転用

- R74の66配布元におけるhistorical全repo差分は`2,985,522,750,447 byte`。今回のQwen1件の集計差349 byteだけを補正する**参考値**は`2,985,522,750,098 byte`。これは履歴台帳全体を書き換える数字でも実機節約量でもない。
- 新たなモデルを増やさず、取得候補として`Qwen/Qwen-Image-2.1`の既存27ファイルだけを維持。QR画像は推論に不可欠という証拠がなく、容量保存の対象から除外する。
- `allow_patterns`型のglobは想定外マッチの恐れがある。正式実行用のコードを承認するときは、パターン名と公開元ファイル一覧の**完全一致のセット比較**、固定SHA、本人権利の三つを分離した非補償ゲートとする。

### 変数表と次元チェック

| 記号 | 日本語の意味 | SI準拠単位 | 定義 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `B_{{api}}` | 固定版APIファイル容量の和 | byte | 33,134,949,212 | 28ファイル、非負 | 整数スカラー |
| `B_{{sel}}` | 選択27ファイルの和 | byte | 33,131,616,412 | 27ファイル、非負 | 整数スカラー |
| `B_{{qr}}` | QR画像ファイル容量 | byte | 3,332,800 | 固定revの唯一の選択外 | 整数スカラー |
| `B_{{hist}}` | R74履歴repo容量 | byte | 33,134,949,561 | 歴史的観測 | 整数スカラー |
| `B_{{delta}}` | 履歴とAPIの容量差 | byte | 349 | 算術差、原因未確定 | 整数スカラー |

次元チェック：`B_api - B_sel`（byte）は`B_qr=3,332,800 byte`、`B_hist - B_api=349 byte`。メタデータ上の正確な算術であり実ディスクの空き容量ではない。

## 3. H / T / D / C / U と ERROR CHECK

**H**：R74の3,333,149 byte差は、実際の除外ファイル1個と歴史的集計差の合成である。

**T**：n_min=固定revisionの公式28ファイル、R74採用27ファイルを完全join。size・Git blob SHA・LFS SHA、選択外一覧、README用途、model_index構成を静的に照合。停止条件は28/28一致または不一致。

**D**：ファイル同一性検証は**PASS**（27/27一致、除外1件3,332,800 byte）。349 byteの旧観測差の原因特定、本人用途適法性、全runtime依存、ローカルSHA、オフライン復元は**UNCERTAIN**。不整合のあるファイルを黙って追加する場合は**FAIL/STOP**。

**C**：異なるcommit、Git LFS pointerサイズと実LFSサイズの混同、APIの集計方式、README画像の誤った実行依存認定。

**U**：残349 byteの観測条件が未確定。統計的な誤差分布がないため合成標準不確かさ`u_c`と包含係数`k`は算出しない。

**ERROR CHECK**：公式28ファイル、選択27件のsize/Git blob 27一致、LFS SHA8一致、欠落0、唯一の未選択はQR画像3,332,800byte、旧観測差349byte。**重み取得・実行・承認0**。

関連領域：デジタル保全（原本再同定）、ソフトウェア供給網（SHA・LFS）、機械学習の構成（pipelineモジュール）、知財・契約法（研究ライセンス）。

## 4.〈次に考える問い〉

**固定公開元の全ファイル列挙によって同様の過剰保存差分を解消できる資産を、残り65配布元から何件特定できるか。**
