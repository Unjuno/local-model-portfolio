# v6：規制予測を維持した費用対効果・実行可能性監査（2026-11-03）

**履歴資料であり、最終の制約として使わないでください。最新は[150B除外のv8](parameter-cutoff-v8-2026-11-03.md)。** [v7の250B以上ハード除外](parameter-cutoff-v7-2026-11-03.md)により、「パラメータ数のみでは除外しない」というv6時点の提案は撤回されました。実行コスパ評価と大きなMoEの実験情報は参考ですが、現在の取得候補には**総パラメータ150B未満の条件**を先に適用します。

## 結論

- **S1→S2→S3の規制連鎖シナリオは最優先の保存調査順位**として維持する。
- **第2軸として費用対効果を導入**。高精度原本のアーカイブ価値と、現在のGPU/RAM/SSDでの実用性は別の判定。巨大モデルでも公式/実験的offloadの証拠があれば、パラメータ数だけで除外しない。
- **第3軸は合法性・アクセス許諾・ユーザー承認**。どのコスパ評価もこれを超えない。
- 正本：[CURRENT v6](../catalog/CURRENT.json)／[全132件の予測順位とリソース判定](../catalog/effective-portfolio-2026-11-03-v6.json)／[詳細監査データ](../catalog/revisions/v6-2026-11-03.json)。
- **今回のスクリーニングはハードウェア実測でも性能のランキングでもない**。取得前の予算と実装の調査順を決めるための必要条件/候補分類。実行可否は一部の外部主張を除きUNCERTAIN。

## 全132件の上流リポジトリ容量クラス

| 観測された上流リポジトリ総量 | 全件 | 有効選定 | 延期・保留 |
| --- | ---: | ---: | ---: |
| 5GB未満 | 38 | 37 | 1 |
| 5GB以上〜15GB未満 | 18 | 17 | 1 |
| 15GB以上〜50GB未満 | 17 | 15 | 2 |
| 50GB以上 | 31 | 24 | 7 |
| **容量未確定** | **28** | **12** | **16** |
| **合計** | **132** | **105** | **27** |

容量は台帳の`upstream_all_files_bytes_observed`であり、**取得する選択ファイル合計ではない**。複数精度・任意データが混ざる場合があり、同一SHAを持つ依存の重複削減やcache/stagingの追加はまだ未評価。未確定28件を0として容量を合算しない。

## 容量圧迫度が高い9件の選別

有効資産のうち上流リポジトリ総量が**100GB以上**の資産は**9件、計1,559,235,498,752バイト（約1.559TB）**。現行3.288TB暫定容量の約47.4%に相当。2件はデータセットであり推論モデルではない。

| 資産 | 予測段階 | 全repo容量（概算） | 審査する点 |
| --- | --- | ---: | --- |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | S1 | 159.4GB | 原本の保存価値と実行の現実性を別審査 |
| [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | S1 | 177.6GB | 原本の保存価値と実行の現実性を別審査 |
| [Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | S1 | 156.0GB | 原本の保存価値と実行の現実性を別審査 |
| [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | S2 | 217.3GB | 原本の保存価値と実行の現実性を別審査 |
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | S2 | 241.9GB | 原本の保存価値と実行の現実性を別審査 |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | S2 | 195.8GB | 原本の保存価値と実行の現実性を別審査 |
| [EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | S2 | 141.1GB | 原本の保存価値と実行の現実性を別審査 |
| [IFM/SFT-Reasoning](https://huggingface.co/datasets/IFM/SFT-Reasoning) | S2 | 158.6GB | データ、推論VRAMを評価しない |
| [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) | S2 | 111.6GB | データ、推論VRAMを評価しない |

**判断：現時点では9件を一括削除しない。** 代わりに、独立能力、派生/量子化形式の重複、取得するシャード集合、元重みと実用形式の必要性、将来の実行経路、別依存、権利の実態を1件ずつ調査。容量の効率が悪い場合にだけ延期を検討し、予測リスクに沿った原本保存の意義が高ければ「保管専用」でも候補を維持する。

## Qwen3-Coder-Next：8GB GPU報告の評価

[Qwen公式モデルカード](https://huggingface.co/Qwen/Qwen3-Coder-Next)では総約80B、活性約3BのMoE。**活性3Bは計算上のトークン当たりのパラメータ数で、全てのexpert重みが3Bに減るわけではない。**

[第三者開発者のPR #562](https://github.com/QwenLM/Qwen3-Coder/pull/562)と[実装](https://github.com/nalexand/Qwen3-Coder-OPTIMIZED)には以下の**未検証の動作報告**がある。

- GPU：ノートPC RTX 3070 Ti、VRAM 8GB；ホストRAM 32GB。Python 3.12、`transformers==5.1.0`を書き換える独自コード。GPU/CPUクロック、batch、context長は不明。
- 重み：元の[Qwen3-Coder-Next-FP8](https://huggingface.co/Qwen/Qwen3-Coder-Next-FP8)を使用。重み一式が約80GBで、8GB VRAMへ全量保持はできず、**SSDからのexpertの遅延読込＋GPU/pinned RAMキャッシュ**で稼働。
- 測定例：207 tokens / 114.78s = 約**1.80 token/s**。別の短い対話等では約0.65〜1.80 token/s。これは**発表者の単独実験**であり、標準設定のGPU完全常駐推論の速度ではない。PRは未マージであり、変更したTransformersファイルの安全性や再現性を保証しない。
- 現行台帳の`Qwen/Qwen3-Coder-Next`（約159.376GB上流repo）と実験で使用した約80GBの**FP8派生チェックポイントは別配布物**。本体を8GBのモデルとして数えず、FP8も自動選定や取得対象に格上げしない。
- **選定判断：S1の重要な原本として維持、実用8GB経路は調査対象**。GPU RAM/SSD/CPUの帯域、OS、KV、タスク品質が確定するまでは「8GBで実用」と称しない。

### 理論的な最低重み容量と次元検査

**理想化した均一量子化**を仮定した概算に限り、下限目安を式で示す。

\[
 B_{\rm ideal}=N_{\rm total}\times\frac{q}{8}
\]

| 記号 | 意味 | SI単位 | 定義 | 定義域・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| \(B_{\rm ideal}\) | 理論重み容量 | バイト（B） | 全重みの理想量子化容量 | 非負。ヘッダ/スケール/非量子化領域除外 | スカラー |
| \(N_{\rm total}\) | 総パラメータ数 | 1（無次元、個数） | 保存する全パラメータ個数 | 非負整数。活性パラメータで代替不可 | スカラー |
| \(q\) | 1重み当たりビット数 | bit/parameter | 量子化ビット幅 | 例：3または4。全重みに同一精度の仮定 | スカラー |
| \(8\) | 1バイト当たりビット数 | bit/B | 固定換算値 | 正確に8 | スカラー定数 |

**例**：総80Bパラメータの4bit理想値は約40×10⁹ B、3bitは約30×10⁹ B。実重みは量子化スケール、混合精度、Embedding、メタデータ、KV cache、ランタイムが追加される。したがって8GBのGPUだけで常駐できることは示さない。

**次元検査**：`parameter × (bit/parameter) ÷ (bit/byte) = byte` で整合。性能指標であるtoken/sとは物理的に別の尺度。

## 小容量で異なる能力を保管する候補

（**サイズと固有の機能のみを確認**。8GB GPUでの実行成功や相対性能優位は未検証。）

| モデル | 段階 | 上流総量 | 保存価値 |
| --- | --- | ---: | --- |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | S1 | 159.376GB | 大型・独自エージェント後学習は保存価値が高い。8GB VRAM動作はSSDからexpertを動的読込する実験であり、FP8重み自体が8GBに収まるわけではない。 |
| [Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | S1 | 2.498GB | 小容量で音声合成・声質制御という異なる能力を持ち、音声合成技術の保全効率を比較可能。 |
| [speridlabs/idol](https://huggingface.co/speridlabs/idol) | S2 | 3.128GB | 約3.13GBの主リポジトリだが外部のGated DINOv3/FLUX.2 VAEが別途必要。モデル単独容量で評価しない。 |
| [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | S2 | 0.915GB | 約0.915GBでVLA基礎を保存。動作には画像入力や依存ライブラリ・ロボット環境が必要。 |
| [autogluon/chronos-2](https://huggingface.co/autogluon/chronos-2) | S3 | 0.478GB | 約0.478GBの時系列予測という独立機能。汎用LLMではない。 |
| [Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | S3 | 1.207GB | 約1.207GBの検索用埋め込み原本。生成LLMと違う役割。 |
| [Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | S3 | 1.207GB | 約1.207GBで検索結果の再順位付けを保全。埋め込み器とは別用途。 |
| [lightonai/LightOnOCR-3-0.8B](https://huggingface.co/lightonai/LightOnOCR-3-0.8B) | S3 | 1.738GB | 約1.738GBで文書OCRの異なる能力。4B版を再検証まで延期する判断は妥当。 |
| [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | S3 | 1.622GB | 約1.622GBでASRの比較原本。音声モデルの性能・速度比較に必要。 |
| [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | S3 | 1.770GB | 約1.770GBで小型推論・実装検証。保存順位はS3だがダウンローダーの安全試験には適する。 |

## 二系統の運用

**A. 予防的保存（archive lane）**：S1予測順位を守り、独自重み・再学習できない専門モデル・原本・依存の保全を目指す。8GB GPUで高速に動かないことは、単独では破棄の理由にしない。HDDは長期保管先。

**B. 日常利用（runtime lane）**：現実のGPU/ホストRAM/SSD容量に合わせ、実証された量子化版・オフロード・CPU推論経路を採用する。対象のGPUに全重みが載らない場合、**一時的な作業コピーをSSD/NVMeへ配置し、HDDをトークンごとにrandom readすることを常用しない**。実行コードは事前監査し、モデル取得の操作ではimport/インストール/実行をしない。

**モードは固定しない**：大きなMoEはSSD streamingで理論的に動作する場合があり、8GB GPUだけを理由に除外しない。ただし0.6〜1.8 token/s程度では対話のUXが厳しい場合があり、速度と精度を用途別に測る。小さなモデルでもAudio Codec/Encoderが必要なら実効占有は増える。

## 実際に必要な追加測定と停止条件

**H**：同一目的の異なる候補について、権利・配布源・能力が確認され、かつ指定機器での実測により一部の小容量モデルが実用条件を満たす。8GBで大型モデルが動いても性能価値を保証しない。

**T**：所有PCのOS/CPU/GPU・VRAM・RAM・SSDを記録してから、同じ量子化・バックエンド・context（まず4096と8192 tokens）・batch=1で各LLMにつき30件以上の同一入力を試す。出力速度、初トークン遅延、成功率、ピークVRAM/RAM、SSD I/O、温度、消費電力、課題成功率を記録。音声はCER/WER/RTF、画像/3Dは独立指標を別設計。ソフト依存のABI、量子化zero-point、KV精度も記録。すべて事前許諾と別実行承認の後。

**D**：実験的な対話LLMについては、例として生成速度の中央値5 token/s以上を**暫定実用の閾値候補**とする（固定基準ではない）。単に生成できたが遅い場合は`RUNS_SLOW`、OOM/失敗は`FAIL_FOR_TEST_CONFIGURATION`、実機・再現試験の欠落は`UNCERTAIN`と記録。保存価値は性能判定と独立。ユーザー実機に関する現在の全判定はUNCERTAIN。

**C**：重量級でもより強いNVMe/キャッシュ/量子化で実用化する、または小さいモデルが特定タスクで大型を上回る可能性。定性的な小容量優位を性能優位とは誤認しない。

**U**：最大の誤差源はベンチマーク環境、モデル版・混合精度、GPU/SSD・CPU帯域、KV長、初回ウォームアップ、データセット、分布差。現時点では評価データと実機情報が不足し、合成標準不確かさ`u_c`を定量算出できない。95%信頼区間等は測定後に評価する。

## 資産全体での優先順位のまとめ

1. **規制予測のS1/S2/S3を維持**し、現在の公開状況・ライセンスの再審査を進める。
2. 同じ波の中で、重み原本の希少性・用途の独立性、増分容量、実用経路の有無を比較する。
3. **大型9件に予算の約47%が集中**していることを個別に再評価する。選択ファイルの正確な容量が確定するまで、この比率は参考値。
4. 28件の上流容量未知（有効12件）を優先的に固定する。未知を0としない。
5. リスクの高いS1の重みも契約や権利を満たさなければ取得しない。モデル本体のダウンロード、推論、音声/動画生成、コード実行の承認は未付与。
