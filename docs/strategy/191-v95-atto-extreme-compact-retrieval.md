# R191 / v95: extreme compact independent retrieval

ADD NeuML/colbert-atto-90k-32d as non-executable CONDITIONAL/R2. Preserve concurrent v94 Transcoda and all 288 prior rows, 133 historical VERIFIED receipts; 289 tracked, 233 active, 177 conditional, all STOP. Source core pointer 362,720 B; full archive, runtime/index and physical bytes unknown. No rights inferred, no downloads or deletion.

## Evidence and decision

Independent pretrained and distilled Atto late-interaction learned state, not a quantization. 90.3K nominal FP32 parameters, 32-d token embeddings; distinctive extreme low-resource retrieval tradeoff rather than a new broad task. Preserve as research-only conditional; existing BGE-M3 already has multivector retrieval, so no replacement.

Publisher English 3-set nDCG@10 mean 0.4454 (ArguAna 0.3435, NFCorpus 0.3263, SciFact 0.6663); 840=0.3139, 9K=0.3655; compact learned state.

950K=0.4816, 4M=0.4818, 25M=0.4995, LateOn 110M=0.5463 on same publisher table; only three datasets, no matched BGE/Qwen/Horizon replay, HW/clock/batch not verified; max sequence 399 and English evidence only; index size, dependency ABI and complete bytes unknown.

conv-conditioned attention / PhaseGatedMoE, Wikipedia MLM then retrieval distillation; training parent NeuML/atto-90k-32d exact revision unresolved. Publisher examples txtai >=9.0, sentence-transformers >=6.0 MultiVectorEncoder, PyLate; custom code reviewed only as metadata, not executed; CPU/GPU RAM, ABI, index footprint and wheels unresolved.

- NeuML/colbert-atto-90k-32d: ADD — Independent pretrained and distilled Atto late-interaction learned state, not a quantization. 90.3K nominal FP32 parameters, 32-d token embeddings; distinctive extreme low-resource retrieval tradeoff rather than a new broad task. Preserve as research-only conditional; existing BGE-M3 already has multivector retrieval, so no replacement.
- NeuML/colbert-atto-950k-128d: HOLD — Higher publisher quality; 947K nominal, 128d; matched resource benefit unresolved
- NeuML/colbert-atto-4m-384d: EXCLUDE_THIS_ROUND — Mean 0.4818 vs 950K 0.4816; larger independent state; insufficient incremental advantage; not a quantization duplicate or irreversible exclusion
- Atto ColBERT 840 / 9K / 14M / 25M and dense siblings: HOLD — Separate trained states; exact state/source scope and task-resource benefit not established
- BAAI/bge-m3: KEEP — Complementary multilingual/context/quality role; matched comparison not established.
- Qwen/Qwen3-Embedding-0.6B: KEEP — Complementary multilingual/context/quality role; matched comparison not established.
- Qwen/Qwen3-Reranker-0.6B: KEEP — Complementary multilingual/context/quality role; matched comparison not established.
- Horizon-Labs/multilingual-reranker-small: KEEP — Complementary multilingual/context/quality role; matched comparison not established.

## Fixed source

- https://huggingface.co/NeuML/colbert-atto-90k-32d/blob/e1734c688cdc8413d08a72007b2e7240a2c3f66e/README.md
- https://huggingface.co/NeuML/colbert-atto-90k-32d/blob/e1734c688cdc8413d08a72007b2e7240a2c3f66e/config.json
- https://huggingface.co/NeuML/colbert-atto-90k-32d/blob/e1734c688cdc8413d08a72007b2e7240a2c3f66e/model.safetensors
- https://huggingface.co/NeuML/colbert-atto-90k-32d/tree/e1734c688cdc8413d08a72007b2e7240a2c3f66e
- https://huggingface.co/NeuML/colbert-atto-90k-32d/commit/e1734c688cdc8413d08a72007b2e7240a2c3f66e
- https://arxiv.org/abs/2004.12832
- https://arxiv.org/abs/2104.08663
- https://huggingface.co/BAAI/bge-m3

SHA-256 publisher pointer: `5f45c75b57a1a729ade4445d9c30b7f2b174df89913988486d74fbca6e15c6f6`. No actual payload hash computed. No confirmed license/access change. See catalog/research/2026-11-28-r191-atto-retrieval-primary-evidence.json and manifests/drafts/r191-2026-11-28-atto-source-partial.candidate.json.

## Next falsifiable test

Matched BEIR three tasks + multilingual held-out retrieval; report nDCG@10, recall, p50/p95 latency, peak RSS/VRAM, disk index bytes, rebuild time with identical corpus/tokenization protocol and explicit backend/batch/HW. No automatic approval.
