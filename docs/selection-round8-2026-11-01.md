# 第8回：5モデルを固定版・ファイル単位の選別へ進める

確認日：2026-11-01。新しいモデル名は追加せず、第7回候補のうち5件について公開メタデータを調査した。これは取得前の構成案であり、重み・実行環境のダウンロードやGated同意は行っていない。

## 1. 今回できたこと

各モデルの現在のmodel-infoで完全な40桁コミットを取得し、その不変コミットのtree APIでファイル名・整数バイト数・Git識別子・公開されたLFS SHA-256を再照合した。公開4モデルのconfig.jsonはテキストとして読んだ。コードのimportやモデル実行はしていない。

[5モデルの固定ファイル構成案](../catalog/acquisition-drafts/round8-pinned-files-2026-11-01.json)には、43ファイルの選択一覧と、選ばなかった25ファイルを記録した。マニフェスト本体が未完成なので、最終lock専用の`manifests/`には入れていない。

## 2. 正確なモデル側ファイル容量

| モデル | ファイル数 | 選択したバイト数 | 十進GB | 状態 |
| --- | ---: | ---: | ---: | --- |
| [DINOv3 ViT-S](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m) | 6 | 86,431,253 | 0.086431 | 手動Gated・取得保留 |
| [Depth Anything V2 Small](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) | 5 | 99,181,304 | 0.099181 | 公開・実行構成の確認待ち |
| [SAM2 Hiera Tiny](https://huggingface.co/facebook/sam2-hiera-tiny) | 8 | 155,874,070 | 0.155874 | 公開・Transformers経路を選択 |
| [Qwen3Guard Gen 0.6B](https://huggingface.co/Qwen/Qwen3Guard-Gen-0.6B) | 10 | 1,519,204,911 | 1.519205 | 公開・Tokenizerを含めて選択 |
| [SmolVLM2 500M Video](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 14 | 2,034,857,549 | 2.034858 | 公開・Safetensors経路を選択 |
| **合計** | **43** | **3,895,549,087** | **3.895549** | **取得未承認** |

選択は本体重みだけでなく、README、設定、必要なTokenizer/Processor等の同一repo内ファイルを含む。依存ライブラリ・OS・ドライバー・実行用wheel・追加のライセンス資料はまだ含んでいない。**これはモデル側ファイル容量であり、完全なオフライン再実行環境の総量ではない。**

単位チェック：バイト数はtree APIの論理ファイルサイズを合算した。GBは十進、GiB換算値やLFS pointerのバイト数は混ぜていない。`usedStorage`も現在の固定snapshot容量と同一視しない。

## 3. 圧縮せず、不要な配布形式を選ばない

固定5リポジトリの全ファイルをパスごとに合算すると9,934,247,320バイト。今回の選別で6,038,698,233バイト、約60.8%を対象から外す案とした。

- **SAM2**：155,906,050バイトの`sam2_hiera_tiny.pt`を別ランタイム用の配布物として除外し、Transformersの`model.safetensors`を選ぶ。ネイティブSAM2のYAMLは小さな再現資料として残す。両形式のバイト同一性を主張していない。
- **SmolVLM2**：ONNXの24ファイル、計5,882,792,183バイトを今回のTransformers構成から除外する。ONNXでの直接実行も保全したい場合には、その必要な一組を別枠で再審査する。全精度・全量子化版を自動保存しない。
- **Depth、Qwen3Guard、DINOv3**：この構成では対象repo内のファイルを全て列挙した。新しい量子化や重み編集はしていない。

この比較は論理的なパス合計に対するもの。重複ブロックやhardlinkが有効なHDDで同じ実容量削減になるとは限らない。モデル精度を比較していないので、性能が60.8%改善したという意味でもない。

**現行台帳の暫定3.234TBから6.039GBを差し引いてはいけない。今回の5件は未適用の追加案で、旧v2容量に含まれていない。**

## 4. 依存の過大計上・取りこぼしを防ぐ

Depth Anythingの固定configは`backbone=null`かつ`use_pretrained_backbone=false`。DINOv2という構造名が書かれているだけで、別のDINOv2 checkpointを二重に保存する必要があるとは判断しない。ただし、実装のオフライン検証までは依存閉包を確定しない。

SAM2は`Sam2VideoModel`で、視覚backbone・マスク・メモリ構成がconfig内にある。`video_preprocessor_config.json`を落とさない。

SmolVLM2は文字と視覚のsub-configを持つ。上位configおよび公開safetensorsメタデータはF32を示す一方、内側のtext_configにはBF16の記述がある。内側の記述だけで保存容量を半分に見積もらない。

Qwen3GuardはBF16。一般Qwen用のテンプレートを推測で代用せず、この固定版の`tokenizer_config.json`を残す。

`config.transformers_version`は保存時の履歴情報であり、今回動作確認したライブラリ版ではない。SAM2の4.56.0.dev0、SmolVLM2の4.47.1、Qwenの4.51.1をそのまま実行環境の最終指定にしていない。

## 5. 権利・ハッシュ・実行条件

DINOv3は公開メタデータ上でmanual gated。固定treeのLFSハッシュが伏せられていたため、checkpointの`source_sha256`はnullのままにした。利用者による正規申請や規約同意は代行せず、制限付きファイル本文も要求していない。

公開4モデルの主重み4ファイルとQwenのTokenizer1ファイルは、固定treeでLFS SHA-256を確認した。その他の小さなGitファイルにはGit blob IDを記録し、SHA-256と混同していない。**重みを取得していないため、ローカル実物とのハッシュ照合はまだゼロ。**

Depth、SAM2、SmolVLM2の今回の固定repoには独立したLICENSEファイルがない。モデルカードのApache-2.0表示は確認できても、適用する全文・NOTICEや利用条件の確認は別途必要。QwenのLICENSEとDINOv3のLICENSE.mdは取得案に列挙したが、適法性確認の完了フラグは上げていない。

共通の実行候補はTransformers + PyTorch。実際のbackend版、Python ABI、OS、CPU/GPU、driver、wheelのハッシュ、動画フレーム数、文脈長、バッチ、RAMは未確定。ネット遮断下の動作・速度・精度テストも未実施。今の情報だけで『実機で動く』『コスパが最高』とは言わない。

## 6. 継続保留

OmniParserは複数revisionとコンポーネント別ライセンス、NLLBは非商用条件とbin形式・runtime、Watermark AnythingはMIT版と旧版のファイル対応の調査が残る。今回の容量に含めず、保留を解除していない。

次に確定させるのは、公開4モデルの共通runtime一式と適用許諾。DINOv3はそれとは別の利用承認待ちとして扱う。未知の依存容量を0として埋めない。

## 7. H / T / D / C / U

| 区分 | 判定内容 |
| --- | --- |
| H | 対象backendを絞り同一repo内の代替形式を選別すれば、重みを再量子化せず保存容量を減らせる |
| T | 5件を完全commitに固定し、treeの全68ファイルを選択43・除外25へ分割。サイズ・ハッシュ型・パス・重複と合計を検査する |
| D | メタデータ整合はPASS。取得承認はBLOCKED。完全依存・許諾・実機適合性はUNCERTAIN |
| C | ONNX実行も必要、外部依存が不足、旧形式に研究上固有の価値がある場合は除外判断を見直す |
| U | 固定版の論理バイト数は整数として確認。ただし実保存量、runtime容量、法的許諾、性能・ピークRAMは未確定。統計的な合成不確かさや包含係数は未定義 |

## ERROR CHECK

ローカル検査16項目を通過。GitHubに再取得したファイルのblob SHA-1は、検証済みローカルJSONから計算した`bb445615c200f32862bcbe8c014f4ae3e08b0848`と一致した。これはレビューJSONの一致であって、モデル重みの安全性・性能証明ではない。

正式台帳110件・有効94件、暫定3,234,067,678,260バイト、取得承認キュー空を維持。`manifests/`に最終lockは作成せず、モデル本体取得・実行・インストール・HDD操作は行っていない。
