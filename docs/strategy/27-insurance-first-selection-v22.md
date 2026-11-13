# v22 — 学習成果を失わないための保険（2026-11-06）

## 1. 目的と今回の変更

公開配布経路が広く失われた場合に備え、価値ある学習成果と、その成果を再利用する部品を保全する。**何を残すかは学習成果の価値、何から先に確保するかは先行制限シナリオと現在の配布状態で決める。** 規制の確証や直近の削除予告を待つ計画ではなく、日常利用で最速のモデルだけを選ぶ計画でもない。全面的な配布消失が確定した、という事実主張はしない。

v21の159資産を変更せず、既存R19/R20調査から4件をconditionalの保全選定に移す。**v22は163資産／有効116件**。全件の準備表を段階別に生成する。4TBの選定枠、実空き200GB、150B以上の量子化同等RAM条件は維持。今回もモデルのダウンロード・クラウド課金・実行は行わない。

## 2. 正式に追加する学習成果

全件の確認日：2026-11-06。Hugging Face connectorで存在・メタデータを再確認し、Exaと一次ページを既存研究台帳と比較した。公開表示は本人への全利用許諾の確認ではない。

| repo ID／一次URL | なぜ失いたくないか | 現在の制限と予測の区分 | 採用範囲・計画枠 | 反証条件・未解決事項 |
|---|---|---|---|---|
| [DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | 拒否制御の編集後に複数段階tuningをした別checkpoint。親Qwenと同じ系列でも同じ学習成果ではない | 公開・Apacheタグ。削除予告未確認。S1は先行制限の仮説 | release-1公開元原本を1系統、**70GB枠**。NEO/CODERや全量子化形式へ自動拡張しない | 独立再実験・汚染検証なし。donor条件、MTP/vision、固定版の範囲を確認。単なる同一重み別名なら再審査 |
| [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3) | 複数話者、音声の履歴条件付き編集、Codebook-MTPの学習成果 | 公開元のFish Audio Community License。停止予告未確認。声の本人同一性への配布見直しは仮説 | 公開元FP8 experts＋BF16重み、**60GB枠**。INT4を別能力として二重採用しない | codec等を含む完全総数未確定、**研究専用conditional**。利用条件、全部品、品質、実機は別に確認 |
| [PrentisAI/GroundGUI-8B](https://huggingface.co/PrentisAI/GroundGUI-8B) | 画面内の要素を定位する専用学習、system promptとscoring。Holo4/Fara全体agentとは役割が異なる | 公開・Apache。ScreenRefデータは別条件。先行制限は仮説 | 公開checkpoint＋prompt・processor等、**25GB枠** | box命中率を長期タスク成功率に言い換えない。画像・データの許諾を重み許諾から推定しない |
| [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | 編集時の構図ずれを抑える独立のrank32学習差分。小さな差分でも学習成果は原本から自動再生できない | 親条件等を別審査。個別の早期規制証拠は未確認だが、保険の対象外にはしない | step1500差分を1つ、**増分1GB枠**。step2000は同時採用しない | 姿勢変更を阻害しうる。base/encoder/VAEを含む全総数未集計で**研究専用conditional**。同一SHAの基盤再利用が証明されるまで容量節約を計上しない |

4件合計の計画枠は**156,000,000,000 byte**。これは実ファイルの測定合計ではなく停止境界である。全ポートフォリオの選択ファイル合計と実空きは未確定なので、4TB以内に収まったとは記録しない。

## 3. 原本・量子化版・付属部品の保存方針

Drama3は省容量だけならINT4もあるが、今回は公開元のFP8/BF16版を保険の代表にする。公開元版でも元学習時の全BF16情報が復元できるとは主張しない。INT4版は実行形式の代替候補に留め、両方を無条件に保存しない。

fine-tuneの完全checkpointを実行するために親checkpointが必須とは限らない。一方、LoRAは対応するbase、text encoder、VAEを失うと単体では使えない。この違いを`preservation_bundle`に記録する。共有部品の削減は完全revision・SHA256の一致を確かめてから行う。比較用の親原本と必須実行依存は区別する。

保存単位には、必要な重み、config、該当するtokenizer/processor、補助学習モデル、LICENSE/NOTICE、対応コードの版と実行環境情報を含める。未知の総数のモデルでは公開metadataによる構成調査までとし、最終取得manifestを作らない。

## 4. 準備する順番

[116件の準備表](../../catalog/preparation/2026-11-06-insurance-bundles-v22.json)は**ダウンローダー用の命令ではない**。既存のS1/S2/S3を条件付きストレスシナリオとして用い、先行制限が想定される能力、高性能・専門成果、基盤・データ・再現部品へ段階的に広げる。必須依存は親を準備する段階で一緒に確認する。小さく独自な補完差分を同時に処理することは妨げない。

実際に保存すべき学習成果の選定と、日常運用の速度・費用の最適化は別工程。いずれも、正規アクセス・利用条件・既存の総数/RAM条件・ファイル固定・保存容量・ユーザー取得承認を省略する理由にはしない。

## 5. 根拠の継承と次の具体作業

[R19](../../catalog/research/2026-11-04-round19-decisions.json)と[R20](../../catalog/research/2026-11-05-round20-decisions.json)の正負の評価を消さずに、採用理由を学習成果保全として明示した。今回の照合は新規の性能測定ではない。

一次情報：[Drama3](https://huggingface.co/fishaudio/drama-3)、[Drama3 INT4比較](https://huggingface.co/fishaudio/drama-3-int4/blob/main/README.md)、[GroundGUI](https://huggingface.co/PrentisAI/GroundGUI-8B)、[Consistency LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA)、[DavidAU公開元](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU)。いずれも具体的な近日停止命令は今回確認していない。

次は候補の無限追加でなく、この4構成と既選定の先頭群について、固定revision、必須部品、利用条件、必要容量を埋める。総数不明2件はmetadataの構成表を先に完成させる。学習成果の保存（機械学習）、依存・版の整合性（ソフトウェア供給網）、実際の復元可能性（デジタルアーカイブ）、行為ごとの許諾（法・ガバナンス）を分けて確認する。

## ERROR CHECK

CIで旧159レコード不変、163管理／116有効、4新規ID重複なし、承認0、準備表と有効選定の一致、未知容量を0としないこと、既存150B超ゲートを弱めていないことを検査する。テストの実際の成否・件数はGitHub Actionsとintegration-checkへ記録する。コード検査のPASSは重み保存・品質・実機動作のPASSではない。
