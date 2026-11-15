# R84｜Kumo-Relational原本2重みのパラメータ上限・重複・依存実査（2026-11-15）

結論：**現行v36の`nvidia/Kumo-Relational`を維持し、`Kumo-Tabular`への統合・置換は行わない。** NVIDIA公式の固定コードで2種類の重み読込経路とパラメータ範囲を確認。これは性能評価による優位証明や、ユーザー実機のダウンロード承認ではない。

## 1.〈本論〉— 名前ではなくコードと原本2チェックポイント

一次資料：[固定NVIDIAコード](https://github.com/NVIDIA/structured-data-models/blob/46a6f20d20f1140912f7a9e6ecdda9a3cd3fda87/sdm/models/kumo/relational/model.py)／[公式モデル仕様](https://docs.nvidia.com/sdgm/structured-data-models/models/kumo-relational)／[配布元モデルカード](https://huggingface.co/nvidia/Kumo-Relational)。調査JSON：[`r84-kumo-relational`](../../catalog/research/2026-11-15-r84-kumo-relational-publisher-parameter-bound.json)。

**固定コードの実見:** `KumoRelational.parameter_count`は「29.93M–30.94M」。`_load_from_pretrained` は分類用`classifier.pt`、回帰用`regressor.pt`をそれぞれ`revision="v1.0.1"`で呼び、`torch.load(..., weights_only=True)` で取得したstate dictを`model.load_state_dict(..., assign=True)`に割り当てる。構成は`RowEmbedding + InvariantGNN + ICLBlock`。これらの固定ソースに**第三の事前学習済み重みをロードする経路は見つからない**。ただしライブラリ全依存を静的に完全証明したわけではない。

| 公式ファイル | パブリッシャーの表示byte | 公開元SHA256（ローカル再計算ではない） |
|---|---:|---|
| `classifier.pt` | 119,862,733 | `0c2e35cc18303f0d3ddeaf04e9cab6ca3a8bd6ea17195ac0e42d47af4bcb2a2d` |
| `regressor.pt` | 123,786,699 | `f863b3632f738e1444fb83a8cea5746f298889b5c96953a000c4720d202ae4cf` |
| 2重み合計 | **243,649,432** | 同一HF repo固定revisionの別ファイル |
| 支持ファイルを含む7ファイル | **243,656,960** | `efdbb110daea5aae123447864a64612e8a3dc6be` の過去公開元参照 |

**パラメータ規模の安全な判定：** NVIDIA公式のモデル別最大値30.94Mを2チェックポイントの両方に適用した上限は61.88M。150B閾値を大きく下回る**配布元根拠の上限制約が成立**する。一方、これはローカルの実tensor要素数全数ではないため、現行`parameter_gate.status=UNVERIFIED_BLOCK_FINAL_LOCK`を勝手にPASSへ昇格しない。別欄で**`PASS_PUBLISHER_TWO_CHECKPOINT_UPPER_BOUND_LT_150B`**として記録する。

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `n` | 読込む独立学習チェックポイント数 | 1 | 2（分類＋回帰） | 2、独立ファイル | 整数スカラー |
| `P_max` | NVIDIAが示す1モデルの最大パラメータ | 1 | 30,940,000 | NVIDIA固定コードが正しく2系統に適合 | 非負整数スカラー |
| `P_bound` | 2モデルの保守的パラメータ上限 | 1 | `n × P_max` | 他の重みが必須でない場合 | 非負整数スカラー |
| `P_gate` | 保存計画の標準モデル規模境界 | 1 | 150,000,000,000 | v36方針、法的な規制閾値ではない | 非負整数スカラー |
| `B_weights` | 2重みの公開元合計容量 | byte | 243,649,432 | 公開元ファイルサイズの和 | 非負整数スカラー |

`P_bound=2×30,940,000=61,880,000 < P_gate=150,000,000,000`。次元検査：モデル数（無次元）×パラメータ数（無次元）＝パラメータ数（無次元）。重みファイル容量のbyteからパラメータ数を推定していない。

### 重複・入替の判断

- `Kumo-Tabular`は単表の列特徴・行attentionの学習済み分類/回帰で、`Kumo-Relational`は外部キー関係と`InvariantGNN`で複数表を推論する。**出力が分類/回帰で一致するだけで、原本を重複扱いしない**。<br>
- `Kumo-Anomaly`は別の時系列拡散異常検知として維持。ただしパラメータ表示2.44Mと約8Mが矛盾し、旧SDKに安全でない`torch.load(weights_only=False)`がある。該当. pthは一切実行しない。<br>
- `Kumo-Forecast`は既存Chronos-2/TTM R3と予測タスクが重なり、独自学習があっても容量増分の正当化に足る同条件比較がないため引き続き非選定。

### 利用条件

[OpenMDW-1.1公式条文](https://openmdw.ai/license/1-1/)に、利用・複製・再配布の広い許諾、再配布時のライセンス・原著表示の保存、他者権利確認の責任がある。配布元の説明はBSD-3-ClauseのTabICLv2帰属も要求する。**一般ライセンス条文を確認したことと、当該revisionの原本LICENSE・Third-Party notices全SHAおよび本人の適法な用途が確定したことは別。**

## 2.〈応用・転用例〉

関係データベースの複数表予測、AutoMLの非定常分類、時系列異常検知に共通の前処理・runtimeを共有する場合、コードcommitとwheelhouseを1セットで保存し、各別学習済み重みのみ別々に原本固定する。ただしSHA一致のない共有推定で容量を差し引かない。

## 3. H / T / D / C / U、ERROR CHECK

- **H**：分類＋回帰の2固定重みは各最大30.94Mパラメータで、重複しない機構を保ちながら150B閾値内に収まる。
- **T**：NVIDIA固定コード5ファイル、2ロード経路、2重み公開元SHA、一次仕様と license/NOTICE を非実行で検査。n_min=両チェックポイント2件、追加学習済みruntime依存が見つかれば停止/再評価。
- **D**：パブリッシャー上限に基づく予備パラメータ判定PASS、独自機構の区別PASS。最終LOCK・実機復元・所有者利用権利はUNCERTAIN。公開元重みSHA不一致または別学習済み外部依存の出現はFAIL。
- **C**：配布元モデル規模が旧版のメタデータである、checkpointに想定外重みがある、自己参照の外部チェックポイントを暗黙取得する、PyTorch ABIの変更。
- **U**：パブリッシャー報告値は丸め、実tensor全要素とwheelhouseは未計測。誤差分布がなく`u_c`・`k`を推定しない。

**ERROR CHECK**：2重み公開元サイズ和243,649,432 byte、7ファイル総計243,656,960 byte、NVIDIA最大値から61,880,000個の上限、canonical選定の追加/削除0、モデルDL/実行0。

関連分野：グラフニューラルネット、統計的分類・回帰、データベース、ソフトウェア供給網。
