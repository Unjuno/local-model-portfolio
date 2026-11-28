# R198 / v102: Tofazzol v2.1 local search-plan specialization

Parent 2b2dfe82c84f081d805a262414f37646053e6e32. 288登録・232有効（SELECT 56、CONDITIONAL 185）。独立全パラメータ後学習1.544Bを研究限定CONDITIONAL追加。既存287行・133取得報告保持。全232取得STOP、承認・重みDL・実行・物理削除0。

[Source manifest](../../manifests/drafts/r198-2026-11-28-tofazzol-source.candidate.json) / [research](../../catalog/research/2026-11-28-r198-local-search-specialist-evidence.json) / [decision](../../catalog/decisions/2026-11-28-r198-tofazzol-formal-add.json) / [overlay](../../catalog/revisions/v102-2026-11-28.json) / [readiness](../../catalog/readiness/v102-2026-11-28-r198-all241-gates.json).

Independent full-parameter search-plan specialization (C-600 continuation) of Qwen2.5-Coder-1.5B-Instruct, 1,543,714,304 BF16 parameters. English natural-language-to-typed document/filename/metadata/Outlook search plans, distinct from embedding/reranking and GUI agents. Private training corpus and intermediate checkpoints unavailable; exact trained BF16 cannot be recovered from base or ordinary quantization. Research-only.

Positive: Publisher exact executed development results: 735/746 files, 217/240 synthetic mail, 952/986 overall; metadata 262/266 vs Gemma 4 31B 255/266. Private confirmation B v2.1 80/100 vs v2 66/100 (15 gained, 1 lost), one mailbox, not public replication. Publisher MLX release consistency regenerated 986 answers. No speed/cost claim.

Negative: Gemma 4 31B 973/986 overall and 240/240 mail vs 952/986 and 217/240; two-file-case margin not superiority, unequal adaptation budgets, adaptive board, comparator runs are for preceding v2. App-assisted v2.1 735/746 vs v2 736/746. Historical inputs/executor unavailable, English only, possible missing constraints and sender/recipient errors. No independent held-out comparison, owner runtime or cross-backend parity.

Fixed HF revision a84e48a8a369135ffccb4a2c30f3a1483c0265fd; published 2026-11-13 04:19 UTC, updated 05:05 UTC. API + 2-page complete tree: 56 files 3,100,135,228 B; selected 34 files 3,099,316,333 B including original BF16 3,087,467,144 B, tokenizer, contexts, inference/training code, evidence. Optional paper figures omitted. 12 small text files matched Git OID and publisher SHA256SUMS; overlapping LFS and sums agree as publisher metadata, not locally verified weights. No weight acquisition. Dependencies and owner bytes unknown; no reservation increase. Apache-2.0 weights; MIT code; private data not included. MLX 0.32.2 and MLX-LM 0.31.3 measured path, Transformers 5.15.1 portable path not equivalent. No owner hardware/clock/batch latency or memory measurement.

## Comparison
- ADD porkr/Tofazzol-v2.1-1.5B: Independent full-parameter search-plan specialization (C-600 continuation) of Qwen2.5-Coder-1.5B-Instruct, 1,543,714,304 BF16 parameters. English natural-language-to-typed document/filename/metadata/Outlook search plans, distinct from embedding/reranking and GUI agents. Private training corpus and intermediate checkpoints unavailable; exact trained BF16 cannot be recovered from base or ordinary quantization. Research-only.
- KEEP google/gemma-4-31B: Existing SELECT base comparison; publisher compared Gemma 4 31B but exact incumbent revision/instruction status parity unverified. Higher aggregate and mail results. Existing full-source proxy 62,578,664,883 B.
- KEEP NeuML/colbert-atto-90k-32d: Concurrent v101 extreme-compact late-interaction retrieval; complementary query-plan stage, not a replacement.
- KEEP BAAI/bge-m3: Existing multilingual dense/sparse/multivector retriever; distinct scoring/index interface, no matched planner equivalence.
- KEEP Qwen/Qwen3-Reranker-0.6B: SELECT relevance scoring, 1,207,488,344 B source proxy; not a typed search planner.
- KEEP Horizon-Labs/multilingual-reranker-small: 140.64M independent multilingual ranker, 597,202,061 B candidate source; complementary stage.
- KEEP ibm-granite/granite-4.1-3b-llmon-preview: Instruction/data separation research, not query executor or permission enforcement.
- KEEP perplexity-ai/pplx-decider-flash-v1.3: Noncausal judgment/span extraction, different interface.
- KEEP Hcompany/Holotron4-30B-A3B: GUI/MCP learned agent, no matched task results or constrained query plan equivalence.
- EXCLUDE mradermacher/Tofazzol-v2.1-1.5B-GGUF: Same learned state conversion, revision a12bb5c5b349e282a2ebe8e06fd7484161ee63a8; no separate archival asset; optional runtime format only.
- HOLD Inomjonov/tiny-voca-english-reproduction: Independent scratch reproduction, inference.pt 18,209,221 B, full 28,350,980 B; versus selected n4ze3m/tiny-voca 4,537,297 core and 23,626,858 B candidate scope, lacks matched WER/MOS and complete census.
- HOLD Kai9987kai/Supermix-Tether: Tiny specialist dependence/shortcut-learning experiments, 146 files 13,852,584 B; many seed/control checkpoints, complete learned dependency census and license unresolved.

HF newest 100 lastModified sample plus web 7/30/90-day searches, bounded not exhaustive. Independent matched benchmark not run. No change to acquisition ledger, approval queue or rights/safety/physical gates.
