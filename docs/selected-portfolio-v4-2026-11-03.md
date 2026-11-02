# 採用ポートフォリオ v4（2026-11-03）

**現行（作業ブランチ）**：132資産を追跡、105有効（select 54・conditional 51）、延期12、保留15。前日版v3の130件に対し、ローカル3DGS生成のIdolとその必須DINOv3 ViT-H+ Encoderを条件付き選定。

- 正本：[CURRENT.json](../catalog/CURRENT.json)
- 機械可読：[effective-portfolio-2026-11-03.json](../catalog/effective-portfolio-2026-11-03.json)
- 変更差分：[v4-2026-11-03.json](../catalog/revisions/v4-2026-11-03.json)
- 高性能/潜在悪用/将来規制の判定基準：[capability-access-risk.md](../policies/capability-access-risk.md)
- Idolの未承認コア7ファイル：[idol-core候補](../manifests/drafts/idol-core-2026-11-03.candidate.json) — 3,078,990,585バイト

## 2件の判定

| 資産 | 区分 | 今ある事実 | 未解決 |
| --- | --- | --- | --- |
| [speridlabs/idol](https://huggingface.co/speridlabs/idol) | R1 / conditional | public、Apache-2.0 Hub表示、2026-10-29の固定sha、上流全repo 3,128,391,338B | DINOv3 Gated・FLUX.2 VAE、依存SDK、実行環境、ライセンス全文と同意、独立性能測定 |
| [facebook/dinov3-vith16plus-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m) | R0 / conditional | manual Gated、独自利用条件、固定sha、上流全repo 3,362,457,679B | 正規アクセス許諾・LICENSE正文・依存関係とlock |

## 容量

v3の**あくまで仮定に基づく**総量 3,281,639,664,565B に上記2 repoの全ファイル合計 6,490,849,017B を加えた計画シナリオは **3,288,130,513,582B**、十進3.8TBとの差は**511,869,486,418B**。実際に選択するファイル、重複削減、実機容量、200GBの空き、cache/stagingは別途検証。ユーザー申告のHDD表示「約3.8TB」はTB/TiBや総容量・空きが未確定であり、使える追加容量を意味しない。

## 配布条件は規制の予告と異なる

高性能なモデルや悪用可能性があるモデルは保存価値と安全上の責任をともに検討するが、将来禁止の断定は不可。EU AI ActはGPAIのシステミックリスクに対し追加義務を設ける一方、全特化モデルを一律禁止するわけではない。Idolに現時点で規制予定の一次根拠はない。

**ダウンロード承認0件。** Idolの依存する手動承認Gatedモデルについて、利用許可を得る前に取得しない。モデル本体や依存コードを実行しない。
