# v56：有効9モデルの総数停止要因／Maya2外部依存だけの追加保存計画

調査日：2026-11-20。基準は `catalog/CURRENT.json` の **v56（211資産・164有効、モデル185＋データ26）**。本書と [9件JSON](../../catalog/proposals/2026-11-20-v56-nine-active-parameter-and-repro-gates.json)、[15ファイル固定source](../../manifests/drafts/2026-11-20-maya2-mimi-ecapa-repro-deps.candidate.json) は、**取得承認ではない**。本人媒体・使用権・外部依存・実行環境を検証するまで、モデル本体の新規取得は行わない。

## 1.〈本論〉取得対象は「未保存の学習済み重み」ではなく「復元に欠ける要素」で判定

現行モデル185件のうち22件の総パラメータ判定が未確定で、有効選定内に9件。最新の [取得報告台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json) では、**Kumo-Anomaly／Kumo-Relational／Maya2 Nativeの3件がすでにVERIFIEDとして記録**されている。61モデル708ファイルの取得報告は、今回の所有者D媒体の再ハッシュではない。同じ原本を取得候補へ再追加するのは重複。

| 調査順 | repo ID／一次URL | 現在の主な根拠（出版社・Hub） | 旧ゲート | 次に実施する審査／交換判断 | 反証・未解決 |
|---:|---|---|---|---|---|
| 1 | [nvidia/Kumo-Anomaly](https://huggingface.co/nvidia/Kumo-Anomaly) | 約8MとSDK2.44Mの厳密個数差。29.6MB .pth原本は2ファイル取得報告 | 総数未確定・最終lock停止 | REHASH EXISTING AND STATIC CHECKPOINT SHAPES | Publisher static tensor census contradicts nominal checkpoint or local owner SHA differs. |
| 2 | [nvidia/Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) | 分類・回帰の2学習済み.pt、5ファイル取得報告、OpenMDW-1.1 | 総数未確定・最終lock停止 | REHASH EXISTING AND STATIC PT TENSOR CENSUS | Static checkpoint parser reveals trained weights ≥150B or local source lacks one of two heads. |
| 3 | [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | main 2,502,398,656個、13ファイル取得報告、MimiとECAPAは別配布 | 総数未確定・最終lock停止 | ADD ONLY UNREPORTED CODEC AND SPEAKER ENCODER AFTER OWNER APPROVAL | Owner archive already has identical MIME/ECAPA hashes, or listed codec/spk embedding are not actually used by pinned engine. |
| 4 | [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts) | 本体9.59M＋複数flow/encoder、auto Gated・CC BY-NC 4.0 | 総数未確定・最終lock停止 | GATED CONSENT AND NC RIGHTS FIRST NO WEIGHT LOCK | Publisher grants user-specific access and all bundled learned components/license and complete weights verified. |
| 5 | [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3) | 全expert含む主重み35,899,643,008個、音声vocoder/ライセンス別 | 総数未確定・最終lock停止 | LICENSE CODEC AND FULL MOE CENSUS BEFORE NEW SOURCE SELECTION | Codec inaccessible or same-task performance/capacity proven redundant vs verified existing TTS. |
| 6 | [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | 159MB級学習Adapterが複数。Qwen Image親/研究ライセンス未審査 | 総数未確定・最終lock停止 | PARENT AND LORA CHOICE FIRST NO DUPLICATE STEPS | Both adapter hashes identical or one step has no independent quality value; selected parent incompatible. |
| 7 | [ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | 166.9GB upstream全repoには多数の量子化重複とencoder/VAEs | 総数未確定・最終lock停止 | CHECK DONOR AND BASE LICENSE AND SELECT ONE PRECISION | Selected checkpoint equivalent to already archived parent or donor license disallows intended act. |
| 8 | [Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | 195.9GB upstream全repoはβ/v1/BF16/int8/GGUF等重複 | 総数未確定・最終lock停止 | COMPARE LTX 25 DERIVATIVE AND LICENSE BEFORE SELECTION | No reproducible quality/behavioral difference from official LTX2.5 or an already chosen variant. |
| 9 | [PrunaAI/P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image) | 主33.123B、他にprompt 9.410B・text4.438B、VAEとconnector未数。99.85GB | 総数未確定・最終lock停止 | GEOGRAPHIC LICENSE AND FULL BUNDLE PROOF BEFORE 100GB | Additional external learned tensors invalidate assumed full pipeline scope or intended territory/use not permitted. |

**反復した重み再取得は今回0件**。Kumo両モデルはローカルSHA・安全な静的 `.pt`/`.pth` 構造検査が先。`torch.load`・pickle実行・モデルコードimportを取得操作に含めない。Whissleは現時点でGatedであり、本人が許諾されるまで処理を停止。LTX2系は同repo内の異精度/異版をすべて取らず、真の独立学習差だけを選ぶ。Fish Drama3やP-H3は親・Codec・LICENSEを先に検証する。

## 2. 具体的に固定した不足source：Maya2の外部2配布元のみ

Maya2の[公式モデルカード](https://huggingface.co/maya-research/maya2-native)によれば、音声codecに `kyutai/mimi`、話者表現に `speechbrain/spkrec-ecapa-voxceleb` が必要。Maya2本体13ファイル・5,021,109,670 bytesは取得台帳にすでに報告済みで、二重取得しない。外部2repoは取得台帳に記録がないが、**ユーザー媒体に存在しないとは断定できない**。

| 外部repo／一次資料 | 固定コミット | upstream全ファイル | 件数 | 依存ライセンス |
|---|---|---:|---:|---|
| [kyutai/mimi](https://huggingface.co/kyutai/mimi) | `89091b3e466eb6a9d11e537bf26b144f194978f7` | 384,657,055 bytes | 5 | cc-by-4.0 |
| [speechbrain/spkrec-ecapa-voxceleb](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) | `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286` | 89,133,738 bytes | 10 | apache-2.0 |
| **合計（未承認）** | | **473,790,793 bytes** | **15** | 原source権利を別々に審査 |

2repoの不変revisionを公開Hub APIで照会し、**全15件のpath/bytes/Git blob SHA-1、3件のLFS SHA-256参照が一致**。音声重みファイルをこの調査中に取得したわけではない。実行環境（モデル以外のPython・CUDA・依存配布元・コードABI）、本人の利用行為の許諾、owner Dの現物SHAが残る。完全offline復元は未達。

## 3. 全パラメータ数について、条件付きの数学的上界と確定値を区別

例として `PrunaAI/P-H3-Image` は、main transformerの33.123Bだけで総数判定をしてはならない。既存v56一次調査は **33,122,992,896（transformer）＋9,409,813,744（prompt upsampler）＋4,437,815,808（text encoder）＝46,970,622,448個** の3構成を記録。残る配布元safetensorsのVAEは5,559,055,392 byte、text connectorは262,308,352 byte。

### 変数表

| 記号 | 意味（日本語） | 単位（SIとの関係） | 定義／値 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `N3` | 3学習済み部品の既知要素数 | 1（個） | 46,970,622,448 | 既知main/upsampler/encoderだけ | 非負整数スカラー |
| `BV` | VAEの未集計重量source長 | byte（情報量単位） | 5,559,055,392 | 未圧縮safetensorsを仮定 | 非負整数スカラー |
| `BC` | text connectorの未集計重量source長 | byte | 262,308,352 | 同上 | 非負整数スカラー |
| `bmin` | 最小表現bit数 | bit/要素 | 1 | 全tensor要素が最低1bitを占める場合 | 正の実数スカラー |
| `Nmax` | 5学習済み部品の上界 | 1（個） | `N3 + 8 × (BV + BC) / bmin` | 5部品ですべてを構成・外部学習依存なし | 非負整数スカラー |
| `Nlimit` | 取得除外上限 | 1（個） | 150,000,000,000 | 以上を取得候補から除外 | 非負整数スカラー |
| `Bdeps` | Maya2の外部2repo source bytes | byte | 473,790,793 | 既存Maya本体を重複取得しない | 非負整数スカラー |

1. 既知の3部品の要素数を合算し `N3=46,970,622,448` とする。
2. **仮定**：VAEとconnectorは未圧縮safetensorsで、すべての要素は最低1bit以上のデータを占め、追加の学習済み依存がない。このとき未数2部品の総数は `8 × (5,559,055,392 + 262,308,352) = 46,570,909,952` 個以下。
3. よって5部品の上界は `Nmax = 46,970,622,448 + 46,570,909,952 = 93,541,532,400 < Nlimit`。
4. **判定は条件付き**：この上界は完全pipelineに未掲載の学習済み依存がないことの証明ではなく、tensorヘッダで5部品の厳密総数を実測した値でもない。現行の `UNVERIFIED_BLOCK_FINAL_LOCK` を解除せず、ライセンス・正式lock・取得承認も不要にはならない。

**次元チェック**：`BV+BC` の単位はbyte。`8 bit/byte` を掛け `bmin(bit/要素)` で割ると要素数（無次元）となり、`N3` に加算できる。バイト数だけからモデル性能や必要VRAMは導けない。

## 4. 規制の事実／仮説と他分野への転用

米国の[2026年11月19日公式官報](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)はAI Diffusion Rule由来のモデル重みECCN 4E091を撤廃する。これは公開モデル重みの一律所有禁止を確認した事実ではなく、個別の配布者LICENSE・Gated・データ削除条件を解除するものでもない。モデル別公開停止確率や規制実施日程は作らない。

関連分野：**(1) MLシステム再現性**＝親/codec/全expertとモデル本体の分離、**(2) デジタルアーカイブ**＝元SHA・固定版・復元物の出自、**(3) 法務・技術政策**＝行為別の権利/Gated/素材の同意、**(4) 信頼性工学**＝実ディスク空き・ステージング容量・失敗時停止、**(5) 実験設計**＝出版社値と同じHW・batchの独立再試験。

## 5. H / T / D / C / U

- **H**：既存保存報告のMaya2の原本を再取得せず、不足したMimiとECAPAの正規同一hashを埋めれば、追加容量約0.474GBでoffline復元できる可能性が高まる。
- **T**：独立2repo・15ファイルの固定publisherメタデータ照合（`n_min=15`）、次は所有者Dをread-onlyでMaya13ファイル・Mimi5・ECAPA10の存在/SHA確認。最初の不一致、未承認ライセンス、容量床200GB違反で逐次停止。推論ベンチはモデル・GPU/clock・backend・quant zero-point・context/batchを固定後に別途実施。
- **D**：PASS_SOURCE＝今回の公開メタデータ15件一致。PASS_OFFLINE＝所有者実HDDハッシュ＋認可された全コード/依存＋ネット非接続の音声生成成功（**未達**）。FAIL＝SHA/権利/版不一致。UNCERTAIN＝現在の実D容量、ライセンスの具体的適用とコードABI。
- **C**：依存はすでにDにあり再取得不要かもしれない。新規の学習済み依存が別に必要かもしれない。模型の性能差が実測で価値を覆すかもしれない。
- **U**：上流sourceサイズと実占有差、baseモジュールの完全性、ユーザーが現に持つ権利・保存媒体・実行条件が主な不確かさ。統計反復測定不足のため合成不確かさ `u_c` と係数 `k` は推定しない。

## 6. ERROR CHECK と〈次に考える問い〉

- v56の211／164と有効な未知9件を参照しているだけで、既存選定は変更していない。9件内訳は既存保存**報告3・未報告6**。
- 追加sourceはMaya2外部2repo・**15ファイル・473,790,793byte・publisher LFS SHA 3件**。Maya本体の再取得申請は0件。
- ユーザー個別の取得承認0、モデル新規転送0、Torch pickleロード0、Gated回避0。全9件の最終lockは停止維持。

**次の問い**：報告済みMaya2の13原本をD上で再ハッシュしたとき、外部Mimi・ECAPAを含む「不足ファイルだけ」の正規取得計画を何ファイル／何バイトまで縮められるか。
