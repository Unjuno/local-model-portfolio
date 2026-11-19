# R110｜v47：ARLoop 1.2B・Kitten TTS 2 Mini原本の研究選定と取得ゲート統合（2026-11-18）

## 1.〈本論〉正式採否の理由

v46の198登録／151有効資産を完全保持し、独立事前学習済み[osunlp/ARLoop-1.2B](https://huggingface.co/osunlp/ARLoop-1.2B)と、日本語音声を含む独立学習済み[KittenML/kitten-tts-2-mini](https://huggingface.co/KittenML/kitten-tts-2-mini)を、**非実行・研究段階CONDITIONALとして2件追加**した。v47は**200登録（174モデル＋26データ）／153有効（SELECT53、CONDITIONAL100）**。既存198の採否を変更・削除しない。新規リポジトリは通常量子化の別名ではなく**別の学習成果**を持つ。現時点で性能の独立非劣性、利用権利、実HDDは未検証のため、**取得承認0・本体ダウンロード0・オフライン復元0**。

[固定publisher source原本42ファイル](../../manifests/drafts/v46-2026-11-18-r110-arloop-kitten-fixed-source.candidate.json)／[Publisher一次調査とRVN訂正](../../catalog/research/2026-11-18-r110-arloop-kitten-rvn-erratum.json)／[正式選定v47差分](../../catalog/revisions/v47-2026-11-18.json)／[200件実効カタログ](../../catalog/effective-portfolio-2026-11-18-v47.json)。

| 独立学習済みモデル | 発行元不変revision | 選択原本ファイル | source byte | Publisher SHA付きファイル |
|---|---|---:|---:|---:|
| [ARLoop-1.2B](https://huggingface.co/osunlp/ARLoop-1.2B/tree/a29f310ac46646edf5c462425dc546b2ce7ea985) | `a29f310ac46646edf5c462425dc546b2ce7ea985` | 15 | 4,838,079,760 | 3 |
| [Kitten TTS 2 Mini](https://huggingface.co/KittenML/kitten-tts-2-mini/tree/c01797caec3967b400da457656e011eb81f530a4) | `c01797caec3967b400da457656e011eb81f530a4` | 27 | 477,936,075 | 19 |
| **合計** | 2 repo | **42** | **5,316,015,835** | **22** |

### ARLoopの独自性と負の側面
[原著arXiv:2611.05234](https://arxiv.org/abs/2611.05234)と[作者モデルカード](https://huggingface.co/osunlp/ARLoop-1.2B)に基づく。重みを共有する24層を3パス反復して72層相当の実効深度を形成し、Attention Residualを採用。約500Bトークンの事前学習済みBase。既存QwenやRaonのDelta Attentionと同一学習結果でなく、同論文ARLoop-0.6B・PreNormLoop-0.6Bは重複した比較用小型対照として今回は**採用しない**。通常のベースモデルであって優れた日本語チャット能力が証明されたわけではない。FP32 3 safetensorsシャードの公開LFS SHAを固定し、モデルコード・tokenizerを保全。作者指示の`transformers==5.12.1`および`trust_remote_code=True`に関連する安全/ABI停止ゲートを設ける。

### Kittenの保全形式の例外
82M規模、16言語・118声・24kHzで、日本語`voices_ja.npz`を含む全16 voice pack、G2P用学習済み`g2p/g2p_bart_en_us/model.safetensors`をpublisher sourceに固定。FP32 `kitten_tts_2_mini.safetensors`を**正式な学習済み原本**、INT8 `kitten_tts_2_mini.onnx`（82,711,386 byte）を**CPU推論がPyTorchなしで可能となる著者公式の運用artifact**として同じモデル資産内に残す。通常量子化の複数形式を別モデルとして増やすものではない。Qwen3-TTS、Gradium Phonon、Maya等と学習済み重みが異なり、専用edge TTSの保全価値がある。日本語phonemization、NumPy voice npzの安全な読み込み（`allow_pickle=False`）、`kittentts`/ONNXRuntimeのABIと実環境音声品質は未検証。作者Model Card/HubにはApache-2.0とあるが固定model repoに独立`LICENSE`ファイルは無く、**契約全文を確認したと誤記しない**。

## 2. RVNモデルのファイル不存在の誤記を訂正

旧[R108原本選定報告](108-v46-original-weights-uncensored-compact-source-finalization.md)には、[0bserverx Heretic RVN](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)の`chat_template.jinja`が「存在しない」と記載されていた。しかし、原本revision `ab8d7bd81d03117501e4da60cccdff4c80f0eea0`の[Publisher API](https://huggingface.co/api/models/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/revision/ab8d7bd81d03117501e4da60cccdff4c80f0eea0?blobs=true)では**8,952byte・Git blob SHA1 `c0c686f9c38d70d179fb7b5f5aa7530bc913dda3`**として実在する。R108旧報告冒頭に正式訂正文を加えた。

**正しい選択判断**：`RVN-Q4_K_M-multilingual.gguf`にtemplateが埋込済みなので、別`chat_template.jinja`は*推論時必須ではない*。推奨GGUF・projectorの固定SHAや保存容量を変える必要はなく、ファイルが存在しないとの事実誤認のみ修正。独立した無検閲学習成果は引き続き別系統として保持し、全repoの量子化形式を重複取得しない。

## 3.〈応用・転用例〉アーカイブ容量・ダウンロード準備

[153件の停止ゲート](../../catalog/readiness/v47-2026-11-18-r110-all153-gates.json)、[条件付き100件公開状態](../../catalog/access/2026-11-18-v47-conditional-hub-gates.json)、[研究候補153件](../../queues/proposed-v47-2026-11-18.json)、[依存準備153件](../../catalog/preparation/2026-11-18-insurance-bundles-v47.json)、[原本publisher source14件](../../queues/proposed-v47-r110-source-pinned-14.json)を整合させた。**12既存+2新規**の原本source構成を固定したが、最終承認には個人の用途別権利・LICENSE正文、repo全必要ファイル、実4TB媒体のフォーマット後空きとcache/staging、Python／torch／CUDA／ONNXRuntime依存、取得後local SHA・完全offline復元が必要。

別作業[R109事前検査](109-v46-twelve-source-download-preflight-tested.md)で確認した接続Linuxの約50.88GB総容量・29.52GB空きは**ユーザーの4TB HDDではない**。この状態でモデル重量を取得するのは200GB最低残床に反する。**owner HDDに合格と判定する証拠は0件**。

| 記号 | 日本語の意味 | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| \(B_A\) | ARLoop保存候補ファイルの出版社byte | byte | 4,838,079,760、未取得 | 非負整数スカラー |
| \(B_K\) | Kitten保存候補ファイルの出版社byte | byte | 477,936,075、未取得 | 非負整数スカラー |
| \(B_T\) | 2候補のpublisher source合計 | byte | \(B_A+B_K\) | 非負整数スカラー |
| \(H_{46}\) | 過去の仮想計画余白 | byte | 27,409,767,827、本人HDDの空き値ではない | 整数スカラー |
| \(R_{47}\) | 新規2件の暫定予約枠 | byte | 7,000,000,000、runtime/転送領域を含む保証ではない | 非負整数スカラー |
| \(H_{47}\) | 更新後の過去資料に基づく仮想余白 | byte | \(H_{46}-R_{47}\) | 整数スカラー |

\[
B_T=4,838,079,760+477,936,075=5,316,015,835\ \mathrm{byte};
\quad H_{47}=27{,}409{,}767{,}827-7{,}000{,}000{,}000=20{,}409{,}767{,}827\ \mathrm{byte}.
\]

**単位検査**：byte＋byte、byte－byteはともにbyte。モデル学習済みパラメータ個数は無次元でありバイト数と混同しない。上記の約20.41GBは古いsource代理と予算予約を混合した歴史的試算で、**実HDD余白でも全153資産のオフライン復元完了後の容量でもない**。

## 4. H / T / D / C / U、ERROR CHECK

**H**：既存v46の198資産を変更せず小さな独立学習原本2件だけ加えると、低容量でアーキテクチャ・音声言語の保全幅が増える。

**T**：Hugging Face出版社API原本2件・42選択source files・公開LFS SHA 22件と旧RVN commitのJinja実在を非実行検査。v47正本・153件ゲート・100件access・153候補/準備を静的ID完全照合。性能テストは同一HW／clock／batch／dtype/zero-point／backendで30試行以上と比較baselineの中央値／ばらつきを要求し、今回は推論テスト0。

**D**：PASS＝原本ソースの不変同定と旧198モデル変更なし、学習済み構造の独立性、source-only採用。FAIL＝無許可Gated回避・重量DL・unsafe custom code実行・実体なしライセンス許可認定。UNCERTAIN＝全本人権利、モデル品質、phys HDD、完全依存、local SHA/restore。

**C**：Kittenの日本語TTSに外部未収録G2P重みが必須で復元不可、ARLoopの反復実装がサポートされなくなりコードは再実装不能、モデルが既存系列と実測で能力重複、権利不適合・現物HDD不足が判明した場合はHOLD再検討。

**U**：Publisher model card/license要約、ソフト/driver ABI、Gated本人許可、容量source代理値、音声品質の不確かさが主。反復試験のデータがないため合成標準不確かさ\(u_c\)・包含係数\(k\)の数値化は不可能。

**ERROR CHECK**：198→200登録、151→153有効、CONDITIONAL98→100、SELECT53不変、旧198件採否不変、Gated20、総数未確認active9、選択file42、Publisher sha 22、重み取得0・取得承認0・実HDD測定0・オフライン復元0、mainのみ。

関連分野：反復Transformerの学習済み計算手法、音声合成・日本語G2P、保存科学／内容ハッシュ、ソフトウェア供給網とABI、AIライセンス／配布政策。

## 5.〈次に考える問い〉

**既存の無検閲27Bや専用専門モデルの取得準備よりも先に、5.316GBのARLoop＋Kittenで「新しい学習済み能力」を保全する価値は、本人の本当の4TB HDD容量と実行再現性を測った後にも成立するか。**
