# R122｜小型学習済みAdapter・外部ドラフターの原本選定（2026-11-19）

対象はGitHub `Unjuno/local-model-portfolio`、mainの**v50・203登録／156有効**。[機械可読の判断](../../catalog/decisions/2026-11-19-r122-pi-adapter-draft-decision.json)、[固定source非実行マニフェスト](../../manifests/drafts/r122-v50-pi-adapter-and-nvidia-draft.candidate.json)。今回の**新規正式登録0、実ダウンロード0、承認0**。

## 1.〈本論〉採否を決定

| Publisher原本ID | 一次URL・観測事実 | 優先順位と決定 |
|---|---|---|
| `harness-hub/Qwen3.8-27B-pi-adapted` | [モデルカード](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted)、発行元固定revision `80d05c9051dfd2ae464e1daf4329cb15524caf60`、学習済みLoRA重み637,610,624 byte。rank32/alpha64、AsyncGRPO、Qwen3.8 27B専用 | **P1・原本source選定確定**（取得許可ではない） |
| `harness-hub/Qwen3.8-27B-opencode-adapted` | [別ハーネスの公式LoRA](https://huggingface.co/harness-hub/Qwen3.8-27B-opencode-adapted)。PIと別SHAの重み637,610,624 byte | **P2・OpenCodeハーネスを用いる場合に限って再評価** |
| `nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft` | [NVIDIA公式](https://huggingface.co/nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft)。4,205,751,296学習済み要素・8,431,580,958 byte、NVIDIA Open Model Agreement | **P2・実機の総スループット比較までHOLD** |
| `nvidia/Qwen3.5-0.8B-Qwen3.8-27B-Draft` | [NVIDIA公式](https://huggingface.co/nvidia/Qwen3.5-0.8B-Qwen3.8-27B-Draft)。752,393,024要素、1,524,849,984 byte | **P3・追加保存を見送り**。長文受理長が内蔵MTPを下回る |
| `tencent/Qwen3.8-27B-DSpine-b16` | [Publisher原本](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16)。GitHub取得実行台帳ではVERIFIED報告済み | **既存候補保持・再ダウンロードしない** |

**Rumble-2-Flashは既にv50のCONDITIONAL登録に昇格**しているため、もう一度追加しない。PI・OpenCodeを「量子化違い」と誤認して同一学習結果とすることも避ける。ただし用途の似たAdapterを無条件で両方保存しない。

## 2. PI原本：7ファイル合計 657,633,248 byte を固定

発行元一次API：`https://huggingface.co/api/models/harness-hub/Qwen3.8-27B-pi-adapted/revision/80d05c9051dfd2ae464e1daf4329cb15524caf60?blobs=true`。全12ファイルから装飾PNG・GIF 5件を除外し、学習済み重み＋設定・モデルカード・tokenizer・templateを選択。

| ファイル | bytes | Hash種類 | Publisher Hash |
|---|---:|---|---|
| `.gitattributes` | 1,776 | git_blob_sha1 | `7dce5fee4125799e7c97b510e85a92a263e1b3e1` |
| `README.md` | 18,848 | git_blob_sha1 | `417b13534b57199ff73ba68e71730da2bb010dcc` |
| `adapter_config.json` | 1,171 | git_blob_sha1 | `cb1814360d6ee9549e6b34b532c5ad5c8856a237` |
| `adapter_model.safetensors` | 637,610,624 | publisher_lfs_sha256 | `869b2a089882c0dac4683993f11081bd70edc30b32c64a988c688d6ac26b792a` |
| `chat_template.jinja` | 9,004 | git_blob_sha1 | `9bd39df8984ba783a0b32cf2ebcd2117136e79ff` |
| `tokenizer.json` | 19,989,339 | publisher_lfs_sha256 | `a5cd9732badce41de57e6efce8302930ded1c1188c5f81feb2bd6c24c4a1941f` |
| `tokenizer_config.json` | 2,486 | git_blob_sha1 | `c23583c51714d887cd67b3b996e128c469fa996e` |

**原本の中身を確認した相違点**：固定公式親`Qwen/Qwen3.8-27B@37561816e66b5b9153b1b64c10968c18c1e6f4a0`の`tokenizer.json` SHA-256は `0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3`。PI Adapterの同名ファイルは `a5cd9732badce41de57e6efce8302930ded1c1188c5f81feb2bd6c24c4a1941f`。**相違するため共用不可と仮置きし、Adapter固有tokenizerを含める**。`chat_template.jinja` はGit blob`9bd39df8984ba783a0b32cf2ebcd2117136e79ff`が親と一致。PIとOpenCodeのtokenizerは同一SHA、LoRA本体は別SHA。

実`adapter_config.json`を参照すると`r=32`、`lora_alpha=64`、PEFT`0.21.2`、`q,k,v,o,gate,up,down_proj`、`task_type=CAUSAL_LM`。`base_model_name_or_path`はQwen3.8-27Bだが`revision=null`なので**実際の訓練時の親モデルcommitは不明**。別のQwen版に無断マージすることを禁じる。PI配布元には固有`LICENSE`ファイルがなく、HubのApache-2.0タグは本人のライセンス全文確認の代わりとしない。実行コードや未監査のインストールは今回実施しない。

## 3. NVIDIA 4B drafter：8ファイルのPublisher候補のみ

公式固定revision `bc5ad93d03d96a9c1ef49748e00ec5130a7080de`。8ファイル source総量 **8,431,580,958 byte**、うち`model.safetensors` **8,411,558,400 byte**（SHA256 `4838b4b88a345c7fdef6c7678617512e5ca5047647af45b15d3cf0531fadbe5a`）。NVIDIA 0.8B兄弟は1,524,849,984 byteだが、新規選定しない。

| ファイル | bytes | Hash種類 | Publisher Hash |
|---|---:|---|---|
| `.gitattributes` | 1,570 | git_blob_sha1 | `52373fe24473b1aa44333d318f578ae6bf04b49b` |
| `README.md` | 20,639 | git_blob_sha1 | `6c1aea2fc577fef359546a3c517d6e05ffb1104b` |
| `chat_template.jinja` | 7,756 | git_blob_sha1 | `a585dec894e63da457d9440ec6aa7caa16d20860` |
| `config.json` | 1,982 | git_blob_sha1 | `dd10c8861c78f375743329e693a48408db52e720` |
| `generation_config.json` | 164 | git_blob_sha1 | `6bc3495abf4617f1310ddce38eef88be858bafa5` |
| `model.safetensors` | 8,411,558,400 | publisher_lfs_sha256 | `4838b4b88a345c7fdef6c7678617512e5ca5047647af45b15d3cf0531fadbe5a` |
| `tokenizer.json` | 19,989,325 | publisher_lfs_sha256 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `tokenizer_config.json` | 1,122 | git_blob_sha1 | `3fc4fc36a1708482b6d7fe329b964f0e4396b07f` |

**作者評価**：16token draft block、SPEED-Benchで受理長は内蔵MTP 3.81（32k長文3.86）、NVIDIA 0.8B 3.92（長文3.60）、NVIDIA 4B 5.58（長文5.11）。**受理長≠tokens/s≠完全推論速度の改善率**。NVIDIAはGroq3 LPU向け設計でvLLM/SGLang/TRT-LLMロード可能と説明するが、所有者のPCで推論速度とRAMを測っていない。さらにDSpine 2.026Bが既存取得報告に存在する。**4Bを購入・ダウンロードする合理性は同じ実機で初めて判断できる**。

## 4. H/T/D/C/U・実装ゲート

| 記号 | 日本語の意味 | 単位（SI） | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `B_pi` | pi原本7ファイルの容量 | byte（情報量、非SI） | 657,633,248 | 全7ファイル、親Qwen原本を含まない | 整数スカラー |
| `B_4` | NVIDIA 4B全8ファイルの容量 | byte（情報量、非SI） | 8,431,580,958 | publisherの固定原本 | 整数スカラー |
| `P_4` | NVIDIA 4B総要素数 | 1（無次元） | 4,205,751,296 | Publisher Safetensors情報 | 整数スカラー |
| `P_{08}` | NVIDIA 0.8B総要素数 | 1（無次元） | 752,393,024 | Publisher Safetensors情報 | 整数スカラー |
| `A` | 1回の検証で受理されたtoken数 | token/verify step（比） | 平均受理長 | 同一設定SPEED-Bench内に限定 | 非負実数スカラー |
| `u_c` | 合成標準不確かさ | 測定量に依存 | 本人実機反復データ未収集 | 算定不能 | 実数スカラー/未推定 |
| `k` | 包含係数 | 1（無次元） | 不確かさの被覆指定 | 未設定 | 実数スカラー/未推定 |

**次元チェック**：source bytesの和はbyte、trained parameterは無次元の要素数。平均受理token/stepをtoken/sの速度へ直接置換できない。精度向上の作者報告は、PI harness思考OFF・1試行、SWE-bench Pro hard51で39.2%→64.7%（+25.5±14.2ポイント）、Terminal-Bench2.1 86件で39.5%→55.8%（+16.3±9.1ポイント）。作者が学習中に選んだstep160にはテストセットに関する選択バイアスが残る。

**H**：PI LoRAによる完全同条件pass@1向上5ポイント以上。NVIDIA 4Bは既存DSpine/MTPより総decode中央値10%以上向上（双方は**事前設定する仮説閾値**であって観測事実ではない）。

**T**：PIは未使用の最低100ペア課題、draftは100件の同一入力で比較。GPUモデル・クロック、OS/driver、backend ABI、model parent revision、zero-point/quant、KV/cache、context、batch=1を固定。中途で有利な結果だけを採用しない。

**D**：PASS＝事前登録した差分閾値と統計的支持＋全publisherハッシュ/権利/owner媒体検査が成立。FAIL＝有意な劣化、またはSHA不一致/無許可取得。UNCERTAIN＝信頼区間がゼロをまたぐ、ローカル実機未実施。現状は**sourceメタデータのみPASS、ダウンロードはSTOP**。

**C**：PIが別revisionの親では読み込めない、作者の選択済みテストで利益が過大推定、NVIDIA追加計算で内蔵MTPより遅くなる。

**U**：親checkpoint未固定、本人権利、実行コード、推論機器、作者ベンチの分散。独立の誤差モデル/反復分散がないため`u_c`、`k`は計算できない。

## 5. 関連分野とERROR CHECK

**機械学習**：PEFTで学習済みLoRAと量子化の違い。**アーカイブ科学**：URLだけでなく固定SHA・tokenizer・依存の保存。**情報法**：APIで公開と本人の正規許諾は別。**システム工学**：所有者4TB/200GB残床・CPU/GPU・実機clock/ABI評価。

**ERROR CHECK**：pi7ファイル657,633,248byte、4B8ファイル8,431,580,958byte、正確なrevision/重みSHA、親vs子tokenizer不一致、pi/opencode別学習重みをpublisher APIで確認。**GitHub正本v50の203登録/156有効は変更しない**。今回モデル取得0、削除0、承認0。実機Pythonテスト・本人Dドライブの独立SHA照合・オフライン復元は未実施。

**〈次に考える問い〉** 保存済み27B原本の同一性を確認できる場合、追加約0.658GBのpi LoRAと追加約8.432GBのNVIDIAドラフターのどちらが、利用者の同一環境で計測できる独立タスク成功率と推論効率をより大きく改善するか。
