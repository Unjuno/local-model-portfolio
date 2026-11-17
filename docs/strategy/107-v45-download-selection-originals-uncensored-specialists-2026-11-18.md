# R107｜v45・151有効資産の「何を取得すべきか」を先に確定する非実行選定（2026-11-18）

**決定**：正式`main`／`catalog/CURRENT.json`→v45 **198登録／151有効（SELECT53＋CONDITIONAL98）**を維持し、既存14件の**ダウンロード対象となりうる原本ファイル名・publisher 40桁commit・byte・SHAを研究用に具体化**した。**これはモデル保存の選定、すなわちファイル単位の選択であり、ユーザー本人の合法的取得承認や実行可能manifestではない。** `queues/approved.json`は0件、所有者HDD・最終dependency bundle・local SHA・offline restoreも未検証。

[全151件の排他的な第一停止要因と14件の推奨ファイルスコープ](../../catalog/decisions/2026-11-18-r107-v45-final-source-selection-and-download-gates.json)、[無検閲／独立学習済みセキュリティ4原本の固定SHA・byte](../../manifests/drafts/v45-2026-11-18-r107-uncensored-and-small-specialist-source.candidate.json)、[既存小型10モデルの107ファイルpublisher source](../../manifests/drafts/v45-2026-11-18-r106-first10-publisher-source.candidate.json)。

## 1.〈本論〉— どのモデルを保存対象として確定するか

規制されそうな印象やHFダウンロード数だけでは選ばない。採用軸は①保存先の独自学習済み能力（原本／後学習／特殊編集）、②利用行為の合法性とGated本人認可、③1種類のoriginal重みで復元するための必要component/ABI、④選択ファイル実容量とSHA aware重複、⑤同条件の品質証拠、⑥未来の配布制限は確率付けしないシナリオの順。

**選択スコープが確認できた14件（取得許可は未付与）**：

| 調査順 | モデル／公開元 | 選択ファイル | publisher source | 役割 |
|---:|---|---:|---:|---|
| 1 | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 5 | 17.177 GB | 無検閲原本 |
| 2 | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | 5 | 17.738 GB | 無検閲原本 |
| 3 | [`usezn/Galvanize-3`](https://huggingface.co/usezn/Galvanize-3) | 9 | 0.597 GB | 小型セキュリティ |
| 4 | [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | 9 | 0.671 GB | 非商用LoRA |
| 5 | [`KRAFTON/Raon-1-nano`](https://huggingface.co/KRAFTON/Raon-1-nano) | 17 | 7.182 GB | 専門原本 |
| 6 | [`abel-lab/Simons-297M`](https://huggingface.co/abel-lab/Simons-297M) | 6 | 1.189 GB | 専門原本 |
| 7 | [`autogluon/chronos-2`](https://huggingface.co/autogluon/chronos-2) | 4 | 0.478 GB | 専門原本 |
| 8 | [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 12 | 1.207 GB | 専門原本 |
| 9 | [`Qwen/Qwen3-Reranker-0.6B`](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | 14 | 1.207 GB | 専門原本 |
| 10 | [`openai/whisper-large-v3-turbo`](https://huggingface.co/openai/whisper-large-v3-turbo) | 13 | 1.622 GB | 専門原本 |
| 11 | [`ibm-granite/granite-speech-5.0-470m-turboctc`](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) | 9 | 0.948 GB | 専門原本 |
| 12 | [`lightonai/LightOnOCR-3-0.8B`](https://huggingface.co/lightonai/LightOnOCR-3-0.8B) | 14 | 1.736 GB | 専門原本 |
| 13 | [`google/siglip2-base-patch16-224`](https://huggingface.co/google/siglip2-base-patch16-224) | 9 | 1.539 GB | 専門原本 |
| 14 | [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base) | 9 | 0.907 GB | 専門原本 |
| | **合計14モデル** | | **54.200 GB** | **全量自動取得禁止** |

この54.200GBは14件の論理publisher source bytesの単純和で、同じ重みの別形式を省いた選択である。既にv45のアーカイブ計画対象になっている資産もあり、**別途54.2GBを予算に追加計上する根拠にはならない**。Git/LFS SHA重複や既存HDDを使う純増bytesは未測定。条件の整わないモデルを「すぐにダウンロード可」と呼ばない。

### 無検閲・拒否制御編集のモデル選定

1. **[0bserverx RVN Heretic](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)**：固定版`ab8d7bd81d03117501e4da60cccdff4c80f0eea0`の`RVN-Q4_K_M-multilingual.gguf` **16,547,400,224byte**と必要に応じ`mmproj-Qwen3.8-27B-Q8_0.gguf` **629,247,008byte**、README・chat template・Git provenanceのみ。配布元**182ファイル1,645,270,647,302byte**を丸ごと取得するのは極めて非合理的。今回選択5ファイル **17,176,701,230byte**、残りの**1,628,093,946,072byte**を選択から除外。既存の旧`Qwen3.8-27B-Heretic-Q4_K_M.gguf`は作者自らlegacy別チェックポイントと説明しており、**現行RVNと取り違えない**。作者報告の二度追加ARA・100問0～1拒否・KL0.0085は**独立測定でない**。同量子化ファミリーQ5/Q6/Q8、GSQ、MTP等を二重保存しない。
2. **[InterpreticAI selective political edit](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)**：固定版`7057fd1235dccb303a6c106eeb7967790c202567`。Q4 model、F16 mmproj、SHA256SUMS・README・Git属性の5ファイル **17,738,329,643byte**。著者の113問実験では政治的回答抑制が98から4に変化（中国語・LLM judge）。これは汎用有害依頼の無制限応答でも事実正確性の検証でもない。GPQA/MMLUのBF16出典値をこのQ4の同条件品質と誤認しない。
3. **[OrcaRouter 27B](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored)**：別の独立編集済みBF16原本だが**現在Gated**。55GB級であるため、本人の正規承認・利用条件・最終byte確認より先にキューへ投入しない。無検閲3ファミリーを同じQwen出自という理由だけで一律削除しない一方、定量的同一タスク比較なしの全形式多重取得はしない。
4. **[knoveleng 9B abliterated](https://huggingface.co/knoveleng/Qwen3.5-9B-Uncensored)**：小型で約17.9GBだが作者の拒否率97%→12%と同時にperplexity16.26→21.26（悪化）、HFのLICENSEタグが空欄で原本READMEがQwen親ライセンスへ委ねる。**現行HOLD維持**。本来の性能保存に反する危険があるため「無検閲」だけで追加しない。
5. **[DavidAU Qwen3.8 27B](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU)**：独立多段階編集は存在するが、原BF16全repo**55,593,410,848byte**で作者のベンチ・マーケティング数値は同一条件再現が不十分。既存Orca、Interpretic、0bserverxとの差分評価と実容量証拠まで調査維持、直ちに選択file優先に上げない。
6. **[ChatR Labs Qwen-Image 2.1 Omni LoRA](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1)**：新しい実体固定`d6f9c7e4e420971b49c3df9ace6b566b3f2eda48`で**9ファイル671,183,504byte**。Rank128独立学習アダプターを選択し、親のQwen Image2.1原重みをLoRAごとに重複取得しない。**Qwen Research License非商用研究／評価用途のみ**、親のencoder/VAEとDiffusers runtimeの完全閉包が必須。作者の画像評価は35 steps/CFG5等の指定があり、SFWでbaseに劣るとの負の結果を隠さない。

**別機能の小型専門**：[usezn/Galvanize-3](https://huggingface.co/usezn/Galvanize-3)はprompt-injection検出の独立140.6M ModernBERT原本で、publisher固定`597237be3b0fabbf5d70ff16ce95fad14a591f20`。**9ファイル597,001,839byte**には原本`model.safetensors`・Apache2 LICENSE／NOTICE・tokenizer・**thresholds.json**を残す。作者は閾値0.9802と最大512 tokenを定義。同じ訓練済み重みの`onnx/model.onnx`563,102,066byteは初期原本候補から除外し、必要なら再現性検証付きで任意形式として別管理する。

## 2. Gated・専門・大規模モデルの次順位（取得承認ではない）

| 実際のモデル | 優先する作業 | 反証・停止条件 |
|---|---|---|
| NVIDIA Ising ColorCode＋SurfaceCode（別学習の量子誤り訂正） | **権利確認P0**。現在Gated表示の二原本は合計数MBの希少な独立学習成果。 | 適法な本人アクセス承認がない限り重み取得は禁止。モデルLICENSEは版ごとに異なる可能性がある。 |
| Runway Praxis DROID／NVIDIA Cosmos／IFM PAN2 | 独立の行動・世界モデルを維持。PAN2は35候補ファイル約86.08GBが出版社SHA固定済み。 | Gatedと外部VAE／視覚encoder／CUDA・ライセンス、Owner HDD/一時stage不明。旧Wan nativeと同名で勝手に重複削除しない。 |
| ChrisColeTech／StuubsのLTX2.5音声同期編集版 | 同じベースでも違う後学習結果の可能性を研究。 | Gemma4 encoder／VAE・親Gated・全学習済み総数・派生ドナー条件が未閉包で、9件のunknown parameter gateに残る。 |
| `orcarouter/Qwen3.8-Flash-Next-Uncensored`（180B）／Mistral Large4（約1T） | 現行基準は**150B以上も量子化済み例外のみ個別検証**。 | 同一HW/backend/context/batchで、指定の150B未満モデル以下の実測完全ピークRAM、512GB未満・品質速度・権利・本人許可すべて必要。現状HOLD。 |

**151件の最新排他的作業区分**：[JSON台帳](../../catalog/decisions/2026-11-18-r107-v45-final-source-selection-and-download-gates.json)に、選択原本14、本人のGated認可が先行19、完全学習済み総数が不明でSTOP9、残り原本/ABI未閉包109を一意に記録。Gated全体は20件（うち1件が総数不明に先に分類）であり、優先順位の合計は151。有効資産の既存採否そのものは変更しない。

## 3. 制限リスクの一次情報と反例

**現在の事実**：Gatedはモデル作者による現行アクセス制御、CC BY-NC／Qwen Research License／Apacheと学習済み依存の契約は別条件。2026-11-15 [米BIS高度計算基盤への遠隔アクセス規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)はローカル公開ウェイト一律所有禁止と同じではない。[EU AI Act GPAIオープンソースFAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は適用の条件と免除を分ける。[Hugging Face Gatedの公式説明](https://huggingface.co/docs/hub/models-gated)によれば本人の申請・承認を要する場合がある。

**仮説**：拒否制御編集→高能力モデル→公開ウェイト全般へ配布制限が拡大する3波はストレス試験用であり、各モデルの未来の消失確率・削除予定日を得る根拠はない。競争環境では公開拡大・条件緩和・アクセス復旧の反例もある。特殊モデルを優先するのは**能力の独自性と復元困難性**であり、悪用されるから禁止されるとの断定ではない。

**調査の制約**：今回ユーザー指定のExa検索・URL取得は**ともにHTTP402で利用枠枯渇**。利用可能なHF連携のrepo表示とHugging Face配布元一次API/固定README・既存の政府機関ソースで確認し、Exaによる追加検証済みとは記述しない。新モデルの網羅性は保証しない。

## 4. 変数表・容量検算と再現性

| 変数 | 日本語の意味 | SI単位 | 定義・定義域・前提 | 型 |
|---|---|---|---|---|
| \(N\) | 有効選定資産総数 | 1（件） | v45、151件、整数 | 非負整数スカラー |
| \(N_f\) | publisher原本ファイルを14資産で選択した件数 | 1（件） | 14、別途合法性未確認 | 非負整数スカラー |
| \(B_{10}\) | 既存R106の10原本selected-source bytes | byte | 18,016,810,996、全runnerは未閉包 | 非負整数スカラー |
| \(B_4\) | 今回R107の無検閲・Galvanize原本4件selected bytes | byte | 36,183,216,216、承認済みHDD使用ではない | 非負整数スカラー |
| \(B_{14}\) | 14原本選択候補の単純合計 | byte | \(B_{10}+B_4\)、別形式を多重選択しない | 非負整数スカラー |
| \(C\) | 保存用HDDの計画上限 | byte | 4,000,000,000,000、実機測定値ではない | 非負整数スカラー |
| \(F\) | HDD空き容量の最低床 | byte | 200,000,000,000、実測未確認 | 非負整数スカラー |

\[
B_{14}=B_{10}+B_4=18{,}016{,}810{,}996+36{,}183{,}216{,}216
=54{,}200{,}027{,}212\ \mathrm{byte}.
\]

**次元チェック**：byte＋byte＝byte。モデル数は単位1でありbyteに加算しない。14モデルは全てv45既存151有効内であり、53/98採否とは別の**選択ファイル粒度**を示す。源source容量と実増分保存byteは等しいと限らず、旧v45予算の仮想余白約27.4GBから上記を差し引くことは**二重計上**になりうる。Ownerの実HDD容量／cache／stage／重複SHA-aware union未検証のため全量取得可能とは判断しない。

## 5. H/T/D/C/U・ERROR CHECK

**H（反証可能）**：最初に14件の独立学習成果の原本ファイルと行為別権利を確定する方が、同一元重みの全GGUF／ONNX形式を取得するより、復元可能能力を増やす。対象v45全151件。

**T（最小検証）**：14件の固定publisher source群、現行151件readiness／98件CONDITIONALアクセス／承認キューをID単位1対1照合。モデル品質の独立テストは同一目的の各モデルにつき事前に固定した30入力×3seed、同一HW/clock、CUDA／backend version、quantizer zero-point、contextとbatch固定、中央値・95%CIを比較し、法律・安全性不備があれば逐次停止。本ターンは重み取得・実測ゼロ。

**D（PASS/FAIL/UNCERTAIN）**：PASS＝151 ID一意、14 exact snapshot candidate scopes＋publisher SHA、Gated本人認可必要19/合計20、9総数未確定、ONNX/余分な量子化回避、approved0。FAIL＝未確認権利や規制確率を「合法」「禁止確定」と認定、Gated bypass、過剰モデル全repo download、第三者コード実行。UNCERTAIN＝個別の法的行為、全学習済み総数／実同質比較、実HDD・復元。

**C（破れ方）**：独自学習済みと思った編集版が実際に同一ウェイト、Q4品質劣化で実用不能、第三者契約で許諾なし、無料モデルの別配布先が同一SHA合法的復元可能、完全ディスク容量不足等が判明した場合は順位・保存形式を再評価。

**U（主要不確かさ）**：HF表示と実ファイルの版差、出版社ベンチと実機、暗黙の依存wheelhouse、Gated本人認可、オリジナル権利／再配布・商用条件、HDD formatted容量・staging・キャッシュ。反復分散が測定されていないため合成標準不確かさ `u_c` と包含係数 `k` は未算定。

**ERROR CHECK**：v45=198登録/151有効、うち14件ソース選択、取得承認0、モデル重量ダウンロード0、実行0、local SHA/オフラインrestore0、Gated20・総数未確定9。全員の行為別権利承認は0。**研究用ファイルスコープ選定を「取得済み」「取得許可済み」と称しない。**

関連分野：モデル後学習・アライメント、サプライチェーンハッシュと技術保存、統計的性能評価、国際AI政策・著作権、GPU/CPU推論実装。

## 6.〈次に考える問い〉

**独立した拒否制御編集の27Bを2系統保持する約35GBの追加ソース価値は、既存の無検閲編集原本／小型モデルとの同条件品質測定によりどこまで実証できるか？** 結果が得られた場合だけ容量超過の代替案を確定する。
