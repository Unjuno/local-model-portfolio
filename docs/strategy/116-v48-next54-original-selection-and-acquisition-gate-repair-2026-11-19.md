# R116｜v48実取得報告の照合・次54資産の原本選定・安全な取得ゲート（2026-11-19）

## 1.〈本論〉— いま何を取得対象として確定するか

**正本**は`catalog/CURRENT.json`のv48、**201登録／154有効（SELECT53・CONDITIONAL101）**。新たな取得対象を安易に増殖させず、**既存アーカイブの現物照合→次の独立原本10件のハッシュ・権利閉包→2つの新規専門候補の個別採否**を優先する。監査機械可読本体は[こちら](../../catalog/decisions/2026-11-19-r116-next54-and-new-originals-selection.json)。新規2件の[完全Publisherファイル一覧](../../manifests/drafts/r115-v48-rumble2-flash-and-nemotron-sigma-original.candidate.json)は合計37ファイル／9,880,970,153byte、LFS SHA-256参照5件。

### 取得済み「報告」と「現物保証」の違い

[過去のAcquisition Ledger](../../catalog/execution/2026-11-19-acquisition-ledger.json)は、**23モデルのうち22モデル・227論理ファイル・162,325,501,646byteを検証済みと報告**（159 Git blob SHA-1と68 LFS SHA-256）、OrcaRouterはGated HOLDとしている。これは作業者の実行台帳であり、R116は本人Dドライブを直接マウントして独立再ハッシュしていない。元の`queues/approved.json`は依然として空で、**別途本人が許可したかどうかも本台帳からは不明**。したがって「取得報告済み」と「合法な完全offline保存完了」は厳密に分ける。

[2026-11-19に生成した次波59件](../../catalog/execution/2026-11-19-discovered-next-waves.json)をledgerと完全ID照合すると、Kumo-Anomaly、Phonon-31M、Lilavati、Lilavati-Checker、Kumo-Relationalの5件が**既にVERIFIED報告と重複**。再取得候補から外し、残り**54件・1,495,443,610,521byte**が未保存の可能性をもつ調査候補になった。これはsource-sizeの総和であり、すべてが合法・復元可能・4TBに収まると確定した数値ではない。

### 次に原本ファイルの閉包を完成させる10件

いずれも既にv48の正式有効選定に存在する。ソースrevisionと発行元側ファイル**件数・総バイト**までが次波台帳で観測済み。ただし*全ファイルのハッシュ・親権利と依存*はこの10件について最終lockされておらず、**今すぐダウンロード可という判定ではない**。

| repo ID | Publisher source GB（10進） | 学習成果と重複判断 |
|---|---:|---|
| [`autogluon/chronos-2`](https://huggingface.co/autogluon/chronos-2) | 0.478 | 時系列予測に特化した原本。LLMでは代替不可 |
| [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base) | 0.907 | 実機行動用VLA。正規化データ・行動依存を保存 |
| [`ibm-granite/granite-speech-5.0-470m-turboctc`](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) | 0.948 | 別系統の小型ASR。Whisper等との誤り比較が必要 |
| [`Qwen/Qwen3-Reranker-0.6B`](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | 1.207 | 検索候補の再ランキング用に別学習 |
| [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 1.207 | 文書・問い合わせ埋め込み。Rerankerと別重み |
| [`PaddlePaddle/PaddleOCR-VL-1.5`](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | 1.929 | 書類OCRとレイアウト。LightOnOCRと実測比較 |
| [`IFM/K2-Horizon-0.9B`](https://huggingface.co/IFM/K2-Horizon-0.9B) | 2.162 | 小規模な世界・動画モデルの原本。codec依存未閉包 |
| [`facebook/vjepa2-vitg-fpc64-384`](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384) | 4.138 | JEPA動画表現。生成動画モデルとは異なる学習成果 |
| [`boltz-community/boltz-2`](https://huggingface.co/boltz-community/boltz-2) | 4.349 | 分子構造・相互作用の科学モデル |
| [`nvidia/RFD4-Proteina`](https://huggingface.co/nvidia/RFD4-Proteina) | 5.236 | タンパク質特化原本。依存・利用条件を別検査 |

**上記10件合計 22,561,484,383byte（約22.56GB）**。これは前処理/親ウェイト/codec/学習済み追加依存や新規staging容量を含む完全オフライン復元費用ではない。優先基準は「同量子化ファミリーを何種類か保存する」より独立学習済み成果を多用途に残すこと。Qwen EmbeddingとRerankerは名前が似ていても別の学習済み機能なので保持する。一方LightOnOCR取得済み報告とPaddleOCRの重複は同条件文書ベンチで否定可能とする。

### 権利・総数が先行する4件

| repo ID | Publisher source GB（10進） | STOP理由 |
|---|---:|---|
| [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini) | 0.776 | ライセンス表示 `apache-2.0_weights;mit_code_reported`、行為別許可未監査 |
| [`nvidia/Kumo-Tabular`](https://huggingface.co/nvidia/Kumo-Tabular) | 2.438 | ライセンス表示 `openmdw-1.1`、行為別許可未監査 |
| [`maya-research/maya2-native`](https://huggingface.co/maya-research/maya2-native) | 5.021 | 学習済み総数不明 |
| [`ACE-Step/acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 19.949 | ライセンス表示 `mit_publisher_tag_and_code_mit`、行為別許可未監査 |

同じv48有効資産でも、非標準ライセンスや学習済み総数が未確認なら、順位上位の原本選択と**実転送の許可**は別にする。Maya2は学習済みcodec/ECAPA/Mimiなどの全構成が未確定で、単一model.safetensorsの推定サイズを最終化に使わない。NVIDIA OpenMDW等はHubのラベルだけで行為別許可を保証しない。

## 2. 新公開原本・Gated・無検閲の比較

| 新候補 | 2026-11-19 Publisher側の観測 | 採否 |
|---|---|---|
| [Reson8 Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 公開非Gated・Apache 2.0。メインBF16重み約1.017GB＋**別の学習済みCTC head 0.357GB**。固定revision `a0c34287229103b706c670d70791683e34379732`。全19ファイル約1.386GB | **P1 新規正式CONDITIONAL候補**。既存Whisper／Qwen3-ASRとの差分は独立評価待ち。モデル単体508,631,552パラメータとCTC headを合計した学習済み数は未閉包 |
| [NVIDIA Nemotron-Labs-Sigma-distill-spec-3B](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B) | 4,236,704,802 serialized parameter、固定source 18ファイル約8.495GB。独自continuous diffusion／self-speculative型 | **研究HOLD**。Hub license=`other`とcustom codeのため、LICENSE全文・ABI/セキュリティのゲートを外せない |
| [SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B) | 9.413B serialized、約19.361GB repo、ループ推論＋mHC。**Hub Gated=auto** | **P0 本人正規アクセス確認、HOLD**。ARLoopとは独立の学習済み重みだが、申請なしの取得不可 |
| [Apple FastFrames-S](https://huggingface.co/apple/FastFrames-S) | 約1.788GB repo。refiner／decoderが独立後学習でも外部Wan2.1が必要。LICENSE=apple-amlr | **HOLD**。親重量とライセンスの閉包が必要 |
| [LongCat-Video-Avatar-1.6](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6) | MITタグ、約77.629GB repo、原本とINT8変換版・デモ動画等を混在 | **HOLD**。必要ファイルだけ切り出し、全repo一括保存を禁止 |

**Rumble出版社の公開ベンチマーク**：2026-11-18版のOpen ASR LeaderboardをH200/vLLMで試したとする英語平均WER 6.60%、多言語平均約6.96%。70xx RTFxは*大きなバッチを充足した測定値*であり、利用者のCPU/GPU単発バッチ1や日本語ノイズ音声の保証ではない。同一HW・clock・backend/zero-point・batchと同一音声セットで30件以上の評価を行うまで、既存Whisperより常に高性能とは結論しない。

**無検閲の高精度保存**：既存の[無検閲原本系譜訂正](113-v48-uncensored-original-parent-replacement-review-2026-11-19.md)と[R115原本マスター容量比較](115-v48-regulatory-correction-and-master-selection-budget.md)を採用。Interpretic v2は元BF16原本55.586GB、0bserverx RVNは作者が公開する最古の再構成元`RVN-F16.gguf` 53.808GB（学習時BF16と断定しない）。既に取得報告された各Q4を**無許可で削除・上書きせず**、原本優先マスターへの交換を検討する。ただし、R115 master 15原本のpublisher source 286.420GBは従来compact15の212.023GBより74.397GB多い。本人HDD・4TB計画の最終容量・外部依存を再測定しない限り自動取得しない。

## 3. 作業上の重大な修正：勝手にダウンロードするコードを止めた

過去の実行スクリプト`scripts/preserve_execute.py`には、公開のsource候補JSONを入力すると**`queues/approved.json`が空でも転送が可能**で、`other`のライセンス表示を許容する欠陥があった。2026-11-19のR116作業で`main`を修正：

- 新規非dry runは、正本`queues/approved.json`の**ユーザー明示承認、完全40桁revision、正確なファイル名・bytes・出版社ハッシュの一致**、LICENSE本文と親権利の審査済み記録がなければ`HOLD_NO_EXPLICIT_APPROVED_MANIFEST`で停止。
- `other`／`openmdw-1.1`等はモデル作者のLICENSEと用途ごとの許可を個別確認しない限り自動許可しない。ファイル名が`LICENSE`であるだけで例外としない。
- 出版社SHAのない`size-only`ファイルは`VERIFIED`にならず、パスの`../`トラバーサルも拒否。正常系と意図的なハッシュ不一致を含む**12件の静的回帰テストをGitHubに追加**。

**注意：12件のテストケースは追加したが、GitHub先のPythonを実行してのPASSは本回では未検証。** この環境からGitHub rawへはDNS到達不能だった。コードの静的修正は保存したが、実機のテストPASSや実ダウンロードの自動再開を宣言しない。承認キューも依然として空。

## 4. 規制の事実と仮説

**一次政府資料**：[米BIS public inspection 文書2026-23529（2026-11-19掲載予定）](https://public-inspection.federalregister.gov/2026-23529.pdf)の第IV.A節は、AI Diffusion Ruleのモデルウェイト規制に当たるECCN 4E091を撤廃する旨を明記。一方、先端半導体と国外データセンターへの遠隔アクセスに関する別の規制が導入される。この公表準備PDFの本文には発効日がテンプレートで残っているため、正式官報の公布日・適用開始は別途確認が必要。**公開ウェイトの一律私的保管禁止が成立したという説明は誤り**。ただし配布元Gated化・契約変更・個別法域の政策は今後の別リスクであり、未確定の確率を恣意的に数値化しない。

関連分野：**機械学習**（学習済みstateと派生量子化の区別）、**ソフトウェア供給網**（不変revision、SHA、依存ABI）、**デジタル保存科学**（可逆性・内容アドレス・媒体破損）、**情報法**（行為別ライセンスと政策現状）。これらを一体として原本保全価値で選定する。

## 5. H/T/D/C/U・単位検査・ERROR CHECK

### H（反証可能な仮説）
一度取得済みと報告された22件の再転送を防ぎ、小型の学習済み異質原本10件と新ASR Rumbleを先に完全なsource/rights/hashesで固定する方が、同容量に複数の同一重み量子化を保存するより多くの独立能力を保全する。

### T（最小検証）
v48の201 IDと取得報告23 IDを連結し、次波59 IDから22検証報告済みの重複5件を除外。正式取得前には全ファイルSHAと元コード・学習済み補助部品・LICENCEを確認する。RumbleとWhisper/Qwen ASRの品質は、同一HW/clock/backend/context/batch、最低30の独立した日英音声でWER/CERとピークRAM、中央値レイテンシの両側区間を出す。事前登録閾値未設定のため品質順位はまだ**UNCERTAIN**。

### D（合否）
`PASS_METADATA`＝59-5=54、旧22の自己申告を区別、次54は正式v48選定に重複登録なし、新候補2のファイルhashとrevision固定済み。`FAIL`＝無権限のGatedアクセス、全学習済み総数未確認の最終化、未承認ダウンロード。`UNCERTAIN`＝本人ドライブの現物再計測、offline復元、実機の精度／速度、今後の規制。

### C（破れ方）
大型モデルに小型では代替できない別学習済み能力があり十分な容量・権利が判明すれば順位再考。RumbleのCTCが既存ASRと機能的に重複し日本語精度が下回る、またはライセンス・runtimeが未対応なら追加はHOLD。

### U（不確かさ）
発行元benchmarkの測定条件、モデルカード表示の総パラメータと外部head・encoder、GitHub実行台帳の自己報告、本人媒体の実HDD空き、別ライセンス、量子化のzero-point。反復実測が不足するため、合成標準不確かさ`u_c`と包含係数`k`の数値は**未算出**。

### 変数表

| 記号 | 日本語の意味 | 単位（SI） | 定義 | 定義域・範囲・前提 | 型 |
|---|---|---|---|---|---|
| `N_0` | 次波発見時の候補数 | 1（無次元） | 59 | 0以上整数、同一source snapshot | 整数スカラー |
| `N_v` | 次波中に既にVERIFIED報告がある数 | 1（無次元） | 5 | IDで完全一致した報告、物理検証ではない | 整数スカラー |
| `N_r` | 照合後の未保存候補数 | 1（無次元） | `N_0-N_v` | 0以上整数、自己申告の範囲 | 整数スカラー |
| `B_0` | 次波全sourceの公開総量 | byte（非SI単位） | 1,496,201,864,921 | 作者repo source、重複や親未差引 | 非負整数スカラー |
| `B_v` | 次波中の取得済み報告source合計 | byte（非SI単位） | 758,254,400 | source照合5件 | 非負整数スカラー |
| `B_r` | 未保存候補source総量 | byte（非SI単位） | `B_0-B_v` | 本人実HDDの新規消費bytesではない | 非負整数スカラー |
| `F_{min}` | 保存時に維持すべき最低空き | byte（非SI単位） | 200,000,000,000 | owner媒体の全転送・stageで遵守 | 非負整数スカラー |

**導出**：`N_r = 59 - 5 = 54`、`B_r = 1,496,201,864,921 - 758,254,400 = 1,495,443,610,521 byte`。件数の無次元差分、byteとbyteの差分でそれぞれ次元一致する。ただしこの`B_r`を4TB容量へ代入して全資産が復元可能と判定することは不可。外部依存・staging/FS overhead・他の選定資産と本体の重複関係が未閉包だから。

### ERROR CHECK

2026-11-19、v48は201登録／154有効（SELECT53／CONDITIONAL101）。台帳の22 VERIFIED・227 hash照合報告と1 Gated保留を維持。次波59件→54件、除外する同一ID5件=758,254,400byte。新規Rumble・Sigma両sourceを37ファイルで固定したが**正式追加0、ダウンロード0（この調査回）、既存削除0、承認済みキュー0**。ExaはHTTP402枯渇、Hugging Face Metadataと発行元一次資料、GitHub履歴でのみ更新。Pythonテストの動作実証は未実施。

## 6.〈次に考える問い〉

取得済みとの報告がある162GBをもう一度ダウンロードするより、現物を再ハッシュして完全offline復元を実証し、その結果を次の10原本・新ASRの取得条件に反映する方が保存失敗の再発を減らせるのではないか。
