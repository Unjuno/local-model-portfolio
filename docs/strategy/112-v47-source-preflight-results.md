# R112 — v47 source selection is actionable: verified dry-run and checksum preflight

Date: 2026-11-18. Canonical v47: 200 tracked, 153 active. This report is a metadata/physical-volume test, not an acquisition authorization.

## 1. What was actually completed

- Added `scripts/verify_v47_download_preflight.py` and `tests/test_verify_v47_download_preflight.py` to main.
- Ran Python 3 unittest on the connected Linux device: **11/11 PASS**. Tests include wrong source SHA, path traversal, wrong revision, bad size, unexpected approval, symlink, and publisher_lfs_sha256 normalization.
- Independently audited R110 proposed source queue against R111 grouping: **14 models, 173 files, 72 publisher SHA-256 references, 211,999,468,264 source bytes**.
- The script does **not** download or execute model code; model weights downloaded = 0, approved queue entries = 0.

## 2. Selection decisions, not another shortlist

| Lane | Models | Source reference bytes | Final disposition |
|---|---:|---:|---|
| A | 10 | 47,030,749,353 | Preserve distinct original trained outcomes; finish rights, dependencies and actual storage |
| B | 1 | 671,173,375 | Preserve image adapter only when Qwen Image 2.1 parent and noncommercial license are resolved |
| C | 2 | 108,711,479,306 | Keep registered but postpone payload transfer pending independent incremental-value tests |
| D | 1 | 55,586,066,230 | Individually gated OrcaRouter original; no implied user access |
| Total | 14 | 211,999,468,264 | All are part of v47 already: not a new capacity reservation |

Keep the separately trained selective-political Interpretic Q4 and the broader ARA 0bserverx RVN multilingual Q4. Do not fetch all Q4/Q5/Q6/Q8/GSQ formats of the same underlying outcome. ARLoop-1.2B is a distinct recurrently trained original; Kitten TTS 2 Mini has Japanese and language-specific learned voices. The investigated tiny-voca stays research-only until immutable exact source and rights are verified.

## 3. Actual environment check and earliest executable metadata step

The connected Linux device exposed **50,884,108,288 bytes total** and **29,269,999,616 bytes free** at the time of this check. The policy requires 200,000,000,000 free bytes, so even a test on IBM TTM R3 (**5,748,963 selected bytes**) returns **FAIL_CAPACITY** on this device. This is not the owner's 4TB archival disk.

Read-only commands to run from repository main when the legitimate physical 4TB archive is mounted:

```bash
python3 scripts/verify_v47_download_preflight.py --archive-root /PATH_TO_4TB --lane A
python3 scripts/verify_v47_download_preflight.py --archive-root /PATH_TO_4TB --repo-id ibm-granite/granite-timeseries-ttm-r3 --show-dry-run
python3 scripts/verify_v47_download_preflight.py --archive-root /PATH_TO_4TB --repo-id ibm-granite/granite-timeseries-ttm-r3 --verify-existing
python3 -m unittest discover -s tests -p test_verify_v47_download_preflight.py -v
```

The dry-run commands are printed, never executed by this script. Hashing is performed only on existing local file data. A metadata PASS is **not** confirmation of model validity, user license permission, completed restore or download approval.

## 4. H/T/D/C/U and uncertainty

**H**: An immutable selection manifest plus physically checked archive can replace endless catalog-only review with real preservation progress.
**T**: All 14 model manifests and 173 file records were checked; 11 regression cases all passed. Stop on a checksum, revision, path, queue or free-space mismatch.
**D**: PASS means static publisher metadata consistent; current connected disk is FAIL_CAPACITY. Owner 4TB capacity, intended-action legal rights and offline restore remain UNCERTAIN.
**C**: A hidden dependency, file moved by publisher, license limitation, or runtime incompatibility can invalidate completeness.
**U**: Source bytes are not final de-duplicated physical bytes; publisher checksums are not locally downloaded checksums. Statistical combined uncertainty u_c and coverage k are not estimable from this evidence.

## Variable table for storage check

| Symbol | Meaning (Japanese) | SI unit | Definition | Domain/assumptions | Type |
|---|---|---|---|---|---|
| `F` | 現物ディスク空き | byte | filesystem reported free | nonnegative; point in time | integer scalar |
| `S` | 選択publisher source合計 | byte | sum of selected file sizes | assumes all files new; not complete runtime | integer scalar |
| `T` | 最大一時ファイル予約 | byte | maximum selected file size | minimum stage assumption, other caches excluded | integer scalar |
| `R` | 最低空き床 | byte | 200,000,000,000 | fixed policy | integer scalar |

Provisional capacity only if **F >= S + T + R**. All four terms use bytes, so dimensions match. Even a pass does not grant acquisition rights.

Related domains: digital preservation, software supply-chain attestation, AI capability evaluation, and licensing.

## ERROR CHECK

v47 200/153; R111 A10/B1/C2/D1; 173 selected files; 72 hashes; 211,999,468,264 source bytes; 11/11 Python tests; unchanged empty approved queue; zero downloaded model weights; one main branch. Exa HTTP 402 credit exhaustion is not new primary evidence.

## Next question

Can the intended 4TB archive be mounted on an authorized computer so that the fixed first model can be transferred, locally hashed, and restored rather than just ranked?
