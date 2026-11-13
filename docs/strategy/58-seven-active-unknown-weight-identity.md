# R58｜v32有効135件のうち、全学習済み総数未確認7モデルの配布元再監査（2026-11-14）

**mainのみ更新。正式な選定182資産・有効135件、UNVERIFIED20（有効7）、取得承認0件は維持。** 非実行のファイル・Gated・ライセンス・学習済み状態監査。

[機械可読のR58全ファイル証拠](../../catalog/research/2026-11-14-r58-seven-active-unknown-dependency-and-format.json)。上流Hugging Face model API `?blobs=true` を再照合、7/7 repoの40桁revisionと公開重み容量・LFS SHA-256を記録した。**本文は決定根拠であり、取得済み・正規許諾済み・動作確認済みの宣言ではない。**

## 1. 重要な対象・保存形式の選択

| モデル | 上流revision冒頭 | 選択する原本重み部分（候補） | 留保する依存・権利 |
| --- | --- | ---: | --- |
| [SteerTTS](https://huggingface.co/WhissleAI/steer-tts) | `65ec6a637f4b` | FP32の異なる機能を持つroot6重み：**216,962,216 byte** | Gated auto・CC BY-NC4.0＋Whissle条件。Vocos、WavLM、MiniLMの第三者権利と外部固定版 |
| [Maya2 Native](https://huggingface.co/maya-research/maya2-native) | `87a83efdd655` | 2シャード **5,004,879,768 byte** | Mimi＋SpeechBrain ECAPAの別学習済み依存SHA/総数 |
| [Fish Audio Drama 3](https://huggingface.co/fishaudio/drama-3) | `78e5ab79e49a` | 15シャード＋`codec.pth` **41,474,651,096 byte** | Fish Audio Research License。Codecはpickleで非承認ロード禁止 |
| [Qwen Image Consistency LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | `58897a02f4f6` | 1500と2000の独立学習段階2本 **318,872,992 byte** | Qwen Image 2.1親、Encoder、VAE、権利と同条件品質 |
| [Pruna P-H3 Image](https://huggingface.co/PrunaAI/P-H3-Image) | `7f98acef503c` | 15 learned files **99,797,308,280 byte** | MiniMax Communityの地域制限／Diffusers、prompt upsampler |
| [ChrisColeTech LTX2.5 FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | `592aaa11f13a` | 一つの推論構成向け暫定5ファイル **30,484,902,414 byte** | Gemma4と映像/音声VAE・donor・版互換。15候補全形式を収集しない |
| [Stubelius Remix](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | `f3160a69a833` | v1 BF16原本1本 **42,008,732,600 byte** | 外部text encoder/VAEs・LTX派生権利。beta1/beta2は別学習段階として独立研究 |

上記各byteは**モデル重み部分だけ**であり、モデルカード、設定、ランタイム、Encoder、Codecなど一部は含まない。`candidate_weight_subset_bytes`は7モデルの最終アーカイブ総量ではなく、重複除去もこれらのハッシュに限定して計算する。

### 2. 重複削減で注意すべき学習済み差分

- **Qwen Consistency LoRA**：1500／2000は両者 **159,436,496 byte** でもソースLFS SHAが異なり、同じFP形式をコピーした通常量子化ではない。[作者の比較](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA)では1500版は色調保持、2000版は厳密な構図保持に有利という品質トレードオフ。追加159MBは独立研究成果の保険価値があるため**双方を条件付き保持**。親Qwen Imageは共有し二重保存しない。
- **SteerTTS**：FP32 rootの音響本体・refiner flow・cloning専用pflow・prompt adapter・speaker vectors・イベント重みは用途が異なる。これらと同じ役割のINT8版・native C版を無理由に重複収集しない。[公式カード](https://huggingface.co/WhissleAI/steer-tts)の「コードMIT」歴史的記述と、最新Gatedプロンプト／Whissle LICENSE.mdのCC BY-NC4.0＋追加条件を区別。権利表記が曖昧なうちはGatedを代理受諾しない。
- **LTX2.5特殊版**：Chrisには15 weight variantsで複数のFP8/INT8/GGUF、Gemma4 Encoder、音声/映像VAEが同repoに混在。全形式は **166,898,780,064 byte**だが独立15モデルを意味しない。Stubeliusはv1 BF16と同v1のINT8/NVFP4/GGUFを重複採用しない。beta1/beta2はv1とは別学習状態であり、量子化違いと混同せず、別の保存価値が証明された時だけ取得。
- **Pruna H3**：15の必須学習済みファイルはTransformer7、Text Encoder2、Prompt Upsampler4、Text Connector1、VAE1。[公式カード](https://huggingface.co/PrunaAI/P-H3-Image)はUpsamplerを省いた手動詳細プロンプトの経路も示す。ただし省略すると標準の短いプロンプト拡張能力が消えるため、完全機能保存には必要。Hubの33.12Bは主Transformerの値であって総pipelineと同じでない。
- **Drama3**：主重み35.899643008B個のSafetensorsとは別に、`codec.pth` **1,871,099,728 byte** が存在。保存すべきCodecを無視して「音声生成がオフラインで再現可能」と判断しない。

### 3. リビジョン変化・停止条件

配布元のSource SHA40の再調査では、Stubeliusが旧R51の`829cf2f7cbdf79872ff365787ba50f80006efe76`から`f3160a69a833565d2c2c620c61d40102c1b2910c`へ変化。他6 repoはR51当時の固定SHAと一致。SHA変化はREADMEだけかモデル重みの変更かをまだ比較できていないため、**同一trained stateと断定しない**。取得は新旧SHAのfile payload一致確認後に検討する。

7モデルとも最終ロックに必要な全学習済み総パラメータ数、外部学習部品の正確なSHA、権利、必要なruntime/OS/backend ABI、品質・本人HWと実ディスクを未確認。研究選定CONDITIONALを維持し、最終取得キューへ昇格しない。

## H/T/D/C/U・ERROR CHECK

H（反証可能）：選択時のtrained-state区別と外部依存を明確にすると、通常量子化の重複を減らしつつ独立能力を維持できる。

T（最小試験）：v32有効7/7の公開源モデル情報、LFS SHA、サイズ、access gateを静的に収集。動作の測定前提：実機HW/clock、backend commit/ABI、quant/zero-point、context、batchを指定し、必要なら各30反復以上。今回のn=7、形式適合の検査と公開データのみ。実重み取得0。

D（合否）：PASS=全7モデルの公開revision/重み候補と独立差分を確認。FAIL=形式重複を別学習済み資産とカウント、Gated認証を迂回、未知のCodecを0扱い、モデル重み取得を偽装。UNCERTAIN=全学習済み総数、権利、完全選択容量、実機。

C（破れ方）：作者の版更新、同一SHAのメタデータ誤り、主Transformer外の予期しない必須学習部品、改訂LICENSE、対応バックエンド変更。

U：公開元メタデータ、ライセンスと依存の未監査、owner-HDD未計測を主要不確かさとする。定量測定なしにつき合成標準不確かさu_c・包含係数kは未定義。

| 記号 | 意味（日本語） | SI単位 | 定義・範囲／前提 | 型 |
| --- | --- | --- | --- | --- |
| N | 未解決の有効資産件数 | 1 | 7固定、非負整数 | 整数スカラー |
| P | すべての必須学習済み部品の合計パラメータ数 | 1 | 7件ともnull（未確定）、全MoE expertを含む | 整数/null |
| B | 指定された源重み部分の容量 | byte | Publisherが公開したファイルサイズ、0以上、外部依存を含まない | 整数スカラー |
| F | 保存後の最低実空き | byte | 200,000,000,000、物理HDD未測定 | 整数スカラー |
| C | 目標容量上限 | byte | 4,000,000,000,000、選定の計画値 | 整数スカラー |

次元チェック：N/Pは無次元、B/C/Fはbyteで同次元。重みbyteと学習済み要素数を混同しない。

**ERROR CHECK**：7ID一意、7/7配布元SHA確認、v32の182件・有効135件、取得承認0件、ブランチmain一本を維持。コミット前にソース最終確認。学際領域：音声工学（Codec/Flow）、画像生成（LoRA/DiT）、ソフトウェア供給網とライセンス（固定revision/配布条件）。

**〈次に考える問い〉**：この7件のうち、外部学習済み依存の固定SHAが最短で揃い、実際の完全復元パッケージへ移せるものをどの順に処理すべきか。
