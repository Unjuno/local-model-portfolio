# R122｜v50継続選定：小型個人情報保護、独立MoE、無検閲差分の容量監査（2026-11-19）

**書込み範囲**：この研究成果は`strategy/2026-11-03-01-risk`専用ブランチ。比較対象`main`の正本は`catalog/CURRENT.json` → **v50、203登録／156有効（SELECT53/CONDITIONAL103）**。このブランチの古いv48を現行正本へ戻さない。過去に[取得報告された53モデル／579ファイル・270,835,576,267B](../../catalog/execution/2026-11-19-acquisition-ledger.json)を無条件に再取得しない。今回所有者Dドライブを再ハッシュしたわけではなく、`queues/approved.json`は空。


**同日正本更新の追認**：調査開始時の比較元`main`はv50（203登録/156有効）だったが、執筆中に`v51-20261119`（**204登録/157有効、CONDITIONAL104**）へ更新。[DaisyRose-27BのBF16原本は正式にR1/conditionalへ採用済み](https://github.com/Unjuno/local-model-portfolio/blob/main/docs/strategy/122-v51-daisyrose-27b-original-selection-and-supply-risk-2026-11-19.md)。固定40桁revision`293a7a2ab54aaea78098ee917c546390667521dc`、34ファイル・55,586,309,473B、親Qwenと異なる重みSHA18/18という資料を追加確認した。DaisyRoseを当ブランチから重複登録しない。引き続き同条件の実利と予算・本人の取得権を評価する。

**取得準備キューとの照合**：さらに`main`の[15配布source重複排除キュー](https://github.com/Unjuno/local-model-portfolio/blob/main/queues/proposed-v50-r122-deduplicated-next15-sources.json)では**15 source repo／12独立学習結果＋データセット2＋コードのみ1／332ファイル／374,701,109,177B**を候補とし、同じ固定ソースの重複**179,484,014,188B**を除外した。これは`GO_AFTER_LOCAL_PREFLIGHT`のメタデータ分類であり、2026-11-19時点のD実容量・合法取得・本人承認ではない。新v51のDaisyRose BF16はこの15 source集合に含まれていないため、追加時には容量とsource identityを別途再計算する。

## 1.〈本論〉目的から逆算した追加・交換判定

研究目的は**将来再構成が難しい独立学習結果・専門能力・元コードと依存を、正当な権利と実容量の範囲で保存すること**。単なる「無検閲」「新しい」「人気」「低bit化」を独自学習成果とみなさない。規制の仮説を法的取得権・緊急性に変換しない。

| 新規または重複候補repo ID | 確認した一次URL／日付 | 現在確認できた配布制限・原本 | 独自性と次の決定 | 反証条件と未解決事項 |
| --- | --- | --- | --- | --- |
| [gravitee-io/bert-small-pii-detection](https://huggingface.co/gravitee-io/bert-small-pii-detection) | [作者カード](https://huggingface.co/gravitee-io/bert-small-pii-detection)、[固定commit](https://huggingface.co/gravitee-io/bert-small-pii-detection/commit/f8c27a85c51c0168f07b9dcf00265bf0a4097939)、2026-11-19照合 | Public・license tag Apache-2.0。28.5M要素（HF概数）。`model.safetensors` **114,116,788B**、Publisher SHA-256=`a6319abf8718ec15956b241e8800b0ff4b6b8be5c6b5aa2a43aef765c6e20de3` | **P0・次版へのCONDITIONAL新規追加提案を確定**。英語25種類のPIIエンティティ検出に独立fine-tuned学習済み重み。3形式のうちFP32 Safetensors原本のみ保存基準、ONNXとINT8 ONNXは別モデル登録しない | 25ラベルのドメイン別F1、個人情報の誤検出/見逃し、全選択ファイルSHAと学習依存の確定。既存処理が同条件で代替可能なら優先度低下。正規LICENSE行為別確認前の取得不可 |
| [maxwell-model/Maxwell-V1-Flash](https://huggingface.co/maxwell-model/Maxwell-V1-Flash) | [作者カード](https://huggingface.co/maxwell-model/Maxwell-V1-Flash)、[原本ファイル一覧](https://huggingface.co/maxwell-model/Maxwell-V1-Flash/tree/main)、2026-11-19 | Public、tag Apache-2.0、[固定commit](https://huggingface.co/maxwell-model/Maxwell-V1-Flash/commit/ca536c4380e0600d6aebdb808d2ce65ec724161b)。HF総36.8106B（非活性expert含むmeta値）／作者は埋込み除外35B全体・3B active。35 safetensors分割を含むrepo表示約**73.6GB** | **P1・独立事前学習MoEとして研究優先、容量HOLD**。学習済みMBSA、mHC、256 experts、MTPは既存Qwen系の通常量子化ではない | `config.json` は`rope_theta=20,000,000`／`max_position_embeddings=524,288`、作者仕様表はRoPE=10,000,000／sequence=262,144。意図的なconfig上限か設定差か要照会。custom Python/ABI、35分割SHA、正確な全MoE tensorと空き容量が未検証 |
| [RadixArk/DaisyRose-27B](https://huggingface.co/RadixArk/DaisyRose-27B) | [作者2026-11-18発表](https://huggingface.co/blog/RadixArk/daisyrose-27b-pushing-the-frontier-of-post-trainin) | Public・Apache2.0タグ、27.7814Bの親系譜。本人利用規約/固定hash未確認 | **v51でR1/conditional正式採用済み、重複登録不要**。作者Terminal Bench 4.1 pass@1 5.6→12.0、144×H200・18日・1,200 tasksという著者条件 | v51で固定34files／55,586,309,473B／20 publisher LFS SHA、18シャードの親対応SHA一致0と記録。本人実機の独立再ハッシュと後学習効果の比較は未実施。BF16/FP8/NVFP4を3重登録しない |
| [ConwayResearch/Underdog-Saluki-27B-1.0](https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0) | [原配布カード](https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0)、2026-11-19 | Public・**CC BY-NC-4.0**。作者称する約7.89GB/2bitのQwen3.8 GSQ-RCO派生 | **P2・小容量tool-calling実行用候補HOLD**。独立学習か単なる2bit serving派生か未証明。商用・別目的の権利確認が先 | 著者の120題比較は独立測定でない。同HW/RAM、llama.cpp、batch、quant zero-pointと親版をそろえて比較、明確な差がなければ追加しない |
| [huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF) | [patch全分割](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF/tree/main/patch-unsloth/patch-unsloth-all)・[静的patchスクリプト](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF/blob/main/patch-unsloth/patch-unsloth-Qwen3.8-27B-dec.py)、2026-11-19 | Public・Apache2.0 tag。patch-allは**約65.6GB・6 GGUF分割＋key**。最後の637MBだけでは全層差分を再構築できない | **P2・無検閲独立差分HOLD**。既存Interpretic/RVNとは編集元・形式が異なり得るが大容量。patch元の`unsloth`重みも同一revisionで確保する必要 | スクリプトはmissing tensorを黙ってコピーする経路があり部分patchを完全保全と誤認する危険。6 shardとkey、元重み、SHA、コードの安全性と既存2系統に対する実測差が揃うまで登録・取得しない |
| [facebook/meta-encoder-v1](https://huggingface.co/facebook/meta-encoder-v1) | HF公式repoメタデータ、2026-11-19 | 28.4318B metadata、**LICENSE tagが確認できない** | **P1研究・HOLD権利確認先**。画像/文書/動画の検索embeddingは独立学習成果候補 | LICENSE正文、作者配布条件、必要重み・専用tokenizer、容量、既存埋込みとの検索指標で優位を確認 |
| [ConwayResearch/pii-30M-mlx-4bit-v1.1](https://huggingface.co/ConwayResearch/pii-30M-mlx-4bit-v1.1) | HF公式メタデータ、2026-11-19 | public、CC BY-NC-4.0。gravitee PIIを親とするMLX4bit版 | **P3・別原本として採用せず**。量子化やformat移植のみなら元の学習済みモデルはgravitee原本で保全 | 別途の再学習重み・性能改善・独自権利が一次資料で証明されれば再審査。正確な総数未確定につき取得準備STOP |
| [EdgeFirst/yolo26-det](https://huggingface.co/EdgeFirst/yolo26-det) | [NXP i.MX95向け作者紹介](https://huggingface.co/blog/EdgeFirst/yolo-imx95-neutron) | public AGPL-3.0、TFLite/ONNX NPU形式、総パラメータ未確認 | **P3・本人HW未確認のため延期**。i.MX95 2 TOPS/多フレームなど作者の実機ベンチは汎用PC/一枚処理性能の根拠ではない | 同一学習成果の単なるNPU formatなら重複。原本、ライセンス、所有HWと学習済み総数を確定するまで取得準備STOP |
| [perplexity-ai/pplx-decider-v1.3](https://huggingface.co/perplexity-ai/pplx-decider-v1.3) | 配布元HFモデルメタデータ、2026-11-19 | Public・Apache-2.0 tag・26.0853B metadata | **P3・既存小型Flashとのタスク重複により見送り**。`perplexity-ai/pplx-decider-flash-v1.3`はv50でconditional済 | 同条件の非生成的判断精度・span抽出が小型Flashでは達成できないことを検証すれば復活 |

**予測シナリオと現在の区別**：提供者によるrepoの削除、Gated化、ライセンス改定はあり得るが、いずれの上記モデルについても個別の近日禁止日や禁止確率を確認していない。HF Gated仕様 https://huggingface.co/docs/hub/models-gated、EU GPAI open-source FAQ https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source、米BIS https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology は公開ウェイト一般の国内保管禁止を確認する資料ではない。アクセス不可が直ちに政治的検閲・規制確率増大を意味しない。

## 2.〈応用・転用例〉具体的な交換と取得順序

- **確定する選定方針**：小型独立PII原本`gravitee-io/bert-small-pii-detection`を次版への**conditional候補**にする。重み原本1個114,116,788Bと設定/語彙類7ファイルの非実行[固定候補manifest](../../manifests/drafts/r122-gravitee-pii-original.candidate.json)を作成。ONNXとquant ONNXは後日必要に応じたservingフォーマットであり3つの別資産にしない。publisher全fileハッシュ・本人権利・学習済み総数の精密censusが未了なのでダウンロード可能な最終lockではない。
- **大型原本の交換候補**：Maxwellは独自アーキテクチャの価値が高いが、既存Qwen3.5-35B-A3BやGranite MoEと比較してから一つの重複性の高い汎用checkpointと交換するか判断。既存保管ファイルを確認するまで削除しない。v45の古いsource proxy約3.732TBと3.8TB管理目安との差は約67.84GBだったが、そこへMaxwellの約73.6GBを無条件追加するのは**仮試算でも余裕を超える**。v50の本当の最終占有値は149資産分の選択容量が未確定であり、歴史的余裕を実空きと取り違えない。
- **無検閲の代替**：現行保全方針のInterpretic高精度BF16/MTP原本と0bserverx RVN-F16を優先（[R121](121-v49-strict150b-ledger-aware-download-selection-2026-11-19.md)）。Huihuiのfull patchは元の`unsloth`重み＋6 shardが必要で、単体637MB追加を同等原本としてカウントできない。DaisyRoseはv51で正式条件付き選定されたが、拒否抑制そのものではなくコード/agent RLが主題なので「無検閲枠」の代用品にしない。
- **150B以上絶対停止**：v50の`orcarouter/Qwen3.8-Flash-Next-Uncensored`約180Bと`mistralai/Mistral-Large-4-1T-A52B`約1.05Tは、quantized例外を認めず候補外。全パラメータ未確認モデル22件（うち有効9件）は非実行調査のみ。MoEの3B activeや量子化容量を総パラメータ数の代わりに使わない。

## 3. H/T/D/C/U：最小検証と不確かさ

**H**：モデル原本の独立性と専門タスクを重視すれば、既存モデルの形式差分を追加するより新しい能力被覆率が増える。第一の反証可能対象は、PII originalのドメイン特異的誤検出率、見逃し率、再現性。

**T**：PIIは最初に公開元40桁revisionの7選択ファイルを完全publisher byte+SHA照合し、依存LICENSEと現在のreadiness検査を完了。権利ある公開・合成PII文例を英語200件以上（保護対象ごとの陽性/陰性を分け、各主要ラベルの検証サンプル不足を明示）準備し、token/char spanごとのmicro F1・precision・recallと偽陰性件数を比較。評価端末のCPU型式、クロック、OS、Transformers/tokenizers/PyTorch/ONNX backend/quant zero-point、batch=1、最大512 tokens、モデルrevisionを固定。同条件の比較基準はregexと既所蔵NER。逐次停止は権限違反、学習済み総数不明、SHA mismatch、200GB安全床違反時に即停止。モデル性能未測定、試験は今後の条件設計。

**D**：`PASS_RESEARCH`＝出版社原本weight sha+sizeとrepo固定、非重複の新学習タスクを資料で確認。`UNCERTAIN_STOP`＝未検証license、外部重み、選択全file byte/SHA、所有者容量、性能ベンチ。`FAIL`＝150B以上、無許可Gated取得、重みの偽SHA一致、同一format重複を独立重みとして加算。現時点の`queues/approved.json`は空で、**取得PASSは0**。

**C（破れ方）**：PIIの英語外精度劣化、未知記号や合成体の誤認識、Maxwell作者表のRoPEとconfig値の不一致による復元失敗、Huihuiの欠落patch silently fallback、既存モデルの同等精度による冗長化、作者の正規配布制約変更。

**U**：実HW/backend/driver、text normalization/tokenizationとラベルの定義差、Publisher表の外部評価データ漏洩、権利・削除条項、HDD file system・重複計数が主な不確かさ。現在試験分布と標本分散がないので合成標準不確かさ`u_c`と包含係数`k`を数値化しない。規制確率も推定しない。

### 変数表（数式の意味と単位）

| 記号 | 日本語の意味 | 単位（SI） | 定義 | 範囲／前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `P_total` | モデルの総学習パラメータ個数 | 1（無次元） | 非活性expert、embedding、MTP含む全学習重み | 非負整数。不明はnull、active値の代用禁止 | 整数スカラー／null |
| `P_cap` | 除外閾値 | 1（無次元） | 150,000,000,000個 | `P_total >= P_cap`で絶対除外 | 整数スカラー |
| `B_original` | PII original重みの保存bytes | byte（B） | 114,116,788B（publisher SHA固定） | 選択パッケージ全体とは異なる | 整数スカラー |
| `B_repo` | Maxwell原本repoの出版社表示容量 | byte（B） | 約73,600,000,000B | 表示丸め、全選択ファイル未確定 | 近似実数スカラー |
| `B_old_margin` | 古いv45 proxyの容量余白 | byte（B） | 67,835,247,038B | 過去資料の仮定、v50実容量でない | 整数スカラー |
| `P` | Precision（適合率） | 1（無次元） | 作者発表0.8182 | 0～1、同一評価集合 | 実数スカラー |
| `R` | Recall（再現率） | 1（無次元） | 作者発表0.9256 | 0～1、同一評価集合 | 実数スカラー |
| `F_1` | 調和平均F1 | 1（無次元） | `2PR/(P+R)` | `P+R>0`、同一評価集合 | 実数スカラー |
| `u_c` | 合成標準不確かさ | 評価量の単位に依存 | 試験分散と誤差源から推定 | 今回未測定 | 未定義／非負実数 |
| `k` | 包含係数 | 1（無次元） | 区間推定の必要精度に応じ設定 | 今回非適用 | 未定義／正実数 |

**数値例・単位チェック**：出版社表から`F_1 = 2×0.8182×0.9256 / (0.8182+0.9256) ≈ 0.8686`。分子・分母とも無次元なのでF1も無次元。これは配布者の同一テスト分布での数値であり、日本語・新業務データの品質保証ではない。`B_repo`と`B_old_margin`はともにbyteだが、歴史的`B_old_margin`と新規保存可能容量の等価性は**未立証**。

## 4.〈応用・転用例〉学際的連携と次アクション

- **機械学習・評価統計**：種類が異なる訓練済み原本と同じ重みの推論量子化を分離、PIIのPrecision/Recallのtradeoffを定量化。
- **デジタル保存工学**：原本と復元依存の閉包、SHA-256・Git blob SHAと固定revisionの比較、媒体故障時の再現。
- **ソフトウェア供給網**：Maxwell custom codeやHuihui patch Pythonは静的監査まで実行禁止。codec/ABI/backendやWindows/Dドライブの安全床を検証。
- **情報法・プライバシー**：PII検出の正当な利用/管理、音声・画像の肖像/著作権、Gated認可とNC/AGPL利用条件を分ける。

## 5. ERROR CHECK

関連JSONは[9件の個別根拠と反証条件](../../catalog/decisions/2026-11-19-r122-v50-small-specialists-moe-uncensored.json)、PIIの[選択7ファイル候補マニフェスト](../../manifests/drafts/r122-gravitee-pii-original.candidate.json)。当作業ブランチの古いv48正本は変更せず、外部でv50→v51（204件・157有効）の正式追加を確認、DaisyRoseを二重登録していない。当ブランチが新たに提案したのは**次版PII条件付き追加の提案1件**のみ、Maxwell・Meta Encoderは権利/容量研究、Daisyはv51採用を追認し実効差を追試待ち、Huihui・Underdogは重複性能/原本差分HOLD。形式再包装2件と特定NPU1件と大Decider1件は新規追加不要。150B絶対除外2件と総数不明22件は維持。今回の重量ファイル転送0、モデル実行0、本人D直接確認0、承認0。Exaは使用枠超過で本回使えず、HF配布元・元コード・一次公開先を検査した。

## 6.〈次に考える問い〉

「PII原本とONNX形式」を別資産として数えず原本115MB級だけ先に保全するなら、残り容量をMaxwellの独自アーキテクチャへ使う価値は、既存MoEの実測タスクをどの程度上回れば十分なのか。
