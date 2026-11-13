# 41 — Hunyuan3D-2.1 PBRのDINOv2・超解像原本・実装ABI・利用許諾（2026-11-07）

## 1. 調査理由

[CURRENT](../../catalog/CURRENT.json) v27-20261107は**管理173件／有効126件**、既知一次ファイル＋既記録の共有学習済み依存は**3,417,685,712,585 B（配布元のメタデータ、ハッシュ識別子による論理重複排除）**。外部依存・権利・実行条件が未閉鎖の資産は35件、ユーザーHDDの物理空きと一時領域・全オフライン環境はUNKNOWN。今回対象の既選定`tencent/Hunyuan3D-2.1`は`0b94677654c57bb9a6b6845cd7b704ccf551d327`に固定、**全配布元30ファイル14,909,683,275 B**。その中に含まれる形状生成重みとPBR texture本体の有無だけでは完全復元を判定できない。

今回、**既存の126選定件数は変更しない**。配布元が外部参照する学習済み2モデルとソースコードを、リポジトリ固定版・ファイル単位で独立調査する。

## 2. 配布元が要求する本当の学習済み外部依存

| 外部依存 | 必須性／固定方法 | 事実と現在の限界 |
|---|---|---|
| [facebook/dinov2-giant](https://huggingface.co/facebook/dinov2-giant) | **PBRのDINOv2 giant（1,136.5M級）の画像特徴量**。配布元の固定元モデル・config/processorだけを別保全 | Tencent[固定Gitコード](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/tree/82920d643c0dc2f7bfd7255f45f62d386edfe60c)の`hy3dpaint/textureGenPipeline.py`は`dino_ckpt_path="facebook/dinov2-giant"`。UNetモジュールは`self.use_dino=True`で、`hy3dpaint/utils/multiview_utils.py`が`Dino_v2(...)`をロード。**従って通常のPBR推論経路で外部重みが必要**。公開モデルカードはApache 2.0タグ、元checkpointの選定ファイル容量・固定SHAは[機械監査](../../catalog/research/2026-11-07-hunyuan3d-pbr/audit.json)で確定。既採用のDINOv3 ViT7B/H+や別のDINOv2 Largeをこの原本の代用と仮定しない。 |
| [RealESRGAN_x4plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth) | **PBR超解像**の学習済みRRDBNet。標準`imageSuperNet`の重みパス | [Real-ESRGAN v0.1.0公式リリース](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.1.0)の資産ID `40831506`、**67,040,989 B**、2021-07-22作成。GitHubリリースAPIの`digest`は`null`、**現物SHA256は不明**。配布元の`hy3dpaint/README.md`・Dockerfileで明示的な取得が必要。Real-ESRGANコードのBSD-3-Clause表示を、原本重みのあらゆる再配布方法の事前許諾とみなさない。 |

**別リポジトリと内部部品の区別**：Hunyuan3DのPBR Diffusers pipeline内部には`CLIPVisionModelWithProjection` image encoderとUNet、text encoder、VAE等が**既存Hunyuan本体repo内**に同梱されている。外部DINOv2 giantをこのCLIP重みと誤って重複排除しない。別repoの`facebook/dinov2-giant`は固定コードで明示的に参照されている。

**背景除去の留保**：shape入力の`rembg`経路はアルファ付き画像なら機能として省略可能な場合がある。一方PBR標準推論が外部DINOv2とReal-ESRGANを用いる事実とは別。その他の背景処理用ONNXやモデルは**使用経路と実行環境で要再検証**。ライブラリの自動ネット取得を許容したまま「offline restore PASS」としない。

## 3. 利用許諾とABIの重要性

[配布元LICENSE](https://huggingface.co/tencent/Hunyuan3D-2.1/blob/0b94677654c57bb9a6b6845cd7b704ccf551d327/LICENSE)は**Tencent Hunyuan 3D 2.1 Community License**。規約上、**EU・英国・韓国は適用対象のTerritoryから除外**、第三者配布時はLICENSEと所定Noticeなど、一定規模以上のユーザー数の場合に別途ライセンス条件がある。これは政府による一般的なモデル配布禁止ではなく**開発元の契約条件**である。

固定コード`hy3dpaint/textureGenPipeline.py`の古いヘッダーには**「TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT」**という表現が残る一方、同一commitの`LICENSE`/ `hy3dpaint/LICENSE`には**3D 2.1 Community License**がある。ヘッダーと契約本文の表示差を安易に都合よく解消せず、実際に適用される文書と利用形態を権利者の一次説明で確認する。

固定コードの[公式環境指定](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/tree/82920d643c0dc2f7bfd7255f45f62d386edfe60c)：Python 3.10、PyTorch 2.5.1+cu124、Transformers 4.46.0、Diffusers 0.30.0、カスタムCUDA Rasterizer／DifferentiableRendererビルド。これらが所有者のHW/clock/driver/ABIで動く実測は**未実施**。開発元の10GB（shape）、21GB（paint）、29GB（combined）のVRAMは**開発元の推奨値**であり、本人のピークRAM測定ではない。

## 4. 容量・重複・取得時使用量

[機械監査](../../catalog/research/2026-11-07-hunyuan3d-pbr/audit.json)はDINOv2 giantの**原本Safetensorsのみ（別形式の同重みを重複選定しない）**とconfig/processor/license、RealESRGANのGitHub release資産サイズ、Tencentコード全固定Gitツリー（公開source blobs 173,699,323 B）の3種類を区別する。v27の既知容量と照合し、**識別子が存在するファイルだけを論理重複排除**する。リリースにSHA256がない場合は異なる可能性のあるもの同士を重複扱いしない。

追加モデルの配布元実ファイル容量が未確定なら`null`とする。CIのsource tree照合後の論理合計が4TB未満でも、**物理HDDにその容量があることを示さない**。最低空き床200,000,000,000 B・実環境のstagingとキャッシュ・GPUランタイム/ローカル依存wheelの格納量は別途評価する。4TBの数値差を「実際の残容量」と呼ばない。

### 固定版メタデータ監査の結果（2026-11-07）

| 必要部品 | 固定版 | 全配布元ファイル容量 | 実際に選ぶファイル容量 |
|---|---|---:|---:|
| `facebook/dinov2-giant` | `611a9d42f2335e0f921f1e313ad3c1b7178d206d` | 9,092,168,005 B | **4,546,010,968 B**（5ファイル） |
| `RealESRGAN_x4plus.pth` | v0.1.0 GitHub Release asset #40831506 | — | **67,040,989 B**（1アセット、公開SHA256なし） |
| Tencent公式コードのGit blob | `82920d643c0dc2f7bfd7255f45f62d386edfe60c` | — | **173,699,323 B**（598 blob、デモ・例示も含む） |

DINOv2の`model.safetensors`は**4,546,005,432 B**、config／preprocessor／README／.gitattributesを含む5ファイルが**4,546,010,968 B**。原本`pytorch_model.bin`は同一学習重みの別シリアライズ形式として**今回の候補から除外**した。

外部ファイル候補の単純総和は**4,786,751,280 B**、Git blob識別子と公開LFS SHA256による論理重複排除後の増分は**4,785,207,663 B**。現在のv27容量正本に加算した研究用シナリオは**3,422,470,920,248 B**。4TBとの数値上の差は**577,529,079,752 B**だが**保存先の空き容量ではない**。DINOv2は公開・Apache-2.0メタデータ表示、Real-ESRGANアセットはGitHub Release APIのdigest欄が`null`で現物SHA256を未検証。

[生成した機械監査JSON](../../catalog/research/2026-11-07-hunyuan3d-pbr/audit.json)／[236件全テストおよび選定監査PASS](https://github.com/Unjuno/local-model-portfolio/actions/runs/42280761830)／[検証記録](../../catalog/research/2026-11-07-hunyuan3d-pbr/verification.json)。新規選定・取得承認は**0**。Metaの原本公開条件とTencent本体の地域契約、RealESRGANの重み固有の配布条件は引き続き**別々に確認**する。

## 5. H/T/D/C/Uと検証境界

- **H**：Hunyuan3D-2.1 PBRの標準出力を再現するにはTencent本体repo以外にDINOv2 giantとRealESRGAN x4plusの別学習済み重み、固定CUDA拡張環境が必要。
- **T**：固定Git SHAとソース`use_dino=True`・HF DINOv2の全ファイルと原本format・GitHub Release asset ID/byteをメタデータのみで照合。コードの短いテキスト以外の推論重み・releaseアセットは**取得しない**。既存v27容量・approved queueを回帰テストで固定する。復元試験は本人の正規取得後にHW/clock/backend/batchを記録して実施。
- **D**：SOURCE PASS＝必要モデル名・原本・容量・ソース版を一致確認。RESTORE PASS＝個人権利、現物SHA256、実行ABIとPBR画像品質の独立再現。現時点RESTOREは**UNCERTAIN**。
- **C**：外部重み未保存、DINOv3との誤代用、アップスケーラrelease資産差替え、古いヘッダーの契約矛盾、Torch/CUDA拡張ビルド失敗、公開されたモデルと本番実装の不一致。
- **U**：配布元byteは固定版メタデータに基づく整数である一方、release重みの真正性、本人のアカウント条件・ディスク・ドライバ・権利・実行ピークはUNKNOWN。実測分布がないため標準不確かさ`u_c`と包含係数`k`は数値化しない。

**ERROR CHECK**：研究文書・検査コード・調査JSONのみを変更。新規正式モデル採用0／HOLD・REJECT変更0、権利・データ保護の抜け道なし、モデル本体ダウンロード0、クラウド課金0、`main`変更0、取得承認0。機械学習／3Dグラフィックス／デジタルアーカイブ／ソフトウェア供給網／法律の5分野を分けて評価する。
