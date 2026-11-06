# R29｜保存候補の機能重複監査（2026-11-07）

**結論：R28のA/B/C容量先行3案は撤回する。** 4TBを使えるという指示は維持するが、800GBを埋めるため同じ役割のモデルを複数積まない。既存v19の150資産（SELECT 53 / CONDITIONAL 52 / HOLD 27 / BACKLOG 12 / EXCLUDED 6）、過去の未決定候補、Nanbeige4.3-33BのSELECTを変更しない。撤回対象は新規取得の一括配分案のみ。

## 1. 現行モデルとの機能重複

| 比較領域 | 既存モデル | 追加候補 | 重複判断・次の操作 |
|---|---|---|---|
| 大規模コード・推論 | Qwen3-Coder-Next、Mistral Small 4 119B、gpt-oss-120b | DeepSeek V4.1 748B、Mistral Large 4 1.05T | **大幅重複**。大規模量子化の新規保存枠は原則1系統以下。原本のDeepSWE・SWE-Bench数値やGGUFのtop-1一致率を互いの直接対決としない |
| Qwen3.8-27B拒否制御 | Qwen原本、OrcaRouter、Interpretic、0bserverx、afdudley | 同系統の新量子化 | **同一祖先**。低拒否率だけでは2種類以上の派生全量を保存しない。選択的政治回答、危険依頼拒否、RP、一般能力を同条件で比較 |
| LTX 2.5動画 | LTX2.5原本、ChrisColeTech FP8、Stuubs Remix、旧2.3 | 別のフルcheckpoint | **高重複懸念**。原本＋能力差が実証された特殊版のみ。差分LoRAなら固定ベースとの一致を検証 |
| 音声合成 | VibeVoice、MOSS-TTS、Qwen3-TTS CustomVoice/Base/VoiceDesign、Audio8 | 別の通常TTS | **同目的が多い**。話者設計・日本語・感情・長文安定性などの固有制御が勝るまで追加しない。ただし異なる制御特性を無条件に同じ重みとしない |
| 音声対話 | **Qwen3-Omni-30B-A3B-Instruct**（既にリアルタイム音声入力・音声出力） | NVIDIA VoiceChat 11B | **主要機能が重複**。NVIDIAの英語tool callingと割込完遂率が既存Omniを上回る同条件実験まで新規保存枠を割り当てない |
| 人物映像 | Wan2.2 TI2V、LTX2.5、LivePortrait | Wan-Animate2、LongCat Avatar | Wan-Animate2の**駆動動画→別人物の全身運動移植**は固有入力の可能性がある。LongCatはLTX2.5の音声ガイドと競合するため、二つ同時の既定追加をしない |
| Qwen-Image2.1 | Qwen-Image2.1本体、ChatR Omni LoRA | 追加LoRAや再配布フルweights | **依存関係**。ベースは固定SHAが一致したときだけ共有し、LoRA差分のみ保存。同じ名称で節約と仮定しない |
| FLUX画像 | FLUX.2-dev、FLUX.2-klein、flux-3-image-klein Base/Post | 追加の生成モデル | **同用途競合**。品質・編集・モデルサイズ・学習Baseの価値を個別評価 |
| 共同依存 | LFM2.5 VL target＋DSpark draft、Lilavati＋Checker | — | **重複でなく補完**。単独で機能しない補助重みを削らず、同一ファイルだけハッシュ単位で共有 |

## 2. R28で比較した候補の修正判断

| 追加候補 | 公称主な選択バイト | 保存差分への判断 | 重要な反証 |
|---|---:|---|---|
| [Wan-Animate-2](https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B-Diffusers) | 45.92 GB | **優先検証：条件付き** | LivePortraitや既存Wanで全身運動制御を代替できれば追加しない |
| [dots.tts.edit](https://huggingface.co/dots-studio/dots.tts.edit) | 約5.15 GB | **優先検証：条件付き** | 既存TTSで局所編集と非編集部分の保持を実現できれば追加しない |
| [DeepSeek V4.1 Flash 1017 GGUF](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF) UD-Q2_K_XL | 約334.8 GB | **条件付き大型例外・最大1構成のみ** | Qwen3-Coder-Nextなどより実際のコーディング・agent・推論の品質/保存容量比が改善しなければ追加しない |
| [Mistral Large 4 GGUF](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF) UD-Q2_K_XL | 約378.3 GB | **今回の増分枠から除外、既存HOLD維持** | 多言語/画像理解などで既存の119B・120B系やDeepSeekと独立の価値が確認された場合は再評価 |
| [LongCat Avatar1.5](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5) | 約44.79 GB | **LTX2.5との比較待ち、既存R23研究保持** | 同一音声・参照人物でLTX2.5の音声ガイドと同等なら追加しない |
| [NVIDIA VoiceChat11B](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-VoiceChat-11B) | 約44.4 GB | **Qwen3-Omniとの比較待ち、既存R27研究保持** | 英語全二重のtool selectionは作者82.5%でも完全Pass@1は33%。Qwenとの差を測る |
| DeepSeekの別IQ2量子化 / Mistralの別IQ2量子化 | 約300.5 / 302.0 GB | **同一重み系列の代替精度であり追加の独立モデルではない** | 選ぶのはどちらか1形式。複数は別性能/別実行目的の証拠がある場合のみ |

**計画上の最大研究ショートリスト**は Wan 45.920934868 GB ＋ dots 約5.1532 GB ＋ DeepSeek Q2 約334.8 GB ≒ **385.87 GB**（公開元に基づく主なファイルの概数であり、依存/キャッシュ/ステージング未含有）。このうちDeepSeekは既存コーダとの独立比較が必要。したがって**正式に取得承認した容量は0**。約800GBの残額を類似モデルで埋めない。

## 3. 判断の証拠と検証規格

DeepSeekの6ベンチ平均は[Unsloth配布者測定](https://unsloth.ai/docs/models/deepseek-v4.1-flash)。Mistralのtop-1一致95.6%も[Unslothの量子化評価](https://unsloth.ai/docs/models/mistral-large-4)であり、タスク正答率と同一視しない。Qwen3-Omniの[公式モデルカード](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct)は19の音声入力言語、10の音声出力言語とリアルタイムストリーミングを明記。音声アバターの[Tight Studio実行比較](https://tight.studio/blog/open-source-talking-avatar-models/)は単一素材でありWan-Animate2との統一品質比較ではない。映像モデルの固有入力については[Wan-Animate2論文](https://arxiv.org/abs/2608.06009)を参照。

## 4. H/T/D/C/U・変数表・ERROR CHECK

| 記号 | 意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| B | 候補構成の主なファイル容量 | byte | 固定ファイル選択の公称値。依存・stagingは未知。非負整数スカラー |
| U | 追加容量の申告値 | byte | 約800,000,000,000。実機空き測定前の非負スカラー |
| N | 同条件比較の独立課題数 | 1 | 最低30、整数スカラー |
| M | 推論ピークRAM | byte | OS/KV/依存込み、実測512,000,000,000未満、非負スカラーまたは未知 |

**H**：追加候補は既存の最高性能ベースラインにない能力を持つ。**T**：固定HW/clock/backend、量子化zero-point/ABI、context/batch、依存を合わせ、最低30の盲検/対応課題を評価。音声/映像は機能別の人間評価・生成物ハッシュも確認。**D**：明確な固有入力制御または事前指定の性能改善があり、権利・完全ファイルSHA・実機メモリを満たせば保存候補PASS。同等なら追加保存FAIL、未測定はUNCERTAIN。**C**：ベンチマーク混同、母体モデル重複、量子化劣化、SSD Engram遅延。**U**：ハッシュや品質実測がないため合成不確かさu_cと包含係数kは未算定。単位確認：B/U/Mはbyte、Nは無次元。保存容量と推論RAM、モデル総パラメータ数は互いに代用不可。

**ERROR CHECK**：このR29は既存v19の150件とその意思決定状態、Nanbeige SELECT、ユーザー指定6 EXCLUDED、過去の研究候補を変更しない。旧R28の配分3案だけを撤回。取得キュー変更0、本体DL0。機械学習評価、映像/ロボティクス、音声処理、供給網・長期保存に転用する。

## 5. 〈次に考える問い〉

同じ用途の重量級を2つ保管する場合、どの独立課題・実行環境・品質差なら「2番目にも代替不能な保存価値がある」と判定できるか。
