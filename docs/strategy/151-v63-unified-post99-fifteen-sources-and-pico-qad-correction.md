# R151／v63 — 99件取得報告の後に残す学習済み原本の統合判定（2026-11-22）

## 1. 今回の結論

`Unjuno/local-model-portfolio` の現行 `main` 正本は **v63（235登録／188有効・SELECT55／CONDITIONAL133）**。所有者側の前回取得台帳は **99モデル／1,478ファイル／1,879,994,309,866byteのVERIFIED報告**であり、本調査でWindows Dドライブを再ハッシュした値ではない。

R149以前の11原本に、その後に並行して保存されたR150各監査を集約すると、**15配布元の固定ソース研究候補**（v63の既登録11、新規研究4）となる。二重カウントした「WeMM-Video-2B」を統合し、`mistralai/Timestral-5M`、`tencent/WeMM-Video-2B`、`GetCartwheelInc/cartwheel-control`、`baselabs/groundhog-1`の独立原本4件を既存候補と区別する。

- [統合15件・先頭6件の非実行審査キュー](../../queues/proposed-v63-r151-unified-15-research-scopes-UNAPPROVED.json)
- [R151機械可読の追加・保留・重複除外判断](../../catalog/decisions/2026-11-22-r151-v63-unified-source-and-license-adjudication.json)
- 元情報：[`r149` 11候補](../../queues/proposed-v63-r149-after99-11-research-only.json)、[`r150` 13候補](../../queues/proposed-v63-r150-after99-13-research-only.json)、[R150の6専門原本](../../manifests/drafts/r150-2026-11-22-six-specialists-source-freeze.candidate.json)、[WeMM＋Timestral 5M](../../manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json)

**R151では既存235レコードと`queues/approved.json`を変更しない。取得できる権利・実媒体の空き・hash・オフライン復元・ユーザーの個別ファイル承認がないため、全部未承認である。**

## 2. 原本保存の優先順位

| 保存・審査レーン | 例 | 処置 |
|---|---|---|
| A：小型で学習成果が固有 | [Timestral-5M](https://huggingface.co/mistralai/Timestral-5M)、既存Pico／Mirage／Timestral-28M／Aurora2、[Cartwheel Control](https://huggingface.co/GetCartwheelInc/cartwheel-control) | **6配布元を最初のファイル単位の所有者審査候補**。新規のTimestral5MとCartwheelは正式v63未登録。Cartwheelには異なるロボットの制御ポリシー3件と複雑なメッシュ／NOTICEがある。移動させるべき実機ロボットへの未検証適用は禁止 |
| A＋：小型無検閲の独立編集 | [Qwen3.5-0.8B-Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA) | **次のSHA凍結対象**。作者の独立2種類のLoRA重み計2,006,488byteと、重複GGUF形式を区別。全レポファイルOID、親Qwenの所有者SHA、権利・実行再現が未閉包なので本体取得は保留 |
| B：無検閲編集を親と共に保全 | [LiquidAI/LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B) ＋ [heretic](https://huggingface.co/saidutta69/LFM3-VL-2B-heretic) | **重みSHAが異なる二つの学習状態**。両者の固定source参照計9,188,749,234byte。親を編集版で置換しない。編集の拒否率は作者プロトコルのみ、一般能力向上と見なさない |
| C：新規の音声付き映像理解 | [Tencent WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B) | **研究上の新規CONDITIONAL候補**。27全ファイル6,590,699,556byte、Publisher宣言SHA25件。2Bはモデル名で、3.28B相当の総学習要素はマルチモーダル部を含む。CUDA 12.9／PyTorch／独自processingとパッチ版vLLM 0.18/0.31・SGLang 0.5.16/0.5.19等の再現条件を別審査 |
| D：大型の特殊意思決定 | [baselabs/groundhog-1](https://huggingface.co/baselabs/groundhog-1) | 26B級MoEの校正・構造化判断原本。16ファイル53,120,939,617byteを固定。既存Intern-Decision 0.8Bと機能重複はあるが重みは別成果。大型なので実測価値とライセンス確認までHOLD寄り |
| E：大型動画・ワールドモデル | MOSS-VL-Realtime／Cosmos3-Nano-Sim-Transfer | 独立重みとして保持するが合計54,438,018,606byteのPublisher sourceと独自GPU／ABI確認が必要。Cosmos VAEは既選定とPublisher SHAが一致するだけで現物共有未検証 |
| F：高機会費用 | Ripple-65B-Preview | BF16原本129,572,889,973byte、P3研究HOLD継続。実験的NVFP4をBF16正本とみなさない |

CartwheelのPublisher別ソースは**154ファイル／304,057,444byte、LFS SHA130件**。先頭6モデル分の固定Publisher選択ソースは**214ファイル／2,559,656,195byte／LFS SHA参照160件**。これは研究上の完全に指定された**取得前審査ファイル集合**であり、実媒体に送る承認済みキューではない。

15研究ソースのうち大型Rippleを除く14配布元の選択ファイル参照は**128,580,722,021byte**。この値にはFastFramesの**別途17,567,235,949byte**の復元依存やCactus実行ファイル、owner媒体の差分・作業領域は加算されていない。空き容量が十分とは判定しない。

## 3. 修正：Kitten Pico INT8のQAD学習を見落とした旧解釈

旧R143には「INT8はINT4の単なる量子化フォーマット重複」として8ファイルを除外した判断があった。しかし[原作者の固定実装ドキュメント](https://github.com/KittenML/KittenTTS/blob/5802f6b956844919ecf210f4e55f4750a6ad7c6f/docs/kitten-tts-2-tiny.md)は、**INT8とINT4をquantization-aware distillationで学習した**と説明する。モデルフォーマットの変換だけという前提は根拠不足である。

従って次を分離する。

1. **既存でソース固定済み**：33ファイル／285,879,877byteのPico source（INT4・FP原本・音声・G2P）。最初の4件54ファイルの静的整合は今もPASS。
2. **追加の独立学習成果の可能性**：INT8 8言語分、**63,628,208byte**。原作者QAD説明は重みの違いの研究根拠だが、8件の出版社側LFS SHA256とGit OIDは未固定。これを現在の取得許可範囲へ混ぜない。
3. **将来の修正候補**：40hex固定rev `a5632deac7d92f6178db814d933eba746a97f2dc` から8件のOID/SHAを取得・突合し、Pico全41ファイル／349,508,085byteの研究原本範囲へ拡張するか判断。デフォルトINT8のONNX Runtime 1.20+、G2Pや声素材も閉包確認する。

[不足している8件の原本資料](../../manifests/drafts/r150-2026-11-22-kitten-pico-int8-qad-source-delta.candidate.json)。差分が残る段階では「Picoは完全保存確定」と称さない。

## 4. 追加するもの・見送るものの判断

**正式v64へのCONDITIONAL追加を審査する4件（まだ未登録）**：Timestral 5M（20.85MB）、Cartwheel（304MB）、WeMM-Video-2B（6.59GB）、Groundhog-1（53.12GB）。保存価値は、既存モデルとの学習済み重みの独立性と、時系列・ロボット制御・音声付き映像・構造化判断という機能分散による。現段階で取得承認にしてはいけない。

**優先研究だが重量取得は保留**：Qwen0.8B Heretic-LoRAの全ファイルソース凍結、Pico QAD INT8 8件の重量SHA、[Kitten TTS 2 1.7B](https://huggingface.co/KittenML/kitten-tts-2)の全依存と利用許諾。Kitten 1.7BのPublisherコンパクト実行体約492MBに対しHub全レポ表示約8.24GBで、コンパクト実行体を完全アーカイブと誤認しない。[Stellon Labs Community License本文](https://huggingface.co/KittenML/kitten-tts-2/blob/main/LICENSE.md)は研究・非商用利用でも撤回可能な利用許諾で、商用は登録が必要。年間売上または累計資金100万米ドル超の条件、帰属・用途制限・音声本人の同意などの確認を要する。GitHub実装Apache2を重みに転用しない。

**今は追加しない**：[OpenUncensored/Inkling-2-Mini-Uncensored](https://huggingface.co/OpenUncensored/Inkling-2-Mini-Uncensored)のフルマージ重み（既選定親＋LoRAを超える固有性未確認）、baselabs/bison-1（Groundhog系兄弟と追加精度未実証）、169Pi/Alpie_seed（9B全結合差分の未検証）、Metric-AI/Ayb（Gated・非商用条件）、abacusai/Smaug-Uncensored（重複削減可能性・追加学習重み差分未検証）。

**規制の事実**：米BISの2026-11-19施行[91 FR 74970、IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion RuleのモデルウェイトECCN 4E091規制を撤廃。モデルの全面所持禁止が決まったという根拠ではなく、個別のLICENSEや残る輸出・最終用途条件は維持。将来の公開停止を定量確率で主張しない。

## 5. H／T／D／C／U・ERROR CHECK

- **H**：同じ重みの量子化派生を集めるより、独立した学習成果と復元依存の原本をそろえるほうが将来の研究再現性を維持する。QAD INT8や別LoRAの「追加学習」をフォーマット変換と取り違えない。
- **T**：既取得99報告のrepo/revisionを除外後、15ソースの一意性を比較し、初回6件214ファイル・160Publisher LFS SHA参照、固定revision、用途別ライセンス、共有親、必要実行ABIを照合する。所有者PCでは別途、既存実ファイルSHA-256・D容量・stage/cache・200GB安全余白を読取専用で検証する。実モデルの性能試験は同一HW/クロック/driver/backend/量子化/コンテキスト/バッチ条件で、最低30反復・独立試験集合を用意する。
- **D**：15配布元の重複無し、6件のファイル数214・容量2,559,656,195byte・LFS160、既存v63とapproved0が一致すれば**メタデータPASS**。INT8 QADを無根拠に形式重複と扱う、重み原本SHAをGit blob SHA1で代用する、LICENSE未承認でDL可とする場合は**FAIL**。実機の保存容量・利用権・オフライン動作は**UNCERTAIN**のため追加取得を停止。
- **C**：メーカー主張したQADや無検閲化が反復評価で有効でない／新モデルの利用条件が所有者の行為に適用されない／オフライン復元が失敗する。その場合は該当項目のみ保留し、既取得ファイルを消さない。
- **U**：Owner媒体・GPU/CPU・コードABI、許諾の個別適用、モデル間性能差の未計測が主要な不確かさ。測定分散が無いので合成標準不確かさ `u_c` および包含係数 `k` の数値を捏造しない。
- **ERROR CHECK**：固定ソース内のrevision形式・LFS SHA形式・ファイル数・Publisherバイト合計・15ID一意性は静的検査、承認・重量転送・現物削除は0。性能ベンチと実HDD SHAは未実施でPASSと呼ばない。

連携分野：①オープンウェイト監査・モデル編集、②モバイル音声/時系列推論、③音声動画認識・ロボット制御、④ソフトウェアサプライチェーン／ライセンス・プライバシー。

**運用**：`main`一本。提出したソース審査だけで`queues/approved.json`を生成・更新しない。モデルの重みや実行ファイルは未審査の状態で読み込まない。
