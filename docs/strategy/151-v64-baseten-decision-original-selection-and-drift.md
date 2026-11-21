# R151 / v64 — 非生成・長文マルチモーダル判定原本の条件付き選定と取得元差分（2026-11-22）

## 結論
**唯一の現行正本: v64, 236登録／189有効 (SELECT55、CONDITIONAL134)**。旧v63 235件の内容・判定は全件同一。新規は [baselabs/bison-1](https://huggingface.co/baselabs/bison-1/tree/bf8350b2c59eb6c36e95d02a2af870aec18724a7) の独立学習済み原本1件のみ。**CONDITIONAL、research-only、取得許可ではない**。従前R150では同一条件ベンチ未測定のためHOLDだが、v64では性能優位の確証ではなく独立の公開後学習済み状態を保全候補に登録した。既存小型判定器を置換せず、P0優先の小型モデルより後に置く。[source 16件＋SHA/byte](../../manifests/drafts/r151-2026-11-22-baseten-bison-and-groundhog-frozen.candidate.json)、[正式overlay](../../catalog/revisions/v64-2026-11-22.json)、[全189 STOP](../../catalog/readiness/v64-2026-11-22-r151-all189-gates.json)、[取得後キュー](../../queues/proposed-v64-r152-post99-13-plus-bison-research-only.json)。

## 事実と選定推論

| 出版社原本 | Publisher SHA commit | HF公開ファイル数と参照byte | 研究判断 |
|---|---|---:|---|
| [bison-1](https://huggingface.co/baselabs/bison-1/tree/bf8350b2c59eb6c36e95d02a2af870aec18724a7) | `bf8350b2c59eb6c36e95d02a2af870aec18724a7` | **16／65,398,108,261** | **CONDITIONAL R2**：Gemma 4 31B ITベース、テキスト・画像に対するtyped decisionと確率校正の独自ポストトレーニング |
| [groundhog-1](https://huggingface.co/baselabs/groundhog-1/tree/f4602c43599114a7af2c158472b59a4ff2d13663) | `f4602c43599114a7af2c158472b59a4ff2d13663` | **16／53,120,939,617** | **RESEARCH HOLD**：MoE・約4B token活性だが53.121GBと大きく、同系列目的、判断Index未測定。保存を二重化しない |
| [Ayb-0.5-0.8B](https://huggingface.co/Metric-AI/Ayb-0.5-0.8B/tree/7184ec226df76c932d604886fa7a43f0becc9e38) | `7184ec226df76c932d604886fa7a43f0becc9e38` | **14／1,773,997,430（公開メタデータのみ）** | **GATED HOLD**：CC BY-NC 4.0、個別アクセス許諾と用途制限を確認せず取得しない |

BisonのPublisher主張：Artificial Analysis Decision Index v2.1 76 (19モデル中の作者掲示順位)、Brier score 0.14、LongMemEval M=84.8/S=87.1、128k文脈。Groundhogの作者公開値はLongMemEval M=77.4/S=79.3、同Index未測定。これらは**所有者同条件ベンチや第三者独立再現の証明ではない**。学習時Bisonは24 nodes × 8 B200、Groundhogは16 nodes × 8 B200と作者が記載するが、これは**推論の計測条件ではない**。推論速度・実ピークVRAMは未知。

Bison HF safetensorsには `total=31,273,086,512` と BF16 stored `32,682,375,020` が併記され、差がある。両者とも150Bを下回るが、**厳密なTensor再カウント、weight tying、実効メモリ検証は未実施**。64GB級の元重みは消費RAMやバックエンド適合の保証ではない。Bison LICENSE/NOTICEはBasetenの変更分MITとGoogle元Gemma 4 31B IT Apache 2.0の併記。作者掲載ライセンス文面は調査したが、**owner固有の保存・再配布・二次利用行為の契約審査は未承認**（`license_text_reviewed:false`）。

## 既存11件の公開元revisionを再調査

[機械可読の差分](../../catalog/research/2026-11-22-r151-publisher-revision-drift-after99.json)は11 repoを固定commitと現行APIで照合し、既得99件との再取得を禁止。**LiquidAI/LFM3-VL-2B の旧 `f83d2b0a2296aaa277f394990a9b8b949ddf9691` と新 `23387beda43c60310348e83e25f78f33c3140d3a` は重量ファイル `model.safetensors` のLFS SHA `a9bb8b1c...` が同じ**。README.md、generation_config.json変更、.eval_results/YAML追加のみ。旧保存対象を黙って新revisionへ更新しない。**公開repo合計**と**選定ファイル集合**を混同しない：Heretic、Kitten、Aurora、FastFramesなどには重複変換・補助ファイルの全repo差がある。

次の研究取得候補は（R150の13配布元を継承して更新）P0五配布元 **2.255599GB**（R150 Timestral 5M含む）、P1五配布元 **18.462108GB**（R150 WeMM-Video-2B含む）、P2三配布元 **119.836127GB（Bison含む）**。P0–P2 13 repo **133,942,279,194byte**。これに Apple FastFrames-Sの親17.567GB、Cactus追加ランタイム4.1MB等の依存を別加算、SHA重複を再計算する必要がある。P3 Ripple129.573GB HOLD。**現物D空き、キャッシュ一時2倍や200GB安全床は今回測定していない**。

## 法令リスクの認識
2026-11-19の米BIS公式規則は旧AI Diffusion Ruleのモデル重みECCN 4E091を**撤廃**（<https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm>）。モデル全面禁止が目前という断定は不成立。ただし別の輸出・用途規制、配布元Gated化、NCライセンス、当事者権利は残る。公開停止の将来確率は推定できない。

## H / T / D / C / U
- **H（仮説）**：独立の非生成・確率校正マルチモーダル原本1件を保存候補とし、同系MoEの53GBをHOLDすれば、目的の異なるtrained outcomesを余分に重複取得せず保全できる。
- **T（検証）**：HF公開APIで厳密16ファイル、4件LFS SHA、全byteと40字commitを固定。旧235行の同一性、189有効/134条件付き、16のowner_SHA=false、全189STOP、approved0を無通信テスト。品質は将来同一文書・画像・クラス比・promptで事前登録した100件以上のbinary/abstainタスクを評価（現在未測定）。
- **D（合否）**：Publisherメタデータ固定および重複排除だけSTATIC PASS。現物SHA、利用行為許諾、Transformers/Gemma4、readout処理、Windows/CUDA/ROCm backend、zero-point/quant/KV、実容量未確認ならDOWNLOAD STOP。秘密の自動許諾=trueや新重み取得を検出した場合FAIL。
- **C（対立仮説）**：既存の小型決定器で十分、Groundhogが実HWで優越、Bison校正が業務のクラス分布に一般化しない。
- **U（不確かさ）**：出版社ベンチ、HFサマリとBF16 element差、owner HDD/VRAM/ABI、契約・個人同意、文脈長／バッチ未検証。反復測定ないため数値`u_c`、包含係数`k`は未算定。

関連分野：確率校正・統計、長文マルチモーダルML、暗号学的供給元検証、著作権／輸出管理。

**今回は取得承認0、重量転送0、Owner D編集0、Gated回避0、第三者コード実行0、既存モデル削除0。**
