# R123｜v52の61モデル取得報告を反映した原本保存・追加モデルの選定（2026-11-20）

**書込み先**：`strategy/2026-11-03-01-risk`。現行`main`の正本は2026-11-19の`v52-20261119`（登録205、有効158＝select53／conditional105）。当専用ブランチの古いv48ポインタは**正本に昇格しない**。本文はモデル選定／監査提案であり、新規の実取得・承認・既存ファイル削除・コード実行はゼロ。固定比較元を[機械可読R123判定](../../catalog/decisions/2026-11-20-r123-v52-ledger61-source-delta.json)に記録した。

## 1.〈本論〉最新の証拠と現時点の保存結論

目的は、将来配布元が消えた場合にも復元できる**独立した学習済み成果＋必要な音声/画像codec・依存ソフト＋ライセンスと固定版**を、4TBの計画上限・常時200GBの空き床・150B未満の総学習済みパラメータで確保すること。危険性や無検閲というラベルは優先調査の要因にはできても、無許可取得を正当化しない。

- [最新の実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)には、**62件中61件VERIFIED報告、1件Gated HOLD、708ファイル、409,835,119,252 byte**。先の53件／579file／270,835,576,267byteから8モデル・129ファイル・138,999,542,985byteの**報告増分**。今回の研究環境が実所有者Dドライブにアクセスし、再ハッシュしたわけではない。
- 新規VERIFIED報告8件：`ResembleAI/chatterbox`、`RWKV/RWKV7-7.2B-20260805`、`microsoft/TRELLIS.2-4B`、`GSAI-ML/iLLaDA-8B-Base`、`OpenMOSS-Team/MOSS-TTS-v1.5`、`PrentisAI/GroundGUI-8B`、`ACE-Step/acestep-v15-xl-turbo`、`kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers`。
- [前回の重複排除済み15source候補](../../queues/proposed-v50-r122-deduplicated-next15-sources.json)は**332ファイル／374,701,109,177byte**。これを同一配布元repo・固定revision・ファイルパス・Publisher SHA-256で61件台帳と突合した。18個のSHA照合可能なファイルについて**47,924,439,388byte**のSHA一致が**台帳上で報告済み**。同じIDやrevisionだけでは重複としない。
- その差として、**326,776,669,789byte**が未照合または未報告source候補。うち**326,719,118,903byte**はPublisher SHAがあるが同一ハッシュ報告がなく、**57,550,886byte**は照合できる既報告Git blob SHAが台帳にない小ファイル等。これは**台帳にある重みが所有者媒体に残っているという条件付き**の論理計画量であり、実Dドライブの追加書込み量の実測ではない。


[**次の15source・未照合ファイルの非実行キュー**](../../queues/proposed-v52-r123-ledger61-delta-15-research-only.json) にsource別の未照合SHA、パス、byte、既報告一致分を一意に保存した。このファイルは実行不可の調査資料であり、`queues/approved.json`への投入や外部ダウンローダーへ直接渡すことを認めない。

### 同一repoでも保存原本が異なる例

| 固定source repo ID | Source全体（B） | Publisher SHA既報告一致（B） | 未照合の候補（B） | 現在の判断 |
| --- | ---: | ---: | ---: | --- |
| `RWKV/RWKV7-7.2B-20260805` | 14,402,000,339 | 14,399,972,864 | 2,027,475 | 重量3 shard一致報告。重み再取得を停止し、現物SHAと小ファイルだけ再確認 |
| `GSAI-ML/iLLaDA-8B-Base` | 16,512,918,618 | 16,512,839,210 | 79,408 | 重量4 shard＋tokenizerの一致報告。依存と小さな設定ファイルを確認 |
| `microsoft/TRELLIS.2-4B` | 16,237,485,044 | 16,237,464,946 | 20,098 | 重量9ファイル一致報告。フルpipeline復元は別に検証 |
| `Zyphra/ZONOS3-Mini` | 15,345,816,226 | 774,162,368 | 14,571,653,858 | 既報告はteacher一部。同revisionでも主LMとcodec、speaker、headsが欠け得るので保全継続 |
| `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | 53,808,326,934 | 0 | 53,808,326,934 | 取得台帳にあるQ4とRVN-F16は別ハッシュ。Q4済みだからF16原本済みとはしない |
| `InterpreticAI/Qwen3.8-27B-Uncensored-v2` | 55,586,056,799 | 0 | 55,586,056,799 | 既存Q4とは別のBF16/MTP原本を選定。ただし行為別権利・本人D検証が残る |

**技術的な反例**：`Zyphra/ZONOS3-Mini`は61件台帳でVERIFIEDだが、その対象scopeの約775.7MBと、今回の15.346GB保存原本は別パッケージ。repo IDを集合で引き算するだけなら、14.57GBの学習済み音声generator等を見落とす。

## 2. 次の保存順位・交換判断（ダウンロード承認とは別）

| 優先 | 対象 | 判断 | 反証・STOP |
| --- | --- | --- | --- |
| P0 | [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 1.386GBの新規ASR＋学習済みCTC head。v50で正式conditional済。少容量で独立価値、まず権利とCTC checksumに集中 | 既存Whisper/Qwen ASRと同一条件の日本語CER/英語WER・低バッチ速度が劣れば取得優先度を下げる |
| P0 | [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | 既存teacher部のみを完成した原本と混同しない。LM+audio generator+speaker等の残り約14.572GB候補を精査 | 現物Dに同SHA全sourceがあるなら新規取得不要。pickle未信頼コードを実行しない |
| P0 | [sensenova/SenseNova-Loop-9B-GGUF](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF) | 公式作者のpublic GGUFとmmproj約19.338GB。元Safetensors作者Gatedとの違いを記録し、許可される範囲のみ | 正式Gated権限/原本のMTP全構成を検証できたらマスター候補を再評価 |
| P0 | [InterpreticAI BF16](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)・[0bserverx RVN-F16](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 異なる編集済み成果を高精度原本で保存。同一Q4/量子化派生の多重保存を避ける。合計source約109.394GB | 親・権利・source全シャード・D実SHAが欠ける間は実取得停止。政治的抑制編集と全面的な無拒否を混同しない |
| P1 | [Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B)・[Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | 独立ブラウザ操作／長期記憶専門能力。両者で約114.887GBのsource、現在該当revisionの取得報告なし | Faraはsandbox実行、Hy-Memoryは3B activeではなく総30.0647B、権利と依存を審査 |
| P2 | [Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)・[Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | 映像・画像の元学習成果。総約67.05GB、codec/VAEの重複があれば個別SHAで差し引く | **現行158有効の予算**に基づき、必要学習済み依存が既取得か確かめる |
| P3 | RWKV7／iLLaDA／TRELLIS.2 | 重量SHA一致済み報告のため**再DLではなく実Dの再ハッシュと復元**に転換 | 現物が欠損・別SHAなら元Publisher固定revisionで差分のみ再取得を検討 |

**未登録小型モデルの検討**（新規正式追加はまだしない）：

- [gravitee-io/bert-small-pii-detection](https://huggingface.co/gravitee-io/bert-small-pii-detection)：固定commit `f8c27a85c51c0168f07b9dcf00265bf0a4097939`、英語PII25種、主F32重み**114,116,788byte／Publisher SHA-256 `a6319abf8718ec15956b241e8800b0ff4b6b8be5c6b5aa2a43aef765c6e20de3`**。公式repoに同学習重みのONNXと量子化ONNXがあるが、それらを独立学習成果と数えない。**次版conditional提案を維持**。Publisher testではP=0.8182/R=0.9256/F1=0.8686（英語の著者評価）。ラベル・データセットが違うモデルと数値だけで性能比較しない。
- [fastino/gliner2-privacy-filter-PII-multi](https://huggingface.co/fastino/gliner2-privacy-filter-PII-multi)：原作者の7言語・42種類PIIに別途fine-tuneした学習済み原本。固定commit`1cb4166094dc58fa8d836429f060d6c95f62b495`、source全repo表示約1.25GB、主重み約1.23GB、[Xet Pointer SHA-256](https://huggingface.co/fastino/gliner2-privacy-filter-PII-multi/blob/main/model.safetensors) `0280f6f39f6012da50b6640bad438d9b7e763a1b0102094115d1b710c4dd79b6`。HF repo総数307.1Mと作者カードbackbone205Mの相違があり**全学習済みテンソル総数は未確定のため取得準備STOP**。作者のSPY F1=0.477は別データ上の比較で、前者の0.8686と直接比較不可。
- [gravitee-io/gliner4j-gliner2-privacy-filter-PII-multi](https://huggingface.co/gravitee-io/gliner4j-gliner2-privacy-filter-PII-multi) は**fastinoモデルのONNX export**と作者が説明。FP32/FP16/INT8を別訓練原本として登録しない。Java/ONNXで必要な場合のみ、別の推論用形式として残す。
- [maxwell-model/Maxwell-V1-Flash](https://huggingface.co/maxwell-model/Maxwell-V1-Flash) はHF総36.8106B、作者説明の非埋込35B総数／3B active。独立MoE、MBSA・mHC・indexer、公開原本表示約73.6GBで、**アーキテクチャとして保全価値は高い**。しかし作者のbackend条件はNVIDIA driver 580以上、CUDA 13、vLLM custom image／`trust_remote_code`を含み、本人の推論環境・セキュリティ静的監査と本当のアーカイブ余裕が未確認。現段階は研究HOLD、既存Qwen/Granite MoEを消して置換しない。

R121で検討した`RadixArk/DaisyRose-27B`は`main` v51、`harness-hub/Qwen3.8-27B-pi-adapted`はv52でそれぞれ**独立後学習原本を条件付き採用済み**。同一モデルをこのブランチから再度追加しない。pi LoRAは657,633,248byteのsourceを選ぶが、適用元Qwenの正確な学習時revisionが未確認であり、LoRA単体の完全再現は保証しない。

## 3. 規制一次資料：実証された事実と予測を分離

**2026年11月19日施行の事実**：[米Federal Register（91 FR 74970–74999, document 2026-23529）](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は、従来のAI Diffusion RuleによるECCN 4E091のモデルweight規制を撤廃し、代わって高度半導体・遠隔大規模計算の転用先/利用者別制限を詳述する。これは**公開モデルウェイト一般の近い将来の保管禁止が確定した**という根拠に反する。一方、日本での合法なローカル保存・国外再配布・学習データ権利・個別ライセンスは別問題で、全自由利用を認める資料ではない。

**将来の予測（未測定）**：能力悪用への個別対応、本人画像音声・著作権の個別権利削除、事業者gating更新、より広い規制はシナリオにすぎない。各モデルの禁止確率・停止日付は根拠なく数値化しない。Gatedの本人許可を回避しない（https://huggingface.co/docs/hub/models-gated）。EUのopen-source GPAI提供者義務例外も一律ウェイト保管禁止とは別（https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source）。

Exa検索はHTTP 402（利用枠超過）で不能。Hugging Face作者原本、固定tree/blob表示、連携アプリと米BIS/Federal Register政府一次文書で代替。対象モデルの公開表示・Licenseタグは**本人の行為別許可や将来の可用性保証ではない**。

## 4. H/T/D/C/U、数式の単位と再現性

### 変数表（式の全変数）

| 記号 | 意味 | SI単位 | 定義（今回） | 定義域・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `B_Q` | 15配布source集合の全論理容量 | byte（B） | 374,701,109,177 | ファイル単位、同一scope重複は前段R122で除去 | 整数スカラー |
| `B_M` | Publisher SHAの一致が既存ledgerに報告された容量 | byte（B） | 47,924,439,388 | 本人Dの現物SHAは未再計算 | 整数スカラー |
| `B_U` | ledgerに同一SHAが報告されていないファイル容量 | byte（B） | 326,719,118,903 | publisher SHAのあるfileのみ | 整数スカラー |
| `B_X` | SHA突合できなかった小さなメタデータ等 | byte（B） | 57,550,886 | publisher SHA不存在、git SHAは別途 | 整数スカラー |
| `B_R` | 既報告一致分を仮に再利用できた場合の候補残容量 | byte（B） | `B_Q-B_M` | 実物が残存し同一SHAである場合のみ | 整数スカラー |
| `B_D` | 現在の本人Dドライブ空き量 | byte（B） | 未観測null | 過去実行の空き報告と区別 | 未知／整数スカラー |
| `F` | 最低空き床 | byte（B） | 200,000,000,000 | 段階取得中も維持 | 整数スカラー |
| `T` | ダウンロード/解凍/キャッシュの最大追加一時容量 | byte（B） | 未観測null | 実装/並列数依存 | 未知／整数スカラー |
| `P_T` | 学習済みモデルの総パラメータ個数 | 1（無次元） | 全expert、embedding、MTP、learned codecの必要範囲 | 不明はnull、active数代用禁止 | 整数スカラー／null |
| `P_C` | 絶対除外上限 | 1（無次元） | 150,000,000,000 | 等号含む以上は不可 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 評価量に依存 | 評価差・媒体測定の誤差合成 | 分散未測定なので数値化不能 | 未定義／実数 |
| `k` | 包含係数 | 1（無次元） | 推定誤差区間係数 | まだ適用不可 | 未定義／正実数 |

**数値検算**：`B_R = B_Q - B_M = 374,701,109,177 - 47,924,439,388 = 326,776,669,789` byte、また`B_R = B_U + B_X = 326,719,118,903 + 57,550,886` byte。項はすべてbyteで**次元整合**。現在の取得適格条件には`B_D >= F+B_R+T`だけでなく4TB計画の全資産選択済み容量、個人権利、150B未満の全学習済み総数、正しい原本依存、明示承認が必要。未知`B_D,T`を0に置かない。

**H**：主重みを前提にした固定SHA差分保存は、repo単位の再ダウンロードより**独立学習成果の保全率を落とさず大容量重複を減らせる**。小型PII原本2系統は既存汎用LLMの量子化コピーでなく専用学習成果を増す。

**T**：まず各publisher SHA・40桁revision・全file pathを本人Dの実物と比較し、既存61件reportedのうち同じ18SHAについて少なくとも一致/不一致を独立追試。未確認ファイルは部分範囲だけを補う。PIIは英語＋各対象言語でモデルごと最低200例の公開・合成例（データ使用権確認済み）を用意し、同じspan定義のprecision/recall/F1を比較。別モデルの作者F1を直接引き算しない。各環境のCPU/GPU、クロック、batch=1、max tokens、backend、precision・zero-point、OSとライブラリABIを固定して測定。疑わしいcustom codeは静的監査まで実行しない。

**D**：`PASS_SOURCE_METADATA`＝Publisher固定SHAと同一ledger報告に矛盾ゼロ。`PASS_DOWNLOAD`＝本人SHA、利用許可、物理容量、依存、150B、明示approvalの全ゲートを満たす場合だけ。`UNCERTAIN_STOP`＝個人権限・SHA・総数・容量・外部重みのいずれかが未確認。`FAIL`＝150B以上、Gated回避、非承認実行。今回`PASS_DOWNLOAD=0`。

**C**：61件台帳が古い/ファイルを失っている、量子化Q4からF16が再構成できるという誤認、モデルの派生先に独立学習が実はない、PIIの言語間性能が低い、BISの規則対象を混同する、ハッシュ一致の対象と選択ファイル名を取り違える等で仮説は破れる。

**U**：実D容量・保存済みSHA、価格ではなくバイトの選択増分、Publisher更新、License/データ利用権、CPU/GPU/backend/量子化、評価データ分布が主要誤差源。統計標本なしの現段階では`u_c`と`k`は**数値未設定**。

## 5. 連携分野・監査

**機械学習**＝MoE非活性expert・別学習LoRA/蒸留・公平な同条件ベンチ。**デジタル保存学**＝SHA・source revision・音声codec復元・メタデータ。**ソフトウェア供給網**＝custom codeとpickleの静的監査・ABI固定。**情報法**＝著作権・個人情報・Gated権限・輸出管理。

**ERROR CHECK**：v52の205登録／158有効、61 VERIFIED報告、15source／332ファイル、135 Publisher SHAファイル、18 SHA一致報告、矛盾SHAゼロ、総source374,701,109,177B、条件付き残326,776,669,789B、20日新規重みDL0・承認0・main変更0。150B超2モデルは絶対除外、総数不明22（有効9）は準備STOP。取得予定候補の数だけで規制されそうだと確定しない。

## 6.〈次に考える問い〉

61件の取得台帳と本人Dの照合が通った後、次の100GBを無検閲BF16/F16マスター2系統へ優先投入するのか、同じ容量で小型PII＋音声/画像/長期記憶の多様性を増やすのか。正しく測るべき目的変数は**容量あたりの再現不能な独立学習成果数と、依存を含む完全復元成功率**。
