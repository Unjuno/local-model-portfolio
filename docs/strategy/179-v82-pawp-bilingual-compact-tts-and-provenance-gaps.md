# R179 / v82 — compact bilingual TTS and provenance gaps

Research date: 2026-11-28 JST. Search bounded to 7/30/90 days; HF primary cards and immutable trees, GitHub code, publisher reports, arXiv search (no matching PAWP paper verified). Started at v80; rebased onto v81 to retain inworld/sava and inworld/voice-isolator. No observed rights/access change proven. A leaderboard result revision dated Nov 27 was a normalization rescore, not new synthesis; five raw result CSV requests returned 401, not evidence of a changed access policy.

## ADD: PAWP 300K, research-only CONDITIONAL

- [Pinned publisher card](https://huggingface.co/Firoj112/pawp-tts-300k/blob/e7f3c94053ea88e9c17df1264475f4a41d90529e/README.md); [code](https://github.com/Firojpaudel/PAWP_TTS/tree/235651848f58f423a602172a6668d7a54fc65642). Two independently trained states (shared-basis EXP-015b and dense EXP-015c), one repo identity. Publisher states 281,078 stored / 328,158 materialized for shared, 281,442 dense. Full independent census pending. Both trained from scratch on same bilingual data, 36k steps, seed 42, RTX4090, 2.25h as reported. Shared and dense EN/NE/mixed WER 6.88/19.71/12.02 and 6.15/20.21/18.09; n=30/30/9. Larger 1.5M 4.02/12.35/12.32. Dense mono PER 5.53 NE and 5.34 EN vs shared 6.35/6.57, across three seeds. No independent MOS or matched incumbent tests. KEEP tiny-voca and Paradee; also preserve v81 audio-front-end specialists, which are not TTS substitutes.
- 23 files / 7,130,007 B publisher scope, 8 source references / 2,306,237 B candidate; two distinct weights 2,293,480 B. Exclude derived ONNX and demo audio from candidate source scope. Complete code, lexicon, G2P, ABI, rights/consent, owner capacity and offline restore remain unknown. No download authorization; not a final lock.

## Other decisions

- **HOLD** [empero-ai/PiVo-1.4M](https://huggingface.co/empero-ai/PiVo-1.4M/tree/515d84fc3420da6ae138f1b81017fcbc24d622a8): Incomplete declared provenance; no corruption claim. Mixed Apache/Opus/CMU notices.
- **EXCLUDE** [litert-community/PiVo-1.4M](https://huggingface.co/litert-community/PiVo-1.4M/tree/a6acc55c53e092f9dcaa76d96eb1adc12cc4854c): Runtime conversion of same learned weights.
- **HOLD** [ampixa/sanoTTS](https://huggingface.co/ampixa/sanoTTS/tree/72ad9e997d03724e100aa0ca86200cd67ab5e8f2): 104215 voice +96511 G2P; 0.5.7 benchmark vs 0.5.8 examples changed G2P; GPL3, scope and runtime rights not closed.
- **HOLD** [gachimoto/tiny-voca-ja](https://huggingface.co/gachimoto/tiny-voca-ja/tree/9b2305c81b9ca92ef8347eba473ea096c86f55c4): Independent 4538827 Japanese/English retrain; publisher n16 CER 1%, n40 EN WER 2.8%; new front-end mismatch, code not pinned and no matched incumbent.
- **HOLD** [Inomjonov/tiny-voca-english-reproduction](https://huggingface.co/Inomjonov/tiny-voca-english-reproduction/tree/4daaf8e2bc0c491ce7e5c3e905f0976f3f4af388): Independent seed from same code/data; 4537291 parameters but no demonstrated incremental quality.
- **KEEP** [n4ze3m/tiny-voca](https://huggingface.co/n4ze3m/tiny-voca): Existing English model reported verified; different language and experimental purpose.
- **KEEP** [sahilmahendrakar/Paradee-8M-v1.3](https://huggingface.co/sahilmahendrakar/Paradee-8M-v1.3): Independent multilingual TTS; no matched replacement evidence.

PiVo full tree has 36 files and 15,402,348 B; five declared evidence paths returned 404, seven metadata checksums matched. Missing lineage files do not prove weight corruption. SanoTTS and tiny-voca-ja may be reconsidered after source closure and matched tests.

## Falsifiable test

H: shared-basis improves mixed-language WER over dense under a preregistered matched test without unacceptable monolingual loss. T: same held-out consented test utterances, minimum 100 per language stratum, same pinned backend, device, threads, batch=1 and clock; paired bootstrap intervals. D: PASS only if 95% CI for mixed WER improvement excludes zero and mono WER loss stays within predeclared 2 percentage points; FAIL if contrary, otherwise UNCERTAIN. C: test-set composition or G2P differences explain advantage. U: sampling, frontend and measurement uncertainty not yet measured. This is a proposal, not completed inference. No weights downloaded or executed. Candidate scope is metadata-only. See [evidence](../../catalog/research/2026-11-28-r179-pawp-and-compact-streaming-tts.json) and [manifest](../../manifests/drafts/r179-2026-11-28-pawp-300k-two-states-source.candidate.json).
