# R84：v36・191資産の目的適合性と取得阻害要因の独立監査（2026-11-15）

## 1. 目的と判断

リポジトリの目的は**強力で代替困難な学習済み原本・専門データ・再現に必要な依存を、正規の権利と検証可能なファイル同一性を満たして長期保存すること**。公開停止・Gated化・ライセンス改定の可能性はストレスシナリオであり、特定モデルの禁止確率を捏造しない。今あるv36は191資産（モデル165、データ26）、有効144（select53、conditional91）。モデル本体の取得・オフライン復元・承認はいずれも0件で、**選定の増加を保存成果と数えない**。

**結論**：現時点で根拠のない交換・削除・新規追加をしない。まず現行144件の取得準備のボトルネックを**9件の総数未確認、18件の利用者Gated権限、115件の固定ソース不足、2件の実HDD事前検証**に分ける。これは互いに独立した唯一の「最初の阻害要因」の分類で、別の阻害要因が消えたという意味ではない。機械可読全件は[研究判断JSON](../../catalog/research/2026-11-15-r84-v36-144-purpose-and-blocker-triage.json)。

## 2. 確認済みの資産判断と交換しない理由

| 対象 | 判断 | 具体的根拠・次の検証 |
| --- | --- | --- |
| [NVIDIA Ising ColorCode](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) と [SurfaceCode](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | **両方CONDITIONAL維持** | v36作者のモデルregistryは異なる符号幾何・学習済みCNNを示す。単なる量子化違いではない。Gated匿名401のため重みを取得したとはしない。[固定原本比較](83-v36-original-ising-qec-source-selection-2026-11-15.md) |
| [Kumo Relational](https://huggingface.co/nvidia/Kumo-Relational)／[Tabular](https://huggingface.co/nvidia/Kumo-Tabular)／[Anomaly](https://huggingface.co/nvidia/Kumo-Anomaly) | **3件CONDITIONAL維持、取得準備は個別STOP** | 既存v33-v34では関係データ予測、単一表分類・回帰、異常検知という異なる学習目的。Relational/Anomalyは総パラメータ未確定のため、構造やファイル形式を確認するまで取得準備不可。 |
| [Muse Glimmer原本](https://huggingface.co/meta-models/Muse-Glimmer-30B)／[別学習DFlash](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant) | **2件CONDITIONAL維持** | v35の原本と学習済みdraft assistantは異なる役割。通常のGGUF/FP8変換を別学習成果として重複登録しない。[v35監査](82-v35-muse-original-and-dflash-formal-selection-2026-11-15.md) |
| [InterpreticAI Qwen3.8 Uncensored GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | **CONDITIONAL維持、取得未承認** | v36 R83で選択バイト17,738,327,225を記録。ただし実HDD・本人の承認・ローカルSHAと復元は未検証。元モデルとビット同一とは認定しない。 |
| [chatrlabs Qwen-Image 2.1 Omni LoRA](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | **CONDITIONAL維持、取得未承認** | v36 R83で選択バイト671,173,375を記録。親モデルや利用権、HDD・復元の独立ゲートを残す。 |
| [Nemotron-3.5-Parse](https://huggingface.co/nvidia/Nemotron-3.5-Parse) | **新規追加しない** | v36でLightOnOCR-3/PaddleOCR-VLとの用途重複を認識。別学習原本というだけで追加せず、定量的な非重複タスク成功・容量・権利の差が得られるまで保留。 |
| [Mistral Large 4](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B)／[OrcaRouter Flash Next](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | **現行HOLD維持・取得不可** | v36は150B以上について従来の絶対除外から「量子化で実用改善・特別な学習成果・実機性能と権利が立証された場合のみ個別再検討」へ変更。両モデルはその要件未充足で、重み取得は認めない。 |

**注意**：v9の「150B以上は絶対除外」はv12以降の現行ポリシーでは変更済み。古い制約を現行v36へ無断復元しない。一方、量子化だけを理由に150B超を自動採用することもない。

## 3. R83の144件から導く実務順

| 最初の停止要因 | 件数 | 最小の次作業 | 合格条件 |
| --- | ---: | --- | --- |
| 総パラメータ不明 | 9 | 同一revisionの公式config・全tensor・別学習済み依存の範囲を静的に検証 | 全モデル総数が確定し現行ポリシーに適合する |
| Gatedの本人権限 | 18 | 利用者本人が公式配布元でアクセス権・条項を確認 | 権限と利用条件を個別に記録（秘密情報は公開しない） |
| 固定ソース集合不足 | 115 | 配布者の40文字revision、必要ファイルallowlist、バイト、SHA、LICENSE、依存を確定 | 同じ版で再取得可能な非実行manifest候補ができる |
| 実HDD事前検証 | 2 | 本人の物理ドライブ・実空き・作業領域を読み取り専用で測定 | 4TB計画・200GB安全余白・既存ファイルを含む実測に合致 |

**実行条件**：推論ピークRAM512GB未満の測定、backend・ABI・量子化zero-point・KV・context・batchの明示、モデル本体/依存の権利確認、SHA-256、ユーザーの明示的な取得承認を別に要する。R83で選択バイトが確定した2件も**ready_to_approve=0**である。

## 4. Exa・政策動向の証拠制約

2026-11-15にExaで最新の政府・配布元・モデル公開動向を検索しようとしたが、**APIはHTTP 402（credits exhausted）で検索結果を取得できなかった**。この監査は現行v36のGitHub一次記録の再集計であり、11月15日の新規規制発表や公開停止を確認したと主張しない。以前の調査にある[EU AI Act原文](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)、[Hugging Face Gated公式文書](https://huggingface.co/docs/hub/en/models-gated)は背景資料。Gated表示、法的な配布禁止、個別の契約、将来の予測は別カテゴリーとして監査する。

## 5. 検証設計と変数表

| 記号 | 日本語の意味 | SI単位 | 定義 | 定義域・前提条件 | 型 |
| --- | --- | --- | --- | --- | --- |
| N | 有効選定の件数 | 1（件） | v36のselect＋conditional | 非負整数、今回は144 | 整数スカラー |
| B | 固定済みの選択ファイルバイト | byte | R83で記録された選択ファイル量 | 0以上整数またはnull、nullは0ではない | 整数スカラー/null |
| F | 最初の阻害要因別件数 | 1（件） | R83のfirst_blocker別資産数 | 非負整数、各資産は一意の分類 | 整数スカラー |
| L | 現行保存予算 | byte | 4,000,000,000,000 | 論理上限、実容量ではない | 整数スカラー |

**次元チェック**：Fの合計は9＋18＋115＋2＝144件でNと一致。BとLはbyteで比較可能だが、B=nullの142件を0とみなして総容量を確定してはいけない。例：上記2件の選択済みファイル容量は17,738,327,225＋671,173,375＝18,409,500,600 byte。ただしこれは全依存・作業領域を含む総必要量ではない。

**H**：固定ソース不足115件に対する公式のファイル列挙を先に行うと、14日間で少なくとも10件の新しい完全allowlistを作れる（取得承認は別）。**T**：同一revisionと上流APIを確認し、最低10件、二重計上なし、7日目に中間停止判定。**D**：10件以上でPASS、10件未満でFAIL、上流API/権限のため検証不能ならUNCERTAIN。**C**：LICENSEや外部依存が主因となり、ファイル列挙だけでは完全allowlistが成立しない。**U**：配布元API変動・Gatedアクセス・外部学習済み依存・repo容量差。測定分布未確定で合成標準不確かさu_cと包含係数kは未算定。

## 6. 全144件の決定・停止表

この表は**正式採否を変更しない**。各資産の初回停止要因を確定し、既存の学習済み原本と単なる量子化重複の区別を検証する作業順である。

| # | repo ID | 現行採否 | 総パラメータゲート | 今行う作業 | 選択バイト | 最初の停止要因 |
| ---: | --- | --- | --- | --- | ---: | --- |
| 1 | `orcarouter/Qwen3.8-27B-Uncensored` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 2 | `InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF` | conditional | PASS_TOTAL_PARAMS_LT_150B | OWNER_HDD_PREFLIGHT_ONLY | 17738327225 | OWNER_HDD_ACTUAL_CAPACITY_AND_STAG… |
| 3 | `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 4 | `Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 5 | `LiquidAI/LFM2.5-24B-A2B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 6 | `usezn/Galvanize-3` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 7 | `microsoft/Fara1.5-27B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 8 | `Qwen/Qwen3-Coder-Next` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 9 | `tencent/Hy-Memory-30B-A3B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 10 | `LiquidAI/LFM3-1.7B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 11 | `KlingTeam/LivePortrait` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 12 | `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1` | conditional | PASS_TOTAL_PARAMS_LT_150B | OWNER_HDD_PREFLIGHT_ONLY | 671173375 | OWNER_HDD_ACTUAL_CAPACITY_AND_STAG… |
| 13 | `microsoft/VibeVoice-1.5B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 14 | `OpenMOSS-Team/MOSS-TTS-v1.5` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 15 | `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 16 | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 17 | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 18 | `ResembleAI/chatterbox` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 19 | `Edge0/Audio8-TTS-Realistic-Air` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 20 | `black-forest-labs/flux-3-image-klein-base` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 21 | `black-forest-labs/FLUX.2-dev` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 22 | `briaai/Fibo-2.0-dev` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 23 | `ideogram-ai/ideogram-4-nf4` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 24 | `Lightricks/LTX-2.5` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 25 | `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 26 | `Stuubs/Stubelius_Remix_Ltx2.5` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 27 | `kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 28 | `Qwen/Qwen-Image-2.1` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 29 | `Tongyi-MAI/Z-Image-Turbo` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 30 | `Wan-AI/Wan2.2-TI2V-5B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 31 | `StephaneBah/AfroRadVoice-FR` | conditional | NOT_APPLICABLE_TO_DATASET | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 32 | `CohereLabs/aya-vision-32b` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 33 | `meta-llama/Llama-4-Scout-17B-16E` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 34 | `allenai/Olmo-3-1125-32B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 35 | `IFM/K2-Horizon-0.9B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 36 | `google/gemma-4-31B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 37 | `ibm-granite/granite-switch-4.1-30b` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 38 | `LiquidAI/LFM3-Omni-2B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 39 | `mistralai/Mistral-Small-4-119B-2603` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 40 | `Nanbeige/Nanbeige4.3-33B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 41 | `nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 42 | `LiquidAI/LFM2.5-VL-3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 43 | `LiquidAI/LFM2.5-VL-3B-DSpark` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 44 | `openai/gpt-oss-120b` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 45 | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 46 | `Qwen/Qwen3.5-35B-A3B-Base` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 47 | `Qwen/Qwen3.8-27B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 48 | `udgamlabs/Lilavati` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 49 | `udgamlabs/Lilavati-Checker` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 50 | `EPFLiGHT/Meditron3-70B` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 51 | `google/medgemma-4b-it` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 52 | `boltz-community/boltz-2` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 53 | `EPFLiGHT/fully-open-meditron` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 54 | `EPFLiGHT/OLMo-2-32B-MeditronFO` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 55 | `facebook/esm2_t33_650M_UR50D` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 56 | `HuggingFaceBio/Carbon-X` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 57 | `IFM/SFT-Reasoning` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 58 | `OctoMed/OctoMed-32B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 59 | `nvidia/Cosmos-Predict2-2B-Video2World` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 60 | `lerobot/pi0_base` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 61 | `lerobot/smolvla_base` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 62 | `microsoft/TRELLIS.2-4B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 63 | `nvidia/GR00T-N1.6-3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 64 | `speridlabs/idol` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 65 | `tencent/Hunyuan3D-2.1` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 66 | `laion/emotional-roleplay-finetuning-dataset` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 67 | `m-a-p/MERT-v2-FullSong` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 68 | `m-a-p/SheetSage2` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 69 | `m-a-p/YuE2-3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 70 | `m-a-p/YuE2-Vae` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 71 | `nvidia/Granary-v2` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 72 | `nvidia/OpenCodeInstruct` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 73 | `nvidia/OpenMathInstruct-2` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 74 | `facebook/dinov3-vit7b16-pretrain-lvd1689m` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 75 | `facebook/dinov3-vith16plus-pretrain-lvd1689m` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 76 | `facebook/sam3` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 77 | `allenai/pixmo-cap` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 78 | `allenai/tulu-3-sft-mixture` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 79 | `answerdotai/ModernBERT-large` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 80 | `autogluon/chronos-2` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 81 | `BAAI/bge-m3` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 82 | `CohereLabs/aya_dataset` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 83 | `deepseek-ai/DeepSeek-OCR-2` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 84 | `elyza/ELYZA-tasks-100` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 85 | `facebook/vjepa2-vitg-fpc64-384` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 86 | `google/siglip2-base-patch16-224` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 87 | `GSAI-ML/iLLaDA-8B-Base` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 88 | `HuggingFaceFW/fineweb-edu` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 89 | `HuggingFaceH4/ultrafeedback_binarized` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 90 | `ibm-granite/granite-speech-5.0-2b` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 91 | `ibm-granite/granite-speech-5.0-470m-turboctc` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 92 | `lerobot/aloha_sim_insertion_human` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 93 | `lightonai/LightOnOCR-3-0.8B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 94 | `LiquidAI/d1-omni-600M` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 95 | `LiquidAI/LFM3-1.7B-Base` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 96 | `llm-jp/magpie-sft-v1.0` | select | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 97 | `openai/whisper-large-v3-turbo` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 98 | `PaddlePaddle/PaddleOCR-VL-1.5` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 99 | `Qwen/Qwen3-ASR-1.7B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 100 | `Qwen/Qwen3-Embedding-0.6B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 101 | `Qwen/Qwen3-Reranker-0.6B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 102 | `Qwen/Qwen3-VL-2B-Instruct` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 103 | `Qwen/Qwen3.5-0.8B` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 104 | `RWKV/RWKV7-7.2B-20260805` | select | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 105 | `tencent/Hy-SimulMT-30B-A3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 106 | `nvidia/Nemotron-Cascade-2-30B-A3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 107 | `nvidia/Nemotron-Cascade-2-RL-data` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 108 | `nvidia/Nemotron-Cascade-2-SFT-Data` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 109 | `Hcompany/Holo4-27B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 110 | `WhissleAI/steer-tts` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 111 | `maya-research/maya2-native` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 112 | `Hcompany/trajectories` | conditional | NOT_APPLICABLE_TO_DATASET | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 113 | `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 114 | `fishaudio/drama-3` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 115 | `PrentisAI/GroundGUI-8B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 116 | `ausboss/Qwen-Image-2.1-Consistency-LoRA` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 117 | `Hcompany/Holotron4-30B-A3B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 118 | `LiquidAI/LFM2.5-24B-A2B-DSpark` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 119 | `pfnet/plamo-3-translate-31b` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 120 | `pfnet/plamo-3-translate-0.8b` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 121 | `nvidia/Cosmos3-Nano-Sim-Bimanual` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 122 | `PrunaAI/P-H3-Image` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 123 | `nvidia/Cosmos3-Nano-Sim-Auto` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 124 | `gradium/phonon-31m-en` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 125 | `gradium/phonon-40m-multilingual` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 126 | `kakaocorp/kanana-2-v-decide-3b-2611` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 127 | `qvac/BotPsy-0.8B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 128 | `ibm-granite/granite-timeseries-ttm-r3` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 129 | `Zyphra/ZONOS3-Mini` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 130 | `robbyant/lingbot-touch-tiny` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 131 | `nvidia/Alpamayo2-Edge` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 132 | `ACE-Step/acestep-v15-xl-turbo` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 133 | `tencent/Qwen3.8-27B-DSpine-b16` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 134 | `nvidia/Nemotron-3-Diarization` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 135 | `nvidia/RFD4-Proteina` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 136 | `ibm-granite/granite-4.1-3b-llmon-preview` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 137 | `perplexity-ai/pplx-decider-flash-v1.3` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 138 | `nvidia/Kumo-Relational` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 139 | `nvidia/Kumo-Tabular` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 140 | `nvidia/Kumo-Anomaly` | conditional | UNVERIFIED_BLOCK_FINAL_LOCK | VERIFY_TOTAL_STOP_ACQUISITION_PREPARATION | null | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| 141 | `meta-models/Muse-Glimmer-30B` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 142 | `meta-models/Muse-Glimmer-30B-assistant` | conditional | PASS_TOTAL_PARAMS_LT_150B | SOURCE_FILE_IDENTITY_AND_RIGHTS_REVIEW | null | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 143 | `nvidia/Ising-Decoder-ColorCode-1-Fast` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| 144 | `nvidia/Ising-Decoder-SurfaceCode-1-Fast` | conditional | PASS_TOTAL_PARAMS_LT_150B | VERIFY_OWNER_ACCESS_NO_DOWNLOAD | null | OWNER_SPECIFIC_GATED_ENTITLEMENT |

## ERROR CHECK

- 現行v36 191件、active144件、R83 144レコードをrepo ID＋asset_kindで一意に照合。
- 最初の阻害要因 9/18/115/2 の合計144。選択バイト既知2件、未確定142件。
- 選定判断、CURRENT、queues/approved.json、実HDD、重みファイル、実行環境には**一切変更なし**。
- この研究台帳の「維持」は、将来の調査を継続する判断であって取得承認ではない。

## 〈次に考える問い〉

**モデルを増やすより、まず何件を原本の固定版・権利・依存まで監査可能にできるか。その改善を、14日で何件の完全allowlistが作れたかで検証すべきではないか。**
