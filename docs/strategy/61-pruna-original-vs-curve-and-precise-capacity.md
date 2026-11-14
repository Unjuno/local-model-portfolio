# R61｜Pruna P-H3 原本の保全とComfyカーブ形式の厳密比較（2026-11-14）

[現在のmainの選定正本](../../catalog/CURRENT.json)は **v32・182件／有効135件**。本研究では「Prunaを33B vs 20Bという表示差で誤判定し、元重みを捨てる」ことを防止する。データは[機械可読R61](../../catalog/research/2026-11-14-r61-pruna-source-curve-capacity.json)、非実行の[原本/代替表現候補](../../manifests/drafts/r61-pruna-original-and-comfy-comparators.candidate.json)を参照。**新モデル登録・採否変更・ダウンロード・許諾受諾は0。**

## 1. 不変ソースの元checkpoint全44件を固定

**[PrunaAI/P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image)** の源コミット `7f98acef503cf2bcfba821a78cb1cf1a9928b2df`。元repo54ファイルからデモ・ベンチの画像10ファイル `assets/` だけを外し、**44ファイル**（重み15、Config・tokenizer・NOTICE・README・LICENSE等29）を保全候補として選定。

| 対象 | Source byte（十進） | 判定 |
| --- | ---: | --- |
| 元の重み15ファイル | 99,797,308,280 | 高精度original trained state。Transformer7、Text Encoder2、Prompt Upsampler4、Connector1、VAE1をすべて含む |
| 元repoの選択44ファイル | **99,840,428,064** | 再現性のメタデータ込み。推論コード、実GPUと外部パッケージは別 |
| 同一ソースファイルSHA/Git blobで重複を除いた固有部分 | **99,828,998,036** | 正確な同一ファイル名違い5組を1回だけ保管できる場合の仮想物理容量（ファイルパスは保持） |
| 元の過去選定上限 | **105,000,000,000** | 保存予算枠（ユーザーの実HDDとは別）。元ソース部分は枠内 |
| 上限から上記44ファイルを引いた仮の余裕 | 5,159,571,936 | python/runtime、cache/staging等を含む本当の空きではない |

同一データ5組には`processor/tokenizer.json`と`tokenizer/tokenizer.json`（同一LFS SHA256・11,422,650 byte）、他Config/テンプレートの同一Git blobが含まれる。合計**11,430,028 byte**の厳密な重複だけを除去可能。Safetensors以外のGit blob SHA1はSHA256と混同しない。

## 2. Comfyは独立再学習ではなく、元重みの変換・圧縮実装

[Comfy版の公式配布源](https://huggingface.co/PrunaAI/P-H3-Image-Comfy)は`base_model_relation: quantized`を宣言する。一方、[Pruna Diffusers](https://huggingface.co/PrunaAI/P-H3-Image)の`transformer/diffusion_pytorch_model.safetensors.index.json` は**638テンソルキー・66,280,430,080 byteの記録データ**、実Transformer7ファイル合計 **66,280,504,088 byte**。推論クラスは`MiniMaxH3Transformer3DModel`、num_layers50・hidden_size5376・time_embed_dim2688。

**原因がコードで判明**：[固定ComfyUIモデル](https://github.com/Comfy-Org/ComfyUI/blob/eee59185ff4f43ae2d9ad122b245619d27d9daad/comfy/ldm/minimax/model.py)は`adaln_t_table`の存在により、時刻埋め込みのfull-width AdaLN学習済み重みを小さな共有カーブで置き換える設計。[固定model_detection](https://github.com/Comfy-Org/ComfyUI/blob/eee59185ff4f43ae2d9ad122b245619d27d9daad/comfy/model_detection.py)はカーブあり/なしで別経路。これにより**約20B級Comfy BF16は元33B級Diffusersと同一ファイル/同一内部表現ではない**。開発元の[技術解説](https://www.pruna.ai/blog/oss-p-h3-image-launch)も約40%の時刻条件ブロックを小さくしたと述べる。**損失ゼロの逆変換、全重みの復元、同一品質は証明していない**。

2026-11-11の[ComfyUI issue #17692](https://github.com/Comfy-Org/ComfyUI/issues/17692)には「MiniMax H3 Image元BF16をそのままComfyに入れるとsilent color noise」との**利用者報告**がある（Prunaを対象にした独立再現試験ではない）。複製を実行できるという断定ではなく、**同じ名前のモデルでもbackend/ABIと形式対応の監査が必須**という反証例として保存する。

## 3. 実行形式の必要な重量だけを計算

| Comfyの構成（元repo SHA `44a0fb73f299da1bb715bdb5ff59ce3fd3c6f543`） | 補完器なし・3重み | 補完器込み・4重み |
| --- | ---: | ---: |
| BF16 | **55,165,475,664** | **74,471,781,216** |
| INT8 | 29,480,935,784 | 39,229,053,508 |
| W4A8 main + Text、INT8 VAE | **20,084,601,325** | **26,808,697,441** |

**追加に必要な学習済みPrompt Upsampler**は同じrepoでBF16 19,306,305,552byte／INT8 9,748,117,724byte／W4A8 6,724,096,116byte。省略しても詳しいプロンプトの基礎画像生成パスを残せるが、短い自然言語指示からの公式標準生成能力を失う。**作者の「20GBの最小構成」は補完器なしの3重み**であり、通常の4重み完全workflowを20GBと誤表示しない。作者サンプルのW4A8本体＋BF16補完器は 39,390,906,877 byte。性能・品質・HW評価は一切未実測。

Comfy開発元のピークGPUメモリ目安は8MP、batch1のBF16 core約56GB、INT8 core約31GB、W4A8 core約21GB。ただしruntimeのComfy commit、comfy-kitchen kernels、CUDA/driver、GPU clock、CPU offload/precision、zero-pointは本人実機で固定できていない。BF16からINT8/W4A8への量子化は独立学習成果ではない。

## 4. 最終保全方針と停止条件

**結論：今は元Pruna Diffusersの44ファイルを1つの保存候補として維持し、Comfy形式を追加の独立資産にしない。** Comfy版しか動かないPCで利用したい場合に限り、1種類の表現を別途実行用に選ぶ。価値判断は保存目的（高精度元trained state）と実用目的（小容量・高速化）で分ける。

取得STOP：MiniMax H3 Community Licenseの地域/用途/Noticeと第三者Qwen componentの原文確認、Diffusers 0.42.0.dev0ソースとtokenizer/processor/Comfy runtime固定、上流ファイルを利用者が合法的に取得できること、物理HDD空き200GBと実容量上限、ユーザーの承認。現在の138資産?? **現行は182／有効135で変更なし**。他134有効資産の完成度は別で、本R61だけで全体の容量収束を宣言しない。

## 5. H/T/D/C/U・単位とERROR CHECK

| 記号 | 意味（日本語） | SI単位 | 定義／型／範囲と前提 |
| --- | --- | --- | --- |
| B_0 | 原本44ファイルの論理バイト | byte | 99,840,428,064、整数スカラー・非負 |
| B_u | Source identical blob/LFSを一意化したbyte | byte | 99,828,998,036、整数スカラー・同一hash only |
| B_c | Comfy三重みの選択量 | byte | dtypeごとのcore列、整数スカラー・別オプションを同時足さない |
| B_a | 補完器を加えたComfy四重みの選択量 | byte | 同一dtype/互換構成のfull列、整数スカラー |
| N | 原本必要ファイル数 | 1 | 44、整数スカラー・重複パスも維持 |
| C | 4TBの計画上限 | byte | 4,000,000,000,000、実ディスク計測と別 |

単位チェック：B_0/B_u/B_c/B_a/Cはいずれもbyte、Nは無次元。保存後の実空き200GBもbyteで別条件。

**H**：Compressed AdaLN curveは原本のtrained-stateを損失ゼロで完全復元できるとは限らない。**T**：公式Hub 2固定repo、Comfyコード・Diffusers indexのソース照合、元54ファイル中必要44件と同一ハッシュ群5つをチェック。**D**：同一ソースSHA・サイズと正確なファイルbytesの判定はPASS、Comfyから原本完全復元はUNCERTAIN、通常量子化形式を別モデル追加ならFAIL。**C**：同一表現への可逆変換が後で証明される、同じ形状を持つ別学習状態が存在する、ランタイムが旧checkpointをサポートしない。**U**：Tensor値の実検証・契約適合・性能測定・HDD残空き不明。合成標準不確かさu_c／包含係数kは未算定。

**ERROR CHECK**：v32の182資産、SELECT53／CONDITIONAL82・有効135件、取得承認0件は不変更。mainに資料と非実行候補・検証テストのみ反映。異なるdtype/圧縮版を無条件に複数保存することを推奨しない。参照先はMLシステム／高精度量子化・ソフトウェアABI／デジタル長期保全・ライセンスを横断。

〈次に考える問い〉：元の学習済み情報を落とさず保存する要件を優先する場合、Comfy変換後の曲線表現だけを残すことに合理的な証拠はあるか？
