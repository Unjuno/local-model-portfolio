**R35最新追補（2026-11-08）**：Chris原repoとfrtertaerミラーは、ファイル数と非モデルファイルに差があるが、モデルと補助重み15件のLFS SHA256とbyteが全一致。前回の『ミラーが同一重みとはいえない』はこの固定版に限って訂正。LTX2.5特殊版の正確な選択構成は[R35](34-r35-ltx-source-vs-mirror-file-identity.md)。Stubelius v1 BF16も**42,008,732,600 bytes**と確定。

# R33｜LTX特殊版の元donor訂正とアダプター容量の完全固定（2026-11-07）

## 1. 〈本論〉— R32の10Erosの版指定は誤りだった

**訂正**：R32は10Erosのv1 BF16を追跡したが、[Stubeliusの一次NOTICE](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/NOTICE.txt)は明確に**10Eros v1.5**をbeta1のタスクベクトル供与元として指定する。これは同じ名前の通常量子化とは別の**後学習バージョン**であり、v1のSHAをv1.5へ転用してはならない。R32は研究履歴として保存し、以下のR33記録を正とする。

### 完全版を特定できた3ファイル（Git LFS原本の登録）

| ファイル | バイト（正確） | 配布元提示SHA-256 | 正確なGitコミット40桁 | 判断 |
|---|---:|---|---|---|
| [10Eros_v1.5_bf16.safetensors](https://huggingface.co/TenStrip/LTX2.3-10Eros/commit/99be68b2b6a3f68cde86b3b70e6f71bc26e726fb) | 46,139,886,366 | `2383d87bc1eea4fc00b73a52eb177bea868c2c46da621511acf9e54b92309f24` | `99be68b2b6a3f68cde86b3b70e6f71bc26e726fb` | HOLD_LINEAGE_VERIFIED_CAPACITY_NOT_APPROVED |
| [LTX-2.3-RL-Lora/adapter_model.safetensors](https://huggingface.co/zghhui/OmniNFT/commit/f9546e6c51b02b901abc8b2cb0716439594eff8a) | 1,233,512,728 | `c8e59836f28a6a7d2660f2652a156e77493ba82fb53a1e1e84f258fdf94ac608` | `f9546e6c51b02b901abc8b2cb0716439594eff8a` | CONDITIONAL_PREFER_ORIGINAL_OVER_CONVERTED_COPY |
| [loras/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors](https://huggingface.co/Kijai/LTX2.3_comfy/commit/ebb24a4a410308bd701438159f341a4060edd87f) | 616,948,520 | `204b491f76da5c7ef0998dee636b4db695a00d28729ebccfda8dfdc3c37df63c` | `ebb24a4a410308bd701438159f341a4060edd87f` | DO_NOT_ADD_INDEPENDENT_MODEL_SLOT; RUNTIME_ALTERNATIVE_ONLY |

10Eros v1.5の原本は46,139,886,366 byte、[配布元LFSコミット](https://huggingface.co/TenStrip/LTX2.3-10Eros/commit/99be68b2b6a3f68cde86b3b70e6f71bc26e726fb)で確認した。OmniNFT LTX2.3版の正確なbyteは1,233,512,728で[作者のLFSコミット](https://huggingface.co/zghhui/OmniNFT/commit/f9546e6c51b02b901abc8b2cb0716439594eff8a)に記録。両者は2026-11-07にダウンロードして再ハッシュしたものではなく、公開元のポインター値の読取である。

### 元LoRAとComfyUI版を別モデルに数えない

[KijaiのComfyUI変換](https://huggingface.co/Kijai/LTX2.3_comfy/commit/ebb24a4a410308bd701438159f341a4060edd87f)は、OmniNFT LTX2.3のLoRAをFP32からBF16に変換し、元のrank32・alpha64に対応するUI適用強度2.0を明記する。Kijai版は616,948,520 byteで、元の1,233,512,728 byteより小さい。しかし**同じ学習済み更新を型とローダー形式だけ変えた表現**であって、独立した強化学習成果ではない。BF16を逆変換しても元FP32の値をビット単位で戻せないので、元学習情報の保存を優先するなら元FP32 LoRAを検討する。ComfyUI版はruntimeの代替であり、両方の自動取得は認めない。

### 既存Stubelius本体・Chris複製の固定できた部分

Stubelius公開repoの最新コミットは[829cf2f7cbdf79872ff365787ba50f80006efe76](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/commit/829cf2f7cbdf79872ff365787ba50f80006efe76)。v1 BF16本体の公開SHAは`6e0ff9c9d8a1d0747579f1f50d10a9c3822a9a8f265322a5edd476044b0fbf4f`。約42GBだが、本調査では**正確なbyteとGemma4/二種VAEの完全な依存構成は未確定**。一方、ChrisColeTechの複製`frtertaer`は2026-09-14の[66cfb26ed3639ccf9fb1360b37a523ed4f9c5c54](https://huggingface.co/frtertaer/LTX-2.5-uncensored-v1.1-FP8/commit/66cfb26ed3639ccf9fb1360b37a523ed4f9c5c54)でコピーされたが、Chris本体にはその後2026-09-15の重み変更と2026-10-15のワークフロー追加がある。**現在のChrisと複製先の重みが一致する保証はない**。5元LoRAの説明は引き続き作者由来のレシピ証拠で、ハッシュ一致は未検証。

## 2. 〈応用・転用例〉— 量子化で音声だけ悪化する実例

[JoaoZaokkの10Eros v1.5通常量子化](https://huggingface.co/JoaoZaokk/10Eros-v1.5-W4A8-ConvRot)には16,641,963,302 byteの動画・音声ともW4A8版と、19,107,895,342 byteの動画W4A8＋音声INT8版がある。量子化担当作者は、前者では音声に金属的なノイズがあり、後者は改善すると述べる。**作者の試聴であり、独立した聴感試験ではない**。特にBF16比較ではGemmaのtext encoder構成が違うため、完全な同条件対照ではない。保存時はこの二つを新しい特殊学習状態2個と数えず、品質・環境の条件を合わせたうえで片方の**実行表現**として評価する。Ampere/Ada用SM8.xカーネルで、Hopper/Blackwellは速度未測定。

## 3. 保存順位と反証可能なゲート

1. **OmniNFT元FP32 RL-LoRA**：rank32・alpha64という実験成果を最小容量で記録できる。既存のLTX2.3親と権利の検証が必要。**CONDITIONAL研究**、取得承認は0。
2. **Stubelius v1 BF16**：同じRL-LoRAだけでなく10Eros v1.5とSulphur2の転移、LTX2.5蒸留LoRAを複合した固有マージ。元LoRAの代替ではない。**CONDITIONAL研究**、本体42GBと依存・許諾の最終ロック未完。
3. **10Eros v1.5 BF16**：マージ前の独立SFT/Style学習状態で、元に戻したり別マージを再生産するなら価値がある。ただし46.14GBの追加は『Stubeliusにも統合済み』の重複費用に見合うか検証が必要。**HOLD**。
4. **Kijai BF16変換、JoaoZaokk通常量子化**：別の学習資産数としては追加0。対応する実行機器・定量品質の理由ができた場合のみ代表形式として採用。
5. **ChrisColeTech v1.1**：複製先の5マージ説明は記録したが、今の原作者repoの重みSHA・ライセンス・Gemma encoder等を検証するまで正式保存しない。

## 4. H／T／D／C／U、変数表、次元確認

| 記号 | 日本語の意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| B_src | 元学習済み重みの選択容量 | byte | 固定Git LFS登録値、非負整数スカラー。全pipelineでない |
| B_conv | 対応する変換形式の容量 | byte | 固定Git LFS登録値、非負整数スカラー。全pipelineでない |
| N | 動画比較の独立入力件数 | 1 | 20件以上、整数スカラー |
| K | 各入力の独立乱数seed数 | 1 | 3以上、整数スカラー |
| R_peak | 推論の実行時ピークRAM | byte | driver、video/audio VAE、encoder等込み、非負実数または未計測null |

**H**：10Eros v1.5、OmniNFT元RL-LoRA、Stubeliusマージには互いに代替不能な学習状態があり、Kijai/JoaoZaokk量子化は別学習ではない。**T**：固定40桁コミットとLFS hash、親のモデル、権利、ComfyUI/PyTorch/CUDA/driver/quantization zero-point/ABI、batch、8-step、CFG1、音声VAE、video VAEの対応を確認し、最低20入力×3seedの映像・音声別ブラインド評価。**D**：権利＋依存＋実際の品質差・固有再学習価値が揃えば保存検討PASS、ただの精度違いを別学習モデルとするならFAIL、現時点の性能・権利・総容量不足はUNCERTAIN。**C**：LoRA親の不一致、音質劣化、Chrisミラーの古い状態、誤った10Erosバージョンの投入。**U**：未知の実機HWと評価データ、派生ライセンス、ランタイム変数が大きく、合成標準不確かさu_cと包含係数kは数値化不可。**単位チェック**：B_src/B_conv/R_peakはbyte、N/Kは無次元。ディスクとRAMを足して一つの必要容量としない。

## 5. ERROR CHECK・関連分野・問い

**ERROR CHECK**：正しい10Eros v1.5、元OmniNFT FP32、Kijai BF16の3件は完全Gitコミット40桁、64桁LFS SHA、正確なbytes付き。v1とv1.5を混同しない。元LoRAと変換BF16は学習済み状態を二重計上しない。v19の150資産・有効105・4TB計画・Nanbeige SELECT、空の取得キューは変更しない。ファイル取得やベンチは未実施。

**学際性**：MLの強化学習とLoRA、数値解析（FP32/BF16の不可逆丸め）、音声・映像工学（同期と音声量子化の劣化）、供給網・法務（LFS証跡と派生許諾）を横断。

### 〈次に考える問い〉

同じ1.23GBのRL学習成果を残すとき、再現可能性を最優先したFP32原本と、すぐ使えるBF16変換版のどちらが長期保存価値を高くするか。
