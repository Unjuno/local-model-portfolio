# R106｜v45の151有効資産：初期10モデルのPublisher SHA・重複・権利停止条件監査（2026-11-18）

**結論**：今回、正式`main`のv45（198登録／151有効）の既存10資産を「**原本source事前照合を優先する第1トランシェ**」として研究上確定した。リポジトリへ新モデルは追加せず、現行`CURRENT.json`の採否を変更しない。10件のHugging Face公開元は2026-11-18時点でprivate:false／gated:falseの**リポジトリ表示**だったが、これは各自の取得・保存・商用利用・派生利用権を保証しない。

[全10資産・107ファイルの固定revision・Publisher LFS SHA256・Git blob ID・byte・除外メディア一覧](../../manifests/drafts/v45-2026-11-18-r106-first10-publisher-source.candidate.json)／[非実行優先調査台帳](../../catalog/research/2026-11-18-r106-small-first10-source-and-dedup-audit.json)。**モデル重みを1byteも取得していない**。ユーザーのHDD SHA・実空き・全依存・復元・法律上の個別合意は未検証。

## 1.〈本論〉— 既存モデルから10件を選ぶ理由

少量モデルを単に性能順に並べたのではない。小さいPublisherファイル構成・多様な学習成果・比較可能な既存ベースライン・権利監査のしやすさを優先した。失われる可能性をモデル別に推測することと、実際に合法的・安全に保全できることは別軸。

| 配布元固定版 | 独自能力 | 候補sourceファイル数 | 候補容量 | 学習済み重みのPublisher SHA256 |
|---|---|---:|---:|---:|
| [`abel-lab/Simons-297M`](https://huggingface.co/abel-lab/Simons-297M/tree/335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a) | PROBABILISTIC_TIME_SERIES | 6 | 1.189 GB | 1 |
| [`KRAFTON/Raon-1-nano`](https://huggingface.co/KRAFTON/Raon-1-nano/tree/39f897a1f835c723ec633c6c905dca7312bd9fd7) | HYBRID_SMALL_LANGUAGE | 17 | 7.182 GB | 4 |
| [`autogluon/chronos-2`](https://huggingface.co/autogluon/chronos-2/tree/60088152a34e242427b44c3100014473a0157d53) | TIME_SERIES_CONTROL_BASELINE | 4 | 0.478 GB | 1 |
| [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/tree/97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3) | RAG_DENSE_EMBEDDING | 12 | 1.207 GB | 1 |
| [`Qwen/Qwen3-Reranker-0.6B`](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B/tree/e61197ed45024b0ed8a2d74b80b4d909f1255473) | RAG_RERANKER | 14 | 1.207 GB | 1 |
| [`google/siglip2-base-patch16-224`](https://huggingface.co/google/siglip2-base-patch16-224/tree/75de2d55ec2d0b4efc50b3e9ad70dba96a7b2fa2) | VISUAL_TEXT_ALIGNMENT | 9 | 1.539 GB | 1 |
| [`ibm-granite/granite-speech-5.0-470m-turboctc`](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc/tree/91dcb0605daf65f88dbb04fef015c423241d941d) | SPEECH_RECOGNITION_STREAMING_CTC | 9 | 0.948 GB | 1 |
| [`lightonai/LightOnOCR-3-0.8B`](https://huggingface.co/lightonai/LightOnOCR-3-0.8B/tree/36d8636925327c671bd8e479c517a004f7566bd9) | DOCUMENT_OCR_LAYOUT | 14 | 1.736 GB | 1 |
| [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base/tree/5e8d12a6e2975b0e5e5fce7c8caf47c371d257b6) | ROBOT_VLA_LOW_MEMORY | 9 | 0.907 GB | 3 |
| [`openai/whisper-large-v3-turbo`](https://huggingface.co/openai/whisper-large-v3-turbo/tree/41f01f3fe87f28c78e2fbf8b568835947dd65ed9) | MULTILINGUAL_ASR_CONTROL | 13 | 1.622 GB | 1 |
| **合計** | **10モデル、すべて既存v45有効選定** | **107参照** | **18.017 GB** | **15件** |

SHA256の重み数は第1トランシェの`model*.safetensors`等の出版社LFSオブジェクト数。**追加の学習済みruntime依存が0という意味ではない**。tokenizer等の小さなGit管理ファイルにはGit blob SHA-1しか公開されていない場合がある。SHA-1とSHA-256を混ぜて同一性判定しない。

### 複数の似た機能をあえて保持する根拠

- **SimonsとChronos-2**：双方は時系列だが、Simonsは32-step patch／変量間attention／9分位点出力とWiSE-FTで訓練した独立原本、Chronosは別の系列予測architecture。復元後のCRPS・MASE比較対象であり**同一学習重みではない**。
- **Qwen3 EmbeddingとQwen3 Reranker**：意味表現の検索段階と候補の再順位付け段階が異なる。重みのLFS SHA256が**異なる**ため片方の重量で代替できない。Git管理の`merges.txt`、`vocab.json`、`tokenizer_config.json`は同一blob IDがあり、**共通トークナイザー素材だけは重複保存を避けられる**。
- **WhisperとGranite TurboCTC**：多言語ASRの比較原本。逐次生成型とCTC／streaming型ではlatency・language-specific CERと実行環境が異なる。メーカー発表の品質だけで片方を捨てず、所有者HW上で比較する。
- **SigLIP2・LightOnOCR・SmolVLA**：画像テキストの類似度、文書レイアウト/OCR、画像＋状態からの行動予測という異なる結果を保全できる。SmolVLAの正規化と逆正規化は**2つの別パス**に同じ640-byte SHA256がある。両方を復元するためパスを省略してはならない。
- **Raon-1 nano**：既存RWKV/LFM/Qwenとの小型モデル構造比較用。main模型3重量ファイルと独立MTP重量ファイルを保存候補に含み、作者README約3.2BとHub main safetensors 3.5299Bの計数不整合を完全に解消するまで、正確な一意学習済み総数を確定したとは言わない。

## 2. 出版社の固定sourceとSHA重複監査

Publisher `/api/models/{repo}/revision/{sha}?blobs=true`相当のメタデータから、合計**107論理ファイル参照、18,016,810,996 byte**を抽出。作者のdemo画像・GIFを候補外にしたが、必要な重み、tokenizer、config、processor、model index、license/NOTICE、SmolVLA postprocessorファイルは選択対象に保持。各repoの**40桁commit、各ファイルbyte、LFS SHA256またはGit blob SHA-1**を台帳へ固定した。

同一publisher内容ハッシュを調べると、6重複グループで内容アドレス方式のファイル保管を仮定した理論的重複削減は **4,463,691 byte**（約4.46MB）。ユニーク内容の論理サイズは **18,012,347,305 byte**。主モデル重みの学習済みSHA一致による冗長モデル削除は発生しなかった。**この約4.46MBは実HDDで確保済みと主張できない**。同一内容の小ファイルを復元時に複数パスへ展開する場合、物理的使用量は戻ることがある。Symlinkを不用意に使わず、復元時にはフルのファイルパスと同一ハッシュを検証する。

参考：[GitHubのLFSとGit objectの区別](https://git-lfs.com/)、[Hugging FaceのGated管理](https://huggingface.co/docs/hub/models-gated)にも注意。管理者の拒否・ライセンス・権限は別のゲート。

## 3. 政策の2026-11-18時点一次根拠と将来仮説

**確認された制度**：[米BISの2026-11-15暫定規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)が対象としたのは第三国のデータセンター等を経た高性能チップ／サーバーへの遠隔アクセス。**既に合法公開された全AI重みを個人が日本で保管することの一般禁止ではない**。[EU公式GPAIオープンソースFAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は条件付きの義務免除を定める一方、著作権ポリシー、学習データ要約、systemic-risk等の義務が残る。[豪ASD/ACSC 2026-11-05公式ガイド](https://www.cyber.gov.au/publication/open-weight-ai-models-opportunities-and-cyber-security-risks)はopen-weightの出自確認・ソフト供給網・運用隔離・監視を勧告するもので、公開重み保有禁止ではない。

**予測・仮説**：標的型アクセス制限→高性能モデル制限→ウェイト配布全般の停止、という3波はストレス仮説。リスクをモデル別消失確率として数値化できる一次ベースレートはない。今回10件は非Gated表示であり**直ちに消えるという予告は確認していない**。一方、既存のGated20件からは、非代替な量子誤り訂正原本 [ColorCode](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast)・[SurfaceCode](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) の2件を**通常手続による本人のアクセス権確認を先に行う研究P0**に置く。Gatedの回避、ミラーを権利なく利用する行為はしない。

## 4. 変数表・容量と次元検査

| 記号 | 意味（日本語） | SI単位 | 定義・定義域／前提条件 | 型 |
|---|---|---|---|---|
| \(N\) | 調査トランシェ内のモデル数 | 1（モデル件数） | 10件のv45有効モデル、非負整数 | 整数スカラー |
| \(F\) | トランシェの論理ファイル参照数 | 1（ファイル件数） | 107、重複ファイルパスを別計数 | 整数スカラー |
| \(B\) | 公開元候補sourceの論理容量 | byte | 18,016,810,996；最終archival byteではない | 非負整数スカラー |
| \(D\) | 完全同一publisher hashに基づく理論的重複 | byte | 4,463,691；物理HDD削減未実証 | 非負整数スカラー |
| \(B_u\) | content-addressed候補ユニーク容量 | byte | \(B-D\)；ファイル構成・全runtimeの増分は未算入 | 非負整数スカラー |
| \(C\) | 保存計画の論理上限 | byte | 4,000,000,000,000、実HDD容量とは別 | 非負整数スカラー |
| \(H\) | 必須物理空き床 | byte | 200,000,000,000、Ownerの実使用・空き未計測 | 非負整数スカラー |

\[
B_u=B-D=18{,}016{,}810{,}996-4{,}463{,}691
=18{,}012{,}347{,}305\ \mathrm{byte}.
\]

**次元検査**：B, D, B_u, C, Hはbyteであり加減算整合。N, Fは件数でありbyteとは加減できない。**今回の10件はすべてv45の151有効資産に含まれ、Raon＋Simonsの8,371,078,617byteも既に前回v45の12GB予約計画に含まれている。** トランシェ容量18.02GBを従来の計画値から**二重に引かない**。4TB／200GB下限後の過去の仮想余白27.41GBは実物の空き領域・完成後の保存容量ではなく、最終適合性はUNCERTAIN。

## 5. 取得前に残る実務ゲート

このトランシェは**順位と配布元source参照を確認した研究用allowlist**であり、`queues/approved.json`に入れない。各モデルで1) fixed original repoと全選択ファイルの発行元LFS SHA、2) LICENSE全文・親学習済みデータや追加利用条件、3) Python／torch／Transformers／LeRobot等の正確なoffline ABI・依存学習済みcodec、4) Owner HDDに実在する容量とcache/staging、5) ユーザー本人の行為別取得承認、6) 取得後のlocal SHAおよびoffline restore成功、が独立PASSになってから別途進める。計算機上でのモデル動作は未検証。

## 6. H / T / D / C / U・ERROR CHECK

**H**：10件の低コスト学習済み原本を同一重み重複なしで正確に指定すれば、無条件に最新モデル名を追加するより多様な将来復元能力を保存準備できる。判定指標は各資産のcomplete rights/runtime/ownerHDDゲート通過数、実復元成功数、同一SHAで重複した取得file bytes。

**T**：v45の151有効repo IDとの集合照合＋Hugging Face connected model summaries 10件＋Publisher固定revisionの10個の全ファイルリスト（n=10モデル、107選択file refs）を照合。全weight-LFS SHA256がなければ先に進めない。実使用時の比較テストはモデルごとに同一タスク30入力以上、batch/context/精度/zero-point/GPU/clock/driver固定で反復と中央値・ばらつきを報告する。今回は重み推論もベンチマークも0回。

**D**：静的合格は10固有ID、107ファイル参照、hash重複6群、LFS checksum列有、18,016,810,996byte、approved0、現行v45正式選定変更0。FAIL条件は重み欠落、前処理パス欠落、LICENSEタグだけで権利PASS、無許可重み／dataset取得、未承認のモデルコード実行。UNCERTAINは権利、全wheelhouse／実機、ピークRAM、off-line復元、各モデル品質。

**C**：候補が既存高品質原本を機能的に代替できない、ライセンスの個別利用に抵触する、元repoのrevisionが削除され再取得不能、同一学習済み重みの実SHAが別の資産と一致する、物理HDD/推論環境に適合しない等で再分類する。

**U**：Publisherメタデータ更新、Git blob SHA1とLFS SHA256の形式差、実HDD容量と同期キャッシュ、ドライバABIとサードパーティコードの安全性、作者の評価条件、個人権利が主な不確かさ。反復校正や統計的誤差分布が無いため`u_c`と包含係数`k`の数値算出は不能。

**ERROR CHECK**：v45=198登録／151有効を保持、10件の公開元source・10固定commit・107 file refs／6重複群／公開元同一性、承認0、重量DL0、所有者の実SHA確認0、全件source比較研究完了。外部公開元のメタデータの整合と本体保存の合格は**区別する**。

学際分野：デジタルアーカイブとコンテンツアドレス保存、AI推論・計算機構造、AI政策・国際契約、統計的モデル評価、ロボティクス／音声処理・時系列予測。

## 7.〈次に考える問い〉

**この10件の最初の1件を安全な完全復元へ進めるため、モデル重みではなく所有者HDDの実空き・LICENSE行為別権利・各runtimeのどのブロッカーを先に実証すべきか？**
