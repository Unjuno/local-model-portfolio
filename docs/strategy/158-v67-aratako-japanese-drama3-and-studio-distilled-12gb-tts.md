# R158 / v67 — 日本語Drama 3独立学習原本と小型KL蒸留モデルを別資産化（2026-11-24）

## 1. 結論（訓練系譜の誤分類を訂正）

発信者が`studio_yebisu`と呼ばれているGGUF配布元は、Hugging Faceでは[StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf](https://huggingface.co/StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf)という正式ID。

**現行v67：248登録・199有効（SELECT56・CONDITIONAL143・HOLD30）。今回追加する独立学習済み資産は2つ**であり、単にフルQ4とフルQ5を1件ずつ保存するのではない。

| 独立学習状態 | Publisher frozen SHA | 非重複の必要ファイル範囲 | v67 |
|---|---|---:|---|
| [Aratako/Drama-3-Japanese](https://huggingface.co/Aratako/Drama-3-Japanese/tree/e3762febfc794eaa1d08ee9931215365f92968a8) | `e3762febfc794eaa1d08ee9931215365f92968a8` | **20 files・41,502,599,201 byte**、8 model shards, codec.pth, tokenizer、設定・LICENSE・タグ等 | **CONDITIONAL** 日本語FT原本 |
| [StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf](https://huggingface.co/StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf/tree/cca4c0d8cfab67a2bccbb634d52e544199ac5108) | `cca4c0d8cfab67a2bccbb634d52e544199ac5108` | **12 files・9,762,550,467 byte**、small IQ3_XXS GGUF、対応sidecar、fast／minimum patch、checksums、LICENSE、NOTICE等 | **CONDITIONAL** 小型専門蒸留原本 |

**計32 file／51,265,149,668byte、11 Publisher LFS SHA256参照**。全選択ファイルのPublisher Git blob SHA1もマニフェストに保存した。[不変Publisher実体の完全Source Freeze](../../manifests/drafts/r158-2026-11-24-aratako-trained-and-studio-distilled-publisher-originals.candidate.json)を参照。*Publisherの参照容量であって、owner Dの現在の空きや物理取得量ではない*。

元の[Fish Audio Drama3](https://huggingface.co/fishaudio/drama-3)は既存v66でCONDITIONAL、[s2-pro](https://huggingface.co/fishaudio/s2-pro)はHOLD。Aratakoのモデルカードは**直接の学習元は`fishaudio/drama-3`**と明記し、Studioの短い紹介である「s2-proに基づく」はアーキテクチャ祖先に限定すべき。Aratako`codec.pth`のPublisher LFS SHAはs2-proの`codec.pth`と完全一致（1,871,099,728byte、SHA256 `74fc41c5a7151c6f350af8bd7e5d6e3accfcc7f3dfbfac23afd35af07052bb2f`）だが**owner HDD実際の共有は未検証**。

## 2. なぜ2独立学習成果なのか

[AratakoのREADME](https://huggingface.co/Aratako/Drama-3-Japanese/blob/e3762febfc794eaa1d08ee9931215365f92968a8/README.md)：Fish Audio Drama3を**約70,000時間の日本語音声**でLoRA（rank32 / alpha32）により1 epoch微調整。token embeddingsとaudio decoderも追加学習。元重量は**総35,899,643,008要素（BF16 3,687,388,288＋FP8 32,212,254,720）**で、35B全てBF16と説明するのは誤り。

[StudioYebisuのNOTICE §3](https://huggingface.co/StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf/blob/cca4c0d8cfab67a2bccbb634d52e544199ac5108/NOTICE)：`small-IQ3_XXS`は**単純な量子化コピーではない**。40層のうち4層で256 experts維持、残る36層で100 expertsへ削減し、MoE expert slotsは**10,240→4,624**。その後**JSUT／JVNV／合成日本語音声でKL蒸留**してからIQ3_XXSへ量子化。従ってAratakoとは**別の追加トレーニング済み状態**として1件追加する合理的根拠がある。小型版の最終GGUF全学習済みtensor数は本研究で独立censusしていないため**UNVERIFIED_BLOCK_FINAL_LOCK**（ユーザー承認・実取得STOP）。

一方、同じStudio repoの`Drama-35B-A3B-Japanese-v3-Q4_K.gguf` 22,359,473,504byteと`Q5_K.gguf` 26,386,005,344byteは**フルAratakoを量子化した表現であり、別学習モデルには数えない**。`audio.cpp`レイアウトのsmall-IQ3_XXS 9,962,579,296byteも、`speech.cpp`用smallモデルと同じ小型蒸留結果の別実行形式であり、最小2モデル保存スコープから除外。将来の推論エンジン互換性保険として別途条件付き検討できるが、無条件全量保存はしない。

## 3. 否定的検証：性能値は何を支持するか

[AratakoのPublisherベンチマーク](https://huggingface.co/Aratako/Drama-3-Japanese)（SGLang-Omni Git `b658fa671d6a8a01d9b973754300837dff49d22d`、temperature1.0、top-p0.9、top-k30、最大2048 acoustic frames）：

- JKYB（13,536テキスト×5試行）**漢字読み目標正解率92.021%（Fish base）→93.188%（日本語FT）**。両方が指定長さを満たした66,423／67,680組のみを採用。**作者測定であり無条件の日本語TTS最高精度ではない**。
- JVS（100話者×5文章×5試行）ではCAM++ speaker similarityが1 reference時 **0.7333→0.7280**、3 references時 **0.7769→0.7688** と悪化。話者の再現性が全指標で改善とは言えない。モデルカードは長文の途中終了・無音・タグ不一致も認める。
- 説明文・感情・囁き・息遣い・参照音声は実装可能な公開者機能。ただしStudio GGUFの展示WAVは`--voice none`で、サンプル単独では実話者クローン品質を証明しない。

[Studio Benchmark](https://huggingface.co/StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf/blob/cca4c0d8cfab67a2bccbb634d52e544199ac5108/README.md)はRTX4090、CUDA12.8、`speech.cpp v0.11.2`、`--experts-on-cpu=false`、small GGUFでの**作者側3ケース**。基準実装との総合リアルタイム係数 **1.31 RTFx→3.88 RTFx**、相対パッチ高速化 **2.96倍**、1ケースの最大リアルタイム係数 **4.18 RTFx**。異なるseedで生成時間・音声長さが変化しており**品質同一で4.18倍速**や**パッチで4.18倍**という主張は許されない。TTFA0.28–0.29秒は上記テスト条件のみ。GPUクロック、通常のユーザーWindows GPU運用、並列バッチは未公表。

**VRAMの重要な境界**：small IQ3_XXSの計算・KVを含めた出版社推定の全GPU必要空きは約**11.48GiB**で、16GB/24GBのPCでも余裕と実運用バックエンド次第。フルQ4_Kは**約23.21GiBの空きVRAM**を要求し、24GBカード物理容量22.35GiB相当では**全GPU完結しない**。GPU + CPUオフロード可能でも速度は別条件。フルQ5は約26.96GiBでさらに高い。フルQ4/Q5はCUDA`ggml-cuda`の`block_q8_1.ds` FP16 overflow警告があり、作者はVulkan/CPUを指定。smallではCUDA+Fast Patchが必要。この辺りは元のモデルサイズだけでは判断不可。

## 4. 権利の完全性：Fish、JSUT、JVNV、声の同意

[Fish Audio Community License 1.0](https://huggingface.co/fishaudio/drama-3/blob/main/LICENSE)の主条件：
- 研究・個人利用は条件付き許諾。商用利用も**年間売上USD500,000未満等の限定条件**の下で許諾があり、すべてを「非商用専用」とは言えない。Hosted Serviceなどは別途書面許諾が必要。
- Noticeと**Built with Fish Audio**表記、派生モデルの変更内容、第三者権利などの追加条件あり。
- 小型蒸留の訓練で利用したJSUTは非商用研究・個人利用系、JVNVはCC BY-SA4.0。**Fishが限定商用を許すことだけではJSUT由来の派生成果の商用・再配布権利まで確定しない**。licensor・データ由来の権利審査が必要。
- Patchesは独立MIT・Apacheポーズ制御原コード出所等のNoticeあり。原本`codec.pth`やダウンロード済みコードの無条件Python deserialization禁止。声のクローンは話者の正当な同意・プライバシーを確認する。

## 5. 次の未承認研究優先順位

[次期研究用ソース範囲](../../queues/proposed-v67-r159-japanese-tts-originals-UNAPPROVED.json)では、小型蒸留モデルの**9,762,550,467byte**をP0、Aratako学習原本の**41,502,599,201byte**をP1とする。元のFish Audio公式版が既存カタログにあるからといって日本語FTやsmall蒸留を**重複モデル**と誤分類しない。実所有権利・現物SHA・GPU ABI・100%オフライン復元が成立しなければ、取得許可は発行しない。

## 6. H／T／D／C／U、学際的価値

**H**：Aratako日本語FTとStudio小型MoE蒸留は別の学習成果であり、モデルID2件を条件付き採用しフルQ4/Q5の量子化違いをモデルとして重複計上しないことで、日本語演技音声の利用権変動に備える独立保全価値が増える。

**T**：Publisher全50件の不変revisionツリーを静的取得し、学習原本20件＋小型12件**計32件／51,265,149,668bytes**と各Git OID、LFS11を照合。Studio`SMALL_SHA256SUMS.txt`の6件を一次公開ハッシュと比較、特に小型GGUF 9,762,406,560byte、SHA256`98edad9311a64ea07524f54f24d6d6db77055a3fe7233f24d3bd4351626d9338`に一致。旧246レコードの不変、199 active、143 conditional、owner承認0と旧116モデルVERIFIED報告の不変をテスト。将来ユーザー実機で日本語音読・話者一致・途中停止・音声表現の30件以上の検証を同じprompt、種、HW、クロック、backend、バッチ、品質閾値で実施する。

**D**：メタデータ完全一致・別学習状態2件・全件fail closedなら**静的選定PASS**。2.96倍改善を4.18倍改善と表示、16GB GPUでフルQ4全VRAM搭載可とする、JSUT商用利用権を自動許諾、同じ親のフルQ4/Q5を3番目4番目の独立学習モデルとして数える場合**FAIL**。ownerライセンス・実行環境・音声品質・完全復元はUNCERTAIN。

**C**：日本語FTの声質一致がベースを下回り、distilled smallではMoE縮小で途中停止・発音誤差が増える。演技タグの正確性とローカル最大RTFxが同時に達成できない可能性。

**U**：作者評価の母集団除外によるバイアス、音声毎の確率変動、GPUクロック・バッチ不明、声の権利と70k時間の訓練データ出所、JSUT/JVNV権利、コーデックとspeech.cpp patch ABI、owner HDDの実容量/現物SHA。独立反復測定がないため、合成標準不確かさ`u_c`および係数`k`は未算定。

**関連分野**：日本語音声学・感情韻律、MoE expert pruning／量子化／KL蒸留、CUDA GPU VRAMと推論実装、ソフトウェア再現性・SHA、音声の肖像／著作権・商用許諾。モデル数よりも**再現可能な独立した学習済み成果と合法な動作経路**の保全を優先する。

**今回の実行境界**：重量モデルDL0、現在のuser Windows D実ファイルの操作・削除・再SHA0、許諾確認完了0、新規実行承認0、未審査モデルコード・pickle実行0。
