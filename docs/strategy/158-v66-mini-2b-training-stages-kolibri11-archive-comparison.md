# R158／v66（2026-11-24）— 小型学習段階の非重複保全と新規75B独立MoE原本の一次監査

## 1. 結論

本調査は [`catalog/CURRENT.json`](../../catalog/CURRENT.json) が示す `v66-20261124`（**246登録／197有効：SELECT56・CONDITIONAL141・HOLD30**）を基準とする。取得台帳には**116モデルVERIFIED・1,758ファイル・2,021,784,002,725byte**の報告があり、116repo IDは現行246件と一致する。ただし、所有者のWindows Dドライブに対する今回の独立SHA-256・法的利用許諾・完全オフライン復元の証明ではない。

**追加取得を検討すべき新しいソース3件の原本範囲を、Publisher固定40桁revisionで確定**した。どれも246件の現行正本および116件取得報告に同一repo IDがなく、同一モデルを再取得する重複計画にはなっていない。

| 調査順位 | モデル／リンク | 固定原本source | 採否（DL未承認） |
|---:|---|---:|---|
| **P0-A** | [MiniCPM5-2B Final](https://huggingface.co/openbmb/MiniCPM5-2B/tree/42433e90dad95123ab87729fd7011e7110629556) | **11 files・5,043,807,977 byte** | **次期CONDITIONAL新規追加を推奨**。2.5168B原本、RL＋OPD後学習の最終版。現行116件にはない |
| **P0-B** | [MiniCPM5-2B Base](https://huggingface.co/openbmb/MiniCPM5-2B-Base/tree/e09861095569642c3cf632d80e3200ee1d30b547) | **10 files・5,043,780,610 byte** | **次点研究CONDITIONAL候補**。独立した事前学習Baseを編集研究・巻き戻し可能性のため保存候補とする。「無検閲と実測済み」とは主張しない |
| **P1-希少** | [Kolibri 1.1](https://huggingface.co/Aleph-Alpha/Kolibri-1.1/tree/bfc33150d363f55a86cd4f0f7f79711deb9e0361) | **42 files・77,556,017,718 byte** | **独立75B学習済みMoEの研究HOLD**。2026年11月23日公開、独英バイリンガル・疎attention・長文対応の別学習成果。専用GPU/runtime未検証につき取得保留 |

**3repo計63ファイル、Publisher LFS SHA-256参照34件、87,643,606,305byte（十進87.64GB）**。実ディスク必要転送バイト、キャッシュ・staging、他の既取得ファイルからのハッシュ共有が未検証なので予算や空き容量の実測値にはしない。公式APIから取得したのは**モデルメタデータとファイル情報のみ**で、重みペイロード・モデルコードは未取得、未実行。

**固定一次資料**：[不変原本ソース・学習段階比較](../../manifests/drafts/r158-2026-11-24-minicpm5-kolibri-stage-fixed.candidate.json)、[採否判断](../../catalog/decisions/2026-11-24-r158-v66-mini-final-base-kolibri-selection.json)、[次期非実行審査キュー](../../queues/proposed-v66-r158-three-new-originals-UNAPPROVED.json)、[静的テスト](../../tests/test_r158_v66_minicpm_kolibri_source_scope.py)。

## 2. MiniCPM5：系列全保存ではなく段階の独自学習を評価

公式モデルカードとHugging Faceの不変Treeで4種の学習済み原本を比較した。4つとも重みのLFS SHA-256が**すべて異なる**。これを「GGUFやINT4のような量子化形式の別表現」として除外するのは誤りである。他方、4つの段階を無条件にすべて取ることも保存効率の最適解とは限らない。

| 学習段階（独立した重みSHA） | 正確なPublisher原本参照容量 | 研究上の位置付け |
|---|---:|---|
| [Base](https://huggingface.co/openbmb/MiniCPM5-2B-Base) | 5,043,780,610byte | 前学習済み、後処理前の原本。Baseでの応答能力や拒否率は未測定 |
| [Midtrain](https://huggingface.co/openbmb/MiniCPM5-2B-Midtrain) | 5,043,780,588byte | 追加の中間学習段階。独立stateだが将来の差分価値は未評価・研究HOLD |
| [SFT](https://huggingface.co/openbmb/MiniCPM5-2B-SFT) | 5,043,780,588byte | 教師あり学習後、RL／OPD前のstate。独立stateだが研究HOLD |
| [Final](https://huggingface.co/openbmb/MiniCPM5-2B) | 5,043,807,977byte | RL＋OPD完了の小型agent最終原本。最優先 |

Finalの1ファイルBF16重みは **5,033,557,096 byte**、HF総格納要素は **2,516,756,480**。モデルは標準`LlamaForCausalLM`、最大文脈長131,072。メーカーが掲げる総合ベンチマーク平均 **53.9** は作者の条件下の集計であり、所有者のHW/ドライバ/クロック/バッチ/推論backend/量子化条件が揃った独立比較ではない。現行のQwen系列・LFM系列等に対して性能優位を断定しない。

**権利上の停止条件**：モデルカード上はApache-2.0で、[OpenBMB公式MiniCPMコードLICENSE](https://github.com/OpenBMB/MiniCPM/blob/main/LICENSE)もApache-2.0。しかし固定HFモデルrepoの11または10ファイル内に独立した`LICENSE`がない。コードのLICENSEとモデル重みの帰属・学習データ権利は確認すべき対象が異なる。ユーザーの使用・再配布・改変行為ごとに最終レビューが必要。Transformer、tokenizer/chat template、131K文脈KV、CPU/GPU使用メモリおよび依存ライブラリcommit未固定のため**DL承認＝false**。

## 3. Kolibri 1.1：新しい疎attention 75Bを旧Kolibri1と入れ替えるか

2026年11月23日付[公式発表](https://aleph-alpha.com/en/blog/kolibri-1-1/)と[モデルカード](https://huggingface.co/Aleph-Alpha/Kolibri-1.1)を確認。Kolibri 1.1は、以前のKolibri1 (78.1B、Publisher full reference 78,862,325,687byte)から継続学習した**別の学習済み結果**。中間層の疎attentionと長文事前学習、独立SFT/RLを含む。

- 作者公表：**75,128,393,984総パラメータ／3,439,874,304活性**、262,144ネイティブ文脈、最大1,048,576の延長可能性。公開元Hub safetensorsメタデータは **75,112,665,344要素**で、**15,728,640**差がある。テンソル内訳を独立計数していないので「完全一致」とは扱わない。いずれの総数も150B未満だが実機RAMとは無関係。
- 配布原本：31分割Safetensors重量＋index・LICENSE・config・tokenizerほか**42files／77,556,017,718byte**。HF LICENSEはApache-2.0。旧Kolibri1より小容量の別構造で、単なるQ4形式変換ではない。
- 参考動作条件（メーカー）：最小**2×H100 SXM5、2×H200、1×B200、1×B300**等。推論の実ピークRAMと長文KV、Transformers/vLLMのバージョン・ドライバ/zero-point、ownerHWの速度を確認していない。**保存対象として技術価値は高いが、現時点でダウンロードREADYには格上げしない**。
- 作者が主張する「GPU時間3.4倍効率化」や「強いベンチ」について、比較対象・測定GPU・clock・バッチ・サンプルと95%信頼区間が独立確認されておらず、プロジェクト側の計測結果とは区別する。

Kolibri1と1.1を両方保存するかは、**独立の技術歴史資料として旧版が必要か**で決める。現時点では後継1.1を優先し、旧1原本は固定revision/重量SHAだけを研究台帳に残す。約78.86GBを余分に取得する判断はしない。

## 4. 無検閲・小型・特殊能力と規制リスクを別軸で扱う

v66にはすでに[nchapman/Qwen3.5-0.8B-Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA)の差分と[abacusai/Smaug-Uncensored](https://huggingface.co/abacusai/Smaug-Uncensored)が登録されている。**無検閲モデルを確保することと、作者の拒否率ベンチのみで一般能力向上を認定することは別**。既存親・LoRA・editを異なる学習stateとして管理し、フルマージ・GGUF形式の再ダウンロードはSHAによる独自性確認までは後回しとする。今回のMiniCPM5 Baseも「Baseだから無検閲性能が優秀」とは主張しない。

米国BISの[2026年11月19日付Federal Register](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion RuleのECCN4E091を撤回した。EUの[AI Act Service Desk（GPAIオープンソースQ&A）](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)では、公開モデルに特定の透明性例外がある場合も、著作権方針・学習データ概要等が残ることを説明している。**これらは保管中の全オープン重みを近日禁止する法律ではない**。モデル固有のGated・ライセンス変更・配布停止をストレスシナリオとして見張る。確率や削除予告日を創作しない。

## 5. 実行条件の分離／容量計算

原本容量の一次照合を数式で記録する。

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| \(B_f\) | MiniCPM5 Final Publisher固定sourceの容量 | B（byte、十進） | 全11ファイルの和 | \(\ge0\)、実機保存量ではない | 整数スカラー |
| \(B_b\) | MiniCPM5 Base Publisher固定source容量 | B（byte、十進） | 全10ファイルの和 | \(\ge0\)、実機保存量ではない | 整数スカラー |
| \(B_k\) | Kolibri1.1 Publisher固定source容量 | B（byte、十進） | 全42ファイルの和 | \(\ge0\)、実機保存量ではない | 整数スカラー |
| \(B_\Sigma\) | 3原本の重複排除前の参照容量 | B（byte、十進） | 上3要素の和 | \(\ge0\)、owner媒体の増分容量は不明 | 整数スカラー |

\[
B_\Sigma=B_f+B_b+B_k
\]

\[
=5,043,807,977+5,043,780,610+77,556,017,718
=87,643,606,305\ \mathrm{byte}
\]

次元検査：byte＋byte＋byte＝byte。十進GBでは**87.643606305GB**。通常の実機保存容量には取得中のステージング、cache、ファイル共有とownerHDD実占有を別途反映するため、この数字だけで4TB上限や200GB実空きのPASSを付けない。

## 6. H／T／D／C／U、ERROR CHECK

- **H（反証可能）**：MiniCPM5 Finalの後学習原本＋Baseの異なる前学習checkpoint、Kolibri1.1の異なる疎attention長文学習成果は、既存116取得報告の再取得を行わずに新しい機能・学習研究の選択肢を増加させる。
- **T（最小検証）**：現行v66・246 repo IDと116 VERIFED報告IDに3新repoとの重複がないこと。HF不変木の**63ファイル・87,643,606,305byte・LFS SHA-256参照34件**を逐次照合。4 MiniCPM学習段階の異なる重量SHAを確認。実機性能試験では固定タスク・seed・GPU型/クロック・CPU/driver・backend commit・OS・context・batch・量子化zero-pointとKV dtypeを記録し、各候補で**最低30独立繰返し**、同一条件の技術的正答率は**100問以上**で評価する。現在の実機推論反復数は0。
- **D（判定）**：静的Publisher source一致・ID非重複・無承認なら**PASS**。権利や実機ソースが不明なのに取得を始める、SHA drift、学習段階を形式変換と取り違える、未審査コードを起動したら**FAIL**。所有者の権利・HDD実際の空き／SHA、GPUの総実行RAMと品質は**UNCERTAINで取得STOP**。
- **C（反証例）**：MiniCPM5の独立品質が既存小型モデルに劣る、BaseとFinalの両保管による研究価値が低い、Kolibri1.1のGPU要件が利用可能なHWを超える、LICENSE適用行為が許可されない。
- **U（主要誤差源）**：Publisherメタデータ、メーカーの性能報告、ローカル実機未測定、個別LICENSE、配布物外のruntime、親・教材の権利。反復データがないので合成標準不確かさ\(u_c\)と包含係数\(k\)の数値は算定しない。

**ERROR CHECK**：このR158は研究用の固定source選定・権利停止付きの3件審査だけをGitHubへ提出する。現行v66の246登録・197有効を無断で変更せず、`queues/approved.json`は0件、新規モデル重みDL0、Owner Windows D現物再SHA0、コード実行0、既存削除0とする。

学際的関連：①ML後学習・モデル編集、②英独多言語・疎attention、③GPU＋KVキャッシュ・SSDストリーミング性能工学、④長期アーカイブの暗号学的ハッシュ、⑤AI利用許諾と規制。

## 7.〈次に考える問い〉

**将来の再構築不能性を最優先するなら、同じ5GBのMidtrain checkpointと、別用途のまったく独立した5GBモデル原本のどちらに先に予算を割り当てるべきか。** 現時点の基準は独立した能力系統・親依存の少なさ・権利の明確性を優先し、Midtrainは追加研究HOLDとする。
