# R63｜ACE-Step XL の公式初期化・保存容量追加監査

調査日 2026-11-14。現行 `main` v32、管理182資産／有効135件。基準コミット `beecd66d1243ffe6f21e04348cbdeba55c71b690`。本監査では重みのダウンロード、モデル実行、選定変更を行わない。

## 1.〈本論〉復元上の発見

[公式固定コード](https://github.com/ace-step/ACE-Step-1.5/tree/ca1e85fe9430179831e6bc6be790c332190a3866) の [model_downloader.py](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/acestep/model_downloader.py) は `MAIN_MODEL_COMPONENTS` に通常2B `acestep-v15-turbo`、VAE、Qwen3-Embedding、1.7B LMを含める。[初期化コード](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/acestep/core/generation/handler/init_service_downloads.py) は XL指定でもこの4構成の存在確認を先に実施し、2Bが欠けると`ensure_main_model`を通してダウンロードを試みる。

**重大な制限**：その `snapshot_download` に固定revisionもファイルフィルタも指定されない。自動取得が生じると版の変動と全repo取得の危険がある。R62のXL最小保存案は学習済み原本の保全には意味があるが、公式プログラムを無変更で完全オフライン復元できるという証明ではない。

## 2. 追加2Bの公開元ファイル

[ACE共有元・固定revision](https://huggingface.co/api/models/ACE-Step/Ace-Step1.5/revision/19671f406d603126926c1b7e2adc169acbcade22?blobs=true)の公開サイズとハッシュを使用。

| ファイル | bytes | 既存R62との関係 |
|---|---:|---|
| `acestep-v15-turbo/config.json` | 1,968 | 同一内容：`root/config.json` |
| `acestep-v15-turbo/configuration_acestep_v15.py` | 13,130 | 新規内容 |
| `acestep-v15-turbo/model.safetensors` | 4,787,825,604 | 新規内容 |
| `acestep-v15-turbo/modeling_acestep_v15_turbo.py` | 96,036 | 新規内容 |
| `acestep-v15-turbo/silence_latent.pt` | 3,841,215 | 同一内容：`XL/silence_latent.pt` |

全5ファイル=4,791,777,953byte。R62で計上済みの2ファイル=3,843,183byte。**新しい内容識別子の増分は4,787,934,770byte**。

## 3. 見積りの2ケース

| 用途 | ソース容量の算術値 | 空4TB・200GB空き床の仮定上の差額 |
|---|---:|---:|
| R62：XL独立学習成果の最小保存案 | 3,466,070,232,173 byte | 333,929,767,827 byte |
| R63：通常2Bも含め、公式main存在検査を満たす案 | **3,470,858,166,943 byte** | **329,141,833,057 byte** |

通常2Bを加えてもコードの安全性・実機起動・全Codec・wheelhouse・ライセンス・実HDD空きは未検証。逆に2Bを省くなら公式コードの明示的な変更と別途オフライン試験が必要。いずれも自動実行・取得不可。

## 4. 供給網とABI

[pyproject.toml](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/pyproject.toml)はPython >=3.11,<3.13、Linux x86_64 PyTorch 2.10.0+cu128、Windows 2.7.1+cu128、transformers >=4.51,<4.58、diffusers >=0.37を指定。[uv.lock](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/uv.lock)のGit blobは `87c2442e7a852af1c19da39e0ee2008fb6e17b41`、416101byte。Git treeの1222 blob論理合計19177578byteは、wheelやドライバ、Git packのサイズではない。

## 5. 変数表・単位検証

| 変数 | 意味（日本語） | SI単位 | 定義／範囲・前提 | 型 |
|---|---|---|---|---|
| B | R62のソース算術容量 | byte | 3,466,070,232,173, 外部runtime未計測 | 非負整数スカラー |
| G | 追加通常2Bの5ファイル | byte | 4,791,777,953 | 非負整数スカラー |
| D | 既存SHAで一致する2ファイル | byte | 3,843,183 | 非負整数スカラー |
| A | 追加2Bの重複除去後 | byte | A=G−D=4,787,934,770 | 非負整数スカラー |
| T | R63の参考合計 | byte | T=B+A=3,470,858,166,943 | 非負整数スカラー |
| C | 4TB計画上限 | byte | 4000000000000 | 非負整数スカラー |
| F | 最低物理空き床 | byte | 200000000000（実測なし） | 非負整数スカラー |
| H | 仮想差額 | byte | H=C−F−T=329,141,833,057 | 整数スカラー |

全加減算はbyte同士で次元一致。モデルパラメータ数、VRAM、Git blob SHA-1とLFS SHA256を混同しない。

## 6. H/T/D/C/U・ERROR CHECK

H：最小の重み保存範囲と無変更の公式起動要件は異なる。T：固定コード2箇所・追加5ファイルのSHA/byteを静的照合。D：静的存在ゲートと容量算術PASS、実機復元・完全依存・適法性はUNCERTAIN、無承認自動取得はFAIL。C：暗黙の別モデル、版更新、ABI不整合、残空き不足。U：実HDDとwheelhouseの分布不明でu_c/kを算出できない。

ERROR CHECK：4,791,777,953−3,843,183=4,787,934,770、3,466,070,232,173+4,787,934,770=3,470,858,166,943。取得承認0。

関連領域：機械学習、デジタルアーカイブ、ソフトウェア供給網、知財法務。

## 7.〈次に考える問い〉

学習済みXLの長期保管と、無変更の公式コードによるオフライン起動のどちらに必要な増分容量を先に配分すべきか。
