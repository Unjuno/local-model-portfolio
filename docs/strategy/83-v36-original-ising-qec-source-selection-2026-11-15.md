# v36｜NVIDIA Isingで異なる2種の量子誤り訂正モデルを正式選定（2026-11-15）

## 1.〈本論〉実際の学習済みモデルを比較

[v36正本191資産・有効144件](../../catalog/effective-portfolio-2026-11-15-v36.json)はv35の189件を**そのまま保持**し、2件の別学習済み量子誤り訂正CNNをCONDITIONALに追加した。[差分](../../catalog/revisions/v36-2026-11-15.json)／[固定sourceのファイル一覧](../../catalog/research/2026-11-15-r80-three-specialist-actual-source-scope.json)。

| 原本 | 内部構造（NVIDIA一次ソース） | 重み原本の公開情報 |
|---|---|---|
| [Ising ColorCode Fast](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | 三角色符号、stem Conv3d＋6個の残差bottleneck、embed512、受容野13、訓練d=T=13 | 5,899,248 bytes、SHA256 `ca17d20ebf40d32360f9b60648b47e03de71d4e4d3c3eea33d311dcf1b2510c9`、モデル要素公表2,936,580 |
| [Ising SurfaceCode Fast](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | 回転表面符号、4層のConv3d、ch 4→128→128→128→4、kernel3、受容野9、訓練d=T=9 | 1,826,360 bytes、SHA256 `22db7ad25b584d7588493d6ef815381c8d1263cfb29f212391a591b285ad0a05`、コード導出912,772パラメータ |

使用した一次ソースは[NVIDIA Isingモデルregistry](https://github.com/NVIDIA/Ising-Decoding/blob/12bbeb13c5cfc1a064171ac91b07aea61f2eaae8/code/model/registry.py)・[predecoder実装](https://github.com/NVIDIA/Ising-Decoding/blob/12bbeb13c5cfc1a064171ac91b07aea61f2eaae8/code/model/predecoder.py)（commit固定）と、各Hugging Faceのcommit固定ファイルAPI。独立研究論文は[ColorCode arXiv:2607.10058](https://arxiv.org/abs/2607.10058)、[SurfaceCode arXiv:2604.12841](https://arxiv.org/abs/2604.12841)。

**重要な限界：** 両社repoの重みファイルの匿名アクセスは401 Gated。公開APIでは名称・サイズ・LFS SHAは確認できるが、**チェックポイントの実際のtensor headerを見たとは主張しない**。CNN構造は公開ソースに基づく。個人認証・モデル本体取得・起動・外部decoderの完全閉包は未確認。正式な研究選定を承認済みダウンロードと混同しない。

## 2.〈応用・転用例〉選定と非選定

- 元のv33 Granite LLMON3B／PPLX Decider／Kumo Relational、v34 Kumo Tabular／Anomaly、v35 Muse Glimmer original／別学習DFlash assistant は保持した。一般LLMやQwen量子化はQECとは別の能力であり、QECの2checkpoint同士も異なる符号幾何・雑音分布に最適化され、相互置換しない。
- **Nemotron 3.5 Parseは非追加**。既に選定済みのLightOnOCR-3とPaddleOCR-VL-1.5と文書読解用途が重複し、実験で増分有効性が認められていないため。
- 本2件の候補選定ファイル（重みと必要な小型説明・ライセンス情報）は**7,760,518 bytes**。完全な物理保存必要量、global QEC decoder、PyMatching/Chromobius、コード依存、学習ノイズデータ、実HDD空きは未測定。4TB計画／最低実空き200GB／150B量子化例外は維持。**取得承認0件**。
- SurfaceCode原本はHFライセンスタグ`other`、作者カードはNVIDIA Open Model License。ColorCodeはOpenMDW1.1。権利条件を混同しない。

## 3.〈変数表・H/T/D/C/U・ERROR CHECK〉

| 記号 | 意味（日本語） | SI単位 | 定義・定義域・前提 | 型 |
|---|---|---|---|---|
| N | 有効資産件数 | 1（件） | 144、SELECT53＋CONDITIONAL91 | 整数スカラー |
| P | SurfaceCodeパラメータ個数 | 1（個） | 912,772、各Conv3d biasありの作者コードから導出 | 整数スカラー |
| B_c | ColorCode原本の選定ファイル容量 | byte | 5,920,963、5ファイル、発行元メタデータ | 整数スカラー |
| B_s | SurfaceCode原本の選定ファイル容量 | byte | 1,839,555、3ファイル、発行元メタデータ | 整数スカラー |
| B | 2モデルの選定参照容量 | byte | B_c＋B_s＝7,760,518 | 整数スカラー |

次元チェック：B_c/B_sはbyte単位で加算可能。P（パラメータ）とN（資産）は件数を表す無次元量で、byteへ加算しない。PはConvの(入力ch×出力ch×27＋出力ch bias)を4層について足した結果。結果は公開モデルの約913kと一致するが実重みヘッダの独立計測ではない。

**H**：2checkpointは別の符号と雑音に学習した代替不能な学習成果。  
**T**：n_min=2の固定配布元APIとNVIDIA固定実装、2原論文を比較。匿名401なら本体読取を停止。  
**D**：原本SHA/byte、独立アーキテクチャの一次コードはPASS。本人Gated許可、実体SHA、実機品質、完全ライセンス/依存、HDDはUNCERTAIN。  
**C**：実体と作者公表との不一致、別雑音への移植失敗、権利未取得。  
**U**：物理ファイル、本人認証、compiler/driver/ABI、global decoder実測が未確認。分布がないため合成u_c／包含係数kは未算定。

**ERROR CHECK**：v35全189件保持→v36 191登録／144有効／165モデル＋26データ、19件Gated、全パラメータ未確認の有効9、取得承認0。重みDL0・実行0。研究証拠を正本へ反映したが物理アーカイブの完成とは宣言しない。

関連分野：量子情報、機械学習、ソフトウェア供給網、デジタル保存、ライセンス・アクセス制御。

## 4.〈次に考える問い〉

Gatedで元checkpointを取得できない期間、再現性を高めるためにノイズモデル・回路幾何・原論文の訓練条件をどこまで固定できるか。
