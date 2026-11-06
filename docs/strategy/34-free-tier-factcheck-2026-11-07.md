# 34 — 無料tier（サービス無料枠）とモデル保全Tierの独立比較・前回Deep Research訂正（2026-11-07）

## 調査範囲・正本

- 対象：[CURRENT](../../catalog/CURRENT.json)、専用ブランチ `strategy/2026-11-03-01-risk`、revision `v26-20261106`、管理172件／有効125件。
- [一次ファイル容量正本](../../catalog/capacity/2026-11-06/v26/capacity-summary.json)：重複前 **3,406,271,632,830 B**、内容識別子による論理重複排除後 **3,403,245,899,240 B**。
- 4,000,000,000,000 B計画枠との差額 **596,754,100,760 B** は**実ディスク空き容量ではない**。34資産に未解決依存があり、完全なオフライン復元総容量はUNKNOWN。所有者HDD空き、現物SHA、ダウンロード時ピーク、同HWでの実行RAMは未測定。
- 無料tier＝外部事業者の無料利用枠。**モデル保全Tier＝失われる学習成果の価値と確保準備順位**。混同しない。2026-11-07公式ページ照合。数値・クォータはアカウント/時点で変化し得る。
- このドキュメントは研究結果のみ。モデル取得、課金、Gated承認、approved queue、main、現行選定には手を付けない。以前の206テスト成功は**v26既存CIの記録**であり、今回の調査のCI成功とは呼ばない。

## 1. 無料サービスtier比較（S/A/B/C/HOLDの相対評価）

S=無料かつ4TBに匹敵する独立・継続・合法保管が実証された場合のみ（今回は**該当なし**）。A=検証用途に実用的、B=限定用途の補助、C=極小/条件付き、HOLD=新規受付停止等。各料金や枠は無料枠の内容であって**モデルの正規取得権限ではない**。

| 分類 | 事業者・サービス | 無料枠／更新 | 4TB保険への適合・制限 | Tier | 公式一次情報 |
|---|---|---|---|---|---|
| 配布 | Hugging Face Hub public | 容量保証なし（best effort） | 自社HFが失われる場合の独立保険にはならない。権利を持たないweight再配布不可 | C | [Storage limits](https://huggingface.co/docs/hub/storage-limits) |
| 非公開保存 | Hugging Face Hub private | Free private **100GB** | 100GBを超える場合は有料。HF単一障害点を解消しない | B | [Storage limits](https://huggingface.co/docs/hub/storage-limits) |
| 配布 | GitHub Git LFS Free | **10GiB保存＋10GiB帯域**（帯域毎月） | 4TB不可。Freeの単一LFS file上限は2GB、公開配布権は別 | B | [Billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)・[Limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) |
| 保管 | Google Drive personal | **15GB**（Gmail/Photos等と共用） | 小型目録向け。長期間容量超過で削除の可能性 | B | [Google One](https://support.google.com/googleone/answer/9004014?hl=ja)・[Quota](https://support.google.com/googleone/answer/6374270?hl=ja) |
| 保管 | Microsoft OneDrive Free | **5GB** | 小型目録向け。転送/地域/保持制限はアカウント別要確認 | C | [Microsoft storage quotas](https://support.microsoft.com/ja-jp/onedrive/microsoft-storage-quotas) |
| 保管 | Dropbox Basic | **2GB** | 長期容量超過で利用制限や削除の可能性 | C | [Basic](https://help.dropbox.com/ja-jp/plans/dropbox-basic-faq)・[Over quota](https://help.dropbox.com/ja-jp/storage-space/over-quota) |
| オブジェクト保管 | Cloudflare R2 Standard | **10GB-month/月**＋Class A 100万/月＋Class B 1000万/月、エグレス無料 | 10GB-monthは毎月の「容量×時間」。数か月貯めると4TBになるわけではない。Infrequent Accessは対象外 | B | [R2 Pricing](https://developers.cloudflare.com/r2/pricing/) |
| GPU研究 | Kaggle Notebooks | **週30時間または高い場合あり**（需要で変化） | GPU保証なし。小型モデル検査向け、永続4TB保管は不可 | A | [Efficient GPU usage](https://www.kaggle.com/docs/efficient-gpu-usage) |
| GPU研究 | Google Colab Free | 無料GPUあり、**正確な週枠とGPU種非公表**／最大12hの場合あり | VM揮発、ファイルホスティング不可、資源保証なし | B | [Official FAQ](https://research.google.com/colaboratory/faq.html?hl=ja) |
| GPU研究 | Paperspace Gradient Free GPU | FreeプランのM4000（旧式）；共有保存5GB、最大自動停止6時間 | P4000/A100の「Free machine」は有料サブスク対象。待ち行列あり | B | [Pricing](https://docs.digitalocean.com/products/paperspace/pricing/)・[Features](https://docs.digitalocean.com/products/paperspace/notebooks/details/features/) |
| GPUデモ | Hugging Face ZeroGPU Free | **日5分**（認証なし日2分）、最初の使用から24hで更新 | キューとホスト資格制限。GPU/モデルweightの永久保存先ではない | C | [ZeroGPU](https://huggingface.co/docs/hub/ja/spaces-zerogpu) |
| CPUデモ | Hugging Face Spaces CPU Basic | 2 vCPU / 16GB RAM / 50GB**揮発ディスク**、時間単価$0 | **新しい実行型（Gradio/Docker）Spaceの作成には有料プランが必要**。Static Spacesは無料 | C | [Spaces overview](https://huggingface.co/docs/hub/spaces-overview) |
| 旧GPU研究 | AWS SageMaker Studio Lab | 既存顧客向けのみ | **新規受付停止**。新規利用者向け無料GPU候補から外す | HOLD | [AWS official](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lab.html) |
| 推論API | Cloudflare Workers AI | **日10,000 Neurons**、00:00 UTC reset | 一部大型モデルはPaid必須。Neurons≠token数。**weight所有権なし** | A | [Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) |
| 推論API | OpenRouter `:free` | **日50 req・毎分20 req** | 失敗呼出しも消費。$10購入後1,000/日は無料枠と区別。**weight保存不可** | A | [Free models](https://openrouter.ai/collections/free-models) |
| 推論API | GroqCloud Free | **モデル別**。例 `gpt-oss-120b` は日1,000 req / 200,000 tokens | 本人のLimitsで確認。組織単位、必ずしも全モデル同じ枠ではない。**weight保存不可** | A | [Groq rate limits](https://console.groq.com/docs/rate-limits) |
| 推論API | Cohere evaluation key | **月1,000 API calls**（trial/評価用） | Production keyとは別。モデルの生weightは所有不可 | B | [Cohere v2 rate limits](https://docs.cohere.com/v2/docs/rate-limits) |

**判定**：調査した無料サービスの利用枠で、3.403TB（さらに未確定依存）を合法・独立・永続的に「無償で」保全できると証明された候補は**ゼロ**。無料GPU/APIは学習成果の評価・目録調査のための補助であり、消失保険のコピーとみなしてはいけない。

## 2. モデル保全Tier（サービス無料tierとは別）

| 優先 | 資産ID | 現v26状態 | 保全根拠／次のボトルネック |
|---|---|---|---|
| S | `PrunaAI/P-H3-Image` | conditional・research-only | MiniMax H3由来の独立蒸留/画像VAE。地理的Community License・全学習済み総数が未確定でLOCK不可 |
| S | `gradium/phonon-40m-multilingual` | conditional・Gated | 5言語独立TTS。本人gate許諾とCC BY-NCの確認が先決 |
| S | `WhissleAI/steer-tts` | conditional・research-only | 12項音響制御の独自後学習。Gated・外部部品/総数欠損 |
| A | `nvidia/Cosmos3-Nano-Sim-Auto`, `nvidia/Cosmos3-Nano-Sim-Bimanual` | いずれもconditional | 各々異なる6つの変換器重み。共通VAE 1,409,400,600 Bは配布元SHA256が同一。CUDA/行動スキーマ・WSM/FA4を固定 |
| A | `pfnet/plamo-3-translate-31b` + `pfnet/plamo-3-translate-0.8b` | conditional | SFT/DPO教師と独立した蒸留生徒。原本と同じweightの量子形式を大量に重複保存しない |
| A | `nvidia/Granary-v2` | conditional dataset | 元の多言語ラベルは111,557,207,020 Bの配布元選定スコープ。原音声は含まれず外部依存・権利を別管理 |
| B | `gradium/phonon-31m-en` | conditional | 英語端末TTS、別codec/voice latentを一組で扱う |
| HOLD | `baidu/ERNIE-5.5-Flash-Base` | catalog外の研究HOLD | 286,245,697,882 serialized elements・全repo288,464,891,869 B。EU/UK/韓国除外等の独自契約、>=150B RAM同等性未実証 |
| HOLD | `orcarouter/GLM-5.3-Flash-Uncensored-GGUF` | catalog外の研究HOLD | Gated・総321B級。元のMTPをGGUFが省略、GPU+CPU総ピークRAMと品質未実測 |
| HOLD | `Louis0324/StyleStream` | tracked hold | 作者がstyle encoder weightsを安全理由で意図的に非公開。任意話者への完全復元不可 |

Tierは**失う学習成果への備え・優先審査**であり、規制の発効確率、性能順位、ダウンロード権限、購入推奨ではない。本人の権限・実機RAM・完全なオフライン復元が確定するまで「選定済」も取得承認にはならない。

## 3. 前回Deep Researchの訂正表

| 先行報告の表現 | v26正本と一次資料に基づく訂正 |
|---|---|
| v26 dedup「3.372TB」 | それは**v25の旧容量**。v26は **3,403,245,899,240 B** |
| v26 primary「約3.712TB」 | v26正本の一次ファイル総和は **3,406,271,632,830 B** |
| 「3.403TBがローカル使用済」 | 実測ではなく配布元ファイルmetadata。所有者HDDは未接続 |
| Qwen397Bの「80GB RAM稼働」 | 重み/量子化ファイル容量・有効expertを実測ピークRAMと混同。150B未満参照機と同一条件比較がないため保留 |
| VibeVoice用「Qwen3.5 tokenizer」 | 固定版候補は `Qwen/Qwen2.5-1.5B@8faed761d45a263340a0528343f099c05c9a4323` のTokenizer subset |
| 「Phononが日本語対応」 | `gradium/phonon-40m-multilingual` の明記対象は英仏独西葡。31M英語はApache-2.0だが40M multiはGated＋CC BY-NC4.0 |
| PLaMo31B BF16「40GB」 | [元repo](https://huggingface.co/pfnet/plamo-3-translate-31b) **63,519,912,375 B**、14-shard |
| Pruna P-H3 original「55GB」 | [Diffusers original](https://huggingface.co/PrunaAI/P-H3-Image)全repo **99,845,388,933 B**、選定44ファイル **99,840,428,064 B**。55GB前後はComfy側の別形式 |
| ERNIE280Bを採用済み | v26 activeには含まれない研究HOLD。既存許諾・地域条件と量子化同等RAM未証明 |
| MOSS-TTSを50MBと断定 | 原本全重み/外部codecを固定確認していない限りUNKNOWN。サイズを創作しない |
| StyleStream完全任意話者再現 | [StyleStream](https://github.com/Berkeley-Speech-Group/StyleStream)ではstyle encoderを未公開。既公開重みだけでフル再現不可 |
| 既存v26 CIを今回の検証と混同 | [Actions 42228957540](https://github.com/Unjuno/local-model-portfolio/actions/runs/42228957540)は以前の206 tests成功。**この文書の調査自体はCI未実行** |

## 4. H/T/D/C/U

- **H:** 無料サービスは4TBの独立した合法な恒久weight保管を提供しないが、小規模な版固定資料・検証作業には利用できる。モデルの保存価値は独自学習成果で決める。
- **T:** 無料枠・無料対象の実際の本人プラン・日次/月次リセット・リスクを公式URLで記録。サービス側の適用は利用直前に再検証。公開不可weightのアップロードは一切行わない。モデルは同一HW/backend/context/batch/精度/同等業務で少なくとも30試行のRAM・品質を別承認後に測る。
- **D:** PASS=公式の当該プラン・モデル・地域で無料/合法かつ必要容量内と確認。FAIL=規約不適合・有料のみ・依存不完全・容量不足。UNCERTAIN=権利、実ディスク、パラメータ総数、実測RAMの未計測。
- **C:** 旧無料枠記事が残る、新規受付終了、実際はAPI/一時GPUのみ、Git LFSでpointerだけが残りpayloadを失う、無料容量超過で削除される、利用規約が改定される。
- **U:** 利用量の変動、契約/地域差、無料枠の告知遅延、真正なSHA確認不足、ソフトウェアABI依存。確率的誤差分布がないため合成標準不確かさ `u_c` と係数 `k` は算出不能。

**ERROR CHECK:** 単位はすべてB/GB/GiB/GB-monthの違いを明示。期間付き無料クレジットを永続無料と数えない。クォータ・容量・実測RAMは別測度。変更内容は本ドキュメントだけであり、重み取得、管理資産、選定履歴、main、実行キューは不変。
