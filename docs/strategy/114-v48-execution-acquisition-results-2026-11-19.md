# v48 Acquisition Execution Results (2026-11-19)

Results of executing the unified pinned-source plan `queues/proposed-v48-r113-source-pinned-15.json` from canonical `catalog/CURRENT.json` (v48-20261118).

- Models: 23 (verified 22, partial 0, failed 0, held 1)
- Verified files: 227
- Verified source bytes: 162325501646
- Minimum observed free bytes: 2818771451904 (200 GB floor maintained: True)

| repo_id | revision | status | verified files | license |
| --- | --- | --- | --- | --- |
| `n4ze3m/tiny-voca` | `d94d2a0338fd1e0eab7dd896ec0ad23d8cdf7c14` | VERIFIED | 14/14 | apache-2.0 |
| `ibm-granite/granite-timeseries-ttm-r3` | `ea17cfd2e3edcaea21eb8dcecd18bf88971482fa` | VERIFIED | 5/5 | apache-2.0 |
| `robbyant/lingbot-touch-tiny` | `f23969ccd4b6bba2163e69cc05a577455a075fe9` | VERIFIED | 5/5 | apache-2.0 |
| `nvidia/Nemotron-3-Diarization` | `52a432672732425e4c19765b9fec9b5810e6f4ba` | VERIFIED | 11/11 | openmdw-1.1 |
| `KittenML/kitten-tts-2-mini` | `c01797caec3967b400da457656e011eb81f530a4` | VERIFIED | 27/27 | apache-2.0 |
| `usezn/Galvanize-3` | `597237be3b0fabbf5d70ff16ce95fad14a591f20` | VERIFIED | 9/9 | apache-2.0 |
| `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1` | `aa213272180d6ad0d03f5fb3d597f0f0322647c5` | VERIFIED | 8/8 | other |
| `qvac/BotPsy-0.8B` | `24561e9681643eaf807fc28b0875210cb17f89c1` | VERIFIED | 11/11 | apache-2.0 |
| `tencent/Qwen3.8-27B-DSpine-b16` | `260a6c23070ca873ff1a5f33b7119ac3f6a245ee` | VERIFIED | 5/5 | apache-2.0 |
| `osunlp/ARLoop-1.2B` | `a29f310ac46646edf5c462425dc546b2ce7ea985` | VERIFIED | 15/15 | apache-2.0 |
| `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | `ab8d7bd81d03117501e4da60cccdff4c80f0eea0` | VERIFIED | 4/4 | apache-2.0 |
| `InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF` | `e6924b3a08765341e01546308ccf2683d43e880b` | VERIFIED | 5/5 | apache-2.0 |
| `Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2` | `6af1278a92223c717ccea671e4571a5cc135f5d8` | VERIFIED | 12/12 | apache-2.0 |
| `orcarouter/Qwen3.8-27B-Uncensored` | `0f639a9bde23fe229a7b064b40a5153c5bec0b48` | HOLD_GATED_OR_PRIVATE | None/None | None |
| `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU` | `079b2b268c637b77f2fb4ab6a5ca1edc47d462a5` | VERIFIED | 25/25 | apache-2.0 |
| `Qwen/Qwen3.5-0.8B` | `2fc06364715b967f1860aea9cf38778875588b17` | VERIFIED | 13/13 | apache-2.0 |
| `lightonai/LightOnOCR-3-0.8B` | `36d8636925327c671bd8e479c517a004f7566bd9` | VERIFIED | 15/15 | apache-2.0 |
| `openai/whisper-large-v3-turbo` | `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` | VERIFIED | 13/13 | mit |
| `nvidia/Kumo-Anomaly` | `369ccba38a105736c6c9e4b5788a330c7e22112e` | VERIFIED | 2/2 | apache-2.0 |
| `gradium/phonon-31m-en` | `8f7a37c94a4c58b04c8287300c53f11d2e208eae` | VERIFIED | 11/11 | apache-2.0 |
| `udgamlabs/Lilavati-Checker` | `7edaac6de4cfe7127f973d8641335c4cb2f84b08` | VERIFIED | 6/6 | apache-2.0 |
| `udgamlabs/Lilavati` | `5aef8c4b79fa6b8aaf5d63a1e8dd05ca572fe25d` | VERIFIED | 6/6 | apache-2.0 |
| `nvidia/Kumo-Relational` | `efdbb110daea5aae123447864a64612e8a3dc6be` | VERIFIED | 5/5 | openmdw-1.1 |

Weight files were compared against publisher LFS SHA-256; ordinary Git blobs were compared by Git blob SHA-1. 'size-only' means no publisher hash existed.
Gated models without verified owner entitlement were recorded as HOLD and no payload was acquired for them.
No model code, pickle payload or weights were imported or executed.
Local absolute paths, usernames and credentials are not exported to the repo.

