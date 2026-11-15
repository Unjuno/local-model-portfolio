# R85 / v37 — 保存の目的から逆算した原本確定と規制事実（2026-11-15）

## 1.〈本論〉— 「規制されそう」と「今取得できる」を分離

**正本v37＝191資産・144有効、構成はv36と同一。** 新規モデルの追加を止め、既存モデルの**実際の学習済み結果と原本ソースを確定**する。公開禁止の確率や年内一律制限は実測値がないので数値化しない。

| 司法管轄 | 現在の一次事実 | 事実からは導けないこと |
| --- | --- | --- |
| 日本 | [2025-09-01全面施行AI法](https://laws.e-gov.go.jp/law/507AC0000000053)は研究・活用推進が目的 | 日本で一般ローカル重み保存が全面違法になる確定予測 |
| EU | [AI Act Article 53](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng) は提供者の義務を規定。開源の条件付き免除は一部義務に適用、systemic riskには例外がない。[欧州委員会ガイドライン](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)は2026-08以降の執行に言及 | 全オープンウェイトの一律禁止 |
| 米国 | [BIS2025-05-13](https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens)はAI Diffusion規則の撤回・不執行方針を発表。[GAO2026](https://www.gao.gov/products/b-337935)は撤回発表の手続的性質を整理。原規則は一部のclosed-weightに関わる | 当該規則により現行の公開ウェイト全体がDL禁止 |
| 中国 | [商務部・科技部2026-10-16公告](https://www.mofcom.gov.cn/zwgk/zcfb/art/2026/art_0a31a3c9ac404f7a9b0e917ce3412997.html)はAI技術等の輸出前登録と改訂案を公表し、すでに開源・公開済みの技術を対象外と説明 | すべての中国モデルweightの既存公開を禁止 |

**保存判断**：合法的な入手が将来容易でなくなり得るのは事実だが、優先度は現在のGated状態、第三者再配布権利、異なる学習済み重み、完全依存の難易度、サイズから判定する。未来の禁止確率を架空計算して選ぶことはしない。

## 2. NVIDIA Kumo-Tabular — 保存する重みを6ファイルに固定

[公式モデルAPI・固定revision](https://huggingface.co/api/models/nvidia/Kumo-Tabular/revision/c5893d418e162b9f841ae179dc767afefff73831?blobs=true) の実返答を照合。source commit `c5893d418e162b9f841ae179dc767afefff73831`、公開Hubは `private:false` / `gated:false`、Model LICENSEは[同一revision OpenMDW-1.1](https://huggingface.co/nvidia/Kumo-Tabular/blob/c5893d418e162b9f841ae179dc767afefff73831/LICENSE) 。文章はモデル資料を条件付きで広く扱えるが、NOTICE保持、特許/著作権訴訟時の終了条項、第三者権利確認がある。**本人の権利・依存コードの許諾は未確定。**

[実装の固定読込コード](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/tabular/model.py) と [固定config](https://huggingface.co/nvidia/Kumo-Tabular/blob/c5893d418e162b9f841ae179dc767afefff73831/config.json) は default_size=`large`、分類`large/classifier.pt`、回帰`large/regressor.pt`。単一表のラベル文脈学習は既存Kumo Relationalの多表グラフ予測と異なり、Chronos/TTMは時系列予測で別目的。

| 選択対象 | 公開元byte | 公開元LFS SHA256 |
| --- | ---: | --- |
| Large分類器 | **854,850,034** | `cc21484316949641cc3d65a7bb6c36cdea854cc569435755ff23b850018ec613` |
| Large回帰器 | **862,909,259** | `745e0e5d97e4256d8a24cb61c2eecbd1128da6c83938c196b7589ea6f62e7421` |
| `LICENSE`/`README.md`/`config.json`/`.gitattributes` | **5,977** | 小型Git blob SHA1を別記録 |
| **原本候補6ファイル** | **1,717,765,270** | 公開元の型別チェックサム |
| **除外4ファイル**（Small/Medium別サイズ） | **720,168,092** | 同一目的のサイズ違い、追加効用未検証 |

通常の量子化コピーはゼロ。**除外720,168,092byteは配布元source候補から外した額**であって実HDD節約済みではない。公開元ファイルの正確なbyte/identityは[機械可読証拠](../../catalog/research/2026-11-15-r85-v37-kumo-tabular-source-and-policy-facts.json)に固定した。PyTorch `.pt` の安全なweight-only読込と完全依存は未検証であるため、正本`selected_file_bytes`と`fully_pinned_revision_sha`は**依然null**。重み本体未取得。

## 3. Perplexity Decider — 誤ったGated判断を修正

[固定revisionのHub API](https://huggingface.co/api/models/perplexity-ai/pplx-decider-flash-v1.3/revision/d06fb3f2d97e0a52325a0d463c450cf0338f44fe?blobs=true) は2026-11-15時点 `private:false,gated:false`。配布者内の `release-manifest.json` に `private:true` が残るが、これは**現行のHubゲート状態そのものではない**。access台帳の旧 `hub_gated:null` を `false` に訂正し、**ユーザー本人の取得・利用権は引き続きunknown**。巨大な2重み/Locate専用adapterと非因果readoutの新学習差分は維持、一般LLM量子化版の重複追加なし。

## 4. 実保存の非補償ゲートとロードマップ

v37は**144有効全て取得未承認**。現行台帳ではGated公表19件、総学習済みパラメータ未確定の有効9件、最終選定byteまたは全依存の完全版不足142件。公開元source subsetが固定できても、full trained pipeline、実HDD、必要最低空き200GB、本人のGated同意、runtime ABI、オフライン復元検証をすっ飛ばしてはいけない。

目的からの順序は ①現時点の適法アクセスとファイル公開状態を記録→②原本重みごとに親と独立学習成果/重複を識別→③１種類の原本ファイル集合とSHA、ライセンス、依存コード・codec・processorを固定→④実HDDのサイズとstagingを測る→⑤本人が承認した対象だけを取得しSHA照合とオフライン復元する。予測リスクは順番を変えるだけで、権利停止の例外にはならない。

## 5. 変数表・検証

| 記号 | 意味（日本語） | SI単位 | 定義／範囲／前提 | 型 |
| --- | --- | --- | --- | --- |
| N | 現行管理資産件数 | 1 | v37=191、整数 | 整数スカラー |
| A | 有効資産件数 | 1 | v37=144、0以上N以下 | 整数スカラー |
| B_s | 固定した6ファイルのbyte | byte | 1,717,765,270、公開元の合計 | 整数スカラー |
| B_e | 非選択4ファイルのbyte | byte | 720,168,092、公開元の合計 | 整数スカラー |
| C | 計画保存上限 | byte | 4,000,000,000,000、実空きとは異なる | 整数スカラー |
| F | 保存後最低空き容量 | byte | 200,000,000,000、実HDD未確認 | 整数スカラー |

次元チェック：B_s、B_e、C、Fは全てbyte単位で足し引き可能。学習済みパラメータ数（無次元）とは直に加算できない。

**H**：二つの公開元Large重みは別タスクであり、最小の6sourceで両者のチェックポイントを保全できる。**T**：固定source10ファイルのbyte/identityを全件照合（n_min=10）。別途全191資産・144有効・91条件付きの一意性と承認0を確認。**D**：source subsetの同一性はPASS、完全オフライン再現はUNCERTAIN/STOP、SHA不一致・権利不成立ならFAIL。**C**：公開元revision差、Python pickle loader、作者評価の非再現、transitive code取得不能。**U**：実ファイルのlocal SHA、OSS ABI、依存license、実HDD容量、時間変化は未知。分布未観測につき数値u_cとk算出なし。

**ERROR CHECK**：追加0／削除0／元の191資産選定保持／144有効／91conditional／公開Gated19／Hubゲート不明0／取得承認0。研究source6ファイルのみ正確に固定し、重み本体DL・実行0。

学際接続：ソフトウェア供給網（不変原本とSHA）、デジタル保存（必要最小集合）、AI規制法（合法アクセス）、統計学（分類・回帰の別学習状態）、サイバーセキュリティ（pickle・ABI）。

〈次に考える問い〉：予測される規制よりも、**現にGatedの19資産の本人許諾と、未固定の復元依存**のどちらが現在の保存遅延を支配しているか。
