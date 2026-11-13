# 40 — NVIDIA GR00T N1.7: 新規学習成果と一次ライセンス矛盾の調査（2026-11-07）

## 0. 前提・判断

正本 `catalog/CURRENT.json` はv27-20261107、**173資産・有効126件**、選定一次スコープ126件を全件容量確認済み、既知論理重複排除後**3,417,685,712,585 B**。35資産の実行・依存・権利が未閉鎖、owner HDD実空き・物理容量・一時stagingピーク・全offline一式は未測定。4TBと最低物理空き200GBの保存上限規則は不変。

新たに調べる`nvidia/GR00T-N1.7-3B`は、既選定`nvidia/GR00T-N1.6-3B`の後継だが、**同一重みの別量子化ではない**。NVIDIAの公式説明はCosmos-Reason2-2B/Qwen3-VLを利用するVLM基盤、相対end-effector動作座標、20,000時間のEgoScale一人称動画による事前学習への変更を示す。ただし、**後継N1.7そのものの発売日を2026-11-07と誤記しない**。2026年4月から公開されており、本調査で新しく判明した出来事は2026年11月5日発生の**一次配布元ライセンス不整合の明示的な指摘**である。

## 1. 確認済みライセンス矛盾

原本：[NVIDIA/Isaac-GR00Tの固定README](https://github.com/NVIDIA/Isaac-GR00T/blob/7b304f95b95790490b79bd263ba57015c3c12dfd/README.md) と [HF N1.7モデルカード](https://huggingface.co/nvidia/GR00T-N1.7-3B) は**商用利用可能、モデル重みは NVIDIA Open Model License**と説明する。一方、[HF N1.7の`LICENSE`原文](https://huggingface.co/nvidia/GR00T-N1.7-3B/blob/main/LICENSE) は**NVIDIA License**であり、Section 3.3が非商用の研究・評価利用に限定する。**コードのApache 2.0とモデル重みの契約を同一視しない**。

[GitHub Issue #803](https://github.com/NVIDIA/Isaac-GR00T/issues/803)は**2026年11月5日13:25 UTC**に第三者が登録したライセンス明確化依頼。今回調査時点ではopen、NVIDIA権利者の訂正・合意を確認できていない。Hugging Faceにも[同主旨のDiscussion #2](https://huggingface.co/nvidia/GR00T-N1.7-3B/discussions/2)がある。**第三者Issueの存在＝法的最終判断ではない**。安全な暫定扱いは「より厳しい表示を前提に、権利者の版固定訂正を待つ」ことであり、公開重みの合法的保存可能性と第三者再配布・商用提供可能性は別に審査する。

[対応するNVIDIA Open Model License原文](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/)へのリンクがあることも、固定HF `LICENSE`の非商用制約を自動的に解消しない。**本人に対する取得/配布の承認権限は研究者側が代行・推認しない**。

## 2. N1.6とN1.7の学習成果差分

| 指標 | 既選定 N1.6 | 新規調査 N1.7 |
|---|---|---|
| GitHubソース枝 | [N1d6](https://github.com/NVIDIA/Isaac-GR00T/tree/n1d6)、固定版`9b37aa1ce69c73c6d165233fa88128283bba4508` | [GA main固定版](https://github.com/NVIDIA/Isaac-GR00T/tree/7b304f95b95790490b79bd263ba57015c3c12dfd) |
| HF原重み | [`nvidia/GR00T-N1.6-3B`](https://huggingface.co/nvidia/GR00T-N1.6-3B)、`d0814e7ecb19202e7c8468b46098b0b7ef3a6d61` | [`nvidia/GR00T-N1.7-3B`](https://huggingface.co/nvidia/GR00T-N1.7-3B)、[固定版研究監査JSON](../../catalog/research/2026-11-07-gr00t-n17-rights/audit.json)を参照 |
| 旧・新VLM | Eagle Block2A 2B v2（N1.6の`config.json.model_name`） | Cosmos-Reason2-2B（Qwen3-VL） |
| 独自学習成果 | GR00T N1d6 Action policy | 人間動画20,000h/relative EEF action融合、N1d7モデル別weights |
| パラメータと保存ファイル | N1.6 publisher全repo **6,573,788,038 B** | N1.7 publisherの固定版全repo・必要ファイル・元tensor要素をCIで確定 |
| ソフトウェア/依存 | N1d6 (`transformers==4.51.3`というREADME比較記載) | N1d7 (`transformers==4.57.3`)、別ABI。互換性/実GPU計測なし |

**注意**：N1.7の元モデルcheckpointにCosmos-Reason2-2Bの全VLM重みが同梱されているか、それとも別途配布元のGated `nvidia/Cosmos-Reason2-2B`のパラメータが必要かは、原tensor indexとN1d7コードの対応関係を確定するまでは**UNKNOWN**。名前の参照だけで「別repoのGatedウェイトが必ず必要」とは断定しない。逆に、既に原本に統合されている証拠なく二重保管もしない。

最新の[Cosmos-Reason2-2B公式モデル](https://huggingface.co/nvidia/Cosmos-Reason2-2B)はGatedで、本人の許可状態は未取得。N1.6の`nvidia/Eagle-Block2A-2B-v2`についても、モデル設定の記載と配布元が現在匿名検索できることは別評価。

## 3. 研究選定と反証条件

**判断：N1.7 `RESEARCH_HOLD_RIGHTS_CONFLICT_AND_BACKBONE_CLOSURE`。** 高い独自学習価値を認めつつ、N1.6を削除せずN1.7もCURRENTの新規有効選定には追加しない。移行によってN1.6にしかない学習成果・embodiment規約が失われ得るため、**後継＝単純置換**は不可。新規採用1件あたりの重量コストを検証するため、既知v27にN1.7の元ファイルを追加したソース-only SHA重複排除容量を別計算する。

未採用判断の反証条件は、NVIDIAが(1)固定`LICENSE`とカード/READMEの齟齬を解消し、(2)N1d7のVLM・processor・robot modality normalizationすべてを合法的にオフライン復元でき、(3)元重みのSHA・実RAM・実空きと相対的品質・独自能力が許容できると確認できた場合。公称ベンチマーク値だけで測定済み推論性能としない。

## 4. H/T/D/C/Uと検証の境界

- **H：** N1d7はN1d6とは異なるロボット動作学習成果で保全価値があるが、公開されているN1.7の法的権利範囲は一次資料相互で矛盾している。
- **T：** 固定HF commitの匿名API treeと`LICENSE`/`README`/config/indexの小型テキストを読む。GitHub固定版READMEと2026年11月5日Issue #803、CosmosバックボーンのGated公開メタデータを別々に記録。内部tensor自体はダウンロードせず、選定容量はSHA-aware source-only計算で実施。N1.6を含む履歴は一切変更しない。
- **D：** RIGHTS PASS=権利者による適用ライセンスの版固定一致、利用用途/本人権限への適合。SOURCE PASS=checkpointとコードの固定版/byte/必須関連ファイルが確定。RESTORE PASS=実際のHW・driver・transformers ABI・robot正規化・オフライン出力まで再現。現状RIGHTS/RESTOREは**UNCERTAIN**。
- **C：** READMEが重みに対する契約を誤記、非商用の制約が残る、独立VLM学習重み未保全、初期化時にGated Cosmosを再取得、embodiment action schemaとコードのABI不一致、ランタイム/現物のRAM過大。
- **U：** 許諾条項の適用範囲、実物SHA256、所有者物理ディスク、実装/backend、埋込VLM重みの重複に未定量化の不確かさがある。測定分布未収集のため合成標準不確かさ`u_c`と拡張係数`k`はUNKNOWN。

**ERROR CHECK：** 既存172以前の監査台帳を上書きせずv27の173/126を維持。新採用/HOLD/REJECTの形式的変更0、approved 0、main 変更0、モデル重みダウンロード0、クラウド課金0、本人HDD測定0。機械学習、ロボティクス、サプライチェーン、デジタルアーカイブ、ライセンスを独立検査する。
