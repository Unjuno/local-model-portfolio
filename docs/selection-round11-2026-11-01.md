# 第11回選定：OmniParserのMIT部品とNLLB研究用原本を固定する

**調査日：2026-11-01。** 第7回で保留していた2モデルについて、Hugging Faceの公式配布データを直接照合し、コミット・ファイル一覧・整数バイト数・公開LFS SHA-256を記録した。**モデル本体を取得・実行・Gated同意したものではない。** [メタデータ全件](../catalog/acquisition-drafts/round11-omniparser-nllb-files-2026-11-01.json)。

## 1. 固定ファイルと容量

| モデル | 固定版（40桁） | 選択ファイル | 選択容量（十進） | 配布物から除いた量 |
| --- | --- | ---: | ---: | ---: |
| [OmniParser v2](https://huggingface.co/microsoft/OmniParser-v2.0) | `f55d0750e5b94db2125ef0b45b0fa4a85ddc59b4` | 9 | 1,365,117,340 B | 40,682,851 B |
| [NLLB-200 Distilled 600M](https://huggingface.co/facebook/nllb-200-distilled-600M) | `f8d333a098d19b4fd9a8b18f94170487ad3f821d` | 9 | 2,482,655,255 B | 0 B |
| **合計** | — | **18** | **3,847,772,595 B（約3.847773GB）** | **40,682,851 B** |

これは**固定リポジトリ内の選択ファイル**の整数バイト数。実行器、Python、FFmpeg、encoder、追加のライセンス資料や実機キャッシュ容量は含まない。すでに選定した第8回の5モデルに加えると、**第7回の7モデルすべて**についてモデル側選択案が存在するが、最終承認済みマニフェストという意味ではない。

## 2. OmniParserは同一コミット内でMIT版を選べる

前回の第7回ではGitHub READMEの古い案内を使い、`icon_detect_v3`がHF PR #37にしか存在しないと扱っていた。しかし今回固定したHFコミットでは、`icon_detect_v3/model.pt`と`icon_detect_v3/LICENSE`が**同じmain版に存在する**。配布物を2つのrevisionから合成する必要はなくなった。

[固定版のモデルカード](https://huggingface.co/microsoft/OmniParser-v2.0/blob/f55d0750e5b94db2125ef0b45b0fa4a85ddc59b4/README.md)は、旧`icon_detect`のYOLOv8派生重みは**AGPL-3.0**、`icon_detect_v3`のYOLOv9-E派生重みと`icon_caption`はそれぞれ**MIT**と明記する。2つのMIT版専用LICENSE本文も今回実際に確認した。単にHF上部のLicense: MITタグだけを信頼していない。

### OmniParserに選んだファイル

| 用途 | 対象 | 取得前チェック |
| --- | --- | --- |
| 検出器 | `icon_detect_v3/model.pt` | 281,182,680 B。公式はTorchScriptと説明。未知の`.pt`を安全確認なしにtorch.jit.loadしない |
| アイコン説明 | `icon_caption/model.safetensors` | 1,083,916,964 B。Florence-2系のモデル。元のbase-ftと重みを二重取得しないが、必要コードの対応を確認 |
| 許諾 | 両サブフォルダの`LICENSE` | Microsoft MIT本文。旧AGPLファイルを同一条件とみなさない |
| 設定・証跡 | caption config/generation config・README・requirements.txt・.gitattributes | 元のモデル設定と宣言を保持、実行手順を勝手に実行しない |

除外対象は旧AGPLの`icon_detect/*`（`.pt` 40,623,819 Bなど）と`handler.py`、空のroot `config.json`。**AGPLだから保有不能という主張ではない。** 今回の目標が利用条件を混在させない小型のMIT構成であるため除外した。

**さらに実行上の落とし穴**：[固定caption設定](https://huggingface.co/microsoft/OmniParser-v2.0/blob/f55d0750e5b94db2125ef0b45b0fa4a85ddc59b4/icon_caption/config.json)は`auto_map`に`microsoft/Florence-2-base-ft`の外部カスタムコードを参照する。Transformers 5.22.1にはFlorence2の**ネイティブモデルコードが存在する**が、今回の微調整済み重みが`trust_remote_code=False`で互換ロードできるかは未試験。`microsoft/Florence-2-base-ft`の元重み463MBを自動で依存として加えることはしない。

**ライセンスと依存の違い**：OmniParser root `requirements.txt`には`ultralytics==8.3.70`も記載されている。しかし作者は新MIT detectorのTorchScript推論にはUltralytics不要と説明する。root requirementsをそのまま全導入すればAGPL依存を含むため、**実際に使用するコードパス単位で必要物を選ぶ**。この点が未解決なので、取得承認は保留。

## 3. NLLBは低資源言語研究原本として容量を固定

Metaの[固定モデルカード](https://huggingface.co/facebook/nllb-200-distilled-600M/blob/f8d333a098d19b4fd9a8b18f94170487ad3f821d/README.md)は**CC BY-NC 4.0**、研究用・文単位翻訳を意図し、本番配備向けではなく、学習時の入力長512 tokens超の性能低下可能性を説明する。これをクラウド翻訳代替の商用製品として推奨しない。

全9ファイル、**2,482,655,255 B**を登録。特に`pytorch_model.bin`（2,460,457,927 B）はPyTorchバイナリであり、`model.safetensors`として置換できない。配布元の完全SHA-256を記録したが、ファイルを取得した実測SHAではない。Tokenizer JSON・SentencePieceモデル・特別トークンも保存案から外さない。

実装参照として、[Transformers 5.22.1のm2m_100実装](https://github.com/huggingface/transformers/tree/446a570e62b04a89ea001604ada7366baac2ea67/src/transformers/models/m2m_100)と[nllb Tokenizer](https://github.com/huggingface/transformers/blob/446a570e62b04a89ea001604ada7366baac2ea67/src/transformers/models/nllb/tokenization_nllb.py)の存在を確認した。**存在確認はモデルロード・翻訳品質の検証ではない**。安全でない旧pickleの自動ロードは禁止。

研究保存価値は、200言語対応の蒸留学習済み翻訳を、比較ベースラインとして残すこと。現行の大型同時翻訳モデルを全機能で置き換えた、という評価は行わない。将来の政府配布停止予定は未確認。

## 4. Watermark Anythingは保留を解除しない

[公式GitHub README](https://github.com/facebookresearch/watermark-anything)は新しい**MIT SA-1B版を`wam_mit.pth`**、元論文の**CC BY-NC COCO版を`wam_coco.pth`**と別名で紹介している。一方、[HFの現在の固定版](https://huggingface.co/facebook/watermark-anything/tree/88ffb2cd1079a76b01d6beda8bf2a433c25fa881)は`checkpoint.pth`しか提供せず、カード内にはHF上に存在しない`wam_mit.pth`のロード例もある。HF checkpointのSHA-256自体は取得したが、公式の`wam_mit.pth`との一致は検証できない。**HFがMITと表示するだけで、この特定のcheckpointをMIT SA-1B原本と断定しない**。

## 5. 次段階と停止条件

今回確定したのは**2つの公式コミット、18ファイルの構成、上流サイズ、5ファイルの公開LFS SHA-256**。適用する許諾の本文・オフライン依存・実行時セキュリティを全て承認したわけではない。独立ソフトウェアへの依存bytesやCPU/GPU/OSはnullのまま。`catalog/CURRENT.json`、`queues/approved.json`、`manifests/`は変更しない。

## H/T/D/C/U

| 区分 | 手順 |
| --- | --- |
| H | 同じリポジトリ内の利用条件が異なる重みをファイル単位で選別すれば、容量と法的条件を制御できる |
| T | メタデータ：固定2コミットのツリーから18ファイルを選択し、同じツリーの他ファイルとの重複・サイズと公開ハッシュ形式を照合。実測は、別途承認後、オフライン隔離環境で各モデル最低3入力と既存競合モデルの同一タスクを比較する。権利・依存が未解決なら停止 |
| D | PASS＝固定版のメタデータ/サイズ・ライセンス表示の根拠が成立。BLOCKED＝許諾不明・危険な重みのロード・取得未承認。性能・安全性・完全再現性はUNCERTAIN |
| C | 作者のMIT新検出器が旧AGPL版と精度やAPI互換性が異なる、root requirementsが不要なAGPLコードを含む、NLLBの非商用・本番利用制限が用途と衝突する |
| U | モデルの真の機能差、旧コード移植、依存・実行メモリ・完全な知識資材量は未測定。確率モデルがないため合成標準不確かさと包含係数の数値は算定しない |

## ERROR CHECK

固定モデル側のファイル・Git blob SHA-1・LFS SHA-256を別フィールドとして記録した。`pytorch_model.bin`とTorchScriptは**保存対象データとしての審査のみ**で、実行していない。第7回の残る2件を加えても正式なダウンロードは0件。