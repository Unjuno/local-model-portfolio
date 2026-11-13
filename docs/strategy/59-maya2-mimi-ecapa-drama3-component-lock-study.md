# R59｜Maya2 + Mimi/ECAPA・Drama3 Codec固定依存監査（2026-11-14）
 
**対象**：mainのv32（182資産、SELECT53・CONDITIONAL82、有効135件）。今回は**選定を追加・削除せず**、未確認7件中2件の最小構成を深化。完全復元/実機動作/ライセンス適用は未認定。モデル取得・実行/権利同意・取得承認は0件。

- [R59機械可読・4つの固定上流repoとファイルSHAs](../../catalog/research/2026-11-14-r59-maya2-drama3-cross-repo-components.json)
- [非実行の固定ファイル候補](../../manifests/drafts/r59-maya2-drama3-four-repo-source-subsets.candidate.json) — 正式 `*.lock.json` ではない

## 1. Maya2 の2学習済み依存を固定

| 公式リポジトリ | 不変40文字revision | 選択された重み部分（十進byte） | 許諾ラベル |
| --- | --- | ---: | --- |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | `87a83efdd6551e038246b6b37836a6264713eec3` | 5,004,879,768 | Apache-2.0 |
| [kyutai/mimi](https://huggingface.co/kyutai/mimi) | `89091b3e466eb6a9d11e537bf26b144f194978f7` | 384,649,828 | CC BY 4.0 |
| [speechbrain/spkrec-ecapa-voxceleb](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) | `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286` | 88,852,935 | Apache-2.0 |
| **3件の重み合計** | — | **5,478,382,531** | 異なる条件。混同不可 |

Mimiは`model.safetensors` 384,649,828byte、公式のテンソル要素表示 **96,151,393**。SpeechBrain ECAPAは`embedding_model.ckpt` 83,316,686byte、`classifier.ckpt` 5,534,328byte、`mean_var_norm_emb.ckpt` 1,921byte。これら3ファイルは各40文字revision `0f99f2d...`に固定され、上流LFSのある大ファイルにはSHA256を記録。**ECAPAの正確な学習済みパラメータ数はなお未確定**。

Mayaは元Qwenをfine-tuneした**2重みシャードにbackboneを含む**。Qwen元モデルを別の必須runtimeファイルとして再取得しない。Mimiは音声デコードに必要。ECAPAはreference speaker embed/cloneに必要だが、一部のnamed voiceでは使わない可能性がある。全20標準声とcloningを将来再現できるよう、ECAPAを機能別optionalではなくフル機能保全用依存として収録する。完全なコードや権利まで成立したわけではない。[Maya公式モデルカード](https://huggingface.co/maya-research/maya2-native/blob/87a83efdd6551e038246b6b37836a6264713eec3/README.md)／[公式実装](https://github.com/MayaResearch/maya2-native/tree/c6b376868e268551d065c4206193e96257bef4a1)。

公式runtimeが公表する**Linux/NVIDIA GPU/CUDA 12.8 driver、Python 3.10–3.12、Torch 2.8.0 cu128、Triton 3.4.0、Transformers 5.6.2、SpeechBrain 1.1.2** は作者のサポートする環境。エンドユーザー機材の実測済みという意味ではなく、同一clock・OS・batch・cache長での性能検証は別の段階。

## 2. Drama 3は別Codecを必ず含める

[Fish Audio Drama 3公式モデル](https://huggingface.co/fishaudio/drama-3/tree/78e5ab79e49aa9a25abe8799eff2c4d73a1c3216)の15シャードは合計 **39,603,551,368** byte。これだけでは音声の再生・編集を再現できない。別学習済み`codec.pth`は**1,871,099,728 byte**、上流SHA256 `74fc41c5a7151c6f350af8bd7e5d6e3accfcc7f3dfbfac23afd35af07052bb2f`。主モデル＋Codecの重みは**41,474,651,096 byte**。licenseは**Fish Audio Research License**であり「一般のApache/MIT」と扱わない。

`codec.pth` はPyTorch pickleの形式を含む（Hugging Face公開ページに `torch._utils._rebuild_tensor_v2` 等を表示）。**SHA256が一致しても安全なロードとはならない**。非実行のダウンロード工程で`torch.load`等に渡してはいけない。[公開元Codec固定版](https://huggingface.co/fishaudio/drama-3/blob/78e5ab79e49aa9a25abe8799eff2c4d73a1c3216/codec.pth)。

[公式SGLang-Omni解説](https://github.com/sgl-project/sglang-omni/blob/main/docs/cookbook/fishaudio_drama3.md)のDrama3推論エンジンは**Triton attention backend**を要求。現行コードHEADを `0a624b1e7974b74cff14497b01db7272f052594d` として記録したが、特定runtimeが本人のOS/GPUで動くことは未確認。別のMLX/INT4形式も同じ重みの単純コピーとは限らないので、通常形式違いは初期取得には増やさない。

## 3. 保存容量の解釈と取得停止

本監査の四つのソースの **選択ファイル参照 48件・計 46,997,323,799 byte**は、README/LICENSE・tokenizer/voice metadataなど必要と思われる小ファイルを含む固定ソース部分。モデル本体をローカル保存した実測容量ではない。開発元のruntimeソース、環境依存、追加権利、staging/cacheピーク、実物HDDの空きは未測定。

Maya2・Drama3の`UNVERIFIED_BLOCK_FINAL_LOCK`は維持する。Maya2外部ECAPA、Drama3 Codecの正確な学習済みテンソル数や合法な利用範囲が分からない段階で「150B未満完全確定」と判定しない。**コンポーネントの有用性・正確な源サイズ・上流SHAの確認は、取得権限の確認に等しくない**。

## 4. 検証仮説と実装前提

H：Maya主重みと別Mimi/ECAPAの固定版を組合せれば、重要な音声codec・話者条件を再構成するための証拠が揃う。Drama3のCodecが欠けた重みのみの保存は不完全。

T：原Publisher Hub 4 repoのファイル一覧と上流SHA、source revisionを照合。最小検証n=4 repo、モデル内からTensorをロードしない。将来の品質/速度計測は各30例以上、同一HW/clock、backend/driver、batch、context/KV、dtype、zero-pointを固定し、可能ならストリーミングTTFAとCER/DERを評価。

D：PASS＝各sourceのファイルのrevision/SHA/byteを静的固定。FAIL＝Codec/encoder漏れや量子化を別学習資産と誤認、違法取得。UNCERTAIN＝完全オフライン復元、依存コードの正確なABI、実測速度とライセンス・本人認証。

C：Maya voice modeの一部でECAPAが不要、あるいは追加encoderを要求、Drama3`codec.pth`が異なる版と非互換、声や学習データに別権利。

U：公開Hubメタデータと外部runtimeの未検証、真の重みハッシュ未実測、音声データ権利、物理HDDを誤差源とする。計量試験ではないため合成標準不確かさu_cと包含係数kは未算定。

| 記号 | 意味（日本語） | SI単位 | 定義・前提／範囲 | 型 |
| --- | --- | --- | --- | --- |
| B_m | Maya単体・音声依存を含む重み量 | byte | 5,478,382,531、上流固定ファイルの合算・非負 | 整数スカラー |
| B_d | Drama3の主15シャードとCodec量 | byte | 41,474,651,096、実ファイル未取得 | 整数スカラー |
| B_s | 4つの選択ソース部分総量 | byte | 46,997,323,799、ソフトウェア等除外 | 整数スカラー |
| N | 固定ファイルの参照件数 | 1 | 48、ファイル数・非負 | 整数スカラー |
| P_e | ECAPAを含むパイプライン総学習済み数 | 1 | null（未確定）、全必要部品を数える | 整数/null |

次元チェック：B_m/B_d/B_sはbyte、N/P_eは無次元。Byteの合算とパラメータ総数の合算を混ぜない。

**ERROR CHECK**：v32の182件・有効135件・UNKNOWN有効7件を保持。4 source repo固定版、Maya主2＋Mimi1＋ECAPA3、Drama主15＋Codec1の学習済み重みファイルをsource SHAと固定。承認・取得・実機実行・ブランチ新設は0件。

〈次に考える問い〉：Maya2の複数voice modeが要求する最小依存を実際に静的追跡し、Mimi/ECAPAへのruntime参照と保存形式が一致するかを先に証明できるか。
