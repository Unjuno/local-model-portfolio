# R109｜v46ダウンロード対象の再確定：小型5原本＋無検閲RVNと容量を伴う交換案

**2026-11-18 訂正**：BotPsy-0.8Bはツール利用を後学習したエージェント原本であり「安全専門・行動リスク分類器」とした旧記述を訂正。現行正本はv47なので、最新の[原本14件容量・役割監査](112-v47-owner-capacity-and-source-role-finalization-2026-11-18.md)を優先参照。

2026-11-18 JST。GitHub `Unjuno/local-model-portfolio`、現行正本 `v46-20261118`（198登録／有効151）。本記録は既存カタログの**取得対象の研究上の確定**であり、権利・実HDD・モデル実行・SHA実測・本人の取得承認を確定するものではない。正本変更0件、`queues/approved.json`変更0件、モデル本体取得0件。

一次資料を保持する[全45ファイル・候補別判定JSON](../../catalog/proposals/2026-11-18-r109-six-originals-wave-and-swaps.json)／ベースとなる[出版社の12モデル131ファイル原本台帳](../../manifests/drafts/r107-v45-12-original-sources-file-freeze.candidate.json)／[v46の151件グローバル最適化](../../docs/strategy/108-v46-global-portfolio-optimization.md)。

## 1.〈本論〉— なぜ取得対象をさらに少なくするのか

4TB計画の目的は、無検閲・独立後学習・小型専門・珍しい構造・科学データなど**後から合法に再構築しづらい学習成果を、同一重みの量子化重複なしに保全すること**である。新しいモデルをカタログに追加するだけでは、許可済みの再現可能なアーカイブは増えない。実際に採用する1つの原本形式、tokenizer・codec・画像projector・外部学習済み依存、ライセンス、HW/ABI条件を固定する必要がある。

`v46`の12原本ソース候補は131ファイル・206,683,452,429byteで、すでに**現行151有効件の一部**。その中から今回は、まず小型5件（2,747,856,039byte）と無検閲RVN 1件（17,176,692,278byte）を、**ファイル名／完全revision／出版社ハッシュの照合済み研究候補**として抜き出した。

### Phase A：小容量・異なる学習成果の5原本

- **時系列**：`ibm-granite/granite-timeseries-ttm-r3`は約5.75MB。単なる汎用LLMでは代替できない1.4M級の時系列学習結果。最初の復元試験として小さいが、TinyTimeMixerライブラリ/パラメータ整合を固定する。
- **触覚**：`robbyant/lingbot-touch-tiny`は約21.9MB。タッチセンサの独自学習特徴。学習済み`encoder.pt`は安全性未確認のPyTorchシリアライズとして扱い、未監査の`torch.load`をしない。
- **話者分離**：`nvidia/Nemotron-3-Diarization`は約397MB、OpenMDW系のライセンスタグ。ASRやTTSとは異なる音声タスクであり、関連コード・wheel・実行ABIとライセンス正文は未確定。
- **プロンプト注入分類**：`usezn/Galvanize-3`は約597MB、ModernBERTの別後学習済み分類原本。量子化ONNXなどの同じ学習済み成果を無条件に二重保管せず、元重みと閾値設定を保持する。
- **小型ツール呼び出しエージェント**：`qvac/BotPsy-0.8B`は約1.726GB。Qwen系のSFT・教師蒸留・RLによりツール利用を後学習した原本で、エージェントの危険性分類器ではない。安全分類器はGalvanize-3であり両者の用途を混同しない。

### Phase B：無検閲モデルは1つの代表成果から

[0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)は、旧Hereticと後続RVNに異なる学習・編集成果があることを区別する。今回の原本候補は**RVN-Q4_K_M-multilingual GGUFと対応するQ8 vision mmprojを1版だけ**。古い同族GGUFや多数の通常量子化形式は取得順へ追加しない。量子化原本の独自性は配布者の改変成果に由来し、GGUFという形式自体が特別な学習成果ではない。推論エンジンは`llama.cpp`の対応commit、GDN/VL/projector、context/batch、量子化ABI、メモリ・速度が未検証。

| 順位 | 配布元の40桁固定モデル原本 | 候補ファイル数 | 候補容量（十進GB） | Publisher SHA-256あり | 最初の停止ゲート |
|---:|---|---:|---:|---:|---|
| 1 | [`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/tree/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa) | 5 | 0.006 | 1 | SOURCE_LICENSE_AND_RUNTIME |
| 2 | [`robbyant/lingbot-touch-tiny`](https://huggingface.co/robbyant/lingbot-touch-tiny/tree/f23969ccd4b6bba2163e69cc05a577455a075fe9) | 5 | 0.022 | 1 | PICKLE_ABI_RIGHTS |
| 3 | [`nvidia/Nemotron-3-Diarization`](https://huggingface.co/nvidia/Nemotron-3-Diarization/tree/52a432672732425e4c19765b9fec9b5810e6f4ba) | 11 | 0.397 | 1 | OPENMDW_LICENSE_AND_CODE_DEPENDENCIES |
| 4 | [`usezn/Galvanize-3`](https://huggingface.co/usezn/Galvanize-3/tree/597237be3b0fabbf5d70ff16ce95fad14a591f20) | 9 | 0.597 | 2 | TRAINED_DEPENDENCIES_AND_LICENSE |
| 5 | [`qvac/BotPsy-0.8B`](https://huggingface.co/qvac/BotPsy-0.8B/tree/24561e9681643eaf807fc28b0875210cb17f89c1) | 11 | 1.726 | 2 | ATTRIBUTION_AND_RUNTIME |
| 6 | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/tree/ab8d7bd81d03117501e4da60cccdff4c80f0eea0) | 4 | 17.177 | 2 | ORIGIN_PARENT_LICENSE_AND_LOCAL_SHA |
| **計** | **6原本／全てv46既存** | **45** | **19.925** | **9** | **本体取得承認は0件** |

全45ファイルの`path`・`bytes`・LFS SHA-256/小ファイルのGit blob SHA-1はR109 JSONに記録した。Git blob SHA-1をSHA-256と誤認せず、Publisherハッシュのないファイルに架空のSHAを与えない。

## 2.交換・延期の明確な判断

ここでいう「交換」は**初期取得する原本の順番とsourceの選び方**の交換であり、独立した別学習済み資産を正式に削除することではない。容量が逼迫している状況で、性能や独自性が証明される前に同系27B原本を複数ダウンロードする作業を止める。

| 現行v46にあるモデル | 今回の初期取得判断 | 既存固定元バイト（参考） | 根拠 |
|---|---|---:|---|
| [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | P0_OWNER_GATED_RIGHTS_ONLY | 55,586,066,230 | Source BF16 refused-edit original potentially nonreconstructible, but Hub gate authorization is not established. No workaround via mirroring. |
| [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | P2_COMPARE_DISTINCT_POLITICAL_EDIT | 17,738,327,225 | Independent censorship-edit checkpoint compared with 0bserverx; no duplicate without demonstrated retention value. |
| [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | P2_NONCOMMERCIAL_PARENT_REQUIRED | 671,173,375 | 671MB fine-tuned image adapter, but distinct shared parent Qwen Image 2.1 and Qwen Research license noncommercial rights and dependencies required. |
| [`tencent/Qwen3.8-27B-DSpine-b16`](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | P2_PARENT_RUNTIME_CLOSURE | 4,051,857,976 | 4GB trained drafter has parent Qwen27B dependency; not standalone 4GB. Keep future selection with parent dedup. |
| [`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2) | DEFER_NEXT_WEIGHT_LOCK_PENDING_INDEPENDENT_QUALITY | 53,121,584,389 | Specialist independent checkpoint, but 53.12GB source and unproven incremental quality versus present reasoning/roleplay originals. |
| [`DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU`](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | DEFER_NEXT_WEIGHT_LOCK_PENDING_INDEPENDENT_QUALITY | 55,589,894,917 | 55.59GB another Qwen27B independent finetune; after already selected RVN and Interpretic checkpoint, needs distinct performance/license comparison. |

特に`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`と`DavidAU/Qwen3.8-27B-TURBO-...-Uncensored`の初期取得を延期すれば、**直近トランシェから108,711,479,306byteの出版社ソース候補を後送り**できる。ただし既存v46の有効選定はそのままであり、4TBの論理予算にこの数字を「新しく空いた容量」と加算しない。既存151件の保存計画の抜本的な削除/節約額には、そもそも現行代理見積もりがその重みを含む範囲、他の必須依存・キャッシュ等の再検証が必要。

`orcarouter/Qwen3.8-27B-Uncensored`のBF16原本（約55.586GB）には独立した拒否方向編集を保全する価値があるが、**Gated本人権限未確認**が主停止条件。`InterpreticAI`の政治回答編集Q4（約17.738GB）は0bserverxと別学習なので削除しないが、先に重み差分・通常能力・容量を比較する。`chatrlabs`の画像LoRA（約0.671GB）はQwen-Image-2.1親原本と非商用研究ライセンスの確認が必要。`DSpine`（約4.052GB）のドラフターは**親Qwen27Bが必要**であり、4GB単体でオフライン使用できるとは言わない。

## 3. v46外の追加候補3件の確定/停止基準

| モデル | 今回の判断 | 根拠 |
|---|---|---|
| [`osunlp/ARLoop-1.2B`](https://huggingface.co/osunlp/ARLoop-1.2B) | P1_RESEARCH_INCLUDE_SINGLE_FINAL_TRAINED_STATE_AFTER_STATIC_TREE | Independently trained pretraining architecture, not another RL-edited Qwen model. Preserve final main / step-238417 once, not every 23 intermediate checkpoints. |
| [`KittenML/kitten-tts-2-mini`](https://huggingface.co/KittenML/kitten-tts-2-mini) | P1_RESEARCH_INCLUDE_NATIVE_ORIGINAL_AND_VOICE_PACKS_ONCE_FIXED | One learned model identity; retain native FP32 as archival original, ONNX INT8 optional convenience artifact only if exact reproduction route cannot be established. Do not count both as separate models. |
| [`xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic`](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic) | P1_STUDY_NOVEL_ABLATION_WITH_PARAMETER_CENSUS_HOLD | Edited 9B Qwen-family (not DeepSeek-owned base weights). 243.3M element difference relative to parent could be omitted submodule or representation change; no inferred root cause. Must validate vision/MTP completeness, parent license, model-alignment quality before promotion. |

**ARLoop-1.2B**：著者の[一次論文 arXiv:2611.05234](https://arxiv.org/abs/2611.05234)と[公式モデルカード](https://huggingface.co/osunlp/ARLoop-1.2B)は、24共有物理層×3反復のAttention Residual、最終約5000億トークン学習、FP32保存重みを説明する。**最終原本は独立して保全する価値がある**が、全23中間チェックポイントを初回から取らない。研究の再現に必要な場合のみ中間版を追加評価する。配布者の`trust_remote_code=True`を事前に自動実行せず、`transformers==5.12.1`と作者コード、OS・Python・Torch・CUDA/ABIを固定する。正確な40桁revision／全ファイルbytes/SHAを未確定としたので、現時点では研究選定であって取得承認ではない。

**KittenML/kitten-tts-2-mini**：[公式モデルカード](https://huggingface.co/KittenML/kitten-tts-2-mini)の82M、16言語・118声を確認。source treeには**約327MBの元FP32 safetensorsと約82.7MBのINT8 ONNX**、16言語の学習済みvoice pack群、`g2p/`がある。**学習済み原本はFP32側**。INT8 ONNXは使いやすい別形式であるが、学習成果2件として二重に数えない。保存候補はFP32と声pack全言語と辞書／構成、ONNXは変換手順を安全に再現できないと確認した場合のみ独立の実用フォーマットとして追加検討する。日本語`voices_ja.npz`を単独で「モデル完成」と数えない。Hub全repo約478MBを最終取得バイトへ置換しない。

**xtools-at/Qwen3.5-9B Heretic無検閲派生**：[編集済み重み](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic)はHugging Faceの配布表示で**9,409.8M要素**、親[Jackrong](https://huggingface.co/Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B)は**9,653.1M要素**。同一表記上の差は**243.3M要素**。この差から「vision towerが削除された」「MTPが必ず欠落した」とは推定しないが、**元の親と同じ完全マルチモーダル構成か未証明**のため、原本の厳格な機能保存目的ではsource構成照合を最優先する。作者の拒否率3/100と親100/100は作者による同一条件の拒否サンプル評価であり総合能力ベンチではない。通常推論品質、親LICENSE、4主シャード+MTPとconfigの同一revision完全性が確認できるまで、正式追加ではなく研究HOLDとする。「DeepSeek」の名称は蒸留/後学習由来であり**DeepSeek社の独立原モデルを保有できることの証明ではない**。

## 4. 4TBとの容量関係と変数表

| 記号 | 意味（日本語） | SI単位 | 定義・条件・定義域 | 型 |
|---|---|---|---|---|
| `B_A` | 小型5件の出版社選択ソース | byte (B) | 2,747,856,039、ファイル選択を固定したが実機未取得 | 非負整数スカラー |
| `B_R` | RVN1件の出版社選択ソース | byte (B) | 17,176,692,278、プロジェクタを含む | 非負整数スカラー |
| `B_6` | 6原本の出版社選択ソース合計 | byte (B) | `B_A+B_R`、現行v46の内数 | 非負整数スカラー |
| `B_D` | 大型後回し2件の固定ソース候補 | byte (B) | 108,711,479,306、**物理空き増分ではない** | 非負整数スカラー |
| `B_C` | 保存計画上限 | byte (B) | 4,000,000,000,000、HDD実測ではない | 非負整数スカラー |
| `B_F` | 必須最低空き容量 | byte (B) | 200,000,000,000、実測未確認 | 非負整数スカラー |
| `N_T` | 主・MoE全expert・補助学習重みの総要素数 | 1（無次元） | 非負整数またはnull（未知は取得準備停止） | 整数/nullable |
| `M_P` | 推論完全ピークRAM | byte (B) | backend／量子化zero-point／context／batch／KV／OSを含む推定・実測 | 非負実数/nullable |

`B_6 = B_A + B_R = 19,924,548,317 byte`。次元確認：加算はbyte同士、結果もbyte。`B_D`は取得順を後にしたもののsourceサイズであり、消し去った既存の物理ファイル量ではない。`N_T`（個数）をGGUFやFP32のbyteと混同しない。

v45からの[151件ソース代理値](../../catalog/capacity/2026-11-18/v45/publisher-source-reconciliation.json)は3,732,164,752,962byte、最低空き200GBを差し引いた仮余裕67,835,247,038byte。ただしv46後の真の依存込み容量ではなく、[R108の仮予約余白27.41GB](../../catalog/decisions/2026-11-18-r108-global-portfolio-optimization.json)とは対象計算が異なる。**いずれも所有者HDDの実空きとしては証明されていない**。今回の6件を「新規19.92GB追加」して二重計上することを禁止する。

## 5. H / T / D / C / U — 最小反証検証

**H**：小型5独立原本＋RVN 1学習済み派生の45ファイルを完全同一性で保存できれば、大型の近接同族チェックポイントを無検証で複数保存するより少ない初期転送バイトで多様な再現可能能力を確保する。ただし性能と規制確率はまだ実証されていない。

**T**：固定source 6repo（n_min=6）と45ファイルを別個のrevision・上流SHAで静的照合。全151件v46 IDの包含確認、初期Phase Aの5件から最小のTTM R3をデータ検証候補とする。品質比較は最低30個の同条件入力を準備して、HW、クロック、batch/context、量子化とbackendを固定し、独立メトリクスで評価する。現在は本体ダウンロード・実行なし。

**D**：PASS＝6件・45パスの完全版とPublisher SHAの整合、source合計が19,924,548,317 byte、承認0。FAIL＝権利・Gated個別許諾を無視、別revisionが混在、未知MoE総数を0として扱う、勝手に重みを取得/任意コードを実行する。UNCERTAIN＝本人HDD・全学習済み外部依存・ABIと合法な具体的利用資格・実行性能。

**C**：小型分類器に外部必須学習済み重みがある、`.pt`の読み込みが安全にできない、RVNのmmprojが固定modelと非互換、Kittenの音声パックやARLoopのコードで別許諾が必要、出版社が正規配布を停止/変更するなど。

**U**：公開元の表示変更、Publisher SHAの適用範囲、著作権と商用/再配布の許諾、personal Gated、未監査サードパーティ依存、推論環境・キャッシュと実際のHDDが主要不確かさ。発生確率・誤差分布を計測しておらず、合成標準不確かさ`u_c`と包含係数`k`は数値化しない。

## 6.〈応用・転用例〉

**機械学習**では独立学習済み重みの保全、**ソフトウェア供給網**では不変版/ハッシュ/ABI・第三者シリアライゼーション監査、**音声・ロボット工学**ではモダリティ別の小型原本、**AI法政策**では権利と将来規制を別に追跡する。公開の「危険度」を根拠のない規制予定に換算しない。

### ERROR CHECK

- 現行v46の198資産／151有効、選定変更0、追加取得承認0。
- Publisher固定6repo・45ファイル・9個の上流SHA-256付きファイルを改めて再集計。全ファイルは40文字SHAの原本から選択したが、手元の現物ハッシュ・推論・HDDは未検証。
- 他6件の固定原本を失わない。後回し2件は消去ではない。
- Exaは2026-11-18の再実行で**402クレジット枠上限**。Exaの新規検索結果を得られたとは記載しない。今後のExa調査には利用枠の回復が必要。
- `main`や`CURRENT.json`・`queues/approved.json`への変更・モデル本体取得なし。

## 7.〈次に考える問い〉

初期の5小型モデルから1件だけ完全オフライン復元まで進める場合、**約5.75MBのTinyTimeMixer**でSOURCE→LICENSE→runtime→実HDD→ローカルSHAの一連の承認手順をまず検証することが、無検閲27Bを直接取得するより合理的か。
