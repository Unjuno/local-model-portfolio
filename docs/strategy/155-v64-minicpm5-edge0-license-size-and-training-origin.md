# R155／v64 — 2026-11-22：MiniCPM5-2B原本確定とEdge0独自NVFP4の正確な保存コスト

## 1. 監査の位置と結論

対象は **Unjuno/local-model-portfolio の main／v64-20261122**。`catalog/CURRENT.json` の **236登録／189有効（SELECT55、CONDITIONAL134）**を変更しない。取得実行台帳は **112モデルVERIFIED／1,714ファイル／2,020,548,143,087byte**を報告するが、今回所有者Windows Dの実ファイルを再ハッシュ・オフライン復元した証明ではない。

**今回確認した新しい学習済みソース**：

| 配布元の原本 | 40桁固定commit | Publisherファイル／バイト | 調査採否 |
|---|---|---:|---|
| [openbmb/MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B) | `42433e90dad95123ab87729fd7011e7110629556` | **11件／5,043,807,977byte** | **CONDITIONAL追加を推奨する原本source確定**。権利・HW実測・承認は未了 |
| [Edge0/Edge0-120B-NVFP4](https://huggingface.co/Edge0/Edge0-120B-NVFP4) | `b0628ee6f3655c40a1afde343d6e265387eea094` | **43件／98,531,583,107byte** | 学習済み潜在MoE・優先研究HOLD |
| [Edge0/Edge0-145B-NVFP4](https://huggingface.co/Edge0/Edge0-145B-NVFP4) | `f7a465395af029f3f59a624caefb0fc273988faa` | **43件／113,772,093,975byte** | 高性能別潜在MoE・優先研究HOLD。120Bから自動置換・二重取得しない |

3配布元のPublisher immutableファイルツリー、サイズ、Git blob OID、LFS SHA-256の静的出典を [`R155 source manifest`](../../manifests/drafts/r155-2026-11-22-minicpm5-edge0-immutable-sources.candidate.json) に固定した。ファイル本体・モデル重み・gated資料を1バイトも取得せず、コードを実行していない。これは**候補の静的ソース同定**であって、ユーザー所有の取得許諾またはダウンロード許可ではない。

## 2. MiniCPM5-2Bを追加候補にする理由

Publisherの[`README`](https://huggingface.co/openbmb/MiniCPM5-2B)と公式Hub safetensorsメタ情報は、2,516,756,480学習要素、42層のLlama系構造、131,072トークン文脈長を示す。原本重みはBF16 single shard `model-00000-of-00001.safetensors`（**5,033,557,096byte**）。その他tokenizerとチャットテンプレート、model indexを含む固定11ファイルの元ソース**5,043,807,977byte**を保存の審査単位とする。量子化版は同一学習状態の実装形式で、別資産として数えない。

作者の総合指標**53.9点**は自己定義された複数ベンチマーク平均であり、所有者実機や既存ポートフォリオ代表モデルとの同条件比較ではない。独立したagent・数学・コード・長文のコンパクトな後学習原本として価値があるが、「他の2B以下より確実に強い」とは断定しない。MiniCPM5-1B（約1.081B／Publisher約2.171GB）も別学習原本だが、同族2.5B版と取得価値が重なるため、現在は追加優先度を低くする。

**権利と復元ゲート**：モデルカードはApache-2.0タグだが、固定11ファイルツリーには独立した`LICENSE`がない。上流コード・モデルの完全な使用条件、UltraData等の学習データ系譜、使用者の目的に応じた許諾は未確認。`LlamaForCausalLM`をサポートするTransformers/llama.cpp等とテンプレートのバージョン、131k KVキャッシュを含むRAM、Win/Linuxでの実際の復元成功も未検証。現物HDDの空きと200GB下限を確認する前にダウンロードしない。

## 3. Edge0：モデルの「コンパクト重み」数値と保存セットを混同しない

PublisherはQwen3.8-Flash-Nextを基にしたlatent sparse MoEへの**構造変更と追加学習**、NVFP4のネイティブ重みを説明する。単純な量子化形式変更と同一視しない。一方、完全なトレーニング起点commitや、現在の学習済みPLE、MTP、Encoderを含む**総パラメータ数の第三者tensor censusは存在しない**。120B/145Bというモデル名だけで150B以下の全学習要素PASSにしてはならない。

特に現行の不変配布リビジョンでは、**`ple-fp8.gguf`が51,200,246,112byte**。この巨大なファイルは両者の`model.json`の標準実行構成に参照され、**Publisher SHA-256で同じ実体**。単体の「120B=32.96GiB」「145B=47.79GiB」という宣伝値は、全Publisherスナップショットや完全な推論依存の保存量ではない。145Bの`experts.bin`だけで47,563,800,576byte、120Bは33,974,255,616byteである。ほかにskeleton GGUF、潜在dense表、MTP head、tokenizer、モデル専用LICENSE/NOTICEとエンジンソースが必要。

### 同一SHAを用いる容量重複排除（静的上限）

同一パス・同一byte数・同一LFS SHA-256／Git OIDの**27ファイル／60,467,010,496byte**が120Bと145Bで一致。これらのPublisher sourceが所有者HDDで実際に存在するか、パスを跨いで再利用できるかは未確認。

| 変数 | 意味 | 単位（SI互換） | 定義 | 範囲／型 |
|---|---|---|---|---|
| \(B_{120}\) | 120B原本のPublisher全ファイル容量 | B（バイト、十進） | 固定revの全ファイル合計 | 非負整数／スカラー |
| \(B_{145}\) | 145B原本のPublisher全ファイル容量 | B（バイト、十進） | 固定revの全ファイル合計 | 非負整数／スカラー |
| \(B_{\mathrm{shared}}\) | 同一Publisherハッシュで再利用可能な参照容量 | B（バイト、十進） | 27一致ファイルの合計 | 非負整数／スカラー、実HDD存在未検証 |
| \(B_{\mathrm{union}}\) | 両原本の完全な一意ファイル集合の理論容量 | B（バイト、十進） | 計算式の値 | 非負整数／スカラー、実占有を示さない |

\[
B_{\mathrm{union}}=B_{120}+B_{145}-B_{\mathrm{shared}}
\]

Publisher固定出典に代入：**98,531,583,107 + 113,772,093,975 − 60,467,010,496 = 151,836,666,586byte**（約151.84GB、十進）。**単位検査**：B+B−B=Bで一致。この値は理想的なハッシュ重複排除の**Publisher参照容量**であり、owner物理占有やstaging・キャッシュ・追加エンジンの保証ではない。

### ライセンスとモデル実行条件

- [固定Edge0ライセンス](https://huggingface.co/Edge0/Edge0-145B-NVFP4/blob/f7a465395af029f3f59a624caefb0fc273988faa/LICENSE)は**Edge0 Community Model License 1.0**。個人研究、改変、非商用共有等に広範な許諾を与えるが、モデル販売や第三者向け推論モデルサービス、独立した商用coding/office assistant提供にはEdge0側の別書面ライセンスが必要な場合がある。
- [固定Qwenライセンス参照](https://huggingface.co/Edge0/Edge0-145B-NVFP4/blob/f7a465395af029f3f59a624caefb0fc273988faa/third-party/Qwen-LICENSE.txt)は**Qwen Community License 1.0**。Model-as-a-ServiceとAI Work Assistantの商用条件は、Edge0の許諾とは**別**に適用される。READMEのソースコード（Apache/MIT等）からモデル本体の権利を推論しない。実際のQwen学習親revisionはリリース記録でも未確認。
- `edge0-infer` / `edge0-strata`、NVFP4 CUDA13、必要なGPU/CPU/ホストRAM/SSD streaming、`model.json`のcontext・KV int8・MTPのABIが未検証。PublisherはRTX 5090 D 24GB上で145B NVFP4のagent decode **98.3 token/s**、VRAM **23.25GiB**＋ホスト **38.27GiB**を主張するが、クロック固定・driver・バッチ・長文KV・追加キャッシュ・第三者反復測定の条件はここで揃わない。最高スループットの広告値をowner環境の性能保証にしない。

**結論**：150B以下の通常モデルとして即承認しない。PLEとMTPを含む学習済み総数、必要ソース、本人ライセンスの許諾、同一条件の30回以上のピークメモリと速度比較を揃えてから量子化例外も含む審査へ進める。120Bは小型・高速基準候補、145Bは品質上限候補。両方を無条件に二重取得しない。

## 4. 高リスクであるが今は保存候補に追加しないモデル

[briaai/RMBG-3.0](https://huggingface.co/briaai/RMBG-3.0)はFibo系8Bの画像のalpha matte抽出・背景除去に特化した別学習状態で、画像編集の産業代替価値がある。ただしHubは**Gated(auto)**、モデルカードは非商用限定ライセンスを案内しており、公開APIでGated重量SHAはマスクされる。**権限がないまま重みハッシュを推測・取得したりGatedの条件を迂回したりしない**。本人利用権、配布権、静的原本hash、完全復元可否を確認するまで**HOLD**。

`qvac/BotPsy-0.8B`と`robbyant/lingbot-touch-tiny`は、既存v64で選定済みかつ今回の112件VERIFIED報告に存在する。同一repo IDで追加採用・二重取得しない。

## 5. テストプロトコル（H／T／D／C／U）とERROR CHECK

- **H**：MiniCPM5-2Bは5.044GBで独立する有用なagent/長文性能を持ち、Edge0の120Bと145Bは通常のQwen重量量子化と異なる追加学習済み構造を持つ。原本の完全なソース同定と非冗長選択をすれば保存済み能力の冗長性を抑えられる。
- **T**：HFの固定40桁commitで全モデルのファイルパス／byte／Git blob SHA-1／LFS SHA-256を静的検証。現行236登録・112取得報告に同一IDが存在しないことを確認。所有者が対象ドライブを読取専用で再SHAした後、同条件HW/driver/backend commit/precision/context/batchで各モデル**30回以上**反復し、少なくとも100件の固定・非訓練agent/コード課題で比較。RAMには重み、OS、推論器、KV、encoder/PLE/MTP、stagingを含める。
- **D**：Sourceが**11＋43＋43ファイル**、それぞれ上記bytes・SHA参照1/13/14、Edge0共通27件／60,467,010,496byte、現行235でなく**236/189**、112報告との重複0、承認キュー0なら静的**PASS**。取得許可や総パラメータを測定済みと誤認すれば**FAIL**。本人使用権、量子化実機ピークRAM、バックエンドABI、性能差は未実測のため**UNCERTAIN**。
- **C**：Edge0作者ベンチが実機で再現しない、PLE等の依存が欠損する、親の許諾が用途に適用されない、MiniCPM5-2Bが既存コンパクトモデルと能力重複している場合は選定価値が低下する。
- **U**：最も大きい不確かさは所有者HDD、作者の性能評価、モデル権利、総学習要素、custom engine ABI。反復測定・分散が無いので合成標準不確かさ\(u_c\)および包含係数\(k\)は計算できない。架空の精度や速度を作らない。

**ERROR CHECK**：R155新規の静的マニフェストはPublisher APIの固定ソース（3モデル97ファイル）のみを対象。モデル重み取得0、Gated回避0、カタログ有効件数変更0、`queues/approved.json`変更0、owner Windows D変更0。完全なruntimeと法的適用は未確認。無断でライセンス承認を合成しない。

関連分野：①パラメータ効率の良い機械学習と学習表現、②GPU／SSDハードウェア性能工学、③内容アドレス型の供給網・データ保全、④モデルの権利管理と流通規制。
