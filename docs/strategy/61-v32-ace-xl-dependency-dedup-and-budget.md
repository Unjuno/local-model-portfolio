# R61｜ACE-Step XLの依存サブセットと既存Qwen重み重複の一次監査（2026-11-14）

**対象**：`Unjuno/local-model-portfolio` `main` v32（182資産／有効135件）。入力 HEAD：`cc47e8b29f4fe53db954ebfb4c8966809bc7eb8d`。

> **取得許可ではない。** 公開元の読み取り専用メタデータと既存監査を照合した概算更新であり、ローカル本体取得・実行・個人Gated承認・選定変更・HDD計測は実施しない。

## 1.〈本論〉重複させずに保全する構成

- 公式の[モデル管理コード](https://github.com/ace-step/ACE-Step-1.5/blob/main/acestep/model_downloader.py)と[インストール手順](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INSTALL.md)を再確認。選んでいるXL Turboは通常版2B Turboの*追加購入*でなく、DiTの置換構成を持つ。必要とされた共有部品は**音楽計画LM 1.7B / Qwen3-Embedding-0.6B / 音声VAE**。4B LM/他DiTは別の学習状態だが、今回の構成では自動採用しない。
- [XL Turbo固定revision](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo/tree/d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee)：`d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee`、[index](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo/blob/d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee/model.safetensors.index.json)には**4,987,310,726個の学習済み要素と19,949,242,904 byteのtensor payload**。これらは4 shardの実ファイル総bytesではない。実シャードサイズはウェブ表示の各約4.99GBであり、配布元LFS SHA-256のみを今回確認。
- [共有元固定revision](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/19671f406d603126926c1b7e2adc169acbcade22)：`19671f406d603126926c1b7e2adc169acbcade22`。LMフォルダ約3.76GB、Qwen3-Embedding約1.21GB、VAE約337MB。**10.1GB全repoには置き換える2B Turbo原本が含まれ、最小必要量としての適用は不適切**。
- **重要なSHA一致**：ACE共有元の`Qwen3-Embedding-0.6B/model.safetensors` SHA-256は`0437e45c94563b09e13cb7a64478fc406947a93cb34a7e05870fc8dcd48e23fd`で、既存v27の`Qwen/Qwen3-Embedding-0.6B/model.safetensors`  **1,191,586,416 byte**と完全一致。v27ソース集合にこの重みを一度計上しているため、**理論上の内容識別子の増分は0 byte**。これは実HDDに既存のファイルがあるという意味ではない。tokenizer/configなどの同一性は未確認。

## 2. XL Turbo本体4 shard：公開元のSHA-256（未取得）

| パス | 配布元SHA-256 | Web表示容量 | 正確な配布ファイルbyte |
|---|---|---:|---|
| `model-00001-of-00004.safetensors` | `e54a8413c981797312f53d512dec9944023d03f42f0740cbe86f62582cc27bdc` | 4.99 GB (UI-rounded) | 未固定 |
| `model-00002-of-00004.safetensors` | `b45f788b6dc9f15957cfa3d9b403f25f3f64c5211ecaf18dda45b67ea6470664` | 4.99 GB (UI-rounded) | 未固定 |
| `model-00003-of-00004.safetensors` | `a4f6bd572eab79cf5f3e4678796f904c6d6c33680a3e6ed09034d6de7cabea4d` | 4.99 GB (UI-rounded) | 未固定 |
| `model-00004-of-00004.safetensors` | `a868b05493c73808408f58b33a903371bb2846b53c8b19bd7476991bc8837259` | 4.99 GB (UI-rounded) | 未固定 |

内部 index の19,949,242,904 byteをそのまま4シャードのディスク量にしない。全ファイルを正確なbyte+SHAで固定するまで完全保存見積はnull。`silence_latent.pt`はPyTorch pickleと表示されているので、取得工程で実行・unpickleしない。

## 3. 共有フォルダと独立学習部品の見積り

| 部品 | 配布元ディレクトリ | 公称容量（十進、丸め表示） | 公開元重みSHA-256 | 保存区分 |
|---|---|---:|---|---|
| 音楽計画LM 1.7B | [`acestep-5Hz-lm-1.7B`](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/19671f406d603126926c1b7e2adc169acbcade22/acestep-5Hz-lm-1.7B) | 約3.760 GB | `f161689da73e5ecefa28ff780d51c2d92a00f056d021d7933c779ed5c6cd7db8` | 今回の共有必須候補 |
| Qwen3-Embedding 0.6B | [`Qwen3-Embedding-0.6B`](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/19671f406d603126926c1b7e2adc169acbcade22/Qwen3-Embedding-0.6B) | 約1.210 GB | `0437e45c94563b09e13cb7a64478fc406947a93cb34a7e05870fc8dcd48e23fd` | 本体重み1,191,586,416byteは**既選定と一致**。周辺メタデータは別監査 |
| 音声VAE | [`vae`](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/main/vae) | 約0.337 GB | `da17edb604c40deaf09e9b24974e590d1ca83a374070e5d0884cfa4bed9a99b0` | 必須候補 |
**配布元ディレクトリの表示容量合計：約5.307GB**。正確な合計ではない。外部source code、ABI、tokenizer、各repoのLICENSE/NOTICE、stagingは未計測。

## 4. 4TB保存計画に対する更新された*参考*シナリオ

| 見積りのケース | サンプル算術の合計（byte） | 4TB＋空き200GBを仮定した差額（byte） | 精度 |
|---|---:|---:|---|
| R58既知ACE除外 | 3,442,028,436,758 | 357,971,563,242 | v27既知SHA union＋後続参照スコープの算術和 |
| R58旧：XL20GB＋共有全repo10.1GB（概数） | 3,472,128,436,758 | 327,871,563,242 | 過大な共有範囲を含む仮定 |
| **R61今回：XL20GB＋共有3フォルダ5.307GB−既知Qwen重み1,191,586,416byte** | **3,466,143,850,342** | **333,856,149,658** | **公称丸めと正確SHAの混合・参考値のみ** |

この差は前回の仮想見積りより約6GB小さくなる**計算例**であり、実際のHDD空きが6GB増えたことや完全依存が閉じた証拠ではない。XL本体そのものの全ファイルbyte、共有meta・学習済みCodec、実行環境、既存同一SHAの物理再利用状況、ゼロ点・ABI・元音声権利は未確定。

### 4.1 変数表

| 変数 | 意味（日本語） | 単位（SI/情報） | 定義 | 定義域・範囲/前提 | 型 |
|---|---|---|---|---|---|
| B0 | v27 SHA-aware union＋後続8件のソース範囲算術和 | byte | 3,442,028,436,758 | 既存依存・全版横断重複未検証 | 整数スカラー |
| A | XL本体の公称原本容量 | byte | 20,000,000,000 | 約値、正確な4 shard総byteではない | 近似スカラー |
| L | LM 1.7Bフォルダ公称容量 | byte | 3,760,000,000 | 約値、tokenizer含む | 近似スカラー |
| E | Qwen3-Embeddingフォルダ公称容量 | byte | 1,210,000,000 | 約値 | 近似スカラー |
| V | VAEフォルダ公称容量 | byte | 337,000,000 | 約値 | 近似スカラー |
| D | SHA一致による既存Qwen3-Embeddingモデル重み | byte | 1,191,586,416 | 公開元の内容一致、実HDD不明 | 整数スカラー |
| C | 保存計画上限 | byte | 4,000,000,000,000 | 物理計測とは別 | 整数スカラー |
| F | 最低物理空き床 | byte | 200,000,000,000 | 実際の空きはnull | 整数スカラー |
| T | 今回の参考ソース計画合計 | byte | T=B0+A+L+E+V−D=3,466,143,850,342 | 近似入力を含み厳密byteを意味しない | 近似スカラー |
| H | 4TB/200GB仮定での机上差額 | byte | H=C−F−T=333,856,149,658 | 実HDD、staging、codec不明 | 近似スカラー |

**次元チェック**：全加減算はbyte。公開元表示GBは十進換算の*丸め代表値*であり、「1B単位まで正確」という意味はない。学習済み要素数は無次元でbyteに変換できない。`index.total_size`はテンソル量、選択ファイル総量でない。

## 5. NVIDIA Kumo Relational：同じ系列内の別学習headとコード版

- [NVIDIA公式モデル実装](https://github.com/NVIDIA/structured-data-models/blob/main/sdm/models/kumo/relational/model.py) はclassificationに`classifier.pt`、regressionに`regressor.pt`を要求し、`revision="v1.0.1"`を指定し`torch.load(..., weights_only=True)`を呼ぶ。
- 公式配布元のSHA-256は [classifier](https://huggingface.co/nvidia/Kumo-Relational/blob/3d5176e4e713d734b71c2846fc9cd19e49e4c7d1/classifier.pt) `0c2e35cc18303f0d3ddeaf04e9cab6ca3a8bd6ea17195ac0e42d47af4bcb2a2d`、[regressor](https://huggingface.co/nvidia/Kumo-Relational/blob/main/regressor.pt) `f863b3632f738e1444fb83a8cea5746f298889b5c96953a000c4720d202ae4cf`。UIは約120MBと124MB。正確なbyteと`v1.0.1` tag⇔コミット一致、利用条件、必要ABIは未解決。**v32未採用なので現在の容量予算へ加えない。**

## 6. H/T/D/C/U と ERROR CHECK

- **H**：既存に同一Qwen重みが含まれるため、ACE XLを復元する追加保存範囲は『共有元全repo』より小さくできる。反証：必要な構成が旧2B DiTにも依存する、SHA一致以外の共有依存が欠ける、実行環境で同一モデルを再利用できない。
- **T**：XL４分割の元SHA4/4、LM+Embedding+VAEの各公式フォルダおよび重みSHA3/3、既存Qwen原本SHA+byte1/1、作者ローダーの部品宣言を静的確認。ユーザー機器上の実行・全payload SHA照合は未実施。
- **D**：SHA一致のソース論理重複はPASS、全ファイル厳密byte・権利/完全復元/HDD実空きはUNCERTAIN。対応ライセンスと全依存/owner権限/実容量が揃うまではダウンロード承認禁止。
- **C**：内部model indexと実シャードbytesを混同する、通常DiTを過剰収集する、version違いでABI不一致、外部リポジトリの利用権限・音声同意がない。
- **U**：rounded foldersの誤差、実ファイルヘッダ、依存ランタイム、HDD空きとstaging。入力分布/測定誤差相関なし→合成標準不確かさu_c・包含係数kは未推定。

**ERROR CHECK**：3,442,028,436,758 + 20,000,000,000 + 3,760,000,000 + 1,210,000,000 + 337,000,000 − 1,191,586,416 = 3,466,143,850,342（byte算術）。4TB−200GB−参考T=333,856,149,658。v32 182件/有効135件、approved0、取得0、local checksum0、現実のHDD検査0。

**学際性**：生成モデルとモデル部品の同一性、デジタル保存の重複排除と依存閉包、ソフトウェア供給網のSHA/ABI、ライセンス・音声利用同意を分離して検証。

## 7.〈次に考える問い〉

原本DiTを保存するだけでは音楽生成の再現性が保証できない以上、重複Qwen Encoderの再利用・VAE/LMの版固定・コードABIのうち、どの順にオフライン復元テストを設計すべきか。
