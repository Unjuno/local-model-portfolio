# R38｜8大型資産のバックエンド別コピー・学習済み原本・データ区分を監査

2026-11-08。**容量先行のモデル削除は禁止**。v19管理150資産・有効105、Nanbeige4.3-33B SELECT、4TB計画を変更せず、全repoが100GBを超える8件について、固定リビジョンの全ファイル群を再分類した。[R38 JSON台帳](../../catalog/research/2026-11-08-r38-large-asset-alternative-layouts.json)。今の判断はダウンロード承認ではなく、同一モデルの重複形式を適切に扱うための研究案。

## 1. 形式を一つ選んだときの容量差（実回収ではない）

| モデル | 全repo byte | 代表する重み一式 byte | 形式を重複保存しない場合の参考差額 byte |
|---|---:|---:|---:|
| [Mistral Small 4](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 241,889,510,745 | HF形式3 shard：120,922,973,936 | 120,966,536,809 |
| [GPT-OSS 120B](https://huggingface.co/openai/gpt-oss-120b) | 195,764,040,609 | HF形式15 shard：65,248,893,184 | 130,515,147,425 |
| [FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | 177,640,374,395 | Diffusers DiT＋text encoder＋VAE：112,805,617,244 | 64,834,757,151 |
| **3件の参考合計** | | | **316,316,441,385 byte（約316.32GB）** |

**参考差額は実機で空きが増えた数字ではない**。全repoを丸ごと保存する非推奨案と、指定した重み形式だけの仮案を比較した差額。config、tokenizer、コード、依存・staging、別実行環境用の正当な保存需要は別途確認する。また単一形式への変換による品質・精度・将来の再構築可能性を証明していない。

## 2. 全8資産の分類と採否ゲート

| 正規repo | 現状の固有性と固定ファイルの内訳 | 取得前のゲート |
|---|---|---|
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next/tree/a7fbcb5c0e12d62a448eaa0e260346bf5dcc0feb) | 学習済みコードモデル。40 shardが**一つの重みセット**（159,358,031,480 byte）。一部shardを減らすのは不正。 | 固有原本全shardを1セットとして扱い、実機と権利を検証。 |
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/tree/a11f36bebf709121056b1dbcc943d1c6afbe494d) | Native形式7 shard=120,927,211,096 byte、HF形式3 shard=120,922,973,936 byte。同じ公開モデルだがbitwise等価は未検証。 | 対象ローダーとNative/HFの設定・ABIを確定して形式選択。両形式を勝手に再ダウンロードしない。 |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a) | MXFP4後学習重み。HF15 shard=65,248,893,184 byte、original/7 shard=65,248,869,800 byte、Metalバイナリ=65,238,253,568 byte。 | HFはTransformers/vLLM、originalは公式Torch/Triton、MetalはApple向け。何を再現したいかで形式選択。 |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/26afe3a78bb242c0a8bb181dcc8937bb16e5c66c) | 単一DiT=64,446,596,128 byteとDiffusers DiT7 shard=64,446,603,128 byte、さらにtext encoder10 shard・VAEが別。Gated。 | 非商用Gated利用権と公開ハッシュのマスク解消が必要。単一DiTとDiffusers DiTを二重取得しない。 |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E/tree/14d516bdff6ac06cec40678529222f193386189c) | 別系統MoE原本。50 shard=217,283,738,720 byte。manual Gated。 | Gated受諾がなければロック禁止。重み原本は他モデルの通常量子化ではない。 |
| [IFM/SFT-Reasoning](https://huggingface.co/datasets/IFM/SFT-Reasoning/tree/4d4dbbe65e478a2ca179c4cce43b5e1f051aacd2) | pretrainデータ=115,169,801,862 byteとinstructionデータ=43,393,764,554 byteは異なる学習工程。 | 権利・構成/重複サンプル・研究用途を区別し、データセットをGGUF重複とは扱わない。 |
| [EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B/tree/1ec3a7ee2355e384149df2e4dd42fed41e7fd08f) | 医学特化の別学習済み重み。30 shard=141,107,497,872 byte。auto Gated。 | 医療特化後学習は固有。ライセンス、アクセスと専門品質を先に確認。 |
| [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2/tree/81402b751b451b5fe4f4c29e8b40f92892f1e440) | 言語別ラベル・コーパス。英語=74,381,590,133 byte、日本語dir=6,182,173 byte。音声波形そのものの保存は未証明。 | 各言語と元収録素材の利用条件を確認し、欠けた音声波形を推定で保存済みにしない。 |

## 3. 一次資料に基づく実行上の違い

**Mistral**：[SGLangのPR #21620](https://github.com/sgl-project/sglang/pull/21620)は、`params.json`と`config.json`が併存するためNative/HF重みの識別を誤り起動に失敗した不具合と修正を記録。省容量化はローダー依存を固定して行う。2種類のtensorがビット単位で同一であるとは主張しない。

**GPT-OSS**：[開発元の参照実装](https://github.com/openai/gpt-oss)は元重みoriginal/をTorch/Triton、HFルートをTransformers/vLLMに、Metalの事前コンパイルファイルをApple向けに使う。三つとも学習済みモデルの別後学習とは確認されておらず、用途別の実行表現とする。反面、Metalバイナリや原本形式の再現可能性という独自の技術史的価値は別途評価する。

**FLUX.2-dev**：[公式の実装](https://github.com/black-forest-labs/flux2)は32B画像生成・編集モデルの利用例を公開。root single-file TransformerとDiffusers分割Transformerは同一公開モデルを表すと考えられるが**実テンソル同等性未照合**。コミュニティの重複ロード報告は[こちら](https://huggingface.co/black-forest-labs/FLUX.2-dev/discussions/35)、未再現なので一般的なバグとして確定しない。Gatedのため重みSHAはマスクされている。

**医学・データ**：Meditron3は医療後学習、Scoutは独立MoE、IFMのpretrain/instructionとGranaryの言語別コーパスは別データ。モデル用途が似ていること・ファイル拡張子が同じことだけを根拠に削除しない。

## 4. H/T/D/C/U・変数表・次元

| 記号 | 日本語の意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| B_repo | 配布元の全ファイル容量 | byte | 固定コミットでの全ファイル合計、非負整数スカラー |
| B_rep | 研究用に選んだ一つの重み表現容量 | byte | Mistral HF/GPT HF/FLUX Diffusersセット。設定・コードは別、非負整数スカラー |
| B_avoid | 全repo丸ごと取得を選ばない場合の参考差額 | byte | B_repoとB_repの差、非負整数スカラー。**実回収容量ではない** |
| R_peak | 実機推論RAMピーク | byte | 追加依存・KV・OS込み、未計測はnull |
| N | 比較タスクの試行件数 | 1 | 実行する場合は少なくとも200件/能力軸を暫定目標、正整数スカラー |

**H**：同一学習成果をNative/HF/Metal/分割形式で必要以上に複製せず、訓練状態のユニークさを維持できる。**T**：ソースモデルと変換パス、モデルカード/通知、LFSハッシュを確認した。今後本人が認めた環境でbackend/ABI、GPU/CPU・clock、quant zero-point、batch/context、出力品質/推論ピークを固定し比較。**D**：一つの実行表現で必要な機能と合法・完全な依存が再現できれば形式削減PASS。再現不能・歴史的な重み原本の重要性があれば別形式併存UNCERTAINとして再審査。権利不適合や容量超過でFAIL。**C**：形式変換での値変化、バックエンドの自動判別ミス、Gated許諾不足、異なる学習工程の誤削除。**U**：実機性能・権利全文・変換精度・maskされたSHAの不確かさで合成標準不確かさu_cおよび包含係数kは未評価。**単位チェック**：B_repo/B_rep/B_avoid/R_peakはbyte、Nは無次元。ディスクとRAMのbyteは別の資源。

## 5. ERROR CHECK・学際性と次の問い

全8資産の完全Git SHA、全repo合計1,403,226,367,788 byteをv19と照合。Mistral 7/3、GPT-OSS 15/7/1、FLUX 7DiT+10Encoderの形式を識別。NanbeigeのSELECT、150管理/105有効、4TBと独立200GB最低空き、取得承認0を維持。機械学習・ABI/コンパイラ・データアーカイブ・法務の4分野で転用可能。

**〈次に考える問い〉**：利用するハードが今と将来で変わっても再現できることを目標にした場合、Native原本とHF変換形式をどの検証条件で一つに絞れるか。
