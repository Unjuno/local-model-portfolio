# R23：全身動作転写・音声駆動アバターの差分選定

確認日：2026-11-05。基準main：`6021cbeb1dc7b5c1068cf4134cf1f1ac71e885c2`。

## 結論と範囲

全142資産（select53、conditional44、hold27、deferred12、excluded6）、CURRENT、提案/承認キュー、過去20件の調査・提案ファイルを照合した。今回の6候補はその台帳に未登録。画像LoRA・一般音声・Qwen派生の再調査は行わず、既存LivePortraitの顔駆動、Wan2.2-TI2V-5B/LTXの汎用動画では代替を確認できない**全身動作転写と音声駆動アバター**に絞った。

**研究推薦はCONDITIONAL2件・HOLD4件。正式カタログへの適用は0件。** CURRENTはv17、142資産・有効97件のまま。Nanbeigeの維持と6件の除外、承認キュー、実機ストレージを変更しない。SELECTに相当する独立品質・実行可能性の十分な証拠は今回得ていない。

## 1. 六候補の比較

| 優先・配布元 | 公開/更新 | 方式と独自性 | 規模・保存容量 | 性能・反証 | 条件・判断・信頼度 |
|---|---|---|---|---|---|
| 1 [Wan-Animate-2 Base Diffusers](https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B-Diffusers) | 元公開2026-08-07、変換repo更新08-13 | 生の駆動動画をdual-branch DiTへ入力。骨格抽出器を介さない全身動作転写 | 主DiT16.395B、画像encoder/T5/VAE込み保存要素22.833B。主な全重み9件45,920,934,868 B | 作者研究で旧Wan-Animateに70%超の対比較選好。n・評定者数・クロック/バッチ未確認。BaseにLiteの速度を移せない | Apache-2.0宣言、公式コードLICENSE本文確認。**CONDITIONAL・中** |
| 2 [LongCat-Video-Avatar 1.5](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5) | 論文2026-05-26、重み更新06-04。90日外 | 入力音声で複数人物を駆動。RLHF後DMD蒸留、継続生成。TTSそのものではない | 元DiT15.853B、確認済み構成23.835B。ただしONNX音声分離器の総数は未知。INT8+依存13重み44,788,614,746 B | 作者主導508組・770人・13,240評定。高速版は安定性に利点、Baseは口同期/表情豊かさに利点。独立再現・日本語・INT8同等性なし | MIT宣言、親とコードの本文確認。Avatar自身の独立LICENSEは一覧で未確認。**CONDITIONAL・中** |
| 3 [SCAIL-2](https://huggingface.co/zai-org/SCAIL-2) | 公開06-09、重み更新07-15、訓練コード08-06 | reverse-driving、合成60K組、人物置換/複数人/relighting | 全数未知。主checkpointだけ65,582,563,395 B、encoder/VAE/LoRA別 | 置換・relightingは固有価値があり得るが、Wanとの同条件優位は未確認 | HF重みMITタグ、コードApacheは別スコープとして要精査。**HOLD・低〜中** |
| 4 [Live-Avatar](https://huggingface.co/Quark-Vision/Live-Avatar) | 公開2025-12-08、重み更新12-09 | 4stepの長時間ストリーミング蒸留LoRA | adapter1,352,769,792 Bだけ。Wan2.2-S2V-14B等の完全依存・総数未知 | 45fpsはmulti-H800の作者測定。1.35GBで全体が動くわけではない | Apache宣言、親/実行依存は別。**HOLD・低〜中** |
| 5 [Hallo-Live](https://huggingface.co/fudan-generative-ai/Hallo-Live) | 重み更新2026-05-15 | テキストから音声と映像を同時生成するcausal dual-stream | 全数未知。主checkpoint23,322,224,760 B、Ovi関連依存別 | 作者20.38fps/0.94秒は2×H200。個人機・日本語・完全構成は未検証 | MITタグ/コード宣言。**HOLD・低〜中** |
| 6 [AVTR-1](https://huggingface.co/avaturn-live/avtr-1) | 重み更新2026-05-31 | speech/listening二入力の動作生成＋LivePortrait派生renderer | 総数未知。既知coreとplugin1,902,560,136 B、renderer/InsightFace/engine別 | 作者表は4060Tiで5frame166msだが反復数/精度/VRAMなし。後段のA100測定との記述も要確認 | auto-Gated、Community/InsightFace研究用/streamer非商用を分離。**HOLD・低〜中** |

古いという理由だけでLongCatを除外しない。作者の現行公開Avatarとして確認した1.5に、音声を指定した複数人物・継続生成と人手評価という保存価値があるための例外候補であり、「全動画モデル中で最新」とは言わない。独立評価は6件とも今回確認できていない。

## 2. 性能を読み違えない

[Wan原論文 arXiv:2608.06009](https://arxiv.org/html/2608.06009)の24fpsは**Lite・4×H100・400×720・3step**。公開Base/Distilledの参照実装は8×A800で720P、2×A800で480Pを説明している。Base、10step Distilled、3step streaming Liteを同一視しない。Liteの個別取得可能checkpointは未確認。本文のviewpoint LoRAも公開した特定版で全機能が再現できるとは未検証。

[LongCat原論文 arXiv:2605.26486](https://arxiv.org/html/2605.26486)では508組、主観770人・13,240判断、専門家10人。作者が設計した中国語/英語評価で、日本語や独立再現ではない。8NFEと150NFEの比較で、速い版がすべての品質軸を改善したわけではない。さらに蒸留の比較からINT8の品質保証を導かない。

Wan参照実装はPython3.11/PyTorch2.7.0/CUDA12.6/FlashAttention、LongCat例はPython3.10/PyTorch2.6.0/CUDA12.4/FlashAttention2.7.4.post1・2プロセス。これは作者の環境で、ユーザーの機器・クロック・RAM・速度の実測ではない。ファイルGBを必要VRAMに読み替えない。

## 3. 完全リポジトリ取得ではなく、必要な重みを分離

[固定した22重みの候補台帳](../../manifests/drafts/round23-motion-avatar.candidate.json)は3repoの不変revision・サイズ・配布元LFS SHA-256を記録した**非実行の重み計画**。設定、tokenizer、LICENSE、runtime、wheel、一時領域まで確定した最終lockではない。

WanはBase Diffusersのimage encoder、T5 3シャード、DiT4シャード、VAE。LongCatはINT8本体4シャード、DMD LoRA、Whisper-large-v3、Kim Vocal分離器、親repoからT5 5シャードとVAEを選ぶ。

[LongCat公式読込コード](https://github.com/meituan-longcat/LongCat-Video/blob/main/run_demo_avatar_single_audio_to_video.py)の読取時Git blobは`5fc822ab6c27cf53fef0d9acb5821fec32846d76`。既存のWhisper-large-v3-turboはこのWhisper-large-v3の代用品としない。vocal separatorは参照コードで読み込まれるので勝手に任意部品にしない。不要な親foundation DiT、BF16/INT8二重取得、WhisperのFP32/bin/Flax複製を除いた。コードは読んだだけで実行していない。

選択重み合計は90,709,549,614 B。VAEの同一SHA-256が確認できた507,591,892 Bだけは、将来の実ファイル照合後に共有できる可能性がある。両構成のT5は同じ要素数でもBF16/F32とファイルハッシュが違うため、同一重みファイルとして容量を消さない。実際のHDD増分・節約量はnull。

## 4. ヘッダー検証と証拠の限界

23ファイルにHTTP Rangeを指定し、合計833,936 Bのヘッダーだけを読み取った。206/Content-Range・長さ・shapeとdtype幅・offset・ファイル末尾を確認。tensor値領域の取得は0 B。`.pt`やTorchScriptをdeserializeせず、モデルや推論コードをimportしていない。

Wanは全保存float要素22,833,447,731（DiT16,394,878,784、T5 5,680,910,336、image encoder630,766,080、VAE126,892,531）。LongCatはBF16元本＋DMD＋Whisper＋T5＋VAEの23,834,929,027まで確認したが、ONNX分離器は未集計なので完全総数はnull。INT8のpacked配列要素数を論理パラメータ数にしない。

| フィールド | 意味 | 単位 | 定義・前提 | 型 |
|---|---|---|---|---|
| serialized_float_scalars | 固定ファイルの保存要素数 | 1（個数） | 各tensorのshape積を合計。buffer/重複を含み得る | 非負整数 |
| selected_weight_bytes | 指定した重みの保存量 | byte | 固定版のAPI表示サイズを整数加算 | 正整数 |
| complete_offline_pipeline_bytes | 設定・runtime込み総量 | byte | 未確定。重み合計と同じにしない | 整数/null |
| local_peak_ram_bytes | 実機推論ピーク | byte | 未測定なのでnull | 整数/null |

単位検査：要素数はbyteではない。BF16/F16は2byte、F32は4byteでoffsetを照合した。GBは十進、速度fpsは保存容量と比較しない。ヘッダーhashと全重みhashは別であり、モデル全体のローカルSHA-256確認は未実施。

## 5. 入替・アクセス・検証の停止条件

LivePortraitを削除しない。軽量顔駆動、全身動画転写、音声駆動、音声映像の同時生成は別の制御機構。Wan2.2-TI2V-5BやLTX2.5を新モデルが完全代替する証拠もない。SCAILとLiveAvatarは機構を比較する保留対象であり、初回から同系列を全部取得しない。

Wanの作者が案内する[ModelScope版](https://modelscope.cn/models/Wan-AI/Wan2.2-Animate-2-14B)は正規代替候補だが、今回のDiffusers版とのrevision/全hash一致は未確認。Pirate Faceの新規検索・seed開始はしていない。AVTRのGated同意・連絡先提供も行っていない。ライセンスタグ単独で不採用にせず、[Wan LICENSE](https://github.com/Wan-Video/Wan-Animate-2/blob/main/LICENSE)と[LongCat LICENSE](https://github.com/meituan-longcat/LongCat-Video/blob/main/LICENSE)本文を読んだ。研究許諾・人物の同意・再配布許諾は別判定。

H：既存モデルにない制御能力が、同意済み人物の固定テストで保持される。T：20動画×3seedを事前固定し、人物保持・動作忠実度・口同期・長時間破綻・GPU/RAMピーク・速度を別々に比較する計画（未実施）。D：品質/資源の事前閾値と完全依存が未確定なので現状CONDITIONAL/HOLD、取得PASSではない。C：小型既存モデルで代替可能、音声同期の劣化、長尺破綻、非実用的なoffloadで推薦を下げる。U：作者選択バイアス、言語差、量子化劣化、機器差が主な未知。実測なしに合成不確かさや規制確率は作らない。

関連分野：機械学習（動画条件付け・蒸留）、人間工学（口同期・人物保持の知覚評価）、ソフトウェア供給網/デジタル保存（実装・依存・固定版の再現）。現在の削除予告や規制予定は6件とも確認していない。人物同一性の合成が先行制限対象になることはあくまで保存シナリオ。

外部メタデータ取得後にFirecrawlのセッションが終了し、追加呼出しはクレジット不足で失敗した。再試行・課金・権限変更はせず、取得済み証拠で範囲を閉じた。未取得のファイルや実行結果を補完していない。

## ERROR CHECK

新規テストは資料未作成時のFAILを確認してから作成。10テストで6件の一意性、反証条件、Base/Liteの分離、未知総数、22重みの加算・固定版・hash形式、LongCat依存漏れ、VAE共有の条件を確認。CURRENT・正式カタログ・approved・HDD・モデル本体に変更なし。CI成功は実機性能や全重みの取得成功を意味しない。
