# R164／v71：Inkling Small、Inkling 2 Smallと無検閲編集版の選定漏れ・原因分析（2026-11-25）

## 結論

保全目的のモデルポートフォリオで、重要な新旧Inkling Small系列と無検閲編集版のファミリー調査が漏れていた。これはユーザーの依頼内容の問題ではなく、**「150B未満の実行上限」を、研究・アーカイブ候補の発見と同一視した選定設計の失敗**である。現行v71の260登録・210有効を変更せず、公式固定revisionの研究資料を追加する。`Inkling-2-Mini`系は既存登録・一部取得報告があっても、`Inkling-Small`、`Inkling-2-Small`の代替ではない。

## 具体的な欠落ソース（Publisher公式リビジョン、参照バイト数）

| リポジトリ | 固定SHA先頭12桁 | ファイル・byte（十進） | ゲート |
|---|---|---:|---|
| [thinkingmachines/Inkling-Small](https://huggingface.co/thinkingmachines/Inkling-Small) | `8cc5877b44d3` | 48／531,916,781,513 | 276B総、12B活性、原版。150B実行上限を超えるが、独立学習原本として研究優先 |
| [distributedcognition/Inkling-Small-abliterated](https://huggingface.co/distributedcognition/Inkling-Small-abliterated) | `c77011b2e437` | 47／698,246,149,596 | アクセス`gated=auto`。26件LFS参照はSHAマスク。権限確認前に取得・ハッシュ確定しない |
| [thinkingmachines/Inkling-2-Small](https://huggingface.co/thinkingmachines/Inkling-2-Small) | `885d78bfca61` | 43／393,510,050,371 | 594B総、17B活性、NVFP4。公式参考集約GPU VRAM最低500GB。CPU/VRAMピーク未実測 |
| [thinkingmachines/Inkling-2-Small-MXFP8](https://huggingface.co/thinkingmachines/Inkling-2-Small-MXFP8) | `14f2cb29a5d0` | 49／553,004,791,314 | MXFP8。公式参考集約GPU VRAM最低800GB。NVFP4と同一配布重みではない |
| [OpenUncensored/Inkling-2-Small-Uncensored](https://huggingface.co/OpenUncensored/Inkling-2-Small-Uncensored) | `88a0173f32de` | 49／553,004,704,928 | MXFP8無検閲編集版。独立学習結果ではなく独立**weight-space edited state**。原作者拒否率・MMLUは独立再測定していない |

これらはモデル重量のPublisherメタデータであって、本人のHDD実体SHAではない。すべて**現行正式選定・116件取得報告のリポジトリIDには無い**。新規ダウンロード・承認はゼロ。

### 編集差分を小さく保存する際の限界

`OpenUncensored/Inkling-2-Small-Uncensored@88a0173f...`の`edit.pt`は**39,174バイト**、Publisher LFS SHA-256は `58554a71aedb111f48cced364c035f102ccfd114e250dba6e165b929d356301a`。対応MXFP8原版とのファイルパス＋Publisher Git OID一致は**3件／14,863,943,654バイト**で、残り538,140,761,274バイトは単純ファイルSHA同一と主張できない。特に同じ594B原版の**NVFP4版は対応する編集再適用先のMXFP8原本ではない**。

編集情報とMXFP8親重みがあれば、技術的には別学習済み編集結果を再現できる可能性があるが、編集スクリプト・乱数と量子化のbit-exact性・依存バージョン・安全なPyTorch pickleロードを独立検証していない。**`edit.pt`を保存しただけで無検閲モデルの完全バックアップが完成した、とするのは誤り**。作者の拒否率低下及びMMLU僅差は著者報告で、オーナー自身の能力測定ではない。

### 規模と優先順位

「150B未満」「推論時のメモリ512GB未満」は**今あるハードウェアでの運用・取得ゲート**として維持する。ただし、独立学習原本の**研究登録・アクセス変化監視**から、これらを一律排除しない。Inkling 2 SmallのNVFP4原版（393.5GB）も、無検閲MXFP8原版（553GB）も、ポートフォリオの4TB上限に対して大きな占有量であり、実追加容量・最低200GBの空きは未計測。単純な重量容量だけで配布元アーカイブが完成するわけではない。

**研究優先順位**：①Inkling 2 Small NVFP4本体、②無検閲MXFP8 edited stateと39KB編集情報、③対応するMXFP8親の元状態、④Inkling Small旧原本、⑤条件付きのInkling Small abliterated。これらは保全価値の研究順位であり、**ダウンロード順ではない**。ユーザーのもう一つの呼称「無限スマイル」は正式モデルIDを裏付ける一次資料がなく、勝手に`InfiniteYou`等と読み替えない。`ByteDance/InfiniteYou`は別途カタログでDEFERRED記録がある。

## H／T／D／C／U／ERROR CHECK

- **H**：大規模・無検閲派生を、現在のローカル実行可能性とは別の保存研究優先軸で列挙すると、主要原本と独立編集stateの漏れを減らす
- **T**：5配布元の40桁固定revision・個別ファイル・サイズ・LFS発行者ハッシュと、v71全260資産・過去116取得報告のIDを比較。実取得・復元は本人の権利、実HDD、メモリ、依存を確認してから
- **D**：配布元メタデータの一致と無承認をPASS。Gated masked SHAの捏造、編集`edit.pt`単体を完全モデルとみなす、実機512GB上限例外を未測定で通すことはFAIL。所有者HDD/実動作/再現性はUNCERTAIN
- **C**：意図した「無限スマイル」が別モデル、編集重みの品質損失、MXFP8親や実行依存の不一致、権利・必要資源の制限
- **U**：名称同定、マスクされたSHA、オーナーの実媒体とGPU、編集の再現性。反復測定がないため合成不確かさ・包含係数を数値化できない

**ERROR CHECK**：R164は研究ファイルと非実行優先キューだけであり、正式v71のモデル追加0・取得承認0・実重量ダウンロード0・Gated迂回0・所有者媒体検査0。関連分野は、①MoE/学習表現、②モデル編集とベンチマーク統計、③Content-addressed archival、④GPUメモリ計画、⑤知財・アクセス条件。

### 次に考える問い

**独立学習済みモデルの保存優先度を、現在のGPU搭載量によって打ち切ってよいか。** 私の修正提案は、収集価値の研究と実機動作の許可を別の承認ゲートへ分離すること。
