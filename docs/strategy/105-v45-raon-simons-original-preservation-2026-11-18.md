# R105｜正式v45：Raon-1 nanoとSimons-297M原本の条件付き選定（2026-11-18）

**決定**：`main`の旧v44（196登録・149有効）を保持し、**独立学習済み原本2件を追加**したv45（198登録＝172モデル＋26データ／151有効＝SELECT53＋CONDITIONAL98）を構成。どちらも研究段階`conditional`であり、**承認された重量取得・モデルコード実行・本人のLICENSE承認・オフライン復元は0**。現行[取得前全151件停止台帳](../../catalog/readiness/v45-2026-11-18-r105-all151-gates.json)、[条件付き98件のアクセス調査](../../catalog/access/2026-11-18-v45-conditional-hub-gates.json)、[非実行提案キュー151件](../../queues/proposed-v45-2026-11-18.json)。

一次資料：[*公開元の不変revisionと全23候補ファイル*](../../manifests/drafts/v45-2026-11-18-raon-simons-original.candidate.json)、[*比較研究・保留候補6件*](../../catalog/research/2026-11-18-r105-raon-simons-primary-selection-and-alternatives.json)、[v45正式選定差分](../../catalog/revisions/v45-2026-11-18.json)、[派生した198件正本](../../catalog/effective-portfolio-2026-11-18-v45.json)。

## 1.〈本論〉— 訓練済み重みの中身による採用判断

| 新規CONDITIONAL | 既存にない保存価値 | 配布元の構成・権利・取得停止 |
|---|---|---|
| [KRAFTON/Raon-1-nano](https://huggingface.co/KRAFTON/Raon-1-nano) | RDA（Delta Rule）18層＋Gated MLA 6層、4-stream Raon-mHC、256次元学習済みper-layer embedding。Raon miniからMoE-to-dense蒸留してさらに3T token継続事前学習しSFT/強化学習。既存LFM3/RWKV7/Mamba/Qwenの単なる量子化・再配布ではなく、言語系の構造多様性を保全。 | [公式版 `39f897a1f835c723ec633c6c905dca7312bd9fd7`](https://huggingface.co/KRAFTON/Raon-1-nano/tree/39f897a1f835c723ec633c6c905dca7312bd9fd7)はpublic・非Gated・Apache-2.0原本。全23ファイル7,182,768,857byteから説明画像6ファイル642,200byteを除外し、**17ファイル7,182,126,657byte**を保存候補とする。Pythonのカスタムremote code、PyTorch/CUDA/Transformersは安全・互換未確認。 |
| [abel-lab/Simons-297M](https://huggingface.co/abel-lab/Simons-297M) | 32時点patchの因果Transformer＋変量間attention、未来既知共変量と9分位点、WiSE-FT後学習の独立確率的予測重み。既存Chronos-2、Granite TTM、Kumo Anomalyと異なる学習済み原本で、訓練コードの公開によって研究上の再現可能性を高める。 | [公式版 `335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a`](https://huggingface.co/abel-lab/Simons-297M/tree/335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a)はpublic・非Gated・OpenMDW 1.1。全12ファイル1,189,519,836byteから説明画像6ファイル567,876byteを除外し、**6ファイル1,188,951,960byte**。外部実行コードは[Abel-ai-lab/Simons固定commit](https://github.com/Abel-ai-lab/Simons/commit/0d0042f8da45140172bd36980be08654c0017d8b)。 |

両者は**性能ランキングだけで採用したのではない**。原本学習過程、アーキテクチャ、用途の独立性、publisher SHAを固定できる小容量という条件を満たすための研究採用である。著者ベンチ値と同条件の実測値は異なり、ここで独立速度優位・品質非劣性を主張しない。

### Raonの「3.2B」表示とHub内部集計は一致しない

Raon作者モデルカードは3.1B主モデル＋MTP約55Mで「3.2B」と記載する。一方、現在のHF配布元APIの`safetensors.total`は**3,529,911,376 elements**、[主モデルindex](https://huggingface.co/KRAFTON/Raon-1-nano/blob/39f897a1f835c723ec633c6c905dca7312bd9fd7/model.safetensors.index.json)は**996個のtensor key／主重み3ファイル**を参照し、`mtp/model.safetensors`は別ファイルに存在する。原因には tied LM headの保存形式や著者の数え方の違いが考えられるが、**同一の「正確なユニーク学習済みパラメータ総数」とは証明していない**。

主重みは2分割shardと`model-tied-lm-head.safetensors`、別MTP 1ファイル。モデル原本3ファイルとMTPの公開SHA256を確認したうえで、いずれも同一revisionの候補に残す。BF16/F32 mixedと添付MTPを扱うため、量子化版のHub集計や「1.5B effective」だけでローカル150B総数screenを判定しない。完全tensor censusは取得後の安全な**非実行ヘッダ監査**まで未確定、取得前の研究screen PASSと本体取得許可は別ゲート。

### Simonsのライセンスは訓練データ全体に一律適用されない

[Simons LICENSE原文](https://huggingface.co/abel-lab/Simons-297M/blob/335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a/LICENSE)のOpenMDW 1.1は配布資料への広い許諾を与える一方、通知保持、第三者権利・訴訟に関する条件がある。[NOTICE原文](https://huggingface.co/abel-lab/Simons-297M/blob/335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a/NOTICE.md)ではERA5、ODbL、CC BY-SA等の訓練データ原著作権・表示義務を明記。[Simons-Pretrain](https://huggingface.co/datasets/abel-lab/Simons-Pretrain)は**独立データ集合**であり、モデルのOpenMDWだけで全データの再配布許可とみなして一括取得しない。ソフトウェアと訓練データの固定版閉包は未完了。

## 2. 他候補を足さない理由と交換保留

| 調査候補 | 今回の判断 | 理由 |
|---|---|---|
| [Salesforce SOV-Transcribe-1](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1) | **HOLD** | Whisper音声encoder＋Gemma4 MoE原本でHF 26.63B、公開repo**53,317,410,780byte**。独立したスタイル制御ASRだが、既存Whisper/Qwen3-ASR/Granite Speechと同条件品質比較が必要。v44仮想余白約39.41GBを全repoだけで上回る。 |
| [Meituan LongCat-Video-Avatar-1.6](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6) | **HOLD** | MIT公表、音声駆動のDMD/OPSD LoRAが独自学習成果。ただしrepo約77.6GBにINT8重複／別ベース・Whisper依存があり、**学習差分のみの合法・完全な復元bundle**と既存動画モデルの増分評価が未確認。 |
| [Continuous Intelligence ci-proto](https://huggingface.co/ContinuousIntelligence/ci-proto) | **HOLD** | 167M時系列は長文コンテキストが魅力でも、独自`ci-proto Code and Model Licence`とcheckpoint安全性、教師データ・予測誤差の再検証が不足。Simonsを先行。 |
| [internlm/Sage-S2.1-Flash](https://huggingface.co/internlm/Sage-S2.1-Flash) | **150B超の特例不成立につきHOLD** | 科学マルチモーダルの元MoEの公開元表示321.323Bは150B超。activeパラメータやFP8サイズだけでは通らず、現行量子化例外に必要な同一HW・正確な総数・品質・実測メモリがない。 |
| Qwen4-Max | **重み未公開で対象外** | 2026-11-16発表はAPI提供で、2.4兆の公称総数、ローカルで固定可能なモデル重みは確認できない。 |
| Huawei CloudRobo WM1.2 | **継続調査HOLD** | 報道上の11-16公開発表はあるが、現行モデルを特定できる`openpangu/CloudRobo-WM1.2`はHFモデルID未解決。作者の宣伝をそのまま重みSHA確定としない。 |

前回提案の[DiffusionGemma](98-v42-discrete-diffusion-and-november-originals.md)は、独自ブロック拡散アーキテクチャの**P1研究価値を維持**する。ただし公式BF16全repo約51.7GBは、v44 PAN2追加後の仮想余白39.41GBを既に上回る。今回は小型Raon＋Simonsの8.371GB原本を優先し、**DiffusionGemmaを「消滅リスクが高い」だけで無理に押し込まない**。モデル機能の優越性や入替で増える空き容量が実証された時点で再検討する。

## 3. 使用容量・計算の変数表と次元チェック

| 記号 | 意味（日本語） | 単位（SI） | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| \(C\) | HDD計画上限 | byte | 4,000,000,000,000。所有者実HDD容量ではない | 非負整数スカラー |
| \(F\) | 保持すべき最低空き床 | byte | 200,000,000,000。実測前 | 非負整数スカラー |
| \(B_{40}\) | v40時点の歴史的・仮想的保存計画額 | byte | 3,670,590,232,173。実HDD使用済みとは別 | 非負整数スカラー |
| \(R_{44}\) | PAN2の暫定保存上限予約 | byte | 90,000,000,000。全依存には未確定 | 非負整数スカラー |
| \(R_{45}\) | 今回2モデルの暫定追加予約 | byte | 12,000,000,000。source候補8.371GB超の仮予約で実容量ではない | 非負整数スカラー |
| \(S_{45}\) | 今回2モデルのpublishersourceファイル総byte | byte | 8,371,078,617（Raon7,182,126,657＋Simons1,188,951,960）。重みローカルSHAは未測定 | 非負整数スカラー |
| \(H_{45}\) | 理論的余白 | byte | \(C-F-B_{40}-R_{44}-R_{45}\) | 整数スカラー |

\[
S_{45}=7{,}182{,}126{,}657+1{,}188{,}951{,}960=8{,}371{,}078{,}617\ \mathrm{byte}.
\]

\[
H_{45}=4{,}000{,}000{,}000{,}000-200{,}000{,}000{,}000-3{,}670{,}590{,}232{,}173-90{,}000{,}000{,}000-12{,}000{,}000{,}000=27{,}409{,}767{,}827\ \mathrm{byte}.
\]

**解釈**：仮想残余約27.41GBは実物理ドライブの空きではない。大部分の既存資産の最終選択ファイルbyte、重複SHA、runtime wheelhouse、解凍用stage等を含まないため**4TB合格ではなくUNCERTAIN**。源候補の8.371GBと、予約額12GBを足し合わせて二重計上してはいけない。

**次元検査**：各加減算はbyteのみで整合。モデルパラメータは無次元個数、checkpointのbyteとは型・dtype・ヘッダ／quantizerによって変換係数が異なるため、混同しない。

## 4. 実装前提と取得前の完全性チェック

Raonの作者例はPython3.12／PyTorch2.13（CUDA13.0）／Transformers5.16.1／Accelerate1.15、カスタム`modeling_raon1_nano.py`を`trust_remote_code=True`でロードする。**このコードは実行せず保存研究のみ**。Zero-point、tokenizer、MTP分離、KV/RDA内部state、batch、device dtype、CPU offload、max context、driver ABI、dependency wheelhouseの厳密な整合は不明。

SimonsはPython `simons` packageでPyTorch CPU/GPUをサポートするが、Python package commitとwheel hash、推論ABI、モデル`model.safetensors`の安全な読み込み経路を固定してから検証する。著者のA100でのspeed報告は利用者HW測定値ではない。選定済みASR／時系列／言語の代替比較では同一HW/clock、量子化方式とzero-point、context、batch、seed、最低30反復と中央値・幅を要求し、**現時点ではベンチ実行0**。

取得前に必要なのは、本人の合法的な保存行為確認、最終bundleの全SHA・bytesと第三者学習済み依存閉包、ユーザーの実HDD空き・staging測定、明示的な承認済みmanifest、取得後のlocal SHA確認、サンドボックス復元テストの順。条件を一つでも満たさなければSTOP。

## 5. 規制政策の事実とストレス仮説

モデル配布元がGatedにする権限と、国の輸出技術登録・AIシステム用途規制・オープンウェイトの保存自体の禁止は異なる。既存[v42一次政策調査](94-v42-ltx-parent-gates-interim-export-policy.md)が検証した中国の2026年技術輸出前登録制度と、EU AI Act GPAI提供者義務は**全ての公開ウェイトが一律に私的保存禁止になった根拠ではない**。2026-11-18の両モデルHF publisher表示はpublic非Gated。将来削除・規制確率は数字を捏造せず、OpenMDW/Apacheライセンスの権利条件を保存する。

学際性：①非逐次・混合Attention/生成モデルの学術的再現、②時系列統計・確率予測、③デジタルアーカイブ/ハッシュ供給網、④国際ライセンス・AI規制、⑤GPU/CPU実行ABI・機器容量管理。

## 6. H / T / D / C / U・ERROR CHECK

**H（反証可能仮説）**：既存原本を維持し、異なる注意機構のRaonと異なる学習法のSimonsだけを追加すれば、同一重みの量子化複製を追加するより再現可能な学習成果の多様性を高められる。

**T（最小検証）**：HFモデル2個、元ファイル23＋12＝35、選択17＋6＝23、LFS SHA計6、公式LICENSE2、Simons NOTICE、モデルカード／既存比較群を静的検証（n=2）。次段階で各独自タスク30入力以上、3 seed、同一backendとHW条件で独立性能測定し、違反・再現失敗は停止。

**D（合否）**：PASS＝2リポジトリ原本ID・固定40文字revision・23選択ファイル8,371,078,617byte・6 LFS SHA／旧196全保持・v45で198件・有効151・CONDITIONAL98・Gated20・未知総数9・approved0。FAIL＝無許可DL、外部訓練データの一括取得、別GGUF/MLXの重複新規採用、パラメータeffective値だけの150B判定、技術原本をコード実行可能と決めつける。UNCERTAIN＝本人の権利、最終不変bundle、実HDD、全学習済みtensorの厳密計数、実行速度と安全性。

**C（破れ方）**：Raonが他の選定済みcheckpointと同一重みであった、Simonsの訓練データに未解決の権利衝突があった、実際の実行環境や本人HDD不足でオフライン復元不能、独立比較で実質重複と判明した場合はHOLDへ再分類。

**U（不確かさ）**：作者ベンチの試験設定・モデルカードとHub tensor count差、シード分散・backend互換・ライセンス地域性・原データ出自・HDD formatted capacity。反復測定分布がないため合成標準不確かさ `u_c` と包含係数 `k` は算定不能。

**ERROR CHECK（静的）**：入力v44=196/149、追加2=198/151、R1 104、S3 active36、CONDITIONAL98、SELECT53、published SHA6件、選択source 23ファイル、実HDD検証0、licensed user approvals0、weights DL0、runtime execution0、approved queue0。モデル個別Gated状態はpublisher metadata観察であり本人の認可ではない。

## 7.〈次に考える問い〉

**新規モデル追加による保全の幅を広げる作業と、既存151資産の取得前ゲートを解消する作業のうち、次にどちらが実際の「将来復元できる学習済み原本数」を多く増やすか？** 現時点では未通過ゲートと実HDDを優先して測るべきである。
