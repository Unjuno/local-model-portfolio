# v31 CONDITIONAL 79件：SELECTへの昇格判定と追加の一次資料監査（2026-11-13）

> 保存対象の選定判断とダウンロード権限を分ける**非実行**の決定表。取得・実行・Gated申請・個人情報処理・既存選定変更は一切行わない。

- リポジトリ：[`Unjuno/local-model-portfolio`](https://github.com/Unjuno/local-model-portfolio)、調査ブランチ：`strategy/2026-11-03-01-risk`、基準HEAD：`bd28e035426bc95933343e5a864b6a80209c36d9`。対象v31：[`catalog/effective-portfolio-2026-11-13-v31.json`](../../catalog/effective-portfolio-2026-11-13-v31.json)。
- 個別の179中79件の研究判定：[`catalog/proposals/05-v31-conditional-selection-review.json`](../../catalog/proposals/05-v31-conditional-selection-review.json)。

## 1. 研究結論

- 現行v31はSELECT53／CONDITIONAL79／HOLD28／DEFERRED13／EXCLUDED6。**79件のうち69モデル、10データをHugging Faceの現行公開メタデータで全件照合した**。
- 79件のうちGatedは**17**、ライセンスタグ未表示・unknownは**2**、総パラメータ不明で最終取得準備停止は**7**。これらは互いに重なる条件（Gatedかつ数値不明等）であり足し算しない。
- 今回SELECTへ即時昇格した資産は **0**。これは保存価値を否定する結果ではなく、既存の[選定規約](../../policies/selection-decision-v17.json)に従い独立/再現可能な同目的品質、固定ハードウェア、ライセンス正文の確認等がまだ足りないという監査結果。判定は個別条件付きとして維持する。
- 第1候補12件は保存価値・独立タスク・小容量・依存上の役割が明確なので、選定確定に最短の追加検証へ進める。取り急ぎ形式だけの量子化を複数選ばず、原重み/独立SFT/codec/adapterを区別。
- **重要な非対称性**：正本のSELECT53件でも、ライセンス正文確認・固定最終SHA・最終選択バイト数の正本フィールドは各0件。一方CONDITIONALではライセンス3件、最終SHA2件、バイト2件。したがって`SELECT`は取得準備完成を意味せず、単純に昇格数を稼ぐことは逆効果。

## 2. 一次資料で得た具体的な修正

| 資産 | 今回確認した事実 | 判定と残課題 |
| --- | --- | --- |
| [GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B/blob/main/LICENSE) | 配布元の`LICENSE`第3.3節では、非商用の研究・評価目的でのみ利用を許す。HFのライセンスタグは未表示。 | `license unknown`を無制限利用と扱わず、**非商用の利用制約を確認済み**として記録。商用使用不可。本人の具体的行為と全依存を確認してから判断。 |
| [Pruna P-H3 Image](https://huggingface.co/PrunaAI/P-H3-Image) | MiniMax H3 Community Licenseの地域除外（EU/UK/韓国/米国）と、8-stepの独自画像生成・編集を配布者が説明。 | 契約の適用地域・二次利用/NOTICE、Encoder・Upsampler・VAE等全15学習済みファイルの数とSHAを確定するまでCONDITIONAL。日本にいることだけで本人や法人の全権利は証明されない。 |
| [SteerTTS公式LICENSE](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/LICENSE) | Whissleのコード・重み・声にCC BY-NC 4.0と追加Whissle条項、第三者WavLM/Vocos等は別権利。 | Gated本人承認と、9.6Mメインモデル以外の全学習済み依存総数が未確定。取得準備STOP。 |
| [IBM TinyTimeMixer R3](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/blob/main/README.md) | 1.4M級Mixer、Apache-2.0、公開源の`model.safetensors`約5.73MB。開発元はGIFT-EvalのMASE/CRPSと高スループットを報告。 | Chronos-2との同一窓/分割・CPU/clock/backend/batch比較なし。現時点の独立性能PASSではない。 |
| [ZONOS3-Mini一次技術記事](https://huggingface.co/blog/Zyphra/zonos3-mini) | メインのMoEは**活性約100M/総数約800M**と開発元は説明し、音声Codec/ runtime・学習済み声設計を別に持つ。 | 総数を活性100Mと取り違えない。最終版の全tensor数・声Codec・音声同意/日本語品質を検証。 |
| [ACE-Step 1.5論文](https://arxiv.org/abs/2602.00744) | 音楽計画LM＋DiTを組合せた独立公開楽曲生成。v31の音楽生成の穴を埋める根拠。 | デフォルト音楽LM、Embedding、VAEと完全encoder/runtime権利、作者性能の独立再現がまだ不足。 |

## 3. 優先12件：SELECT昇格に近づける最小検証

| 優先 | repo ID | なぜ研究するか・必要な追加検証 |
| ---: | --- | --- |
| 1 | [`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | IBMが配布する独立のMixer/時系列モデル、約1.4M・公開約6MB。Chronos-2との同一データ/条件でMASE、CRPSとCPU遅延を比較する |
| 2 | [`qvac/BotPsy-0.8B`](https://huggingface.co/qvac/BotPsy-0.8B) | Qwen3.5-0.8Bの独自SFT・蒸留・RL。同一BFCL形式のツール呼出し・日本語で親との差を評価する |
| 3 | [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini) | 音声Codec ZAC-1とGated DeltaNet/MoEの独立TTS。英日音声サンプルと対照比較、必要コーデックを静的検査する |
| 4 | [`ACE-Step/acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 現行の音楽生成モダリティ空白を補う8-step蒸留音声DiT。音楽LMとVAEの正式な必須部品を固定する |
| 5 | [`robbyant/lingbot-touch-tiny`](https://huggingface.co/robbyant/lingbot-touch-tiny) | 磁気・圧力・視触覚統合のJEPA型Encoderで既存ロボットVLAとは独立。重み/外部センサ依存と用途ライセンスを確定する |
| 6 | [`nvidia/Alpamayo2-Edge`](https://huggingface.co/nvidia/Alpamayo2-Edge) | 車載因果説明＋軌道生成の学習済みアクション頭部。公式OpenMDW-1.1正文と別Gatedデータを検査する |
| 7 | [`LiquidAI/LFM2.5-VL-3B`](https://huggingface.co/LiquidAI/LFM2.5-VL-3B) | DSparkドラフターが依存する正式な3.12Bターゲット。親とドラフターを版・ABIで固定する |
| 8 | [`LiquidAI/LFM2.5-VL-3B-DSpark`](https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark) | 独立学習した約279.5Mドラフター。ターゲットと同一条件の速度・品質を測定する |
| 9 | [`m-a-p/SheetSage2`](https://huggingface.co/m-a-p/SheetSage2) | 音楽から譜面とMIDIを抽出する独立小型モデル。MERT FullSongとの依存、同意ある音源での転写精度を検証する |
| 10 | [`m-a-p/MERT-v2-FullSong`](https://huggingface.co/m-a-p/MERT-v2-FullSong) | SheetSage2の必要な音響エンコーダで30秒版では置換互換が未確認。非商用条件と固定シリアライゼーションを確認する |
| 11 | [`nvidia/Granary-v2`](https://huggingface.co/nvidia/Granary-v2) | 人手に近い音声再ラベルの専門データ。ただしソース音声は付属せず、許諾された素材との再結合が必須 |
| 12 | [`kakaocorp/kanana-2-v-decide-3b-2611`](https://huggingface.co/kakaocorp/kanana-2-v-decide-3b-2611) | 型付き判定・確率出力の別後学習原本。信頼度校正と既存d1-omniの同条件比較を先に行う |

**ここでの『優先』は実際のダウンロード順位でない。** 小型の代替タスクが明確、必須Codec/Encoderで他モデルに依存される等、保存のオプション価値と未確認点の少なさを考えた**研究順**である。大型でも将来重要な原本を自動除外しない。

## 4. 79件全件の調査トラック・判定

凡例：`RETAIN_CONDITIONAL`＝現行研究選定は維持するが、SELECTへ無根拠に昇格しない。`PARAMETER_CENSUS_STOP`＝取得準備停止。`GATED_PERMISSION`＝利用者本人の正規手続が必要。`MATCHED_QUALITY`＝単独作者測定でなく固定した基準と比較。観測された配布状態と将来規制仮説を混同しない。

| No. | repo ID・一次URL | 種別 | HF現行表示 | HFライセンスタグ | 150B/総数ゲート | 主要検証トラック | 新判断 | 昇格を止めた理由 |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | model | Gated | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 2 | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 3 | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 4 | [`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 5 | [`LiquidAI/LFM2.5-24B-A2B`](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 6 | [`LiquidAI/LFM3-1.7B`](https://huggingface.co/LiquidAI/LFM3-1.7B) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 7 | [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 8 | [`Edge0/Audio8-TTS-Realistic-Air`](https://huggingface.co/Edge0/Audio8-TTS-Realistic-Air) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 9 | [`black-forest-labs/flux-3-image-klein-base`](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 10 | [`black-forest-labs/FLUX.2-dev`](https://huggingface.co/black-forest-labs/FLUX.2-dev) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 11 | [`briaai/Fibo-2.0-dev`](https://huggingface.co/briaai/Fibo-2.0-dev) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 12 | [`ideogram-ai/ideogram-4-nf4`](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 13 | [`Lightricks/LTX-2.5`](https://huggingface.co/Lightricks/LTX-2.5) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 14 | [`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | model | 公開表示 | unknown | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 15 | [`Stuubs/Stubelius_Remix_Ltx2.5`](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | model | 公開表示 | other | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 16 | [`kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers`](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers) | model | 公開表示 | mit | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 17 | [`Qwen/Qwen-Image-2.1`](https://huggingface.co/Qwen/Qwen-Image-2.1) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 18 | [`StephaneBah/AfroRadVoice-FR`](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | dataset | Gated | cc-by-4.0 | NOT_APPLICABLE_TO_DATASET | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 19 | [`CohereLabs/aya-vision-32b`](https://huggingface.co/CohereLabs/aya-vision-32b) | model | Gated | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 20 | [`meta-llama/Llama-4-Scout-17B-16E`](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 21 | [`IFM/K2-Horizon-0.9B`](https://huggingface.co/IFM/K2-Horizon-0.9B) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 22 | [`LiquidAI/LFM3-Omni-2B`](https://huggingface.co/LiquidAI/LFM3-Omni-2B) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 23 | [`nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 24 | [`LiquidAI/LFM2.5-VL-3B`](https://huggingface.co/LiquidAI/LFM2.5-VL-3B) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 25 | [`LiquidAI/LFM2.5-VL-3B-DSpark`](https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 26 | [`Qwen/Qwen3-Omni-30B-A3B-Instruct`](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 27 | [`udgamlabs/Lilavati`](https://huggingface.co/udgamlabs/Lilavati) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 28 | [`udgamlabs/Lilavati-Checker`](https://huggingface.co/udgamlabs/Lilavati-Checker) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 29 | [`EPFLiGHT/Meditron3-70B`](https://huggingface.co/EPFLiGHT/Meditron3-70B) | model | Gated | llama3.1 | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 30 | [`google/medgemma-4b-it`](https://huggingface.co/google/medgemma-4b-it) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 31 | [`boltz-community/boltz-2`](https://huggingface.co/boltz-community/boltz-2) | model | 公開表示 | mit | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 32 | [`IFM/SFT-Reasoning`](https://huggingface.co/datasets/IFM/SFT-Reasoning) | dataset | 公開表示 | apache-2.0 | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 33 | [`nvidia/Cosmos-Predict2-2B-Video2World`](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 34 | [`lerobot/pi0_base`](https://huggingface.co/lerobot/pi0_base) | model | 公開表示 | gemma | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 35 | [`nvidia/GR00T-N1.6-3B`](https://huggingface.co/nvidia/GR00T-N1.6-3B) | model | 公開表示 | 未確認 | PASS_TOTAL_PARAMS_LT_150B | LICENSE_TEXT_AND_PROVENANCE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 36 | [`speridlabs/idol`](https://huggingface.co/speridlabs/idol) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 37 | [`tencent/Hunyuan3D-2.1`](https://huggingface.co/tencent/Hunyuan3D-2.1) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 38 | [`laion/emotional-roleplay-finetuning-dataset`](https://huggingface.co/datasets/laion/emotional-roleplay-finetuning-dataset) | dataset | 公開表示 | cc-by-4.0 | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 39 | [`m-a-p/MERT-v2-FullSong`](https://huggingface.co/m-a-p/MERT-v2-FullSong) | model | 公開表示 | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 40 | [`m-a-p/SheetSage2`](https://huggingface.co/m-a-p/SheetSage2) | model | 公開表示 | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 41 | [`m-a-p/YuE2-3B`](https://huggingface.co/m-a-p/YuE2-3B) | model | 公開表示 | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 42 | [`m-a-p/YuE2-Vae`](https://huggingface.co/m-a-p/YuE2-Vae) | model | 公開表示 | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 43 | [`nvidia/Granary-v2`](https://huggingface.co/datasets/nvidia/Granary-v2) | dataset | 公開表示 | openmdw-1.1, cc-by-sa-4.0 | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 44 | [`facebook/dinov3-vit7b16-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 45 | [`facebook/dinov3-vith16plus-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 46 | [`facebook/sam3`](https://huggingface.co/facebook/sam3) | model | Gated | other | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 47 | [`allenai/pixmo-cap`](https://huggingface.co/datasets/allenai/pixmo-cap) | dataset | 公開表示 | odc-by | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 48 | [`allenai/tulu-3-sft-mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | dataset | 公開表示 | odc-by | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 49 | [`HuggingFaceFW/fineweb-edu`](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | dataset | 公開表示 | odc-by | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 50 | [`LiquidAI/d1-omni-600M`](https://huggingface.co/LiquidAI/d1-omni-600M) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 51 | [`LiquidAI/LFM3-1.7B-Base`](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 52 | [`tencent/Hy-SimulMT-30B-A3B`](https://huggingface.co/tencent/Hy-SimulMT-30B-A3B) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 53 | [`nvidia/Nemotron-Cascade-2-30B-A3B`](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 54 | [`nvidia/Nemotron-Cascade-2-RL-data`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) | dataset | 公開表示 | odc-by | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 55 | [`nvidia/Nemotron-Cascade-2-SFT-Data`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) | dataset | 公開表示 | other | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 56 | [`Hcompany/Holo4-27B`](https://huggingface.co/Hcompany/Holo4-27B) | model | 公開表示 | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 57 | [`WhissleAI/steer-tts`](https://huggingface.co/WhissleAI/steer-tts) | model | Gated | cc-by-nc-4.0 | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 58 | [`maya-research/maya2-native`](https://huggingface.co/maya-research/maya2-native) | model | 公開表示 | apache-2.0 | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 59 | [`Hcompany/trajectories`](https://huggingface.co/datasets/Hcompany/trajectories) | dataset | 公開表示 | apache-2.0 | NOT_APPLICABLE_TO_DATASET | DATA_PROVENANCE_AND_CONTENT_SCOPE | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 60 | [`DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU`](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 61 | [`fishaudio/drama-3`](https://huggingface.co/fishaudio/drama-3) | model | 公開表示 | other | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 62 | [`PrentisAI/GroundGUI-8B`](https://huggingface.co/PrentisAI/GroundGUI-8B) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 63 | [`ausboss/Qwen-Image-2.1-Consistency-LoRA`](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | model | 公開表示 | other | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 64 | [`Hcompany/Holotron4-30B-A3B`](https://huggingface.co/Hcompany/Holotron4-30B-A3B) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 65 | [`LiquidAI/LFM2.5-24B-A2B-DSpark`](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B-DSpark) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 66 | [`pfnet/plamo-3-translate-31b`](https://huggingface.co/pfnet/plamo-3-translate-31b) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 67 | [`pfnet/plamo-3-translate-0.8b`](https://huggingface.co/pfnet/plamo-3-translate-0.8b) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 68 | [`nvidia/Cosmos3-Nano-Sim-Bimanual`](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Bimanual) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 69 | [`PrunaAI/P-H3-Image`](https://huggingface.co/PrunaAI/P-H3-Image) | model | 公開表示 | other | UNVERIFIED_BLOCK_FINAL_LOCK | PARAMETER_CENSUS_STOP | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 70 | [`nvidia/Cosmos3-Nano-Sim-Auto`](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 71 | [`gradium/phonon-31m-en`](https://huggingface.co/gradium/phonon-31m-en) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | TRAINED_STATE_DISTINCTNESS_AND_FORMAT | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 72 | [`gradium/phonon-40m-multilingual`](https://huggingface.co/gradium/phonon-40m-multilingual) | model | Gated | cc-by-nc-4.0 | PASS_TOTAL_PARAMS_LT_150B | GATED_PERMISSION_AND_SOURCE_RIGHTS | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 73 | [`kakaocorp/kanana-2-v-decide-3b-2611`](https://huggingface.co/kakaocorp/kanana-2-v-decide-3b-2611) | model | 公開表示 | other | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 74 | [`qvac/BotPsy-0.8B`](https://huggingface.co/qvac/BotPsy-0.8B) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 75 | [`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 76 | [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 77 | [`robbyant/lingbot-touch-tiny`](https://huggingface.co/robbyant/lingbot-touch-tiny) | model | 公開表示 | apache-2.0 | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 78 | [`nvidia/Alpamayo2-Edge`](https://huggingface.co/nvidia/Alpamayo2-Edge) | model | 公開表示 | openmdw-1.1 | PASS_TOTAL_PARAMS_LT_150B | LICENSE_DEPENDENCY_AND_HIGH_COST | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |
| 79 | [`ACE-Step/acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | model | 公開表示 | mit | PASS_TOTAL_PARAMS_LT_150B | MATCHED_QUALITY_AND_RECOVERY | 維持（追加検証） | PROMOTE_SELECT in policies/selection-decision-v17.json requires independent or reproducible match… |

## 5. 厳密な判定ルールと次の調査

**保存価値の判定**：独立した後学習/蒸留/Encoder/Codec/ロボット行動等の学習済み成果は、元モデルを単純量子化しても復元できない。他方、同じSFT checkpointのGGUF/FP8を複数選定する根拠にはならない。コストは本体だけでなく必要依存のincremental unique bytesと既存保存原本を照合する。

**SELECTへの昇格テスト**：必ず(1)一次repoと原学習状態、(2)同用途ベースライン対照と統計的な品質差/劣化範囲、(3)固定HW/clock/driver/backend/ABI/quant zero-point/context/batch、(4)当該ライセンス正文・親・依存権利、(5)復元対象と増分保存コストを確認する。公開者の速度/品質だけでPASSにしない。データはsplit・来歴・同意・原著作者ライセンス・内容整合性で置き換える。

**取得への進行は別**：総パラメータ未確認7モデルはMoE全expert/外部学習済み部品が判明するまで準備停止。Gated17件は本人承認まで取得不可。全79件について固定された最終取得セット、現実の4TB HDD空きと200GB床、権利、SHA、別途ユーザー承認がなければ取得・実行しない。現在の承認キューは0件。

### 5.1 H/T/D/C/U と変数表

| 記号 | 日本語の意味 | 単位（SI） | 定義/範囲/前提 | 型 |
| --- | --- | --- | --- | --- |
| N | 今回のCONDITIONAL審査対象件数 | 1（無次元の個数） | N=79、各repo_id＋asset_kindは一意 | 整数スカラー |
| G | HF公開メタデータでGated表示を確認した件数 | 1（無次元の個数） | G=17。本人許可を意味しない | 整数スカラー |
| U | 全学習済みモデルの総パラメータ未確認で準備停止中の件数 | 1（無次元の個数） | U=7、Gと重なり得る | 整数スカラー |
| B | 最終保存構成の重複除去後bytes | byte | 全件未確定（別の一次容量監査は存在） | 非負整数またはnull |
| P | 各モデルのMoE全expertを含む総学習済みパラメータ | 1（個数） | unknownはnull、量子化しても総数不変 | 非負整数またはnull |

**次元チェック**：件数N/G/UやパラメータPは無次元、保存容量Bはbyte。GとUのように重複する集合の件数を足して79の相補集合と扱わない。必要容量Bを上流repo全量から単純代入しない。

- **H**：既存の厳格SELECT選定条件を緩めず、一次メタデータ＋権利と実験の欠損を埋めると、再現可能で価値のあるCONDITIONALから順次SELECTへ移行できる。
- **T**：79件のrepo情報を全数照合（n_min=79）。初期短縮評価は12件で開始し、LLMは選定規則の200例/タスク等、画像40prompt×3seed、動画20prompt×3seed、音声30文/言語・同意5話者、実行速度30試行以上を同一構成で比較。データは許諾splitと完全ファイル/派生来歴を静的検証。モデル実行は個別承認後のみ。
- **D**：`PASS`=独立/再現可能品質とライセンス正文・実機評価が揃い、保存価値が既存代表に対して独立と確認できたらSELECT。`FAIL`=同一checkpoint形式重複しかない、致命的権利不適合、再現不能を立証したらHOLD/EXCLUDED再審査。`UNCERTAIN`=今回のような未検証ならCONDITIONAL維持・download不可。
- **C**：公開者のみの誇張、別版や評価汚染、本人Gated権未承認、非商用/地域制限、純量子化コピーが別学習と誤判定、依存Codec/ABI欠損。
- **U（不確かさ）**：最新ライセンス本文・特定版の全ファイル/部品総数、現実のHDD、独立ベンチ、変更の発生順序。数量誤差の観測分布がないため合成標準不確かさ`u_c`と包含係数`k`は推定不可。

### 5.2 ERROR CHECK

- 79件の一意キー確認（69 model / 10 dataset）；HFリポジトリ公開メタデータ79/79件が存在。Gated17、ライセンスタグなし・unknown2、active総数不明7。
- 現行SELECT53、CONDITIONAL79は**改変なし**。明示的承認0、本体取得0、Gated承認依頼0、モデル実行0、テスト実行0。
- 厳格SELECT条件の新規検証が足りないため今ラウンドの昇格0、今後の短期候補12という判定を全件に反証条件付きで記録。Exa追加クレジットはHTTP402で利用不能のため、HF公式メタデータ・一次論文・配布者LICENSEにより補完。

## 6. 〈応用・転用例〉

**計算機科学/ML**：Base・蒸留・RLの学習状態差をハッシュと同条件品質で判断。**デジタル保存**：原本・依存Codec・ライセンス・ABIの閉包を維持。**法学/契約**：公開表示とGated本人許可、非商用/地域/再配布権を分離。**統計的実験設計**：開発元単独ベンチではなく、同一評価セット・複数比較の補正と信頼区間を採用。

## 7. 〈次に考える問い〉

最初の独立評価対象として、容量が数MBのTinyTimeMixer R3と、数十GB＋外部依存のACE-Step XLを、何を優先指標として順番づけるべきか。
