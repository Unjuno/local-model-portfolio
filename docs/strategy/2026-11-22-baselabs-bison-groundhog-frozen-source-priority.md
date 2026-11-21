# 2026-11-22: Base Labs Gemma 4 decision-specialist original-preservation judgment

This is a **technical preservation recommendation**, not a source download approval or a canonical v64 catalog change. Keep existing v63 decisions intact. The 32-file machine-readable original source is at [immutable Bison/Groundhog census](../../catalog/research/2026-11-22-baselabs-bison-groundhog-immutable-source-selection.json).

## Fixed originals, with no weights transferred

| Publisher | Frozen 40-character revision | Publisher files | Source bytes (decimal) | Full model parameter count |
|---|---|---:|---:|---:|
| [baselabs/bison-1](https://huggingface.co/baselabs/bison-1) | `bf8350b2c59eb6c36e95d02a2af870aec18724a7` | 16 | 65,398,108,261 | 31,273,086,512 |
| [baselabs/groundhog-1](https://huggingface.co/baselabs/groundhog-1) | `f4602c43599114a7af2c158472b59a4ff2d13663` | 16 | 53,120,939,617 | 25,805,933,872 |

The manifest records upstream Git blob SHA1 or LFS SHA256 for every file, including tokenizer, model shard index, `readout.json`, LICENSE/NOTICE and two original trained checkpoint shards each. **All local-SHA flags are false**; the byte totals are publisher file references rather than verified owner storage. The models are distinct full fine-tunes of Gemma 4, not alternative GGUF quantizations. They were observed ungated/public at their frozen revisions.

## Decision, reason for non-duplication

1. **Bison: prioritize a future formal conditional source selection**. It is an independently post-trained 31B decision checkpoint with 128k *advertised API context*, text + image input and single-pass calibrated probabilities. The [publisher](https://www.baseten.co/blog/meet-bison-1-and-groundhog-1/) quotes Artificial Analysis Decision Index v2.1 **76** of 19 evaluated decision systems and Brier score **0.14**, based on [the evaluator's six-domain methodology](https://artificialanalysis.ai/methodology/decision-index). The exact hardware, clock, batch, latency and local reproducibility were not measured. Keep its BF16 publisher original, not its redundant quantized formats.
2. **Groundhog: research HOLD as alternative, not an automatic second acquisition**. The full checkpoint has 25.806B total parameters even though a routed token uses about 4B active parameters. It has a publisher file-size advantage of 12,277,168,644 bytes, but insufficient comparable independent accuracy and real-world memory/latency evidence to warrant both full originals immediately.
3. **No replacement of small specialists**. The current `internlm/Intern-Decision-0.8B` and `perplexity-ai/pplx-decider-flash-v1.3` are not strictly dominated by a 65GB BF16 source. Performance and portability need tests on identical tasks and runtime environments.
4. **License correctness**. HF's `license:other` label is not a claim that these models are unlicensed. The [Bison publisher LICENSE](https://huggingface.co/baselabs/bison-1/blob/bf8350b2c59eb6c36e95d02a2af870aec18724a7/LICENSE) states MIT for the producer's modifications and Apache-2.0 for the Google Gemma 4 source, with origin explicitly recognized in [NOTICE](https://huggingface.co/baselabs/bison-1/blob/bf8350b2c59eb6c36e95d02a2af870aec18724a7/NOTICE). Preserve both license files and validate owner's intended usage acts; full downstream dependencies are not approved here.
5. **Execution blockers**. A complete local restore still needs the exact Gemma 4 readout, tokenizer and inference backend ABI; RAM/VRAM, context length and staging estimates; owner actual drive free bytes and matching SHA256; and owner's separate rights and approval. Do not use unreviewed repository code during source audit.

## Falsifiable check

- **H:** Bison achieves a reproducible quality/calibration advantage of 3 index points over Groundhog on matched held-out decision tasks while operating within owner hardware memory limits.
- **T:** Fix six benchmark families and a minimum 200 disjoint examples per family (1,200 total), one exact preprocessing pipeline, same GPU, driver, clock, context, backend and batch. Freeze the dataset in advance; stop early only on rights/runtime failure.
- **D:** PASS requires Bison's 3-point improvement and a positive 95% bootstrap interval at practical local memory; FAIL on runtime/license ineligibility or verified inferior quality, otherwise UNCERTAIN. **No local test was run.**
- **C:** Groundhog may win on cost per decision or Bison may benefit from benchmark overlap and nontransferable inference software.
- **U:** Owner checksum, source-rights specifics, installed CUDA/Transformers ABI, hardware and sampling variance remain unknown. A numeric combined standard uncertainty `u_c` and coverage factor `k` cannot be computed without measured trials.

Adjacent domains: ML architecture and calibration; software supply-chain integrity; statistical decision theory; software licensing and policy. The study transferred **0 model bytes**, added **0 acquisition approvals** and changed **0 canonical selections**.
