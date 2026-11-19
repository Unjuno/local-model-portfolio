# R123｜v51 204資産から保存の次波を確定：OrcaRouter独自原本・既取得との照合

**検査日** 2026-11-19。**基準main** `58ebb1d5dcaf9447104b271f4cdd4a726b8b2cbe`、`CURRENT.json` **v51**、204件（157有効・178 models / 26 datasets）。新規正式選定・削除なし。これは研究判断であり重みの取得承認ではない。

## 1.〈本論〉監査と優先順位

- 現行v51に追加された [`RadixArk/DaisyRose-27B`](https://huggingface.co/RadixArk/DaisyRose-27B) は、異なる学習済み重みの強化学習済み原本として**既に採用済み**。固定34ファイル・55,586,309,473byteのPublisher sourceに対し、ユーザーDドライブ現物・LICENSE・取得承認が未確定。再追加しない。
- 独立した原本の最初の新規source検証対象は **[`Reson8/Rumble-2-Flash`](https://huggingface.co/Reson8/Rumble-2-Flash)**（19 files, **1,385,998,807 byte**, revision `a0c34287229103b706c670d70791683e34379732`）と **[`InterpreticAI/Qwen3.8-27B-Uncensored-v2`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)** BF16（32 files, **55,586,056,799 byte**, revision `84ab13688128c19d5ef10be430bc5de649b7823f`）。両者ともv50の17ソース候補でPublisher metadataを固定済みだが転送は正式未承認。
- **[`orcarouter/LFM3-1.7B-abliterated`](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated)** を小型無検閲独自編集原本の**新規調査第1位**とする。HF表示1.7288B、親 `LiquidAI/LFM3-1.7B` とは違う拒否方向編集後の学習済み成果。現時点では**Gated、license other（LFM Open Licenseの正文要再調査）、custom code、安全評価未確認**なので **CURRENT追加/最終lock/ダウンロードはSTOP**。
- 同じ27B系列からのGGUF量子化のみを独立学習成果として二重登録しない。**[Nex 35B級](https://huggingface.co/orcarouter/Nex-N2.5-mini-Uncensored)** は別個の視覚＋エージェント安全制御編集候補として、Gated・元親モデルの許諾・16 BF16シャードの完全revision固定を優先調査。
- v50 17件のsource候補・156件のreadinessを **v51の正本に書き戻していない**。現行v51の有効157件すべてに研究上の次アクションを [JSON](../../catalog/decisions/2026-11-19-r123-v51-source-reconciliation-orca-review.json) で付与した。別セッションの選定を無断で上書きしない。

## 2. 出版社が固定した17原本ソースと取得履歴の差分

**照合キー**：repo ID、immutable 40桁revision、ファイル数、source総byte数、Publisher SHA256参照が既存の同名ファイルhashと整合すること。これは**ledgerの自己報告どうしの照合**であって、実Windows Dの独立再hashではない。

| No. | 原本source repo | files | 選択source byte | 過去の取得報告 | 研究用GO/HOLD |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | `ibm-granite/granite-timeseries-ttm-r3` | 5 | 5,748,963 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 2 | `robbyant/lingbot-touch-tiny` | 5 | 21,873,479 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 3 | `n4ze3m/tiny-voca` | 14 | 23,626,858 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 4 | `KittenML/kitten-tts-2-mini` | 27 | 477,936,075 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 5 | `usezn/Galvanize-3` | 9 | 597,001,839 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 6 | `qvac/BotPsy-0.8B` | 11 | 1,726,201,481 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 7 | `osunlp/ARLoop-1.2B` | 15 | 4,838,079,760 | 既報告4条件＋公開SHA一致（実機未検証） | GO_AFTER_LOCAL_PREFLIGHT |
| 8 | `Zyphra/ZONOS3-Mini` | 24 | 15,345,816,226 | 既報告だがファイルscope相違 | GO_AFTER_LOCAL_PREFLIGHT |
| 9 | `InterpreticAI/Qwen3.8-27B-Uncensored-v2` | 32 | 55,586,056,799 | 旧台帳に取得成功報告なし | GO_AFTER_LOCAL_PREFLIGHT |
| 10 | `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | 3 | 53,808,326,934 | 既報告だがファイルscope相違 | GO_AFTER_LOCAL_PREFLIGHT |
| 11 | `nvidia/Nemotron-3-Diarization` | 11 | 397,030,277 | 既報告4条件＋公開SHA一致（実機未検証） | HOLD_LICENSE_AND_RUNTIME_REVIEW |
| 12 | `tencent/Qwen3.8-27B-DSpine-b16` | 5 | 4,051,857,976 | 既報告4条件＋公開SHA一致（実機未検証） | HOLD_TARGET_PARENT_ABI |
| 13 | `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1` | 8 | 671,173,375 | 既報告4条件＋公開SHA一致（実機未検証） | HOLD_NONCOMMERCIAL_PARENT_LICENSE |
| 14 | `Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2` | 12 | 53,121,584,389 | 既報告4条件＋公開SHA一致（実機未検証） | HOLD_REDUNDANCY_AND_DELTA_EVAL |
| 15 | `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU` | 25 | 55,589,894,917 | 既報告4条件＋公開SHA一致（実機未検証） | HOLD_REDUNDANCY_AND_DELTA_EVAL |
| 16 | `orcarouter/Qwen3.8-27B-Uncensored` | 31 | 55,586,066,230 | Gated許諾不足による停止 | HOLD_GATED_PERSONAL_ENTITLEMENT |
| 17 | `Reson8/Rumble-2-Flash` | 19 | 1,385,998,807 | 旧台帳に取得成功報告なし | GO_AFTER_LOCAL_PREFLIGHT |

**検算**：12件はsource scopeと既報告のhash metadata一致、2件は同じrepo ID/revisionでも異なるsource scope、2件は未取得報告、1件はGated停止。

**原本の交換（物理差分確定は未完了）**：
- `Zyphra/ZONOS3-Mini`：旧報告 **775,728,152 byte** vs 原本source **15,345,816,226 byte**。算術上の差は **14,570,088,074 byte**。
- `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`：旧Q4＋mmproj **17,176,692,278 byte** vs 原本F16 source **53,808,326,934 byte**。差は **36,631,634,656 byte**。
- 数値の差は**取得すべき追加bytesではない**。同名・同SHAの物理ファイル集合を比較し、必要ファイルのみ評価。旧Q4・既存データは勝手に削除しない。

## 3. OrcaRouter新規候補（規制仮説と観測事実を分ける）

| 調査順位 | 一次配布URL | 公式表示総数の目安 | 現状 | 判断 |
| ---: | --- | ---: | --- | --- |
| 1 | [`orcarouter/LFM3-1.7B-abliterated`](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated) | 1.73B | GATED | P0_RIGHTS_AND_CHECKPOINT_AUDIT |
| 2 | [`orcarouter/Nex-N2.5-mini-Uncensored`](https://huggingface.co/orcarouter/Nex-N2.5-mini-Uncensored) | 35.10B | GATED | P1_SOURCE_RIGHTS_AND_QUALITY_AUDIT |
| 3 | [`orcarouter/Flint-abliterated-GGUF`](https://huggingface.co/orcarouter/Flint-abliterated-GGUF) | 39.79B | GATED | P2_UNIQUE_LEARNING_VERIFICATION |
| 4 | [`orcarouter/OrcaCyber-Nano-1.0`](https://huggingface.co/orcarouter/OrcaCyber-Nano-1.0) | 未確認 | GATED | HOLD_TOTAL_AND_DISTINCT_TRAINING_UNVERIFIED |
| 5 | [`orcarouter/Ripple-65B-abliterated-GGUF`](https://huggingface.co/orcarouter/Ripple-65B-abliterated-GGUF) | 65.00B | GATED | P3_BF16_AND_COST_HOLD |
| 6 | [`orcarouter/Gemma-4-26B-A4B-it-Uncensored-FP8`](https://huggingface.co/orcarouter/Gemma-4-26B-A4B-it-Uncensored-FP8) | 25.81B | GATED | P2_PARENT_LICENSE_HOLD |
| 7 | [`orcarouter/OrcaSAQ-2-Cyber-27B-Uncensored-GGUF`](https://huggingface.co/orcarouter/OrcaSAQ-2-Cyber-27B-Uncensored-GGUF) | 27.78B | GATED | DUPLICATE_TRAINING_DO_NOT_ADD_AS_MODEL |
| 8 | [`orcarouter/LFM3-1.7B-abliterated-GGUF`](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated-GGUF) | 1.73B | GATED | DUPLICATE_TRAINING_DO_NOT_ADD_AS_MODEL |
| 9 | [`orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF`](https://huggingface.co/orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF) | 748.00B | GATED | HOLD_150B_EXCEPTION_UNVERIFIED |
| 10 | [`orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF`](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF) | 180.00B | GATED | HOLD_150B_EXCEPTION_UNVERIFIED |
| 11 | [`orcarouter/orcacyber-hy4`](https://www.orcarouter.ai/models/orca/orcacyber-hy4) | 未確認 | CLOUD_RESEARCH_TIER | MONITOR_NO_WEIGHT_MANIFEST |

**評価上の留意点**：
- **LFM編集版**：作者は単一H200、BF16、greedy、thinking disabled、ルールベース拒否判定で拒否率の大幅低下を主張する。これは**独立した能力維持・悪用性測定ではない**。親/編集原本/ライセンス・評価を固定してからCONDITIONAL採否を検討する。
- **Nex編集版**：配布者が35.1B、視覚を含む1026 tensorのうち122編集と説明。8×H100の作者条件と一般PC実行性能は別。重み全総数を**active expert数やファイル容量で代替しない**。
- **OrcaCyber Nano**：名称やdraft GGUF 2GBだけで小型の独立主モデルと誤判定しない。Qwen3.8 27Bを親とするGGUF＋vision projector＋draft の可能性を静的に調査し、独立学習成果と総数は不明のまま取得STOP。
- **DeepSeek 748B級・Qwen Flash Next 180B級**は150B以上で、現行[量子化同等メモリ例外](../../policies/limits.json)の**同一HW/backend/OS/ABI/context/batchで両モデル30回以上、全ピークRAM<512GB、150B未満の事前指定モデル以下、品質・速度・権利**の確認がないため購入／実行／取得を承認しない。
- クラウドAPI `OrcaCyber Hy4` は公開された同一重みファイルと正規取得権を証明しない。ローカルアーカイブに追加しない。

**法令は証拠と仮説に分ける**：[Hugging Face Gated](https://huggingface.co/docs/hub/models-gated) は配布者の承認制。[BIS 2026-11-16遠隔コンピュート管理](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology) と [EU AI Act第53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53) は、**ローカル公開ウェイト全体の一律所有禁止を示す資料ではない**。配布停止や規制の未来の確率は不明。高リスクだから無許可取得してよい、という推論は認めない。

## 4. 取得前の必須ゲートとH/T/D/C/U

**STOP**：`queues/approved.json`は現在0件。ユーザー本人による各モデルのGated承認、行為別LICENSE/親権利、source revisionとSHA、必要な他の学習済み依存、推論実装ABI/zero-point、実際のHDD容量・200GB空き・cache/staging、個別固定マニフェストのユーザー明示承認のいずれか未解決なら転送不可。新規ファイルの実取得、モデルのロード、未信頼コード実行は本作業で行わない。旧ledger VERIFIEDは完全offline restoreの証明ではない。

**H**：独立編集重み・学習済み原本の保存が、既存量子化との重複なく再構築オプションを増やす。**T**：17原本scopeの静的照合（n_min=17）・157有効の一意アクション（n_min=157）。許諾後の本人環境では全ファイルSHA、モデル実測は同一HW/clock/ABI/backend/量子化/バッチ・コンテキスト固定で最低30反復。権利違反や空き不足を検知したら逐次停止。**D**：PASS=17件排他12+2+2+1、157件一意、承認0を維持。FAIL=紛失ファイルをVERIFIEDと断定・巨大MoEをactive数で判定・Gatedの無許可取得。UNCERTAIN=実機hash、個人許諾、依存・ベンチ。**C**：メーカー編集結果が単なる量子化、台帳のownerファイルが不整合、法律/ライセンス条件が変化。**U**：実機の物理占有/転送cache、Gated個人権限、metadataの過不足、独立評価不足。合成不確かさ `u_c` と係数 `k` は確率分布未推定のため算定不可。

### 変数表と次元検査

| 記号 | 日本語の意味 | 単位(SI) | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_old` | 過去取得報告のsourceサイズ | byte（SI基本単位外） | 旧source scopeの全file bytes | 0以上、旧原本集合 | 整数スカラー |
| `B_new` | 新しい選択原本sourceサイズ | byte（SI基本単位外） | 新scopeのfile bytes合計 | 0以上、選択ファイル集合 | 整数スカラー |
| `ΔB` | 2つのscopeの容量差 | byte（SI基本単位外） | `B_new - B_old` | 物理重複除去後の転送量ではない | 符号付きスカラー |
| `N_total` | 全trained parameter個数 | 1（無次元） | inactive expertやMTPも含む全数 | 未知null/原則150Bスクリーン | 非負整数またはnull |
| `R_peak` | 全推論ピークメモリ | byte（SI基本単位外） | CPU/GPU/OS/KV/runtimeを含む（UMA二重計上除外） | 未測定はnull、厳密例外では512GB未満 | 非負整数またはnull |

**次元チェック**：差の両項は同じbyte単位なので `ΔB` はbyte。一方 `N_total` は無次元のパラメータ個数であり、GGUF容量やMoE active数を総数に読み替えない。

### ERROR CHECK

本作業のbaseline v51は管理204／有効157。17source＝12+2+2+1。全157資産の研究アクションと11件の新規Orca研究カードは非実行。旧ledgerの53 VERIFYは自己報告、物理再検査なし。新規正式採用0・承認0・モデル重量取得0。Exaは本日HTTP402、HF公式Repo metadataと既存Publisher原本sourceのみで検証し、網羅調査と称しない。

### 〈応用・転用例〉

モデル公開政策・著作権（合法な配布元）、デジタルフォレンジック（ハッシュと来歴）、ML評価（独立学習の比較）、システム/ストレージ設計（runtime依存と媒体安全床）の4軸で保存対象を絞る。

### 〈次に考える問い〉

**所有者Dドライブで差分SHAを検査したとき、実際に追加で取得する必要があるユニーク高精度原本は何バイトか。**
