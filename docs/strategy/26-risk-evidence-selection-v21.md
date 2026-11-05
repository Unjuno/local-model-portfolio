# v21 — 規制・配布制限の一次証拠に基づく追加選定（2026-11-06）

## 1. 結論

「危険そうな能力」だけでは採用しない。**現在の配布制限、将来の条件付きシナリオ、失われる独自の学習成果、品質の負の証拠**を別々に記録する。既存154資産は変更せず、4件を非実行のconditional選定に追加し、1件をHOLDとして登録する。結果は159資産・有効112件。2つの音声モデルは全依存パラメータ数未確定の研究専用conditionalで、取得準備は停止したまま。

4TBの選定上限と実空き200GBの条件、150B超量子化の同等RAM規則は変更しない。今回の追加計画上限は**92GB**（Holo4 75GB、SteerTTS 2GB、Maya2 10GB、公開評価軌跡5GB）。上限枠であって実測された使用量・残量ではない。既存全件の選択ファイル容量は未確定で、全体が4TB以内と検証したわけではない。

## 2. 規制の事実と推論

**事実：** 中国CACの[2026年4月30日通知](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm)は、無断の顔・声の模倣、agentによる認証情報窃取、重大なリスクを持つ開源モデル・データセットの安全管理不備を対象にする。[7月6日の実施報告](https://www.cac.gov.cn/2026-07/06/c_1785081384384987.htm)は開源データセット9件の下架を報告している。ただし記事はそのrepo IDを示さず、今回の候補との同一性は確認できない。外国のHF配布や日本での個人研究が一律禁止されたという意味ではない。

**反対証拠・適用範囲：** [FTCのTAKE IT DOWN Actガイド](https://www.ftc.gov/business-guidance/resources/complying-take-it-down-act)は2026年5月19日以降、対象プラットフォームに非同意のintimate画像に関する有効な削除要請への対応を求める。これは一般モデル重みの一律配布禁止ではない。

**配布者の現実の制限：** [StyleStream公式カード](https://huggingface.co/Louis0324/StyleStream)は、voice-cloning misuseを減らすためstyle encoderの重みを含めないと明記する。これは政府の命令でなく、公開する能力を開発者が限定した一次事例。公開部分はcurated target embeddingsを使うため、論文が記述する任意話者クローン全能力とは区別する。

**推論：** 本人同一性のある音声、複数の外部操作を実行できるagent、環境・個人情報を含み得る評価記録は、今後のアクセス制限や配布方針見直しに注目する価値がある。ただし**今回の5件に対する削除命令・近日停止予告・規制確率は確認していない**。Gated/非商用条件だけで削除確率が高いとも推定しない。

## 3. 全件比較表

全件の確認日は2026-11-06。HF connectorの現在メタデータとExa/一次Web資料を使用。ファイル本体の取得・実機実行はしていない。各リンクが一次配布元。

| repo ID | 確認済みの制限 | 条件付きシナリオ | 独自性・採否 | 調査優先と反証条件 | 未解決事項 |
|---|---|---|---|---|---|
| [Hcompany/Holo4-27B](https://huggingface.co/Hcompany/Holo4-27B) | CC BY-NC4.0の重み。親QwenはApache2.0と明記 | 自律GUI/コード/MCP操作の権限・悪用管理 | **conditional**。独立SFT/RLと評価軌跡の組。Faraや親Qwenとの同一条件比較対象 | S1。親/既存モデルとの独自差が消えたら延期 | 作者harness依存、固定版・容量・条件、本人実機 |
| [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts) | **Gated**、声・重みの非商用条件。READMEとLICENSEのコード条件に相違 | 声の同意・出典・アクセス条件の強化 | **研究専用conditional**。12音響属性の明示数値制御 | S1。既存TTSに制御の実用上の利点がなければHOLD | 全依存総数、本人Gated承認、コード条件の版矛盾、声/イベントbank権利 |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | 主重みApache2.0、Mimi/ECAPAは別部品。停止予告なし | 声の本人同一性を持つモデルの将来の配布見直し | **研究専用conditional**。11インド諸語＋英語の後学習とstreaming | S1。既存TTSで同等の言語品質なら重複として延期 | 全依存総数・固定版・独立自然さ評価・クローン評価 |
| [Hcompany/trajectories](https://huggingface.co/datasets/Hcompany/trajectories) | Apache2.0＋上流taskライセンス。作者はマスキング・一部省略を明記 | 出典・個人情報管理による記録の改訂/部分削除 | **conditional**。7366の公開評価軌跡、失敗・検証過程。訓練データではない | S1。未除去の秘密/個人情報や権利不適合があれば問題範囲を除外 | 画像を含むprivacy/権利、完全固定ファイル、offline verifier |
| [Louis0324/StyleStream](https://huggingface.co/Louis0324/StyleStream) | **style encoder非公開**、research/education/not-for-profit条件 | 部分公開という実例の記録。公開subsetの停止は予測しない | **HOLD**。声質変換の公開subsetのみ研究 | 公開部分の総数・再現品質が確認できた場合のみ再審査 | 全総数不明、任意話者clone不可、.ckpt安全検査。非公開重みを迂回取得しない |

代替配布元は、全候補について**同一revision・同一SHA256で正規配布が確認された独立ミラーは未確認**。GitHubの推論コードは重みミラーではない。本人アクセス許諾やGated同意は取得していない。

## 4. 品質評価で修正した点

[Holo4公式記事](https://hcompany.ai/newsroom/holo4)は、OSWorld2の**部分点61.7%**と**成功率41.5%**を区別している。前者を完了率としない。AutomationBench公開600タスクのうち480は学習データを集めたsplitに属し、120件のheld-out比較を重視する。実験は作者harness、OSWorld2は単一run、評価HW/clock/batchは不明。利用料によるcostをユーザー実機速度に置き換えない。

SteerTTSは作者による62未見話者×16文の再測定を示すが、pause/voiced/cppsなど弱い制御も示す。全モデル9.6Mと書くのは誤りで、外部vocoder/encoderやflowを含めて未確定とした。[LICENSE.md](https://huggingface.co/WhissleAI/steer-tts/blob/main/LICENSE.md)のMITコード表記と現在READMEのNC表記を、固定commitで解消するまで法的クリア済みとしない。

[Maya2公式カード](https://huggingface.co/maya-research/maya2-native)は6000held-out文の自動ASR評価であり、人の自然さ評価・任意話者clone性能の証明ではない。HFの主重み2.5024Bには別取得のMimi/ECAPAを混同しない。独立ランキングの版同一性も未確認。

## 5. H/T/D/C/U・適用分野

**H：** 今後12か月の候補ごとの配布状態・LICENSE・公開部品の差分を調べると、少なくとも一部にアクセス条件の変更が観測される。ただし規制が原因とは自動分類しない。**T：** 固定したrepo、日付、ライセンス本文、公開履歴を初期値として、変更は前後2観測と当事者一次説明で確認。性能は同条件・未見データで評価し、参照モデル・閾値・試行数を事前登録する。**D：** 変更の存在は差分と一次説明が両方確認できたらPASS、検証期間中に変化なしなら「当該期間の変化仮説」はFAIL、欠測や原因不明はUNCERTAIN。採用/取得は独立の全ゲートが揃うまでUNCERTAIN。**C：** 不具合・価格・商用戦略・権利訂正による制限であって政府規制ではない場合。**U：** 履歴欠落、キャッシュ、版相違、評価の訓練混入、パラメータ数の部品漏れ。分布未測定のため合成標準不確かさや規制確率を捏造しない。定期監視は本作業では設定していない。

関連分野は**AIガバナンス**（法と任意の公開方針を分離）、**計算機システム**（RAM・量子化・依存の完全性）、**音声/agent評価**（機序別の対照・測定）、**デジタル保存とデータ権利**（版と出典、合法な公開範囲の保全）。

## ERROR CHECK

元154件の採否・説明・保留を維持。新規5件のrepo+kind重複なしをプログラムで検査し、全件download_approved=false。unknown-totalのconditionalは取得準備停止。元の150B超2件はHOLD維持、同等RAM規則を緩めない。全件容量はnullを含み、92GBの追加計画枠を実測容量や物理残量に流用しない。CIの実行結果はintegration-checkとActionsログで確認する。
