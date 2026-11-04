# v11補足：無検閲・NSFWの具体的チェックポイント抽出

**抽象的な分類で止めず、実在する配布元repo IDを4件抽出**。現行v11の97有効資産とは別の候補台帳で管理する。未検証のまま取得キューに追加しない。

| 候補 | 分野・技術 | 一次根拠 | 判断 |
|---|---|---|---|
| [coder3101/Qwen3.5-27B-heretic](https://huggingface.co/coder3101/Qwen3.5-27B-heretic) | MPOAによる拒否方向重み編集 | 作者報告は拒否14/100、元モデル94/100。**作者測定であり独立再現なし** | 比較候補。27Bの本体数は公表、視覚/補助学習済み構成の全数を要検証 |
| [IbarakiDouji/WAI-NSFW-illustrious-SDXL](https://huggingface.co/IbarakiDouji/WAI-NSFW-illustrious-SDXL) | 成人向け画像微調整 | 正確な配布元repoとv12の6.94GBチェックポイントを確認 | 比較候補。総パラメータ数・版別ライセンス未確認 |
| [ChrisColeTech/LTX-2.3-uncensored-v1.4-FP8](https://huggingface.co/ChrisColeTech/LTX-2.3-uncensored-v1.4-FP8) | NSFW＋蒸留＋参照詳細LoRAの動画音声マージ | 作者が構成ファイルと用途を明記。license:unknown | 比較候補。全モデル総数・権利未確認 |
| [Phr00t/LTX2-Rapid-Merges](https://huggingface.co/Phr00t/LTX2-Rapid-Merges) | 旧NSFW動画マージ | 作者自身が旧版化・保守縮小を説明 | 今回は不採用 |

## 既存モデルとの比較と決定条件

- テキスト：`orcarouter/Qwen3.8-27B-Uncensored`と**異なる基盤モデル・編集方式**であるため、単なる同一モデルの量子化ではない。作者報告の拒否率だけで品質が優れるとは判断しない。
- 画像：現行の`OnomaAIResearch/Illustrious-XL-v1.1`は総数未確認でHOLD。WAIは別チェックポイントだが、両方の総数とライセンスを確認してからどちらかを代表選定。
- 動画：現行の`Lightricks/LTX-2.3`は汎用原本。NSFWマージ版は後学習差分の研究対象。親モデルの許諾、LoRAの各権利、全構成のパラメータ総数を確定するまで取得禁止。
- 音声：成人向け専用TTSの独立した一次チェックポイントを今回確定できていないため、存在を捏造して追加しない。

**次の比較実験**：同条件の一般性能・拒否率・成人向け生成品質・音声同期・保存容量・必要VRAMを評価。顔・声の本人同意とプライバシー、違法コンテンツの除去要請を独立ゲートにする。

## ERROR CHECK

一次repo IDを4件確定、比較候補3件、不採用1件。現行有効97件に変更なし。150B以上は絶対除外、総数不明は取得準備停止。取得承認0件。実機・X:ドライブへの操作なし。
