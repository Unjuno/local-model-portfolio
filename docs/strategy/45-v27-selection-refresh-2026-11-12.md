# v27（173資産）全体選定再監査・最新候補差分（2026-11-12）

**非実行提案**。対象ブランチ `strategy/2026-11-03-01-risk`、固定基準 `3c434641041359c4844bafe9b941b4fcd66ddcb0`。現在の`catalog/CURRENT.json`、旧判断、承認キュー、ユーザーHDDを変更しない。本文の観測は11月12日に全173個の配布元が再確認されたことを意味しない。Exaはクレジット上限HTTP402、Hugging Faceモデル検索メソッドは未提供だったため、限定した公式配布ページと既存資料を利用。

## 1. 〈本論〉期間・現行状況

GitHub `main` の正式CURRENTはv19・150件だが、専用ブランチは**v27・173件（147モデル・26データ、126有効）**。SELECT53／CONDITIONAL73、HOLD28／延期13／EXCLUDED6。モデル総数不明20件のうち**有効7件**は取得準備を止める。150B以上量子化例外2件は検討HOLDで、同一実機条件の品質・RAM検証なし。GitHubの`queues/approved.json`は空で、現実のHDD上の既存保存量は未測定。

確認できるリポジトリ最初の仕様コミットは2026-10-30 00:12:09 JST、今回のブランチ先頭は2026-11-11 17:04:58 JST。**暦上12日16時間52分49秒**であり、実作業時間を推定する根拠はない。

## 2. 全173件の停止条件・再検証

全173件一意の資産IDについて、元の判断・固有能力の選定理由・一次URL・証拠の元確認日・旧S波・モデル総数・配布元repoの過去容量・調査優先度・反証条件を[機械可読全件表](../../catalog/proposals/04-v27-selection-refresh-2026-11-12.json)へ格納。**提案は現行SELECT/HOLD/EXCLUDEDを自動変更しない**。

| 分類 | 件数 |
| --- | ---: |
| P1_LEGAL_ACCESS | 24 |
| P3_UNIQUENESS_AND_FORMAT | 87 |
| H_HELD | 28 |
| P2_DEPENDENCY_CLOSURE | 8 |
| D_DEFERRED | 13 |
| P0_UNKNOWN_TOTAL_METADATA_ONLY | 7 |
| X_EXCLUDED | 6 |

総数不明で有効な7件は次のとおり。権利・他の条件を満たしていても、MoE全expertや外部学習済み部品の総数を確認できなければ最終lock不可。

1. `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`（conditional）
2. `Stuubs/Stubelius_Remix_Ltx2.5`（conditional）
3. `WhissleAI/steer-tts`（conditional）
4. `maya-research/maya2-native`（conditional）
5. `fishaudio/drama-3`（conditional）
6. `ausboss/Qwen-Image-2.1-Consistency-LoRA`（conditional）
7. `PrunaAI/P-H3-Image`（conditional）

旧規制研究は150B以上絶対除外、現行v27は**固定した150B未満比較モデルと同じHW/OS/backend/context/batchでピークRAMが同等以下、品質と速度も検証される量子化例外**という別の上位方針。両者を黙って統一しない。現時点で例外の取得承認はない。

## 3. 11月12日までの候補評価と既存との重複

| 新規または再調査 | 判断 | 既存の保全状態との比較 | 必須の次の検証 |
| --- | --- | --- | --- |
| [qvac/BotPsy-0.8B](https://qvac.tether.io/models/botpsy) | RESEARCH_PRIORITY_R1_NOT_IN_V27 | Qwen3.5-0.8B already selected, but BotPsy separately SFT/distilled/RL-trained for tool calling | exact HF repo revision, LICENSE complete text, tensors, hardware, incremental package SHA not independently checked |
| [ibm-granite/granite-timeseries-ttm-r3](https://huggingface.co/collections/ibm-granite/granite-time-series) | RESEARCH_PRIORITY_R2_NOT_IN_V27 | Tiny Time Mixer independent time series learning architecture vs selected autogluon/chronos-2 | exact checkpoint, terms, artifact bytes, dependent runtime |
| [NousResearch/Arete-27B](https://huggingface.co/NousResearch/Arete-27B) | RESEARCH_HOLD_LARGE_DUPLICATION | Distinct alignment SFT may be independent, but Qwen3.8 official and several edited 27B already selected | original license, revisions, independent task quality premium |
| [autotrust/AutoTrust-JEV-27B-v1.1](https://huggingface.co/autotrust/AutoTrust-JEV-27B-v1.1) | RESEARCH_HOLD_27B_TYPED_DECISION | Separate typed decision training; overlaps selected kakaocorp Kanana 3.665B and LiquidAI d1-omni | independent accuracy benefit vs extra storage, CPU/GPU, and full licence |
| [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | RETAIN_2026_11_11_RESEARCH_HOLD | undistilled source distinct from selected Pruna P-H3, multiple repo presentations not multiple learned models | region restricted licence, complete dependencies, immutable selected file set and duplicate elimination |

11月11日公開のBotPsyは、開発元による0.8B原精度1.73GB、Qwen3.5-0.8BからSFT/蒸留/RLを施した独立状態。ベンダーBFCL v4 44.0対23.4は**開発者測定**で、日本語・所有者ハードの再検証なし。IBM TTM R3は公式コレクションに存在するが、Chronos-2との同条件評価なし。Arete27BとAutoTrust27Bは独自の調整があっても単に54.7GB追加する根拠が弱くHOLD。

**再追加禁止**：すでにv28提案の`beipo-ai/NorthCUA-Mini`／`qiyuan-robot/PrimeSim`／`meta-models/Muse-Glimmer-30B`は独立提案に46ファイル、SHA重複排除後の既知145,004,061,364Bの監査がある。11月11日報告のUnderdog日本語Woof、LLM-jp-Moshi、BayLingも未採用の別レーンで追跡。PLaMo、Phonon、Kanana、Pruna P-H3はv27内に既存。

## 4. 容量・品質・開始条件

v27の**既知ソース論理集合**は3,417,685,712,585B。計画上限4,000,000,000,000Bとの差は582,314,287,415B。仮にフォーマット済みの空の4TBドライブであっても、空き200GBを維持した**机上余力は382,314,287,415B**。v28追加の既知増分145,004,061,364Bを仮置きすると237,310,226,051B。**実機容量、cache/staging、外部encoder/codec、現在既保存の重みを確認した数字ではない**。

| 変数 | 意味（日本語） | SI単位 | 定義・範囲・型・前提 |
| --- | --- | --- | --- |
| C | アーカイブ計画上限 | byte | 4e12、非負整数スカラー、実機値と区別 |
| Fmin | 取得後の実空き安全床 | byte | 2e11、非負整数スカラー、現物未測定 |
| Bknown | v27既知ソースのSHA重複除去後容量 | byte | 3417685712585、非負整数スカラー、完全復元ではない |
| Badd | v28未採用4repoの既知増分 | byte | 145004061364、非負整数スカラー |
| Factual | 実機の空きと一時コピーを含む余裕 | byte | null、測定前は不明、非負整数またはnull |

**次元チェック**：上の差は全てbyte同士の演算。パラメータ数は無次元であり、重みサイズ・RAMと混同しない。モデル性能は同じHW/clock/backend、ABI、量子化zero-point、context/batch、KV、30試行以上の条件固定が必要。未測定性能で採否確定しない。

**実行可能な次工程**：総数不明7件の静的確認→本人Gated権限・LICENSE→全学習済み依存とハッシュ→実HDD空き・staging実測→必要なら固定manifestを別途ユーザー承認。最初の取得テスト候補は既存の`elyza/ELYZA-tasks-100`約7.79MBと`autogluon/chronos-2`約477.94MB。ただし取得は未実施・未承認。

## 5. H / T / D / C / U と ERROR CHECK

H：特殊SFT/RL/画像・音声学習成果を残しながら、同一量子化・重複依存の保存費用を減らせる。T：全173の固定repoと小型新規2候補でSHA/訓練履歴/権利比較、推論は別承認・同条件30例以上。D：権利・完全ファイル・全依存・実機容量・本人承認が全てPASSなら取得審査可、明確な重複/禁止/容量不足はFAIL、それ以外UNCERTAIN。C：別のSFTだが性能差がなく追加コストに見合わない、codec/権利が欠ける。U：実機空きと最新ライセンス、独立品質値が不明、u_c・包含係数kは未算定。

**ERROR CHECK（静的）**：全173 ID一意、147モデル・26データ、126有効、総数未確認20（有効7）、150B以上例外2、元EXCLUDED6保持、GitHub approved=0。現在のカタログ選定変更0、新規取得・実行0。CIや所有者HDDチェックの完了は主張しない。

関連分野は機械学習の学習状態鑑定、デジタルアーカイブ、ソフトウェア供給網/ABI、知的財産・同意管理。

### 〈次に考える問い〉
新しい学習済みモデルを増やす前に、既存126のうち一つを完全な復元可能パッケージとして確定させ、何が実際の保存を妨げているか測定すべきではないか。

## 付録：v27全173資産の調査帯索引

| repo ID | 既存判断 | 元モデル数ゲート | 調査帯 |
| --- | --- | --- | --- |
| `orcarouter/Qwen3.8-27B-Uncensored` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `afdudley/Qwen3.8-27B-abliterated-NVFP4` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `orcarouter/Qwen3.8-Flash-Next-Uncensored` | hold | OVER_150B_QUANT_REVIEW_REQUIRED | H_HELD |
| `dphn/Dolphin3.0-Llama3.1-8B` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `knoveleng/Qwen3.5-9B-Uncensored` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `LiquidAI/LFM2.5-24B-A2B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `usezn/Galvanize-3` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `opus-research/opus-moderation-4-neo` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `microsoft/Fara1.5-27B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-Coder-Next` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `tencent/Hy-Memory-30B-A3B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `LiquidAI/LFM3-1.7B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `InstantX/InstantID` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `KlingTeam/LivePortrait` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `microsoft/VibeVoice-1.5B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `OpenMOSS-Team/MOSS-TTS-v1.5` | select | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `Plachta/Seed-VC` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `ResembleAI/chatterbox` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Edge0/Audio8-TTS-Realistic-Air` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `SWivid/F5-TTS` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `ByteDance/InfiniteYou` | deferred | UNVERIFIED_BLOCK_FINAL_LOCK | D_DEFERRED |
| `coqui/XTTS-v2` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `fishaudio/fish-speech-1.5` | deferred | UNVERIFIED_BLOCK_FINAL_LOCK | D_DEFERRED |
| `fishaudio/s2-pro` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `onnx-community/higgs-audio-v3-tts-4b` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `TencentARC/PhotoMaker` | deferred | UNVERIFIED_BLOCK_FINAL_LOCK | D_DEFERRED |
| `black-forest-labs/flux-3-image-klein-base` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `black-forest-labs/FLUX.2-dev` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `briaai/Fibo-2.0-dev` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `ideogram-ai/ideogram-4-nf4` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `black-forest-labs/flux-3-image-klein` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `black-forest-labs/FLUX.2-klein-9B` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `briaai/Fibo-2.0-edit-turbo` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `bytedance-research/Lance` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `Lightricks/LTX-2.5` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `Lightricks/LTX-2.3` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `Stuubs/Stubelius_Remix_Ltx2.5` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `OnomaAIResearch/Illustrious-XL-v1.1` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen-Image-2.1` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `Tongyi-MAI/Z-Image-Turbo` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Wan-AI/Wan2.2-TI2V-5B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Laxhar/noobai-XL-Vpred-1.0` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `StephaneBah/AfroRadVoice-FR` | conditional | NOT_APPLICABLE_TO_DATASET | P1_LEGAL_ACCESS |
| `amphion/Emilia-Dataset` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `bigcode/starcoderdata` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `bigcode/the-stack-v2` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `laion/relaion2B-en-research` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `lmsys/lmsys-chat-1m` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `allenai/WildChat-1M` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `CohereLabs/aya-vision-32b` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `meta-llama/Llama-4-Scout-17B-16E` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `allenai/Olmo-3-1125-32B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `IFM/K2-Horizon-0.9B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `google/gemma-4-31B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `ibm-granite/granite-switch-4.1-30b` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `LiquidAI/LFM3-Omni-2B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `mistralai/Mistral-Small-4-119B-2603` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Nanbeige/Nanbeige4.3-33B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `LiquidAI/LFM2.5-VL-3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `LiquidAI/LFM2.5-VL-3B-DSpark` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `openai/gpt-oss-120b` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-Omni-30B-A3B-Instruct` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `Qwen/Qwen3.5-35B-A3B-Base` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3.8-27B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `udgamlabs/Lilavati` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `udgamlabs/Lilavati-Checker` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `mistralai/Mistral-Large-4-1T-A52B` | hold | OVER_150B_QUANT_REVIEW_REQUIRED | H_HELD |
| `Nanbeige/Nanbeige4.3-33B-Base` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `EPFLiGHT/Meditron3-70B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `google/medgemma-4b-it` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `boltz-community/boltz-2` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `EPFLiGHT/fully-open-meditron` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `EPFLiGHT/OLMo-2-32B-MeditronFO` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `facebook/esm2_t33_650M_UR50D` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `HuggingFaceBio/Carbon-X` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `IFM/SFT-Reasoning` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `OctoMed/OctoMed-32B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `EPFLiGHT/Apertus-70B-MeditronFO` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `StanfordAIMI/CheXagent-8b` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `nvidia/Cosmos-Predict2-2B-Video2World` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D` | hold | NOT_APPLICABLE_TO_DATASET | H_HELD |
| `ACERobotics/Puffin-World` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `lerobot/pi0_base` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `lerobot/smolvla_base` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `microsoft/TRELLIS.2-4B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/GR00T-N1.6-3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `speridlabs/idol` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `tencent/Hunyuan3D-2.1` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `laion/emotional-roleplay-finetuning-dataset` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `m-a-p/MERT-v2-FullSong` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `m-a-p/SheetSage2` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `m-a-p/YuE2-3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `m-a-p/YuE2-Vae` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `nvidia/Granary-v2` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/OpenCodeInstruct` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/OpenMathInstruct-2` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `facebook/dinov3-vit7b16-pretrain-lvd1689m` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `facebook/dinov3-vith16plus-pretrain-lvd1689m` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `facebook/sam3` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `allenai/pixmo-cap` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `allenai/tulu-3-sft-mixture` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `answerdotai/ModernBERT-large` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `autogluon/chronos-2` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `BAAI/bge-m3` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `CohereLabs/aya_dataset` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `deepseek-ai/DeepSeek-OCR-2` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Edge0/Audio8-TTS-Realistic-0.6b` | hold | PASS_TOTAL_PARAMS_LT_150B | H_HELD |
| `elyza/ELYZA-tasks-100` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `facebook/vjepa2-vitg-fpc64-384` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `google/siglip2-base-patch16-224` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `GSAI-ML/iLLaDA-8B-Base` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `HuggingFaceFW/fineweb-edu` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `HuggingFaceH4/ultrafeedback_binarized` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `ibm-granite/granite-speech-5.0-2b` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `ibm-granite/granite-speech-5.0-470m-turboctc` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `lerobot/aloha_sim_insertion_human` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `lightonai/LightOnOCR-3-0.8B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `LiquidAI/d1-omni-600M` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `LiquidAI/LFM3-1.7B-Base` | conditional | PASS_TOTAL_PARAMS_LT_150B | P1_LEGAL_ACCESS |
| `llm-jp/magpie-sft-v1.0` | select | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/nemotron-labs-unified-asr-0.6b` | excluded | PASS_TOTAL_PARAMS_LT_150B | X_EXCLUDED |
| `openai/whisper-large-v3-turbo` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `PaddlePaddle/PaddleOCR-VL-1.5` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `PerceptronAI/Isaac-0.2-2B-Preview` | excluded | PASS_TOTAL_PARAMS_LT_150B | X_EXCLUDED |
| `qvac/TranscribePsy-250M-EU` | excluded | PASS_TOTAL_PARAMS_LT_150B | X_EXCLUDED |
| `Qwen/Qwen3-ASR-1.7B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-Embedding-0.6B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-Reranker-0.6B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3-VL-2B-Instruct` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Qwen/Qwen3.5-0.8B` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `RWKV/RWKV7-7.2B-20260805` | select | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `state-spaces/mamba-2.8b` | excluded | PASS_TOTAL_PARAMS_LT_150B | X_EXCLUDED |
| `tencent/Hy-SimulMT-30B-A3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `Wigtn/KoGovDoc-Bench` | excluded | NOT_APPLICABLE_TO_DATASET | X_EXCLUDED |
| `Wigtn/Qwen3-VL-2B-WigtnOCR` | excluded | PASS_TOTAL_PARAMS_LT_150B | X_EXCLUDED |
| `inclusionAI/Ming-3.0-tts-0.5B` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `lightonai/LightOnOCR-3-4B` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `m-a-p/MERT-v2-30s` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `nvidia/Nemotron-Cascade-2-30B-A3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/Nemotron-Cascade-2-RL-data` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/Nemotron-Cascade-2-SFT-Data` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `orcarouter/Qwen3.8-27B-Uncensored-FP8` | deferred | PASS_TOTAL_PARAMS_LT_150B | D_DEFERRED |
| `Hcompany/Holo4-27B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `WhissleAI/steer-tts` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `maya-research/maya2-native` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `Hcompany/trajectories` | conditional | NOT_APPLICABLE_TO_DATASET | P3_UNIQUENESS_AND_FORMAT |
| `Louis0324/StyleStream` | hold | UNVERIFIED_BLOCK_FINAL_LOCK | H_HELD |
| `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `fishaudio/drama-3` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `PrentisAI/GroundGUI-8B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `ausboss/Qwen-Image-2.1-Consistency-LoRA` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `Hcompany/Holotron4-30B-A3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `LiquidAI/LFM2.5-24B-A2B-DSpark` | conditional | PASS_TOTAL_PARAMS_LT_150B | P2_DEPENDENCY_CLOSURE |
| `pfnet/plamo-3-translate-31b` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `pfnet/plamo-3-translate-0.8b` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `nvidia/Cosmos3-Nano-Sim-Bimanual` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `PrunaAI/P-H3-Image` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | P0_UNKNOWN_TOTAL_METADATA_ONLY |
| `nvidia/Cosmos3-Nano-Sim-Auto` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `gradium/phonon-31m-en` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `gradium/phonon-40m-multilingual` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |
| `kakaocorp/kanana-2-v-decide-3b-2611` | conditional | PASS_TOTAL_PARAMS_LT_150B | P3_UNIQUENESS_AND_FORMAT |