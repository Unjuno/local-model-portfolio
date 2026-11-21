# R149／v63 — 99取得報告を除外した11原本の一次再審査と規制判断（2026-11-22）

## 1. 結論／実際に維持する取得候補

**正本は v63（235登録、188有効＝SELECT55＋CONDITIONAL133）。正式選定追加0・削除0・再取得0。** `queues/proposed-v63-r149-after99-11-research-only.json` の11原本は取得台帳99件とのID非重複として研究候補に維持する。ただし **未取得という断定は99件の履歴台帳ベース**であり所有者Windows D実体を今回再ハッシュしていない。

- **P0**（4配布元、2,234,744,280 byte）：Mirage（237,985,863）、Timestral 28M（111,307,038）、Kitten Pico（285,879,877）、Aurora2 FP32（1,599,571,502）を保存候補として維持。MirageのネイティブCactus 4.1.4 runtime約4,137,947 byte は別参照、現物保存済みか未測定。
- **P1**（4配布元、11,871,408,047 byte）：Intern-Decision、Liquid LFM3-VL親、Heretic別編集重み、FastFrames-S。HereticのBF16＋Q4_K_M＋mmprojは別学習3モデルではなく **同一編集結果の原本＋実行派生表現**。FastFramesにはCausal Forcing++／Wan原本17,567,235,949 byteの追加依存参照があり「本体0.948GBを単体保存で復元可能」としない。
- **P2**（2配布元、54,438,018,606 byte）：MOSS Realtime（22,687,497,344）とNVIDIA Sim-Transfer（31,750,521,262）を保持し、GPU・ABI・依存・法的行為権限を先に審査。
- **P3**（1配布元、129,572,889,973 byte）：Ripple 65Bは追加取得保留。約130GBの大きさだけでは希少性を示さず、能力差・依存・所有者実空きが未知。

P0〜P2のpublisher **参照値**は計68,544,170,933 byte。Apple親依存17,567,235,949 byte・Cactus runtime4,137,947 byteを単純に加算した数も実増分ではない。全件に所有者実容量、staging、ライセンス、モデルコード・ABI・ローカルSHAと明示承認の停止ゲートが残る。

## 2. 新しい一次情報による修正と比較

| 対象 | 一次ソースで確かめた内容 | 選定への影響 |
|---|---|---|
| [Timestral-28M](https://huggingface.co/mistralai/Timestral-28M/blob/main/LICENSE) | Modified MIT LICENSEは**会社／雇用主の前月連結月商が2000万米ドル超**なら本許諾で権利行使不可。Hubタグは `license:other` | 小型だから無条件に使用可能とせず、個別行為と法人条件を先に確認 |
| [Kitten TTS Pico](https://huggingface.co/KittenML/kitten-tts-2-pico) | 8言語、言語ごと7.2M、30声、24kHz、Apache2。F32原本＋INT4 ONNX、既存INT8重複は非選択 | Picoを保持。日本語は対象外で、学習済み総数とG2P/声の復元は未確定 |
| [Kitten TTS Nano](https://huggingface.co/KittenML/kitten-tts-2-nano) | 8言語、言語ごと**17M**、37声。Picoより**大きく**、声の種類のみ7増 | 名前「Nano」だけでPicoと置換しない。追加は**研究HOLD**、同条件の聴感・遅延差が必要 |
| [Mirage](https://huggingface.co/Cactus-Compute/mirage) | 画像理解モデルはApache2だが、公開カードの簡易コードはCactus engineを初回使用時にダウンロードする | モデル5ファイルの保全では完全オフライン復元とは言えない。Cactus engineの固定・検査が先 |
| [Aurora2-400M](https://huggingface.co/AuroraAI-Research/Aurora2-400M-A20M) | 399.6M MoE・独自モデリングコードを伴う | FP32学習済み原本のみ維持、BF16派生の多重選定なし。未審査custom code実行禁止 |
| [Heretic](https://huggingface.co/saidutta69/LFM3-VL-2B-heretic) | 作者の固定100問拒否試験で元98/100→編集版3/100、`lm-eval` 0.4.13のMMLU14,042問では元34.37％／編集版34.44％・標準誤差各0.40pp。作者のRTX PRO 6000 Blackwell 94.97GB／CUDA13.0／driver595.71.05で編集実験、所有者再現ではない | 無検閲の**独立編集学習結果**を保全する理由あり。ただし作者セット限定・視覚品質未検証、一般的無制限性能の証明ではない |
| [Liquid親](https://huggingface.co/LiquidAI/LFM3-VL-2B) | 1.918B BF16、独自コードとLFM Open License v1.0、`transformers>=5.21`案内 | 作者レシピが指定する40桁親revに固定し、Heretic派生と権利・runtimeを別々に評価 |
| [Apple FastFrames-S](https://huggingface.co/apple/FastFrames-S) | Apple AMLR、親Causal Forcing++を凍結利用し周辺部を学習。Linux x86-64/CUDA12.8前提。作者35.4ms/frameはフルKVキャッシュ・GPU条件を要確認 | 親重み＋code license＋runtimeを独立停止。小さい追加checkpointだけでは未復元 |
| [NVIDIA Cosmos3 Sim-Transfer](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Transfer) | Hub表記 `license:other`、15.156B; ライセンス原文と共有VAEのshaが重要 | P2からP0へ昇格しない |
| [US法](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm) | BIS 2026-11-19規則は旧AI Diffusion Ruleのモデル重み規制ECCN4E091を**撤回**。輸出先／用途別の別の制約を消した意味ではない | 「近く全ローカルモデル禁止」という断定は棄却。公開停止・Gated化は将来仮説として扱う |
| [EU AI Act](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source) | GPAIオープンソースの例外は条件付き・一部義務に限定、著作権方針・学習情報概要まで全面免除ではない | open-weights／Apacheタグと配布利用許可の同一視禁止 |

## 3. 先に解決する既存保存物の不整合

[前回99件と9 revisionの監査](../../catalog/research/2026-11-22-r148-ledger99-immutable-revision-drift.json)で、8repoは重みSHA同一・非重み差、**nvidia/RFD4-Proteinaの1repoは重みSHAと原本部品構成自体が異なる**。新規モデルの拡張より、**RFD4の現物版を誤って原本として上書き・重複取得しない**ことを先に確認する。選定済み側は `cf31b93509df5af854c7f6ad704f5c83c77c0698`、取得報告は `5ec66c399bf0b48727ab24e6b298dcf33864fa07`。根拠なく同一trained stateと扱わない。

## 4. H / T / D / C / U

- **H（仮説）**：P0の独立4能力は約2.235GBのpublisher source参照で保存可能であり、巨大モデルや同一学習状態の量子化派生を先行するより、能力の種類と再現可能性の増分が高い。
- **T（最小検証）**：既存11件と99台帳のID重複ゼロ／Publisher40桁rev固定／参照byteの合計とSOURCEの検算。所有者実機ではSHA、当該ライセンス行為別確認、4TB HDDの200GB安全残床、全外部codeとABIを最初に確認して不一致で逐次STOP。Heretic拒否率を比較するなら少なくとも100件の同一問題・同一推論環境を使用。MMLUは出版社の14,042問条件での比較か事前登録した同一subsetを使用。GPU・clock・backend・dtype・quant zero-point・context・batchを記録。
- **D（判定）**：11/11照合と承認ゼロは静的選定PASS。旧重みのSHA混同、未許諾取得、自動承認はFAIL。性能優越・合法な個別取得・完全オフライン復元・現物bytesは**UNCERTAIN**、実転送STOP。
- **C（反証）**：PicoよりNanoの音声品質が実測優秀で容量増を正当化、Mirageが独自runtimeなしで復元可能、Apple親が既存保存物とbit同一、Hereticが第三者評価では性能悪化する等。
- **U（不確かさ）**：所有者D再SHA・所有者権利、staging／GPU・ABI／視覚品質が未測定で合成標準不確かさ `u_c` と包含係数 `k` は算定不能。作者の評価値は条件付き一次主張、規制予測は不確かな仮説。

関連分野：モデルの学習状態／表現、ソフトウェア・サプライチェーン、ローカルHWシステム、安全性評価、法規制・知財。

## 5. 変更境界

[機械可読11件判定](../../catalog/decisions/2026-11-22-r149-v63-next11-source-adjudication.json)を追加したのみ。**v63 235件/188有効・既存候補11件・現行readiness/approvalキューを変更しない。追加重量取得0、所有者D現物変更0、承認0、Gated回避0、未審査コード実行0。** 
