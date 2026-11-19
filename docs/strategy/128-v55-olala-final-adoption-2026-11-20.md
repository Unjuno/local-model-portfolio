# R128: Olala original 2成果の正式選定・整合台帳 v55

**日付：2026-11-20。正本main v55＝209登録／162有効（SELECT53＋CONDITIONAL109）**。正式追加2件・旧207件不変・承認／重み取得0。詳細の一次観測は[元研究](docs/strategy/128-olala-small-hybrid-two-distinct-originals-research-2026-11-20.md)、[Publisher固定33files/9LFS_SHA source](manifests/drafts/r128-2026-11-20-olala-mini-final-and-base-originals.candidate.json)、[overlay](catalog/revisions/v55-2026-11-20.json)、[readiness](catalog/readiness/v55-2026-11-20-r128-all162-gates.json)。

## 1.〈本論〉正式採用と保留

[Olala-v1.0-mini-7A1B](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B)をCONDITIONAL/R1、Publisher BF16 original20ファイル13,595,420,813byteとして選定。[Olala-v1.0-mini-7A1B-base](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B-base)をCONDITIONAL/R2、事前学習12.8T token原本13ファイル13,591,509,967byteとして選定。双方6,773,124,144全学習格納parameterでモデル本体SHA256は別。事前学習状態をSFT+RLから完全復元できない。SFT中間原本は別trained resultだが増分13.59GBの実験価値未証明で保留。GGUF/MLX/量子化違いは独立trained modelとして採用しない。

**規制リスク**：確認済みは現時点のPublisher repo public ungated／Apache2.0 LICENSEと上流Qwen tokenizerのNOTICE。モデルごとの公開停止や全面規制の時期・確率は未確認。Baseが無検閲であることも未測定。カスタムMamba3/Attention/MoEは標準Ollama・llama.cpp・vLLMでは作者forkなしに動かない。owner Windows GPU/CPU、CUDA/driver、backend ABI、量子化ゼロ点、context、batch1、品質と速度未検証。本人行為別契約・D実容量・SHA・offline restore・個別取得承認のすべてをSTOPゲートとして残す。

## 2. 旧集計の修正と容量

v54 materialized内の181モデルを再計数するとPASS157＋OVER150B例外2＋総数不明22＝181だが、v54 CURRENT expectedはPASS158と誤記。v55はPASS159（157＋Olala2）／OVER2／UNKNOWN22＝183モデル、26 datasetで209登録。既存選定207件の判断変更なし。既報告61取得モデルのowner現物再ハッシュ・完全復元は本研究では実施していない。

## 3. 変数表、単位検証

| 記号 | 意味（日本語） | 単位（SI/備考） | 定義 | 範囲／前提 | 型 |
|---|---|---|---|---|---|
| S | 2Publisher原本の合計 | byte | 27,186,930,780 | 実際のディスク増分ではない | 整数スカラー |
| P | 1重量最大ファイル | byte | 13,579,677,592 | Publisher原本 | 整数スカラー |
| F | 最低空き床 | byte | 200,000,000,000 | owner実測必要 | 整数スカラー |
| H | 保守的一時領域込みの必要空き参考値 | byte | S＋2P＋F | 外部コード/OS等別 | 整数スカラー |

H＝27,186,930,780＋2×13,579,677,592＋200,000,000,000＝254,346,285,964 byte。全てbyteで次元整合PASS。ユーザー物理Dの現在空きの証拠ではない。

## 4. H/T/D/C/U、ERROR CHECK

**H**：後学習推論モデルと事前学習Baseは独立の将来価値がある。**T**：33fileのPublisher SHAと学習段階相違を静的確認済み。今後30件以上の日本語・agent・code課題を同じHW/driver/clock/backend/quant zero-point/context/batchで測り、実機オフライン復元と同じ固定sourceのSHAを確認。**D**：正式選定の一意性・件数・Publisher重量SHA相違はPASS_METADATA。実機と本人行為別法的許可はUNCERTAIN。未承認DL/unsafe code実行はFAIL。**C**：実用品質が別の小型モデルより低く、保存容量の価値が不十分であれば段階的再評価。**U**：active expert数の作者資料1Bと1.5B表記差、owner HW/ABI/再現試験不足。合成標準不確かさu_c、包含係数kは測定反復不足で数値化できない。

**ERROR CHECK**：209資産、162有効、183モデル＋26 dataset、全量子化重複追加0、source33ファイル27.187GB、approved0、重み追加DL0、実機現物SHA0、既存削除0。

関連分野：状態空間AI・Mixture-of-Experts、アラインメントと後学習、内容アドレス長期保全、モデル配布政策、推論ABI/サプライチェーン。

## 5.〈次に考える問い〉

Baseから後学習済み原本への有用性差が同条件で小さいと判明した場合、Base13.59GBの再学習価値をどう検証して保持するか。

