# R106 — v45・151選定資産の公開元容量と重複保存の再計算（2026-11-18）

## 1.〈本論〉— 4TBに対する容量再評価

最新正本は v45（198資産、151件active）。歴史的なv27の126件については配布元の選択ファイルSHA-aware union、以降の新規25件については出版社の公開Hub source-sizeを突き合わせた。**ダウンロード済みサイズではなく、保存予定の配布元sourceの暫定代理値**である。

| 区分 | 十進単位 | byte（整数） |
| --- | ---: | ---: |
| v27・126件の旧SHA-aware source union | 3.417686 TB | 3,417,685,712,585 |
| v28〜v45追加25件のrepo全量 | 433.652 GB | 433,651,894,316 |
| 2件で除外した別形式・付属コンテナ | 119.173 GB | 119,172,853,939 |
| 追加25件の調整後source代理容量 | 314.479 GB | 314,479,040,377 |
| **現行151件のsource計画代理値** | **3.732165 TB** | **3,732,164,752,962** |
| 4TB上限から最低空き200GBを引いた枠 | 3.8 TB | 3,800,000,000,000 |
| **追加依存・HDD未計測の仮余裕** | **67.835 GB** | **67,835,247,038** |

**判断:** 以前の約3.76TBという数値を、v45の実容量として確定しない。現時点の新しいsource proxyは**約3.732TB**だが、追加ソフトウェア・学習済み依存・キャッシュ・ステージング・ライセンスと実ドライブ計測が済んでいないため、3.8TB以内に実際に収まる保証はない。個別取得承認は0件。

## 2.〈応用・転用例〉— 重み構造から決めた保存方式

**RFD4-Proteina:** 公式repo全体107.083GBから、native flow+AE統合済み学習原本、独立事前学習Base、後学習LoRA、および設定・LICENSE等の12ファイル**3.494GB**を固定した。現行モデル本体SHAは旧v45に記録された先行コミットと新しい配布元コミットで一致。独立した抗体版チェックポイントは、今回の原本とは別学習成果の可能性があるため無断削除や重複認定は行わず別件審査に残す。AlphaFold/OpenFoldの外部refolding containerには別ライセンスがある。[固定ファイル・SHA](../../manifests/drafts/r106-v45-rfd4-pretrain-plus-merged-original.candidate.json)／[公式モデルカード](https://huggingface.co/nvidia/RFD4-Proteina)。

**ZONOS3-Mini:** 公式repo全体30.918GB、原本PyTorchのLM、ZAC-1 codec、SSL teacher、2つの独立学習済みdecoder（keep2/full_mr）、speaker encoder、音声編集LoRA、必要なレジストリの20ファイル**15.335GB**を固定。GGUF・WebGPU変換とvoice demoは他形式の重複として選定しない。旧非公開release lexiconは現在公開されていないため、発音辞書関連の完全機能復元は主張しない。[固定ファイル・SHA](../../manifests/drafts/r106-v45-zonos3-native-original.candidate.json)／[開発元のreleaseチェックポイント説明](https://github.com/Zyphra/ZONOS3-Mini/blob/1182469aa752e9881acfdab1734f7ece25193e8b/docs/release_checkpoints.md)。

この2件は独立した原本・LoRA・専門デコーダの学習成果を残しており、単純な容量削減のために必要な訓練済み成果を失う方針ではない。ただし、モデルの外部コード・codec・モデルを必要とする利用形態、本人の目的における権利と再現性の個別審査は継続する。

## 3. 追加25件の配布元ソース容量 — 個別照合

| モデル | 配布元全量 GB | 計画に計上 GB | 計画の種類 |
| --- | ---: | ---: | --- |
| [qvac/BotPsy-0.8B](https://huggingface.co/qvac/BotPsy-0.8B) | 1.726 | 1.726 | 全repoの暫定代理値 |
| [ibm-granite/granite-timeseries-ttm-r3](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | 0.006 | 0.006 | 全repoの暫定代理値 |
| [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | 30.918 | 15.335 | 固定した原本部分集合 |
| [robbyant/lingbot-touch-tiny](https://huggingface.co/robbyant/lingbot-touch-tiny) | 0.022 | 0.022 | 全repoの暫定代理値 |
| [nvidia/Alpamayo2-Edge](https://huggingface.co/nvidia/Alpamayo2-Edge) | 5.320 | 5.320 | 全repoの暫定代理値 |
| [ACE-Step/acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 19.953 | 19.953 | 全repoの暫定代理値 |
| [tencent/Qwen3.8-27B-DSpine-b16](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | 4.052 | 4.052 | 全repoの暫定代理値 |
| [nvidia/Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization) | 0.710 | 0.710 | 全repoの暫定代理値 |
| [nvidia/RFD4-Proteina](https://huggingface.co/nvidia/RFD4-Proteina) | 107.083 | 3.494 | 固定した原本部分集合 |
| [ibm-granite/granite-4.1-3b-llmon-preview](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview) | 7.327 | 7.327 | 全repoの暫定代理値 |
| [perplexity-ai/pplx-decider-flash-v1.3](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3) | 9.626 | 9.626 | 全repoの暫定代理値 |
| [nvidia/Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) | 0.244 | 0.244 | 全repoの暫定代理値 |
| [nvidia/Kumo-Tabular](https://huggingface.co/nvidia/Kumo-Tabular) | 2.438 | 2.438 | 全repoの暫定代理値 |
| [nvidia/Kumo-Anomaly](https://huggingface.co/nvidia/Kumo-Anomaly) | 0.032 | 0.032 | 全repoの暫定代理値 |
| [meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | 59.582 | 59.582 | 全repoの暫定代理値 |
| [meta-models/Muse-Glimmer-30B-assistant](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant) | 5.112 | 5.112 | 全repoの暫定代理値 |
| [nvidia/Ising-Decoder-ColorCode-1-Fast](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | 0.006 | 0.006 | 全repoの暫定代理値 |
| [nvidia/Ising-Decoder-SurfaceCode-1-Fast](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | 0.002 | 0.002 | 全repoの暫定代理値 |
| [higurashi-ai/Haru-4B](https://huggingface.co/higurashi-ai/Haru-4B) | 10.560 | 10.560 | 全repoの暫定代理値 |
| [runwayml/praxis-1-droid](https://huggingface.co/runwayml/praxis-1-droid) | 54.405 | 54.405 | 全repoの暫定代理値 |
| [XiaomiRobotics/Xiaomi-Robotics-U0-4B](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B) | 10.175 | 10.175 | 全repoの暫定代理値 |
| [GroundingPI/GroundingPI](https://huggingface.co/GroundingPI/GroundingPI) | 9.806 | 9.806 | 全repoの暫定代理値 |
| [IFM/PAN2](https://huggingface.co/IFM/PAN2) | 86.174 | 86.174 | 全repoの暫定代理値 |
| [KRAFTON/Raon-1-nano](https://huggingface.co/KRAFTON/Raon-1-nano) | 7.183 | 7.183 | 全repoの暫定代理値 |
| [abel-lab/Simons-297M](https://huggingface.co/abel-lab/Simons-297M) | 1.190 | 1.190 | 全repoの暫定代理値 |

25件すべての配布元の公称repo容量は確認したが、**個別の最終必要ファイル一式を固定したのは今回2件**。残り23件の全repo代理値は重複形式を含み得るため過大評価の可能性があり、逆に外部にある学習済み必須部品やwheelhouseは未算入で過小評価の可能性がある。Meta Muse Glimmerの1件はHugging Face APIのusedStorage数値（ファイル別和ではない）。詳細は[容量根拠JSON](../../catalog/capacity/2026-11-18/v45/publisher-source-reconciliation.json)に保管した。

## 4. 変数表・算術および次元検査

source代理値の算術： B_proxy = B_old + Σ S_i - D_R - D_Z = 3,732,164,752,962 byte。

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
| --- | --- | --- | --- | --- |
| B_proxy | 現行source代理合計 | byte | 非負、完全保存容量ではない | 整数スカラー |
| B_old | v27歴史的source union | byte | 3,417,685,712,585 | 整数スカラー |
| S_i | 新規25件の各repo全量 | byte | 非負、公開メタデータ | 整数スカラー |
| D_R | RFD4の採用しないソース部分 | byte | 103,589,187,635 | 整数スカラー |
| D_Z | ZONOS3の採用しないソース部分 | byte | 15,583,666,304 | 整数スカラー |
| C | 計画上の上限容量 | byte | 4,000,000,000,000 | 整数スカラー |
| F | HDDに維持すべき空き容量 | byte | 200,000,000,000、未実測 | 整数スカラー |

単位確認：加減算に用いる量はすべて byte。10^12 byte = 1TB、10^9 byte = 1GB で換算。C-F-B_proxy = 67,835,247,038 byte は計算上の残差であり、所有者HDDの実空き容量ではない。

## 5. H/T/D/C/U および ERROR CHECK

H: 親原本・追加学習差分・独立デコーダを保存しながら通常変換版を除外すれば、公開元容量が減る。
T: v27 126 IDとv45 151 IDの差分25件、全25 source bytes、選択済み32ファイルとSHAをコードで検算。原本には一切実行/ダウンロードしない。
D: 151 activeのメンバー、25件source metadata、RFD4 12 / ZONOS3 20 file selection、容量算術が整合するなら研究監査PASS。現物保存についてはUNCERTAIN。
C: 外部必須codecやthird-party licenseでソースが使えない、実HDDに他データがある、選定対象が変わる場合は計画見積りが破れる。
U: 旧126 sourceの鮮度、23件の選択ファイル、依存環境、ファイルシステムの実測が主要な未確定源。測定分布不在につき合成不確かさu_cや包含係数kは算出不可。

**ERROR CHECK:** 新25件の全repo合計433,651,894,316 byte、2件の非選択部分119,172,853,939 byte、代理総容量3,732,164,752,962 byte、実際の取得承認0。旧126件に追加25件、撤回0を確認。これはダウンロードの実績ではない。

## 6.〈次に考える問い〉

次は残り23件のリポジトリ全量を配布元SHA付きの必要ファイルだけに絞り、真の依存総量と実HDD残容量を照合すべきではないか。
