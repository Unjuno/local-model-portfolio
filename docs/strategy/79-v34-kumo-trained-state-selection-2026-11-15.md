# v34：NVIDIA Kumo独立学習成果2件を正式な研究選定へ（2026-11-15）

## 1.〈本論〉

基準v33は185資産・138有効。v34は**187資産・140有効（モデル161・データ26、SELECT53・CONDITIONAL87）**。旧185件の採否を変更せず、次の2学習結果をCONDITIONAL追加した。単純量子化・small/mediumモデルの一括保存はしない。

| 原本モデル | 実際に検査した内部／固定ファイル | 判定 |
|---|---|---|
| [Kumo-Tabular](https://huggingface.co/nvidia/Kumo-Tabular) | Large分類器`large/classifier.pt`と回帰器`large/regressor.pt`は別学習。数値/カテゴリFourierセル埋込み→行/列attention→24層1024chのICL。公式公称**213.67M+215.68Mパラメータ**。公開treeの二重量は855MB/863MB（丸め値） | **追加**。Large一組に限定。モデルrepo完全SHAと個別LFS hashは未固定 |
| [Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) | v33の7ファイル・243,656,960byteの独立関係表モデル。外部キー間のグラフ伝播を含む | **維持**。重複追加なし |
| [Kumo-Anomaly](https://huggingface.co/nvidia/Kumo-Anomaly) | 無ラベル多変量時系列の拡散復元と異常閾値。単一`final_model.pth`は**29,600,287byte**、公開SHA256 `e7c2c06ac290d5ad42c8528caaefea3e6e0cb3d77227d2eca79f81ee427811a5` | **追加、実行STOP**。総学習済みパラメータ数不一致で最終ロック不可 |
| [Kumo-Forecast](https://huggingface.co/nvidia/Kumo-Forecast) | MOMENTバックボーン+DARR時系列予測。既存Chronos-2/IBM TTM R3と目的が重なる | **非追加**。追加利益未実証 |

**ソースコード実見:** NVIDIA `structured-data-models` [固定commit `46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87`](https://github.com/NVIDIA/structured-data-models/tree/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87) の[Tabular](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/tabular/model.py)、[Relational](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/relational/model.py)、[Anomaly](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/timeseries/anomaly/model.py)についてファイル名・学習対象・`torch.load(weights_only=True)`を照合。**重み本体のtensor内容を取得・逆シリアライズしたものではない**。［モデル一次仕様］(https://docs.nvidia.com/sdgm/structured-data-models/overview)

### 保存上の問題

Kumo TabularとRelationalはOpenMDW-1.1、AnomalyはApache-2.0メタデータ。完全ライセンス・権利と各依存は未閉包。Kumo Anomalyの旧Kumo-TSには`weights_only=False`経路があり、代替NVIDIA公式コードには同一SHAの`weights_only=True`経路があるが、PyTorch修正版・OS/driver/ABI・隔離復元を確認するまで**絶対に実行しない**。公式モデルカードの「約8M」と公式SDM APIの2.44Mが異なるので全テンソル総数は未確認。

## 2.〈応用・転用例〉

単一表ICLは統計学／AutoML、Relationalはデータベースとグラフ学習、Anomalyは計測時系列と設備保全に対応する。既存予測器を削除せず、異なる入力型・目的・学習済み重みの差で保存する。

## 3. 検証・安全限界

| 記号 | 日本語での意味 | SI単位 | 定義・前提／範囲 | 型 |
|---|---|---|---|---|
| N | 管理資産件数 | 1 | 187、非負整数 | 整数スカラー |
| A | 有効研究選定件数 | 1 | 140、0〜N | 整数スカラー |
| B_t | Tabular暫定研究枠 | byte | 2,500,000,000、確定容量でない | 整数スカラー |
| B_a | Anomaly暫定研究枠 | byte | 500,000,000、確定容量でない | 整数スカラー |
| C | HDD計画予算 | byte | 4,000,000,000,000、物理実測でない | 整数スカラー |
| F | 保存後必要な実空き | byte | 200,000,000,000、実測前 | 整数スカラー |

新規予約枠は**3,000,000,000byte**。追加のPyTorch実体や依存ソフト容量・stagingは未検証。次元確認：B_t、B_a、C、Fはいずれもbyteで、パラメータ個数とは加算できない。

**H**：追加2件は既存185件と同一訓練重みの別形式ではない。**T**：全187 ID照合と公式コードの2種チェックポイント、公開SHA、権利、隔離復元を検査。n_min=187、ローカルテンソル・実機推論は未実行。**D**：重複0／有効140／承認0はPASS、実HDD保存・安全な復元・完全権利はUNCERTAIN／取得STOP。**C**：同一重み重複、pickle実行、未適合契約、ABI崩壊が反例。**U**：公開容量の丸め、未固定Tabular重みSHA、Anomaly総数不一致、実機容量が誤差源。実測なしでu_c/kは算出不能。

**ERROR CHECK:** v33の185件はそのまま、v34で2件のみ追加、モデル161/データ26、select53/conditional87、PASS137・UNVERIFIED22・大型HOLD2。Gatedは本人権限と混同しない。モデル本体DL0、承認0。

〈次に考える問い〉：新しい専門モデルを保存する際、機能差と重み差のどちらが不可逆な情報損失の判定により強く効くか。
