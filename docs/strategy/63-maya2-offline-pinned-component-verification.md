# R63: Maya2 Native offline dependency verification (2026-11-14)

**main v32 / 182 assets / 135 active. No change to portfolio decisions or approved downloads.**

## Finding

The published source [MayaResearch/maya2-native at c6b3768](https://github.com/MayaResearch/maya2-native/blob/c6b376868e268551d065c4206193e96257bef4a1/maya3/hub.py) calls snapshot() for Mimi and ECAPA with revision=None at lines 136-137. The parent Maya source revision argument fixes only the parent model. The helper searches cached snapshots and can fall back to remote latest if not offline. Therefore the old method can mix model and encoder revisions.

## Source identity pinned without downloads

| Repo | Immutable revision | R59 source files | Source bytes |
| --- | --- | ---: | ---: |
| [Maya2 Native](https://huggingface.co/maya-research/maya2-native) | 87a83efdd6551e038246b6b37836a6264713eec3 | 13 | 5,021,109,670 |
| [Kyutai Mimi](https://huggingface.co/kyutai/mimi) | 89091b3e466eb6a9d11e537bf26b144f194978f7 | 4 | 384,655,536 |
| [SpeechBrain ECAPA](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) | 0f99f2d0ebe89ac095bcc5903c4dd8f72b367286 | 7 | 88,988,901 |
| **Total** | | **24** | **5,494,754,107** |

The published file hashes and byte counts are versioned in [R59](../../catalog/research/2026-11-14-r59-maya2-drama3-cross-repo-components.json). They are source metadata until acquired files are hashed locally.

## New read-only checker

[verify_maya2_local_bundle.py](../../scripts/verify_maya2_local_bundle.py) accepts **three user-provided materialized local source directories**. It compares each exact filename and byte count against R59 and streams SHA-256 for Hub LFS files or Git blob SHA1 for ordinary small files. Git blob SHA1 is not the full-file SHA256. Missing files, path traversal, symlinks, extra/missing source scopes, revision syntax, digest or byte mismatch are rejected. It does not import PyTorch, unpickle checkpoints, run code from a model directory, contact the network, accept a gated license or download weights.

Example after separately authorized lawful source acquisition and file materialization:

    python3 scripts/verify_maya2_local_bundle.py --maya-root /archive/maya2-native --mimi-root /archive/mimi --ecapa-root /archive/ecapa

A successful report certifies only those 24 locally present file bytes matching recorded publisher metadata. It explicitly retains download_authorized=false, license_cleared_for_user=false and full_offline_runtime_verified=false. Hugging Face cache symlinks are intentionally not accepted as immutable local copies.

## ABI and legal/operational blockers

Author reference code [pyproject.toml](https://github.com/MayaResearch/maya2-native/blob/c6b376868e268551d065c4206193e96257bef4a1/pyproject.toml) pins Torch 2.8.0+cu128, Transformers 5.6.2, SpeechBrain 1.1.2 and Triton 3.4.0, with Linux NVIDIA GPU and CUDA 12.8. These were not benchmarked on the owner's hardware; clock, batch, driver and inference precision remain unmeasured. Named voices may use cached speaker references while cloning requires ECAPA. It remains part of the complete capability bundle.

Mimi uses CC-BY-4.0; Maya2 and ECAPA are tagged Apache-2.0. License texts and the actual intended use/redistribution must be separately reviewed. Stored tensors including ECAPA are not counted fully yet, so Maya2 retains UNVERIFIED_BLOCK_FINAL_LOCK. 4TB planning limit and minimum 200GB real free space do not follow from the 5.49GB partial bundle size.

## Validation

Test file: [test_verify_maya2_local_bundle.py](../../tests/test_verify_maya2_local_bundle.py). Nine offline fixtures cover PASS and mismatch, missing files, symlinks, unsafe paths, absent revision, duplicate file records, Git blob mismatch and non-authorization.

H: fixed three-repo hashes detect accidental revision swaps. T: verify all 24 reference files after lawful materialization; in CI test 9 tiny synthetic cases without GPU or model code. D: PASS only on exact file integrity; FAIL on mismatch; UNCERTAIN for licenses, execution and owner hardware. C: a source file changes without manifest update, cache revision drifts, or runtime needs additional learned dependencies. U: upstream publisher SHA provenance, native runtime ABI, user access rights; no measured uncertainty distribution, so combined u_c and k are not estimated.

Related fields: digital preservation (snapshot identity), software supply chain (hash verification), speech ML systems (Mimi/ECAPA dependency compatibility).

**ERROR CHECK:** v32 selection 182/135 unchanged, new branches 0, downloads 0, approved queue remains empty.

**Next question:** Can the author runtime and third-party codec be kept executable offline with pinned wheel hashes without adding another learned checkpoint?
