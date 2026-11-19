# R106｜v45取得前台帳の参照修復とHugging Faceの未確定4モデル監査（2026-11-18）

## 1.〈本論〉

正本は**v45の198資産（モデル172・データ26）、有効151（SELECT53・CONDITIONAL98）**。以前の[CURRENT](../../catalog/CURRENT.json)はv45実効選定／readinessを参照する一方、研究候補キューと依存準備だけ古いv44の149件を指していた。既存のv45ファイル[151件キュー](../../queues/proposed-v45-2026-11-18.json)と[151件依存](../../catalog/preparation/2026-11-18-insurance-bundles-v45.json)に修復。新しい選定revisionを発行せず**選定198件の採否を変更しない**。98件の[アクセス条件](../../catalog/access/2026-11-18-r106-v45-conditional-hub-gates.json)と151件の[停止ゲート](../../catalog/readiness/v45-2026-11-18-r106-all151-gates.json)は最新参照に同期。

## 2.〈応用・転用例〉— 源泉内訳と4つの独立した取得停止理由

[4モデルの一次API固定revision・ファイル数・SHA・停止条件](../../catalog/research/2026-11-18-r106-four-unknown-model-static-scope.json)を再確認。

| モデルと固定revision | 出版社ファイルscope | 原本の中身・判断 |
| --- | ---: | --- |
| [PrunaAI/P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image)、`7f98acef503cf2bcfba821a78cb1cf1a9928b2df` | 54 files、99,845,388,933 byte | 公式`modular_model_index.json`ではTransformer7、upsampler4、text encoder2、connector1、VAE1の5 trained componentsが同じrepoを指す。前回R66の**15 safetensors 49,635,347,496 stored elements**を再利用（今回新規ヘッダ計数ではない）。ただしsubcomponent `revision:null`のため実際のoffline loaderがこの40桁版を読む保証はない。未確定ゲート維持。 |
| [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3)、`78e5ab79e49aa9a25abe8799eff2c4d73a1c3216` | 25 files、41,502,571,262 byte | 15 safetensors shard、公式indexに62,245 tensor名、39,594,895,616byte payload。同repoの学習済み`codec.pth`は1,871,099,728byte、Publisher SHAは固定。pickleをデシリアライズせずcodecパラメータ・安全性未確定を維持。 |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native)、`87a83efdd6551e038246b6b37836a6264713eec3` | 30 files、5,056,388,035 byte | 2 weight shard、source index 731 key、`maya3_config.json` main 2,502,398,656 elements。外部学習済み部品`kyutai/mimi`と`speechbrain/spkrec-ecapa-voxceleb`の完全固定・権利・総数を確認するまで停止。 |
| [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts)、`65ec6a637f4bd9d868064846c69ed85e37d302a0` | 79 files、973,512,551 byte | 公式Gated:autoで匿名configは401。音響・vocoder・speaker learned weightsとINT8/元形式の両方が存在。原形式9件とINT8形式8件の意味ある差を実体未取得で同一と断定せず、本人の適法な権限確認まで取得しない。 |

4件とも**CONDITIONALを維持**。学習済み成果の機能が似るだけで重複とは判定せず、同じ原本の別量子化・シリアライゼーションは追加資産と数えない。特にPrunaのR66は内部原本要素数＜150Bを支持するが、runtimeの完全学習済み依存と個別LICENSEが未閉包なので`UNVERIFIED_BLOCK_FINAL_LOCK`を解除しない。Dramaのpickle、Mayaの外部codec、WhissleのGatedは別の停止ゲートとして改訂した。ユーザー端末や重み本体は調査していない。

**法規制と公開状態:** EUの[AI Act Article 53説明](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は条件付きopen-source例外を含み、全ての公開重みのローカル保管禁止ではない。モデルごとのGated・ライセンス・地域条項と政府の一律禁止は混同しない。将来配布制限の拡大は仮説であって確率化しない。

## 3. 変数表・H/T/D/C/UとERROR CHECK

| 記号 | 意味（日本語） | SI単位 | 定義・定義域・前提条件 | 型 |
| --- | --- | --- | --- | --- |
| N | 管理資産数 | 1 | 198 | 整数スカラー |
| A | 有効選定 | 1 | 151、SELECT53／CONDITIONAL98 | 整数スカラー |
| P_s | Prunaの固定15原本保存要素 | 1 | 49,635,347,496、R66過去数え上げ | 整数スカラー |
| P_total | Pruna全学習済み依存の真の総要素 | 1 | NULL、暗黙外部依存が未監査 | 整数またはnull |
| L | 通常パラメータ境界 | 1 | 150,000,000,000、量子化例外別途 | 整数スカラー |
| B_d | Drama3配布元全repo容量 | byte | 41,502,571,262、source APIであり実保存量ではない | 整数スカラー |
| C | HDD計画上限 | byte | 4,000,000,000,000 | 整数スカラー |
| F | 必要最低空き | byte | 200,000,000,000、未実測 | 整数スカラー |

次元チェック：P_s、P_total、Lは要素数（1）、B_d、C、Fはbyteであり混用不可。P_s＜LでもP_total＜Lとは確定しない。

**H**：4モデルは異なる原因の不確かさにより最終取得停止中。**T**：4固定repoの公開ファイル・構成索引と既存R66数え上げを比較（n_min=4）。**D**：149?ではなく151件のID結合と98件アクセス、承認0をPASSとする。外部部品・権利・実機未測定はUNCERTAIN、無承認取得やpickle実行はFAIL。**C**：作者config以外に暗黙trained weightsがある、source revision不一致、codec無害性が反証された場合。**U**：ライセンス・ownerHDD空き・PyTorch/Transformers ABI・未計数外部学習済み部品。誤差分布がないため合成u_c／包含係数kは未算定。

**ERROR CHECK**：v45 198 unique／151 active、98 conditional、Gated20、総数未確認active9、承認／本体DL／実機復元0。原本保存容量の物理的適合は未確認。学際関連：機械学習、音声生成、デジタル保存、情報セキュリティ、AIライセンス。

〈次に考える問い〉：PrunaのNULL revisionを固定した完全offline loaderと、MayaのMimi/ECAPA外部原本固定のどちらが少ない実機テストで復元条件を満たせるか。
