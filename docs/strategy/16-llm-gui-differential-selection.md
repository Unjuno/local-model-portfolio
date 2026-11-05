# R20 — 無検閲LLMの機能分離とGUIモデルの差分選定

確認日：2026-11-05。基準main：`bab561a3dee1e6895feb526f816ada6c47b98341`。

## 1. 範囲と結論

CURRENTはv17、管理142／有効研究選定97（select53＋conditional44）／hold27／deferred12／excluded6。前回R18/R19の画像・音声を再調査せず、今回は**LLMの後学習・挙動変更**と**GUI位置特定・操作エージェント**の2領域に限定した。優先期間は2026-08-07から2026-11-05。Hugging Face、Exa、開発者GitHub、原論文、評価実施者の公開記録を照合した。Acumenは発見補助であり、採否を裏付ける一次証拠とはしていない。

研究台帳上の結論は**CONDITIONAL 3、HOLD 2、REJECT 1、SELECT 0**。確度を超えて正式採用とはしない。CURRENT・実体化カタログ・proposed/approvedキュー・既存モデルの状態は**変更していない**。今回の6件は97件に追加済みではない。メタデータと本文を調べたがモデル本体取得、推論、GUI操作、同意手続、P2Pシード、ローカル削除は行っていない。

正本：[6候補の機械可読判定](../../catalog/research/2026-11-05-round20-decisions.json)、[ファイル証拠](../../manifests/drafts/round20-llm-gui-evidence.candidate.json)、[判断規約補足](../../policies/llm-gui-evidence-addendum-r20.md)。

## 2. 候補一覧

全件の確認日は2026-11-05。更新日はHubから得た観測で、初回公開日やウェイト変更日と同一視しない。総数は公開されている主モデル規模と完全構成の確定を区別する。GBは十進。

| 優先 | 正確なモデル／配布元 | 更新日の観測 | 技術・機序 | パラメータ情報 | 容量の根拠 | 判断・信頼度 |
|---|---|---|---|---|---|---|
| 1 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)／[同作者GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | 11-04 | 政治的な回答拒否に焦点を当てた派生。具体的編集・学習手順は未開示 | 主モデル約27.7814B。完全構成の実査未了 | Q4本体16,810,714,592 B、画像projector927,606,944 B。合計17,738,321,536 Bは2重みだけ | **CONDITIONAL**。出所中／品質中（作者評価） |
| 2 | [DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | 09-16 | 多段調整＋拒否方向変更＋healing追加学習という作者説明 | 主モデル約27.7814B、補助MTP等は選択版ごとに確認 | 元repo表示55.6GB。12シャードと追加MTP等。選択byte・Q6実体の完全固定は未了 | **CONDITIONAL**。出所中／品質中。既存派生との入替比較候補 |
| 3 | [PrentisAI/GroundGUI-8B](https://huggingface.co/PrentisAI/GroundGUI-8B) | Hub10-15。treeの相対日時とは不整合あり | ScreenRef SFT→on-policy自己蒸留→RLOO。単画面の対象位置推定 | 主モデル約8.7671B。フル実行構成の確定は別 | 本体17,534,340,584 B。tokenizer/processor/設定は別 | **CONDITIONAL**。出所中〜高／品質中（作者評価） |
| 4 | [inclusionAI/UI-Venus-2-9B](https://huggingface.co/inclusionAI/UI-Venus-2-9B) | 09-02 | GUI中間学習＋offline RL＋複数teacherのon-policy蒸留 | 名称9B。indexの1,469,680は設定と矛盾。確定総数はnull | indexのtensor payload18,819,627,488 B。実ファイル合計・実行RAMではない | **HOLD**。出所中／総数低／性能中 |
| 5 | `inclusionAI/UI-Venus-2-27B`（[作者プロジェクト](https://github.com/inclusionAI/UI-Venus)） | 未確認 | 論文に27Bファミリーの報告あり | 公開チェックポイントの全総数未確認 | 指定HF IDの検索はnot found。容量不明 | **HOLD**。重みの実在配布確認待ち。不存在を断定しない |
| 6 | [OBLITERATUS/Qwen3.8-27B-OBLITERATED](https://huggingface.co/OBLITERATUS/Qwen3.8-27B-OBLITERATED) | 08-24 | 拒否変更派生、複数包装形式 | 公開主モデル約27.7814B。採用ファイル未選択 | 未確定。人気・ダウンロード数から推測しない | **REJECT：今回の実用保存枠**。失敗解析の価値は別 |

### 今回の基準

政治的な回答拒否、無害な依頼への過剰拒否、有害な依頼への拒否、回答の正確性、一般能力は別の軸である。「より多くの有害依頼に答える」ことを品質改善と扱わない。GUIでは位置特定・局所動作・長いタスクの完了を別々に評価する。現在の公開制限と将来シナリオも混同しない。今回、6件に対する新たな削除予告・規制確率は確認していない。

## 3. 性能の比較条件と反証

| 対象 | 採る理由・既存との差 | 性能の根拠・条件 | 不採用側の理由と次の検証 |
|---|---|---|---|
| Interpretic v2 | 既存のOrcaRouter／0bserverxの広範な拒否変更と異なる、領域選択的な挙動の対照 | 作者BF16：政治的質問113件で拒否98→4。有害依頼100件の拒否100→95。政治試験は非thinking・greedy・最大4096token。一般能力はthinking xhigh・最大65536token。200問の同条件MMLU87.5→86.5。Q4の政治試験も4/113 | 115件中2件を知識欠落として除外している。GPQA89.2→86.4とIFBench79.5→79.0の基準は公式cardで、全て同条件再実行ではない。BF16の有害拒否・一般能力をQ4に移さない。中国語・text-only、LLM judge、評価HW/clock/batch不明。全115＋30問と日本語、正確性・安全拒否を実際のQ4で再検証 |
| DavidAU release1 | 作者のhealing学習が既存の重み編集のみと異なる可能性。単純にもう1つの量子化を足す話ではない | [評価実施者の記録](https://huggingface.co/datasets/spicysharkco/uncensored-leaderboard/blob/main/README.md)：GSM8K250問94.0→96.4、MMLU-Pro500問57.6→67.2。同じ出力形式で答えた430問でも差+8.8ポイント。Q6_K／llama.cpp c1d0e7a00／CUDA／greedy／thinking off。refusal256・GSM8K1024・MMLU-Pro8token上限 | 測定者はモデル作者とは別だが、この比較の別モデルの量子化も配布。GPU型番・clock・batch未記載。汚染未検査、多重比較未補正。Q4・最新の別枝・思考ありに成績を移せない。強みが保持されれば既存Qwen派生との**入替**を検討 |
| GroundGUI | Faraとは異なり、単画面の対象位置を特化学習した部品。[原論文](https://arxiv.org/html/2610.19100)とモデル/データ/コードを公開 | 作者ScreenSpot-Pro1011/1581=63.9%、OSWorld-G369/564=65.4%。vLLM・greedy・temperature0・最大1024token。system promptを明示指定。モデルはBF16。評価HW/clock/batch未確認 | 位置が当たることは複数手順のタスク完了を意味しない。既定generation_configはsamplingなのでそのままでは測定条件不一致。Fara単体vsFara＋grounderの評価が必要。モデルのツール出力を自動実行しない |
| UI-Venus2-9B | mobile/web/desktop全域の別学習系列。[作者報告](https://arxiv.org/html/2609.00028)には長いタスク・安全性の測定もある | OSWorld-Verified70.8%は361task系の参考値。一方OSWorld2.0は108task・150stepで完全成功0%、partial7.5%。author報告WebVoyager90.8%／Online-Mind2Web74.0%。agent推論とgroundingの温度・reasoning条件も違う | 70.8%と0%は同じ試験ではないが、難しい長い操作の弱点を無視できない。Faraの引用値と実行足場・更新日が違う。総数矛盾を修正し、Faraとの同環境の完了率を検証するまで保留。ライセンスunknownだけが理由ではない |
| UI-Venus2-27B | 27Bファミリーが論文表にある | 配布元として指定したHF IDが見つからず、公開重みの試験値と認定不可 | 公開元の正確なリンク・ファイル・版が出た時のみ再調査。9Bやミラーの別名を27Bと誤認しない |
| OBLITERATUS | 重み変更の失敗研究には価値があり得る | 上記第三者Q6測定：MMLU-Pro57.6→53.0、共通形式430問でも-5.1ポイント。有害300件中136拒否。定型句検査だと拒否0となるがjudgeはそう判定していない | 現在の目的では性能損失と既存派生の重複が勝るため不採用。拒否ラベルは安全性と同一でもなく、judgeも誤る。修正版の独立した良好な証拠が出たときだけ再開 |

各数値は作者／評価実施者の観測で、当環境によるモデルの再実験ではない。APIや論文のスコアを別の配布版へ自動継承しない。

## 4. UI-Venusの総数矛盾：小さい表示で通過させない

一次資料は[config](https://huggingface.co/inclusionAI/UI-Venus-2-9B/blob/main/config.json)と[index](https://huggingface.co/inclusionAI/UI-Venus-2-9B/raw/main/model.safetensors.index.json)。indexはtotal_parameters=1,469,680、tensor payload=18,819,627,488 byte。一方、configの語彙と隠れ次元に対応する埋込行列がweight mapに存在する。

| 記号 | 意味 | SI単位 | 定義 | 前提・範囲 | 型 |
|---|---|---|---|---|---|
| V | 語彙数 | 1（個数） | configの248,320 | 正整数 | スカラー整数 |
| H | 埋込幅 | 1（個数） | hidden_sizeの4,096 | 正整数 | スカラー整数 |
| L | 1埋込行列の要素数 | 1（個数） | V×H | 通常のdense埋込というconfigとweight_mapの記述に基づく | スカラー整数 |
| P | index記載の総数 | 1（個数） | 1,469,680 | この値は矛盾を検査する対象 | スカラー整数 |

L=V×H=1,017,118,720であり、Pより大きい。従ってこのconfig/weight_mapを採用する限り、Pを完全モデルの総数とは扱えない。これは完全総数を求めた計算ではない。全tensor headerとdtypeを読んで確認する必要がある。**次元チェック**：ここでは要素数を比較しており、18.82GBのbyte数をそのままパラメータ数へ置換していない。重み全体が一様BF16だと未検証のまま仮定することも避ける。

## 5. 権利・再取得・容量

GroundGUIのLICENSE本文はApache-2.0を確認したが、データセット／スクリーンショットの利用条件は別。InterpreticはApache継承を作者が明記、GGUF側LICENSE URLの取得は失敗しており、本文一式の保全は未完。DavidAUはApacheのmetadataで、全ドナー・親モデルの条件照合は未完。UI-Venus作者は重量物のライセンス確定待ちと矛盾の存在を明示している。このための調査を止めるのではなく、性能・同一性と独立して非商用研究用途の条項を調べる。

正規HFを第一経路とした。今回は新たなCivitai/ModelScope/Pirate Faceを使う必要性を確認していない。これらにミラーが存在しないという意味ではなく、無関係な索引を調べるために範囲を拡張しなかった。取得条件の迂回・同意代行・P2Pの起動はしていない。

Interpretic Q4＋画像projectorの2ファイルとGroundGUI本体の**出所記録**は合計35,272,662,120 B。ただし2候補の完全推論一式でも、このサイクル全候補の総追加容量でもない。Git LFSのSHA-256とサイズは確認したが、mainは可変参照であり、完全commit・設定・コード・tokenizer等が未固定。ローカル本体hash実測をしたとは記録しない。

台帳の3.8TB／空き200GBと、会話内の約3.95TBの希望は未照合。実ディスク空きも未測定。今回は予算や取得許可を変更せず、どちらの数字も空き容量として使わない。150Bは通常候補の目安、超過量子化例外は現行ルールのまま。新しい6件に超過例外を追加していない。

## 6. 実際の入替方針と検証の終了条件

**変更しないもの**：Nanbeige4.3-33B、既存の6除外、公式Qwen3.8原本、現在のFara選定。過去の保留を最新という名前だけで戻さない。

DavidAUはOrcaRouter／0bserverxのどちらかと入れ替える比較先であり、3派生を無条件に積み増さない。Interpreticは選択的挙動の対照枠として別価値を検証する。GroundGUIはFaraの視覚位置特定を補えるかを試し、完全エージェントの置換とはしない。UI-Venusは総数と実際の長期タスクを再検証するまで保留する。

H：基盤にない学習成果が、同一条件の実用課題で有用である。
T：既存ルールの固定ハード・backend・quant・context・batchの比較。政治試験は除外した項目も併記し事実性を評価、LLMは公開学習分布と別の課題、GUIはoffline位置特定と隔離環境内の完了率を別に測る。閾値は評価を見る前に決める。
D：機能差と品質・資源条件が確認できれば昇格、重複や重大劣化なら不採用、証拠不足はUNCERTAIN。研究判定から取得権限を導かない。
C：知識不足を検閲と誤認、judge偏り、回答形式の差、訓練汚染、backend不一致、座標精度を成功率と混同、長いcontextでOOM。
U：judge系統誤差、ハード/clock不明、入力分布・ベンチ選択・量子化差。実測分布がないため合成不確かさや生成速度を捏造しない。

今回の公開資料調査はこの6件で終了する。実機データのないまま候補名だけを追加して回数を稼がない。次は新しい名前探しより、上位3件の固定版と既存モデルとの比較を優先する。

## 7. 検証範囲

`tests/test_research_round20.py`は研究台帳、反証、拒否軸、総数矛盾、SHA/byteの由来を検査する。フルrepoを利用できるCIでは142件全ての状態・ID一意性・97件とqueueの一致・Nanbeige・6除外を検査する。ローカル作業ディレクトリにはフルrepoを取得できなかったため、その1検査はskipしCI結果と区別する。ネットワークもモデルも実行しない標準ライブラリの検査で、性能を証明するテストではない。
