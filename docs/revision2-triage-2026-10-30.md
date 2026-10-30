# ポートフォリオ第2稿 — 2026-10-30

第1稿は完成版として扱わず、最新の公開情報・再現困難性・選択容量で継続的に再審査する。

## 保存優先度の入れ替え案

| 状態 | モデル | 理由 |
| --- | --- | --- |
| 後回し | [FLUX.2 klein 9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | FLUX系列の重複。先に独立画像系列を保存 |
| 後回し | [Apertus MeditronFO 70B](https://huggingface.co/EPFLiGHT/Apertus-70B-MeditronFO) | 医療特化の他候補と予算競合。独立性の評価待ち |
| 後回し | [Nemotron 3.5 Transcribe 30B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | 小型ASR・翻訳との性能・費用比較待ち |
| 後回し | [Nanbeige4.3 33B Base](https://huggingface.co/Nanbeige/Nanbeige4.3-33B-Base) | 後学習済み版を暫定優先。Baseは後から再審査 |

## 追加を優先する能力

- 画像制作の別系列：<https://huggingface.co/briaai/Fibo-2.0-dev>。現在Gated、非商用利用条件。フル重みの原本保全が目的
- 音楽の生成・楽譜：<https://huggingface.co/m-a-p/YuE2-3B> と <https://huggingface.co/m-a-p/SheetSage2>、音響VAEと音楽Encoderも関連付ける。非商用ライセンス
- 小型音声：<https://huggingface.co/Edge0/Audio8-TTS-Realistic-0.6b>。多言語音声合成の別系列
- 小型判断モデル：<https://huggingface.co/LiquidAI/d1-omni-600M>。文字・画像・音声入力の分類判断を生成無しで実行
- 小型エージェント：<https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB>。4GB版の公開重み
- ハイブリッドMoE：<https://huggingface.co/LiquidAI/LFM2.5-24B-A2B>。24B総数・約2.45B活性
- 音声出力を含むOmni：<https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct>。音声・動画入力と音声生成

どの順位変更も将来の削除を断定するものではない。利用条件が未確定の資産はダウンロード承認しない。旧候補は削除せず比較・採用変更履歴として残す。
