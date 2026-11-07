# 44 — v28候補3件の固定ファイル監査・依存共有・容量再計算（2026-11-08）

## 1. 〈本論〉現在の確定事項・選定判断

対象は専用ブランチの[選定提案v28](../../catalog/proposals/03-v28-original-models-2026-11-08.json)にある3モデル、およびMuseの必須ではないが独立に訓練されたDFlash支援モデルである。**正式な選定正本は引き続きv27（173資産・有効126件）**。この研究は**メタデータ取得と静的なGitHub原文検査のみ**であり、重み取得、ファイル実体ハッシュ測定、モデル実行、許諾取得は行っていない。

成果：公開元の**完全SHAのリビジョン4本と46個の選択ファイルの正確なbyte**、そのうちNorthCUAの**16シャード全てのSHA256照合**、PrimeSimが必要とする既存Wan2.2の**6部品の一致**まで確認した。[機械可読・ファイル別の証拠](../../catalog/research/2026-11-08-r33/pinned-file-capacity-and-dependency-audit.json)に全SHAと出典URLを保持。公開元API/Xet/LFSのメタデータを検査したことと、ローカル実体のSHA256を計算したことは別である。

| 選定対象 | 固定revision | 選択範囲 | 公開元から算出した選択ファイルbyte | 既知のv27内容識別子との重複排除後増分 |
| --- | --- | ---: | ---: | ---: |
| [NorthCUA-Mini](https://huggingface.co/beipo-ai/NorthCUA-Mini) | `cafee9af6a950bffea2a4a17544f253abf80d44b` | 16 safetensors＋config/tokenizer/processor/権利文書など27ファイル | 70,234,627,663 B | 70,214,626,587 B |
| [PrimeSim G2](https://huggingface.co/qiyuan-robot/PrimeSim) | `2b213fa94d2c84cb3e042283c9c92aaa3ea8ba3b` | 後学習G2重み＋READMEの**2ファイルだけ** | 10,095,626,552 B | 10,095,626,552 B |
| [Muse Glimmer 30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | `f84ecc3a0ea984a4c04542a84269e3d065350a6e` | BF16 2 shard＋付属文書・tokenizer 12ファイル | 59,581,824,753 B | 59,581,813,395 B |
| [Muse DFlash assistant](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant) | `2c86316d689027b91123638739743fef1d425233` | 支援モデル単独＋設定とLICENSEなど5ファイル | 5,112,011,418 B | 5,111,994,830 B |
| **計** | 四repo、**3本体＋1補助学習済み部品** | **46ファイル** | **145,024,090,386 B** | **145,004,061,364 B** |

除外：NorthCUA-Nano/Pro、PrimeSimの`primesim_base.safetensors`、Museの追加GGUF二形式・大量のExecuTorch PTE・モデルカード画像。前半の学習済みチェックポイントを「単なる量子化」とは呼ばないが、**今回の目的（実行用独立成果を保全し容量を抑える）では同時採用を正当化する追加の品質・復元価値がない**。科学用途でBaseの復元を必要とする場合は別途審査する。

## 2. 一次資料で確定した同一性とパラメータ数

### 2.1 NorthCUA Mini

[配布元完全固定tree](https://huggingface.co/beipo-ai/NorthCUA-Mini/tree/cafee9af6a950bffea2a4a17544f253abf80d44b)・[固定SHA256一覧](https://huggingface.co/beipo-ai/NorthCUA-Mini/blob/cafee9af6a950bffea2a4a17544f253abf80d44b/checksums.sha256)・[学習報告](https://arxiv.org/abs/2611.02102)。Hub safetensors metadataは**35,107,181,936個（全MoE expert含む）**を報告、16 shardの重みファイル合計70,214,494,016 B。index内のtensor payloadは70,214,363,872 B。差はsafetensorsファイルヘッダを含むかどうかであり、容量の矛盾ではない。

NorthCUAの独立したGUI訓練成果は旧Fara/ Holo4のファイル変換ではない。公式資料のOSWorld-Verified 85.30%（361タスク）、WebArena-Verified 70.43%（812タスク）は**開発元報告のRL実験**であり、今回固定したリリースcheckpoint975そのものの独立再測定ではない。元repoが当日公開されていたこととHarness正常動作を混同しない。既知のv27内容識別子では`tokenizer.json`（**19,989,343 B**）など3ファイルが既存と同一。実物ファイルの共有は別途SHA256で検証。

### 2.2 PrimeSim G2と既存Wan2.2

[PrimeSim配布元固定tree](https://huggingface.co/qiyuan-robot/PrimeSim/tree/2b213fa94d2c84cb3e042283c9c92aaa3ea8ba3b)で、`primesim_posttrain_g2.safetensors`の**正確なサイズは10,095,624,506 B**、公開元LFS payload SHA256は`ce2abce0ae21090392e0825e8b7c9052c7f05f1d5a009fa1762d4ad53671b39d`。Baseも同byteだが別SHAで、訓練済み重量として別物。BaseとG2の両方を自動採用しない。

[公開コード完全コミット](https://github.com/PrimebotTech/PrimeSim/tree/b1e92466184da1bf3c55cc1a555dc4c2a06a597a)の`config/model/primesim.yaml`、README、[GPLではないApache 2.0のLICENSE](https://github.com/PrimebotTech/PrimeSim/blob/b1e92466184da1bf3c55cc1a555dc4c2a06a597a/LICENSE)を読取確認。**HF重量repo自身にLICENSEファイルがない**が、カードはApache-2.0と記載。これは「禁止」の証明ではない一方、GitHubコードの許諾が重みにどう及ぶかは原文・同意を再確認する必要がある。

同じ著者のコードは、Wan2.2-TI2V-5Bの`models_t5_umt5-xxl-enc-bf16.pth`、`Wan2.2_VAE.pth`、`google/umt5-xxl/`のファイルを**外部必須**とする。既存v27の`Wan-AI/Wan2.2-TI2V-5B@921dbaf3f1674a56f47e83fb80a34bac8a8f203e`の**選択済みファイル台帳**を直接検査し、この**6ファイル・計14,202,213,669 B**が、同一固定元・同一payload SHA/Blob IDで既に計上済みであると確認した。したがって**一次資料に基づく追加の論理容量としてこの14.20GBを二度計上しない**。所有者HDDに実ファイルがあるかは不明。

PrimeSimの完全学習済みpipeline総パラメータ数は未確定。本体約5Bを口実にT5/VAEの総数を省かず、正式取得lockを停止する。著者の10.1 FPSは**NVIDIA A100 80GB、BF16、3視点各288×384、4ステップ**。クロック・バッチ等未確定であり実機ベンチではない。

### 2.3 Muse Glimmer と DFlash

[BF16固定tree](https://huggingface.co/meta-models/Muse-Glimmer-30B/tree/f84ecc3a0ea984a4c04542a84269e3d065350a6e)のsafetensors indexは**29,776,626,688パラメータ／tensor payload 59,553,253,376 B**、ファイル2 shardのヘッダ込みbyte合計は59,553,435,272 B。[DFlash固定tree](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant/tree/2c86316d689027b91123638739743fef1d425233)の独立支援ネットワークは**2,555,985,152パラメータ／5,111,976,608 B**。両者を足した保存構成の公開tensor総数は**32,332,611,840**（150B未満）。DFlashは**ターゲット専用に学習された投機生成補助**であり、単純な量子化複製とは異なる。

公式カードが示すRTX 5090・llama.cpp・batch=1・greedy・**K-Quant＋DFlash**の74.9→233.4 token/sは**BF16＋BF16支援の直接測定ではない**。投機支援のターゲット互換と品質を試験するまで性能保証しない。Apache-2.0と別の`USAGE_POLICY.md`があり、その利用上の条件・派生権利は個別に照合する。固定assistant repoと後日のmain更新を混同しない。

## 3. 4TB計画の再計算（byteは十進）

v27は126有効資産の既知選択コンテンツを**3,417,685,712,585 B**とする。今回の4repoにおける根拠なく件数を増減させず、**46選択ファイル**の明細を集計した。既存v27と今回内部の重複内容識別子を除いた追加分は**145,004,061,364 B**。特にNorthCUAの同一TokenizerとMeta/DFlashのLICENSE・USAGE_POLICYが重複対象になる。

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・範囲・前提条件 | 型 |
| --- | --- | --- | --- | --- | --- |
| B₀ | v27で監査済みの既知論理容量 | byte | 3,417,685,712,585 | 不明な環境容量を含まない | 非負整数スカラー |
| ΔB | 今回の新たな内容識別子で重複排除した選択ファイル容量 | byte | 145,004,061,364 | HF公開元payload SHA256かGit blob SHA-1を一致判定に用い、現物未検証 | 非負整数スカラー |
| C | 保存計画上限 | byte | 4,000,000,000,000 | 実HDD空き容量と同一ではない | 非負整数スカラー |
| U | 机上の容量差額 | byte | C − B₀ − ΔB | 未測定依存・runtime・stagingを含まない | 整数スカラー |
| F | 所有者の物理空き容量 | byte | 実ディスクから読出す値 | 不明。最低200,000,000,000 Bを確保する条件 | 非負整数スカラーまたはnull |

演算は**byte同士の加減算で次元が一致**する。U = 4,000,000,000,000 − 3,417,685,712,585 − 145,004,061,364 = **437,310,226,051 byte**。既知論理選択容量は**3,562,689,773,949 B（約3.563TB）**。これは実空きFでも最終保存可能枠でもない。

前回の3モデル合計**171GBは政策上の予約枠**で、今回の約145GBの正確な一次対象bytesと一致させる必要はない。差の約26GBを確定した余裕と呼ばない。ソース実装、復元依存、ローカルキャッシュ、データの権利、実HDD空きは依然不明。

## 4. 追加候補の排除と新規性確認

- **Dharma Field Extractor**：[開発者一次記事（2026-11-04）](https://huggingface.co/blog/Dharma-AI/dharma-field-extractor)は2B版DharmaOCR-LITE v1.1への43,384件の別LoRA学習を記す。しかしHFモデル検索の`author=Dharma-AI`で確認できた正式公開repoは`Dharma-AI/Dharma-OCR-LITE`のみ。**Field Extractorの固定ダウンロード可能なadapter ID・LICENSE・ファイルは未確認**なので研究HOLD。記事の「使える」を「重み取得できる」と言い換えない。医療文書や本人確認書類に言及する記事は、これらの現実の個人データを取得する権利も意味しない。
- **Granite Switch 4.1.1**：[IBM開発元の4.1.1モデルカード](https://huggingface.co/ibm-granite/granite-switch-4.1-30b)はDecision aLoRA改訂と音声更新を説明。**v27台帳の`ibm-granite/granite-switch-4.1-30b`は既に4.1.1固定版`eb206725d03c0f1c409ce3aa512afe325fdf8731`を選定済み**。追加モデルとして再採用しない。既存原本の持続的保存優先度と分けて扱う。

## 5. H / T / D / C / Uと学際的評価

- **H（反証可能仮説）**：3件の独立後学習モデルと別学習済みDFlash補助の保存によって、既存v27と異なるGUI・ロボット未来映像・エージェント学習の再現範囲が増える。反証は同一SHA・同一学習成果、または選定した必要構成で所期の独立能力を再現できないこと。
- **T（最小検証）**：外部repo4本・選択ファイル46件・親Wan2.2必須6件（固定元同一）を全数静的照合。NorthCUA16/16シャードSHAと元checksumを比較。以後の実機は**同一backend/OS/HW/量子化/バッチ/コンテキスト条件で対象を評価**するまで未実施。今回は公開元の重み・本体バイトを取得しない。
- **D（判定）**：PASS＝公開元の46選択ファイルの名前・byte・識別子、North16/16、Wan6/6、v27原簿不変、取得承認0。FAIL＝不一致・無許諾アクセス・同モデル形式重複・現物無しで「保存済み」と記載。UNCERTAIN＝PrimeSim全総数、コード互換、LICENSE解釈、実HDD空き、ローカルSHA。
- **C（破れ方）**：公開カードの計測が実repoに結び付かない、WANバイトが一致してもbackend ABIが違う、Hubメタデータと実ファイルが食い違う、同じソースSHAでもローカル不完全。
- **U（不確かさ）**：**容量算術の整数byte自体には丸め誤差がない**が、配布元メタデータの信頼性・権利契約・追加runtime bytes・所有者ディスク容量が系統的な不確かさ。分布未定義のため合成標準不確かさu_c、拡張係数kは非適用。

応用分野：**機械学習**（SFT/蒸留成果の独立性）、**ソフトウェア供給網**（immutable SHA、ABI、依存グラフ）、**デジタルアーカイブ**（同一内容識別子の保存計画と復元可能性）、**法・契約管理**（公開・許諾・Gatedと再配布を分離）。

## 6. ERROR CHECK / 〈次に考える問い〉

静的計算は[JSON監査資料](../../catalog/research/2026-11-08-r33/pinned-file-capacity-and-dependency-audit.json)に再現可能な46ファイルの内容識別子とbyteで残した。North16/16 checksum、Wan6/6源データ一致を確認。これは**現物のSHA256一致・実機性能・所有者HDD保存済み・完全権利確認ではない**。CURRENTと取得承認キューに変更はない。

**次に考える問い：** 別学習済み補助部品DFlashは、原本モデルを復元した後に必要な処理速度が再現不能な場合、どの条件で「任意」から「保全必須」へ移すべきか。
