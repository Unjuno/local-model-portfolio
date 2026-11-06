# R30｜特殊版を残し、通常量子化の過剰な重複だけを減らす

2026-11-07。旧R29の『1ベースに特殊版は原則1つ』という扱いは**過度の制限で撤回**。今回の主眼は同一訓練状態のQ4、Q5、FP8、NVFP4、GGUF等を**別モデルとして数えない**こと。異なるSFT、RL、NSFWマージ、拒否方向編集、独自LoRAは、同じ親由来でも性能と改変方法が本当に違えば複数保管する価値がある。研究選定と取得承認は別。

### 1. 13候補の学習状態と形式の違い

| 正規配布元 | 学習状態の分類 | 当面の判断 | 良い根拠と否定材料 |
|---|---|---|---|
| [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | ORIGINAL_FULL_TRAINED_WEIGHTS | KEEP_EXISTING_SELECT | 新規能力と比較する基準の原本。ベースの重みと通常量子化は別の学習成果ではない |
| [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | WEIGHT_EDITED_SPECIAL | KEEP_EXISTING_CONDITIONAL | 拒否方向の重み編集という訓練状態の変更。未量子化27Bを単なる普通の量子化と誤分類しない。 |
| [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | SPECIAL_TRAINED_STATE_IN_QUANTIZED_FORMAT | KEEP_EXISTING_CONDITIONAL_CHOOSE_ONE_REPRESENTATION | 中国語政治113問でQwen原本抑制98/113、特殊版Q4は4/113（作者測定）。一般的危険依頼はBF16で95/100拒否。特殊版の変更は独自だが、同じInterpretic版のBF16/FP8/Q4/IQ3は別学習モデルではない。Q4 main16.8GB+視覚0.93GB；IQ3は一般能力低下報告。 |
| [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | SPECIAL_TRAINED_STATE_IN_QUANTIZED_FORMAT | KEEP_EXISTING_CONDITIONAL_NO_LEGACY_QUANT_HOARD | 親trohrbaugh ARAと作者による追加2回のARA重み編集。名前はGGUFでもQwen公式の単純量子化ではない。旧RVN以前のlegacy GGUFを同じ最新重みとして全保存しない。 |
| [afdudley/Qwen3.8-27B-abliterated-NVFP4](https://huggingface.co/afdudley/Qwen3.8-27B-abliterated-NVFP4) | SPECIAL_TRAINED_STATE_IN_QUANTIZED_FORMAT_WITH_RECIPE | KEEP_EXISTING_HOLD_FOR_REPRODUCIBLE_METHOD | Heretic重み編集+固定ツール/設定/パッチ。NVFP4圧縮だけが価値ではない。作者は20.56GB重み、元のBF16 text-only別公開、生成手順の完全ビット再現は不可と明示。査読済み独立能力比較未了。 |
| [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | ORIGINAL_FAMILY | KEEP_EXISTING_CONDITIONAL | 音声・動画生成の基準モデル。Distilled/未蒸留/量子化は入力出力と品質が違う場合にのみ各固定形式を選ぶ。 |
| [ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | CLAIMED_SPECIAL_MERGE_IN_FP8_NEEDS_LINEAGE_AUDIT | KEEP_EXISTING_CONDITIONAL_RESEARCH_ONLY | 現行台帳は成人向けLoRA/蒸留/参照保持マージを主張。HFメタデータは親のquantizedタグのみで変更履歴とweight provenanceは別途固定が必要。『FP8だから通常量子化』とも『uncensoredという名前だから学習成果あり』とも推定しない。 |
| [Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | SPECIAL_RL_MERGE | KEEP_EXISTING_CONDITIONAL_SELECTED_REPRESENTATION_ONLY | 作者v1 2026-10-07 はOmniNFT RL訓練結果をマージ、蒸留LoRAもベイク。独自のNSFW生成と映像細部・動画音声品質を主張。Q4/NVFP4/int8は同じv1の形式選択であり独立した特殊版ではない。 |
| [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | SPECIAL_ADAPTER_DELTA | KEEP_EXISTING_CONDITIONAL_DELTA_ONLY_WHEN_BASE_SHA_CONFIRMED | 独自rank128アダプターの学習成果。対応する正確なQwen-Image2.1ベースを共有できればフルウェイトの再ダウンロード不要。親SHA未検証で節約確定としない。 |
| [ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | DISTINCT_MODEL_FAMILY_PUBLISHED_IN_QUANTIZED_FORMAT | KEEP_EXISTING_CONDITIONAL | 他のFLUX等の重みを単純変換したものではなくIdeogram系の独立学習済み画像モデルをNF4形式で配布している候補。量子化の文字列だけで能力が重複しているとは言えない。 |
| [unsloth/DeepSeek-V4.1-Flash-1017-GGUF](https://unsloth.ai/docs/models/deepseek-v4.1-flash) | ORDINARY_QUANTIZED_REPRESENTATION_OF_DIFFERENT_SOURCE_MODEL | SOURCE_MODEL_RESEARCH_HOLD_NO_INDEPENDENT_QUANT_SLOTS | DeepSeek V4.1 1017自体の552B backbone+196B Engram/コード性能を既存Qwen3-Coder等と比べる。UnslothのQ2とIQ2は同じ訓練済みDeepSeek原本の量子化なので別々の新規モデルとして数えない。150B超例外が通れば代表量子化形式一つで保存可能。 |
| [unsloth/Mistral-Large-4-1T-A52B-GGUF](https://unsloth.ai/docs/models/mistral-large-4) | ORDINARY_QUANTIZED_REPRESENTATION_OF_EXISTING_HOLD | KEEP_EXISTING_HOLD_NO_INCREMENTAL_QUANT_SLOTS | v19で既にMistral Large 4はHOLD。Unslothの2bit派生同士に新しい後学習能力はない。1T級モデル自体に他の大規模汎用モデルを上回る実証があった場合に実用表現を一つ選ぶ。 |
| [orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | WEIGHT_EDITED_SPECIAL_OVER_150B | KEEP_EXISTING_HOLD_SPECIAL_EXCEPTION | 約180B総数の拒否方向編集後学習成果。150B超の量子化を検討する理由は特殊重みの保存価値であり単にQ4であることではない。原本と量子化の両方を自動採用しない。 |

### 2. 特に重要な修正

**Interpretic v2** は通常QwenのQ4コピーではなく、政治回答の重み制御を加えた別学習状態をQ4で配布したもの。開発者Q4検証では政治113件中回答抑制4件（元Qwenは98件）。ただし有害依頼95/100件拒否はBF16測定でありQ4と混同しない。[モデルカード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)。InterpreticのBF16、FP8、Q4、IQ3を別々の独自モデルとして取得する必要はない。

**RVN Heretic** はARAを合計3回適用した特殊重み。RVN最新と過去のlegacy版を区別し、同じRVNからの多数のGGUFを一括取得しない。[配布元説明](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)。**afdudley**は特殊な編集重みと再現レシピを備える。NVFP4の圧縮だけが独自性ではない。[作者の再現条件](https://huggingface.co/afdudley/Qwen3.8-27B-abliterated-NVFP4)。

**Stubelius Remix LTX 2.5** はOmniNFTのRLマージと蒸留LoRAを含む特殊版。同じv1のQ4、NVFP4、INT8は形式選択。作者の29勝9敗10分のAI評価は参考値で、独立品質測定ではない。[配布元](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)。**ChrisColeTech**は台帳では成人向けマージとされるがHFメタデータではquantizedと記載され、改変の来歴は要検証。名前だけで採否を決めない。

**DeepSeek V4.1／Mistral Large 4** のUnsloth Q2とIQ2は、同じ訓練済み原本の通常量子化。普通の量子化を個別の新モデルとして足した旧R28案は取り下げる。ただし150B超の大規模原本自体が高い独自性と性能を持つなら、実行可能な**1つの量子化保存形式**として採用可能。単純に量子化モデル全部を除外しない。

### 3. 実施規則

学習成果を識別する単位は`base repo + fixed revision + training/edit/merge source + learned weight identity`。その下に`representation`（precision / quantization / shard / backend）を持つ。一つの学習成果に複数精度を選ぶのは実行互換性や非再現可能な独自量子化の明確な理由がある場合のみ。特殊版を複数保持する上限は機械的には設定しない。ベースとadapterを組む場合は元のSHAが一致したファイルのみ共有する。

### 4. H/T/D/C/U・変数表

| 記号 | 意味 | SI単位 | 定義／範囲／型 |
|---|---|---|---|
| N_s | 相異なる学習済み重み状態の数 | 1 | 0以上の整数スカラー、編集とRLマージを区別 |
| N_f | 同じ重み状態の保存形式数 | 1 | 0以上の整数スカラー、BF16・Q4等 |
| B | 完全な選択ファイル容量 | byte | 0以上の整数スカラーまたは未測定null、依存込み |
| M | 推論ピークRAM | byte | 0以上のスカラーまたは未測定null、OS/KV/依存込み |

**H**：特殊版が独自学習結果を保存するなら、親と実際に異なる行動・品質を示せる。**T**：来歴、元・派生SHA、特殊能力と一般品質の対応試験、実機backend/ABI/quant/zero-point/context/batchを固定して評価。**D**：重み状態が異なり機能の増分が認められるなら別の特殊版保存候補PASS。同じ原本の単純圧縮を独立モデルと数える場合はFAIL（必要な実行形式として別途保存可）。不明ならUNCERTAIN。**C**：GGUFでも特殊後学習済み、逆に名称が無検閲でも重みの変更がない可能性。**U**：未取得原本のSHA、マージ元、ライセンス、独立比較の欠測が主要誤差源。合成u_cおよび包含係数kは測定不足で未定義。単位確認：N_s、N_fは無次元、B、Mはbyteでありディスクとメモリは別の測定。

### 5. ERROR CHECK・次に考える問い

13件一意の配布元IDを記録。正式v19の150資産、Nanbeige4.3-33B SELECT、ユーザー指定EXCLUDED 6件と承認キューは変更なし。ダウンロード・削除0。機械学習、音声・映像工学、符号化/推論エンジン、デジタル保存・供給網へ転用可能。

**問い**：同じベース由来の特殊版を2つ残すとき、どの固有の制御性能・再現困難性があれば双方を保存する価値があるか。
