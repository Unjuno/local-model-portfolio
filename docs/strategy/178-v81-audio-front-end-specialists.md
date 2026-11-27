# R178 v81: 音声信号処理・対話ターン制御の補完

2026-11-28 JST; base 6fedaf75e9d51b6137c3aec5c4983c1b6e209a59. 273→275 tracked / 217→219 active; SELECT56, CONDITIONAL163; 273 previous rows and 133 acquisition reports unchanged; all 219 STOP.

## inworld/sava: ADD / CONDITIONAL

2026-11-18 official release. [Fixed source card](https://huggingface.co/inworld/sava/blob/1beae7c1dd0df6b0f92030644fc905eb087dc6a0/README.md), [LFS pointers](https://huggingface.co/inworld/sava/commit/1beae7c1dd0df6b0f92030644fc905eb087dc6a0), [fixed implementation](https://github.com/inworld-ai/sava/blob/b4221a54458ea60df8c777911d0567418994cacc/pyproject.toml), [benchmark](https://github.com/inworld-ai/sava/blob/b4221a54458ea60df8c777911d0567418994cacc/bench/README.md).

Three Mamba-2 blocks plus attention and speech/turn heads; 16 kHz mono; 40 ms frames; VAD 120 ms lookahead, EOT none. Publisher ~5,000 h unique audio; training recipe, code and data unreleased.

Positive: Publisher AMI threshold 0.5: 85.5% within 200 ms vs smart-turn v3.2 30.8%; M3 Max CPU 3.8 ms per 40 ms frame, one stream.

Negative: AliMeeting VAD AUC 0.9376 vs Silero 0.9635; VAD timing unequal due to lookahead; quiet speech-like noise false positives; no target-speaker selection or independent owner evaluation.

Portfolio difference: Whisper/Granite transcribe and Nemotron diarizes; acoustic-semantic EOT adds a different function. Exact training outcome cannot be reconstructed from released inference source alone.

Weight reference 51051668 bytes. Python >=3.10, huggingface-hub, numpy, safetensors, soundfile, soxr, torch>=2.1. Apache-2.0 publisher claim; rights and dependency closure pending. No code executed.

## inworld/voice-isolator: ADD / CONDITIONAL

2026-11-18 official release. [Fixed source card](https://huggingface.co/inworld/voice-isolator/blob/9b0285b3fe8403aa8e2f1dbb2165a80a4294c970/README.md), [LFS pointers](https://huggingface.co/inworld/voice-isolator/commit/9b0285b3fe8403aa8e2f1dbb2165a80a4294c970), [fixed implementation](https://github.com/inworld-ai/voice-isolator/blob/c73b3fab81a870410cbac50d2f05f25edc4d10aa/pyproject.toml), [benchmark](https://github.com/inworld-ai/voice-isolator/blob/c73b3fab81a870410cbac50d2f05f25edc4d10aa/bench/README.md).

48 kHz mono, 46 STFT bands, seven attention/Mamba dual-path blocks, mask+residual; 64M offline and 58.2M causal realtime checkpoints; two trained states, not quantizations. Publisher ~10,000 h unique training audio; exact training set/reconstruction not established.

Positive: Publisher VIBE uses common 48 kHz scoring on 5,502 items / 77 conditions; distinct full-band offline and realtime checkpoints. Realtime 63 ms algorithmic delay at 20 ms lookahead.

Negative: Publisher tuned its own checkpoint; private eval set, 36 items may share training speakers. Independent superiority not established. No restoration or target-speaker selection; similar-level voices may remain, small GPUs untested.

Portfolio difference: Adds waveform denoising rather than transcription/synthesis/diarization; complements existing speech assets. Keep both trained execution regimes under one repository identity.

Weight reference 489040928 bytes. Python >=3.10, numpy, soundfile, safetensors, torch>=2.1, torchaudio>=2.1, huggingface-hub. Apache-2.0 publisher claim; rights and dependency closure pending. No code executed.

## Comparison and HOLD

- ibm-granite/granite-speech-5.0-470m-turboctc — KEEP: Complementary transcription, diarization or speaker embedding; no matched replacement evidence. 
- openai/whisper-large-v3-turbo — KEEP: Complementary transcription, diarization or speaker embedding; no matched replacement evidence. 
- nvidia/Nemotron-3-Diarization — KEEP: Complementary transcription, diarization or speaker embedding; no matched replacement evidence. 
- speechbrain/spkrec-ecapa-voxceleb — KEEP: Complementary transcription, diarization or speaker embedding; no matched replacement evidence. 
- weya-ai/hush — HOLD: Publisher 1.8M/8 MB, 16kHz, CPU claim; matched quality, fixed source scope, and hardware conditions missing. https://huggingface.co/weya-ai/hush
- bmarti44/before-the-implant-causal-enhancer — HOLD: Tiny causal enhancement with simulation-only evidence and erratum; no clinical or matched real-world validation. https://huggingface.co/bmarti44/before-the-implant-causal-enhancer
- isseninc/issen-vad — HOLD: Recent listing, direct primary card not retrievable; precise release date and source scope unknown. https://huggingface.co/isseninc/issen-vad
- DeepFilterNet (reference) — HOLD: Older real-time comparator; current exact checkpoint and matched incremental quality unresolved. https://arxiv.org/abs/2110.05588

Searched bounded 7/30/90-day windows. Recent HF listing surfaced issen-vad but primary card unavailable; Nov18 Inworld original releases verified. No observed license change; future restrictions not asserted. Old DeepFilterNet papers included as comparators. No matched local benchmark performed.

## Capacity / authority

Three publisher LFS pointer files 540092596 B, not full selected or physical bytes. Both independent offline/realtime checkpoints retained as one repo identity. Exact tensor census, full file list bytes, wheelhouse, license/NOTICE, owner HDD, local SHA and offline restore remain unresolved; 4TB cap and 200GB floor unchanged. No model payload transfer, execution, acquisition approval, or deletion. Preserve existing rows, receipts and all gates.

H/T/D/C/U: hypothesis — consented audio front-end improves existing offline ASR/turn-taking; test held-out licensed recordings on fixed hardware, thread count, sample rate, paired CER/WER, false deletion, VAD/EOT latency/p95 and premature cut; conditional until matched metrics and safety/runtime gates meet predefined limits. Competing explanation: existing ASR or smaller baseline suffices; denoising removes quiet speech. Uncertainty: private dataset, lookahead, ABI, privacy, owner storage. Not an experimental PASS.
