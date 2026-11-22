# R157／v65：既存112取得報告との差分、無検閲LoRA原本だけを残す、Cartwheel権利HOLDを維持（2026-11-22）

## 1. 現時点の正本と今回の採否

唯一の現行正本は[CURRENT](../../catalog/CURRENT.json) **v65・240登録／192有効、SELECT56・CONDITIONAL136・HOLD29**。取得実行側は**112モデル／1,714ファイル／2,020,548,143,087byte**のVERIFIEDを報告し、1件Gated HOLD。これはowner Windows Dの**今回の現物SHA再検証／完全オフライン復元／個別ライセンス審査を意味しない**。

別作業で正式登録済みの[Timestral-5M](https://huggingface.co/mistralai/Timestral-5M)はSELECT、[WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B)と[nchapman Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA)はCONDITIONAL、[Cartwheel Control](https://huggingface.co/GetCartwheelInc/cartwheel-control)はHOLD。**同じv65を二重に再追加せず、この4判定を維持する**。既に取得報告のあるTimestral5MとWeMM原本、既存Qwen3.5親は再ダウンロード不要。

今回独立に進めた作業は、[Cartwheel＋Hereticの原本だけに絞った61ファイルsource SHA](../../manifests/drafts/r157-2026-11-22-cartwheel-policy-52-and-heretic-lora-9-unique-source.candidate.json)、[次の未取得候補・権利HOLDを分けた後112件キュー](../../queues/proposed-v65-r157-post112-noduplicate-and-rights-HOLD-UNAPPROVED.json)、および**新規取得計画の偽承認と重複取得防止**。

## 2. 重複学習を計上しない原本選択

| 実物リポジトリ | 出版元全ファイル | 学習成果原本の限定選択 | 技術価値・否定的評価 |
|---|---:|---:|---|
| [nchapman/Qwen3.5-0.8B-Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA/tree/92e2ae29c379d7378c696511ec9c70ace8be1434) | 16files・6,165,749byte | **9files・2,026,596byte** | 2独立MPOA rank3編集済みLoRA重量。rootとPareto trial002の`adapter_model.safetensors`は**完全SHA一致**、trial004は別SHA。root/trial2の二重保存と派生GGUF3種を避ける。作者100問の拒否数はbase93、root4、trial004 6。KL値0.0714／0.0275 natsは作者測定。拒否数減少は一般性能・安全性向上を証明しない。|
| [GetCartwheelInc/cartwheel-control](https://huggingface.co/GetCartwheelInc/cartwheel-control/tree/24fc279af8f70097f503767b81db5384d779aae5) | 154files・304,057,444byte | **52files・110,571,134byte** | RP1/Asimov-1/G1用の**3個の異なるpolicy.safetensors**とconfig/motion/LICENSE/NOTICEだけを選択。ソース原本全部を合法取得可能と誤記しない。モデルは50Hzで関節目標を出す作者仕様で、シミュレーションのみ・実機未検証。|

合計**61ファイル／112,597,730byte、Publisher LFS SHA256 47件**。両者は現取得台帳112に存在しないが、**本研究で新しく転送した重みは0byte**。全原本16+154ファイルは[従前R154 Publisher監査](../../manifests/drafts/r154-2026-11-22-four-primary-sources-after112.candidate.json)に保持。今回の原本限定ファイルscopeは別trained outputそのものと、パッケージングだけの複製を分けるための研究用候補であり、権利取得や正式承認ではない。

Hereticの親`Qwen/Qwen3.5-0.8B@2fc06364715b967f1860aea9cf38778875588b17`は取得台帳VERIFIED。ただし**LoRA作者の学習時に用いた正確な親commitがそのSHAだったとは独立に証明できない**。LoRAの原本重量2つは独立SHAだが、将来のフル推論のためPEFT・Transformers・tokenizer・baseとの互換性と使用者の個別権利確認が必要。発行元のApache2タグだけでは、別`LICENSE`の存在や本人の行為別許可を自動的に認定できない。

Cartwheelモデル重量の[別ライセンス全文](https://huggingface.co/GetCartwheelInc/cartwheel-control/blob/24fc279af8f70097f503767b81db5384d779aae5/LICENSE)には条件付きの撤回・改定と著作権/特許訴訟時の終了規定がある。[NOTICE](https://huggingface.co/GetCartwheelInc/cartwheel-control/blob/24fc279af8f70097f503767b81db5384d779aae5/NOTICE)では**RP1外形メッシュ・robot.glbに上流ライセンスが無い**。Unitree G1形状BSD、Asimov-1形状CERN-OHL-S-2.0も別許諾。**モデルポートフォリオではHOLDを維持**し、今回は52ファイルを「将来ライセンス審査の単位」として固定する。102ファイル・193,486,310byteの形状/画像系を今回の取得候補から除外したため、これ単独ではロボットのオフラインシミュレーションが完結しない。実機へ勝手に制御ポリシーを適用しない。

## 3. 取得台帳の更新を反映した次期優先順位

[112取得報告後の未承認研究キュー](../../queues/proposed-v65-r157-post112-noduplicate-and-rights-HOLD-UNAPPROVED.json)は、小容量原本と学習済み依存の未確定箇所を分離する。

1. **Heretic-LoRAの独立編集重み2件、2,026,596byte**：親は報告済み。作者の訓練親revision・個別利用権・本体Quality/PEFT互換性の確認後にのみ取得可。
2. **Kitten Pico INT8の追加8ファイル、63,628,208byte**：すでに保存報告のある33file／285,879,877byteを再取得しない。[Publisher SHA8件はR154監査で固定済み](../../catalog/research/2026-11-22-r154-pico-eight-int8-extra-publisher-sha.json)。量子化認識蒸留による別学習成果か、通常の重量変換に過ぎないかは作者証拠とTensor比較が必要。論理モデルIDは1件を保持。
3. **Cartwheel政策core 110,571,134byte**：第三者形状のライセンス・シミュレータABIが未解決なので現時点のHOLDを解除しない。**優先候補の数値に含めても実行・取得GOではない**。
4. **大型のGroundhog 53.12GB／Ripple65B 129.57GB**：既存の意思決定能力との独立ベンチマークと保存費用が未確定、HOLD維持。

小型3項目の原本参照を合算すると**176,225,938byte**であるが、**実際に直ちに審査すべきCartwheel以外の原本・QADが計65,654,804byte**。これは追加ダウンロード実績・許可・所有者HDD現在の空き容量ではない。

## 4. 取得計画生成器の再発した偽承認を封じ、同一13モデル再取得を停止

最新mainの`scripts/build_v64_plan.py`に前回v62と同型の危険なバグが再発していた。研究用キューから`approved_by_user:true`・`license_text_reviewed:true`等を無条件に生成し、`D:/AI_VAULT/state/approved-v64.json`へ書く実装であった。

修正後は**`review-v64-UNAPPROVED.json`に全てfalseのレビュー用JSON**を書き出し、`approved-v64.json`は上書きしない。追加で[現在の報告済み取得台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)の個別`repo_id`／固定40hex revision／選択ファイル数／総bytesが同一であれば、たとえ実行環境からDドライブが見えなくても**重複転送計画から除外**する。固定v64 R152キューでは13モデルがすべて報告VERIFIED scopeと一致し、**転送計画は0件／0byte、approval0件**となる。

重要：取得台帳のVERIFIEDは過去の取得器によるハッシュ報告であり、所有者のドライブ現物を本研究で独立再ハッシュした証明ではない。もし利用者の実物に欠落があれば、現物ハッシュを別途審査し、**誤って旧データを削除したり自動再取得したりせず**再承認する。源の承認はファイル別SHA・権利・200GB残床・依存閉包・キャッシュ一時領域・実機コード安全性を満たすまでSTOPとする。

## 5. 時系列の品質優劣と実際の規制を分ける

既に[SELECTのTimestral-5M](https://huggingface.co/mistralai/Timestral-5M)は小ささに独立保存価値がある一方、作者GIFT-Eval MASEは**5M 0.705 vs 28M 0.678**と5Mが劣る。[第三者Baywayの13タスク統一zero-shot比較](https://huggingface.co/datasets/Bayway/italian-open-timeseries)でも5MのMASE skill14.6に対し28M20.1と下回る（Apple M2 Pro、CPU/MPS、時系列context最大8192）。**小型の保存価値と推論品質優越は独立**。ライセンスModified MITの企業・雇用主直前月連結売上USD20M超条項は両者に同じく適用される。

米BISの[2026-11-19改正§IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧モデル重量ECCN4E091を撤廃。**一律のローカル所持禁止が目前という一次資料は確認できない**。配布元HOLD・ライセンス制限・ベンチマークの弱さ・ソース供給消失可能性を別々に監査する。

## 6. H／T／D／C／U

**H**：同じLoRA learned stateを別々のGGUFやPareto trialとして保存しない、ロボットの未許諾形状を権利確定済みpolicy weightに混ぜない、取得済み112モデルを再取得計画しないことで、保存ポートフォリオの増分価値・合法性が改善する。

**T**：Cartwheel全154 Publisher SHAから学習済み3policyを含む52、Heretic全16 Publisher SHAから2独立safetensorsを含む9を抽出。61ファイル・112,597,730bytes・47 LFS SHAと元R154資料を比較。Pico8 SHAはR154固定source参照。v64取得計画生成器を隔離tempで実行し、本人承認bool全false、112同一repo+rev+files+bytes13件がスキップされ、既存承認ファイルが書かれないことを静的検証。最新v65は240登録／192有効、旧236の全行不変。

**D**：すべて一致ならPublisher原本範囲の静的確認PASS。CartwheelをHOLDから条件付きに無断変更、LoRA同重量の重複保存、元取得済み13件を重複計画、ユーザー承認を自動trueにしたらFAIL。owner LICENSE・実媒体SHA・Runtime完全復元と品質はUNCERTAINで取得STOP。

**C**：LoRAへのAbliterationが通常の正答率を落とす、Cartwheelは形状/関節座標がないとpolicyを再実行できない、Pico INT8は単純な量子化違い、Timestral5Mが品質不足で全く有用でない可能性。

**U**：出版社の100問拒否テスト、限定13時系列タスク、Linux/Windows・CUDA・PEFT ABI・量子化zero-point・バッチ・親revision・第三者コンテンツ権利が主要不確かさ。独立反復品質測定が無いため合成標準不確かさ`u_c`と包含係数`k`を捏造しない。

転用分野：**モデルサプライチェーン/ハッシュ、ロボット物理シミュレーションと法的依存閉包、PEFT安全制御編集、時系列予測性能評価、端末GPU・データライセンス**。

**実行結果の境界**：新規モデル重量DL0、承認追加0、owner Dへの書き込み／既存削除0、未審査モデルコード実行0、Gated回避0。既存v65の240資産・正式採否は変更せず、研究成果と取得安全スクリプトのみ更新。
