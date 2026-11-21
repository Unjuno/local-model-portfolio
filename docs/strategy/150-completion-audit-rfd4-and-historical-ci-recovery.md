# R150：保存済み99件からの完成度監査・RFD4中心原本同一性・歴史的テスト修復（2026-11-22）

## 目的と今回の最終判断

取得を確定した対象は既に保存済みとのユーザー申告を尊重し、**再取得・自動承認・既存ファイル削除・未審査モデル実行は実施しない**。正式正本 [v63 CURRENT](../../catalog/CURRENT.json)の235資産について、未取得ではなく**現時点の取得台帳で「報告VERIFIEDか、報告HOLDか、報告がないか」**を分離する。取得台帳のVERIFIEDは独立したowner Windows Dの本セッション再SHAや完全オフライン復元を意味しない。

[全235件機械可読の完成度一覧](../../catalog/audits/2026-11-22-r150-all235-completion-status.json)は、[再生成コード](../../scripts/audit_completion_r150.py)で現行正本、readiness、access、既存取得台帳を一対一照合。結果は下表の通り。

| 分類 | 全235登録 | 有効188 | 追加作業 |
|---|---:|---:|---|
| 取得台帳VERIFIED報告 | **99** | **99** | 再ダウンロードせず、実媒体SHA、ライセンスとオフライン推論を検証 |
| 取得台帳GATED HOLD報告 | **1** | **1** | 配布元の正規本人権限以外で回避しない |
| 台帳に取得済みの記録なし | **135** | **88** | 物理不在とは断定しない。選定・アクセス・依存とowner現物の存在照合を先行 |

さらに、**有効な総パラメータ未確定13件**、**条件付きでGatedのPublisher観測21件**、有効全188件の取得・復元readinessは**0件PASS**。これは**保存品質の未検証数**であって、全188件が実際に動作不能という意味ではない。高精度原本の研究選定から「完成したアーカイブ」へ進むため、repo ID／revision／ファイル集合／各実行依存と実機復元状態を明示的に分ける。

## RFD4-Proteina：重大な訂正と本体採否の確定

[R150 RFD4 Publisher二世代のSHA監査](../../catalog/research/2026-11-22-r150-rfd4-core-weight-same-auxiliary-diff.json)は、[NVIDIA旧rev](https://huggingface.co/nvidia/RFD4-Proteina/tree/cf31b93509df5af854c7f6ad704f5c83c77c0698)と[実取得報告rev](https://huggingface.co/nvidia/RFD4-Proteina/tree/5ec66c399bf0b48727ab24e6b298dcf33864fa07)の**全ページの公式ファイル一覧**を再確認した。

- 中心merged`model.safetensors`（1,742,660,596byte）の**両revision Publisher LFS SHA256は完全一致**：`5b549dd61adb2f6c6b5cb95bda13f40f5e31556b4e6c755edc0ca6f011c68fb0`。このSHAは取得台帳の重量受領報告とも一致。**中心原本の再取得は不要。**
- `transformers/model.safetensors`のSHAは旧`2fcecba5656ae980750b78034ce768cb1fcbf2c2fc1afe7d9e64de6c8b5cd96f`と取得版`e753bed3e506f5f907276c30e8bf711df6c74b05a1cadecd643973867d71cdb7`で異なる。旧51ファイル→新78ファイル。新revisionにはbase、adapter、抗体variantなどの別学習成分が追加されている。
- 歴史的[R106の厳密な12ファイル・3,493,648,941byte原本マニフェスト](../../manifests/drafts/r106-v45-rfd4-pretrain-plus-merged-original.candidate.json)は、既に**取得側revision `5ec66c...` を固定**していた。つまり以前のR148で指摘したcatalog古い観測revisionとの差は、**中心原本を別学習済みモデルとして扱う根拠にはならない**。今後は**中心原本を確定維持、追加variantだけ個別の推論・研究依存として検査**し、2つのフルrepoをダウンロードしない。
- 取得台帳では17files／5,236,405,470byteをVERIFIEDと報告するが、完全なOpenFold／refolding runtime、CUDA ABI、他のantibody ckpt全種が再現可能かは今回検証していない。承認されていない追加取得は依然STOP。

## 現行ソース検証・歴史的回帰テストの修復

変更前の全658件の`unittest discover`では失敗21件、エラー5件。R150では、旧v19/v34/v35/v36/v38/v40/v43/v45/v47/v53/v55、R60/R61/R106/R117/R122/R126/R128/R135の歴史的テストが**今日のCURRENT・今日のledgerも昔の数字でなければならないと誤検査**していた問題を修正。履歴はそれぞれ不変のvXXファイルに固定し、現在の件数・取得報告とは独立に検査する。退行テストを削除・無効化せず、ユーザー承認0と履歴不変条件を保持。

実害があったファイルパス検証は、`baseline/preds/anthropic.claude-v2:1.csv`のような**Hugging Faceでは合法なUNIX Publisherパス**をWindowsでそのまま解決できない問題。旧v32の研究用source一覧に限り、`:`を`%3A`とする決定的なポータブル別名と**元Publisher pathを同時に記録**するよう修正。ユーザー指定の`a:b`、ディレクトリ遡及、symlinkの安全チェックは引き続き拒否。これにより全135件の静的source inventory監査を安全に実行できる。所有者の実際の保存場所を勝手に変更したわけではない。

パラメータの安全判定では、通常の完全総数と**「親原本＋LoRAパラメータの保守的な上限が150B未満」**を区別し、根拠と非実行・未承認フラグがある場合のみ研究スクリーニングを許容。正確な全tensor要素数がnullのモデルを、上限推定のみで`download-ready`に変更しない。Kumo-Anomalyはモデル・取得キューの**両方**で研究専用かつ承認不可を証明させる。従来の`UNKNOWN`が承認される抜け道は作らない。

[現行ポリシー監査](../../scripts/audit_selection_decisions.py)と[150B/512GB監査](../../scripts/check_parameter_cutoff.py)が無制限に過去revisionの一覧を更新しなければ通らない旧実装も修復。現在の正本と歴史的policy祖先の両方を検証する。

**統合回帰**：別作業で追加された研究記録・テストも保持した統合main候補は、全691テストが失敗0／エラー0。

**計測条件**：検証はクラウドLinuxのPython3.12標準ライブラリ、ネットワークから独立したローカル版比較とunit test。モデル重量読込、GPUクロック、推論バッチ、AI品質ベンチマークは**実施していない**ため、作者公表速度との比較や実機性能の主張はない。

## H / T / D / C / U

**H**：歴史的スナップショットの時系列整合性を守り、99モデル受領報告を正しく分類し、RFD4の中心原本再取得を不要と確定することで、既存実体の保管安全性とポートフォリオの運用完成度が改善する。

**T**：235行を元選定・readiness・access・ledgerとjoinし、VERIFIED99・HOLD1・報告なし135を区別する。RFD4の二revを含む全ページで主要重量SHAを照合し、旧スナップショット検査と未来revision許容テスト、未知パラメータを偽のLOWとした負例を含めユニットテストを実行する。

**D**：レポート235行一意、取得台帳99件全一致、RFD4中心SHA一致、全188有効で未承認・未知総数は停止し、全unit testが失敗0であれば**コードとPublisherメタデータ整合PASS**。owner Dの独立SHA・依存閉包・実推論・個別利用権利が未確認なら**最終運用完成はUNCERTAIN／新規取得STOP**。

**C**：中心原本の重量SHA一致でも変わった`transformers`コードやadapterが本体出力に異なる効果を与える可能性、定量品質は旧版と一致しない可能性がある。後学習アダプタに独立保存価値があり、代替推論器が必要となる対立仮説を残す。

**U**：所有者現物再ハッシュ、端末GPU/CPU実装、量子化/zero-point、親モデル/codecとランタイム、改変variantの学習済み範囲、ライセンス個別行為が不確か。反復推論品質データ未取得につき合成標準不確かさ`u_c`、包含係数`k`は未算定。

関連分野：**ソフトウェア供給網・ハッシュ検証／AIモデル学習系譜／バイオ・蛋白質モデルのvariant管理／Windowsファイルシステムと推論実装**。保全対象は「同名repo」ではなく学習成果、Publisher SHA、ファイルスコープ、動作依存の明示的な組合せで確定する。

**最終状態の区別**：選定・台帳構造・コードテストの完成は改善。所有者のデータがすべて実行可能という証明はしていない。既取得ファイルの再ダウンロード0、削除0、承認0、未審査モデル実行0。
