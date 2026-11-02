# 保存戦略 v5：規制の連鎖シナリオから優先順位を決める（2026-11-03）

**目的：**「まず悪用しやすい高能力・合成・権利リスクの重みが対象化され、その後高性能AI一般へ、最後にオープンウェイト全体へ制限が広がる」というユーザー指定の損失シナリオに対し、**合法的に現在保全可能な情報を失うリスクを先に下げる**。これは実際の規制日程や確率の予報ではなく、**仮定に基づく判断規則**。

- 正本：[catalog/CURRENT.json](../catalog/CURRENT.json)
- [132件の予測順位付き現行ビュー](../catalog/effective-portfolio-2026-11-03-v5.json)
- [優先順位だけを変更するv5差分](../catalog/revisions/v5-2026-11-03.json)
- [S1→S2→S3を反映した調査作業表](../queues/proposed-v5-2026-11-03.json)
- [予測と現行法・権利条件を分離する規則](../policies/capability-access-risk.md)

## 変更前との違い

これまでのR0は**「現在Gatedなどの制限がある」優先区分**に近かった。v5では、**想定する将来の制限段階を第一の選定順**とし、現行アクセス状態は「今どう調達できるか」の実行ゲートに移した。R0/R1/R2の履歴は保持するが、取得準備順の正本にはしない。従来の小型Qwen・OCR・Whisperの3件は**ダウンローダーの試験候補**であり、予防保存順位の上位3件ではない。

## 予測段階別の分類（全132件）

| 想定段階 | 有効選定 | 延期/保留 | 計 | 予測メカニズム |
| --- | ---: | ---: | ---: | --- |
| S1 先行的な標的制限 | 27 | 18 | 45 | 拒否制御変更、行動エージェント、本人同一性を使う顔/声合成、高度画像/動画生成、権利・個人情報を含み得るデータ |
| S2 高性能一般への拡張 | 39 | 5 | 44 | 高性能汎用LLMとOmni、医療・科学、ロボット・世界モデル、専門データ |
| S3 オープンウェイト全般 | 39 | 4 | 43 | Base、軽量比較モデル、一般基盤・評価データ・実装依存 |
| **計** | **105** | **27** | **132** | |

**重要：** S1の45件が現実に危険・禁止・将来規制対象となるという意味ではない。カテゴリーと理由を照合可能な仮説として保存。元重みの能力・悪用可能性は、独立測定なしに事実化しない。

## S1の最初の有効選定18件（調査優先、取得許可ではない）

| 調査順位 | 配布元 | 観測された現行アクセス | 今行う調査 |
| ---: | --- | --- | --- |
| 1 | [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | gated | 利用者本人による正規の許諾、契約、固定ファイルを確認 |
| 3 | [dphn/Dolphin3.0-Llama3.1-8B](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 5 | [LiquidAI/LFM2.5-24B-A2B](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 6 | [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 7 | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 8 | [tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 9 | [InstantX/InstantID](https://huggingface.co/InstantX/InstantID) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 10 | [KlingTeam/LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 11 | [microsoft/VibeVoice-1.5B](https://huggingface.co/microsoft/VibeVoice-1.5B) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 12 | [OpenMOSS-Team/MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 13 | [Plachta/Seed-VC](https://huggingface.co/Plachta/Seed-VC) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 14 | [Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 15 | [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 16 | [Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 17 | [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 18 | [SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS) | public | 権利本文、ファイル固定、重複・依存を確認 |
| 25 | [black-forest-labs/flux-3-image-klein-base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | gated | 利用者本人による正規の許諾、契約、固定ファイルを確認 |
| 26 | [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) | gated | 利用者本人による正規の許諾、契約、固定ファイルを確認 |

### S1でもHOLD/BACKLOGに留めた18件

法的・安全上の問題や権利不明を理由に延期/保留にしたものは、**規制リスク上の調査順位は上げるが、選定や取得権限は自動的に変えない**。無検閲派生・音声声質変換・人物生成・コード/実対話/音声データのうち、原本の権利と同意が不明なものを含む。どの理由で保留されているかは機械可読の作業表で追跡。

## 判定根拠の一次資料

1. [米NTIA 2024年報告書](https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations/recommendations)：能力・リスク指標を監視し、証拠が整えば重みへのアクセス制限等も検討する政策上の選択肢を提示。これは制限が決定したことを意味しない。
2. [Hugging Face Gatedモデル公式文書](https://huggingface.co/docs/hub/models-gated)：Gatedモデルの許可は配布者が変更・撤回できる。個々の許諾は利用者本人の手続き。
3. [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026)：オープンウェイトは再配布の不可逆性と安全対策変更の容易さという異なる難点を持つ。
4. [EU AI Act 第55条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-55)：一部GPAIモデルのシステミックリスクに追加義務。すべての高性能モデルの一律禁止とは異なる。

## 保存・法的停止条件

- モデル・datasetの各URL、正確なrepo ID、バージョン・配布者の利用権限・親依存・選択ファイル容量とSHA-256を確定する。
- 未承認のGated/Private、モデル契約違反、無同意の顔/声・個人データ、私的データの無断取得を行わない。
- 全132件に予測区分はあるが、**download_approved=false、queues/approved.jsonは空**。新規の制限観測は優先順位・契約確認の見直しの引き金であって、自動ダウンロードのトリガーではない。
- 3.8TBは論理的上限。ユーザー申告の実際の約3.8TBと物理容量・200GB空き条件の整合は未確定。作業領域も含めて検証する。
- あらかじめ公開される評価/倫理資料、コード、tokenizer、音声Codec、画像Encoder等もS3までに欠かさず確保する方針。ただし「すべて保存できる」とは断定しない。

## H / T / D / C / U

- **H**：2026-11-03〜2027-11-03に**新規に観測される**配布権限の狭まりがS1群で先行し、S2、S3へ広がる。この仮説はモデルの性能ではなく、配布者/政策の行動に対する仮定。全群を同じ頻度で監視する。
- **T**：132件全件を同じ週次間隔で状態確認し、最低12週間にわたり公式Hub/API・ライセンス・配布元告知・公的規則を記録。毎回の対象はn=132、各状態変更は変更前後の時刻とURLを保存。観測期間が短い場合は中間報告のみ。
- **D**：PASS＝各波を独立した複数の配布者で順序通り観測し、出典と時点を示せる。FAIL＝S2/S3が先行または一律同時制限となりS1先行仮説を否定。UNCERTAIN＝制限が少数・出典欠落・発生なし/期間不足で順位を検証不能。**現状UNCERTAIN**。
- **C**：規制ではなく商用契約・収益・データ権利が原因である、またはどの群も公開し続ける、あるいは全面規制が一度に起きる可能性がある。
- **U**：配布理由の不透明さ、国/配布元ごとの制度差、サンプル選択、観測間隔、政策反転が主要不確実性。モデルに基づく実測確率も合成標準不確かさ`u_c`も推定できず、`k`は未適用。

**結論：** このv5によって、将来制限の**予測シナリオが管理する優先順位の第1軸**になった。禁止を既成事実化することでも、Gated制限の回避でもない。
