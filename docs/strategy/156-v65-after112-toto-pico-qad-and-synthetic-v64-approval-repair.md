# R156 / v65 — 112取得後の真正差分小型モデル保存とv64無断承認器の修正（2026-11-22）

## 1. 目的と最終判定

**現行正本はv65 240登録／192有効（SELECT56・CONDITIONAL136）で据置**。旧14配布元中13件（140,553,833,221 byte）は取得台帳112件に、repo ID・immutable revision・ファイル数・総byteが全て一致する。よって**この13配布元を再度取得しない**。Ripple-65BはP3 HOLD。v65は既取得のTimestral5M、WeMM-Video-2Bを正本へbackfillし、後続R154で小型Heretic LoRAをCONDITIONAL、Cartwheelの制御学習成果をHOLDとして登録している。SmaugはR153研究系列の別候補として扱い、現行採否との混同を避ける。いずれも今回再ダウンロードしていない。

[R153別調査](../strategy/153-v64-post112-next-small-rare-originals-and-no-repeat.md)はnchapman小型Heretic-LoRA、LingSante 16.7M生理信号エンコーダ、Cartwheel 3学習済み制御、Primal VAEのPublisherソースを固定済み。**同じモデルの調査登録を重複しない**。Pico8 SHAは既存のR154監査にも記録されているため、今回の監査は固定ソースと実行器のSTOPゲートを補強する目的である。

**今回追加して固定した差分研究sourceは2スコープだけ**：

| 原本 | Publisher immutable revision | 正確な参照ファイル数／byte | 研究判定 |
|---|---|---:|---|
| [Datadog/Toto-2.0-4m](https://huggingface.co/Datadog/Toto-2.0-4m/tree/8306a9801cf98c0f5ffe4b2dcc8f496e616d84d9) | `8306a9801cf98c0f5ffe4b2dcc8f496e616d84d9` | 7 files / **17,727,464 B** | **CONDITIONAL研究候補、取得未承認**。4,144,448 F32 elements、Publisher Apache-2.0。既取得Timestral5Mとは別学習・別時系列アーキテクチャ。作者GIFT-Eval MASE 0.757は作者発表・独立評価なしで、Timestral5Mの0.705より数値が大きいが、同条件の直接比較結果ではない。外部 `toto-models` Pythonソース、Torch runtime ABI、予測horizon等未凍結 |
| [Kitten Pico INT8 QAD 8言語](https://huggingface.co/KittenML/kitten-tts-2-pico/tree/a5632deac7d92f6178db814d933eba746a97f2dc) | `a5632deac7d92f6178db814d933eba746a97f2dc` | **追加8 files / 63,628,208 B** | **同一repoの追加差分で別カタログモデルIDにはしない**。以前の33files/285,879,877byteは112件取得台帳で報告済み。出版社のINT8 ONNX8ファイルのLFS SHA256とGit OIDを凍結。作者はQADの別学習と説明するが、モデル実体の量子化前後比較・音質同条件実測未実施 |

[Publisher原本ファイルと不変SHA](../../manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json)、[新規研究未承認キュー](../../queues/proposed-v65-r156-toto4m-pico8-UNAPPROVED.json)、[機械可読採否](../../catalog/decisions/2026-11-22-r156-v65-toto4m-pico8-no-repeat.json)。

**保存ファイルのPublisher参照量**：

\[
B_{\mathrm{scope}} = B_{\mathrm{Toto}} + B_{\mathrm{QAD}}
= 17{,}727{,}464\ \mathrm{B}+63{,}628{,}208\ \mathrm{B}
=81{,}355{,}672\ \mathrm{B}.
\]

| 変数 | 意味（日本語） | 単位（SI表記） | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| \(B_{\mathrm{scope}}\) | 2研究scopeの参照ファイルの合計 | byte (B) | 2項の加算 | 非負整数、owner HDD増分ではない | スカラー・整数 |
| \(B_{\mathrm{Toto}}\) | Toto全ファイル | byte (B) | 17,727,464 | immutable commitの7ファイル全体 | スカラー・整数 |
| \(B_{\mathrm{QAD}}\) | Pico INT8追加対象8ファイル | byte (B) | 63,628,208 | 旧33ファイルの再取得を含めない | スカラー・整数 |

次元検査：両辺すべてbyteで一致。**この参照量はキャッシュ・親・実ディスク空き・完全オフライン復元必要量ではない**。所有者Dの実物SHA／実空き残床200GB、本人の行為別使用権は独立ゲート。

## 2. 重大なセキュリティ回帰の修正

旧 `scripts/build_v64_plan.py` は研究sourceから `D:/AI_VAULT/state/approved-v64.json` を自動作成し、`approved:true`、`approved_by_user:true`、`license_text_reviewed:true` を事実なく書き込んでいた。実行器は「user directive 2026-11-19」を一部拒否していたが、生成器の設計自体が危険であり、また取得済み13配布元を再度転送候補にしていた。

**修正後**：v64 filenameの下位互換を保持しつつ、`scripts/build_v64_plan.py` は現在v65 R156の2scopeだけを読み、最新112 ledgerに対して旧14source中13件の正確なrepo/revision/files/bytes一致を再確認。Picoの8ファイル以外の旧33を混入させない。作成できるものは `plan-v65-r156-RESEARCH-ONLY.json` と `review-v65-r156-UNAPPROVED.json` のみ。6つの承認・権利フラグはすべてfalseで `approval_ref:null`。所有者が明示承認した実ファイルは上書きしない。 `scripts/preserve_execute.py` も過去の既知の `v64 R152 canonical post99 source queue` synthetic refを拒否する。

これは**GitHubソースの修正であって、所有者Windows Dドライブの旧approved-v64.jsonを遠隔変更・削除したことではない**。更新された実行器を使う前に、旧生成器で作られたファイルを信用しないこと。

## 3. 選定の反証可能性

**H**：Toto4mの独立trained stateと、単なるpost-training quantizationではない可能性があるPico INT8 QADを小容量で保存する価値がある。

**T**：Publisher immutableコミットに固定したToto7file＋Pico8file、全15 path/bytes/Git OID/LFS SHAを静的照合。112取得台帳と13旧sourceを照合し、old synthetic approvalを実行器が拒否することを無通信テスト。用途別性能の実測では、最低100の独立シーケンス/音声入力を使い、CPU/GPU型・クロック・RAM/VRAM・Torch/ONNX Runtimeとzero-point/量子化形式・バッチ1と予測ホライズン・音声指標を固定する。

**D**：発行元のファイル同一性と承認ゼロはSTATIC PASS。権利・ライブ媒体SHA・実容量・外部依存ABI・完全オフライン復元はUNCERTAIN/STOP。重みSHA不一致や本人許諾未成立はFAIL。

**C**：Totoが既取得Timestralに対して独自価値を示さない、INT8が後変換のみで新たな重み表現を保存していない、外部実装やcodecで復元不可能。

**U**：作者カードのベンチ条件差、未評価の音質/性能、ユーザーGPU/CPU・driver/OS・runtime ABI・現物HDD・権利の不確かさ。繰返しの測定分散がないため、合成\(u_c\)と包含係数\(k\)を数値化しない。

学際性は **モデル供給網と暗号学的hash**、**時系列統計と確率予測**、**音声処理と量子化認識蒸留**、**知財／AI安全保障規制**の4領域。2026-11-19の[米BIS規則](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧ECCN 4E091を撤廃。公開重みが近い将来一律禁止されるとの確証はなく、Gated・第三者LICENSE・輸出用途の法的評価を個別に行う。

## ERROR CHECK

新規7件の追加停止テストと、旧版を含むPython unittestの全件を実行してからcommit。自己テストのPASSと利用者の権利、原本保有事実、オフライン推論の稼働は異なる証拠水準として明記。**今回：重量転送0、承認0、第三者モデルコード実行0、ユーザー媒体改変0、旧モデル削除0。**
