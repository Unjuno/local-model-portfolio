# R96 — Hugging Face実配布状態38件・権利ゲート・規制一次資料の整合監査（2026-11-15）

**対象：** GitHub `Unjuno/local-model-portfolio`、監査基準`main`の`v41-20261115`（195登録、148有効）。Hugging Face連携で**38資産を新規照会**し、これまでのCONDITIONALでGatedと記録した**20件全数**を再照合した。今回モデル選定の昇降格・Gated回避・モデル重量取得・取得承認は行わない。

[機械可読の実配布観測台帳](../../catalog/access/2026-11-15-r96-v41-live-hf38-sample.json) / [v41全148件の取得前停止理由](../../catalog/readiness/v41-2026-11-15-r92-all148-gates.json)。

## 1.〈本論〉20件のGated状態を再確認

**事実：** 現行v41のGated資産20件を2026-11-15にHugging Face `hub_repo_details`でそれぞれ照会し、**20/20件ともGated表示を確認**した。モデル19件と医療音声データセット1件を含む。後者をmodel種別で検索するとメタデータが取得できないため、`dataset`種別として照会した。**モデルの欠落や非Gated化と誤判定しない**。

| 現在Gatedと表示された配布元 | 種別 | 現行HFライセンスタグ | v41での最初の取得阻害要因 |
|---|---|---|---|
| [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | model | `apache-2.0` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`black-forest-labs/flux-3-image-klein-base`](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`black-forest-labs/FLUX.2-dev`](https://huggingface.co/black-forest-labs/FLUX.2-dev) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`briaai/Fibo-2.0-dev`](https://huggingface.co/briaai/Fibo-2.0-dev) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`ideogram-ai/ideogram-4-nf4`](https://huggingface.co/ideogram-ai/ideogram-4-nf4) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`Lightricks/LTX-2.5`](https://huggingface.co/Lightricks/LTX-2.5) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`CohereLabs/aya-vision-32b`](https://huggingface.co/CohereLabs/aya-vision-32b) | model | `cc-by-nc-4.0` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`meta-llama/Llama-4-Scout-17B-16E`](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`EPFLiGHT/Meditron3-70B`](https://huggingface.co/EPFLiGHT/Meditron3-70B) | model | `llama3.1` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`google/medgemma-4b-it`](https://huggingface.co/google/medgemma-4b-it) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`nvidia/Cosmos-Predict2-2B-Video2World`](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`facebook/dinov3-vit7b16-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`facebook/dinov3-vith16plus-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`facebook/sam3`](https://huggingface.co/facebook/sam3) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`WhissleAI/steer-tts`](https://huggingface.co/WhissleAI/steer-tts) | model | `cc-by-nc-4.0` | COMPLETE_TRAINED_TOTAL_PARAMETERS |
| [`gradium/phonon-40m-multilingual`](https://huggingface.co/gradium/phonon-40m-multilingual) | model | `cc-by-nc-4.0` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`nvidia/Ising-Decoder-ColorCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | model | `openmdw-1.1` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`nvidia/Ising-Decoder-SurfaceCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | model | `other` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`runwayml/praxis-1-droid`](https://huggingface.co/runwayml/praxis-1-droid) | model | `apache-2.0` | OWNER_SPECIFIC_GATED_ENTITLEMENT |
| [`StephaneBah/AfroRadVoice-FR`](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | dataset | `cc-by-4.0` | OWNER_SPECIFIC_GATED_ENTITLEMENT |

**観測の限界：** 当日のモデルページメタデータの再照会であって、当該不変commitの将来の存続や、現在ログイン中のユーザーが重みへアクセスできることの証明ではない。Gated表示は**政府によるモデル禁止ではなく、配布者側のアカウント単位のアクセス制御**である。[Hugging Face Gatedの公式説明](https://huggingface.co/docs/hub/models-gated)を参照。ライセンスタグが`apache-2.0`でも、全親依存と行為別適用法令が自動的に解決するわけではない。

## 2. 利用価値が高いが総学習済み構成が未確定の9件

9件すべてのHub配布表示を再照会した。ただしHFの「Parameters」はしばしば**主モデルに限定**される。text encoder、VAE、vocoder、draft/adapter、speaker encoder、全MoE expertなどを含む、実行構成全体の正確な値ではない場合がある。このため既存の`UNVERIFIED_BLOCK_FINAL_LOCK`を**そのまま維持**する。

| 既存CONDITIONALのモデル | HFが表示したパラメータ | HFライセンスタグ | 現時点のGated表示 |
|---|---:|---|---|
| [`WhissleAI/steer-tts`](https://huggingface.co/WhissleAI/steer-tts) | 9.6M | `cc-by-nc-4.0` | Gated |
| [`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | —（Hub単体数なし） | `unknown` | Gated表示なし |
| [`Stuubs/Stubelius_Remix_Ltx2.5`](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | —（Hub単体数なし） | `other` | Gated表示なし |
| [`maya-research/maya2-native`](https://huggingface.co/maya-research/maya2-native) | 2502.4M | `apache-2.0` | Gated表示なし |
| [`fishaudio/drama-3`](https://huggingface.co/fishaudio/drama-3) | 35899.6M | `other` | Gated表示なし |
| [`ausboss/Qwen-Image-2.1-Consistency-LoRA`](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | —（Hub単体数なし） | `other` | Gated表示なし |
| [`PrunaAI/P-H3-Image`](https://huggingface.co/PrunaAI/P-H3-Image) | 33123.0M | `other` | Gated表示なし |
| [`nvidia/Kumo-Relational`](https://huggingface.co/nvidia/Kumo-Relational) | —（Hub単体数なし） | `openmdw-1.1` | Gated表示なし |
| [`nvidia/Kumo-Anomaly`](https://huggingface.co/nvidia/Kumo-Anomaly) | —（Hub単体数なし） | `apache-2.0` | Gated表示なし |

**特記：** `WhissleAI/steer-tts`は主モデルの少数パラメータ表示だけで完結しない。作者が必要とするVocos/WavLM/MiniLM/flow/refinerの全学習済み合算が未検証、しかもGated＋非商用条件である。Prunaの主transformerパラメータ表示だけでも全学習済みpipelineを確定できない。LTX2.5由来の2派生は量子化形式・マージ・外部encoderの出典と利用権が未完成。NVIDIA Kumo Relational/Anomalyは公開元Python/torchチェックポイントの静的tensor count・safe loaderの個別検証が必要で、**第三者pickleを実行して確認しない**。

## 3. SELECTの非Gated対照群、ライセンスと選定方針

`SELECT`から抽出した10モデル（Qwen Coder Next、LivePortrait、VibeVoice、MOSS-TTS、Olmo、Gemma、Mistral Small、Nanbeige、gpt-oss、DeepSeek OCR）を照会し、**10件ともGated表示なし**。ただし現行のCONDITIONAL専用アクセス台帳はSELECT 53件の本人権限を網羅していないため、いずれも取得承認とは扱わない。38件の**HFライセンスタグと既存catalogのタグに直接的矛盾は0件**だったが、原本LICENSE正文と著作権上の行為別権限まで一様であるという意味ではない。

**今回の採否決定：既存195資産の採否・モデル構成を変更しない。** 単なる量子化複製を増やしたり、モデルを消去する根拠はない。交換は、固定checkpoint SHAの一致、学習成果の同一性、またはHW/backend/context/batchを揃えた品質・メモリ・速度の優越が立証できた場合に限る。

**調査優先度（取得優先度や規制確率ではない）**：

1. **権利最優先**：Gated20件の本人による正規許諾・実際に許される行為を調べる。NVIDIAの符号種別が異なる量子誤り訂正小型原本2件、Runway Praxis DROID、Whissleの数値制御TTS等は独自成果の可能性が高いが、取得禁止状態のまま扱う。
2. **原本の閉包**：Gated表示のない有効候補について、40文字revision・選択ファイルSHA/byte・全学習済み外部依存・ライセンス正文を1資産ずつ固定する。HDD実空き、キャッシュ、stagingを測る前に正式保存予算を決定しない。
3. **総数不明9件を閉じる**：安全なtensor index/headerや一次実装の静的解析を使う。量子化bit数・MoEのactive expert数を全総数の代用品にしない。親重みを重複取得するのでなく、必要な学習済み依存を明示する。

## 4. 規制に関する確定事項／仮説

- **EUの現行事実**：[AI Act第53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)は一定の自由・オープンソースGPAIについて文書義務の一部を免除する一方、著作権方針と訓練内容要約の義務は残す。[施行FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start)によればGPAIの執行は2026-08-02開始。これはローカル保有・公開ウェイト全体の一律禁止とは異なる。
- **追加の現行日程**：[EU執行タイムライン](https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act)は2026-12-02以降の特定の非同意性的生成物等に関する禁止と透明性移行期限を列挙する。これを「無検閲重み自体が12月2日に禁止される」と読み替えない。
- **中国の現行説明**：[商務省による2026年の輸出技術見直し](https://english.mofcom.gov.cn/News/SpokesmansRemarks/art/2026/art_74bf283f105a4b19a11f7430df3671ae.html)は制限対象となる技術移転を限定し、原則として多くのAI技術の輸出を引き続き可能と説明。モデル個別の公開停止日を示すものではない。
- **仮説**：S1＝特定の高リスクな出力能力、S2＝高度な自律/科学/汎用モデル、S3＝ウェイト公開全般へ提供制限が拡大するシナリオ。今回の38観測で禁止確率や発生順を推定できず、利用権限を上書きできない。

## 5. 変数表・次元確認

| 記号 | 日本語での意味 | SI・情報単位 | 定義 | 定義域・範囲・前提 | 型 |
|---|---|---|---|---|---|
| `A` | 有効選定資産数 | 1（件） | 148 | v41正本、非負整数 | 整数スカラー |
| `G` | 再確認したGated資産数 | 1（件） | 20 | 条件付き20件全数 | 整数スカラー |
| `U` | 総学習済み数が未確認の有効モデル | 1（件） | 9 | canonicalの研究停止ゲート | 整数スカラー |
| `O` | GとUに重なる資産数 | 1（件） | 1（Whissle） | ID+asset_kindで同一性を定義 | 整数スカラー |
| `S` | SELECT対照サンプル件数 | 1（件） | 10 | 全53のうちの意図的抽出、無作為標本でない | 整数スカラー |
| `R` | 今回の重複除去後の照会件数 | 1（件） | `G+U-O+S=38` | 各repo一意 | 整数スカラー |
| `C` | アーカイブ計画容量上限 | byte | 4,000,000,000,000 | HDD実際容量ではない | 非負整数スカラー |
| `F` | 最低実空き余白 | byte | 200,000,000,000 | 本人HDD実測必須 | 非負整数スカラー |

**単位チェック：**`R`は件数だけで加減算し38件となる。`C`と`F`はともにbyteだが、実測の全選定ファイル和・ソフトウェア環境・既存データ・stagingがないため物理容量の適合判定はできない。モデル総パラメータ数・推論ピークRAMとも混同しない。

## 6. H/T/D/C/U・ERROR CHECK

**H：**公開側のGated表示は少なくとも現行20件について以前のメタデータから変わっていない。
**T：**20 Gated全数＋9未確認＋10 SELECT対照（重複1件を除きn_min=38）、模型はmodel、`AfroRadVoice-FR`はdatasetとしてHF連携で照会。作者/HFライセンスタグと既存台帳を比較。
**D：**20/20 Gated一致・38/38一意・ライセンスタグ直接矛盾0件で当日の**メタデータ整合PASS**。本人のGated取得権・全学習済み依存・固定シャードSHA・HDD・オフライン復元は**UNCERTAIN**。無権限取得や依存コード自動実行は**FAIL/STOP**。
**C：**配布元が後日状態を変える、Gated表示が個人の実アクセスを代替しない、モデルのLICENSE正文がタグと異なる、同一学習重みの二重登録が判明する。
**U：**メタデータ時点・HF UI/APIの表示差・ライセンス本文・本人権限・未計数依存・実HDD。測定分布を持たないため合成標準不確かさ`u_c`と包含係数`k`は推定不可。

**ERROR CHECK：**モデル追加・置換・除外0件、登録195／有効148、meta Gated20、未知総数9、承認0、モデル重みDL0。今回の連携では検索API（model_search/paper_search）が利用できず、**新モデル網羅探索を完了したとは主張しない**。

**〈次に考える問い〉：**「次の1件を増やすこと」と「選定済みの1件を法的・技術的に復元可能な状態へ進めること」では、再取得不能性リスクを実際に減らせるのはどちらか。
