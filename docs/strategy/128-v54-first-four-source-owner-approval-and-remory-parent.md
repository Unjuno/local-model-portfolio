# R128｜v54：取得報告61モデルを踏まえ、最小4原本・評価データを固定し、REMORYの親欠損を明示

基準日：2026-11-20（JST）。正本[CURRENT](../../catalog/CURRENT.json)は**v54／207登録・160有効（SELECT53／CONDITIONAL107）**。この報告は実モデルの新しい学習結果を追加するものではなく、既存モデルのファイル選択と取得順を決める。本人Dドライブを今回再マウントしたり重みを新規転送したものではない。

## 1.〈本論〉現状の61モデル取得報告を優先する

[2026-11-19最新取得台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)には、**61モデル・708ファイル・409,835,119,252byteがpublisherハッシュと一致したと報告**、1 Gated HOLD。記録上の最小空きは2,445,946,363,904byte。ただし保存環境を本作業から直接操作して再ハッシュした事実はない。未報告98件に対する原本選定は、61報告済みモデルの再ダウンロードではなく差分が原則。

[160件完全監査](../../catalog/decisions/2026-11-20-r128-v54-live-ledger61-and-parent-gap.json)では**61報告済み・Gated保留1・取得報告なし98**の排他的分類に一致。どのactive assetがすでに報告に載り、どれが追加取得候補かを全件一意に記録した。

## 2. 今回確定した4件の最小バッチ

| 順位 | 固定publisher源 | source byte | 固有の保存価値 |
|---:|---|---:|---|
| 1 | [elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | 7,606,817 | 日本語評価問題・過去対照回答、非重みデータ |
| 2 | [CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 140,160,376 | 多言語の学習・評価で人手注釈を保全 |
| 3 | [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 1,385,998,807 | 45言語ASRと独立CTC head、既存Whisper/Qwen3-ASRと別の学習結果 |
| 4 | [microsoft/Aion-1.0-Instruct-2.3B](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B) | 4,593,276,272 | 2.3B・日本語対応の独立小型Windows向けSLM |
| **計** | **2モデル＋2データ** | **6,127,042,272** | **101ファイル／publisher SHA256参照9件** |

同じrepoの固定commit SHA、file path/byte、LFS SHA256/Git blob SHA1は[新R128の非実行sourceキュー](../../queues/proposed-v54-r128-first-four-delta-source.json)で全件固定。以前の[R125](../../queues/proposed-v52-r125-ledger61-delta-next15.json)の3assetと[R126](../../queues/proposed-v53-r126-aion-bf16-first-public-source.json)のAionを**そのまま再利用した部分集合**。将来の大規模原本を追加で二重計上するための新規6.127GB予約ではない。

**Windows上の取り扱い**：ELYZA配布元に存在するコロンを含む旧ベースラインCSV1件（181,663byte）はNTFSに元ファイル名で保存不能。この最初のsource scopeからは除外し、原本のpath/hashを[R122履歴](../../queues/proposed-v50-r122-deduplicated-next15-sources.json)に記録。**評価本体test.csvは選択維持**。したがってELYZAの完全リポジトリミラーとは表現しない。後日、可逆リネームまたはPOSIX媒体の保存形式で完全保全を別途計画する。

## 3. 実際の取得を妨げる一回限りの本人承認を簡素化

[Windows取得器](../../scripts/download_r115_windows.py)へR128（4 source/101 file）対応を実装。[owner review template作成器](../../scripts/prepare_owner_scope_approval.py)を追加。前者は4件のファイル・ライセンスタグ・非Gated/Hub名前空間を一括検証し、**`--execute`だけでは通信・取得しない**。後者は実Dボリュームの容量を観測し、全4件のimmutable source fingerprintを埋めた**未承認**JSONを生成できる。**本人同意・法律的な権利・ボリューム確認・approvedの四つはすべて`false`から始まり、AIが勝手にtrueにはしない**。

所有者のWindows端末、実際のアーカイブルートが`D:\AI-Models`である場合の使用例：

```powershell
# 0. GitHub main更新後、固定4原本のファイル構成とディスクを読取で確認
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v54-r128-first-four-delta-source.json" --dry-run --root "D:\AI-Models"

# 1. 既存承認ファイルは上書きせず、4 sourceのレビュー用ドラフトをDに生成
py -3 scripts/prepare_owner_scope_approval.py --manifest "queues/proposed-v54-r128-first-four-delta-source.json" --root "D:\AI-Models" --output "D:\AI-Models\approvals\owner-r128-review.json"

# 2. 本人が各sourceの行為別ライセンス・親/ABIと実HDD容量を審査し、
#    取得するsourceの consent, rights, volume, approved を明示的にtrueとする。
#    調査環境は実装/可否を確認していないため、ここで自動trueにはしない。

# 3. 明示承認後に本人が取得を開始する場合のみ
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v54-r128-first-four-delta-source.json" --execute --approval-file "D:\AI-Models\approvals\owner-r128-review.json" --root "D:\AI-Models"
```

**未取得・未承認の現状**：正式`queues/approved.json`は空のまま。所有者のDドライブがこのリサーチ端末からは接続されておらず、今回の作業では重みの転送・親モデルのロード・推論を行っていない。添付CLI例の`D:\AI-Models`はパス例であり、実際の所有者ルートである保証はない。モデルファイルには未審査のcustom Python/pickleが含まれうるため、重みを保存しても自動実行しない。

## 4. 中大型・無検閲・特化モデルの維持と交換判断

**無検閲**：0bserverx RVN-Q4、Interpretic v2 Q4は取得台帳にVERIFIED報告があり**再取得しない**。フルBF16 Interpretic v2、RVN-F16のマスター化は別source scopeであり、60GB級の残容量と実ライセンス、元の推論実装が確認できた後の候補として維持。0bserverx SafetensorsはRVN-F16からの再構成であり、独立学習済み重みとして二重保存しない。OrcaRouterはGated HOLDを維持。

**小型特殊**：harness-hub pi RL LoRAは0.658GBの独立コーディング後学習を保持する価値が高いが、作者の正確な訓練親revisionが未固定であるため復元保証なし。DaisyRoseは55.586GBの独立RL原本だが、Qwen親・既存派生との同一タスク実測がないまま第一バッチを押しのけない。

**REMORYは特に注意**：[配布元REMORY](https://huggingface.co/fudan-generative-ai/Qwen3.8-27B-REMORY-1.9B)はオンライン継続学習済みsource **8,023,113,280byte**と独立した約2.006Bの学習済みmemory tensorを提供。正確な`Qwen/Qwen3.8-27B`親は`1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`。旧親と18の重量shardが同一、差分3小ファイル91,892byteと[作者の固定source](../../manifests/drafts/r127-2026-11-20-remory-20file-online250-and-parent-delta.candidate.json)は報告。しかし最新61モデル取得台帳に`Qwen/Qwen3.8-27B`は含まれない。**『REMORYを8GBだけで完全offline復元できる』はFAIL/未証明**。既存HDDのQwen parent全18重みshardの現物とSHAを確認するか、正当な親原本を含めた別容量/権利計画を作るまでREMORYのoffline-ready昇格は保留する。REMORYアーカイブ元ファイルを研究CONDITIONALから削除する必要はない。

## 5. 変数表・容量チェック

| 変数 | 意味（日本語） | 単位（SIとの対応） | 定義 | 定義域・範囲/前提条件 | 型 |
|---|---|---|---|---|---|
| `B_1` | R128第一バッチ固定publisher source容量 | byte（8 bit） | 6,127,042,272 | 4源のsource合計、全新規仮定 | 非負整数スカラー |
| `B_peak` | バッチ最大1ファイル長 | byte（8 bit） | 4,577,698,688 | Aion BF16重み一式、原publisher bytes | 非負整数スカラー |
| `S` | 一時コピー向け予備 | byte（8 bit） | `2 B_peak` | 本実装の概算、実cacheは別途変動 | 非負整数スカラー |
| `F` | 最低維持空き容量 | byte（8 bit） | 200,000,000,000 | 取得中も必要、policy | 非負整数スカラー |
| `D` | 本人保存先で現在観測する空き | byte（8 bit） | `disk_usage(D:).free` | 現在未観測、同時処理で変動 | 非負整数スカラー |

本バッチの一次判定は`D >= F + B_1 + S`。代入すると **215,282,439,648byte** 以上が必要という**初期source計画の保守的な例**になる。各項はbyte単位のため次元一致。これは後続の親/codec、他プロセス、OS/FS使用量や完全wheelhouseを含む最終保証ではない。過去台帳の空き2.446TBを今の`D`へ代入してはいけない。

## 6. H/T/D/C/U・ERROR CHECK

**H**：取得報告済み61と完全一致する重みの再取得を排除し、取得未報告4資産の最小バッチを実行できれば、同一保存枠で独立学習結果2つと人手データ2つを増やせる。

**T**：固定4source／101ファイル／9publisher SHA256参照の完全照合（n_min＝4、逐次停止＝初回版・SHA・パス・権限・容量床違反）。R128 11件＋owner template 7件＋既存R125 13件／R126 5件／R122 12件／R115 10件／R119 6件／承認7件、計**71件のローカルPython回帰テストPASS**。実モデル推論ベンチのHW・clock・batch・contextは未収集。

**D**：PASS_METADATA＝4源全ファイルのrevision/size/hashが既存固定sourceと一致し、71テストPASS。FAIL＝現物SHA不一致、Gated回避、無権利、空き200GB下限割れ。UNCERTAIN＝本人D実HDD、重み転送、offline restore、REMORY親シャード現物。

**C**：現行所有者HDDには61報告と別の大容量Qwen親がすでに存在する、Rumble/ASRのpublisher CTC動作が未保管runtimeに依存する、Aion custom_codeが環境ABIに非互換、データセットの公開付属ファイルに再配布制限がある。

**U**：アーカイブファイルの実在・ハッシュ、ライセンス適用目的、学習時の親依存とcheckpointの品質差、staging余裕。反復測定分布がないため合成不確かさ`u_c`および包含係数`k`は推定せず、数値を創作しない。

**ERROR CHECK**：v54 207登録／160有効。61報告＋1 Gated HOLD＋98未報告＝160。選定第一弾2モデル・2データ、101 files／SHA256参照9／6,127,042,272byte。数十GB級の別モデルを無断混入させない、既存重み削除0、正式承認0、所有者D新DL0。71/71単体テスト、Linux実験環境の空き不足はDドライブ測定ではない。mainブランチ上の資料・コード変更のみ。

関連分野：デジタル長期保存（ハッシュ・世代管理）、機械学習/LoRA・残差メモリ（親重み/ABI）、多言語ASR・言語評価、ファイルシステム（NTFS）、ライセンス・技術政策。

###〈次に考える問い〉

**本人ディスクに存在する61報告済みモデルとQwen親のSHAを再確認し、4原本の一括承認・差分取得を完了できるか。** 追加モデルの発見数よりも、オフライン復元できる原本数を増やすことを完了条件にする。