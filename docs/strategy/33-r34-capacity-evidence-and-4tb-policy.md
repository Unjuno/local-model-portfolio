**R35容量更新（2026-11-08）**：Stubelius全14ファイル**195,942,118,539 byte**、最新版v1 BF16**42,008,732,600 byte**、差**153,933,385,939 byte**へ丸め値を置換。Chrisの本家・ミラー15重みSHAが一致し、FP8 scaledの暫定基本構成は**36,468,259,016 byte**と確定。[R35 exact LFSファイル監査](34-r35-ltx-source-vs-mirror-file-identity.md)を参照。下記の約195.9GB/42GB/153.9GB表記は当時の丸め値のまま保持。

# R34｜4TB保存計画の容量証拠：150資産のメタデータ監査

2026-11-08。現行v19の150資産を再集計した読み取り専用の研究。今までのSELECT/CONDITIONAL/HOLD/BACKLOG、Nanbeige4.3-33B SELECT、6件のユーザー指定EXCLUDEDを変更しない。

[全150件の監査台帳](../../catalog/research/2026-11-08-r34-capacity-evidence.json) / [実機の読み取り専用検査](../../scripts/archive_preflight.py) / [固定済みR21モデル構成](../../manifests/drafts/round21-pinned-preservation.candidate.json)

## 1. 何が分かり、何が分からないか

| 指標 | 件数・容量 | 注意点 |
|---|---:|---|
| 全資産／有効選定 | 150／105件 | モデル90・データ15。ダウンロード承認とは別 |
| 配布元repoサイズが確認できる有効資産 | 83件 | 合計2,861,783,364,610 byteは**全repo**の表示容量で、実際の保存計画容量ではない |
| 配布元repoサイズが不明な有効資産 | 22件 | LTX 2.5、Stuubs、Chrisなどを含む。未知値を0とはしない |
| カタログ内で選択ファイルのbyteが確認できる資産 | 2件 | 合計18,409,500,600 byte。依存ファイルを含む全構成ではない |
| 全repoの表示サイズが100GB以上の有効資産 | 8件 | 全repo合計1,403,226,367,788 byte。個別選択サイズではない |
| 保存計画上限 | 4,000,000,000,000 byte | 実際の空き・staging未測定。200GB安全空きを別に維持 |

**重要な誤解の防止**：全repoの既知合計2.862TBを4TBから引き、1.138TBが実際に空いているとは言えない。既知のrepoには不要な別精度・過去重みがあり、22件の未確認値は抜けている。この数字は選択ファイルの必要容量の上限でも下限でもない。

## 2. 先にファイル構成を確定させる8件

| 配布元 | 現行判断 | 全repoの容量 | 実施すべき監査 |
|---|---|---:|---|
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | SELECT | 241.89 GB | 固有の学習済み重みを確認。選択ファイル・依存未確定 |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | CONDITIONAL | 217.32 GB | 固有の学習済み重みを確認。選択ファイル・依存未確定 |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | SELECT | 195.76 GB | 固有の学習済み重みを確認。選択ファイル・依存未確定 |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | CONDITIONAL | 177.64 GB | 固有の学習済み重みを確認。選択ファイル・依存未確定 |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | SELECT | 159.38 GB | 固有の学習済み重みを確認。選択ファイル・依存未確定 |
| [IFM/SFT-Reasoning](https://huggingface.co/IFM/SFT-Reasoning) | CONDITIONAL | 158.56 GB | 学習データ・ラベルの固有性を確認。選択ファイル・依存未確定 |
| [EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | CONDITIONAL | 141.12 GB | 固有の学習済み重みを確認。選択ファイル・依存未確定 |
| [nvidia/Granary-v2](https://huggingface.co/nvidia/Granary-v2) | CONDITIONAL | 111.56 GB | 学習データ・ラベルの固有性を確認。選択ファイル・依存未確定 |

8件には独立した汎用重み、コード専門学習、画像・医療特化、再収集が難しいデータが混在する。用途が似ていても**同一の学習状態とは限らない**。元重みを残す価値を、単なる量子化別コピーの有無と区別して評価する。

## 3. 実際の選択ファイルと依存を積み上げる例

| R21固定構成 | カタログ内の個別ファイル容量 | 別repoの不可欠な依存 | 完全な研究構成 |
|---|---:|---:|---:|
| Interpretic Q4 + 画像projector + 許諾・設定 | 17,738,327,225 byte | 原BF16 repoのLICENSE・config等30,127 byte | **17,738,357,352 byte** |
| ChatR Qwen-Image2.1特殊LoRA | 671,173,375 byte | 固定Qwen-Image2.1ベース・Encoder・VAE 33,131,616,412 byte | **33,802,789,787 byte** |

上記のR21限定2構成は合計**51,541,147,139 byte**。これは105件全体の容量ではない。ChatRの33.13GBのベースがローカルの既保存重みと一致した場合は再取得不要になり得るが、**実機で同一SHAを確認していない**ため節約を確定させない。Interpreticの30,127byteの差は誤差でなく別repoのライセンス・来歴等の必須ファイル。

## 4. 通常量子化の過剰保存を減らす具体例：LTX Stubelius

[Stubelius公式モデルツリー](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/tree/main)は現在、約195.9GB分の7種類の重みを表示する。しかし独立した学習状態はbeta1、beta2、v1の**3段階**で、beta2のBF16/INT8、v1のBF16/INT8/NVFP4/Q4は学習状態ごとの異形式。

最新版v1の高精度原本だけなら**約42GB**であり、全7ファイルを保存する構成と比べ**約153.9GBを計上せずに済む**という概算シナリオになる。これは実ディスクで回収済みの容量ではなく、すべて公開画面の丸め表示に基づく。beta1/beta2も異なる学習成果なので、実際の研究価値があれば複数段階を保存可能。**特殊版の件数に機械的な上限を置かない**。

## 5. スクリプトの実修正

従来のscripts/archive_preflight.pyは3.8TBを固定の既定値としていた。修正後はpolicies/limits.jsonから**4TB保存枠と200GB安全空き**を読み込み、古い3.8TBケースも明示的な値で再試験可能。読み取り専用で、ハッシュが確認できない既存ファイルを再利用済みと扱わない。これはソフトウェア動作の修正であり、重み取得や削除ではない。

## 6. H/T/D/C/Uと変数表

| 記号 | 意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| C | 長期保存の計画上限 | byte | 4,000,000,000,000、非負整数スカラー・実機未測定 |
| F | 実機で最低限維持する空き | byte | 200,000,000,000、非負整数スカラー |
| R_i | 第i資産の全repo公開サイズ | byte | 観測値は非負整数、未確認はnull |
| S_i | 第i資産の全選択ファイル容量 | byte | 固定SHAの原本・依存込み、未確認はnull |
| D | 同一SHAで既存ファイル再利用を実証した容量 | byte | ローカルの完全ハッシュ一致が必要。未測定はnull |
| N | 有効候補の件数 | 1 | 105、正整数スカラー |

**H**：同じ学習済み状態の精度違いを整理すれば、特殊な学習成果を削らず保全容量を効率化できる。**T**：まず22件のsource容量未知候補と8件の大規模repoの全ファイル一覧・immutable revision・ライセンスを特定し、実機HDDの空き・既存重み・stagingを読み取り専用で測定。推論を検証する場合はHW、クロック、GPU/RAM、OS、backend/ABI、quant/zero-point、context/batch、KV/encoder/VAEを記録。**D**：完全ファイルと親依存、権利、実機資源、タスク別品質が満たされれば取得審査PASS。未知はUNCERTAIN、容量超過・利用条件不適合はFAIL。**C**：全repoを選択byteと混同、単純量子化を別の訓練状態と認識、親LoRAを二重取得、推論RAMと保存HDDを混同。**U**：未確定source22件、selected byte103件、実機空き、測定条件が主要な不確かさ。合成標準不確かさu_c、包含係数kは未算定。**単位確認**：C/F/R_i/S_i/Dはbyte、Nは無次元。ディスクと推論メモリは同単位でも別の量。

## 7. ERROR CHECKと分野横断

R34は150資産一意、105有効、83/22の全repoサイズ確認数、8件の高容量、R21の親ファイル分を再集計した。Nanbeigeを削らず、4TB枠、空のapproved queueを維持し、重みは取得しない。デジタル保存・OSストレージ・機械学習（後学習）・ソフトウェア供給網/権利の4分野で再利用できる。

### 〈次に考える問い〉

22件の未確定容量から先に調べるべきものは、実行上の依存が重いLTX特殊版、独自音声モデル、再収集困難な学習データのどれか。
