> **履歴資料（R162／v68当時の調査結果）**。当時未完了だった全非重量ファイルのGit OID・Publisher SHA確認は**R163で完了**し、Aurum2BとQJev1.5Bは[正式v71のCONDITIONAL選定](../../catalog/revisions/v71-2026-11-25.json)に昇格しました。取得実行は引き続き未承認。現在の正本は[CURRENT](../../catalog/CURRENT.json) **260登録／210有効**です。原本SHAと取得権限を混同しないこと。[R163詳細](163-v71-aurum-qjev-complete-source-and-uncensored-originals.md)。以下の数値・『未完了』記述は当時の履歴を示します。

---

# R162／v68（2026-11-25）— 無検閲2B視覚・1.5B意思決定原本の優先研究選定と空LoRAの排除

## 1.〈本論〉正本、目的、今回の結論

唯一の正式正本は [`catalog/CURRENT.json`](../../catalog/CURRENT.json) **v68-20261125：252登録、203有効（SELECT56、CONDITIONAL147）**。過去の取得台帳[`2026-11-19-acquisition-ledger.json`](../../catalog/execution/2026-11-19-acquisition-ledger.json)は、**116モデル／1,758ファイル／2,021,784,002,725byte VERIFED**と報告。これらは所有者Windows Dの**本回独立SHA・ライセンス上の利用権・完全オフライン復元の証明ではない**。

今回の目的は、(1) 既取得116・正式252からの学習済み重量の重複除去、(2)「無検閲」という自己申告と独立した重み状態・用途の分離、(3) 使用者の権利・実装・復元可能性を伴う保存準備、(4) 将来の供給途絶を**未検証のストレスシナリオ**として扱うことである。

**研究判断**：新たに [2Beyes/Aurum-2B-Uncensored](https://huggingface.co/2Beyes/Aurum-2B-Uncensored)をP0、[AnkitNayak-dev/QJev-1.5B-Abliterated](https://huggingface.co/AnkitNayak-dev/QJev-1.5B-Abliterated)をP1として**次の保存候補の研究順に確定**。条件付き正式v69への昇格・重量の取得は未承認。原因はPublisherの**全非重量ファイル別サイズ・Git OID/LFS SHA固定が未完了**、Owner個別行為権・HDD・offline runtime未確認だからである。

証拠：
- [R162 Publisher固定revision・学習済み重量SHA・全ファイル名・未完了ゲートを記載](../../manifests/drafts/r162-2026-11-25-new-uncensored-and-decision-partial-publisher-sha-RESEARCH.candidate.json)
- [新2件優先・2件HOLD・空LoRA除外の未承認研究キュー](../../queues/proposed-v68-r162-post116-uncensored-specialists-UNAPPROVED.json)
- [決定と拒否・品質悪化の反証可能仮説](../../catalog/decisions/2026-11-25-r162-small-uncensored-decision-model-selection.json)
- [R162回帰試験（ソース追加・実行未実施）](../../tests/test_r162_v68_uncensored_and_decision_source_gates.py)

## 2. P0/P1の独立学習成果と負の証拠

| 資産／固定40文字Publisher revision | 公開元全repo総サイズ | 静的証拠と採否 |
|---|---:|---|
| **P0 [2Beyes/Aurum-2B-Uncensored](https://huggingface.co/2Beyes/Aurum-2B-Uncensored/tree/56c735e8dc8efb82d81ad8db95e9eefb2ae7129d)** `56c735e8dc8efb82d81ad8db95e9eefb2ae7129d` | **23 files／4,572,557,909byte** | Qwen3.5-2Bを41テンソルで拒否方向編集した**独立BF16視覚言語原本**、Apache-2.0タグ＋LICENSE。重量`model.safetensors-00001-of-00001.safetensors` **4,548,221,520byte**、LFS SHA256 `54b60b4e66348f40d9672dbd245407d85a19189e586aab5b06cb635304371c1c`。同じ学習済み結果のGGUF別repoは二重登録しない。 |
| **P1 [AnkitNayak-dev/QJev-1.5B-Abliterated](https://huggingface.co/AnkitNayak-dev/QJev-1.5B-Abliterated/tree/1df03fe639898580f53a984355b7cbf3cca24bf4)** `1df03fe639898580f53a984355b7cbf3cca24bf4` | **15 files／3,102,137,211byte** | Qwen2.5-1.5Bを使った選択肢確率判定器QJevの**拒否方向編集済み独立原本**。重み`model.safetensors` **3,087,467,144byte**、SHA `5272c8590c74528d5f8604a6a058ddc6a8908089bfb92c010fd73fabd36c796e`。学習済み`decision_head.safetensors` **3,183,276byte**、SHA `ec01a57a7e61c3ee052a5b7ea939cb4e5ae2cfacf2fe84f5e1d67d962805bebe`を同梱。判定用`qjev.py`／`handler.py`／`serve.py`も別途静的レビュー対象。 |

**Aurumの著者の結果の扱い**：危険・非危険合計1,113プロンプトの「拒否0」は著者がモデル側を**手動レビュー**し、元Qwen側は**自動ヒューリスティック**で判定した結果が混在する。拒否率の単純な厳密因果比較にはならない。さらに適切なツールがない場合のBFCL irrelevanceは**元87.9→Aurum62.5**と大幅に低下。GPQAの長い推論でも予算切れが増え、画像内計算にも悪化例。出版社の111token/sは**AMD RX 6600 8GB、Vulkan、llama.cpp build12289、Q4_K_M**という著者環境のもので、GPUクロック・バッチ・nとOwner HWは一致未検証。**高性能・完全無検閲・安全なagentを保証しない**。

**QJevの校正リスク**：[通常版](https://huggingface.co/AnkitNayak-dev/QJev-1.5B)モデル重量SHA `48fea648140195c0b5f38a9dc79c48ab63556f221166cc69edb5d15746a6fea7` に対しAbliteratedは `5272c...`、一方**決定ヘッドのSHA `ec01a...`は通常版と同一**。したがって「安全拒否だけが消え、校正精度は不変」とは論理的にいえない。ヘッドの入力となる隠れ表現が重み編集で変化するからだ。作者はJevBench 240例／1468試行・strict tolerance0.05で62.53%、平均推論約31ms等を報告するが**Owner実機や第三者追試はない**。ソフトに組み込まれた緊急制御/サイバー対処をAIに単独で行わせる判断は本採用の意図に含まない。研究保存と高リスク自律行為は明確に分離する。

## 3. P2 HOLD・却下と既存原本の交換禁止

| 公開元固定revision | 全ソース量 | 判断 |
|---|---:|---|
| [OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated](https://huggingface.co/OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated/tree/266067bc254dbf72d76154016023d1687cc0e3d5) | 11 files／**4,593,269,888byte** | **HOLD**。取得報告済み親[`microsoft/Aion-1.0-Instruct-2.3B`](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B)の重量SHA `6c779881...` と編集版 `5e3cd31b...` は別。MITだが、拒否5/100・KL「very low」は数値・テスト手順不足。新たな4.593GBに見合う独立性能の証拠を待つ。既存親は削除しない。 |
| [MC7ever/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16-heretic](https://huggingface.co/MC7ever/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16-heretic/tree/9a9220a20924249e07d782fc0cd912345858728e) | 16 files／**7,968,035,453byte** | **HOLD**。Doryのrecurrent loop/MTP的演算と拒否方向編集は別状態。OpenMDW v1.1利用条件、vLLM PR 60149／llama.cpp Dory専用commit、1〜4ループ別KV-cache、学習元親がOwnerに未保存である点を審査。通常モデルのコード互換と同一視しない。 |
| [electroglyph/Spark-X2.6-4B-uncensored-experimental-LoRA](https://huggingface.co/electroglyph/Spark-X2.6-4B-uncensored-experimental-LoRA/tree/82fd1a8d83837c35164c958404dce198bf43fe94) | **1file／1,519byte** | **REJECT**。公開されているのは`.gitattributes`のみ。LoRA weightもモデルカードも無い。名前に「uncensored/LoRA」があっても重みの学習結果は存在しない。 |

既存ポートフォリオの無検閲原本や、先行v68のMiniCPM5／Ivonnet／IVE／WeMM Ecom、台帳116件は今回の判断で置換しない。低拒否率が別学習成果であることは、同じモデルの各量子化を多数の資産IDとして保存することを意味しない。

## 4. 欠けている原本・権利・実行閉包

この調査で確認した公開元metadataは**40桁commit、全ファイル名、repo整数総バイト、学習済み重量6個のLFS SHA256（2候補に3個）**である。**非重量ファイルすべての個別`size`・Git blob OID／LFS SHA256を完全照合する前に正式v69へ昇格してはならない**。公式Hub APIの後続照合が利用枠に達したため、その部分を未検証のままにしている。この欠落を勝手に`verified=true`にしない。

実行には、本人の用途別LICENSE/NOTICE確認、研究用モデルの精密なパス・SHAの凍結、現HDD空き200GB安全床＋cache/staging、親・tokenizer／vision／decision headの依存閉包、実機Python/torch/CUDA/ROCm/Transformersと全customコード静的レビュー、**ネットワークなしの完全復元テスト**、本人の**個別ファイル範囲への明示承認**が必要。AurumのpublisherライセンスはApache2、QJevもApache2表示、モデルとデータ・関連サーバコードのすべての権利が自動的に確認されたわけではない。

米BISの[2026-11-19 Federal Register 91 FR 74970 §IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion Ruleのモデル重量ECCN4E091を撤回。**近い将来に全オープンウェイト所持が一律違法化されるという事実は確認されない**。別の輸出先・用途・チップ/リモート計算制限、出版社独自のライセンス、配布停止は別問題である。

## 5. 変数表・次元チェック

| 記号 | 意味（日本語） | SI/情報単位 | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `B_A` | Aurum原本全repo参照バイト | byte（B） | 4,572,557,909 | 公開元23file総量／owner取得量ではない | 非負整数スカラー |
| `B_Q` | QJev無検閲原本全repo参照バイト | byte（B） | 3,102,137,211 | 公開元15file総量／owner取得量ではない | 非負整数スカラー |
| `B_P` | P0+P1出版社参照バイト合計 | byte（B） | `B_A+B_Q` | 別repo同一物理SHA重複は未検証 | 非負整数スカラー |
| `B_W` | P0/P1の既知学習済み重量3個総バイト | byte（B） | 7,638,871,940 | 3 LFS参照、実際の転送量ではない | 非負整数スカラー |
| `B_aux` | P0/P1の非重み残容量 | byte（B） | `B_P-B_W` | 元ファイル別git OID未揃い | 非負整数スカラー |
| `D_free` | 所有者保存媒体の現在空き | byte（B） | null（未測定） | 取得時点の実媒体。過去台帳の最少空きではない | 非負整数又はnull |
| `D_floor` | 取得処理中の最低空き安全床 | byte（B） | 200,000,000,000 | cache/staging等も含む実媒体監視 | 非負整数スカラー |
| `n` | 独立性能計測回数 | 1（無次元） | 同一条件の反復 | 予定`n≥30`、現在0 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 測定量と同単位 | 測定誤差分散の合成 | 系列未観測、数値未算定 | 非負実数またはnull |
| `k` | 包含係数 | 1（無次元） | CI／不確かさの拡大倍率 | 覆域/分布未設定 | 正実数またはnull |

計算を省略せず記録：`B_P=4,572,557,909+3,102,137,211=7,674,695,120byte`、`B_aux=7,674,695,120-7,638,871,940=35,823,180byte`。**単位チェック**：byte＋byte＝byte、byte−byte＝byte。パラメータ要素数と実際のGPUピークRAM、出版社ファイルバイトを混同しない。

## 6. H／T／D／C／UとERROR CHECK

- **H（反証可能）**：2B視覚言語無検閲編集と1.5B非生成意思決定編集は、既存のQwen編集LoRAや文書判定器とは異なるtrained statesを追加できる。しかし両者の機能・品質が既存選定より上回るとは仮定しない。
- **T（最小検証）**：原本5 repoのID・commit・サイズ・weight SHA、正式252/203と取得116のID非重複、空LoRA学習済み0、取得承認queue0を全照合。P0/P1の全38原本ファイルに個別OID/sizeを追加照合する。実機では100以上の合意済み合法な画像/OCR・文書分類・option-calibration課題を準備し、各モデルについて同一CPU/GPU、clock、driver、backend、dtype、入力、context、batch、量子化scale/zero-point条件の反復`n≥30`を実施。作者の「危険な指示に答えた割合」は一般品質保証として使わない。
- **D（判定）**：現在はモデルのSHAとrepo属性のみ`SOURCE_WEIGHT_REFERENCE_PASS`。全ファイルSHA・Owner権利・HDD・完全offline復元・品質は`UNCERTAIN→DOWNLOAD STOP`。空LoRAを取得候補に追加、ヘッド不変を確率校正不変と断定、自動LICENSE承認または無監査任意コード実行が起きたら`FAIL`。
- **C（対立仮説）**：Aurumは拒否低下の代償として不適切なtool call、GPQAや画像数学の失敗が増加。QJevはreadout同一でも入力特徴の編集によって校正が破れる。Aionは他の軽量無検閲と重複。Doryはcustom looping推論器非互換で再生できない。
- **U（主要不確かさ）**：Publisher自身の評価と測定条件欠落、非重量ファイルOIDの未完成、個人の行為別権利、実際のGPU/HDD・コード危険性、学習データ評価重複。実機反復0のため`u_c`・`k`は算出しない。

**ERROR CHECK（静的）**：最優先2 repo／38 Publisher file名／7,674,695,120byte、3 LFS重量SHA。P2研究HOLD2repo、重み0のSpark LoRA除外。正本v68を変更せず252登録／203有効、取得報告116の新転送なし、承認queue0、実ファイル削除0、Gated回避0、未審査コード実行0。

学際性：**暗号学的ソース保全、視覚言語モデル編集/安全評価、確率校正と分類、GPU推論ABI、サイバー・産業制御の人間監督、モデル・学習データの著作権と輸出管理**。

## 7.〈次に考える問い〉

**Aurum2Bが既存の無検閲小型モデルよりも「適切な道具使用率」を下げずに、同条件の拒否低下を再現できるか。再現不能なら、2Bクラスの無検閲編集原本を保存優先順位P0に据える根拠は残るか。**
