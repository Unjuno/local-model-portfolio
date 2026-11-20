# R133｜Spark4BとHeretic9B 高精度原本の研究採否（2026-11-20）

**状態**：現行`CURRENT` v56/211登録・164有効のまま。v57への正式差分を作成したがGitHubのrate limitで`main`反映に失敗。**正式CONDITIONAL追加は未達成**。所有者Dの現物SHA/権利/ABI/容量と`queues/approved.json`の取得承認も未完了。

## 保存すべき原本

- [FrostWolf Spark-X2.6-4B Abliterated](https://huggingface.co/FrostWolfAI/Spark-X2.6-4B-abliterated) `505257b7969eb03a5a62d81f9afec6f88abd26e4`：出版社22ファイル／8,239,173,287 byte、重量LFS SHA256 2件、BF16 4,112,079,360 params。Heretic ARA元親は5 sharded weights、編集後は2 shard。再分割によるファイルSHA相違だけではテンソル差を証明しない。作者の100問拒否率2/100とKL0.0177は独立未再現。custom code未監査。
- [xtools DeepSeek-V4-Pro Qwen3.5-9B Uncensored Heretic](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic) `fbccdc6adf70a1981e8f40e91a8370e428e4f998`：出版社19ファイル／19,331,656,364 byte、LFS SHA256 6件。主index 9,409,813,744に15テンソル/486,583,016byteのMTP headを加えた総学習済み数**9,653,104,368**。古いMTP欠落版を採用しない。親や教師データの利用権とMTP/vision backend未検証。

[固定41ソースマニフェスト](../../manifests/drafts/r133-2026-11-20-spark4b-and-heretic9b-bf16-mtp-originals.candidate.json)はGitHub mainに保存済み。**27,570,829,651 byteはPublisher選定の論理容量**、本人の必要増分転送量ではない。

旧weight規制については米BIS 2026-11-19 [Federal Register 91 FR 74970](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)でECCN4E091を撤回しており、差し迫った一律所有禁止を証明するものではない。

## H/T/D/C/U

**H**：2原本を先行保存研究に加えると小型異アーキテクチャとMTP蒸留の多様性が増す。**T**：Publisher41件のSHA、ownerの個別ファイル実SHA、ライセンス全文、同HW/clock/backend/context/batchの30反復試験。**D**：PASS metadata=41ソース、8 LFS SHA、MTP15、正式取得承認0。FAIL=旧9.4098Bを全数と誤認、量子化派生重複、権利未確認取得。UNCERTAIN=実Tensor差・実機性能。**C**：再シャーディングに由来するSHA差のみ、MTP非対応、モデル品質低下。**U**：作者報告バイアス、モデル現物/ABI、行為別権利。

|記号|意味(日本語)|SI単位|定義|範囲・前提|型|
|---|---|---|---|---|---|
|N_total|9B全学習済み数|1(無次元)|9,653,104,368|MTP込み|整数|
|N_core|主index個数|1(無次元)|9,409,813,744|MTP除外|整数|
|N_mtp|別MTP個数|1(無次元)|243,290,624|15 tensors|整数|
|B_source|二原本ソース容量|byte(SI基本単位外)|27,570,829,651|物理増分ではない|整数|

**次元確認**：主9,409,813,744＋MTP243,290,624＝9,653,104,368無次元。8,239,173,287＋19,331,656,364＝27,570,829,651 byte。

**ERROR CHECK**：既存正本v56未変更。候補2、原本41ファイル、新重量取得0、approved0。追加選定は書き込み制限のため**未反映**。

## 〈次に考える問い〉

GitHub書き込みが復旧した後、v57で2モデルをCONDITIONALに昇格しつつ、所有者の物理SHAとABI実測を取得の必須ゲートとして維持できるか？
