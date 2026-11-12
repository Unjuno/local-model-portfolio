# R51｜7モデルの依存監査・SteerTTSライセンス矛盾・NanoのSTNB停止条件（2026-11-13）

> 指定ブランチ `strategy/2026-11-03-01-risk`、親 `29da1dc0c6f1aad599b74a4eb60864d1890edfd6`。**現行v30・178資産／有効131件・ダウンロード承認0件は維持**。モデル本体取得・外部コード実行なし。2026-11-06の固定ソース台帳は2026-11-13のライブHF状態と同義ではない。Firecrawlはクレジット上限のため、HF連携・公式GitHub・公開モデルカード・既存一次ファイル証拠で再審査。

## 1.〈本論〉有効モデル総数未確認7件

次表の数は**メイン重みのみのHF要素**。完全な学習済み部品の合計ではない。旧repo容量は通常量子化・旧checkpoint・宣伝画像まで含むため、保存すべき容量の最終値ではない。

| # | 現行CONDITIONAL | 主モデル個数 | 旧全repo GB | 次の調査・権利条件 |
| --- | --- | ---: | ---: | --- |
| 1 | [`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | 未確定 | 166.916 | LTX2.5 DiT＋Gemma4 text encoder＋映像/音声VAEの総数とdonor license。FP8/INT8/GGUF同重み多形式は一代表。 |
| 2 | [`Stuubs/Stubelius_Remix_Ltx2.5`](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | 未確定 | 195.942 | v1 DiT＋Gemma4/VAE総数、LTX Community License。beta1/beta2/v1は別学習成果だがv1の4精度は別形式。 |
| 3 | [`WhissleAI/steer-tts`](https://huggingface.co/WhissleAI/steer-tts) | 9,585,639 | 0.974 | Vocos13.53M、flow17.64Mまたはpflow24.67M、WavLM約101M、MiniLM約22.7Mなど全学習済み依存。本人Gated権とCC BY-NC code+weights。 |
| 4 | [`maya-research/maya2-native`](https://huggingface.co/maya-research/maya2-native) | 2,502,398,656 | 5.056 | Mimi約96.2MとSpeechBrain ECAPAを追加し完全数を確定。Qwen backbone/depth decoderは本体に含まれ元親の重複取得は不要。 |
| 5 | [`fishaudio/drama-3`](https://huggingface.co/fishaudio/drama-3) | 35,899,643,008 | 41.503 | 外部codec.pth 1,871,099,728byteの学習済み総数、Fish Audio Research License。非承認pickleロード禁止。 |
| 6 | [`ausboss/Qwen-Image-2.1-Consistency-LoRA`](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | 未確定 | 0.329 | rank32 LoRAとQwen Image2.1親＋text encoder/VAEを合算。step1500/2000は各159,436,496byteでSHAが異なる学習段階、二重採用未承認。 |
| 7 | [`PrunaAI/P-H3-Image`](https://huggingface.co/PrunaAI/P-H3-Image) | 33,122,992,896 | 99.845 | Transformer7 shard以外にencoder2、prompt upsampler4、connector1、VAE1の計15学習済みsafetensors。MiniMax地域/用途制限とApache部品。 |

各モデルの40桁固定revision・旧repo bytes・主テンソル数（確認された範囲）・次に解く依存は[機械可読R51](../../catalog/research/2026-11-13-r51-dependency-and-abi-review.json)を正とする。7件とも`UNVERIFIED_BLOCK_FINAL_LOCK`を維持。未知の`P_full`を0にしない。

**Maya2**：本体2,502,398,656個にはQwen初期化backboneとdepth decoderを含む。[Mimi](https://huggingface.co/kyutai/mimi)約96.2Mと[ECAPA](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)の正確な総数、CC BY4.0／Apache2.0のライセンスを別確認。親Qwenの重みを別の実行必須ファイルとして二重計上しない。

**Drama-3**：主モデル35,899,643,008個、別の`codec.pth`は1,871,099,728byte。codecの学習済み総数とFish Audio Research Licenseを未確認。未審査のPyTorch pickleを実行しない。

**Pruna P-H3**：33,122,992,896個は主Transformerのみ。text encoder、prompt upsampler、connector、VAEなどを含めて15学習済みsafetensorsの数を計算する。元MiniMax-H3の地域制限付きCommunity Licenseを別に検証する。**画像LoRA**ではstep1500とstep2000はSHAが違う別学習段階だが、共通元モデルを重複保存しない。**LTX特殊版2件**では各モデルのDiT・Gemma・動画/音声VAEの総数とdonor権利を調べ、通常量子化違いのみを整理する。

## 2.〈本論〉SteerTTSの権利訂正

現行[Whissle公式GitHub LICENSE](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/LICENSE)は**コード・重み・話者音声をCC BY-NC4.0とWhissle独自条件**の対象とする。歴史的な「コードMIT」の説明は現在の公式ソースと矛盾し、今後の権利判定に転用不可。GitHub LICENSEは少なくとも2026-10-31のコミットに存在するため、今月の突然の変更・過去許諾の遡及失効とは断定できない。Vocos MIT、WavLM CC BY-SA3.0、MiniLM Apache2.0など第三者の権利は別確認。SteerTTSはHF側Gatedであり本人の承認を代行しない。

## 3.〈本論〉新候補NanoとEdge2.0は採用保留

[SteerTTS Nanoモデルカード](https://huggingface.co/WhissleAI/steer-tts-nano)は重み`nano.bin`を**STNB v2**と表記。一方、[固定Cヘッダ](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/esp32/components/steertts_nano/include/nano_bin.h)は`NANO_BIN_VERSION=1`、[固定ローダー](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/esp32/components/steertts_nano/src/nano_model.c)はv1以外を拒否し、同revisionのPython writerもv1。**実バイナリの先頭8byte未検証**であり必ず動かないと断定しないが、モデルカードの版が正しい場合は明確にABI不一致。正規アクセスと版に合うローダーの確認が必要。

NanoはESP32-S3・16kHz・2話者・約2.99MB INT8＋約1.8MB前処理で動作する独立小型訓練成果。メーカーRTFはGitHub0.66／モデルカード約0.75で測定条件が違い、混合平均を出さない。[SteerTTS Edge2.0](https://huggingface.co/WhissleAI/steer-tts-edge)には別のv2学習済み音響重みがあり単なるINT4量子化ではないが、v1と機能重複が大きい。**両候補を研究HOLDとし、モデル数を増やさない**。

## 4.変数表とH/T/D/C/U

| 記号 | 意味（日本語） | 単位SI | 定義／型／定義域・前提 |
| --- | --- | --- | --- |
| `N_u` | 有効選定で完全総数未知の件数 | 1 | 7、正整数スカラー |
| `P_root` | 主モデルの個数 | 1 | 非負整数またはnull、全依存を含まない |
| `P_full` | 必須全学習済み数 | 1 | 7件全てnull、未確定 |
| `B_repo` | 旧全repo展示容量 | byte | 非負整数スカラー、2026-11-06版 |
| `B_selected` | 依存を含む選択ファイル容量 | byte | null可、全モデル未確定 |
| `C` | 計画上限 | byte | 4,000,000,000,000、実機未測定 |
| `F_min` | 実機の最低空き | byte | 200,000,000,000、未測定 |

**次元検査**：`P`は無次元、`B`・`C`・`F_min`はbyteだが別の量。主モデル個数と全repo byteから完全総数を推測しない。

**H**：ソースSHA、別学習成果、ライセンス、ABIを分ければ重複保存を減らせる。**T**：現行7元repoの依存メタデータとNanoのSTNB実体版、権利を非実行監査。品質測定は本人承認後、HW/clock/backend/ABI/zero-point/context/batch固定・30例以上。**D**：全総数不明はUNCERTAIN、Nano実体v2＋このv1 CローダーならFAIL、本人Gated許可と全依存・HDD条件を満たすまで取得NO-GO。**C**：メーカーのバージョン誤記や別のV2ローダーが存在する可能性。**U**：実モデル先頭バイト、本人認証、全trained要素、実機RAM未測定。合成`u_c`・包含係数`k`は不定。

**ERROR CHECK**：v30の7件を一意に記録。既存178件／有効131件、20モデル総数未確認、150B超例外2、EXCLUDED6とapproved queue0を変更しない。実重みDL・コード実行・Python CIテストは未実施。機械学習系譜、音声工学、組込みABI、法務/アーカイブの4分野に転用可能。

## 5.〈次に考える問い〉

同じモデル系列でも**学習済み状態が違う**ことと、**今の実装で再現できる**ことは別である。この2条件を満たすまで選定昇格を止めるべきではないか。
