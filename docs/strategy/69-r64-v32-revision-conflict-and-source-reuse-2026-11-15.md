# R69｜R64原本ファイル参照とv32正本の突合・revision不一致の隔離（2026-11-15）

## 1.〈本論〉

[機械可読R69台帳](../../catalog/research/2026-11-15-r69-r64-v32-source-join.json)は、v32正本と[R64候補マニフェスト](../../manifests/drafts/r64-eight-source-scopes.candidate.json)を`repo_id`で厳密結合した**読み取り専用の照合結果**。8有効資産＋ACE-Stepコード/依存1repo、9repo・91ファイル・38,519,866,446 byte（配布元ファイル参照の単純合計）。原本ダウンロード・SHA現物検査・ライセンス許諾・復元試験を意味しない。

| revision照合結果 | repo数 | 意味 |
|---|---:|---|
| v32にrevisionなし、R64に固定revisionあり | 6 | **情報の未転記**。配布元の欠損や不一致とは呼ばない |
| v32観測revisionとR64固定revisionが一致 | 2 | revision文字列一致。取得可能・復元可能を保証しない |
| v32観測revisionとR64固定revisionが異なる | 1 | **差分未解決**。原本同一性の審査が必要 |

### 差分1件：`nvidia/RFD4-Proteina`

- v32正本の`upstream_revision_sha_observed`: `cf31b93509df5af854c7f6ad704f5c83c77c0698`
- R64原本マニフェストの`revision`: `a06e2509c7033b010fc43614e9fd840303588502`
- **判定：DIVERGENT_REVISIONS_NEEDS_SOURCE_DIFF**。リビジョン差だけでは、重みが変更されたか、READMEだけが更新されたか判別できない。
- 次の最小検証：両revisionの全選択ファイルについて`path/size/LFS SHA256/Git blob SHA1`を比較。重みの完全一致を確認できれば同一原本の別コミットとして説明可能。いずれかが異なれば新旧学習済み状態の差分を調べ、保存する版を明示的に選択する。
- **禁止：** v32正本のrevisionをR64の値で無条件に上書きすること、ファイル同一性未検証でlockをPASSにすること。

### 他8repoの扱い

- 一致2件：`nvidia/Alpamayo2-Edge`、`ACE-Step/acestep-v15-xl-turbo`。
- 正本revision空欄6件：`qvac/BotPsy-0.8B`、`ibm-granite/granite-timeseries-ttm-r3`、`robbyant/lingbot-touch-tiny`、`tencent/Qwen3.8-27B-DSpine-b16`、`nvidia/Nemotron-3-Diarization`、`ACE-Step/Ace-Step1.5`。最後は有効資産そのものではなく外部依存repo。
- R64の91ファイル参照は、全て記載bytesの合計とrepo選定bytesが一致する。LFS SHA256が記録されたファイルは22件。Git blob SHA1は91件分記録。ただし現物は一件も照合していない。
- これはR68の「133件最終revision未固定」という**正本フィールド監査の意味を限定する発見**。R64の固定ソース情報はあるが、法的権利・全依存・実物ハッシュが未解決なので、最終ロック済み件数を増やさない。

## 2.〈応用・転用例〉

同じ`repo_id`結合をR57/R59/R61など既存の研究manifestへ適用すれば、135件を対象に、(a)既存一次証拠あり、(b)正本未転記、(c)同一repoでrevision衝突、(d)依存repoだけ存在、(e)真の未調査を分離できる。ファイル名が同じだけでは同一性と見なさず、ハッシュとbyteで判定する。

## 3. H/T/D/C/U・変数表

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| N | R64 repo数 | 1（件） | 9、整数 | 整数スカラー |
| A | R64内のv32有効資産数 | 1（件） | 8、整数 | 整数スカラー |
| F | R64ファイル参照数 | 1（件） | 91、整数 | 整数スカラー |
| B | R64配布元ファイル参照の単純合計 | byte | 38,519,866,446、重複排除前 | 整数スカラー |
| M | v32観測revisionとR64固定revisionが一致するrepo数 | 1（件） | 2 | 整数スカラー |
| X | revision文字列が不一致のrepo数 | 1（件） | 1 | 整数スカラー |
| U | v32に観測revisionがないrepo数 | 1（件） | 6 | 整数スカラー |

次元チェック：N、M、X、Uはrepo件数で加算可能。Fはファイル件数、Bはbyteなので件数とbyteを加算しない。

**H:** 既存manifestとのjoinで「正本未転記」と「revision不一致」を分離できる。**T:** R64の9repo/91ファイルをv32と突合し、ファイルbytesを全件加算（n_min=9repo、91ファイル）。**D:** 9=6+2+1、8 active＋1 external、全ファイルbytes一致なら台帳照合PASS。RFD4原本同一性・権利・実物・取得はUNCERTAIN。**C:** 同一revisionでも必要な外部学習済み依存が欠落する、別revisionでも重みが同一である。**U:** 原本SHA現物検証・ライセンス・ユーザー実HDDは未測定。合成u_cとkは確率モデルがないため未算定。

**ERROR CHECK:** 9repo・91ファイル・38,519,866,446byte、revision状態6+2+1=9。RFD4差分1件。取得承認0、モデルダウンロード0、実機実行0。

関連分野：ソフトウェア供給網（revisionと内容同一性）、機械学習（学習済み状態の区別）、デジタルアーカイブ（原本証拠の統合）、法務（許諾の独立審査）。

## 4.〈次に考える問い〉

RFD4の2つのrevisionで重みSHAが一致した場合、同じ重みを二重保存する代わりに、どのrevisionのLICENSE・README・コードを正本として保全すべきか？
