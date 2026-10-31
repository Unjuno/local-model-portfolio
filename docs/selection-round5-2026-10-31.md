# 第5回モデル選定レビュー — 分野横断・実能力を基準とする再分類（2026-10-31）

> **監査範囲:** 既存v2の110件を16カテゴリに再分類し、追加候補11件（モデル10・データセット1）、監視/権利保留14件を調査。新規11件はすべて**選定候補**で、正式な`CURRENT`へは適用していない。ダウンロード/同意/実行の許可ではない。

## 1. なぜ再分類するのか

以前の`group`は履歴別の整理ラベルであり、110件中30件の`group`が未設定、25件がひとまとめの「小型高効率・分野別業務代替」だった。これでは既存重みの能力を横断比較できず、欠落している分野を正しく判定できない。

本ラウンドでは、分類は**能力の多重ラベル**とし、規制・配布制限の評価、固有の学習価値、容量やライセンスの審査を**別軸**で実施した。分類数を増やすために重複モデルを足してはいけない。

## 2. 既存110件の16カテゴリ

以下の件数は[機械可読の110件全件タグ付け](../catalog/reviews/capability-taxonomy-v1-2026-10-31.json)から算出した。重複タグを許すため列の和は110にならない。**実測性能/技術的独立性をすべて証明するものではない。**

| カテゴリ | 既存件数 | 欠落・重複の判断 |
| --- | ---: | --- |
| 汎用LLM・基盤重み | 25 | 候補が豊富。巨大版を足す前に原本の代表性と3.8TB枠を再審査 |
| コード・GUI・自律エージェント | 15 | 一部は汎用LLM。安全性や実行資材を別途確認 |
| AI安全性・セキュリティ | 2 | 拒否挙動編集由来。専用の入力防御・エージェント保護器は実質不足 |
| 画像生成・編集 | 9 | FLUX / Fibo / Ideogram の原本・蒸留を同系列重複として確認 |
| 動画生成・編集 | 3 | 動画専用の選定が狭い。人物アニメーション別タスクを検討 |
| 人物・話者同一性 | 3 | 同意・肖像・プライバシーと派生モデル権利を別扱い |
| ASR・TTS・音声対話 | 19 | 数が多い。前回までのGated音声を優先し、重複追加を抑制 |
| 音楽・音響 | 5 | YuE2 系は既存。音源を編集するFlow Matching系は不足 |
| 視覚認識・OCR・3D | 20 | OCR / セグメンテーション / 3D生成が混在。SAM 3D契約は未解決 |
| VLA・ロボット制御 | 5 | N1.6 / pi0 / smolvlaなどがあるがN1.7と依存Gatedの確認が必要 |
| 世界モデル・シミュレーション | 4 | 未来動画・動作条件付き予測・物理推論を分離 |
| 医療・生命科学 | 8 | 医療対話中心。ゲノム予測・タンパク質生成は別分類 |
| 地球科学・時系列 | 1 | 既存1件は一般時系列で、地球物理専用モデルなし |
| 検索・埋め込み・Rerank | 7 | 主要な基準系はあり、当面新規より依存の保存を優先 |
| データセット | 23 | 大分類は存在するがロボット操作等の専門データが限定 |
| 独立ランタイム資材 | 0 | モデルを再実行できる依存物が独立した正式選定資産として記録されていない |

## 3. 今回新規の11件（選定を提案）

優先順位は調査の優先であり、規制される確率や取得を許す順序ではない。R0は観測済みGated等、R1は専門成果と契約、R2は低緊急の比較原本を意味する。

| 分野 | 配布元資産 | 判定 | 何を失う可能性があるか・主要制約 |
| --- | --- | --- | --- |
| world_simulation・robotics_control | [nvidia/Cosmos-Reason2-2B](https://huggingface.co/nvidia/Cosmos-Reason2-2B) | R0/条件付き | ロボット/物理空間推論に特化したVLM。現行GatedかつGR00T N1.7のバックボーン。商用利用可能と書くNVIDIA契約を『非商用制限』と誤記しない。 |
| robotics_control・agents_code | [nvidia/GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B) | R1/条件付き | N1.6からバックボーンが変化。旧版を無条件で追加保存せず、選択と重複を比較。Cosmos-Reason2のGated同意とモデル本体の公開を分離。 |
| world_simulation・robotics_control | [agibot-world/Genie-Envisioner-Sim-v2.0](https://huggingface.co/agibot-world/Genie-Envisioner-Sim-v2.0) | R1/条件付き | 行動条件付きの閉ループロボット動画世界シミュレータ。公開2B蒸留チェックポイントとpi05テストポリシーを分離。Gemma条項と非商用条件を併記。 |
| world_simulation・robotics_control | [nvidia/Cosmos3-Edge](https://huggingface.co/nvidia/Cosmos3-Edge) | R1/条件付き | 複数モダリティと行動軌跡を扱う世界モデル。2026-08-25にチェックポイント更新の告知。OpenMDW 1.1本文と版間差を要審査。 |
| medical_biology | [arcinstitute/evo2_7b](https://huggingface.co/arcinstitute/evo2_7b) | R1/条件付き | ゲノム特化のDNA系列原本。Carbon-Xとは異なる学習系列。安全性とトークナイザ・40B別版を要比較。現時点公開、法規制予定の確証なし。 |
| medical_biology | [biohub/esm3-sm-open-v1](https://huggingface.co/biohub/esm3-sm-open-v1) | R2/条件付き | 配列・構造・機能条件によるタンパク質生成。既存のESM2配列Encoderとは異なる。READMEではMIT、HFメタデータと実ライセンスを再照合。 |
| music_audio・speech | [facebook/melodyflow-t24-30secs](https://huggingface.co/facebook/melodyflow-t24-30secs) | R1/条件付き | MusicGen/YuE2生成と区別するテキスト指示音源編集重み。CC-BY-NC-4.0の原本とMITコード、pickle形式の実行リスクを分離。 |
| video_generation・identity_biometrics | [Wan-AI/Wan2.2-Animate-14B](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B) | R1/条件付き | 既存Wan2.2 TI2V 5Bとは別の人物アニメーション特化。公開Apache-2.0、将来規制は未確認。権利ある素材のみ対象。 |
| earth_time_series | [microsoft/aurora](https://huggingface.co/microsoft/aurora) | R2/条件付き | 気象・大気化学・海洋波浪を扱う地球物理予測。既存Chronosは一般時系列で別能力。公開MIT・制限変更根拠が弱いため低緊急のR2。 |
| earth_time_series・vision_spatial | [ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL) | R2/条件付き | 6バンド衛星観測の時空間表現。通常のRGB/LLMとは異なる。公開Apache-2.0で低緊急のR2。 |
| datasets・robotics_control | [nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim) | R1/条件付き | 複数ロボット形態の操作軌跡という学習データ。公開CC-BY-4.0。tree表示約270GBは全ファイル参考値、必要サブセットを選んでから容量計測。 |

**すべての新規候補について**`pin_revision_sha=null`、`selected_file_bytes=null`、`peak_ram_bytes=null`、`download_approved=false`。今回判明したHubの全repo容量やパラメータ数を、取得に必要な厳密バイト数に置き換えない。

## 4. 法的・技術的制約を過大評価しない

1. **Gatedと法規制を分ける**：[NVIDIA Cosmos-Reason2](https://huggingface.co/nvidia/Cosmos-Reason2-2B) はGatedだが、公式ページに商用利用可能というNVIDIA Open Model Licenseの記載がある。保護機能の無断除去による終了条項もある。『Gatedだから利用不可』とは言わない。
2. **バックボーンへの依存を評価する**：[GR00T N1.7公式実装](https://github.com/NVIDIA/Isaac-GR00T)は、モデル本体公開とCosmos-Reason2 Gatedバックボーンの読み込みを区別する。重みだけを持っていても完全オフライン実行を保証しない。
3. **同一系列を全部保存しない**：既存Cosmos2・候補Cosmos3・Predict2.5、既存GR00T N1.6・候補N1.7は、重みが違うからという理由だけで全版併存させない。失う研究成果と依存・容量を比較する。
4. **コード・重み・学習データの権利は別**：[GE-Sim 2.0](https://huggingface.co/agibot-world/Genie-Envisioner-Sim-v2.0)はApacheコード、非商用資材、pi05にGemma条件が存在。どれが原本保存・再実行の範囲かを分ける。
5. **人物とデータの利用条件**：[Wan2.2 Animate](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B)とロボット動作データは、配布可能でも第三者の肖像/同意が必要な場合がある。無断の個人識別・偽装利用を目的にしない。
6. **生体安全と権利**：[ESM3公開カード](https://huggingface.co/biohub/esm3-sm-open-v1)には安全フィルタ処理が明記され、これは現状の技術的事実であって将来の政府禁止予告ではない。研究に必要な機能・承認条件を確認する。
7. **原本の容量と実用版は別**：公開モデルやPython/PyTorchの実行コードがすべて安全なわけではない。pickle重みを自動ロードせず、完全revision、同種のSHA-256照合、依存バージョンを別に確定する。

## 5. 今回選ばず監視/保留とする14件

| 配布元 | 未採用とする理由 |
| --- | --- |
| [nvidia/Cosmos-Predict2.5-2B](https://huggingface.co/nvidia/Cosmos-Predict2.5-2B) | Gatedだが旧Cosmos2およびCosmos3-Edgeと重複するため代表版を比較するまで重複採用しない。 |
| [nvidia/Cosmos3-Super](https://huggingface.co/nvidia/Cosmos3-Super) | 多モーダル原本だが約65B級でEdgeと同系。実容量・差分を見て大型枠で比較。 |
| [google/medsiglip-448](https://huggingface.co/google/medsiglip-448) | 医療画像向けencoderの既存MedGemma依存との差を要調査。 |
| [nvidia/FourCastNet3](https://huggingface.co/nvidia/FourCastNet3) | 公開Apache-2.0の気象系比較候補。Auroraを優先し、重複と性能の独立検証後に判断。 |
| [Horizon-Labs/prompt-injection-guard-base](https://huggingface.co/Horizon-Labs/prompt-injection-guard-base) | 公開Apache-2.0の防御器。既存に専用防御モデルが少ない一方、配布制限・回復不能性の証拠が現状弱いため監視。 |
| [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | 公開MITの高能力LLM。サイバー能力の外部評価はモデル重みの配布制限予定を意味せず、321B級の完全構成が未審査。 |
| [facebook/sam-3d-objects](https://huggingface.co/facebook/sam-3d-objects) | MetaのGated/独自SAM Licenseの内部解析適合性が未解決で、既存Round4と同様に保留優先。 |
| [apple/Sharp](https://huggingface.co/apple/Sharp) | Apple研究ライセンスは終了時コピー削除を定める。長期保全目的との権利適合性が未確認。 |
| [nvidia/GR00T-N1.7-ApplePnP-V1](https://huggingface.co/nvidia/GR00T-N1.7-ApplePnP-V1) | 特定タスクのONNX派生重みで、N1.7原本を優先し、派生変換・学習増分の必要性を確認。 |
| [nvidia/PhysicalAI-Robotics-Open-H-Embodiment](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment) | 公開・CC-BY-4.0のロボット動作群。採用中データと用途・容量の重複確認を優先。 |
| [nvidia/PhysicalAI-Robotics-Locomanipulation-GRAIL](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Locomanipulation-GRAIL) | 公開・CC-BY-NC-4.0の4D人体-物体相互作用データ。生成元映像・人物由来等の権利確認を優先。 |
| [nvidia/PhysicalAI-Robotics-NuRec](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-NuRec) | Gated・CC-BY表示の3D再構成場面。元映像・場所・人物等の権利と巨大容量の検証前は取得保留。 |
| [facebook/sam-3d-body-dataset](https://huggingface.co/datasets/facebook/sam-3d-body-dataset) | Gated・独自SAM Licenseに加え第三者データ源を含む。元データの権利と個人情報を照合するまで保留。 |
| [genrobot2025/Gen-HumanWholeBody](https://huggingface.co/datasets/genrobot2025/Gen-HumanWholeBody) | Gated・独自条件の人間動作データ。個人情報と被写体同意が不明なまま取得しない。 |

上記14件は一括して同じ理由で落としたわけではない。**公開MITの防御器**と、**権利・個人情報未解決のGatedデータ**は、同じ『監視』という言葉でもアクションが異なる。正式台帳へ昇格させるには独立ゲートを使う。

## 6. 最小検証の標準化（H / T / D / C / U）

| 要素 | 実施内容 |
| --- | --- |
| **H：反証可能仮説** | 『新規11件は既存110件に無い独立能力または正規再取得が難しくなり得る契約・配布条件を持つ』。後で同一重みが合法的に得られるか、機能が再現可能なら降格する |
| **T：最小検証** | 各候補で公式モデルカード1件以上、適用LICENSE本文1件以上、必要依存・別配布元調査、同一形式/元重み差分を確認。欠ければSTOP。性能比較が必要なときは評価データと測定HW/クロック/バッチ/推論器を事前に固定 |
| **D：合否** | PASS＝固有理由・直接リンク・実在・制限と推論の区別が成立する選定。FAIL＝存在しない・価値が完全重複・必要権利が得られない。UNCERTAIN＝本文/ファイル/容量/実行器不明。PASSは取得許可ではない |
| **C：対立仮説** | Gatedは連絡先収集のみ、データはCC-BYでも元素材の権利が異なる、ベースモデルに同一機能が既にあり特殊版の再現性が高い、後継版が代替可能 |
| **U：不確かさ** | ライセンス本文改訂・権利継承・作者報告と独立試験の差・上流ファイル更新・モデル改訂の識別・実行オーバーヘッド。確率分布未定義のため合成不確かさと包含係数の数字は出さない |

## 7. 優先して次に検証する順序

**第1優先**：[Cosmos Reason 2](https://huggingface.co/nvidia/Cosmos-Reason2-2B) と [GR00T N1.7](https://huggingface.co/nvidia/GR00T-N1.7-3B) のセット。アクセス条件を守り、Gatedの依存が必要である事実を確認して整合したマニフェスト案を作る。

**第2優先**：既存Cosmos2と [Cosmos3-Edge](https://huggingface.co/nvidia/Cosmos3-Edge) の版差と重複、[GE-Sim 2.0](https://huggingface.co/agibot-world/Genie-Envisioner-Sim-v2.0)の非商用・Gemma依存、ロボット専門データの権利/サブセット容量を検査。

**第3優先**：[Evo 2](https://huggingface.co/arcinstitute/evo2_7b)と[ESM3](https://huggingface.co/biohub/esm3-sm-open-v1)の研究用途適合性、[MelodyFlow](https://huggingface.co/facebook/melodyflow-t24-30secs)の非商用・コードと重みの条件差を確認。

**第4優先（低緊急）**：[Aurora](https://huggingface.co/microsoft/aurora)、[Prithvi](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL)を代表的科学原本として比較保存計画へ進める。現時点でGated化や公開停止を予告する根拠はない。

## 8. 3.8TB予算に関する停止条件

現行の`catalog/CURRENT.json`はv2：110件追跡・94件有効で、暫定計算に使用する原本repo全ファイル容量は約3.234TB、暫定余裕約0.566TB。ただし選択ファイルと全依存を精算した容量ではなく、**今回11件を一斉に追加できる保証はない**。

正式取得へのゲートは(1)利用目的・同意・元データ権利の確認、(2)固定完全commit、(3)採用対象の全ファイルとSHA、(4)正確な必要バイト、(5)3～4bitでの現実的な量子化と実行器版、(6)OS/KV/作業領域込みのピーク推論RAMが512GB未満、(7)HDD空き200GB以上、(8)ユーザーの明示承認。上記が一つでも未解決なら`queues/approved.json`へ入れない。

## ERROR CHECK

- 新規11件は10モデル・1データセット、全件conditional。既存110件の多重タグは110/110件で非空を確認。
- モデルのGatedや商用制限は政府が将来禁止すると確定した根拠ではない。独自コードのGPL/MITと重みの独自ライセンスも混同しない。
- 保留/監視を採用済みに数えない。過去v3/round4のIDが存在していてもその事実を尊重し、変更するときは明示する。
- `catalog/CURRENT.json` と `queues/approved.json` は変更しない。配布者のGated同意や、重み・データの実ダウンロード/実行は実施しない。
