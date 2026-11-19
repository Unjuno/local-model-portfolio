# R126｜v53：Microsoft Aion 2.3B原本追加と既存61件との重複排除（2026-11-20）

## 1.〈本論〉目的と今回の確定

2026-11-19のv52（205登録／158有効）を起点に、Microsoft Windows Applied Sciences Groupによる[Aion-1.0-Instruct-2.3B](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B)を**別の学習済み原本1件**として条件付き追加。v53は**206登録／159有効、SELECT53・CONDITIONAL106**。旧205レコードは1件も変更しない。新規取得のユーザーWindows D現物再ハッシュ・モデル本体DL・コード実行はこの回0件。

[Publisher固定source manifest](../../manifests/drafts/v53-2026-11-20-aion-instruct-2.3b-original-bf16.candidate.json)と[単一original queue](../../queues/proposed-v53-r126-aion-bf16-first-public-source.json)を作成。Microsoft publisher HF revision `28902cbfd9f4e0347d6c853aa1301f5d559b2fc0`、非Gated、LICENSE原文はMIT、11ファイル **4,593,276,272 byte**、うちBF16 `model.safetensors` **4,577,698,688 byte**、Publisher LFS SHA256 **`6c779881b539d9074f356964ad3089459e9e837da7649d6f271859135256984e`**。元ソースのコードとtokenizer、config/chat templateも保存対象。非必須広告画像834,462byteは除外。派生ONNX/INT4などは独立学習済み結果として加えない。

**モデル固有の独立価値**：原本configで28 decoder層、sliding attention 21層（window2048）、full attention 7層（RoPE/YaRN）、32,768 token、語彙200,029、タイドembedding、HF公称2.2888B総params。日本語を含む8言語。32K/2.3B級のWindows公式SLMの公開ソースを、将来OS統合パッケージから独立に保全できる。Microsoftの[公式Windows計画（2026-11-13）](https://devblogs.microsoft.com/foundry-on-windows/aion-instruct-local-ai-windows-gpu/)ではAion導入・今後のコンテンツモデレーション組合せと2027年1月OS展開予定を公表しているが、**現在の公開checkpointが将来撤回されるという発表はない**。モデルカードの作者によるMMLU 55.15やIFEval 83.90は同一HW・clock・batchの比較実測値ではないためポートフォリオの相対性能優位とは断定しない。

MITライセンスは公開版モデルの源LICENSEから確認した。custom code `configuration_aion_instruct.py` / `modeling_aion_instruct.py` は `trust_remote_code=True` が必要で、アーカイブ手順では**自動実行しない**。完全オフライン復元・配布行為別の法的条件・Windows GPU backend／Torch ABIは未確認。

## 2. 過去61モデル取得報告を踏まえた実転送差分

[GitHub実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)の最新版は、**62対象中61 VERIFIED報告、708ファイル、409,835,119,252 byte**。これは過去の取得器がSHA照合を報告した値であり、今回所有者Dディスクを直接同定し再ハッシュしたものではない。2026-11-19の実行時の最小空きは2,445,946,363,904 byteと記録されているが、本人の今のDドライブ残量に代用しない。

[R125 15sourceの最新差分キュー](../../queues/proposed-v52-r125-ledger61-delta-next15.json)は、R122元ソース374,701,109,177 byteから同じrevision/publisher SHAで報告済みのRWKV・iLLaDA・TRELLIS学習済み重み**47,152,036,163 byte**を次回再取得対象から外し、補助コード等だけを追加する。改訂sourceは15 repo、287ファイル、**327,549,073,014 byte**。過去重みがD上に存在するかは取得器がSHA256で独立照合する必要があり、**未発見なら補助だけで完全復元済みと扱わない**。

| 次回batch | モデルsourceと目的 | publisher source bytes | 判定 |
|---|---|---:|---|
| A | 新v53 Microsoft Aion MIT原本11ファイル | 4,593,276,272 | 優先度高：小型、変更のない学習済み原本、customコード静的保存 |
| B | R125残15source、2 dataset/独立学習済みsource/コード依存 | 327,549,073,014 | v52の既登録資産へ原本を補完。既存同一SHA学習済み原本47.152GBを重複要求しない |
| **計** | **別queueで重複しない16publisher repo** | **332,142,349,286** | staged & verified transfer、既存実物と再照合 |

2026-11-19以前にVERIFIEDと報告された大容量モデル `RWKV/RWKV7-7.2B-20260805`、`GSAI-ML/iLLaDA-8B-Base`、`microsoft/TRELLIS.2-4B`のトレーニング重みは、SHA一致を前提として再取得しない。実物不明なら停止し、既存保存ルートを探索して再検証する。Dドライブの保存済み元ファイルを**絶対に無断削除・上書きしない**。

### 取得の実行仕様

[Windows取得器](../../scripts/download_r115_windows.py)はR125差分15件とR126 Aion単体の双方を検証できる。現在の正本`queues/approved.json`は空であり、**研究source選定と実行承認は別**。所有者の端末上で一括source scope/法的用途/実D空きを確認した後、`--execute`と`--approval-file`を渡す。モデルごとに対話で確認を繰り返す必要はない。未確認のGated入手・重み/モデルコード実行は禁止。

```powershell
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v53-r126-aion-bf16-first-public-source.json" --dry-run --root "D:\AI-Models"
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v53-r126-aion-bf16-first-public-source.json" --execute --approval-file "owner-approved-aion.json" --root "D:\AI-Models"
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v52-r125-ledger61-delta-next15.json" --dry-run --root "D:\AI-Models"
```

`owner-approved-aion.json`はユーザーが端末で固定source・利用条件を検査して記録した承認ファイルであり、この研究では**作成済みとは主張しない**。モデル本体実取得や`--execute`の動作はここから検証されていない。

## 3. 規制事実とシナリオ

米国BISの[2026-11-19公布の暫定最終規則（Federal Register一次資料）](https://public-inspection.federalregister.gov/2026-23529.pdf) IV.Aでは、AI Diffusion Ruleのモデル重み規制ECCN 4E091指定を**撤回**すると明記。一律に「ローカルモデルが近日全禁止される」という事実根拠にはならない。一方、提供者のGated化、ライセンス変更、削除、技術プラットフォーム依存の問題は実際に個別観察でき、保全の目的として十分合理的。保管行為、第三者への再配布、商用推論、輸出等を区別する。

## 4. 容量判定・変数表と次元

| 記号 | 日本語の意味 | 単位(SIへの対応) | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| B | Dドライブの現在の実空き | byte（8 bit） | 当該volumeの`disk_usage.free` | 0以上、今回独立未観測 | 整数スカラー |
| F | 維持すべき自由容量 | byte（8 bit） | 200,000,000,000 | 固定アーカイブ運用条件 | 整数スカラー |
| S | 新source論理量 | byte（8 bit） | R126 + R125 = 332,142,349,286 | 既存同一SHA実物の存在で変動 | 整数スカラー |
| O | キャッシュ・stage・filesystem余裕 | byte（8 bit） | backendと最大ファイルの追加書き込み次第 | 非負、現在未測定 | 整数スカラー |

単一媒体で全sourceを新規取得する安全条件：`B ≥ F + S + O`。両辺はすべてbyteなので次元一致。順次単位ファイル取得なら`S`を各段階の実欠損分へ減らして判定する。

## 5. H/T/D/C/U・ERROR CHECK

**H**：Aionの原本追加とR125再取得削減は、別モデルの学習成果数を増やしながら47.152GBの不要な重複転送を避けられる。

**T**：固定revision、publisher SHA256/Git SHA1、R125先行重み前提ファイルを正しいvolumeで検査し、静的テストに加えWindowsで少なくとも1件の実manifest SHA完了・オフライン復元・カスタムコード監査を実行。受け入れ1モデルをpilot n_min=1、逐次失敗は即停止・そのモデル保留、別の合法的sourceは継続。

**D**：出版者source scope SHAとv53 206 unique/159 activeが一致し、旧205レコードが全件一致なら**PASS_METADATA**。本人DファイルのSHA/復元がない現在は**UNCERTAIN_PHYSICAL**。Gated越え、ファイルSHA不一致、最低空き床違反なら**FAIL**。

**C**：過去61 VERIFIEDの一部は別保存先・欠損・metadata差分、AionカスタムモデルコードがWindowsのbackendに不適合、発行者が公開原本を更新する可能性。

**U**：記録であり実測値でないD空き、キャッシュ最大値、コード依存、安全性検証、ライセンス適用範囲、発行者性能評価の試験条件。反復測定値が未収集なので合成標準不確かさ`u_c`と包含係数`k`は未算出。

**学際分野**：ソフトウェア供給網（revision/ハッシュ）、機械学習システム（BF16とcustom backend）、デジタル保存（重複除外・復元性）、技術政策・法務（提供者アクセスと現在の規制）。

**ERROR CHECK**：v53登録206／有効159＝SELECT53＋CONDITIONAL106。R125差分327,549,073,014 bytesにR126 Aion4,593,276,272 bytesを追加して332,142,349,286 byte。旧205件不変更。21 Gated条件付き中本人許諾0。取得実行台帳61件VERIFIEDは未再ハッシュ。Aion量子化重複0、Gated越え0、実重みDL0。

## 6.〈次に考える問い〉

**現物ハッシュの一致が確認されたモデルの転送を繰り返すより、新たな学習済み状態と復元に不可欠な依存ファイルを優先できているか。** v53とR125/R126はこれを判定の原則とする。
