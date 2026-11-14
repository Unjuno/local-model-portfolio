# R82｜正式v35：Muse Glimmer原重みとDFlash別学習成果の選定更新（2026-11-15）

**正本移行先：v35、189資産・有効142件。** 2026-11-15 v34（187件・有効140）から、Metaの独立学習済み2件のみをCONDITIONAL研究追加。旧187件は項目内容も選定も変更しない。追加の全ファイル・重みペイロードの取得・実行・利用許可は**0件**。

## 1.〈本論〉— 内部構成に基づく変更

詳細な公開元ファイル証拠と利用規約差分は[R81調査](81-muse-glimmer-original-and-dflash-learned-states-2026-11-15.md)、[証拠JSON](../../catalog/research/2026-11-15-r81-muse-glimmer-original-and-assistant.json)。

| 採用形式 | 重みと機構 | 独自性・選定 | 不確実性 |
|---|---|---|---|
| `meta-models/Muse-Glimmer-30B` | BF16原本2分割、29,776,626,688 stored parameters、index tensor payload 59,553,253,376 byte、言語52層・視覚50層 | マルチモーダル原本としてCONDITIONAL | 同一40桁revisionで重み/補助ファイルとMeta Usage Policyの全件権限未確定 |
| `meta-models/Muse-Glimmer-30B-assistant` | 専用DFlash5層、16-token block、target layer IDs [1,13,25,37,49]、5.11GB公開重みSHA | 原本と異なる後学習重みとしてCONDITIONAL（親target必須） | 2.556BパラメータはHub概数、親・runtimeの固定互換は未検証 |

**採用しない形式**：公式 `meta-models/Muse-Glimmer-30B-GGUF`（元原本の表現違い）。新規原本と専用学習ドラフターの2件だけを記録する。

独立性はモデルの性能優位と同義ではない。第三者による同一HW/backend/context/batchの比較品質およびassitantのspeculative受入率は未測定。Metaの[USAGE_POLICY](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/USAGE_POLICY.md)をApache-2.0タグと**別に確認・保全**し、事前の同意や適法な利用権限があると推定しない。

## 2. 一意性・容量・取得ゲート

v35 `catalog/effective-portfolio-2026-11-15-v35.json`に全189件を収録。キュー`queues/proposed-v35-2026-11-15.json`、依存`catalog/preparation/2026-11-15-insurance-bundles-v35.json`、access`catalog/access/2026-11-15-v35-conditional-hub-gates.json`、[全142件ゲート](../../catalog/readiness/v35-2026-11-15-r82-all142-gates.json)を同一ID集合で照合する。正式取得ロック／ローカル実機チェック／オフライン復元は0件。

- 新規保存計画枠：原本650億byte＋助手60億byte＝**710億byte**。実際の必要空き容量・一時 staging・共有runtimeは別であり、4TBと200GB空き床の物理適合は未証明。
- 取得ブロック：有効142件すべて。最終選択byte未確定140件、最終40桁pin未確定140件、完全学習パラメータ未確認9件、Gated観測17件。これらは選定記録の未完了性であり重み取得済みではない。
- `download_enabled=false`、`approved=false`、`queues/approved.json`空、全アイテム`download_approved=false`を保持する。

### 変数表と容量の次元チェック

| 記号 | 意味（日本語） | SI準拠単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_o` | Muse原本暫定確保枠 | byte | 65,000,000,000 | source統計ではなく予算上限 | 非負整数スカラー |
| `B_a` | DFlash助手暫定確保枠 | byte | 6,000,000,000 | 実bytes未確定 | 非負整数スカラー |
| `B_v` | v35増分の暫定計画枠 | byte | `B_o+B_a` | 全依存・stagingは別途 | 非負整数スカラー |

`B_v = 65,000,000,000 + 6,000,000,000 = 71,000,000,000 byte`。次元はbyte+byte=byteで整合。物理的容量を主張する式ではない。

## 3. H/T/D/C/U とERROR CHECK

- **H:** 配布元2件は異なる学習済み状態で、GGUFコピー重複を避けると原本＋ドラフター2件で独自性を保存できる。
- **T:** 配布元config/index/pointer/usage policy 2 repo、全v34→v35旧187 record完全一致、v35新規2 record、全142 active IDのqueue/preparation/access/readiness joinを検査。n_minは2新規原本、189全資産で一意性検査。
- **D:** 構成・独立性と管理IDはPASS、実機・完全権利/依存・ネットワークなし再現はUNCERTAIN、許可なし取得はFAIL/STOP。
- **C:** 異なるHF commitでconfigとshardsが不整合、DFlashとターゲットの版不一致、同一成果の量子化重複保存、ライセンスとusage policyを混同。
- **U:** 誤差の主因は最終選択ファイル・依存・runtime・実機物理容量の未知。測定誤差分布がないため`u_c`・包含係数`k`は定量不可。

**ERROR CHECK:** 既存187件を一切変更しない＋新規2件、189 ID一意、active142、SELECT53/CONDITIONAL89/HOLD28/DEFERRED13/EXCLUDED6、モデル163/データ26、全取得未許可。

**関連分野：** MLアーキテクチャ、デジタルアーカイブ、ソフトウェア供給網、ライセンス法。

## 4.〈次に考える問い〉

**原本・ドラフターの二系統を、4TB実物理容量の範囲で、変更追跡と権利・実行再現性を損ねず固定できるか。**
