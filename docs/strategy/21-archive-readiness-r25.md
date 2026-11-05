# R25 実機保存完成度と安全なローカル事前診断（2026-11-05）

## 結論
`catalog/CURRENT.json` はv18・144資産・有効99件。今回の対象はR21/R22で固定した**ChatR画像LoRA＋基盤**と**Interpretic Q4＋画像projector**の2構成のみ。[進捗の機械台帳](../../catalog/preparation/2026-11-05-completion-readiness.json)に16の排他的工程を定義した。**8工程PASS、残り8工程UNCERTAIN**（単純な項目数50%。作業量や実保存完了率を意味しない）。ユーザーHDDへの保存率は未観測で**算定不能**。GitHub承認済みキューは空。2026-11-05のDesktop Commanderデバイス照会で接続端末0、よって実機情報は一切捏造しない。

## 現実の状態・残る障害
| 対象 | 固定保存ファイル | 配布者ファイル合計 | 今回まだ不足する証拠 |
|---|---:|---:|---|
| ChatR LoRA＋Qwen Image 2.1 | 35 | 33,802,789,787 byte | 同一版基盤の実機ハッシュ・ディスク空き・新設定35step/CFG5の独立品質・CUDA/PyTorch完全lock |
| Interpretic Q4＋vision projector＋原本資料 | 12 | 17,738,357,352 byte | 目標環境のllama.cpp版とCPU/GPU RAM、Q4一般能力、ディスク空き、取得後の全SHA |

R22は10重みの**ヘッダー形状**、37非重み補助ファイルの同一性を確認したが、**重み10ファイルの全データのSHA256照合は未実施**。ChatRの`README.md`/`inference.py`について作者`SHA256SUMS`と実Git blobに矛盾があるので原文双方を保存したまま。これは重み破損の証明ではない。

## 追加したローカル・オフライン検査
標準ライブラリのみの[`scripts/archive_preflight.py`](../../scripts/archive_preflight.py)と[テスト](../../tests/test_archive_preflight.py)を追加。スクリプトは**読むだけ**で、ネットワーク通信・モデルロード・ダウンロード・ファイル書込・削除・インストール・Torrent起動を実装しない。既存ファイルについて**サイズ一致だけでは重複保存分を差し引かず**、元のLFS SHA256または通常Git blob SHA1を全件ハッシュ照合した場合だけ同一アーカイブ内の保存済み分を差し引く。

### Windowsでの使用例
実際のHDD・保存先をユーザー自身が指定する。下記の例示フォルダーは**存在を確認したパスではない**。

```powershell
py -3 scripts/archive_preflight.py --archive-root "E:\AI-Archive" --source-root "qwen-image-base=E:\AI-Archive\models\Qwen\Qwen-Image-2.1" --hash
```

この呼出ではstage/cache必要量と既存アーカイブの予算消費量が未入力なので、容量ゲートは**UNCERTAINのまま**。ユーザーが作業領域と既存合計を実際に測定した場合のみ、追加で`--staging-reserve-bytes`、`--existing-archive-bytes`（十進byte）を指定できる。

### macOS/Linuxの例
```bash
python3 scripts/archive_preflight.py --archive-root /mnt/AI-Archive \
  --source-root qwen-image-base=/mnt/AI-Archive/models/Qwen/Qwen-Image-2.1 --hash
```

全ファイルハッシュ照合は約33GB以上を逐次読み出すことがあり、HDDで時間がかかる。対象が存在しない場合はステータス`PARTIAL_OR_MISSING`。リンクが元リポジトリ外へ出る場合は`UNSAFE_PATH`。保存済みファイルが別ボリュームにある場合、正しいデータでも**今回のHDDに保存済みとは数えない**。

容量は**自由空間とアーカイブ計画予算を別判定**する。空き200,000,000,000byteの保持、アーカイブ計画3,800,000,000,000byteは設定の原則。USB HDDの物理機器識別、他ジョブが同時に使う容量、実際の前後処理のtempは別確認。両判定が画面上PASSでも取得承認ではない。

## 技術・測定条件
- **AIモデル評価**：R22の保存テンソル要素数を学習可能パラメータ数・VRAM・性能と誤認しない。量子化GGUFを一律4bitとは解釈しない。
- **システム工学**：Windowsのドライブレターだけでは物理ディスクを識別できない。実機のシリアル・接続先とユーザー指定を別の操作で照合する。
- **供給網とデジタル保存**：Hugging Face LFS payload SHA256、通常Git blob SHA1、トレントの配布・許諾条件を混同しない。

### 変数表・単位
| 記号 | 意味 | 単位(SI) | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `archive_target_bytes` | 保存予算 | byte | リポジトリの3.8TB十進方針 | 0以上 | 整数スカラー |
| `free_floor_bytes` | 必須空き余裕 | byte | リポジトリの200GB十進方針 | 0以上 | 整数スカラー |
| `pinned_selected_bytes` | 今回固定した保存対象合計 | byte | 4repo47ファイルの長さの和 | 0以上、元配布者情報 | 整数スカラー |
| `confirmed_reused_bytes` | 再利用がハッシュで確定した同一アーカイブの内容 | byte | repo全ファイル一致の容量合計 | 0以上、全ハッシュ済みに限定 | 整数スカラー |
| `staging_reserve_bytes` | 一時領域の明示的な予約 | byte | ユーザー環境の測定・計画により設定 | 未入力はnull、推定ゼロ禁止 | 整数または欠損 |
| `existing_archive_bytes` | 既存アーカイブ予算消費量 | byte | ユーザー実機で計測した値 | 未入力はnull | 整数または欠損 |

**次元チェック**：全てbyteで比較。base重みなどのディスク容量を推論RAMと同一視しない。単純チェックリスト8/16（50%）は無次元で、実機の保存進捗・性能不確かさへの換算不可。

## 判定と不確かさ（H/T/D/C/U）
- H：正しい元重み・正しい保存先なら全ファイル元ハッシュ一致と必要空きの両立が可能。
- T：実機の指定ディレクトリ、最大47ファイル全数、ハッシュ検証は標本抽出なし。取得やモデル推論は禁止。
- D：ソースハッシュ全件一致かつ実測空き・予算・ステージ条件を満たせば時点限定の容量PASS。未入力はUNCERTAIN、違反はFAIL。**最終取得可否の判定とは分離**。
- C：異なるリビジョン、同サイズ別ハッシュ、symlink逸脱、別ディスク重複、作業領域と同時ダウンロードによる空き不足。
- U：I/O競合、手動設定したstage幅、ドライブの物理識別、同時書込、ハッシュ検査後の時点差。評価システムの速度・品質・合成標準不確かさは未測定。根拠のない信頼区間や合成標準不確かさは作らない。

## ERROR CHECK
- 新規ツールはオフライン・読み取り専用。テストはファイルサイズ一致での誤節約、異なるSHA、ボリューム外再利用、symlink逸脱、stage不足、未知情報の不正PASSを検証。
- 既存の正式v18カタログ144件/有効99件、Nanbeige維持、ユーザー除外6件、`queues/approved.json`は変更しない。
- ユーザーの実機ファイルを一切変更していない。
