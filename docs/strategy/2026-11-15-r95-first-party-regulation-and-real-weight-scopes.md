# R95 — 現行規制・配布条件・保存ファイルの一次資料監査（2026-11-15）

**基準:** `main` の `v40-20261115`（監査時点）。これは既存選定の削除・ダウンロード承認ではなく、実際の配布条件とモデル実体に基づく次回の取得確定判断のための一次証拠である。

## 1. 現行法令の事実と将来シナリオを混同しない

| 論点 | 一次資料で確認した事実 | この保存戦略への効果 |
| --- | --- | --- |
| EU AI Act Art. 53 | GPAIの一定の自由・OSSライセンス公開モデルには同条1(a)(b)の文書義務免除があるが、**著作権方針(1(c))と訓練内容要約(1(d))まで免除されない**。systemic riskには2項免除はない | **公開ウェイト一律禁止とは断定しない** |
| 2025年1月 BIS AI Diffusion IFR | 一定の先進**closed-weight**モデルの重みに新規規制を設けた規則。open weight全般の新規禁止という説明は不正確 | 元規則を一般的なopen-weight禁止根拠に流用しない |
| 2025年5月13日 BIS | BISはAI Diffusion Ruleについて**不執行指示**と正式撤回の規則化計画を公表。発表だけで正式撤回の日付・法的現行条文まで断定しない | 法律上の実施状態を原文で継続確認。旧規則が全面的に現在有効との推論も禁止 |
| 2024年NTIA | open weightsの便益・リスク継続監視と将来の対象別措置を示す報告。全国一律のclosed-weight義務ではない | リスクは個別の取得条件・再取得可能性・独自能力で評価 |

**一次資料:**
- [EU Article 53](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)
- [EU open-source GPAI Q&A](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)
- [2025 BIS original IFR](https://www.federalregister.gov/documents/2025/01/15/2025-00636/framework-for-artificial-intelligence-diffusion)
- [2025-05-13 BIS enforcement/recission announcement](https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens)
- [NTIA 2024 primary report recommendations](https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations/recommendations)

## 2. 実際に確認できた配布上の制限と学習済み内部構成

### WhissleAI/steer-tts — Gated + NCの個別事実

- 公開API固定SHA: `65ec6a637f4bd9d868064846c69ed85e37d302a0`; `gated=auto`。プロジェクト登録は`conditional`、本人による権限受諾は未確認。
- 当該固定版Hugging Face `LICENSE.md` および作者GitHubの現行 `LICENSE` は **code/weights/voices = CC BY-NC 4.0 + Whissle独自条件**。過去の検索キャッシュに残る「コードMIT」の説明は当該固定版の利用許可として採用しない。
- モデルの正規FP32本体に加え、独立Vocos/MiniLM/WavLMとflow/refiner/prompt adapter/話者ベクトルがある。HFのmainの9,585,639パラメータだけを「完全なTTS pipeline total」としない。
- Publisherが明記した主要6モデルの公称和は約189.13M、prompt adapter 0.5Mや2,825件の512次元speaker vectorも別に存在する。**全テンソル計測をしていないため、この合算は厳密な上界ではない**。150B gateは既存どおり未確定維持。
- 固定版79ファイル973,512,551 bytesから、学習済み原精度FP32・必要な補助モデル・コード/notice中心の57ファイル767,327,370 bytesを抽出。量子化の二重取り、サンプル・評価専用を外した。SHAは配布元メタデータ、ownerローカル照合ではない。
- [R91 fixed source candidate](../../manifests/drafts/v40-20261115-r91-steer-tts-original-fp32.candidate.json), [HF pinned LICENSE](https://huggingface.co/WhissleAI/steer-tts/blob/65ec6a637f4bd9d868064846c69ed85e37d302a0/LICENSE.md), [author code](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/LICENSE).

**判断:** 固有の数値制御TTSを`conditional`で維持。オーナーのGated受諾、NC利用条件、別権利のイベント音、完全パラメータ、コード/ABI、HDD実測が揃うまで取得承認しない。

### ausboss/Qwen-Image-2.1-Consistency-LoRA — step1500を保存、step2000は重複採用しない

- Hub固定SHA `58897a02f4f60f88376eab5676738dd45e5ed1a2`。`step1500`の学習差分159,436,496 bytes、LFS SHA256 `4f44ada1be2189cc23b3d010f9603543403f48454e2f76842a3d30109b20bd63`。
- 開発者テスト（独立測定ではない）ではstep2000はpixel alignmentを改善する一方、原画の色/画風から大きく離れる。作者の推奨step1500を1系統残す。
- 選定はLoRA + README + 2 workflowの4ファイル159,542,938 bytes。元repo全体328,616,200 bytesとの差169,073,262 bytesを保存候補から外す。
- 親`Qwen/Qwen-Image-2.1`を再ダウンロードして二重計上しない。**Qwen Research License**正文、親のrevisions/hash、LoRA互換性を別判定する。
- [R93 source candidate](../../manifests/drafts/v40-20261115-r93-qwen-image-consistency-lora-step1500.candidate.json), [author comparison](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA).

### maya-research/maya2-native — 元重み + Mimi + ECAPAを固定し親Qwen重み二重保存なし

- モデルSHA `87a83efdd6551e038246b6b37836a6264713eec3`、2 original BF16 shards、Hub総2,502,398,656要素（Maya本体の数値。555M depth decoderは既に本体に含む）。
- 必須 `kyutai/mimi@89091b3e466eb6a9d11e537bf26b144f194978f7`、`speechbrain/spkrec-ecapa-voxceleb@0f99f2d0ebe89ac095bcc5903c4dd8f72b367286` は別学習済み資産。Qwen3-1.7B元重みはMaya shard内へ統合済みのため再保存を要求しない。
- 3 public source repoの全スナップショット容量**5,530,178,828 bytes**。これは必要ファイルを削った最終サイズでもソフトウェア一式の最終容量でもない。
- ライセンスは本体Apache-2.0、Mimi CC BY 4.0、ECAPA Apache-2.0。固定コードGit SHA `c6b376868e268551d065c4206193e96257bef4a1`。実行環境はLinux CUDA12.8 / Python3.10–3.12 / Torch2.8 / Transformers5.6.2 / SpeechBrain1.1.2 の作者条件。GPU8GB以上の記述はオーナー実機検証ではない。
- [R94 tri-repo candidate](../../manifests/drafts/v40-20261115-r94-maya2-native-model-codec-ecapa.candidate.json), [author engine](https://github.com/MayaResearch/maya2-native/blob/c6b376868e268551d065c4206193e96257bef4a1/docs/ENGINE.md).

**判断:** 12言語TTSの独立後学習を`conditional`維持。必要なMimi/ECAPAの著作権表示と`.ckpt`安全な読込、完全パラメータ数、SHA実測とオフライン実行を必須にする。

## 3. ポートフォリオの未達状態と今後の実務

`v40-20261115` の監査時点で、登録195・有効148（うちmodel130 / dataset18）、有効内総パラメータ未確定9、Gated条件付き20、実際の承認済みdownload 0。さらにHDD容量、個別owner entitlement、厳密な全対象ファイルバイト、全ライセンスの正文と依存を横断的に確認できていない。

**優先動作（物理容量と権利は一切飛ばさない）:** 本報告の固定SHA subsetをowner取得マニフェストへ変換 → ユーザー本人の取得条件と空き容量確認 → 毎ファイルhash検証 → システムネットワークを遮断したオフライン復元 → 最終選定・必要なら置換。新たな量子化形式を際限なく増やさない。

S1/S2/S3は「規制がS1→S2→S3の順に現実に進行している」という事実ではなくストレステスト。個別モデルの削除日や規制確率を計算値として創作しない。先に公開された資料の公開日と、後日の検索キャッシュやlicense変更の観測日時を分離する。

**ERROR CHECK:** 3件の固定source候補を生成したがモデルペイロード・SHAをowner側で取得確認した事実は0。研究候補を`approved`と取り違えていない。全件追加や無断ダウンロードは実施していない。
