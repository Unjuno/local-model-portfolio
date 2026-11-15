# R93：LTX-2.5 Pre-Trainedの独立学習済み原本を発見・研究HOLDに登録（2026-11-15）

## 1.〈本論〉— 新たに発見した学習段階

**発見：** [Lightricks/LTX-2.5-Pre-Trained](https://huggingface.co/Lightricks/LTX-2.5-Pre-Trained) は、現在アーカイブでCONDITIONAL選定されている [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) と**異なる学習段階**。メーカー公式カードに、後者のSFTとその他後学習より前のpretraining原本であることが明記されている。同一チェックポイントのGGUF/NVFP4/INT8変換ではなく、通常版からlosslessly逆生成できない学習済み状態として保存検討価値が高い。

**結論：新規1件を研究HOLD候補として別台帳に記録。正式正本v42の195資産・有効148件は変更しない。** [非正本HOLD候補](../../catalog/proposals/08-ltx25-pretrained-gated-2026-11-15.json) に保存し、Gated本人権限・原本の固定SHA・実ディスク容量が揃うまで正式採用しない。 現有の一般LTX2.5 dev/distilledや作者派生の採否は変えない。追加容量をactive確定枠に加算しない。Gated modelの本人アクセス許可は不明であり、同意・取得は一切実行していない。

| 種別 | 配布元の実際の構成 | 採否 |
|---|---|---|
| **Pre-Trained** | 22B級DiT＋video VAE・audio VAE・vocoder・duration head・text embedding projectionsを**原本`ltx-2.5-22b-pt-bf16.safetensors`に束ねる**。別の学習済み`ltx-2.5-22b-gemma4-12b/`（Gemma 4 12B、`gemma4-12b-ltx-v1`互換）が必須 | **研究HOLD候補（未採用）**、Gated権限・SHA・容量が未確定 |
| 現在のLTX-2.5通常版 | `diffusion_models/ltx-2.5-22b-dev-transformer-bf16.safetensors`と`...distilled...`など、SFT・後学習版の別学習結果を分割配布。テキストencoderとaudio/video VAEはファイル分離 | CONDITIONAL既存維持。全部の量子化形式を重複保存しない |
| Stubelius v1 Remix | 10Eros/Sulphur由来のtask-vector merge、OmniNFT **RL fine-tune**、蒸留LoRAを統合した別学習済み結果。作者のv1 BF16は約42GB、Xet公開SHA256 `6e0ff9c9d8a1d0747579f1f50d10a9c3822a9a8f265322a5edd476044b0fbf4f` | CONDITIONAL維持。BF16を原本研究候補にし、INT8/Q4/NVFP4およびbeta旧版はデフォルトから除外 |
| ChrisColeTech v1.1 FP8 | Eros10・DMD distillation・IC-LoRA・IC detailer・Img2Vid LoRAを一体化した作者報告の別学習済みマージ。専用TE・VAEあり、HF tagは`license:unknown` | CONDITIONAL研究維持。通常LTX2.5の単なる再量子化と断定しないが、完全なライセンス・5 donor・正確なファイルSHAは未確認 |

**原本の一次証拠：** [LTX2.5 Pre-Trained README](https://huggingface.co/Lightricks/LTX-2.5-Pre-Trained/blob/main/README.md)／[Gatedファイル一覧](https://huggingface.co/Lightricks/LTX-2.5-Pre-Trained/tree/main)／[通常版README](https://huggingface.co/Lightricks/LTX-2.5/blob/main/README.md)／[Stubelius v1 BF16重みpointer](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/ltx2.5-Stubelius_remix_v1_bf16.safetensors)／[Stuubsモデルカード](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/README.md)／[ChrisColeTech v1.1カード](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8)。

### ライセンスと同一性が未解決

GitHub配布元の [`LICENSE-2_x`](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) は**2026-10-29改訂のLTX-2.x Community License**。コード自体のApache2.0を、モデルウェイトの自由な利用・再配布権と混同しない。年商1000万米ドルの一定の事業者利用には別契約があり、派生重みの取り扱いにも条件がある。Pre-Trainedの本人Gated同意条件・原本LICENSE全ファイル・許容利用行為の最終照合は未完了。これは法律で一般に禁止されたことを意味しない。

**重み同一性：** Pre-Trainedに必須の`ltx-2.5-22b-gemma4-12b/`は、通常版の`text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors`と**SHA一致を未確認**。名前がGemma4で同じだけで容量を差し引かない。Pre-Trained本体は公式が約43GiB、HF一覧は約46.2GB。いずれも丸め値で**正確なファイルbyte・SHAはGatedのため未確認**。

## 2.〈応用・転用例〉— 調査用の容量ストレス

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| \(B_0\) | v41移行前のv40計画上の残余 | byte | 129,409,767,827 | publisher参照＋予約枠の仮説値 | 整数スカラー |
| \(B_m\) | Pre-Trained本体の公称ファイルサイズ | byte | 約46,200,000,000 | HF tree丸め表示、実ファイルは未確認 | 概数スカラー |
| \(B_g\) | 必須Gemma4 text encoder＋Tokenizerの実サイズ | byte | 未確定 | 同一revisionで要件照合、既存SHA流用は未証明 | 未知の非負スカラー |
| \(B_e\) | Runtime・wheelhouse・stagingの増分 | byte | 未確定 | OS/GPU/ABI・取得方法・オフライン復元依存 | 未知の非負スカラー |
| \(M\) | Pre-Trainedを有効化した場合の見かけの余白 | byte | \(B_0-B_m-B_g-B_e\) | 暫定値、実機に対する保証なし | 未知のスカラー |

**次元チェック：** byteからbyteを引くので単位整合。\(B_m\)が約46.2GBだけでも、\(B_g\)、\(B_e\)が不明のため**確定の余白は求まらない**。43GiBの数学的換算は46,170,898,432 byteだが、これは「原本の実測byte」ではない。

**H:** Pre-Trainedは通常LTX2.5の後学習版と同じ学習済み重みではない。**T:** 原著モデルカード、HF固定対象ファイル一覧、LTX公式ライセンス・Trainerコード、Stubelius/Chris派生作者カードを比較（異なる学習段階1＋既存派生3、n_min=4）。**D:** 独立学習段階の存在はPASS、追加購入/取得可能・完全byte・実機容量はUNCERTAIN。本人権限・適法性や正確ファイルリストを欠いた取得はFAIL/STOP。**C:** 原本BF16 SHAが通常版devと一致する場合（現状証拠なし）またはGemma4が無条件に共有可能という誤仮定。**U:** Gated access、丸めサイズ、TE重複、契約適用、runtime/ハード。測定分布がないため合成標準不確かさ\(u_c\)と包含係数\(k\)は未定義。

**ERROR CHECK:** v41→v42の正式資産195件と有効148件は変更せず、原本1件は非正本の研究HOLD候補にのみ追加した。CONDITIONAL95/SELECT53および取得キューも変更しない。重み取得0、モデルコード実行0、Gated権限の変更0、承認0。

**学際連携:** 動画/音声生成基盤のプレトレーニング研究、デジタル保存の学習状態の差別化、ソフトウェア供給網のhash/ABI、契約・ライセンスの権利追跡。

### 3.〈次に考える問い〉

**個人で利用する権利とGated許可が確認された際、46.2GB原本と必須Gemma4 TEをどのsource SHAで固定し、既存LTX原本との重複をゼロにできるか。**

**版競合の訂正（R93）：** 別作業のv42が既存LTX親・派生3件のメタデータ更新として確定しており、`catalog/CURRENT.json` の正本件数は195件である。Pre-Trainedはこのv42の正式`items`には存在しないため、研究HOLDの提出先を別のproposalに限定した。未適用のv42候補成果やstaleな196件集計を正本と称しない。
