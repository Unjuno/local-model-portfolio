# R88｜v38の全146有効資産を再判定：現在アクセス・重複学習成果・4TB余白

**監査日：2026年11月15日**。基準 `main` → `catalog/CURRENT.json` v38（193管理／有効146）。[機械可読・全146件の新判断](../../catalog/research/2026-11-15-r88-v38-146-access-risk-and-capacity-triage.json)／[93件の修正アクセス台帳](../../catalog/access/2026-11-15-v38-conditional-hub-gates.json)。

**判断：新たに有効選定へ無理に追加する資産はない。既存v38のHaru/PraxisとKumoを維持し、Underdog Saluki、Nemotron-Parse、巨大GLM追加は見送る。** v38の既存193件は変更しない。**重量取得・推論実行・本人Gated許可・登録済ダウンロード承認は0**。

## 1.〈本論〉— 観測されたリスクと将来仮説

2026年11月15日の公開元・行政一次資料は、規制対象が**無差別な全オープンウェイト禁止ではない**ことを示す。

| 出典・確実性 | 公開元で確認した事実 | 保存方針への影響 |
|---|---|---|
| [EU AI Act Service Desk（開源適用）](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source) | オープンソースでもsystemic-riskモデルの提供者義務は免除されず、その他は条件付き免除がある | 150Bというローカル運用上限と法定訓練計算量・systemic riskを混同しない |
| [EU AI Act適用日程](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline) | 2026-12-02の非同意の性的ディープフェイク等のAIシステムに関する禁止施行予定が掲載 | **AIシステム・生成行為規制であり、全NSFWモデル重みを一律禁止する予告ではない** |
| [中国CAC 2026-04-30](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm) | 公開モデル・データ管理の不備に対する取締りが明記 | 将来の失効シナリオを条件付きで優先審査するが、個別削除予告とはしない |
| [中国MOFCOMの技術輸出管理説明](https://english.mofcom.gov.cn/News/SpokesmansRemarks/art/2026/art_74bf283f105a4b19a11f7430df3671ae.html) | 既に公開されたオープンソース技術の扱いについて例外等を説明 | 輸出規制とモデル配布元の認証・利用許諾を別ゲートにする |
| [Hugging FaceモデルGating](https://huggingface.co/docs/hub/models-gated) | モデル所有者がアクセス申請・承認を制御できる | **現在のGatedは20/93条件付き**、本人許諾の有無・将来の法律とは別の事実 |

2026年11月15日のHugging Faceモデル照合で、[Haru-4B](https://huggingface.co/higurashi-ai/Haru-4B) はpublic metadata、[Praxis DROID](https://huggingface.co/runwayml/praxis-1-droid) はGated。旧v37アクセス台帳91件を正本v38に流用していた不一致を修正し、**v38のCONDITIONAL93件に正確に93 access行が対応、Gated20件**とした。SELECT53件はこの条件付き専用台帳で公開状態を独立に測定していないため、**非Gatedと推定しない**。

### 再調査の優先作業（区分は重複なし）

| 最初の作業 | 件数 |
|---|---:|
| A 本人のGated権限＋原本利用条件を先に確認 | 20 |
| B Perplexity旧プライベートmanifestと現在Hub公開状態の版差 | 1 |
| C 非商用・研究専用・地域制限等の明記 | 8 |
| D 権利表示が独自／非標準の原本 | 27 |
| E その他の学習済み構成総数・依存が未閉包 | 2 |
| F 原重み・依存・完全runtime照合 | 88 |
| **合計** | **146** |

**9件が全パラメータ構成未閉包**だが、その一部はA〜Dにも属するためEの2件だけを数えると過小評価になる。また、最終取得ファイルbyteとrevisionを**まだ144件で正本上確定できていない**。現有モデルを「保存済み」とはしない。

## 2.〈応用・転用例〉— モデル内部構成に基づく採否

| モデル | 決定 | 内部構成・権利の根拠 |
|---|---|---|
| [Haru-4B](https://huggingface.co/higurashi-ai/Haru-4B) | **CONDITIONAL継続** | 同時音声入出力の独自学習重み、公式[コードの固定NOTICE](https://github.com/higurashi-ai/Haru/blob/7fe6b7665f8bf035998f401f8cb779fbe53f2751/THIRD_PARTY_NOTICES.md)がVibeVoice音響codecの**学習済みパラメータをHaru原本に内包**と明記。別VibeVoice重みは依存として追加しない |
| [Runway Praxis-1 DROID](https://huggingface.co/runwayml/praxis-1-droid) | **CONDITIONAL継続（Gated許可先行）** | 17 BF16 shard＋別の行動head、原本とは別のQwen3.5-2B encoder13ファイルが必要。Wan2.2 VAEは既選択のSHAと一致する公開元ソースを参照、ローカル再利用は未認定 |
| [NVIDIA Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) | **CONDITIONAL継続** | 公式[固定コード](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/relational/model.py)の外部キーGNN/関連表message passingは単表Kumo-Tabularの通常変換ではない。二つの学習済み分類/回帰headの全tensorは未検証 |
| [Underdog Saluki 27B](https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0) | **非追加** | 公開元の現行表示はCC BY-NC 4.0で親が既量子化Qwen3.8系。独立した追加学習成果・改善が未確証。第三者の11月5日ライセンス変更記録は現行表示だけでは実証できない |
| [Nemotron-3.5-Parse](https://huggingface.co/nvidia/Nemotron-3.5-Parse) | **非追加** | LightOnOCR/PaddleOCRの既保存対象と機能が重なる。OCRの同条件改善とcustom ABIを示す検証なし |
| [GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | **150B超例外の研究候補に留める** | Hubに総321B級の情報あり。MoEの活性数を全数と誤認せず、同一HW/backend/context/batchのRAM/品質/速度試験がないので昇格しない |

**取り違え防止**：既存Cosmos、Praxis、Alpamayo、GR00Tは動画世界シミュレーション、身体行動、車両軌跡、汎用VLAと出力分布・学習目的が異なる。性能の作者報告だけで削除する根拠はない。逆に量子化だけの2本目を「独立学習成果」と数えない。

## 3. 容量・必要追加依存のストレステスト

| 記号 | 日本語の意味 | 単位（SI準拠） | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `B_0` | v32歴史的SHA-aware原本ソース算術 | byte | 3,466,070,232,173 | 完全ランタイム/実HDDではない | 非負整数スカラー |
| `B_{33:36}` | v33〜36の仮の追加枠 | byte | 94,520,000,000 | 4版の予約を合算 | 非負整数スカラー |
| `B_{38c}` | v38の追加計画枠 | byte | 80,000,000,000 | 見積枠、実選択bytesではない | 非負整数スカラー |
| `B_{38s}` | v38 Haru/Praxis/Qwen公開ソース参照合計 | byte | 69,536,354,285 | VAE重複参照を含まず、実HDD未確認 | 非負整数スカラー |
| `C` | 保存先計画上限 | byte | 4,000,000,000,000 | 所有HDD容量の測定値ではない | 非負整数スカラー |
| `F` | 実空き安全床 | byte | 200,000,000,000 | 必ず物理検証 | 非負整数スカラー |
| `H_c` | 計画枠シナリオ余白 | byte | `C-F-(B_0+B_{33:36}+B_{38c})` | 全依存/staging不明 | 整数スカラー |
| `H_s` | 公開元追加ソースシナリオ余白 | byte | `C-F-(B_0+B_{33:36}+B_{38s})` | 完成済みHDD余白ではない | 整数スカラー |

**具体的な計算**：保守的な計画予約枠で`H_c=159,409,767,827 byte`（約159.41GB）。新2モデルとQwen依存の公開元ソース参照を使用すると`H_s=169,873,413,542 byte`（約169.87GB）。**次元チェック**：全てbyte同士の加減算で整合。実際の残容量は**不明**、全runtime・wheelhouse・staging・暗黙取得分が約159GBを超えると、この単純シナリオは4TBと200GB余白条件に収まらない。全モデルの完全SHA-aware再計数を実施するまでは`PASS`としない。

## 4. H/T/D/C/UとERROR CHECK

- **H:** 公開済みソースのGated状態を現在の正本で一意照合し、容量と独自学習成果から優先作業を再設計できる。
- **T:** 正本193全件からactive146を全数取り、93条件付きアクセス台帳＋146readiness IDをexact join。最小`n_min=146`、全行一致かID不一致で停止。2新原本の公開元コード／Hub状態を再確認。
- **D:** **PASS**＝146/146一意、アクセス93/93、Gated20、6作業区分計146、全DL承認0。**UNCERTAIN**＝実物hash・依存ライセンス閉包・HDD物理容量・復元成功・将来のモデル個別規制。**FAIL**＝Gated権利回避、根拠のない一律禁止断定、容量を実測として扱う。
- **C:** ソフトの暗黙依存、Haru内蔵codecを別重複重みとして加える、PraxisのGated状態を未記録、同一モデルの量子化コピーを独立成果に誤計上。
- **U:** 配布元ファイル更新、未計測のトランジティブ依存、ユーザー実機、ライセンス条項と法域。実測値の誤差分布がないため合成標準不確かさ`u_c`や包含係数`k`は定めない。

**ERROR CHECK**：193／146、A20＋B1＋C8＋D27＋E2＋F88＝146、現在のGated20、残余約159.41GBは**仮説値で物理余白ではない**。新規選定0・不合理な削除0・本体DL0・承認0。

**学際的な転用**：MLアーキテクチャ（真の学習成果単位）、デジタル保存（重複排除と完全復元）、ソフトウェア供給網（SHA/ABI）、行政法・知財（配布と行為規制を分離）。

## 5.〈次に考える問い〉

**最優先は新たな大型重みの追加か、それとも現在Gated20件の本人権限、権利、完全ファイルと物理容量を先に閉じることか。**
