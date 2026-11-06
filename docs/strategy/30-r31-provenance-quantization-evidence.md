# R31｜特殊学習済み重みと量子化の同一性：原論文・公開元・第三者の性能データによる再査定

> 2026-11-07、研究専用。既存v19の150資産（SELECT 53／CONDITIONAL 52／HOLD 27／BACKLOG 12／EXCLUDED 6）は変更しない。Nanbeige4.3-33B SELECT、4TB計画、approved queue空は維持。詳細な[機械可読7件台帳](../../catalog/research/2026-11-07-r31-special-weights-evidence.json)。R20で既に調査したDavidAUを**新発見と数えない**。

## 1. この回で明らかになった、R30からの実質的進歩

**保存対象は、学習済み状態ごと。形式だけ違うファイルは原則一つを選ぶ。** しかし、状態の違いが立証できても品質が低い版まで全部確保するのは過剰。追加の権利、同一条件の性能、将来の再現困難さ、選択SHAが必要。以下は『特殊版そのものを削除する』判断ではない。

### 1-A. Stubelius Remix：通常のLTX2.5 FP8とは異なる学習・マージ来歴を確認

[作者のREADME](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)と[NOTICE.txt](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/NOTICE.txt)が、Beta1のSulphur 2＋10Eros task-vector、Beta2のLTX2.5蒸留LoRA、v1のOmniNFT（[公開RL-LoRA](https://huggingface.co/zghhui/OmniNFT)）を段階ごとに列挙する。単純に量子化した原本ではない。作者v1対beta2の同じプロンプト／シード48件では、AI評価29勝・9敗・10分。『細部+55%、動作+15%』は統計的定義がなく外部測定ではない。

| v1の同じ学習状態の配布表現 | 作者表示の本体サイズ | 検証と保存判断 |
|---|---:|---|
| `ltx2.5-Stubelius_remix_v1_bf16.safetensors` | 42 GB | **長期保存の高精度原本として第一候補**。一つの特殊重みを後から再量子化可能な形で残す。ただし権利・SHAと完全依存は未確認 |
| `ltx2.5-Stubelius_remix_v1_int8_convrot.safetensors` | 21.5 GB | ComfyUIでの実行候補。BF16と両方取得する実用上の必要性は未証明 |
| `ltx2.5-Stubelius_remix_v1_nvfp4.safetensors` | 14.4 GB | Blackwell（RTX 50系）向け実験形式。作者はINT8との画質比較未完と明示 |
| `ltx2.5-Stubelius_remix_v1_Q4_K_S.gguf` | 12.5 GB | 低VRAM向け実験形式。作者はINT8との画質比較未完と明示 |

配布されるBeta1/Beta2はv1と**異なる途中段階の学習成果**であり、単純な量子化重複ではない。ただし現在の保存優先度はv1で、途中段階も比較・再現の理由が成立するまで全量保存しない。実行時はGemma4 12B text encoder、映像・音声の各VAEを別途要する。**42GBをフルパイプライン容量とはしない**。

**権利面**：README/NOTICEはLTX-2.x Community License AgreementのSection 4とAttachment Aを適用し、原LTX、Sulphur、10Eros、OmniNFT、変換コードの由来を別々に列挙する。年間売上1,000万米ドル以上の企業は指定の商用利用に別契約を要すると説明している。合法取得・学習元の実体や著作物の権利全てを確認したという意味ではない。

### 1-B. Interpretic：同じ特殊状態のQ4とIQ3では品質差が大きい

[Q4配布元](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)と[IQ3_XXS作者の同時比較](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-IQ3_XXS-GGUF)。政治回答の変更はInterpreticの特殊重み自体の特性。Q4とIQ3は別の後学習モデルではない。

| 量子化比較（作者の同時試験） | Q4_K_M | IQ3_XXS |
|---|---:|---:|
| モデル主重み | 約16.8 GB | 約10.5 GB |
| MMLU（1,000問）の正答率 | 81.9% | 78.0% |
| 中立質問110件の異常回答数 | 1件 | 7件 |
| 100件の有害質問に対する拒否数 | 92件 | 85件 |
| 中国語政治113件の回答抑制数 | 5件 | 3件 |

**結論**：4TB規模の保存で約6.3GBを節約するために品質劣化を選ぶ必要は薄い。既存R22のQ4構成（主重み16,810,714,592 byte、画像projector 927,606,944 byte）は維持し、**IQ3を追加の学習済みモデルとして保存しない**。IQ3に限定した低RAM用途が生じた場合は実行形式として別途検証。以前のQ4単独カードは政治抑制4/113と記載し、今回の比較表は5/113。**異なる評価実行の分子を混在させない**。

### 1-C. RVN Heretic：特殊ARAは本物だが、同一レポ内の大量量子化は不要

[0bserverx公式カード](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)は`trohrbaugh`のARAに追加2回の行列最適化を適用したと明記。作者は旧版拒否3/100からRVN 0–1/100、基準分布とのKL 0.0535から0.0085と報告する。ただし『2台のGPUでindependent』は**作者側の異なる実行環境**を指し、外部第三者の独立評価ではない。KL減少自体は実用タスク正答率の改善を証明しない。

現在の推奨`RVN-Q4_K_M-multilingual.gguf`は作者表示約15.41 GiB（十進GBではない）。必要な画像projectorは別途約0.63GB。**何十種類ものGGUFやMTP組込み版を一括保存しない**。なお旧`Qwen3.8-27B-Heretic-Q4_K_M.gguf`は新RVNとは別の以前のARA学習済み状態であるため、『同じ重みの通常量子化』として完全同一視しない。保存を先送りする理由は新版と比べた独自性の証拠不足。

### 1-D. DavidAU：第三者試験で一般能力も改善した特殊版

**既存R20の再検証**。特殊な段階学習＋Heretic編集＋healingを備えた`DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU`（Release #1）が[第三者スコア表](https://huggingface.co/datasets/spicysharkco/uncensored-leaderboard/blob/main/README.md)に収載されている。

| 同一Q6・同じ課題 | 通常Qwen3.8-27B | DavidAU release #1 |
|---|---:|---:|
| MMLU-Pro（500件） | 57.6% | 67.2% |
| GSM8K（250件） | 94.0% | 96.4% |
| 有害300件での拒否数 | 267 | 51 |
| 無害350件での拒否数 | 40 | 2 |

MMLU-Proの対応ありMcNemarの無調整p値は2.8e-7、全モデルが出力形式を守った430問に限っても差は+8.8ポイント（p=1.9e-6）。**ただし10比較の多重検定調整なし、訓練データ汚染未検査、GPU型番/クロック不明、評定者が競合モデルの量子化を配布する利益相反を開示。** 測定はQ6・固定revision prefix `fd6a26869dc5` のRelease #1だけに帰属し、作者の新しい別枝やQ4版に移してはならない。現時点は優先CONDITIONAL研究で、フルSHAと正しい選択ファイルを固定してから審査する。

### 1-E. 他の候補を無条件追加しない理由

- **[JonathanColetti版](https://huggingface.co/JonathanColetti/Qwen3.8-27B-Uncensored)**：外部同条件評価で有害拒否27/300、無害拒否0/350、MMLU-Pro57.2%、基準57.6%。特殊な重み編集であり単なる量子化ではないが、独自性は未確立。
- **[Huihui版](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)**：有害拒否34/300、無害拒否0/350、MMLU-Pro57.0%、基準57.6%。低拒否/一般能力維持という点ではJonathanや既存Orcaとの重複が大きい。双方自動取得しない。
- **[ChrisColeTech LTX2.5](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8)**：Hubには`base_model:quantized`と`license:unknown`のメタデータがあり、未認証の公開ページはSensitive Contentの案内まで。既存R30の『成人向けマージ』という説明を、変更系譜が実証されたと扱わない。逆に名称・量子化タグだけで、実際に特殊重みではないと断定しない。**通常の正規アクセスでのモデルカード・NOTICE確認までは取得lockなし**。

## 2. 次に進める実際の選定と容量の考え方

今の保存候補は『通常Qwen3.8派生も全部』『LTX量子化を全部』ではない。**異なる学習成果だけを評価**し、必要な能力に応じて形式を一つ選択する。Stubelius v1 BF16 42GBは特殊重みの高精度記録、DavidAU Q6は第三者が検証した特殊後学習の再現、Interpretic Q4は選択的回答編集を品質を落とさず実行する選択肢、RVN Q4 multilingualはARA比較系統を代表する研究構成。**これらはまだ4件のダウンロード承認ではない**。変更系統の違いを記録し、観測品質が不足するものをHOLDとする。

### 変数表

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| N_s | 一意な学習済み重み状態数 | 1 | 0以上の整数スカラー。特殊SFT/重み編集/RLマージごとに区分 |
| N_q | 1学習状態の保存形式数 | 1 | 0以上の整数スカラー。Q2/Q4/FP8等は別状態ではない |
| B | 選択する保存構成の完全容量 | byte | 全シャード・依存込み、未測定はnull。非負整数または欠損 |
| R | 実機推論RAMピーク | byte | OS・KV・audio/video encoder・backend込み、実測未了。非負実数または欠損 |
| N | 対照モデルと比較する課題数 | 1 | LLMの軸ごと最低200、動画20プロンプト×3seed。正整数 |

### H/T/D/C/U

**H**：異なる学習済み状態は一般能力を保ちつつ異なる特殊目標を満たす。一方、同じ状態の単純量子化は新能力を作らず、低ビットで品質を落とし得る。**T**：一次README/NOTICEとHF fixed commit、配布元SHA、独立固定データでMMLU-Pro・過拒否・安全拒否・出力破綻を比較。動画は20プロンプト×3seed、映像の同条件人手ブラインド比較と対応推定を行う。実機はCPU/GPU型番・クロック、OS/driver、backend ABI、quant zero-point、context、batch、Codec、推論ピークRAMと保存バイト数を記録する。**D**：固有重み・用途性能・権利・完全実行構成が成立する場合のみ正式SELECT審査PASS。劣化した同一形式の追加保存はFAIL、測定不十分・許諾不確かならUNCERTAIN。**C**：データ汚染、テンプレート差、量子化の破綻、学習元からの寄与と後マージの混同、比較母集団差。**U**：u_cと包含係数kは誤差分散・固定データ・機種不足のため数値化不可。単位チェック：N_s/N_q/Nは無次元、B/Rはbyte。ただしディスクのBと実行RAMのRは同じ単位でも物理的に別の測度。

## 3. ERROR CHECK・学際的な応用・次の問い

**ERROR CHECK**：7件一意の正規repo、R20の既存DavidAUを重複新候補と数えない、Stubelius 4形式を1学習状態と扱う、Interpreticの2つの政治評価を混同しない、RVN旧版と新版の重み変更を識別、Chrisは未検証と明記。正式150資産/105有効、ユーザーのNanbeige SELECT、4TB計画と空の取得承認キューは維持。モデル本体のダウンロード・実行0。

機械学習（重み編集/後学習）、統計（対応比較・多重検定）、動画生成（VAE/LoRA/制御）、デジタルアーカイブ・法務（差分重み/原本SHA/派生ライセンス）の4分野に転用できる。

**〈次に考える問い〉**：大容量を使えるとき、同じ特殊重みをBF16の高精度原本として保存する価値は、低ビット実行版との速度差・画質差・再構築可能性によって、どの条件なら逆転するか。
