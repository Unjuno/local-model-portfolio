# 独立蒸留多言語再順位付け — 2026-11-28

基準 main 3c64592e1483dcdc69d9e51330f251af87d28dae。直近7/30/90日と旧公開候補を調査。

ADD推奨 / CONDITIONAL研究限定: Horizon-Labs/multilingual-reranker-small @ 23139fec6f1f448cdf89a5ac2d2c6bf5e8c7b398。Publisher matched nDCG@10 MIRACL/Wikipedia/other/mean .779/.969/.793/.847 versus existing Qwen3-Reranker-0.6B .785/.958/.793/.845. 140641921 stored F32 elements; independent cross-encoder distillation rather than quantization. MIRACL lower .006; teacher Qwen3-Reranker-4B mean .875; BGE v2-m3 .866; Horizon 308M .855. MIRACL training-domain overlap, trained 384 tokens; no independent significance, long technical query generalization, matched owner hardware, batch, clock, latency or ABI evidence.

HOLD: CheezOne/reranker-chinese-japanese-korean-small — 独立教師だが同サイズで僅差、親MIT通知と追加価値未解決。旧alias重複不可。

HOLD: hq-bench/coreb-code-reranker — コード専用LoRA成果、8GB統合重み、単体adapter・依存・通常検索品質未確定。

KEEP: 既存Qwen3-Reranker-0.6B、embedding、ModernBERT/NandiBERT比較資産。置換・除外なし。

配布元31ファイル 1428709912 B、候補28ファイル 597202061 B、同一成果ONNX除外 831507851 B。FP32原本。教師推論不要、完全依存・実機・権利・復元未検証、owner増分null。承認0、重み転送0、物理削除0。[研究JSON](../../catalog/research/2026-11-28-horizon-reranker-distillation-evidence.json)、[候補マニフェスト](../../manifests/drafts/2026-11-28-horizon-reranker-source.candidate.json)。同一クエリ・候補集合・長さ層、CPU/GPU/クロック/バッチ/精度/ABI固定、paired bootstrap、遅延中央値・p95・ピークRAMを将来検証。速度優位・有意差は未確定。
