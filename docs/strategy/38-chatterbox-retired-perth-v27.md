# 38 — Chatterbox保守終了とPerthの再現可能な音声透かし依存（2026-11-07）

## 判断（新モデルの追加なし）

`catalog/CURRENT.json` **v27-20261107：173資産／有効126件**、既知一次重み・関連選定ファイルの論理重複排除後 **3,417,685,712,585 B**を正本とする。オフライン復元に未解決事項がある資産は**35件**。所有者ディスクの実空き、取得ピーク、完全依存込み総バイトはUNKNOWN。本件は**既選定のResembleAI/chatterboxの調査、復元プログラムと学習済み透かしモデルの保存設計**であり、新規採用・除外・取得承認は行わない。

## 1. 実際の変更：配布元によるChatterbox研究終了

- [配布元Chatterbox README](https://github.com/resemble-ai/chatterbox/blob/ab55923c27757c90cfcc407baa57dc25a7d25217/README.md)：2026年8月以降「retired research」「no longer maintained」と告知。**モデルの配布削除予告とは言っていない**。最終のREADME更新commitは2026年11月4日。保守停止により将来のソフトウェア依存更新を保証できなくなったことが、早期**復元準備**の実務的根拠。
- [配布元chatterbox Git SHA](https://github.com/resemble-ai/chatterbox/tree/ab55923c27757c90cfcc407baa57dc25a7d25217) `ab55923c27757c90cfcc407baa57dc25a7d25217`。GitHub APIの全ファイルツリー**66 blob／1,870,627 B**。MITコードと`pyproject.toml`を含む。Git object/pack/zip展開実測ではない。
- [Perth SHA](https://github.com/resemble-ai/Perth/tree/ff1c8ac55a976971245cdd53c18d6131ca00d993) `ff1c8ac55a976971245cdd53c18d6131ca00d993`。全ツリー**37 blob／38,066,448 B**、MIT source licence。**Perthは学習済みの別モデルを同梱**している。
- Perth必要checkpoint：`src/perth/perth_net/pretrained/implicit/perth_net_250000.pth.tar`、**37,429,684 B**、Git **blob SHA-1** `22fbc47e03a4df700425819e9b5a1f81304f3a60`。**SHA-256は今回未取得／未実測**。ファイル名とGit SHA-1をペイロードSHA-256と偽らない。

## 2. 因果的な必須依存と再現不能の破れ方

[Chatterbox固定版multilingual実装](https://github.com/resemble-ai/chatterbox/blob/ab55923c27757c90cfcc407baa57dc25a7d25217/src/chatterbox/mtl_tts.py)では、`perth.PerthImplicitWatermarker()`をモデル初期化時に生成し、最終波形に`apply_watermark`を適用する。Perthの[既定models_dir](https://github.com/resemble-ai/Perth/blob/ff1c8ac55a976971245cdd53c18d6131ca00d993/src/perth/config.py)はパッケージ内部`perth_net/pretrained`で、[Perth読み込みコード](https://github.com/resemble-ai/Perth/blob/ff1c8ac55a976971245cdd53c18d6131ca00d993/src/perth/perth_net/perth_net_implicit/perth_watermarker.py)が学習済みチェックポイントを読む。**透かしの除去やバイパスは提案しない**。正確なアーカイブには公表の透かしモデル自体を一組として保存する。

**重要なv3選定とloader既定の不一致：** このChatterbox実装は多言語T3のデフォルトが`t3_mtl23ls_v2.safetensors`だが、v27で保存選定したのは`t3_mtl23ls_v3.safetensors`。そのため、v27の選定ファイルだけで復元する際は`from_local(..., t3_model="v3")`を明示する必要がある。固定版ローダーが読むS3Genは`s3gen.pt`（既存選定）であり、別に存在する`s3gen_v3.pt`が本来必須と断定する証拠はない。S3Gen v3は別重みとして公開されているが、形式重複と独立訓練能力の確認前に自動追加しない。

**別の変動箇所：** [固定版`pyproject.toml`](https://github.com/resemble-ai/chatterbox/blob/ab55923c27757c90cfcc407baa57dc25a7d25217/pyproject.toml)は`resemble-perth @ git+https://github.com/resemble-ai/Perth.git@master`で最新版を動的取得する。これでは1年後に同じ環境を再構成できるとは限らない。`ff1c8ac...`へ参照版を固定した**別途アーカイブ用環境manifest**を準備すること（今回実際のソースコード/依存を変更したりpipで導入はしない）。

## 3. ABI・ライセンスの残問題

- 配布元Chatterboxの`pyproject.toml`にはPython `>=3.10`、Python 3.14未満は`torch==2.6.0`／`torchaudio==2.6.0`、`transformers==5.2.0`、`diffusers==0.29.0`が指定される。一方[開発元README](https://github.com/resemble-ai/chatterbox/blob/ab55923c27757c90cfcc407baa57dc25a7d25217/README.md)が報告するテスト環境はPython 3.11／Debian 11。CUDA/HW/clock/ABIと各wheelハッシュ、実GPUメモリ、30試行・生成品質は未計測。
- [Perth fixed `__init__.py`](https://github.com/resemble-ai/Perth/blob/ff1c8ac55a976971245cdd53c18d6131ca00d993/src/perth/__init__.py)は`ImportError`を捕捉して`PerthImplicitWatermarker = None`を代入する。この場合、単に`import perth`できても**音声透かしが動作する保証はない**。[上流Issue #23](https://github.com/resemble-ai/Perth/issues/23)にも同様の利用者報告があるが、報告にある特定PyPI公開失敗は本調査で独立再現していない。
- [Perth上流Issue #22](https://github.com/resemble-ai/Perth/issues/22)ではMITライセンスの適用範囲と学習済み37.43MB checkpointの権利・原本来歴について配布元確認が要求され、現時点でIssueは未解決。**MITコードを確認したこと≠チェックポイントの再配布適法性の最終判定**。保存可否・第三者公開は本人権利を個別確認する。

## 4. 容量（GitHub Git blobの生バイト・実保存容量ではない）

| 構成要素 | 全コードツリーの配布元Git blobバイト数 |
|---|---:|
| Chatterbox runtime 66 blob | 1,870,627 B |
| Perth 37 blob（学習済み重みを含む） | 38,066,448 B |
| **追加コード・透かし重みの生ファイル総和** | **39,937,075 B** |

[機械監査JSON](../../catalog/research/2026-11-07-chatterbox-perth/audit.json)では、v27の全126一次スコープ＋既算入のMOSS等共有依存に、この2つの固定ソースツリーを加えてGit SHA識別子で論理重複排除し直す。**今回の候補容量を正本のv27 3,417,685,712,585 Bに無条件加算しない**。測定可能なファイルの既知サイズと、実際のオフライン完結・パッケージホイール・ソフトウエア、実ディスク残量、stagingは明確に分ける。

4TB＝**4,000,000,000,000 B**、物理空き床＝**200,000,000,000 B**は不変。上流のgit bundle（履歴全部）、wheelhouse等はこのGit blobサイズには入っていない。保存先HDDへのアクセス権がないので使用可能な実空きは**UNKNOWN**。

## 5. H/T/D/C/U・ERROR CHECK

- **H**：Perth固定モデル・コード、元Chatterboxコードを保存し、多言語v3の明示指定を行わないと元の出力を正確に再構築できない可能性がある。ソースと重みの再取得不可になる確率は推定していない。
- **T**：固定Git commit各1個の全ファイルGit SHA-1／byte、README保守終了宣言、MIT原文、`mtl_tts.py`とPerthコードの依存先を読取専用で照合し、既存v27容量のGit blob識別子による重複排除増分を機械計算。ソースファイルは小さいテキストのみ読み、37MB学習済み透かし重みは**ファイルツリーメタデータのみ**確認。配布元実行コードの実行、音声生成、本人HDD測定、取得はなし。
- **D**：SOURCE PASS＝SHA・bytes・原コード依存・全ファイル集合の整合。RESTORE PASS＝本人権利、実ファイルSHA256、Python/Torch/Transformer/wheelhouseのABI、実ディスク保管、ローカル音声出力の復元。後者は現在**UNCERTAIN**。
- **C**：Chatterbox側`master`を更新するとPerthパッケージ/チェックポイントが変わる、デフォルトv2が選定v3と合わない、`PerthImplicitWatermarker`がNone、著作権・依存wheelの不備、再現性喪失。
- **U**：配布元のGitツリーメタデータの整数バイトは厳密だが、現物SHA256、パッケージ固有の圧縮・キャッシュ、使用GPU/環境不明。正規誤差分布がないため合成標準不確かさ`u_c`と包含係数`k`は数値化不可。

**ERROR CHECK**：新規採用0、新規HOLD/REJECT0、`CURRENT.json`・取得承認・main・既存選定ファイル総和は不変。学習成果／デジタルアーカイブ／ソフトウェア供給網／権利の観点を区別。実機復元とローカル容量測定は行っていない。
