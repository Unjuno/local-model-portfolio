# v32 selected-model publisher metadata review — 2026-11-15

## Scope

Read-only check of **10 currently selected model IDs** against the connected Hugging Face repository-details service on 2026-11-15. Canonical selection: `catalog/CURRENT.json` → `v32-20261114`, 182 tracked, 135 active. This document adds fresh source metadata evidence without changing the canonical selection, download approval, or any parameter gate.

| Selected model ID | Hub model parameter count (if supplied) | Hub license tag | Source |
| --- | ---: | --- | --- |
| `microsoft/Fara1.5-27B` | 27,356.7M | MIT | https://huggingface.co/microsoft/Fara1.5-27B |
| `Qwen/Qwen3-Coder-Next` | 79,674.4M | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-Coder-Next |
| `KlingTeam/LivePortrait` | not returned | MIT | https://huggingface.co/KlingTeam/LivePortrait |
| `microsoft/VibeVoice-1.5B` | 2,704.0M | MIT | https://huggingface.co/microsoft/VibeVoice-1.5B |
| `OpenMOSS-Team/MOSS-TTS-v1.5` | 8,489.8M | Apache-2.0 | https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5 |
| `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | 1,928.7M | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base |
| `ResembleAI/chatterbox` | not returned | MIT | https://huggingface.co/ResembleAI/chatterbox |
| `Tongyi-MAI/Z-Image-Turbo` | 6,154.9M | Apache-2.0 | https://huggingface.co/Tongyi-MAI/Z-Image-Turbo |
| `Wan-AI/Wan2.2-TI2V-5B` | not returned | Apache-2.0 | https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B |
| `openai/gpt-oss-120b` | 116,829.2M | Apache-2.0 | https://huggingface.co/openai/gpt-oss-120b |

**Observed:** All 10 repository identities were returned by the connected Hub tool, and all 10 license *tags* were reported. Seven supplied numerical Hub model parameter counts; three did not. Model-name size (for example, `1.7B` or `120b`) is not an independently established full inference pipeline total.

**Important correction to completion claims:** A Hub parameter field may be calculated from a particular hosted weight configuration and can exclude separately loaded codecs, encoders, or other trained modules. A tag of `mit` or `apache-2.0` is not a substitute for exact governing weight license text, and the presence of a repository is not proof of full immutable file access. No files or model weights were downloaded.

## Source-specific dependency review queue

- `microsoft/Fara1.5-27B`: Hub reports a Qwen3.5-27B fine-tune lineage. Determine whether all required multimodal components are embedded or external; preserve provenance.
- `Qwen/Qwen3-Coder-Next`: Hub reports 79.67B and `qwen3_next` architecture. Count **total**, not active, MoE parameters, including all experts, and inspect tokenizer/config requirements.
- `KlingTeam/LivePortrait`: no numerical Hub count returned; enumerate motion/appearance modules, face detectors and other trained dependencies.
- `microsoft/VibeVoice-1.5B`: Hub reports 2.704B despite the product name; inspect codec and auxiliary component scope.
- `OpenMOSS-Team/MOSS-TTS-v1.5`: Hub reports 8.49B; external MOSS codec dependency must be accounted for separately and deduplicated only with immutable hashes.
- `Qwen/Qwen3-TTS-12Hz-1.7B-Base`: Hub reports 1.9287B; determine exact codec and tokenizer model requirements.
- `ResembleAI/chatterbox`: model total absent from this metadata result; resolve checkpoint manifest and audio dependencies.
- `Tongyi-MAI/Z-Image-Turbo`: Hub reports 6.1549B; include selected text encoder and VAE, not merely the transformer.
- `Wan-AI/Wan2.2-TI2V-5B`: count trained video VAE/text components and the exact inference pipeline.
- `openai/gpt-oss-120b`: Hub reports 116.8292B; verify complete MoE experts, tokenizer, quantization representation, and runtime RAM independently.

## Status and decision

**Research metadata check:** 10/10 source IDs returned; 10/10 license tags recorded; 7/10 numerical parameter fields returned. **Acquisition-ready:** 0/10, because no exact pinned file manifest, full dependency license review, physical storage measurement, or explicit approval was established by this lookup.

This is a *source-observation delta*, not a license clearance or revision promotion. Do not modify `catalog/effective-portfolio-2026-11-14-v32.json` on the basis of model-page metadata alone.

**H:** Every one of these 10 selected IDs has a discoverable publisher model listing and reported license tag.

**T:** Exact-ID census of the 10 selected records using Hugging Face Hub repository details, with no weight downloads.

**D:** PASS for listing and tag presence (10/10); UNCERTAIN for full trained tensor totals, exact selected-file bytes, licenses, and offline reproducibility.

**C:** Metadata may omit dependencies, use a different revision, or normalize a custom license; model title may differ from stored total parameters.

**U:** Primary uncertainty is scope mismatch between Hub model-level counts and complete reproducible pipeline counts. No numeric error bound is justified without pinned tensor inventories.

**Related disciplines:** machine-learning systems (MoE and component accounting), software supply chain (immutable revisions and license provenance), digital archiving (reproducible pipeline and deduplication).

**Question:** Which selected models already share an identical external codec or text encoder, proven by immutable hash, and therefore admit safe logical deduplication without weakening offline reproducibility?
