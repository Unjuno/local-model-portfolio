# R133／v57：公開Spark4BとHeretic9BのBF16編集原本を条件付き採用（2026-11-20）

## 1.〈本論〉— 採用と取得を分離

従来v56の**211資産・164有効**を一件も変更せず、独立した小型無検閲研究対象2件を**CONDITIONAL**で追加する。v57は**213登録・166有効（SELECT53／CONDITIONAL113）**。根拠は[出版社原本固定マニフェスト](../../manifests/drafts/r133-2026-11-20-spark4b-and-heretic9b-bf16-mtp-originals.candidate.json)、[v57差分](../../catalog/revisions/v57-2026-11-20.json)、[機械可読判断](../../catalog/decisions/2026-11-20-r133-v57-spark-heretic-original-selection.json)。正規の`queues/approved.json`は依然空。**CONDITIONALを重量ダウンロード許可と解釈しない。**

| 原本 | 40桁出版社revision | Publisher全files／source byte | 全学習済み数 |
|---|---|---:|---:|
| [FrostWolf Spark-X2.6-4B Abliterated](https://huggingface.co/FrostWolfAI/Spark-X2.6-4B-abliterated) | `505257b7969eb03a5a62d81f9afec6f88abd26e4` | 22／8,239,173,287 | 4,112,079,360 |
| [xtools DeepSeek-V4-Pro-Qwen3.5-9B Uncensored Heretic](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic) | `fbccdc6adf70a1981e8f40e91a8370e428e4f998` | 19／19,331,656,364 | **9,653,104,368** |

合計**41 files／27,570,829,651 byte／出版社LFS SHA256 8件**。これはPublisher全ソースの論理容量であり、所有者媒体への実増分転送量や完全オフライン復元の証明ではない。

### Spark 4B：独立した後学習原本の証拠の限界

配布者の`reproduce/reproduce.json`はHeretic 2（git `efb1be6e3f979581b8878be978e001e34260159b`）、seed 2026102902、ARA方向編集の対象layers9–19、最終BF16重量2シャードのSHA256を含む。元親`XHToken/Spark-X2.6-4B`は5シャードに分割されるため、**SHAファイル差だけではテンソル値の独立変化を証明できない**。編集レシピの存在を保存選定の根拠に採用するが、差分テンソル比較と同一Hardwareの性能検証を今後の条件とする。出版社の拒否2/100対100/100、KL 0.0177は選別100例の作者報告であって独立安全性・品質の実証ではない。custom `modeling_spark.py`は未実行。

### Heretic 9B：MTP付き現行原本の数値訂正

現在のPublisher sourceは**4本のBF16主重量＋独立`model-mtp.safetensors`（486,583,016 byte）**を含む。モデルindexの775件のうち**15テンソルがMTP**である。`model.safetensors.index.json`の9,409,813,744は主モデルの数であり、別ファイルのMTP 243,290,624を加えた**9,653,104,368**が完全総数。以前の「MTPが欠けている9.4098B」という説明を現行リビジョンに適用しない。元親`Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B`とTrainerの蒸留データ、Apache-2.0カード表示とLICENSE正文、vision/MTPランタイムは実機検証前である。現行source19件に単独LICENSEがないため利用権利について追加確認が必要。

## 2.〈応用・転用例〉— ポートフォリオと供給制約

Spark4Bは既存1.7B LFMとは別アーキテクチャ。Heretic9Bは既存27B Qwen3.8派生とは別の9B蒸留＋編集成果。一般的なGGUF・MLX変換を新しい学習モデルとして二重登録しない。開発・推論は未信頼のcustom codeを無審査実行せず、親重量やtokenizer/chat template、MTP、visionとABIを同一環境で監査する。

過去の[取得実行ledger](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**66モデル／801ファイル／851,289,867,641byte**のVERIFIEDを**報告**しているが、この調査で所有者Windows Dドライブを独立にハッシュした事実はない。4TBという保存予算、現在空き最低200GB、staging/一時キャッシュ容量、全選択ファイルSHAとLICENSEの本人行為別確認、明示的なfile-scope承認が揃うまで実取得不可。削除・Gated迂回・自動model code実行は行わない。

米BISの[2026-11-19 Federal Register公示](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は旧ECCN4E091のモデルweight分類撤回を記載しており、全open-weightの差し迫った所持禁止が確認されたわけではない。将来のアクセス制限は反証可能な仮説であり、個別の規制成立や確率を創作しない。

## 3. H/T/D/C/U・変数表・ERROR CHECK

**H**：独立の4Bと9B編集済み原本を含む高精度ソースを残すと同一GGUF量子化重複より能力多様性を保てる。**T**：出版社41件のpath、byte、SHA、MTP indexを全数確認し、後でOwner実物のSHAとWindows backend ABIを確認。性能評価には同一HW/clock/OS/driver/backend/zero-point/context/batchで各30回以上の繰り返しを要求。**D**：PASS_METADATA＝213件一意／166有効／41ソース／8 SHA256参照／MTP15／承認0。FAIL＝MTP漏れ、未承認取得、ファイルSHA差を実Tensor差の証明と主張。UNCERTAIN＝Tensor差、権利、品質、実機復元。**C**：再シャードに由来する同一Tensor、ABI不整合、蒸留ソースの利用制約。**U**：出版社記録の偏り、owner実媒体/品質測定、ライセンス。反復誤差分布を得ていないため合成標準不確かさu_c、係数kは定量化不能。

|記号|意味（日本語）|SI単位|定義|範囲・前提|型|
|---|---|---|---|---|---|
|N_total|9B全学習済み数|1（無次元）|9,653,104,368|MTPを含む|整数|
|N_main|9B主index数|1（無次元）|9,409,813,744|MTP除外|整数|
|N_mtp|別学習済みMTP数|1（無次元）|243,290,624|15テンソル|整数|
|B_source|両モデルのPublisherソース長|byte（SI基本単位外）|27,570,829,651|取得増分とは別|整数|
|R_peak|ランタイム全ピークメモリ|byte（SI基本単位外）|OS/KV/CPU/GPU等含む|未測定null、512GB条件を審査|整数/null|

**次元検査**：9,409,813,744＋243,290,624＝9,653,104,368（無次元）、8,239,173,287＋19,331,656,364＝27,570,829,651byte。重みbyteとパラメータ個数を直接比較しない。150B総数以上には既存量子化実測例外の30回以上/同HW・品質・権利・許可を要求。

**ERROR CHECK**：v57=213登録166有効、SELECT53＋CONDITIONAL113、原本41ファイル・出版社SHA8、既存211件は不変、approved0、重みダウンロード0。関連分野：学習来歴、MLアラインメント、推論/ハードウェア、法務と技術アーカイブ。

## 4.〈次に考える問い〉

SHA付き原本の論理ファイルを固定した後、本人の実HDDとMTP/visionバックエンドのどちらを先に検証すれば完全復元までの検証コストを最小にできるか？
