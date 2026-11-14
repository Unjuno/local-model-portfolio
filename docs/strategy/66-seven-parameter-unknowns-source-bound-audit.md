# R66｜有効7モデルの総パラメータ保留・原本ヘッダーによる厳格な上界監査

2026-11-15。正本main v32/135件。対象7件は既存の `UNVERIFIED_BLOCK_FINAL_LOCK` を変えず、公開元の*学習済みファイル内の確認済み部分*と、依存未確認部分を区別。モデル本体・コード・pickleは実行・ダウンロードしていない。

## 1.〈本論〉最重要の新しい定量的知見

- **Pruna P-H3 Image** の15 safetensors（Transformer7、Prompt Upsampler4、Text Encoder2、Connector1、VAE1）について、過去のヘッダー専用全数監査はテンソル要素を **49,635,347,496個**と確定。推定ではなく、固定リビジョンの全15ファイルに記載された形状の累積値である。
- この個数は公開された15ファイルの*保存テンソル要素*の上界として扱える（内部にbuffersや共有/tied状態が含まれても保守的）。**150,000,000,000より小さい**。ただし、実際のunique trainable parameterそのものの厳密値ではない。
- [Pruna原本の構成監査](../catalog/research/2026-11-14-r61-pruna-source-curve-capacity.json)はDiffusers原本に独立MiniMax H3の完全親重みが必要だとは認めていない。とはいえ、オフラインloadの外部独立学習済み依存の完全性/ABIは独立に確認していないので、**全パイプライン総数確定・取得可能のPASSにはしない**。

## 2. 7件の区別

| ID | 公開元で確認された学習済み部分 | 未確定・取得阻止条件 |
|---|---|---|
| `PrunaAI/P-H3-Image` | 49,635,347,496 elements | The catalog's FINAL_LOCK gate demands full learned pipeline (including external components if any), publisher license/rights and owner authorization; static headers only bound the 15 repository files. The original source review says standalone MiniMax donor not required for full Diffusers restore but actual loader ABI and external models have not been independently checked. |
| `maya-research/maya2-native` | Maya+Mimi 2,598,550,049（ECAPA除外） | ECAPA trained checkpoint tensor element count and full required module scope remain unknown. Do not treat partial counts as total. |
| `fishaudio/drama-3` | 主重み 35,899,643,008 | Mandatory codec.pth is serialized PyTorch pickle, not safetensors; do not unpickle or execute, custom learned state unknown. Full rights require Fish Audio Research License. |
| `WhissleAI/steer-tts` | 主重み 9,585,639 | External Vocos/WavLM/MiniLM, optional native/int8 variants and Gated auto entitlement unresolved. |
| `ausboss/Qwen-Image-2.1-Consistency-LoRA` | 複数重み/依存の部分のみ | Qwen Image 2.1 parent/encoder/VAE count and exact compatible trained state must be traced, both LoRAs differ in LFS SHA and are not ordinary re-quantizations. |
| `ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8` | 重み 30,484,902,414 B（パラメータ数でない） | Gemma4 text encoder, video/audio VAEs, LTX 2.5 donor/original license and complete tensor census unverified. |
| `Stuubs/Stubelius_Remix_Ltx2.5` | 複数重み/依存の部分のみ | External learned text encoder and audio/video VAE counts missing, old/new publisher revisions need trained-payload SHA comparison; normal INT8/FP8/GGUF duplicates not extra learned states. |

## 3. 150B閾値の論理と変数表

| 記号 | 意味（日本語） | 単位（SI） | 定義・定義域／範囲／前提条件 | 型 |
|---|---|---|---|---|
| S | Pruna原本15 safetensors内のテンソル要素 | 1 | 49,635,347,496、固定ファイル数15、非負整数 | 整数スカラー |
| P | 実行時必須な全学習済み部品の要素総数 | 1 | null（外部trained component有無未閉包） | 整数スカラーまたはnull |
| L | モデル総数の標準スクリーニング基準 | 1 | 150,000,000,000、MoE全expert・補助学習済み部品含む | 整数スカラー |
| E | 外部必須学習済み状態の追加要素数 | 1 | null（未確定）。外部重みが実際は不要なら0 | 整数スカラーまたはnull |

- **厳密な結論**：保存対象Pruna15ファイル内部の要素総数はS、S＜L（PASS_SOURCE_INTERNAL）。しかし完全パイプラインはP=S+E（E未知）なので、P＜Lを論理的に確定できない（UNCERTAIN_PIPELINE）。
- **次元チェック**：P、E、S、Lはいずれも無次元の要素数。byte容量やメモリ使用量と加減しない。Pruna原本の99.83GB保存計画は別指標。

## 4. H/T/D/C/UとERROR CHECK

- H: Pruna15原本の公開テンソル数は総150B未満を満たすが、他6件と同様に外部必須部品の存在証拠が欠ける限り完全取得へ進めない。
- T: 15 safetensorsの過去header監査と5 component別個数の合計検算。7/7の既存公開元ピンと未解決要素数を比較。n_min=7資産＋Pruna15ファイル。逐次停止: 一つでも未固定の必須外部学習済み依存を発見したら取得可判定を停止。
- D: PASS=Pruna固定15原本の内部S＜L・7件一意。FAIL=表示byteからパラメータ数を推測、pickleを開く、Gated回避。UNCERTAIN=実行に必要な全依存とlicense・本人権限・実HDD。
- C: 公開の重み以外に大きな学習済みエンコーダが存在、学習済み状態の複数版が混在、Pickleに入ったCodecが未数え。
- U: safetensorsヘッダー上の個数は整数算術だが、実物SHA・外部実行依存と権利は不明。確率分布が与えられていないので合成標準不確かさu_c/係数kは定量できない。
- ERROR CHECK：49,635,347,496 = 9,409,813,744 + 65,576,960 + 4,437,815,808 + 33,122,992,896 + 2,599,148,088 (全て要素数)、閾値 150,000,000,000 未満。正本7件のunknown総数判定は変更0、承認0、実物0。

**関連分野**：機械学習の学習済み状態監査、デジタルアーカイブの部品閉包、ソフトウェア供給網のヘッダー・SHA、知的財産/地域ライセンス。

## 5.〈次に考える問い〉

Prunaの主Transformerだけではなく、Upsampler・Text Encoder・VAEを含む49.635Bの15ファイルが完全学習部品であると、モデル実行コードの静的な参照グラフからどう反証可能に確かめるか？
