# R130 / v56｜小型無検閲の原本2件を正式条件付き採用・配布元ファイル確定（2026-11-20）

## 1.〈本論〉確定した採否

調査開始時の正本v55（209登録、162有効）へ、**既存209のID／採否／モデル原本を1件も変更せず**、異なる学習済み成果2件を研究限定CONDITIONAL／R0として追加。**正式v56は211登録・164有効（SELECT53／CONDITIONAL111）**。これは取得する権利を承認した意味ではない。全164件の取得前ゲートと、`queues/approved.json`0件を維持。

| 独立original | 不変40桁revision | publisher原本 | LFS SHA256 | 採否 |
| --- | --- | ---: | ---: | --- |
| [FrostWolf LFM3 Abliterated](https://huggingface.co/FrostWolfAI/LFM3-1.7B-abliterated) | `fc0f808655210ef891515bad9b5195b03d89f11b` | 13ファイル **3,475,637,066 byte** | 2件 | R0／CONDITIONAL |
| [Phala Qwen3.8 Uncensored LoRA](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA) | `588752bc181b999247f0e7df578bbc55d2b920e9` | 7ファイル **13,034,727 byte** | 1件 | R0／CONDITIONAL |
| **合計** | Publisher pinned | **20ファイル／3,488,671,793 byte** | **3件** | 正式保存対象の研究選定のみ |

ファイルごとのpath、bytes、Git blob SHA1、LFS重量SHA256は[20ファイル原本manifest](../../manifests/drafts/r130-2026-11-20-frostwolf-and-phala-originals-fixed.candidate.json)に記録済み。原本weightとtokenizerのPublisher SHAは、現時点の「配布元データ」の証拠であり、**所有者HDDでのSHA一致を証明しない**。

### 1.1 FrostWolf：なぜ別モデルなのか

公式重み`model.safetensors`は**3,457,635,448byte／SHA256 `4064371dcfed8660f03d688dd7688aad48cce630fd3117ec30572a976352f165`**。元親[LiquidAI/LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B)@ `1da06bec6a819da10b54c67e5c90972b46d81871`の同サイズの重みSHA256 `135922caef64e81e52af88ede8b7c3ddaa9d6da220a9737fb3065275dbfb4330`とは**内容が異なる**。tokenizerのSHAも相違。HFモデルカード上`base_model_relation: quantized`という表記だけで「通常の元重み再量子化」と決めるのは誤り。出版社の`reproduce/reproduce.json`はHeretic v2.1.0 ARA編集学習とseed/重みSHAを記録している。

別作者[OrcaRouter LFM3-1.7B Abliterated](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated)は**Gated**。編集方法・重みの同一性を確証できず、Orca版は従来どおり正規利用権が得られるまでHOLD。FrostWolfのGGUFはこの同じ学習結果の変換物なので独立資産として登録しない。

公式[LFM Open License v1.0 原文](https://huggingface.co/FrostWolfAI/LFM3-1.7B-abliterated/blob/fc0f808655210ef891515bad9b5195b03d89f11b/LICENSE) §5は、年商 **USD 10,000,000以上**の法人の商用利用を標準ライセンスの許諾対象外とする。再配布時にはLICENSE/権利通知等を維持する義務がある。使用者の業務・商用・研究の行為別権利は未確認。`configuration_lfm3.py`・`modeling_lfm3.py`等のcustom codeは保存候補であって、`trust_remote_code`を自動実行しない。

### 1.2 Phala：13MBだけで復元できるわけではない

発行者7ファイルの中で`adapter_model.safetensors`は**13,014,120byte／SHA256 `1abf13b2191c9973a4dc4d978448512d3ce2efabfd1e671edd5956b6aebfa5ac`**。出版社`SHA256SUMS`と固定リポジトリ情報が一致。`adapter_config.json`の`base_model_name_or_path=Qwen/Qwen3.8-27B`、`revision=37561816e66b5b9153b1b64c10968c18c1e6f4a0`を一次資料で確認。**R129の「Phala親revision未確定」は訂正**。ポートフォリオの親Qwen参照版と同じである。

ただし作者の性能試験は`Qwen/Qwen3.8-27B-FP8@017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`、NVIDIA H200上の専用SGLangを使用。Windows利用者のCPU/GPUやBF16親での実行成功、推論品質、ピークメモリは未検証。**親27B原本は取得成功61モデルのログに含まれておらず**、13MBアダプターのみの完全保存は不可能。

[Phala公式NOTICE](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA/blob/588752bc181b999247f0e7df578bbc55d2b920e9/NOTICE)はAdapter重みにApache-2.0を適用し、学習用`harmless_alpaca`がStanford Alpaca由来CC BY-NC 4.0であることとAdvBenchの出自を明示。Adapterに当該NC条件が法的に自動継承されると断定しないが、**利用行為ごとの権利審査は必須**。

## 2.〈応用・転用例〉原本の保存・交換・追加順序

**正式採用：2件**。同じ編集済み重みのGGUFやmerged FP16は別の学習済み成果ではないため採用しない。FrostWolfの親LFM3と編集後BF16はどちらも保持価値がある。Phalaは既存Qwen親をSHA再利用できた場合だけの小容量増分が約13.035MB。元親が無い実物環境では新たに親原本の保全が必要。

**追加取得の判断順**：(1)既存61件のGitHub取得履歴と所有者ドライブのSHA照合、(2)FrostWolfの13固定ソースとライセンス、(3)Qwen親の18+原本付属ファイルとPhalaの7sourceの確認、(4)コード安全性／実行ABI、(5)権利・容量・明示承認後のみダウンロード。モデルごとの反復確認は不要だが、承認manifestに含めた範囲以外の転送は禁止。

**現時点では正式カタログがCONDITIONALであることを、DL解禁と混同しない**。`queues/proposed-v56-2026-11-20.json`は非実行候補、`queues/approved.json`は空。

## 3. 政策の事実と仮説

米BISの[2026-11-19公布の規則 §IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は旧AI Diffusion Ruleのモデル重み規制ECCN 4E091を撤回。遠隔計算・輸出先・用途別の規則は独立する。全公開モデルの私的所有禁止が成立したという証拠ではない。**将来のホスト制限強化の確率は不明**。選定順位は観測されたアクセス・原本の独自性・全ソース保全価値・容量に基づくストレス設計である。

## 4. 変数表と次元チェック

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・条件 | 型 |
|---|---|---|---|---|---|
| `S_F` | FrostWolf原本ソース量 | byte（8 bit） | 3,475,637,066 | 非負整数、元repo全13ファイル | 整数スカラー |
| `S_P` | Phala原本ソース量 | byte（8 bit） | 13,034,727 | 非負整数、元repo全7ファイル | 整数スカラー |
| `S_T` | 新規選定ソース論理量 | byte | `S_F+S_P` | 3,488,671,793、実HDD増分でない | 整数スカラー |
| `N_F` | FrostWolf学習済み総要素数 | 1（無次元） | 1,728,801,536 | Hub BF16 serialized tensor census | 整数スカラー |
| `N_B` | 親Qwen学習済み総要素数 | 1（無次元） | 27,781,427,952 | Hub BF16親の全要素数 | 整数スカラー |
| `B_A` | LoRA重量ファイル長 | byte | 13,014,120 | Header含む、正確なtensor要素数は未集計 | 整数スカラー |
| `N_U` | 親＋LoRAの保守的学習済み要素上界 | 1（無次元） | `N_B + 8 B_A`（1bit/要素の上界換算） | 他の独立学習済み依存がない場合 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 対象変数依存 | 未測定 | 反復実機評価なし | 実数／欠損 |
| `k` | 包含係数 | 1（無次元） | 未設定 | 統計誤差モデル未確定 | 実数／欠損 |

**算術と次元**：`S_T=3,475,637,066+13,034,727=3,488,671,793 byte`。Phalaは`N_U=27,781,427,952+8×13,014,120=27,885,540,912`要素で、仮定下では150B基準より小さい。byte×8bit/byte÷1bit/parameter＝パラメータ個数となり次元は一致。これはRAM、VRAM、評価品質、完全オフライン復元の認証ではない。

## 5. H／T／D／C／UとERROR CHECK

**H**：異なる学習結果の小型BF16原本とrank3 Adapterの原本を固定すると、既存Qwen/LFM親と比較可能な修正後モデルを約3.489GBの追加sourceで記録できる。  
**T**：Publisher全20ファイルと3 LFS SHA256、対象の40桁revision・LICENSE/NOTICE・親revを一次照合（n_min=20）。User Dドライブでは全選択pathの実SHAを再確認。定量性能は同一HW/clock/backend/quant/zero-point/context/batch条件で日本語/英語の安全過剰拒否・正常タスク各30件以上、差を事前登録。権利／SHA／200GB残床／依存停止のどれかで逐次停止。  
**D**：PASS_METADATA＝209旧ID全不変、追加2件独立、計211／164、2repo20 files、3 SHA、明示的親revision。FAIL＝誤SHA・Gated回避・商用条件違反・無断転送・異なる版の親を動作確認なしに使用。UNCERTAIN＝本人の正規取得資格、owner HDDと完全復元、実測品質。  
**C**：公開された拒否率は最適化trialや作者判定者に過適合の可能性。PhalaはBF16親とのruntime互換性不足で復元できない場合がある。  
**U**：実体保存先、学習データ契約の適用範囲、再現性、GPU/ABI・code、出版社ベンチ選択バイアス。反復実測がないため合成`u_c`と`k`の数値算定不可。

**ERROR CHECK**：旧209件全レコードJSON一致、新2件、211登録164有効（SELECT53／CONDITIONAL111）。配布元20ファイル・3公開SHA、総3,488,671,793byte。Gatedの追加0、承認キュー0、モデル実重量取得0、コード実行0、過去ファイル削除0。現物HDD/オフライン再現は検査していない。

関連分野は**機械学習の系譜（親と後学習）・情報法（LFM/NC/配布規約）・供給網セキュリティ（静的コード、SHA、ABI）・デジタル保全（重複除外・完全復元）**。

## 6.〈次に考える問い〉

既存Qwen親が将来DドライブでSHA検証済みとなった場合、Phalaの13MB Adapterと55GB級の新しい別フル原本のどちらが、追加1GB当たりの性能と独立性を改善するか。

**要約**：FrostWolfのLFM3 ARA後学習済みBF16全13ファイルとPhala rank3 LoRA全7ファイルを、発行者の40桁revision、原本weight SHA、権利原文で固定した。v55既存209件を不変更にして2件をv56研究CONDITIONALへ追加した。Qwen親の参照revが明示されていた点を訂正し、無検閲モデルの量子化重複・アクセス規制の誤認を防いだ。本人権利・物理保存先・offline実行・実ダウンロードのゲートは引き続き全件STOP。
