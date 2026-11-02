# 第9回：公開4モデルのライセンスと共通実行環境

確認日：2026-11-01。前回固定したモデルを増やさず、実行環境の重複と未解決の許諾・依存を整理した。取得・インストール・モデル実行は一切していない。

## 1. 今回進めた範囲

対象はDepth Anything V2 Small、SAM2 Hiera Tiny、Qwen3Guard Gen 0.6B、SmolVLM2 500M Videoの公開4モデル。モデル側ファイルは前回の固定一覧を変更せず、合計 **3,809,117,834バイト**。手動GatedのDINOv3 ViT-Sは今回の公開4件から分離し、従来の承認待ちを維持する。

[機械可読の実行環境・ライセンス記録](../catalog/runtime-drafts/round9-runtime-license-2026-11-01.json)には、モデルの版、適用宣言の根拠、共通ランタイム候補、追加依存、未完了事項を記録した。最終的な取得lockではない。

## 2. ライセンス証拠を一段具体化

| モデル | 確認した一次資料 | 判断の範囲 |
| --- | --- | --- |
| Depth Anything V2 Small | [固定版README](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf/raw/5426e4f0f36572d16453bbda7a8389317b1bef99/README.md)、[作者のライセンス区分](https://github.com/DepthAnything/Depth-Anything-V2/blob/main/README.md) | SmallはApache-2.0の宣言。Base/Large/Giantの非商用条件を混ぜない |
| SAM2 Hiera Tiny | [固定版README](https://huggingface.co/facebook/sam2-hiera-tiny/raw/7c218beaf0bb87874785f32b582f640134fc1c09/README.md)、[公式SAM2説明](https://github.com/facebookresearch/sam2/blob/main/README.md) | モデル重みのApache-2.0宣言を確認。デモ用フォントやデータの条件は別 |
| Qwen3Guard | [固定版LICENSE全文](https://huggingface.co/Qwen/Qwen3Guard-Gen-0.6B/raw/fada3b2f655b89601929198343c94cd2f64d93cc/LICENSE) | Apache-2.0本文とAlibaba Cloudの表示を確認 |
| SmolVLM2 | [固定版モデルカード](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct/raw/7b375e1b73b11138ff12fe22c8f2822d8fe03467/README.md) | チェックポイントをApache-2.0で公開するという明示を確認 |

[Apache-2.0標準本文](https://www.apache.org/licenses/LICENSE-2.0)の許諾・特許・再配布・表示・免責を読んだ。LICENSEが独立ファイルとして無いだけで「無許諾」とは扱わない。ただし、宣言と適用対象を保存し、標準本文を補足資料として添える場合は元repo内ファイルと混同しない。必要な著作権表示・NOTICE・変更履歴を保全する。

この確認は提供者のチェックポイント許諾の証拠整理であり、学習データの全権利、あらゆる用途の適法性、ユーザーの取得承認を認定しない。実行ソフトウェアもすべてApacheになるわけではない。追加依存num2wordsはPyPIでLGPLと表示され、適用版と配布方法の別審査が残る。

## 3. 共通ランタイム候補を固定

**Transformers 5.22.1**を検証候補とした。これは実機で動作確認済みの推奨環境ではない。

- 公式Git tagの対応commit：`446a570e62b04a89ea001604ada7366baac2ea67`。
- [PyPIの固定版メタデータ](https://pypi.org/pypi/transformers/5.22.1/json)でPython 3.11以上、Torch追加機能の宣言下限2.6以上、依存の制約を確認。下限をそのまま安全な導入版としない。
- 固定ソース内の`depth_anything`、`sam2_video`、`qwen3`、`smolvlm`各モジュールの実装参照を確認。モデルを実際にロードしたわけではなく、重みとの完全互換性は未検証。
- 学習、クラウド提供、全機能、開発用extrasは基本構成から外す。単に`transformers[all]`を保存して容量・依存を膨らませない。
- CPU/GPU、OS、Python ABI、TorchとTorchvisionの組、動画decoder、必要な全wheelとドライバーはまだ固定しない。ユーザーの実機情報を推測で補わない。

### 特定した配布ファイル（メタデータのみ）

| 配布ファイル | 正確なバイト数 | 用途 |
| --- | ---: | --- |
| transformers-5.22.1-py3-none-any.whl | 13,051,755 | 共通実行パッケージ候補 |
| transformers-5.22.1.tar.gz | 10,381,794 | ソース・再現資料候補 |
| num2words-0.5.14-py3-none-any.whl | 163,525 | SmolVLM前処理に必要な依存候補 |
| num2words-0.5.14.tar.gz | 218,213 | 対応ソース・ライセンス確認用候補 |
| **合計** | **23,815,287** | **約23.815MB、完全runtimeの総量ではない** |

各ファイルの公開SHA-256をJSONへ記録した。バイナリもソース配布アーカイブも取得していないため、ローカル実物のハッシュ照合は未実施。Git commit、Git blob SHA-1、配布ファイルSHA-256は区別している。PyPIの脆弱性一覧が空でも、安全性証明とはしない。

## 4. 今回見つかった実装上の落とし穴

**SmolVLMにはnum2wordsが必要。** [固定Processor実装](https://github.com/huggingface/transformers/blob/446a570e62b04a89ea001604ada7366baac2ea67/src/transformers/models/smolvlm/processing_smolvlm.py)は、存在しない場合に初期化を失敗させる。num2words 0.5.14自体が`docopt>=0.6.2`へ依存するため、これも完全な環境ロックで解決する。

**動画用テンプレートがモデルファイルの文字列だけでは決まらない。** 同じ固定実装は、動画があり明示的なtemplate指定が無い場合、後方互換のため修正済みテンプレートを使う。元モデルのchat_templateを勝手に上書きせず、実行時に実際に使われたtemplateと版を別に記録する。

**Processorの設定を既定値で代用しない。** 固定SmolVLM2の`processor_config.json`は`image_seq_len: 64`。コードの既定値169で再作成する方法は、このcheckpointの再現にならない可能性がある。

**SAM2の実行経路を混ぜない。** 今回はTransformersの`Sam2VideoModel`とSafetensorsを選択した。ネイティブSAM2 predictorのサンプルを、そのまま同じ取得構成に適用するとは限らない。

## 5. 旧版の保存と通常実行を分離

[GHSA-29pf-2h5f-8g72](https://github.com/advisories/GHSA-29pf-2h5f-8g72)はTransformers 5.3.0未満の問題を説明し、5.3.0を修正版としている。モデルconfigに記録された4.xを、それだけで標準の実行版にしない。

別の[GHSA-x9r9-c232-4q39](https://github.com/advisories/GHSA-x9r9-c232-4q39)は4.49.0〜5.8.1を影響範囲として列挙するが、修正版欄は未指定。5.22.1がその範囲外であることと、あらゆる脆弱性が修正済みであることは別である。今回の照合は2件の公開勧告と配布情報に限定し、包括的監査とは呼ばない。

後日の実行では、明示的なローカルパス、Safetensors、remote code無効、custom generation不使用、ネットワークをOS/コンテナ側で遮断、認証情報・ユーザーファイルを渡さない隔離が必要。オフライン環境変数だけに依存しない。旧ランタイムは研究用資料としての保全と通常実行を分ける。

## 6. 次の承認ゲート

| 項目 | 状態 |
| --- | --- |
| 公開4checkpointの宣言・標準許諾本文の照合 | 証拠を記録済み。全権利監査ではない |
| 共有候補版・対応ソース・4配布ファイルのサイズと公開ハッシュ | メタデータとして固定済み |
| 全ての推移的依存・Torch/vision/decoder・OS/ABI | 未完了 |
| ネット遮断下の読み込み・推論・RAM・品質測定 | 未実施 |
| DINOv3 Gated同意・取得許可 | 承認待ち、代行していない |
| 正式なダウンロードキュー | 0件のまま |

H：共通の実装経路で4モデルを扱えば、無関係なbackendを重複保存せずに済む可能性がある。
T：まずソース・依存・許諾を確定。取得と実行の別承認後、各タスクのローカル入力で読み込み・出力構造・非有限値・ネットアクセスを検査する。
D：メタデータ照合はPASS。実行互換性、完全な保存容量、実機適合性はUNCERTAIN。未承認なら取得はBLOCKED。
C：モデルの版移行や前処理差、別decoder、ライセンス条件によって共通化案が破れる場合がある。
U：OS/ABI、推移的依存、実データ権利、精度・性能が未測定であり、合成不確かさや包含係数を数値化しない。

## ERROR CHECK

ローカルのメタデータ検査18項目を通過。モデル4件の版・ソース参照、公開ハッシュ形式、バイト集計、未承認フラグを確認した。推論テストではない。

正式台帳の暫定3.234TBへ今回の資材容量を加算していない。未知の依存容量を0で補っていない。モデル本体・wheel・ソースアーカイブの取得、インストール、外部コードの実行、HDD操作は行っていない。
