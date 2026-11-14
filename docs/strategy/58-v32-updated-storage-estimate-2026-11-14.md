# R58 — v32の4TB容量見積書更新・NVIDIA特殊資産の追加調査（2026-11-14）

> **現行R62見積り（2026-11-14）**：[ACE XL固定34ファイル／重複QwenとNVIDIA Kumo確認](62-v32-ace-exact-file-census-and-kumo-tag.md)。R58・R61の丸め値は歴史的な参考試算。今回確定したACE source 増分は **24,041,795,415 byte**、全体の部分ソース算術合計は **3,466,070,232,173 byte**。最終オフライン容量・現実のHDD空きは未確認。

> **R61 ACE dependency refinement (2026-11-14)**: [ACE-Step XLの共有部品・既存Qwen SHA重複精査](61-v32-ace-xl-dependency-dedup-and-budget.md)。R58の10.1GB共有元全量は取得必須容量ではない。約5.307GBの対象3フォルダと既選定Qwen重み1,191,586,416byteのSHA一致を確認。**新しいR61値は公称丸めを含む参考計算で、最終保存byteを保証しない。**

**現行はmain/v32**（本更新前HEAD: `cf2dbe8d3774442652c59674a7a73a6eae25a704`）。研究ブランチ`strategy/2026-11-03-01-risk`は現時点で存在せず、v31資料を残したままmainの新規ファイルのみ追加する。**CURRENT、選定判定、取得承認キュー、本体ファイル、実HDDには変更なし。**

この「見積書」は保存容量の明細。ベンダー・数量・単価が未指定のため円建て購入費・税・配送費は**未見積**。ダウンロード済み容量を表すものでもない。

## 1. 新しい研究確認

- v32管理182件、アクティブ135件（SELECT53＋CONDITIONAL82）。v27の126件からの新規9件のうち8件は公開元の固定したsource/file範囲がある。残る**ACE-Step XL**の選択byteと必要共有モデルはまだ正確に固定されていない。
- v32でRFD4-ProteinaとNemotron-3-Diarizationは既に条件付き選定済みであり、前回のNVIDIA提案に改めて候補として存在しても**新規二重加算しない**。RFD4は公開元106GB全repoではなく、Flow+AEの固定元7ファイルだけ1,742,698,063byte。
- NVIDIA IsingのColorCodeとSurfaceCodeは現在Gatedで正規本人許可の研究が先。Kumo Relationalは公式repoのclassifier.pt約120MB・regressor.pt約124MBで、約244MBは**公開表示の丸め値**でありSHA固定byteではない。Kumo Anomaly/Tabular/Forecast、Nemotron Parse、GR00T N1.7、QCalEvalは原本性・依存・権利の追加調査対象。**新規候補のbytesを不明だから0円/0byteとして予算へ混入しない**。

## 2. 正本に基づくv27＋v28–v32の源ファイル範囲

- **v27**: [固定範囲の集計](../../catalog/capacity/2026-11-07/v27/capacity-summary.json) により126有効資産の既知内容SHA union `3,417,685,712,585`byte。約3.418TB。必要な外部音声/動画原本・復元実行環境は未閉包。
- **v28–v30、v32の8資産**：固定元のsource/一部reference scopeを足した `24,342,724,173`byte。**v29のZONOS3 14-file keep2は確定最小構成でない**。版横断すべての同一hashを最終統合したわけではなく、合計は最終SHA-aware unionを主張しない。
- **v31の1資産**：ACE-Step XL本体の作者表示約20GBと共有元repo約10.1GBはどちらも概数。後者には採らない2B系などが含まれるため全部を必要依存と断定できない。

| # | 版 | 資産 | 公開元の選択/参考スコープ（byte） | エビデンス分類 | 根拠 |
| ---: | --- | --- | ---: | --- | --- |
| 1 | v28 | [`qvac/BotPsy-0.8B`](https://huggingface.co/qvac/BotPsy-0.8B) | 1,726,201,481 | `FULL_REPO_IMMUTABLE_SOURCE` | [固定元](../../catalog/research/2026-11-12-r49-botpsy-ttm-immutable-census.json) |
| 2 | v28 | [`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | 6,126,375 | `FULL_REPO_IMMUTABLE_SOURCE` | [固定元](../../catalog/research/2026-11-12-r49-botpsy-ttm-immutable-census.json) |
| 3 | v29 | [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini) | 11,076,560,635 | `PINNED_14_FILE_KEEP2_REFERENCE_SCOPE_NOT_PROVEN_MINIMAL` | [固定元](../../catalog/research/2026-11-12-r48-pinned-scopes.json) |
| 4 | v29 | [`robbyant/lingbot-touch-tiny`](https://huggingface.co/robbyant/lingbot-touch-tiny) | 21,873,479 | `FULL_REPO_IMMUTABLE_SOURCE` | [固定元](../../catalog/research/2026-11-12-r48-pinned-scopes.json) |
| 5 | v30 | [`nvidia/Alpamayo2-Edge`](https://huggingface.co/nvidia/Alpamayo2-Edge) | 5,320,375,887 | `FULL_REPO_IMMUTABLE_SOURCE` | [固定元](../../catalog/research/2026-11-12-r50-alpamayo-edge-immutable.json) |
| 6 | v32 | [`tencent/Qwen3.8-27B-DSpine-b16`](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | 4,051,857,976 | `PINNED_SOURCE_SUBSET_REUSES_PARENT_QWEN` | [固定元](../../catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json) |
| 7 | v32 | [`nvidia/Nemotron-3-Diarization`](https://huggingface.co/nvidia/Nemotron-3-Diarization) | 397,030,277 | `PINNED_SOURCE_SUBSET_NO_DUPLICATE_GGUF_NEMO` | [固定元](../../catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json) |
| 8 | v32 | [`nvidia/RFD4-Proteina`](https://huggingface.co/nvidia/RFD4-Proteina) | 1,742,698,063 | `PINNED_NATIVE_FLOW_AE_SOURCE_SUBSET` | [固定元](../../catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json) |

## 3. 差額の試算（**現実のHDD空きではない**）

| ケース | 部分スコープ算術和（byte） | 約TB（十進） | 空の4TB+200GB床仮定の机上差額（byte） |
| --- | ---: | ---: | ---: |
| v27既知＋後続8固定/参考スコープ（ACE未算入） | 3,442,028,436,758 | 3.442 | 357,971,563,242 |
| 上にACE XL原本の作者公称約20GBを仮加算 | 3,462,028,436,758 | 3.462 | 337,971,563,242 |
| さらにACE共有元全repoの公称約10.1GBを仮加算 | 3,472,128,436,758 | 3.472 | 327,871,563,242 |

上記は**上限/下限の統計区間ではない**。ZONOS3参考範囲やACE共有元全repoは削減可能な一方、未確認の外部学習済みcodec・実行コード・ABI・staging・キャッシュ・所有者の既存ファイルは容量を増加させる。**4TBへの適合性判定はUNCERTAIN**。v31の概算を厳密byteにすり替えない。物理的空き200GBの床をゼロとして予算を使い切らない。

## 4. 未採用NVIDIA候補（元のv32の135件には予算算入しない）

| 候補の公式URL | 調査 | 公開状況 | 公開源参考容量 | 独自機序・止まる理由 |
| --- | --- | --- | --- | --- |
| [`nvidia/Ising-Decoder-ColorCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | P0 | GATED | 未確定 | Distinct quantum color-code predecoder; no personal gated approval |
| [`nvidia/Ising-Decoder-SurfaceCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | P0 | GATED | 未確定 | Distinct surface-code predecoder |
| [`nvidia/Kumo-Relational`](https://huggingface.co/nvidia/Kumo-Relational/tree/main) | P0 | PUBLIC_METADATA_ONLY | 約244MB（丸め表示） | Two learned task heads classifier and regressor approx 120MB +124MB published display; not exact selected files |
| [`nvidia/Kumo-Anomaly`](https://huggingface.co/nvidia/Kumo-Anomaly) | P0 | PUBLIC_METADATA_ONLY | 未確定 | Different diffusion anomaly detection trained state |
| [`nvidia/Kumo-Tabular`](https://huggingface.co/nvidia/Kumo-Tabular) | P1 | PUBLIC_METADATA_ONLY | 未確定 | Single-table task distinct from Kumo Relational |
| [`nvidia/Kumo-Forecast`](https://huggingface.co/nvidia/Kumo-Forecast) | P1 | PUBLIC_METADATA_ONLY | 未確定 | DARR retrieval-based timeseries forecasting |
| [`nvidia/Nemotron-3.5-Parse`](https://huggingface.co/nvidia/Nemotron-3.5-Parse) | P1 | PUBLIC_METADATA_ONLY | 未確定 | Learned document parser, not identical to OCR model |
| [`nvidia/GR00T-N1.7-3B`](https://huggingface.co/nvidia/GR00T-N1.7-3B) | P1 | PUBLIC_METADATA_ONLY | 未確定 | Independent robot VLA generation, compare incumbent N1.6 and action schema |
| [`nvidia/QCalEval`](https://huggingface.co/datasets/nvidia/QCalEval) | P0 | PUBLIC_METADATA_ONLY | 未確定 | Annotated quantum calibration evaluation data, rights/corpus audit needed |
| [`nvidia/RFD4-Proteina`](https://huggingface.co/nvidia/RFD4-Proteina) | COVERED | ALREADY_CONDITIONAL_V32_NOT_READD | 未確定 | Already in v32 pinned native subset; do not duplicate as new option |
| [`nvidia/Nemotron-3-Diarization`](https://huggingface.co/nvidia/Nemotron-3-Diarization) | COVERED | ALREADY_CONDITIONAL_V32_NOT_READD | 未確定 | Already v32 selected subset; do not duplicate |

## 5. 変数表と次元チェック

| 変数 | 意味（日本語） | SI単位 | 定義 | 定義域／前提・型 |
| --- | --- | --- | --- | --- |
| `C` | 選定計画上限 | byte | 4,000,000,000,000 | 非負整数スカラー、実HDD総容量とは独立 |
| `Fmin` | 取得後の最低空き床 | byte | 200,000,000,000 | 非負整数スカラー、実測前 |
| `B27` | v27既知内部SHA union | byte | 3,417,685,712,585 | 非負整数スカラー、完全学習済み依存を含まない |
| `ΔB` | 8資産の固定/参考元scopeの算術和 | byte | 24,342,724,173 | 非負整数スカラー、v29の参考範囲含みクロス版dedup未確認 |
| `BACE` | ACE XL本体公称原本 | byte | 約20,000,000,000 | 近似スカラー、正確な選択payloadではない |
| `BSH` | ACE shared repo全量公称（採用しない2B含む） | byte | 約10,100,000,000 | 近似スカラー、採用構成でない |
| `Factual` | 物理ディスクの実空き | byte | null | 非負整数/null、所有者機器未接続 |
| `U` | 机上差額 | byte | C−Fmin−既知scope等のケース別仮合計 | 整数スカラー、実空きではない |

**次元・単位チェック**：すべての加減算はbyte同士。TBは十進1兆byte。モデルパラメータ数は無次元で量子化後の実重量bytesやCPU/GPUピークRAMと同じではない。512GB推論上限も保存HDD容量と混同しない。

## 6. H/T/D/C/U・合否基準

- **H**：独立学習成果と必要原本を一つずつ同定すれば、性能順位に依存せずモデルの長期復元能力を広げながら、過剰量子化/変換重複を削減できる。
- **T**：既存135件の現行ID、v27の126件の集計、v28以降9件のうち8件の公開元固定スコープ（残り1件は不明）を照合。Kumo等の未採用候補は配布源・ライセンス・固定byte/全依存を別の非実行マニフェストで検証。HDDは所有者許可と同定が済むまで非接続扱い。
- **D**：数字の和はPASS（上記）だが、完全なv32最終容量と200GB空きの同時成立は**UNCERTAIN**。権利不適合、無承認取得、実容量超過が確認された場合は取得FAIL/STOP。
- **C**：同じ重みの異形式が重複している、SHAが同一でもランタイムABIが異なる、未知の学習済みVAE・安全processor・外部素材が必要、現在Gatedの権利を得られない。
- **U**：元repoメタデータはローカルSHA実測と異なり、ACE公称値は丸め、保存領域の空きと依存・stageは未測定。分布が定義できず合成標準不確かさu_cと包含係数kは不算出。

## 7. ERROR CHECK・変更の境界

- v32=182/135、v27=126、後続アクティブ9（8 source scope、ACE1未確定）。ΔB=24342724173、ケースA=3462028436758、ケースB=3472128436758。
- 元repoのGit blob SHA1はSHA256と混同しない。固定Hugging Face SHAもローカル内容照合にはなっていない。v27と新規8資産の跨いだSHA unionは完全には検証していない。
- **approved queue=0**、モデル取得=0、実機実行=0。mainの現行選定と正本を変更せず、read-only推計ファイルのみ追加。

### 〈応用・転用例〉

機械学習：重み系譜と独立SFT/蒸留を識別。デジタルアーカイブ：音声codec/AE/外部データを含む復元閉包。ソフトウェア供給網：SHAとruntime ABIの完全性。法務：Gated権とライセンス地域/用途の評価。

### 〈次に考える問い〉

ACE-Step XLの外部共有学習済み部品とNVIDIA Ising/Kumoの必要ファイルを固定した結果、実ディスクの200GB安全床と両立する独立学習状態はどれか。
