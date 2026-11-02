# 採用ポートフォリオ v3（2026-11-02）

**決定結果**: 旧94有効対象から2件を延期し、候補20件を審査して**11件を有効選定・3件を延期・6件を保留**。現行管理対象130件、有効103件（select 54 / conditional 49）、BACKLOG 12件、HOLD 15件。モデル本体の取得許可は0件。完全な固定取得マニフェストは別工程。

[機械可読の現行ポインタ](../catalog/CURRENT.json) / [全130件を実体化した一覧](../catalog/effective-portfolio-2026-11-02.json) / [変更の根拠](../catalog/revisions/v3-2026-11-02.json)

## 優先判定（採用は取得許可ではない）

- **select** = 原本・用途の独自性が明確で、調査・将来の保存対象として採用。ただし必要容量/確定版/依存/権利本文/実機RAM未確認なら取得不可。
- **conditional** = 能力は採用したいが追加の権利・依存・安全監査が必須。特にLlama3.1、SDXL、音声や顔、pickle重み、非商用モデル。
- **deferred/BACKLOG** = 既存の同種機能に対して追加価値が未実証、または依存/容量に比して優先度が低い。歴史を消さない。
- **hold/HOLD** = 個別の利用条件・配布権・学習来歴や安全性の確認不足が重大。取得対象に含めない。

## 新候補20件の決定

| repo ID | 判定 | 表示総repo容量（十進GB、概算） | 特記 |
| --- | --- | ---: | --- |
| [dphn/Dolphin3.0-Llama3.1-8B](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B) | **conditional** | 16.1 | 独自の後学習。Llama 3.1利用条件の確認が必要 |
| [knoveleng/Qwen3.5-9B-Uncensored](https://huggingface.co/knoveleng/Qwen3.5-9B-Uncensored) | **hold** | 未確認 | モデル使用条件の表示不足、元モデルと拒否編集方法を確認 |
| [OnomaAIResearch/Illustrious-XL-v1.1](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.1) | **conditional** | 6.94 | SDXL派生のイラスト特化原本。SDXLライセンスと学習素材権利を確認 |
| [Laxhar/noobai-XL-Vpred-1.0](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0) | **hold** | 未確認 | 権利・配布条件とIllustrious系との重複が未解決 |
| [InstantX/InstantID](https://huggingface.co/InstantX/InstantID) | **conditional** | 4.22 | 人物ID保持という独立能力。pickle重みと顔利用同意の審査が必要 |
| [KlingTeam/LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | **select** | 2.14 | MIT表示の動画モーション系。顔の利用同意を前提に研究用原本を保全 |
| [TencentARC/PhotoMaker](https://huggingface.co/TencentARC/PhotoMaker) | **deferred** | 未確認 | InstantIDと同系統の人物一貫性。差別化の実測まで延期 |
| [ByteDance/InfiniteYou](https://huggingface.co/ByteDance/InfiniteYou) | **deferred** | 43.2 | FLUX.1-devへの依存と43GB級の追加コスト。権利・固有性能比較まで延期 |
| [Plachta/Seed-VC](https://huggingface.co/Plachta/Seed-VC) | **conditional** | 3.94 | 独立した音声変換系。配布重みとコードの別個の権利を審査 |
| [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) | **select** | 13.9 | 表現力・多言語TTS。MIT表示、pickle/音声依存と声同意は別ゲート |
| [SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS) | **conditional** | 6.74 | フローマッチングTTS。非商用・音声データ由来を確認 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | **select** | 4.54 | 同系列VoiceDesignと区別し、音声参照/追加学習に使えるBase原本を保全 |
| [fishaudio/s2-pro](https://huggingface.co/fishaudio/s2-pro) | **hold** | 未確認 | 独自ライセンス正文を確認するまで高性能の主張を採用へ格上げしない |
| [OpenMOSS-Team/MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | **select** | 17 | 長文/停止/多言語韻律に独自性。custom_codeは実行承認前に監査 |
| [onnx-community/higgs-audio-v3-tts-4b](https://huggingface.co/onnx-community/higgs-audio-v3-tts-4b) | **hold** | 未確認 | 第三者変換版の元重み・利用条件・再配布条件が未確認 |
| [microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) | **select** | 3.14 | 医科学画像と言語の対照表現。研究用で臨床配備対象外 |
| [StanfordAIMI/CheXagent-8b](https://huggingface.co/StanfordAIMI/CheXagent-8b) | **hold** | 未確認 | 医療研究用の明確なライセンス表示未確認、custom_codeの静的審査前 |
| [boltz-community/boltz-2](https://huggingface.co/boltz-community/boltz-2) | **conditional** | 6.2 | 分子構造/相互作用予測の非LLM基盤。checkpointのpickle安全審査が必要 |
| [coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2) | **hold** | 未確認 | 独自モデルライセンスと新規TTSとの保存重複を解決するまで保留 |
| [fishaudio/fish-speech-1.5](https://huggingface.co/fishaudio/fish-speech-1.5) | **deferred** | 未確認 | S2 Proなど同系列の世代重複。独立した復元価値確認後に再評価 |

## 既存94件から延期した2件

- [black-forest-labs/flux-3-image-klein](https://huggingface.co/black-forest-labs/flux-3-image-klein)：同一FLUX系列のbase重みが別に候補化済み。43.3GB級の重複を避け、異なるIllustrious系列に調査/保存枠を再配分。特殊性能が実証されれば復帰。
- [lightonai/LightOnOCR-3-4B](https://huggingface.co/lightonai/LightOnOCR-3-4B)：0.8B版が全機能を保有する配布者説明に基づき、4B版約9.11GBの追加性能が定量的に示されるまで延期。

## 3.8TB保存枠の慎重な算定

- v2 の旧暫定repo全量（FineWeb-Eduは10BTサンプルのみ）は **3,234,067,678,260 bytes**。
- 延期2件の旧上流repo容量を合算して **52,428,013,695 bytes** 控除する。
- 新規有効11件の公開サイトの丸め表示repo合計は**約84.86 GB**。これは全ファイルの実バイトではなく、しかも別精度の重複を含む可能性がある。
- 新11件に**100,000,000,000 bytes**を仮に確保した計画シナリオでは **3,281,639,664,565 bytes**、余白 **518,360,335,435 bytes**。この余白は**保証値ではない**。すべての固定ファイル容量、cache/staging作業領域、独立依存、実機のHDD空き、権利制限は未確定。
- **実機容量の追補（2026-11-02）**：購入した4TB HDDについて、ユーザーは「実際は約3.8TB」と申告。ただしOSの正確な総容量/空き容量とTB/TiB単位は未確定。仮に正確な利用可能容量が十進3.8TBなら、安全空き200GBを維持すると保存量は最大約3.6TB以下。既存の3.282TB計画からの物理的な追加枠は**約318GB以下**となり、518GBという数字は**3.8TBの論理的選定予算との差に過ぎない**。依存と作業領域の計測後に再計算する。詳細は[保存予算の追補](storage-budget-policy-2026-11-02.md)。
- **ユーザーの利用許可（2026-11-02）**：3.8TBまで有用な取得内容を選定してよく、現行シナリオの3.282TBは終着点ではない。**518,360,335,435バイトの暫定残余**は権利・性能・重複を解決したモデル/専門データ/依存を追加する候補枠として扱う。これは確定空き容量でも、他の安全条件を免除する余剰でもない。
- 価値の低い量子化重複で埋めるのは避ける。追加枠は優先度に従って段階的に埋め、必要ファイルと実機容量が確定するまで確保済みと称しない。

## 最初の取得準備バッチ（別ファイルで固定）

1. Qwen/Qwen3.5-0.8B — 軽量LLM/画像入力基準
2. lightonai/LightOnOCR-3-0.8B — 文書OCR/配置抽出
3. openai/whisper-large-v3-turbo — 音声認識/比較基準

上記は**以前の台帳ですでに選定済み**の低容量モデル。GitHubに保存済みの2026-10-30上流ファイルサイズ/SHAを元に、`manifests/drafts/` に**承認前の非実行取得案**を生成する。依存、ライセンス本文、推論メモリ、HDD検証の未解決があるため`queues/approved.json`には入れない。

## 安全・検証

本人同意なしの声・顔なりすまし、性的Deepfake、権利未確認のデータ取得は承認しない。高性能・将来規制への推測を観測事実に格上げしない。モデルの重み、runtime、認証/ライセンス、動作の各ゲートを独立に管理。マニフェストは固定コミット・全シャード/processorを基準に作り、モデル本体の自動ロードはしない。
