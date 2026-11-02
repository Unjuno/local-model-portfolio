# 第4回モデル選定レビュー — 2026-10-31

> **45件の予備審査と対象を絞った一次資料確認。取得・実行の承認ではない。** 本文と [45件の判定台帳](../catalog/reviews/round4-2026-10-31.json) が、このラウンドで審査したIDに関する最新のドラフト判断です。過去のv3文書を履歴として残します。`catalog/CURRENT.json` はv2のままです。

## 1. 今回の結果

| 判定 | 件数 | 意味 |
| --- | ---: | --- |
| 新規の条件付き候補 | 6 | 正本110件に含まれない追加案。大型2件は容量競合する代替案 |
| 前回v3案を継続 | 5 | 前回6件のうちGenpioを除く |
| 既存候補の調査優先度を引き上げ | 1 | VibeVoice-1.5B。実際のコード撤去履歴あり |
| 既存の条件付き候補を維持 | 3 | 元版との差・Gated・独自系列を再確認 |
| その他の既存候補を維持 | 3 | 比較原本又は契約再確認を伴う維持 |
| 保留 | 9 | 許諾目的、依存、原本性、実機構成の問題を先に解決 |
| 監視・今回は追加しない | 17 | 研究価値と公開制限の証拠は別。重複・低緊急性を再評価 |
| 比較資料のみ | 1 | Pocket TTSの機能制限版 |
| **合計** | **45** | 重複IDなし |

45件すべての重み・コード・性能を監査したという意味ではありません。Hugging Face連携での配布メタデータ照会に、公式モデルカード、ライセンス、公開履歴を重ねました。モデル本体は取得せず、推論も行っていません。

**優先軸は変えません。** 将来の規制・Gated化・配布条件変更に備え、独自学習成果を正規に保存する価値を評価します。ただし今回、特定モデルの将来の政府による配布禁止は確認していません。現在の契約制限を、将来の禁止予定や数値確率に置き換えません。

## 2. 今回新たに残した6候補

### PersonaPlex — 音声対話の独立した完成重み

[nvidia/personaplex-7b-v1](https://huggingface.co/nvidia/personaplex-7b-v1) は、聞くことと話すことを同時に扱う全二重の音声対話モデルです。通常のTTS・ASRと同一機能ではありません。

観測した制限はGatedと [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/) です。**この契約は商用利用を認めています。** 非商用専用とは書きません。一方で法令対応の契約更新条項や個別部品の条件があるため、将来も無条件の権利が保証されるとは扱いません。

選定案：条件付き。Mimi codec、tokenizer、音声素材、PyTorch等の実装を含む一式の許諾と容量を確認します。Hubの表示上、主重み16.7GB、codec385MBですが、これは丸められた表示で、取得ファイル合計の確定値ではありません。

### MedGemma 1.5 — 既存1.0から区別すべき医療画像・文書の後学習

[google/medgemma-1.5-4b-it](https://huggingface.co/google/medgemma-1.5-4b-it) はCT/MRI、病理スライド、経時画像、医療文書等への対応を公式カードが説明しています。既存のMedGemma 1とは別の完成重みとして比較保存する価値があります。

Gatedで、[HAI-DEF利用条件](https://developers.google.com/health-ai-developer-foundations/terms) が適用されます。コードのApache-2.0を重みの許諾と混同しません。臨床利用の適否・必要な承認は別です。**新しい版が全評価課題で一律に優れるとは判断しません。** 共通画像encoderの重複と専用前処理を確認します。

### TxGemma Predict — 一般医療対話とは別の予測用重み

[google/txgemma-9b-predict](https://huggingface.co/google/txgemma-9b-predict) は治療開発関連の予測課題向けの追加学習版です。条件付きで基礎研究用の候補とします。predictとchatの全サイズを無条件で併存させません。

HAI-DEF条件とタスク定義用ファイル等を含めて確認します。**カードはF32重みと表示しているため、名称の9BからBF16保存容量を決めつけません。** 性能・研究上の有用性は独立実測前です。

### HunyuanVideo 1.5 — 現実の地域・用途条件を持つ動画系列

[tencent/HunyuanVideo-1.5](https://huggingface.co/tencent/HunyuanVideo-1.5) の [公式LICENSE](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/LICENSE) はEU・英国・韓国を許諾地域から除外し、他AIモデルの改善への利用にも制約を設けています。これは配布者の契約条件であり、その地域の政府がこの重みを禁止した証拠ではありません。

条件付き候補として、利用地域と目的に適合する代表checkpoint一つから審査します。研究・生成・同系列の微調整と、他系列モデルの学習資材にすることは同一ではありません。旧NOTICEの別版ライセンスを現在のLICENSEと取り違えないことも必要です。

### Devstral 2 と Qwen Flash Next — 大型モデル枠の代替案

[mistralai/Devstral-2-123B-Instruct-2512](https://huggingface.co/mistralai/Devstral-2-123B-Instruct-2512) は [Modified MIT](https://huggingface.co/mistralai/Devstral-2-123B-Instruct-2512/blob/main/LICENSE) です。会社又は雇用主の売上規模による別許諾条件があり、通常MITではありません。公開されたFP8表現と、既存Devstral Small 2の後学習の違いを確認します。

[Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) は [独自Community License](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/LICENSE) を持ち、MaaS/AI Work Assistant等の商用条件と内部利用の例外があります。既存Qwen3.8-27BのApache-2.0をこのモデルへ横滑りさせません。

**この2件を同時に取得対象へ昇格させる判断はしていません。** 既存119件の初期レビューに名前がある場合も、現行110件への採用とは別です。両者を大型枠の代替案として比較し、正確な原本サイズ・依存・実行器・ピークRAMを測定条件付きで固定してから絞ります。ユーザーに直ちに売上条件が適用されるとも、将来削除されるとも推定しません。

## 3. 新規追加より重要だった既存VibeVoiceの再評価

[MicrosoftのREADME](https://github.com/microsoft/VibeVoice/blob/main/README.md) は、**2025-09-05に想定外の利用を理由としてVibeVoice-TTSコードを撤去した**と明記しています。これは単なる規制予測より強い、提供者による実際の変更履歴です。

ただし、**1.5B重みが削除された、全VibeVoiceが停止した、とは言っていません。** 現在も1.5Bの公式配布ページがあり、後発のRealtime-0.5B等もあります。既存 `microsoft/VibeVoice-1.5B` の調査優先度だけを引き上げ、重複登録しません。

今回、[別の観測記録](../catalog/snapshots/2026-10-31-vibevoice-metadata-review.json) に以下を記録しました。

- 公開ページで観測した完全commit `c00898d257e6b46004e3e2866a47534085fb685a`。
- 3つのsafetensorsシャードの配布元表示SHA-256。Xet識別子とは区別。
- exact byte数・依存関係・固定commitでの全ファイル照合は未完了。

これはマニフェストでもローカルハッシュ照合結果でもありません。公開ページにはキャッシュがあり得るため、取得前に現行の正規メタデータと全ファイルを再照合します。権利の確認できないコードや制限を迂回した取得は行いません。

## 4. 降格・保留の判断

| 資産 | 今回の判断と理由 |
| --- | --- |
| [Genpio Voices](https://huggingface.co/GuidenAI/genpio_voice) | 前回v3の条件付き候補から保留へ。配布者は承認がread accessのみであると説明し、研究保存・再利用の範囲が不十分。独自学習や品質も配布者主張の段階 |
| [EXAONE 4.0 32B](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-32B/blob/main/LICENSE) | 内部解析等の制限と終了時のアーカイブ削除条項を確認。長期保全という目的と両立する許諾範囲を確認するまで保留 |
| [SAM Audio](https://github.com/facebookresearch/sam-audio/blob/main/LICENSE)、[SAM 3D Objects](https://github.com/facebookresearch/sam-3d-objects/blob/main/LICENSE)、[SAM 3D Body](https://github.com/facebookresearch/sam-3d-body/blob/main/LICENSE) | 内部構成の探索等に関する契約条件を確認。推論利用と内部解析を区別し、後者を含む目的への適合確認を優先。研究利用全般が禁止だとは断定しない |
| [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3) | 特殊な商用条件と巨大な原本の容量・実装条件を別々に評価。総パラメータ数だけを根拠にRAM不適合とはしないが、保存構成が未確定なので保留 |
| [InfiniteYou](https://huggingface.co/ByteDance/InfiniteYou)、[InstantID](https://huggingface.co/InstantX/InstantID)、[LivePortrait](https://huggingface.co/KlingTeam/LivePortrait) | 自モデルのライセンスを全依存物の許諾と取り違えない。ベース重みや顔処理などの依存・用途・同意確認が未完了 |

終了・削除条項を持つのはEXAONEだけではありません。他の独自契約にも適用条件があります。今回の保留は、条項の存在を一律に禁止と解釈したためでなく、**目的との衝突や許諾範囲の未解決が重大なものを止める**判断です。契約適合性は必要に応じて専門家の確認を要します。

## 5. 監視に留めた17件と比較資料

GLM-5.3-Flash、Command R+、Command A、Aya Expanse、Falcon H1、Step-Audio、VibeVoice-Realtime、Apple SHARP、Wan Animate、Wan S2V、InfiniteTalk、MedSigLIP、ESM3、Evo2、Stable Diffusion 3.5、Stable Video Diffusion、Cosmos 2.5は、今回新規採用へ昇格させません。理由と正確なIDは45件台帳に個別記録しています。

特に [biohub/esm3-sm-open-v1](https://huggingface.co/biohub/esm3-sm-open-v1) の現在のカードはMITを示しています。過去の名称や条件から、現在も非商用・Gatedと断定するのは誤りです。生物学分野というだけで規制予定を作りません。

Pocket TTSの機能制限版は比較資料です。作者のゼロ化スクリプトは原本との差を示しますが、**全世界の合法な代替配布先まで不存在と証明したわけではありません。** 公開版しか残らなければ必ず全機能が永久に失われる、といった過剰な断定は避けます。

## 6. 既存提案への適用方法

- 本ラウンドは**ドラフトの判断**です。対象IDの選定理由と優先度については本レビューが旧v3の判断を更新しますが、正本110件は変更しません。
- 旧v3の6候補は5件継続、Genpio1件を保留としました。今回の6候補は別の追加案です。追加案11件全部の同時保存を確定したわけではありません。
- `catalog/CURRENT.json`、`queues/approved.json`、既存原本台帳と取得マニフェストを変更しません。旧判断は履歴として削除しません。
- 次のマニフェスト案は、既存VibeVoiceの原本・正規実行資材の確認、Pocket TTSの条件、PersonaPlexの依存、医療系のファイル重複、大型2候補の容量比較の順に作成するのが妥当です。これは自動取得の指示ではありません。

## 7. 検証ゲートと不確かさ

| 区分 | このラウンドの基準 |
| --- | --- |
| H：検証対象 | 制限や提供変更の観測事実があり、失うと別モデルから単純に作り直せない学習成果を優先する、という選定上の仮説 |
| T：最小確認 | 個別の正規ID・配布ページに加え、上位候補ではLICENSEと変更履歴を確認。各種類で最低1件の一次資料を目標にし、未取得は明記。実行試験の標本数とは別 |
| D：合否 | 選定根拠が揃えば候補継続。権利目的に重大な不一致があれば保留。保存承認は全件未成立で、取得・実行フラグをfalseに維持 |
| C：反証 | Gatedが単なる連絡先登録、合法な同一原本が安定配布、想定する規制が用途だけを対象とする場合は緊急度を下げる |
| U：未確定 | 将来の提供方針、契約解釈、ミラー同一性、キャッシュ鮮度、依存容量、backend/量子化/バッチ/コンテキスト/KVによるRAM。統計モデルなしに確率や合成誤差を創作しない |

保存上限は3,800,000,000,000バイト、最低空き200,000,000,000バイト、ピーク推論RAMは512,000,000,000バイト未満です。今回は新候補の選択ファイル量と実機ピークを確定していません。上流全repoの丸めた表示を足して『3.8TB内』と結論しません。モデル名の1.5B/7B等と全構成のサイズも同一視しません。

**関連分野**：契約・AIガバナンスは保存権と利用権を分離し、機械学習の再現性は原本・派生・後学習を区別し、ストレージ設計とセキュリティは完全性・依存・安全な隔離を扱います。この3つが揃うまで保存完了とは呼びません。

## ERROR CHECK

45行のID重複、判定別件数、直接リンク、参照キー、未承認フラグ、SHA表記を検査する対象としました。モデルの実行・品質測定・実ファイル照合は未実施。Gated同意、ダウンロード、インストール、HDD操作、PRのマージは行いません。
