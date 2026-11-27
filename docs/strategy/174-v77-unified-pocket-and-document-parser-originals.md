# R174 / v77: 統合小型モデルと文書解析原本の追加（2026-11-28 JST）

基準 main: `ae97caf4e5c7bf51a73c1b2d6266cf5676411fa9`。並行R172 Indra OCR / DepthPro2研究およびR173 CTSM 1.5選定は全保持。正式差分 ADD 2、REPLACE/EXCLUDE 0、旧267行不変。研究 HOLD 1（未登録）。取得承認・重み取得・物理削除 0。

## 一次資料・比較
- Tencent [WePM 論文](https://arxiv.org/abs/2611.27365)、[4B固定原本](https://huggingface.co/tencent/WePocketModel1.0-4B/tree/d57517468ff546df8cb9c6da5c76319810d3523b)、[2B固定原本](https://huggingface.co/tencent/WePocketModel1.0-2B/tree/68d8975772f76ea053ce9f696e47b185d51936b4)、[固定コード](https://github.com/Tencent/WePocketModel/tree/8e32ded1ac20703599d57ff10a83230091a5b3bf)。11/23更新（7日窓）、コード11/26。MGVB/ULKD/SEMOによる生成・embedding・判断統合、必須aux重みを別保存する必要。4B作者HCD 65.1%/約8GB BF16対分離構成64.2–64.8%/21–43GB。作者の丸めた重みのみでありピークRAMや独立検証ではない。Qwen3 Embedding、Intern-Decision、Ivonnet、IVE、Kananaとは役割が重なるがタスク単位優越なし。4B ADD CONDITIONAL、2B独立原本は同一方式の追加価値と実機比較不足で研究HOLD、通常量子化は別登録しない。4Bの全repo 9,152,926,978 B、2B 4,492,710,970 B（差4,660,216,008 B）。Hub stored/target countとaux込み総数は区別、総数未確定。Apache-2.0と第三者条件、個別行為許諾未確認。
- NVIDIA [3.5 Parse固定原本](https://huggingface.co/nvidia/Nemotron-3.5-Parse/tree/ea2e1fe486bea3e7d0d505df9bafa4ad562407a0)、[DFlash2 manifest](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/ea2e1fe486bea3e7d0d505df9bafa4ad562407a0/dflash2/manifest.json)。公開10/17（90日窓）、更新11/14（30日窓）。11/26学習解説。SFT→GRPO 66.24→71.38、反復異常126→29。ParseBench 3-pass 75.20 / LightOnOCR-3-4B 75.10 / 0.8B 74.60。単一pass 72.74は既存0.8Bに劣る。処理回数異なるため上位互換としない。LightOnOCR、PaddleOCR-VL、DeepSeek-OCRを維持。ADD CONDITIONAL。F32 target 2,523,266,640 B、DFlash2補助原本178,657,376 B（manifest target hash一致、step148000、vLLM 0.32.1rc1.dev505+g00b6c4c56）。DFlash2は別学習成果だが任意の同一bundle部品であり独立モデル二重登録しない。作者target unique 630,800,496、Hub stored 630,800,504、MTPとdraft含む完全census未確定。OpenMDW-1.1、tokenizer MIT、第三者条件と個別行為許諾未確認。
- 両者とも公開ungated観測、配布条件変更の証拠なし。独立検証、所有者環境、完全復元、権利と安全評価は未完。危害実行能力・安全回避力は選定指標にしていない。

## 容量・保全
[候補原本全ページ](../../manifests/drafts/r174-2026-11-28-wepm-and-nemotron-immutable-source.candidate.json) は3repo 263 file refs、26 LFS SHA、16,380,934,947 B。採用2repo 241 refs / 11,888,223,977 B。Git OIDとLFS SHAを区別、重みは一切転送せず。全repo source参照であり、依存込み最終選択範囲ではない。既知active source proxy 3,923,105,480,792 → 3,934,993,704,769 B、49不明、4TBに対する既知source proxy残65,006,295,231 Bは物理空き容量ではない。200GB床、150B原則/512GB runtime、個別承認は維持。取得報告133件の現物再SHAはしていない。容量実増分=null。

## 実験計画
同一合法文書・画像・質問集合、同一機器/backend/precision/context/batchで既存各専門モデルと比較する。最低100問/タスク、ペア差と95% bootstrap CI、失敗/無回答/校正/速度/ピークRAM記録。閾値の事前登録（品質非劣性2ポイント、運用メモリ改善20%を暫定提案）は実験結果でない。CI下限が非劣性閾値を下回れば置換せず、独立評価まで保留。文書ではsingle/multi-pass、draft有無を別条件。重みは未取得・モデル未実行。

## 正本とゲート
269 tracked / 213 active (56 select,157 conditional,37 hold,13 deferred,6 excluded); all213 STOP. [差分](../../catalog/revisions/v77-2026-11-28.json)、[判断](../../catalog/decisions/2026-11-28-r174-wepm-parse-decisions.json)、[readiness](../../catalog/readiness/v77-2026-11-28-r174-all213-gates.json)。全旧行保持、承認キュー・取得台帳・選定方針は不変更。回帰テストは tests/test_r174_v77_specialist_originals.py。独立性能試験・所有者HDD・完全依存closureは未実施。
