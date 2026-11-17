# R107：最初に保存すべき8件の原本・無検閲モデルを選び、不要な追加取得を止める

**基準：2026-11-18 / v45（登録198・有効151）。** 機械可読の[8件取得ターゲット＋保留・交換検討台帳](../../catalog/decisions/2026-11-18-r107-download-selection.json)を正本とする。これは**何を保存すべきかの選定確定**であって、HDDへのダウンロードの承認でも、合法な重みファイル全部の最終lockでもない。承認キュー`queues/approved.json`は空のまま。

## 1. 〈本論〉容量を重複させず独立学習結果を優先

規制予測だけではモデルを選ばない。使用許諾と正規再取得の可能性、モデル自体の学習差分、元モデル・同族量子化との重複、必要な依存、HDD実測とオフライン復元が判断軸。特に**無検閲は独立能力**：政治的応答抑制のみを調整したモデルと、広い拒否制御を編集したモデルは同一の保存成果物ではない。逆に同系統のGGUFを何十個も保存することは原則重複。

| 調査順位 | 選定済み・取得対象にすべきrepo ID | 過去の選択ファイル候補（byte） | 選ぶ理由 | 次のゲート |
|---:|---|---:|---|---|
| 1 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | 17,738,357,352 | Politically selective uncensor edit with Q4+vision projector; not interchangeable with general abliteration | Current fixed-revision and model/projector checksums, llama.cpp quant/backend and right to archive |
| 2 | [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 16,560,392,734 | Multi-stage ARA edited RVN multilingual Q4; preserve one trained derivative rather than whole 1.645TB quant repo | RVN-Q4_K_M-multilingual.gguf exact version and file hashes, llama.cpp template, rights |
| 3 | [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | 1,769,980,465 | Compact official posttrained model, not the separate pretrained Base | Old snapshot needs live immutable source and license recheck |
| 4 | [lightonai/LightOnOCR-3-0.8B](https://huggingface.co/lightonai/LightOnOCR-3-0.8B) | 1,737,771,835 | Small learned OCR, document tables and forms; independent specialized task | Processor and all dependencies, frozen weights and actual doc quality |
| 5 | [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | 1,622,466,054 | Multilingual ASR reference to assess new specialist models | Current exact source files, runtime, local WER and rights |
| 6 | [usezn/Galvanize-3](https://huggingface.co/usezn/Galvanize-3) | 597,573,024 | Distinct prompt-injection/jailbreak detector in compact ONNX, complementary to uncensored chat weights | Frozen ONNX and tokenizer, opset, false-positive metrics |
| 7 | [KRAFTON/Raon-1-nano](https://huggingface.co/KRAFTON/Raon-1-nano) | 7,182,126,657 | Delta attention/MLA independent small hybrid with unique posttraining | Remote custom code safety and ABI, conflicting rounded parameter count, separate MTP |
| 8 | [abel-lab/Simons-297M](https://huggingface.co/abel-lab/Simons-297M) | 1,188,951,960 | Probabilistic forecasting independent learned weights and covariate handling | OpenMDW notices and training-data rights, frozen offline runtime |

**8件の過去の選択source合計は48,397,620,081 byte（48.397620081 GB、十進）**。`Interpretic`は[Round21の12ファイル](../../manifests/drafts/round21-pinned-preservation.candidate.json)（Q4、projector、LICENSEなどのprovenanceを含む）、`0bserverx`は[Wave2の11ファイル](2026-11-11-wave2-source-scope-and-v3.md)（RVN multilingual Q4だけ）を参照。旧Qwen/LightOnOCR/Whisperは2026-10-30固定の未承認候補、Raon/Simonsは2026-11-18作者原本の候補。**これら8件はすべて現行v45有効選定の内数であり、4TB予算に48.398GBを追加算入してはいけない。** 過去の選択byteは依存・ランタイム・cache・stageを含む完全アーカイブ容量ではない。選択ファイルSHAはユーザーHDDで未検証。

特に [Interpretic v2 Q4](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) は作者の中国語政治質問で回答抑制98/113→4/113と報告する一方、一般の有害依頼拒否95/100やGPQA等は**BF16版の数値**。Q4の無条件な同品質は言えない。著者実験は独立計測ではない。 [0bserverx RVN](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) は作者が複数ARAを主張し、旧`Qwen3.8-27B-Heretic-Q4_K_M.gguf`をレガシーと明記。正しい対象は`RVN-Q4_K_M-multilingual.gguf`。大量の量子化repo全体を取得すると約1.645TBの不要な容量浪費となる。

## 2. 権利・親重み・大型原本を先に確定する別レーン

| 既存v45モデル | 判定 | なぜ一括自動取得しないか |
|---|---|---|
| [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | KEEP_RESEARCH_ONLY_PARENT_LICENSE_FIRST | Unique unmerged rank128 adapter; non-commercial Qwen Research agreement and exact Qwen-Image-2.1 parent+encoder+VAE required |
| [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | KEEP_GATED_PERMISSION_FIRST | Distinct BF16 refusal-edit origin; Gated user-specific permission required |
| [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | KEEP_SPECIALIZED_CAPACITY_REVIEW | Distinct GUI agent policy, ~54.7GB source repository |
| [IFM/PAN2](https://huggingface.co/IFM/PAN2) | KEEP_WORLD_MODEL_SOURCE_REVIEW | 29.202B independent video world model; large 86.08GB fixed source candidate and dependencies |
| [speridlabs/idol](https://huggingface.co/speridlabs/idol) | KEEP_GATED_DEPENDENCIES_REVIEW | 3DGS requires separately gated DINOv3 and FLUX.2-VAE |

[ChatRの画像用LoRA](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1)は671,173,375 byteという比較的小さい別学習済み成果を保存できる。ただしLoRAだけでは動かない。Qwen-Image-2.1の正確な基盤・encoder・VAEと**Qwen Research Licenseの非商用研究条件**が成立して初めて復元可能。[メーカーREADMEの作者自身の評価](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1)では成人向けprompt adherenceに改善がある一方、一般SFWや解剖学的忠実度に低下も見られ、検閲解除が品質向上に直結するわけではない。

`orcarouter`原本はGatedであり、**作者の将来削除可能性はユーザー許可の代わりにならない**。Fara/PAN2は別学習済み独立性を維持し、元重みの高価値アーカイブとして比較するが、優先8件の正規取得準備を先に解決する。

## 3. 交換・保留の具体的判断

| モデル | 今回の決定理由 |
|---|---|
| DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU | Multiple 27B variants already selected; no independent quality-vs-byte gain established. Do not delete existing catalog entry; defer new manifest. |
| ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8 | Complete learned parameter/codec pipeline and license unknown; block weight lock |
| Stuubs/Stubelius_Remix_Ltx2.5 | Complete learned parameter/codec pipeline and rights unknown; block weight lock |
| ConwayResearch/Underdog-Woof | Noncommercial usage and no speech-model training/distillation; legal-use mismatch for part of portfolio |
| osunlp/ARLoop-0.6B | Same-family duplication of the 1.2B research original without independent target |

ここでの延期は**既存catalogからの即時削除ではない**。既存の専門的後学習結果が失われないよう原本価値は維持しつつ、将来の同系量子化/巨大シャードを無差別に取り込む作業だけを止める。誤って原本を削るより、容量と独立品質の一次根拠が揃った時点で正規のrevision overlayで交換する。

## 4. 次に正式選定へ追加すべき新規2件

| まだv45外の候補 | 研究価値 | 追加の条件 |
|---|---|---|
| [osunlp/ARLoop-1.2B](https://huggingface.co/osunlp/ARLoop-1.2B) | Distinct recurrent depth architecture and independent 500B-token pretraining; not registered v45 | Fixed 40-character source revision, source file hashes and actual bytes, custom-code security, capacity |
| [KittenML/kitten-tts-2-mini](https://huggingface.co/KittenML/kitten-tts-2-mini) | 82M compact multilingual CPU TTS including Japanese; not registered v45 | Fixed ONNX/G2P/voice selection hashes, license and voice notices, Japanese quality, actual bytes |

ARLoop-1.2B（学習済み約1.2087B、公式[arXiv:2611.05234](https://arxiv.org/abs/2611.05234)）は深さ方向Residual Attentionの反復型Transformer、Kitten TTS 2 Mini（公称82M、CPU INT8 ONNXと日本語voice）は実用方式が異なる。**いずれも固定モデルSHA40・全必要ファイルの正確なbyte・ハッシュと実機互換が未確定**なので、正式なv46追加や取得承認は時期尚早。

## 5. 規制想定の使い方と取得前の停止条件

現時点の公開`public`、`gated`、LICENSEメタデータはモデルの将来規制確率ではない。Hugging FaceのGated許可は利用者本人について確認する。Exa検索はこの回でHTTP 402（クレジット上限）を返し、**Exaで新資料を検証したとは主張しない**。公開モデルカードと既存の作者原本、既存の一次証拠・政策台帳から限定的に選んだ。

既存の[現行資源規約](../../policies/limits.json)は**150Bを基準**に、超過量子化モデルの例外を同一HW/backend/context/batch・30試行以上の比較実測などに条件づける。**MoEは全expert合算**、総数不明なら最終lockは停止。今回の8件はこれを緩和しない。4TBは**計画上限**、200GB以上の空きを物理的に残す必要があり、未測定の余白27.409GBは実際の取得可能容量ではない。

| 記号 | 意味（日本語） | SI単位 | 定義・値 | 定義域/条件 | 型 |
|---|---|---|---|---|---|
| `B_8` | 初回8件の過去選択元ファイル合計 | byte | 48,397,620,081 | v45既存原本の内数。完全復元bundleではない | 非負整数 |
| `B_max` | 論理アーカイブ上限 | byte | 4,000,000,000,000 | 既存内容とcache/stagingを除外していない | 非負整数 |
| `B_floor` | HDDに残すべき空き容量 | byte | 200,000,000,000 | 取得後・最も使用するstagingで維持 | 非負整数 |
| `P_base` | 量子化例外が必要となる総モデル数境界 | 1（無次元） | 150,000,000,000 | MoE inactive expert含む。上限超は例外比較実測が必要 | 非負整数 |
| `P_model` | 審査対象モデルの総学習済みパラメータ | 1（無次元） | 作者・配布元資料/固定tensorで評価 | 不明ならlock停止 | 非負整数またはnull |

**次元チェック**：8件容量はbyte同士を加算し、モデル総パラメータ（無次元）とは混同していない。8件の保存準備だけなら約48.398GBの選択source候補であり、初回優先を決める根拠にはなるが実ディスクでの成功や権利適合を証明しない。

取得GOには「原本配布元・完全revision・選択files全件SHA/byte・LICENSE正文・依存／親の権利・ユーザー本人のGated許諾・実HDD測定・安全なbackend/ABI・明示的最終マニフェスト承認」が必要。**本体取得・モデルロード・無許可Gated回避・再配布は実施しない。**

## 6. H / T / D / C / U とERROR CHECK

- **H**：異なる目的の2系統の無検閲Qwenと6系統の小型/専門原本が、重複量子化より高い保存の増分価値を提供する。
- **T**：旧スナップショットの8件合計選択file件数とbyte、固定ID、親/依存、最新Hub状態を一件ずつ照合。owner実機の測定と合法的取得を別工程として停止。現行テスト対象n_min=8。
- **D**：PASSは必要な全ファイル/親/license/本人権利/実HDD/ハッシュ/ABIを満たした個別対象のみ、FAILは権利不一致・真の重複・選択集合不成立、UNCERTAINは未確認が残る現在の状態。
- **C**：作者が公開を続ける、合法な同一SHAミラーが現れる、Q4品質が低下する、他の小型モデルに能力が代替される。
- **U**：配布元の仕様更新、partial source coverage、独立実機測定欠如、利用許諾・法域、音声/画像依存。確率分布・校正がないため`u_c`と`k`の数値化は行わない。

**ERROR CHECK**：8件全てv45（198資産・有効151）の既存選定に存在、ユニークrepo ID8。選択済み元ファイル候補合計48,397,620,081byte、データを再加算しない。5件の権利/依存重い追跡、5件の延期、次期候補2件。現行`queues/approved.json`への変更0・重み取得0・実行0。**本書はリポジトリの取得方針を具体化するが、未承認のキューを実行可能に変更しない。**

### 〈次に考える問い〉

現在の最大のボトルネックはモデル選定の不足か、それとも既に選定した8件の**完全原本source、本人権利、実HDD・オフライン復元の未完了ゲート**か。後者を優先解決しなければ、モデル候補を増やしても保存可能性は増えない。
