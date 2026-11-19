# R123｜v52（205資産/158有効）の保存対象決定とDドライブ再取得回避

2026-11-20 JST。対象は`Unjuno/local-model-portfolio`の唯一の正本`main`。`CURRENT.json`は**v52・205資産／158有効（SELECT53＋CONDITIONAL105）**。R122の15固定配布元とv51の[DaisyRose-27B BF16](https://huggingface.co/RadixArk/DaisyRose-27B)、v52の[piエージェントRL adapter](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted)を統合し、**17 source／正本16資産／373固定files／Publisher LFS SHA157参照／430,945,051,898 bytes**を全件検算した。

[機械可読R123全158資産・373ファイル・ハッシュ重複台帳](../../catalog/decisions/2026-11-20-r123-v52-delta-aware-17-source-preservation.json)。正本`catalog/CURRENT.json`、`queues/approved.json`、既存ソースと現物重みは変更していない。今回Windows Dドライブは未マウント・実ハッシュ未測定。**記録上61モデル708ファイル409.835GBのPublisherハッシュ検証済み報告**と、**現時点の完全オフライン復元完了**を同一視しない。

## 1.〈本論〉— 既存のファイルを再取得しない

最新[実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)の61件VERIFIED報告を、R122既存15sourceとv51/52追加2sourceの全**373ファイル**にSHA-256で照合した。

- **20ファイル、47,955,851,385byte**は、配布元と過去のVERIFIED報告のSHA-256が一致する。
- そのうち**18ファイル、47,924,439,388byte**は**同一配布元・同一40桁revision**で一致。内訳はRWKV7重み3件、iLLaDAの4重量＋tokenizer5件、TRELLIS.2重み9件、ZONOS3 teacher codec 1件。
- 追加の**2ファイル、31,411,997byte**は別配布元で同じ内容SHAが確認されたファイル。パス、権利、配布元を混同してはならない。
- **現在のDドライブに上記のファイルが物理的に存在すると独立確認したわけではない**。現物がない、別ボリュームにある、または破損している場合、実際の再取得必要量は増える。
- 同じ新規17source内にもInterpreticとDaisyRoseの`tokenizer.json`で**同一SHA 12,809,320byte**が1組ある。保存時にcontent-addressed dedupする場合でも、両者の復元パスは維持する。

従って、source論理総量`430,945,051,898byte`から過去ハッシュ一致分を控除した**382,989,200,513byteは「過去取得台帳のSHAで再利用証拠が確認できなかった論理source容量」**であり、現在の物理純増や必要取得容量として断定しない。ここでの「一致しない」はSHAの証拠が足りないだけで、ファイル不在の証明ではない。

## 2. 17 sourceの維持・優先・保留

| 固定配布元 | 出版社source byte | 既存VERIFIED報告の同一SHA byte | 独立機能／扱い |
|---|---:|---:|---|
| [`elyza/ELYZA-tasks-100`](https://huggingface.co/elyza/ELYZA-tasks-100) | 7,606,817 | 0 | 日本語評価。Windows非互換ファイル1件を別管理 |
| [`CohereLabs/aya_dataset`](https://huggingface.co/CohereLabs/aya_dataset) | 140,160,376 | 0 | 多言語指示・評価データ |
| [`Reson8/Rumble-2-Flash`](https://huggingface.co/Reson8/Rumble-2-Flash) | 1,385,998,807 | 0 | 45言語の小型ASR＋独立CTC head |
| [`RWKV/RWKV7-7.2B-20260805`](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14,402,000,339 | 14,399,972,864 | 再帰型LM。3重量SHA一致 |
| [`GSAI-ML/iLLaDA-8B-Base`](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 16,512,918,618 | 16,512,839,210 | 拡散言語LM。4重量とtokenizer一致 |
| [`microsoft/TRELLIS.2-4B`](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16,237,485,044 | 16,237,464,946 | 3D形状/材質。9重量SHA一致 |
| [`sensenova/SenseNova-Loop-9B-GGUF`](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF) | 19,338,124,279 | 0 | 公開BF16 GGUF＋vision、公式元SafetensorsはGated |
| [`sensenova/SenseNova-Loop-9B-Preview`](https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview) | 26,724 | 0 | 公式一致コードだけ、Preview configは使用しない |
| [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini) | 15,345,816,226 | 774,162,368 | 音声LM・Codec。teacher 1重みSHA一致 |
| [`Tongyi-MAI/Z-Image-Turbo`](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | 32,848,321,404 | 11,422,654 | 高速画像生成別学習系統 |
| [`Wan-AI/Wan2.2-TI2V-5B`](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | 34,201,539,556 | 0 | 動画・音声/画像生成 |
| [`microsoft/Fara1.5-27B`](https://huggingface.co/microsoft/Fara1.5-27B) | 54,743,814,229 | 19,989,343 | GUI操作エージェントの独立後学習 |
| [`tencent/Hy-Memory-30B-A3B`](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | 60,142,913,025 | 0 | 長期メモリモデル |
| [`InterpreticAI/Qwen3.8-27B-Uncensored-v2`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | 55,586,056,799 | 0 | 無検閲政治回答編集BF16元重み |
| [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 53,808,326,934 | 0 | RVN F16、再構成Safetensorsの既知の元 |
| [`RadixArk/DaisyRose-27B`](https://huggingface.co/RadixArk/DaisyRose-27B) | 55,586,309,473 | 0 | 長期ソフトウェアエージェントRLのBF16 |
| [`harness-hub/Qwen3.8-27B-pi-adapted`](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) | 657,633,248 | 0 | pi coding-agent RL LoRA、親モデルrevision未確定 |

計17sourceは**16件の現行v52有効資産**を構成する。SenseNova Previewの2ファイルは公開作者コードのみであり、元9Bモデルと別個の学習済み成果を数えない。ELYZA等の2件はdatasetで、学習済みモデルとは分ける。全17sourceをダウンロード許可に昇格しない。

### 優先順序

**P0：現物再ハッシュと補完**。RWKV7/iLLaDA/TRELLIS.2の学習済み重量ファイルは全Publisher SHAが同一固定revisionの既存報告と一致した。**まず現物を検証し不足するメタデータ／README／実行コードだけを補完**。ZONOS3もteacher codec重みを照合後、残りのgenerator/decoder等を保全する。コードやpickleを無条件実行しない。

**P1：低容量で独立性の高い原本**。[Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash)は0.5B級・45言語ASR＋CTC headで1,385,998,807byte。WhisperやQwen3-ASRと学習済み重みが別であり、小型の専門用途を補完。出版社の高バッチ速度7,000×実時間という主張は、個人端末batch1の実測ではない。[Hugging Face公式ブログ](https://huggingface.co/blog/rumble-2-flash)。

**P1：無検閲の高精度原本**。Interpretic v2のBF16元シャード55.586GBと0bserverx RVNのF16 GGUF53.808GBは、拒否方向編集後の別学習成果を保存する。`RVN-F16.gguf`は後続のSafetensors再構成元だが、学習時の元BF16が発見されたわけではない。すでにあるQ4を勝手に上書きせず、二重量子化の追加採用は行わない。

**P1（形式制約あり）：SenseNova Loop-9B**。9.4B級の層反復型マルチモーダルモデルはARLoopとは異なる独自学習済み状態。公式SafetensorsはGatedなので、本人の正規権限がない場合は作者公開BF16 GGUF＋mmprojへ限定。Previewの元チェックポイント/configは正式原本とは違うため混用しない。

**P1研究／取得HOLD：pi-adapted LoRA**。配布元固定7ファイル、657,633,248byte（うち学習済みLoRA重み637,610,624byte）。rank32・alpha64、AsyncGRPOによるcoding-agentの独立学習成果。ただし**これは658MBで動く独立LLMではなくQwen3.8-27Bの訓練時親重みが必要**。adapterのtokenizerは親のSHAと異なり、作者の設定に訓練親の不変revisionもない。よって**完全な親＋adapterのオフライン復元は未確定、取得承認不可**。作者のSWE-bench/Terminal-Bench数値は出版社条件での報告にとどまる。[作者モデルカード](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted)。

**P2研究／大容量HOLD：DaisyRose-27B**。55,586,309,473byte、BF16シャード18件、元Qwenに対し全18重みSHAが異なるRL後学習済み原本。別の学習成果として正式CONDITIONAL維持。Terminal Bench4.1 5.6→12.0の改善は**出版社評価のみ**で、同一HWとハーネス・信頼区間付きの独立結果がないため、古いQwen派生を無条件で置換する根拠にはならない。FP8/NVFP4の通常量子化違いは別モデルとして追加しない。[発行元](https://huggingface.co/RadixArk/DaisyRose-27B)。

**そのほか**：動画Wan、画像Z-Image、GUI Fara、長期記憶Hy-Memory、データELYZA/Ayaは用途と学習成果が異なるので保持。ただしデータライセンスとファイルシステムの制約を個別に守る。ELYZAのWindows NTFSコロン入りCSV 1件がR122初期対象から除外済みであり、全元データの完全コピーと称しない。

## 3. 規制と保存動機を区別する

2026年11月19日付で施行された米BISの[官報規則](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)では、**AI Diffusion Rule由来のモデル重み専用ECCN 4E091が撤廃**された。同時に先端半導体および遠隔計算設備の目的地・用途別統制は存在する。したがって「米国で公開重みすべての個人所持が禁止される」という断定は不正確である。Hugging FaceのGated、派生利用・商用制限、第三者の配布中止は別々の事実・将来リスク。モデル別の禁止時期・確率は根拠がなく算出しない。

**Gated観測21件、学習済み総数不明の有効9件**は、権利またはパラメータ数の確認前に最終ダウンロードlockへ入れない。150B超の扱いは`policies/limits.json`の実測条件付き量子化例外だけとし、MoEのactive数で代用しない。

## 4. 4TBアーカイブ計画の変数表と次元確認

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_all` | 17sourceのPublisher論理総容量 | byte (B) | 430,945,051,898 | 正の整数、過去ファイルが含まれる | 整数スカラー |
| `B_hist` | 過去VERIFIED報告と同一SHAの論理容量 | byte (B) | 47,955,851,385 | 現物未再確認、20ファイル | 整数スカラー |
| `B_rest` | SHAの正の再利用証拠がないPublisher論理容量 | byte (B) | `B_all - B_hist` | 0以上、物理的な欠落容量ではない | 整数スカラー |
| `B_dupe` | 17source内の同一tokenizer内容重複量 | byte (B) | 12,809,320 | 二重計上しない条件付き候補 | 整数スカラー |
| `F_floor` | 保存後最低空き床 | byte (B) | 200,000,000,000 | 固定方針 | 整数スカラー |
| `D_now` | 現在の所有者Dの実空き | byte (B) | null（未測定） | 0以上／未知 | nullable整数スカラー |
| `O_peak` | 取得時の最大一時・依存量 | byte (B) | 未測定 | 0以上／未知 | nullable整数スカラー |

算術：`B_rest=430,945,051,898 - 47,955,851,385 = 382,989,200,513 byte`。**次元チェックPASS**：すべてbyteで統一。ただし`B_rest`を`D_now`と誤認しない。R122の15repo374.701GBにDaisy55.586GBとpi adapter0.658GBを追加した**論理選択差分**であり、既存v52全158資産の容量監査完成ではない。取得実行はowner Dの測定、全依存と最大一時容量、個人の利用行為・LICENSE正文、当該source SHAスコープの明示承認を必要とする。`queues/approved.json`は現状空。全ownerファイルを無断で削除しない。

## 5.〈応用・転用例〉／H・T・D・C・U

- **学習・モデル保存**：別RL学習済みadapterとフルBF16の独立性、元checkpointと量子化を分離。
- **ソフトウェア供給網**：Publisher LFS SHA・Git blob SHA1・Python/torch/PEFT/ONNX/CodecのABI・NTFS互換を検証。
- **デジタルアーカイブ**：同一内容の実体を一度だけ保存し、必要な復元パスを保持。
- **法政策と評価**：Gated/利用条件/法域規制と将来仮説を分離し、著者のベンチを独立測定の代わりにしない。

**H**：同一Publisher SHAの重複転送を除外し、独立RL/SFT/拡散/ASR原本を固定すれば保存容量あたりの再構築可能能力が増える。**T**：158現行資産・62履歴・17source／373ファイル／157上流SHA参照を全件照合（逐次停止はSHA、版、容量、権利不一致）。実Dのハッシュ再検証と欠けたコード／runtimeの復元を次工程とする。モデル比較は同一H/W・backend・量子化・clock・batch/contextで30以上の独立反復を要求。**D**：メタデータの同一SHA参照と算術はPASS。現物D容量・本人の利用行為・独立性能・完全復元はUNCERTAIN。無許可取得／Gated回避／実機の容量床割れはFAIL。**C**：過去の重みが別ディスクにある、学習時親が違う、必要な付随学習済みCodecが欠落している場合。**U**：現在のD残容量、公開メタデータの鮮度、法律、実行環境、モデル性能分散が主要因。実測値の統計分布がないため合成標準不確かさ`u_c`・包含係数`k`を数値化しない。

### ERROR CHECK

- v52 **205登録／158有効（SELECT53＋CONDITIONAL105）**維持。
- 過去台帳61 Publisher検証済み報告、1 Gated HOLD、158有効の内訳は61報告＋1 HOLD＋モデル未報告78＋データセット18。
- 17配布元／16現行資産／373論理ファイル／157上流SHA-256参照（156一意）、source総量430,945,051,898byte。
- 20ファイル（47,955,851,385byte）過去SHA一致、同repo・同版18ファイル（47,924,439,388byte）。量子化違い・同一tokenizerと別学習済み重みを混同していない。
- 正式選定の追加・削除・本人承認・モデル重み取得・モデルコード実行は**今回0件**。Owner Dの現物は未調査。Exaはクレジット402、検索結果なし。

## 6.〈次に考える問い〉

**47.924GBの同一revision重みの現物SHAを先に確認して、付随ファイルだけを補完したうえで、残る容量を無検閲原本・pi LoRA・DaisyRoseのどれに優先配分すべきか。**
