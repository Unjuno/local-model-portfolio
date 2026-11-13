# 第10回レビュー：4モデルのCPU参照環境と動画デコーダー

確認日：2026-11-01。**メタデータ調査のみ、ダウンロード・インストール・推論は未実施。** [参照環境JSON](../catalog/runtime-drafts/round10-cpu-reference-compatibility-2026-11-01.json)に、公式GitタグとCPU専用wheelの配布元SHA-256を記録した。

## 1. 固定した構成候補

| ソフトウェア | 対応版 | 根拠 |
| --- | --- | --- |
| Transformers | 5.22.1、commit 446a570e62b04a89ea001604ada7366baac2ea67 | 前回固定の4モデル共通実装 |
| PyTorch | 2.14.1、commit 5c4886908584029761b579af026dcfb627c84070 | 公式CPU wheelあり |
| Torchvision | 0.29.2、commit f12281517f1b2f6255904639b027c9436f3e5008 | 2.14以降対応、2026-10-28のアーカイブ展開とCPU演算検証の修正を含む |
| TorchCodec | 0.17.0、commit d9dc54238e173000bc3969eb3959777026ff9ae8 | PyTorch 2.11以降に対応、動画用 |
| Python | 3.11系 | Transformers 5.22.1の条件と一致。パッチ版は未固定 |
| FFmpeg | 未固定 | 動画デコードに必要な共有ライブラリ、権利/容量未確定 |

2026-10-28にPyTorch 2.15.0も公表されたが、今回は新しい版を追うのではなく、**2.14.1＋0.29.2を固定した比較基準**とした。速さ、安全性、動作の実測優位を意味しない。

## 2. CPU専用の2つの参照プロファイル

公式CPU index上の完全wheel名・公開SHA-256を、Linux x86_64とWindows amd64の各3wheelについて保存した。Linux想定はglibc 2.28以上、Python CPython 3.11。Windows想定は64bit・CPython 3.11。実機のOS/GPU等は**不明**なので両者は候補であり、両方を取得する計画ではない。

参照元：[PyTorch CPU index](https://download.pytorch.org/whl/cpu/torch/)、[Torchvision CPU index](https://download.pytorch.org/whl/cpu/torchvision/)、[TorchCodec CPU index](https://download.pytorch.org/whl/cpu/torchcodec/)。公開indexに表示されたSHA-256は、取得後に実物を検証したハッシュではない。

PyPIのLinux版PyTorch 2.14.1にはCUDA関連の依存宣言があるため、**通常のPyPI wheelのSHA・容量をCPU専用wheelへ転記しない**。公式CPU wheelの正確なサイズはまだ未取得であり、見積りのゼロ埋めはしない。

## 3. 動画デコーダーの重要な発見

[Transformers 5.22.1の固定video_utils.py](https://github.com/huggingface/transformers/blob/446a570e62b04a89ea001604ada7366baac2ea67/src/transformers/video_utils.py)では、動画ロード時の既定バックエンドは**PyAV**。TorchCodecを選ぶなら明示的にbackendを指定する必要がある。TorchCodec 0.17の[固定README](https://github.com/meta-pytorch/torchcodec/blob/d9dc54238e173000bc3969eb3959777026ff9ae8/README.md)では動画/音声の読み込みにFFmpeg共有ライブラリが必要で、サポート対象のメジャーバージョンは4～9と説明する。

前回決めたSmolVLM2のimage_seq_len=64、必要なnum2words、動画の有効チャットテンプレート、FPSと時間情報を維持する。SAM2のVideoProcessorについても、ネイティブ.pt用の手順とTransformers Safetensors用の手順を混同しない。動画機能の検証と、静止画・テキストの検証を分離する。

## 4. 追加のライセンス/依存

num2words 0.5.14はLGPL、その依存docopt 0.6.2はMIT。PyPIでdocoptの配布はソースアーカイブだけで、25,901バイトと公開SHA-256を記録した。これをビルドして互換wheelを得るには別の再現環境と作業承認が必要。FFmpegの共有ライブラリ、モデルの学習データ、Torchソフトウェアの許諾を全てApache-2.0とみなしてはいけない。

**未完了**：Pythonのパッチ版、OSイメージ/VCランタイム、CPU/GPUとドライバー、Torch等の実配布物容量、FFmpeg実体とライセンス、tokenizers/hub/Pillow等の推移的依存lock、実機RAM・レイテンシ・品質。公開4モデル側のファイル合計3,809,117,834バイトに、これらの未知容量を足した完全バンドル量は未確定。

## 5. H/T/D/C/U

| 記号 | 最小検証 |
| --- | --- |
| H | 共通CPU参照環境と単一動画バックエンドで、4モデルの実行資材をまとめられる |
| T | 公式コミットと両OS向け3wheelずつのSHAを確認。取得と実行の別承認後に各タスク3件以上のローカル入力でネット遮断、出力型、有限値、RAMを検証。不明な権利や欠落依存で逐次停止 |
| D | メタデータ一致はPASS。実機動作と完全な容量はUNCERTAIN。ライセンス・取得許可・完全依存が未解決ならダウンロードはBLOCKED |
| C | PyAV既定のまま起動、FFmpeg共有ライブラリ欠落、CPU BF16非対応、ネイティブ拡張/OS ABI不一致など |
| U | 依存容量・性能と実行環境は未測定。統計分布を設定していないため合成標準不確かさと包含係数は算定しない |

## ERROR CHECK

現行正式台帳はv2の110件・有効94件、暫定3,234,067,678,260バイト。取得承認キューは0件で、Gated申請・モデル/パッケージのダウンロード・インストール・実行・HDD操作は行わない。
