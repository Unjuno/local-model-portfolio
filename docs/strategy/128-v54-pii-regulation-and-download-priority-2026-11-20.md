# R128｜v54: 小型プライバシー原本の選定交換・実取得台帳・規制リスク再評価（2026-11-20）

> **対象**：`Unjuno/local-model-portfolio`。本調査の書込み先は以前指定された `strategy/2026-11-03-01-risk` ブランチのみ。読み取り比較した `main` の正本は `catalog/CURRENT.json` → **v54-20261120**（207登録、160有効、SELECT53/CONDITIONAL107）。当ブランチの`CURRENT`は歴史的v48のままで、古いポインタを現行v54として書き換えない。既存資産の削除や取得の承認はしていない。

## 1.〈本論〉現行モデルの事実、監査エラー、次の選定

2026-11-20のread-only GitHub照合により、現行v54のモデル181・データ26、150B未満のモデルPASS **157**、150B以上の現行量子化例外審査 **2**、パラメータ総数UNVERIFIED **22**（うち有効9）と確認。`catalog/CURRENT.json` の `expected.parameter_gate.PASS_TOTAL_PARAMS_LT_150B=158` と、実体 `catalog/effective-portfolio-2026-11-20-v54.json` の実数157が不一致。181=157+2+22で実体は整合する。

**修正案**：`main`側で現在のblob/revisionを比較した後、対象の期待件数を**158→157だけ**修正する。モデル単位のステータス、選定、権限の自動更新は不要。防止策として [版非依存カウントテスト](../../tests/test_r128_dynamic_parameter_gate.py)を本ブランチに追加（既存の古いv48でも正しくPASSし、v54のズレを検出する設計）。**この作業ではmainへの修正コミットなし**。

厳格な150B上限：MoEの非活性expert、embedding、外部学習済み部品を含む総数が**150B以上で絶対除外**。v54の`orcarouter/Qwen3.8-Flash-Next-Uncensored`180B、`mistralai/Mistral-Large-4-1T-A52B`約1.05Tは量子化例外を認めない。総数不明22件も取得準備STOP。現行ポートフォリオの量子化実行例外ポリシーは、この厳密なユーザー制約に不適合であり本調査では無効。

## 2. 〈採否〉小型・専門モデルの選定交換（出版社一次資料）

| repo ID／一次URL（確認日：2026-11-20） | 総数／公開制限 | 独自能力・実容量 | 優先・反証・未解決 |
| --- | --- | --- | --- |
| [Horizon-Labs/pii-redactor-small](https://huggingface.co/Horizon-Labs/pii-redactor-small) | **140.7M**。公開非Gated、Apache-2.0、LICENSE/NOTICE有 | **37言語（日本語含む）・29検出分類**。独立ModernBERT PII/secret検出。FP32原本562,671,180B＋必須tokenizer34,363,288B＝**597,034,468B**の2大ファイルを固定。Publisher [SHA256SUMS](https://huggingface.co/Horizon-Labs/pii-redactor-small/blob/a20835db9e671267b21a2951f5bf2c76e4901708/SHA256SUMS)に原本ハッシュ公開 | **次期正式CONDITIONAL追加の第一提案**。固定revision `a20835db9e671267b21a2951f5bf2c76e4901708`。全ソースの選択容量、権利と日本語精度、owner D実測は未完。既存小型モデルの同条件性能が上なら再評価 |
| [gravitee-io/bert-small-pii-detection](https://huggingface.co/gravitee-io/bert-small-pii-detection) | 28.5M、public、Apacheタグ。単独LICENSEはroot一覧で確認できず | 英語専用25 PIIラベル。モデル原本114,116,788B SHA256 `a6319abf8718ec15956b241e8800b0ff4b6b8be5c6b5aa2a43aef765c6e20de3` | **前R122の第一採用案を、超小型英語対照原本候補へ引き下げ**。日本語・複数言語機能ではHorizon優位の可能性。RAM/英語精度が決定的なら復活 |
| [OpenMed/privacy-filter-multilingual-v2](https://huggingface.co/OpenMed/privacy-filter-multilingual-v2) | 総**1.3996B** MoE（50M active）。public、Apacheタグ | 16言語・54細分PII分類、v2の新学習成果。repo約2.83GB、作者ラッパーが`trust_remote_code=True`を使用 | **HOLD**：追加細分ラベルの便益、Viterbi・custom code・完全LICENSEと版対応を確認。日本語条件で明確な独自精度が出た場合のみ上位 |
| [Horizon-Labs/pii-redactor-base](https://huggingface.co/Horizon-Labs/pii-redactor-base) | 307.6M、public、Apacheタグ | 同作者の高精度大版v1.0。作者の4つの別言語評価F1平均0.898、small v1.1が0.883 | **HOLD**：重複大、追加原本と保存容量の費用対効果を同条件で検証。日本語で実用上の改善が有意なら再審査 |
| [maxwell-model/Maxwell-V1-Flash](https://huggingface.co/maxwell-model/Maxwell-V1-Flash) | 総36.8106B MoE、active約3B、public Apacheタグ | 独自MBSA/router系。公開repo約73.6GB、custom modeling code | **HOLD容量・ABI**：既存MoEと重複比較し、全35シャードSHA、RoPE設定の差異、実4TB空きを検証するまでは交換・取得準備しない |
| [huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF) | 親総約27.8B、派生Tensor閉包未確定 | 拒否方向の別編集だがpatch-allは約65.6GBの6分割＋キー、元Unsloth原本が必須 | **HOLD**：小さい末尾637MBのみの保存は不可。正規の親／全patch SHA／安全な再構成とInterpretic/RVNとの差分評価が揃うまで追加しない |

**重要：性能値の証拠階級**。Horizon small作者の四つの外部公開評価集合（アラビア・フランス・韓国・トルコ）を用いた平均redaction F1は**0.883**、同作者が同じ手順で評価したgraviteeは**0.491**。これは「外部コーパスに対する作者測定」であり、外部機関による独立追試ではない。日本語はこの4言語表に含まれず、**日本語の実精度向上を確認済みとはしない**。その作者自身も実文書へのdomain drift、過剰マスク、再識別を限界としている。[一次モデルカード](https://huggingface.co/Horizon-Labs/pii-redactor-small)。Horizonは学習データのCC BY 4.0由来NOTICEも保存する。

**学習済み原本と変換形式**：Horizonで保存する第一候補はF32 Safetensors＋固定tokenizer、LICENSE/NOTICE、config、検証用SHAと静的コード。ONNX 2形式は同じ学習済み重みの推論変換であり別の学習成果として数えない。固定12ソース候補は[候補マニフェスト](../../manifests/drafts/r128-2026-11-20-horizon-pii-v11-original.candidate.json)。大容量2ファイルの整数byteとハッシュは公開元で照合済み、残る小ファイルの正確な総容量と本人ローカルSHAは未完。`redact.py`/`llm_guard_conf.py`は未審査コードにつき取得しても自動実行しない。

## 3. 次の取得候補は形式重複を排除して段階化

2026-11-19の実行台帳は**61モデル／708file／409,835,119,252byte VERIFIEDを報告**（1件Gated HOLD）。この研究環境ではowner Dドライブを独立再ハッシュしていない。旧53件という件数は歴史値。正本`queues/approved.json`は空、取得承認は0。

| 段階 | 固定source範囲 | source容量と判定 |
| --- | --- | --- |
| 0：現物検証 | 61件の既報告ファイルを読取専用でSHA再検算 | 新規取得ゼロ。実保存先が同一revision/ファイル集合である証拠が先 |
| 1：小型独立能力と付属物 | Rumble ASR 1.386GB、ELYZA 7.607MB、Aya 140.160MB、報告済RWKV/iLLaDA/TRELLISの付属12file計367,838B、Horizon FP32+tokenizer最低597.034MB | **2,131,168,306byte＋未確定のHorizon小ファイル分**を第一トランシェの候補に選ぶ。重要：**下限**であり確定DL容量ではない |
| 2：独立専門・音声 | ZONOS3-Mini完全原本15,345,816,226B、出版社公開SenseNova GGUF19,338,124,279B | 完全Codec/vision等と、SenseNova公式Gated原本との差を確認。GGUF単独をMTP完全原本と呼ばない |
| 3：無検閲2系統の高精度原本 | Interpretic v2 BF16全32file＝55,586,056,799B、0bserverx RVN-F16 3file＝53,808,326,934B | 計**109,394,383,733byte**。既存Q4取得報告とは別の重みSHA。RVN-F16はSafetensors再構成元だが、その前の訓練時BF16とは断定しない。従来の量子化品を検証前に削除しない |
| 4：大きい専門原本 | Fara1.5 27B、Hy-Memory30B-A3B、必要なら動画・画像原本 | 正規LICENSE、全依存、選択容量、4TB最終総計とピーク一時領域が確定するまで保留 |

既存の[15配布ソースに関するR125差分候補](../../queues/proposed-v52-r125-ledger61-delta-next15.json)は**287ファイル／327,549,073,014byte**。旧重複控除47,152,036,163byteは過去のpublisher SHAに照らした取得候補の削減であり、物理Dドライブ容量が同じ量だけ空いたことを証明するものではない。新v54 REMORYやv53 Aion、v51 DaisyRose、v52 coding LoRAも正式CONDITIONALであり、同一元Qwen重みの重複や他の投資判断を差し引く前に無造作に容量加算しない。

## 4. 規制に関する確認済み事実と未来仮説

**事実**：米国BISの2026年11月19日施行の[91 FR 74970～74999、IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は、旧AI Diffusion Ruleのmodel-weights専用ECCN 4E091等を撤廃した。一方、半導体/データセンター/特定用途等の管理は別途残る。EU委員会の[GPAIオープンソース例外FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は提供者の義務・例外を説明するのであり、一般利用者の全ウェイト保管を禁止した宣言ではない。[HF Gated仕様](https://huggingface.co/docs/hub/models-gated)では作者は個人アクセスを取消できる。

**予測／不確実**：将来的な著作権申立て、license改定、host gating、危険能力に関する個別配布制限は起こり得る。ただし、ここに記載した各原本について政府が具体的な禁止を予定しているとの一次証拠はない。数値的規制確率・停止日を作らず、「リスクを高く推定した」ことを無許可DLやtoken共有の理由にしない。Exaは2026-11-20の調査でもHTTP402で利用枠超過、配布者公式ページと政府一次資料で代替した。

## 5. H/T/D/C/U と変数表

**H：反証可能仮説**。Horizon smallがgraviteeより日本語における直接識別子の再現率を高め、英語で精度を著しく損なわない。資産選定価値とは区別し、実運用前に同条件テストする。

**T：最小検証**。権利ある日本語文書200件以上＋英語200件以上、匿名化／公開の別のデータソースを使い、個々のPII spanラベル、長さ別、数字・記号・会社名・住所・氏名・API keyを層化。最低各言語200件の同一文書について、Horizon vs graviteeをpaired比較し、character-level redaction recall/precisionとmicro F1、偽陰性の件数を記録。評価端末のCPU/GPU・クロック・OS・Torch/Transformers/tokenizers版、tokenizer長512、batch1、dtype FP32、推論backendと推論コンテキストを固定。200件に達するまで性能の途中判定で停止せず、不正許可・ファイルSHA不一致・保存媒体200GB床違反なら即時中止。

**D：PASS/FAIL/UNCERTAIN**。保存対象選定PASS＝第三者の原本と異なる学習済みcheckpoint、総数150B未満の根拠、正規publisher固定版、保存価値がある固有PII能力。運用上の条件付きPASS＝日本語recall差のpaired 95%区間下限が0より大きく、英語precision低下が事前許容範囲0.03以内かつ必要な最低安全要件を満たすこと（**この0.03は採否用事前規則で、実測値ではない**）。FAIL＝違法取得、重み不一致、150B以上、無許可Gated回避。現状は個人権利、全bytes、実HDD、実運用評価が未済なので取得判定`UNCERTAIN_STOP`。

**C：破れ方／対立仮説**。Horizonの作者ベンチマーク構築者バイアス、実際の日本語書類での過剰マスク、token spanアライメント差、別のより小さいMLX/ONNX servingで同等性能、既存の軽量ルールによる高精度、あるいは依存licenseの用途制限。

**U：不確かさ**。データ収集バイアス、labelsの定義差、モデルカードからの推論、SHAの出版社値とOwner実測の差、ファイルサイズ・キャッシュ、driverやABIを主要源とする。反復と分布を未測定なので合成標準不確かさ`u_c`と包含係数`k`は数値化不能であり、適当な分散や規制確率を記載しない。

### 変数表（単位・範囲・型）

| 記号 | 意味 | SI単位・量 | 定義 | 定義域・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `N_{model}` | 現行モデル数 | 1（無次元） | 181 | v54固定 | 整数スカラー |
| `N_{pass}` | 150B未満と分類された数 | 1（無次元） | 157（実体記録より） | v54、厳格な取得許可とは別 | 整数スカラー |
| `P_{total}` | モデル全学習済み要素数 | 1（無次元） | 非活性expert含む全パラメータ個数 | 非負整数。不明はnullで取得STOP | 整数／null |
| `P_{cap}` | 除外パラメータ閾値 | 1（無次元） | 150,000,000,000 | `P_{total} >= P_{cap}`なら絶対除外 | 整数スカラー |
| `B_{side}` | 3モデル付属ファイル差分 | byte（B） | 367,838 | Publisher候補、現物欠落未証明 | 非負整数スカラー |
| `B_{data}` | ELYZA＋Aya候補ソース | byte（B） | 147,767,193 | Publisher source固定 | 非負整数スカラー |
| `B_{ASR}` | Rumble候補ソース | byte（B） | 1,385,998,807 | 全19ファイルのpublisher値 | 非負整数スカラー |
| `B_{H}` | Horizon大ファイル2件 | byte（B） | 597,034,468 | 全package容量ではなく下限 | 非負整数スカラー |
| `B_{small}` | 第1段階の既知source下限 | byte（B） | `B_{side}+B_{data}+B_{ASR}+B_H` | 不明な他のHorizon小型ファイルを除く | 非負整数スカラー |
| `B_{free}` | 所有者Dドライブの空き容量 | byte（B） | 今回未観測 | 0以上、staging時に再計測 | 非負整数／null |
| `B_{floor}` | 最低残空き | byte（B） | 200,000,000,000 | 安全床、temp領域は別 | 非負整数スカラー |
| `R_{JA,H}` | Horizonの日本語redaction再現率 | 1（無次元） | 独立日本語テストの真PII文字数に対する捕捉割合 | 0〜1、現在未測定 | 実数／未定 |
| `R_{JA,G}` | graviteeの日本語再現率 | 1（無次元） | 同一文書・同一正規化規則 | 0〜1、現在未測定 | 実数／未定 |
| `u_c` | 合成標準不確かさ | 測度の単位 | 試験誤差から推定 | 未測定 | 非負実数／未定 |
| `k` | 包含係数 | 1（無次元） | 所望信頼水準を定める | 未設定 | 正実数／未定 |

**数値チェック**：`B_small=367,838+147,767,193+1,385,998,807+597,034,468=2,131,168,306 byte`。すべてbyteで加算し、**ソース下限**であることを明示。学習済み総数は`157+2+22=181`でモデル件数と整合する。再現率差`R_{JA,H}-R_{JA,G}`も無次元。GPUピークRAMの測定値やdisk空きの代用ではない。

## 6. ERROR CHECK／学際的適用

- **統計評価**：ドメインシフトとpaired confidence interval、出版社測定と独立評価の区別。
- **AIアーキテクチャ**：PIIスパン分類とprompt-injection分類のタスク差、MoEの総数とactive値、重み原本とONNX形式。
- **デジタルアーカイブ**：SHA256／40桁revision／train依存グラフとオフライン復元、重複容量削減の測定。
- **法学・プライバシー工学**：LICENSE、CC-BY NOTICE、学習元データの出所、個人情報の扱い、Gated個別権限と新しい法令。

**実施結果**：R128判定JSON／Horizon固定マニフェスト／本報告／版非依存カウントテストをブランチ内に記録。v54の207/160、61検証報告、150B除外2、総数不明22、P0小型source下限2,131,168,306byte、全ソース権限未承認を静的に照合。**実重み取得0／許諾変更0／既存資産削除0／main更新0／モデル性能ベンチマーク未実施**。Owner Dの実ファイルとストレージはここから見ていない。

## 7.〈次に考える問い〉

**0.6GBの独立PIIモデルを保全することは、既存の27B無検閲派生をもう1セット高精度で保存することより、アーカイブ全体の復元可能な独自能力をどれだけ広げるか。** 答えは出版社名や「無検閲」タグでなく、重複重みのSHA・測定能力・利用可能性から決める。
