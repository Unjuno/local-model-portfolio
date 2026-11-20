# R136｜v57 66件取得報告と新しい原本3件の比較に基づく取得候補確定

基準：2026-11-20。現行正本 [CURRENT](../../catalog/CURRENT.json) は調査時 **v57・213登録／166有効**。新しい3配布元の[全source固定](../../manifests/drafts/r134-2026-11-20-rikiya08b-mellum-mtp-ripple65b.candidate.json)、[13 source統合キュー](../../queues/proposed-v57-r135-ledger66-next-deduplicated-sources.json)、[機械可読判定](../../catalog/decisions/2026-11-20-r136-v57-next-original-model-source-and-triage.json)と[無通信テスト](../../tests/test_r135_v57_ledger66_phases_and_mtp.py)を基準とする。

**対象と非対象**：独立した学習済み状態・評価データ・外部codecを合法的かつ重複なく長期保全する。一般のHFモデルカード表示／性能の作者自己評価／将来の公開停止予測は、本人使用権、実験性能、取得許可を代替しない。本作業では**モデル重量・PyTorch pickle・custom codeを取得も実行もしていない**。

## 1.〈本論〉重複計上の修正：61ではなく66件が報告済み

[取得実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は **66モデル・801ファイル・851,289,867,641byte** を `VERIFIED` と報告、さらにGated/Private HOLD1件。台帳の日付付き結果であり、**所有者の現在の物理Dドライブを今回独立にre-hashした事実ではない**。

重要な変化として **`Qwen/Qwen3.8-27B@37561816e66b5b9153b1b64c10968c18c1e6f4a0`** の**30選択ファイル・55,586,105,207byte（18学習済み重みシャードとSHA256参照）** が台帳でVERIFIEDになった。この固定revisionは [Phala rank3 LoRA](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA) の `adapter_config.json` が要求する親revisionと一致する。よって過去の「親原本が台帳にない」は最新台帳では否定される。ただし実Dを検査していないため**同じ親が現に使用可能という証明ではない**。Phala作成データのStanford Alpaca由来CC BY-NC条件とSGLang上のFP8親互換性は別途STOP。

**REMORYも修正**：独立残差メモリ約2.006BはQwen親が必要。過去の[R127](../../manifests/drafts/r127-2026-11-20-remory-20file-online250-and-parent-delta.candidate.json)による訓練親revision `1d4bf0f2ff6012fd82039d0dd7c60c0` は2026-11-20の公開APIで404だった。旧台帳の29個のシャード/ファイルハッシュ同一報告と3小メタデータ差分は再利用の有力な根拠だが、**今のowner実物SHA・正規メタデータ・コードABIを検証しない限り完全offline復元PASSではない**。

## 2. 今回新たに選定した学習済み原本3件と交換判断

| 原本／一次資料 | Publisher固定revision | 元source（十進byte） | 完全な学習済み数の検証範囲 | 判定と置換 |
|---|---|---:|---|---|
| [RikiyaT Qwen3.5 0.8B Weight-Space Programming](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming) | `d1671a178705bcab7644806d23c535517f35723b` | 1,779,420,899（17files） | 873,438,784（HF主checkpoint） | **CONDITIONAL正式採用を推薦**。小型の直接重み編集研究を重複改変より優先 |
| [JetBrains Mellum2.1 12B A2.5B Thinking-MTP](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-MTP) | `d55846102dd1c047e95d4841070f88290227c3b7` | 25,165,148,781（17files） | **12,578,294,528**（主12,149,923,072＋MTP 428,371,456） | **CONDITIONAL正式採用を推薦**。無MTP版の主重みを別保存しない |
| [Ricursive Ripple-65B Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | `d58dbcf43344e27494a40cec6727e180450f4a6b` | 129,572,889,973（32files） | 64,782,689,360（HF全主safetensors） | 独立事前学習のアーカイブ価値は高いが、**実容量・コード/ABI・品質の評価までP3取得保留** |

3源合計 **66 publisherファイル・156,517,459,653byte・LFS SHA256参照25件**。出版社の公開APIを40桁revision固定で照会し、66件の名前・byte・Git OID／LFS SHA256参照を照合。一方でローカルの重量ファイルに対するSHA256再計算はしていない。

**Rikiyaの価値と限界**：出版社はQwen3.5-0.8Bの2つのMLP層で約131,072個の重み要素を直接編集、親の固定revisionと変更tensorのhash/編集コードを公開。出版社側のH200/vLLM0.33.0によるMATH-500全500題×4生成は編集モデル51.0%。ただし元モデルの比較が25題のsmoke testで、**同条件・同設問・同標本数の独立比較は未達**。小ささが高精度を保証するわけではない。

**Mellumの元重みを二重にしない**：出版社は通常版の5本のBF16主重量とMTP版の5本のLFS SHA256が完全一致すると明記し、実際に公開APIで5/5一致。MTP別ファイル `model-mtp.safetensors` は856,767,160byte、**HTTP Range 206でヘッダ8byte＋24,240byteだけを読み**、205 tensor・BF16・428,371,456個の学習済み要素と集計。主12,149,923,072に加えた**12,578,294,528個**を保全対象の全パラメータ数とする。通常版repoを別に保存すれば約24.3GB級の主重みを重複。モデルはMoEで**inactive expertも全部数える**。作者のHumanEval+91.5%、SWE-bench Verified47.0%は出版社評価、Pi v0.73.1のagent harness、context114K、1回16K生成上限、Mellumの温度1.0という条件であり、ユーザー実機の測定ではない。

**Rippleの保存価値**：出版社は別体系のdense 65Bを12T tokenから事前学習した原本と説明。既存Qwen27B編集版の単なる量子化・マージではない。ただし独立事前学習の事実と特定ベンチの優秀性は分ける。出版社の1,048,576 token context・SWE-bench Verified76.5%は実機独立測定で未検証。129.573GB BF16原本を最初に転送しない。

**交換・不採用の比較**：[Huihui Qwen3.5-0.8B abliterated](https://huggingface.co/huihui-ai/Huihui-Qwen3.5-0.8B-abliterated)は約1.77GB・Apache-2.0だが作者自身proof-of-conceptで比較ベンチが弱く、Rikiyaの編集来歴をまず優先。[Vortecks LFM3 Heretic](https://huggingface.co/Vortecks/LFM3-1.7B-Heretic-Abliterated)は既存FrostWolfと同じLFM3親の別編集だが、3/100という作者試験のみではもう3.476GBを追加する費用効果は不明。[Nous Arete-27B](https://huggingface.co/NousResearch/Arete-27B)は政治的価値観7区分の後学習SFTという固有性がある一方、出版社自身の政治評価と既存Qwen27B基盤の系譜重複があり、約54.74GBを今すぐ追加せず独立評価待ちとする。いずれも永久除外ではない。

## 3. 実務上のsource確定：66取得報告を引いた13配布元

対象は[非実行の段階別固定キュー](../../queues/proposed-v57-r135-ledger66-next-deduplicated-sources.json)。各源の40桁rev、全243fileのpath/byte/元Git SHA1・LFS SHA256と、現行取得報告のモデルIDを照合。**66報告済み原本は新キューに1件も再要求していない**。本キューは取得器のapproved入力ではない。

| 手順 | 非実行のsource範囲 | 件数 | ファイル | 十進source bytes |
|---|---|---:|---:|---:|
| P0 親を共有・依存を補完 | Phala 13MB、Maya2のMimi codec／ECAPA話者encoder | 3 | 22 | 486,825,520 |
| P1 独自の小型モデル＋評価基盤 | Rikiya0.8B、FrostWolf LFM3 1.7B、ELYZA、Aya、Rumble ASR、Aion 2.3B | 6 | 131 | 11,382,100,237 |
| P2 中型・コード/MTP・別アーキテクチャ | Spark4B、Heretic9B、Mellum2.1 MTP | 3 | 58 | 52,735,978,432 |
| P3 大型・継続検証 | Ripple65B BF16 | 1 | 32 | 129,572,889,973 |
| **合計** | **未報告の13 sourceのみ** | **13** | **243** | **194,177,794,162** |

P0でMaya2の学習済み本体（取得報告13ファイル・5.021GB）もQwen27Bの学習済み本体（取得報告55.586GB）も**再取得しない**。外部codec/adapterがowner実物に無ければ、[Mimi/ECAPA15ファイル固定元](../../manifests/drafts/2026-11-20-maya2-mimi-ecapa-repro-deps.candidate.json)とPhala7ファイルを個別ライセンス審査する。P1のELYZAはNTFS上で使えない元ファイル名の旧CSVを意図的に外した既存R128スコープであり、全公開sourceミラーと表示しない。

## 4. 変数表と容量／次元チェック

| 記号 | 意味（日本語） | 単位（SIとの関係） | 定義（この調査の観測値） | 前提／範囲 | 型 |
|---|---|---|---|---|---|
| `B0` | 親再利用・依存source | byte（情報量単位） | 486,825,520 | 未取得を仮定した選択ファイル合計 | 非負整数スカラー |
| `B1` | 小型・評価source | byte | 11,382,100,237 | 6配布元選択ファイル合計 | 非負整数スカラー |
| `B2` | 中型独立学習source | byte | 52,735,978,432 | 3配布元選択ファイル合計 | 非負整数スカラー |
| `B3` | 大型保留Ripple source | byte | 129,572,889,973 | 近々の取得承認対象には含めない | 非負整数スカラー |
| `B_near` | P0～P2の論理source合計 | byte | `B0+B1+B2` | 共有ハッシュ・実ディスク占有は未検証 | 非負整数スカラー |
| `B_all` | P0～P3全source | byte | `B_near+B3` | 未承認であり追加取得予測ではない | 非負整数スカラー |
| `D_free` | ユーザー現在の実HDD空き | byte | **未観測** | owner D実機の同一ボリュームに限る | 非負整数またはnull |
| `F` | 保持するHDD最小空き容量 | byte | 200,000,000,000 | ステージング中も維持 | 非負整数スカラー |
| `N_base` | Mellum本体の全主学習要素数 | 1（個、無次元） | 12,149,923,072 | BF16 main5シャード | 非負整数スカラー |
| `N_mtp` | Mellum追加ヘッド学習要素数 | 1（個、無次元） | 428,371,456 | safetensorsヘッダ205tensor | 非負整数スカラー |
| `N_total` | MellumとMTPの総要素数 | 1（個、無次元） | `N_base + N_mtp` | inactive expertも含める | 非負整数スカラー |
| `N_limit` | 新規モデル研究の硬い上限 | 1（個、無次元） | 150,000,000,000 | 以上を今回の取得候補に入れない | 非負整数スカラー |

1. `B_near = 486,825,520 + 11,382,100,237 + 52,735,978,432 = 64,604,904,189 byte`、つまり約**64.605十進GB**。
2. `B_all = 64,604,904,189 + 129,572,889,973 = 194,177,794,162 byte`、約**194.178十進GB**。
3. Mellumの `N_total = 12,149,923,072 + 428,371,456 = 12,578,294,528 < 150,000,000,000`。単なる2.5B **active**では判定せず、inactive expertsと追加MTPも合算。
4. **次元チェック**：B系はすべてbyteなので加算可能。N系はテンソル要素個数なので加算可能。byteとパラメータ数を直接加減算せず、量子化だけで総学習済み要素数が減ったとは解釈しない。
5. 現実のディスク審査には `D_free` 及び重み・依存・一時キャッシュ/staging中の最大占有量が必要であり、数値未観測の現時点では `D_free >= F + B_near + cache` を証明できない。既存台帳の最小空き約2.051TBを現在値として代入しない。

## 5. 公開規制は3つの独立経路で追跡

**法令上確認された事実**：[米国BIS 2026-11-19 Interim Final Rule](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は旧AI Diffusion Ruleのモデル重量ECCN **4E091を撤廃**。別途、先端半導体／遠隔データセンター等の特定用途・送付先規制はあり、全open-weightの所持禁止が成立したと推論できない。[EU AI Act Article53](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)はGPAI提供者の書類・著作権等義務を定め、一部オープンソースの例外を認める。全公開weightsの禁止ではない。[HF Gatedの一次規程](https://huggingface.co/docs/hub/en/models-gated)によればアクセスは本人単位の承認で、あとから取消し可能。権利確認と将来Gated化仮説は分ける。

**本調査で確認できない仮説**：次に無検閲モデルだけが先に閉鎖される、より小さい重みだけを一律禁止する、大規模原本の取得期限が何日と定まっている等。モデル別公開終了日と発生確率は**測定不能**。S1→S2→S3という将来予測を取得順位の自動根拠にせず、既存原本の重複の有無・学習独自性・ライセンス・パラメータ・保存/復元条件で判断。

## 6. H/T/D/C/U・ERROR CHECK

**H（反証可能仮説）**：Qwen27BとMaya2の取得報告済み原本を再利用し、初回は小型編集済み重み・必要codecと評価データを選べば、同じストレージ枠で互いに異なる学習成果を増やせる。MellumのMTP版1repoは非MTP版との重複を排除しながら推論用学習ヘッドを保存する。

**T（最小検証）**：元のPublisher SHA/固定revisionのパス・byte・Git SHA1・LFS SHA256をR134の66件とR135の243候補全件で照合（`n_min=243`のリポジトリファイル参照、各モデルは何か一つ不一致なら停止）。オーナーDでは66取得報告の本体を読み取り専用再ハッシュし、特にQwen18シャードを先行。性能は同一GPU/clock/driver/CUDA/backend/量子化zero-point/バッチ/コンテキストを記録し、P0/P1研究課題を最低100 paired held-out入力で独立比較。出版社評価と別にする。

**D（合否）**：PASS_SOURCE＝既知メタデータ3配布元66ファイルと選定済み13配布元243ファイルの相互整合、MTPヘッダ205テンソルを含むこと。PASS_ACQUIRE＝利用者の行為別権利・実媒体とSHA・staging込み200GB床・コードABI・不変snapshotの個別取得承認が全て証明された場合のみ（**今回未達**）。FAIL＝重複原本、超過または不明総数の無条件取得、本人許可なきGated取得。UNCERTAIN＝実機依存・能力維持と将来の規制変化。

**C（破れ方）**：Qwen親は台帳上存在してもownerD上に存在しない、PhalaのFP8推論互換が崩れる、Rikiyaの微小編集は別条件では品質低下、Mellum MTPがuser backendに対応しない、Rippleがメモリ/容量で非現実的、出版社の公開状態は安定したまま規制仮説が成立しない。

**U（不確かさ）**：上流repo一覧の鮮度、重みハッシュとowner媒体現物の差、ライセンス適用行為、CUDA/ABI、作者試験の選択バイアスとサンプルサイズ、容量cache。統計的反復と外部独立ベンチが不足するため合成標準不確かさ`u_c`および包含係数`k`を創作しない。

**ERROR CHECK**：研究時v57=213登録／166有効、既存66取得報告に対する再ダウンロード重複0。新規検証固定元3件66files／SHA参照25／156.517GB。全段階13源243files／194.178GB（P0～P2 64.605GB、P3大型保留）。新しい重みDL0、本人Gated権限の代理同意0、正式approved0、既存model削除0、従来v57正式カタログの変更0。関連分野：ML学習系譜、長期保存の整合性、法令・契約、実験計画、計算機アーキテクチャ。

###〈次に考える問い〉

**取得報告済みQwen27Bの18重量シャードとMaya2の13ファイルを所有者Dで独立再ハッシュした結果、Phala/Mayaの復元に本当に不足する原本は何バイトか。** 追加モデル数より**合法・オフライン復元できる学習済み能力の純増数**を次の評価指標にする。
