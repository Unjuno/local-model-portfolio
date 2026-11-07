# R35｜特殊動画モデルを「1つの学習状態＋必要ファイル」で保存するための実体調査（2026-11-08）

**重要な進展**：ChrisColeTech原配布元とfrtertaer複製先の**15モデル／補助重みのファイルサイズと公開LFS SHA256を全数照合し、完全一致**。両方のrepo全体を別の学習済み資産として保管する必要はない。また、ChrisとStubeliusの全ファイルをHugging Face公開APIから固定revision付きで調査し、丸め表示ではない必要byteが判明。[R35 取得承認前JSON台帳](../../catalog/research/2026-11-08-r35-ltx-pinned-file-census.json)。

## 1. 3配布元の固定コミットと現行ファイル総数

| 正規repo | 観測したfull git commit | ファイル数 | 全repoの現行ファイルサイズ（byte） |
|---|---|---:|---:|
| [ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | `592aaa11f13a7e480169455aa885f58c42d89766` | 43 | 166,915,795,579 |
| [frtertaer/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/frtertaer/LTX-2.5-uncensored-v1.1-FP8) | `66cfb26ed3639ccf9fb1360b37a523ed4f9c5c54` | 34 | 166,910,840,173 |
| [Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | `829cf2f7cbdf79872ff365787ba50f80006efe76` | 14 | 195,942,118,539 |

上記はHugging Faceの[公開モデルツリーAPI](https://huggingface.co/api/models/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8/tree/main?recursive=true)と[モデル情報API](https://huggingface.co/api/models/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8)を読み取った結果。過去版も含むストレージ課金量や、数値だけが似たモデルの量子化同一性とは別である。モデル本体はダウンロードしていない。

## 2. Chris原配布元・ミラーの同一性

モデル・推論補助重みに当たるGGUF/safetensors 15ファイルは、**共通パス15件がすべて同じLFS SHA-256と同じbyte**で、元だけにあるモデル重みと複製先だけにあるモデル重みは0件。一方、原repo43ファイル、ミラー34ファイルと、README・workflowやサンプル等の非モデルファイルに差がある。したがって**ミラーは同一重みの代替配布元として記録できるが、別の特殊モデルとして数えない**。複製先が合法的な取得権限や原作者のライセンス同意を代替するとは限らない。

**R32/R33の『原本とミラーの一致未検証』という保留を前進**：現時点で一致が確認されたのは、配布元のソースハッシュ情報である。転送後のローカル再ハッシュによる独立の内容検証は別途必要。配布元のバージョンが変われば再照合する。

## 3. Chrisの具体的な候補ファイル集合

通常量子化の重複を避けて、**1つの動画Transformer形式、対応するtext encoder、audio/video VAEを各1個**選ぶ。ここではFP8 scaledを保存研究の第一候補、Q6 GGUFを実用代替とした。補助upscalerは利用するworkflowにより選択する。

| 役割 | 正確なrepo相対パス | byte | 配布元提示SHA256 |
|---|---|---:|---|
| transformer_fp8_scaled | `split/diffusion_models/ltx25_uncensored_v1.1-fp8_scaled.safetensors` | 21,473,651,432 | `25a62cfdbcf7337c5c610447ce446330d21ccde44c8d31a4ae725bab0a9e9de9` |
| transformer_q6_alternative | `split/diffusion_models/ltx25_uncensored_v1.1-Q6_K.gguf` | 17,759,973,824 | `88b73acf4c798fc8f617c2209a863e2d7137dd1ddee38288ae9d5feb950c42ed` |
| gemma4_encoder_int8 | `split/text_encoders/gemma4_12b_ltx25_uncensored-int8.safetensors` | 13,157,517,698 | `61e0ada28e8e016e5c5bbd7a830b0c4ed4a574a203e0d7d347db6474b77d00c9` |
| audio_vae | `split/vae/ltx25_uncensored_audio_vae.safetensors` | 364,866,540 | `c52733d37f6a7fb7949c3dc0fb468c6cb2169e4d836983a73babb9f0d54837a5` |
| video_vae | `split/vae/ltx25_uncensored_video_vae.safetensors` | 1,472,223,346 | `847e14ca7f3355debca0cea4eaa24ac0fbcdf0061da054ac89ca638a869ddba3` |
| spatial_upscaler | `split/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors` | 995,778,752 | `eb5a71fe4068ee87ccdb1c3aa635e547ca76bd2d30ae20ae889f2c325c0677e8` |
| temporal_upscaler | `split/latent_upscale_models/ltx-2.5-latent-temporal-upscaler-x2-bf16-1.0.safetensors` | 261,944,000 | `2bc3300f2b3c3c1834d72164fbf13a3b9fd73e5a741e8a2c3f4035f89a75c3fe` |

| 研究用の暫定構成 | モデル重み等の選択byte | 完全実行構成か |
|---|---:|---|
| FP8 scaled動画モデル＋INT8 Gemma4 encoder＋audio/video VAE | **36,468,259,016** | いいえ、実行コード・外部依存等が未確定 |
| Q6動画モデル＋同じGemma4 encoder＋両VAE | **32,754,581,408** | いいえ |
| FP8 scaled基本構成＋空間・時間upscaler | **37,725,981,768** | いいえ、workflowによる追加依存は別審査 |

**誤った表示サイズも訂正**：モデルREADMEのQ6 GGUFは「約21.5GB」とあるが、現行ツリーの`ltx25_uncensored_v1.1-Q6_K.gguf`は**17,759,973,824 byte**。README表示を選択ファイルの確定バイトとして使わない。独立した動画品質試験やFP8対Q6の精度劣化測定は未実施。量子化という理由でFP8とQ6を2つの特殊モデルとして数えない。

## 4. Stubeliusの正確な全体容量と形式の重複

固定repo[Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)の**14ファイル総量195,942,118,539 byte**、重み7ファイル総量195,941,911,488 byte。最新版v1 BF16は**42,008,732,600 byte**、比較上の差額**153,933,385,939 byte**を確定。これは現在空きが増えた数字ではなく、全repoを保存するかv1 BF16一つを保存するかという**代替選択の容量差**。

ただしbeta1/beta2/v1は実際に異なる追加学習・マージ段階であり、その固有再現価値がある場合は複数段階を合法的な保存候補として維持できる。重複と呼べるのは、beta2のBF16/INT8やv1のBF16/INT8/NVFP4/GGUFなど同一学習状態の複数表現。元RL-LoRAのFP32アダプターも完全なv1マージ重みとは別の科学的成果として区別する。

## 5. 保留したままの取得・実行ゲート

Chrisのカードはlicense:unknown、StubeliusはLTX-2.x Community License。Lightricks本体・元LoRA/donorのLICENSE/NOTICE、正規アクセス権、必要なComfyUI/torch/driver/ABI、依存重みの正確な固定版を確認する。大きなモデル一式をダウンロードして試験した、品質を確認した、権利条件を満たした、とは主張しない。ユーザー申告の4TBと実際のHDD空き・200GB安全余裕も別々に測る。

## 6. H/T/D/C/Uと変数表

| 記号 | 意味 | SI単位 | 定義・定義域・型 |
|---|---|---|---|
| B_repo | リポジトリの現行ファイル総バイト | byte | Gitツリー内ファイル実サイズの合計、非負整数スカラー |
| B_core | 特定の実行構成の必須重みbyte | byte | 選択Transformer+encoder+VAEs、非負整数スカラー。外部依存未含 |
| B_src | 同一SHAで確認された配布ファイルbyte | byte | 公開LFS元情報から読取、非負整数スカラー。ローカルハッシュ再計算は未実施 |
| N_w | 重みファイル数 | 1 | Chrisは15、Stuubsは7、非負整数スカラー |
| R | 実機推論RAMピーク | byte | CUDA runtime、encoder、KV等含む。実測不明はnull、非負整数または欠損 |

**H**：複製先と原配布元は重み一致、同じ学習状態の多数の量子化を削減しても固有の特殊学習成果は維持できる。**T**：配布元モデルツリーAPIとfull commitで全重みを照合した。次は正規アクセス、実機ハッシュ、対象GPU・clock・batch・resolution・denoise steps・backend/ABI・quant/zero-point・VAEを固定した最低20プロンプト×3seedの同条件評価。**D**：SHA一致は配布元メタデータ同一性にPASS、モデル本体の受領・推論性能・実機と法的条件はUNCERTAIN、正式取得は未承認。**C**：mirrorのサンプル/ワークフロー差、量子化による映像・音声劣化、必要upscalerの見落とし、法的権利の非承継。**U**：元LFS SHAは配布元の検査値であり内容再検査なし、完全runtime依存・品質・実機残量は未知。合成標準不確かさu_cと包含係数kは未計算。単位検査：B_repo/B_core/B_src/Rはbyte、N_wは無次元。保存HDDと推論RAMの制約は別物。

## 7. ERROR CHECK・学際性・次に考える問い

R35は**15件のモデルファイルについて原配布元とミラーのSHAとbyteの一致**、3 repoのfull revision、選択coreのファイル合計、Stubelius7重みの容量と3つの学習状態を確認した。既存v19の150資産とNanbeige SELECT、4TB計画、取得キュー空は維持。重みダウンロードは0。応用分野はデジタルアーカイブ（重複排除）、供給網セキュリティ（出典とバイナリ同一性）、動画/音声信号処理（量子化品質）、ML訓練系譜（マージ状態の独立性）。

### 〈次に考える問い〉

同じ特殊版がFP8とQ6の両方で公開されるとき、いつ高精度保存を優先し、いつ低ビット実行版が長期保全の主要表現になるか。
