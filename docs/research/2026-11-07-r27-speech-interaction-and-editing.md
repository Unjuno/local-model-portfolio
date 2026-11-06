# R27｜音声編集・全二重音声モデルの再調査（2026-11-07）

**基準main**：`29529656ac9af944e37c1a803d7271d045860a44`、v19 = 150資産／有効105。Nanbeige/Nanbeige4.3-33Bを保持。これは調査のみ、**SELECT追加0／CONDITIONAL研究5／HOLD研究3、ダウンロード承認0**。対応する[機械可読台帳](../../catalog/research/2026-11-07-r27-speech-interaction-and-editing.json)。

## 1. 調査した2分野

**音声の局所編集**：既存Qwen3-TTS、Audio8、VibeVoiceに足りない「既存録音の指定部分だけを変更し、周囲を保持する能力」を調査。**全二重音声**：音声認識・発話終了判定・音声生成・ツール実行を同一カテゴリーにせず評価した。前回11月4日の9候補の未反映結果をv19基準で再査定し、NVIDIA VoiceChat・Realtime-Venusと最新の作者・外部ベンチ証拠を追加した。

## 2. 全8候補：一次URL／更新日／総パラメータ／サイズ／性能／採否

| 優先 | 配布元（正規repo ID） | 公開・更新日 | 技術方式・主パラメータ | 目安容量（完全な選択容量でない） | 性能証拠と独立検証 | 採用と反対の根拠 | ライセンス | 判断と次の調査 |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [`dots-studio/dots.tts.edit`](https://huggingface.co/dots-studio/dots.tts.edit) | 2026-10 v1.1 | 連続ARと文字範囲を指定する局所音声編集／公開主モデル2.2B、**完全総数不明** | 主重み4.4GB＋vocoder0.724GB＋話者Encoder0.029GB（増分容量不明） | doteBench計2081件：全件one-take全操作成功49.0%、複合編集部分集合37.92%。作者測定。 独立同条件再現は**未実施** | 強い感情の編集成功8.50%。日本語未対応。HF license:otherと開発元Apache-2.0の適用範囲を照合できていない。 | other / 開発元はApache-2.0と明記 | **CONDITIONAL**・MEDIUM_research_only。同一の文章・話者・変更範囲で40例×3seed、局所保持と音質をAuK等と比較し、正確な重みLICENSE/NOTICEを監査。 |
| 2 | [`tencent/AuK-Flash`](https://huggingface.co/tencent/AuK-Flash) | 2026-09-09 | 4-step蒸留、指示ベース音声生成・音声編集・分離／公開主モデル1.5B、**完全総数不明** | 本体6.12GB＋VAE0.637GB、別途Qwen2.5-Omni-3B semantic encoder（増分容量不明） | 作者論文：内部教師32-NFE比4.5倍のwall-clock速度、MMAEの全条件達成率EMR13.85%。 独立同条件再現は**未実施** | EMR13.85%は高くない。外部semantic encoder込みの完全サイズ・総数・実機速度が未確認。局所編集には外部alignerが必要な比較条件あり。 | MIT（作者の重みを明示）、外部encoder別途 | **CONDITIONAL**・MEDIUM_research_only。外部encoder・VAE・全重みの固定rev/sha/許諾確認。既存TTSと局所編集・話者保持・実機速度を測定。 |
| 3 | [`nvidia/NVIDIA-NemotronLabs-VoiceChat-11B`](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-VoiceChat-11B) | 2026-08-03（90日外、独自機構例外） | 双方向音声生成・入力同時処理・独立ツールチャネル／公開主モデル11B、**完全総数不明** | 公式model.safetensors44.4GB＋tokenizer等（増分容量不明） | 作者論文FDB-v3ツール選択F1 82.5%、引数正答42.2%、Pass@1 33%。H100 PCIe80GBで4音声ストリーム、160msチャンクあたりp95推論118ms。 独立同条件再現は**未実施** | 実行完遂33%に止まる。FDBの約448msとチャンクp95は別測定。日本語・量子化・長時間劣化の再現未了。 | OpenMDW-1.1 | **CONDITIONAL**・MEDIUM_research_only。固定rev・原本SHA・OpenMDW全文を確認。20分×10会話の破綻と日本語・正しいツール引数を検証。 |
| 4 | [`adventists-ai/DuplexJev-4B-Para`](https://huggingface.co/adventists-ai/DuplexJev-4B-Para) | 2026-11-04 v1.4 | 音声Encoder→単一トークンのターン・感情・強調判定（音声出力なし）／公開主モデル4.22B、**完全総数不明** | BF16二分割重み約8.43GB、推論想定GPU約10GB（増分容量不明） | 開発者公表：Smart Turn v3.2 n=8749の正解率92.9%、eot-bench英語300ms時の誤打切り21.8%。 独立同条件再現は**未実施** | 真の音声対音声全二重ではない。21.8%は高い誤打切り。v1.4の音声長修正にplugin>=0.4が必須。独立再試験なし。 | CC-BY-NC-4.0 | **CONDITIONAL**・MEDIUM_research_only。同一ハードで軽量Turn detectorと比較。audio_full_lengthとvLLM-plugin版を固定し日本語/雑音/30秒超の精度を測る。 |
| 5 | [`inclusionAI/Realtime-Venus`](https://huggingface.co/inclusionAI/Realtime-Venus) | 2026-09-12論文 | 同一HF repo内Realtime-Venus-Audio（9B）、音声を出しながら入力処理、非同期委任／公開主モデル9B、**完全総数不明** | HF全repo約640GBはAudio専用容量でない。Audio主シャード表示約17.5GB＋Token2wav約1.17GB、固定バイト未照合（増分容量不明） | 作者論文FDBv1.5：割込応答75%、相づち継続97%、他人宛発話88%、背景会話86%。委任経路Audio68.89%。 独立同条件再現は**未実施** | 75%割込応答は完全ではなく、委任経路はタスク完遂率ではない。カスタムTransformersコード・補助重み・個別権利・実機条件が未監査。 | HF Apache-2.0タグ（追加LEGAL未審査） | **CONDITIONAL**・MEDIUM_research_only。Audioフォルダのみの4 shard, token2wav, LICENSE/LEGAL/NOTICEを固定。NVIDIAと長時間・相づち・実用ツール完遂を比較。 |
| 6 | [`penguinfish1688/dialogue-to-duplex`](https://huggingface.co/penguinfish1688/dialogue-to-duplex) | 2026-10-12論文 | Qwen3-Omniを音声Encoder蒸留＋対話SFTで全二重化、qwen-80ms版／公開主モデル総数不明、**完全総数不明** | 作者目安重み約73GB、空き100GB、RTX PRO6000 96GB GPU/96GB RAM推奨（増分容量不明） | 作者論文VoiceBench70.07、FDBターン成功99.2%、割込成功99.5%、一時停止成功21.3%。 独立同条件再現は**未実施** | 521msは計算・ネットワーク除外の音響ギャップ。標準会話文脈約54秒、長時間・RAM要件と総MoEパラメータ再確認が必要。 | 派生/親の正文未確認 | **HOLD**・LOW_to_MEDIUM。qwen-80msと親Qwen3-Omniの完全固定、20分対話と実計算込みの遅延、別モデルとの重複検証。 |
| 7 | [`adventists-ai/DuplexJev-32B-Para`](https://huggingface.co/adventists-ai/DuplexJev-32B-Para) | 2026-11-03 v1.5 | 4Bの大規模版、音声判定・非言語/多言語聴覚／公開主モデル32.96B、**完全総数不明** | BF16約66GB、80GB GPU推奨（増分容量不明） | 作者v1.5 Smart Turn94.4%、英語誤打切り17.7% @300ms。日本語等の高い品質を主張。 独立同条件再現は**未実施** | 4Bとの精度差に対し約8倍の保存量。両版同条件・日本語再試験なし、音声出力なし。 | CC-BY-NC-4.0 | **HOLD**・LOW_to_MEDIUM。4B v1.4との日本語・雑音・強調の対応あり比較、66GBの増分価値を判定。 |
| 8 | [`tencent/AuK`](https://huggingface.co/tencent/AuK) | 2026-09-09 | AuK-Flashの蒸留元32-NFE教師、指示音声編集／公開主モデル1.5B、**完全総数不明** | 本体6.12GB＋VAE0.637GB＋別Qwen2.5-Omni encoder（増分容量不明） | 作者論文のFlash比較対照となる教師重みで、蒸留後に復元しにくい学習成果を持つ。 独立同条件再現は**未実施** | Flashとの重複が大きい。実際の品質上積み、同一VAE・EncoderのSHA重複、容量、実機遅延未検証。 | MIT（外部encoder別途） | **HOLD**・LOW_to_MEDIUM。Flash優先で局所編集・音質を測り、教師の改善が有意な場合のみ保存を再審査。 |

## 3. 比較と反証

- **dots.tts.edit** の2081件全件49.0%と、論文の複合編集集合37.92%は測定母集団が異なる。[doteBench](https://github.com/studio-dots-ai/doteBench)。強感情8.50%は失敗例として保持。
- **NVIDIA VoiceChat** のH100・BF16/FP32、4並列、160msチャンクのp95計算118msは、音声応答の約448msとは異なる。ツール選択82.5%でも完全なPass@1は33%。[一次論文](https://arxiv.org/abs/2609.21967)。
- **D2** の521msは計算・ネットワーク除外の音響間隔。推奨96GB GPU・96GB RAM、会話約54秒、pause21.3%で現時点HOLD。[開発者一次README](https://github.com/penguinfish1688/D2-dialogue-to-duplex)。
- **AuK** はMIT重みと外部Qwen Encoderの権利を分離。Flashの4-stepは蒸留であり量子化ではない。編集EMRは13.85%と絶対値は低い。[一次論文](https://arxiv.org/abs/2609.08936)。
- **Realtime-Venus** は同repo 640GBにOmniとAudioなどを同居。Audioフォルダを別repo IDとして登録しない。検証済みの選択ファイルと依存の正確なバイト数は不明。[一次論文](https://arxiv.org/abs/2609.13814)。
- **長時間評価**：[FD-LHB](https://arxiv.org/abs/2610.32349)は複数全二重モデルの長時間劣化を報告。新候補すべてを直接評価したものではない。[MultiTalkBench](https://huggingface.co/datasets/MultiTalk/MultiTalkBench)は104例56.52時間、モデル本体の正規重みID未確認なので追加しない。

## 4. 検証計画（H／T／D／C／U）と変数表

| 変数 | 意味 | SI単位 | 定義と範囲 | 型 |
| --- | --- | --- | --- | --- |
| N_edit | 編集テスト事例数 | 1 | 40件以上、異なる操作・話者・長さ | 整数スカラー |
| S | 事例ごとの乱数種子数 | 1 | 3以上 | 整数スカラー |
| N_spk | 同意済み話者数 | 1 | 5以上 | 整数スカラー |
| N_conv | 長時間音声対話の試験件数 | 1 | 10以上 | 整数スカラー |
| T_conv | 1対話の長さ | s | 1200秒以上 | 実数スカラー |
| N_runs | ランタイムの反復数 | 1 | 30以上、固定環境 | 整数スカラー |
| B_selected | 依存込み選択バイト数 | B | 0以上、未確定はnull | 非負整数または未知 |
| RAM_peak | 推論時RAMピーク | B | 512,000,000,000未満が必要 | 非負実数または未知 |

**H**：領域固有の性能改善が既存モデルより大きい。**T**：上記の同条件評価、音声編集の指定操作成功率と局所保持・話者類似度を分離し、会話では割込・相づち・20分持続・ツール引数・成功率を測る。CPU/GPU・クロック・VRAM/RAM、backend/ABI/quant/zero-point、context、batch、Codecを固定。**D**：再現可能な有意な固有能力と合法・実行条件が揃えばSELECT審査、低品質や実行不能/重複ならREJECT、欠測はUNCERTAINとしてHOLD/CONDITIONAL。**C**：データ漏洩・同一モデルとの構成差・ベンチ汚染・評価プロトコル相違。**U**：主な不確実性は元repoコミット・正確な容量・独立評価・実機負荷・権利で、合成標準不確かさu_cを数値化できず包含係数kは未適用。

**単位検査**：パラメータ数とケース数は無次元、音声継続時間は秒、容量・RAMはbyte。ソース全repo容量≠実際の増分容量、主モデルの公称総数≠trained dependency全数、分布開始≠取得権限。

## 5. 分野横断の転用とERROR CHECK

音声信号処理（部分変更と非変更部分の保持）、HCI（割込・バックチャネル）、MLシステム（蒸留・GPU制約・コード安全）、デジタル保存・法務（原本・ライセンス・依存・固定SHA）に転用。今回の改訂は調査文書のみで、CURRENT/正式キュー/既存ダウンロード/実データは無変更。全件の総数・選択byte・正式承認は未確認のままです。

## 6. 〈次に考える問い〉

正式SELECTへ昇格させるため、最優先に証明すべき指標は「局所音声編集で元音声を保持できること」か「20分以上の全二重対話で破綻しないこと」か。
