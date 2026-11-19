# R114｜v48：無検閲Qwenの学習原本とGGUF再構成物の系譜訂正（2026-11-19）

## 1.〈本論〉結論とR113訂正

現行v48（201登録/154有効）の選定は変更しない。R113の「InterpreticAIと0bserverxのSafetensorsはどちらもGGUFより元の学習済み原本」という一般化は**誤り**。モデル作者のREADME原文を直接調査し、**0bserverxのSafetensorsは既存 `RVN-F16.gguf` からの再構成物**で、元のpre-GGUF BF16 checkpointではないことを確認した。

- **InterpreticAI**：作者の[BF16モデルカード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)はfull BF16 checkpoint、Qwen3.8-27BのMTP headを保持すると明記。固定revision `84ab13688128c19d5ef10be430bc5de649b7823f`、ルート32ファイル、55,586,056,799 bytes。モデル原本としてGGUF Q4より優先。
- **0bserverx RVN**：[Safetensorsモデルカード](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored)は、13 sharded safetensors/851 text tensors、F16 498とF32 353、text-only、MTP/visionなし、既存RVN-F16.ggufから再構成と明記。固定revision `c2cb2cfb239f2964595bee87fcfda55ad5fe33dd`、ルート26ファイル、53,810,927,493 bytes。**独立した再学習済み原本と数えず、再構成形式の推論互換性用候補**とする。

**RVNの再構成元GGUFを固定**：公式[GGUF API](https://huggingface.co/api/models/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/revision/ab8d7bd81d03117501e4da60cccdff4c80f0eea0?blobs=true)のrevision `ab8d7bd81d03117501e4da60cccdff4c80f0eea0`で、`RVN-F16.gguf` は **53,808,281,888 bytes**、publisher SHA-256 `f20c72c23a6564211c5e44af35ea1277d697c009ce8a25ab28d100447e0f155a`。このF16 GGUFは再構成Safetensorsの**既知の元形式**だが、元の学習時BF16チェックポイントと断定してはいけない。

同repoには `RVN-BF16.gguf`（53,808,281,888 bytes）、`RVN-F16-mtp.gguf` と `RVN-BF16-mtp.gguf`（各54,259,602,656 bytes）がある。MTP付加版は作者のSafetensors text-onlyと同じ学習済み集合とは限らない。4形式の一括保存は行わない。正確な出典・サイズ・SHAは[機械可読訂正](../../catalog/decisions/2026-11-19-r114-uncensored-lineage-correction.json)に記録。

## 2. ダウンロード候補の差し替え方針

| 系統 | 現行の研究候補 | 修正後のマスター候補 | 状態 |
|---|---|---|---|
| InterpreticAI | GGUF Q4＋mmproj 17.738GB | **フルBF16 55.586GB** | 原本優先、重複GGUFは別途必要性判定 |
| 0bserverx RVN | GGUF Q4 17.177GB | **RVN-F16.gguf 53.808GB** | 現在確認できる再構成元を優先。元の学習時BF16は未発見 |
| 0bserverx移植用 | Safetensorsルート 53.811GB | RVN-F16.ggufからの派生と明示 | 別の学習済み成果ではない。デフォルト二重取得しない |

容量はpublisher公開サイズであり、Dドライブの実空き容量ではない。R113統合15件sourceキューは現時点で旧GGUF Q4を指しているため、**新方針とキューの差分が存在する**。この文書をキューの暗黙上書きとせず、R114決定が先行し、キューの原本置換は権利/保存容量と完全復元条件を検証後に行う。既存のモデル資産を重複して登録しない。

## 3. 事実・推論・仮説

**事実**：モデル作者はRVN SafetensorsをGGUFから再構成と明示。InterpreticAIはフルBF16とMTPを明示。両repoの固定revision・file size・LFS SHAをpublisher APIで確認。両系統のメタデータはApache-2.0、非Gated。

**推論**：再量子化や将来のモデル変換を重視する保全では、InterpreticAIのBF16とRVNのF16 GGUFをマスター候補とするのが合理的。ただし、RVNのF16 GGUFは元の学習時重みの完全復元ではない。

**未検証**：作者の無検閲性能主張の再現、学習系統の独立性、MTP付きRVNとF16の関係、全推論依存、本人のライセンス利用行為、Windows Dドライブ容量。将来の配布禁止確率を数値化しない。

## 4.〈応用・転用例〉H/T/D/C/U

機械学習では重み精度・学習時重みの系譜と推論形式を区別する。ソフトウェア供給網では固定revisionとSHAで再取得可能性を測る。情報法では現在の公開権限と将来の規制仮説を分ける。

- **H**：BF16/F16ソース保存はQ4のみよりモデル変換の自由度を維持する。
- **T**：作者の変換記録を確認し、同じ32件以上のテスト・固定seed/バッチ1でF16とQ4の差を測る。原本の再現可能な推論環境が必要。
- **D**：系譜と全ファイルのSHA・復元が一致すればPASS、欠落/無許可ならFAIL、現在はUNCERTAIN。
- **C**：F16 GGUFも元BF16から変換済みであり、欠落したtrained tensorsを回復できない可能性。
- **U**：未測定の品質・本人実機・コード依存・ライセンス・作者の前段階checkpointの消失。統計的反復がないため合成標準不確かさ u_c と包含係数 k は未算出。

### ERROR CHECK

- v48の201登録/154有効、既存選定・承認キューは変更なし。
- R114では実重みDL0、本人Dドライブ実測0、ローカルSHA0。
- **R113の「0bserverx Safetensorsが元の学習原本」という主張を明示的に訂正**し、RVN F16 GGUFのrevision/bytes/SHAを一次資料で固定。

## 5.〈次に考える問い〉

失われた学習時BF16 checkpointが存在する場合、GGUF F16を唯一の残存マスターと見なすか、それとも配布者に元チェックポイントの所在を確認してから保存形式を確定するか。
