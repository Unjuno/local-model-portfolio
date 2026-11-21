# R141｜v59・76取得報告を反映した無検閲小型原本の保存判断（2026-11-21）

**正本：v59／221登録・174有効（SELECT53、CONDITIONAL121）**。[v59選定差分](../../catalog/revisions/v59-2026-11-21.json)／[新規4調査対象の不変source](../../manifests/drafts/r139-2026-11-21-inkling-micro-edits-and-deepseek4b-varloop.candidate.json)／[76取得報告に対する21配布元324ファイルの優先スコープ](../../queues/proposed-v59-r140-ledger76-next-21-deduplicated-sources.json)／[機械可読採否](../../catalog/decisions/2026-11-21-r141-v59-small-edit-and-ledger76-selection.json)。本書はPublisher metadataをもとにした**非実行・未承認のモデル選定**であり、Ownerドライブ現物・利用権・動作・品質検証ではない。

## 1.〈本論〉容量効率ではなく独立に保全できる状態で優先する

現在の[取得実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**76モデル／1,078 files／1,657,769,112,167 bytes**をVERIFIED報告している（Gated HOLD1件）。台帳の空き最小値は**1,313,320,169,472 bytes**だが歴史値であり、今回ユーザーDドライブを独立re-hashしていない。v58正式218資産の選定は変えず、重複・大容量の追加モデルより小型の異なる学習済み結果と可逆的編集差分を検討した。

| 採否 | 出版社一次原本 | 固定revision | 実際に選んだpublisher固有source | 価値と保留条件 |
|---|---|---|---:|---|
| **CONDITIONAL追加** | [aaaaygd/DeepSeek-V4-Pro-Qwen3.5-4B-UNCENSORED-heretic](https://huggingface.co/aaaaygd/DeepSeek-V4-Pro-Qwen3.5-4B-UNCENSORED-heretic) | `cdd9b11e7f92e4ba53dfeb6c02c6e7baf7a7e8a1` | **9,345,162,884 bytes／17file** | 4B級の後学習・Heretic編集BF16＋別MTP。既存9BのGGUF量子化版ではない。親・teacherの権利と推論ABI未検証。 |
| **CONDITIONAL追加** | [satellitedown/Inkling-2-Mini-abliterated-ingine](https://huggingface.co/satellitedown/Inkling-2-Mini-abliterated-ingine) | `6e823ba0031071d549e4973ec8caf86873cf60db` | **1,190,518 bytes／20file** | 221,280 F32要素の動的ablation編集状態＋コードと作者評価の再現記録。v58原本の13ファイル・20,191,588,440bytesとSHAが一致したため重複転送対象から除外。Linux CUDA13/Blackwell専用でowner実行未検証。 |
| **CONDITIONAL追加** | [OpenUncensored/Inkling-2-Mini-Uncensored-LoRA](https://huggingface.co/OpenUncensored/Inkling-2-Mini-Uncensored-LoRA) | `b328f8112173024d0f097aba1ea09e5f475ca7f9` | **877,939 bytes／5file** | rank2・40tensor/215,040 F32要素の別LoRA。元Inklingの20GBを複写しない。author adapter_configの親revision=null、PEFT task_type CAUSAL_LM vs Inkling Seq2Seqとの互換は未検証。 |
| **研究HOLD** | [thinkingmachines/TML-d24-varloop-research](https://huggingface.co/thinkingmachines/TML-d24-varloop-research) | `657b53ba5da7baefe9ff15dca5cd25f5bd3dbaa2` | **20,191,620,855 bytes／14file（取得候補から除外）** | 元のInkling Miniとは異なる重みとMTPで1〜5パスを変動させて学習。真の別学習済みcheckpointだが追加20.19GB、作者自身production非推奨。 |

**入れ替え判断**：52.845GBの[Electroglyph Inkling BF16編集全repo](https://huggingface.co/electroglyph/Inkling-2-Mini-uncensored)や同系統の複数GGUFを一律採用せず、独立編集差分2つの**合計2,068,457 bytes**を残す。一方、同種の結果・コード兼容性は同一GPU/シード/非有害品質/拒否評価の対比較が未実施で、優劣や規制リスクの確率を作らない。

同日公開された[Inkling 2 Small](https://huggingface.co/thinkingmachines/Inkling-2-Small)はPublisher表示**594,050,672,720 total parameters**、公式全source約393.51GB。現行の**150B以上を取得候補から外す保守的ゲート**を越えており、Miniより大きい方が良いという理由では今回追加しない。v59の3候補は保存上限より小さい。

## 2. 出版社コード・学習成果・MTPの計数を分離

4Bは[出版社モデルカード](https://huggingface.co/aaaaygd/DeepSeek-V4-Pro-Qwen3.5-4B-UNCENSORED-heretic)と固定`model.safetensors.index.json`により、MTPを含んだ**4,539,265,536** total parameters（主2 BF16シャード＋別MTP）。**MTP 15tensor・120,599,552 BF16要素はすでにモデルindexに含まれる**ため二重加算しない。作者はQ8 GGUFのMTPを使ってGSM8K 1,319問×2回で91.7741%を報告しているが、公開するBF16 checkpointと同じ質・同じHWであるとは証明されていない。GPU型・clock・ドライバと推論batchの一致を確認するまで実測ベンチマークにはしない。

Satellitedownは**元学習済みInkling主重みもMTPも変更していない**。作者の最適化済み係数とcodeを実行中に適用する別手法。固定配布元33ファイルをv58 Inkling元repoとpath/size/Git SHA1/LFS SHA256で突合した結果、**13ファイルを完全同一と判定**し、20固有ファイルのみを[固定source](../../manifests/drafts/r139-2026-11-21-inkling-micro-edits-and-deepseek4b-varloop.candidate.json)に選定。オリジナル元weightsが実Dに存在することは台帳で未報告で、**1.19MBだけ保存してもモデルは動かない**。

OpenUncensoredも小さいが別機構。著者PEFT設定は`r=2`,`lora_alpha=2`,`base_model_name_or_path=thinkingmachines/Inkling-2-Mini`、`revision=null`。後から親revを推測で上書きせず、選定側が**v58元モデルrev `1fb4134b9a74f9681054f4ef82e4bf1f458a2337`**を検証対象として指定する。merge_adapter.pyの安全な静的監査、同じquantized modelopt形式での差分再構成、MTPの扱い、フレームワークに合ったロード法の確認が停止条件。

### 主張の限界

無検閲モデルの拒否率は作者のテスト集合に強く依存し、無害指示の能力維持、再現性、性質の永続性を証明しない。4B作者のMTP-Q8評価、OpenUncensoredの32プロンプト、Satellitedownの独自refusal suiteを同一条件の品質スコアのように比較することは禁止する。文献の[Arditi et al., 2024, arXiv:2406.11717](https://arxiv.org/abs/2406.11717)は拒否方向についての一次研究であって個別の派生モデル性能を保証する権威ではない。

## 3. 全資産取得候補は76報告と統合し、アクセスリスクを分けて優先する

以前の13候補、v58のInkling＋Dettato5原本、今回の3候補を合わせ、**21 distinct repo／324 publisherファイル参照**を[未承認のR140取得候補](../../queues/proposed-v59-r140-ledger76-next-21-deduplicated-sources.json)に固定した。76既存報告の名前と重複0。

| 段階 | 追加保全する主な機能 | 元repo数 | files | 出版社の論理source bytes |
|---|---|---:|---:|---:|
| P0 | Dettato 4段、Maya2 codec/ECAPA、Phala LoRA、Inkling tiny edits2件 | 9 | 72 | 609,360,574 |
| P1 | Rikiya0.8B、LFM3 1.7B、Rumble、Aion、ELYZA/Aya、独立4B BF16＋MTP | 7 | 148 | 20,727,263,121 |
| P2 | Inkling原本（32GBメモリ推奨）、Mellum MTP、Spark4B、Heretic9B | 4 | 72 | 72,927,621,703 |
| P3 | Ripple65B（大容量で権利/HW審査まで保留） | 1 | 32 | 129,572,889,973 |
| **合計** | **21固有配布元／全source研究範囲** | **21** | **324** | **223,837,135,371** |

4B/9Bで`tokenizer.json`のpublisher LFS SHA256が同一であることも確認。**19,989,339 byteの重複潜在節約**。同じcontent hashは出版社の公開元の証拠であり、所有者媒体上の物理ファイル再利用までは確認していないため、取得器がそのままHardlinkを作れると断定しない。重複候補はR140へ厳密な2 repoとpath/SHAで記録。

## 4. 変数表・容量とパラメータ数の次元チェック

| 変数 | 意味（日本語） | 単位（SI・情報単位） | 定義・数値 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `B0` | 共有親/小容量補完 | byte | 609,360,574 | P0元source論理容量、現物は未確定 | 非負整数スカラー |
| `B1` | 小型独立原本 | byte | 20,727,263,121 | P1 sourceの合計 | 非負整数スカラー |
| `B2` | 中型native原本 | byte | 72,927,621,703 | P2 sourceの合計 | 非負整数スカラー |
| `B3` | 大型Ripple保留 | byte | 129,572,889,973 | P3 source、現段階取得対象外 | 非負整数スカラー |
| `B_near` | P0〜P2の総source | byte | `B0+B1+B2` | 二重転送前のpublisher論理値 | 非負整数スカラー |
| `B_all` | 全21配布元の論理source | byte | `B_near+B3` | 履歴取得済み76件を含まない | 非負整数スカラー |
| `B_reuse` | 同じtokenizerの潜在再利用byte | byte | 19,989,339 | 両modelのLFS SHA256とbyte数が同一 | 非負整数スカラー |
| `D` | 現在のowner Dドライブ空き容量 | byte | null（未観測） | 取込中のstaging・cache・既存ファイルを含めて実機測定 | 非負整数またはnull |
| `F` | 保存処理中の最低空き安全床 | byte | 200,000,000,000 | repoの既存保守ルール | 非負整数スカラー |
| `P4` | 4B原本の全学習パラメータ数 | 1（個） | 4,539,265,536 | MTP120,599,552個**込み**、ModelIndex | 非負整数スカラー |
| `Pe` | ingineの固有編集係数数 | 1（個） | 221,280 | FP32・4 tensor。ベース全総数と区別 | 非負整数スカラー |
| `Pl` | rank2 LoRAの学習・編集要素数 | 1（個） | 215,040 | FP32・40 tensor、親rev不明 | 非負整数スカラー |
| `Plimit` | 既存hard param guard | 1（個） | 150,000,000,000 | 不活性expert/親/MTPも含める | 非負整数スカラー |

1. `B_near = 609,360,574 + 20,727,263,121 + 72,927,621,703 = 94,264,245,398 byte`（約94.264十進GB）。P3を加算すれば `B_all = 223,837,135,371 byte`。
2. 将来publisher一致SHAでtokenizer共有できる場合、該当1ファイル分だけ `B_all - B_reuse = 223,817,146,032 byte` になる**条件付き論理値**。owner実増分は未知。
3. **次元チェック**：BとD/Fの単位はbyte、従って加減算可能。P系は無次元個数で、byteと直接比較・加算してはいけない。4BのMTP個数はP4に内包されるので再度足さない。
4. 厳密な実取得可能条件にはOwnerの`D`が必要。報告書の歴史的最小空き1.313TBを現在のDとして置かず、staging/cacheピーク不確かさを含めて `D >= B_near + F + staging_peak` を満たすか測定し、権利/承認の別ゲートも全通過させる。

## 5. 規制事実・H/T/D/C/U・ERROR CHECK

[2026-11-19米国連邦官報](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)では旧AI Diffusion Ruleのモデル重み規制項目4E091が撤廃された。これは公開済み全重みの**所持禁止が近日中に確定した**証拠ではない。モデル配布元の使用ポリシー、データセット権利、Gated/輸出規則は独立問題。**個別モデルの非公開化予定日・禁止確率は未測定**。

**H**：元Inkling原本の約20GBを1回だけ保管し、2つの異なる差分を約2.07MBで併存させると、親全コピーを二重保存せず拒否方向編集研究の再現性が保てる。加えて4B＋MTPは9Bの単純量子化ではない学習結果。

**T**：Publisher固定revを読むだけの4repo・全ファイル計69件、4B MTP・ingine edit・PEFT editのsafetensors静的ヘッダ検査。R140の**21repo／324論理ファイル（n_min=324）**でpath/size/sha/hash全数確認。所有者媒体のread-only SHA・コード実行監査・ライセンス適用確認は追加検証。性能を比較する場合は30以上の無害held-out反復入力、同一GPU/clock/driver/CUDA/backend/quant scales+zero-point/batch/context/seedで測定。1件でも権利・SHA・媒体床に違反すれば逐次停止。

**D**：PASS_SOURCE＝出版社source識別、特定SHA重複排除、MTP総数を二重加算しないこと。PASS_DOWNLOAD＝本人行為別利用権、個別scope承認、実ドライブ容量・stagingとSHA、親/codec完全性、対応ABIの全成立時のみ（**未達**）。FAIL＝無承認取得・間違ったparent・MTP欠落・unsafe code自動実行。UNCERTAIN＝品質・速度・合法性の具体的行為、将来規制。

**C**：作者の拒否測定を独立に再現できない、4B Q8ベンチとBF16性能が一致しない、LoRA task_typeがInkling native Seq2Seqに対応しない、ingineがCUDA13/Blackwell限定でowner環境では動かない、将来公開停止の予測が外れる。

**U**：上流メタデータ鮮度、親コード/ABI、作者の評価偏り、適用ライセンス、実D空き・cache、デバイスの量子化表現誤差が主要誤差源。複数条件の独立測定がないので合成標準不確かさ`u_c`と被覆係数`k`は数値化しない。

**ERROR CHECK**：v58の既存218資産は不変、v59で追加CONDITIONAL3件→**221登録／174有効**。新規original source3配布元42選択ファイル・9,347,231,341 bytes、既存InklingとSHA一致13元ファイル計20,191,588,440bytesを重複保全しない。VARLOOP独立研究checkpointは文書に確定したがv59正式資産からは保留。R140は21source324論理参照、LFS unique70、SHA等価tokenizer1件19,989,339byte。レポート76取得報告をre-download対象から排除。**承認0・新規重量DL0・本人D rehash0・custom code実行0**。

**関連分野**：MLモデル学習系譜、セキュアなコード・実行環境、確率的ベンチマーク設計、デジタル保存・content-addressing、AI法務・著作権。

###〈次に考える問い〉

**元Inkling Miniを安全なNative runtimeで1回復元した後、2つの約1MB編集差分は性能・拒否・実行互換性の三条件を同じ実験で区別できるか。** その結果でモデル本体の重複再保存・安全性主張なしに採否を再評価する。
