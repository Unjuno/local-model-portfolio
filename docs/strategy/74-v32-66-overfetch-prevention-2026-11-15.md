# R74｜4TB保存枠の全リポジトリ誤取得防止：66資産・1,425ファイル明示スコープ

基準：2026-11-15、`main`、v32（182管理／135有効）。新規選定なし、重み取得なし、許諾への同意なし、approvedキュー変更なし。

**成果物**：[66配布元の完全な選択ファイル名・byte・公開元ハッシュ種別・固定revision](../../manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)。データは[v27原本](../../catalog/capacity/2026-11-07/v27/selected-file-capacity.json)の**実ファイル行**から抽出。[全135資産のR73証拠台帳](../../catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json)と整合。候補ファイル一覧は最終取得の許可ではない。

## 1.〈本論〉— 既存ポートフォリオの最重要容量リスク

126資産の元の公開元scopeを、厳密なファイル選択scopeと比較したところ、**66資産で配布元観測範囲が必要なファイル選択より大きい**。この66資産を無条件に`snapshot_download`や`hf download`のrepo全体モードで取得すると、意図していない形式・量子化・旧checkpoint・巨大データまで取得するおそれがある。

| 測度（元v27） | 正確な値 |
| --- | ---: |
| 126資産の公開元観測scopeを単純合計 | 6,399,135,485,511 byte |
| 126資産の選択ファイル範囲を単純合計 | 3,413,612,735,064 byte |
| **不要な観測scope差分の単純合計** | **2,985,522,750,447 byte** |
| repo全体と選択ファイルが一致しない資産 | **66件** |
| R74に明示収録した選択ファイル | **1,425ファイル** |
| 1,425ファイルのうち公開元payload SHAが未確定 | **80ファイル** |

大きい差分は複数形式・複数学習段階・別データを配布しているためであり、そのまま重みの性能差や追加学習成果を表すわけではない。

### 誤取得が非常に高額となる具体例

| 配布元 | 観測repo scope | 選択ファイルscope | 選択外の差 |
|---|---:|---:|---:|
| [0bserverx Qwen3.8 ARA GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 1,645.27 GB | 16.56 GB | **1,628.71 GB** |
| [NVIDIA Cascade 2 SFT](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) | 592.92 GB | 68.40 GB | **524.52 GB** |
| [Stuubs LTX2.5 Remix](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | 195.94 GB | 21.50 GB | **174.44 GB** |
| [OpenAI gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | 195.76 GB | 65.28 GB | **130.49 GB** |
| [ChrisColeTech LTX2.5 FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | 166.92 GB | 36.47 GB | **130.45 GB** |
| [Lightricks LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | 200.85 GB | 71.12 GB | **129.73 GB** |

1番目は配布元全量が選択scopeの約**99.35倍**。4TB保管計画に対し、これだけで約1.629TBの不要な観測範囲を追加するリスクがある。ここでの「repo全量」はv27固定revisionでの観測上限であって、ユーザー端末への実転送量を測った値ではない。

## 2. 〈応用・転用例〉— ダウンロードエージェントの失敗防止

- **形式の過剰保存を禁止**：1配布元につき、独立に保存する学習成果/必要表現形式のファイル名だけを採用。歴史的v27の`profile`と`excluded_files`から、選択されたパス1,425本を完全列挙した。原本全配布repoを別の保存対象として追加しない。
- **ダウンロード開始前の非補償ゲート**：利用者本人の合法アクセス/ライセンス全文/選択revision/SHA/全学習済み依存/実HDD容量・staging/最終manifest承認が全部PASSの場合のみ、別の実行用lockへ昇格。R74自体は`executable=false`・`download_authorized=false`。
- **許可リスト以外へのフォールバック禁止**：パスの不足や元SHAが不明なときは取得STOP。便利だからと`allow_patterns=['*']`やフル`snapshot_download`へ切り替えてはならない。
- **リスクの定量化**：選択外約2.986TBは全repo範囲での**延べ差分**。複数repo間の共有・キャッシュ・既存ファイル、外部codecやruntime、実HDDの容量は含まず、実機の節約量ではない。

## 3. 完成条件・容量設計

R73で135件すべての歴史的公開元ファイルscopeを参照できるが、最終取得lockは依然として未完成。66件の明示allowlistは**過剰取得回避という一部分だけを解消**する。特にGatedモデルの公開元payload SHA未確認80ファイル、外部依存、地域・利用許諾、所有者HDD現物は未解決。

4TBは**計画上限**であり、最低実空き200GBを確保する必要がある。既存の[R64容量レビュー](64-v32-135-source-lock-readiness.md)はSHA-aware source union約3.466TBの暫定算術を保持する。すべての資産の依存・wheelhouse・stagingを足した保存可能性は実証されていない。容量の演算で権利不足を相殺してはならない。

### 変数表と次元チェック

| 変数 | 意味（日本語） | SI単位 | 定義 | 定義域/条件 | 型 |
|---|---|---|---|---|---|
| `B_r` | v27配布元観測repo範囲の延べ容量 | byte | 6,399,135,485,511 | 非負・対象126件、形式混在 | 整数スカラー |
| `B_s` | v27選択ファイル範囲の延べ容量 | byte | 3,413,612,735,064 | 非負・126件の選択済み範囲 | 整数スカラー |
| `B_x` | 取得対象から外した観測範囲の延べ容量 | byte | 2,985,522,750,447、`B_r − B_s` | 同じ126件のソースrevisionで比較 | 整数スカラー |
| `C` | 保存計画上限 | byte | 4,000,000,000,000 | 実測HDD容量ではない | 整数スカラー |
| `F` | 実空き床 | byte | 200,000,000,000 | 実HDDを測定して初めて判定 | 整数スカラー |

**次元検査**：差分`B_x`はbyte同士の引き算。パラメータ数、GPU RAM、ファイル数をこの容量差と混同しない。

**H（反証可能仮説）**：66資産で全repo取得を禁止し固定選択パスだけに限定すると、観測範囲の約2.986TBに相当する**余分な選択を計画から除外**できる。実機節約量は別途実測する。

**T（最小検証）**：126資産全数、**66対象資産の選択1,425ファイル**を完全allowlist化。全source revision SHA40文字、path traversalなし、ファイル別byte和と元primary byte合致を確認。ファイル未取得。停止条件66件処理完了または不一致発見。

**D（PASS/FAIL/UNCERTAIN）**：PASS＝66件/1,425件、差分2,985,522,750,447 byte一致、重複path0・悪性相対path0、`download_authorized=false`。FAIL＝いずれか相違。実機転送節約、権利・復元はUNCERTAIN。

**C（破れ方）**：固定ソース自体に別の必須学習済みファイルが未選択、旧選定形式が不適切、外部runtimeが追加取得、Gated許諾拒否。

**U（不確かさ）**：source observation時点差、重複、外部依存、ライセンス、実HDD。測定分布がなく合成標準不確かさ`u_c`と包含係数`k`は未算定。

**ERROR CHECK**：66 repos、1,425明示ファイル、masked80件、単純余分scope 2,985,522,750,447 byte。モデルを追加/除外しない。approvedキュー0。

## 4.〈次に考える問い〉

**本人による取得を開始する前に、個別資産が指定するファイルallowlist以外の重量ファイルを、取得エージェントが絶対に選ばないことを検証できるか。** 
