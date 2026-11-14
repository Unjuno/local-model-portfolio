# R65 | 現物検査へ進むためのオフライン手順

対象: GitHub main v32 / 135有効資産 / R64の8資産・9配布元・91ファイル。公開元のソース参照生容量 38,519,866,446 byte。重複排除後の新規ダウンロード量ではない。承認キュー0。

## 1. 目的と制限

既存の `scripts/archive_preflight.py` を利用し、所有者が正規に保持するファイルの有無・正確なbyte数・LFS SHA256またはGit blob SHA1を読み取り専用で検査する。HDDの現物がこのチャットから見えないため、検査実行済みという主張はしない。ネットワークアクセス・モデルコード実行・インストール・承認キュー変更は一切しない。

## 2. 物理HDDのルートを置換して実行する例

パス `/YOUR_ARCHIVE_ROOT` は、**既に存在する正規のHDDディレクトリ**で置換する。別レイアウトなら各 `--source-root` を個別変更する。`--hash`を省くとサイズのみ確認になりSHAによる実物検証はできない。

```bash
python scripts/archive_preflight.py \
  --archive-root /YOUR_ARCHIVE_ROOT \
  --manifest manifests/drafts/r64-eight-source-scopes.candidate.json \
  --hash \
  --source-root 'qvac-botpsy-0-8b=/YOUR_ARCHIVE_ROOT/store/huggingface/model/qvac/BotPsy-0.8B/24561e9681643eaf807fc28b0875210cb17f89c1' \
  --source-root 'ibm-granite-granite-timeseries-ttm-r3=/YOUR_ARCHIVE_ROOT/store/huggingface/model/ibm-granite/granite-timeseries-ttm-r3/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa' \
  --source-root 'robbyant-lingbot-touch-tiny=/YOUR_ARCHIVE_ROOT/store/huggingface/model/robbyant/lingbot-touch-tiny/f23969ccd4b6bba2163e69cc05a577455a075fe9' \
  --source-root 'nvidia-alpamayo2-edge=/YOUR_ARCHIVE_ROOT/store/huggingface/model/nvidia/Alpamayo2-Edge/b92b6aa326bd3e2235db28f248ad5a30b5890e64' \
  --source-root 'tencent-qwen3-8-27b-dspine-b16=/YOUR_ARCHIVE_ROOT/store/huggingface/model/tencent/Qwen3.8-27B-DSpine-b16/5f54174d301dbca65d9aa4448dc47e56732d9a12' \
  --source-root 'nvidia-nemotron-3-diarization=/YOUR_ARCHIVE_ROOT/store/huggingface/model/nvidia/Nemotron-3-Diarization/52a432672732425e4c19765b9fec9b5810e6f4ba' \
  --source-root 'nvidia-rfd4-proteina=/YOUR_ARCHIVE_ROOT/store/huggingface/model/nvidia/RFD4-Proteina/a06e2509c7033b010fc43614e9fd840303588502' \
  --source-root 'ace-step-acestep-v15-xl-turbo=/YOUR_ARCHIVE_ROOT/store/huggingface/model/ACE-Step/acestep-v15-xl-turbo/d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee' \
  --source-root 'ace-step-ace-step1-5=/YOUR_ARCHIVE_ROOT/store/huggingface/model/ACE-Step/Ace-Step1.5/19671f406d603126926c1b7e2adc169acbcade22'
```

`--existing-archive-bytes`と`--staging-reserve-bytes`は実測できたときだけ指定する。測定値がなければツールは容量ゲートをUNCERTAINのまま保持する。`PASS_POINT_IN_TIME_ONLY`は使用許諾/実行認証ではない。

## 3. 未解決の承認条件

Gatedモデルは個別アカウントで作者の正規許諾を確認。必要な全学習済み親モデル・Codec/Encoder/VAEと再現コードをSHA/byte/版で固定。4TB計画上限・実空き200GBとstage/cacheの余裕を実測。ライセンス/NOTICE/本人承認が成立するまでcandidateをlockに昇格しない。ACE-Step XL公式コードは通常2Bを暗黙に要求して自動取得するため、このまま実行してはいけない。

## 4. 変数表・次元検査

| 変数 | 意味 | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| C | 保存計画上限 | byte | 4,000,000,000,000、非負 | 整数スカラー |
| F | 最低空き床 | byte | 200,000,000,000、非負 | 整数スカラー |
| P | R64 rawソース参照合計 | byte | 38,519,866,446、重複未排除 | 整数スカラー |
| H | 所有者のHDD空き | byte | null、未計測 | 整数スカラーまたはnull |

次元チェック: 比較するストレージ値は全てbyte。パラメータ数とVRAMは別指標。

## 5. H/T/D/C/U と ERROR CHECK

H: 正規ファイル現物が揃っているかを、メタデータだけでなく実HDD上のSHAで検証可能。T: 承認済み端末の9repo91ファイルをストリーミングで比較。D: SHA・依存・契約・空き・承認が揃えば次の取得審査、欠落または無承認時はSTOP、値が不明ならUNCERTAIN。C: 互換性違い、シンボリックリンク、HDD自動移動、外部wheel欠落。U: 現物不明につき合成標準不確かさu_c/係数kは未算出。

ERROR CHECK: 9repo、8資産、91ファイル、38,519,866,446byte。今回のコード実行/実HDD検査/取得なし。Python unittestはGitHub Actions実績がなく未実行。

関連分野: デジタル保存、機械学習、ソフトウェア供給網、法務。

## 6.〈次に考える問い〉

実HDD内の既存保存物を含めてSHAを確認すれば、最初にどの8資産をオフライン復元PASSにできるか。
