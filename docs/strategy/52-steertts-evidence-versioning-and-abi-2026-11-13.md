# R52｜SteerTTS NanoのABI検証器とTTSベンチのバージョン混同の訂正

2026-11-13。対象 Unjuno/local-model-portfolio、専用ブランチ strategy/2026-11-03-01-risk、基準commit d2653aaf4bda91be501c117305c3ec727d0a0df9。

**研究・非実行ツールの追加のみ**。正本 v30・178資産・有効131件、総数未確認20件（有効7）、取得承認0を変更しない。モデルの重みやGatedファイルを取得・ロードせず、契約に代理同意しない。

## 1.〈本論〉NanoのSTNB v2と公開v1ローダーが衝突

[SteerTTS Nano原配布元](https://huggingface.co/WhissleAI/steer-tts-nano)は nano.bin を「STNB v2、f0-driven excitation vocoder」と記載する。一方で[固定Cヘッダ](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/esp32/components/steertts_nano/include/nano_bin.h) は NANO_BIN_VERSION=1、[固定Cローダー](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/esp32/components/steertts_nano/src/nano_model.c)は異なる版を拒否する。[固定Python writer](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/esp32/tools/nanobin.py)もversion=1。2026-11-13照合時点でコードのmain HEADは引き続き 5008f8e032f69266c3f37788825cfda3112eab55。

**観測されたのは文書とコードの不一致**であり、公開 nano.bin の実際の先頭8byteを見た証拠ではない。現物v2なら固定v1ローダーとの組合せは不適合、現物v1なら文書側に誤りがある可能性。配布元の修正や対応するv2実装が出るまでNano新規保存選定はHOLD。

この条件を運用可能にするため、[非実行STNB検査](../../scripts/check_stnb_abi.py)と[合成ヘッダ単体テスト](../../tests/test_check_stnb_abi.py)を追加した。既に本人が正規に取得・検査許可を得たローカルファイルがある場合だけ、最初の8byteを読み取り、magic STNBとlittle-endianの32bit版番号を照合する。**PASS_HEADER_VERSION_ONLYはモデル動作・学習成果・権利・完全なハッシュのPASSではない。** インターネット接続や重みの実行はない。

最小実証：合成バイト STNB+v1 はPASS_HEADER_VERSION_ONLY、STNB+v2とv1ローダーはFAIL_VERSION_MISMATCH、欠損/不明形式/不存在は独立判定。実験環境はPython 3.10以降・stdlib、HW/クロック/バッチ非依存。実モデルのビット列は用いず5件のunittestをローカル実行して全件PASS。CI全体や実重み動作試験は未実施。

## 2. 比較ベンチマークの「提出者評価」と「最新版の指定」を分離

[Open TTS Leaderboard PR #39](https://github.com/huggingface/open-tts-leaderboard/pull/39)は2026-11-13照合時点でopen、未マージ。**PR本文にある数値はWhissle開発者が自らローカル評価したもの**で、Hugging Faceが第三者独立測定として確定した正式ランキングではない。

| PR本文で測定した版 | 平均WER | UTMOS | 評価主体 |
| --- | ---: | ---: | --- |
| SteerTTS v1.3.0、flowあり | 0.97% | 4.418 | 提出者のローカル測定 |
| SteerTTS Edge v2.0.0 | 0.92% | 4.322 | 提出者のローカル測定 |

評価対象はEnglishのSeed TTS 1088、CV3 500、MiniMax 100例。同一評価指標上でEdgeのWERがやや良い一方、UTMOSはフルのほうが良い。モデルのサイズはPR記載40.7M対15.5M学習済みパラメータ。音声品質の独立優越を証明しない。

**重要な版のズレ**：PR説明欄はv1.3.0/Edge v2.0.0だが、PRの最新コミット 00298cd0580e18487cead341975e3c536c722d9a は11月3日に評価スクリプトのrevisionを v1.4.0/Edge v2.1.0へ更新。したがって古い本文スコアを新しい固定版の成績として転載しない。HFモデルカードが Edge を quantized とタグ付けしていても、出版社の v2音響訓練版が単なる v1形式変換なのか、異なる追加学習済み成果なのかは版ごとのtensor identityとレシピで判断する。

[Nano発行者モデルカード](https://huggingface.co/WhissleAI/steer-tts-nano)と[現行コードのLICENSE](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/LICENSE)にある非商用利用・本人Gated許諾は独立した取得停止条件である。旧MITの説明は権利正文との矛盾を解決するまでは使用しない。

## 3. Maya2とPruna P-H3の復元ゲートを具体化

**Maya2 Native**は既存の2,502,398,656要素の主重みに加え、公開[原モデルカード](https://huggingface.co/maya-research/maya2-native)が示す2個の独立学習済み外部モデル、Kyutai Mimi（CC BY 4.0）とSpeechBrain ECAPA-TDNN（Apache-2.0）が必要。本体に含まれるQwen学習初期化backboneを第三のランタイムcheckpointとして無条件に再取得しない。音声の12言語、Mimi32コードブック、ECAPA192次元埋込は公式仕様。両外部依存の実行時revision/全ファイルSHA、ECAPAの正確なテンソル数、Python/CUDA/ABIはまだ未確認。Maya2の6,000例・各言語500例・H100 NVL/224接続の開発元評価値は自身の実機の指標に読み替えない。

**Pruna P-H3 Image**では[原カード](https://huggingface.co/PrunaAI/P-H3-Image)と[Diffusers公式説明](https://huggingface.co/docs/diffusers/main/en/api/pipelines/p_h3_image)が、33.1B本体だけでなく4B系のtext encoder、Qwen3.5-9B由来prompt upsampler、text connector、VAEを必要とすることを裏付ける。既存保存予定の15学習済みsafetensorsを量子化重複扱いしてはいけない。prompt upsamplerは明示したプロンプトをそのまま出力する用途では除去可能だが、短い入力の通常workflowを完全に保全するなら必要。8MP、batch1、B200で著者公表約83GB（upsamplerなし）/101GB（upsamplerあり）。HW/clock/ソフト版・オフロード条件を統一せず別モデルと性能比較しない。重みライセンスはMiniMax H3 Community、Qwen部品はApache 2.0であり、地域・用途条件に注意。完全数P_fullは未確定。

## 4. 変数表、再現性、反証

| 記号 | 日本語の意味 | SI単位 | 定義／定義域／型・前提 |
| --- | --- | --- | --- |
| H | ヘッダ先頭magic | 1 | 4byte STNB、文字配列、完全一致が必要 |
| V | 実ファイルのSTNB形式版 | 1 | 8byte目までのlittle-endian unsigned32bit、非負整数スカラー |
| V_loader | ローダーが受理する版 | 1 | 固定Cコードで1、正整数スカラー |
| B_header | 静的に読むファイルの先頭バイト長 | byte | 8byte、固定整数 |
| P_main | 主HFモデルの学習済み総数 | 1 | 表示確定分のみ、非負整数スカラー |
| P_full | 独立する全学習済み必須部品の合計 | 1 | Maya/Prunaはnull、欠測扱い、非負整数またはnull |
| B_disk | ユーザー機器の実空き | byte | null、未測定 |
| u_c / k | 合成標準不確かさ／包含係数 | 対象測度の単位／1 | 実ファイル・モデル実行の誤差分布が無く未推定 |

**次元検査**：形式番号Vは無次元、B_headerはbyte、パラメータ数Pは無次元であり、Pとbyteを加算しない。STNB版一致は容量や音声の正確さを保証しない。

**H（仮説）**：公開Nanoが実際にSTNB v2なら現在の固定v1ローダーは版照合で拒否する。
**T（最小検証）**：合成版1/2各1本を先にテスト（5つの検査PASS）。正規ライセンス許諾済み実ファイルについてはユーザー承認後に最初の8byteだけ読む。n_min=2の版間合成ケース＋欠損・異常系、逐次停止は版が一致しない時点。
**D（判定）**：magicが不一致ならFAIL、8byte未満ならUNCERTAIN、実体のV=V_loaderならPASS_HEADER_VERSION_ONLY、異なればFAIL_VERSION_MISMATCH。動作可否は常に別のUNCERTAIN。
**C（反証）**：カードのv2誤記、別のv2対応コード、あるいは訓練差分が別でない可能性。
**U（不確実性）**：実nano.bin実ヘッダ、本人Gatedアクセス、モデル全パラメータ、OS/runtime検査、実HDD空きは未知。u_cやkを捏造しない。

**ERROR CHECK**：コードと合成5件の単体テストはローカルPythonで実行し全件成功。実モデルの重量ファイル、ユーザーPC、所有者の権利やCI全体は未検査。現行v30=178資産/131有効、20総数未確認・有効7・150B超例外HOLD2、approved queue0を変更しない。

学際転用は音声工学、マイコンのC/ABI、学習済み差分の保全、ライセンス・ソフトウェア供給網、時系列と画像生成の依存グラフ。

###〈次に考える問い〉
機能的には価値があっても、公開バイナリと配布コードの版が一致しないモデルを、「取得済みなら復元できる」と評価する根拠はあるか。
