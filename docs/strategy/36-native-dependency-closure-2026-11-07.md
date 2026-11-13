# 36 — 音声Codec・映像Pipeline・Tokenizerの復元依存調査（2026-11-07）

## 監査対象と変更しないもの

対象は`CURRENT.json` v26-20261106、172資産・有効125件、固定された一次ファイル容量は総和**3,406,271,632,830 B**、既知内容識別子による論理重複排除後**3,403,245,899,240 B**。4TB差額596,754,100,760 Bは所有者の空きではない。未解決の依存・権利・実装は34資産、完全なオフライン復元容量・実物ハッシュ・ディスク空き・取得ピークは未測定。選定や承認は今回変更しない。

今回の新事実：**OpenMOSS-Team/MOSS-TTS-v1.5 の固定processor実装は、明示`codec_path`がなければ`OpenMOSS-Team/MOSS-Audio-Tokenizer`を別途`AutoModel.from_pretrained`で読み込む。** このaudio codecの重みと推論コードを別に保全しない限り、オフラインで正常な音声を復元できない恐れがある。**v2は別の48kHzステレオcodecで、MOSS-TTS-v1.5のデフォルトではない**。同じ名称の派生というだけで代用しない。

一次証拠： [固定版MOSS processor実装](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5/raw/cdd3b911b1585e3f2dbc7775ef10f9926f58850a/processing_moss_tts.py)、[OpenMOSS-Audio-Tokenizerモデル](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer)、[v2モデル](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-v2)、[MOSS音声Codec論文 arXiv:2602.10934](https://arxiv.org/abs/2602.10934)。READMEに別repoがあることと、音声符号化のインタフェースが一致することは区別。**実機でMOSS-v1.5＋固定Codecを読み込んだ実験は実施していない**。

## 復元依存の扱い（親の選定容量と追加候補は別）

| 既選定の学習済みモデル | 一次選定ファイル公称容量 | 新しい復元依存と対応策 | 実装/権利の残課題 |
|---|---:|---|---|
| `OpenMOSS-Team/MOSS-TTS-v1.5@cdd3b911b1585e3f2dbc7775ef10f9926f58850a` | **16,995,761,910 B** | デフォルトcodec `OpenMOSS-Team/MOSS-Audio-Tokenizer`。Hugging Face APIの固定版のファイル名・byte・SHA256を[ソース監査](../../catalog/research/2026-11-07-dependency-readiness/audit.json)に記録。v2は別ロール | `AutoProcessor(... trust_remote_code=True)`のコード静的審査。Python/Transformers/CUDA/torch/torchaudio固定とApacheライセンス各ファイルを要確認 |
| `Lightricks/LTX-2.5@49b093a39c19169a8a81721dcc541e07e945232f` | **71,118,789,776 B** | 固定版の蒸留BF16ベース6部品（DiT・Gemma4-12B text encoder・video VAE・audio VAE・duration head・spatial upscaler）は**同一gated配布元に含まれる**。Comfy/Gemma4 E2B prompt enhancerは**任意** | Gated本人許諾、Gemma系特有のTokenizer/codec frontend、`LTX-2`コードcommitとCUDA≥12.7/Python≥3.12。INT8/convrotはPyTorch APIと互換しない |
| `microsoft/VibeVoice-1.5B@c00898d257e6b46004e3e2866a47534085fb685a` | **5,408,337,065 B** | `Qwen/Qwen2.5-1.5B@8faed761d45a263340a0528343f099c05c9a4323`のTokenizer等9ファイル**11,505,079 B**を共有依存として既存v26計上。Qwen本体重みは複製しない | Transformers統合commit実在、Microsoft自身の`VibeVoice-1.5B-HF`公開をまだ確認できない。変換の1,204 tensor一致はコミュニティ提案でありこちらの再現ではない |
| `maya-research/maya2-native@87a83efdd6551e038246b6b37836a6264713eec3` | **5,021,124,225 B** | 既に別repoのKyutai Mimi 384,657,055 BとSpeechBrain ECAPA 89,133,738 Bを研究台帳に固定。対象二repoを本体と別に保全 | 別々のCC BY 4.0 / Apache2.0、codec互換/話者入力を実機再現していない |
| `gradium/phonon-31m-en`/ `gradium/phonon-40m-multilingual` | **103,745,734 B / 122,629,650 B** | 102件の事前潜在話者約26.18MBが共有依存に計上。**音声から新規話者潜在を作るencoderは非公開**で完全任意voice cloningは復元不能 | 多言語40MはGated+CC BY-NC 4.0、既存アクセス権なしにweight取得不可 |

### LTX-2.5の必須と任意の区別

[LTX公式PyTorchセットアップ](https://docs.ltx.io/open-source-model/integration-tools/pytorch-api)の蒸留モデル標準レシピは、選定6ファイル内の依存だけで構成される。別の`Comfy-Org/gemma-4`の`gemma4_e2b_it_bf16.safetensors`は[公式ComfyUI Text-to-Videoガイド](https://docs.ltx.io/open-source-model/usage-guides/text-to-video)にある**任意prompt enhancer**であり、デフォルトのテキスト強化付きComfyワークフローを完全再現したい場合に追加審査する。これを所有するからといってvanilla Gemma4で学習専用Gemma encoderを置き換えてはいけない。なおLTX本体の6つのLFS payload SHAは匿名メタデータでは伏字であり**ローカル照合済みではない**。

### GitHub実装の版固定（コード存在の検証と実行互換は別）

| 本体・互換候補 | GitHub公開commit SHA（存在を確認済） | 留保 |
|---|---|---|
| `OpenMOSS/MOSS-TTS` | `934d6826b084c46a0d033402174d5f8ac4ed2519` | 最新代表版のGit SHA。MOSS固定codecとの環境再現・ABI試験は未実施 |
| `Lightricks/LTX-2` | `4f521619ae0029e8fbb64d555030c2b121a33b4f` | 公式v2.5のソース候補。LTX HF固定weightとの実機一致は未検証 |
| `microsoft/VibeVoice` | `16fb2cb1217c9934a886e1948ffb06120caa2df5` | Microsoftのソース版。実際の取得・音声生成なし |
| `huggingface/transformers` | `640a08a597034221ca1c4fc0c129cf0118179225` | VibeVoice native integration PR #40546のmerge commitは実在。ただし公式Microsoft-HF配布を示すものではない |

## 今回の新Codec容量・証拠と未解決箇所

[研究JSON](../../catalog/research/2026-11-07-dependency-readiness/audit.json)で、MOSS Audio Tokenizer（v1.5必須）とv2（48kHzステレオ別系列）の**別々の固定HF commit、safetensors shard index全数、選定候補ファイル byte、license metadata、SHA識別子**を機械読取可能に記録する。**これらは125モデルの既存一次容量の外**であり、実物を取得したのではない。既知v26の3.403TBに安易に二重加算して「最終容量」と称しない。新Codecにも収録済みのsource token/noticeがあるか照合し、必要ソフトや依存権利・不可逆性の定量化を継続する。

## H/T/D/C/U

- **H:** 元音声をoffline再構成するためにMOSS TTS-v1.5の別Audio Tokenizerの固定原本が必要であり、v2を機械的に代替すると出力仕様が合わない。LTXの選定6部品はベース蒸留生成を開始するために十分だが、独立した再現性と法的許可は未確認。
- **T:** 固定モデルrepo index・実バイト・SHA256識別子と読取専用のprocessor実装を照合。GitHub CIでAPIメタデータを収集してテスト。実際に音声・動画を生成するのは本人が承認しHW/clock/batch/context/backendを固定した後、最低30試行で検証。
- **D:** SOURCE PASS=必須encoder/decoder重みとindexファイル集合が一致。RESTORE PASS=全必要部品と個別ライセンス、対応ABI、ownerディスク実空き、本人権限でoffline出力再現。現在は**RESTORE UNCERTAIN**。
- **C:** ソースがrepo頭で更新されたため個別SHAが互換しない、v2が混入する、source weight mapと数が違う、Gemma4専用エンコーダ欠損、HF -HF名の未公開を誤って採用、推論ライブラリのABI不整合。
- **U:** 配布元メタデータの総バイトは整数で確定できるが、本人の現物SHAとGPU/RAM、OS/runtime/依存Codecの差が支配的。確率分布が得られていないため合成標準不確かさ`u_c`・係数`k`は数値化しない。

**ERROR CHECK:** 本稿は研究・補充候補の調査であって`CURRENT.json`や承認キューの更新ではない。モデル重み・クラウドGPU利用・利用許諾の取得を実行しない。機械学習の非重複性、長期デジタルアーカイブの可逆性、ソフトウェア供給網の固定版、ライセンス/法の四分野を別評価する。
