# R64 — 8資産・9配布元・91ファイルの固定版取得前マニフェスト

現行v32、GitHub HEAD `e9be3695c3456b33d69e927601565b977a4cc0a5` を基準。計画対象は正式SELECT/CONDITIONALからの8資産で、別配布元のACE共有LM/VAEを別sourceとして保管。実体取得・推論・自動承認はゼロ。

## 1.〈本論〉源ファイル全91件の監査

以下の各資産について、公式Hugging Faceの40桁不変コミットと、公開元のファイルbytes・LFS SHA256またはGit blob SHA1を全て確認。元からSHAのない実体に想像上のSHA256を記録しない。

| 対象 | ソースrepo数 | ファイル参照 | 生bytes | 未解消条件 |
|---|---:|---:|---:|---|
| `qvac/BotPsy-0.8B` | 1 | 11 | 1,726,201,481 | TRANSFORMERS_BACKEND_ABI, FULL_LICENSE_TEXT |
| `ibm-granite/granite-timeseries-ttm-r3` | 1 | 6 | 6,126,375 | GRANITE_TSFM_CODE_REVISION, OFFLINE_CPU_TEST |
| `robbyant/lingbot-touch-tiny` | 1 | 5 | 21,873,479 | PT_STATIC_PICKLE_AUDIT, SENSOR_CALIBRATION_AND_RIG_SCHEMA |
| `nvidia/Alpamayo2-Edge` | 1 | 12 | 5,320,375,887 | ALPAMAYO_PROCESSOR_RUNTIME, SAFETY_AND_DATA_RIGHTS |
| `tencent/Qwen3.8-27B-DSpine-b16` | 1 | 5 | 4,051,857,976 | QWEN_PARENT_IMMUTABLE_SHA_REUSE, SGLANG_FA3_ABI |
| `nvidia/Nemotron-3-Diarization` | 1 | 11 | 397,030,277 | NEMO_OR_TRANSFORMERS_ABI, AUDIO_PRIVACY_CONSENT |
| `nvidia/RFD4-Proteina` | 1 | 7 | 1,742,698,063 | PIN_ROSETTA_SOURCE_AND_LICENSING, FLOW_AUTOENCODER_RUNTIME |
| `ACE-Step/acestep-v15-xl-turbo` | 2 | 34 | 25,253,702,908 | STOCK_INIT_IMPLICIT_2B_DOWNLOAD_R63, PIN_WHEELHOUSE_AND_OFFLINE_CODE |

全モデル合計は9repo、91ソース参照、**38,519,866,446 byte**（重複未排除）。これは既存4TB計画へ追加する新規容量ではなく、v27→v32に**すでに含まれる資産**の部分ソース明細。

## 2. 取得の停止条件

本マニフェストは既存 `scripts/archive_preflight.py` の `audit_source_manifest()` に合わせた **candidate** 形式。所有者承認がなければ `manifests/*.lock.json` に変換しない。公開元の現在のリストが見えることと、本人利用許諾・Gated解除、親LMのハッシュ、runtime/ABI閉包、実HDD余力、ローカルSHA一致は異なる。

ACE XLは既知の2B既定初期化依存があり、選択したソース34件を勝手に自動取得コードへ渡してはいけない。RFD4は106GB全部を取らずFlow+AE原本7ファイル。DSpineはQwen親27Bを二重取得しない。Lingbot `.pt` は静的監査中に `torch.load` しない。

## 3. H/T/D/C/U / ERROR CHECK

H: 資産識別とファイルSHA/bytesを収束させることで、承認後の失敗を防止できる。T: 公式7repoの固定版とACEの2repo既存監査を読み取り、9repo91参照を数値・ハッシュで全数照合。D: 源データのSOURCE_PINNEDはPASS、取得可能/オフライン復元はUNCERTAIN。C: 法的権利不一致、親依存、巨大runtimeやソース更新。U: wheel/owner disk/ライセンス誤差に分布なし、合成u_c/kは未算定。

ERROR CHECK: files=91, repos=9, packages=8, source raw bytes=38,519,866,446。正式135件の選定変更0、モデル取得0、承認0。

学際領域：ML学習状態鑑定、デジタルアーカイブ、ソフトウェア供給網、知的財産/契約。

## 4.〈次に考える問い〉

小型TTMを完全に復元し、独立した同条件CPU出力テストを通過させるために必要な追加コード・設定・ユーザー承認は何か。
