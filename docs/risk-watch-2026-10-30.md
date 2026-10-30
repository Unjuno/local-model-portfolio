# 今すぐ確認すべき保存候補 — 2026-10-30

> **調査・選定用です。取得承認ではありません。** 既存119件の一次候補を維持しつつ、現在のアクセス制限・消失時の再現困難性で別に優先順位を付けています。3.8TBの確定収容量ではありません。

## 最重要の確認結果

- **The Stack v2** はGated。ページにはSoftware Heritage/INRIAとの**一括取得に関する追加合意**が必要と明記され、検証済み削除要求を反映した利用可能版への更新義務もある。無条件の全量永久保存対象にはできない。
- **Emilia-Dataset** はGatedで、Hubのライセンス表示と同意条件を分けて読む必要がある。Emilia本体は同意文で**CC-BY-NC**、Emilia-YODASは**CC-BY**。権利確認まで取得承認しない。
- **LMSYS-Chat-1M** はGated。ユーザーの対話データであり、同意・個人情報の評価をしないまま収集対象にしない。
- **DINOv3大型視覚Encoder** と複数の画像・世界モデルは現在Gated。これは観察済みのアクセス制限だが、将来の削除や規制を断定する根拠ではない。
- **OctoMed・MeditronFO・Fara** などの専門SFTは現時点公開だが、元モデルのみでは同一の学習成果が残らない。公開状態よりも消失時損失の軸で優先する。

## A — 現在Gatedのモデル（アクセス・権利・容量を先に確認）

| モデル | 観測状態 | なぜ先に調べるか |
| --- | --- | --- |
| [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | Gated | 公式Qwenと比較できるBF16の第三者拒否方向編集済み重み。公開元への依存がある。 |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | Gated | 32B級の独自画像生成・編集モデル。取得元・実行系の依存が大きい。 |
| [ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | Gated | 独立した画像生成系列。現在Gatedで原本の形式・再利用条件が特別。 |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | Gated | Qwenと異なる約109B MoE。独立系列の比較・解析に価値。 |
| [nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | Gated | 動画から世界を予測する別能力。単なる動画生成では代替できない。 |
| [facebook/dinov3-vit7b16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | Gated | 大型視覚Encoder。画像生成モデルとは異なる汎用視覚表現を保全。 |
| [CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | Gated | 多言語VLMの別系列。商用・非商用境界に注意して保存を検討。 |
| [facebook/sam3](https://huggingface.co/facebook/sam3) | Gated | 画像・動画セグメンテーション。ほかの生成LLMでは代替しづらい。 |
| [google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | Gated | 医療領域の専門後学習済みモデル。独自の評価・利用条件。 |

## データセット — 法的条件の精査が最優先

| データセット | 状態・注意点 | 判定 |
| --- | --- | --- |
| [bigcode/the-stack-v2](https://huggingface.co/datasets/bigcode/the-stack-v2) | Gated同意だけでは一括保存を認められない。ソースごとの権利と更新・削除義務を守る | A-LEGAL-HOLD |
| [bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata) | 使用可能版の通知・帰属表示・データ削除に従い、無条件で永久保存しない | A-LEGAL-HOLD |
| [amphion/Emilia-Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset) | HubメタデータCC-BY-4.0と同意画面のCC-BY-NCの差異を解消。話者同意・著作物・非商用条件を精査 | A-LEGAL-HOLD |
| [lmsys/lmsys-chat-1m](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | 対話中の個人識別情報、同意、公開用途、アクセス条件を精査。無条件取得不可 | HOLD-PRIVACY |
| [allenai/WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M) | 個人情報、権利、匿名化、データ最小化を評価するまで取り込まない | HOLD-PRIVACY |

## B — 再現困難な専門モデルとデータ

| 資産 | 理由 | 判定 |
| --- | --- | --- |
| [EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | 専門家設計・医学系SFTの完成重み。Baseだけでは同一モデルに戻せない。 | B |
| [OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | 医療画像・推論SFTで大規模な独自学習トレースを使用。再現コストが高い。 | B |
| [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | GUI自律操作に特化した27B級の学習済み重み。汎用LLMだけでは同じ行動性能を復元しにくい。 | B |
| [nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B) | 2026年のロボットVLA制御専門モデル。現実・合成ロボットデータの再現コストが高い。 | B-LEGAL-REVIEW |
| [lerobot/pi0_base](https://huggingface.co/lerobot/pi0_base) | 視覚・言語・行動を結合するπ0系ロボット制御のBase。独自アーキテクチャー。 | B-LEGAL-REVIEW |
| [CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 多数言語の人手注釈・翻訳指示データ。消失時に人手の再収集が必要。 | B |
| [allenai/pixmo-cap](https://huggingface.co/datasets/allenai/pixmo-cap) | 人手の高密度画像説明データ。画像と注釈の対の収集コストが高い。 | B-LEGAL-REVIEW |
| [lerobot/aloha_sim_insertion_human](https://huggingface.co/datasets/lerobot/aloha_sim_insertion_human) | ロボット操作デモの学習用データ。VLAモデルとの対応が必要。 | B |

## 実行前の区別

1. **本調査のA/Bは取得順ではなく調査優先度。** Gatedの同意や法律上の権利の確認が先。`A-LEGAL-HOLD`は自動ダウンロード禁止。
2. **最終選定には**完全なcommit、選択ファイルの正確なバイト数・すべての依存物・権利の確認が必要。
3. **モデル・データの取得、個人情報を含む生データの保存、モデル実行をこの文書から許可しない。**
4. **調査する候補が増えたことは3.8TBの保存可否を証明しない。**
5. 他資産のライセンスとアカウント承認を回避しない。

## このラウンドで新たに見つけた候補

[facebook/dinov3-vit7b16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m)、[bigcode/the-stack-v2](https://huggingface.co/datasets/bigcode/the-stack-v2)、[bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata)、[amphion/Emilia-Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset)、[lmsys/lmsys-chat-1m](https://huggingface.co/datasets/lmsys/lmsys-chat-1m)、[nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B)、[lerobot/pi0_base](https://huggingface.co/lerobot/pi0_base)、[CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset)、[allenai/pixmo-cap](https://huggingface.co/datasets/allenai/pixmo-cap)、[allenai/WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M)、[lerobot/aloha_sim_insertion_human](https://huggingface.co/datasets/lerobot/aloha_sim_insertion_human)

**合計 22件、既存119件にない候補 11件。** 一部は法的確認待ち。
