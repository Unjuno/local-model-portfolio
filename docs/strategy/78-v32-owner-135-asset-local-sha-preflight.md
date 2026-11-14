# R78｜v32全135資産を所有者HDDから読み取り専用で検査する（2026-11-15）

## 1.〈本論〉実装と現時点の合否

[既存ファイルSHA検査コード](../../scripts/audit_owner_v32_files.py)と[回帰テスト](../../tests/test_audit_owner_v32_files.py)を追加した。Python 3.10以上、標準ライブラリのみ。**Hugging Faceや外部モデルコードをimport・実行しない**。ファイルのダウンロード、モデル重みの読込/デシリアライズ、ライセンス同意、ファイルの変更・削除・承認キュー操作、利用者HDDへの接続を行わない。

- 正本v32は**登録182/有効135**。v27由来126資産は[旧一次ファイル選定台帳](../../catalog/capacity/2026-11-07/v27/selected-file-capacity.json)から、最近の8資産は[R64マニフェスト](../../manifests/drafts/r64-eight-source-scopes.candidate.json)から、ZONOS3は[R48のkeep2参考範囲](../../catalog/research/2026-11-12-r48-pinned-scopes.json)から、`repo_id`一致で構成する。
- **135資産の一次ファイル参照数は60,020**。内訳は旧59,938、R64の8資産68、ZONOS3の14。従来の[R73全参照](../../catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json)の**60,043**には、別途学習済み依存repo `ACE-Step/Ace-Step1.5` の23件を含む。これは137番目のモデルでも新規選定ではなく、R64の既存`archive_preflight.py`で別に検査する。
- 一致できる証拠はLFS等の**公開元SHA-256**または**普通のGit blob SHA1（blobヘッダー込み）**。LFSの**GitポインタSHA1**はモデル本体のSHA1ではないため、代替に使わない。ハッシュのないGatedのファイルはサイズが合っても`PUBLISHER_HASH_UNKNOWN`で止まる。シンボリックリンクは参照先がアーカイブ内部でも拒否する。
- 既存のモデル重みパスを固定した上で一つずつ選択してハッシュ検査する。デフォルトの全3TB走査は行わない。検査の結果が`SOURCE_HASHES_MATCH_ONLY`でも、**正規の許諾・全外部Codec/Encoder・runtime・4TBと200GB実空き・取得承認・オフライン復元のPASSではない**。

### 所有者がすでに正規に保持するファイルの検査例

リポジトリのルートで実行し、以下を既存HDDの実パスに置き換える（`/YOUR_ARCHIVE_ROOT`は仮値）。

```bash
python3 scripts/audit_owner_v32_files.py \
  --archive-root /YOUR_ARCHIVE_ROOT \
  --asset-id ibm-granite/granite-timeseries-ttm-r3 \
  --source-root ibm-granite/granite-timeseries-ttm-r3=/YOUR_ARCHIVE_ROOT/EXISTING_TTM_DIRECTORY
```

標準格納形式で保存済みなら`--source-root`は省略できる。探索される相対パスは`store/huggingface/model/<organization>/<repo>/<40-character revision>/<filename>`。既存Hugging Faceキャッシュのファイルが別レイアウトの場合には`--source-root`で**該当repoの既存ディレクトリ**だけを明示する。現物がない場合は`MISSING`、サイズ不一致は`BAD_SIZE`、ハッシュ不一致は`BAD_HASH`、根拠SHA不足は`PUBLISHER_HASH_UNKNOWN`、危険なリンクは`UNSAFE_PATH`を返す。

### 実装前提・攻撃面

- Python 3.10+、Windows/Linux/macOSの通常ファイル。ハッシュ計算は4MiBのストリーミング単位。GPU/CUDA/モデルランタイム・ABI・zero-pointに一切依存しない。
- **既存HDDにアクセスし読み取るのはユーザーが明示的にCLIを起動した時のみ。** 本研究では利用者HDDのファイルと空き領域を検証していない。
- シンボリックリンクはチェック時に拒否するが、別プロセスが同時にファイルを差し替えるTOCTOU競合は完全には排除しない。読み取り専用の安定したスナップショット（例：権限で変更を防いだボリューム）で実行し、用途別のライセンス・ファイルmanifestを別に保管する。
- 大規模な135資産全体を一度にハッシュすると長時間のHDD走査になるため、最小依存から始める。新規ダウンロードや外部runtimeの自動インストールを兼ねさせない。

## 2.〈応用・転用例〉

1. [IBM TTM-R3固定6ファイル](../../catalog/research/2026-11-15-r69-ibm-ttm-r3-publisher-runtime-pin.json)のような小型資産から`SOURCE_HASHES_MATCH_ONLY`を実測し、欠落・サイズ違い・ハッシュ不明を区別。参照が見つからなければダウンロード承認を自動作成せず調査へ戻す。
2. ACE-Step音楽生成については、同じ本体と親Qwen Embedding・VAEをハッシュで一致させ、共通SHAのファイルだけを再利用する。公式コードに暗黙のストック2Bモデル自動ダウンロードがあるので、重みの原本ハッシュ検査と実行は分離。
3. LTX動画の別fine-tuneは、同名/同容量を同一学習状態と見なさずSHA差・追加学習の一次証拠で判断する。

## 3. H/T/D/C/U・変数表と次元チェック

| 記号 | 意味（日本語） | SI単位 | 定義／範囲／前提 | 型 |
|---|---|---|---|---|
| N | 有効研究資産件数 | 1（件） | 135、v32のみ | 整数スカラー |
| F27 | v27旧参照ファイル件数 | 1（件） | 59,938、旧台帳由来 | 整数スカラー |
| F64 | R64新8資産の参照ファイル件数 | 1（件） | 68、ACE外部23除外 | 整数スカラー |
| F48 | ZONOS3の参照ファイル件数 | 1（件） | 14、nonminimalな参考scope | 整数スカラー |
| F | 135有効資産の参照ファイル件数 | 1（件） | F27＋F64＋F48＝60,020 | 整数スカラー |
| E | R64外部ACE repoの参照ファイル件数 | 1（件） | 23、有効資産数に加算しない | 整数スカラー |
| B | 所有者HDDの現物容量 | byte | 未測定、null。空きとは別 | 整数スカラーまたはnull |

単位チェック：F27/F64/F48/F/Eはファイル件数で加算可能。Nは資産件数、Bはbyteなので互いに加算しない。

H：公開元の固定sha/revisionと既存HDDの実ファイルhashを比較すると、保存済みと未保存を合法的に識別できる。  
T：全135 asset IDのsource参照を構築し、初回n_min=1資産、各ファイルのサイズとハッシュを検査。不一致が出たらその資産をSTOP。  
D：全要求ファイルが一致すれば`SOURCE_HASHES_MATCH_ONLY`、欠損・SHA不明等は`INCOMPLETE_OR_UNKNOWN`。どちらも取得承認・オフライン再現はUNCERTAIN。  
C：保存されたリポジトリが別revision、LFSポインタSHAを誤比較、ファイルが途中で変更された、外部必須コードや権利が欠損。  
U：現物・本人権限・GPU環境・staging/cache・実機の空き・競合変更。確率モデル未定義のため合成標準不確かさu_cと包含係数kを数値化しない。

**ERROR CHECK：** SHA/サイズ・リンク・SHA不明・パストラバーサルの**合成小型フィクスチャ6条件をローカルPythonでPASS**。実v27の59,938行を用いたGitHub上の全レポジトリ回帰テストは未実行。実モデルファイルDL0、外部runtime実行0、GitHub承認キュー変更0。

**関連分野**：デジタルアーカイブ（真正性）、サプライチェーン（署名・SHA）、MLOps（再現性）、セキュリティ（TOCTOUとデシリアライズ）、知的財産（用途別権利）。

## 4.〈次に考える問い〉

原本ファイルのSHAが一致した後に、学習済み外部依存とPython wheelhouseのSHAまで追跡するには、どのバイナリ依存を最初の不可欠ノードとして固定すべきか？
