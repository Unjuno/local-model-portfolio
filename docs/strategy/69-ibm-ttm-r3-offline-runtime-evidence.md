# R69 — IBM TTM R3：公開元原本と公式runtimeの固定証拠、オフライン復元の停止条件

調査日：2026-11-15（日本時間）。対象：v32の有効135件のうち、最初の小型復元試験候補`ibm-granite/granite-timeseries-ttm-r3`。**本書は根拠の追加であり、ダウンロード承認・実HDD保存・復元合格を意味しない。**

機械可読証拠：[R69 JSON](../../catalog/research/2026-11-15-r69-ibm-ttm-r3-publisher-runtime-pin.json)／既存6ファイル：[R64 8資産マニフェスト](../../manifests/drafts/r64-eight-source-scopes.candidate.json)／正本：[CURRENT](../../catalog/CURRENT.json)。

## 1.〈本論〉— 公開元の実物同一性

- 公式モデルrepo：[`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/tree/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa)。
- 固定revision：`ea17cfd2e3edcaea21eb8dcecd18bf88971482fa`。
- R64で列挙済みの6ファイル：`.gitattributes`、`README.md`、`config.json`、`model.safetensors`、`model.sig`、`ttm_image.webp`。合計 **6,126,375 byte**。この容量はモデルrepo部分のみ。
- 重みファイル：**5,729,424 byte**。R64の公開元SHA256 `8ec0509a18a38f65b02f046fc28298ab3acf5d54eecb0a0df959b9fa001bc9fb`と、[同revisionのHugging FaceのXet pointer表示](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/blob/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa/model.safetensors)のSHA256が**一致**。独立の実ファイルSHA再計算ではない。
- [モデル`config.json`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/blob/main/config.json)：`context_length=512`、`prediction_length=30`、`num_input_channels=1`、`distribution_output=student_t`。Hubの約1.4Mパラメータ表示は参考値であり、静的tensor censusの実測値ではない。
- Hubの`apache-2.0`タグは確認。ただし**モデルrepoには専用のLICENSE全文ファイルがない**。タグを所有者ごとの利用許可確認と同一視しない。

## 2. 公式runtimeのソース版を今回新たに固定

IBM公式ソース：[`ibm-granite/granite-tsfm` commit `31fa2f01573341f17e9997280f61481de18ce28c`](https://github.com/ibm-granite/granite-tsfm/tree/31fa2f01573341f17e9997280f61481de18ce28c)。

以下は上記固定commitの`pyproject.toml`をGitHubから直接読み、対象ファイルのGit blob SHAもR69 JSONに記録した結果。

| 条件 | 公式固定ソースの宣言 | 検証上の意味 |
| --- | --- | --- |
| Python | `>=3.11,<3.15` | READMEの「3.10対応」を優先しない |
| PyTorch | `>=2.10,<2.12` | CPU/GPU backend・ABI・wheelを別途固定 |
| Transformers | `>=4.57.6,<6` | v4/v5間の互換性を実行環境で確認 |
| NumPy | `<3` | 下限は固定ソースに指定なし |
| pandas | `>=2.3.3,<4` | 上限の範囲だけでは復元同一性を保証しない |
| scikit-learn | `<1.8` | 依存wheelは未固定 |
| filelock | `>=3.20.3` | 上限未指定 |
| einops | `>=0.7` | 上限未指定 |
| ビルド | setuptools/Cython/setuptools-scm | ビルド環境とwheelhouseの固定が必要 |

**コード検査上の新しい注意点：** `tsfm_public/models/tinytimemixer/__init__.py`は`utils_tinytimemixer`の3関数を遅延exportするが、上記commitで`tsfm_public/models/tinytimemixer/utils_tinytimemixer.py`の取得は404だった。GitHubコード検索でも当該実装が見つからず、`__init__.py`の参照だけ確認された。特定のutility importが失敗する**可能性**がある。ただし遅延importのため、モデル予測が失敗すると断定はできない。必要なimport経路をオフラインで検証するまではruntime互換をPASSにしない。

上記は**公式ソースを固定して依存宣言を確認した**段階。pip解決済みwheel、外部推論コード、端末OSとCPU ABI、モデルのテンソルshape、単体予測動作、実速度を確定したものではない。現時点でCUDAやGPUの使用を前提にしない。

## 3. 閉じていないゲートと安全な検証順

1. **権利と原本**：モデルrepoのライセンスタグとコードrepoのApache-2.0 LICENSEを区別し、用途・NOTICEの適用を確定する。
2. **完全なruntimeソース**：公式の固定commitを参照し、実行に必要なパッケージファイルと内部import全体の閉包を列挙する。コードを実行する前に内容を審査する。
3. **依存wheelhouse**：Python/PyTorch/Transformersとtransitive requirementsの具体的バージョン・wheel SHA256・OS/ABI・CPU instruction setsを固定する。上表の範囲条件はlockfileではない。
4. **実機現物**：本人の正規所有ファイルについて既存の`scripts/archive_preflight.py`を`--hash`付きで使用。OSファイルシステムの実空きとstage/cacheを確認。**未取得ファイルを自動で入手しない**。
5. **オフライン復元**：ownerの明示実行許可後、ネットワーク遮断、`HF_HUB_OFFLINE=1`、`TRANSFORMERS_OFFLINE=1`、モデルpathは絶対ローカルパス、`local_files_only=True`で合成時系列を入力。テスト開始前に固定ソースSHAを照合する。入力の予定shapeは`[1,512,1]`、想定の予測期間は30 step。具体的な推論API互換性は未検証。
6. **PASSの証拠**：ローカルSHA一致、依存wheel/コードSHA一致、推論結果のfinite値・出力shape、二度目の独立なオフライン起動の再現とログ。数値誤差閾値・PyTorch backend設定は実機指定後に設定する。いずれの実行も本調査では行っていない。

### 変数表

| 変数 | 日本語の意味 | 単位（SI） | 定義・範囲・前提条件 | 型 |
| --- | --- | --- | --- | --- |
| `B_total` | 固定モデルrepo6ファイルの公開元容量 | byte | 6,126,375。R64指定ファイルの和、非負 | 整数スカラー |
| `B_weight` | モデル重みファイル公開元容量 | byte | 5,729,424、非負 | 整数スカラー |
| `L_context` | 入力時系列長 | 1（sample数） | 512、固定モデルconfig | 整数スカラー |
| `L_pred` | 予測時系列長 | 1（sample数） | 30、固定モデルconfig | 整数スカラー |
| `C_in` | 入力チャネル数 | 1（channel数） | 1、固定モデルconfig | 整数スカラー |
| `H_disk` | 実HDDの現在空き | byte | 未計測、非負 | 整数スカラー／null |

**次元チェック：** 6,126,375 byteと5,729,424 byteの差は396,951 byteの支援ファイル。bytes同士の差であり、モデルパラメータ個数と混ぜない。

## 4. H / T / D / C / UとERROR CHECK

- **H（反証可能仮説）**：公式の固定モデル6ファイルと固定コード+wheelを合法に揃えれば、ローカルCPUで短い時系列予測をオフライン再現できる。
- **T（最小検証）**：model repo6ファイル、official Git commit1、全wheelのSHA照合後、同一の合成入力で別プロセス2回。未承認の取得は行わない。
- **D（合否）**：PASS＝SHA/ABI/許諾/完全依存と2回の有限出力・shape一致。FAIL＝ハッシュ不一致、import破綻、権利不足等。UNCERTAIN＝未取得・未測定（**現在**）。
- **C（破れ方）**：READMEとpackage要件の差、optional import欠落、未固定wheel、外部の遠隔モデル取得、CPU演算差。
- **U（不確かさ）**：publisher metadataだけではローカルbit同一性が未証明。誤差分布・ハード構成がないため合成標準不確かさ`u_c`と包含係数`k`は未算出。

**ERROR CHECK：** モデル6ファイル・6,126,375 byte、公開元重みSHA一致、runtime Git commitと公式依存要件を固定。実HDD hash未検証、学習済み全依存/runtime wheels未完全固定、実行・取得・承認は0件。

## 5.〈次に考える問い〉

**IBMの固定runtimeコードで`TinyTimeMixerForPrediction`の予測経路が、欠落しているutility exportに依存せず完全にオフライン動作することを、ownerの端末で確かめられるか。**
