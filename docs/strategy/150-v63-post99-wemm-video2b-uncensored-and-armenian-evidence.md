# R150 / v63: 99取得報告の後の小型映像理解、無検閲差分、低資源言語の採否（2026-11-22）

## 結論と正本の扱い
正本は引き続き `catalog/CURRENT.json` の **v63: 235件登録 / 188件有効（SELECT55 / CONDITIONAL133）**。今回のR150は**調査決定を追加**するが、正式overlayや取得済み台帳を変更せず、実行可能な承認・重量ダウンロード・モデルコード実行・既存ファイル削除を発生させない。

99モデル / 1,478ファイル / 1,879,994,309,866 byteは取得実行台帳上のVERIFIED**報告**。所有者Windows Dドライブの再SHA、個別の法律上の利用行為許諾、完全なオフライン復元を今回検証した結果ではない。11repoの次回研究対象（10repo=68,544,170,933 byte + Ripple HOLD 129,572,889,973 byte）は[既存R149キュー](../../queues/proposed-v63-r149-after99-11-research-only.json)を正本として残す。

## 新しい研究結果と判定

| 候補 | 判断 | publisher source / 目的 | 停止条件 |
|---|---|---|---|
| [Tencent WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B) | **R1/CONDITIONALに向けた研究ソース固定**。まだv63正式資産ではない | 元動画・音声を同期的に扱う小型時系列multimodal学習状態。大規模MOSS-VL-Realtimeと用途が重なるが学習済み原本と容量が異なるため、無測定の置換は禁止 | 27ファイルの出版社immutable revision、25ファイルに発行者SHA256。二分割Safetensors。custom code + patched vLLM/SGLang ABI・第三者依存／権利／GPUピーク未検証。別のpublisher tree censusと25/25 SHA一致、全27file正確に6,590,699,556byte |
| [OpenUncensored Inkling Mini Full](https://huggingface.co/OpenUncensored/Inkling-2-Mini-Uncensored) | **フル約20GBの追加保全を見送る** | 公開者は同じ拒否編集のrank2 LoRA版も提供。既存v59に親ThinkingMachines Inkling・rank2 LoRA・別ablation編集を登録済み | LoRA再合成とfullのtensor完全一致は独立検証前。現物を削除したり同一性を断定しない |
| [Metric-AI Ayb-0.5-0.8B](https://huggingface.co/Metric-AI/Ayb-0.5-0.8B) | **HOLD** | Qwen3.5-0.8B派生でアルメニア語特化。低資源言語アーカイブとしては独自価値 | GatedアクセスとCC BY-NC 4.0。本人のgate許可・行為許諾・固定SHAが揃わない。迂回不可 |
| [Ricursive Ripple-65B](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | **P3 HOLD継続** | 既存研究キューの約129.573GB原本 | 同条件実測による独立価値・復元環境・容量証明の不足 |

### Timestral-5Mの超小型予測原本と競合比較

[Mistral公式Timestral-5M](https://huggingface.co/mistralai/Timestral-5M)を追加の**非実行ソース固定・研究CONDITIONAL候補**とする。immutable revision `bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f`、全6ファイル **20,854,471byte**（F32 `model.safetensors`ほか）を[出版社tree census](../../manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json)から確認済み。現行にすでにある28M版とは**パラメータを少なくした独立学習済み原本**であり、元の28Mを置換する根拠ではない。作者ベンチマークGIFT-Eval MASEは5M **0.705**、28M **0.678**（小さいほど誤差が小さい）。改善ではなく、容量と品質のトレードオフ。作者記事は8-thread CPUの1日先予測を5M約17msと報告するが、実機再現なし。モデル全体がModified MIT：**利用者本人または雇用者の前月連結月商がUSD20m超の場合、別途ライセンス取得が必要**。無料使用の無条件認定は禁止。取得許可・本人行為別ライセンス審査は別。

比較候補 [Datadog Toto-2.0-4m](https://huggingface.co/Datadog/Toto-2.0-4m) はApache-2.0公開・約4Mで、作者はA100・バッチ8・予測長1024条件の約3.8ms forward passを報告（クロック未記載）。**同一HW・context・データのTimestral-5Mとの直接性能優越性は未実証**。Publisher不変revisionと完全ファイルSHAを未固定のため、正式追加ではなくwatchlistにとどめる。time seriesの小型保存は無検閲LLMと別のタスクであり、汎用QAの代替にはならない。

### WeMM 原本とSHAの意味
[公開元の不変コミット](https://huggingface.co/tencent/WeMM-Video-2B/commit/821690998399cac0f55bb7f7f805ebafa650c3a4)は `821690998399cac0f55bb7f7f805ebafa650c3a4`。[publisher SHA256SUMS](https://huggingface.co/tencent/WeMM-Video-2B/raw/821690998399cac0f55bb7f7f805ebafa650c3a4/SHA256SUMS)は25 pathのdigestを列挙する。27 pathのうち `.gitattributes` と `SHA256SUMS` 自身には同表にhashがなく、Git tree OID/byte censusが追加で必要。モデルindexの `metadata.total_size=6,567,256,208 byte` は**重みのtensor payload表記**であり、ダウンロード対象全ファイルのbyte数ではない。別のpublisher tree全27file監査と25/25 SHA照合を行い、**全体6,590,699,556byte、重み2 shard合計6,567,395,904byte** を正本のPublisher参照値として確定した（[照合先](../../manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json)）。ただしオーナー媒体の存在や権利・動作環境は確定しておらず、取得未承認の研究候補とする。

[機械可読publisher digest一覧](../../manifests/drafts/r150-2026-11-22-wemm-video2b-publisher-sha256.candidate.json)を公開元の記録として転記した。Dの現物を検査したものではなく、モデルの重みをロード・実行してもいない。公開者のモデルカードはApache-2.0を掲示するが、第三者ライブラリ・音声映像の利用条件は別。コードに `trust_remote_code` / custom `modeling_wemm.py` / `h5_modeling_*.py`等があるため、未審査ロードを停止する。報告されたハードウェアL20/H20、パッチ付きvLLMは利用者環境の保証ではない。2Bは名称上のtext規模であり、全multimodal学習済みtensor総数を独立に数えていない。

### 重複排除と順位
既存最小P0 4repo合計 **2,234,744,280byte**を先に審査し、その次に20.85MBのTimestral-5MのModified MIT権利と28M差分の実測を行う。次にWeMMのsource/実ディスクbyte差分とcustom codeレビューを行い、P1の無検閲親・2B視覚対話に追加する価値を審査する。既存OpenMOSS 22,687,497,344byteとWeMMを性能比較せずに入れ替えない。既存P0–P2 10repo **68,544,170,933byte**に、追加の新2repo Publisher原本6,611,554,027byteを参照する（単純合計75,155,724,960byteはオーナーの増分所要容量ではない）。既存sourceにWeMMの`model.safetensors.index.json` payloadを単純加算して正式予算と称してはならない。30億パラメータ規模というHF UI表記と「Video-2B」という名称も、合計tensor censusで検証してから総パラメータ制約を判定する。

## 規制リスクと権利の分離
[米BIS連邦官報2026-11-19](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧モデルウェイトECCN 4E091を撤廃。半導体／最終用途関連の規制や発行者のライセンス、Gated条件は別。個別モデルの将来禁止確率は**計測していない反証可能仮説**として扱い、過度な規制予測で選定順位を偽装しない。無検閲の保存価値は編集差分・親との関係・検証可能な重みが残るかで判断する。

## 次の最小検証ゲート（H/T/D/C/U）
- **H**: WeMMは既存のOpenMOSSとは異なる有用な2B級音声動画タスク原本で、容量削減の価値がある（出版社が訴求する範囲の仮説）。構成・重みSHA・独立再現によって反証できる。
- **T**: まず非実行でimmutable 27全ファイルと25発行者SHAを照合し、LICENSEとcustom code依存を静的監査。次に権利が許す場合だけ、同一動画音声タスク・同じGPU/クロック/バッチ/contextの複数試行を比較する。未承認ならそこで停止。
- **D**: `PASS` は全source identity・法的取得行為許諾・安全な起動・200GB以上の物理空き床・GPU/品質ゲート全て成立。`FAIL` はsource不一致または権利不成立。`UNCERTAIN` は未測定・権利不明・モデル評価未実施。現在`UNCERTAIN`。
- **C**: Transformer/codec/patch ABI不適合、低フレームレート失敗、音声同期喪失、元より性能低下、出版社SHA再配布差分。
- **U**: 主要不確かさは発行者自己申告、file byte census未収集、所有者HDD未接続、GPU/バッチ/字幕正規化差、データ偏り。拡張不確かさ`u_c`と包含係数`k`は実測標本がないため数値を作らない。

## 隣接分野
- **システム工学**：GPUピークRAM、ストリーミング時のI/O、custom codeのサプライチェーン検査
- **法務・AIガバナンス**：配布許諾と個人の保存行為、Gated、音声映像・生体情報の権利
- **デジタルアーカイブ学**：original hash、親・adapterの最小再構成closure、immutable provenance

すべての新たな取得は非実行研究キュー。既存取得99repoを重複転送せず、`queues/approved.json`は空。新規モデル正式登録が必要なら、明示的v64 overlay・全派生データ・全テストを同期してから実施する。
