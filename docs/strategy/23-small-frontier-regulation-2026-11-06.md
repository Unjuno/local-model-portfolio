# R26 — 2026年新世代の異常に高性能な小型モデルと中国の公開制限リスク（2026-11-06）

## 判断
対象は **小型推論・エージェント** と **効率的マルチモーダル推論**。従来v18の144資産と重複チェックし、**6件（4つの保存可能な技術機序、うち依存が2組）をCONDITIONAL**としてv19に追加。入手後のテストなしにSELECT・download-readyへ上げない。R26調査のみの比較対照はSpark-X2.6、JOSIE-2、Orchard-GUI未公開weightとOrchard dataset。Nanbeige4.3-33Bと6件の既存除外は維持。

## 注目成果と明確な弱点

| 作者・原本 | 配布モデル／真正の学習済み規模 | 本体重みbyte | 作者または外部の比較（個別タスク） | 不採用側の証拠・当面の検証 |
|---|---:|---:|---|---|
| [Liquid AI LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) | tri-hybrid 1,728.8M、Baseは既存選定 | 3,457,635,448 | 2026-10-27公表、メーカーvLLM BF16 WebArena-Verified38.42% vs Qwen3.5-9B28.94%（最大40 steps） | 著者評価。GPQAは63.37 vs 同9B80.40%、128K RULERも劣る。日本語・実機未測定 |
| [IFM K2-Horizon-0.9B](https://huggingface.co/IFM/K2-Horizon-0.9B) | **1,078,285,824（名前0.9Bと違う）** | 2,156,600,968 | 2026-09発表。作者AIME2026 48.5% vs Qwen3.5-2B38.8%、HumanEval+79.9 vs75.6 | 作者評価、ハード/思考予算一致不明。GPQA27.3 vs54.9、BFCL28.0 vs43.6。カスタムコード監査必須 |
| [LiquidAI/LFM2.5-VL-3B](https://huggingface.co/LiquidAI/LFM2.5-VL-3B) | 3,123.5M target | 6,247,065,472 | DSparkを動かすための同一アーキテクチャVLM基盤。既存LFM3-Omniとは非互換 | 単独で3x高速化したわけではない。完全な設定/tokenizer固定前 |
| [LiquidAI/LFM2.5-VL-3B-DSpark](https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark) | 単独279.5M、**target込み3,403M** | 558,942,914 | 2026-09-24、作者H100 80GB SGLang BF16 batch1 decode **2.04–2.66x**、end-to-end **1.64–2.27x**；M5 Max FP16 batch1 decode **2.30–3.13x**、E2E **1.56–2.62x** | 品質を増やすモデルではなく厳密検証付き投機復号。量子化Q4の高速化、実機互換未測定。同じtargetが必須 |
| [udgamlabs/Lilavati](https://huggingface.co/udgamlabs/Lilavati) | 94.7M、プログラム生成器 | 189,484,448 | 2026-10-16、作者GSM8K n=1319、単発greedyで54.7% | 一般会話ができず、無解問題・単位変換に弱い。生成Pythonは承認済みsandbox以外で実行禁止 |
| [udgamlabs/Lilavati-Checker](https://huggingface.co/udgamlabs/Lilavati-Checker) | 自身94.7M、**generator込み189.4M** | 189,484,448 | 48候補を生成・sandboxで実行しchecker加重投票、作者GSM8K 72.3% | 48試行と検証コードが必要で、上記単発との同費用比較ではない。独立再現なし |

6つの主重みLFSポインターにはそれぞれSHA256・byteがある。**重みのみ合計12,799,213,698byte（十進約12.799GB）**。これはtokenizer、config、LICENSE、custom Python、runtime、追加依存、temp、既存ディスク重複の実査ではない。元モデルのリポジトリのimmutabile commitをこのラウンドでは確定できていないので**全資産の`fully_pinned_revision_sha=null`**、final lock/取得は不可。

## 競合候補を増やさない理由

- [XHToken/Spark-X2.6-1.7B](https://huggingface.co/XHToken/Spark-X2.6-1.7B)：HF約1,707.7M、BF16シャード計3,415,340,496byte。第三者CamThinkの二言語69課題×2評価でthink-on厳密成功率63.8%、think-off43.5%。LFM3との同条件think-on比較不足、小標本・別harnessがあるため**HOLD研究のみ**。作者独自技術の価値は否定しない。
- [JOSIE-2-4B-OSS](https://huggingface.co/Goekdeniz-Guelmez/JOSIE-2-4B-OSS)：HF数4,659.9M。作者ARC-C95.5% vs base83.4、TruthfulQA69.2 vs48.9の強い主張だが、汚染排除・同条件の独立再現不足で**HOLD**。
- [Microsoft Orchard-GUI 4B](https://www.microsoft.com/en-us/research/blog/orchard-an-open-framework-for-scalable-agentic-ai/)：作者は4Bでブラウザ3評価平均68.4%、235B教師超えの一部タスクを報告。ただし**同一性能の公開モデルcheckpoint IDを確認できない**。API結果だけを「重み保存済み」と見なさない。[Orchardデータセット](https://huggingface.co/datasets/microsoft/Orchard)はSWE107,185軌跡約9.72GB・GUI3,070件約1.25GBで別研究候補。元スクリーンショットやコードの個別権利・完全manifest未確認。
- [microsoft/Fara1.5-4B](https://huggingface.co/microsoft/Fara1.5-4B)：実在する約4.539Bの小型GUI重みだが、すでに27B Faraを選定している。小型実用レーンとしては別途比較するが、今回の異機序選定では追加せず**HOLD研究**。

## 10月16日：AI技術輸出管理改訂案の正確な範囲

[商務部・科技部2026年第48号公告](https://www.mofcom.gov.cn/zwgk/zcfb/art/2026/art_0a31a3c9ac404f7a9b0e917ce3412997.html)は、AI関連23技術を含む技術輸出管理目録**改訂案の意見募集**と、指定された技術輸出取引の**暫定事前登録**を発表。公告は、**すでにオープンソース公開・論文公開等で公知となった技術を管理範囲から除外**する方針も示す。[公式解説](https://www.mofcom.gov.cn/xwfb/xwfyrth/art/2026/art_d7661dbf62794345a221404f82a25959.html)は、禁止候補にAI駆動の悪意あるコード生成・変異技術、制限候補にAI補助脆弱性発見などを含み、国外現地配備の技術移転とAPI/SaaS/軽量端末サービスを区別する。

**区分を厳守**：改訂案の列挙=最終禁止の確定ではない。暫定事前登録があること=人間を超えるモデルすべてが無許可で取得禁止ではない。中国境内から国外へ移す技術と、公開済みのHFモデルを日本で個人研究する行為は同一視できない。今回追加する小型モデルが規制対象になった事実、将来削除される日付や確率は見つかっていない。オープンソース公開済み技術の除外方針があっても、別の権利・公開元のルール・Gated手続は残る。

## 規制の事実・仮説の区別

**公式発表の現在の事実**：[CAC 2026-04-30「清朗」AI應用乱象](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm)は、オープンソースコミュニティにおける危険なモデル/データセットの審査・削除不備を規制対象として明示。モデル届出、生成物表示、無許可な顔/声使用、違法な自動化などアプリ運用面も対象。[CAC 2026-09-14の安全治理框架3.0](https://www.cac.gov.cn/2026-09/14/c_1791137092283345.htm)はリスク分類と技術対応を掲げる政策的枠組み。[2026-05-08 agent政策意見](https://www.cac.gov.cn/2026-05/08/c_1779979789472520.htm)は安全なagent普及の政策。
**未確認の主張**：「人間の能力を超えたすべてのopen-weightモデルが即一律禁止・回収される」という公式法令・閾値は確認できない。研究能力のベンチ超えは、法令上の禁止トリガーではない。**将来のモデル別削除日や確率は予測できない**。ただし個別モデル/データが公開停止され得る制度運用のリスクを保存戦略へ反映する。

## 保存戦略・数学・比較方法

- **H**：小型モデルが既存のより大型モデルを専門課題では上回る（反証可能、作者のみはUNCERTAIN）。
- **T**：現行モデル・旧モデルと同一データ/ハーネス/思考・量子化・ハードで対比較。前登録したタスク：数学30問×複数seedだけで十分とは言えず、AIME/GSM8Kなどの公式分割と再現可能スクリプト、GUIは少なくとも100新課題、メモリ/速度30試行。
- **D**：対象分野の再現可能な品質改善と一定の一般能力維持ならSELECT再審査。作者測定のみ⇒CONDITIONAL、真正な重み・権利・RAM・保存先が未検証ならdownloadはBLOCK。
- **C**：汚染、プロンプト/思考モード差、作者評価judgeバイアス、専用のtool executionに依存、4bitで性能低下、異なるrepository commit。
- **U**：誤差はsampling、判定モデル、バッチ・クロック、training overlap、UI環境変化、量子化。定量的ユーザー実機u_cや拡張係数kは未測定で未定義。

**変数表**（数字は主重みと補助ファイル全体を区別）：

| 記号 | 意味 | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `W` | 元配布者の主重み合計 | byte | 六つのLFS主重みbyteの合計 | 0以上、主重みのみ | 整数スカラー |
| `P` | 全学習済み部品の合計パラメータ数 | 1（個数） | target+drafter、generator+checkerを重複なく合計 | 0以上、依存対応版 | 整数スカラー |
| `n` | 同条件の評価事例数 | 1（個数） | 事前分割ベンチ件数 | 正整数 | 整数スカラー |
| `r` | 正答率・成功率 | 1（無次元） | 成功件数/評価件数 | [0,1] | 確率スカラー |
| `t` | 生成レイテンシ | s | 同一入力のwall-clock | 非負 | スカラー |
| `u_c` | 合成標準不確かさ | 対象量と同じ | 誤差を評価した場合に限り推定 | 今回未定義 | スカラーまたは欠損 |
| `k` | 拡張不確かさ係数 | 1 | 未設定、実測データで指定 | 正値 | スカラーまたは欠損 |

**次元チェック**：Wはbyte、Pとnは無次元個数、tは秒。性能の無次元倍率やパラメータ数を重みbyteと直結させない。モデル比較の成功率を「人間の知能越え」という単一軸に変換しない。

## ERROR CHECK

v19想定：150資産／有効105件（select53/conditional52/hold27/deferred12/excluded6）。モデル127/データ23。総パラメータPASS111、未知14、超150B量子化調査2。旧Nanbeige維持、既存除外6件復活なし。取得承認0、モデル本体ダウンロード0、Torrent開始0、HDD削除0。
