# R111｜v47保存原本の優先再確定・極小TTS追加監査（2026-11-18）

## 1.〈本論〉現行v47に対する判断

対象GitHubは Unjuno/local-model-portfolio、現在のmain正本はv47（登録200件・有効153件、SELECT53/CONDITIONAL100）。既存の取得候補14モデルについて、出版社の固定source、選択ファイルの容量とSHAメタデータを再照合し、**保存の調査順番**を決めた。これは正式なダウンロード承認ではない。全件で本人の利用権・完全な依存・実際の4TB HDD・ローカル検証を満たしていないため、重み取得0・実行0を維持する。

### 既存14モデルの決定

| 区分 | 件数 | 選択済み出版社source bytes | 作業決定 |
|---|---:|---:|---|
| A | 10 | 47,030,749,353 | 異なる学習成果の保存原本としてファイル固定を維持し、契約・依存・HDDの取得前監査を先行 |
| B | 1 | 671,173,375 | 非商用の画像LoRA。親Qwen Image2.1およびencoder/VAEを固定するまで完全bundle不可 |
| C | 2 | 108,711,479,306 | PantheonとDavidAU。大型容量に見合う独立性能・既存候補との差が実測できるまで新規取得優先から保留 |
| D | 1 | 55,586,066,230 | OrcaRouter 27B。現在Gatedで、本人アクセス許諾を最初に審査 |
| 合計 | 14 | 211,999,468,264 | すべて非実行・未承認 |

14件すべての採否は引き続きv47に属する。CもDも重みを削除しない。Aの中には無検閲版Interpreticと0bserverx RVN、時系列TTM、Galvanize防御モデル、BotPsy、小型音声話者分離、触覚encoder、DSpine draft、ARLoop、Kittenが含まれる。Qwen3.8という親系列が共通でも、独立した微調整・編集成果なら差分がある。他方で、同じ学習済み原本の多数の量子化形式は重複して保存しない。

### 14件のpublisher fileスコープ

| 区分 | repo ID | 固定source bytes | 出版社40桁revision | publisher SHA256件数/選択ファイル件数 |
|---|---|---:|---|---:|
| A | [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | 17,738,327,225 | e6924b3a08765341e01546308ccf2683d43e880b | 2/5 |
| A | [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 17,176,692,278 | ab8d7bd81d03117501e4da60cccdff4c80f0eea0 | 2/4 |
| A | [ibm-granite/granite-timeseries-ttm-r3](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | 5,748,963 | ea17cfd2e3edcaea21eb8dcecd18bf88971482fa | 1/5 |
| A | [usezn/Galvanize-3](https://huggingface.co/usezn/Galvanize-3) | 597,001,839 | 597237be3b0fabbf5d70ff16ce95fad14a591f20 | 2/9 |
| A | [qvac/BotPsy-0.8B](https://huggingface.co/qvac/BotPsy-0.8B) | 1,726,201,481 | 24561e9681643eaf807fc28b0875210cb17f89c1 | 2/11 |
| A | [nvidia/Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization) | 397,030,277 | 52a432672732425e4c19765b9fec9b5810e6f4ba | 1/11 |
| A | [robbyant/lingbot-touch-tiny](https://huggingface.co/robbyant/lingbot-touch-tiny) | 21,873,479 | f23969ccd4b6bba2163e69cc05a577455a075fe9 | 1/5 |
| A | [tencent/Qwen3.8-27B-DSpine-b16](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | 4,051,857,976 | 260a6c23070ca873ff1a5f33b7119ac3f6a245ee | 1/5 |
| A | [osunlp/ARLoop-1.2B](https://huggingface.co/osunlp/ARLoop-1.2B) | 4,838,079,760 | a29f310ac46646edf5c462425dc546b2ce7ea985 | 3/15 |
| A | [KittenML/kitten-tts-2-mini](https://huggingface.co/KittenML/kitten-tts-2-mini) | 477,936,075 | c01797caec3967b400da457656e011eb81f530a4 | 19/27 |
| B | [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | 671,173,375 | aa213272180d6ad0d03f5fb3d597f0f0322647c5 | 1/8 |
| C | [Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2) | 53,121,584,389 | 6af1278a92223c717ccea671e4571a5cc135f5d8 | 4/12 |
| C | [DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | 55,589,894,917 | 079b2b268c637b77f2fb4ab6a5ca1edc47d462a5 | 14/25 |
| D | [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | 55,586,066,230 | 0f639a9bde23fe229a7b064b40a5153c5bec0b48 | 19/31 |

基礎台帳：[source固定14モデル・173ファイル](../../queues/proposed-v47-r110-source-pinned-14.json)。今回の機械可読全件台帳：[R111監査JSON](../../catalog/decisions/2026-11-18-r111-preservation-tranche-and-swap-audit.json)。sourceの論理容量211,999,468,264byteはユーザーHDDに新たに必要な純増量ではなく、他の現行選定の予算に追加して二重計上してはいけない。全offline依存bundle容量も未確定。

## 2. 新規モデルの採否：n4ze3m/tiny-voca

[作者の一次モデルカード](https://huggingface.co/n4ze3m/tiny-voca)で2026-11-18に確認。ゼロから訓練されたモデルは英語2固定声の24kHz TTSで、source-filter波形生成まで含む4,537,291学習パラメータ。公開表示はApache-2.0。原本PyTorch重み約18.2MB・ONNX約21.4MB・phonemizer約5.4MBがあるが、整数byteと固定40文字revisionの確定はできていない。

公開者のtiny-voca.ptファイルSHA-256：ebb22871524c5732520fb1652e6aefcec708a7452e83bdd00adcf6181db5ef70。ONNX model.onnx SHA-256：fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46。作者ソース：[GitHub](https://github.com/n4ze3m/tiny-voca)。音素辞書・語形データには別のLICENSE.cmudict / LICENSE.homograph-data、[教師合成音声dataset](https://huggingface.co/datasets/n4ze3m/tiny-voca)にはCC BY4.0がある。

**結論：研究用CONDITIONAL追加提案とし、正式登録は現時点で保留**。現行のPhonon 31M英語、Phonon 40M多言語、Kitten 82Mを入れ替えない。tiny-vocaは独立構造で極小だが、英語専用・声2種類・声の複製不可・ストリーミング不可・決定論的な韻律という制約がある。モデル作者のCPU約70倍実時間と公開leaderboardの品質数値は、CPU型番/クロック・batch・評価セットの独立再現ではない。小さい訓練集合から比較的安く再作成できる可能性も高く、他の希少な後学習済み原本を押しのける証拠はない。

パラメータ成分の出版者値は16,704＋1,588,864＋123,906＋795,971＋1,985,984＋25,862＝4,537,291（個数、SI無次元）。いずれも重複しない成分として報告されている。正式採用・取得の前に固定revision、全正確bytes/Hash、phonemizer・teacherデータの権利、未審査pickleとONNX実装・ABI、既存TTSとの同条件比較を確認する。モデル・データの取得は行わない。

## 3. 事実と規制シナリオの分離

2026-11-15 [米国BIS公式リリース](https://media.bis.gov/sites/default/files/documents/BIS%20Issues%20Rule%20Addressing%20Remote%20Access%20to%20American%20Super%20Intelligence%20Technology.pdf)は第三国データセンターを介した先端チップ/サーバーの遠隔利用制御を説明し、ローカル公開モデル重み一般のダウンロード禁止を宣言するものではない。正しい適用は原規則全文・施行日を個別照合する。[Hugging Face Gated公式説明](https://huggingface.co/docs/hub/models-gated)の通り、個々のモデルの許諾とGated状態の変化は独立した証拠であり、将来の禁止確率は捏造しない。

今回Exa検索は402のクレジット上限に達し、新しいExa結果は取得できなかった。新候補の根拠はHugging Face公式カードと現行GitHubのpublisher固定sourceに限定する。今のv47で有効モデル総数未確認9件・Gated条件付き20件・超150B量子化例外審査2件は引き続き取得不可。過去のポリシーとの相違は勝手に変更せず、現在のpolicies/limits.jsonに従う。

## 4.〈応用・転用例〉H/T/D/C/Uと実行準備

**保存科学**：重みSHAとencoder、tokenizer、音声codec、OS/runtimeの依存を単一固定bundleに対応させる。**AI評価**：Cの約108.71GB追加価値を既存の27B系列と同一prompt・seed・context・batchで比較する。**情報法**：モデル本体、親、合成学習データ、声の同意を別々に審査する。**計算機工学**：実ユーザーHDDの容量・空き200GB・stageを現物測定し、GPU/CPU、量子化zero-point、backend ABIを固定してから動作を主張する。

**H**：先行10原本に独立な保存価値があり、Cの大型2件には追加比較が必要。**T**：全14件について同じ項目で権利/依存/版を監査（n_min＝14）、Cは最低30対の同一条件評価を事前登録。**D**：PASSは固有学習済みの証拠と権利/依存/固定sourceが充足、FAILは単純コピー・利用規約衝突が確認された場合、現時点UNCERTAIN。**C**：大型後学習の増分が著しい、または小型原本の依存負荷が予想より大きい場合には判断を逆転。**U**：ライセンスの解釈、公開元カードの測定バイアス、バイト列未照合、物理HDD未計測。合成標準不確かさu_cおよび包含係数kの統計値は未推定。

### ERROR CHECK

固定14モデルをA10+B1+C2+D1に排他的に分割した。173選択ファイルのうちpublisher SHA-256は72件（従来のsha256 50件とARLoop/Kittenのpublisher_lfs_sha256 22件）である。source総量47,030,749,353＋671,173,375＋108,711,479,306＋55,586,066,230＝211,999,468,264byte。現在の200登録/153有効は不変更。承認0・取得0・モデル実行0。提案ファイル以外の選定ポリシーとqueues/approved.jsonは変更しない。

## 5.〈次に考える問い〉

最初の合法的なHDD取得試験には5.7MBの時系列TTMを使ってハッシュ・復元を実証するべきか、17GB超の無検閲独立原本から優先するべきか。現状は取得許可・実HDD不足のため後者以前に実環境の確認が必要。
