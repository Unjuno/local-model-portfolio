# R91 — 最新規制の一次資料と現行v40の148件保存停止要因（2026-11-15）

## 1.〈本論〉目的・到達地点・誤解の訂正

目的は、モデル公開条件が将来変化しても、**独立した価値を持つ学習済み原本を正規に取得できるときに、再現に必要な重み・tokenizer・別学習済み依存・ライセンス・実行環境を安全に保存すること**である。単なる高性能モデルの人気ランキング、通常量子化の多重保存、配布制限の回避を目的にしない。

現行正本：[CURRENT.json](../../catalog/CURRENT.json) → [v40・195登録、148有効](../../catalog/effective-portfolio-2026-11-15-v40.json)（SELECT 53、CONDITIONAL 95）。[公式取得前ゲート](../../catalog/readiness/v40-2026-11-15-r90-all148-gates.json)のready_to_approveは0。配布元のSHA・容量を調査したことは、本人HDDで重み本体を保存したこと、LICENSE全文が許容すること、安全に推論できること、取得が承認されたことを意味しない。

新規成果：[全148件の一意な非実行監査表](../../catalog/research/2026-11-15-r91-v40-148-policy-and-insurance-triage.json)を作成。各件に配布元・証拠日・利用条件メタ・選定理由・将来波の仮説・本人Gated観測・総学習済み要素・現時点の全停止ゲート・最初の停止ゲート・次の安全な行動・反証条件を結び付けた。**旧件の採否を証拠なく降格しない、新規モデルも追加しない。**

### 以前のDeep Researchでの3つの具体的な誤り

1. **「150B以上は絶対除外」ではない。** 現行[limits.json](../../policies/limits.json)の正式方針は2026-11-06以降、MoEの**全expertを含む総数150B**を通常基準とし、150B以上は量子化派生の同一HW・backend・context・batchにおける150B未満参照モデル以下の実測完全ピークRAM、512GB未満、速度・品質・ライセンス・本人承認の全条件を満たす場合のみ**例外を審査する**。現時点で例外承認は0。大きいモデルを勝手にSELECTへ昇格させない。
2. **「全資産がApache-2.0」は事実誤認。** [GroundingPI原本のKimi K3派生条件](90-v40-groundingpi-original-decision.md)、[WhissleAI/steer-ttsのCC BY-NC](https://huggingface.co/WhissleAI/steer-tts)、[Pruna P-H3 Imageの地域限定コミュニティ契約](https://huggingface.co/PrunaAI/P-H3-Image)、UNKNOWN/otherの配布物などが混在する。Hubのlicenseタグと利用・複製・改変・再配布に適用される全文を区別する。
3. **Xiaomi U0-4Bを34Bと呼んではならない。** 4B系列のHub公表主モデル5.0821B、必須外部[Emu3.5 VisionTokenizer](https://huggingface.co/BAAI/Emu3.5-VisionTokenizer)0.4553Bは別repo。全18ファイルの候補出版社バイト11,991,440,188は[固定調査](90-v39-unis4b-source-allowlist-runtime-gates.md)の参照値であり、実HDD確認ではない。34Bは別の同系列checkpoint。

## 2.〈事実〉2026-11-15時点の政策・モデル配布制限

| 一次資料 | 現在観測される事実 | 予測ではないこと・限界 |
|---|---|---|
| [EU委員会のAI Act執行説明](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act) | 2026-08-02以降にGPAIの執行権限。違反に関し公開制限を求める権限がある | **全公開ウェイトの無条件・一律禁止ではない** |
| [EU AI Act Article 53(2)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53) | 一定の無料・オープンソースGPAIは文書化義務の一部免除、systemic risk対象はその免除なし | 著作権対応義務の包括免除ではない |
| [中国MOFCOM公式説明](https://english.mofcom.gov.cn/News/SpokesmansRemarks/art/2026/art_74bf283f105a4b19a11f7430df3671ae.html) | 技術輸出の限定的な管理案と、公開済み技術・オープンソースや自社海外拠点向けの区分・簡素な許可措置に言及 | どの提案条項が正式施行済みかは別途一次文書で確認する。すべての国内外ダウンロード禁止とは断定できない |
| [米国2026-06-02大統領令3条](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/) | 高度モデルの政府との事前協力は任意枠組み。同条は強制的なリリース事前許可を新設しないと明記 | 他の法的輸出規制や将来の制度が存在し得ないという主張でもない |
| [Hugging Face公式Gated運用](https://huggingface.co/docs/hub/models-gated) | 作者がユーザー個人のアクセス権を付与・撤回し得る | Gated状態だけでは政府規制の発動を証明しない |
| [GEITje作者による削除説明](https://goingdutch.ai/en/posts/geitje-takedown/) | 著作権関係の要請後にモデルが配布停止した実例 | 他モデルの削除予定日・合法性は導けない |

**シナリオ（仮説）**：S1＝拒否方針編集・身元・音声など用途別／S2＝高度な自律・科学・汎用モデル／S3＝広範な公開ウェイトへの規制波及。一次資料は一律の法的配布停止確率を与えない。観測したGated・地域制限・作者削除・著作権と将来の法的リスクを別フィールドに保持する。予測を取得権限の代用品にしない。

### 具体的な研究記録の誤り修正

[GroundingPI旧R88研究JSON](../../catalog/research/2026-11-15-r88-groundingpi-thinker-original-license-comparison.json)に、公開元固定APIとv40アクセス側のgated:falseに反してmodel_gated:trueの値が残っていた。**publisherが公開・非Gatedと観測した証拠**に基づきfalseへ訂正し、旧値と一次URLを追跡できるメタデータを加えた。一方、LICENSEと本人の行為別許可は依然**未承認**。これはモデル採否や取得を変更しない訂正である。

## 3.〈応用・転用例〉148件を止める実務要因

[機械可読148件の全件表](../../catalog/research/2026-11-15-r91-v40-148-policy-and-insurance-triage.json)の集計（相互排他的な**最初の停止要因のみ**）：

| 最初の停止要因 | 件数 | 次の非実行タスク |
|---|---:|---|
| 不変原本ファイル集合・依存・権利の確定 | **118** | Publisher固定commit、ファイルallowlist、SHA、重み依存、適用LICENSEの結合 |
| Gatedモデルの本人権限 | **19** | 作者公式のアクセス条件とユーザー本人の既存権限を確認。回避・共有トークンの保存なし |
| 総学習済みパラメータ不明 | **9** | 安全な静的テンソル計数と音声/画像エンコーダ、MoE全expert・後学習パーツの全数確認 |
| 所有者HDDと作業領域 | **2** | 本人の実ボリューム空き、キャッシュ、staging、安全床の読取専用測定 |
| **合計** | **148** | **全件とも取得承認0** |

上記は最初の停止要因であり、各資産が他の停止要因をクリアしたという意味ではない。**CONDITIONAL 95件のアクセス台帳にはGated観測20件**。初回停止要因19件との差は優先順位付けによるもの。**SELECT 53件はCONDITIONAL専用のGated側帳簿では未確認**であり、公開・利用可能とみなさない。

### 次に確定すべき具体例

- **既に選定ファイル量を記録した2件**：[InterpreticAI Qwen3.8 Uncensored GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) 17,738,327,225 byte、および[chatrlabs Qwen-Image 2.1 LoRA](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) 671,173,375 byte。最初の停止要因は所有者HDD検証であり、直接ダウンロードを開始する理由にはならない。
- **GroundingPI**：独立座標トークンの学習成果・[28ファイルの出版社候補](../../manifests/drafts/v39-groundingpi-source28.candidate.json)9,704,102,624 byteを保持。Kimi由来の利用権、作者patched Transformers/vLLM実行境界、ユーザー実機での精度を解決してから初めて承認判断する。現在は非Gatedだが権利の無条件許諾を意味しない。
- **Xiaomi U0-4B**：[18ファイルの静的allowlist](../../manifests/drafts/v39-unis4b-and-vq-source.candidate.json)を保持。VQ作者コードがtorch.load分岐とtrust_remote_code=True分岐を含み、重み形式がsafetensorsでも実行安全性は自明でない。同族4B Sequence/34B/38Bは独立性能の増分なしには追加しない。
- **NVIDIA Kumo Relational/Anomalyなど9件**：研究CONDITIONALとして保持するが、公開元サイズと完全テンソル総数を混同せず取得準備を停止。安全なpickle静的監査・作者のバージョン固定・全依存を優先する。
- **150B以上の量子化候補2件**：現在HOLDのまま。全expert総数、実機の完全メモリ、同一条件の150B未満参照と品質/速度、権利を実証しない限り例外採用しない。

## 4. 変数表・検算

| 記号 | 日本語の意味 | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| N | 今回の有効資産数 | 1（件） | 148 | 現行v40のSELECT＋CONDITIONAL | 整数スカラー |
| S | SELECT件数 | 1（件） | 53 | v40の固定決定 | 整数スカラー |
| C | CONDITIONAL件数 | 1（件） | 95 | v40の固定決定 | 整数スカラー |
| G | 最初のGated停止要因の件数 | 1（件） | 19 | readinessのfirst_blocker | 整数スカラー |
| P | 最初の総数不明停止要因の件数 | 1（件） | 9 | 同上 | 整数スカラー |
| F | 最初のsource停止要因の件数 | 1（件） | 118 | 同上 | 整数スカラー |
| H | 最初のHDD停止要因の件数 | 1（件） | 2 | 同上 | 整数スカラー |
| B | 計画アーカイブ上限 | byte | 4,000,000,000,000 | 本人実HDDでは未確認 | 整数スカラー |
| R | 最低空き容量 | byte | 200,000,000,000 | 実HDDで未測定 | 整数スカラー |

整合：**N = S + C = 53 + 95 = 148**、**N = G + P + F + H = 19 + 9 + 118 + 2 = 148**。両式とも件数の加算なので次元が一致する。BとRはbyteで比較可能だが、モデル総パラメータとbyteを混同しない。実HDDの容量・全148件のSHA単位union・外部学習済み依存・キャッシュ・ソフトウェアの合計バイトは未確定で、4TBに収まる確証はない。

## 5. H/T/D/C/U と ERROR CHECK

- **H（反証可能仮説）**：公開規制予測を直接DL許可へ転用せず、現行148件の個別の実務ゲートを分類し、実取得の前に必要な監査・保存単位を減らせる。
- **T（最小検証）**：正本195件、active148件、readiness148件、CONDITIONALアクセス95件をID/ポリシー/責務で結合。最低n_min=148、各件一意・first blocker一意・該当ライセンスと不変ソースの不明は不明のまま維持する。将来実機検証時は各モデルで固定HW/clock/driver/backend/quant-zero-point/context/batchと30試行以上を記録。取得試験は承認後のみ。
- **D（PASS/FAIL/UNCERTAIN）**：採否・ID・初回停止分類・公開規制根拠の区分はPASS。実HDD容量、本人取得権限、最終ファイル集合、全依存、local SHA、復元、比較性能はUNCERTAIN。無許可DL、自動権限回避、誤ったGatedや全体ライセンスの一律断定はFAIL。
- **C（対立仮説）**：モデルの追加価値が既存実装で再現できる、禁止予測よりも期限切れ権利や依存ソフトの喪失の方が先に保存の失敗原因になる、単なるfile scopeが再現できない。
- **U（不確かさ）**：Hubとライセンスの更新、アクセス本人差、データセットの可否、外部モデルの取得、CPU/GPU/HDD実機、量子化と性能評価。経験分布がないため合成標準不確かさu_cと包含係数kは未算定。将来の法的禁止確率も未推定。

**ERROR CHECK**：R91は非実行の分析成果であり、**195登録／148有効、SELECT53/CONDITIONAL95を変更しない。重み本体保存・コード実行・ダウンロード承認0件**。全件の整合は研究JSON生成時に検査した。Python実機の単体テストとユーザーHDD実測が完了したと主張しない。

## 6.〈次に考える問い〉

保存戦略の進捗は「モデル候補を何件追加したか」ではなく、**利用条件・不変原本・依存・本人HDD・オフライン復元まで実証したモデルが何件あるか**で測るべきではないか。
