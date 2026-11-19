# R129｜Aya dataset：評価データ保存のプライバシー境界と最小原本scope（2026-11-20）

## 1.〈本論〉— R128の4 source pilotの重要な未審査点

`main` `31335040e785bacbff792a1b16029c4c849ad258` の正本はv54・207登録／160有効。現行[4 source pilot](../../queues/proposed-v54-r128-first-four-delta-source.json)は2モデル＋2データセット、101ファイル／6,127,042,272 byte、本人承認0。ここで `CohereLabs/aya_dataset` は**204k件程度の人手注釈instructionデータ**だけでなく、**注釈者demographicsのParquetファイル**を含む。公式[配布元カード](https://huggingface.co/datasets/CohereLabs/aya_dataset)もdemographics dataの存在を明記。公開配布されていることと、すべての利用行為・保存・再配布にプライバシー上の問題がないことは別。

元の選択6ファイル／140,160,376byteのうち、`demographics/train-00000-of-00001.parquet`は**113,702byte**、出版社LFS SHA256 `6468cc56f1c115458507368381fd2b9e74d7b7a5dc0228f6b550146e5320bc2d`。このファイルは個人情報・センシティブな属性を含み得るため、**元のR128原本sourceキューを勝手に実行可能にせず、研究用の「demographics除外」5ファイル案**を追加する。

| 項目 | 出版社の固定source情報 |
|---|---:|
| Publisher revision | `f9ea04583f02a8f86404ff6c58bf75fe637df8a2` |
| 既存フルsource | 6ファイル／140,160,376byte |
| demographics | 1ファイル／113,702byte（保留） |
| 代替core-only | **5ファイル／140,046,674byte** |
| core-only LFS SHA256参照 | 3 |
| 取得承認・物理ハッシュ検証 | 0件 |

差分はdemographicsの113,702byteだけ。**これだけでデータ本体が匿名化済みと判断しない**。train/test Parquet自体の個人情報・権利・研究同意も未確認。公式ライセンスタグはApache-2.0だが、今回の固定6ファイルに独立の`LICENSE`ファイルは含まれない。README内の表示と元データ利用条件、再配布の可否を分けて審査する。

## 2.〈応用・転用例〉— 既存選定と競合しない改善

[研究用5ファイル代替manifest](../../manifests/drafts/r129-2026-11-20-aya-core-only-privacy-hold.candidate.json)は**非実行・未承認**で、R128の101ファイル案を上書きしない。将来、所有者が個人研究目的の利用条件と個人情報処理の適法性を確認した場合にのみ、core-only案の正確なファイル集合を採用する。元6ファイルを再現する必要があるならdemographicsを別の保護・アクセス権限・明示同意付きで審査する。

分野横断：MLデータ来歴、プライバシー工学、著作権・データライセンス、長期デジタルアーカイブ。

## 3. H/T/D/C/U

**H**：人手注釈の言語学習価値を維持しつつ、不要な属性データの無条件取得を避けられる。**T**：元6件のPublisher固定ファイルから1件除外し、残り5件のpath・byte・SHAと和を照合（n_min=6）。**D**：PASS=5件140,046,674byte・除外113,702byte、元pilot不変、承認0。FAIL=属性データを同意なしに自動取得、5件だけで完全匿名と宣言。UNCERTAIN=元Parquet内の個人情報と権利。**C**：コアデータにも個人情報が含まれる、demographicsが評価再現に不可欠、ライセンス上の条件が別途存在。**U**：配布元カードとデータ本文の差、同意範囲、再識別リスク。分布未定のため合成不確かさu_cと係数kは数値化不能。

| 記号 | 意味（日本語） | SI単位 | 定義 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `B_full` | 元source総byte | byte（SI基本単位外） | 140,160,376 | 非負整数、固定6ファイル | 整数スカラー |
| `B_demo` | demographics byte | byte（SI基本単位外） | 113,702 | 固定1ファイル | 整数スカラー |
| `B_core` | 代替core-only byte | byte（SI基本単位外） | `B_full-B_demo` | 固定5ファイル、権利未承認 | 整数スカラー |

**次元チェック**：両項byteの差はbyteであり、140,160,376−113,702=140,046,674byte。容量が小さいことはプライバシー安全性の証拠ではない。

**ERROR CHECK**：元6ファイル重複なし、5件byte和一致、Gated回避なし、現物取得0、承認0、正式catalog変更0。

## 4.〈次に考える問い〉
データセットの人手注釈を保存する際、評価再現性のために本当に必要な属性データと、匿名性を優先して除外できる属性をどこで分離するべきか？
