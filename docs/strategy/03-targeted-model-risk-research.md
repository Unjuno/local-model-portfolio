# 規制リスク中心のモデル選定の再調査（109モデル、2026-11-03）

対象 `Unjuno/local-model-portfolio` ／基準コミット `6e9389c97d24528df97e4b14a6bc772780141fd3` ／ブランチ `strategy/2026-11-03-01-risk`。対象は**モデル109件**。データ23件は別監査。付属する[全109件の証拠と変更案](../../catalog/proposals/02-targeted-model-risk.json)は**非実行の調査提案**であり、既存v9、01成果物、取得キューは変更しない。

## 1. 〈本論〉結論

従来の選定は**将来の配布制限から原本を守る**という主目的と、一般的な日常利用・全分野技術研究を混同した。検索、OCR、ASR、時系列、基準用小型モデルを、具体的な配布停止根拠なしに上位に置いたのは選定上の誤り。**目的は「危険そうなモデルを数多く集める」ではなく、正規配布が失われる可能性を一次資料で調べ、再取得困難な重みだけを適法に選ぶこと。** 公開停止確率は作らない。

今回の研究で、109モデルについて**公式に公開停止日が告知された個別モデルは確認していない**。網羅的不存在証明ではない。既存Gatedだけでは安全上の停止予告ではなく、ライセンスも商用・契約目的であることが多い。

### 外部の具体的な停止事例（本109モデルではない）

[Hugging Faceの無効化されたGLM-5.3派生ページ](https://huggingface.co/audnai/penclaw-GLM-5.3-abliterated-for-offensive-cyber/tree/main)に**アクセス無効化とContent Policy違反**が明記される。一方で停止時の完全な重みが元repoにアップロード済みだったか、個別の適用条項や停止日時は未確定。[ホスト公式のContent Policy](https://huggingface.co/content-policy)はケース別に無効化できると説明する。モデル名称のuncensored一般への一律禁止の証拠ではない。

このGLM系[関連リポジトリ](https://huggingface.co/audnai/penclaw-GLM-5.3-abliterated)には総数約753Bと表示されるため、**150B以上絶対除外規則で保存候補にしない**。元の無効化repoと完全に同一重みだったというハッシュ証拠もない。[NIST（2026-09-17）](https://www.nist.gov/news-events/news/2026/09/caisis-assessment-zais-glm-53-cyber-capabilities)のサイバー能力評価は能力の公的実測であって、政府からの公開停止命令ではない。

### 対象内の一次資料から確認したこと

- [OrcaRouter Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored)：Gatedかつ拒否制御の変更を開発元が明記。**規制・公開停止予定を確認したわけではない**。原本重みの独自性と親モデルの権利を再調査する最初の対象。
- [FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev)：開発者が安全性調整、禁止用途のフィルタ、条件付きのGated公開を説明。現状の条件付き公開と将来の禁止は別。
- [Fara1.5](https://www.microsoft.com/en-us/research/articles/fara1-5-computer-use-agent/)：2026-07-22にMITの公開重みが一般提供された。エージェント能力があるだけで早期制限されるという単純な仮説には**反対方向の事実**。
- [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)：総80B、active3B、コードエージェント。公開元が配布を継続。具体的な近い将来の禁止予告は未確認。
- [Fibo2 Dev](https://huggingface.co/briaai/Fibo-2.0-dev/blob/main/README.md)や[Ideogram4](https://huggingface.co/ideogram-ai/ideogram-4-nf4/blob/main/LICENSE.md)のGated・非商用制限は**商用/契約条件が確認できるだけ**で、安全上の撤去予定ではない。
- [LivePortrait LICENSE](https://github.com/KlingAIResearch/LivePortrait/blob/main/LICENSE)はMIT本体とInsightFace学習済み依存の研究用途条件を分離。[Fish S2 Pro](https://huggingface.co/fishaudio/s2-pro/blob/main/LICENSE.md)は別の研究・非商用ライセンス。声・顔の合成能力の存在だけでは配布禁止を断定しない。

**政策の逆方向の証拠：** [2026-06-02米国大統領令§3(b)(c)](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/)は政府との任意の事前協力枠を述べ、この節では新モデル公開に強制的な許認可・事前審査を創設しないと明記する。法令本文から公開ウェイト全般の現在の禁止を推定しない。

## 2. 109モデルの新しい非実行リスク調査分類

| 分類 | 件数 | 根拠／取り扱い |
|---|---:|---|
| `EVIDENCE_TARGETED` | 2 | Gated now and publisher describes targeted safety/refusal controls; investigate original legality and irreplaceability first, no observed future ban. |
| `CATEGORY_HYPOTHESIS` | 7 | Relevant capability, but first-party takedown announcement absent in this focused review; require capability test and observed restriction before archive promotion. |
| `LICENSE_NOT_SAFETY` | 12 | Host gate/noncommercial terms mainly document licensing, not a safety-based open-weight prohibition; investigate rights separately. |
| `BROAD_ONLY` | 19 | Only S2/S3 broad-capability restrictions are a hypothesis; do not treat general model power as an imminent delisting. |
| `DEPENDENCY_ONLY` | 6 | Only needed as legally permitted parent/comparator/codec/encoder for a retained risk-core model; not a primary regulatory target. |
| `NO_EVIDENCE_DEPRIORITIZE` | 49 | No model-specific targeted restriction evidence; remove from regulation-first core, preserve ordinary functional catalog if separately desired. |
| `PARAMETER_UNKNOWN_STOP` | 12 | Total model parameter count unresolved: metadata-only research, acquisition preparation and final lock forbidden. |
| `HARD_EXCLUDE_150B` | 2 | At least 150B total trainable parameters including MoE inactive experts: no weight preparation or acquisition. |
| **計** | **109** | うち2件は150B以上除外、12件は総数不明で取得準備停止 |

最優先の*追加調査*は**2件**であり、これらもダウンロード許可を意味しない。能力の特徴のみで注意する`CATEGORY_HYPOTHESIS`は一次資料での規制予定がなく、個別の再取得難度・安全上の公開方針・代替原本の厳密照合が必要。用途一般や性能比較のための`NO_EVIDENCE_DEPRIORITIZE`は規制中心の最優先から外す。**データセット23件は本計数に含めない**。

## 3. 主要モデルの根拠を再確認

| モデル | 新分類 | 確認済み／未確認の境界 |
|---|---|---|
| [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | `EVIDENCE_TARGETED` | First-party refusal-alignment removal card and currently gated Hub listing; specific future withdrawal unconfirmed. |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | `EVIDENCE_TARGETED` | Publisher documents safety fine-tuning, filters and conditional gated open-weight release. No announced future ban. |
| [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | `CATEGORY_HYPOTHESIS` | Microsoft expanded public MIT weight release on 2026-07-22 and describes consent checkpoints; this contradicts automatic early agent withdrawal. |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | `BROAD_ONLY` | Publisher confirms total 80B (3B active) public code agent. No model-specific restriction or dangerous capability established. |
| [KlingTeam/LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | `CATEGORY_HYPOTHESIS` | MIT project with noncommercial-research InsightFace pretrained dependency; neither licensing nor face animation establishes a pending weight ban. |
| [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | `CATEGORY_HYPOTHESIS` | No model-specific targeted publisher takedown evidence established in this research; old v9 synopsis alone is insufficient. |
| [fishaudio/s2-pro](https://huggingface.co/fishaudio/s2-pro) | `CATEGORY_HYPOTHESIS` | Research/noncommercial use permitted, commercial use separately licensed; no scheduled model removal evidenced. |
| [briaai/Fibo-2.0-dev](https://huggingface.co/briaai/Fibo-2.0-dev) | `LICENSE_NOT_SAFETY` | Gated noncommercial terms with separate commercial agreement; not a safety-ban announcement. |
| [ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | `LICENSE_NOT_SAFETY` | Gated distribution under Ideogram Non-Commercial Model Agreement; not evidence of a proposed safety ban. |
| [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | `NO_EVIDENCE_DEPRIORITIZE` | No model-specific targeted publisher takedown evidence established in this research; old v9 synopsis alone is insufficient. |

## 4. 全109モデルの台帳比較

一次配布リンクと確認日は全件JSONに保存。未提示のモデル固有の規制確率はnull。Hubの公開表示は取得権限を示さず、独自性の定量評価も未実施。

| repo ID・一次URL | 新分類 | Hub状態（v9） | 150Bゲート | 今回の個別証拠深度 |
|---|---|---|---|---|
| [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | `EVIDENCE_TARGETED` | gated | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`orcarouter/Qwen3.8-Flash-Next-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | `HARD_EXCLUDE_150B` | gated | 150B以上除外 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`dphn/Dolphin3.0-Llama3.1-8B`](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`knoveleng/Qwen3.5-9B-Uncensored`](https://huggingface.co/knoveleng/Qwen3.5-9B-Uncensored) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`LiquidAI/LFM2.5-24B-A2B`](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`microsoft/Fara1.5-27B`](https://huggingface.co/microsoft/Fara1.5-27B) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`Qwen/Qwen3-Coder-Next`](https://huggingface.co/Qwen/Qwen3-Coder-Next) | `BROAD_ONLY` | public | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`tencent/Hy-Memory-30B-A3B`](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`InstantX/InstantID`](https://huggingface.co/InstantX/InstantID) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`KlingTeam/LivePortrait`](https://huggingface.co/KlingTeam/LivePortrait) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`microsoft/VibeVoice-1.5B`](https://huggingface.co/microsoft/VibeVoice-1.5B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`OpenMOSS-Team/MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Plachta/Seed-VC`](https://huggingface.co/Plachta/Seed-VC) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-TTS-12Hz-1.7B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`ResembleAI/chatterbox`](https://huggingface.co/ResembleAI/chatterbox) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`SWivid/F5-TTS`](https://huggingface.co/SWivid/F5-TTS) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`ByteDance/InfiniteYou`](https://huggingface.co/ByteDance/InfiniteYou) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`coqui/XTTS-v2`](https://huggingface.co/coqui/XTTS-v2) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`fishaudio/fish-speech-1.5`](https://huggingface.co/fishaudio/fish-speech-1.5) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`fishaudio/s2-pro`](https://huggingface.co/fishaudio/s2-pro) | `CATEGORY_HYPOTHESIS` | public | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`onnx-community/higgs-audio-v3-tts-4b`](https://huggingface.co/onnx-community/higgs-audio-v3-tts-4b) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`TencentARC/PhotoMaker`](https://huggingface.co/TencentARC/PhotoMaker) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`black-forest-labs/flux-3-image-klein-base`](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`black-forest-labs/FLUX.2-dev`](https://huggingface.co/black-forest-labs/FLUX.2-dev) | `EVIDENCE_TARGETED` | gated | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`briaai/Fibo-2.0-dev`](https://huggingface.co/briaai/Fibo-2.0-dev) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`ideogram-ai/ideogram-4-nf4`](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | FOCUSED_PRIMARY_PUBLISHER_REVIEW |
| [`black-forest-labs/flux-3-image-klein`](https://huggingface.co/black-forest-labs/flux-3-image-klein) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`black-forest-labs/FLUX.2-klein-9B`](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`briaai/Fibo-2.0-edit-turbo`](https://huggingface.co/briaai/Fibo-2.0-edit-turbo) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`bytedance-research/Lance`](https://huggingface.co/bytedance-research/Lance) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Lightricks/LTX-2.3`](https://huggingface.co/Lightricks/LTX-2.3) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`OnomaAIResearch/Illustrious-XL-v1.1`](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.1) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen-Image-2.1`](https://huggingface.co/Qwen/Qwen-Image-2.1) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Tongyi-MAI/Z-Image-Turbo`](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Wan-AI/Wan2.2-TI2V-5B`](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Laxhar/noobai-XL-Vpred-1.0`](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`CohereLabs/aya-vision-32b`](https://huggingface.co/CohereLabs/aya-vision-32b) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`meta-llama/Llama-4-Scout-17B-16E`](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`allenai/Olmo-3-1125-32B`](https://huggingface.co/allenai/Olmo-3-1125-32B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`google/gemma-4-31B`](https://huggingface.co/google/gemma-4-31B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`ibm-granite/granite-switch-4.1-30b`](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`LiquidAI/LFM3-Omni-2B`](https://huggingface.co/LiquidAI/LFM3-Omni-2B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`mistralai/Mistral-Small-4-119B-2603`](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Nanbeige/Nanbeige4.3-33B`](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`openai/gpt-oss-120b`](https://huggingface.co/openai/gpt-oss-120b) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-Omni-30B-A3B-Instruct`](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3.5-35B-A3B-Base`](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) | `DEPENDENCY_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`mistralai/Mistral-Large-4-1T-A52B`](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | `HARD_EXCLUDE_150B` | public | 150B以上除外 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Nanbeige/Nanbeige4.3-33B-Base`](https://huggingface.co/Nanbeige/Nanbeige4.3-33B-Base) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`EPFLiGHT/Meditron3-70B`](https://huggingface.co/EPFLiGHT/Meditron3-70B) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`google/medgemma-4b-it`](https://huggingface.co/google/medgemma-4b-it) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`boltz-community/boltz-2`](https://huggingface.co/boltz-community/boltz-2) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`EPFLiGHT/OLMo-2-32B-MeditronFO`](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`facebook/esm2_t33_650M_UR50D`](https://huggingface.co/facebook/esm2_t33_650M_UR50D) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`HuggingFaceBio/Carbon-X`](https://huggingface.co/HuggingFaceBio/Carbon-X) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`OctoMed/OctoMed-32B`](https://huggingface.co/OctoMed/OctoMed-32B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`EPFLiGHT/Apertus-70B-MeditronFO`](https://huggingface.co/EPFLiGHT/Apertus-70B-MeditronFO) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`StanfordAIMI/CheXagent-8b`](https://huggingface.co/StanfordAIMI/CheXagent-8b) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`nvidia/Cosmos-Predict2-2B-Video2World`](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`ACERobotics/Puffin-World`](https://huggingface.co/ACERobotics/Puffin-World) | `PARAMETER_UNKNOWN_STOP` | public | 総数不明・取得準備停止 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`lerobot/pi0_base`](https://huggingface.co/lerobot/pi0_base) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`microsoft/TRELLIS.2-4B`](https://huggingface.co/microsoft/TRELLIS.2-4B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`nvidia/GR00T-N1.6-3B`](https://huggingface.co/nvidia/GR00T-N1.6-3B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`speridlabs/idol`](https://huggingface.co/speridlabs/idol) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`tencent/Hunyuan3D-2.1`](https://huggingface.co/tencent/Hunyuan3D-2.1) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`m-a-p/MERT-v2-FullSong`](https://huggingface.co/m-a-p/MERT-v2-FullSong) | `DEPENDENCY_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`m-a-p/SheetSage2`](https://huggingface.co/m-a-p/SheetSage2) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`m-a-p/YuE2-3B`](https://huggingface.co/m-a-p/YuE2-3B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`m-a-p/YuE2-Vae`](https://huggingface.co/m-a-p/YuE2-Vae) | `DEPENDENCY_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`facebook/dinov3-vit7b16-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | `DEPENDENCY_ONLY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`facebook/dinov3-vith16plus-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m) | `DEPENDENCY_ONLY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`facebook/sam3`](https://huggingface.co/facebook/sam3) | `LICENSE_NOT_SAFETY` | gated | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`answerdotai/ModernBERT-large`](https://huggingface.co/answerdotai/ModernBERT-large) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`autogluon/chronos-2`](https://huggingface.co/autogluon/chronos-2) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`BAAI/bge-m3`](https://huggingface.co/BAAI/bge-m3) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`deepseek-ai/DeepSeek-OCR-2`](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Edge0/Audio8-TTS-Realistic-0.6b`](https://huggingface.co/Edge0/Audio8-TTS-Realistic-0.6b) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`facebook/vjepa2-vitg-fpc64-384`](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`google/siglip2-base-patch16-224`](https://huggingface.co/google/siglip2-base-patch16-224) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`GSAI-ML/iLLaDA-8B-Base`](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`ibm-granite/granite-speech-5.0-2b`](https://huggingface.co/ibm-granite/granite-speech-5.0-2b) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`ibm-granite/granite-speech-5.0-470m-turboctc`](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`lightonai/LightOnOCR-3-0.8B`](https://huggingface.co/lightonai/LightOnOCR-3-0.8B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`LiquidAI/d1-omni-600M`](https://huggingface.co/LiquidAI/d1-omni-600M) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`LiquidAI/LFM3-1.7B-Base`](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`nvidia/nemotron-labs-unified-asr-0.6b`](https://huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`openai/whisper-large-v3-turbo`](https://huggingface.co/openai/whisper-large-v3-turbo) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`PaddlePaddle/PaddleOCR-VL-1.5`](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`PerceptronAI/Isaac-0.2-2B-Preview`](https://huggingface.co/PerceptronAI/Isaac-0.2-2B-Preview) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`qvac/TranscribePsy-250M-EU`](https://huggingface.co/qvac/TranscribePsy-250M-EU) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-ASR-1.7B`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-Reranker-0.6B`](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3-VL-2B-Instruct`](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Qwen/Qwen3.5-0.8B`](https://huggingface.co/Qwen/Qwen3.5-0.8B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`RWKV/RWKV7-7.2B-20260805`](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`state-spaces/mamba-2.8b`](https://huggingface.co/state-spaces/mamba-2.8b) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`tencent/Hy-SimulMT-30B-A3B`](https://huggingface.co/tencent/Hy-SimulMT-30B-A3B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`Wigtn/Qwen3-VL-2B-WigtnOCR`](https://huggingface.co/Wigtn/Qwen3-VL-2B-WigtnOCR) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`inclusionAI/Ming-3.0-tts-0.5B`](https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`lightonai/LightOnOCR-3-4B`](https://huggingface.co/lightonai/LightOnOCR-3-4B) | `NO_EVIDENCE_DEPRIORITIZE` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`m-a-p/MERT-v2-30s`](https://huggingface.co/m-a-p/MERT-v2-30s) | `DEPENDENCY_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |
| [`nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | `BROAD_ONLY` | public | 150B未満のv9判定 | V9_PRIMARY_URL_CATALOG_ONLY |

## 5. 取得準備を停止する規則と変数表

モデル総数は**150,000,000,000以上を絶対除外**、MoEは非活性expert、学習済みembeddingやMTPも評価する。12件は総数未確認なので一次資料の計数のみ。最終lock、ファイル選択、容量予約、取得準備、取得承認は停止。通常群もGated本人の合法な承認・ライセンス全文・親/外部依存・保存先HDD・空き200GB・3.8TB予算・選択SHA/バイト・RAM上限（512GB未満）・明示ユーザー承認が揃わない限り取得不可。

| 変数名 | 意味（日本語） | 単位（SI） | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `n_total` | 全学習済み総パラメータ数 | 1（無次元） | MoE全expert・付属学習済み構成を含む | 非負整数/null | 整数スカラー/null |
| `n_cap` | 絶対除外閾値 | 1（無次元） | 150000000000 | 以上除外 | 整数スカラー |
| `b_repo` | 上流repo全量 | byte | 台帳上の全ファイル容量 | 非負整数/null | 整数スカラー/null |
| `b_sel` | 選択予定ファイル全量 | byte | 必須依存・シャードを含む固定容量 | 全109件不明null | 整数スカラー/null |
| `group` | 調査優先分類 | 1（無次元） | 上記8分類 | 規制確率ではない | カテゴリ |

**次元チェック：** `n_total`・`n_cap`はいずれも無次元個数で比較できる。量子化でbyteが減っても学習済み総パラメータ数は減らない。`b_repo`と`b_sel`は単位が同じでも測定対象が違い、未確定を0とできない。

### H/T/D/C/U

**H：** 2026-11-03から2027-11-03までに安全性条件を伴うモデル群で実際の追加的配布制限が発生する場合、全一般モデルに一律適用されるより早いという仮説。**T：** 毎週109のrepo ID、完全revision、Gated/Disabled、LICENSE正文と公式告知を比較する設計（`n_min=109`、12週レビュー、52週判定）。継続実行未設定。**D：** PASSは独立配布者の一次措置で対象限定変化→広範囲変化を順に確認した場合。FAILは逆順・同時一律実施。UNCERTAINは事例不足、原因不明、欠測。**C：** 契約・権利・保守終了による変更、又は公開拡大が対立仮説。**U：** 法域、配布者の理由、本人のアクセス、元重みとの同一性、依存/容量などが主要不確かさ。確率分布未校正のため`u_c`と`k`は数量化しない。

## 6. ERROR CHECK／〈応用・転用例〉／〈次に考える問い〉

全109 IDのv9一致、2件の150B絶対除外、12件の総数未確認取得準備停止、記録した全件の取得承認false、旧選定状態を変更しないことを静的に検査。実機ベンチマーク、モデル本体取得、LICENSE全件審査、Gated承認検証、シャードのハッシュ計算は未実施。必要な応用先は**法制度の先行指標、アーカイブの出典・改訂証跡、ソフトウェア供給網/依存管理、HDD保存費用の選別**の4分野。

**次に考える問い：** 個別の公開停止予告が確認できないモデルを、単に「危険に見える」という理由だけで最上位に残すべきか。
