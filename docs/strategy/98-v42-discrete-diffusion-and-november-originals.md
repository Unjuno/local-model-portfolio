# R98｜v42保存候補の再選定：DiffusionGemma・Arete・Ripple（2026-11-15）

**調査の結論**：正式正本は `main`／`catalog/CURRENT.json` → **v42：195登録、148有効（SELECT53／CONDITIONAL95）**。今回は3つの未登録学習済み系列をHugging Face配布元で照合し、**DiffusionGemmaのみP1研究昇格案**、Nous AreteとRicursive Rippleは**P2保留**とした。いずれもv42正式正本には**追加しない**。実機容量・ファイル全SHA・LICENSE行為別権利・オフラインABIが未確定で、現時点で正式CONDITIONALや取得キューに自動投入するのは不適切。新規ウェイト取得、実行、個人のGated承認、ダウンロード承認は**全て0**。

[機械可読の3候補比較とDiffusionGemmaの22ファイル部分source固定](../../catalog/proposals/2026-11-15-r98-diffusiongemma-arete-ripple-original-selection.json)／[現行v42](../../catalog/effective-portfolio-2026-11-15-v42.json)／[取得前148ゲート](../../catalog/readiness/v42-2026-11-15-r94-all148-gates.json)。

## 1.〈本論〉— 3系統の原本に対する採否

| 配布元原本 | 確認できた学習済み内部構成・実体 | 保存価値と既存との比較 | 決定 |
|---|---|---|---|
| [Google DiffusionGemma 26B A4B IT](https://huggingface.co/google/diffusiongemma-26B-A4B-it) | HF表示25.8238B、Apache-2.0、非Gated表示、11枚BF16 safetensors、リポジトリ表示**約51.7GB**。30層、128全expert中8 active、256 token canvas、27層vision encoder。 | **自己回帰encoder＋双方向diffusion decoder**の異種混合。既存[GSAI iLLaDA-8B](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base)は別学習の拡散系列、既存Gemma4 31Bは一般の自己回帰系列。単純GGUFや別精度ではない**独立の学習済み重み**。 | **P1研究優先・次期CONDITIONAL候補**。保存準備と取得は停止。 |
| [Nous Arete-27B](https://huggingface.co/NousResearch/Arete-27B) | 既存Qwen3.8-27BのテキストSFT。作者発表は約52.8M tokens、1202 steps、vision frozen、MTP無効。Apache-2.0、HF表示27.3567B。 | 政治・価値判断の学習目的は独立しうるが、既存Orca／InterpreticAI／0bserverx／DavidAU派生の比較研究と重なる。新しいarchitectureではない。政治回答と事実誤認を分けた同条件測定がない。 | **P2 HOLD**。重み等価ではないが追加価値未証明。 |
| [Ricursive Ripple-65B Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | 約65B dense、約12T pretraining tokens、80層の独立事前学習と特殊attention実装、Apache-2.0。**BF16全repo約130GB**、作者独自コード。 | 学習原本は実在し、Qwen派生ではない。ただしv40からの仮想残容量約129.41GBを全repoだけで超過する。作者ベンチは条件の異なる比較が混在。 | **P2 HOLD**。データセンター級の性能順位だけで既存原本を交換しない。 |

DiffusionGemmaについて[Google公式model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)では「25.2B total／3.8B active」のテキスト系報告がある一方、HFの全モデルメタデータは**25.8238B**と表示する。vision encoderなど報告スコープと丸め差を考慮すべきで、**完全なsafetensors tensor censusを行って数値を一致させたという意味ではない**。しかし両方とも現行150B総数screenを大きく下回る。active 3.8BだけでMoE総数を判定しない。

**負の性能情報も残す**：Google作者同条件のMMLU-Proは77.6対自己回帰Gemma4 82.6、AIME 2026は69.1対88.3、MMMU-Proは54.3対73.8。汎用能力の優位ではなく、**並列拡散生成・局所的挿入編集・小batch生成の異なる手法**が保存理由。Googleの「1,000 tokens/s超」はH100・FP8・小batchという作者条件であり、手元HW・クロック・batchを照合した実測ではない。[Googleの公表測定](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)。

## 2. DiffusionGemma：再現可能な保存sourceの境界

配布元Hugging Face [固定commit `f7f5b7f5fa82ffc52addd066915886d497f5517b`](https://huggingface.co/google/diffusiongemma-26B-A4B-it/commit/f7f5b7f5fa82ffc52addd066915886d497f5517b) のファイル一覧を静的照合した。源候補は**22ファイル**：BF16重み11 shard、model.safetensors.index.json、model_index.json、tokenizer.json／config、chat_template、model/processor/generation config、scheduler/scheduler_config.json、README、.gitattributesなど。小さなschedulerが抜けてもdiffusion再現性を欠くため、モデル重みのみを保存する設計は禁止。

- publisher確認済み**第1 shardのSHA-256**：`3efe137998af7d2bde4e3ab04ab3524823699a4ac3130adace5003ef40cceeb6`（[固定repoの公開元ファイル](https://huggingface.co/google/diffusiongemma-26B-A4B-it/blob/f7f5b7f5fa82ffc52addd066915886d497f5517b/model-00001-of-00011.safetensors)）。**ローカルでハッシュ照合した値ではない**。
- 他10 shard・tokenizer・scheduler等の**バイト単位サイズとSHA-256は未確定**。公開元のファイル一覧にあるGB表示は丸め済みであり、正式selected_file_bytesではない。
- [Google公式実行手順](https://ai.google.dev/gemma/docs/diffusiongemma/inference-diffusiongemma-with-hf) は `transformers>=5.11.0`、torch、accelerateを使用し、BF16のノートブックはGPUメモリ**60GB超**を前提とする。diffusers schedulerの互換バージョン、PyTorch/ CUDA/driver ABI、batch、context長、量子化zero-point、wheelhouseをまだ固定していない。量子化で「18GB以下」という宣伝値を原本BF16のメモリ要件に流用しない。
- [Google本家model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card) はApache-2.0を明記するが、原本の固定スナップショットの全LICENSE／NOTICEと個人の具体的行為許諾を機械的にPASSにしない。

**必要な前進**：残り21ファイルのpublisher SHA／正確なbytes／ライセンス・ランタイムを一意に固定し、既存146件のsource未閉包と競合するディスクの計画容量を再計算したのち、次回正式revisionへのCONDITIONAL投入可否を判定する。

## 3. 量子化メタデータが全パラメータ数を偽装する可能性

今回の重要な**データ品質上の発見**は[Ripple原本BF16](https://huggingface.co/ricursiveAI/Ripple-65B-Preview)のHub表示 **64.7827B**に対し、**同一学習成果の作者NVFP4変換版** [Ripple-65B-Preview-NVFP4](https://huggingface.co/ricursiveAI/Ripple-65B-Preview-NVFP4)のHub表示が **39.6169B**であること。作者model cardにはMLPにNVFP4、attentionにBF16を適用した**BF16原本の量子化**とある。異なるTensor dtype/packingのHub表示差を、学習済みの全パラメータ削除と解釈してはならない。**65Bのモデルが39Bの小型アーキテクチャになったとは言えない**。

本例の原因となる実装計数詳細（packing、scales、tensor types）は本体ヘッダ未取得につき未証明だが、**元モデルの公称全数と量子化チェックポイントのHub自動集計が一致しない**という観測は、150B超モデルの量子化例外判定に直接関わる。原本のMoE全expert・embedding・MTPなど全学習済み構成数を基準とし、実際の保存fileや圧縮後byte数と混同しない。

## 4. 容量判定の計算・次元確認

| 記号 | 意味（日本語） | 単位（SI準拠） | 定義／定義域・前提 | 型 |
|---|---|---|---|---|
| \(P\) | DiffusionGemmaのHF表示概数 | 1（個） | 25,823,800,000、丸められたHub表示、厳密なtensor countではない | 非負実数スカラー |
| \(b\) | BF16の1パラメータ当たり保存byte | byte／個 | 2、同値のBF16 tensor本体を仮定、header/その他不含 | 正実数スカラー |
| \(B_{\mathrm{nom}}\) | BF16想定学習済みtensor payload | byte | \(P b\)、丸め誤差あり | 非負実数スカラー |
| \(B_{\mathrm{repo}}\) | HFサイトの丸め表示repo容量 | byte | 約51,700,000,000、*publisher metadata*で実測ではない | 非負実数スカラー |
| \(H_{40}\) | 旧v40時点の仮想容量余白 | byte | 129,409,767,827、計画額の差、実HDD空きではない | 整数スカラー |
| \(H'\) | 上記仮想余白にモデルを仮加算した差 | byte | \(H_{40}-B_{\mathrm{repo}}\)、外部runtimeやstaging含まず | 整数スカラー |

\[
B_{\mathrm{nom}}=P\,b\approx 51{,}647{,}600{,}000\ \mathrm{byte};
\quad
H'=H_{40}-B_{\mathrm{repo}}\approx77{,}709{,}767{,}827\ \mathrm{byte}.
\]

**導出**：BF16 2byte×25.8238B個＝51.6476×10^9 byte（表示容量約51.7GBと概ね整合）。旧v40の仮想余白129.4098GBからrounded repo 51.7GBを仮控除して77.7098GB。ただし現行v42も物理HDD未測定であり、依存・cache・stagingの必要容量は不明。この数字を**安全な取得許可**として使用しない。**次元チェック**：個×(byte／個)=byte、byte－byte=byteで整合する。

RippleのBF16リポジトリ約130GBは同じ仮想余白129.41GBを**約0.59GB超過**し、他の安全余裕なしで追加する合理性はさらに低い。

## 5. 規制ストレス・取得前の独立停止条件

公開ウェイトが必ず「悪用能力→大規模→全モデル」と禁止されるという事実はない。法的な輸出前登録、Gated権限、民間プラットフォームの削除、第三者利用許諾は別の現象である。[v42の中国MOFCOMとEU一次資料検証](94-v42-ltx-parent-gates-interim-export-policy.md)は維持。今回のDiffusionGemmaは**公開元・Apache-2.0・非Gated listing**を観察しているため、将来の消失確率が高いと捏造することはできない。それでも独立学習済み拡散architectureの学術的保全価値はある。

同じ重みのNVFP4/GGUFを**別学習成果として複数登録しない**。全資産の利用許諾、repo SHA、元データ由来権利、依存runtime、所有者実HDDの200GB空き下限、推論ピークRAM・ユーザー承認を独立ゲートとする。v42の150B超量子化例外審査は独立条件を全て満たす場合のみで、**量子化により総パラメータ数が150B未満になったと誤判定して適用範囲をすり抜けさせない**。

## 6. H / T / D / C / U と ERROR CHECK

**H**：オープン原本のDiffusionGemmaは、v42既存のiLLaDA・Gemma4との重複なしに、ブロック拡散デコードの保存価値を増やす。質的判断は次の比較実験に反証可能。

**T**：今回の最小検証は3候補＋量子化比較1モデル、固定公式card、Google config、22ファイルの構成調査。品質を確定させる次段階の実験案は、同一prompt 50件×3seed、同一GPU/clock、backend/dtype、context、batch=1でinfill/JSON整形/スループットと正確性を記録する。モデル重みは今回取得しておらず、**ベンチマーク未実施**。

**D**：PASS＝3候補を正本に未登録と確認、公開元の根拠・独立学習構成・11shardと固定commit・1ファイルPublisher SHAを記録、全量DL0、現行148資産不変更。UNCERTAIN＝残りfileSHA、量子化計数原因、個人権利と実HDD、GPU測定、差分能力。FAIL＝量子化メタデータだけで総パラメータ削減認定、全SHAなしのapproved lock、無許可取得・実行。

**C**：DiffusionGemmaが既存iLLaDAと実タスクで同等で新規保存価値が見つからない場合、またはGoogle/配布元ライセンスの例外・物理HDD超過で保存不可能な場合、P1からHOLDへ戻す。Areteが既存Qwen群と明確に異なる学習能力を示せば研究優先度を再評価。Rippleは容量交換による利得が証明されれば代替考慮。

**U**：Publisher Hub表示の丸め、ベンチ設定と独立性、モデルfile/header未実査、全zero-point等runtime差、手元HDD・必要一時領域が主な誤差源。反復実測がないため合成標準不確かさ `u_c` と包含係数 `k` は計算不能。

**ERROR CHECK**：3候補既存v42非登録、22候補source中11shard、Publisher SHA取得1／22、原本モデル追加0、選定降格0、重量DL0、取得承認0、main正本v42維持。学際：非逐次モデル学習、デジタル保全、メモリ階層／GPU推論、AI配布契約・規制、統計的比較。

## 7.〈次に考える問い〉

**この51.7GBを使うなら、既存で同一成果の量子化重複をさらに削る方が価値があるのか、それとも独自アーキテクチャ原本を1系統追加する方が将来の復元可能な能力集合を広げるのか？**
