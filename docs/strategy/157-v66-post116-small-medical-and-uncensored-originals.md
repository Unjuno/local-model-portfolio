# R157／v66（2026-11-24）—最新116取得報告を正式照合、無検閲DPOと医療マルチモーダルの独立原本を採否確定

## 1. 正本と対象
前の正本v65は**240資産／192有効（SELECT56、CONDITIONAL136、HOLD29）**。取得台帳`catalog/execution/2026-11-19-acquisition-ledger.json`の最新報告は **116モデルVERIFIED／1,758ファイル／2,021,784,002,725byte**。名前と版を逐一比較すると、未登録の取得報告は次の3repoのみ：
- [Datadog/Toto-2.0-4m](https://huggingface.co/Datadog/Toto-2.0-4m/tree/8306a9801cf98c0f5ffe4b2dcc8f496e616d84d9) 7files・17,727,464byte、4,144,448 F32要素、Apache2。Datadogの独立観測時系列Transformer。作者のBOOM MASE0.624／GIFT-Eval MASE0.757。単独実機評価ではない。
- [inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0/tree/51582cc8487ab0e0f48d866bfc0124afbaf6562a) 7files・66,946,541byte、16,708,352 F32要素、MIT。128Hz生体信号の独立学習済みエンコーダ、学習済みの診断ヘッドではない。channels.npzと本人情報保護、別PythonパッケージのABIが必要。
- [ostris/primal_vae](https://huggingface.co/ostris/primal_vae/tree/dc3e96c879e8cf4247c9474c3109bc2847099b50) 14files・1,145,019,884byte、Apache2。2x1/2x2/4x1の**3個の異なる学習済みF32重み**の合計1,132,129,000byte。1モデルリポジトリの中に3成果があり、変換クローンとして二重登録しない。作者のPSNR比較は3枚の画像のみで、実務品質の証明ではない。custom `modeling_primal_vae.py` と3個の学習済み総tensor censusは未検証。

これらは116取得台帳の正確なrepo ID・40桁SHA・全ファイル数／整数byteと一致するため、**新規転送無しのCONDITIONAL登録**。

## 2. 既存の無検閲成果との比較
[abacusai/Smaug-Uncensored](https://huggingface.co/abacusai/Smaug-Uncensored/tree/e4bbcf7aec54ab72f4ce720569f3b3dc7b973087)は公式Qwen3.8-27Bの独立DPO+NLL重み。32files・55,586,070,091byte、18重量シャード中、公式QwenとSHA一致2件 **5,934,994,296byte**、異なる16件 **49,628,012,480byte**（[Publisher比較マニフェスト](manifests/drafts/r157-2026-11-24-post116-five-originals-medical-moe.candidate.json)）。モデル名だけの「無検閲」ではなく、**別学習済み状態**としてCONDITIONAL採用。ただしDPO adapterの可逆復元未証明、作者OR-Bench-Hardの過剰拒否45.2→2.3%（n=1309）は独立測定ではなく、一般回答品質向上の証拠でもない。既存の別Heretic/Abliteration/GGUFとのモデル系譜も保持。

## 3. 医療マルチモーダル先端2モデル
- [inclusionAI/LingSante-3.1-air-VL](https://huggingface.co/inclusionAI/LingSante-3.1-air-VL/tree/1f398c937d6069994a156689636832c47d8c09be)：**124,848,460,496総格納要素**（約124.85B）、5.5B activeとされる医療画像+テキストの別学習済みMoE。75 tree entriesからディレクトリを除いた**完全74files・249,721,924,398byte／モデル50 shard**を固定。MITタグ。256K文脈、出版社実行例は4×141GB GPU、patched SGLang/vLLM、remote codeなどが必要。**条件付きアーカイブ選定のみ**。医療機器ではなく診断・処方を自律実行しない。臨床性能も個人の実機RAM/GPUも未検証。
- [inclusionAI/LingSante-3.1-flash-MXFP4](https://huggingface.co/inclusionAI/LingSante-3.1-flash-MXFP4/tree/56229393c30374608ce101f14fa2483b51c2229c)：正式**HOLD**。オリジナルの学習済みモデルは**560B総パラメータ**で、MXFP4はRTNの**学習なし量子化**。HF Safetensorsメタデータの格納要素294,289,983,808を元モデルの総パラメータ数と誤認しない。Publisherモデルカードのファイル総量313,230,131,991byteは参考値、174filesの完全な個別source scopeは未固定。既存の150B未満参考モデルとの同HW/backend/context/batchにおける**少なくとも30回のピークRAM<=参考モデル、両方<512GB**という例外条件を満たしていないため、最終取得に進めない。

## 4. 容量・独立した停止条件

[本研究で固定した5配布元・134個の公開元ファイル、合計306,537,688,378byte](manifests/drafts/r157-2026-11-24-post116-five-originals-medical-moe.candidate.json)は、**既取得済み3repoの容量＋新しい2repoの完全ファイル参照量**。所有者ドライブの新規取得サイズ・実残容量ではない。LingSante Flash HOLDはこの合計に含まない。配布元SHA・サイズはOwner現物SHAを検証したものではない。

現在のポートフォリオ規則は4,000,000,000,000byteの最大選定予算、空き200,000,000,000byte以上維持、ピーク実行RAM<512GB（十進）、150B超は参考モデルとの同一条件実測例外が必須。歴史的な取得側の最少空き約1.022TBは**現在の実ディスク空き値ではない**。キャッシュとstaging、本人許諾、Gated個別権限、第三者ライセンス、コード・tokenizer/codec ABI、SHAと完全オフライン復元、明示されたファイル別ユーザー取得承認が完了しない限り新たな重みをダウンロードしない。

2026-11-19の[米BIS 91 FR 74970 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)はモデルウェイトECCN4E091を撤廃。全open weightsの近日禁止を断定しない。公開終了・規制危険性は仮説として保存の優先づけにのみ使用し、適法性を上書きしない。

## 5. H・T・D・C・Uと関連分野

| 項目 | 判定方法 |
| --- | --- |
| **H** | 116取得報告の未登録3原本を重複取得無しに登録し、SmaugとLingSante-airの新規学習成果をアーカイブ候補へ、560B MXFP4は例外証拠が無いのでHOLD |
| **T** | IDで116全件照合、旧240行不変、5Publisherの134ファイルSHA/byte、197有効のqueue/prep/readinessと141条件付きaccessの同一ID集合、approved0。ユーザー実機性能はHW/driver/backend/context/batch/quant zero-pointを固定し最低30反復、事前評価セットで中央値と95%CIを報告 |
| **D** | Publisherメタデータ・選定正本が一致：**PASS**。本人実媒体/実行/許諾は **UNCERTAIN→STOP**。自動承認・未審査custom codeの実行・フル原本重複転送は **FAIL** |
| **C** | Smaugが中立品質を損なう、Toto/Primalの差別化が実測で成立しない、医療VLMのcustom ABIが不一致、量子化RAMや権利が成立しない |
| **U** | 外部Publisher SHAとowner現物SHA、サンプル数が限られた作者評価、体験装置/HWの未知。測定系列がないため合成標準不確かさu_c・包含係数kは数値化不可 |

変数表（この監査の量を表す記号）：

| 記号 | 意味 | 単位 | 定義 | 範囲・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `B_source` | 5配布元の公開ソース総容量 | byte（B） | Publisher全ファイルサイズの合計 | 非負整数、Owner追加量ではない | 整数スカラー |
| `B_owner` | 実際の追加保存量 | byte（B） | ローカルSHA再利用後の新規占有量 | 未測定、≥0 | 整数スカラー |
| `M_peak` | 実機推論時のRAM・VRAMピーク | byte（B） | OS・KV・実装・依存含む、共有メモリ二重加算なし | 未測定、<512GBが必須 | 実数スカラー |
| `n` | 同条件の独立評価回数 | 1（無次元） | 事前固定された評価反復数 | 最低30、性能試験未実施 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 測定対象と同単位 | 各独立誤差源を適切に合成 | 分散不明・未算定 | 非負実数 |
| `k` | 包含係数 | 1（無次元） | 不確かさの拡大係数 | 被覆率と分布仮定未定 | 正実数 |

次元チェック：容量の集計はすべて**十進byte**で一致させる。TB/TiB混同と量子化ファイルサイズをピークRAMとみなす誤りを禁止する。

学際性は①機械学習/DPO・蒸留、②時系列統計と医療信号、③画像圧縮とVAE、④ソフトウェア供給網と暗号学的ハッシュ、⑤知財・輸出管理、⑥GPUのMoE実行特性。

**ERROR CHECK**：正式選定変更後は旧240件を不変とし、正本246件・有効197、モデル総220・データ26、SELECT56、CONDITIONAL141、HOLD30、全116取得報告IDを包含、承認0を確認する。テストソースを追加するが、実モデルの第三者コード・重み・Ownerディスクを本研究では実行または変更しない。

