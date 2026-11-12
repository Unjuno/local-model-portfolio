# R49｜BotPsyとGranite TTM R3の固定公開ソース・署名・ライセンス監査

> 2026年11月12日。専用ブランチ `strategy/2026-11-03-01-risk`、基準コミット `394ca677ec6755ac0ab39f98786ff7114df9f440`。**現行v29の177資産／有効130件、取得承認0、4TB上限、200GB最低空き、旧モデル採否を変更しない。** 2つの固定モデルrepoの全ファイル情報を元配布元で照合。ウェイト本体取得、ファイル実体hash計算、モデル実行、外部ライセンス同意は行っていない。

## 1.〈本論〉2件のファイル実体スコープ

| 確認対象 | 不変のHFモデルrevision（40桁） | 公開テンソル数（総数） | 現行source全ファイル | 主重み | 元repoに含まれるLICENSE |
| --- | --- | ---: | ---: | ---: | --- |
| [qvac/BotPsy-0.8B](https://huggingface.co/qvac/BotPsy-0.8B) | `24561e9681643eaf807fc28b0875210cb17f89c1` | **852,985,920** | **11ファイル、1,726,201,481 B** | 1,706,030,528 B | あり、Apache-2.0 |
| [ibm-granite/granite-timeseries-ttm-r3](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | `ea17cfd2e3edcaea21eb8dcecd18bf88971482fa` | **1,414,514** | **6ファイル、6,126,375 B** | 5,729,424 B | **なし**。カードのApache-2.0タグのみ確認 |
| **合計** | 2repo | — | **17ファイル、1,732,327,856 B** | 1,711,759,952 B | 権利・復元全体は別審査 |

公開元の各ファイルのソースSHAは[JSON台帳](../../catalog/research/2026-11-12-r49-botpsy-ttm-immutable-census.json)にある。**LFS SHA256は4件、Git blob SHA1は13件**であり、後者は原本のbyte列そのもののSHA256でない。LFS SHAも取得後に自分のHDDでhashした結果ではない。取得可能とみなすかは別。機械的には17件の一意性、32bitを含む各byteの整数、正規のhash長、合計を照合。

**出典**：[BotPsy不変HF全ツリー](https://huggingface.co/api/models/qvac/BotPsy-0.8B/tree/24561e9681643eaf807fc28b0875210cb17f89c1?recursive=true)、[TTM不変HF全ツリー](https://huggingface.co/api/models/ibm-granite/granite-timeseries-ttm-r3/tree/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa?recursive=true)。エビデンスはこれらの公開元APIからの**ファイル名・サイズ・提供元SHA**であり、ファイルの実体はコピーしていない。

### 1.1 BotPsyに関する修正と独自性

開発元カードは既存のQwen3.5-0.8Bを元にSFT、多教師蒸留、RLを独立実施したと記録。BF16の`model.safetensors`だけでなく、**`tokenizer.json`=19,989,325 B、`chat_template.jinja`=7,791 B、`ATTRIBUTIONS.md`=120,449 B、`LICENSE`=11,357 B**を含む11ファイルを一括固定した。BotPsyと元のQwen3.5-0.8Bの同名tokenizerの公開SHA256は一致しない。親モデルが既選定だからという理由でtokenizerの実バイト容量を差し引かない。

開発元[固定モデルカード](https://huggingface.co/qvac/BotPsy-0.8B/raw/24561e9681643eaf807fc28b0875210cb17f89c1/README.md)は公式vLLM/BF16共同ハーネスでBFCL v4=44.0対親23.4（3run）、ACEBench=58.7対30.1（2run）と報告。一方、BrowseComp-Plus=4.5と極めて低い絶対スコア、英語推奨、高リスク用途に不向きを明記。**メーカーの同条件とユーザー実機・日本語・安全性は違う**。モデルconfigは`Qwen3_5ForConditionalGeneration`と表記するが、作者カードの使用はtext-onlyであり、視覚・動画タスクへの効果を推測しない。config中Transformers 5.8.1は**モデル書出し時の宣言**で、ユーザー実機のABI互換試験結果ではない。

### 1.2 TTM R3に関する修正と供給網署名

TTM-R3のこの原本`model.safetensors`は**F32の1,414,514テンソル要素**。固定`config.json`の主要値は**context_length=512、prediction_length=30、9分位点、Student-t出力、trend/residual分解**。R3モデル群にある1M–35Mの全枝が1,414,514パラメータという意味ではなく、別の長さ/horizonを必要とする場合は別checkpointを調査する。

公開API `usedStorage=1,475,868,508 B`は**この固定repoの現行6ファイル合計6,126,375 Bと異なる**。履歴等を含む集計可能性はあるが、原因を確定していないため旧配布版への説明を作らない。**保存必要量としては固定スナップショットの6,126,375 Bを使い、usedStorageから差し引かない**。

固定版に`model.sig`=8,912 Bの**Sigstore署名bundle**が存在。IBMの[署名検証手順](https://www.ibm.com/granite/docs/model-standards/signature-verification)は所定の署名ツールと発行者検証を示す。しかし現実にツールを実行した署名PASSではない。モデルrepo内にはLICENSEファイルがなく、**HFのメタデータ/カードはApache-2.0表記に留まる**。既存のIBMソースコードは別GitHubリポジトリで、観測HEAD `31fa2f01573341f17e9997280f61481de18ce28c`。最新公開Pythonパッケージ0.3.12（2026-10-29）は互換候補であるが、このF32 checkpointの実機ロードとABI一致は未確認。

IBMのGIFT-Eval MASE/CRPSとCPU/GPU throughputは**R3系列の開発元数値**で、今回の1.414M・512→30固定モデル自身と断定しない。メーカーのHW/クロック/バッチが欠測しているため計測値の無根拠な比較をしない。

## 2. 非実行保存マニフェストと段階別停止

[研究用ファイル別マニフェスト](../../manifests/drafts/r49-two-compact-immutable.candidate.json)は、17ファイルのパス、元revision、出典SHAとbyteを保持。ただし`executable=false`、`download_authorized=false`、`approved_manifest=false`、物理HDD未確認。署名bundle含むファイル構成の確定と**最終取得指示**は別物である。

- **P0**：IBMカードによるApache表示と現行LICENSEファイル欠落の法的出典を記録し、QvacはLICENSE+ATTRIBUTIONSを維持する。
- **P1**：IBMの`model.sig`署名主体・対象範囲を、入手と実行が別途承認された環境で検証する。元LFS SHAを現物のhashと比較しない段階では未検証。
- **P2**：BotPsyの固有tool call/chat templateとLLM runtime、TTM R3の`granite-tsfm`版・model family branch selection・ABIを固定し、両者の正確な増分容量を計測する。
- **P3**：日本語ツール操作の厳密な比較と時系列Chronos-2比較は、実機取得・モデル実行を別途承認した後に実施。

## 3. 容量、変数表、次元検査

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・型・前提 |
| --- | --- | --- | --- |
| `B_B` | BotPsyの現在の全公開ツリー | byte | 1,726,201,481。非負整数スカラー、他のruntime依存を含まない |
| `B_T` | TTM R3の現在の全公開ツリー | byte | 6,126,375。非負整数スカラー、独立コードの保存を含まない |
| `B_all` | 新2資産の同一ファイルを仮定しない合計 | byte | 1,732,327,856。非負整数スカラー |
| `B_res` | v28採用時の容量予約上限 | byte | 2,700,000,000。非負整数スカラー。実ファイル容量ではない |
| `U` | 上記予約枠と全ツリーの差 | byte | 967,672,144。符号付き整数スカラー。実HDD空きではない |
| `C` | 計画上限 | byte | 4,000,000,000,000。非負整数スカラー。実機未測定 |
| `F` | 独立した実空き床 | byte | 200,000,000,000。非負整数スカラー |

**単位検査**：全数値は情報量のbyte。F/Cは利用できる実機容量と計画容量で異なる対象であり、`U`が正でも実機保存可能とは断定できない。4TBソース予算、実ファイルの既保存hash、staging/キャッシュ、外部学習済み部品が別に必要。

## 4. H/T/D/C/UとERROR CHECK

H：研究専用固定版で17ファイルの提供元IDが分かれば、同じモデルの量子化別コピーに頼らず復元準備を進められる。T：公開元の不変ツリー11+6で静的なパス/byte/hash検査。別途取得許可の後、最低30回の同一HW/OS/backend/context/batchにおける品質・速度を検証。D：**固定版のメタデータ照合PASS**、物理実体の署名/全依存/ユーザー承認はUNCERTAIN。不正許諾/偽hash/ABI失敗はFAIL。C：元コード互換性欠落、実HDD容量不足、モデル親とtokenizerの差分無視。U：実バイト再ハッシュと署名検証・外部runtime・ライセンス本文が未実施。合成標準不確かさ`u_c`・包含係数`k`は推計しない。

**ERROR CHECK（静的）**：2repo・17一意ファイル・公開LFS SHA256行4・Git blob SHA1行13、公開元全ツリーbyte合計1,732,327,856を再計算。v29=177件/有効130件、既存6 EXCLUDED、approved 0件は改変しない。GitHub Actions、署名の実体検証、Python推論、ダウンロードは未実施。

**応用分野**：エージェントLLM・ツール契約、統計/時系列予測、署名済みソフトウェア供給網、デジタル保存と法的ライセンス管理を横断する。

###〈次に考える問い〉
モデルの全公開ツリーを固定できても、利用権利の証拠、実行ABI、依存ファイル、ユーザーHDDと署名検証のどれが実際の取得許可を最も長く止めるのか。
