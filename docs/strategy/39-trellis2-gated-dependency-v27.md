# 39 — TRELLIS.2のGated画像特徴抽出器・外部構造デコーダの復元監査（2026-11-07）

## 0. 正本と作業範囲

`Unjuno/local-model-portfolio`の[CURRENT](../../catalog/CURRENT.json)は **v27-20261107、173資産／有効126件**。選定一次ファイル126件を固定版メタデータで算定し、既知の論理重複排除後 **3,417,685,712,585 B**。外部依存・実行ABI・利用権利を含む完全な保全サイズは**UNKNOWN**、関連問題を持つ資産は**35件**。今回の研究はこの中の既採用`microsoft/TRELLIS.2-4B`を修復可能な状態へ近づける。新規モデルの選定・承認・ウェイト取得は実施しない。

選定済みの親：`microsoft/TRELLIS.2-4B@af44b45f2e35a493886929c6d786e563ec68364d`、全24ファイル**16,237,485,044 B**。[固定版`pipeline.json`](https://huggingface.co/microsoft/TRELLIS.2-4B/blob/af44b45f2e35a493886929c6d786e563ec68364d/pipeline.json)と[Microsoft公式Git SHA](https://github.com/microsoft/TRELLIS.2/tree/75fbf0183001ed9876c8dbb35de6b68552ee08bd)を一次証拠とする。

## 1. 厳密なモデル復元依存（原本の重みからは再構築できない）

| 外部配布元／ファイル | 役割・必須性 | 確認済みアクセスと異なる権利 |
|---|---|---|
| [`microsoft/TRELLIS-image-large`](https://huggingface.co/microsoft/TRELLIS-image-large)の`ckpts/ss_dec_conv3d_16l8_fp16`（同名`.safetensors`と`.json`） | **構造復号の学習済みモデル**。TRELLIS.2の`args.models.sparse_structure_decoder`が別repoを参照。TRELLIS.2の全24ファイルには同名の復号重みがない。 | 元のTRELLIS-image-largeのmodel cardはMIT。個別部品の正確な版・byte・SHAは[自動調査結果](../../catalog/research/2026-11-07-trellis2-closure/audit.json)を参照 |
| [`facebook/dinov3-vitl16-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m) | **DINOv3 ViT-L16の画像特徴抽出器。学習成果として必須**。Microsoft実装の`DINOv3ViTModel.from_pretrained`が起動時に参照。 | **現在Gated**、[Meta DINOv3 License](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m/blob/main/LICENSE.md)。個人の本人アクセス許可未確認 |
| [`briaai/RMBG-2.0`](https://huggingface.co/briaai/RMBG-2.0) | BiRefNetによる前景分割。背景除去機能自体は**交換可能**だが、標準`from_pretrained`はDINOと同じくRMBGも**無条件に初期化**。 | **現在Gated**、ライセンスmetadataは`other`。個別商用・再配布条件が確認されるまでは実際の保存と利用権限を推定しない |

**重要な誤解の訂正**：既存ポートフォリオには`facebook/dinov3-vit7b16-pretrain-lvd1689m`と`facebook/dinov3-vith16plus-pretrain-lvd1689m`があるが、**ViT-L16の訓練済み特徴空間を代替できない**。単なるDINOv3同一シリーズという根拠でハッシュの異なる学習成果を重複扱いしない。

**背景除去の条件分岐**：[Microsoft公式の説明](https://github.com/microsoft/TRELLIS.2/issues/22)ではDINOは必須だが、RMBGは他の背景除去モデルに置き換え可能。RGBAのalphaがある画像に背景除去の実行は不要な場合もある。ただし[固定版ローダー](https://github.com/microsoft/TRELLIS.2/blob/75fbf0183001ed9876c8dbb35de6b68552ee08bd/trellis2/pipelines/trellis2_image_to_3d.py)は**前景分割モデルを常に生成する**ため、*標準コードをそのままオフライン再現する一式*と*透明背景画像を対象にした変更版の最小実行*を分ける。後者のプログラム修正を実施したとは主張しない。

**レンダリング契約**：Microsoft公式Issue #22ではnvdiffrast/nvdiffrecを表示用途として省略できるとの開発者コメントがあるが、textured GLBのPBR bakeまで同じことが可能かは議論中。CUDА/コンパイラ、o-voxel、NVIDIA依存の実行環境容量と個別ライセンスは**UNKNOWN**。パイプラインファイルだけで商用GLB出力を許可されたと考えない。

## 2. バイト計測とGated検査

[機械監査`audit.json`](../../catalog/research/2026-11-07-trellis2-closure/audit.json)には、3つの外部配布元の**公開HF API固定head、完全tree可否、個別ファイル名と公称バイト、匿名Gated状態、公開LFS SHAの有無とmasked状態**を格納する。欠落・401・サイズ未確認の場合は`null`として残し、0としない。

選定重みファイルは元BF16/Safetensors原本を優先。安全に比較できるSHAがないGated重みは、同名/同容量だけで既選定とdedupしない。Microsoftの外部構造decoderは`ss_dec_conv3d_16l8_fp16.safetensors`と同名`.json`を組にする。BRIA/RMBGはデフォルトの追加ソース重みだが、改変コードで回避できる機能と無条件初期化は区別。研究時点のAPI treeが失敗した依存は「source bytes UNKNOWN」とする。

v27の3,417,685,712,585 Bは一切変更しない。既存126件と外部重み3セット＋Microsoftコードソースに対して、同一identifierでの**調査用論理和**を計算し、源Repo合計・必要選定ファイル合計・権限未検証を混同しない。最低空き床200,000,000,000 B、計画枠4,000,000,000,000 Bは不変。ユーザーHDD空き・実staging/一時cache・完全オフライン復元実行の総量は**UNKNOWN**。

## 3. 反証可能性、一次論文、付随する新モデル動向

- [TRELLIS.2論文](https://arxiv.org/abs/2512.14692)；[DINOv3論文](https://arxiv.org/abs/2508.10104)。これらは学習構造の資料であり、個人へのGatedアクセス承認ではない。
- [Issue #38](https://github.com/microsoft/TRELLIS.2/issues/38)：2つのGated modelへのアクセスが取得できず、ユーザーが再現できなかったとの報告。非公式ミラーによるアクセス回避は推奨・実施しない。
- [Issue #161](https://github.com/microsoft/TRELLIS.2/issues/161)：TransformersのDINOv3内部API（layer access、RoPE形式）不一致を2026年5月にユーザー報告。修正PRが存在しても、**この固定Git SHAと特定のTransformers ABIが実機で動作することは未検証**。
- 別件として[NVIDIA Isaac GR00T N1.7](https://github.com/NVIDIA/Isaac-GR00T)は既選定のN1.6から新しいCosmos-Reason2-2B/Qwen3-VL backboneへ変更した学習成果だが、公式説明ではbackboneがGated。入手権限と容量・独自性を確認する前に追加採用しない。GR00T N1.7は**今回新発表されたモデルとの主張ではない**。

## 4. H/T/D/C/U・ERROR CHECK

- **H：** TRELLIS.2の完全オフライン復元にはDINO ViT-L16と別配布元の構造デコーダが必要。標準ローダーの無改変保存にはRMBGを含む。既選定DINO 7B/H+を流用しても型・特徴空間互換が実証されない。
- **T：** HF固定SHAの公開treeと各ファイルbyte、GitHub固定コードSHAのソース文字列、親の`pipeline.json`参照を機械照合。130モデル以上の既存選定・取得承認0・4TB制限に影響しないことを全回帰CIで監査する。TensorをダウンロードせずGitHub/Hubの公開meta情報と小型JSON/コードのみ読む。
- **D：** SOURCE PASS＝必須リポジトリが実在し正確な固定repo/ファイル/byteに解決できたこと。RESTORE PASS＝本人にGated権限、個別license、すべての現物SHAと実行ABI、オフライン同品質出力が確認されたこと。現時点は**RESTORE UNCERTAIN**。
- **C：** Gated許可が拒否される、間違ったDINOの代用、別repo decoder欠損、source revisionに非互換なDINOv3 Transformers API、背景除去が必要だがRMBGは商用未許可、CUDAライセンスが目的に不適合。
- **U：** 個人の権限/実ディスク、PyTorch/Transformers version、GPU VRAM/clock、source SHA maskedの現物ハッシュ、配布元LICENSE変化。確率分布がないため合成標準不確かさ`u_c`と包含係数`k`はUNKNOWN。

**ERROR CHECK：** 新規採用0、HOLD/REJECT変更0、重みダウンロード0、承認変更0、クラウド課金0、main変更0。既存モデルの利用条件・アーカイブ完全性と研究容量シナリオは別に記録。機械学習、デジタル保全、供給網、法律/ライセンスの4分野を別評価。
