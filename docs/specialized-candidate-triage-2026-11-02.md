# 特化モデル・無検閲・成人向け隣接・顔/声合成の初期調査（2026-11-02）

**履歴資料**：この候補調査の後、[v3最終選定](selected-portfolio-v3-2026-11-02.md)で20件のうち有効11/延期3/保留6を決定した。最新判断は [CURRENT.json](../catalog/CURRENT.json) を参照。

## 目的と管理範囲

- 本資料はv2当時の**初期候補調査**。調査記録自体は当初110件/有効94件に未計上だったが、後続のv3差分で20件すべての行先を決定済み。
- 追加モデル **20件**（candidate 14件、held 6件）。うち既存の119件一次レビューに出ていたもの 3件。**モデル本体の取得・自動実行・再配布は0件**。
- 配布元は原則 [Hugging Faceモデルカード](https://huggingface.co/models)。Pirate Faceは[別取得経路](https://pirateface.co/)の候補であり、特定のモデルがtorrentで取得できることは**未確認**。サイトの説明は配布者主張として扱い、元リポジトリの固定版・ファイル単位SHA-256・配布権限を独立確認する。

## 領域別の候補数

| 領域 | 件数 |
| --- | ---: |
| uncensored_llm | 2 |
| adult_image_adjacent | 2 |
| identity_synthesis | 4 |
| voice_conversion | 1 |
| expressive_tts | 8 |
| medical_research | 2 |
| scientific_specialist | 1 |

## 候補一覧

| ID | 領域 | 調査優先度 | 状態 | Hub表示ライセンス |
| --- | --- | --- | --- | --- |
| [dphn/Dolphin3.0-Llama3.1-8B](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B) | uncensored_llm | T1 | candidate | llama3.1 |
| [knoveleng/Qwen3.5-9B-Uncensored](https://huggingface.co/knoveleng/Qwen3.5-9B-Uncensored) | uncensored_llm | T2 | held | 未表示 |
| [OnomaAIResearch/Illustrious-XL-v1.1](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.1) | adult_image_adjacent | T1 | candidate | other |
| [Laxhar/noobai-XL-Vpred-1.0](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0) | adult_image_adjacent | T2 | held | other |
| [InstantX/InstantID](https://huggingface.co/InstantX/InstantID) | identity_synthesis | T1 | candidate | apache-2.0 |
| [KlingTeam/LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | identity_synthesis | T1 | candidate | mit |
| [TencentARC/PhotoMaker](https://huggingface.co/TencentARC/PhotoMaker) | identity_synthesis | T2 | candidate | apache-2.0 |
| [ByteDance/InfiniteYou](https://huggingface.co/ByteDance/InfiniteYou) | identity_synthesis | T1 | candidate | cc-by-nc-4.0 |
| [Plachta/Seed-VC](https://huggingface.co/Plachta/Seed-VC) | voice_conversion | T1 | candidate | gpl-3.0 |
| [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) | expressive_tts | T1 | candidate | mit |
| [SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS) | expressive_tts | T2 | candidate | cc-by-nc-4.0 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | expressive_tts | T1 | candidate | apache-2.0 |
| [fishaudio/s2-pro](https://huggingface.co/fishaudio/s2-pro) | expressive_tts | T1 | held | other |
| [OpenMOSS-Team/MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | expressive_tts | T1 | candidate | apache-2.0 |
| [onnx-community/higgs-audio-v3-tts-4b](https://huggingface.co/onnx-community/higgs-audio-v3-tts-4b) | expressive_tts | T2 | held | other |
| [microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) | medical_research | T1 | candidate | mit |
| [StanfordAIMI/CheXagent-8b](https://huggingface.co/StanfordAIMI/CheXagent-8b) | medical_research | T1 | held | 未表示 |
| [boltz-community/boltz-2](https://huggingface.co/boltz-community/boltz-2) | scientific_specialist | T1 | candidate | mit |
| [coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2) | expressive_tts | T2 | held | other |
| [fishaudio/fish-speech-1.5](https://huggingface.co/fishaudio/fish-speech-1.5) | expressive_tts | T2 | candidate | cc-by-nc-sa-4.0 |

個別の保存理由、既存系列との差、権利/依存ゲート、一次論文URL、調査日の記録は [JSON台帳](../catalog/candidates-specialized-2026-11-02.json) に保存する。Hubのライセンスタグと許諾本文は同一ではなく、T1は**保存承認優先順位ではない**。

## 重要な再調査ポイント

1. **無検閲**：Dolphin3.0はLlama系列の後学習重み。Qwen3.5-9B-Uncensoredは配布者による重み直交化の主張であり、拒否率・安全性・性能低下の独立実験は未実施。旧Qwen編集版と同一物として扱わない。将来の規制を確定事実にしない。
2. **成人向け画像生成**：Illustrious XLはイラスト特化だが、NSFW許容範囲の断定は不可。NoobAIは`not-for-all-audiences`メタデータと追加的な利用条件を確認している。実在人物・未成年・権利不明の素材は取得候補にも無条件で含めない。
3. **人物/声の合成**：InstantID、LivePortrait、PhotoMaker、InfiniteYou、Seed-VCはID保持/モーション/音声変換の機能を区別。本人同意のないなりすましや性的Deepfakeの生成・配布に使用しない。音声/顔の参照元への同意証跡は公開Gitに置かない。
4. **高表現力TTS**：新候補はChatterbox、Qwen3-TTS Base、MOSS-TTS v1.5、Fish Audio S2 Pro、F5-TTS、Fish Speech 1.5、XTTS-v2、Higgs Audio v3 ONNX。既存のQwen VoiceDesign、Audio8 TTS、VibeVoice等と重複評価。S2-Pro/Higgsは独自利用条件を精査するまでheld。
5. **医療・科学**：BiomedCLIP、CheXagent、Boltz-2を候補化。前2者は画像/文書の医療研究や胸部X線が中心で診断用途には使用しない。第三者の医療個人データを無許可で収集しない。CheXagentは許諾不明とcustom_codeが承認阻害要因。

## Pirate Faceの扱い

[公式サイト](https://pirateface.co/)によると、BitTorrentとHugging Face由来のハッシュ照合を提案するサービス。これは**同サイトの技術説明**であり、個別モデル・ファイルの正常性や法的権限の保証ではない。次を**すべて**満たして初めて代替配布元として採用する。

- 元のHugging Face repo ID、権利許諾、取得元の完全commit、個々のファイル名/バイト数とSHA-256が照合可能である。
- ファイルのhash値は上流の**完全ファイルSHA-256**と種類を合わせる。Git blob SHAやXet識別子を自動的に同一視しない。
- Gated/非公開/削除された重みを、アクセス制限回避の根拠にしない。許諾が不明なtorrent/seedは**利用・再配布しない**。
- torrentクライアント・外部コードの実行やseedingは別許可であり、既定で無効。安全性・スパイウェア検査は別ゲート。
- 一切のモデル本体取得は、`manifests/*.lock.json`と`queues/approved.json`に対する明示承認の後。

## 残る前提と次作業

- 20件の完全コミットSHA、ファイル台帳、実際の選択容量、ライセンス本文、実行依存、推論RAMは**未確認**。
- まずT1モデルの配布ライセンス/必要ファイルを1件ずつ特定。TTSは [評価・調整計画](tts-expressiveness-evaluation-2026-11-02.md) を別工程で実施。
- 初期調査の時点では保存容量の変更を未算定だった。後続のv3で2件を延期し、100GBの新規採用予算を置く計画シナリオを示した。取得ファイルの容量確定とは区別する。
