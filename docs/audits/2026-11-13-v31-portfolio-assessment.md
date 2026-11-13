# v31（179資産）ポートフォリオ評価：2026年11月13日

この文書は専用ブランチのメタデータ監査のみ。取得・実行・権利同意・現行選定・approvedキューの変更なし。

## 1. 基準・評価結果

GitHub Unjuno/local-model-portfolio / branch strategy/2026-11-03-01-risk / 基準 9b9cc355d6c26c2cb2a88c71a5278529f25d91b2
mainのv19とは分岐しており、現行研究正本はcatalog/CURRENT.jsonのv31。
179件（モデル153、データ26）、有効132件（select53、conditional79）、hold28、deferred13、excluded6。全179件一意。
総数PASS131／UNKNOWN20／150B以上例外研究HOLD2、データ26は対象外。UNKNOWNのうち有効7は取得準備停止。承認キュー0。
多様な専門用途を保存する設計自体は合理的。ただし復元可能な一式（学習済み依存、固定SHA、ライセンス正文、実HDD空き）としての完成度は低く、現時点で大規模取得はNO-GO。

## 2. 現行選定132件の取得ゲート

正本に選択byte未登録：130、固定最終SHA未登録：130、ライセンス正文レビュー未登録：129、依存レビュー未登録：130。これらのnullは別容量調査の既存scopeがなかったことを意味しない。
有効で総数が未確認の7モデル：
- ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8
- Stuubs/Stubelius_Remix_Ltx2.5
- WhissleAI/steer-tts
- maya-research/maya2-native
- fishaudio/drama-3
- ausboss/Qwen-Image-2.1-Consistency-LoRA
- PrunaAI/P-H3-Image
元モデルの主数値だけでなく、MoE全expert、追加のcodec/encoder/VAE等も定義・静的計数し、証拠がなければ取得準備を停止。

## 3. 物理容量と既知ソース容量の分離

v27に記録された126件の既知ソース内容SHA重複除去後容量は3,417,685,712,585 byte。v28〜v31追加6資産、完全学習済み依存、実ディスクのキャッシュ・一時コピー・現在空きは未確定。
計画上限4TB/最低空き200GB。空の4TBフォーマット済み容量を仮定するとv27の既知ソースを置いた後の仮想余力382,314,287,415 byte。もし空の3.8TBなら182,314,287,415 byte。実機余力の主張ではない。

### 変数表・次元チェック
| 記号 | 日本語の意味・定義 | SI単位 | 範囲/前提 | 型 |
| --- | --- | --- | --- | --- |
| C | 仮のフォーマット後容量 | byte | 4e12又は3.8e12、実測前 | 整数スカラー |
| B | v27の重複除去後ソース容量 | byte | 3417685712585、後続依存外 | 整数スカラー |
| F | 安全空き床 | byte | 200000000000 | 整数スカラー |
| R | 理論残余 C−B−F | byte | v28以降/一時キャッシュ不算入 | 整数スカラー |
| P | 全学習済みパラメータ総数 | 1（無次元） | MoE全expert含む、未知null | 整数/null |
| M | 実装依存の推論ピークRAM | byte | OS/KV/codec含む、実測null | 整数/null |
Rの減算は全項がbyteで次元一致。Pの個数を直接byteとして扱うことは禁止。

## 4. 選定品質と重複審査

同系統でも別学習SFT/RL/蒸留は固有研究資産だが、量子化だけのコピーを増やしてはいけない。次の群は重複確定ではなく学習状態と容量比較対象。
- Qwen3.8-27B：有効5件。orcarouter/Qwen3.8-27B-Uncensored、InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF、0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF、Qwen/Qwen3.8-27B、DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU
- LTX-2.5：有効3件。Lightricks/LTX-2.5、ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8、Stuubs/Stubelius_Remix_Ltx2.5
- Qwen-Image-2.1：有効3件。chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1、Qwen/Qwen-Image-2.1、ausboss/Qwen-Image-2.1-Consistency-LoRA
- Qwen3 TTS：有効3件。Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice、Qwen/Qwen3-TTS-12Hz-1.7B-Base、Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign
特にLTX-2.5の派生2件とQwen-Imageの親＋LoRAの学習済み依存閉包、Qwen3.8の5件の実測差別化を優先。

## 5. 2026-11-13時点の一次資料で確認した穴

Runway Praxis-1は2026-11-11公開の27.2B総数MoEワールド行動モデル。公開元 https://runway.com/news/company-news/praxis-1-is-now-available と技術報告 https://runway.com/research/praxis-1-video-pretraining-to-robot-control、実装 https://github.com/runwayml/praxis-1-oss 。runwayml/praxis-1-droidは未採用候補として独立性/容量/権利を比較する。BF16本体の公称54.4GBにWan2.2 VAE、Qwen3.5-2B encoderが必要。DROID/YAM/Base/NVFP4 QATを全保存しない。RoboLab-120 46.2%/1200エピソードは開発者報告で実機独立再試験ではない。
既存の未採用meta-models/Muse-Glimmer-30B、PrimeSim、NorthCUAは docs/strategy/44-v28-pinned-source-capacity-2026-11-08.md で既に原本バイト監査済み。先にその報告を再利用する。
thinkingmachines/Inkling-2-Smallは公式に594B total /17B activeと表示。150B以上量子化の同等RAM実測証拠なしで取得候補にしない。

## 6. 150Bポリシー矛盾

v9の150B絶対除外と現行v31のBASELINE_WITH_QUANTIZED_RUNTIME_EXCEPTIONは異なる。現行の2例外はHOLDのままで、同一HW/backend/ABI/context/batchの150B未満対照モデルに対して、30試行以上でピークRAM・品質・速度・権利を検証するまでは取得不可。量子化はパラメータ総数を減らさない。

## 7. 研究実行順

1. ユーザーHDDの実容量・空き・cache測定。
2. v31選択ファイル・学習済み依存の固定SHAと重複排除後bytes再計算。
3. 有効7件の総数不明をモデル実行なしの静的検査で解決。
4. Gatedの本人アクセス権限とライセンス正文の確認。
5. Qwen27B、LTX2.5、画像LoRAの学習状態重複と再現性比較。
6. Praxis-1と既存Cosmos/Alpamayo/GR00Tの差分検証、Muse/PrimeSim/NorthCUAは旧監査を参照。
7. 別途本人の承認があれば小型ELYZA又はChronosで取得・現物SHAチェックを開始。今回は未実施。

## 8. H/T/D/C/U と ERROR CHECK

H：候補追加より現在の権利、未知総数、容量・依存を閉じるほうが承認可能な取得パッケージを増やす。
T：n_min=179件全件を静的照合、うち132有効の権利・SHA・依存・容量・承認を再確認。推論が許可されれば同HW/clock/backend/量子化zero-point/context/batchで30試行以上。
D：PASS＝全必須依存、正規の権利、固定全ファイルSHA、実HDD床、ユーザー承認が揃い、取得後現物整合。FAIL＝無許可、150B等の規則違反、容量不足、SHA不一致。その他UNCERTAIN。現状一括NO-GO。
C：外部codec/ABI不適合、同一重み異形式の重複、cache倍化、規制ではなく配布者権利更新。
U：外部依存の未知容量、HDD空き、上流変更、契約と性能が未測定。合成標準不確かさu_cと包含係数kは標本なしで定義できず、数値化しない。
ERROR CHECK：179一意・153/26・132有効・総数131PASS/20UNKNOWN/2例外研究・承認0。Exa追加検索はHTTP402で未実施、代替Webの開発元一次資料を使用。

〈次に考える問い〉：完全復元可能な最初の1資産を確定させる作業と、新規候補をさらに10件追加する作業のどちらが、実際の保存失敗リスクをより下げるか？
