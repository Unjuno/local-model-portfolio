# R132｜v56小型・無検閲原本の新候補5件（2026-11-20）

## 1.〈本論〉
正本v56は211登録・164有効。既存のFrostWolf LFM3 1.7BとPhala Qwen3.8 27B LoRAは既にCONDITIONAL選定済みであり、今回の新候補に二重計上しない。公式Hugging Faceモデルメタデータを確認し、次の5件を研究台帳に追加した。**今回の正式選定追加0、重量取得0、正式承認0**。

| 順 | 一次配布元 | Hub表示総パラメータ | 判定 |
|---:|---|---:|---|
| 1 | [FrostWolf Spark-X2.6-4B-abliterated](https://huggingface.co/FrostWolfAI/Spark-X2.6-4B-abliterated) | 4.1121B | 小型公開Apache-2.0表示。元親との差分SHA、custom code確認待ち |
| 2 | [xtools DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic) | 9.4098B | 公開Apache-2.0表示。親9.6531Bとの差、MTP/補助重みを要確認 |
| 3 | [llmfan46 Gemma-4-31B-it-uncensored-heretic](https://huggingface.co/llmfan46/gemma-4-31B-it-uncensored-heretic) | 31.2731B | 公開。大型原本と既存無検閲VLMとの重複を調査後に判断 |
| 4 | [FrostWolf Frost-Cyber-Mini-1.0](https://huggingface.co/FrostWolfAI/Frost-Cyber-Mini-1.0) | 4.2058B | Gated、CC BY-NC-SA 4.0。本人アクセス・用途別権利・学習データの許諾がSTOP |
| 5 | [nazeshinjite Qwen3.8 Flash-Next Abliterated LoRA](https://huggingface.co/nazeshinjite/Qwen3.8-Flash-Next-Abliterated-LoRA) | 未確定 | 公開LoRAでも親MoE総数・150B実測例外・ライセンス未閉包でSTOP |

FrostWolf Sparkの公式Hubメタデータは「abliterated」を主張する一方、親へのbase_modelタグがquantizedなので、**単なる量子化を独立した学習成果と誤認しない**。まず出版社の固定revision、safetensors全重みSHAと親重みのSHAを照合する。xtoolsの編集後モデルとJackrong親はHub報告パラメータ数が異なるため、MTPや学習済み部品の有無を検査する。作者の「無検閲」「高性能」は実測ではない。

## 2.〈応用・転用例〉
モデル名・人気ではなく、独立した学習済み原本、権利、正確な固定ファイル、Windows上の復元可能性を評価する。既存FrostWolf LFM3とPhala LoRAの原本はpublisher固定20ファイル／3,488,671,793byteだが、所有者Dドライブの現物SHAと親Qwen完全依存を未確認。新候補より先に既存sourceの復元条件を解消する。

## 3. H/T/D/C/Uと変数表
**H**：別アーキテクチャの4B編集済み原本は同系統27B量子化複製より保存多様性を高める。**T**：5件の公式モデルカードメタデータ、親・編集後のimmutable source SHA/tensor census、同一HW・clock・backend・ABI・zero-point・context・batchで30反復以上の品質・速度測定。**D**：PASS研究=5件重複なし、正式選定0、承認0。FAIL=未許諾取得、同一量子化の別モデル計上、未知総数の最終lock。UNCERTAIN=編集差分、品質、権利、本人現物。**C**：親と同じ重み、MTP脱落、データ由来権利制限。**U**：Hubタグ誤分類、未確認Tensor、作者性能バイアス。合成標準不確かさu_cと係数kは分布不明で数値化不能。

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| N_total | 全学習済みパラメータ数 | 1（無次元） | 非活性MoE、MTP等を含む | 未知null、基準150B | 整数/null |
| B_source | 選択固定source容量 | byte（SI基本単位外） | 選択ファイル長の和 | 未確認null、非負整数 | 整数/null |
| R_peak | 実行時全ピークRAM | byte（SI基本単位外） | OS/KV/runtime/CPU/GPU、UMA重複なし | 未計測null、512GB未満の条件 | 整数/null |

**次元チェック**：N_totalは無次元、B_source/R_peakはbyteであり直接比較できない。量子化は全パラメータ数を減らさない。150B超の量子化例外は同条件30回以上の実測メモリ同等性、品質、速度、権利、本人承認を満たすまでSTOP。

**ERROR CHECK**：211登録・164有効、未登録新候補5件、正式選定0、承認0、重量取得0。モデル学習来歴・ライセンス法務・計算資源工学・長期デジタル保存を横断。

## 4.〈次に考える問い〉
Spark 4Bが親と異なる学習済み原本であるとSHA照合できた場合、既存LFM3 1.7Bと比べてどの独立能力を保全するか？
