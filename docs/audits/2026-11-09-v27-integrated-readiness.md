# v27（173資産）統合・権利・容量・取得準備監査 — 2026-11-09

> **非実行・取得未承認**。基準：`0ae31662bd38fe5e0ce8d7504d3f80926fbc089e`、ブランチ `strategy/2026-11-03-01-risk`。原本の `catalog/CURRENT.json`、現行v27、承認キューは変更しない。並行作業による変更を上書きせず新しい監査成果物だけ追加する。

## 1. 〈本論〉判定結果・根拠

- **173資産すべてを `asset_kind::repo_id` で一意に照合**（既存v9 132、v10–v27追加41）。モデル147、データセット26。有効126、非有効47。
- 保存価値の戦略判定：**KEEP 119 / HOLD 48 / DROP 6**。このKEEPは**取得許可でも完全再現性証明でもない**。
- 全モデル総数：PASS 125、UNVERIFIED 20、量子化例外研究のみ 2。総数未確認のうち有効7件は監査上HOLDに補正（カタログの選定値は非破壊）。
- 有効資産35件に外部学習済み依存・ソフトウェアABI・法律/再現上の課題が記録されている。完全な依存閉鎖とは判断しない。
- v27全件でライセンス本文確認済みは2、本人アクセス確認済みは0。この数値は履歴の真偽値で、第三者による最新の契約適法性監査ではない。
- 公的/事業者の規制事実と将来の公開制限シナリオは区分。個別モデルの近い将来の削除を断定せず、**Gated掲載＝本人承認済**という誤りも避ける。
- v28提案3件（`beipo-ai/NorthCUA-Mini`、`qiyuan-robot/PrimeSim`、`meta-models/Muse-Glimmer-30B`）は未採用。173件に混ぜない。

### 選定の定義

- `KEEP`：現行選定が有効で、現在のメタデータでサイズ上限を通過。特有の学習成果の可能性を優先して保存候補に残す。独立検証・取得ゲートは別。
- `HOLD`：旧hold/deferred、総パラメータ未確認、150B以上の例外未実証。**HOLDは最終ロック不可**だが自動削除ではない。
- `DROP`：v27で既に明示excludedの6件。物理ファイルの削除を意味しない。
- 同じ基盤のGGUF/FP8/BF16でも微調整済み重みが異なることがある。**特殊版を無差別排除しない**。ハッシュ・系譜・モデルの改善が同条件で測定されたときに重複統合を判断する。
- `acquisition`は全件 `BLOCKED_NO_APPROVAL`。公開リポジトリでも本人承認・ライセンス・固定ファイルSHA256の検証を省かない。

## 2. 差分一覧

| 比較 | 件数/状態 | 判定 |
|---|---:|---|
| v9→v27 同一ID照合 | 132/132 | 残存 |
| v9→v27 新規 | 41 | 追加一覧は監査JSONの `deltas` |
| 現行select | 53 | KEEP候補 |
| 現行conditional | 73 | サイズ未確証7件は監査HOLDに変更 |
| 現行hold/deferred/excluded | 28/13/6 | HOLD/HOLD/DROP |
| v28新規案 | 3 | 未採用、追加研究のみ |

## 3. 政策衝突（重大度、対応）

### P01 — BLOCKER
- **A:** v27は>=150B量子化の例外研究を認める
- **B:** v9リスク案と2026-11-08厳格審査は>=150B一律除外を用いる
- **処置:** 現行v27の例外は政策上の調査可能性のみ。2件はHOLD、同一HW/OS/driver/backend/ABI/context/batchで<150B参照モデル以下の実測ピークRAM、品質・速度、権利確認なしに承認不可。別途厳格比較を併記。
- **根拠:** `policies/limits.json`、`catalog/proposals/02-v27-selection-review-2026-11-08.json`、`catalog/proposals/01-regulation-priority.json`

### P02 — BLOCKER
- **A:** v27でconditionalの7件が総学習済みモデル構成未確認
- **B:** 未知総数は最終ロック禁止という現行policy
- **処置:** 原カタログは変更せず統合監査の取得準備判定をHOLDに補正。7件全て既知なら改めて判定。
- **根拠:** `catalog/effective-portfolio-2026-11-07-v27.json`、`catalog/proposals/02-v27-selection-review-2026-11-08.json`

### P03 — BLOCKER
- **A:** 既知選択ファイル範囲126/126
- **B:** 35件の依存/権利/ABI未解決と完全復元総容量がnull
- **処置:** source-only容量を完全アーカイブと同一視しない。依存が閉じるまで取得不能。
- **根拠:** `catalog/capacity/2026-11-07/v27/capacity-summary.json`

### P04 — BLOCKER
- **A:** 保管上限4.0TB
- **B:** 200GB空き維持と物理空き容量未実測、キャッシュ二重保持の最大ピークが4TB超過
- **処置:** 容量上限だけでPASSとしない。実機dfとcache/staging削減方式・空きフロアの両方を実測後に判断。
- **根拠:** `catalog/capacity/2026-11-07/v27/capacity-summary.json`、`policies/limits.json`

### P05 — BLOCKER
- **A:** 公開・GatedのHub一覧メタデータが存在
- **B:** 本人アクセス権・個別ライセンス・再配布用途が未確認、承認キュー空
- **処置:** 要同意／要条項確認に分類し、全件非実行。自動同意・Gated迂回は禁止。
- **根拠:** `catalog/effective-portfolio-2026-11-07-v27.json`、`queues/approved.json`

### P06 — NOT_ADOPTED
- **A:** v28新規3モデルが条件付きで提案された
- **B:** CURRENTはv27のまま、3件の追加145GBは既知ソース分のみ
- **処置:** 173件カタログへ勝手に挿入しない。PrimeSimの全学習済み総数、全3件の依存・権利・実機容量確認後に別版で審査。
- **根拠:** `catalog/proposals/03-v28-original-models-2026-11-08.json`、`catalog/research/2026-11-08-r33/pinned-file-capacity-and-dependency-audit.json`

### P07 — REVIEW
- **A:** 通常の量子化・微調整版と原重みが共通基盤を持つ
- **B:** 重みファイルの共有・本当に独立の訓練結果・同品質という証拠は未完備
- **処置:** 同一学習成果の別量子化だけなら代表形へ集約。ただし独自NSFW、distill、調整学習成果を無差別DROPしない。厳密な同一性・用途差と追加容量を実測。
- **根拠:** `catalog/effective-portfolio-2026-11-07-v27.json`、`catalog/proposals/02-v27-selection-review-2026-11-08.json`


## 4. 未確認モデル・学習済み依存・権利

**未確認総数20件の全ID**（有効7件を含む）：
- `InstantX/InstantID` — v27=hold、監査=HOLD。依存未解決=0件。単一参照画像からID保持生成を行う独自アダプタ/制御ネットワークを研究用に保全する。
- `Plachta/Seed-VC` — v27=hold、監査=HOLD。依存未解決=0件。TTSとは別の音声変換方式を保全し、声質再現・音声編集を比較できるようにする。
- `SWivid/F5-TTS` — v27=hold、監査=HOLD。依存未解決=0件。フローマッチング型TTSの原本と音声コーデックの比較を可能にする。
- `ByteDance/InfiniteYou` — v27=deferred、監査=HOLD。依存未解決=0件。FLUX系の人物パーソナライズ適応重みを保全する。
- `coqui/XTTS-v2` — v27=hold、監査=HOLD。依存未解決=0件。比較原本として多言語声質複製・音声スタイル移行を保全する。
- `fishaudio/fish-speech-1.5` — v27=deferred、監査=HOLD。依存未解決=0件。DualAR音声合成系統の旧世代原本を保存し、S2-Proとの発展比較を可能にする。
- `onnx-community/higgs-audio-v3-tts-4b` — v27=hold、監査=HOLD。依存未解決=0件。音声会話、感情・間・効果音の制御に関するONNX配布形態の保存価値を調査する。
- `TencentARC/PhotoMaker` — v27=deferred、監査=HOLD。依存未解決=0件。人物の一貫性を保つ写真・画像生成アダプタを比較基準として保全する。
- `bytedance-research/Lance` — v27=hold、監査=HOLD。依存未解決=0件。約3Bで画像/動画の理解・生成・編集を統合した独特のマルチタスク研究モデル。複数機能を小容量にまとめた学習レシピと原本の保存価値が高い。
- `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8` — v27=conditional、監査=HOLD。依存未解決=1件。現行LTX2.5の成人向けLoRA/蒸留/参照保持マージ。モデル固有の編集後学習成果を保全する研究候補であり、通常の2.5単純量子化と別。作者は動画・音声付属パーツを公表。
- `Stuubs/Stubelius_Remix_Ltx2.5` — v27=conditional、監査=HOLD。依存未解決=1件。LTX2.5にOmniNFT RL改善マージ・蒸留LoRAを統合した独自の動画音声派生。作者によるblind AI-judge A/Bではv1がbeta2に29勝9敗10分、Q4 GGUFやint8等が公開。
- `OnomaAIResearch/Illustrious-XL-v1.1` — v27=hold、監査=HOLD。依存未解決=0件。画像生成の独立したアニメ・イラスト特化微調整系統の原本を比較用に保全する。
- `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` — v27=hold、監査=HOLD。依存未解決=0件。医学論文の画像とテキストを結びつけた表現学習系統を保全する。
- `ACERobotics/Puffin-World` — v27=hold、監査=HOLD。依存未解決=0件。画像から重力・深度・見た目を統合した3D世界状態を推論・生成する独自世界モデル。RGB動画生成器だけでは同じ幾何表現を復元できない。
- `WhissleAI/steer-tts` — v27=conditional、監査=HOLD。依存未解決=1件。12種類の音響属性を数値指定する独立機序。既存QwenTTSの自然言語VoiceDesignや一般TTSとは異なる制御研究を小容量で保全する。
- `maya-research/maya2-native` — v27=conditional、監査=HOLD。依存未解決=2件。11インド諸語と英語の音声合成・言語間声条件付けの独立checkpoint。既存TTSで当該言語品質が同等と未確認で、少数言語と生成手順の比較用に保全。
- `Louis0324/StyleStream` — v27=hold、監査=HOLD。依存未解決=0件。声質・accent・感情を音声から変換する公開機序を研究記録に追加。作者が悪用対策でencoderを非公開にした一次事例を保全する。
- `fishaudio/drama-3` — v27=conditional、監査=HOLD。依存未解決=1件。複数話者・音声生成の継続編集とCodebook-MTPの独自学習成果を保全する。INT4の省容量だけを優先せず公開元のFP8 experts＋BF16原本を1系統選ぶ。親の元学習BF16が全部公開されているとは主張しない。
- `ausboss/Qwen-Image-2.1-Consistency-LoRA` — v27=conditional、監査=HOLD。依存未解決=1件。step1500のrank32学習差分は再現困難な編集対から得た独立成果で、小さい増分で画像編集の幾何一貫性を保全できる。早期規制対象とは断定せず、広い保険の補完として採用。
- `PrunaAI/P-H3-Image` — v27=conditional、監査=HOLD。依存未解決=4件。MiniMax H3動画原本から追加のDMD 8-step画像拡散蒸留、32B→4Bテキストエンコーダ蒸留、単一画像用の新decoder、Qwen3.5-9Bベースの学習済みprompt upsamplerを持つ別学習成果。単なる再量子化でなく、他の画像モデルやH3原重みだけでこの差分は容易に再構築できない。保険の独自

**特に追加した一次資料に基づく確認事項**：
- `WhissleAI/steer-tts`：製作者は音響9.59M、Vocos13.53M、追加refiner17.64M、cloning向けWavLM約101M、自由文向けMiniLM約22.7Mと公表。**モード別に外部学習済み依存が変わる**ため、単に9.59Mや40.8Mを完全総数として確定してはいけない。CC BY-NCと追加利用規約を確認。出典：https://huggingface.co/WhissleAI/steer-tts
- `maya-research/maya2-native`：本体2.50Bの製作者表記、MimiとECAPAが外部で必要。全パイプラインの総数とファイル・契約を未確定として維持。出典：https://huggingface.co/maya-research/maya2-native
- `fishaudio/drama-3`：製作者による約35B/36B表記差、audio codebook decoder等がある。総学習済み依存の確証なし。出典：https://huggingface.co/fishaudio/drama-3
- `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`：改変済みtransformer・Gemma4 12B int8 text encoder・audio/video VAEsを別ファイルとして挙げる。完全な合算・権利未確証。出典：https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8
- `Stuubs/Stubelius_Remix_Ltx2.5`：bf16/int8/NVFP4/GGUFは同じ派生の複数表現を含むが、独立のチューニング成果を持つ。音声/動画VAE・Gemma encoderが別途必要。出典：https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5
- `ausboss/Qwen-Image-2.1-Consistency-LoRA`：rank32の編集一貫性LoRAでQwen Image 2.1本体に依存。Adapter本体だけの数は全パイプライン総数ではない。ベースのQwen Research Licenseが適用と記載。出典：https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA
- `PrunaAI/P-H3-Image`：MiniMax H3 Community LicenseはEU・英国・韓国・米国を原則対象地域外とする規定。個々の派生モデルと利用地域の適用を別途確認。出典：https://huggingface.co/PrunaAI/P-H3-Image/blob/main/LICENSE
- **Gated本人アクセス未確認**：Hugging Face公式仕様では権限は個人に付与され、配布者は撤回可能。出典：https://huggingface.co/docs/hub/models-gated

35件の依存・法的ブロッカーはJSONの各資産の `dependencies.open_issues` に原文粒度で記録。126件全体の完全な復元権利・runtime ABIは未証明。

## 5. 容量と取得ピーク（10進バイト）

| 変数 | 意味（SI単位） | 定義域/型/前提 |
|---|---|---|
| `C_src` | 既知ソースファイルの論理的重複排除合計（B） | 非負整数/スカラー、実機に存在するとは限らない |
| `C_peak` | 一時ファイル・キャッシュを含む追加ピーク容量（B） | 非負整数/スカラー、採用方式依存 |
| `C_env` | 未計測の実行環境・復元用資産（B） | 未知の非負整数/スカラー |
| `F_real` | 開始時の**実測**空き容量（B） | 現時点で不明、非負整数/スカラー |
| `F_floor` | 作業後の最低空き容量（B） | 200,000,000,000B/スカラー |
| `C_cap` | archive計画上限（B） | 4,000,000,000,000B/スカラー |

**条件付き判定式：** `F_real - C_peak - C_env >= F_floor`、かつ最終アーカイブ容量が `C_cap` 以下。すべてバイト差なので次元整合。測れない量をゼロにしてPASSにしない。

| 条件 | 既知部分の増分ピーク（B） | 必要開始空きの**理論的下限**（+200GB）（B） |
|---|---:|---:|
| 直接最終ディレクトリ・キャッシュ非保持 | 3,417,685,712,585 | 3,617,685,712,585 |
| 最大選択ファイル1個分のコピーを追加 | 3,473,628,641,758 | 3,673,628,641,758 |
| 全量キャッシュ保持＋最終＋1ファイル | 6,891,314,354,343 | 7,091,314,354,343 |

既知source-only重複排除量：**3,417,685,712,585B**。選択ファイル元の合計 3,413,612,735,064B、報告依存追加 7,472,641,032B。これらは重複があるため安易に足し合わせない。v28候補3件を別枠で追加する仮定だと、ソースのみ **3,562,689,773,949B**。完全復元・物理空き容量・最大実機取得ピークは**未確定**。

実機計測不可：現在接続済みのDesktop Commander機器がない。物理容量・空き・ファイルシステム・ローカルキャッシュを**実測したと主張しない**。

## 6. Gated・契約・本人承認、試験

全件未承認。資産別 `rights.access_class` は**公開掲載情報に基づく予備区分**であって法的許諾確定ではない。取得不可と未許諾を混同しない。詳細はJSON参照。承認キューは0件のまま。固定revision候補は2件のみ最終ピン済と記録されているが、完全ファイルSHA256・実機ハッシュなしに承認不可。

非実行マニフェスト `catalog/preparation/2026-11-09-v27-manifest-readiness.json` に126件のsource byte・revision候補・停止条件・未実施の小規模試験仕様を記録。SHA-256のないGit blob SHA-1を代用しない。ライセンス同意・権限・取得・インストール・モデル実行は行わない。

## 7. 173件統合監査表

**注**：パラメータ総数 `UNKNOWN`／依存未解決＝取得HOLD。掲載容量は原配布元の**選択済みソースファイル総量**であって、実際のディスク使用量・追加容量ではない。CSV/JSONに個別根拠、アクセス状態、推定重複群、ブロッカーを全件収録。

| # | repo_id | v27 | 判断 | 総パラメータゲート | 依存課題数 | 選択ソースB | v9照合 |
|---:|---|---|---|---|---:|---:|---|
| 1 | `orcarouter/Qwen3.8-27B-Uncensored` | conditional | **KEEP** | PASS | 0 | 55,586,066,230 | v9 |
| 2 | `InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF` | conditional | **KEEP** | PASS | 0 | 17,738,327,225 | ADDED |
| 3 | `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | conditional | **KEEP** | PASS | 0 | 16,560,392,734 | ADDED |
| 4 | `afdudley/Qwen3.8-27B-abliterated-NVFP4` | hold | **HOLD** | PASS | 0 | UNKNOWN | ADDED |
| 5 | `orcarouter/Qwen3.8-Flash-Next-Uncensored` | hold | **HOLD** | EXCEPTION HOLD | 0 | UNKNOWN | v9 |
| 6 | `dphn/Dolphin3.0-Llama3.1-8B` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 7 | `knoveleng/Qwen3.5-9B-Uncensored` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 8 | `Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2` | conditional | **KEEP** | PASS | 0 | 53,120,711,400 | ADDED |
| 9 | `LiquidAI/LFM2.5-24B-A2B` | conditional | **KEEP** | PASS | 0 | 47,962,796,250 | v9 |
| 10 | `usezn/Galvanize-3` | select | **KEEP** | PASS | 0 | 597,573,024 | ADDED |
| 11 | `opus-research/opus-moderation-4-neo` | hold | **HOLD** | PASS | 0 | UNKNOWN | ADDED |
| 12 | `microsoft/Fara1.5-27B` | select | **KEEP** | PASS | 0 | 54,743,814,229 | v9 |
| 13 | `Qwen/Qwen3-Coder-Next` | select | **KEEP** | PASS | 0 | 159,376,351,965 | v9 |
| 14 | `tencent/Hy-Memory-30B-A3B` | select | **KEEP** | PASS | 0 | 60,143,172,163 | v9 |
| 15 | `LiquidAI/LFM3-1.7B` | conditional | **KEEP** | PASS | 0 | 3,475,686,813 | ADDED |
| 16 | `InstantX/InstantID` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 17 | `KlingTeam/LivePortrait` | select | **KEEP** | PASS | 0 | 658,957,150 | v9 |
| 18 | `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1` | conditional | **KEEP** | PASS | 0 | 671,173,375 | ADDED |
| 19 | `microsoft/VibeVoice-1.5B` | select | **KEEP** | PASS | 1 | 5,408,337,065 | v9 |
| 20 | `OpenMOSS-Team/MOSS-TTS-v1.5` | select | **KEEP** | PASS | 1 | 16,995,761,910 | v9 |
| 21 | `Plachta/Seed-VC` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 22 | `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` | select | **KEEP** | PASS | 0 | 2,498,388,392 | v9 |
| 23 | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | select | **KEEP** | PASS | 0 | 4,544,229,700 | v9 |
| 24 | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | select | **KEEP** | PASS | 0 | 4,520,163,832 | v9 |
| 25 | `ResembleAI/chatterbox` | select | **KEEP** | PASS | 1 | 3,209,057,119 | v9 |
| 26 | `Edge0/Audio8-TTS-Realistic-Air` | conditional | **KEEP** | PASS | 0 | 2,565,494,726 | ADDED |
| 27 | `SWivid/F5-TTS` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 28 | `ByteDance/InfiniteYou` | deferred | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 29 | `coqui/XTTS-v2` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 30 | `fishaudio/fish-speech-1.5` | deferred | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 31 | `fishaudio/s2-pro` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 32 | `onnx-community/higgs-audio-v3-tts-4b` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 33 | `TencentARC/PhotoMaker` | deferred | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 34 | `black-forest-labs/flux-3-image-klein-base` | conditional | **KEEP** | PASS | 1 | 20,300,554,474 | v9 |
| 35 | `black-forest-labs/FLUX.2-dev` | conditional | **KEEP** | PASS | 0 | 112,823,045,100 | v9 |
| 36 | `briaai/Fibo-2.0-dev` | conditional | **KEEP** | PASS | 1 | 25,479,156,514 | v9 |
| 37 | `ideogram-ai/ideogram-4-nf4` | conditional | **KEEP** | PASS | 0 | 16,106,834,204 | v9 |
| 38 | `black-forest-labs/flux-3-image-klein` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 39 | `black-forest-labs/FLUX.2-klein-9B` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 40 | `briaai/Fibo-2.0-edit-turbo` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 41 | `bytedance-research/Lance` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 42 | `Lightricks/LTX-2.5` | conditional | **KEEP** | PASS | 1 | 71,118,789,776 | ADDED |
| 43 | `Lightricks/LTX-2.3` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 44 | `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8` | conditional | **HOLD** | UNKNOWN | 1 | 36,468,384,300 | ADDED |
| 45 | `Stuubs/Stubelius_Remix_Ltx2.5` | conditional | **HOLD** | UNKNOWN | 1 | 21,504,132,027 | ADDED |
| 46 | `OnomaAIResearch/Illustrious-XL-v1.1` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 47 | `kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers` | conditional | **KEEP** | PASS | 0 | 26,670,725,000 | ADDED |
| 48 | `Qwen/Qwen-Image-2.1` | conditional | **KEEP** | PASS | 0 | 33,131,616,412 | v9 |
| 49 | `Tongyi-MAI/Z-Image-Turbo` | select | **KEEP** | PASS | 0 | 32,864,088,840 | v9 |
| 50 | `Wan-AI/Wan2.2-TI2V-5B` | select | **KEEP** | PASS | 0 | 34,201,539,556 | v9 |
| 51 | `Laxhar/noobai-XL-Vpred-1.0` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 52 | `StephaneBah/AfroRadVoice-FR` | conditional | **KEEP** | DATA | 0 | 1,040,330,586 | v9 |
| 53 | `amphion/Emilia-Dataset` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 54 | `bigcode/starcoderdata` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 55 | `bigcode/the-stack-v2` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 56 | `laion/relaion2B-en-research` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 57 | `lmsys/lmsys-chat-1m` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 58 | `allenai/WildChat-1M` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 59 | `CohereLabs/aya-vision-32b` | conditional | **KEEP** | PASS | 0 | 66,296,141,864 | v9 |
| 60 | `meta-llama/Llama-4-Scout-17B-16E` | conditional | **KEEP** | PASS | 0 | 217,315,708,790 | v9 |
| 61 | `allenai/Olmo-3-1125-32B` | select | **KEEP** | PASS | 0 | 64,476,874,755 | v9 |
| 62 | `IFM/K2-Horizon-0.9B` | conditional | **KEEP** | PASS | 0 | 2,161,772,471 | ADDED |
| 63 | `google/gemma-4-31B` | select | **KEEP** | PASS | 0 | 62,578,664,883 | v9 |
| 64 | `ibm-granite/granite-switch-4.1-30b` | select | **KEEP** | PASS | 1 | 59,991,296,229 | v9 |
| 65 | `LiquidAI/LFM3-Omni-2B` | conditional | **KEEP** | PASS | 0 | 4,499,443,673 | v9 |
| 66 | `mistralai/Mistral-Small-4-119B-2603` | select | **KEEP** | PASS | 0 | 120,960,168,209 | v9 |
| 67 | `Nanbeige/Nanbeige4.3-33B` | select | **KEEP** | PASS | 0 | 66,259,307,131 | v9 |
| 68 | `nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB` | conditional | **KEEP** | PASS | 0 | 6,180,517,517 | v9 |
| 69 | `LiquidAI/LFM2.5-VL-3B` | conditional | **KEEP** | PASS | 0 | 6,265,014,358 | ADDED |
| 70 | `LiquidAI/LFM2.5-VL-3B-DSpark` | conditional | **KEEP** | PASS | 0 | 558,964,083 | ADDED |
| 71 | `openai/gpt-oss-120b` | select | **KEEP** | PASS | 0 | 65,276,859,410 | v9 |
| 72 | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | conditional | **KEEP** | PASS | 0 | 70,530,595,574 | v9 |
| 73 | `Qwen/Qwen3.5-35B-A3B-Base` | select | **KEEP** | PASS | 0 | 71,926,986,405 | v9 |
| 74 | `Qwen/Qwen3.8-27B` | select | **KEEP** | PASS | 0 | 55,586,114,907 | v9 |
| 75 | `udgamlabs/Lilavati` | conditional | **KEEP** | PASS | 0 | 190,656,047 | ADDED |
| 76 | `udgamlabs/Lilavati-Checker` | conditional | **KEEP** | PASS | 0 | 190,649,144 | ADDED |
| 77 | `mistralai/Mistral-Large-4-1T-A52B` | hold | **HOLD** | EXCEPTION HOLD | 0 | UNKNOWN | v9 |
| 78 | `Nanbeige/Nanbeige4.3-33B-Base` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 79 | `EPFLiGHT/Meditron3-70B` | conditional | **KEEP** | PASS | 0 | 141,116,879,850 | v9 |
| 80 | `google/medgemma-4b-it` | conditional | **KEEP** | PASS | 0 | 8,639,644,263 | v9 |
| 81 | `boltz-community/boltz-2` | conditional | **KEEP** | PASS | 1 | 6,204,364,262 | v9 |
| 82 | `EPFLiGHT/fully-open-meditron` | select | **KEEP** | DATA | 0 | 511,345,597 | v9 |
| 83 | `EPFLiGHT/OLMo-2-32B-MeditronFO` | select | **KEEP** | PASS | 0 | 64,477,464,469 | v9 |
| 84 | `facebook/esm2_t33_650M_UR50D` | select | **KEEP** | PASS | 0 | 2,609,510,572 | v9 |
| 85 | `HuggingFaceBio/Carbon-X` | select | **KEEP** | PASS | 0 | 29,655,678,789 | v9 |
| 86 | `IFM/SFT-Reasoning` | conditional | **KEEP** | DATA | 0 | 158,563,572,761 | v9 |
| 87 | `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 88 | `OctoMed/OctoMed-32B` | select | **KEEP** | PASS | 0 | 66,726,453,842 | v9 |
| 89 | `EPFLiGHT/Apertus-70B-MeditronFO` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 90 | `StanfordAIMI/CheXagent-8b` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 91 | `nvidia/Cosmos-Predict2-2B-Video2World` | conditional | **KEEP** | PASS | 1 | 14,661,005,052 | v9 |
| 92 | `nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D` | hold | **HOLD** | DATA | 0 | UNKNOWN | v9 |
| 93 | `ACERobotics/Puffin-World` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | v9 |
| 94 | `lerobot/pi0_base` | conditional | **KEEP** | PASS | 1 | 14,005,628,513 | v9 |
| 95 | `lerobot/smolvla_base` | select | **KEEP** | PASS | 1 | 906,731,641 | v9 |
| 96 | `microsoft/TRELLIS.2-4B` | select | **KEEP** | PASS | 1 | 16,237,485,044 | v9 |
| 97 | `nvidia/GR00T-N1.6-3B` | conditional | **KEEP** | PASS | 1 | 6,573,788,038 | v9 |
| 98 | `speridlabs/idol` | conditional | **KEEP** | PASS | 1 | 3,078,990,585 | v9 |
| 99 | `tencent/Hunyuan3D-2.1` | conditional | **KEEP** | PASS | 1 | 14,909,683,275 | v9 |
| 100 | `laion/emotional-roleplay-finetuning-dataset` | conditional | **KEEP** | DATA | 0 | 6,667,420,582 | v9 |
| 101 | `m-a-p/MERT-v2-FullSong` | conditional | **KEEP** | PASS | 0 | 2,529,878,111 | v9 |
| 102 | `m-a-p/SheetSage2` | conditional | **KEEP** | PASS | 0 | 231,081,591 | v9 |
| 103 | `m-a-p/YuE2-3B` | conditional | **KEEP** | PASS | 0 | 7,264,394,226 | v9 |
| 104 | `m-a-p/YuE2-Vae` | conditional | **KEEP** | PASS | 0 | 530,751,018 | v9 |
| 105 | `nvidia/Granary-v2` | conditional | **KEEP** | DATA | 1 | 111,557,207,020 | v9 |
| 106 | `nvidia/OpenCodeInstruct` | select | **KEEP** | DATA | 0 | 6,861,119,940 | v9 |
| 107 | `nvidia/OpenMathInstruct-2` | select | **KEEP** | DATA | 0 | 12,628,474,179 | v9 |
| 108 | `facebook/dinov3-vit7b16-pretrain-lvd1689m` | conditional | **KEEP** | PASS | 0 | 26,864,283,632 | v9 |
| 109 | `facebook/dinov3-vith16plus-pretrain-lvd1689m` | conditional | **KEEP** | PASS | 0 | 3,362,457,679 | v9 |
| 110 | `facebook/sam3` | conditional | **KEEP** | PASS | 0 | 3,445,031,383 | v9 |
| 111 | `allenai/pixmo-cap` | conditional | **KEEP** | DATA | 1 | 1,101,532,176 | v9 |
| 112 | `allenai/tulu-3-sft-mixture` | conditional | **KEEP** | DATA | 0 | 1,412,964,994 | v9 |
| 113 | `answerdotai/ModernBERT-large` | select | **KEEP** | PASS | 0 | 1,585,710,451 | v9 |
| 114 | `autogluon/chronos-2` | select | **KEEP** | PASS | 0 | 477,940,832 | v9 |
| 115 | `BAAI/bge-m3` | select | **KEEP** | PASS | 0 | 2,295,443,588 | v9 |
| 116 | `CohereLabs/aya_dataset` | select | **KEEP** | DATA | 0 | 140,160,376 | v9 |
| 117 | `deepseek-ai/DeepSeek-OCR-2` | select | **KEEP** | PASS | 0 | 6,789,165,316 | v9 |
| 118 | `Edge0/Audio8-TTS-Realistic-0.6b` | hold | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 119 | `elyza/ELYZA-tasks-100` | select | **KEEP** | DATA | 0 | 7,788,480 | v9 |
| 120 | `facebook/vjepa2-vitg-fpc64-384` | select | **KEEP** | PASS | 1 | 16,464,857,277 | v9 |
| 121 | `google/siglip2-base-patch16-224` | select | **KEEP** | PASS | 0 | 1,539,458,338 | v9 |
| 122 | `GSAI-ML/iLLaDA-8B-Base` | select | **KEEP** | PASS | 0 | 16,512,918,618 | v9 |
| 123 | `HuggingFaceFW/fineweb-edu` | conditional | **KEEP** | DATA | 0 | 28,518,222,076 | v9 |
| 124 | `HuggingFaceH4/ultrafeedback_binarized` | select | **KEEP** | DATA | 0 | 649,980,296 | v9 |
| 125 | `ibm-granite/granite-speech-5.0-2b` | select | **KEEP** | PASS | 0 | 5,047,717,206 | v9 |
| 126 | `ibm-granite/granite-speech-5.0-470m-turboctc` | select | **KEEP** | PASS | 0 | 948,033,277 | v9 |
| 127 | `lerobot/aloha_sim_insertion_human` | select | **KEEP** | DATA | 0 | 91,348,537 | v9 |
| 128 | `lightonai/LightOnOCR-3-0.8B` | select | **KEEP** | PASS | 0 | 1,736,123,523 | v9 |
| 129 | `LiquidAI/d1-omni-600M` | conditional | **KEEP** | PASS | 0 | 2,353,572,356 | v9 |
| 130 | `LiquidAI/LFM3-1.7B-Base` | conditional | **KEEP** | PASS | 0 | 3,475,641,783 | v9 |
| 131 | `llm-jp/magpie-sft-v1.0` | select | **KEEP** | DATA | 0 | 284,157,816 | v9 |
| 132 | `nvidia/nemotron-labs-unified-asr-0.6b` | excluded | **DROP** | PASS | 0 | UNKNOWN | v9 |
| 133 | `openai/whisper-large-v3-turbo` | select | **KEEP** | PASS | 0 | 1,622,466,054 | v9 |
| 134 | `PaddlePaddle/PaddleOCR-VL-1.5` | select | **KEEP** | PASS | 0 | 1,930,468,959 | v9 |
| 135 | `PerceptronAI/Isaac-0.2-2B-Preview` | excluded | **DROP** | PASS | 0 | UNKNOWN | v9 |
| 136 | `qvac/TranscribePsy-250M-EU` | excluded | **DROP** | PASS | 0 | UNKNOWN | v9 |
| 137 | `Qwen/Qwen3-ASR-1.7B` | select | **KEEP** | PASS | 0 | 4,703,114,308 | v9 |
| 138 | `Qwen/Qwen3-Embedding-0.6B` | select | **KEEP** | PASS | 0 | 1,207,489,041 | v9 |
| 139 | `Qwen/Qwen3-Reranker-0.6B` | select | **KEEP** | PASS | 0 | 1,207,488,344 | v9 |
| 140 | `Qwen/Qwen3-VL-2B-Instruct` | select | **KEEP** | PASS | 0 | 4,266,648,961 | v9 |
| 141 | `Qwen/Qwen3.5-0.8B` | select | **KEEP** | PASS | 0 | 1,769,980,465 | v9 |
| 142 | `RWKV/RWKV7-7.2B-20260805` | select | **KEEP** | PASS | 0 | 14,402,000,339 | v9 |
| 143 | `state-spaces/mamba-2.8b` | excluded | **DROP** | PASS | 0 | UNKNOWN | v9 |
| 144 | `tencent/Hy-SimulMT-30B-A3B` | conditional | **KEEP** | PASS | 1 | 60,803,459,351 | v9 |
| 145 | `Wigtn/KoGovDoc-Bench` | excluded | **DROP** | DATA | 0 | UNKNOWN | v9 |
| 146 | `Wigtn/Qwen3-VL-2B-WigtnOCR` | excluded | **DROP** | PASS | 0 | UNKNOWN | v9 |
| 147 | `inclusionAI/Ming-3.0-tts-0.5B` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 148 | `lightonai/LightOnOCR-3-4B` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 149 | `m-a-p/MERT-v2-30s` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 150 | `nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B` | deferred | **HOLD** | PASS | 0 | UNKNOWN | v9 |
| 151 | `nvidia/Nemotron-Cascade-2-30B-A3B` | conditional | **KEEP** | PASS | 0 | 63,176,817,785 | ADDED |
| 152 | `nvidia/Nemotron-Cascade-2-RL-data` | conditional | **KEEP** | DATA | 0 | 2,859,999,928 | ADDED |
| 153 | `nvidia/Nemotron-Cascade-2-SFT-Data` | conditional | **KEEP** | DATA | 0 | 68,397,032,645 | ADDED |
| 154 | `orcarouter/Qwen3.8-27B-Uncensored-FP8` | deferred | **HOLD** | PASS | 0 | UNKNOWN | ADDED |
| 155 | `Hcompany/Holo4-27B` | conditional | **KEEP** | PASS | 0 | 54,736,673,609 | ADDED |
| 156 | `WhissleAI/steer-tts` | conditional | **HOLD** | UNKNOWN | 1 | 767,336,820 | ADDED |
| 157 | `maya-research/maya2-native` | conditional | **HOLD** | UNKNOWN | 2 | 5,021,124,225 | ADDED |
| 158 | `Hcompany/trajectories` | conditional | **KEEP** | DATA | 0 | 2,741,330,342 | ADDED |
| 159 | `Louis0324/StyleStream` | hold | **HOLD** | UNKNOWN | 0 | UNKNOWN | ADDED |
| 160 | `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU` | conditional | **KEEP** | PASS | 0 | 55,589,894,040 | ADDED |
| 161 | `fishaudio/drama-3` | conditional | **HOLD** | UNKNOWN | 1 | 41,502,571,262 | ADDED |
| 162 | `PrentisAI/GroundGUI-8B` | conditional | **KEEP** | PASS | 0 | 17,550,250,270 | ADDED |
| 163 | `ausboss/Qwen-Image-2.1-Consistency-LoRA` | conditional | **HOLD** | UNKNOWN | 1 | 159,544,753 | ADDED |
| 164 | `Hcompany/Holotron4-30B-A3B` | conditional | **KEEP** | PASS | 3 | 66,051,239,820 | ADDED |
| 165 | `LiquidAI/LFM2.5-24B-A2B-DSpark` | conditional | **KEEP** | PASS | 2 | 655,754,954 | ADDED |
| 166 | `pfnet/plamo-3-translate-31b` | conditional | **KEEP** | PASS | 2 | 63,518,748,101 | ADDED |
| 167 | `pfnet/plamo-3-translate-0.8b` | conditional | **KEEP** | PASS | 2 | 1,784,411,750 | ADDED |
| 168 | `nvidia/Cosmos3-Nano-Sim-Bimanual` | conditional | **KEEP** | PASS | 2 | 31,830,399,442 | ADDED |
| 169 | `PrunaAI/P-H3-Image` | conditional | **HOLD** | UNKNOWN | 4 | 99,840,428,064 | ADDED |
| 170 | `nvidia/Cosmos3-Nano-Sim-Auto` | conditional | **KEEP** | PASS | 3 | 32,364,133,043 | ADDED |
| 171 | `gradium/phonon-31m-en` | conditional | **KEEP** | PASS | 3 | 103,745,734 | ADDED |
| 172 | `gradium/phonon-40m-multilingual` | conditional | **KEEP** | PASS | 5 | 122,629,650 | ADDED |
| 173 | `kakaocorp/kanana-2-v-decide-3b-2611` | conditional | **KEEP** | PASS | 3 | 7,341,102,234 | ADDED |

## 8. H/T/D/C/U、ERROR CHECK

- **H（反証可能仮説）**：重み入手困難化のシナリオは確定的な禁止法ではない。検証尺度は個別IDの公開状態と同SHA再取得の可否（次の四半期、同条件観測）。
- **T（最小検証）**：本人同意なしで可能な匿名メタデータの照合と契約文面確認、モデル本体を取得しない。特定のアクセスを要する観測は手動本人同意後。
- **D（合否）**：静的173件整合性はPASS。取得・完全容量・権利・実機ピークはUNCERTAIN/NOT_APPROVED。取得機能をONにしない。
- **C（破れ方）**：配布元変更、別ファイルSHA、同じ基盤の独立の訓練成果、依存repoの欠落、契約地域、ユーザー実機容量が仮定を崩す。
- **U（不確かさ）**：主要誤差源＝物理容量、外部trained component、ファイルhash、ABI、契約。統計的標準不確かさ `u_c` と包含係数 `k` は測定値・分布が無く算定不能。虚偽の数値精度を付与しない。

検証結果：**20/20 PASS**、失敗ゼロ。これらはレコード/結合/論理制約の**静的検証**であり、実機・ダウンロード成功試験ではない。

## 9.〈応用・転用例〉

機械学習（完全なtrained依存）、デジタル保存（暗号学的固定・重複排除）、法務（契約同意・再配布と地域）、運用工学（物理容量・ピークRAM）の4工程がすべて成立して初めてアーカイブ取得へ進める。

## 10.〈次に考える問い〉

4TBの計画上限と実機空き容量が一致しない場合、まず約3.418TBの現行126件について低追加価値の重複量子化を抑えるべきか、それとも独立した学習成果の新規モデルを追加するべきか。根拠を伴う容量限界を見て決める。
