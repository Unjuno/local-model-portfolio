# R87 — Xiaomi U0-4B：実際の学習成果・同族重複・依存の追加監査（2026-11-15）

## 1.〈本論〉選ぶ目的と暫定判定
リポジトリの目的は、将来の配布経路変更に備え**独立学習済みの価値ある原本・依存・実装を適法に保存すること**であり、規制予測の断定や形式違いの量産ではない。

**判断：** [XiaomiRobotics/Xiaomi-Robotics-U0-4B](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B)を**次回正式版のCONDITIONAL候補に採用推奨**。2026年11月15日の公式HFメタデータはUNIS architecture、主モデル5,082.1Mパラメータ、Apache-2.0タグ、public model listingを表示。作者の[固定GitHub README](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/blob/e722003980958f242203af265718ee980b834deb/README.md)と[固定推論手順](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/blob/e722003980958f242203af265718ee980b834deb/inference/README.md)は4Bの自己回帰推論とT2I/X2I、ロボット複数視点**Scene Gen/Transfer**を明記する。[原論文](https://arxiv.org/abs/2607.11643)を参照。動画生成[Wan2.2 TI2V](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)・[Cosmos Predict2](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World)と学習目的・入力/出力が同一でないため、研究上の追加価値がある。ただし比較実機品質の優越は未検証。

**同族の重複は採用しない。** [4B Sequence](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B-Sequence)は別interleave_subtask/video能力を持つが増分価値が未測定。[34B原本](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0)と[38B FlashAR](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-FlashAR)は保存費用増が大きく、4Bで代替できないタスクの独立実証が先。作者公表のH20・FlashAR-vLLM **5.44秒/画像・82.86倍**は大型モデル系列の条件であり、4B eager ARの速度ではない。

## 2.〈応用・転用例〉原本と依存を一組で扱う
**必須依存**は[BAAI/Emu3.5-VisionTokenizer](https://huggingface.co/BAAI/Emu3.5-VisionTokenizer)という別学習済みVQ（HF公表455.3M）。4B weights、processor/tokenizer/config、VQ weights、公式コードcommit `e722003980958f242203af265718ee980b834deb`、全LICENSE/NOTICE、Python3.10 eager AR環境・ABIを別々に監査する。RGB条件のTransferはDepth Anything 3を**任意**の追加依存とし、必須と決めつけない。

[Xiaomi公式コードLICENSE](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/blob/e722003980958f242203af265718ee980b834deb/LICENSE)のApache2.0とモデルHubタグは区別し、モデル重み・第三者VQ・商用/再配布へ適用する正文を別審査する。作者が案内する[ModelScopeの公式別配布元](https://modelscope.cn/models/XiaomiRobotics/Xiaomi-Robotics-U0-4B)は同一revision/全ファイルSHAと権利を照合した**ビット同一バックアップではない**。

4Bの固定weight revision、全shard SHA、選択ファイルbyte、依存の完全テンソル数、本人のアクセスと利用権、4TB計画内の実HDD容量・最低200GB空き、ピークRAM、品質、明示承認は未解決であり、**取得準備とモデル本体取得は停止**。公開廃止予定はモデル個別に確認できず、S1→S2→S3の将来規制連鎖は確率をつけない仮説。

## 3. 変数表と次元チェック
| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| P_m | 4B原本の公表主パラメータ | 1（無次元、個） | 5,082,100,000 | Hubメタデータ、完全pipelineではない | 整数スカラー |
| P_v | 外部VQ学習済みパラメータ | 1（無次元、個） | 455,300,000 | 別repo、完全一致SHAは未確認 | 整数スカラー |
| P_b | 150B基本スクリーン | 1（無次元、個） | 150,000,000,000 | 超過は現行の量子化例外審査 | 整数スカラー |
| B_s | 取得する全ファイル量 | byte（8 bit） | すべての必須重み・付属物の選択byte | 未確認=null（0ではない） | スカラー/null |

**単位検査**：公表済み2部品の合算は5,537,400,000**パラメータ個**であり、B_s（byte）と比較できない。全学習済み構成の厳密な合算とも断定しない。

## 4. H/T/D/C/U、ERROR CHECK
**H**：UNIS-4Bは既存の動画モデルだけでは保全できない多視点Scene Gen/Transferの独立学習成果。**T**：4B/Sequence/FlashAR/VQの公式ページ、作者固定コード、原論文を比較。次の実機評価ではScene Gen・Transfer各30試行、HW/backend/context/batch/量子化・入力を固定。**D**：固有技術機構の研究採用はPASS、取得権限・固定ファイル・依存・ベンチ実測はUNCERTAINで取得STOP。**C**：Wan/Cosmosの適切な後処理で同等の多視点成果を追加学習なしに得られる、または親権利を解決できない場合はHOLDへ戻す。**U**：HF計数の丸め、コード/weight版の不一致、VQ、権利、ABIと実機性能。分布未確定で合成u_cと包含係数kは算出不可。

**ERROR CHECK**：この監査は既存のCURRENT・候補キュー・承認済みキュー・正式資産件数を変更しない。既存選定と競合する間に不完全な正式versionを公開せず、独立証拠だけ先行記録する。モデル本体DL・実行は0。

## 5.〈次に考える問い〉
同一のロボット複数視点Transfer入力に対し、既存Wan/Cosmosで再現できないUNIS原本の学習済み能力を、何の定量指標で検証するか。
