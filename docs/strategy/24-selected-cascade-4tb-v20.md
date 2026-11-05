# v20：4TBの選定枠とCascade2原本・学習来歴の正式選定

## 採用判断

2026-11-06の「リポに選定して入れて、4tまで」という指示を受け、前回の非実行提案から3件を**正式なconditional選定**へ反映する。条件付きは有効選定であって取得承認ではない。旧v19の150レコードを保存し、Orca FP8は重複形式としてdeferredを1件追加。**新規4レコード、うち採用3件。計154資産／有効108件**。旧105件の採否を勝手に変えない。

正本：[CURRENT](../../catalog/CURRENT.json)、[v20全件](../../catalog/effective-portfolio-2026-11-06-v20.json)、[差分](../../catalog/revisions/v20-2026-11-06.json)、[108件非実行キュー](../../queues/proposed-v20-2026-11-06.json)。変更はstrategy/2026-11-03-01-riskブランチだけ。

| repo ID | 採否・範囲 | 一次資料の表示容量（概算） | 今回の計画上限 | 固有価値と未解決事項 |
|---|---|---:|---:|---|
| nvidia/Nemotron-Cascade-2-30B-A3B | conditional、公式原本と必要部品 | 全repo約63.2GB | 80GB | 数学・コード推論の独立後学習。全MoE約31.5779BはHFの丸め表示。全tensor・固定版・実機・部品権利は未確認。 |
| nvidia/Nemotron-Cascade-2-RL-data | conditional、4部分 | 全repo約2.86GB | 5GB | IF/RL/MOPD/SWEの学習来歴。元のデータ・コード条件、重複、環境の再現性は別審査。 |
| nvidia/Nemotron-Cascade-2-SFT-Data | conditional、math/math_proof.jsonlとswe/swe_agentic.jsonlのみ | 約55.9GB＋12.5GB、約68.4GB | 80GB | 数学証明とagentic SWEを優先。**全593GBは不採用**。全SFTの再現用コピーとは呼ばない。 |
| orcarouter/Qwen3.8-27B-Uncensored-FP8 | deferred、既存原本との重複 | 今回の採用容量に含めない | 割当なし | クラウド形式の実用性と独立価値が確認できるまで追加保存しない。 |

今回の採用3件は表示容量の合算で**約134.5GB**、計画上限の割当は**165GB**。165GBは管理上の停止境界であって実測された最大容量ではない。metadata・依存・stagingを含む固定した取得容量は未確定。既存全件の選択容量も未確定なので、**全ポートフォリオが4TBに収まると検証したわけではない**。未確定を0にせず、最終合計と残量はnullのまま保持する。

## 4TBの意味

選定の許可上限を**4,000,000,000,000 byte（十進4TB）**へ更新する。容量を必ず埋める目標ではない。実測空き200,000,000,000 byte、既存ファイル、一時領域は独立条件。物理実容量がちょうど4TBなら、既存ファイル・一時領域を除く前でもペイロードは3.8TB以下になる。これは選定枠を3.8TBへ戻す意味ではなく、実機の物理上限と論理予算を区別するためである。HDDは未接続・未計測。

## 根拠と負の根拠

[Cascade2公式カード](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B)と[原論文arXiv:2603.19220](https://arxiv.org/abs/2603.19220)が後学習手法と比較を公開する。一般知識・多言語・agent系の全項目で既存Qwenを上回るわけではない。作者の競技結果をユーザー機器の速度や一般能力保証へ転用しない。

[RLカード](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data)は4部分の由来を記す。[SFTカード](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data)、[数学ファイル](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data/tree/main/math)、[SWEファイル](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data/tree/main/swe)から保存範囲を限定した。Web抽出にはキャッシュがあり、今回のアクセス日時は新規リリース日時ではない。最終immutable revisionと完全ファイルSHAは別に固定する。

[NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/)のGuardrail・規制対応改訂・別部品条件と、[ODC-By](https://opendatacommons.org/licenses/by/1-0/)のデータベース権利／個別コンテンツの区別を記録する。上位ライセンス本文を読んだことは、全素材の権利審査や利用者の同意を済ませたことではない。危険性や配布停止の可能性で権利を迂回しない。

## 検証・境界

生成処理はPython標準ライブラリでカタログJSONを読むだけ。モデルのimport、重み取得、外部API呼出し、HDD操作、クラウドGPU契約を行わない。既存全150レコードとqueues/approved.jsonを維持。新規モデルは全MoE総数150B未満を必須とし、既存150B超HOLDを昇格させない。unknown総数の取得準備停止は維持。

10個の合成fixture単体テストは、重複、150B境界、不明総数、誤承認、予算超過、旧レコード保存、非実行キューを検査する。これは実機性能テストではない。実リポジトリでは適用後に既存全テスト、check_parameter_cutoff.py、audit_selection_decisions.pyを別途実行し、その出力を確認する。実行前に成功したとみなさない。

**H:** 指定3件が既存能力と学習来歴を重複を抑えて補完する。**T:** 固定版・権利・全量を先に確認し、モデル比較は別の許可済み実機評価で行う。**D:** 容量上限超過・権利不適合・補完性不成立なら取得を停止し再選定。**C:** Qwen等で用途が完全代替される、元データと完全重複する。**U:** 表示容量の丸め、未固定revision、未測定の速度・品質・依存容量。合成不確かさの数値は未算定。

法・契約の適合、機械学習の比較評価、ソフトウェア供給網の固定版、保存工学の容量管理を分離する。次に判断すべき問いは、数学証明とagentic SWEの二部分に、将来の研究目的に対する十分な補完価値があるか。
