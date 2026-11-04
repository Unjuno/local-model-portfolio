# v13 — Hugging Face 2026-11-04 最新モデル抽出と性能スクリーニング

## 変更点
- 現行v12の**132件→134件**、有効**97件→98件**。追加は2資産のみ。1件conditional（公開GGUF）、1件HOLD（Gated再現可能NVFP4）。
- 単なる古い無検閲モデルの寄せ集めを避けるため、2026年Qwen3.8-27Bを使い、OrcaRouter方式とは異なるARA編集をサブカテゴリーとして比較。
- 新規候補は**ダウンロード承認していない**。同じモデルの全量子化ファイルを収集しない。実際の固定SHA・必要ファイル・実機品質・ライセンス本文まで別ゲート。

### 1. 新たに有効選定（conditional）
- **[0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)**
- 2026-09-20更新、HubモデルメタデータはApache-2.0・公開・配布者のRVN後継。選択検討対象は**`RVN-Q4_K_M-multilingual.gguf`**、提供者表示16.55GB（十進）。旧`Qwen3.8-27B-Heretic-Q4_K_M.gguf`は作者自身が旧版扱いとしており**選ばない**。`chat_template.jinja`の要否を固定版で検証。画像にはmmprojが必要。
- [独立比較DreamFast](https://huggingface.co/DreamFast/Qwen-3.8-27b-abliterlitics)はベース＋派生13系統を同条件で比較。RTX 5090、dynamic FP8、400件の評価、評価モデルはglm-5.3-flash-v2。**RVNは400件中104件で思考未終了、95件でトークン予算打ち切り**を報告。これは通常業務の品質評価とは異なるが、重要な失敗モード。
- 提供者自身のPPLはF16が4.5477、Q4 visionが4.8751（tiny_shakespeare、context2048、RTX PRO 6000 Blackwell）。**これを提案Q4 multilingualの実測値と扱わない**。
- 追加価値はARA多段編集と現行27B級性能、実際の公開GGUF。OrcaRouter同系列と比較するまで**conditional**。

### 2. 再現性研究にHOLD
- **[afdudley/Qwen3.8-27B-abliterated-NVFP4](https://huggingface.co/afdudley/Qwen3.8-27B-abliterated-NVFP4)**
- 2026-08-31更新、Gated、Apache-2.0 metadata。配布者はHeretic実装commit/patch/config、`SHA256SUMS`、NVFP4重みとBF16の視覚/MTPコンポーネントの付け直し手順を公開。作者報告は拒否2/100、原本70/100、KL0.069。**外部による同設定の一般性能比較は未確認**。
- Hub表示26.896Bと親モデル27.7814Bの差があるため、総数は保守的に親の値を記載し、テンソル構成は最終チェック必須。
- 0bserverxとの保存重複、本人のGated承認が未確認なので**HOLD**。

### 3. 既存候補との比較
- 既存[OrcaRouter Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored)は引き続きconditional。DreamFast比較では拒否率だけでなく能力保全・出力安定性を評価。全モデルを無条件で保存するのではなく、独自編集方式の対照として比較。
- 旧[Dolphin3.0](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B)はHOLD継続。3年前の旧モデルを拒否が少ないだけで復活させない。
- NSFW動画[ChrisColeTech LTX-2.3 Uncensored](https://huggingface.co/ChrisColeTech/LTX-2.3-uncensored-v1.4-FP8)は2026-10-14更新をHubで確認したが、license=unknown。正式採用は停止。
- SDXL WAIは古い技術系列で現行2026の生成品質比較未済。NSFW特化だけで優先順位を上げない。
- Mistral Large 4 / OrcaRouter Flash Nextの150B超量子化研究はv12で継続。**実機で使えることの証明がない以上、容量を確保・承認しない**。

### 保全とダウンロード
- X:ドライブ・実機ランタイムにはアクセスしていない。GitHubの更新だけで進行中の旧キューは止められない。
- 現在の3.8TB保存予算は原則維持。ただし**旧v3の暫定3.288TBシナリオに新しい16.55GBを単純加算して確定予算とはしない**。全選択ファイルと既存データ・一時領域・空き200GBを再確認する。

### ERROR CHECK
- 合計134、有効98、R1=57、HOLD=24、BACKLOG=12、R0=14、R2=27、EXCLUDED=0。
- モデル111件、データ23件。150B未満PASS=97、150B超量子化審査2、総数不明12。
- 取得許可0。GitHub Actions静的監査は新revisionに対応。

### 次に考える問い
独立比較で出力途絶が多いARA派生を、OrcaRouter版との同条件試験でどの程度の性能改善が確認できた場合に残すべきか。
