**R39更新（2026-11-08）**：Mistral Small4・GPT-OSS120B・FLUX.2-devの7実行形式について、重み全シャード＋必要な設定/Tokenizer/許諾ファイルの**選択byteと固定revision**を作成。[R39詳細報告](38-r39-backend-specific-selection.md)／[R39非実行マニフェスト](../../manifests/drafts/r39-backend-specific-large-sources.candidate.json)。本R38の全repo・参考差額の表は歴史的な容量比較であり、取得承認や物理的な空き領域ではない。

# R38｜大型8資産の形式別・訓練工程別容量（2026-11-08）

現行v19の有効資産で配布元全体が100GB以上の8件を、**各リポジトリの固定40桁コミットと全ファイル容量**で確認した。[機械可読の全ファイル台帳](../../catalog/research/2026-11-08-r38-large-asset-alternative-layouts.json)。合計1,403,226,367,788 byteは全repo容量であり、選択モデルの実必要容量ではない。4TBを使えるという指示と、現行の150資産・105有効・Nanbeige SELECTを維持する。取得承認0。

## 1. 配布元8件

| 正規repoと固定リビジョン | 状態 | 全repo（byte） | Gated |
|---|---|---:|---|
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next/tree/a7fbcb5c0e12d62a448eaa0e260346bf5dcc0feb) | select | 159,376,351,965 | なし |
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/tree/a11f36bebf709121056b1dbcc943d1c6afbe494d) | select | 241,889,510,745 | なし |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a) | select | 195,764,040,609 | なし |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/26afe3a78bb242c0a8bb181dcc8937bb16e5c66c) | conditional | 177,640,374,395 | auto |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E/tree/14d516bdff6ac06cec40678529222f193386189c) | conditional | 217,315,708,790 | manual |
| [IFM/SFT-Reasoning](https://huggingface.co/datasets/IFM/SFT-Reasoning/tree/4d4dbbe65e478a2ca179c4cce43b5e1f051aacd2) | conditional | 158,563,572,761 | なし |
| [EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B/tree/1ec3a7ee2355e384149df2e4dd42fed41e7fd08f) | conditional | 141,116,879,850 | auto |
| [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2/tree/81402b751b451b5fe4f4c29e8b40f92892f1e440) | conditional | 111,559,928,673 | なし |

## 2. 実際に重複が大きいモデル形式

**Mistral Small 4 119B** は同じ公開モデルに native/consolidated 7シャードとHF 3シャードが同居する。Native側 **120,927,211,096 byte**、HF側 **120,922,973,936 byte**。モデルの訓練状態が2つとは主張しない。ただしテンソル値がビット同一とまでは確認していない。実際、[SGLangの2026-03修正](https://github.com/sgl-project/sglang/pull/21620)ではNativeのconfigとHFの重み名を混ぜてロードに失敗している。**どのバックエンドを残すかを先に決め、必要な形式を一つ選ぶ**。

**GPT-OSS 120B** は3つの実行形式がある。HF/Transformers・vLLM用ルート15シャード **65,248,893,184 byte**、公式PyTorch/Triton用`original/`の7シャード **65,248,869,800 byte**、Apple Metal用`metal/model.bin` **65,238,253,568 byte**。3種の別学習モデルではない。公式モデルはMXFP4を組み込んだ後学習済み公開重みである。[公式実装](https://github.com/openai/gpt-oss)はバックエンドごとに元形式を使い分ける。再構築を優先するならoriginal、一般実行を優先するならHFなど、実機と保存目的で一つを優先し、3形式一括取得を既定にしない。

**FLUX.2-dev** はrootの単一Transformer **64,446,596,128 byte**とDiffusersの7分割Transformer **64,446,603,128 byte**が同じモデルの別ロード形式として同居する。加えて、必要なText Encoder10シャード **48,022,800,560 byte**とVAE **336,213,556 byte**がある。Diffusers方式の3部分合計は**112,805,617,244 byte**（実行コード・cache除外）。Transformerの単一版と分割版を両方無理由に保存しない一方、Encoder/VAEは独立の必要学習コンポーネント。**Gated=autoで公開APIのLFS SHAはマスク**され、取得権限とハッシュ・使用許諾を確認するまでロック禁止。

### 2-A. 3資産での「全repo取得」対「1実行形式」の差額（実回収ではない）

| 資産 | 全repo容量 | 1形式の候補重み | 形式を重複計上しない場合の参考差額 |
|---|---:|---:|---:|
| Mistral Small 4 | 241,889,510,745 byte | HF 3 shard：120,922,973,936 byte | 120,966,536,809 byte |
| GPT-OSS 120B | 195,764,040,609 byte | HF 15 shard：65,248,893,184 byte | 130,515,147,425 byte |
| FLUX.2-dev | 177,640,374,395 byte | Diffusers 7DiT＋10Encoder＋VAE：112,805,617,244 byte | 64,834,757,151 byte |
| **合計** | | | **316,316,441,385 byte（約316.32GB）** |

この差額は**実ディスクで節約・回収済みの容量ではない**。全repoを丸ごとミラーする仮計画と、各1形式の重みを選ぶ仮計画の差であり、必要なコード、config、tokenizer、staging、実行再現性や複数backendの必要性は未判定。Mistral Native/HF、GPT原本/HF/Metal、FLUX単一file/Diffusersは**同一ビット列と実測で立証されたわけではなく**、実行環境ごとに正当な併存理由がある場合は再審査する。独自の後学習モデルや訓練用データセットを整理対象に含めない。

## 3. 重複ではない高容量資産とデータセット

- **Qwen3-Coder-Next**：40個の重みシャード合計159,358,031,480byte。40個の別モデルではなく、一つの学習済み80B級コードモデル。除外しない。
- **Llama 4 Scout**：50個のシャード、217,283,738,720byte。Meta系独立学習済みMoE。Gated=manualなので許諾・ファイルSHA未確定。
- **Meditron3-70B**：30個のシャード、141,107,497,872byte。独立した医療追加学習重みであり、汎用Llamaの単なる量子化ではない。Gated=autoでアクセス未確認。
- **IFM/SFT-Reasoning**：事前学習・3effortsデータ115,169,801,862byte、Instruction-Following 43,393,764,554byte。内容/学習工程が違うため、容量を節約するという理由だけで片方を重複扱いしない。
- **Granary-v2**：英語のコーパス別教師ラベル74,381,590,133byte、その他言語＋サポート37,178,338,540byte、うち日本語subdir 6,182,173byte。JSONLなどのラベル群を保存しても、外部参照の音声原本まで取得済みとは言えない。各コーパスの利用許諾・著作権を分離する。

## 4. 研究方針

既存のSELECT/CONDITIONALは残す。最初に**独立の学習済み重みか、専門SFTか、訓練工程別データか**を判定し、そのあとに必要backend・quant・精度・変換レイアウトを選ぶ。HF版とNative版は技術要件によって両方に価値がある可能性もあるため、機械的な禁止はしない。ただし二重取得するには将来の復元・性能保持・ABI互換の具体的理由が必要。作者提示・公開メタデータの全ファイルSHAはローカル実ファイルの完全検証ではない。

## 5. H/T/D/C/U・変数表

| 記号 | 日本語の意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| B_repo | 配布元全体のファイル容量 | byte | 固定commitでのファイルサイズ総和、非負整数スカラー |
| B_fmt | 特定実行形式の重み容量 | byte | その形式で必要な分割ファイルの和、非負整数スカラー |
| B_dep | 必須別学習コンポーネント容量 | byte | EncoderやVAE等。未確認はnull、非負整数または欠損 |
| N_shard | 重みファイルの分割数 | 1 | 非負整数スカラー。モデル種類数ではない |
| R_peak | 推論時RAMピーク | byte | OS・engine・KV・encoderを含む、未測定はnull |

**H**：同じ公開モデルの多形式ファイルは無条件の能力増分でない。一方、異なる専門学習や学習データは独自保存価値を持つ。**T**：8件の固定APIリビジョンと分割ファイルbyte/メタデータSHAを監査。採用時はHW/clock/precision/quant・zero-point/backend ABI/context/batchを固定し、最低30の対応評価タスクを検証。**D**：実機で互換性・品質・法的許諾・200GB安全空き・<512GB推論RAMを満たした場合のみ最終取得審査PASS。未知はUNCERTAIN、規約不適合や物理的超過はFAIL。**C**：形式変換のテンソル差、Gatedハッシュ、Tokenizer/Encoder欠落、データの権利混在。**U**：実機未測定と推論バックエンド未固定が主要誤差源。合成標準不確かさu_cと包含係数kは未算定。**単位検査**：B_repo/B_fmt/B_dep/R_peakはbyte、N_shardは無次元。ディスクとRAMを同じ制約として扱わない。

## 6. ERROR CHECK・学際性・問い

8件の配布元総量1,403,226,367,788byte、各固定SHA、Mistral7+3、GPT15+7+Metal、FLUX Diffusers7とText Encoder10、Scout50、Meditron30、IFM二系統データ、Granary各言語フォルダを静的検証する。**現行150資産・105有効・4TB計画・承認0・本体DL0**を保持。適用は計算機アーキテクチャ、推論エンジンABI、生成画像/音声、学習データ法務、長期デジタル保存。

**〈次に考える問い〉**：学習済み重みが同一系統なら、将来性のある元重み形式と、現在確実に動く実用形式のどちらを第一保存形式として選ぶべきか。
