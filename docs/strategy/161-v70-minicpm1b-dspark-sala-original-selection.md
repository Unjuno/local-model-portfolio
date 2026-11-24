# R161／v70（2026-11-25）—超小型最終学習と独立DSpark原本の正式CONDITIONAL選定、疎線形SALAはHOLD

## 1.〈本論〉正本・選定結果

最新v69 `catalog/CURRENT.json`（**255資産／206有効、SELECT56／CONDITIONAL150**）から、旧255行の採否・ソース・バイトを完全保存したまま**v70を258資産／208有効、SELECT56／CONDITIONAL152／HOLD31**へ更新する。取得台帳の**116 VERIFIED／1,758ファイル／2,021,784,002,725 byte**は過去の実行側報告であり、所有者Windows Dの今回独立SHAや本人の法律上の許諾、完全オフライン復元を証明しない。今回の3原本repoは116取得済み報告とID重複なし。

**新規の学習済み原本のPublisher不変配布物**を正確に**3repo・30ファイル・21,778,440,013 byte・LFS SHA-256参照7件**として固定する。これは選定可能な研究用Publisher source参照容量で、実ダウンロード量でもOwner実HDD占有でもない。

| 正式採否 | 原本と固定40桁revision | Publisherファイル、容量（十進） | 理由と停止条件 |
|---|---|---:|---|
| **CONDITIONAL／最優先小型** | [`openbmb/MiniCPM5-1B`](https://huggingface.co/openbmb/MiniCPM5-1B/tree/ac83f813ba7da263c51a9f3ec37c2072597e54af) | **11件／2,171,355,218 byte** | 独立1,080,632,832要素のRL＋OPD最終学習原本。1B Base/SFTや従前v68選定の2Bとは学習成果が異なる。実機評価・ユーザー使用許諾は未確認 |
| **CONDITIONAL／最優先特殊補助** | [`openbmb/MiniCPM5-2B-DSpark`](https://huggingface.co/openbmb/MiniCPM5-2B-DSpark/tree/a63eb96b9bba7e999639d3fe3b6d70a0ea38eabd) | **4件／647,565,508 byte** | 新たに学習された323,776,001要素の推測デコーダ。親は既存既存v68選定`openbmb/MiniCPM5-2B`（取得報告116には未掲載）。ターゲット固定SHA/トークナイザ/hidden-state/SGLang結合が必要 |
| **HOLD／希少な別学習** | [`openbmb/MiniCPM-SALA`](https://huggingface.co/openbmb/MiniCPM-SALA/tree/9180fe1db74f71fb81bc7105efe88f6b19c959b0) | **15件／18,959,519,287 byte** | 疎25%＋線形75% Attentionの9,477,203,968要素の独立学習済み重み。`trust_remote_code`とOpenBMB SGLang fork/CUDA拡張が必要、未審査コード実行不可 |

厳密な[30ファイル・各Git blob SHA-1／Publisher LFS SHA-256](../../manifests/drafts/r161-2026-11-25-three-novel-small-dspark-sala-origins.candidate.json)、[正式採否・親子依存](../../catalog/decisions/2026-11-25-r161-v70-three-trained-origins-and-sala-hold.json)、[v70選定overlay](../../catalog/revisions/v70-2026-11-25.json)、[全208停止](../../catalog/readiness/v70-2026-11-25-r161-all208-gates.json)を区分して保存する。**`queues/approved.json` は空のまま**、モデルコード実行・重み取得・Owner媒体削除0。

## 2. 独立学習結果／量子化版の違い

**MiniCPM5-1B Final**はBase及びSFTとLFS SHA256が異なる（一次Publisher正本の異なる重み）。1B Finalと既存2B Finalはモデル規模と学習済み結果が異なる。モデルカードの「1Bクラス強力」「RL＋OPDで平均約16ポイント改善」は出版社自己報告であり、既存のQwen0.8B、LFM2.5-1.2B、MiniCPM5-2Bとユーザー実機で比較した証拠ではない。限られた容量で使用可能な独立stateを優先する。1B Base/SFTは研究メタデータを固定するが、本版では正式追加しない。

**DSpark**は、公式モデルカードが約**1,959,525系列、7,054,154,509 training tokens、6epoch、CE＋L1＋confidence loss**の学習レシピを公開した独立学習済みspeculative draft。5層、target hidden-stateレイヤー`[1,10,20,30,39]`、1検証ブロック7トークン。作者報告のtemperature 0 **acceptance length平均5.5174**は、1回の推測検証あたり採択した長さの指標であって**5.5倍のtoken/secではない**。公開されたDSpark-GGUFは基本的に異なる配布形式の候補であり、追加学習が独立している証拠がないので別モデル登録しない。Parentの学習時具体revはモデルカードで公開されておらず、既存2B Finalの固定SHAがその学習版と完全一致すると主張しない。

**SALA**は、別系統のTransformer-to-hybrid継続学習で作られた9B級で、MiniCPM5 1B/2Bの量子化ではない。作者は**NVIDIA A6000D、256K入力、Qwen3-8B比較で最大3.5倍**を掲げるが、GPUクロック、精度、バッチ、長文KV、コンパイラ等の実測全条件が今回揃っていない。ソースには`configuration_minicpm_sala.py`、`modeling_minicpm_sala.py`が付属し、独自Attention kernelのコンパイルと安全審査が必須。作者推論例は**`trust_remote_code=True`**。推論コードの参照は`OpenBMB/sglang` `minicpm_sala` branch の観測コミット `d29fb130c7fc797902d113027ca68860e1a54d41`を記録したが、このSHAだけでDocker/PyTorch/CUDA 12+/infllmv2などの完全動作を証明できない。

## 3. 保存容量の推定とDSpark親の取り扱い

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| \(B_1\) | 1B FinalのPublisher原本参照容量 | byte | 11ファイルの和 | 非負整数、所有者増分ではない | 整数スカラー |
| \(B_D\) | DSpark原本参照容量 | byte | 4ファイルの和 | 非負整数、親を含まない | 整数スカラー |
| \(B_S\) | SALA原本参照容量 | byte | 15ファイルの和 | 非負整数、外部CUDAコード除外 | 整数スカラー |
| \(B_P\) | 既存選定MiniCPM5-2B Final親のPublisher原本容量 | byte | 11ファイルの和 | 5,043,807,977、取得台帳116では未確認 | 整数スカラー |
| \(B_T\) | 上記新3repo合計のPublisher参照容量 | byte | \(B_1+B_D+B_S\) | ステージング・重複排除前 | 整数スカラー |
| \(B_{PD}\) | 実行可能な推測デコーディング親子参照容量 | byte | \(B_P+B_D\) | 親が実保存できる場合のみ | 整数スカラー |

\[
B_T=2,171,355,218+647,565,508+18,959,519,287
=21,778,440,013\ \mathrm{byte}.
\]

\[
B_{PD}=5,043,807,977+647,565,508
=5,691,373,485\ \mathrm{byte}.
\]

**次元検査**：byte＋byte＝byte、双方とも十進単位を用いる。**重要**：親MiniCPM5-2B Finalがカタログに存在することと、所有者HDDに推論可能な状態で存在することは別。Parentの署名済みmanifestとOwner物理SHA・容量実測が無いまま、DSparkの647MBだけをダウンロードREADYとしない。

## 4. 法令と権利の判断：事実と予測を区別

モデルカードはOpenBMB各モデルを**Apache-2.0**と記載し、[公式コードLICENSE](https://github.com/OpenBMB/MiniCPM/blob/f4293a1a7bde05d1acce99488235792615fc241b/LICENSE)を参照する。HF個別リポジトリには必ずしも独立LICENSEファイルがないため、モデル重みの公表許諾とコード、学習データ及び第三者の権利を別々に確認する。**PublisherがApacheタグを付したことは、個々の所有者の全目的での利用・再配布を私が許可したことを意味しない**。

[米BISの2026-11-19最終的な暫定規則91 FR 74970](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion Rule由来の**ECCN 4E091モデル重量管理を撤回**した。高度計算機半導体、特定の仕向け／用途、サービス提供、モデル固有ライセンス等は引き続き別の審査がある。**一律のオープンウェイト所持禁止が迫っている**との確証はない。将来の供給元削除・アクセス変更・利用条件変更は保存のストレスシナリオに留め、危険率は測定不能として記録する。

## 5. 実行停止の具体的な必要条件

- Owner Windows D等の実体を読取専用で再SHA（発行者SHAとGit blob OIDの区別を保持）。現物容量・staging・cacheを含め4TB上限、**最低200GB空き**を確かめる
- 指定した本人利用行為（ローカル実行、改変、二次配布、商用提供等）ごとにLICENSE／NOTICE・親の契約条件を確認する。Gatedなら正規の権限が必要
- Native backend/driver/CUDA/ABIを固定する。1BはTransformers 5.6+とSGLang 0.5.12+等のPublisher例、DSparkはDSPARK mode、SALAはcustom Pythonとfork/extensionを静的監査。**未審査のモデルコードを実行しない**
- 実推論で、context、GPU型・クロック・CPU/OS、バッチ、KV dtype、量子化scale/zero-point、依存のGPU/ホストRAMピークを揃え、少なくとも**同条件30回**の速度・RAM試験と**100以上の固定課題**で新しいモデルの増分価値を判定する
- 上記実測・明示された**ファイル別ユーザー取得承認**が未完了なら`queues/approved.json`を変更せずモデルペイロード転送しない

## 6. 反証可能なH／T／D／C／UとERROR CHECK

**H（仮説）**：1B独立後学習原本＋323.8Mの専用学習済みDrafterは約2.819GBの公開元sourceで、既存の2B Finalとは異なる学習能力を保存する。SALAはより希少な技術だが、custom実行依存を未解決のまま取得対象へ昇格させない。

**T（検証）**：公開元40桁revで3repo・30ファイル、Git blob OID、LFS SHA-256参照7件、合計21,778,440,013byteを再照合。v68旧252件の完全一致、v70登録258／有効208、116取得報告のID重複なし、active208件のreadiness／worklist／preparation、conditional152件のaccessが同集合、承認0を回帰テストする。オーナーの品質/HW反復は別工程。

**D（合否）**：Publisherの静的原本・決定・各台帳集合一致かつ全208件STOPは**PASS**。外部コード実行、Gated迂回、同一GGUFを別学習結果と数える、親未取得を無視してDSpark READYとする、自動承認は**FAIL**。Owner媒体・実性能・ライセンス・将来の規制確率は**UNCERTAIN**。

**C（反証）**：1Bが既存コンパクトモデルより用途性能で劣る、DSparkによって小バッチのレイテンシが悪化する、SALA CUDA forkがOwner OSで利用できない、適用ライセンスやデータ権利が対象行為を禁止する。

**U（不確かさ）**：Publisher自己報告のbench及びtraining、Owner HW/clock/VRAM/CPU/SSD/OS、本人許諾、local SHA／依存closureが未検証。繰り返し測定とサンプル分布がないため合成標準不確かさ\(u_c\)と包含係数\(k\)を数値化しない。

**ERROR CHECK**：旧255資産を完全保持して新規CONDITIONAL2＋HOLD1、v70 **258登録・208有効／SELECT56・CONDITIONAL152・HOLD31**。全205取得STOP／`queues/approved.json`空／新規モデル重みDL0／Owner D独立SHA0／customモデルコード実行0／既存ファイル削除0。

学際的関連：①LLM後学習とspeculative decoding、②CUDA/long-context GPUエンジニアリング、③暗号学的原本保存とソフトウェア供給網、④AIライセンスと輸出管理、⑤不確かさ評価と再現性ベンチマーク。

### 7.〈次に考える問い〉

**小型モデルをさらに1つ加える場合、独立した学習結果の幅を増やすことと、既存モデルに専用Drafterを付加して実用推論速度を改善することのどちらを先にするべきか。** 原本保存価値と実測アクセラレーション効果を別々に計測して判断する。
