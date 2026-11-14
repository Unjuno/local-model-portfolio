# R64：現行有効135資産の取得準備全件監査（2026-11-15）

結論：135件の監査行は完成。しかし完全な長期アーカイブおよび取得承認を完成とみなせる資産は0件。選定v32を不変更。

全件の監査根拠（ID・採否・アクセス・依存・未固定revision・ファイル容量・次の作業）は[機械可読監査台帳](../../catalog/audits/2026-11-15-v32-135-completion-readiness.json)。

## 確定した監査数字

| 対象 | 件数 |
| --- | ---: |
| 現行資産 | 182 |
| 有効SELECT / CONDITIONAL | 53 / 82（計135） |
| 歴史的v27の一次ソース範囲が存在 | 126 |
| その後の固定一次ソース調査が存在 | 9 |
| 最終取得用revisionとselected bytesを正本が保持 | 2 |
| 正本の最終revision未設定／容量未設定 | 133 / 133 |
| 全文ライセンスレビュー済みの表記／依存レビュー済み表記 | 3 / 2 |
| 未確認総学習済みモデル（有効資産） | 7 |
| 条件付き82件中、配布元公開情報がGated | 17 |
| 本人の利用・取得許諾／実HDD残空きが実証済み | 0 / 0 |
| 取得承認・完了したオフライン復元ロック | 0 / 0 |

## 4TB保存枠の意味

v27 126件のSHA-awareソース和：3,417,685,712,585 byte。v28〜v32（ACE以外8件）のソース和：24,342,724,173 byte。ACE XL/Sharedの重複をSHAで排した純増：24,041,795,415 byte。
これらの和：3,466,070,232,173 byte。4TBの空のドライブで実空きを200GB以上残すと仮定した算術差：333,929,767,827 byte。
重要：この値は135件の完全依存・実行環境・合法な保存条件の合計ではない。ユーザーの実HDD、既存ファイル、stagingやcache未測定。余裕が証明されたという結論は禁止。

## 未確定7モデル

| Repo | 調査優先順位 | 主なゲート |
| --- | --- | --- |
| ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8 | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW |
| Stuubs/Stubelius_Remix_Ltx2.5 | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW |
| WhissleAI/steer-tts | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW, GATED_OWNER_ACCESS_AUTHORIZATION |
| maya-research/maya2-native | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW |
| fishaudio/drama-3 | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW |
| ausboss/Qwen-Image-2.1-Consistency-LoRA | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW |
| PrunaAI/P-H3-Image | P0_PARAMETER | UNKNOWN_FULL_PIPELINE_PARAMETERS, LICENSE_FULL_TEXT_REVIEW |

Pruna P-H3の15 Safetensorsには49,635,347,496保存要素が存在することをR61後のヘッダー限定計数で確認。ただしパラメータ重複/buffer、外部依存、MiniMax地域制限、本人利用権利を別審査するため、カタログのUNVERIFIED_BLOCK_FINAL_LOCKは維持する。
Maya2はMimi/ECAPAの固定ソースをR63で特定。ECAPAの厳密テンソル数と互換性を確定する必要がある。Drama3はcodec.pthの安全な非実行分析が残る。

## 完成までの実行順序

1. 7モデルの総学習済み計数と必須Codec/Encoderの閉包。2. Gated17件の本人取得権限・許諾原文。3. 残133件の正本final SHAとファイルbytesを既存のv27→v32一次資料から検証しながら統合。4. 実HDD空き/キャッシュ/ランタイム容量の評価。5. 個別の明示取得承認後にダウンロードとSHA実測。

## 変数表と単位・検証

| 変数 | 日本語の意味 | SI単位 | 定義・前提／型 |
| --- | --- | --- | --- |
| A | 有効資産数 | 1 | 135、非負整数スカラー |
| B | 既知ソース範囲の合計 | byte | 3,466,070,232,173、未完全部品を含まない |
| C | 計画上限 | byte | 4,000,000,000,000、実HDDとは別 |
| F | 最低必要空き | byte | 200,000,000,000、実測未実施 |
| U | 空4TB仮定での算術差 | byte | 333,929,767,827、実空きではない |
| P | 総学習済みパラメータ数 | 1 | 7件未確認、MoE非活性expert含む |

次元チェック：B/C/F/Uはbyte、A/Pは無次元。
H：135行全てに1つの研究採否とブロッカーが存在する。T：n_min=135の全IDとqueue、条件付き82件のアクセス表を照合。D：一致はPASS、取得判断はBLOCK、完全なオフライン復元はUNCERTAIN。C：上流SHA変更、依存/権利変化、データ重複。U：公開元ソース、ライセンス、実機、未取得ファイル。u_c/kは測定不在のため未算定。
関連分野：MLモデル依存管理、ソフトウェアサプライチェーン、デジタル保存と法務。
ERROR CHECK：選定182／有効135維持、実モデルの取得・実行・許諾受諾0件、新ブランチ0件。
次の問い：133件の既存source範囲から、法的に正しい固定取得lockへ最短で昇格できるモデルはどれか？
