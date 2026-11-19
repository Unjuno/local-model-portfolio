# R117: v48取得報告53件を反映した、次23原本の確定調査（2026-11-19）

正本は `main`、[`catalog/CURRENT.json`](../../catalog/CURRENT.json) の **v48 201登録・154有効**。この選定は**取得承認ではない**。機械可読の全23判定：[R117 decisions](../../catalog/decisions/2026-11-19-r117-source-priority-and-dedup.json)。基準コミット：`72b72c22aacab55c374111d814463ecf897dcb71`。

## 1.〈本論〉旧R116の54件は最新取得報告と不整合

最新[実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は **53モデル、579ファイル、270,835,576,267 byte**を検証済みと**報告**。所有者の実ディスクを本調査で独立再ハッシュしておらず、offline復元や権利取得の証明ではない。

旧[59モデル発見波](../../catalog/execution/2026-11-19-discovered-next-waves.json)から、**repo ID、40桁revision、選択ファイル件数、選択source byte**の4情報が一致する **36件・109,268,329,021 byte**を重複報告として隔離。旧R116の「5件だけ除外→54件残り」は現在の53モデル取得報告に照らし**誤った古い中間結果**。修正後は **23件・1,386,933,535,900 byte**が未取得の可能性がある原本候補。

とくにR116で「次の未保存9件」としたChronos-2、SmolVLA、IBM 470M ASR、Qwen Embedding/Reranker、PaddleOCR、V-JEPA2、Boltz-2、RFD4は、**本日台帳ではすべて一致**。同じモデルを再ダウンロードせず、本人実ディスクでSHA照合・完全offline復元を優先する。source同一性と所有者の物理保存一致は別検査。

## 2. P1：原本sourceと学習済み依存の固定を先行（8件、約196.564GB）

| repo ID / 公式source | publisher source GB | 固定revision | 独自の採用理由 |
|---|---:|---|---|
| [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 55.586 | `37561816e66b…` | 無検閲派生と比較する正規親BF16。重み差の基準に必須 |
| [RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14.402 | `9e47155004fe…` | 既保管Transformerとは異なる再帰型学習済み原本 |
| [GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 16.513 | `a1b5b5f8a31a…` | 離散拡散言語モデルの独自生成機構・Base原本 |
| [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16.237 | `af44b45f2e35…` | メッシュ/PBR 3D。取得報告済みIdol Gaussian表現と非同一 |
| [PrentisAI/GroundGUI-8B](https://huggingface.co/PrentisAI/GroundGUI-8B) | 17.550 | `9db378189fdd…` | GUI要素の専門grounding。GUI agent全体とは別役割 |
| [ACE-Step/acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 19.949 | `d4a0b288b83e…` | 音楽生成原本。既保存TTS/ASRと違うモダリティ |
| [kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers) | 26.671 | `4c487e8b4aee…` | 5秒映像と音声の同期生成、静止画とは別能力 |
| [HuggingFaceBio/Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | 29.656 | `17de89165e25…` | DNA×言語の学習済み表現、既保存ESM/RFD4タンパク質系とは別用途 |

公式Qwen3.8-27Bは既報告の無検閲派生と差分を比較する親原本。他は再帰LLM・拡散LLM・3D形状・GUI grounding・音楽・動画音声同期・DNA言語という独立の学習結果を保全する。選択source file合計を実ディスク増分や動作速度と混同しない。これら8件でも完全file SHA、依存、権利正文、ユーザー承認が未確認であり**今すぐ転送可ではない**。

## 3. P2：機能差・大容量とライセンス検討（9件）

| repo ID / 公式source | publisher source GB | 固定revision | 独自性・保留理由 |
|---|---:|---|---|
| [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) | 10.681 | `5bb1f6ee58e5…` | 既保管多数TTSとの差分・水印/感情制御を比較 |
| [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | 54.744 | `299c8406a6c6…` | PC画面操作agent、GroundGUIと機能が異なるが54.7GBを要する |
| [tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | 60.143 | `64a460a94d54…` | 長期記憶専門MoE。約60GBと外部frameworkの費用確認 |
| [ibm-granite/granite-switch-4.1-30b](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | 59.991 | `eb206725d03c…` | モジュラaLoRA・音声を全構成で検査 |
| [EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | 64.477 | `04c6953977c3…` | 臨床SFTと独立医学データの権利/用途を評価 |
| [OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | 66.726 | `7b480e62a0f5…` | 独立医学VLM、臨床用途ではなく研究利用を区別 |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | 130.526 | `b5c939de8f75…` | 独立MoE高精度重みだが原本約130GBの費用を評価 |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 159.376 | `a7fbcb5c0e12…` | 80B級コード専用学習成果、source約159GBの投資対効果を比較 |
| [meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | 59.582 | `1297fd7dfeac…` | 独立視覚統合学習済み重み、既保管VLMと比較 |

## 4. P3：重複または容量効率から取得後順位（6件）

| repo ID / 公式source | publisher source GB | 固定revision | 後順位の根拠 |
|---|---:|---|---|
| [OpenMOSS-Team/MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | 16.996 | `cdd3b911b158…` | 既保管Qwen/Kitten/Zonos/VibeVoice TTSとの重複とcodec確認 |
| [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) | 62.579 | `5bbc2fb1c1b2…` | 一般汎用原本、独立専門原本を先行 |
| [allenai/Olmo-3-1125-32B](https://huggingface.co/allenai/Olmo-3-1125-32B) | 64.477 | `c2b61dae89a1…` | 別訓練系列だが原本約64GB、追加価値の証拠待ち |
| [Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | 66.257 | `df919e1e2cf0…` | 他コード/agent系との品質差未実証 |
| [Qwen/Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | 71.927 | `0f0813072d23…` | 汎用Base、公式27B親の保存を先行 |
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 241.887 | `a11f36bebf70…` | 独立119Bだが約242GB、他の高独自性原本を先行 |

P1/P2/P3は現在のv48のSELECT/CONDITIONALを取り消すのではなく、**ファイル固定・調査順**を決める。失う可能性が高いという規制確率を付けてはいない。

## 5. R115高精度マスターの3件を別扱い

[R115 GO source候補10件](../../queues/proposed-v48-r115-master-sources-16.json)のうち、現在の取得報告とID+revision+files+bytesまで一致するのは**7件**。差分のある**3件**は：

| 訓練成果 | 変更されたファイル選択 | source規模と注意 |
|---|---|---|
| [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | 先行報告0.776GBのcoreから追加codec等を含む原本範囲へ | **15.346GB** source計画。すでにcoreを取得報告しているが完全学習済みcodecの復元が未閉包 |
| [InterpreticAI/Qwen3.8-27B-Uncensored-v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | 先行GGUF Q4にない元BF16 full | **55.586GB**、正本原本の優先調査 |
| [0bserverx RVN-F16](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 先行Q4に対するF16 GGUF | **53.808GB**、元学習BF16とbit同一とは未証明 |

これらは3つの**新しい学習済みモデル**ではない。既存Q4やcoreを勝手に削除・置換せず、必要なファイル集合・hash・親ライセンスを定義する。

## 6. 新モデルの採否

**[Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash)**：2026-11-18 [発行元発表](https://huggingface.co/blog/rumble-2-flash)。45言語の小型ASR。すでに[R115の19ファイル・1,385,998,807 byte・2 LFS SHA256固定候補](../../manifests/drafts/r115-v48-rumble2-flash-and-nemotron-sigma-original.candidate.json)があり、新規CONDITIONAL登録を**推奨**する。ただし0.5086Bの主モデルに**別の学習済みCTC head**があるため、全trained parameter総数・`ctc_head.py`コード・LICENSE本文の検証までは正式v48に追加せず、取得準備STOP。H200/vLLM高バッチの作者WERは利用者環境の実測ではない。

**[sensenova/SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B)**：[2026-11-17公式発表](https://www.sensetime.com/en/news/sensenova-loop-9b-release-20261118-1435)。約9.413B、32物理層の24中間層を2周する共有重み・mHCによる独立モデル。公式Q4約4.9GBは原BF16の代わりにはならない。現在**Gated**で`trust_remote_code`が必要。**P0アクセス/権利調査・新規研究HOLD**。ARLoop-1.2Bとは独立学習だが、個人の正規Gated同意・実行ABI・完全sourceなしに取得しない。

**[nvidia/Nemotron-Labs-Sigma-distill-spec-3B](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B)**：原本sourceはR115の18ファイル。Hub`license:other`、custom codeのため権利・実装を確認するまで**研究HOLD**。

## 7. 実証していない規制予測は確定扱いしない

[米BIS 2026-11-16公式発表](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は先端半導体・データセンターへの越境リモートコンピュートの規制。[2026-11-19官報掲載予定のpublic inspection原案](https://public-inspection.federalregister.gov/2026-23529.pdf)は旧AI Diffusion RuleのECCN 4E091の撤廃を明記するが、発効日は正式官報で別途確認する。これは**公開ウェイトすべての個人保管が禁止**という主張とは異なる。Gated化・LICENSE変更・配布中止の可能性はストレスケースであり、無根拠なモデル別発生確率を与えない。Exaは2026-11-19にHTTP402利用枠超過となり、Exa網羅調査を完了とはしない。

## 8. H/T/D/C/U・変数・単位・ERROR CHECK

| 変数 | 日本語の意味 | 単位(SI) | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `N_d` | 元発見波件数 | 1（無次元） | 59 | 自分の59件固定台帳 | 整数スカラー |
| `N_o` | 取得報告と3属性一致した数 | 1（無次元） | 36 | ID・revision・files・bytes一致 | 整数スカラー |
| `N_r` | 残候補件数 | 1（無次元） | `N_d-N_o` | 0以上 | 整数スカラー |
| `B_d` | 全発見source容量 | byte（非SI単位） | 1,496,201,864,921 | 完全オフライン総量とは限らない | 整数スカラー |
| `B_o` | 重複source容量 | byte（非SI単位） | 109,268,329,021 | 36件のsource byte | 整数スカラー |
| `B_r` | 残候補source容量 | byte（非SI単位） | `B_d-B_o` | 追加依存未計上 | 整数スカラー |
| `B_{P1}` | 8原本のsource容量 | byte（非SI単位） | 196,564,162,457 | file選択まだ未lock | 整数スカラー |
| `B_{floor}` | 必要最低空き領域 | byte（非SI単位） | 200,000,000,000 | 物理owner媒体で計測必須 | 整数スカラー |
| `P_{total}` | モデル総学習済みパラメータ数 | 1（無次元） | 全expert+learned aux | 不明は取得準備STOP | 非負整数又はnull |

**次元チェック・数値例**：`59−36=23`（モデル件数同士）。`1,496,201,864,921−109,268,329,021=1,386,933,535,900 byte`（情報量同士）。総パラメータ数とbyteを比較しない。現行v48は150B絶対除外から条件付き量子化例外へ改訂済み。150B以上を検討するには同一HW/clock/OS/backend・量子化/zero-point・context/batch・ワークロードで固定150B未満原本との最低30反復、候補完全ピークRAMが参照以下かつ512GB未満、品質・速度・正規利用許諾・承認済みmanifestが必要。今回の例外承認0件。

**H**：重複36の再取得防止と、P1 8原本のsource閉包により保存容量当たりの独立能力が増える。
**T**：発見59と報告53のID/固定revision/files/bytes全件を静的照合。次に原本の全SHA、codec/encoder、Ownerディスク、30代表タスクの実機評価を行う（この回未実施）。
**D**：`PASS_METADATA`=36一致、23残、P1/P2/P3=8/9/6、R115 GO=7既報告一致+3別ファイル集合。`FAIL`=未確認学習総数、Gated無許可、誤SHA、容量不足のまま取得。`UNCERTAIN`=外部依存、利用許諾、本人HDD、offline復元、性能。
**C**：P1が他の原本で完全に代替できる、またはP2に実測で独自機能が確認できる場合、順位修正。
**U**：最大誤差要因は出版社sourceの論理量と物理増分、完全依存・license、ユーザーHW/ABI、自己報告ledger。反復データの誤差分布が無いため合成標準不確かさ`u_c`と包含係数`k`は算定不能。

**学際的転用**：MLアーキテクチャ（基盤/派生/量子化の区別）、デジタルアーカイブ（ハッシュと復元）、情報法（Gated/License）、ストレージ工学（ディスク空きと運用RAM）。**ERROR CHECK**：v48登録201/有効154、取得報告53/579、全件重複再照合36、残23、原本8+9+6、マスター差分3、承認キュー0、実ダウンロード0、既存ファイル削除0。Python CI、本人HDD SHA、バックエンド実行試験は未実行でPASSと主張しない。

## 9.〈次に考える問い〉

同じ約200GBを無検閲系の原本高精度・専用Codec閉包に充てる場合と、まだ無い独立アーキテクチャ8種の原本に使う場合、合法的な再取得不可能性・比較に必要な親重み・本体SHA検証の3条件を揃えた後、どちらが失われる研究選択肢を減らすか。
