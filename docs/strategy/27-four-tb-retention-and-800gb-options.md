**訂正（R29・2026-11-07）**：以下のR28 A/B/C 3案は、既存モデルとの機能重複を十分比較していなかったため、**新規保存・取得案として撤回**。容量4TBの計画上限と既存/未決定候補の保持は有効です。今後は[R29 機能重複監査](28-overlap-dedup-r29.md)と[機械可読判定](../../catalog/research/2026-11-07-r29-overlap-audit.json)を使用してください。

# R28｜4TBを使う保存戦略と、除外しない800GB級比較（2026-11-07）

**ユーザーの訂正を正本へ反映**：保存計画上限を旧3.8TBから4.0TBへ更新。現行v19の150件をすべて保持し、R19/R20/R23/R27の未決定・保留候補も削らず記録した。Nanbeige4.3-33BはSELECT維持、ユーザー指示の6件EXCLUDEDは勝手に戻さない。[全ID付き計画JSON](../../catalog/proposals/2026-11-07-r28-four-tb-capacity.json)。正式SELECTの追加・取得承認・既存ファイル操作はない。

## 1. 容量を正しく区別する

ユーザー申告の**4,000,000,000,000 byte**を計画上限とする。過去のv3/v4計画3,288,130,513,582 byteを単純に引くと、仮の余力は**711,869,486,418 byte（約712GB）**である。一方、ユーザーの『約800GB追加で使える』は別の報告で、現時点のv19選定ファイル・既存ダウンロード実体・SHA重複を測定した数字ではない。古い仮見積りを根拠に候補を除外しない。

**独立安全条件**：200GBの最低空き容量は維持。4TBが実機の全容量なら4TBのファイルを全格納することはできない。4TBが安全空きを除いた使える枠という報告であれば、実機のフォーマット容量・空き・stagingを照合してから判断する。未測定の容量は0としない。

## 2. 実際に容量を割り当てる候補案（まだ取得していない）

| 案 | 正規チェックポイント構成（同系統の精度違いは重複保存しない） | 主な公開ファイル概算 | 旧v3/v4計画と合算した場合の余裕 |
|---|---|---:|---:|
| A-diversity | DeepSeek-V4.1-Flash-1017-GGUF UD-Q2_K_XL、Wan2.2-Animate-2-14B-Diffusers R23 fixed、LongCat-Video-Avatar-1.5 R23 INT8+DMD、NVIDIA-NemotronLabs-VoiceChat-11B BF16/FP32、dots.tts.edit V1.1 | 475.06GB | 236.81GB |
| B-800GB-large-exceptions | DeepSeek-V4.1-Flash-1017-GGUF UD-IQ2_XXS、Mistral-Large-4-1T-A52B-GGUF UD-Q2_K_XL、Wan2.2-Animate-2-14B-Diffusers R23 fixed、LongCat-Video-Avatar-1.5 R23 INT8+DMD、dots.tts.edit V1.1 | 774.66GB | -62.79GB |
| C-two-large-old-base-envelope | DeepSeek-V4.1-Flash-1017-GGUF UD-Q2_K_XL、Mistral-Large-4-1T-A52B-GGUF UD-IQ2_XXS、Wan2.2-Animate-2-14B-Diffusers R23 fixed、dots.tts.edit V1.1 | 687.87GB | 24.00GB |

**A**：475GBで大規模コードモデル・全身動作・音声駆動アバター・全二重会話・局所音声編集を幅広く保存する検討案。**B**：775GBで1T級モデル2件を含む案。ただし旧計画をそのまま基準とすると**約63GB超過**し、取得可能と結論できない。**C**：688GBで2つの大規模量子化とWan/音声編集に絞る案。いずれも依存・staging・実機RAM未積算。案から外れた過去の候補は不採用とはしない。

## 3. 候補別の保存価値・失敗例・一次根拠

| 候補と正規HF配布元 | 総数／容量概算 | 性能根拠・独自性 | 否定根拠・権利条件 | 研究状態 |
|---|---|---|---|---|
| [unsloth/DeepSeek-V4.1-Flash-1017-GGUF / UD-IQ2_XXS](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF) | 748B／300.50GB | Distinct 552B MoE plus 196B Engram coding/agentic weights. Publisher six-test average 86.63 vs Q8 87.68. [一次資料](https://unsloth.ai/docs/models/deepseek-v4.1-flash) | Publisher-only result; no user hardware/SSD latency and rights verification.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | CONDITIONAL_RESEARCH |
| [unsloth/DeepSeek-V4.1-Flash-1017-GGUF / UD-Q2_K_XL](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF) | 748B／334.80GB | Publisher six-test mean 87.49 against Q8 87.68. [一次資料](https://unsloth.ai/docs/models/deepseek-v4.1-flash) | Same base as IQ2; choose one not both; 34.3GB premium.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | ALTERNATE_ONLY |
| [unsloth/Mistral-Large-4-1T-A52B-GGUF / UD-Q2_K_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF) | 1050B／378.30GB | Distinct 1.05T multimodal multilingual model; publisher top-1 agreement 95.6%. [一次資料](https://unsloth.ai/docs/models/mistral-large-4) | Top-1 is not task success; 310-390GB publisher RAM estimate, runtime and rights unverified.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | EXISTING_MODEL_HOLD_EXCEPTION |
| [unsloth/Mistral-Large-4-1T-A52B-GGUF / UD-IQ2_XXS](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF) | 1050B／302.00GB | Smaller 1T preservation option; publisher top-1 93.9%. [一次資料](https://unsloth.ai/docs/models/mistral-large-4) | More quality loss than higher variant; do not save both without demonstrated independent purpose.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | ALTERNATE_ONLY |
| [Wan-AI/Wan2.2-Animate-2-14B-Diffusers / R23 fixed](https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B-Diffusers) | 総構成不明／45.92GB | Full-body motion transfer distinct from LivePortrait; R23 selected weights sized. [一次資料](https://arxiv.org/abs/2608.06009) | Quality independent benchmark and full component census unverified.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | PRIOR_CONDITIONAL_RETAIN |
| [meituan-longcat/LongCat-Video-Avatar-1.5 / R23 INT8+DMD](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5) | 総構成不明／44.79GB | Multi-speaker audio-driven avatar unlike full-body driving; author study 508 pairs and 770 raters. [一次資料](https://arxiv.org/abs/2605.26486) | INT8 quality, vocal separator component, Japanese lip sync unverified.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | PRIOR_CONDITIONAL_RETAIN |
| [dots-studio/dots.tts.edit / V1.1](https://huggingface.co/dots-studio/dots.tts.edit) | 総構成不明／5.15GB | Explicit localized speech editing and preservation; doteBench 2081 author trials. [一次資料](https://arxiv.org/abs/2608.02673) | Intense emotion low success; Japanese untested, exact weights license scope uncertain.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | PRIOR_CONDITIONAL_RETAIN |
| [nvidia/NVIDIA-NemotronLabs-VoiceChat-11B / BF16/FP32](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-VoiceChat-11B) | 11B／44.40GB | Full duplex speech with tool calls distinct from TTS; author tool selection 82.5%. [一次資料](https://arxiv.org/abs/2609.21967) | Complete tool Pass@1 33%; local runtime and long-horizon benchmark not reproduced.。ライセンス正文・固定revision・全ハッシュと必要依存は取得前に確認 | PRIOR_CONDITIONAL_RETAIN |

**注記**：Unslothが報告するDeepSeek 2bitの六ベンチ平均、Mistral Large4のtop-1一致率は開発・量子化提供者の測定であり、独立したユーザー実機のタスク成功率ではない。DeepSeekの552B backboneに196B Engramを含め**748B総数**、Mistralは約**1.05T総数**として150B例外審査する。実行時ピークRAM512GB未満、品質・速度、権利、完全ファイル/依存、ユーザー個別承認が必要。

## 4. 変数表・H/T/D/C/U・検証

| 記号 | 意味 | SI単位 | 定義／範囲／型 |
|---|---|---|---|
| C | 保存計画上限 | byte | ユーザー申告4e12、非負整数・実機未検証 |
| H | 古い計画総量 | byte | 3,288,130,513,582、非負整数、v19現物ではない |
| S | 追加案の主なファイル総量 | byte | 各案の公表値の合計、依存は未知、非負整数 |
| F | 安全空き下限 | byte | 2e11、非負整数 |
| U | 実際の保存可能な増分容量 | byte | 実機未測定なのでnull、測定後非負整数 |

**H**：旧選定を消さず、同一SHAや構成差を調べれば再現困難な追加能力を4TB以内に収められる。**T**：現物HDDの空き、既保存ファイル、全シャード・VAE・音声/画像encoder・READMEライセンス・固定コミットを調べ、実行承認後のみ30件以上でハード/クロック/量子化zero-point/ABI/context/batchを固定した品質・RAM・速度実測。**D**：容量・200GB安全空き・品質・実機RAM上限・権利を満たすまで正式LOCKと取得はUNCERTAIN。超過・不適合はFAIL。**C**：異なる量子化の二重保存、SSD EngramのランダムI/O、重複・ファイル欠落、量子化品質低下。**U**：旧見積のずれ、増分容量、RAMピーク、性能差が未知。合成u_c、包含係数kは未測定で算出不可。**次元検査**：C/H/S/F/Uはいずれもbyteで計算。総パラメータ数は個数でありbyteやピークRAMではない。

## 5. ERROR CHECK／応用／次に考える問い

既存150件のIDと判断状態を保持。条件付き・HOLD・BACKLOGを削除しない。過去研究のR19=8、R20=6、R23=6、R27=8候補も照合できる。ローカル本体取得・削除0件。映像/ロボット動作、音声工学、LLM量子化、デジタルアーカイブ/供給網の4分野で再利用する。

**次に考える問い**：4TBの実測可能な増分空きを確定した後、約775GBの大規模量子化・専門モデル混合案と約475GBの多様性重視案のうち、どちらが既存モデルでは代替できない能力を多く残せるか。
