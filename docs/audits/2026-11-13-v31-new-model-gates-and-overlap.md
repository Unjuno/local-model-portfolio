# v31追加監査：Gated正規化、DSpine/PAN2、MiniMax H3 Image（2026-11-13）

対象：`Unjuno/local-model-portfolio`・`strategy/2026-11-03-01-risk`・固定監査HEAD `e60a31e4625a9ea12db429bd3a8e8335b132270c`。**非実行の監査証拠であり、現行採否、承認キュー、実機、モデル本体は変更しない。**

## 1. 監査上の重大不整合：Gatedフィールドの自由文字列

現行v31は**179件（モデル153、データセット26）、有効132件（SELECT 53/CONDITIONAL 79）**。公開元再監査 `catalog/proposals/05-v31-conditional-selection-review.json` のCONDITIONAL79件にはGated **17件**。一方、`observed_access === "gated"` の完全一致で数えるとCONDITIONALでは**16件**。`gradium/phonon-40m-multilingual` の現行値は `Gated auto (anonymous metadata); user authenticated gate permission NOT verified` であり、**実際はGatedにもかかわらず単純フィルタを通過する**。このミスは取得キュー生成の誤承認につながる。

**P1修正提案（まだ実装せず）**：自由文章 `observed_access` は来歴として維持し、`upstream_access_status` を `public / gated_auto / gated_manual / unknown` のenum、`owner_access_authorized` を `true / false / unknown` として別管理。両者未確認はfail-closedでダウンロード不可。Gatedでもライセンスと依存と本人承認は独立ゲート。

## 2. 既存v31と今回の新規／既調査候補

| repo ID | 正式v31収録 | 本監査の保存判定 | 一次資料・保存上の理由 |
|---|---|---|---|
| [tencent/Qwen3.8-27B-DSpine-b16](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | なし | **CONDITIONAL研究追加提案** | 2.026B級・repo表示4.05GB、既存Qwen3.8-27B用に独立訓練した5層・16 token/8192 windowドラフター。単なる量子化ではない。原Qwenは重複取得せず固定依存にする |
| [IFM/PAN2](https://huggingface.co/IFM/PAN2) | なし | **CONDITIONAL研究追加提案** | 公開源86.2GB（独自Transformer67.4GB＋Qwen系Encoder15.9GB＋VAE2.82GBなど）。約29.2B表示の映像世界モデルで既存Cosmos/Wanとの差分検証価値がある。MBZUAIのApache-2.0と第三者Wan2.2/Qwen3.5の権利を別管理 |
| [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | なし | **HOLD・対Pruna原本比較/権利調査** | 元の33.1B画像DiT。repo全量204GBは複数形式を含む。公式の選択構成表示を足すと外部text encoder込み約135.355GB（rounded）で、完全取得量ではない。v31のPrunaAI/P-H3-Imageは別の蒸留済み学習成果で、単純量子化コピーではない |
| [meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | なし | **既存R33研究を再利用** | [v28固定容量監査](../strategy/44-v28-pinned-source-capacity-2026-11-08.md)に既出。再発見として二重登録しない |
| [thinkingmachines/Inkling-2-Small](https://huggingface.co/thinkingmachines/Inkling-2-Small) | なし | **150B超・HOLD** | 配布元に594B総/17B活性と明記。活性数で上限判定しない。量子化例外の同一条件メモリ・実測証拠なし |

## 3. 性能・ABI・ライセンスを混同しない

- **DSpine**: [Tencent公式実験](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/main/README.md)はSGLang `0.5.22`、BF16、FlashAttention3、同時8、ReplaySSM。WorkBuddy Code/lowのトークン合計/経過秒はAR **253.35**、DFlash2 **590.27**、DSpine **686.23 token/s**。作者の同一条件測定であってユーザー実機や1スレッド性能ではない。GPU機種/clock不足・独立再現なし、タスク成功率を証明しない。
- **PAN2**: [配布元カード](https://huggingface.co/IFM/PAN2)は自前のコード・重みをApache-2.0、Wan2.2/Qwen3.5-9B等は元の許諾に従うと区別する。元データの許諾と生成再現性、公開ファイルのSHA一致が未確認。既存Wan派生とはファイルと学習状態を照合してから容量を共有する。
- **MiniMax**: [2026-11-10公式LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image/blob/main/LICENSE)はEU/UK/韓国/米国を標準ライセンス地域から除外（日本をその一覧に含まない）。地域外への配布禁止など追加条件あり、モデルカードだけでは本人の利用適合を断定できない。正式LICENSEが11月11日更新されているため**重みとライセンスの同一revision固定**が必須。選択形式は `transformer/` と `transformer_diffusers/` を無根拠に両方取らない。公式の新しいH3-Image LICENSEと既存Pruna派生のH3 Community LICENSEは同名だから同条件と決めつけない。
- **既存収録の確認**: `robbyant/lingbot-touch-tiny` はv29以降CONDITIONAL、`nvidia/GR00T-N1.7-3B` はv31 [既存NVIDIA調査](../strategy/55-nvidia-rare-archival-mechanisms-2026-11-13.md)対象。再登録しない。

## 4. 実際の保存準備ギャップ

v31有効132件のうち**最終固定取得コミット/選択ファイルbyte未登録が各130件**。総パラメータ数不明は有効7件。正式取得承認は**0件**。過去の選択容量調査はあっても最終lock済みという意味ではない。4TB計画上限、最低空き200GBを維持し、v27の既知ソース重複除去3.417685TBを全179件の実容量とみなさない。

## 5. H/T/D/C/U・単位／ERROR CHECK

| 記号 | 意味（日本語） | 単位（SI） | 定義・定義域/前提 | 型 |
|---|---|---|---|---|
| N | 正式研究資産数 | 1 | v31の179、非負整数 | スカラー |
| A | 正式有効資産数 | 1 | v31の132、0以上N以下 | スカラー |
| G | Gated数 | 1 | CONDITIONAL対象のHF再監査17、非負整数 | スカラー |
| B | 選択ファイル保存量 | byte | 構成未固定ならnull、非負整数 | スカラー/null |
| C | 保存容量計画上限 | byte | 4,000,000,000,000、実ディスク未測定 | スカラー |
| F | 保存後最低空き | byte | 200,000,000,000 | スカラー |
| P | 全学習済みパラメータ数 | 1 | 全MoE expert・依存を含む総数、未確認null | 整数/null |

**次元検査**：N/A/G/Pは無次元、B/C/Fはbyteで同次元。容量とパラメータ数の同一視禁止。

**H**：アクセス状態が自由文字列なら単純フィルタでGatedを見落とす。独立学習済みドラフターや世界モデルは重複量子化ではない。
**T**：v31全179件一意、条件付き79件の現行公開元監査とカタログ文字列を全照合。新モデル2件、H3原本1件、旧調査1件、150B超1件を公式カード・LICENSE・ファイル一覧で検査。実機推論ゼロ。
**D**：正常化Gated全件正しく阻止、独立学習の確認がPASS。誤った非Gated扱いや同一重みを重複取得する場合FAIL。依存・ライセンス・SHA・性能不足はUNCERTAIN。
**C**：親・子でtrained-stateが実は同一、Gatedステータス更新、基準HW・batchでドラフト性能再現不能、ライセンスの新revision変更。
**U**：更新日、外部LICENSE、未確定モデル依存、実HDD、SHA一致。測定分布・誤差源の定量データ不足で合成標準不確かさu_cと包含係数kは未算定。

**ERROR CHECK**：179資産一意、SELECT53/CONDITIONAL79、総数不明7（有効）、Gated公開元17対厳密一致16（Phononの表記差）。今回正式採否は不変更、ダウンロード/許諾/実行0。

〈次に考える問い〉：未採用の大型原本を増やす前に、最も価値の高い有効資産の固定SHA・依存・権利をどこまで確定すれば、重複を増やさず取得可能にできるか？
