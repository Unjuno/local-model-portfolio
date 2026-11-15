# v41：LoRA原本の一本化とPruna地域ライセンスを正本に確定（2026-11-15）

## 1.〈本論〉
v40の195登録・148有効（SELECT53/CONDITIONAL95）と全件の採否を維持し、既存2件の原本・権利メタデータだけを更新。Gated20件、総パラメータ数未確定の有効9件、取得承認0。
ausboss/Qwen-Image-2.1-Consistency-LoRA：HF固定revision 58897a02f4f60f88376eab5676738dd45e5ed1a2、作者推奨step1500、1重みSHA256 4f44ada1be2189cc23b3d010f9603543403f48454e2f76842a3d30109b20bd63、5ファイル159,544,753byteを一次ソース候補として正本に記録。作者の別step2000は色と位置のトレードオフがあり初期保存から除外。親Qwen/Qwen-Image-2.1は有効既存資産だが現物SHAでの共有は未実証。Qwen Research Licenseは非商用であり、別の商用許可が必要。
PrunaAI/P-H3-Image：MiniMax H3の標準ライセンスはEU・英国・韓国・米国を地域から除外。主transformer 33,122,992,896＋prompt upsampler 9,409,813,744＋text encoder 4,437,815,808＝既知3部46,970,622,448。VAEとtext connectorが未計数で総数未確定。modular_model_index各componentのrevision=nullは完全オフライン化に不適切なため固定ローカルrootを要求。Apache2のQwen派生部とMiniMax派生部の権利も区別。
根拠：[9件監査](../../catalog/research/2026-11-15-v40-nine-parameter-and-license-closure.json)、[step1500源5件](../../manifests/drafts/v40-qwen-image21-step1500.candidate.json)、[一次調査説明](2026-11-15-nine-gates-lora-pruna-territorial-rights.md)。

## 2. 変数表と次元検査
| 記号 | 意味（日本語） | 単位(SI準拠) | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| Ba | LoRA原本重量 | byte | 159,436,496、Publisher LFS | 非負整数スカラー |
| Bs | LoRAの5source容量 | byte | 159,544,753、未取得 | 非負整数スカラー |
| Pt | Pruna transformerパラメータ | 1(個) | 33,122,992,896、publisher | 非負整数スカラー |
| Pu | Pruna prompt upsamplerパラメータ | 1(個) | 9,409,813,744、公式index | 非負整数スカラー |
| Pe | Pruna text encoderパラメータ | 1(個) | 4,437,815,808、公式index | 非負整数スカラー |
Bs-Ba=108,257byte、Pt+Pu+Pe=46,970,622,448個。単位の異なるbyteと個数を混同しない。Publisher source byteは実HDD空きではない。

## 3. H/T/D/C/U・ERROR CHECK
H：同一学習タスクのLoRA二チェックポイントを無差別に保存せず、推奨原本を一つ固定する。T：11公開ファイルの選択5/除外6、Pruna LICENSE/NOTICE/3 index、全195の同一選定・148キュー/依存/停止ゲート・95アクセスを静的照合。D：元sourceと件数PASS、完全pipeline総数・個人権利・HDD/ローカルSHA/復元UNCERTAIN、無許可DLはFAIL。C：step2000の幾何精度が色忠実性より重要な場合・Pruna別地域使用時の特別ライセンス。U：作者評価・本体の実体・ライブラリABIと法律適用の不確かさ。統計分布が無いのでu_c/k算出不可。
ERROR CHECK：新規0、除外0、195登録/148有効、9未確認、Gated20、承認0。学際分野は画像生成ML、保存科学、ソフト供給網、国際契約。

## 4.〈次に考える問い〉
残る9件の完全学習済み総数を安全なtensor censusで閉じる順序をどう決めるか。
