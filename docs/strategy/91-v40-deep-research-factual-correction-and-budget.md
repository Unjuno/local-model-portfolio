# R91｜v40原本と容量の再検査：未検証の「4TBに収まる」を撤回する（2026-11-15）

## 1.〈本論〉— 確定した事実と採否

対象は `main` の[正式v40全195資産](../../catalog/effective-portfolio-2026-11-15-v40.json)と有効148件。**採否は変更しない**。既存の独立学習成果を、推定の性能や未証明の将来規制確率だけで削除しない。

| 候補 | 確認した学習成果・原本 | 判断 |
|---|---|---|
| [GroundingPI/GroundingPI](https://huggingface.co/GroundingPI/GroundingPI) | Qwen3系言語重みとKimi由来視覚部分を統合した独立学習済み座標token生成器。BF16 2 shard、publisher index **4,843,664,384** stored parameters。 | **CONDITIONAL維持**。追加原本へ昇格済み。単なる量子化コピーではない。 |
| [UBTECH-Robotics/Thinker-WM](https://huggingface.co/UBTECH-Robotics/Thinker-WM) | 深度・RGB・action学習という別目的。ただし25GB級 `.bin` pickle系原本、CC BY-NC-SA、Praxis/Cosmosと一部重複。 | **研究HOLD継続**。安全な読み方と差分実測がないため追加しない。 |
| GroundingPIのGGUF等 | 同一学習済み重みの別表現。 | **重複追加しない**。 |

### 配布元ファイルの全数チェック

[GroundingPI原本のv40正式差分](../../catalog/revisions/v40-2026-11-15.json)の固定元commit `afe658ba07cc47168371d69cc66b40ae9dcede7c` では、全37ファイル **9,805,907,792 byte**。候補28ファイル **9,704,102,624 byte**、除外した9デモファイル **101,805,168 byte**。BF16 2 shard合計 **9,687,403,168 byte**、公開indexのテンソルpayloadは **9,687,328,768 byte**、差の **74,400 byte** はファイルヘッダ等の領域に相当する。**公開元pointer SHAの整合証拠であり、利用者のHDD SHA検証ではない。**

同model cardの[利用条件](https://huggingface.co/GroundingPI/GroundingPI)は「作者の独自部分がApache-2.0、Kimi由来部分はKimi K3の派生条件を引き継ぐ」。単独の`license:apache-2.0`として全内容の再配布権を確定してはならない。固定checkpointに必要な学習済み視覚部分は統合済みとして公開されるため、巨大なKimi K3元checkpointを丸ごと新たな依存として要求する根拠はない。ただし作者の改変Transformers fork、vLLM、GPU/CUDA、利用条件は未閉包である。

### 公開状態の自己矛盾を訂正

[旧R88比較JSON](../../catalog/research/2026-11-15-r88-groundingpi-thinker-original-license-comparison.json)は`ground.model_public=true`と`ground.model_gated=true`を同時に持つ。**両方を正しい観測として使うことはできない**。現行の[条件付き95件の台帳](../../catalog/access/2026-11-15-v40-conditional-hub-gates.json)はGroundingPIを`hub_gated=false`としており、v40の固定ソース観測（private:false, gated:false）と整合する。旧R88は履歴のまま保持し、今回の[訂正証拠](../../catalog/research/2026-11-15-r91-v40-budget-and-publisher-evidence-correction.json)を優先する。ただし公開状態は本人の取得権限・法的許諾の証明ではない。

## 2. 容量の厳密な再計算

直前v39は、v32以前のソース参照とv33以後の**保存計画枠（実ファイルの集計ではない）**を混ぜた研究用上限 `3,656,590,232,173 byte` を用いている。v40 GroundingPI用の暫定枠 `14,000,000,000 byte` を加えると、**仮想の保存後余白は129,409,767,827 byte（約129.41GB）**。新たな外部runtime／ファイルキャッシュ／ステージングも、実際のHDD空きも未計測なので、**4TBに収まるという最終判定は不可**。

| 変数 | 意味（日本語） | 単位（SI接頭辞） | 定義 | 定義域・範囲・前提条件 | 型 |
|---|---|---|---|---|---|
| `C` | 目標保存媒体の計画上限 | byte | 4,000,000,000,000 | decimal TB。実HDD容量とは別 | 非負整数スカラー |
| `F` | 保持すべき空き領域の下限 | byte | 200,000,000,000 | 実空き領域未測定 | 非負整数スカラー |
| `B_{39}` | 旧v39の仮想保全枠 | byte | 3,656,590,232,173 | 旧ソース参照＋計画枠、実容量でない | 非負整数スカラー |
| `R_{40}` | GroundingPIの追加計画枠 | byte | 14,000,000,000 | 実source候補9,704,102,624 byteと区別 | 非負整数スカラー |
| `B_{40}` | v40の仮想計画合計 | byte | `B_{39}+R_{40}` | 全依存・一時stageの増分未含有 | 非負整数スカラー |
| `H_{40}` | v40の仮想床差引後余白 | byte | `C-F-B_{40}` | 実物理HDD空きではない | 整数スカラー |

計算：`B_{40}=3,656,590,232,173+14,000,000,000=3,670,590,232,173 byte`。`H_{40}=4,000,000,000,000-200,000,000,000-3,670,590,232,173=129,409,767,827 byte`。**次元チェック**：byte＋byte、byte－byte－byteで全項がbyte。4TB（10¹² byte単位）を4TiBや4096GBと混同しない。

単純な公開元ソース参照だけを使う代替計算では、v39 `3,642,118,026,646 byte`＋GroundingPIの28ファイル `9,704,102,624 byte`＝`3,651,822,129,270 byte`、床差引後 `148,177,870,730 byte`。両者は計画枠とsourceスコープの**異なる上限試算**であり、実機の真の空き領域ではない。重複除外が正しいかどうかも物理ファイルSHA照合前に断定しない。

## 3. 規制の一次事実と将来仮説

- [EU公式AI Act FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)：一定のオープンソースGPAIへの文書免除はあるが、システミックリスクモデルは免除外。著作権政策と学習概要の要件は別。全面ウェイト禁止の証拠ではない。
- [米国2026-06-02 EO 14409](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/)：政府への先行アクセスは自主的な枠組み。Section 3(c)はモデル公開の政府強制事前許可を設ける権限を与えない。
- [中国2026-04-30 CAC](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm)：管理不十分なオープンソースコミュニティの危険なモデル・コード・データの審査と除去を重点とする。公開ウェイトを一律に禁止したものではない。

**推論**：将来の配布停止・Gated化は予想するが、個別モデルの禁止確率や期限は未測定。実観測のGated20件と未確認の本人資格を優先して調査する。ただし無許可の取得や利用条件の迂回をしない。

## 4. H/T/D/C/U・ERROR CHECK

**H**：固定モデル原本と現在のアクセス台帳を突合することで、形式重複・過大取得・不適切な容量確定を防げる。**T**：v40全195件、active148、CONDITIONAL95、GroundingPI候補28ファイルを全数一致検査。法規制の一次資料を別途照合。**D**：ID/重みsource計算・計画枠の算術はPASS。本人権利、実HDD、外部依存、実行、ローカルSHA、復元、真の保存可能性はUNCERTAIN。無許可DLはSTOP。**C**：旧Gatedフラグを採用する、4TBを4096GBとみなす、tensor payloadと全モデルパッケージを同一視する、同一親重みの量子化を別学習成果と数える。**U**：未確認の実容量・wheelhouse・外部codec・一時ステージングなどは非統計的な不確かさであり、合成標準不確かさ`u_c`・包含係数`k`を定量化できない。

**ERROR CHECK**：195登録／148有効／CONDITIONAL95／Gated20／総数不明の有効モデル9、正式選定変更0件、ダウンロード承認0件、モデル実行0件、機器実測0件。関連分野はML構造、デジタルアーカイブ・ストレージ、ソフトウェアサプライチェーン、規制・知財法である。

## 5.〈次に考える問い〉

**140件超の最終取得scope未確定を、実際のモデル能力と公表元の取得制限に応じてどの順序で減らすべきか。**
