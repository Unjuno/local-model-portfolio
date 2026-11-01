# 第12回：3.8TB保存枠に合わせた実際の再選定シナリオ

**基準日：2026-11-01。** [正本CURRENT](../catalog/CURRENT.json)はv2の110件・有効94件で、承認キュー0件。従来の第4〜11回のレビューはすべて未マージの評価資料。今回から**ただ候補を足すのではなく、残す・ファイル形式を絞る・大型を後回しにする・小型を追加する**という差分案を作った。[構造化差分案](../catalog/revisions/proposed-efficiency-reallocation-2026-11-01.json)を参照。これは現行版に適用していない。

## 1. Hugging Face公式配布情報に基づく上位5モデルの採否

公式Hugging Face接続で公開状態とライセンスを再確認。Mistral4、gpt-oss-120b、Qwen3-Coder-Nextは公開Apache-2.0。Llama4 ScoutはGated・独自ライセンス、FLUX.2-devはGated・独自ライセンス。**Gatedは政府による配布禁止の予告ではない。** 完全コミットごとの公式配布ファイルツリーと整数バイト数は[第12回のファイル単位記録](../catalog/acquisition-drafts/round12-top5-selective-files-2026-11-01.json)に残した。

| モデル | 元リポジトリ全量 (GB) | 1形式選択案 (GB) | 未選択候補 (GB) | 提案する構成 |
| --- | ---: | ---: | ---: | --- |
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 241.890 | 120.957 | 120.933 | hf_three_shards |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | 195.764 | 65.277 | 130.487 | reference_original_seven_shards |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | 177.640 | 112.823 | 64.817 | diffusers_full_pipeline |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | 217.316 | 217.316 | 0.000 | single_published_50_shard_original |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 159.376 | 159.376 | 0.000 | single_published_40_shard_original |

**5件合計は全repo 991.986GB → 一形式案675.748GB、差額316.237GB。** これは数学的なファイル除外量であり、**精度・機能・元重みのテンソル同値性を未確認のまま『316GB節約できた』とは主張しない**。元重み・ネイティブ推論形式の区別を見失わず、ファイルを自動削除しない。Llama4・FLUXのGated状態に対する実行・保存権限も未承認。

特にMistral Small4は3シャードのHF形式と7シャードのconsolidated形式がそれぞれ約121GB。gpt-oss120bは、原作者コードが扱う`original/`と、HF14シャード、Metal版の各約65GBが同じrepoにある。FLUX.2-devは単一checkpointとDiffusersのtransformer/vaeが重複する可能性があるが、テキストencoder約48GBはモデル稼働に必要である可能性が高い。**ファイル名と大きさだけで同じ重みだと証明はできない**。

## 2. 159GBの大型コードモデルを取得後順位へ

現行R1/selectedの[Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)は、公開ファイルツリーで40シャード一組、約159.376GBを確認。これと同じ原本の別精度セットは当該repo内に存在しない。**ファイル選別だけで大幅な削減はできない**。現行の他のコードモデルとの同タスク/同環境性能と、独自の訓練成果・正規ミラー調査が未完のため、`R1/select → BACKLOG/deferred`を**提案**する。モデルの品質が悪い、代替可能と立証されたという意味ではない。

## 3. 小型の独立機能7件を次の採用対象へ

第7回で選び、第8回と第11回で完全コミット/ファイル一覧を固定した7モデルを、次期台帳に追加する提案。全7件は**61ファイル、7,743,321,682 B**（モデルリポジトリ内の選択ファイルのみ）。DINOv3はGated同意待ち、NLLBは非商用研究目的、OmniParserはMIT部品だけの選定で、旧AGPL検出器の自動取得を含めない。

| 候補 | 研究上の順位/選定 | 選択側の容量 (GB) | アクセス |
| --- | --- | ---: | --- |
| [facebook/dinov3-vits16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m) | R0/conditional | 0.086 | manual gated |
| [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) | R2/select | 0.099 | public |
| [facebook/sam2-hiera-tiny](https://huggingface.co/facebook/sam2-hiera-tiny) | R2/select | 0.156 | public |
| [Qwen/Qwen3Guard-Gen-0.6B](https://huggingface.co/Qwen/Qwen3Guard-Gen-0.6B) | R1/select | 1.519 | public |
| [microsoft/OmniParser-v2.0](https://huggingface.co/microsoft/OmniParser-v2.0) | R1/conditional | 1.365 | public |
| [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) | R1/conditional | 2.483 | public |
| [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | R2/select | 2.035 | public |

**この7件は未取得・未承認です。** モデル側のファイル量が正確でも、OS、実行器、Tokenizer外部依存、GPU/CPU対応、法的適合性、完全オフライン動作について未確定事項が残っている。新たなビット数の量子化で高精度の原本を置き換える提案でもない。

## 4. 3つの検証可能な容量シナリオ（十進GB）

以下はいずれも**原本の上流repo見積り3.234TB**を起点にした予算の*仮定計算*であり、実際のHDD使用量ではない。以前のv3、round4/5/6の新規候補はこの計算に**含めない**。必要依存と一時作業領域も未知。

| シナリオ | 想定量 (GB) | 3.8TBとの差 (GB) |
| --- | ---: | ---: |
| v2_with_seven_no_refinement | 3241.811 | 558.189 |
| v2_defer_qwen_add_seven_no_format_change | 3082.435 | 717.565 |
| v2_defer_qwen_add_seven_choose_one_format_top_three | 2766.197 | 1033.803 |

選定の判断：**最初に行うのはQwen3-Coder-Nextを期限付きで調査後順位にすること**。これだけでも暫定計算の比較枠が変わるが、モデルの原本を削除する指示ではない。次にMistral4 / gpt-oss / FLUXの単一形式が研究目的に十分か検証できた場合のみ、最も容量が低い第三シナリオへ進む。Gatedで再取得条件のあるLlama4とFLUXを安易に最下位へ落とさない。

## 5. 容量では測れない条件と次の作業

1. **権利**：モデル重み・前処理・訓練データの権利を区別。Gatedへの同意は本人のみ。ライセンスが商用を許すかどうかと、研究保存の目的が適合するかを個別に確認。
2. **形式**：異なるcheckpointの正規学習由来・tensor名/shape/precision・必要な実行器の対応関係を比較できてから、一方を不要形式と断定する。
3. **性能**：コードモデルなら同じコード編集・テスト修復タスク、同じ問題集合、CPU/GPU、クロック/電力・backend・量子化・コンテキスト・バッチを固定して優位性を測る。研究用Baseの唯一性と処理時間/消費電力の双方を評価。
4. **保存予算**：3.8TB上限と空き200GBを別々に確認。選定済み全ファイルだけでなく依存・キャッシュ・一時ファイルを集計し、3〜4bitスクリーニング時のOS/KV込みピーク推論RAMが512GB未満であることを実機前提で判断。
5. **記録を修正**：READMEの『現行97件』を正本110件に更新する。追加提案を現行と同じ件数として表示せず、すべてドラフトと明記。

## H/T/D/C/U

| 区分 | 実施内容 |
| --- | --- |
| H | 同一学習済み重みの別形式を整理し、重複保全を避けつつ小型の専門能力を追加できる |
| T | 上位5件の固定版219ファイルに対し選択・除外を全件照合、7新規モデルの61ファイルと既存正本のID/容量を再集計。同値性・性能は別途実機と取得の承認後に評価。規約/Gated/依存が不明なら停止 |
| D | メタデータと整数バイト計算はPASS。`CURRENT`正式変更/モデル取得/形式の同値・コスパ実測は未承認またはUNCERTAIN |
| C | 異なる重み形式は元精度/学習履歴が違う、GPUバックエンド要件が非互換、候補の違いが実用精度で大きい、Gatedの保存許可が得られない |
| U | 権利・モデル版・外部依存・品質・実機メモリ・ステージング容量は未確定。合成標準不確かさ・包含係数は分布が未定義で数値化しない |

## ERROR CHECK

README/機械可読台帳を実際に変更した後、正式台帳・承認キューを再照合する。完全な重みファイルを取得・実行していないため、Tensor同値性・ファイルSHA実物の一致・推論能力を検証したとはしない。
