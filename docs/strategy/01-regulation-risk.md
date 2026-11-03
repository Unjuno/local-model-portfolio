# 配布制限の連鎖を想定した長期アーカイブ戦略：132資産の独立再評価

<small>2026-11-03 · Session 01 / 規制・公開リスク調査</small>

## 1. エグゼクティブ判断

**保存の最大化ではなく、将来の正規再取得経路の収縮に対する損失を抑える**のが目的。利用者が指定した「まず潜在的悪用能力、次に高性能モデル、最後にオープンウェイト全般」というシナリオを**反証可能なストレスケース**として維持する。ただし、これを特定モデルの禁止日程や実測規制確率とはみなさない。

旧S1/S2/S3は能力の危険性と権利・ホスティング条件を混同していた。そこで**(A)予測対象となる変更の経路（ターゲット能力、プライバシー/出典、契約/Gated、全モデル配布）**、**(B)現在実際に観測された制約**、**(C)独自重み/再構築困難性・第三者依存**を別に扱う。

**成果物**：[全132資産の順位と根拠を格納した非実行JSON](../../catalog/proposals/01-regulation-priority.json)。この資料は**選定案**であり、ダウンロード承認、規約同意、mainの変更、`CURRENT.json`の更新を行わない。

- 基準コミット：`6e9389c97d24528df97e4b14a6bc772780141fd3`、元の台帳`v9-20261103`
- 追跡資産：**132件**（モデル109、データセット23）
- **総パラメータ150B以上2モデルは完全除外**、12モデルは総数不明でlock作成不可
- **24件のGated表示をHugging Faceアプリのメタデータで2026-11-03に再確認**。残り108件の「public」は旧v9台帳の観測値であり、**2026-11-03時点の再検証済みとは主張しない**。
- 費用制約：十進3.8TBの論理上限、200GBの物理空き確保、推定推論ピークRAM512GB未満。上流全リポジトリ容量と取得する選択ファイル容量を混同しない。

## 2. 実在する公開/権利の変更と、まだ起きていないシナリオ

| 分野 | 一次資料と確認された事実 | 資産選定への帰結 |
| --- | --- | --- |
| **データ安全** | [LAION自身の再公開報告（2024-08-30）](https://laion.ai/blog/relaion-5b/)：2023-12-19のLAION-5B停止と安全性の再点検、既知の問題リンク除去後のRe-LAION-5B公開 | 旧アーカイブを無条件で保管する理由にならない。適法・修正済み版を優先し、各版の権利を再確認 |
| **権利者による個別のモデル公開停止** | [GEITje作者の告知（2025-01-25）](https://goingdutch.ai/en/posts/geitje-takedown/)：著作権権利者団体の求めを受けてモデルファイルをHugging Faceから削除 | 「公開後の取得停止」はモデル本体でも実例がある。ただしこの個別事例は他のモデルの停止を予告しない |
| **ソースコードの削除申請** | [BigCode The Stack v2（現行カード）](https://huggingface.co/datasets/bigcode/the-stack-v2)：検証されたopt-outを反映するv2.1/v2.2改訂。大量取得にはSoftware Heritage/INRIAとの追加合意を要求 | 「原データの保存」より**許可された処理済み版、帰属、版差分・利用条件**の審査が必要 |
| **ライセンス変更** | [Stability AIによるSD3 Community License改定（2024-07-05）](https://stability.ai/news-updates/license-update)：一部条件を緩和して利用範囲を拡張 | 利用条件は**厳しくなる一方ではない**。規制連鎖が必然だとする仮説への反例 |
| **提供元のアクセス制御** | [Hugging Face Gatedモデル公式文書](https://huggingface.co/docs/hub/models-gated)：自動/手動承認とユーザー別アクセス撤回が可能 | Gatedは**観測されたアクセス制御**であって「間もなく禁止」の証拠ではない。本人のアクセス許諾は別途必要 |
| **AI生成コンテンツ** | [EU AI Act第50条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50)：生成・操作コンテンツの表示/透明性、Deepfake開示等 | 概して**出力・提供/利用の義務**であり、画像/動画/TTS全モデル重みの公開禁止ではない |
| **汎用AIの提供者義務** | [EU AI Act第53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)：文書、著作権ポリシー、学習内容概要等。オープンソースモデルには一定の例外 | 許認可・提供者義務を、そのまま個人のモデル保有禁止と読み替えない |
| **米国の比較軸** | [米NTIAの2024年提言](https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations)：当時は即時の幅広い重み制限より継続監視を推奨 | **2024年時点の公的検討**。2026年の全制度・全配布者の立場を保証するものではない |
| **技術的な不可逆性** | [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/2026-report-extended-summary-policymakers)：公開済み重みは取り戻して完全に回収できない一方、保護策の改変が容易 | **公式Hubから消えても市場からすべてのコピーが消えるとは限らない**。しかしミラーの権利・ハッシュ一致は別途証明が必要 |

**根拠の強さ：** 直接観測した停止/改定・現在のGatedは「事実」。T1→T2→T3の時間順、モデル別に将来の規制対象となること、具体的な確率は「仮説」。どちらでもないモデルを「危険だと判明」とは書かない。

## 3. 旧S1/S2/S3に対する批判と新T1/T2/T3

### 誤分類を直す考え方

1. **一般的な画像/動画生成＝直ちに先行的な重み制限、ではない。** ユーザーに知らせる透明性義務と、ウェイト公開停止の間には別の政策判断が必要。FLUX、Fibo、Ideogram、LTXなど広い合成生成群は原則T2へ移動。顔の一致・声の複製など本人同一性に直接関連する候補とは区別する。
2. **データセットの再配布制限は独立の時系列で起こり得る。** BigCodeのopt-outやLAIONの安全性修正はAI全体の能力規制を待たずに生じる。そのため`DATA_RIGHTS`という別経路を設け、出典・同意・削除条件を先に調べる。
3. **医療・身体動作の制限は用途/専門領域の規則とモデル重みの公開条件で分離する。** MedGemmaの [Health AI Developer Foundations terms](https://developers.google.com/health-ai-developer-foundations/terms)は現に研究/臨床等の利用条件を規定するが、医療モデルが全部削除予定という証拠ではない。
4. **依存が唯一なら、予測段階がT3でも今から権利を確認する。** Idolが必要とする[公式DINOv3 ViT-H+](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m)はGated。別の7B DINOモデルを保存していても同じ重みではないため代替認定しない。
5. **「高性能」「無検閲」の語は性能評価値ではない。** コード・GUIエージェントや改変済みモデルをT1の仮説的対象に置いても、危険な機能の実測や法的分類が終わったと扱わない。

### シナリオ段階の比較

| 旧区分 | 旧件数 | 新区分 | 新件数 | 変更の主眼 |
| --- | ---: | --- | ---: | --- |
| S1 | 45 | T1：ターゲット能力と独立の権利/プライバシー経路 | **32** | 一般画像・動画/TTSを無条件で一括「先行規制」にしない |
| S2 | 44 | T2：高性能/一般合成・専門分野の拡張 | **60** | 自由に使えるのと法的に提供されるのは別 |
| S3 | 43 | T3：広範なウェイト・比較基盤の収縮 | **40** | 直接の制限根拠が薄い基準原本は監視を維持 |

**旧分類から23資産を変更**。段階は予測であり採否は変更しない。段階がT3でも実際にGatedであればアクセス確認は優先できるため、段階と調査の着手順は同一ではない。

### 優先度の運用（確率を捏造しない序数）

| 調査バンド | 件数 | 意味と停止条件 |
| --- | ---: | --- |
| **P0** | **22** | Gatedや権利更新の実例、複製不能な専門原本・重要依存をまず調査。**取得許可ではない** |
| **P1** | **35** | T1のその他の検討、公開条件のあるT2、固有性が高い原本の比較 |
| **P2** | **35** | 拡張波の能力・専門性・学習データ・依存を再確認 |
| **P3** | **38** | 広範な公開モデルの監視、保存容量や重複コストの高い候補 |
| **PX** | **2** | 総パラメータ150B以上のモデルを**完全除外**、根拠と履歴だけ保持 |

この順位は法律上の危険度スコアや規制確率ではない。`P0`のうちHOLD/BACKLOGは**許諾/データ出典の調査だけ**を最初に行う。実際のダウンロード可能順位を意味しない。

## 4. 特に重要なモデル・データの判断例

*全132資産の、repo ID、確認日、一次URL、Gated事実、代替配布元の検証状態、シナリオ/反証条件、独自性、順位、残課題は[JSON全件表](../../catalog/proposals/01-regulation-priority.json)に収録。*

| 調査順位 | 資産と一次URL | 旧→新段階 | 判定 | 最初に解く障害 |
| ---: | --- | --- | --- | --- |
| 1 | [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | S1→T1 | P0 | Gated・個別許諾未確認 |
| 4 | [bigcode/the-stack-v2](https://huggingface.co/datasets/bigcode/the-stack-v2) | S1→T1 | P0 | 既存HOLD/延期 |
| 5 | [laion/relaion2B-en-research](https://huggingface.co/datasets/laion/relaion2B-en-research) | S1→T1 | P0 | 既存HOLD/延期 |
| 6 | [lmsys/lmsys-chat-1m](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | S1→T1 | P0 | 既存HOLD/延期 |
| 8 | [KlingTeam/LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | S1→T1 | P0 | 権利・lock未完了 |
| 10 | [Plachta/Seed-VC](https://huggingface.co/Plachta/Seed-VC) | S1→T1 | P0 | 総数未確定 |
| 11 | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | S1→T1 | P0 | 権利・lock未完了 |
| 17 | [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | S1→T2 | P0 | Gated・個別許諾未確認 |
| 19 | [google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it) | S2→T2 | P0 | Gated・個別許諾未確認 |
| 21 | [facebook/dinov3-vith16plus-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m) | S3→T3 | P0 | Gated・個別許諾未確認 |
| 93 | [nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D) | S2→T2 | P3 | 既存HOLD/延期 |
| 132 | [mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | S2→T2 | PX | 150Bで除外 |
| 131 | [orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | S1→T1 | PX | 150Bで除外 |

**条件付きの具体例**：

- `orcarouter/Qwen3.8-27B-Uncensored` はT1/P0。Gated表示は2026-11-03に再確認したが、無検閲派生のメタデータと元モデルの配布条件の整合は未検証。**許諾なく取得しない**。
- `bigcode/the-stack-v2` はT1/P0でも**現在HOLDのまま**。作者ページが明示するbulk取得の追加合意と削除申請対応を無視して「保存できる」扱いにはしない。
- `black-forest-labs/FLUX.2-dev` は旧S1→T2、ただしGatedおよび独立ライセンスのためP0で先に権利を確認する。上流全repo約177.6GBという**容量負荷**も別問題。
- `mistralai/Mistral-Large-4-1T-A52B`（約1.05T）と`orcarouter/Qwen3.8-Flash-Next-Uncensored`（約180B）は**総パラメータ150B超過でPX**。規制予測上どれほど高く評価しても例外なし。
- `nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D`は上流全repoが約**9.225TB**で、3.8TB保存枠を超える。HOLD/P3。正規のファイル選別と権利が確認されない限り**全量保存不可**。

## 5. 代替配布元と「再取得できる」の必要条件

- **実在する追加の公式配布経路**：[Qwen公式GitHub](https://github.com/QwenLM/Qwen3.8)はQwen3.8-27BおよびQwen3.5-0.8BのHugging Face/ModelScope両方での提供を記載。ただし**両ホスト間で同一コミット・完全ファイルSHA-256を照合したわけではない**。即座に相互代替可能とは認定しない。
- **代替とは限らないもの**：[Software Heritage](https://www.softwareheritage.org/software-heritage-faq/)の一般アーカイブは、BigCodeが権利整理・重複処理した特定バージョンのThe Stack v2をそのまま合法的に一括取得する代替経路ではない。
- **ミラー／torrent**：出所・配布権・個々の重みSHAを検証できない配布元は`NO_FIRST_PARTY_EQUIVALENT_VERIFIED`。アクセスが必要なGatedを迂回せず、他人の同意が必要な音声や画像を無断収集しない。
- **所有だけで永続利用を保証しない**：規約・契約・著作権は別に審査し、ダウンロードできたことを再配布やあらゆる用途の許可と混同しない。

## 6. 反証可能な監視・実装計画

### H（反証可能仮説）

H1：今後12か月（**2026-11-03〜2027-11-03**）の間に、少なくとも複数の独立配布者について、公開重み/モデルカード/アクセス契約の**新規制限**がT1で先行し、その後T2、T3の順に観測される。

H2（対立）：権利・プライバシーによるデータ改訂がモデル性能に無関係に起こり、T2/T3がT1に先行する、またはどの段階も制限されない。**公開者の意思決定が最終的にこの順序に従うとは断定しない**。

### T（最小検証）

- 対象：132資産のユニークな`asset_kind + repo_id`全件（**n_min=132**）、初期状態は基準コミットのv9。調査は**一週ごとの手動/将来の承認済み自動チェックを推奨**する設計であり、本セッションでは継続監視の自動化を設定していない。
- 観測：配布者の公式Hub/APIを定期確認し、`public/gated/manual/removed`の遷移、ライセンスの本文とrevision、公式撤回告知、帰属/削除申請、代替配布の完全ファイルハッシュを記録。前回状態、公式URL、確認日、観測の有効範囲を残す。
- **事後のスコア変更を恣意的にしない**：T1/T2/T3の分類を当初のv9からの変化として固定し、再分類する場合は新revisionで理由と反証条件を追記する。
- 初回は12週間を中間検討、12か月の終了で順序の成否を判定。特定の公式な利用条件変更を観測した場合は、そのモデルのダウンロードを**自動化せず停止し、権利を再確認**。

### D（PASS / FAIL / UNCERTAIN）

- **PASS（仮説の観測に限る）**：少なくとも2つの独立配布者でT1の制限が先行し、後に別のT2/T3を含む段階的な変化が一次証拠と日付で確認される。
- **FAIL**：T2/T3で実質的な広い配布制限がT1より先に発生する、または12か月の固定予測期間内に想定された連鎖が成立しない場合。ただし後者は**その期間の仮説に対する否定**であり「永久に起こらない」という意味ではない。
- **UNCERTAIN**：少数例、配布者の判断理由不明、同日多発の順序不明、公式出典が失われた場合。モデル単体の危険性・法的責任の合否とは別。

### C（破れ方・対立説明）

同時規制、素材の著作権だけに起因する削除、企業収益上の非公開化、Gated状態が継続したまま重み公開も続く場合、逆にStability AIのように緩和される事象、実際の利用行為への規制が重みそのものには及ばない場合。

### U（不確かさ）

支配的な不確かさ：地域ごとの法律と執行、モデルカードとライセンスの時間差、配布者の私的な契約、全体の真の母集団が不明なこと、依存の追加、二次流通の権利不明。確率サンプルと結果分布が存在しないため、合成標準不確かさ`u_c`と係数`k`を定量化できない（適用なし）。

## 7. 監査・統合時の注意

- **書込み許可範囲**：この専用ブランチの`docs/strategy/01-regulation-risk.md`と`catalog/proposals/01-regulation-priority.json`のみ。他の5つの並列セッションのファイルは上書きしない。
- **現行正本との区別**：正本は引き続き`catalog/CURRENT.json`の**v9**。この提案は`v10`を統合する担当が採否を検討すべき`non_executable_research_proposal`であり、新しい`CURRENT`もダウンロードキューも作っていない。
- **単位と性能**：150Bは無次元の総パラメータ（B=10⁹、バイトではない）。HDDのTBは十進バイト。MoE活性数/重みの低bit化/SSD offloadで150Bを下回ったことにはしない。
- **追加調査**：12件の総パラメータ未知を静的に確定。ユーザー個人のGated許可、ライセンス原文、全部品のSHA、正確な選択バイト数、推論実機のOS/backend/量子化zero-point/KV/context/batchとRAM、3.8TBと空き200GBの同時実測を済ませる。
- **監査の停止条件**：`EXCLUDED`や`UNVERIFIED`を実行対象に混入させる、確証のないミラーを正規配布と扱う、法令/契約/本人同意に反するファイルを取得することは禁止。

**自己検証（ERROR CHECK対象）**：全132ユニークIDの一次URL・推定と確認日、24 Gated再確認/108 public履歴、予測変更23件、2件EXCLUDED、12件総数未確認、全行ダウンロード未承認。CIの成功を本提案の実行成功と混同しない。
