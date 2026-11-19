# R121｜v50：小型多言語ASR原本の正式選定と保存順序・取得停止（2026-11-19）

## 1.〈本論〉— 正式に追加したモデルと理由

**正式選定：[`Reson8/Rumble-2-Flash`](https://huggingface.co/Reson8/Rumble-2-Flash)を1件、R2/CONDITIONALとして追加。** v49の202登録／155有効から**v50=203登録／156有効（SELECT53・CONDITIONAL103）**へ進める。v49で既に選定された`sensenova/SenseNova-Loop-9B`のGated原本を含めて202件の採否は**変更せず、既存ファイルの削除0**。ダウンロード権限を付与したわけではない。

### なぜRumbleなのか

2026-11-18公開の[出版社公式技術説明](https://huggingface.co/blog/rumble-2-flash)で、**45言語**のASR原本と、追加学習済みのCTC headを提供。Qwen3-ASR系アーキテクチャだが、配布元が別学習した本体重み・CTC headを備える。既存の`Qwen/Qwen3-ASR-1.7B`や`openai/whisper-large-v3-turbo`と同一学習済み重みの別量子化ではなく、新しい学習成果として容量増分が約1.386GBであるため保存する価値がある。

| 項目 | 一次証拠に基づく記録 |
|---|---|
| Publisher repo | `Reson8/Rumble-2-Flash` |
| 不変40桁revision | `a0c34287229103b706c670d70791683e34379732` |
| 選択source | **19論理ファイル／1,385,998,807 byte** |
| 重量source | `model.safetensors` 1,017,318,776 byte／`ctc/ctc_head.safetensors` 357,476,284 byte |
| Publisher SHA256 | main `6dc35af40ad150e50767382a9d401eb9af9c3a1ad4e915c61fe05aecfa79a3e1`／CTC `c13befc1c60a8410185a730cdccefc825df12ac8af75d4411fdff8106291ede7` |
| 他の原本ファイル | 17 Git blob SHA-1参照、LICENSE、processor/tokenizer、ctc_head.py、CTC vocabを含む |
| アクセス・タグ | 公開・非Gated・Apache-2.0（ただし本人の目的別権利とコード依存は未確認） |
| 固定ソース台帳 | [R115 Publisher不変manifest](../../manifests/drafts/r115-v48-rumble2-flash-and-nemotron-sigma-original.candidate.json) |

モデル作者はH200/vLLMでOpen ASR英語WER6.60%、中国語・欧州言語・ヒンディー語等9言語評価の平均6.96%を公表。**「全45言語の平均」ではない**。著者の7,000 RTFx以上は十分なバッチがあるときの報告で、端末GPUやCPUのバッチ1・低遅延性能は未測定。CER/WER・速度とベンチマーク数値を混同しない。

## 2.〈応用・転用例〉— 配布条件と原本の優先順序

[正式source提案キュー](../../queues/proposed-v50-r121-master-sources-17.json)は以前の16件にRumble19ファイルを加え、**17件・256ファイル・104 LFS SHA256・303,234,274,385 byte**。11件を`GO_AFTER_LOCAL_PREFLIGHT`、6件をHOLDと表示するが、これは研究用メタデータの分類であって**ダウンロードの明示承認ではない**。正本v50の156有効全体を網羅したサイズでも、所有者Dドライブの実占有量でもない。Sensenova Gated別ファイルscopeは旧16件には含まれず、これをpublic 17件sourceと混同しない。

| 次の調査順 | モデル | 判断 |
|---|---|---|
| 1 | 既存取得ログに載る53モデル | まず現物ファイルを独立再ハッシュ。GitHubの`VERIFIED`報告を完全offline復元の証明としない |
| 2 | [SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B) | v49採用済み。作者原本Gated21件の一つであり本人の正規承認、full MTP/vision/ABIの確定を優先 |
| 3 | Rumble-2-Flash | **v50選定確定、source選択固定。** CTC tensor census・コード安全性、個人LICENSE、同条件の日本語CERを次に閉じる |
| 4 | [harness-hub/Qwen3.8-27B-pi-adapted](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) | 独立RL-LoRAの原本、親`Qwen/Qwen3.8-27B`と正確なadapter revision/SHAを固定。融合55GBを二重アーカイブしない |
| 5 | [NVIDIA Sigma](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B)、[Apple FastFrames](https://huggingface.co/apple/FastFrames-S)、[LongCat Avatar](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6) | 特殊能力を保留研究。独自LICENSE・コードABI・親学習済み依存・不要な大容量派生を先に除外 |

別系統の無検閲`0bserverx` RVNと`InterpreticAI` v2は維持。同じRVN学習結果から生成された`RVN-F16.gguf`と再構成Safetensorsを**二つの独立学習成果として数えない**。高精度マスター追加と、すでに保存報告のあるQ4実行形式の重複は別条件で審査。

### 権利・保存実務のSTOP

- 個人のGated承認、ライセンス正文と親/データ/アダプターの行為別許可を確認。
- Git/LFS SHAと選択pathを固定し、既存現物と本当に一致するなら再ダウンロードしない。未知のコード`ctc_head.py`やPyTorch pickleを自動実行しない。
- 4TBの現物保存媒体・フォーマット後の空き、cache/staging最大量、200GB安全残床を検証。GPU/CPU、driver、Transformers/vLLM/PyTorch、batch/context/zero-pointを固定する。
- `queues/approved.json`が空の限り**今回も新規モデル重量を取得しない**。過去取得台帳は**53 VERIFIED報告・579ファイル・270,835,576,267byte**だが、当作業ではowner媒体を独立再ハッシュ・offline復元していない。

## 3. 技術的検証：変数表・次元

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・範囲・前提条件 | 型 |
|---|---|---|---|---|---|
| `N_m` | main学習済み要素数 | 1（無次元） | 508,631,552 | HF main safetensors metadataのみ | 非負整数スカラー |
| `B_c` | 別学習済みCTC headファイル長 | byte（非SI単位） | 357,476,284 | 固定source、厳密CTC tensor census未完 | 非負整数スカラー |
| `N_u` | 公開原本ファイルの要素数に対する保守上界 | 1（無次元） | `N_m + 8 B_c`、bit/element換算 | 各格納パラメータは最低1 bit、隠れた独立学習済み外部重みは別審査 | 非負整数スカラー |

保存ファイルを最低1bit/要素とする上界スクリーンは`N_u = 508,631,552 + 8×357,476,284 = 3,368,441,824`で、150B基準を下回る。**厳密な全CTCパラメータ数ではない**。次元はbyte×8bit/byte÷1bit/要素＝要素数、`N_m`と加算可能。必要RAM/VRAMと品質はこの計算では推定できない。

## 4. 規制の事実／仮説とH/T/D/C/U

**法制度の事実**：[米BISの2026-11-16遠隔計算資源規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は、公開weightsの一律ローカル所持禁止とは同義ではない。[EU AI Act GPAI Open Source FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)の提供者義務/例外も保管禁止と同一視しない。**未来の削除・Gated化**はリスクシナリオであり、確率を根拠なしに推定しない。今回ExaはHTTP402で失敗し、Exaで一次調査済みとは主張しない。

**H**：Rumbleは同一量子化の再包装ではなく、新しい学習済み小型ASR＋CTCを追加するので保存対象の多様性を増やす。

**T**：19 publisher filesとrevision/sha/source bytesの静的チェック。今後、30件以上×日本語・英語・雑音の評価音声を、同一HW・clock・backend・batch1・context/前処理条件でWhisper/Qwen3 ASRと比較し、CER/WER、中央値のRTFx、ピークRSS/VRAM、推論品質の区間を保存。逐次停止は権限/ハッシュ/安全床違反で直ちに停止。

**D**：PASS＝v50の202→203、一意のモデルID、19固定sourceを保存候補として選択。FAIL＝承認前の新規転送、違法なGated回避、既存量子化の独立学習成果への二重計上。UNCERTAIN＝本人権利、CTC厳密総数、実機品質、offline restore。

**C**：独立の後学習原本が実際には旧Qwen3-ASRの重みと実質同一、または既存ASRが同一容量で総合的に優越するなら採否見直し。

**U**：出版社H200フルバッチ値と利用者実環境、メタデータ/学習済み外部依存、権利、実際のモデル挙動が主要誤差源。反復観測未実施のため合成標準不確かさ`u_c`と包含係数`k`の数値化不可。

**ERROR CHECK**：v50は203登録・156有効（SELECT53／CONDITIONAL103）、Gated21件、総数未確認active9件据置。17個のpublisher original source候補256files/104 SHA/303,234,274,385bytes、新規DL承認0、今回の重量実取得0。GitHub資料の静的検証だけでPython推論試験は未実施。

関係する分野：**多言語音声認識・転移学習、デジタル長期保全と内容ハッシュ、ソフトウェアサプライチェーンとABI、AI配布政策・著作権**。

## 5.〈次に考える問い〉

新規ASRの独立した重みを保存する価値を、既存Whisper/Qwen3-ASRと同一日本語・雑音データでどの最小性能差／追加学習可能性によって反証可能にするか。
