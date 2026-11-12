# v28｜独立小型モデル2件の条件付き選定（2026-11-12）

**選定のみ、取得/実行は未承認**。指定ブランチstrategy/2026-11-03-01-risk、親コミット5327907928efc9743ea5b5ec0fb8fc9ca45c215b。既存v27の173件を保持し、新規2件で**175資産／有効128件**（モデル149／データ26、SELECT53／CONDITIONAL75／HOLD28／延期13／EXCLUDED6）とした。4TB計画枠・最低空き200GB・150B超同条件実測例外の研究HOLDは変更しない。

## 1. 〈本論〉今回選んだ独立重み

| 追加repo ID・一次URL | 具体的な別学習と競合 | 配布元のサイズ情報 | 未解決・反証条件 |
| --- | --- | ---: | --- |
| [qvac/BotPsy-0.8B](https://huggingface.co/qvac/BotPsy-0.8B) | 既採用Qwen3.5-0.8Bを別途SFT/多教師蒸留/RLでツールエージェント特化。メーカー自己計測BFCL v4 44.0対Base 23.4 | 約853M total、BF16本体約1.73GB | 英語主体、日本語未測定。LICENSE正文、原本SHA、固定revision、同一タスク独立性能を要確認 |
| [ibm-granite/granite-timeseries-ttm-r3](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | TinyTimeMixer-R3の独立時系列学習。既採用Chronos-2とは別系統。main単体を代表とし他枝/通常量子化の多重収集はしない | main約1.41M total、repo表示約6.13MB | R3 family全枝の総数とは混同不可。固定版とLICENSE、runtimeとChronos2同条件比較が未了 |

一次資料：[QVAC公式告知](https://qvac.tether.io/blog/on-device-ai-agent-botpsy)（2026-11-11）、[公式モデル情報](https://qvac.tether.io/models/botpsy)、[IBM公式モデルカード](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3)、[IBM実装](https://github.com/ibm-granite/granite-tsfm/blob/main/tsfm_public/toolkit/get_model.py)。HF連携でBotPsy約853M、TTM R3 main約1.41MのモデルサイズとApache-2.0メタデータを確認。ただし実体テンソルの精密な全カウント、全LICENSE/依存を確認したとの主張ではない。IBM CPU180 samples/s、GPU7500 samples/sも開発者自己評価でHW/clock/batch不完全のため実機値とはみなさない。

## 2. 研究HOLD、既存提案の保持

[NousResearch/Arete-27B](https://huggingface.co/NousResearch/Arete-27B)は独立52.8MトークンSFTで単なる量子化ではない。約54.7GBをさらに割くには既採用Orca/Interpretic/公式Qwenと同一タスクの追加価値を証明すべきで今回は研究HOLD。[AutoTrust JEV27B](https://huggingface.co/autotrust/AutoTrust-JEV-27B-v1.1)は型付き確率判定で既存3B Kananaと機能重複し、開発者のB300・vLLM0.31測定が独立の同条件比較ではないため研究HOLD。旧v28-r1のNorthCUA-Mini／PrimeSim／Muse-Glimmer-30Bは145GB固定ソース監査を残す**未採用提案**で、今回選定した2件と重複登録しない。

## 3. 容量・変数表・安全性

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・型 |
| --- | --- | --- | --- |
| C | 計画上限 | byte | 4,000,000,000,000、整数、実HDD容量未確認 |
| F | 最低空き | byte | 200,000,000,000、整数、実機値未測定 |
| S | 旧v27既知重複除去ソース量 | byte | 3,417,685,712,585、非負整数、完全依存総量でない |
| R | 2件の新規研究予算上限 | byte | 2,700,000,000（2.5GB+0.2GB）、整数、取得ファイル実測でない |
| P | 模型の学習済み総数 | 1（無次元） | Hub丸め値853M/1.41M、型は整数、固定精密数は未確認 |
| M | RAM/VRAM統合ピーク | byte | null、HW/backend/clock/quant zero-point/context/batch未測定 |

**次元検査**：C/F/S/Rはいずれもbyteのため和差計算可能。Pはパラメータ数でありbyteと直接加算できない。以前の3.418TBは旧126件の既知範囲で、v28新2件と外部学習済み依存・cache/staging・現物HDDを含む最終容量を示さない。ダウンロード用の正確なrevision、ファイルSHA、選択バイト、LICENSE、ABI、本人の容量と承認が揃うまで取得禁止。

## 4. H/T/D/C/U・ERROR CHECK

**H**：異なる学習済み状態の小型2件を保存候補とし、通常の同一重み量子化を増やさない。**T**：正規repo固定40字SHA・ファイル全SHAと完全依存・LICENSE・実機容量を静的審査、品質測定は取得/実行の別承認後に同HW/OS/backend/context/batchで最低30試行。**D**：カタログ選定の一意性と旧判断保存は静的PASS、取得可否は未確定（UNCERTAIN）、権利不適合・欠落ファイル・容量超過・重複ならFAIL。**C**：BotPsyのエージェント能力に有意差なし、TTM R3が用途上冗長。**U**：実ファイル/契約/マシンの誤差分布が無く、合成u_c/k算出不可。

**ERROR CHECK**：旧173件の内容を一意に全維持、2件のみ新規、175件／128有効／6除外／20総数未確認（有効7）／2つの150B超例外HOLD／承認済み0。Python単体テスト・実機実行は未実施。関連分野：端末AIエージェント、時系列統計、アーカイブ・ファイル同一性、ソフトウェア供給網/法務。

###〈次に考える問い〉
同じ保存容量なら、BF16の新たな学習済み重みと、既存重みから再現できるGGUFコピーのどちらを先に保全すべきか。
