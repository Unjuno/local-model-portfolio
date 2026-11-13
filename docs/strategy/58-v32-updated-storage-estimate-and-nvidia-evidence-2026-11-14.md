# v32（182資産）容量見積書・NVIDIA特殊モデル一次資料更新 — 2026-11-14

> `main`に反映する**読み取り専用調査／容量見積書**。本体取得・実行・Gated同意・承認キュー・選定正本は変更しない。金額の購入見積ではなく、保存に必要なbyteの予算表。実機空き容量は未知。

基準GitHub HEAD: `9c91204e685c5433e5cb824ecb2b30d26b781caf` ／ 正本 `catalog/CURRENT.json`：v32-20261114（182管理・135有効＝SELECT53＋CONDITIONAL82）。

## 1. 事実・推論・未確定の境界

- **確認済み**：v27のSHA-aware source scope unionと、v28/v29/v30/v32の固定部分。各repoの公開ファイル・公表SHA/byteを読み取った既存監査資料がある。
- **推定値**：v31 ACE-Step XL Turboの本体約20GBと、共有元全repo約10.1GBは丸め公表値。共有元には不要な学習済み重みを含み、完全な最小依存セットでもない。
- **未確定**：v32での世界共通SHA union（時系列を跨ぐ完全な同一SHA照合）、Codec/Encoder/Runtime/SFTデータなど外部依存、実HDD総量・既存占有・cache/staging、すべての正規利用権限。
- **運用**：学習済み原本の希少性で保存候補を評価し、一般ベンチマーク優劣で独立した専門学習状態を削らない。ただし保存価値と実取得許諾・再現性能は別判定。

## 2. 既存資産の固定ソース容量明細（十進byte）

| 版 | 既存選定と照合したソース範囲 | byte | 証拠種別 | 注意 |
|---|---|---:|---|---|
| v27 | 126 then-active source union | 3,417,685,712,585 | PUBLISHER_SHA_AWARE_UNION_ONLY | Already hash-aware deduplicated within v27; excludes complete offline dependency closures |
| v28 | qvac/BotPsy-0.8B + ibm-granite/granite-timeseries-ttm-r3 | 1,732,327,856 | PUBLISHER_FULL_FIXED_REPOS | 17 files across two repositories, source metadata; not owner HDD |
| v29 | Zyphra/ZONOS3-Mini | 11,076,560,635 | PINNED_KEEP2_REFERENCE_NOT_MINIMAL | Native keep2 research profile, optional components and incomplete runtime; not a final baseline package |
| v29 | robbyant/lingbot-touch-tiny | 21,873,479 | PUBLISHER_FIXED_REPO | Full five-file source scope; sensor/runtime calibration missing |
| v30 | nvidia/Alpamayo2-Edge | 5,320,375,887 | PUBLISHER_FULL_FIXED_REPO | Actual samples/robot runtime and any external dataset rights not included |
| v32 | tencent/Qwen3.8-27B-DSpine-b16 + nvidia/Nemotron-3-Diarization + nvidia/RFD4-Proteina | 6,191,586,316 | PUBLISHER_FIXED_SELECTED_SOURCE_SCOPE | Three source subsets, 23 files, 3 model LFS SHA-256; local SHA untested. Parent Qwen shard reuse supported by matching publisher hashes |

- 既知スコープ算術合計（**v31 ACE除外**）＝ **3,442,028,436,758 B（約3.442028 TB）**。v28以降のスコープ算術増分＝**24,342,724,173 B**。
- 注意：v27内部のSHA-aware unionと、版をまたぐソーススコープの**算術和**を混同してはいけない。v29 ZONOSの11.08GBは研究用keep2 profileで最終最小構成ではない。これを『最終確定必要容量』と書かない。
- v32のDSpine/Diarization/RFD4はすでに選定済みで、新規候補枠に加算しない。DSpineの親Qwen重み18 shard+tokenizerは既存元とSHAが一致し再取得しない。

## 3. 4TB計画・200GB安全床の算術シナリオ（実空きではない）

| シナリオ | 容量（byte） | 4TBの仮想空ディスクで200GBを残す算術差（byte） | 重要な未確定事項 |
|---|---:|---:|---|
| `S0_FROZEN_PLUS_R48_NATIVE_RESEARCH` | 3,442,028,436,758 | 357,971,563,242 | v27 known publisher SHA union + v28/v29/v30/v32 source scopes; exclude ACE |
| `S1_ACE_XL_DISPLAY_PROXY` | 3,462,028,436,758 | 337,971,563,242 | S0 plus approximate XL Turbo model root public display, exclude shared |
| `S2_ACE_XL_AND_SHARED_FULL_REPO_PROXY` | 3,472,128,436,758 | 327,871,563,242 | S1 plus full ACE shared repo public display approx; contains unneeded 2B weights and may miss other dependencies |

これらは、空の4TB実ディスクに完全なソースバイトのみ配置した**仮想計算**である。OS実空きやcomplete offline runtime、checksum重複、未保存素材の有無を反映せず、実際の購入余裕・取得許容量ではない。もし実総容量が仮に3.8×10^12Bなら、安全床を残した許容占有は3.6×10^12Bであり、S2相当の算術差は127,871,563,242Bまで縮む。これも実測ではない。

## 4. 実際の公開元を再照合したNVIDIAの特殊候補（現在の予算には加えない）

| 正確なrepo ID | 現行v32登録 | HFの一般向け表示 | 正確な最終選択byte | 公開元の概数／確認事項 | 優先研究 |
|---|---|---|---:|---|---|
| [`nvidia/Kumo-Relational`](https://huggingface.co/nvidia/Kumo-Relational/tree/main) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 約244,000,000 B （丸め） | P0_ARCHIVE_RESEARCH |
| [`nvidia/Nemotron-3.5-Parse`](https://huggingface.co/nvidia/Nemotron-3.5-Parse/tree/main) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 重み約2,520,000,000 B（丸め） | P1_ARCHIVE_RESEARCH |
| [`nvidia/Ising-Decoder-ColorCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | NOT_V32_ACTIVE | GATED | 未固定 | 未確認 | P0_GATED_PERMISSION |
| [`nvidia/Ising-Decoder-SurfaceCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | NOT_V32_ACTIVE | GATED | 未固定 | 未確認 | P0_GATED_PERMISSION |
| [`nvidia/Kumo-Anomaly`](https://huggingface.co/nvidia/Kumo-Anomaly) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 未確認 | P0_SPECIALIST |
| [`nvidia/Kumo-Tabular`](https://huggingface.co/nvidia/Kumo-Tabular) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 未確認 | P1_SPECIALIST |
| [`nvidia/Kumo-Forecast`](https://huggingface.co/nvidia/Kumo-Forecast) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 未確認 | P1_SPECIALIST |
| [`nvidia/GR00T-N1.7-3B`](https://huggingface.co/nvidia/GR00T-N1.7-3B) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 未確認 | P1_ROBOT_ACTION |
| [`nvidia/QCalEval`](https://huggingface.co/datasets/nvidia/QCalEval) | NOT_V32_ACTIVE | UNGATED_PUBLIC_METADATA | 未固定 | 未確認 | P0_ANNOTATED_SCIENCE |

### 4.1 Kumo Relational：2つの学習済みhead

- [NVIDIA配布元ファイルツリー](https://huggingface.co/nvidia/Kumo-Relational/tree/main)では**総表示244MB**、分類用`classifier.pt`約120MBと回帰用`regressor.pt`約124MBを確認。**四捨五入されたUI値**であり実byteではない。両タスクの長期保存を選ぶなら2 headの権利・依存を確かめ、1本に勝手に統合しない。
- [公式モデルカード](https://huggingface.co/nvidia/Kumo-Relational)はOpenMDW-1.1、TabICLv2由来のBSD-3-Clause帰属、`THIRD-PARTY-NOTICES.txt`を明記。これはKumo Forecastや既存Chronos2と同一の学習状態ではない。実行前に`structured-data-models`/ABIと選択headのSHAを固定する。

### 4.2 Nemotron 3.5 Parse：weightsだけでなく対応ランタイムを固定

- [公式HFモデル重み](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/main/model.safetensors)は約2.52GBの表示、[公開repo](https://huggingface.co/nvidia/Nemotron-3.5-Parse/tree/main)は約2.74GBで、後者には任意の別学習済み`dflash2`、コード、テスト等を含む。一般画像OCRとは異なる文書構造・図表・読み順の学習成果を持つが、現在のv32には未採用。
- **版の互換性が核心**：公開元の新しい重みSHA256は`81dd7609c589f3694ce75520c25af5010953231358de6aec4d03e8c6aac787e9`。古いrc3版の40桁revision `8570c1c75bc1b1ab4176066d0d250056048e2611`では重みSHA256 `fa5980193d8519efbdcd45054f3a7616c961d06f7a7653bdafcfba60a412f09c`、wheel SHA `20d3a4504c1a74cac4b403f7afd72d77ce07d5c335993bb5fb53a44c164a0171`。これらは同じパスでも**同一重みではない**。
- [開発元の変更記録](https://huggingface.co/nvidia/Nemotron-3.5-Parse/commit/9a64c9d390232578b9124212a3c1f84e5440e31c)では新wheelに対するGPU再検証未実施と記される。モデル＋対応wheel/Transformers/vLLM/torch/FlashAttention/ABIをセットで固定するまでは、約2.52GBだけで完全保存と認定しない。計画候補容量にも未加算。

### 4.3 Ising：すでにGatedだが、公開撤回の予定ではない

- [ColorCode Fast](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast)と[SurfaceCode Fast](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast)は**Gated表示**。ColorCodeはOpenMDW-1.1タグ、SurfaceCodeはモデル種別/版ごとのライセンス再照合が必要。本人の許可が未確認なのでファイル取得・SHA/byte確定は不可。
- SurfaceCode **Accurate**のファイル表示3.6MBを、**Fast**の重み容量に転用してはいけない。別符号/別最適化の学習結果であり、単なる量子化違いとは決めない。
- NVIDIAが近く一斉に重み公開を撤回する事実は確認できない。現行Gatedと将来配布制限の仮説を分離する。

## 5. 変数表・次元検査

| 記号 | 日本語の意味 | SI／情報量単位 | 定義（式）・範囲・前提 | 型 |
|---|---|---|---|---|
| C | ポートフォリオ計画上限 | byte | 4,000,000,000,000。非負。実HDD測定ではない | 整数スカラー |
| Fmin | 保存後に残す最小物理空き | byte | 200,000,000,000。非負 | 整数スカラー |
| B27 | v27監査済み内部SHA-awareソース集合 | byte | 3,417,685,712,585。126アクティブの既知ソースのみ | 整数スカラー |
| ΔB | v28/v29/v30/v32固定元のソース範囲算術和 | byte | 24,342,724,173。版横断同一SHAは未検証 | 整数スカラー |
| A | v31 ACE XLの公表元重み容量（概数） | byte | 20,000,000,000。厳密値でない | 近似スカラー |
| S | ACE共有元全repo容量（概数） | byte | 10,100,000,000。必要最小部品より広い可能性 | 近似スカラー |
| U | 空の4TB実ディスクを仮定した算術差 | byte | U=C−Fmin−(B27+ΔB+A+S)。実際の空きではない | 整数スカラー（概数を含む） |
| H | 実HDD空きバイト | byte | null：所有者PC未計測。既存占有・staging/別ドライブも不明 | null／整数スカラー |
| P | 全MoE expert・補助学習済み部品込み総パラメータ | 1（個数） | unknownはnull、active数と区別、量子化で減らない | 整数スカラー／null |
| M | OS/backend/KV/codec等込みピークメモリ | byte | null、OS/HW/clock/ABI/量子化zero-point/context/batch未測定 | 整数スカラー／null |

**次元検査**：Uの右辺は全てbyte。Pは無次元であるからbyteや活性expert数と置換不可。TBは十進10^12byte、TiBは2^40byte。合成標準不確かさu_c・包含係数kは、欠落依存と実機観測分布がないため定量化できない。

## 6. H/T/D/C/U、ERROR CHECK

- **H**：原本学習状態ごとの取得ファイルと必要依存を固定し、重複形式を除けば、ポートフォリオの再現範囲を守りつつ費用を削減できる。反証：実際には親と同一SHA・必要Codec不一致・許諾不能。
- **T**：元v27の126資産とその後のv28/v29/v30/v31/v32の9新規選定分を照合（現v32の有効135件）。既知ソースはファイル単位SHA/byte、未確定ACEは別枠。新しいNVIDIA候補9件を公式repoとライセンス/依存で静的照合。オンラインメタデータだけで実物取得しない。
- **D**：PASS＝全必要学習部品と原本同一性、適法なアクセス、現物SHA/実HDD/staging、本人承認が成立。FAIL＝禁止/容量超/重複形式・SHA不一致。現時点は**UNCERTAIN**で取得は許可しない。
- **C**：隠れた第三者依存、Gated未許諾、推論backend違い、releases間のモデルとwheel不一致、ZONOSの研究スコープが過大、ACEの音楽LM/VAE欠落。
- **U**：外部学習依存・GPU/CPU ABI・cache/staging・ライセンス・実HDD。数量的誤差分布未定義ゆえu_c/k未算定。
- **ERROR CHECK**：v27源${fmt(v27)}＋後続スコープ${fmt(scopesAfterV27)}＝${fmt(baseScope)}B。追加ACE表示proxyケースB=${fmt(scenarios[2].byte_scope)}B。空の4TB+200GB床での机上差額=${fmt(scenarios[2].empty_four_tb_and_floor_arithmetic_margin)}B。新候補9件は既存v32のIDと重複なし、候補容量は上記シナリオに未計上。DL承認0、モデル実行0、実HDD検査0。CI実行/物理SHA照合は主張しない。

**学際的応用**：機械学習（独立学習状態）、ソフトウェア供給網（immutable SHA/ABI）、デジタル保存（依存閉包・容量）、法学・契約（Gated/用途/再配布）。

## 7.〈次に考える問い〉

最後に残せる容量が250–330GB程度という机上の差額に対し、大きな別学習済み原本と、必要な外部Codec・権利・実機空き確認のどちらを先に確定すべきか。
