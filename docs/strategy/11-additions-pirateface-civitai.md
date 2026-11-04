# v15 新規モデル選定とPirate Face・Civitai調査（2026-11-04）

### 選定
- **usezn/Galvanize-3**：select。新しい140.6M多言語プロンプト注入分類器、Apache-2.0、ONNX。作者測定AUROC 0.965、非公開3309件で再現率89.6%/偽陽性率0.6%。**公開評価には訓練との重複可能性、512token上限**。[配布元](https://huggingface.co/usezn/Galvanize-3)
- **Edge0/Audio8-TTS-Realistic-Air**：conditional。2026-11-02更新、601.2M本体＋codec、23言語（日本語を含む）。作者のPreview比較はCV3 error 4.80→4.56%、SIM 0.682→0.704。一方Seed-TTS error 1.23→1.25%と悪化もある。**現行Realisticとの同条件比較ではない**。[配布元](https://huggingface.co/Edge0/Audio8-TTS-Realistic-Air)
- **Lightricks/LTX-2.5**：conditional。新multi-shotとdiffusion decoder、22B主DiT＋12B Gemma4 encoderの動画＋音声生成。**Gated・Community License（売上条件等）**、フル依存と実行性能の検証が必要。[配布元](https://huggingface.co/Lightricks/LTX-2.5)
- **kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers**：conditional。独立MITモデル3.178B主変換器、10ステップ・5秒動画＋44kHz音声。作者[GitHub](https://github.com/kandinskylab/kandinsky-6)測定：5秒480×864の動画でRTX4090 24GB・1run 68.0秒、H100 80GB・3run中央値31.2秒（FlashAttention3、module offload）。品質の独立比較と必要encoder/vocoderは未検証。[配布元](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers)
- **opus-research/opus-moderation-4-neo**：HOLD。395.8MのJailbreak技法検出器。作者reported 2万件 F1 .938、英語のみ、512token、学習データにCC-BY-NCがあり権利未確定。[配布元](https://huggingface.co/opus-research/opus-moderation-4-neo)

### 入替
`Edge0/Audio8-TTS-Realistic-0.6b`と`Lightricks/LTX-2.3`を、重複の可能性があるため有効選定から**HOLD**へ移す。旧重みの履歴を消さず、LTX2.3特有のLoRA依存があれば再審査する。Nanbeige4.3-33Bは**select維持**。ユーザー指定除外の6件は復活させない。

### Pirate Face代替取得
[公式](https://pirateface.co/)と[配布ポリシー](https://pirateface.co/policy)を確認。同サービスはHugging Face原本に対応するrevision・SHA256付きTorrentの**二次索引**であり、権利許諾・ファイル完全性・アクセス成功を保証しない。
- Kandinsky：revision `efbaeb9961770cc82fece5b9cb2197049d8c983c`、観測Seeder **0**。
- Audio8 Air：revision `23c305cc013fde378edb459f538317043c993a74`、観測Seeder **0**。
- Galvanize3とLTX2.5はAPI取得不可、Seeder**不明**。不存在と断定しない。
- 原本ライセンス・Gated本人の条件承諾・全ファイルSHA256・実Peerを個別照合し、正規のHFを第一経路とする。P2Pアップロードは利用者のIPを第三者に示すので自動実行しない。

### Civitaiその他
[CyberRealistic Z-Image Turbo v10.0](https://civitai.com/models/2218365/cyberrealistic-z-image-turbo) は元Z-Image Turboの写真特化、FP8約6.41GB。Civitai modelId=2218365、外部資料上のmodelVersionId=3411348。ただしEarly Access/作者会員権限と版別の再配布許諾・元SHA・品質比較が未確定。**研究HOLD、HF repo IDを偽装してアクティブ化しない。** [Gryphe/Pantheon-Reasoning-27B](https://huggingface.co/Gryphe/Pantheon-Reasoning-27B)は2026年SFT/ロールプレイ代表候補だが、作者も十分な品質試験未実施と記述したため研究のみ。OrcaCyber Zero 1.5は重み非公開（API提供）であり保存候補にはできない。

### 実装・誤差・ERROR CHECK
モデルの量子化実行は実機GPU/ホストRAM、backend、ABI、quant/zero-point、context、batch、KV形式、encoder/codec依存の実装条件を必須とする。**今回の配布者計測値は実機性能の保証ではない。** 完全manifestのbyte、immutable revision、SHA256、ライセンス本文、本人Gated同意、3.8TB HDD枠/空き200GB、実機速度・品質、取得の明示承認は未検証。Audio8の`trust_remote_code=True`はコード監査なしに実行しない。LTXはComfy専用int8とPyTorch版を混用しない。

v15想定：管理139資産、内モデル116/データ23。有効94（select53、conditional41）、HOLD27、deferred12、excluded6。総数150B以下ゲート102、総数不明12、量子化例外2。ダウンロード承認0、Torrent開始0、ローカル削除0。
