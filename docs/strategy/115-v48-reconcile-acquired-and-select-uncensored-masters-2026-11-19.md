# R115｜v48：取得済み報告22件の出所監査と無検閲2系統のマスター保存選定（2026-11-19）

**現行正本**：[`catalog/CURRENT.json`](../../catalog/CURRENT.json) v48、201登録／154有効（SELECT 53・CONDITIONAL 101）。**機械可読判断**：[R115監査台帳](../../catalog/decisions/2026-11-19-r115-post-acquisition-master-selection.json)。この回のモデル本体取得・実コード実行・承認キュー変更・既存ファイル削除は**0**。

## 1.〈本論〉実行記録の監査 — 「すべて未取得」を訂正

前回までの文書は「全モデル重量未取得」としていた。しかし、2026-11-19には[ローカル取得実行報告](114-v48-execution-acquisition-results-2026-11-19.md)と[機械可読ledger](../../catalog/execution/2026-11-19-acquisition-ledger.json)が新しく作られているため、**2026-11-19時点の履歴として「未取得0を継続」は誤り**。ただしこのR115作業では**その物理ドライブを直接マウントして再ハッシュしたわけではない**。当該報告の完全性と正当な取得許諾も、GitHub中の数字だけでは証明できない。

| 出所を明記した値 | 台帳上の結果 | 何を証明するか |
|---|---:|---|
| 取得を試みたモデル | 23 | R114 ledgerにある識別子23件 |
| **`VERIFIED`と報告** | **22** | R114報告が発行元hashとローカルファイルを比較したという自己申告。R115自身の独立現物検証ではない |
| GatedでHOLD | **1** | `orcarouter/Qwen3.8-27B-Uncensored`；本人アクセスを推定しない |
| **検証済みと報告された論理ファイル** | **227** | 159件Git blob SHA-1・68件LFS SHA-256、size-only 0件と台帳で整合 |
| **検証済みと報告されたsource容量** | **162,325,501,646 byte** | 22モデルの各`source_bytes`の和と完全一致。物理的な新規占有bytesとは限らない |
| 報告された最小空き容量 | 2,818,771,451,904 byte | 台帳のある実行環境での測定値、所有者4TB HDDだとこの回で独立同定していない |
| 正規の`queues/approved.json` | **0件** | 既存の**承認ゲートは空**。過去の取得実行と権利・承認の整合を別途監査する必要あり |

[2026-11-19統合15件キュー](../../queues/proposed-v48-r113-source-pinned-15.json)に含まれるモデルは**14件VERIFIED報告／1件Gated保留**で、14件の合計は**156,437,028,892 byte**。この15件以外の8件がさらに**5,888,472,754 byte**。**15件キューとは別の8件**：`Qwen/Qwen3.5-0.8B`, `lightonai/LightOnOCR-3-0.8B`, `openai/whisper-large-v3-turbo`, `nvidia/Kumo-Anomaly`, `gradium/phonon-31m-en`, `udgamlabs/Lilavati-Checker`, `udgamlabs/Lilavati`, `nvidia/Kumo-Relational`。個別40文字revision・byte・hash照合方法はR115 JSONに収録。

**不足する証跡**：現在の再マウントで独立に読み直した全227ファイルSHA256、論理パスと所有者ストレージvolume IDの検証、法的行為別の承認、モデルの依存を含むoffline restore試験、原本と量子化版の品質同条件評価。これらなしに「22モデルが完全なオフライン長期保存として完成」とは判定しない。

## 2. 無検閲2系統：同じ学習済み結果を重複登録せずマスターを追加する

| 保存対象の学習結果 | すでに報告された実行用ファイル | **追加の高精度マスター候補** | 判定 |
|---|---|---|---|
| **[InterpreticAI v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)**：中国語政治質問の選択的応答編集 | [GGUF Q4](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) 5ファイル約17.738GB | **BF16 32ファイル、55,586,056,799 byte**、出版社revision `84ab13688128c19d5ef10be430bc5de649b7823f`、19 publisher LFS SHA参照。MTP/vision系も含む | **マスター追加を優先提案**。Q4を自動削除しない |
| **[0bserverx RVN](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored)**：ARAによる別編集 | [GGUF Q4](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) 4ファイル約17.177GB | **`RVN-F16.gguf` 53,808,281,888 byte**、publisher SHA256 `f20c72c23a6564211c5e44af35ea1277d697c009ce8a25ab28d100447e0f155a`、同GGUF原本repoの固定revision `ab8d7bd81d03117501e4da60cccdff4c80f0eea0` | **利用可能な最も高精度の既知マスター候補**。作者の別Safetensors再構成を新規学習結果として重複計上しない |

**重要な実証の差**：[InterpreticAI v2配布者カード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)はフルBF16とMTP headを記載。一方[0bserverx Safetensors配布者カード](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored)は、13 sharded safetensorsを`RVN-F16.gguf`から再構成したと明記する。RVN-F16 GGUFを**学習直後の元BF16チェックポイント**と偽ってはならない。公開の逆変換では原BF16 bitの復元は保証されず、元の学習済みcomponentにMTP/visionもない。

**容量**：この2件のPublisher新候補source合計は**109,394,338,687 byte（約109.394GB）**。既に取得報告されているQ4の34.9GBを単純に削除・上書きしない。外部依存、キャッシュ、ステージング、filesystem overheadは別。R115は取得を新たに開始していない。

**追加を見送る近縁候補**：[InterpreticAI v3](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v3)はNousResearch/Arete-27B由来の**別の学習成果**（Hub表示27.3567B、Apacheタグ）。著者の中国語政治質問評価ではv2の3.5%に対してv3が2.6%の回答抑制率だが、同一報告内の差は約0.9ポイントにすぎずv3はMTPを保持しない。新たな55GB級保存を正当化できる未重複の汎用能力や利用者実機差は未測定。**新規CONDITIONAL登録ではなくHOLD研究**。モデル名に`uncensored`が含まれていても、あらゆる危険な依頼への無条件応答を意味しない（v2の作者評価では有害100問の95問を拒否）。

## 3. 法制リスク：事実とシナリオを分離

- **確認できる政府発表**：[米BIS 2026-11-16公式発表](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)が対象とするのは機微な高度計算インフラの国境越え遠隔アクセスであり、公開ウェイト全般の所持・配布を一律違法化したという意味ではない。
- **現行EU法**：[EU AI Act全文](https://eur-lex.europa.eu/eli/reg/2024/1689)にはGPAIモデル提供者などへの義務と適用条件が存在する。ローカルopen-weightの保管そのものの一律禁止とは同一視しない。
- **将来予測**：公開元がgated化・削除・利用条件変更する可能性は**ストレスシナリオ**。この2つの無検閲モデルがいつ禁止されるかという予測時刻や確率を捏造しない。
- **ライセンスは別の停止ゲート**：公開Git repoの`license:apache-2.0`等のタグだけで、本人の個別行為、全親依存や著作権帰属まで全て承認済みと判断しない。OrcaRouter Gatedを回避しない。

## 4.〈応用・転用例〉取得仕様の完成順

1. **再照合**：まず台帳で取得報告された22モデルについて、実保存先volume IDをユーザー側で合法的に確認し、全ファイルの実SHA256とpublisher checksum・manifest pathを照合。既存のSHA照合報告がある事実と、R115が独立に確認したことは区別。
2. **別原本の固定**：Interpretic v2 BF16の32ファイルについて既存`manifests/drafts/r113-v48-two-uncensored-original-fp16-parents.candidate.json`を使い、同repo内不要量子化や別系列の過剰取得を排除。RVN F16は単一の固定SHA付きファイル＋必要な周辺ソースだけを組にする。
3. **ライセンスとABI**：sourceのLICENSE/NOTICE、親Qwen/Arete、tokenizer/preprocessor/MTP、llama.cppまたはTransformers/vLLMのバージョン、quantization/zero-point、context/batchを固定。未信頼のコードや`.pt` pickleを自動実行しない。
4. **物理量・承認**：現物4TB媒体の実容量・空き・ステージングピークと200GB残床を照合。既存`queues/approved.json`は0件のまま、**新しいファイル固定manifestをユーザーが明示承認するまで取得しない**。

### 変数表・単位検査

| 記号 | 日本語の意味 | 単位（SI） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_I` | Interpretic v2 BF16原本の公開source合計 | byte（情報量を表す非SI単位） | 55,586,056,799 | publisher固定32ファイル、実測HDDではない | 非負整数スカラー |
| `B_R` | RVN-F16 GGUF単体の公開source | byte（非SI単位） | 53,808,281,888 | publisher固定SHA、付属必要code分を除く | 非負整数スカラー |
| `B_M` | 2つのマスター新候補の合計 | byte（非SI単位） | `B_I+B_R` | publisher source値 | 非負整数スカラー |
| `B_L` | 旧取得台帳が検証済みと報告した量 | byte（非SI単位） | 162,325,501,646 | 再監査では実ファイルを未読 | 非負整数スカラー |
| `F` | 保存後最低空き床 | byte（非SI単位） | 200,000,000,000 | staged download全期間も維持 | 非負整数スカラー |
| `S` | 追加stage/キャッシュ・ファイルシステム予備領域 | byte（非SI単位） | 未計測 | 非負整数スカラー、現物測定が必要 | 非負整数スカラー |

**容量の導出**：`B_M = B_I + B_R = 109,394,338,687 byte`。同じ情報量単位byte同士の加算で整合する。報告の`B_L`は論理ファイルの合計であり、重複排除後の新規物理占有量の証明ではない。`S`未計測なので、報告された空き容量から新規ダウンロードを自動開始しない。

## 5. H / T / D / C / U、ERROR CHECK

- **H**：Q4だけを残すよりInterpretic BF16とRVN-F16をマスター候補にすることで、将来の別量子化・移植の可能性が高い。15ソースキューの再取得より取得済み台帳の検証を先にする方が保全の失敗率を下げる。
- **T**：15キューと23モデルledgerを全IDで照合。22 VERIFIED・1 HOLDの出所を点検し、227ファイルをSHA照合方法で159/68に分解。マスターのpublisher固定32ファイル、1ファイル、SHAを静的に検査。同一実機比較が可能になった時点で、各モデル少なくとも30代表タスク、同一backend/clock/context/batch、品質・中央値・速度範囲、容量ピークを報告する。
- **D**：報告値の整合性・出典区分は**PASS_METADATA**。完全off-line復元、本人権利、ドライブ同定、Q4↔F16品質差は**UNCERTAIN**。無許可のGated回避・誤SHA・無許可取得は**FAIL**。
- **C**：元のRVN学習BF16が別に発見されれば現F16 GGUFをマスター最上位と見なさない。v3の汎用能力がv2を有意に超えた場合はHOLD見直し。過去実行の一部ファイルが欠落・破損していれば再取得計画が変わる。
- **U**：公開元メタデータ、取得実行ログの自己報告、LICENSE契約範囲、量子化誤差とruntime ABI、本人ストレージの不確かさ。実測の反復データ・誤差分布がないので合成標準不確かさ`u_c`と包含係数`k`は数値化しない。

**ERROR CHECK**：現在のv48は201登録／154有効で不変。取得実行報告は23モデル=22 VERIFIED + 1 HOLD、227ファイル=159 Git blob SHA-1 +68 LFS SHA-256、162,325,501,646 byte=156,437,028,892 byte（15計画内の14件）+5,888,472,754 byte（計画外8件）。追加マスター候補2系統は**合計109,394,338,687 byte**。無検閲新規学習資産登録0、既存削除0、承認キュー変更0、今回の本体ダウンロード0。**現行ポインタはR115へ更新するが、既存結果を自動的に取得許可へ昇格させない**。

関連分野：機械学習の量子化と重み系譜、デジタルアーカイブと内容アドレス、ソフトウェア供給網・依存復元、AI利用許諾と政府規制。

## 6.〈次に考える問い〉

過去の取得報告の内容を実HDDで独立に照合できない状況では、次の110GBの新規マスターを保存することと、既存162GBの完全オフライン復元を実証することのどちらを先に行うべきか。**答えは後者を先に検証し、前者を確定ファイル候補として保持すること。**

## 7. 追補：並行して公開されたR115 16原本source計画と安全な実行契約

現行の[機械可読source提案](../../queues/proposed-v48-r115-master-sources-16.json)は、**16原本、237論理ファイル、102 publisher LFS SHA256、301,848,275,578 byte**。そのうち**10件・132,430,668,414 byteはメタデータ上の`GO_AFTER_LOCAL_PREFLIGHT`**、**6件・169,417,607,164 byteはHOLD**。前のR113 15件／212GBは**履歴**として残る。主な差はInterpretic BF16、RVN F16、Zyphra/ZONOS3-Miniのcodecを含む原本など。**16候補はv48の新しい正式選定資産16件ではない**。

このsource提案が列挙する`GO`という表記は実行承認を意味しない。R115時点で承認キューは空であり、[Windowsスクリプト](../../scripts/download_r115_windows.py)は**通常実行・`--dry-run`とも読み取り専用PLAN**へ訂正した。新たな転送は`--execute`と明示的に承認された正確なsourceファイル集合を必要とする。[後戻り防止テスト](../../tests/test_download_r115_authorization.py)には空の承認キュー、誤revision、fingerprint mismatch、権利・所有者ボリューム未確認で実行を止める7検証例を追加（今回のGitHub編集ツールからテストは**未実行**）。過去の22件報告を新たな10件への無条件承認へ読み替えてはならない。

さらに[新規2原本source候補](../../manifests/drafts/r115-v48-rumble2-flash-and-nemotron-sigma-original.candidate.json)は**正式v48登録に追加していない**：

| 新候補 | 固定publisher sourceの規模 | 判断 |
|---|---:|---|
| [`Reson8/Rumble-2-Flash`](https://huggingface.co/Reson8/Rumble-2-Flash) | 19ファイル／1,385,998,807 byte、2 LFS SHA、40桁revision `a0c34287229103b706c670d70791683e34379732` | **次の小型ASR研究優先**。0.5B級・45言語／CTC専用headを含む独立学習済み成果。既存Whisper / Qwen3 ASRとの差を同条件で比較してから正式追加。作者のOpen ASR Leaderboard英語WER6.60%はH200/vLLMであり利用者実機性能ではない |
| [`nvidia/Nemotron-Labs-Sigma-distill-spec-3B`](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B) | 18ファイル／8,494,971,346 byte、3 LFS SHA、40桁revision `9769b2d388000e0ff61736d26359074efbf0dc9d` | **HOLD**。自己推測型continuous diffusionとAR verificationの独自学習済み二head。NVIDIA独自ライセンス、`trust_remote_code`、GPU BF16・custom backend依存のため権利・ABI・独自性が未閉包 |

発行元一次資料：[Rumble-2-Flash技術発表（2026-11-18）](https://huggingface.co/blog/rumble-2-flash)、[Sigma作者カード（2026-11-12公開）](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B)。**新候補を追加する理由は、新しい学習結果・必要componentと将来の復元に価値があるかであって、最新版やモデル名の特殊性そのものではない**。

**追補ERROR CHECK**：現行source 16=GO10+HOLD6、237ファイル、102 LFS hash、301,848,275,578 byteで各ファイルbyte和・一意IDを静的検査。現行`CURRENT.json`のsource pointerはR115を参照し、v48の201登録・154有効という正式選定は変更していない。取得の新規承認0、今回の重量ダウンロード0。
