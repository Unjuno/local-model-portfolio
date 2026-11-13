# 2026-11-11 日本語・ネイティブ音声Full-Duplex追加調査（非実行）
> **ブランチ** `strategy/2026-11-03-01-risk`、参照コミット `f45a30ceea81cabcc0cd386bb97cb0aa8ac9182a`、現行v27・173件、承認0件を**不変**にする。リポジトリにモデル本体を取得・インストール・実行しない。

## 1.〈本論〉今回の結論

**日本語話者向け独立訓練結果である`llm-jp/llm-jp-moshi-v1`をP0優先調査、ネイティブToken制御型`BayLing-Models/BayLing-Duplex`をP1条件付き研究候補とする。** `nu-dialogue/j-moshi`と`j-moshi-ext`はCC BY-NCの研究史上の別重量だが、容量のためP2。Shizuku-Duplexは研究発表のみで公開重み未確認の監視対象。

| 正確なrepo | P | 固定revision | source-only B | 著者/モデルカードの権利表示 |
|---|---|---|---:|---|
| [kyutai/moshiko-pytorch-bf16](https://huggingface.co/kyutai/moshiko-pytorch-bf16) | P1_FOUNDATIONAL | `2bfc9ae6e89079a5cc7ed2a68436010d91a3d289` | 15,760,704,992 | cc-by-4.0 |
| [llm-jp/llm-jp-moshi-v1](https://huggingface.co/llm-jp/llm-jp-moshi-v1) | P0_JAPANESE_RESEARCH_HOLD_LEGAL | `1b5ccfae9cb4f9e981af7538c55671175236af40` | 15,760,962,950 | apache-2.0_publisher_declared_with_J_CHAT_NC_data_rights_unresolved |
| [nu-dialogue/j-moshi](https://huggingface.co/nu-dialogue/j-moshi) | P2_HISTORICAL_RESEARCH | `bb8192b7abb97decb676e5b9613eb42072ab9d1a` | 15,760,964,957 | cc-by-nc-4.0 |
| [nu-dialogue/j-moshi-ext](https://huggingface.co/nu-dialogue/j-moshi-ext) | P2_DISTINCT_TRAINING | `c4676f5aae2155bb20c300dd6c71b6115f97ec1f` | 15,760,964,960 | cc-by-nc-4.0 |
| [BayLing-Models/BayLing-Duplex](https://huggingface.co/BayLing-Models/BayLing-Duplex) | P1_ARCHITECTURE_LICENSE_AUDIT | `b314288d7fc545cdac3b2fe0c4caeb9084c5526b` | 19,091,806,599 | glm-4-voice-License_registration_for_commercial_use |
| [zai-org/glm-4-voice-tokenizer](https://huggingface.co/zai-org/glm-4-voice-tokenizer) | DEPENDENCY_OF_BAYLING_ONLY | `a5f2404e63c84e92f5238908e1706316324ebafa` | 1,458,385,871 | glm-4-voice-License_registration_for_commercial_use |
| [zai-org/glm-4-voice-decoder](https://huggingface.co/zai-org/glm-4-voice-decoder) | DEPENDENCY_OF_BAYLING_ONLY | `81ed541f0350d0b81728681afb628acee62772c2` | 527,082,087 | glm-4-voice-License_registration_for_commercial_use |

### ファイルの実体・重複

- Moshi原本、LLM-jp-Moshi、J-Moshi、J-Moshi-extの**4チェックポイントの`model.safetensors`は全て異なるLFS SHA256**。**1つも単純なビット精度変換やバイト同一コピーではない**。ただしシリアライズハッシュの違いだけで独立した学習内容の品質差は実証できない。各配布元は別の日本語追加学習を説明。
- 4つに含まれるMimi音声トークナイザ`tokenizer-e351c8d8-checkpoint125.safetensors`は**すべて同じSHA256**、サイズ **384,644,900 B**。
- 日本語3モデルの`tokenizer_spm_32k_3.model`もLFS SHA256一致、サイズ **805,634 B**。独立の日本語学習済みコアは各 **15,375,500,136 B**。複数版を保存するなら音声・文字トークナイザは共有させる。
- `LLM-jp`のHub全ファイルは15,760,962,950Bだが、モデルAPIの`usedStorage`は46.5GB程度と大きく異なる。**現行固定スナップショットと履歴を含むリポジトリ容量は別**。4TB計算は現行選択ファイルに限定する。
- BayLingは本体 19,091,806,599B、外部tokenizer 1,458,385,871B、外部decoder 527,082,087B、合計 **21,077,274,557B**（実行環境未含）。`zai-org`の外部学習済み2部品もApacheではなくglm-4-voiceライセンス。
- Shizuku-Duplex ([企業一次発表](https://shizuku.ai/blog/1/)) は2026-11-08発表、80msクロックの相互作用モデル＋非同期の背景モデル。現在公開チェックポイントを公式資料から確認できず、**公開重みが実在すると扱わない**。

## 2. 〈権利〉NIIのApache表記とJ-CHAT非商用条項

- [NII公式発表](https://www.nii.ac.jp/news/release/2026/0225.html)では`LLM-jp-Moshi-v1`をApache-2.0・商用利用可能と説明。`J-CHAT`で事前学習し、約1,000時間の`LLM-jp-Zoom1`で追加学習したことも明記。
- 一方、**[J-CHAT元データセットのカード](https://huggingface.co/datasets/sarulab-speech/J-CHAT)はCC BY-NC 4.0、商用利用不可と明記**。すなわち学習データの利用契約とモデル著者のApache宣言の適用関係は**未解明**。重みにNCが自動伝播するとは断言できず、著者が別途権利を取得した可能性もある。法的な違反/安全性を断定しない。取得の最終審査では公開元への確認が必要。
- `LLM-jp-Zoom1`はNII発表時に公開予定と書かれているが、今回現時点の生データ全量の正当な配布・再配布条件を確認できていない。**同一重みを保管できることと再学習できることは別**。
- `J-Moshi`と`J-Moshi-ext`はCC BY-NC。非商用の保全目的か、再配布したいかを区別する。
- BayLingの[固定版LICENSE](https://huggingface.co/BayLing-Models/BayLing-Duplex/raw/b314288d7fc545cdac3b2fe0c4caeb9084c5526b/LICENSE)はGLM-4-Voice独自ライセンス。**学術研究は無償、商用利用には別登録**。表示義務や名称規定・用途制限などがあり、契約原文を保持する。実際のユーザーの用途・許可を未照合。

## 3. 完全総パラメータのデータ不整合

BayLingの[固定版索引](https://huggingface.co/BayLing-Models/BayLing-Duplex/raw/b314288d7fc545cdac3b2fe0c4caeb9084c5526b/model.safetensors.index.json)には`metadata.total_parameters=516096`とある。しかしHub APIは**BF16重み 9,542,557,728 elements**を報告し、4ファイルの重みだけで約19GB。**索引値をモデル全体のサイズに使うと不合理**。外部Speech Tokenizerは364,587,264 elements、decoderは全学習済み総数未検証。

このためBayLingの完全な`総パラメータ<150B`最終ロックは**UNCERTAIN**。音声復号器の全学習済み部分を含めた独立センサスが必要。適用量子化・モデル名の数字では代替しない。

## 4.〈容量〉v28未採用候補との共同選定

| 記号 | 意味 | SI単位 | 定義 / 定義域 / 型 / 前提 |
|---|---|---|---|
| `B_0` | v27既知source-only重複排除後容量 | B | 3,417,685,712,585 / 非負整数スカラー |
| `B_{28}` | v28未採用3件のSHA-aware追加source-only | B | 145,004,061,364 / 非負整数スカラー、承認なし |
| `B_J` | LLM-jp-Moshiの固定公開ファイル | B | 15,760,962,950 / 非負整数スカラー |
| `B_B` | BayLing +外部音声tokenizer/decoder公開ファイル | B | 21,077,274,557 / 非負整数スカラー |
| `C_{formatted}` | 所有者のフォーマット済実機容量 | B | 未計測の非負整数スカラー |
| `C_{other}` | ABI,ソフトウェア,一時領域,既存ファイル等 | B | 未計測の非負整数スカラー |
| `F_{min}` | 残すべき最低空き容量 | B | 200,000,000,000、スカラー |

容量シナリオは`B_0`に各候補の上界を加算しており、**全てB（バイト）同士の加算**で次元は整合。仮にフォーマット済みで空の3.8TBを想定する場合、少なくとも`B_total + C_other + F_min <= C_formatted`が必要だが、`C_other`が不明なので正式なPASSは出さない。

| シナリオ | source-only合計B | 3.8TB空ボリュームで200GBを残した後の**理論余裕B** |
|---|---:|---:|
| A_v27_only | 3,417,685,712,585 | 182,314,287,415 |
| B_v27_plus_llmjp | 3,433,446,675,535 | 166,553,324,465 |
| C_v27_plus_llmjp_and_bayling | 3,454,523,950,092 | 145,476,049,908 |
| D_v27_plus_unadopted_v28 | 3,562,689,773,949 | 37,310,226,051 |
| E_v27_v28_plus_llmjp | 3,578,450,736,899 | 21,549,263,101 |
| F_v27_v28_llmjp_and_bayling | 3,599,528,011,456 | 471,988,544 |
| G_v27_v28_llmjp_and_minicpm | 3,598,499,372,719 | 1,500,627,281 |

- **v27+未採用v28全3件+LLM-jp+BayLing**は仮想容量だけなら**471,988,544B**の余裕しかなく、ほぼ確実に完全環境・一時領域の検証不能。**取得可能という意味ではない**。
- v28の3件の追加が条件付き提案であり、必ず採用するものではない。容量最適化では独立学習価値・許諾・再取得困難・実行環境を同一候補集合で比較し、巨大かつ未検証の重複を機械的に積み増さない。

## 5.〈独立評価〉全二重性を正答率と混同しない

- [EMNLP 2026査読論文](https://aclanthology.org/2026.emnlp-main.1126/)は、全二重性を単なる製品タグではなくL0–L3の意思決定位置、`T×I×R`の相互作用、IDLE/LISTEN/SPEAK/WAIT/DUAL状態で分類。
- [InteractionBench一次研究](https://arxiv.org/abs/2611.02430)（2026-11-02公開、実験は8–9月）は同じ音声入力で約1,519採点実験。Moshiの音声課題は **3/50**、PersonaPlex **9/50**、カスケード **38/50**。長期会話の事実保持はMoshi **7/50**、PersonaPlex **15/50**、カスケード **39/52**。すなわち、全二重は必ずしも知的応答の成功率を意味しない。
- **これらの数値は日本語Moshi、BayLing、Sophon、Shizukuの独立評価ではない**。英語タスクやバックエンド・時期が異なるため自動的な順位付けには使わない。
- [IWSDS 2026論文](https://aclanthology.org/2026.iwsds-1.10/)は訓練会話の様式により自然さ・重なり・意味の一貫性が変わることを示す。これがMoshiの同系派生を**ハッシュだけで捨てず、学習成果単位で保存判断する理由**。

## 6. H / T / D / C / U、ERROR CHECK

**H**：4つのMoshi系checkpointは単純な同一ファイルコピーではなく独立した重みが存在。測度＝LFS SHA256。反証条件＝4件の`model.safetensors`のハッシュ一致。  
**T**：4/4のcheckpoint（全選択ファイル）を公開の固定revisionで調査、全必須のLFSハッシュを照合。本文の品質評価は別途本人承認、固定GPU/driver/clock/backend/context/batch、各条件最低30サンプルで測定。  
**D**：4モデルコアのハッシュが相互に異なる＝PASS。Mimi共通ハッシュ一致＝PASS。権利・実容量・実行性能・BayLing全学習済み総数＝**UNCERTAIN / 取得不承認**。  
**C**：前処理や学習コードの欠落、非商用元データの追加契約、公開元の重み差し替え、長時間の相づち/応答破綻、外部音声コーデックの不整合。  
**U**：モデルの再学習に必要なデータ許諾・話者同意、学習済みdecoder、環境・ディスク余裕、独立評価の統計誤差が主要未測定。合成標準不確かさ`u_c`と包含係数`k`は未計測のため設定不能。

**ERROR CHECK**：14件の静的な照合を実施、失敗0件。本人権利は承認せず、モデル取得・実行・正式カタログ編集も行わない。

## 7.〈次に考える問い〉

**日本語の優先軸を、商用利用可能性、失われやすい日本語学習済み重み、対話品質のいずれに置くか？** 単純にすべてのGGUFを持つより、独立学習の元重みを必要な契約/データ出典とともに保存する方が有用な可能性が高い。
