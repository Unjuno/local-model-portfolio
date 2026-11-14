# R72｜v32有効135件の証拠・第一停止要因・原本固定・本人権限の最終統合（2026-11-15）

## 1.〈本論〉

正本`catalog/CURRENT.json` v32（182登録、53 SELECT＋82 CONDITIONAL＝135有効）に対して[R64全件レディネス](../../catalog/readiness/v32-2026-11-15-r64-all-active.json)、[R68 first blocker](../../catalog/readiness/v32-2026-11-15-r68-135-actionable-triage.json)、[R71歴史候補manifest索引](../../catalog/research/2026-11-15-r71-v32-135-cross-draft-source-index.json)、[R70 RFD4公開元重みSHA同一性](70-rfd4-identity-resolution-stale-release-manifest-2026-11-15.md)を正確な`asset_kind + repo_id`で**135件一対一join**。成果は[機械可読R72台帳](../../catalog/readiness/v32-2026-11-15-r72-consolidated-135-cross-evidence.json)。各資産の出典、現在の不足ゲート、次に確認する証拠を1レコードに統合した。

| 分類 | 件数 | 進捗の意味 |
|---|---:|---|
| v27歴史的source censusあり（R64の現行分類） | 126 | **近時の全ファイル再照合ではない** |
| v28〜v32新規の固定source evidenceあり | 9 | その中に外部依存・別backend・実行不明の未解決あり |
| 歴史的candidate manifestにも直接ファイル参照あり | 29 | 上記126/9と**重複する補助証拠**。加算しない |
| candidate manifestで40桁revisionあり | 27 | 必要ファイルすべての最終保存SHAが揃う意味ではない |
| 現行Gatedリスク対象（正規化済み） | **17** | 本人のアクセス権限を確認するまで不可 |
| 完全な合法取得・全依存・現物SHA・実機空きを満たす | **0** | ダウンロード承認0、オフライン復元PASS0 |

### 実証したカウントの誤差：Gated 16件と17件

R68の歴史的な静的抽出は`observed_access === "gated"`という**文字列完全一致**により16件を抽出。しかし`gradium/phonon-40m-multilingual`のv32正本値は`Gated auto (anonymous metadata); user authenticated gate permission NOT verified`であり、正規化前の文字列一致から**漏れた1件**だった。[配布元のモデルページ](https://huggingface.co/gradium/phonon-40m-multilingual)を2026-11-15にHugging Faceアプリで再確認すると**Gated**、ライセンスタグはCC BY-NC 4.0。

**正しいGated本人許諾審査対象は17件**。既存R64側のGatedサイドカーとも一致。R68の16件を「全Gated件数」として利用してはならない。R72の正規化はサイドカーのGatedフラグ、または`observed_access`値が`gated`で始まる場合に限る。`public_ungated`の文字列を誤ってGatedとしない。

### 135件の最初の停止要因（R68分類を維持）

| 最初に解決すべき条件 | 件数 |
|---|---:|
| 本人Gatedアクセス確認 | 16 |
| v27一次ファイルscopeを現在の台帳と再結合 | 2 |
| 全学習済み/実行依存の閉包 | 110 |
| 完全モデルパラメータ数の検証 | 7 |
| **合計** | **135** |

**注意：** この表のGated16は「最初の停止要因」がGatedという意味であり、Gatedリスクを持つ全17件ではない。ある資産ではより上位にパラメータ不明がある。モデル総数不明7件は[R66](66-seven-parameter-unknowns-source-bound-audit.md)/[R67](67-v32-seven-unknowns-hub-metadata-recheck-2026-11-15.md)に追跡されている。

### RFD4の原本整合と法的ゲート

[R70](70-rfd4-identity-resolution-stale-release-manifest-2026-11-15.md)により、v32旧観測rev`cf31b935…`とR64固定rev`a06e2509…`のroot`model.safetensors`の公開SHAは同じことを検証。旧revの`release-checkpoints.json`はそれより前の異なるSHAを持つ旧リリースを記述していた。**二重root保全不要**、R64固定7ファイル原本scopeを維持。

追加の法務原本確認：選定revの[LICENSE](https://huggingface.co/nvidia/RFD4-Proteina/blob/a06e2509c7033b010fc43614e9fd840303588502/LICENSE)はBSD 3-Clauseを本文まで確認。[同revのREADME](https://huggingface.co/nvidia/RFD4-Proteina/blob/a06e2509c7033b010fc43614e9fd840303588502/README.md)には一方で**Private release preview／authorized account**の記述が残る。2026-11-15 Hub listingはGated表示なし、[NVIDIAのサービスモデルカード](https://build.nvidia.com/ipd/rfd4-proteina/modelcard)はBSD3と商用利用可を案内するが、APIサービス契約はモデル重みの取得権利とは異なる。そこで**版依存のアクセス条件を未解決として保持**し、本人権利や外部refolding oracleの別許諾を勝手にPASS扱いしない。

## 2.〈応用・転用例〉残作業を実行単位に切り出す

- すでに選定されたR64の8資産・9配布元・91ファイルについて、まず固定ファイルSHA、親・Codec・Processor・実行ソース、ライセンスの出典をまとめ、所有者が実HDD上で正規に持つものだけを`scripts/archive_preflight.py --hash`で検証する。利用者による明示承認がなければ取得・実行はしない。
- v27歴史source censusの126件は全repoをもう一度web検索するのではなく、原本固定マニフェストを現在の選定スコープへjoinして、証拠の使い回しと真正の欠損を分ける。
- 150B超量子化例外は現行ルールどおり同じHW/OS/driver/backend/context/batchで測定し、RAM・品質・権利・容量を非補償ゲートとして保持する。現在承認0は変わらない。
- 4TBは上限の計画値。200GBの最低実空き・staging/cache・既存ハッシュ一致による実増分は実機計測なしに確定させない。

## 3. 変数表・次元検査・H/T/D/C/U

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| N | v32有効資産数 | 1（件） | 135 | 整数スカラー |
| V | v27歴史source census分類数 | 1（件） | 126 | 整数スカラー |
| R | v28〜v32新規source分類数 | 1（件） | 9 | 整数スカラー |
| G | 正規化されたGatedリスク資産数 | 1（件） | 17、個人権限未確認 | 整数スカラー |
| D | R71で直接ドラフト証拠のある資産数 | 1（件） | 29、V/Rと重複あり | 整数スカラー |

次元チェック：VとRは異なる排他的なsource分類の資産件数で合算可能。一方Dは同じ資産の別軸なのでV/Rへ加算しない。容量byteやパラメータ数とも混合しない。

**H:** 既存一次資料と135件の正本を厳密に結び、Gated文字列の表記揺れを正規化すれば、漏れと重複なしの現行停止条件を確定できる。  
**T:** v32/R64/R68/R71の各135件（n_min=135）を厳密キーでjoinし全件一意検査。Gated台帳17件とHubのPhonon実表示を直接照合。RFD4は2revでroot SHA・manifestを比較。  
**D:** 一意135、53+82=135、126+9=135、Gated正規化17がPASS。実体取得準備と完全再現性は`UNCERTAIN/STOP`、許可された取得0。  
**C:** Gatedが将来解除、歴史資料と現在配布物が一致しない、サイドカーのGated状態が古い、旧マニフェストがrootファイルを誤記していた。  
**U:** 現地権利・物理HDD・依存環境・配布元変化が主要な未測定要因。統計分布未提示のため合成標準不確かさu_cと包含係数kは未算定。

**ERROR CHECK:** 182=135有効+47非有効。135=53+82=126+9=16+2+110+7。Gated全件17、完全一致文字列のみ16、漏れ`gradium/phonon-40m-multilingual`1件。R71直接証拠29（履歴126/新9に重複）。取得承認0、payloadの取得0、ローカルハッシュ測定0。

関連分野：機械学習（学習済み依存）、ソフトウェアサプライチェーン（固定rev）、デジタル保存（同一性）、アクセス制御・ライセンス（本人許諾と利用契約）。

## 4.〈次に考える問い〉

135件について、すでに固定された原本ファイルと不足している**実機・権利・Codec依存**をどう分離し、まず1件を合法的に完全復元できる状態へ進めるか？
