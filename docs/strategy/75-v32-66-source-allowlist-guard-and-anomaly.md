# R75：66配布元の明示ファイル取得候補をfail-closed検証（2026-11-15）

**対象**：現行`main` v32・182資産のうち、[R74候補](../../manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)に収録された66配布元。出力は**非実行の研究・検証**であり、重み・データの取得、許諾同意、実機実行、承認を行っていない。

**追加した実装**：[検証スクリプト](../../scripts/verify_v32_overfetch_scope.py)／[回帰テスト](../../tests/test_verify_v32_overfetch_scope.py)／[検証結果JSON](../../catalog/audits/2026-11-15-r75-overfetch-allowlist-hardening.json)。根拠は[R73公開元同一性台帳](../../catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json)と[R74候補ファイル一覧](../../manifests/drafts/r74-66-source-overfetch-allowlists.candidate.json)。

## 1.〈本論〉— 新しい静的検証の実結果

| 検証した対象 | 実測した台帳値 | 意味 |
|---|---:|---|
| 配布元スコープ | **66** | R73とasset_kind＋repo_idで突合 |
| 厳密ファイルパス | **1,425** | 相対パス・重複・glob文字を全件検査 |
| 選択ファイル容量の単純合計 | **1,782,172,555,461 byte** | 対象66件のファイル候補部分のみ |
| 観測配布元スコープの超過差分 | **2,985,522,750,447 byte** | 過剰取得する可能性がある延べ範囲であり、実節約容量ではない |
| LFSの公開元SHA256表記あり | **491** | 文字列形式を検査。実ファイルをハッシュ再計算していない |
| Git blob SHA1表記あり | **854** | 内容のGit同一性参照。LFS本体SHA256を意味しない |
| 配布元ペイロードSHA未検証 | **80** | Gated等のため実体と照合できていない |
| 正当なゼロバイトGit blob | **3** | 空ファイルを誤って不正扱いしない |
| 要説明のメタデータ差分 | **1** | Qwen/Qwen-Image-2.1 |
| 追加した取得承認 | **0** | 承認キューは空 |

検証プログラムは、全66件のimmutable revision（40桁hex）、1,425個のファイルパス、公開元同一性の型・形式、R73のrevision/byte/ファイル数/マスク数、全source超過分の合計、`download_authorized=false`等を要求する。**欠損や矛盾があれば例外で停止**する。公式`huggingface_hub.snapshot_download`の`allow_patterns`は`fnmatch`のワイルドカードを用いるので、今の候補は`*`・`?`・`[]`を含まない**文字列としての厳密ファイル名**のみ許可する。さらに`..`・絶対パス・Windows区切りを拒否する。API仕様：[Hugging Face公式ガイド](https://huggingface.co/docs/huggingface_hub/main/guides/download)および[関数仕様](https://huggingface.co/docs/huggingface_hub/package_reference/file_download)。

### 静的照合で明らかになった2件の注意事項

**A. 誤検知の原因：ゼロバイトでも合法なGitファイルが3件ある。** `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`の`samples/nul`と`workflow_examples/nul`、`KlingTeam/LivePortrait`の`.gitkeep`。これらはすべてGit空blobのSHA1 `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`を持つ。単純に`bytes > 0`で検査すると正規の選択対象を不当に弾くため、**ゼロバイトを許すのはGit空blob同一性が一致した場合のみ**にした。

**B. 要調査：`Qwen/Qwen-Image-2.1`でsource超過容量と除外ファイル数が食い違う。** R74では観測repo scope **33,134,949,561 byte**、選択scope **33,131,616,412 byte**、差 **3,333,149 byte**、一方`source_excluded_file_count=0`。ファイルが何件不足しているか、メタデータの課金外範囲・版差などが原因かは**現時点では証明不能**。数値を勝手に修正せず、`UNEXPLAINED_METADATA_SCOPE_DIFFERENCE`として記録した。解決には[固定revision `790c92633540aa0cb11d9abf19eb46d861714758`](https://huggingface.co/Qwen/Qwen-Image-2.1/tree/790c92633540aa0cb11d9abf19eb46d861714758)の公開元全ファイルscope・時点と選択27ファイルの再照合が必要。

### 既存テストの実装不整合も修正

`tests/test_verify_v32_primary_source_capacity.py`が`audit.verify(root)`を呼ぶ一方、`scripts/verify_v32_primary_source_capacity.py`の関数が引数無しだったため、**その回帰試験では意図した重複ファイル行検出の分岐に到達できない**。今回関数に、履歴レポートの参照rootだけを置換できる任意引数`report_root`を追加した。既存の通常呼出しと其他の`audit.j`モック経路は変更していない。

**実施範囲の境界**：GitHubコネクタから取得したJSONを独立の読み取り専用JavaScript照合で実データ全件検査し、上述の件数・差異を確認した。Python版検証プログラムおよび単体テストはGitHubへコミットしたが、**このターンではPythonテストもGitHub Actionsも実行していない**。したがって`PASS`は公開元台帳の構造照合のみに限定する。元v27約21MBの原本の全ペイロードSHAを再計算したものでもない。

## 2.〈応用・転用例〉

- **モデル保存**：取得エージェントがprofile外のGGUF量子化・旧重みや不要な動画サンプルを取得することを事前に防ぐ。
- **ソフトウェア供給網**：revision・SHA256とGit blob SHA1を分離し、ハッシュ未確認のGated資産を誤って「検証済み」としない。
- **デジタルフォレンジック**：0 byteファイルでも真正のGit空blobなら正規の来歴として記録する。
- **法務／ストレージ管理**：所有者のGatedアクセス、配布元のライセンス正文、実HDD空き200GB、別学習済みcodecやruntimeの閉包は、ファイルリストに合格しても独立の停止条件として維持。

### 実装前提と検査手順

Python **3.10以上**の標準ライブラリのみ。repoルートで`python scripts/verify_v32_overfetch_scope.py`を実行すると読み取り専用JSONを返す。`python -m unittest tests.test_verify_v32_overfetch_scope`（テストpackageとして発見可能な環境）または`python -m unittest discover -s tests -p 'test_verify_v32_overfetch_scope.py'`で回帰試験できる。どちらもネットワーク・モデル本体取得・実行不要。出力は**ダウンロード命令ではない**。ユーザーの実機Python/CPU/OS/パス・取得権限は未検証。

## 3. 変数表、次元検査、検証設計

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `R` | 検査した配布元数 | 1（個） | R74の配布元数66 | v32・非実行候補 | 整数スカラー |
| `F` | 選択ファイル参照数 | 1（個） | R74の各ファイルを列挙した1,425 | 重複パス不可 | 整数スカラー |
| `B_s` | 選択scope容量 | byte | 1,782,172,555,461、66件の選択容量和 | 参照延べ合計で共有重み未排除 | 整数スカラー |
| `B_x` | 観測されたscope超過容量 | byte | 2,985,522,750,447、観測repo容量から選択容量を減じたもの | 実HDDの節約実績ではない | 整数スカラー |
| `B_q` | Qwen資産の未説明差 | byte | 3,333,149 | 固定スコープの由来は調査待ち | 整数スカラー |
| `H` | SHA256本文未検証ファイル参照数 | 1（個） | 80 | R74対象66件のみ | 整数スカラー |

**単位チェック**：`B_s`、`B_x`、`B_q`はbyte同士で比較できる。`R`、`F`、`H`は無次元の件数であり、byteとは加減算できない。

**H（仮説）**：固定文字列パスと公開元revision/SHA情報だけを用いると、66件について意図しないrepo全量取得を静的に防止できる。

**T（最小検証）**：66件、1,425ファイル全件（最小サンプル`n_min=1425`）、正常データと不正パス・重複・SHA改変・承認フラグ改変・0 byteの異常Git blobを試験。全件処理終了または最初の不一致でSTOP。

**D（判定）**：PASS＝全件の形式・原本revision・集計一致、承認追加0。FAIL＝不正パス、ハッシュ文字列不整合、出典矛盾、権限フラグ不一致。UNCERTAIN＝本体SHA再計算・法務・依存・実HDD・オフライン復元（現在）。

**C（対立仮説）**：完全に適法な取得でも、候補scopeに外部必須EncoderやVAEが入っておらず復元不可能な場合がある。Gatedのメタデータからは正規取得権限を立証できない。

**U（不確かさ）**：配布元の時点差、Qwenの3,333,149 byte差、masked80、親モデル再利用の未検証、wheelと端末容量。独立の測定分布がないため合成標準不確かさ`u_c`と包含係数`k`は計算できない。

**ERROR CHECK**：66件／1,425参照／491 LFS SHA256表記／854 Git blob参照／80本体SHA未確認／3空Git blob／不整合1件／approved0。全135件の取得可能性や完成保存を意味しない。

## 4.〈次に考える問い〉

**固定revisionのQwen-Image-2.1で3,333,149 byteのsource差が何から生じたかを、全ファイル一覧と選択対象の突合で確定できるか。**
