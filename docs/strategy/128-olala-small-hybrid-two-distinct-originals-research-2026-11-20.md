# R128｜小型6.773B Olala hybridのBaseとSFT＋RL最終原本の実体監査（2026-11-20）

**基準はmain v54（207登録／160有効）**。2026-11-20の新規候補はOVHの完全に独立した2つの学習済み成果。正式採否を更新する場合はv55 overlayで一意に追加する。現時点の原本固定は[Publisher33ファイル・9LFS SHA](../../manifests/drafts/r128-2026-11-20-olala-mini-final-and-base-originals.candidate.json)。**本調査でモデル重量の取得、権利行為の本人承認、owner HDDアクセス、Python model実行、旧ファイル削除は行わない。**

## 1.〈本論〉公開元sourceの固定

| 原本 | 不変revision | 全sourceサイズ（byte） | LFS SHA256 | 研究採否 |
|---|---|---:|---:|---|
| [OVHaiLLM/Olala-v1.0-mini-7A1B](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B) | `b40f8165ee2254c18601220e19842600c6d91794` | 13,595,420,813（20件） | 6 | **CONDITIONAL推奨**：最終SFT＋RL |
| [OVHaiLLM/Olala-v1.0-mini-7A1B-base](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B-base) | `e88cbedb580bc58f6d7c50ab374fa339693a7a51` | 13,591,509,967（13件） | 3 | **CONDITIONAL推奨**：12.8T事前学習Base |

Publisher Hugging Faceの`?blobs=true`公式APIによりパス、整数byte、LFS SHA256、Git blob SHA1、source commitとgated状態を確認。両モデルはpublic、非Gated、Apache-2.0 LICENSEとNOTICEを持つ。メイン学習済み重みは共に13,579,677,592byte、しかし元BF16のSHA256は**最終：`99a208e1b45a4677ac1ce2eeaeb45150aa3c28aac173df3d22dc7985e9356442`**、**Base：`33dad784e7c2bd3828a8d22bc1e4e8b9dd0431ac30a57e19deb94097c99b5f83`**で異なる。学習済み状態の非一致は明瞭だが性能優位の証明ではない。`LICENSE`・`configuration_olala.py`・`modeling_olala.py`の3つはpublisher Git blob SHAが一致し、論理パスを維持しつつ内容アドレスで物理重複排除可能。

**同一モデルとして除外**：[GGUF量子化/BF16変換](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B-GGUF)と[MLX変換](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B-MLX)は別の学習成果ではない。[SFT中間モデル](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B-SFT)はさらに別学習済みSHAの原本だが、Baseと最終の対に13.592GBを追加する増分価値は未証明で研究HOLDとする。**Baseの拒否率・安全性が未検証である以上、「Base＝無検閲モデル」とは断言しない。**

## 2. 重み内部・実装前提と法的条件

作者の[公式モデルカード](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B)は、36層のMamba-3/Attention/256-expert MoE、約7層のKVキャッシュを要するattention、37言語（日本語を含む）、32K context、ツール使用を説明。HF本体serialized要素数は**6,773,124,144**（BF16 6,756,461,568＋F32 16,662,576）。出版社READMEはactive約1B、一方[OVH製品カタログ](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/olala-v1-0-mini-7a1b/)は1.5Bと記載し正確なactive数は**不一致**。total MoE expertsを減らして150B閾値を判定する誤りを禁止。

作者READMEは**stock Ollama/LM Studio/llama.cpp/vLLM/MLXでは未対応**とし、Publisher forkを指示。vLLM例はLinux、Python3.12、CUDA13/ドライバ580以上、24GB級NVIDIA GPU。すべて作者案内であり、利用者のWindows、CPU、VRAM、backend/clock/batch/contextにおける動作・速度実測ではない。`config.json`の`auto_map`は`configuration_olala.py`と`modeling_olala.py`に依存し、配布元コードの任意実行・pickleロードは別の供給網審査まで禁止。重み以外の学習済み依存は完全閉包未検証。

権利は配布元のApache-2.0 LICENSEを基本とし、NOTICEには原作者OVHおよび上流Qwen tokenizer帰属を要求。最終repoにはEU AI Act Art53対応の学習内容公開文書を同梱。**事実**は現時点のpublic ungatedと文書が存在すること。将来のGated化・削除・一般規制はストレス仮説にすぎない。個別ライセンスの予定使用行為への許諾、フォークruntime権利、同梱NOTICEとexport条件は別に審査する。

## 3. 他の取得候補と優先度

現行GitHub実行台帳には61件VERIFIED／708ファイル／409,835,119,252byteの取得一致が**報告**される。ただしOwner Dをこの研究環境から独立再ハッシュしておらず、現在の個別原本が全て存在するとは言い切れない。先に既取得の不足ファイル（RWKV7推論コード、iLLaDA modeling、ACE-Step silence latent、TRELLIS meta）を[R125](../../queues/proposed-v52-r125-post61-gap66plus-2026-11-20.json)で照合し、モデル重み全量を二重転送しない。既存の無検閲Interpretic/0bserverx原本は維持し、Olalaを無検閲原本の代用とみなさない。

実行承認条件：各repo・40桁source SHA・全ファイルhash/bytes、LICENSE用途、owner HDD現在空きとcache/staging・200GB安全床、backend ABI/zero-point/KV、依存closure、完全offline復元可能性、個別の明示承認。`queues/approved.json`が空ならダウンローダーには投入しない。

## 4. 変数表・容量算術と次元

| 記号 | 意味 | 単位（SI/備考） | 定義 | 前提と範囲 | 型 |
|---|---|---|---|---|---|
| `S_f` | 最終版publisher原本 | byte | 13,595,420,813 | full repo、実増分ではない | 非負整数 |
| `S_b` | Base publisher原本 | byte | 13,591,509,967 | full repo、実増分ではない | 非負整数 |
| `P` | 最大重み単独ファイル | byte | 13,579,677,592 | 2つとも同byte | 非負整数 |
| `F` | 最低残すowner物理空き | byte | 200,000,000,000 | 方針上の必要条件 | 非負整数 |
| `H` | 全量新規の仮定下の最低空き参考値 | byte | `S_f+S_b+2P+F` | 外部依存・OS領域別 | 非負整数 |

`H=13,595,420,813+13,591,509,967+2×13,579,677,592+200,000,000,000=254,346,285,964 byte`。各項byte、単位整合**PASS**。これは**ownerの現在空き容量が254GBある**という証拠ではない。なお2つを同時に転送する必要はなく、各独立原本ごとに一時領域を確保できる。

## 5. H/T/D/C/UとERROR CHECK

**H**：最終後学習と生の事前学習を同じアーキテクチャで残すことで、指示追従能力と独立訓練基盤の両方を将来再現できる。**T**：publisher固定33fileメタデータ全件、別重みSHA（n_min=2）を確認済み。実際の価値検証は30件以上の日本語・英語・coding・tool課題を同GPU/CPU・driver・clock・backend/ABI・context・batch1・量子化/zero-pointで対比較する。**D**：メタデータ一意・重みSHA差＝PASS_METADATA。本人権利・D実SHA・ソフト復元＝UNCERTAIN。未許可転送、Gated迂回、危険なコードの自動実行＝FAIL。**C**：Baseが既保有モデルに性能/学習可能性で劣る、出版社専用forkが維持されない、RL版の業務性能改善が確認できない場合。**U**：作者のactive数表記不整合、owner実機、LICENSEの目的別行為、モデル依存と再現テストが主要。合成標準不確かさ`u_c`と包含係数`k`は測定分布不足で数値化しない。

**ERROR CHECK**：公式原本2repo、33ファイル／9publisher LFS SHA／27,186,930,780byte。新規重量DL0、未審査実行0、承認0、owner HHD独立測定0。v54既存選定207件は本R128調査文書のみでは変更しない。注意：v54 CURRENT expectedの150B未満PASS158はv54 materialized実数PASS157（157＋2超過＋22不明＝181モデル）と一致せず、正本訂正が必要。

関連分野：状態空間モデル・MoE効率化、転移学習とアラインメント、供給網コード検証、長期デジタル保全と内容ハッシュ、著作権と輸出管理。

## 6.〈次に考える問い〉

**Baseと最終RLを両方残す増分価値を、同条件30件の推論評価と将来の再学習可能性でどのように実証できるか。**
