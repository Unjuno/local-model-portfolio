# R39｜大型モデルをバックエンド別の取得前ファイル構成へ落とし込む（2026-11-08）

**結論**：R38で判明した形式重複について、Mistral Small 4・GPT-OSS 120B・FLUX.2-devの**3つの独立学習済みモデル、7つの異なる実行表現**を、Git/HF固定40桁revision＋重み全シャード＋必要な設定/Tokenizerファイルに分けて登録した。[非実行・未承認R39マニフェスト](../../manifests/drafts/r39-backend-specific-large-sources.candidate.json)。**通常量子化やバックエンド用パッケージを7個の別モデルとして数えない**。一方、特殊な後学習や学習データ段階を消すものでもない。

## 1. 7形式のファイル構成をバイト単位で確定

| 形式・用途 | 重みファイル数 | 設定・許諾・Tokenizer等 | 重みbyte | 設定等byte | 合計byte | 現時点の扱い |
|---|---:|---:|---:|---:|---:|---|
| `mistral4-hf` | 3 | 10 | 120,922,973,936 | 33,571,076 | **120,956,545,012** | FIRST_RUNNABLE_RESEARCH_OPTION |
| `mistral4-native` | 7 | 6 | 120,927,211,096 | 19,928,964 | **120,947,140,060** | ALTERNATE_WITH_ABI_JUSTIFICATION |
| `gptoss120-hf` | 15 | 10 | 65,248,893,184 | 27,964,656 | **65,276,857,840** | FIRST_RUNNABLE_RESEARCH_OPTION |
| `gptoss120-original` | 7 | 8 | 65,248,869,800 | 27,948,874 | **65,276,818,674** | ALTERNATE_WITH_REPRODUCIBILITY_JUSTIFICATION |
| `gptoss120-metal` | 1 | 5 | 65,238,253,568 | 27,891,043 | **65,266,144,611** | HOLD_UNTIL_APPLE_HARDWARE_CONFIRMED |
| `flux2-diffusers` | 18 | 16 | 112,805,617,244 | 17,425,989 | **112,823,043,233** | BLOCKED_ACCESS_NOT_DOWNLOAD_READY |
| `flux2-single-file` | 12 | 9 | 112,805,607,980 | 17,385,234 | **112,822,993,214** | BLOCKED_ACCESS_NOT_DOWNLOAD_READY |

**参考研究構成**：`mistral4-hf`と`gptoss120-hf`を組む場合、今回選択した重み・設定の合計は**186,233,402,852 byte**（約186.23GB）。この数字はダウンロードが許可された容量でも、実行可能な全依存込み容量でも、ユーザーがすでに保存した容量でもない。実機の4TB枠、200GB最低空き、キャッシュ/ステージング/別エンコーダーは別条件。

### 1-A. Mistral Small 4

固定モデルrevisionは[`a11f36bebf709121056b1dbcc943d1c6afbe494d`](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/tree/a11f36bebf709121056b1dbcc943d1c6afbe494d)。HF形式は`model-00001-of-00003.safetensors`など3分割、Nativeは`consolidated-00001-of-00007.safetensors`など7分割。**一つの公開モデルに二つの重みレイアウト**がある。重みの数値がビット単位で一致するかは未検証で、両形式を無条件に捨てたり同時取得したりする理由にはならない。

HF候補では`config.json`/`model.safetensors.index.json`/Tokenizer/Chat Template/Processorを含み、Nativeでは`params.json`/`consolidated.safetensors.index.json`/`tekken.json`等を分けた。**両設定を同じ実行ディレクトリへ混ぜない**：[SGLang PR #21620](https://github.com/sgl-project/sglang/pull/21620)は両形式の識別ミスで起動不能になった症状を2026-03-30に修正した。修正マージcommitは`1d6424d5ad2dd1edb5ce9bb477be81dcf2b06eef`。公開[vLLMレシピ](https://recipes.vllm.ai/mistralai/Mistral-Small-4-119B-2603)は`vllm >= 0.20.0`、`mistral_common >= 1.11.0`を案内するが、これだけでユーザーのドライバ/GPUで動作が保証されない。実際のwheel、CUDA、torch、context（256K設定時KVキャッシュ）とbatchを別に固定する。

### 1-B. GPT-OSS 120B

固定モデルrevisionは[`b5c939de8f754692c1647ca79fbf85e8c1e70f8a`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a)。公式の後学習済みMXFP4モデルで、一般的なQ4量子化コピーを別モデルとして足した例ではない。

- **HFルート15分割**：vLLM/TransformersとHarmony形式を主用途とする。`model.safetensors.index.json`、`config.json`、Tokenizer、Chat Template、LICENSE、USAGE_POLICYを含む。
- **`original/` 7分割**：OpenAI公式Torch/Triton参照実装向けの重み/形式。`original/config.json`、`dtypes.json`、original indexを固定する。HFとは同一訓練状態だが、参照実装で再現できるという理由で別レイアウトに価値が残る。
- **Metal単一ファイル**：Apple Silicon向けにコンパイルされた成果物で、学習データの異なるモデルではない。対象ハードが未確定なので現時点の主保存形式にはしない。

[OpenAIの参照コード](https://github.com/openai/gpt-oss/tree/277020131d524f06bed5f66b694a92ed7f6e5224)を2026-10-29のGitコミットで固定。参照Torch実装は4×H100などの多GPUを要し、最適化したTriton実装は単一80GB GPUでの動作例を示す（**開発元構成例であり、ユーザー実機の測定値ではない**）。Python 3.12/CUDA/torch/Tritonの正確な環境やGPUクロック、バッチはまだ確定していない。

### 1-C. FLUX.2-dev

固定公開revisionは[`26afe3a78bb242c0a8bb181dcc8937bb16e5c66c`](https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/26afe3a78bb242c0a8bb181dcc8937bb16e5c66c)。Diffusers方式はTransformerの7分割とText Encoderの10分割、VAE、各コンポーネントの設定・Tokenization用ファイルを含む。単一ファイル方式も**同じ学習済みTransformerを別レイアウトで利用する候補**だが、数値的完全等価を再計算したわけではない。

**Gated（非商用利用条件）で公開ハッシュがマスクされている。** バイト数の公開表示は固定できるが、実LFS SHAが不明なまま最終取得ロックをかけない。認証済み正規アクセス権、親・依存の利用許諾、[公式コード](https://github.com/black-forest-labs/flux2)、Diffusers/ComfyUIでの動作条件が必要。未認証のミラーを権利回避の代替とはみなさない。

## 2. 保存計画への意味

既存の4TB枠で優先すべきことは、**独立モデルを減らすのでなく、同一モデルをバックエンド用に複数フル取得する状況を避けること**。今回は7形式を相互排他的な候補表として整理した。モデル全体のQ2/Q4を複数持つ例外、実行環境が複数ある場合の併存、研究的なNativeの保存価値は別途実証できれば許容する。反対にQwen3-Coder-Nextの40シャードは一つのモデルの必要部分であるため、勝手にシャード単位で削除してはいけない。

作業を進めた結果、Mistral/GPTは**ファイル全数＋配布元SHAに基づく取得前の比較が可能**になった。ただし全依存・性能・物理空き・現実のABI・ファイル受領後のハッシュ未検証なので**SELECTを変えず、正式取得承認も0**のまま。

## 3. H/T/D/C/U・変数表

| 記号 | 意味（日本語） | SI単位 | 定義・前提・定義域・型 |
|---|---|---|---|
| B_w | 指定形式の全重み容量 | byte | 固定repo revisionでの選択シャードの合計、非負整数スカラー |
| B_s | 同形式の設定/Tokenizer/許諾等のサイズ | byte | 選択したサポートファイルの合計、非負整数スカラー |
| B_p | 指定したファイル集合の容量 | byte | B_w と B_s の合計。ただし外部コード・追加モデルは含まず、非負整数スカラー |
| B_disk | ユーザーの実測利用可能なストレージ | byte | 未測定ならnull、非負整数または欠損 |
| M_peak | 実機での最大推論メモリ | byte | GPU/CPU/OS/KVを含む、未実測ならnull、非負実数または欠損 |
| N_test | 独立した性能比較課題数 | 1 | 最低200件/能力軸を検証設計の暫定値とする正整数スカラー |

**次元チェック**：B_w/B_s/B_p/B_disk/M_peakはbyteなので足し引きの次元は一致する。ただしディスク容量とメモリは別の物理的制約。N_testは無次元で、重み容量の計算には含めない。

**H**：同一学習済みモデルについて、適切な1形式を選択すれば独立した能力を失わず不要な重み重複を削減できる。**T**：固定リビジョンの重量・SHA・support対応を静的に検算。続いて実行権限を得た機器で同じモデルのNative/HF/Metal間のテンソル変換と出力同等性をテストし、GPU型番/clock・driver・backend/ABI・quant zero-point・batch/contextを固定する。**D**：学習済み重み状態と権利・完全環境・性能・安全容量がそろえば取得候補PASS、単なる余分な形式の保存はFAIL、機器/権利/等価性が未確認ならUNCERTAIN。**C**：Native/HFの変換誤差、プロンプト規約・tokenizer不一致、Gatedアクセス権、MetalのSDK依存、巨大KVキャッシュ。**U**：ハッシュの再計算、依存ABI、実機測定がないので合成u_cと包含係数kは未算出。

## 4. ERROR CHECK・他分野への転用・次に考える問い

7候補の重み数はMistral 3/7、GPT 15/7/1、FLUX 18/12。公開元40桁SHAを維持し、Mistral/GPTの公開重みには配布元のSHA256がある。FLUXの重みSHAは非公開のままブロック。既存150資産、Nanbeige SELECT、4TB計画、最低空き200GB、0ダウンロード承認は維持。計算機アーキテクチャ・ML学習状態・ソフトウェア供給網/ABI・長期保存の4分野へ転用。

**〈次に考える問い〉**：10年後の推論エンジンが変化した場合、元のNative重みからHFへ安全に変換可能だと証明できれば、どの実行形式を残すのが最も容量効率がよいか。
