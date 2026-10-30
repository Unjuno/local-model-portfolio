# 第3次AIモデル選定・規制曝露リスク優先レビュー — 2026-10-30

> **レビュー用・現行未適用。取得/実行/ライセンス同意の承認ではない。** 今回は「分野網羅」を目的から外し、公開停止・Gated化・ライセンス厳格化などに直面しうる固有重みの正規保全に重点を戻した。現行 `catalog/CURRENT.json` は v2（110件追跡・94件有効）。

## 目的と判断の境界

**対象:** 配布元が公開しているモデル・データセットのうち、(a)現にアクセスや利用が制限され、(b)将来さらに条件が変わり得る具体的な能力・制度との接点があり、(c)失うと同等の重みを再現しにくい資産。無制限の人気ランキング、モデルの性能コンテスト、ジャンルの穴埋めではない。

**証拠区分:**
- `fact_access` — Gated、配布停止、用途制限、ライセンス改訂など現在確認できる状態。将来の削除日を意味しない。
- `fact_legal` — 現行法・施行日・行政による具体的規制。特定モデルへの規制が確認できなければ、モデルごとの『規制決定』とは書かない。
- `scenario` — 能力と現行の規制論点からの**反証可能な将来シナリオ**。規制確率は算出しない。
- `recovery_loss` — 学習・専門データ・蒸留・重み編集・ライセンス/再配布制限により、失った場合に独立再現が難しいこと。
- `blocked` — 権利不明、個人情報、必要機材/容量、正確な取得ファイル、revisionなどが未確定。`conditional`も取得承認ではない。

**法令の注意:** EU AI Actの一般目的モデル規則（2025-08-02適用、2026-08-02から関連執行）がある。システミックリスクモデルに安全・報告等の追加義務があるが、公開重み全体の一律禁止ではない。生成物・用途に関する透明性義務をモデル重みの禁止と混同しない（[欧州委員会FAQ](https://digital-strategy.ec.europa.eu/en/faqs/general-purpose-ai-models-ai-act-questions-answers)、[施行FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start)）。

## 今回の追加・条件付き候補（4件）

| 取得条件の調査順 | モデルと出典 | 観測事実 | 固有性と将来シナリオ（推論） | 選定案 |
| --- | --- | --- | --- | --- |
| A1 | [fishaudio/s1-mini](https://huggingface.co/fishaudio/s1-mini) | **Gated**。連絡先共有/同意が必要、HubではCC-BY-NC-SA-4.0。個別モデルとcodecの重みがある | 0.5B音声モデルの独自学習版。話者・音声生成の利用条件厳格化シナリオはあり得るが**禁止予定未確認** | **R0/conditional** |
| A2 | [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3) | 2026-10の新公開原本。付属[`LICENSE`](https://huggingface.co/fishaudio/drama-3/blob/main/LICENSE)はFish Audio Community License、収益・Hosted Service・本人同意に関する制限。HF画面で`fish-audio-research-license`と表示される箇所があり**不一致の調査が必要** | 複数人物の長尺音声・部分編集と反復修正の専門学習価値。音声模倣への制限強化は仮説 | **R0/conditional** |
| A3 | [stabilityai/stable-audio-open-1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) | **Gated**、Stable Audio Communityライセンスと商用別案内 | 効果音/環境音生成のDiT系統。著作物・音源の利用条件変化は研究監視対象だが削除予告はない | **R0/conditional** |
| B1 | [ByteDance/LatentSync-1.6](https://huggingface.co/ByteDance/LatentSync-1.6) | **公開**、Hub表示`openrail++`。公式[実装](https://github.com/bytedance/LatentSync)は1.6を現行チェックポイントと記載 | 顔映像に対応する音声同期・口元編集の専門学習。本人同意のない人物合成・ディープフェイク規制との接点は**利用方法次第**であり、重みの配布規制ではない | **R1/conditional** |

いずれも完全revision SHA、選択ファイルの総バイト数・ファイルSHA-256・実行依存・3/4bitでのRAM測定は未確定。`selected_file_bytes=null`、`download_approved=false`を維持する。

## 前回7件案の修正理由

- **継続**: Stable Audio Open 1.0はGatedと独自ライセンスの観測事実があるため残す。
- **上位選定から外す**: [pyannote Community-1](https://huggingface.co/pyannote/speaker-diarization-community-1)はGatedだが、配布者自身が『無料公開を継続する』趣旨を明記。連絡先登録ゲートと将来公開停止の兆候を混同していたため、規制リスク上位にしない。
- **用途網羅として後回し**: Aurora（気象）、Prithvi（衛星）、SAM2.1（領域分割）、Depth Anything（相対深度）、Boltz-2（分子構造）。研究価値は否定しない。ただし現在の配布制限/規制曝露の強い証拠に欠け、今回の**規制リスク重視**では新規アクティブに追加しない。
- **版の選択を修正**: LatentSyncは配布者が推す1.6を検討し、1.5を無理由に並行保存しない。

## 監視は必要だが採用保留とするもの

| 公式資産 | 懸念・根拠 | なぜ直ちに選定しないか |
| --- | --- | --- |
| [coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2) | 少量の音声から多言語の声を再現、Coqui Public Model License（非商用） | 旧モデルで公開期間が長く、再取得の困難性を優先して証明できない。新しいFish系と重複する |
| [fishaudio/s2-pro](https://huggingface.co/fishaudio/s2-pro) | Fish Audio Research License、商用は別契約 | Drama3より古い同系列として差別化と権利本文を調査 |
| [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3) | 2.78T級、自律エージェント、[公式LICENSE](https://github.com/MoonshotAI/Kimi-K3/blob/main/LICENSE)に一定規模のMaaS別契約 | **3–4bitでも全パラメータ重みだけで512GB超**。現行のハード上限を満たせない。将来容量/実機方針を変える場合のみ再審査 |
| [Qwen/Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) | 2.446T級、[公式LICENSE](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/blob/main/LICENSE)に一定規模のMaaS等の別契約要件 | 同様に3–4bitの重みだけで512GB超。現行の取得承認対象ではなく**規制・ライセンス推移のみ監視** |

なお[HFの2026年夏季調査](https://huggingface.co/blog/state-of-open-models-summer-2026)は、大型モデルの公開ライセンスが一律に緩いわけではなく、Kimi・Qwenの特定大型版に商業条件が付く事例を記録している。**市場のライセンス条件**と**政府の配布禁止**は別々に管理する。

## 現行v2から先に再調査する資産（未再検証の台帳記載を含む）

| 調査順 | v2の既存資産 | 主な確認課題 |
| --- | --- | --- |
| I | [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | 台帳ではGated、元版との差分とライセンス・供給変化を確認。研究目的の隔離が必要 |
| I | [meta-llama/Llama-4-Scout-17B-16E](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E) | 台帳ではGated、独自ライセンスと比較原本を固定 |
| I | [black-forest-labs/flux-3-image-klein-base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base)、[FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | Gated・独自条件。Base/蒸留/系列重複を区別して原本選択 |
| I | [briaai/Fibo-2.0-dev](https://huggingface.co/briaai/Fibo-2.0-dev) | 現時点Gated（2026-10確認）、独立画像系列と利用条件 |
| II | [CohereLabs/aya-vision-32b](https://huggingface.co/CohereLabs/aya-vision-32b) | 台帳ではGated/非商用、多言語VLMの配布契約 |
| II | [nvidia/Cosmos-Predict2-2B-Video2World](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World) | 台帳ではGated。動画から世界状態を予測する重みの独自性と権利 |
| II | [google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it)、[EPFLiGHT/Meditron3-70B](https://huggingface.co/EPFLiGHT/Meditron3-70B) | 台帳ではGated。医療モデルの専門学習・利用条件、外部データ権利 |

この表は**新たな削除予定の発表ではない**。v2の記録を再監査する優先調査順であり、法令・提供者の変更履歴を確認するまで推測に留まる。

## H/T/D/C/U — 選定の反証可能性と承認ゲート

- **H（仮説）:** 2026-10-30の初回記録を基準に、各候補の公開条件に将来の追加制限が生じる可能性がある。『規制される確率が高い』等の数値は根拠がないため付さない。以後30日単位または配布元の変更発表ごとに状態変化を確認する。
- **T（最小検証）:** 候補ごとに(1)公式モデルカード (2)同じ版のLICENSE全文 (3)ファイル一覧と完全コミット (4)コード/依存 (5)現行v2との重複 (6)当該用途に適用されうる公式法令資料を確認する。`n_min=1`は各種類の一次資料の最低確認数を意味し、性能ベンチマークの標本数ではない。矛盾する資料があれば解決まで停止。
- **D（判定）:** `PASS`=固有の保存理由と直接リンク、現実の制限または明示した具体的シナリオ、最低限の権利情報が揃う**選定**。`FAIL`=IDが存在しない/無権限/完全重複/目的不適合。`UNCERTAIN`=契約矛盾・許諾不明・容量未確定。PASSは**取得承認ではない**。
- **C（対立仮説）:** Gatedは宣伝・連絡先収集のみで提供継続、ライセンス制限は以前から同じ、あるいは規制は運用主体への義務で公開ウェイトには影響しない。事例があればランキングを降格する。
- **U（不確かさ）:** 主因は将来の政策変更、モデルカードの更新遅延、ライセンス解釈、実際の利用目的、配布元revision、重み形式/依存/ROM・RAM。現状は統計量が定義できず、合成標準不確かさ `u_c` と包含係数 `k` を数値化できない。根拠のない確率推定で代用しない。

## 保存・実行境界

- `catalog/CURRENT.json`、`queues/approved.json`、HDDおよび実機設定は**変更しない**。モデル重みをダウンロードしない。
- 採用であっても権利・同意・ファイル選択・ピン留めコミット・正確なバイト数・SHA-256・依存・推論環境を別途確定し、ユーザーのマニフェスト承認後にのみ保存可能。
- `.pt`/`.pth`/`.ckpt`や未知のコードを**ダウンロードしただけで自動実行しない**。個人の声・顔の利用は本人同意と適用法を別途確認。制限回避、無断取得は行わない。
- 保存予算は**3.8 TB（十進）**、最低空き**200 GB**、3–4bit下でのピークRAM**512 GB未満**。ハード条件を満たさない大型モデルは規制ウォッチに留める。公開表示容量を取得ファイル容量と混同しない。

このレビューを別ブランチのドラフトPRに保持し、権利と正規取得可能性を確認した候補から順に正本への反映を検討する。
