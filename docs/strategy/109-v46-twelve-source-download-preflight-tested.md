# R109｜v46・12モデルの取得前検証を実装・9試験PASS（2026-11-18）

**目的**：候補選定を繰り返す工程から、合法なファイル取得とオフライン原本復元へ移行する。v46正式正本198登録／151有効、前回R108で151全件の一意の研究判断、R108の12モデルのpublisher単一revisionを確定済み。今回**新規モデル選定数は増やさず、実機とローカルモデルデータの取得前STOPを自動判定できる再現ツールを追加**。

- [実装：`scripts/verify_v46_download_preflight.py`](../../scripts/verify_v46_download_preflight.py)
- [回帰：`tests/test_verify_v46_download_preflight.py`](../../tests/test_verify_v46_download_preflight.py)
- [12モデル原本凍結候補](../../manifests/drafts/r107-v45-12-original-sources-file-freeze.candidate.json)
- [12モデル131ファイルの研究キュー](../../queues/proposed-v46-r108-source-pinned-12.json)
- [151件の全体判定](../../catalog/decisions/2026-11-18-r108-global-portfolio-optimization.json)

## 1.〈本論〉選定結果と、取得前STOPの実装

既存12モデルの固定revision／全選択ファイルのpath・byte・LFS SHA256／Git blob SHA1を、R108凍結マニフェストと提案キューで**全件照合**。正規repo IDの重複、40桁revisionの欠損、危険な相対パス、原本とキューのSHA/byte差分、learned binaryのSHA欠損、`queues/approved.json`が空でない場合、**FAIL**させる。公表ファイルのchecksumと、転送後のローカル実ファイルSHAは別の結果として扱う。

| チェック項目 | 実際の結果 |
|---|---:|
| 対象v46選定モデル | 12 |
| 選択ファイル数 | 131 |
| SHA256が明記された上流ファイル参照 | 50 |
| 学習済み重みファイル | 44 |
| 公開元の選択source合計 | 206,683,452,429 byte |
| 明示的取得承認済み | 0 |
| 実重みのダウンロード・モデルコード実行 | 0 |
| 回帰テスト | 9件 PASS |

**誤解防止**：上記206.683GBは元配布者の12モデル選択ファイル参照合計。これは既存151有効資産の**内数**であり、v46全体予算へ追加加算する新規206.683GBではない。ランタイム・親モデル・外部VAE/codec・wheelhouse・ステージング・実機重複排除は未確定で、完成オフラインアーカイブのbyteではない。

### 実際にPythonを実行して検証

オンライン接続中のLinux環境でスクリプトの文法検査と、9件の`unittest`を実行し**9/9 PASS**。パス脱出、壊れたbyte、固定revision変更、承認キューの混入、SHAの誤り、シンボリックリンクなど、意図的な負例が停止することも確認。

同環境に対して実測したドライブのfilesystem総量は**50,884,108,288 byte**、その時点の空きは**29,520,904,192 byte**。初回のTTM R3（5,748,963 byte）を選んだ場合でも、**最低空き200,000,000,000 byteを維持できないため`FAIL_CAPACITY`**。これはユーザー所有の別の4TB HDDを検査したものではなく、接続中のLinuxに見えるドライブの測定である。取得可能な空き容量を捏造しない。

## 2.〈応用・転用例〉4TB保存先での実施手順

**本人の4TBアーカイブディスクをマウントした端末上**で、GitHubの`main`最新ソースを使用する。準備コマンドは**読取専用、モデル重み取得なし、外部の作者コード実行なし**。

```bash
# 12件全数の公開元source整合性・保存先容量・SHA計画だけを検証
python3 scripts/verify_v46_download_preflight.py \
  --archive-root /YOUR_4TB_ARCHIVE \
  --show-dry-run

# 最小容量の独立学習済み時系列原本から個別のmetadata-only dry-runを生成
python3 scripts/verify_v46_download_preflight.py \
  --repo-id ibm-granite/granite-timeseries-ttm-r3 \
  --archive-root /YOUR_4TB_ARCHIVE \
  --show-dry-run

# 適法に所有するローカル原本が存在する場合、その現物の SHA256 / Git blob を計算
python3 scripts/verify_v46_download_preflight.py \
  --archive-root /YOUR_4TB_ARCHIVE \
  --repo-id ibm-granite/granite-timeseries-ttm-r3 \
  --verify-existing
```

`--show-dry-run`は`hf download ... --revision <commit> --include <exact-file> --dry-run`という**実行していないコマンド文字列**を出力するだけ。実際のダウンロード・CLIインストール・本人のライセンス受諾・Gated権限・SNS/トレント・モデルロード・圧縮解凍を行わない。保存済みファイル検証は既定の`<archive-root>/<publisher>/<repo>/<40桁revision>/<relative-file-path>`構成を前提にする。ファイルが無いときは`local_hashes.complete=false`となるだけで取得許可を意味しない。

**最小パイロット案（研究元SHAが存在する3件、未承認）：** `ibm-granite/granite-timeseries-ttm-r3`（5,748,963 byte）、`usezn/Galvanize-3`（597,001,839 byte）、`qvac/BotPsy-0.8B`（1,726,201,481 byte）。合計**2,328,952,283 byte**。15B+モデルを先行して取得する必要はない。権利と現物HDDを確認できた1件から固定SHAsで転送・検算していく。いずれもまだ実ファイルをダウンロードしない。

**無検閲原本2件の保全価値は維持**：`0bserverx` RVN-Q4約17.1767GBと`InterpreticAI` Q4約17.7383GB、合計34,915,019,503 byte。公開元メタデータに基づく2系統の異なる編集結果であり、同系Q5/Q6/Q8等の全量子化を追加しない。本人許諾と4TBの実体容量を確認した後に独立した比較を行う。

## 3. 固定バイトから4TBの合格条件を判定する方法

| 変数 | 意味（日本語） | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `F_now` | 指定ディスクの実空き容量 | byte | `shutil.disk_usage(...).free`の読み取り時点の値 | 非負、同時処理により変動 | 整数スカラー |
| `B_selected` | 指定したsubsetの元ファイル総量 | byte | publisherの各`source_bytes`の和 | 未取得を全量新規として保守的計算 | 整数スカラー |
| `B_peak_file` | 一時コピーに割く最大ファイル分 | byte | subsetの最大`source_bytes` | 単一重みの一時コピー仮定、ランタイムは別 | 整数スカラー |
| `F_floor` | 保存後に残す最低空き | byte | 200,000,000,000 | 政策上の下限 | 定数スカラー |

保守的な一次容量判定は**`F_now >= B_selected + B_peak_file + F_floor`**である。これは作業用領域が最大単一ファイル1個分という仮定の**仮判定**であり、キャッシュや別の大規模依存がある場合には必要量がさらに増える。全ての変数はbyteなので加算・比較の次元は一致。たとえこの条件を満たしても、契約・本人Gated権利・固定ランタイムとoffline restoreまでは自動合格にしない。

## 4. H / T / D / C / U

- **H**：原本選定と権利審査を別段階にし、固定ファイルマニフェストを1つの読み取り専用検証器で照合することで、既存の8/12/14件の並行計画から生じる誤取得を減らせる。
- **T**：12固定repo・131ファイル・50 SHA256の全件相互照合、9個の正負テスト、接続Linuxドライブ容量の読み取りを実施。標本最小件数は全件12、逐次停止は不一致が1つでも出た時点。ユーザーの4TB現物は未測定。
- **D**：PASS＝研究用source metadataが整合し、ハッシュ監査器が正しい。FAIL＝版・サイズ・ハッシュ・不正パス不一致、または空き容量不足。UNCERTAIN＝本人権利と実HDD、最終的な依存とオフライン復元の現状。
- **C**：正規配布元がfile再編、元repoのGateが変更、fileが欠損/重複、ライセンス不適合、4TB媒体の実空きが想定より小さい場合、モデル取得前STOPが継続。
- **U**：ファイルシステム空きは観測時刻と同時処理で変動。完全推論実装・HW/clock/batch/context、量子化zero-point、未数えの親/codecは未知。標準不確かさ`u_c`・包含係数`k`を適当に置かない。

**関連分野**：デジタルアーカイブ（content hashes/重複排除）、ソフトウェア供給網（再現性・Git/LFS SHA）、法務・AI配布政策（個人権利/Gated）、機械学習（量子化と特定タスクの保持性能）。

### ERROR CHECK

1. 研究source 12モデル・131ファイル・publisher SHA256参照50・206,683,452,429byte一致。test 9/9 PASS。
2. 実際に接続中の48GB級Linuxで`FAIL_CAPACITY`、**4TBユーザーディスクを検査したとは主張しない**。
3. v46登録198、有効151、未認可ダウンロード0、明示的最終批准マニフェスト0。
4. 新規選定・カタログ変更0、モデルコード/重み実行0、資料系GitHubファイルのみ追加。
5. ExaはHTTP 402で利用枠不足。これを解消していないのでExaによる2026-11-18時点の独立新規検索・一次資料取得は未実施。

### 〈次に考える問い〉

**これ以上モデルを探すより、既にsource固定した最小の原本1件について、実HDD・本人ライセンス・現物SHA・完全オフライン復元をPASSにする方が保存成果を確実に増やせるのではないか。**
