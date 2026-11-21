# R142: v59正本化と次回取得対象の厳格な段階判定（2026-11-21）

## 1. 目的と事実の範囲

本リポジトリは、モデル能力と学習成果の長期保全を目的とする。人気・「無検閲」タグ・将来規制の憶測だけで重みを取得しない。唯一の正本は `catalog/CURRENT.json`、今回のv59は元のv58・218件の内容を変更せず、3件を研究用 `conditional` に追加した **221登録／174有効／SELECT53＋CONDITIONAL121** である。これらは取得の許可でも、動作品質の実測証明でもない。

正本の追加差分 `catalog/revisions/v59-2026-11-21.json`、静的な出版社source記録 `manifests/drafts/r139-2026-11-21-inkling-micro-edits-and-deepseek4b-varloop.candidate.json`、個別判断 `catalog/decisions/2026-11-21-r141-v59-small-edit-and-ledger76-selection.json` に準拠。新規3repoの論理42ファイル、重複元を排した追加source参照9,347,231,341 byte。これは取得した実ディスク使用量ではない。

## 2. 採用・代替・保留

| 対象と一次配布元 | 判定 | 保存する独立価値・問題点 |
|---|---|---|
| [aaaaygd/DeepSeek-V4-Pro-Qwen3.5-4B-UNCENSORED-heretic](https://huggingface.co/aaaaygd/DeepSeek-V4-Pro-Qwen3.5-4B-UNCENSORED-heretic) | **CONDITIONAL**、BF16＋MTP原本 | 公開原本17ファイル約9.345GB。4,539,265,536学習済み要素（MTP 120,599,552を含む）。9B派生と異なる小型独立重み。作者GSM8K値は別のQ8 GGUF条件であり、BF16・同一HWの再現値ではない。親・蒸留教師・データ権利とMTP/visionコードABI未確認 |
| [satellitedown/Inkling-2-Mini-abliterated-ingine](https://huggingface.co/satellitedown/Inkling-2-Mini-abliterated-ingine) | **CONDITIONAL**、編集パラメータだけ保全 | publisher原本内の親13ファイル約20.192GBはv58 Inkling原本とSHA一致として重複計上しない。選択差分20ファイル・約1.191MB。ただし親が使用者HDDに存在するとは未検証。作者の拒否評価とCUDA/ModelOpt対応は実測・第三者監査なし |
| [OpenUncensored/Inkling-2-Mini-Uncensored-LoRA](https://huggingface.co/OpenUncensored/Inkling-2-Mini-Uncensored-LoRA) | **CONDITIONAL**、別編集方式 | 5ファイル877,939 byteのLoRA（rank2、編集要素215,040）。作者の親固定revision欠落、PEFT `CAUSAL_LM` とInklingのmulti-modal seq2seq実装との整合性未検証。動作できると宣言しない |
| [thinkingmachines/TML-d24-varloop-research](https://huggingface.co/thinkingmachines/TML-d24-varloop-research) | **HOLD**、v59有効一覧には追加しない | 可変1〜5回loopの別研究重み約20.192GB。追加容量に見合う独立用途・性能が未確認。既存[Inkling 2 Mini公式原本](https://huggingface.co/thinkingmachines/Inkling-2-Mini)を無条件に置換しない |

**原本と差分の関係**：原本への同一SHA確認は配布元の静的ファイル照合に限る。実HDDでの親重み一致、ローカル再構成成功、推論互換性を保証しない。ユーザーによる各行為別のライセンス、モデル本体のAUP、上流データの条件をそれぞれ別に確認する。

## 3. 次にダウンロード「候補として準備する」順序

2026-11-21時点の[取得報告台帳を反映した21配布元研究キュー](../../queues/proposed-v59-r140-ledger76-next-21-deduplicated-sources.json)は、既存76モデル／1,078ファイル／約1.658TBの検証**報告**を参照する。今回、owner Windows D媒体の現物を直接re-hashしていない。既存報告は法律上の権利・オフライン復元・今後の取得承認ではない。

| 調査段階 | 配布元 | 公開元source容量 | 判断 |
|---|---:|---:|---|
| P0：低容量・依存先・小型編集 | 9 | 609,360,574 byte | **取得前権利/ハッシュ/HDD審査を最優先**。Dettato4、Mimi、ECAPA、Inkling2種類の編集差分、Phala LoRAを含む。実転送はSTOP |
| P1：小型独立原本 | 7 | 20,727,263,121 byte | Rikiya0.8B、FrostWolf1.7B、Aion2.3B、Heretic4B、音声等。P0完了と個別承認前はSTOP |
| P2：中型の特殊原本 | 4 | 72,927,621,703 byte | Mellum MTP、Spark4B、Heretic9B、Inkling2 Mini親。重複parent hashを検証してから計画 |
| P3：大容量独立研究 | 1 | 129,572,889,973 byte | Ripple65Bは容量・本人環境・性能優位性未確認でHOLD |

P0–P2の公開元参照は計94,264,245,398 byte。**これは次に実行してよい取得量を意味しない**。publisher同一SHAや過去取得報告から即時スキップ・取得済みと断定せず、owner媒体の現物ハッシュを最初に確認する。キュー全体223,837,135,371 byteを一括取得しない。

## 4. 規制・権利・技術の停止条件

**確認済み法的事実**：米BISの2026-11-19発効の[Federal Register 91 FR 74970 §IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は従来のAI Diffusion Ruleのモデル重み向けECCN 4E091を撤廃。一律のローカル所持禁止とは解釈できない。他の輸出先・最終用途管理、出版社利用規約、人物権、個人情報等は別途審査する。

**仮説**：無検閲・安全制御を変更したモデルの公開方針が今後変わる可能性。個別の変更予告・確率は未確認。将来の規制を理由に実権利ゲートを迂回しない。

**非補償型ゲート**： (1) 個人に許された利用行為とGated権限、(2) immutable 40桁source/revision・全必要ファイル・SHA256、(3) 親・tokenizer・MTP・ModelOpt/PEFT・CUDA/ドライバ・Python/backend ABI（安全でないコードは静的監査優先）、(4) 所有者の4TB上限と実HDD最低空き200GB・cache/stagingピーク、(5) 物理保存後のSHAと完全offline restore、(6) `queues/approved.json` の個別明示承認。6条件を全て満たさなければ **ダウンロード不可**。実行環境を持たない現段階では全174有効件がSTOP。

## 5. 反証可能性（H/T/D/C/U）と学際的応用

- **H（仮説）**：SHAが同一の13親ファイルを論理再利用すれば、別編集2件を大規模親の追加取得なしに保存準備できる。
- **T（最小検証）**：出版社42参照ファイルの不変SHA・バイト数の静的照合、v58旧218件の完全一致、v59 sidecar 174件/121件、owner媒体で必要な全SHAの逐次検証。品質測定はWindows GPU/CPU、量子化、context、batch、ドライバ・backend固定の上で別途最低30試行。
- **D（合否）**：静的な選定整合は一致ならPASS、SHA不一致ならFAIL。現物ローカルSHA・利用権・PEFT互換性・実用性能は未測定ゆえUNCERTAIN。取得可否は未承認のためFAIL-CLOSED。
- **C（対立仮説）**：親版やコードABIが異なり差分復元不能、編集方式が実質同等、Heretic4Bが既存の一般小型モデルより劣る。
- **U（不確かさ）**：作者ベンチマークの偏り、親の実物ハッシュ、上流訓練権、転送先容量、一時領域、OS/zero-point/backend差。独立反復測定なしのため合成標準不確かさと包含係数は算出不可。

**関連分野**：機械学習（独立学習成果と性能再現）、ソフトウェアサプライチェーン（SHA/親の再現可能性）、知的財産・輸出管理（配布権と所有行為）、システム工学（HDD/VRAM/RAM/一時容量）。いずれの分野も高順位という理由だけで不足情報を補わない。

## 6. 実行結果の境界

v59の研究採用は3件、旧218件の採否変更0、候補削除0、既存ファイル削除0、`queues/approved.json` 0件。今回の作業で新規モデル重み取得0・未審査モデルコード実行0・ユーザーDドライブ現物ハッシュ確認0。実HDD・権利の未確認状態を成功に書き換えない。
