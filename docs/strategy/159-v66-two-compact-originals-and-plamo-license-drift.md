# R159／v66：新しい小型視覚モデル・2.5B汎用原本の選定、PLaMoライセンスrevision差分とERNIE 280B例外HOLD（2026-11-24）

## 1.〈本論〉監査前提と決定

唯一の正本は [catalog/CURRENT.json](../../catalog/CURRENT.json) の **v66（246登録／197有効、SELECT56／CONDITIONAL141）**。最新の[取得側実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は116モデル・1,758ファイル・2,021,784,002,725byteをVERIFIEDと**報告**する。所有者Windows Dドライブのこのセッションによる独立SHA、本人の具体的利用行為許諾、完全オフライン再生試験の完了は証明していない。

**今回の研究決定：新しい独立2原本を次期CONDITIONAL正式採用の先頭候補に固定し、既存モデルの二重登録を防止する。取得承認ではない。**

- [固定Publisher6repo全229file・Git blob OID／LFS SHA256・整数bytesとPLaMo新旧比較](../../manifests/drafts/r159-2026-11-24-wemm-ecom-plamo-ernie-immutable-sources.candidate.json)
- [2新規原本＋3HOLD＋既選定revision監査の非実行キュー](../../queues/proposed-v66-r159-post116-edge-UNAPPROVED.json)
- [構造化採否・2026規制と停止条件](../../catalog/decisions/2026-11-24-r159-compact-models-plamo-drift-and-ernie-hold.json)
- [現行R158・既存Smaug無検閲／LingSante医療VLMの研究順位](../../queues/proposed-v66-r158-post116-prioritized-UNAPPROVED.json)

今回のモデル本体の新規取得は**0byte**、`queues/approved.json`は**0件**、旧236/246学習資産を削除・交換せず、第三者モデルコード・学習済みpickle・実行形式の実行なし。現在の正本v66は一切昇格しない。

| 固定公開元原本 | 固定40文字commit | 完全Publisher参照source | 判定 |
|---|---|---:|---|
| [tencent/WeMM-Ecom-0.8B](https://huggingface.co/tencent/WeMM-Ecom-0.8B) | `b40297975d72386f1c53103371d80ae0e5a9bd58` | **20files・1,733,044,450byte** | **最優先・条件付き採用を推薦**。EC業務の独立追加訓練済み視覚言語0.853B原本 |
| [openbmb/MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B) | `42433e90dad95123ab87729fd7011e7110629556` | **11files・5,043,807,977byte** | **条件付き採用を推薦**。約2.517BのRL/OPD思考・コード・agent別学習成果 |
| [pfnet/plamo-3-translate-0.8b](https://huggingface.co/pfnet/plamo-3-translate-0.8b) | `c5a33c561bc6a4fbac38c3460bbb384e15c0b231` | 16files・1,785,590,177byte | **すでにv24から選定済み／別資産追加禁止**。法的条件とchat templateのrevision差分をレビュー |
| [tencent/WeMM-Ecom-2B](https://huggingface.co/tencent/WeMM-Ecom-2B) | `6ae63ecd178805abb367b489ce2c9723b5ba2a23` | 22files・4,453,620,451byte | **研究HOLD**：0.8Bとは別訓練結果だが、同じEC用途の品質差とHW費用を未評価 |
| [pfnet/plamo-3-translate-2b](https://huggingface.co/pfnet/plamo-3-translate-2b) | `1df825232e862b1e338c24f46be51921d415d787` | 18files・5,762,122,137byte | **研究HOLD**：PLaMo0.8Bと31B教師の間の別学習成果。効果・追加価値未測定 |
| [baidu/ERNIE-5.5-Flash-Preview](https://huggingface.co/baidu/ERNIE-5.5-Flash-Preview) | `ace1100dcde7bf4eb06add6ae11ce4f43a11ddfe` | **142files・165,935,900,630byte** | **150B超例外審査HOLD**。280B総数14B activeのMoE+DSpark頭、実行ピーク未実測 |

上記6repo合計**229files／184,714,085,822byte・LFS SHA256参照159件**は論理的な出版社全原本参照量であり、実行計画・所有者媒体占有・必要な新規ダウンロード量を表さない。今回の**新規推薦2repo／31file／6,776,852,427byte**も同じ定義である。

## 2. 新2原本を選定する固有の理由と限界

### WeMM-Ecom-0.8B：同じ親でも別訓練済み状態

[作者モデルカード](https://huggingface.co/tencent/WeMM-Ecom-0.8B)／[原論文 arXiv:2611.30662](https://arxiv.org/abs/2611.30662)。Qwen3.5-0.8Bから、ECを含むマルチモーダル継続事前学習とhybrid-thinkingのposttrainingを施した**別結果**。静止画像・複数画像・動画/テキストの製品属性、文字、領域、商品比較や検索関連タスクに意味がある。既存台帳のQwen3.5-0.8B親・WeMM-Video-2B（音声＋映像）と役割が異なる。エンコーダが内包されているかと全必要依存を実機で確認し、**EC理解＝音声付き動画理解と同一機能**とはしない。

出版社はEC28ベンチのうち**23が社内評価**、一般64ベンチと自己比較する。0.8BのEC平均が親Qwen3.5-0.8Bより+16.43ポイント、一般+6.93ポイントとの**作者値**は、独立同一HWの性能保証でない。モデル重みはBF16 `model.safetensors` **1,706,030,496byte**、SHA256 `5a84c44f4e3beaf16ab0b6aa8238c66a6033291d77b13b81d934098a02d68bf4`。Publisher全20ファイルにApache-2.0のLICENSE、tokenizer、vision前処理、`chat_template.jinja`と評価図が含まれる。BF16を原本として選び、GGUF/FP8/GPTQを新学習モデルと数えない。

**実装前提**：作者はPython3.11例、`transformers>=5.2.0`、PyTorch+torchvision、BF16、`AutoModelForImageTextToText`、`AutoProcessor`。動画経路はTorchCodecと互換FFmpegの独立検証が必要。262,144トークン文脈はモデルの公称値であり、所有者GPUでのVRAM適合や最大長応答は未確認。GPU/CPU、クロック、バッチ、KV、backend commit、画像入力サイズ、量子化・zero-pointを固定して比較する。

### MiniCPM5-2B：一般モデルでも小容量への知識圧縮という固有成果

[作者カード](https://huggingface.co/openbmb/MiniCPM5-2B)／[R155先行原本研究](155-v64-minicpm5-edge0-license-size-and-training-origin.md)。BF16 `model-00000-of-00001.safetensors` **5,033,557,096byte**、SHA256 `14fb8e7f0a18d53d1f239773758bf581cee7e456a4523a54622c3a245b64402c`。原論文／作者の技術説明は、SFT・領域別RL教師からOPDで能力を統合した学習状態という独自性を示す。単純にQwenやAionを4bit量子化したものではない。

作者は複数のコード/長文/agentベンチの平均「53.9」を公開するが、複数ベンチと推論設定が混在し、所有者の実機における有用性を証明しない。**本repoは11件で独立`LICENSE`を含まない**。HFタグ`license:apache-2.0`だけから、モデル全体・訓練元・実行コード・再配布の本人利用権を自動PASSにしない。正式採用の前に別の一次LICENSE参照を確定する。Llama系backend、tokenizer/template、contextとKVの整合を検証する。

## 3. PLaMo旧選定の重量一切変更無し・ライセンス改訂の監査

既存正式選定は[2026-11-06 v24](../../catalog/revisions/v24-2026-11-06.json)の `pfnet/plamo-3-translate-0.8b`、固定版 `cc8e88169807d5a272e8ff06db12eb0129b67f81`（16files・1,785,576,024byte）。新しく観測された現行版 `c5a33c561bc6a4fbac38c3460bbb384e15c0b231`（16files・1,785,590,177byte）を全path/byte/Git OID/LFS SHAで差分化した。

**訓練済み `model.safetensors` のSHA256 `7c9f0066d166c075bdbe83ada3d444e08bd7a6ee3f345f47a1f3c442aa6898c5` は新旧で同一**。違うのは以下の5非重みファイルのみ。

| 変更ファイル | 旧byte | 新byte | 解釈 |
|---|---:|---:|---|
| `LICENSE/en` | 7,629 | 14,585 | 利用許諾が大幅に増補、行為別再審査 |
| `LICENSE/ja` | 8,720 | 15,669 | 同上、日本語版 |
| `README.md` | 39,615 | 39,639 | 説明更新 |
| `README_ja.md` | 41,614 | 41,638 | 説明更新 |
| `chat_template.jinja` | 5,206 | 5,406 | 推論挙動やプロンプト構成の差を要検証 |

**厳密差+14,153byte**。重みが同じでもテンプレートが変われば出力同値とは限らない。旧固定選定の重みを黙って置換・再取得せず、必要時に両revisionの非重みメタデータを区別する。

現在の[英文ライセンス原本](https://huggingface.co/pfnet/plamo-3-translate-0.8b/blob/c5a33c561bc6a4fbac38c3460bbb384e15c0b231/LICENSE/en)は**2026-11-17改訂**を記載。非商用・学術/個人の利用、前年度の売上1,000,000,000円以下の法人等の商用事前登録、超過時の別ライセンス、モデルの第三者提供の帰属、出力で訓練した派生モデル、終了時のコピー削除条件などを区別する。**法律・契約が過去保存へどのように適用されるかの結論は未確定**。本人が何の行為をするかを先に分類してレビューする。PLaMo0.8Bはすでに正式選定済みであり、当該原本の再登録・全重みの追加取得を禁止。

2Bは別の2.879B学習結果だが、旧選定0.8B・31B教師との相対品質/速度/費用が揃うまで研究HOLD（量子化版とは扱わない）。

## 4. ERNIE Preview：配布サイズの小ささとパラメータ総数を混同しない

[2026-11-24公式公開モデル](https://huggingface.co/baidu/ERNIE-5.5-Flash-Preview)は作者による**280B total/14B active**の別ポストトレーニングMoE、1Mコンテキスト、混合FP8・MXFP4 expertの量子化対応学習およびDSpark投機復号ヘッドを持つ。Hub APIの`safetensors.total=299,559,241,286`はシリアライズ表現を含んだ値であり、メーカーの公称論理総数と同じ定義であると証明されていない。

出版社の固定コミット上**142ファイル／165,935,900,630byte・133 LFS SHA参照**を収録元として静的固定。しかし、150B基準を超えるので即時の取得承認は不可。**例外審査**にはあらかじめ150B未満の比較モデルを固定し、同じHW/clock/backend/quantization/zero-point、batch、contextで**30以上の実測ピークRAM**が候補≦基準、両者とも十進512GB未満であること、実用品質/速度、全依存閉包が必要。現実にはOwner Windows D・GPU・backendが未確認なので **HOLD**。元のERNIE BaseやBF16/FP8別repoを重複対象に加えない。

## 5. 容量・変数表・次元チェック

| 記号 | 意味（日本語） | SI/情報単位 | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `B_W` | WeMM-Ecom0.8原本 | byte（B） | 1,733,044,450 | 20Publisherファイル全scope | 非負整数スカラー |
| `B_M` | MiniCPM5-2B原本 | byte（B） | 5,043,807,977 | 11Publisherファイル全scope | 非負整数スカラー |
| `B_two` | 今回推薦2原本の論理合計 | byte（B） | `B_W+B_M` | owner増分の実測ではない | 非負整数スカラー |
| `D_free` | 所有者の現在空き容量 | byte（B） | null、未実測 | 0以上・現在値が必要 | 非負整数又はnull |
| `F_min` | 処理中安全床 | byte（B） | 200,000,000,000 | staging/cacheは別途 | 非負整数スカラー |
| `M_cand` | 候補の推論時ピーク（OS/GPU/CPU/KV/codec込み） | byte（B） | 未測定 | 実行HW/ABIによる | 非負実数スカラー又はnull |
| `M_ref` | 150B未満固定比較モデルの推論時ピーク | byte（B） | 未測定 | 同条件 | 非負実数スカラー又はnull |
| `n` | 独立測定数 | 1（無次元） | 性能/ピーク測定の反復回数 | 事前設定、少なくとも30 | 非負整数スカラー |

`B_two = 1,733,044,450 + 5,043,807,977 = 6,776,852,427byte`（十進約6.777GB）。`M_cand`と`M_ref`を比較するには同じ測定条件が必要。**次元チェック**：B同士／M同士はともにbyteなので比較可能。パラメータ数は個数（1）、ディスクbyteやピークRAMとの同一視は禁止。現在の`D_free`とstagingピークがnullのため、保存枠4TBと歴史的約2.022TBだけで新規取得GOとはしない。

6repoのPublisherモデル間ではWeMM0.8B/2Bの`tokenizer.json`、PLaMo0.8B/2Bの評価PNG2個に**同一LFS SHAの共有候補3組（約13.972MBの参照重複）**がある。ただし双方を採用する判断でもOwnerの同一物理ファイル確認でもない。

## 6. 法務・規制の事実と研究仮説

[米BIS 91 FR 74970 IV.A（2026-11-19）](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion RuleのモデルウェイトECCN 4E091を撤廃した。公開済み全ウェイトの近い将来の所持禁止日や確率は資料から決められない。配布元のgated/ライセンス改訂、モデルの独立訓練再現難度を**供給保全のストレスシナリオ**として別に記録する。Smaug無検閲DPO（[R158研究キュー](../../queues/proposed-v66-r158-post116-prioritized-UNAPPROVED.json)）を本候補のために削除・格下げしない。

## 7. H/T/D/C/U — 反証可能な次段階

- **H**：新0.8B専用ECモデルは同条件の既取得Qwen3.5-0.8Bより、未見の合法な商品画像／比較タスクに有意な上積みを示す。MiniCPM5-2Bは同規模既取得モデルに対し、保管5.044GBに見合う推論/コード/agentの有用な独立性能を示す。予測閾値は**独立held-out正答差の95%信頼区間下限>0**（これは本研究の採否ルール案であり達成値ではない）。
- **T**：WeMMのECカテゴリ計100件以上、MiniCPMのコード/推論/agent課題計100件以上を訓練データと分離し、同じモデル呼出しAPI/プロンプトポリシーを使用。メモリ/速度は同じGPU/CPU、固定クロック/driver/OS/backend、context/画像サイズ、batch=1及び実業務バッチ、quant bit/scale/zero-pointで**各30回以上**測定。速度はmedian・測定範囲を記録。安全/権利/ファイルSHA/空き床が欠けたら直ちに停止。外部ネットワークでの未承認取得や第三者コード実行なし。
- **D**：固定ソースとPLaMo5変更が一致すれば**STATIC_SOURCE PASS**。品質の下限>0かつ実機実行互換が成立すれば**QUALITY PASS**。権利不成立・SHA不一致・未承認転送なら**FAIL**。現時点は所有者ライセンス行為・現在の空き・依存・実HW評価が不明で **DOWNLOAD UNCERTAIN→STOP**。
- **C**：作者のEC23社内ベンチが過学習で未知の画像では改善しない、MiniCPM集計の条件が混在、PLaMo新テンプレートが旧重みの挙動を変える、ERNIEの高圧縮重みが実SSDで遅すぎる、PLaMo新契約が目的の利用行為と合致しない。
- **U**：主な不確かさはPublisherの宣言とowner現物SHAの混同、ベンチサンプルの非独立性、GPUメモリ/量子化ABI/キャッシュ、本人契約上の利用目的/第三者権利。今は実機の誤差系列がないため合成標準不確かさ `u_c`（測定量に応じた単位）・包含係数`k`（無次元）は算出不可。

**ERROR CHECK**：固定ソース6repo229files／184,714,085,822byte、LFS159件。新推薦2repo31files／6,776,852,427byte。PLaMo新旧16fileで5非weight変更・新旧重みSHA一致・新旧容量差14,153byte。ERINIE142filesの論理総数と量子ファイルbytesを同じ量とみなさず、旧v66資産246/197・承認0・新重みDL0を維持。公開元ファイル情報の静的監査と、Ownerの現物復元・契約上の許可を明確に区分。

関連分野：①マルチモーダル機械学習とEC/商品処理、②小型LLM知識蒸留・コードエージェント、③多言語翻訳/契約法のrevision管理、④MoE/QAT/GPUメモリ工学、⑤デジタルアーカイブと内容アドレスハッシュ。

###〈次に考える問い〉
**Smaugの無検閲別DPOと、WeMM-Ecom0.8Bの軽量独立EC学習成果のどちらを実測・取得前審査の最初の対象にするべきか。その優先順を、ライセンス・容量・実機再現コストを数値で比較して決定する。**
