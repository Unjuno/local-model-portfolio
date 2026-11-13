# R60｜PrunaとMiniMax H3 Imageの本当の重複・権利・保存構成（2026-11-14）

現行[mainのv32正本](../../catalog/CURRENT.json)（182資産・有効135件）。**追加モデル・採否変更・重みダウンロード・Gated承認0**。機械可読[ソースSHA・LICENSE比較表](../../catalog/research/2026-11-14-r60-pruna-minimax-h3-licensing-format.json)。

## 配布元の固定ファイル形式

| 形態 | 元の固定revision | 上流の重み部分（byte） | 結論 |
| --- | --- | ---: | --- |
| Pruna [P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image) BF16 Diffusers | `7f98acef503cf2bcfba821a78cb1cf1a9928b2df` | 99,797,308,280 | 既存CONDITIONAL維持。Transformer7、Text Encoder2、Prompt Upsampler4、Connector1、VAE1の15ファイル |
| [Pruna Comfy](https://huggingface.co/PrunaAI/P-H3-Image-Comfy) BF16四重み | `44a0fb73f299da1bb715bdb5ff59ce3fd3c6f543` | 74,471,781,216 | 形式・内部重み変換未解明。元Diffusersと無根拠に同一視／重複収集しない |
| 同W4A8/INT8四重み | 同上 | 26,808,697,441 | 実行用量子化。高精度保存とは別目的なら個別審査 |
| 同LoRAのみ | 同上 | 1,956,195,360 | **親動画H3 FL2VAを別途要す**。親BF16だけで 66,280,487,368 byte |
| MiniMax [H3 Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image)原形式（PEなし） | `5f90473023975e6271b0ed1dd84c4e88e4bbc6d3` | 135,343,354,088 | 原本HOLD。全41重み合計203,969,758,064 byteにはTransformer・VAEの別形式が重複 |
| 同Diffusers形式（PEなし） | 同上 | 135,353,705,656 | 上記と同時取得しない |

上記のbyteはソースの重みのみ。各Repoのprocessor・scheduler・NOTICE・推論コードと事前権利・実空き・stagingは別。原本の[MiniMax H3 Image PE](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image-PE)は**任意のプロンプト拡張器**。公式READMEで別repo約17.9GB。使用時だけ別学習済みcomponentとして固定し、基本生成に必須とはしない。

**LoRAの本当の代償**：[Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3)の`minimax_h3_fl2va_bf16.safetensors`が必要で、親＋LoRAの**重みだけでも68,236,682,728 byte**。現在v32に親H3動画原本はSELECT/CONDITIONALとして入っていない。単に「1.96GBですべて保存可能」とは言えず、別途Text EncoderやVAE、コードも要る。

## SHAで立証した共有と未証明の等価性

MiniMax H3動画原本`FL2VA/text_encoder`14シャードとMiniMax H3 Image`text_encoder`14シャードは、配布元上流LFS SHA256とbyteが**14件すべて一致、66,714,912,872 byte**。将来両者を選ぶ場合の共有余地だが、いずれも現行v32選定対象ではなく現在の節約計上は0。

Pruna Diffusers15重みとMiniMax Image41重みの同一LFS SHA件数は0、PrunaとComfy12重みの一致も0。**ファイルSHAが異なるだけでは別学習状態と断定できない**。通常量子化、shard再配置、backend再形式化でもSHAは変わる。

**矛盾・要監査**：Pruna開発者は20B Transformerへ圧縮と説明するが、HF DiffusersのTransformer重みは約66.28GB、Safetensors要素合計33.12B、Comfy BF16単体は約40.47GB。単純に同じモデルのBF16量子化として扱わず、Tensor keyとshape及び画像同条件の差を確認する。[開発元一次技術説明](https://www.pruna.ai/blog/oss-p-h3-image-launch)。

## ライセンスは2つの別契約（公式原文固定）

- [PrunaのLICENSE](https://huggingface.co/PrunaAI/P-H3-Image/blob/7f98acef503cf2bcfba821a78cb1cf1a9928b2df/LICENSE)：**MiniMax H3 Community License**（2026-08-02、H3動画由来）。商用製品・サービスの年間収益が**2,000万USD超**なら事前書面許諾を要する。
- [MiniMax H3 ImageのLICENSE](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image/blob/5f90473023975e6271b0ed1dd84c4e88e4bbc6d3/LICENSE)：**MiniMax-H3-Image Community License**（2026-11-10）。年換算**100万USD超**または第三者向け**Hosted Serviceの提供**で事前書面許諾を要する。画像用PEにも適用。
- どちらもEU・英国・韓国・米国を通常許諾対象から除外し、NOTICE/再配布・用途制限を持つ。**これは2製品別の契約であり、同一モデルの許諾が遡及的に変更された証拠ではない**。日本が除外一覧にないことだけで個別の権利承認はできない。

## 実装・反証・数値範囲

PrunaカードのNVIDIA B200、BF16、batch1、8MP、no compilation/offloading条件でのVRAMピークは作者発表約83GB（prompt upsamplerなし）／約101GB（あり）。B200のclock・driver/ABIや本人実機は未確認。Diffusers ModularPipelineとComfyUIは異なるbackendであり、モデルtensor identityおよび画像品質は固定seed・同環境で比較が必要。

**H**：重みや学習済み部品をSHAで識別し、同一実体を二重保管しない。**T**：固定の公式ソース5repo、LICENSE正文2件、Pruna15+Comfy12+MiniMax41の重みSHA、H3動画原本とのText Encoder14件。**D**：14件全て同一SHA+byteはPASS。0件一致から学習状態差を確定したらFAIL。正規権利・パイプライン復元・user GPU性能はUNCERTAIN。**C**：作者が形式変換以外の新学習状態を公開した／モデルの形状が異なる／ライセンスが改定されたなど。**U**：公開元メタデータ、ソフト/codec依存、利用者の権利、実機空き、local hash未実施につきu_cとkは未定。

| 記号 | 日本語の意味 | SI単位 | 定義／定義域・前提 | 型 |
| --- | --- | --- | --- | --- |
| B_P | Pruna Diffusers保存候補の15重量 | byte | 99,797,308,280、Publisher LFSサイズの和、非負整数 | 整数スカラー |
| B_I | MiniMax原本一形式の重み量 | byte | 135,343,354,088、PEなし・外部依存なし | 整数スカラー |
| B_S | 原本2種の共有Encoder容量 | byte | 66,714,912,872、SHA/byte一致ファイルのみ | 整数スカラー |
| N | 共有重みファイル件数 | 1 | 14、非負整数 | 整数スカラー |

**次元チェック**：B_P/B_I/B_Sはbyte同士、Nは無次元。主重みbyteを完全オフライン総容量と混同しない。

**ERROR CHECK**：v32 182件・有効135、選定のPruna条件付き／原MiniMax HOLDは変更せず。取得・実行・契約受諾・新ブランチ0。取得承認キュー0。

〈次に考える問い〉：Pruna Diffusersの15重みとComfy BF16の4重みが同一画像能力を持つと証明できるなら、両方ではなく単一表現に統合すべきではないか？
