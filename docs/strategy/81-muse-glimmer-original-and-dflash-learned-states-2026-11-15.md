# R81｜Muse Glimmer 30Bと専用DFlash assistantの内部構成・原重み確認（2026-11-15）

基準：GitHub `main` v33／185資産（調査開始時）。本資料は**公開元のconfig、safetensors index、重みpointer、usage policyの実査**である。重み本体のローカルダウンロード・推論実行・権限同意は行っていない。

## 1.〈本論〉— 同じモデルの量子化ではない2件

| 出典と学習済み成果 | モデル原本 | DFlash assistant |
|---|---|---|
| 配布元 | [Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | [Muse-Glimmer-30B-assistant](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant) |
| 公開元の構成 | 52層テキスト、3 sliding＋1 full attention、50層vision tower | 5層、16-token block、target_layer_ids=1,13,25,37,49 |
| 公開パラメータ | 正規の[重みindex](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/model.safetensors.index.json)で**29,776,626,688** | Hub説明の**約2,556,000,000**（概数） |
| 一次容量 | indexのtensor payload合計**59,553,253,376 byte**（2 shards、ヘッダ/他ファイル別） | safetensors公開表示**約5.11GB**（正確なファイルbyte未取得） |
| 学習成果 | Meta独自の画像を含むテキスト生成重み | ターゲットに対する別学習の投機ドラフター |
| 採否 | CONDITIONAL研究追加を推奨 | CONDITIONAL研究追加を推奨、ターゲット依存 |

### 重みの内容を根拠にした判断

1. 主モデルの公式[config](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/config.json)には`muse_glimmer`テキスト52層・sliding_window=2048・KV heads=2・視覚tower50層がある。[index](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/model.safetensors.index.json)は2 BF16 shardsと実在のweight mapを示す。単なるモデル名の推定ではない。
2. assistantの公式[config](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant/blob/main/config.json)は`MuseGlimmerAssistantModel`で、16-token DFlash専用の5層が明示される。原本を普通にQ4/GGUF量子化したコピーではない。公式[重みpointer](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant/blob/main/model.safetensors)はSHA256 `fd88d337eb84f8d0e6ba33a7684d7efa6722d4460ba4d6badca9699418392a84`を示す。
3. 主原本2 shardの公開pointer SHA256は`8eef61530e1283642c77ce2e6721feb5c6f348fa055c00e90f2844a136372694`と`b58cc2144ba1ba1af4420f67f4ca3ced7f09298510b80464cc75018a0be14381`。**ローカルSHA再計算ではない。**
4. [Muse Glimmer Usage Policy](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/USAGE_POLICY.md)がApache-2.0タグとは別に存在する。利用行為・親依存・個人権利を未承認のまま「ダウンロード準備完了」としない。runtime config記載は`transformers_version=5.15.0.dev0`であり、同等ABIを確認しない。
5. [Muse-Glimmer-30B-GGUF](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF)は元の重みの別表現であり、別学習成果として追加しない。

**採用差分判断：** 正本にまだ無いことを確認してから2件だけ正式追加。メインモデルとドラフターは独立した学習済み状態として追跡するが、保存時は共有tokenizer・親を別途二重取得しない。既存同族モデルを性能証拠なしに削除しない。

## 2.〈応用・転用例〉— 容量と再現性

現在確認した59.553GBは*原本のtensor payloadサイズ*であり、完成済み保存パッケージのbyte数ではない。計画枠として原本65GB・ドラフター6GBを割当てることはできるが、合計71GBは**容量上限仮置き**であり、実HDD空き・既存重複・全runtime/事前展開・stageの測定前に採用可能と断定しない。

| 変数 | 意味 | SI単位 | 定義 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `B_t` | 元モデルindex tensor payload合計 | byte | 59,553,253,376 | 公開元のindexのみ | 非負整数スカラー |
| `B_m` | 主原本に割当てる暫定保存枠 | byte | 65,000,000,000 | 予算予約で実測ではない | 非負整数スカラー |
| `B_d` | assistant暫定保存枠 | byte | 6,000,000,000 | 予算予約で実測ではない | 非負整数スカラー |
| `B_p` | 両方の暫定合計枠 | byte | `B_m+B_d` | 共通のbyte単位 | 非負整数スカラー |

`B_p=65,000,000,000+6,000,000,000=71,000,000,000 byte`。次元チェックはbyte＋byte＝byte。**実保存サイズではない。**

## 3. 判定ゲートとERROR CHECK

- **H**: Muse主原本と5層DFlashは別学習済み成果であり、既存Qwen/LFMの通常変換重複ではない。
- **T**: 配布元2モデルのconfig/index/weight pointer/license関連を確認（n=2）。後日一つの固定40桁revisionで全選択path・byte・SHAをjoinし、同一HW/backend/context/batchの速度・品質を試験。
- **D**: 学習成果の分類は**PASS（公開元構成証拠）**。最終ファイル選択・機器・権利・オフライン復元は**UNCERTAIN**。二重カウントや異版mixを検出したら最終取得はFAIL。
- **C**: publisherのmodel-indexとpointerが異なるcommit、assistantが特定ターゲット版に適合しない、usage policyをライセンスタグだけで無視する、text/model shardとvision towerを重複取得。
- **U**: 端末実測も全ファイルbyteもないため合成標準不確かさと包含係数`k`は定義しない。

**ERROR CHECK**: この調査ではモデルファイルの取得0、実行0、許可0、計画以外の容量確定0。現行正本が変更された場合は最新revisionへrebaseしてから追加する。

**関連分野**：機械学習アーキテクチャ（画像・言語統合）、デジタル保存（学習成果の重複回避）、ソフトウェア供給網（ファイルSHA/ABI）、ライセンス法（利用条件）。
