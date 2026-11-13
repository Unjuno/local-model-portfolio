# v20追補 — 150B超量子化モデルの「同等RAM」選定（2026-11-06）

## 1. 変更内容

**総パラメータ数150B以上のモデルも、正規の特定量子化版について実行時ピークRAMが150B未満の比較モデル以下なら選定審査に進める。** 150B以上というだけで除外しない。MoEの非活性expert、PLE埋め込み、MTP、独立する学習済み部品は元の総数から除かない。重みファイルの小ささはRAMの証明ではない。

これはv12から存在した量子化例外の**同条件比較基準**を明示する変更であり、v20の追加4レコードで<150Bを条件にした歴史的変換スクリプトの制約を全選定に広げない。**現行154件／有効108件は変えず、既存超150Bの2件はHOLDのまま**。新たな2候補は取得不可の研究台帳にのみ追加する。

## 2. 比較プロトコル

選定前に、**150B未満の有効選定モデルの固定repo/revision**を参照として登録する。候補と参照の両方について、同じ実機または正式に承認されたクラウドのGPU/CPU/RAM、OS・driver、backend commit/ABI、context長、batch、KV形式、代表タスク、コールド/ウォーム条件を合わせて**各30試行以上**で測定する。GPU VRAMとホストRAM、OS、重み、KV、量子化スケール、encoder、vision projector、codec、ドラフトヘッド、処理中の最大使用量を含み、統合メモリの二重計上を避ける。mmap済み大容量ファイルのRSSとプロセスの実効メモリを混同しない。

| 変数 | 意味（日本語） | SI単位 | 定義 | 範囲・測定条件 | 型 |
|---|---|---|---|---|---|
| `P_total` | 大型モデルの元学習済み総パラメータ | 1（無次元個数） | 全expertと必要学習済み部品の和 | 1500億以上、本審査対象 | 整数スカラー |
| `P_ref` | 参照する小型モデルの総パラメータ | 1（無次元個数） | 事前登録の有効モデルの総数 | 0以上1500億未満 | 整数スカラー |
| `M_q` | 量子化大型モデルの実行ピーク | B（情報量のbyte） | OS・RAM・VRAM・KV・全依存・実行領域を含む実測 | 30回以上、同一条件、未測定null | 整数スカラー／欠測 |
| `M_ref` | 参照モデルの実行ピーク | B（情報量のbyte） | `M_q`と同条件で測定 | 30回以上、未測定null | 整数スカラー／欠測 |
| `M_cap` | 絶対推論ピーク上限 | B（情報量のbyte） | 512000000000 | 厳密未満 | 整数スカラー |
| `S_quant` | 量子化ファイル容量 | B（情報量のbyte） | 固定された必要全ファイルのサイズ合計 | 未確定null。RAMではない | 整数スカラー／欠測 |
| `S_archive` | アーカイブ選定上限 | B（情報量のbyte） | 4000000000000 | 実HDD空き・既存ファイル・stagingは別 | 整数スカラー |
| `V_med` | デコード速度中央値 | token/s | 代表30試行以上の速度中央値 | backend/HW/clock/context/batchとセット | 実数スカラー／欠測 |

**厳格判定式：** \(P_{ref}<150\times10^9\)、\(M_q\leq M_{ref}<512\times10^9\,\mathrm{B}\)。両者は同一HW/ソフトと負荷、測定規則で比較する。**次元チェック**：メモリは双方byteで比較できるが、`S_quant`（ディスク保存量）は同じbyte表記でも`M_q`（稼働時使用量）ではない。100GBのGGUFを「100GBのRAMだけで稼働する」とは断定できない。

## 3. 追加4候補の一次資料レビュー

| 調査 | 厳密なrepo ID | 元の全パラメータ（公表/表示概数） | 公表量子化サイズ（RAM実測ではない） | 正の根拠／主要な反証要因 |
|---|---|---:|---:|---|
| 1 | [unsloth/Qwen3.5-397B-A17B-GGUF](https://huggingface.co/unsloth/Qwen3.5-397B-A17B-GGUF) | 名前397B、HFメタデータ約403.4B | Q3約179GB、Q4約214GB | 高性能VL-MoEの別系列。[Unsloth公式ガイド](https://unsloth.ai/docs/models/qwen3.5)はH200上の第三者750題評価を引用。ただし比較対象RAMは未計測、既存モデルとの重複評価も必要 |
| 2 | [orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF) | 約180B | IQ4_XS約97.5GB | 27Bとは異なる編集後重み。Gated許可と上流`other`・派生`apache-2.0`表示の適合性が未確認 |
| 3 | [unsloth/Qwen3-235B-A22B-Instruct-2507-GGUF](https://huggingface.co/unsloth/Qwen3-235B-A22B-Instruct-2507-GGUF) | 約235B | 別配布者bartowskiのQ4_K_Mが約142.65GB（同一ファイルとみなさない） | 旧世代比較は可能だが重複大。今の実測と量子版の機能差が必要 |
| 4 | [unsloth/Mistral-Large-4-1T-A52B-GGUF](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF) | 約1.05T | UD-IQ1_S約233GB | 小さなRAMでSSDストリーミング動作の独立例はあるが、低速度・低ビット品質が重大懸念 |

出典：[Unsloth Qwen3.5公式ガイド](https://unsloth.ai/docs/models/qwen3.5)、[第三者GGUF実験](https://kaitchup.substack.com/p/lessons-from-gguf-evaluations-ternary)、[Orca公式runbook](https://www.orcarouter.ai/blog/qwen3-8-flash-next-uncensored)、[Unsloth Mistralガイド](https://unsloth.ai/docs/models/mistral-large-4)、[Mistral実験生データ](https://huggingface.co/datasets/pratikgx/mistral-large-4-1t-m5-pro-mac-mini-bench)。Mistralの**0.35 token/s・初トークン約150秒**はM5 Pro Mac mini／64GB UMA／SSD offload／llama.cpp `3c809f4`／context 2048／441入力・128出力／n=3に限定された第三者中央値であり、**30試行の合格証拠ではない**。Qwen3.5の約403.4BはHFパラメータ表示値であり、名称397Bとの差を全テンソル計測で解消する必要がある。

## 4. H/T/D/C/U

**H（仮説）：** 150B以上の量子化形式でも、固定した150B未満の基準モデルと同じ環境・ワークロードで同等以下の実測RAMと、必要な品質・速度が成立する。**T（最小検証）：** 入手前に公表総数、版、利用条件を静的に審査。権利・別途実行承認後、同機器／backend／context／batchで30回ずつ実測、中央値速度、p95 TTFT、ピーク使用量を記録。**D（合否）：** PASS＝比較RAM以下かつ512GB未満、品質/速度、ライセンス、独自性、完全なファイル固定と保存枠を満たす。FAIL＝測定超過、速度/品質不足、権利条件不適合。UNCERTAIN＝証拠不足→研究HOLD（**全4件が現状UNCERTAIN**）。**C（対立仮説）：** 低bitが品質を破壊、SSD I/Oで実用速度なし、必要Codec/vision依存でピーク上振れ、比較モデルが不適切。**U（不確かさ）：** RAMの計測境界、CUDA unified memoryの二重計上、mmapページ、モデル改訂・シャード差、データ汚染。誤差分布が未測定なので`u_c`及び係数`k`を根拠なく数値化しない。

**ERROR CHECK：** 既存v20の154件／有効108件、approved 0、4TB上限、物理空き床200GBを不変とする。量子化形式を保存対象化しても元1Tモデル全repoの無条件取得はしない。元重量の学習済み総数は変わらない。HDD接続・取得・モデル実行・有料クラウド契約・Torrentなどは本調査で行わない。
