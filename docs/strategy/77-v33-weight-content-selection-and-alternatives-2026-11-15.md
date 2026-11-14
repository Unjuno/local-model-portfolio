# v33・2026-11-15：実際の重み・構成・学習機構で専門モデル3件を追加選定

**結論：** `main`の正式選定をv32の182資産／有効135件から、**v33の185資産（159モデル・26データセット）／有効138件（SELECT53・CONDITIONAL85）**へ改訂した。研究対象は独立の学習済み成果3件だけ増やす。通常量子化や同族のサイズ違いを増やさない。既存採用資産を性能上の根拠なしに降格させない。**ダウンロード承認0**。

[正式差分](../../catalog/revisions/v33-2026-11-15.json)、[全185件の正本ビュー](../../catalog/effective-portfolio-2026-11-15-v33.json)、[非実行138候補](../../queues/proposed-v33-2026-11-15.json)、[138件の依存準備](../../catalog/preparation/2026-11-15-insurance-bundles-v33.json)。

## 1.〈本論〉— 何を実際に検査したか

### A. IBM Granite 4.1 3B LLMON preview — CONDITIONAL追加

- [モデル公式カード](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview)、[固定revisionのconfig](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview/blob/55a14cac002854bb64c7f465c30da29209b170c8/config.json)、[公開元の重みtensor形状とSHA](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview/blob/55a14cac002854bb64c7f465c30da29209b170c8/model.safetensors)、[IBMによる学習方法の一次説明](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite)。
- 公式配布元の計数は**3,659.7M**学習済みパラメータ。実際のconfigは`GraniteForCausalLM`、**40層・hidden2560・attention heads40・KV heads8・MLP8192・BF16**。約**7.32 GB**の単一`model.safetensors`のXet SHA256は`1b3bca7852237cd0d23d0b71c3e809231568425f66ce4005b3cdad1e992af3dc`（公開元表示、ローカル実物未ハッシュ）。明示的なLLMON予約delimiterとチャットテンプレートが要る。
- Baseから別々のSFT/RL/DPOを受けた学習済み状態。入力の命令・資料・tool response等を型付きblock/IDと`exec`束縛で結び、非信頼データ中の指示に従わないことを学習させる。これは`usezn/Galvanize-3`のような事後注入検知器や通常のGraniteモデルとは**別機構**。
- 研究側の同じサイズの3B比較：MMLU 68.05 vs 67.02、MMLU-Pro **46.08 vs 49.83**、HumanEval 84.15 vs 81.71、BFCL v3 60.71 vs 60.80（全てメーカーの異なるタスク）。**MMLU-Pro悪化も確認**。目的は一般スコア上昇ではなくデータ/命令境界にある。多ターン適応攻撃に対する堅牢性は未証明、独立実機未測定。
- **8B LLMONを同時保存しない**：同一後学習方式・独自メカニズム、約8.79Bの別サイズのみ。3Bで成立する能力を追加容量なしに実証するのが先。
- 必須scope：BF16原本単一重み、config/tokenizer/chat template、公式LLMON表現生成ツールの固定source/license、ABI。Model CardのApache2.0タグは見たが、取得許可・公開元LICENSE全文の行為別検証は未完了。

### B. Perplexity Decider Flash v1.3 — CONDITIONAL追加

- [作者モデルカード](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3)、[固定commit `d06fb3f2d97e0a52325a0d463c450cf0338f44fe`のrelease-manifest](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/release-manifest.json)、[config](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/config.json)、[判定専用readout](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/readout.safetensors)。
- Hubのパラメータ表示は**4,539.3M**。実際のconfigはQwen3.5系**32層・hidden2560・linear/full attention混合**、視覚encoder24層。作者専用推論コードは**full-attention部分だけ非因果**にし、各質問の`<|fim_suffix|>`で**255×2560のBF16 readout**を取得する。通常の因果言語生成では同じcheckpointの判断を再現できない。
- 重みの正確な公開元配布サイズ：本体2シャード **4,972,946,624 byte**（SHA`0048d1ddf2c5754fc05540fccdbc4ac50407e5cf14a35326be01cac0756b4de6`）と**4,105,669,472 byte**（SHA`40e0c0ccb3248a59db0724ffd1ad1c81fc935d9f474e6fd52e9df32af4690608`）。判定用readout **1,305,712 byte**（SHA`46358a2e2639f1956561687ba261dd9b37506f878e90eb5eabc15f114532bec3`）。さらに**Locate**専用Adapter **519,509,312 byte** とhead **6,588,228 byte**、別のtokenizer、custom `pplx_decider`実装が必要。前記5重量ファイルのみの単純和は**9,606,019,348 byte**。
- `choice/noul/score`は既存`kakaocorp/kanana-2-v-decide-3b-2611`とも重複するが、Perplexityの**画像、Locate原文オフセット抽出、noncausal readout、蒸留と専用較正**が別能力。既存Kananaを削除するのではなくこの差分のみ保存。
- **作者release-manifestに`private:true`がある**：現時点でモデルページやLFS pointerが可視でも、ユーザー本人のHFアクセスは未確認として取得・承認を停止。Python3.12+・CUDA GPU・BF16本体約8.5GiB以上に加え実動作余白、custom code審査が必要。作者報告のfast-path相対速度1.7–1.9倍、9–18倍は**異なるパス同士の作者測定**であり、ユーザーHWのベンチマークではない。
- 26B Deciderも同じprotocolの大型モデルなので**同時採用しない**。flashの多質問精度が不十分と独立に証明できた場合だけ再評価。

### C. NVIDIA Kumo-Relational — CONDITIONAL研究追加（取得停止）

- [NVIDIA公式repo](https://huggingface.co/nvidia/Kumo-Relational)、[別々のclassifier/regressorの原本SHAを含む既存の一次調査](../../catalog/proposals/07-rare-specialist-2026-11-15.json)、[NVIDIA公式コード固定版](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/relational/model.py)。
- 固定revision`efdbb110daea5aae123447864a64612e8a3dc6be`。公式repo7ファイル合計 **243,656,960 byte**。独立した`classifier.pt` **119,862,733 byte**（SHA`0c2e35cc18303f0d3ddeaf04e9cab6ca3a8bd6ea17195ac0e42d47af4bcb2a2d`）と`regressor.pt` **123,786,699 byte**（SHA`f863b3632f738e1444fb83a8cea5746f298889b5c96953a000c4720d202ae4cf`）。**時系列予測モデルTTM/Chronosとも、OCRとも異なる関係表のクラス判定・数値予測**。両者を別repoモデル2件と数えるような増加はしない。
- **総学習済みパラメータ数は公開元メタデータで確定しなかったため`UNVERIFIED_BLOCK_FINAL_LOCK`を維持**。`.pt`重み本体をデシリアライズ・実行していない。実装コードは原本がないとHFから自動取得する可能性があり、未監査のネットワークfallbackを防ぐこと。ライセンスOpenMDW1.1/第三者NOTICE、親TabICLv2の依存ABIは未確定。研究選定は最終取得の許可ではない。

## 2.〈応用・転用例〉— 増やさないもの／置き換えないもの

| 検討対象 | 判定 | 非採用の理由 |
|---|---|---|
| IBM LLMON 8B | DEFERRED（v33台帳には追加しない） | 3Bと同じ独自学習方式。増量の独立価値未検証 |
| Perplexity Decider 26B | DEFERRED（追加しない） | Flashと同じ判断protocol、容量負担が大きい |
| [inclusionAI/Duo-1.0-distill](https://huggingface.co/inclusionAI/Duo-1.0-distill) | RESEARCH HOLD（正式資産としては未追加） | 同期音声動画の4step Realization overlayであり、実際に`inclusionAI/Duo-1.0-causal-base`のIntent/Codec/Speech等を必要とする。MiniMax H3由来LICENSE、全学習済み総数・外部必要byteが未確定 |
| [NousResearch/Arete-27B](https://huggingface.co/NousResearch/Arete-27B) | DEFERRED（追加しない） | 同一Qwen3.8-27Bに対する政治・価値観SFTで、既存の選択的拒否制御派生と能力が重なる。作者の803問・5回評価は有益だが比較条件を揃えた増分利益が未証明 |
| 既存のKanana v-Decide / Galvanize-3 / TTM R3 | **維持** | 決定対象、検知器、時系列予測のそれぞれの独立目的が保存価値を持つ。**重複が証明されないので恣意的には除外しない** |

## 3. 保存予算と取得停止

選定対象の**研究予算上限**は、LLMON **8.5GB**、Decider Flash **11.5GB**、Kumo **0.5GB**、合計 **20.5GB**。これは実バイトの完全保存額ではなく、容量検証が失敗すれば範囲を再設計する限度。v32のSHA調整済み公開元scope試算3,466,070,232,173 byteを唯一の基準とした仮の増分上限は **3,486,570,232,173 byte**。4TB/200GBの差は**313,429,767,827 byte**。**実HDDの空き、既存ファイル、stage/cache、全学習済み依存のbyteは未測定なので保存できるとは言わない。**

| 変数 | 意味（日本語） | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_0` | v32既知ソース算術値 | byte | 3,466,070,232,173 | 公開元scopeであり完全アーカイブではない | 非負整数スカラー |
| `B_Δ` | v33追加研究の計画枠 | byte | 20,500,000,000 | 3モデル合計の上限、未測定 | 非負整数スカラー |
| `B_{Σ}` | 仮の研究ソース予算 | byte | `B_0 + B_Δ` | 全依存未計上 | 非負整数スカラー |
| `C` | 保存計画上限 | byte | 4,000,000,000,000 | ユーザー認可の予算・実容量ではない | 非負整数スカラー |
| `F` | 最小実空き床 | byte | 200,000,000,000 | 実測前提 | 非負整数スカラー |

次元確認：`B_0`、`B_Δ`、`B_{Σ}`、`C`、`F`はすべてbyte、加減算の次元は一致。モデルのパラメータ数・推論VRAMをbyte容量と同一視しない。

H：3件には既存135件と同一ではない学習済み能力が少なくとも1種類存在する。  
T：各公式のモデルconfig／tensor header／独自訓練方式と、既存の役割が近いモデル3種（Galvanize/Kanana/TTM）を比較する（`n_min=3`）。次にランタイムと権利・ファイルの閉包へ進み、検証不能なら取得STOP。  
D：研究選定PASS＝独立の機構または別重みと配布元原本の出典が確認できる。取得可能性＝**UNCERTAIN/STOP**。独立性が否定される、重み不整合、法的許可不足はFAIL。  
C：LLMONの追加効果が形式によるものだけ、DeciderのLocateが既存の抽出器で同等再現可能、Kumoの一方が元TabICLと同一なら保存増分を引下げる。  
U：研究自己評価、依存wheel/ABI、特定アカウントの権利、実機性能、完全sourceバイトと量子化による誤差。確率分布未定のため`u_c`・係数`k`は未算出。

**ERROR CHECK**：旧182件を不変更、追加3件は一意、合計185／有効138、総数未確定のKumoは研究専用かつ最終取得不可、承認0、同族大型版と通常量子化は非採用。書き込みはカタログ／準備／調査ファイルだけで重み・HDD・実行環境は操作していない。

## 4.〈次に考える問い〉

**Kumoの2種類の`.pt`重みを実行せずに全tensor総数・親依存を確定できる公開元の安全なメタデータがあるか。無ければ総数未確定のまま研究専用に留める。**
