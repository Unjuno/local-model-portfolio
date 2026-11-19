# R121｜v49の実取得報告を踏まえた次期保存原本の確定調査（2026-11-19）


**2026-11-19再照合（重要）**：調査開始時の正本は`main` v49（202登録/155有効）だったが、その後`main`に[v50正式追加の原文](https://github.com/Unjuno/local-model-portfolio/blob/main/docs/strategy/121-v50-rumble-original-selection-and-acquisition-order-2026-11-19.md)が反映され、**203登録/156有効、RumbleはR2/conditionalで正式追加済み**と確認した。本R121の7学習成果は**取得対象sourceの比較**であり、Rumbleを二重登録しない。承認・取得権限は増えていない。元v49に対する比較/差分として以下の表を保持する。

> **書込み先**：`strategy/2026-11-03-01-risk` 限定。調査開始時の比較元は別ブランチ `main` の `catalog/CURRENT.json` → `v49-20261119`。現在はv50正式採用まで追認。この文書はv49の**非破壊的な選定提案**であり、古い当ブランチのv48ポインタを正本として上書きしない。モデル追加・正式ダウンロード承認・新規実取得は0。

## 1.〈本論〉目的／事実／方針を分離

目的は単なる「危険そうなものを急いで確保」ではなく、**正規に再取得可能なうちに、再学習が難しい独立学習成果を少ない重複と容量で保全し、後から実際に復元可能にすること**。パラメータ、精度・量子化、法律・Gated、配布元固定版、実ディスク、依存重みを別ゲートで扱う。

- **2026-11-19調査開始時の事実**：`main` v49は202資産（モデル176・データ26）、有効155件（`select` 53件〔モデル45・データ8〕、`conditional` 102件）。別の`catalog/execution/2026-11-19-acquisition-ledger.json`は53モデル／579ファイル／270,835,576,267 byteが`VERIFIED`と**過去の実行で報告**。今回、所有者Dドライブの再ハッシュも復元テストも実施していない。かつ`queues/approved.json`は空。
- **意思決定**：この台帳の既取得と報告される軽量版・Q4を高精度原本の実取得と混同しない。次の研究選定は下記7学習成果（配布sourceは8件）へ集中。うち**Rumble-2-Flashだけがv49には未登録の独立学習成果**だったが、その後のv50でR2/conditionalとして正式採用されたため本ブランチからは重複追加しない。
- **厳格な150Bルール**：全MoE expertsと学習済み部品を含む総パラメータが150,000,000,000以上なら**量子化しても絶対除外**。v49に残る「量子化なら例外審査」という現行policyは、この専用調査のユーザー制約では無効。 `orcarouter/Qwen3.8-Flash-Next-Uncensored`（180B）と`mistralai/Mistral-Large-4-1T-A52B`（約1.05T）は取得準備禁止。総数不明22モデル（有効9件）は取得準備STOP。
- **規制事実と仮説の分離**：Hugging Faceのgatingは個別repo作者によるアクセス制御（https://huggingface.co/docs/hub/models-gated）。EU GPAIオープンソースFAQは一部義務例外と著作権・訓練データ概要義務を説明するが、全ウェイト一律保管禁止ではない（https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source）。米BISの2026-11-16発表は高度計算資源への遠隔アクセス規制に関するもので、公開weightsの一般的所持禁止の確認ではない（https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology）。「能力制限→広範囲の規制」の連鎖はストレス仮説であって個別モデルの停止確率ではない。

## 2. 次に保全する原本：一意のsourceと交換判断

容量は十進byteで、全ファイルをpublisher sourceに固定した**候補値**。追加の依存・作業領域、実行容量、本人の合法な取得権、本人ローカルハッシュ確認はまだ含まない。

| 順位 | 正規repo ID・確認したsource | 固定revision（先頭12桁） | 提案source byte | 判定と独自性・重複回避 |
| ---: | --- | --- | ---: | --- |
| 1 | [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | `a0c342872291` | 1,385,998,807 | **v50正式条件付き採用を追認**。508.63M主ASR＋別学習CTC head、19ファイル。既存Whisper/Qwen ASRと比べる。 |
| 2 | [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | `2921b8821772` | 15,345,816,226 | **軽量実行版から原本sourceにアップグレード**。台帳の775,728,152Bはcodec等を含む原本一式ではない。 |
| 3 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | `84ab13688128` | 55,586,056,799 | 政治的応答抑制を編集したBF16/MTP完全版。既取得報告のQ4は別表現。出版社の拒否率は独立未評価。 |
| 4 | [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) `RVN-F16.gguf` | `ab8d7bd81d03` | 53,808,326,934 | 別の拒否方向編集済み重み。後発SafetensorsはF16 GGUFから再構成であり追加原本には数えない。vision/MTP不在を明示。 |
| 5 | [sensenova/SenseNova-Loop-9B-GGUF](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF) | `11c121055062` | 19,338,124,279 | **出版社公式のpublic形式**。原本Safetensors [sensenova/SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B) はGated、同一publisherだがMTP/vision全学習部品の完全代替ではない。 |
| 5a | [sensenova/SenseNova-Loop-9B-Preview](https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview) の同一作者code2件 | `89d7970926e2` | 26,724 | 上記モデルのコード依存。**別の学習成果ではない**。Preview重み全体は保存しない。 |
| 6 | [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | `299c8406a6c6` | 54,743,814,229 | ブラウザー操作へ特化した独立後学習成果。Qwen基盤の単純複製でない。実行は隔離・承認型。 |
| 7 | [tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | `64a460a94d54` | 60,142,913,025 | 長期記憶書込み専門MoE。**A3Bは活性値**であり、厳格判定は総30.0647B。 |

**検算**：既存R119のpublisher source7件258,965,078,216 byte＋Rumble1,385,998,807 byte＝**260,351,077,023 byte**（R121の候補上限ソース集合）。これはv49で既に計上された資産の形式差分を含むため、過去の4TB proxy容量へそのまま足すと二重計上する。全資産のfinal選択ファイル、ハッシュ重複、外部学習依存、段階的stagingと200GBのfree floorを合成した確定フィット試算はまだない。

**第一段階の最小集合**：Rumble＋ZONOS3原本＝16,731,815,033 byte（約16.73GB）。小さく独立した結果からsource権利・現物・復元を確かめる。次にInterpretic BF16とRVN-F16を同時に重複判定、最後にFara/Hy-Memoryを特殊能力として評価。順番は法的緊急性の確率ではなく、独立学習成果、部分取得との隔たり、負担の比較。

## 3. 交換・不採用（将来予測に依存しない）

- **KEEP別学習成果**：Interpretic v2と0bserverx RVNは編集目的／音声映像能力範囲が異なる。互いを完全な代替として消去しない。元Qwen baseの重みも比較に役立つが、別の通常量子化を機械的に追加しない。
- **SWAP形式**：Interpreticの既存Q4は実行用のまま保持し、保全原本はBF16/MTPへ。RVNの後発Safetensors再構成ではなく、最も上流と確認できたpublisher F16 GGUFを選ぶ。既得原本の検証前にQ4を削除しない。
- **HOLD**：`harness-hub/Qwen3.8-27B-pi-adapted` はLoRAのbase+adapter固定revision/全学習パラメータが未了。`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`等は全学習部品総数不明。`LiquidAI/LFM3-1.7B`は出版社ライセンスがApacheではなく利用条件付きなので行為別権利確認が先。ミラーや異名コピーが同一SHA・正規権限と確認できない限り取得代替としない。
- **STOP**：150B以上2件は永久にこの方針の保存対象外。総数不明の有効9件はモデル構成／依存の調査のみ許す。高リスク・無検閲・現在Gatedという事実から無許可取得を許容しない。

## 4. 検証プロトコル H/T/D/C/U

**H（反証可能仮説）**：Rumbleは既存のWhisper Turbo／Qwen3-ASRと異なる学習済みCTC headを持ち、小容量で独立した保存価値を増す。別の仮説として、編集済み27BのBF16/F16原本は現在報告済みQ4より将来の変換・再現性の選択肢を増す。

**T（最小検証）**：まず固定revisionのpublisher SHA（LFS SHA-256／通常blob Git SHA-1）を本人D上の全ファイルで比較し、依存の欠落と正規ライセンスを点検。Rumbleの能力は日本語30発話以上（CER）、英語30発話以上（WER）、同一録音・同一HW/クロック/precision/backend/batch=1、同一前処理、固定バージョンでpaired比較。欠損発話またはラベル不備があれば追加収集し、比較可能データ30件に達するまで性能合否は未判定。出版社の高速化7,000 RTFxはH200/vLLMの高バッチ条件であり、手元のbatch1性能ではない。評価実行未着手。

**D（合否）**：source識別＝固定revision・全publisher対象ファイルが列挙された範囲では`PASS_METADATA`。実取得＝本人の同意／license本文／Gated許諾／総数／容量／local SHA／依存が一件でも未確定なら`UNCERTAIN_STOP`、150B以上やアクセス規約違反なら`FAIL_STOP`。今回の新規`approved`は0。

**C（破れ方）**：Rumbleが日本語・ノイズ環境で既存ASRに劣る可能性、作者CTCヘッドが別学習でなく実質変換である可能性。F16の元trained BF16が作者から見つかる可能性。404やGated表示の理由が規制ではなく配布者運用・権利の整理である可能性。

**U（不確かさ）**：ublisherメタデータの変化、学習済み依存、利用目的による契約条項、実D容量、ハード環境・ドライバ・ABI、所蔵台帳53件の独立再現が主要誤差源。測定標本を取得していないので合成標準不確かさ`u_c`と包含係数`k`は未算出（数値推定不可）。規制確率も算定しない。

### 変数表（単位はbyteを明示）

| 記号 | 意味（日本語） | 単位（SI次元・実用単位） | 定義 | 定義域／前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `N_core` | 主ASRモデルの学習済み要素数 | 1（無次元） | 508,631,552 | publisherモデル索引の主重みのみ | 非負整数スカラー |
| `B_ctc` | CTCヘッドのsource容量 | byte（8bitで換算） | 357,476,284 | サブファイル全体、重み・header等を含む | 非負整数スカラー |
| `N_upper` | CTCを1bit/要素以上とした条件付きパラメータ上界 | 1（無次元） | `N_core + 8 B_ctc` | 非圧縮バイナリ、未列挙外部trained weightがない場合 | 非負整数スカラー |
| `N_cap` | 総パラメータ数の絶対除外閾値 | 1（無次元） | 150,000,000,000 | MoE非活性expert等も全数 | 非負整数スカラー |
| `S` | 提案source集合合計 | byte | 260,351,077,023 | R119の7source＋Rumble、依存追加なし | 非負整数スカラー |
| `D_free` | 本人保存先の現在の物理空き | byte | 実機で別途観測 | 今回不明（null） | 未知または非負整数スカラー |
| `F_floor` | 常時保持する空き容量 | byte | 200,000,000,000 | 4TBアーカイブ計画から別途要求 | 非負整数スカラー |
| `T_peak` | ダウンロード時の最大追加一時書込領域 | byte | 並列/キャッシュ挙動の実測 | 今回不明（null） | 未知または非負整数スカラー |

**次元検査**：`N_upper = 508,631,552 + 8 × 357,476,284 = 3,368,441,824 < N_cap`。ここで8はbit/byteを意味し、1bit/要素を除すため結果は無次元。これを正確なCTC tensor数と主張しない。容量条件は `D_free >= F_floor + S + T_peak` で、双方はbyteで次元整合。ただし本当に必要な増分は本人の既存同一SHAファイルを検出してから確定し、式が満たされても4TB総アーカイブ制約と合法性は別に点検する。

## 5. 関連分野と監査

1. **機械学習**：独立学習成果と単なる量子化の違い、LoRA・MoE総数、paired CER/WER検証。
2. **デジタル保存学**：revision・publisher SHA・二重保存対策・将来オフライン復元。
3. **ソフトウェア供給網**：未信頼コード/重みの静的検査、Python/CUDA/ABI、実機隔離と再現性。
4. **情報法**：利用・保管・複製・再配布、gating同意、著作権・本人音声のプライバシー。

**ERROR CHECK**：比較元はv49の202登録/155有効、現行確認はv50の203登録/156有効（Rumbleは追加済み・二重登録なし）、別の実行台帳は53モデル/579ファイル（本回独立SHAなし）。厳格cap除外2件、パラメータ未確定22モデル（うち有効9）、新規正式追加0、main変更0、取得承認0、今回のモデル重量取得0。計画元source金額ではなく **260,351,077,023 byte** のファイル合計。Exaは本日HTTP402で利用できず、Hugging Face公式アプリと配布者一次ページ、公式公共機関資料で代替。実機性能、法的正文の行為別確認、保存先ドライブは未検証。

## 6.〈次に考える問い〉

もし実Dドライブの最新SHA照合でZONOS原本15.346GBが既に完全に存在すると判明した場合、同じ容量でいくつの独立した小型専門モデルを確保できるか。能力多様性と将来復元性のどちらを優先するかを測定データで判断する。
