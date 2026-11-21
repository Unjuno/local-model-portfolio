# R150｜v63/99取得済み報告後：小型Heretic差分と意思決定モデルの採否再評価（2026-11-22）

> **状態**：非実行の一次資料研究更新。正式正本は依然として `v63-20261122`（235登録・188有効＝SELECT55 / CONDITIONAL133）、取得報告99モデル、`queues/approved.json`は0件。**新規weight取得0、ユーザー実HDD編集0、正式SELECT追加0**。承認行為は生成しない。

- [個別の比較判断と検証ゲート](../../catalog/research/2026-11-22-r150-tiny-heretic-and-decision-specialists.json)
- [最優先小型LoRAの公開元固定SHA研究manifest](../../manifests/drafts/r150-2026-11-22-qwen0p8b-heretic-lora-two-unique-weights.candidate.json)
- [前回から維持する11件非実行キュー](../../queues/proposed-v63-r149-after99-11-research-only.json)
- [旧SOV固定ソース全シャード](../../catalog/research/2026-11-18-r102-sov-transcribe-original-and-dflash.json)

## 1. 今回の選定判断：最重要は6.17MBの可逆差分

**研究最優先（未正式採用）**：[nchapman/Qwen3.5-0.8B-Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA/tree/92e2ae29c379d7378c696511ec9c70ace8be1434)。独立の出版社コミット`92e2ae29c379d7378c696511ec9c70ace8be1434`を確認。root `adapter_model.safetensors` **1,073,240byte**（LFS SHA256 `269cee632d7b2dc1cb5163d6f1b2a378df3b2130e51c8b08c686709997c28679`）と別Pareto `pareto/trial_004_ref6_kl0.0275/adapter_model.safetensors` **933,248byte**（SHA256 `26836a1374eb43aef39f04970b558f347a62558ebce8c0e00388ff217146ba6e`）の**異なる2つの学習済みLoRA差分**が含まれる。**異なる trained-state 合計2,006,488byte**。root と `pareto/trial_002_ref4_kl0.0714/adapter_model.safetensors` の重みSHAは同一。GGUF版3本は変換物であって独立学習成果を増加させない。6.17MBは変換物・メタデータ込み出版社UI丸め値であり、完全原本保存範囲の厳密byteではない。

作者のHeretic v2.1／MPOA rank 3、46 residual projectionへのLoRA編集、`mlabonne/harmful_behaviors test[:100]`で原本拒否93/100→root 4/100、もう一方6/100。通常プロンプトfirst-token KLはroot 0.0714 nats、別差分0.0275 nats。**これは作者の単一プロトコルであり、独立の同条件安全・推論品質テストではない**。既存SELECT `Qwen/Qwen3.5-0.8B`を前提に差分のみの保存余地があるが、**所有者実HDD上の親のrevisionとSHA、PEFT/vLLM/llama.cpp量子化・zero-pointとadapter ABIは未確認**。

**対照候補**：[darrellbest/Qwen3.5-0.8B-Heretic](https://huggingface.co/darrellbest/Qwen3.5-0.8B-Heretic/tree/fe1b6c084607d8b75f013d41bbf4b95cc9ea9109)。1.78GBの完全checkpoint、vision encoder と MTP、36個のF32特殊tensor保全を作者が明示。拒否98→15/100、思考型算術/文章題は原本26/40、改変27/40。一方、より強い拒否低下を目指した編集は10/40に劣化したという作者の対照観測。**nchapmanの4/100拒否を理由にdarrellbestより総合的に優秀と結論しない**。最初は6.17MB差分を固定する価値が高く、1.78GBフルコピーの新規取得はベンチ比較までHOLD。

## 2. 新型意思決定の固有性と容量

| 新モデル | 出版社ファイル容量（概数） | 技術価値 | R150 |
|---|---:|---|---|
| [baselabs/bison-1](https://huggingface.co/baselabs/bison-1) | **65.4GB** | 31B dense、校正済み非生成 decision、公式カードにAA Decision Index 76・Brier 0.14 | **HOLD** |
| [baselabs/groundhog-1](https://huggingface.co/baselabs/groundhog-1) | **53.1GB** | 26B総数・約4B active MoE、128k文書・確率分類 | **HOLD** |

両者は同じ**6.71M decision訓練セットの派生兄弟**。品質証拠は非対称で、groundhog単体のAA Decision Indexはまだ記載なし。既存の意思決定専用モデルとの同条件比較がない段階で両方を買う／保存する判断は不合理。後日一方だけに絞るか、既存で十分なら双方棄却する。元モデルGemma4とBaseten改変部分にApache2+MIT権利条件が共存する（`LICENSE`/`NOTICE`を確認）。

## 3. 既検討モデルを二重採用しない

[R102](102-v44-canonical-ledger-repair-sov-asr-hold-2026-11-18.md)で全37files・54GB近い原本と任意DFlash（親に依存）を固定済みの **Salesforce SOV-Transcribe-1** は引き続きHOLD（旧34file候補53,315,653,534byte）。既存Whisper/Qwen3-ASR/Graniteとの同条件評価と`trust_remote_code`安全監査なしに採用しない。**ci-proto** も既に[R105](105-v45-raon-simons-original-preservation-2026-11-18.md)でHOLD。約1.34GB／167M×2原本は有用だが、`ci-proto Code and Model Licence` §10に外部配布・サービスの帰属/通知義務があり、Simons297Mとの比較及びcheckpoint loader安全監査がないため維持。**初発見ではなく再審査**である。

2026-11-22の最新uncensored検索にはDaisyRose27BとInkling2Mini派生の新名称が大量に存在。しかし既存portfolioに同じ親モデル群があり、新しいファイル名・GGUFだけでは独自学習結果を証明できない。既存 `saidutta69/LFM3-VL-2B-heretic` は親 `LiquidAI/LFM3-VL-2B` とセットでR149キュー研究中。似た名前のHereticコピーを自動置換しない。

## 4. 取得順位を確定するうえでの停止条件

1. **S0**：99件実取得報告の所有者ローカルSHAを再照合。特に `nvidia/RFD4-Proteina` の旧revision対報告取得revisionの重み差は別学習scope。既存を消去しない。
2. **S1**：約6MBの新規LoRA原本2差分を非実行manifestとして固定（今回の作業）。残りの非重み全pathのbyte/OID、親revision・LICENSE/NOTICE、作成者評価再現を完成して初めて個別の正式候補を判定。
3. **S2**：既存[R149 P0 4 repo](../../queues/proposed-v63-r149-after99-11-research-only.json)（Cactus mirage／Timestral28M／KittenTTS pico／Aurora2）**2,234,744,280byte**の選定候補は引き続き優先し、別の取得計画へ無断変更しない。
4. **S3**：P1親+heretic、P2動画／decisionの必要実行条件を比較。P3 Ripple65BはHOLD。

「個別モデルをダウンロードすべき」という**研究判断**と「すでに所有者の権利審査・許可が出た」という**実行承認**は異なる。ownerの4TB上限、200GBの最低空き、staging、復元閉包、固定40hex revision、LFS SHA、LICENSE、依存、特殊モデルコード・pickle実行安全を全件個別に確認するまで `queues/approved.json` を変更しない。今回は重み取得も実機性能テストも行っていない。

## 5. 規制に関する一次政策確認（事実と仮説）

2026-11-19施行の米国BIS[91 FR 74970 §IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は、従前AI Diffusion Ruleのmodel-weight `ECCN 4E091` を**撤廃**し、その一方でadvanced semiconductorの遠隔コンピュート／国・用途別規制を導入した。**すべてのローカルモデルweightsの私的保存が一律禁止されるという主張は不正確**。将来の配布停止・規制強化・Gated転換は保全リスクとして検討するが確率を創作しない。配布元権利・ユーザーの取得行為・用途・越境移転は別々に判定する。

## 6. H／T／D／C／U と ERROR CHECK

- **H**：Qwen0.8Bにrank3 LoRAを重ねる可逆構成が、親原本の追加コピーを避けつつ拒否低下と中立能力を両立できる。
- **T**：同一親40hex revision＋LoRAの2 distinct LFS SHAを固定。将来ownerが許可した同一hardware/clock/backend/dtype/quantizer zero-point/context/batchで最低100ペアの中立テスト、100拒否ベンチ、40題×5seedの推論テストを事前登録。中立正答率の95%信頼区間で非劣性を評価し逐次停止条件を事前固定する。今回owner実行n=0。
- **D**：原本重複SHAを一学習stateとして数え、参照が不変・承認0はメタデータPASS。中立正答率の非劣性マージンを5 percentage pointsとし、その差の95%信頼区間下限が-5 pointsを上回り、かつ拒否低下を独立再現できた場合のみ品質PASS。その他はFAILまたはUNCERTAIN。
- **C**：拒否markerの読み替えだけで品質は改善しない、LoRAの親layerとCUDA/quantizer実行経路不一致、低拒否が推論悪化につながる。
- **U**：作者実験の標本バイアス、モデル重み中身・未凍結非重みファイル、モデルコード・時計・backend・parent SHA・重複量子化、実機HDDとライセンス行為。反復データが無く合成標準不確かさ`u_c`と包含係数`k`は算出不能。

**ERROR CHECK**：既存v63アセット235・188有効は不変／取得済み報告99の再ダウンロード0／新規独立LoRA重みSHAは2件／rootとtrial_002 SHA一致を除外／FFIや量子化版のGGUFは新たな学習成果と数えない／承認0／`owner`実HDD・バイナリ未接触。これは完全な再現検証PASSを意味しない。

**関連分野**：①低ランク線形代数とパラメータ編集、②評価統計・安全性と推論能力の多目的最適化、③ソフトウェアサプライチェーン・ハッシュの不変性、④ストレージ・GPUランタイムABI、⑤国際輸出管理とライセンス。
