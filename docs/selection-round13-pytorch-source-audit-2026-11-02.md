# 第13回：PyTorch Hub・原研究GitHubの独立重みを横断審査

> **調査日：2026-11-02。選定調査のみ・権利/取得/実行未承認。** HF以外のモデルを扱うとき「PyTorch」という単一の保管場所は存在しない。公式の[PyTorch Hub](https://pytorch.org/hub/)の`hubconf.py`から起動するモデル、作者GitHub Release配布物、Meta/NVIDIAのCDN原本、旧TorchAudio/TorchText実装を分ける。GitHub元ソースのコミットと各モデルの実際の重み配布先を第一に追跡する。

## 1. 実際に起きている提供/互換性の変化

- [PyTorch公式ブログ（2026-10-05）](https://pytorch.org/blog/evolution-of-the-pytorch-media-processing-landscape/)は、TorchCodecに音声・動画/画像の入出力を集約し、TorchVision/TorchAudioからモデル/データ/パイプラインの主な開発対象を縮小したことを説明。TorchAudio 2.8で非推奨になった機能の一部は2.9から削除済み。重み単体より**実行時API・FFmpeg/ABIの履歴の保全**も重要。
- [TorchText](https://github.com/pytorch/text)はArchived。旧版の最後の公式`v0.18.0`ソースcommit `9bed85d7a7ae13cf8c28598a88d8e461fe1afcb4`を旧ソフトウェア候補にする。重みの独自配布/存在まで証明するものではない。
- [Demucs](https://github.com/facebookresearch/demucs)、[Denoiser](https://github.com/facebookresearch/denoiser)の元コードはArchived。Demucs原READMEは開発者離脱と保守終了を明示。一方、元重みは別の`dl.fbaipublicfiles.com`で公開される設計。**元コードのArchived ≠ 重みが消去された**。
- [InsightFaceのモデル規約](https://github.com/deepinsight/insightface)はソースMITと事前学習重みの非商用研究制限を別に定め、2025-11からface-swap/recognitionの個別ライセンス問い合わせを告知。非商用研究の範囲・本人同意と再配布可能性を確認するまで取得に進めない。

## 2. モデル系の保存・調査候補5件

| プロジェクト / 配布元 | 調査優先 / 状態 | モデル側で確認できた容量 | 明確なリスク・制約 |
| --- | --- | ---: | --- |
| [snakers4/silero-vad](https://pytorch.org/hub/snakers4_silero-vad_vad/) | A / PROMOTE_TO_FILE_SCOPED_CANDIDATE | 2.322 MB（source + jit） | 公開MIT（ただし実行安全性審査） |
| [facebookresearch/demucs](https://github.com/facebookresearch/demucs) | A / PIN_SOURCE_AND_ORIGIN_MODEL_POINTER_NEXT | 未確認 | 源コードがGitHub Archived |
| [facebookresearch/denoiser](https://github.com/facebookresearch/denoiser) | A / PIN_SOURCE_AND_ORIGIN_MODEL_POINTER_NEXT | 未確認 | 源コードがGitHub Archived |
| [sczhou/CodeFormer](https://github.com/sczhou/CodeFormer) | B / CONDITIONAL_NONCOMMERCIAL_RESEARCH_CANDIDATE | 539.425 MB（暫定3重み） | 独自非商用ライセンス |
| [NVlabs/stylegan3](https://github.com/NVlabs/stylegan3) | B / CONDITIONAL_NONCOMMERCIAL_ORIGINAL_RESEARCH_CANDIDATE | 未確認 | 独自非商用ライセンス |

### 2.1 Silero VAD：唯一のファイル単位・低コストに近い候補

公式[PyTorch Hub](https://pytorch.org/hub/snakers4_silero-vad_vad/)掲載モデル。作者の[`snakers4/silero-vad`](https://github.com/snakers4/silero-vad/tree/066409f3d9db45a30d21dfcbf9147826ffdd7052)の完全commitに`silero_vad.jit`が**2,272,526 B**で埋め込まれており、`LICENSE`本文はMITと確認。`hubconf.py`、`src/silero_vad/utils_vad.py`、設定等を選んだ**9ファイルのモデル側＋選択ソース合計2,321,515 B**を[JSON台帳](../catalog/reviews/pytorch-source-originals-2026-11-02.json)に記録。別ONNX形式を理由なく同時保存しない。

ただし、Git treeの40文字blob IDはGit SHA-1であってファイル本体SHA-256ではない。自動`torch.hub.load`/`torch.jit.load`は禁止。正しいエンドポイント検出や推論速度を今回実測したわけではない。

### 2.2 DemucsとDenoiser：Archivedのモデル原本

Demucs v4の[固定pretrained.py](https://github.com/facebookresearch/demucs/blob/e976d93ecc3865e5757426930257e200846a520a/demucs/pretrained.py)はMeta CDNを参照し、[`remote/htdemucs.yaml`](https://github.com/facebookresearch/demucs/blob/e976d93ecc3865e5757426930257e200846a520a/demucs/remote/htdemucs.yaml)と[`remote/files.txt`](https://github.com/facebookresearch/demucs/blob/e976d93ecc3865e5757426930257e200846a520a/demucs/remote/files.txt)から`htdemucs`原本の重み名`955717e8-8726e21a.th`まで確認した。ただし**現在のCDN応答・厳密バイト・完全SHA-256・重み自体の利用許諾は未検証**。旧ソースMITと学習曲原本の利用条件を混同しない。`htdemucs_ft`は4モデルのensembleで、単一モデルではない。

Denoiserは旧[固定pretrained.py](https://github.com/facebookresearch/denoiser/blob/8afd7c166699bb3c8b2d95b6dd706f71e1075df0/denoiser/pretrained.py)に`dns48-11decc9d8e3f0998.th`などの元URLが存在。リアルタイム音声ノイズ除去はTTS・ASRでは代替できないが、権利がCC BY-NC・重みの容量/現在の入手性未検証のため取得は条件付きで止める。

### 2.3 CodeFormerとStyleGAN3：人物生成・復元の独立研究

CodeFormerの[GitHub Release v0.1.0](https://github.com/sczhou/CodeFormer/releases/tag/v0.1.0)は`codeformer.pth`を376,637,898 Bで提供。顔検出ResNet50 109,497,761 Bとparsing BiseNet 53,289,463 Bを加えた**参考選択3重み539,425,122 B**を記録した。これは完全実行バンドルではない。コードを含め適用される[NTU S-Lab License 1.0](https://github.com/sczhou/CodeFormer/blob/master/LICENSE)は**非商用**。Github Release metadataに資材のSHA-256 digestは見当たらないので、モデル実体の照合は未実施と明記。

StyleGAN3の[元研究実装](https://github.com/NVlabs/stylegan3)は一時的に公開した研究コードであり、[NVIDIA Source Code License](https://github.com/NVlabs/stylegan3/blob/main/LICENSE.txt)のSection 3.3が非商用研究/評価に用途を限定する。選ぶ候補は`stylegan3-r-ffhq-1024x1024.pkl`の原本だが、**NGCで現在取得できるか、原本bytesと完全SHAをまだ確認していない**。`.pkl`を実行せず、学習画像・人物の権利と元GAN重みの再現性を審査する。

## 3. 権利/本人同意の問題で取得保留4件

| 配布元/モデル | 配布元で示されたサイズ | 判断理由 |
| --- | ---: | --- |
| deepinsight/insightface:cheetah_s | 27.116 MB | One of the smaller original face/person recognition packages (PersonAnalysis). Source SDK is MIT but official pretrained weights are noncommercial research only. Data subject consent and any special licensing/manifest authorization must be reviewed. Release is current (2026-10-03 upload). |
| deepinsight/insightface:inswapper_128 | 554.254 MB | The author announced special contacts for face-swap licensing in 2025-11. The GitHub published ONNX binary is not proof of unlimited commercial or identity-image rights. Do not use for nonconsensual identity editing or tracking. |
| Rudrabha/Wav2Lip | 未知 | Original lip-sync model weights are linked through Google Drive; the author states research/academic/personal use only and forbids commercial use because of LRS2 training data. Current downloadable complete checkpoint and hashes not checked. Existing LatentSync overlaps task but not original weights. |
| snakers4/silero-models:v5_cis_base_nostress | 未知 | Original Silero Models repository LICENSE is CC BY-NC-SA 4.0, but LICENSE_CIS is MIT. Must prove this particular chosen CIS model is covered by permissive LICENSE_CIS and the source server's required distribution and data rights. Dataset and speaker permission distinct. |

InsightFaceの[model-zoo GitHub Release](https://github.com/deepinsight/insightface/releases/tag/model-zoo)には、`cheetah_s.zip` **27,116,086 B**、`inswapper_128.onnx` **554,253,681 B**が公開されており、GitHub Release APIが両方のSHA-256 digestを公表。**ウェブ上に重みが存在することと、適用用途に許諾を得ていることは別**であり、ライセンス・個人情報・同意を確認するまでHOLDとした。

元Wav2Lipの[公式README](https://github.com/Rudrabha/Wav2Lip)はLRS2を用いた学習のため商用禁止と記載し、Google Driveの配布先を示す。ファイルの正確な容量・現在の完全入手性・SHAは未確認。既存LatentSyncと機能が一部重なるため、性能や原本の学習差で追加価値を確認するまで保留。

Sileroの[総合TTSリポジトリ](https://github.com/snakers4/silero-models)は基本`LICENSE`にCC BY-NC-SA 4.0があり、別`LICENSE_CIS`はMITを含む。例として`v5_cis_base_nostress.jit`が作者の`models.yml`にあるが、**ファイル単位でどちらのライセンスに属するか、本人の音声使用権を確認していない**。従ってMITと断言して追加しない。

## 4. 今回は優先追加しない比較対象

| モデル/実装 | 審査 | 理由 |
| --- | --- | --- |
| facebookresearch/pytorchvideo:efficient_x3d_xs | WATCH_R2 | Official PyTorch Hub action classification differs from generative video but the repo remains active; no observed removal. Independent checkpoint hash, file size and exact preprocessing are not pinned. |
| TencentARC/GFPGAN:GFPGANv1.4.pth | WATCH_COMPARE_CODEFORMER | Official pretrained portrait restoration competing with CodeFormer; root code license says Apache2 excluding third-party components. No independent same-task quality or additional value established. |
| s0md3v/roop | WATCH_SOURCE_ONLY_NOT_EXTRA_WEIGHT | Project is archived with AGPL code, but original independent weight asset was not verified; it depends on externally licensed face swap model packages. Do not mistake code-only wrapper for a distinct archive checkpoint. |
| NVlabs/stylegan2-ada-pytorch | WATCH_SUBSTITUTE_STYLEGAN3 | Historical GAN baseline and older source. Compare alias-free StyleGAN3 original with older StyleGAN2 variant; do not automatically retain every training set/resolution/checkpoint. |

## 5. PyTorch読み込み自体の危険

[PyTorch GHSA-63cw-57p8-fm3p](https://github.com/pytorch/pytorch/security/advisories/GHSA-63cw-57p8-fm3p)は2026-01-26公開、`torch.load(weights_only=True)`でも細工されたcheckpointからRCEの可能性があることを説明。影響バージョン<=2.9.1、修正>=2.10.0。**修正版ならどんな`.pth/.pt/.pkl`も安全だという意味ではない**。

公式[PyTorch Hubの仕様](https://docs.pytorch.org/docs/stable/hub.html)は`torch.hub.load()`がGitHubコードをimportして呼び出すと説明。したがって**ウェブページを見つけたらtorch.hub.loadでチェックする**こと自体が危険。将来のローカル試験は、データとして保存→出所署名/ハッシュ→旧ソフトウェア/依存のソースレビュー→無ネットワーク隔離環境→許可されたモデルロード、の順とする。

旧PyTorch2.8/2.9が必要なコードでも、当該旧ライブラリを現在のパソコンで直に実行しない。TorchText v0.18.0およびTorchAudio v2.8.0は**モデル重みではなく旧ソフトウェア資産**として別に保存計画を作る。TorchCodecは既存のランタイム候補と共有し、同じソースを二重計上しない。

## 6. 容量・次段階の結論

今回**容量が整数で確定した選択資材**はSilero VADモデル側＋ソース **2,321,515 B**、CodeFormerの参考3重み **539,425,122 B**。他モデルの完全バンドル容量は**未知**。InsightFace小型パックのサイズが分かっていても**権利HOLD**なので取得予算の採用量に加えない。

現在の正式台帳v2は110件・有効94件、上流repoベースの暫定3,234,067,678,260 B。今回は選定レビューのみで、**新規容量を現行TBに加算していない**。既存の3.8TB上限・最低空き200GB・ピーク推論RAM<512GBの条件を維持。取得マニフェスト、パッケージダウンロード、Gated同意、Torrent接続、HDD操作、実行は一切行わない。

## H/T/D/C/U

| 項目 | 反証可能な検証 |
| --- | --- |
| H | 原研究リポジトリの固定コードとオリジナルcheckpointを保存すれば、HF一覧に未登場の専門能力と提供停止リスクを独立に保全できる |
| T | GitHubコミット・公式ハブのcheckpoint URL・ReleaseアセットのサイズとSHAを一件ずつ照合。元モデルの合法利用条件、tensor serialization、全依存を検証。実行や取得は許可まで停止 |
| D | PASS_METADATA：固定のID・commit・配布元・表示容量が一致。UNCERTAIN：外部weightリンクの現稼働、重み/データ権利、容量、実機RAM、推論精度は未確認。FAIL：許諾違反、捏造原本、必要資材が欠落 |
| C | 元repoがArchivedでもCDN重みは生きている、別の合法コピーで再現できる、古い依存コードの代わりに現行実装で同等結果が得られる、学習原本の違いが無い |
| U | 配布元リンクの変動、コード/重みライセンスの相違、GitHub Release mutable asset、PyTorch pickle危険性、OS/CUDA ABI、モデル比較の実測不足が主要不確かさ。統計モデル未定義のため合成標準不確かさと包含係数は数値評価しない |

## ERROR CHECK

PyTorch Hub直結と一般のPyTorch実装を明確に分け、サイズのないファイルを0Bとして計上しない。パブリッシャーのSHAとGit SHA1は別。将来規制予測は事実と区別。モデル重みの配布権限は人間が承認し、第三者の肖像・音声同意を無視しない。

