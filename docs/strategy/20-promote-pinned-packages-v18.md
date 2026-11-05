# v18: R21/R22実査済み2組を正式な条件付き研究選定へ反映（2026-11-05）

## 決定
- **CONDITIONAL追加** `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`：固定版の独立rank128画像生成/編集LoRA。本体・encoder/VAEは**既存** `Qwen/Qwen-Image-2.1` を再利用し、別モデルとして二重に選ばない。保存パッケージ33,802,789,787byte（35件）、うちLoRA側671,173,375byte。既存ベースの完全版が実機で同一と確認できた場合の追加容量は671,173,375byteだが、**実際の増分は未検証**。
- **CONDITIONAL追加** `InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`：中国語の政治的回答抑制を変更した選択的派生。Q4重み・F16画像projector、関連元LICENSE/設定資料を合わせ17,738,357,352byte（12件）。別のBF16原本重み18シャードは選択しない。
- もとの `orcarouter/Qwen3.8-27B-Uncensored` / 0bserverx は評価比較用に維持。**低拒否だけで優越を主張しない**。ユーザー指定で維持するNanbeige4.3-33B、除外6件、R23研究のみのモーション/音声アバター候補は変更しない。

## 一次資料によるゲート
[R21固定ファイル計画](../../manifests/drafts/round21-pinned-preservation.candidate.json)は4repo・47ファイル、重み10ファイル全てについて元配布者LFS SHA256および正確なbyteを記録。[R22保存テンソル監査](../../docs/strategy/18-component-census-and-checksum-audit.md)は全10ヘッダーをパースしてChatRのDiT7,115,124,736+encoder8,767,123,696+VAE337,740,404+LoRA335,544,320=16,555,533,156要素、InterpreticのGGUF言語27,320,697,856+vision460,730,096=27,781,427,952要素を確認。両方**150B未満**。保存テンソル要素数は固有trainable数と厳密同義でなく、その上限として判定。

ChatRの作者の[非商用Qwen Research License](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/blob/aa213272180d6ad0d03f5fb3d597f0f0322647c5/LICENSE)を確認。Interpretic[原本LICENSE](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2/blob/69227901b022d2a039fe52e220383f0b79517063/LICENSE)はApache2.0。適切な研究目的での保存候補には適合するが、ユーザー本人の契約承諾・再配布許可・ローカル取得権限を代行したわけではない。

**負の証拠・限界**：
1. ChatRは実際のrank128重みと基盤224/224対応形状を検証済みだが、**作者の最近の推奨35steps/CFG5.0に対応した独立画質・速度試験なし**。2×RTX4090 24GBで旧25steps/CFG4.0だった時間の流用禁止。差分の優位、成人向け品質の保証なし。
2. R22でChatRのREADME.md、inference.pyは作者SHA256SUMS記載と実内容のハッシュ不一致を発見。**配布元重み自体の破損証拠ではない**が、整合性記録は消さない。Git blob IDは実内容と一致。
3. Interpreticは作者の中国語政治113問 Q4評価で抑制回答98→4。一般的有害依頼拒否95/100は**BF16**、GPQA/IFBench/MMLUも**BF16**であり、Q4の総合能力は同条件で未検証。中国語政治回答の事実正確性も別評価。量子化全tensorの数値同一性・実機RAM/速度は未確認。
4. R22で確認した総scalar数は重要な配布元ファイル静的検査であって、**重み全ファイルのデータSHA256ローカル照合ではない**。モデル本体をダウンロードしていない。

## 正本・容量・取得
- v18 CURRENT=144資産・有効99件（select53、conditional46、hold27、deferred12、excluded6）。モデル121件／データ23件。総数PASS105、未確認14、150B超量子化審査2。
- R21における両パッケージの保存対象データ合計51,541,147,139 byte（十進約51.541GB）。OS/runtime/cache/stagingの必要容量と実機空き・既存基盤照合はまだ不明。3.8TBは目標予算であって物理的空きを証明しない。
- `queues/proposed-v18-2026-11-05.json`は**非実行の候補99件**。`queues/approved.json`は変更しない。本文・LICENSE・Noticeはデータとして扱い、外部スクリプトは実行しない。ファイル最終lock、保存先と実空き、明示的な取得承認は別。

## H/T/D/C/U
**H**：2件の選定構成は、強い既存モデルでは再現しにくい専門能力を含み、150B未満で利用用途上の品質を保つ。
**T**：R21/R22の固定ヘッダー/ファイル同一性を全数確認済み。次段で同基盤・同seedの画像40題×3seed、選択的回答抑制113問と一般能力各200問の事前分割試験、実機の固定backend/クロック/batch/contextで速度30反復。
**D**：総要素数<150B/重み配置/static LoRAはPASS。独立品質・実行RAM・取得後SHA・物理容量はUNCERTAIN（取得許可ではない）。権利条項不一致・実機RAM超過・品質重大低下ならFAIL。
**C**：R22 shapeのみ一致で適用時に欠落、拡張モデル能力の不実、Q4で他能力の低下、作者checksumの古さによる誤検出、GPUメモリ不足。
**U**：主要誤差源は評価データと判定モデルの系統誤差、推論ハード差、未取得ファイルの検証、仕様書の更新差。定量評価未実施のため合成標準不確かさu_c・拡張係数kは未推定。

## ERROR CHECK
- 新規2件とも正規Hub ID・不変commit・R21 full-source files・R22 scalar total一致、Nanbeige・6除外は維持。
- v18でカタログと提案キューのID集合が99件で一致。旧研究台帳R19/R20/R23・古いR21候補マニフェストは当時の状態を示す歴史的記録として不変。
- 実機の重み、HDD、取得進行、Gated同意、Torrent、approvedキュー、ファイル本体は変更なし。

関連分野：機械学習の評価設計、ソフトウェア供給網の版・ハッシュ照合、長期保存の差分容量管理。
