# v32：小容量・独立学習成果3件の正式研究選定（2026-11-14）

対象：GitHub `Unjuno/local-model-portfolio` の **main**。起点v31（179件／有効132件）を一件も削除・採否変更せず、3モデルをCONDITIONAL研究として追加し、**v32全182件／有効135件**を機械可読で作成。

- [現行正本](../../catalog/CURRENT.json)／[v32全件](../../catalog/effective-portfolio-2026-11-14-v32.json)／[追加3件の個別採否](../../catalog/revisions/v32-2026-11-14.json)
- [未承認取得候補135件](../../queues/proposed-v32-2026-11-14.json)／[必須部品調査135件](../../catalog/preparation/2026-11-14-insurance-bundles-v32.json)／[CONDITIONAL 82件のアクセス状態](../../catalog/access/2026-11-14-v32-conditional-hub-gates.json)
- **変更を含むのは論理選定、調査台帳、テスト、説明文だけ。ダウンロード済み、権利同意済み、実機推論成功の意味ではない。取得承認0を維持。**

## 1. 対象の選定評価

| 原本repo | 採否 | 既存から見た保存価値 | 保管する表現／外す表現 | 一次資料 |
| --- | --- | --- | --- | --- |
| [Tencent DSpine-b16](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | **CONDITIONAL** | 既存[Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)のBF16/GGUFコピーではなく、専用の5層・16トークンドラフター2.0259B。既存のLiquidAI DSparkは別ターゲット・別訓練 | `model.safetensors` 約4.05GB、`config.json`、LICENSE/README、[公式コード](https://github.com/Tencent/DSpine)を固定。既存親の二重取得、安易な変換形式は外す | [モデルファイルとXet SHA](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/main/model.safetensors)、[公式論文 arXiv:2609.36173](https://arxiv.org/abs/2609.36173) |
| [NVIDIA Nemotron 3 Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization) | **CONDITIONAL** | ASR/TTSではなく話者の時系列分離・同一性追跡を学習した99.2M原本。最大8話者、AOSC/FIFO話者キャッシュ | `model.safetensors` 約397MBを基本。native `.nemo` 約199MB、GGUF約107MBを無理由に複数保存しない | [公式カード](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/main/README.md)、[重みXet SHA](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/main/model.safetensors)、[Transformers](https://huggingface.co/docs/transformers/main/model_doc/nemotron3_diarization) |
| [NVIDIA RFD4-Proteína](https://huggingface.co/nvidia/RFD4-Proteina) | **CONDITIONAL** | 配列と全原子構造のFlow生成＋対応Autoencoderを統合した435,622,465要素。既存の構造予測や埋め込み器とは別学習成果。現在のreleaseはLoRAマージを含む | root `model.safetensors` **1,742,660,596 byte**とconfig/provenance/LICENSE。106GB repoにはbase/adapter/native ckpt、評価Oracle、runtimeイメージ等が混在。Base＋LoRAの別訓練状態は研究目的で個別に検討 | [公開元マニフェスト](https://huggingface.co/nvidia/RFD4-Proteina/blob/main/release-checkpoints.json)、[BSD3条文](https://huggingface.co/nvidia/RFD4-Proteina/blob/main/LICENSE) |

### 学習済み原本と形式違いの境界

DSpineはQwen原重みの精度違いではなく、別途学習されたドラフト予測器。話者分離は単なるASR後処理ではない。RFD4はrootのFlow＋AE bundle、Base checkpoint、独立LoRA、旧世代checkpoint、ネイティブ形式に分かれる。**同じ学習済みテンソルの再パッケージは二重カウントしないが、別学習済みBase＋LoRAは必要性を個別審査する。**

RFD4の本体には別リポジトリの訓練用データ全量**約2.13TB**を含めない。出典： [RFD4原著者の学習データ一覧](https://huggingface.co/datasets/nvidia/RFD4-Proteina)。再学習用データ保全は容量と個別の著作権・原データの来歴を別途審査し、モデルをダウンロードしただけで学習データの取得権限が付くと推定しない。

## 2. 実装条件と性能の根拠階級

- DSpine作者測定のWorkBuddy Code/low aggregate throughput：AR **253.35**、DFlash2 **590.27**、DSpine **686.23 token/s**。**SGLang 0.5.22、BF16、FlashAttention3、concurrency=8、ReplaySSM**。これは単一ユーザーのdecode token/sや改善確率ではない。GPU機種、clock、zero-point、KV実装、長文の実端末品質、独立測定が欠けるため実用保証しない。[原カード](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/main/README.md)
- NVIDIA Diarizationの**80msは最小入力バッファ**であり、エンドツーエンド遅延・実測WER/DERではない。NeMo/Transformers/NeMo-Speech.cppの版、OS、stream chunk、batchを独立に記録。[原カード](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/main/README.md)
- RFD4 root bundleは作者の2026-10-19版、latent 32・147種類の残基語彙。旧版はlatent 16・33種類で**FlowとAEを交換できない**。開発元はLinux x86_64、Python3.12、CUDA13系の実行前提を記載。モデル約1.74GBをピークGPUメモリと解釈しない。[正確なSHAと構成](https://huggingface.co/nvidia/RFD4-Proteina/blob/main/release-checkpoints.json)
- Gatedについては既存79件の配布元確認を保持し、今回公開メタデータで未Gatedだった3件を追加。82 CONDITIONAL中17がGated。**それ以外のSELECTやHOLDまで公開済みとは推定しない。本人の権利・利用条件全文の承認は全件0。**

## 3. 収録を見送った候補と負の根拠

| 候補 | 今回の判断と棄却ではない理由 |
| --- | --- |
| [IFM/PAN2](https://huggingface.co/IFM/PAN2) | **HOLD研究**。29.2Bの物理世界シミュレーション独立原本だが、上流86.2GB、Qwen3.5-9B/Wan2.2部品のハッシュ一致・第三者ライセンス・Cosmos等に対する独自性が未決。候補として残し、容量が空いているという理由だけで追加しない |
| [MiniMax H3 Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | **HOLD研究**。既存Pruna P-H3-Imageとは学習済み状態が別だが、204GBには複数の重み形式。公式[LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image/blob/main/LICENSE)はEU/英国/韓国/米国を標準許諾対象外とし商用/Hostedサービスの条件もある。利用地域と行為を確認するまで一括取得しない |
| RFD4の外部学習データ | **今回のセットから除外**。別の2.13TB原典・別の許諾・保存目的。Flow+AEモデルのオフライン生成に不要 |

## 4. 容量監査と単位

| 記号 | 意味（日本語） | SI単位 | 定義／定義域と前提 | 型 |
| --- | --- | --- | --- | --- |
| N | 正式選定台帳の資産総数 | 1 | v32: 182、非負整数 | 整数スカラー |
| A | SELECTまたはCONDITIONAL数 | 1 | v32: 135、0以上N以下 | 整数スカラー |
| P | モデル全学習済みパラメータ数 | 1 | 非活性expert・必要な別学習部品を含む。予備公開値は最終計数でない | 整数/null |
| B | 固定ファイルと必要依存の最終保存byte | byte | v32ではnull、選択完了前は合計しない | 整数/null |
| C | 計画上限 | byte | 4,000,000,000,000、実ディスク値ではない | 整数 |
| F | 保存後最低空き | byte | 200,000,000,000、キャッシュ/既存ファイルは別 | 整数 |
| H | 今回の新規予備予算（3件分） | byte | 9,700,000,000、見積予約上限で実測ではない | 整数 |

本研究で新規3件に設定した**9.7GBは予備計画枠**。公開元表示のDSpine約4.05GB、Diarization約397MB、RFD4の正確なroot約1.743GBは**モデルファイルに限った部分値**。これらを「135件の完成アーカイブ総量」や「HDD残空き」と同一視しない。

次元検査：N/A/Pは無次元、B/C/F/Hはbyte。同じSI単位の値だけを容量として比較し、パラメータ数とファイルサイズを直接加算しない。量子化のビット数でMoE全パラメータ数は減らない。

## 5. 最小反証試験・停止条件（H/T/D/C/U）

- **H 仮説**：この3件は同じ学習状態の単純変換ではなく、既存汎用/特殊モデルでは喪失時に再生成できない独立価値がある。
- **T 最小検証**：n_min=182のID全件照合／新3件について公開元の完全40桁revision、選択全ファイルのサイズとSHA256、ライセンス全文、ターゲット・Codec・Flow/AE依存、実行コードABIを静的に確認。推論は別承認の下で同一HW・clock・backend・context・batchの30反復＋所定の音声DER、Flow整合、ドラフト受理長評価。
- **D 合否**：PASS＝明確に異なるtrained-stateと権利・全SHA・依存・物理空き・別途明示承認が揃った時のみ個別取得可。FAIL＝同一重みの形式だけの重複、違法取得、必須モデル欠落、SHA不整合。その他UNCERTAIN。
- **C 破れ方**：既存にbit-identical同一学習状態が存在する、DSpineターゲットに互換でない、NeMo/GGUFのラベル精度が異なる、RFD4 AEが不一致、契約・第三者資料が許容しない。
- **U 不確かさ**：公開Hubのmutable main、RFD4追加部品、HW・ABI・本人の権利、実ファイル残量・通信途中複製。統計観測がないため合成標準不確かさu_cと包含係数kの数値は未確定。

**ERROR CHECK**：v31の179件を採否含めそのまま保存、v32でID重複0／追加3／182資産（モデル156・データ26）／有効135（SELECT53、CONDITIONAL82）／UNKNOWN20・150B超例外研究2・新3件PASS研究のみ／Gated部分台帳82中17・取得承認0。実機・モデル本体・クラウドの操作0。

学際的接続：**MLシステム高速化**（DSpine）、**音声処理とプライバシー保護**（Diarization）、**構造生物学・分子設計**（RFD4）を、同じ原本重み／依存／正規許諾管理の枠組みで保全できる。

〈次に考える問い〉：新しい大規模ワールドモデルをさらに登録する前に、現在の135件から実際に合法的な固定取得パッケージへ昇格できる独立資産は何件あるか。
