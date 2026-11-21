# R144 / v61 — リアルタイム映像・高速動画・シミュレーションの独立学習成果保全（2026-11-22）

## 1. 目的と結論

[現行正本](../../catalog/CURRENT.json)はv60の224登録／177有効を不変更で保持し、**独立後学習済み3モデルをCONDITIONAL（研究選定・取得未承認）**として追加するv61（**227登録・180有効・SELECT53／CONDITIONAL127**）へ更新。単なる高性能・無検閲タグ・将来規制の予言ではなく、既存ポートフォリオでは再現できない学習済み能力を優先する。重量の自動ダウンロードを実行しない。

[新規3repoの公開元固定source manifest](../../manifests/drafts/r144-2026-11-22-video-world-and-streaming-publisher-sources.candidate.json)／[個別H/T/D/C/U判断](../../catalog/decisions/2026-11-22-r144-v61-new-visual-capabilities.json)／[v61 overlay](../../catalog/revisions/v61-2026-11-22.json)／[全180件STOP](../../catalog/readiness/v61-2026-11-22-r144-all180-gates.json)。

## 2. 正式採否と比較

| モデル／作者primary | 選定 | 独立価値／注意点 |
|---|---|---|
| [apple/FastFrames-S](https://huggingface.co/apple/FastFrames-S/tree/aa099efcedf1b65447106bf9004cde75821f7387) | **CONDITIONAL**・6ファイル947,927,443 byte | 2-step Causal Forcing++生成器は**凍結**し、FastFrames独自の**KV refiner 692,418,448 byte**と**pixel decoder 255,494,944 byte**を新規学習。別形式コピーや未学習wrapperではない。Apple model license apple-amlr（科学研究向け・許諾取消条件等）、実行はLinux x86_64／CUDA12.8。256pではなく**480p**での作者推論速度はユーザー環境のベンチマークではない。 |
| [OpenMOSS-Team/MOSS-VL-Realtime](https://huggingface.co/OpenMOSS-Team/MOSS-VL-Realtime/tree/d1f71a588deaf2b9b9cea7c6fff66cb10847cc86) | **CONDITIONAL**・20ファイル22,687,497,344 byte | 作者11.336B BF16原本5シャード。タイムスタンプ付き連続フレームを受け取り生成中に見る・応答/待機を判断する別の学習済みリアルタイム能力。MOSS-TTSやHaru音声全二重とは違う。custom Python modelling/video_processing実装を固定するが未審査実行禁止。作者の「一つのモデルインスタンスでactive session1件」はスケーラビリティの制約。[技術報告](https://arxiv.org/abs/2608.15045)は作者評価であり実機再現なし。 |
| [nvidia/Cosmos3-Nano-Sim-Transfer](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Transfer/tree/45510d5b8cefa338b7abc01eb702cf1e9cdf6742) | **CONDITIONAL**・44ファイル31,750,521,262 byte | **depth/segmentation/edge/blur**など既存物理シミュレータから生成RGB動画へ変換する因果蒸留済み16Bモデル。既存のSim-Auto（ドライビング／LiDAR）とSim-Bimanual（動作条件付き未来予測）とは異なる重みで、主要6シャードのSHAが異なる。NVIDIA OpenMDW1.1、Hopper/Blackwell・vLLM-Omni/SGLang・Isaac系依存を個別審査する。 |

**非採用の具体例**：[FastFrames-L](https://huggingface.co/apple/FastFrames-L)は別学習結果だが173.55GBの中間重み・14B生成器が大量に重複し、追加価値の実測不明につきHOLD。[OpenMOSS/MOSS-VL-Instruct](https://huggingface.co/OpenMOSS-Team/MOSS-VL-Instruct)はオフライン映像理解の別学習成果だが今回はstreaming固有能力を先行しHOLD。[nvidia/Cosmos3-Nano-Transfer-Auto](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto)は34.497GBの別訓練済み多カメラ／LiDAR元モデルだが、既存Sim-Autoとの増分と実機容量を評価するまでHOLD。既存Inkling無検閲原本の全重量再配布コピーは、選定済み編集差分・高精度親との独立性と品質差が未証明なら追加採用しない。

## 3. 全ファイルと親依存の閉包

出版社API **recursive treeはページ分割**される。特にCosmosでは最初の50エントリだけを全ファイルと誤認しないこと。今回、2ページすべてを取得してSHA・sizeを固定した。

| ソース | Publisher全ファイル | 選択ファイル | 今回の選択source bytes |
|---|---:|---:|---:|
| Apple FastFrames-S | 10 | 6 | 947,927,443 |
| OpenMOSS MOSS-VL-Realtime | 23 | 20 | 22,687,497,344 |
| NVIDIA Cosmos3 Sim-Transfer | 60 | 44 | 31,750,521,262 |
| **計** | **93** | **70** | **55,385,946,049** |

選択はGit blob40桁とPublisher LFS SHA256（16参照）で固定。FastFrames別目的のLingBot独立最適化モデルと実演素材、MOSS図像、Cosmosのサンプル動画・図像は本体と混ぜない。

**FastFramesは追加学習重み0.948GBだけではオフライン実行不能**。作者の[固定チェックポイント手順](https://github.com/apple-aiml-research/ml-fastframes/blob/a65c59240e01cf1de86197fa771ca09b38cf592a/docs/installation.md)に従い次も必要：
- [zhuhz22/Causal-Forcing](https://huggingface.co/zhuhz22/Causal-Forcing) source revision `2f8eb8bb6eeb1238da9d13e5420d342a74d634a6`：`causal-forcing++/framewise-2step.pt` **5,676,220,819 byte**、Publisher SHA256 `8f899a016dffb9539788fac82c6200e43ef6e23b6e61ec6b885bb507a760ce42`。
- [Wan-AI/Wan2.1-T2V-1.3B](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) source revision `37ec512624d61f7aa208f7ea8140a131f93afc9a`：推論向けVAE／UMT5 encoder／tokenizer／license等**10ファイル11,891,015,130 byte**。凍結Causal Forcing generatorで代替できるWanの元DiT約5.676GBは追加取得候補から除外する。訓練時の依存は別途確認。
- 依存sourceの合計**17,567,235,949 byte**は上記3repoの55.386GBに**含まれない**。HDDに既存かは未検証であり、依存ソースを勝手に重複取得／削除しない。`.pt`や`.pth`の信頼できないpickleデシリアライズは静的安全監査を終えるまで実行しない。

Cosmos Sim-Transferの`vae/diffusion_pytorch_model.safetensors` **1,409,400,600 byte**は、選定済みSim-Auto／Sim-Bimanualの同パスPublisher LFS SHA256 `230496cb59ff85bc9c040487737c4062480cb61c71e697b197b4c30142f2a0da`と一致。ただし所有者HDD現物には未照合であり、実転送の削減額としては未確定。モデルの正常復元には当該VAEが必須。

## 4. 96件の取得報告後、次に審査するsource

[取得台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**96モデル・1,370ファイル・1,752,033,357,565 byte**をVERIFIEDと報告。これは本研究が所有者Windows Dを独立再ハッシュしたことや、現在の取得承認の証拠ではない。R140の旧21配布元のうち**20repoが最新ledgerで同一repo IDのVERIFIEDに移行**。残る[ricursiveAI/Ripple-65B-Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview)129,572,889,973 byteはP3 HOLDとする。

新しい[後96件の7配布元 research-only キュー](../../queues/proposed-v61-r145-post96-next-research-sources.json)は、P0：Timestral28M＋Kitten Pico **0.397GB**、P1：InternDecision＋FastFrames追加モジュール **2.683GB**（FastFrames親17.567GBは別）、P2：MOSS-VL-Realtime＋Cosmos Sim-Transfer **54.438GB**、P3：Ripple **129.573GB HOLD**。P0～P2の6source **57,517,864,334 byte**はPublisher参照であり、権利・実機・依存・owner file hash完了前に実行する転送量ではない。

## 5. 現行規則と将来仮説

米BISの[2026年11月19日施行規則§IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion Ruleのモデル重みECCN4E091規定を撤廃。全てのオープンウェイトのローカル所有が禁止されたと主張する証拠ではない。他の輸出先・最終用途要件、Apple研究利用契約、NVIDIA OpenMDW、Apache2著作権表示、第三者データの条件は**それぞれ独立の具体的な停止条件**。将来のモデル固有takedownの確率は不明と記録する。

## 6. H／T／D／C／U：反証可能性と不確かさ

- **H**：既存224件では復元できない高速動画・見ながら対話する映像LLM・シミュレータ制御のRGB生成の3学習成果が保存できる。既存Cosmos VAEのPublisher SHA一致で物理重複を避けられる可能性がある。
- **T**：3repoの全93Publisherファイルと採用70ファイルを列挙、各path・byte・OID/LFSをimmutable40hex revisionに固定。v60旧224件の逐語同一性を検証。180件readiness／127件access／承認0をテスト。ユーザーHW・ドライバ・バックエンド/ABI・量子化方式（zero-point等）・コンテキスト・batchを固定した各30試行で、品質・ピークRAM・レイテンシ・推論速度を後日独立比較。
- **D**：70ファイルのpublisher参照、親SHA、過去224件、全件STOPが一致すれば**メタデータ選定PASS**。SHA不整合はFAIL。本人行為別許諾、Gated権限、実HDD最低残床200GB、全依存、local SHA、off-line復元および明示承認のどれか未確認なら実取得は**FAIL-CLOSED**。実用性能はUNCERTAIN。
- **C**：FastFrames親GPU/Appleライセンス非互換、MOSS realtimeの一例1stream制限や未審査remote code、Cosmosの実機推論負荷大・既存モデルとの差が小さいなどが反証。
- **U**：Publisherのみの品質評価／不完全な親tensor census、物理HDD容量・VAE SHA・未審査torch pickle／CUDA ABI、用途固有品質が主要誤差源。独立反復データ未取得につき合成標準不確かさ`u_c`と包含係数`k`は数値化できない。

学際的連携：機械学習（独立訓練・確率・動画の挙動）、ソフトウェアサプライチェーン（SHA・ABI・安全実行）、法政策（ライセンス・輸出管理・将来規制の区別）、GPUシステム工学（VRAM・外部cache・物理保存の実容量）。

**実行状況**：旧224資産の削除／格下げ0、正式取得承認0、重み取得0、ユーザーHDDの今回の独立再SHA0、未審査モデルコード実行0。承認キューは[queues/approved.json](../../queues/approved.json)で空。
