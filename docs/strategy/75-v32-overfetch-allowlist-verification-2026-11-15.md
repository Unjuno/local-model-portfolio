# R75 — 66件の選択ファイルallowlistを機械検証し、未説明の容量差分を隔離する

調査日：2026-11-15。正本：`main`のv32（管理182／有効135）。**追加・削除・承認・本体取得・モデル実行なし。**

[R74の66配布元・1,425ファイルの非実行候補](../../manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)を、独立の[R73・全135件の公開元ファイル同一性一覧](../../catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json)と厳密な`asset_kind+repo_id`で照合。検証用の[標準ライブラリのみの読み取り専用スクリプト](../../scripts/verify_r74_overfetch_allowlists.py)と[破損データに対する回帰テスト](../../tests/test_verify_r74_overfetch_allowlists.py)を追加した。

## 1.〈本論〉— 誤ったリポジトリ全量取得を防ぐ

| R74の観測値（66配布元のみ、重複あり） | byte／件数 |
|---|---:|
| 公開元repo範囲の単純延べ合計 | 4,767,695,305,908 byte |
| 選定したファイルだけの単純延べ合計 | 1,782,172,555,461 byte |
| **選定外の観測差分** | **2,985,522,750,447 byte** |
| 明示された選定ファイル | 1,425件 |
| 選択ファイルの公開元LFS SHA256あり | 491件 |
| Git blob SHA1だけで同一性を記録 | 854件 |
| Gated等で公開元ペイロードSHA256未確認 | 80件 |

同一配布元・revision・選択数・byte・masked件数は、**66件すべてでR73と一致**した。上表の1,425は66件の部分集合であり、R73全135資産の60,043ファイル参照やGated資産のSHA未確認762件と混同しない。

[R74 JSON](../../manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)の**正確な選択ファイル名**を使用する。Hugging Faceの[公式snapshot_downloadの仕様](https://huggingface.co/docs/huggingface_hub/main/guides/download)では`allow_patterns`はglobとして評価される。したがって、承認なしの`snapshot_download`、ワイルドカード、相対パス上位参照、選定外ファイルへの自動フォールバックを禁止する。スクリプト自体は**ダウンロードコードを含まず、読み取りと比較だけ**実施する。

### 新たに特定した追加調査事項：Qwen Imageの3,333,149 byte

`Qwen/Qwen-Image-2.1`のR74選択ファイルは**27件・33,131,616,412 byte**。同じ過去観測のrepo総容量は**33,134,949,561 byte**で、選択外の差は**3,333,149 byte**。しかしR74の`source_excluded_file_count`は**0**。数量差と除外ファイル件数の内訳が一致していないように見えるが、配布元サイズ集計方式または別のファイルメタデータによる差もあり得るため、追加ファイルの存在や改ざんは断定しない。

このケースを`unattributed_excess`として**レビュー待ちの警告**に分離し、誤って「除外済みファイル数ゼロだから全repo取得可能」と解釈しない。取得候補は従来どおり選択27ファイルに厳密限定する。R74選定やユーザーの許諾状態は変えない。

## 2.〈応用・転用例〉— 保存前の検証と停止条件

コードはPython 3.10以上、標準ライブラリのみ。Hugging Face、GitHub、モデルコード、外部コマンド、OSのネットワーク機能は呼ばず、権利情報の受諾も行わない。

```bash
python scripts/verify_r74_overfetch_allowlists.py
python -m unittest tests.test_verify_r74_overfetch_allowlists
```

機械監査で検査する条件：
- 66配布元がR73の135件に含まれ、固定revision、選択file countとbyte、観測repo byte、masked件数が一致する
- 選択file pathが絶対パスでも`..`でもglobでもなく、重複もない
- `lfs_payload_sha256`は64桁、`git_blob_sha1`は40桁。Gatedで未確認のblob SHA1を実重みのSHA256として扱わない
- `executable/download_authorized/auto_execute/auto_seed/allow_full_repo_download`がすべてfalse、各assetの権利・SHA・取得認可の未完了フラグも維持
- `queues/approved.json`のエントリが0件

**実施済み検証：** GitHub上のR74/R73/承認キューを読み、独立のJavaScript全件再集計で66レコード、1,425ファイル、masked80、差分2,985,522,750,447 byte、ID・revision・byte・SHA形式・ファイルパスの矛盾0を確認。上記**Python unittestの実行はこのセッションでは行っていない**ため、ソフトウェアテスト合格と混同しない。単体試験は回帰実行用成果物である。

### 変数表・単位検査

| 記号 | 意味（日本語） | SIに準じた単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_r` | 66配布元の観測全repo延べ容量 | byte | 4,767,695,305,908 | 非負・履歴revision | 整数スカラー |
| `B_s` | 選択した1,425ファイルの延べ容量 | byte | 1,782,172,555,461 | 非負・重複未排除 | 整数スカラー |
| `B_x` | 意図しない追加取得の観測差分 | byte | `B_r - B_s = 2,985,522,750,447` | 実機の節約量ではない | 整数スカラー |
| `N_f` | 明示選択ファイル参照数 | 1（件数） | 1,425 | 対象66配布元 | 整数スカラー |
| `N_m` | 選択ファイル中の未確認SHA256数 | 1（件数） | 80 | Gatedを含む、非負 | 整数スカラー |

次元検査：`B_r`と`B_s`はともにbyteであり、差分`B_x`もbyte。ファイル個数`N_f`、`N_m`との直接加減算はしない。

## 3. H / T / D / C / UとERROR CHECK

**H（反証可能仮説）**：66配布元の全ファイル名を明示し、非承認操作を拒否すれば、偶発的な全repo取得（最大観測差分約2.986TB）を未然に検出できる。

**T（最小検証）**：n_min=66配布元・1,425ファイルをR73と突合し、ファイル名改変・SHA型偽装・承認フラグ改変の回帰テストを実施する。停止条件は全66件完了または初回の不整合。外部取得なし。

**D**：公開元メタデータ計算は**PASS**。Python unittestの実際の実行・Gated本人許諾・ローカルSHA・完全復元は**UNCERTAIN**。権利がない取得や一致しないchecksumは**FAIL/STOP**。

**C**：異なるrevisionによるファイル増減、参照先の権利変更、必須codec/encoderの漏れ、単純リポジトリ観測容量とファイルリストの差。

**U**：将来の公開元revision、未確認SHA、ownerのHDD既存ファイル、runtime依存。測定誤差分布がないため合成標準不確かさ`u_c`と包含係数`k`は未算出。

**ERROR CHECK**：全66 IDをR73と照合、選択1,425、SHA491/854/masked80、計3分類の和1,425、容量差2,985,522,750,447 byte、候補取得承認0。**主張は一次データ整合性まで、実HDD保存成功を意味しない。**

関連領域：デジタル保存（原本同一性）、ソフトウェア供給網（依存・SHA）、ML実装（runtime再現性）、情報法務（権利・Gated）。

## 4.〈次に考える問い〉

**66配布元のうち、外部依存と権利が揃い、実HDDを確認できるものから、どれを最初のオフライン復元PASSに昇格できるか。**
