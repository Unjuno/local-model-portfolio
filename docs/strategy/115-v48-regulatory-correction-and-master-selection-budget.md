# R115｜v48 高精度原本の取得候補・容量交換・2026年11月米BIS制度の事実確認

基準日：2026-11-19。正本 `catalog/CURRENT.json` は v48（201登録／154有効、SELECT53・CONDITIONAL101）。本研究は原本保存の**選択スコープの代替案**であり、正式取得承認・重み取得・既存資産削除を意味しない。

## 1.〈本論〉モデルを『原本』だけで判断しない

**事実：Interpretic v2**：公開者の[原本BF16モデルカード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)は元Qwen3.8 27BのBF16フルfine-tune、MTP head保持と説明。32固定ファイル・55,586,056,799byteが[既存publisher manifest](../../manifests/drafts/r113-v48-two-uncensored-original-fp16-parents.candidate.json)で確認できる。元GGUF Q4の17,738,327,225byteは元の学習済みcheckpointとは別のシリアライズ／量子化形式であり、原本と無条件二重取得しない。

**事実：0bserverx RVN**：[作者のSafetensorsカード](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored)は13 shards/851 text tensorsを`RVN-F16.gguf`から再構成したと説明。**学習時BF16ではなく、vision encoder/MTPも含まない**。最古の確認済み変換元として作者が示す`RVN-F16.gguf`（53,808,281,888byte／SHA256 `f20c72c23a6564211c5e44af35ea1277d697c009ce8a25ab28d100447e0f155a`）を、[公開GGUF元](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)の同じ固定リビジョンから原本保全候補に採る。ただし過去の学習時tensorビットは復元できない。

**補足：視覚入力の互換性**：作者は別の`mmproj-Qwen3.8-27B-Q8_0.gguf`（629,247,008byte）を使用するとRVNのGGUFでvision入力可能と説明。ただしF16テキスト原本単独にvision学習済み重みは同梱されない。このため**本マスタープロファイルは元のQ4＋projectorの全ユースケースと同等と主張しない**。画像入力が保全対象ならprojectorを共有依存として別途固定、動作検証する。

## 2. 固定ソース15モデルの2プロファイル

| 出典と対象 | 容量優先（現行R113） | 原本保全優先（R115） |
|---|---|---|
| Interpretic v2 | Q4＋mmprojの5ファイル | BF16フル原本32ファイル |
| 0bserverx RVN | multilingual Q4＋projector等4ファイル | `RVN-F16.gguf`と同じ固定版のREADME/.gitattributes、3ファイル |
| Kitten TTS 2 Mini | 原safetensors＋ONNX＋声とG2P | 同一学習済みの派生ONNXを除き、原本と声・G2Pを保持 |
| ほか12モデル | 元source固定 | 同じsource scope／元取得状態維持 |
| **15モデル総量** | **212,023,095,122 byte** | **286,419,747,966 byte** |

[R115原本優先・15モデル212ファイル／SHA参照89件の機械可読別案](../../queues/proposed-v48-r115-archival-master-alternative-15.json)は、旧[R113容量優先の15モデル187ファイル／SHA74件](../../queues/proposed-v48-r113-source-pinned-15.json)を置き換えて実行しない。どちらも元v48有効資産の部分集合であり、15件を重複資産として新規登録していない。R115全件のmetadata一致は**PASS**、ダウンロードは0。

原本優先の11モデルA群だけを見るとpublisher sourceは**121,451,029,055byte**（旧A群47,054,376,211byte）。B（671,173,375byte）は親Qwen Imageと非商用条件を解決するまで停止、Cの大型2件（108,711,479,306byte）は性能差が独立検証されるまで取得延期、DのOrcaRouter（55,586,066,230byte）は本人Gated権限が確認されるまで停止。

上流SHAが同一のtokenizer.json（12,809,320byte）がInterpretic BF16とGated OrcaRouterで確認できた。89 SHA参照のうち異なる内容SHAは88個。**双方が正当に取得され、現物内容が一致した場合だけ**重複排除を認める。これは物理節約の実測ではない。

## 3.〈応用・転用例〉容量と実ダウンロード優先順位

元のv47予算に残った20,409,767,827byteは、完全offline bundleやユーザーDドライブの実測ではない仮想余白。両原本への交換で74,396,652,844byte増加するので、**以前の代理計算の選択ファイルが重複なしで全てそのまま含まれる場合に限り**、単純な余白は-53,986,885,017byteになる。4TBに合格したとも物理的に超過したとも断言しない。

容量が実測できる前の実取得は進めない。取得の最小パイロットは元ソースが固定済みの`ibm-granite/granite-timeseries-ttm-r3`（5,748,963byte）とし、本人合法アクセス・保存先・ローカルSHA・offline restoreをまず1件で実証する。小型原本（tiny-voca・Kitten・Galvanize・ARLoop）は他の重複原本を増やすより優先。無検閲2高精度マスターの取得は、同じ容量枠で代替・減額できる重複が確定してから。

## 4. 米国BIS規制、事実と予測を分離

**一次資料（公表準備段階）**：[Federal Register Public Inspection, 2026-23529](https://public-inspection.federalregister.gov/2026-23529.pdf)（`Addressing Remote Access to Advanced Semiconductors`）は2026-11-19掲載予定のinterim final rule。Section IV.Aは2025年AI Diffusion Ruleの**モデル重みの輸出統制ECCN 4E091を撤廃**すると明記。同時に遠隔データセンターの計算資源／先端半導体の別の輸出・最終用途規制を強化する。これを『公開ウェイト全般のダウンロード禁止』と解釈するのは誤り。公開予定のinspection版を確認したものであり、連邦官報の正式掲載・適用時刻・個別取引は必要に応じて最新正文を照合する。

配布者のGated化、ライセンス、利用国別規制は別要因。将来の全面規制を**仮説**として保全のストレステストに使うのは適切だが、個別モデルの削除確率や取得禁止確率は一次根拠なしに数値化しない。150B学習済み全パラメータ上限は本リポジトリ固有の運用ポリシーであり、ECCN 4E091の学習演算量基準と混同しない。

## 5.新候補v3を交換対象にしない理由

[InterpreticAI/Qwen3.8-27B-Uncensored-v3](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v3)はNousResearch/Arete-27Bからの別fine-tuneなので**独立学習済み成果**として調査価値がある。一方、v3にはMTPがなく、著者の政治回答指標3/115とv2の4/113は評価分母と構成が異なる。単発著者試験の1回答程度の差を一般性能優位とみなさない。容量、正確なsource revision、利用権、out-of-sample精度の計測なしにv2をv3へ交換しない。**v3は研究保留・正式追加0**。

## 6. 変数表、数値整合

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| `S_c` | 現行容量優先source総量 | byte | 212,023,095,122 | 既存15モデルpublisher metadata | 非負整数スカラー |
| `S_m` | 原本優先source総量 | byte | 286,419,747,966 | 15モデルpublisher metadata | 非負整数スカラー |
| `D` | 原本交換増分 | byte | `S_m - S_c` | 同じ15資産集合だけを比較 | 符号付き整数スカラー |
| `H` | 歴史的な仮想容量余白 | byte | 20,409,767,827 | v47代理source見積、実HDDではない | 符号付き整数スカラー |
| `M` | 条件付きの新仮想余白 | byte | `H-D` | 元のsource一致と他変更なしを仮定 | 符号付き整数スカラー |
| `F` | 保存後の最低物理空き | byte | 200,000,000,000 | 本人実HDDのstaging中にも必要 | 非負整数スカラー |

次元チェック：全てbyteであり、`D=74,396,652,844byte`、`M=-53,986,885,017byte`。この計算は**sourceの選択差分**であり、親・codec・wheel・キャッシュの実増分を証明しない。`F`は政策下限で、`M`と比較して実空きと判断しない。

## 7. H/T/D/C/U・ERROR CHECK

**H**：学習済み独立成果を保持しつつ精度変換の重複を抑えれば、将来の再量子化能力と保存効率の両立が可能。

**T**：15 asset ID、全212ファイル、89 publisher SHA参照（ユニーク値88）を別案と既存publisher metadataで比較。性能については同一H/W・clock・context・batch1、同一decode設定で最低30問ではなく**最低30反復の独立held-outタスク**を事前設計し、性能差が0.5%未満なら『明確な優位なし』とする暫定研究仮説。環境・検体がないためまだ未実施。

**D**：source metadata整合PASS。実4TB／法的本人許諾／offline restore／性能ベンチはUNCERTAIN。source不整合やGated無許諾はFAIL。

**C**：別のより早いRVNの元checkpointが見つかる、MTPやvision学習済みが別ソースでのみ復元できる、追加圧縮で高精度原本の保全効果が弱まる可能性。

**U**：出版社カード報告の計測バイアス、現物HDD未測定、GGUF backend/量子化zero-point、依存全ファイル未閉包。標準合成不確かさ`u_c`と包含係数`k`は標本がなく算出不能。

**ERROR CHECK**：v48の201登録/154有効、compact15とmaster15の同じ資産集合、R115 212ファイル・89 SHA参照・source286,419,747,966byte、一意SHA88。主配布元の重み取得0、本人4TB測定0、承認0、mainのみ。*先行sourceの研究判断が増えても実保存は完了していない*。

### 〈次に考える問い〉

不足する約54GB相当の仮想容量を、学習済み能力が本質的に同一の派生ファイルの整理で確保できるか。それとも高精度原本を後順位として、まず小型・希少原本のオフライン再現性を完成すべきか。