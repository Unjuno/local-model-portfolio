# R149／v63（2026-11-22）：取得報告99件後の候補11原本を再優先し、新しい特殊学習モデル5件を研究キューへ

## 目的と正本
対象：[v63 CURRENT](../../catalog/CURRENT.json) は **235登録・188有効（SELECT55／CONDITIONAL133）** のまま。取得側ledgerの **99モデル／1,478ファイル／1,879,994,309,866 byte VERIFIED** は報告値であって、今回のユーザーWindows D現物の独立SHA・法的権利・完全オフライン復元の実証ではない。既取得99件を再取得させない。

今回は、[R149旧キュー](../../queues/proposed-v63-r149-after99-11-research-only.json)で固定済みの11 repositoryの40字 immutable revision、selected path、publisher byteを **変更せず**、研究・保存の最適順序を確定し直す。[新しい研究専用順位表](../../queues/proposed-v63-r150-prioritized-sources-and-watchlist.json)を正本の補助文書とする。モデル重量取得・ユーザーによる個別manifest承認・コード実行・既存HDD削除は行わない。

## 1. 11配布元原本の優先順位とソース固定

| 段階 | 固定Publisher原本 | 選択byte | 研究上の判断 |
|---|---|---:|---|
| P0A | [KittenML/kitten-tts-2-pico](https://huggingface.co/KittenML/kitten-tts-2-pico) | 285,879,877 | 小型独立原本を先行審査 |
| P0A | [AuroraAI-Research/Aurora2-400M-A20M](https://huggingface.co/AuroraAI-Research/Aurora2-400M-A20M) | 1,599,571,502 | 小型独立原本を先行審査 |
| P0A | [internlm/Intern-Decision-0.8B](https://huggingface.co/internlm/Intern-Decision-0.8B) | 1,734,731,370 | 小型独立原本を先行審査 |
| P0B | [Cactus-Compute/mirage](https://huggingface.co/Cactus-Compute/mirage) | 237,985,863 | 固定するが権利/実装STOP |
| P0B | [mistralai/Timestral-28M](https://huggingface.co/mistralai/Timestral-28M) | 111,307,038 | 固定するが権利/実装STOP |
| P1 | [LiquidAI/LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B) | 3,854,651,108 | 親＋無検閲編集原本を連結保管 |
| P1 | [saidutta69/LFM3-VL-2B-heretic](https://huggingface.co/saidutta69/LFM3-VL-2B-heretic) | 5,334,098,126 | 親＋無検閲編集原本を連結保管 |
| P2 | [apple/FastFrames-S](https://huggingface.co/apple/FastFrames-S) | 947,927,443 | 外部親がない単体取得は不完全 |
| P3 | [OpenMOSS-Team/MOSS-VL-Realtime](https://huggingface.co/OpenMOSS-Team/MOSS-VL-Realtime) | 22,687,497,344 | 大規模専門モデルの実機条件待ち |
| P3 | [nvidia/Cosmos3-Nano-Sim-Transfer](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Transfer) | 31,750,521,262 | 大規模専門モデルの実機条件待ち |
| P4 | [ricursiveAI/Ripple-65B-Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | 129,572,889,973 | 容量・プレビューのためHOLD |

**計測対象と誤差**：非HOLD10配布元のPublisher **68,544,170,933 byte**。別途FastFramesのCF++/Wan親 **17,567,235,949 byte**、Cactus4.1.4ランタイム **4,137,947 byte** が必要。二重参照を単純加算した保守的ソース値 **86,115,544,829 byte** は取得予定容量・owner物理HDDの実空きではない。同一SHAのfileを調べてから再利用する。HOLD Ripple **129,572,889,973 byte** はこの10配布元集計に含まれない。

## 2. 決定の論拠と交換しない理由
**P0A** Kitten Picoの8言語別F32学習成果、Aurora2のscratch訓練MoEルータ、InternDecisionの独立した構造化選択予測は異なる能力を増やす。一般LLMの量子化違いは新モデルに数えない。PicoのINT8追加8形式を選択しない。Picoに日本語音声はない。
**P0B** Mirageは約51M極小視覚理解とcact+Safetensorsを1モデル成果に束ね、別cactus runtimeのABIとコード安全をSTOP。Timestral28Mは時系列の確率分位点推定としてIBM TTMと異なるが、Modified MITの前月連結月商USD20m条件があり権利を自動承認しない。
**P1** LFM3-VL-2B公式BF16親（1,918,181,888 learned elements）を指定40字commitで保管し、saidutta69 Heretic独立編集BF16重みとの差を保全する。Q4_K_M+mmprojは同じ編集学習成果の実行形式であり追加1モデルとは数えない。著者の拒否低減値は画像入力品質の優越を証明しない。LFM Open License v1.0に商用条件あり。
**P2・P3** FastFrames-S単体ではWan/CF++ parentの動画再現不可。MOSSリアルタイム映像とCosmos sim-transferは小型OCRとは異なるが、GPU/codec/driver/ライセンスと全依存の保全が必要。Ripple65Bは現物RAM/品質と追加価値が確認できるまでHOLD。

## 3. 今回発見したが正式カタログ採用にはまだしない5学習成果

| 新規一次公開元 | 既存モデルとの独立価値 | 仮判定と停止条件 |
|---|---|---|
| [inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0) | 16.7M physiological signal encoder distinct from forecasting | RESEARCH_HIGH。Physiological privacy/medical validity, source SHAs and full reconstruction not verified. |
| [tencent/WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B) | 3.2836B audio-and-video reasoning vs MOSS streaming video | RESEARCH_HIGH。Patched vLLM/SGLang, custom model code and complete processor/source scope unverified. |
| [ostris/primal_vae](https://huggingface.co/ostris/primal_vae) | Distinct approx 80M 2x1/2x2 learned VAE states | RESEARCH_HIGH。Exact checkpoints, custom code, latent compatibility and quality unverified. |
| [Octen/Octen-WebGR-0.6B](https://huggingface.co/Octen/Octen-WebGR-0.6B) | 730.3M generative navigation retrieval and 30,931,888 URL semantic-ID mapping | RESEARCH_MEDIUM。Weights alone insufficient; exact ID table, offline trie and use rights unverified. |
| [sorryhyun/anima-pixel-decoder](https://huggingface.co/sorryhyun/anima-pixel-decoder) | Approx 25M independent Anima pixel readout head | RESEARCH_HOLD。Needs exact Anima model and pipeline, derivative rights and visual fidelity validation. |

現行新規5件のモデルカードとlicenseメタデータを確認したが、全fileの40桁immutable revision・path・各整数byte・Git/LFS SHAと、実装依存を固定できていない。従って正式 `catalog/revisions/` に追加せずresearch only（新規正式選定0）。以前の235件を実験なしで置換しない。

## 4. 規制の一次根拠
[米国BIS 2026-11-19 Federal Register 91 FR 74970 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は、旧AI Diffusion Ruleのモデル重みECCN 4E091を撤廃。ほかの仕向け地/最終用途/先端半導体/遠隔計算の規制や個別MODEL LICENSEは消滅していない。**日本のローカル無検閲ウェイト一般の近い将来の所有禁止を確定事実としない**。今後のGated化やモデル公開削除は反証可能なストレスシナリオであり、予測の確率値は設定していない。

## 5. H／T／D／C／U
- **H**：11既存sourceのimmutable IDを保存したまま小型独立学習成果を先行させれば、99既取得の重複保存を抑えたまま最大限の構造多様性を確保できる。
- **T**：11/11ユニークIDと各40桁固定revの一致、上記phase byte再集計、5watchlistが固定source未完成のためdownload falseであること、approved0を静的検証。性能はowner環境のCPU/GPU/clock、driver、backend、quant方式/zero-point、context、batchを固定し、各能力30件以上を比較。権利・SHA・HDD最低空き200GBが破れたら逐次中止。
- **D**：正本数とID/byte・未承認一致ならSTATIC PASS。無断承認・同一重み重複・変更された重みrevを同一とした場合FAIL。owner SHA、権利、実runtimeの速度・完全復元はUNCERTAINなので実ダウンロードSTOP。
- **C**：Aurora Base品質が低い、Picoの必要言語がない、Hereticが視覚性能を落とす、Cactus native runtimeが動かない、WeMMとMOSSが実用途上重複して新モデル価値が低い可能性。
- **U**：Publisher性能測定の偏り、使用許諾、owner HDD残量、parent/processor、外部native ABI、ゼロポイント/量子化誤差を未測定。反復測定がないため合成標準不確かさ u_c と包含係数 k は数値化不可。

## 6. 学際的転用と境界
機械学習（小型MoEと重み編集）、音声・生体/動画信号処理、検索（semantic ID）、ソフトウェアサプライチェーン（SHAと実行ABI）、法律（ライセンスと輸出）に適用。**今回の新規重量DL0、owner SHA再検証0、approved queue変更0、未審査model code実行0、既存資産削除0**。
