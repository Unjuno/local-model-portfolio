# R107｜v45のダウンロード対象確定：12原本のファイル選定と無検閲・特殊モデルの取捨（2026-11-18）

> **状態：保全する原本とファイル選定の研究確定であり、取得承認ではない。** 実行可能な `queues/approved.json`、正本の `catalog/CURRENT.json`、HDD、モデル重み、第三者コードは変更していない。すべての取得対象に個別権利・ローカル空き・依存・本人承認の停止ゲートが残る。

基準：`Unjuno/local-model-portfolio` の **v45-20261118（198登録、151有効）**。基準mainコミット：`e1fe20e83c23e075dacdf56c39d519046c1387ea`。今回の選定結果を記録した非実行JSONは [R107全件台帳](../../catalog/proposals/2026-11-18-r107-download-selection.json)。既存の[元10モデルの出版社source台帳](https://github.com/Unjuno/local-model-portfolio/blob/e1fe20e83c23e075dacdf56c39d519046c1387ea/manifests/drafts/v45-2026-11-18-r106-first10-publisher-source.candidate.json)、[RFD4の12ファイル](https://github.com/Unjuno/local-model-portfolio/blob/e1fe20e83c23e075dacdf56c39d519046c1387ea/manifests/drafts/r106-v45-rfd4-pretrain-plus-merged-original.candidate.json)、[ZONOS3の20ファイル](https://github.com/Unjuno/local-model-portfolio/blob/e1fe20e83c23e075dacdf56c39d519046c1387ea/manifests/drafts/r106-v45-zonos3-native-original.candidate.json)を、同一の内容・バイト数のまま集約する。

## 1.〈本論〉— 実際に残すべき重みの選定規則

目的は、規制・削除・配布者の経営方針に左右されにくく、**権利に適合した固定revision・モデル重み・学習済み依存・実行コードと再現情報を後から再構築できる状態**を作ること。単に新モデルを数多く保存したことや、強いモデルだけを集めたことを成果としない。

三つの独立レーンを使う。

1. **失ったら再現できない学習成果**：元重み、特殊SFT/RL、拒否方向編集、独立した音声/動画/ロボット/量子誤り訂正/科学モデルと、その修正差分。容量あたりの固有性を重視する。
2. **低コスト高実用性**：OCR・ASR・埋め込み・再順位付け・予測など、単独または小さな閉包依存でオフライン業務に転用できる原本。速度や品質はメーカー測定と独立評価を分離する。
3. **再現とコンプライアンス**：LICENSE正文、Gated本人承認、全学習済みCodec/Encoder、40桁revision、出版社SHA/整数byte、実際のHDD空き・権限・ランタイム、明示的な取得承認を**他の高い性能スコアで補償しない**。

現行`main`の150B超量子化例外は、本人の同条件HW/backend/コンテキスト/バッチで品質・メモリが確認されて初めて審査するもの。MoEは全expert・MTP/埋め込みを含む**全パラメータ数**で評価し、active数を流用しない。モデル全総数が不明なら重み取得準備停止。今回の第1原本12件は通常の150B閾値以下として研究上の候補になっているが、完全ランタイムと補助学習重みの審査は未了。

## 2. 第1保存候補として**原本と選択ファイルを確定**した12件

**判定：`ORIGINAL_SOURCE_SELECTED / OWNER_RIGHTS_AND_RUNTIME_PENDING`**。既存v45有効モデルから選び、作者の40桁固定コミット、候補ファイルパス、整数byte、重みLFS SHA256またはGit blob IDの出版社証跡を保存。モデル本体をダウンロードしたわけではない。

| 順 | 元の配布者の固定revision | 選択files | ソース候補容量 (GB, 十進) | revision冒頭 | ライセンスタグ（正文未審査） |
|---:|---|---:|---:|---|---|
| 1 | [`abel-lab/Simons-297M`](https://huggingface.co/abel-lab/Simons-297M/tree/335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a) | 6 | 1.189 | `335dc22e4ce2…` | openmdw-1.1 |
| 2 | [`KRAFTON/Raon-1-nano`](https://huggingface.co/KRAFTON/Raon-1-nano/tree/39f897a1f835c723ec633c6c905dca7312bd9fd7) | 17 | 7.182 | `39f897a1f835…` | apache-2.0 |
| 3 | [`autogluon/chronos-2`](https://huggingface.co/autogluon/chronos-2/tree/60088152a34e242427b44c3100014473a0157d53) | 4 | 0.478 | `60088152a34e…` | apache-2.0 |
| 4 | [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/tree/97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3) | 12 | 1.207 | `97b0c614be4d…` | apache-2.0 |
| 5 | [`Qwen/Qwen3-Reranker-0.6B`](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B/tree/e61197ed45024b0ed8a2d74b80b4d909f1255473) | 14 | 1.207 | `e61197ed4502…` | apache-2.0 |
| 6 | [`google/siglip2-base-patch16-224`](https://huggingface.co/google/siglip2-base-patch16-224/tree/75de2d55ec2d0b4efc50b3e9ad70dba96a7b2fa2) | 9 | 1.539 | `75de2d55ec2d…` | apache-2.0 |
| 7 | [`ibm-granite/granite-speech-5.0-470m-turboctc`](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc/tree/91dcb0605daf65f88dbb04fef015c423241d941d) | 9 | 0.948 | `91dcb0605daf…` | apache-2.0 |
| 8 | [`lightonai/LightOnOCR-3-0.8B`](https://huggingface.co/lightonai/LightOnOCR-3-0.8B/tree/36d8636925327c671bd8e479c517a004f7566bd9) | 14 | 1.736 | `36d863692532…` | apache-2.0 |
| 9 | [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base/tree/5e8d12a6e2975b0e5e5fce7c8caf47c371d257b6) | 9 | 0.907 | `5e8d12a6e297…` | apache-2.0 |
| 10 | [`openai/whisper-large-v3-turbo`](https://huggingface.co/openai/whisper-large-v3-turbo/tree/41f01f3fe87f28c78e2fbf8b568835947dd65ed9) | 13 | 1.622 | `41f01f3fe87f…` | mit |
| 11 | [`nvidia/RFD4-Proteina`](https://huggingface.co/nvidia/RFD4-Proteina/tree/5ec66c399bf0b48727ab24e6b298dcf33864fa07) | 12 | 3.494 | `5ec66c399bf0…` | bsd-3-clause |
| 12 | [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini/tree/2921b8821772b0bd10a04456863d21abf9d2f283) | 20 | 15.335 | `2921b8821772…` | apache-2.0 |
| **計** | **12モデル** | **139** | **36.845** | — | **取得承認0** |

**これらの意味**：12の独立学習済みチェックポイント/保存パッケージについて、どのファイルを取るかを出版社メタデータの範囲で定義できた。139の参照全てに`bytes`、`path`、上流で判明している同一性ハッシュを記録し、不明な個別SHA-256はnullとした。**取得後のローカルSHA-256一致、学習済みの完全依存、コードの安全なオフラインロード、本人の権利は検証していない**。

RFD4-Proteinaは配布元repoの約107.08GBを無条件にコピーせず、merged flow+AE、独立Base、LoRAなど12ファイル約3.494GBに絞った。ただし別の抗体学習成果があれば同一重みと決めつけない。ZONOS3-Miniは約30.918GBのrepoから、元LM、ZAC-1 Codec、学習済みdecoder二種、speaker encoder、編集LoRA等を20ファイル約15.335GBに絞った。GGUF・WebGPUの同一重み変換を重複追加しない。ZONOSの`.pth`はpickle実行の懸念があるため、保存対象のファイル選択と安全なデシリアライズを分離する。

**容量の重要な注意**：これら12件はv45の151有効選定**に既に含まれている**。新たに36.845GBを保存計画に足すのではない。

## 3. 第2のファイル確定対象：無検閲・特殊・高価値モデル

次の20件は既存有効選定から先に調べる対象。取得を今すぐ許可する意味ではない。**同系の複数量子化を全部買い足す/保存するのではなく、元の独立学習重みと1つの必要な形式を比較して選ぶ**。

| 優先 | 対象 | 次の判断 | なぜその原本なのか・条件 |
|---:|---|---|---|
| 1 | [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | `RIGHTS_FIRST` | Independent BF16 refusal-direction edited multi-modal original; gated publisher; Qwen parent alone does not recover modified source. |
| 2 | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | `COMPARE_ORCA_NOT_BOTH_UNPROVEN` | Public Q4_K_M + F16 vision projector; compare exact training/weight provenance with Orca and Heretic before reserving both. |
| 3 | [`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2) | `SOURCE_LICENSE_AUDIT` | Gemma4 MoE reasoning/creative posttraining checkpoint; architecture and training path distinct from Qwen uncensored. |
| 4 | [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | `NONCOMMERCIAL_RIGHTS_AND_PARENT_FIRST` | Different rank-128 trained adapter; official original 671 MB with SHA256SUMS; requires pinned Qwen-Image-2.1 base and upstream noncommercial research agreement. |
| 5 | [`Qwen/Qwen-Image-2.1`](https://huggingface.co/Qwen/Qwen-Image-2.1) | `PIN_SHARED_BASE_ONLY_ONCE` | Trained base for Qwen-Image-2.1 LoRAs; shared weights should not be acquired per adapter. |
| 6 | [`higurashi-ai/Haru-4B`](https://huggingface.co/higurashi-ai/Haru-4B) | `PIN_NEXT` | Independent full-duplex voice dialogue with speech/text joint training; source ~10.56GB, distinct from standard ASR and TTS. |
| 7 | [`microsoft/Fara1.5-27B`](https://huggingface.co/microsoft/Fara1.5-27B) | `PIN_NEXT_IF_CAPACITY` | Original GUI agent posttraining with observed ~54.74GB source; speed/capability claims require independent fixed-HW tests. |
| 8 | [`nvidia/Ising-Decoder-ColorCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | `GATED_RIGHTS_FIRST` | Original specialist quantum code decoder; only ~6MB repo, but personal Gated grant cannot be assumed. |
| 9 | [`nvidia/Ising-Decoder-SurfaceCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | `GATED_RIGHTS_FIRST` | Different quantum code, not a quantization copy of ColorCode; repo ~2MB; requires official gate permission. |
| 10 | [`nvidia/Kumo-Tabular`](https://huggingface.co/nvidia/Kumo-Tabular) | `PIN_NEXT` | Small separate tabular foundation learning, not another general LLM or ASR. |
| 11 | [`microsoft/TRELLIS.2-4B`](https://huggingface.co/microsoft/TRELLIS.2-4B) | `PIN_NEXT_IF_CAPACITY` | Generative 3D reconstruction representation distinct from Idol; source ~16.24GB, learned VAE dependencies additional. |
| 12 | [`Wan-AI/Wan2.2-TI2V-5B`](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | `PIN_NEXT_IF_CAPACITY` | 5B original image/text to video; ~34.20GB publisher repo; do not assume external text encoders included. |
| 13 | [`runwayml/praxis-1-droid`](https://huggingface.co/runwayml/praxis-1-droid) | `GATED_RIGHTS_AND_CAPACITY_FIRST` | DROID-specialized action+video policy, distinct from general language models; ~54.4GB source and Gated rights. |
| 14 | [`XiaomiRobotics/Xiaomi-Robotics-U0-4B`](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B) | `DEPENDENCY_SAFETY_FIRST` | Trained robot action model and external vision tokenizer; source ~10.18GB plus pretrained dependency rights. |
| 15 | [`Lightricks/LTX-2.5`](https://huggingface.co/Lightricks/LTX-2.5) | `GATED_PARENT_LICENSE_FIRST` | Original video generation model; source availability and non-commercial restrictions must be cleared before derived variants. |
| 16 | [`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | `BLOCK_TOTAL_AND_LICENSE` | Separately edited video model, but unknown total learned components and HF metadata unknown license: no file preparation. |
| 17 | [`Qwen/Qwen3-Coder-Next`](https://huggingface.co/Qwen/Qwen3-Coder-Next) | `KEEP_HIGH_VALUE_BUT_DEFER_159GB` | Distinct coding MoE original; large source ~159.38GB competes with tight physical free space. |
| 18 | [`nvidia/Cosmos3-Nano-Sim-Bimanual`](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Bimanual) | `PIN_AFTER_REAL_HDD_CHECK` | Independently trained action-conditioned world model (robot bimanual video); ~31.83GB source. |
| 19 | [`Hcompany/Holo4-27B`](https://huggingface.co/Hcompany/Holo4-27B) | `COMPARE_FARA_GUARDRAILS` | Agentic model checkpoint; compare to Fara before storing redundant same-purpose 27B original. |
| 20 | [`LiquidAI/LFM3-1.7B-Base`](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | `PIN_NEXT` | Distinct LFM recurrent/hybrid base checkpoint for future fine-tuning, unlike instruction-only releases. |

### 3.1 無検閲モデルの具体的取捨

- **27B LLM原本**：[OrcaRouter Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) のBF16編集済み原本を研究上の第一候補に置く。約55.586GB（配布元全量）、Gated。親`Qwen/Qwen3.8-27B`とは重みが一致せず、単なるQ4への変換でもない。**本人がGated許諾を持つか未確認なので取得停止**。公開されている[InterpreticAI Q4 GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)は同一原本のミラーとは確認できず、別版として学習差分と必要ファイルを検証し、無条件に2本とも選択しない。
- **小型の無検閲LLM**：[xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic)を**v45外の優先研究候補**とする。HF記載は約9.41Bで、系譜は`Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B`の派生で**元アーキテクチャはQwen3.5**。DeepSeek社の原版重みと誤って登録しない。作者のHeretic v2による100件拒否試験3/100と親100/100は**作者の拒否評価**であり、総合性能・安全性の独立実証ではない。正式追加の前に版固定・必要シャード・親ライセンス・同条件の通常タスク性能を照合する。
- **画像の無検閲後学習**：[ChatR Labs Omni-LoRA v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1)は、`Qwen/Qwen-Image-2.1`のrank128・step32,000の別学習済みBF16アダプター（作者記載約671MB）。元画像Baseとの重複ファイルを取らず、差分LoRAを1個と親の不変バンドルを確認する。**Qwen Research Licenseで非商用研究/評価に限る**ため、単に名前がUncensoredだから自由な実用保存と解釈しない。作者による判定で一般SFW画像品質は元Baseより低下しており、悪用可能性と高品質は同義ではない。
- **動画の無検閲後学習**：[ChrisColeTech LTX2.5 FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8)は候補の独自性を調査するが、HFライセンスタグはunknown、主DiT以外の学習済みエンコーダ等の全総数が未確定。**権利・総数の二重STOP**。類似[Stuubs Remix](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)とのモデル差分も未確定のため、まとめて取得しない。

### 3.2 重複・追加容量の検討を先送りした5モデル

| 既存有効モデル | 現状の合理的判断 |
|---|---|
| `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | Compared to Orca BF16 and Interpretic Q4. Same parent Qwen; additional learned changes and quality improvement not yet proven. |
| `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | Distinct voice design task vs Base, but multiple Qwen TTS variants should compete for capacity with Haru and ZONOS native rather than all prioritized together. |
| `LiquidAI/LFM2.5-VL-3B-DSpark` | Draft speculative head should be archived only with compatible parent and exact executable backend, not automatically a standalone general VL model. |
| `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU` | Author describes another independently trained Qwen 27B edit; cannot take every near-size 27B before same-task evaluation. |
| `meta-models/Muse-Glimmer-30B-assistant` | Separate adapter/assistant addition must be validated as trained difference and source scope before double-counting with Muse-Glimmer-30B. |

**今回の正式な採否変更は0件**。これらは元の`select`/`conditional`を維持したまま、取得ファイル準備順位を下げている。独立学習重みの同一性や品質を検証せず「不要モデル」と断定し、既存カタログから即削除しない。

## 4. 151有効資産への全件判定と容量上限

[全151件の個別保全判定・優先区分・取得停止要因](../../catalog/proposals/2026-11-18-r107-download-selection.json)を出力している。

| 状態 | 件数 | 意味 |
|---|---:|---|
| `F0_FIXED_SOURCE_SELECT` | 12 | 出版社の固定版・ファイル選択を研究上確定。未承認 |
| `F1_FOLLOWUP_MODEL_SELECT` | 19 | 次に原本固定、容量と権利を審査 |
| `F2_RETAIN_EXISTING_RESEARCH` | 106 | 既存v45を保全候補として維持 |
| `F3_DUPLICATE_OR_RUNTIME_COMPARE` | 5 | 近接ファミリー/追加価値の比較が先 |
| `HOLD_UNKNOWN_TOTAL` | 8 | 150Bの全学習済み総数を立証できない |
| `HOLD_UNKNOWN_TOTAL_AND_LICENSE` | 1 | 総数と独自利用条件の両方未確定 |
| **合計** | **151** | **実行可能な承認キュー0** |

ソース容量は既存[全151件のR106容量監査](https://github.com/Unjuno/local-model-portfolio/blob/e1fe20e83c23e075dacdf56c39d519046c1387ea/docs/strategy/106-v45-151-active-capacity-reconciliation-2026-11-18.md)の**3,732,164,752,962byte**を変更しない。最低空き200GBを差し引いた代理余白は**67,835,247,038byte**。これは選択された全ファイルの真の完成容量ではない。外部Codec/Encoderやstaging、実際のHDD使用量を加えるまで新規50GB級の追加枠とみなせない。

## 5. 取得承認に進むための変数表と単位監査

| 記号 | 意味（日本語） | SI単位 | 定義（範囲・前提） | 型 |
|---|---|---|---|---|
| `N` | ファイル選定済みモデル | 1（件） | 12、現行151の部分集合 | 非負整数スカラー |
| `F` | 選択された論理ファイル参照 | 1（件） | 139、同じ内容でも必要パスは別に数える | 非負整数スカラー |
| `B_s` | 固定済み配布元source容量 | byte | 36,845,228,483、追加依存と実際の物理容量を含まない | 非負整数スカラー |
| `B_p` | 151件の暫定source代理容量 | byte | 3,732,164,752,962、非最終値 | 非負整数スカラー |
| `B_c` | 保存計画上限 | byte | 4,000,000,000,000 | 非負整数スカラー |
| `B_f` | 最低空き容量 | byte | 200,000,000,000、実測未了 | 非負整数スカラー |
| `B_h` | 代理上の空き余裕 | byte | `B_c-B_f-B_p` | 整数スカラー |
| `N_t` | 学習済み総パラメータ数 | 1（無次元） | 全MoE expert/埋め込み/MTP、依存は別途精査。未知はnull | 非負整数またはnull |
| `M_p` | 推論ピークRAM | byte | 重み＋OS＋KV＋バックエンド作業領域。HW/精度/文脈・バッチ固定 | 非負実数またはnull |

したがって、`B_h = B_c - B_f - B_p = 67,835,247,038 byte`。同じ単位byteの加減算のみで整合する。`N_t`は無次元で、GGUF/NVFP4のバイト数を直接代入できない。量子化後に重み容量が小さくなっても**総パラメータ数や推論ピークRAMが同じ数値になるわけではない**。実機テスト条件はCPU/GPU型式、ドライバ、CUDA/Metal等、クロック、量子化zero-point、batch/context、KV cache、SSD offloadを固定してから比較する。

## 6. H / T / D / C / U・反証可能性

**H（仮説）**：独立原本と1つの実用形式に限定すれば、同族量子化を多数保存するより、低容量で多くの再現困難な能力を確保できる。ただしモデル別の規制確率を推定したのではない。技術の提供制限は権利/規制/企業判断を別事象として観測する。

**T（最小検証）**：固定済み12ソースの139ファイル、完全40桁revision、各整数byte・Publisher LFS SHA256（ある場合）を照合。次の20件は本人許諾、ライセンス、MoE全総数、実行依存に対する停止判定を先に行う。151有効IDを1回全数照合（n_min=151）。速度・品質の比較は最低30同条件入力、HW/clock/batch/contextを固定し中央値とばらつきを記録。今回はモデルロード・ベンチ実施0回。

**D（PASS/FAIL/UNCERTAIN）**：PASSは静的な12ソース・139参照・36,845,228,483byte・151一意ID・承認0・元のv45維持が矛盾しないこと。FAILは、署名されていない取得、ライセンスの無視、別revisionの混在、未知総数を0として取得、実機空き不足でも強行すること。UNCERTAINは本人の利用資格・完全依存・HDD・復元・品質。

**C（対立仮説）**：見かけ上独自のファインチューニングが実際には再量子化しただけ、独自音声/画像Encoderの保存を忘れた、旧LICENSEや削除義務が成立する、学習済みadapterが元Baseと非互換、学習済み総数が閾値を超える等。

**U（不確かさ）**：出版社元情報の更新、LICENSE適用範囲、個人アクセス、補助Codec、元重みの実ハッシュ、HDDの物理容量、デコードバックエンドABIが主誤差源。サンプル分布を作れないため規制の数値確率、合成標準不確かさ`u_c`、拡張係数`k`は算出しない。

## 7.〈応用・転用例〉— 保全を実行可能にする分野横断

- **デジタルアーカイブ**：学習済み重みをSHAと固定revisionで記録し、同一モデルの量子化変換と異なる学習済み成果を区別。
- **ソフトウェア供給網**：`trust_remote_code`、pickle、依存wheelhouse、CUDA/PyTorch ABI、NOTICE、不要な外部アクセスを分離監査。
- **AI法政策・権利処理**：モデル別Gated・非商用ライセンス、学習データの二次利用・削除申請、政策の対象者/行為の法域を調査。
- **計算機アーキテクチャ・評価**：低bit実測と元モデル総数を別評価し、ローカルHWで独立性能比較を可能にする。

政策の一次情報：[中国2026年10月第48号公告](https://www.mofcom.gov.cn/zwgk/zcfb/art/2026/art_0a31a3c9ac404f7a9b0e917ce3412997.html)は輸出目録の提案と一部技術の暫定輸出前登録を区別、[米BIS 2026年11月の規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は高度チップ/サーバーへの遠隔アクセスを対象、[EU GPAI公式FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は条件付きオープンソース例外を定める。いずれも「日本の全公開ウェイトのローカル保存が即座に違法」という根拠ではない。

### ERROR CHECK

- **検算済み**：v45有効151件の重複IDなし／保全区分151件に一意割当／12原本、139選択パス、36,845,228,483byte。選択ファイルのバイト和を各モデル・全体で再計算した。
- **未実施**：モデルのダウンロード、ユーザー端末HDDの計測、モデルコードの実行、LICENSE行為別最終承認、発行元SHAとローカルSHAの照合、実運用品質評価。重み取得承認0。
- **変更範囲**：専用ブランチの非実行R107成果物のみ。`main`、`CURRENT.json`、`queues/approved.json`、既存モデルのSELECT/CONDITIONAL/HOLDを更新しない。

## 8.〈次に考える問い〉

**次の1回の作業で、元重みを一切取得せずに突破できる停止ゲート（ライセンス正文、Gated本人許可、元checkpointの完全SHAなど）のうち、どれが最大数の独立原本をダウンロード承認候補へ進められるか。**
