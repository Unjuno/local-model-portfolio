# P0の22資産：配布元メタデータ再照合（2026-11-03）

基準コミット：`6e9389c97d24528df97e4b14a6bc772780141fd3`。元提案：[132件のJSON](../../catalog/proposals/01-regulation-priority.json)。Hugging Faceの配布元詳細を22件確認。**重み・データ本体・依存・コードは取得・実行していない**。

## 観測

モデル12件、データ10件。Gated13件、Public9件。Hubの表示は**本人のGated取得承認ではない**。ライセンスラベルは適用本文の審査ではない。独自能力は未ベンチマーク、同一SHAの合法ミラーは未検証。

| 調査順位 | repo ID・一次URL | 種別 | Hubアクセス | ライセンス/総数の表示（判明分） | 未解決・最初の検証 |
|---:|---|---|---|---|---|
| 1 | [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | モデル | gated | apache-2.0 | 権利本文・依存・固有性・選択容量が未確認 |
| 2 | [`StephaneBah/AfroRadVoice-FR`](https://huggingface.co/datasets/StephaneBah/AfroRadVoice-FR) | データ | gated | cc-by-4.0 | 権利本文・依存・固有性・選択容量が未確認 |
| 3 | [`amphion/Emilia-Dataset`](https://huggingface.co/datasets/amphion/Emilia-Dataset) | データ | gated | cc-by-4.0 (Hub) | Hub CC BY 4.0表示と原版CC BY-NC 4.0記述の適用範囲が未解決 |
| 4 | [`bigcode/the-stack-v2`](https://huggingface.co/datasets/bigcode/the-stack-v2) | データ | gated | other | opt-outとバルク取得の契約・権利を先に審査 |
| 5 | [`laion/relaion2B-en-research`](https://huggingface.co/datasets/laion/relaion2B-en-research) | データ | gated | cc-by-4.0 | 権利本文・依存・固有性・選択容量が未確認 |
| 6 | [`lmsys/lmsys-chat-1m`](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | データ | gated | unknown | 実ユーザー会話の同意・個人情報を優先 |
| 7 | [`bigcode/starcoderdata`](https://huggingface.co/datasets/bigcode/starcoderdata) | データ | gated | other | 権利本文・依存・固有性・選択容量が未確認 |
| 8 | [`KlingTeam/LivePortrait`](https://huggingface.co/KlingTeam/LivePortrait) | モデル | public | mit | 権利本文・依存・固有性・選択容量が未確認 |
| 9 | [`microsoft/Fara1.5-27B`](https://huggingface.co/microsoft/Fara1.5-27B) | モデル | public | mit; Hub 27356.7M | 権利本文・依存・固有性・選択容量が未確認 |
| 10 | [`Plachta/Seed-VC`](https://huggingface.co/Plachta/Seed-VC) | モデル | public | gpl-3.0; 総数未表示 | Hub総数未表示：全学習済み構成の静的計数まで取得準備停止 |
| 11 | [`Qwen/Qwen3-Coder-Next`](https://huggingface.co/Qwen/Qwen3-Coder-Next) | モデル | public | apache-2.0; Hub 79674.4M | 権利本文・依存・固有性・選択容量が未確認 |
| 12 | [`Qwen/Qwen3-TTS-12Hz-1.7B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | モデル | public | apache-2.0; Hub 1928.7M | Hub表示約1,928.7M。名称1.7Bとの差は全構成確認対象 |
| 13 | [`HuggingFaceFW/fineweb-edu`](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | データ | public | odc-by | 権利本文・依存・固有性・選択容量が未確認 |
| 14 | [`allenai/WildChat-1M`](https://huggingface.co/datasets/allenai/WildChat-1M) | データ | public | odc-by | ハッシュIP・リクエストヘッダー等のプライバシーを審査 |
| 15 | [`laion/emotional-roleplay-finetuning-dataset`](https://huggingface.co/datasets/laion/emotional-roleplay-finetuning-dataset) | データ | public | cc-by-4.0 | 権利本文・依存・固有性・選択容量が未確認 |
| 16 | [`nvidia/Granary-v2`](https://huggingface.co/datasets/nvidia/Granary-v2) | データ | public | openmdw-1.1 / cc-by-sa-4.0 | Hubにopenmdw-1.1とcc-by-sa-4.0の複数タグ |
| 17 | [`black-forest-labs/FLUX.2-dev`](https://huggingface.co/black-forest-labs/FLUX.2-dev) | モデル | gated | other; Hub 32223.3M | Gated、独自ライセンス、上流全repo約177.6GB |
| 18 | [`EPFLiGHT/Meditron3-70B`](https://huggingface.co/EPFLiGHT/Meditron3-70B) | モデル | gated | llama3.1; Hub 70553.7M | Llama 3.1派生元条件と本人Gated承認を検証 |
| 19 | [`google/medgemma-4b-it`](https://huggingface.co/google/medgemma-4b-it) | モデル | gated | other; Hub 4300.1M | 権利本文・依存・固有性・選択容量が未確認 |
| 20 | [`facebook/dinov3-vit7b16-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vit7b16-pretrain-lvd1689m) | モデル | gated | other; Hub 6716.0M | 権利本文・依存・固有性・選択容量が未確認 |
| 21 | [`facebook/dinov3-vith16plus-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m) | モデル | gated | other; Hub 840.6M | Idol等の依存候補。異サイズDINOは同一重みのミラーではない |
| 22 | [`facebook/sam3`](https://huggingface.co/facebook/sam3) | モデル | gated | other; Hub 859.9M | 権利本文・依存・固有性・選択容量が未確認 |

## 取得準備の停止ゲート

- `Plachta/Seed-VC` は総パラメータ未確認。静的な全構成計数以外の取得準備を禁止。
- **150B以上は絶対除外**。MoEは活性数でなく非活性エキスパート等を含む総数。量子化やオフロードで閾値を緩和しない。
- Gated13件は本人の権限、契約、派生元のライセンス、依存を別々に審査。HOLDのデータは権利・再選定だけを行う。
- Public9件も権利本文、固定revision、選択ファイル容量、独立の同一SHAミラー、比較ベンチマークを未確認。保存優先度は取得許可ではない。
- 特にEmiliaのライセンス適用版差、The Stack v2のopt-out、WildChatの個人情報、Qwen3-TTSの名称1.7BとHub表示約1.929Bの差を先に確認する。

## H / T / D / C / U

**H**：2026-11-03〜2026-12-03に22件のうち少なくとも1件で権利・依存・本人アクセス上の追加障害が一次資料で確認される。確率は推定しない。

**T**：n_min=22。全件のカード・適用契約本文・固定revision・依存を非実行で確認し、本人のアクセス権限は本人が提示した場合のみ判断。モデル/データ本体は取得しない。

**D**：一次URLと日付を伴う障害確認なら当該件PASS、全件完全確認で障害なしなら期間限定FAIL、欠測はUNCERTAIN。いずれも取得承認を意味しない。

**C**：Hubタグと本文の版差、地域・アカウント差、配布者の自主的変更、機能代替を同一重みと誤認する場合。

**U**：未固定revision、本人の権限、全構成の総数、権利本文、同一SHAミラー、選択容量。確率分布がないため合成標準不確かさu_cと係数kは定量化しない。

## ERROR CHECK

P0は一意の22件（モデル12、データ10、Gated13、Public9）。全件でライセンス本文・固定マニフェスト・本人の取得許可・ダウンロード承認は未完了。元のv9・提案JSON・承認キューは変更しない。

**次に考える問い**：同じ容量なら、再取得不能な独自原本と、正規ミラーがある高性能原本のどちらを先に保存候補へ昇格させるべきか。
