# R165 — v71公開後整合監査、QJev校正の親重み照合、取得STOP保護

**対象：2026-11-25、Unjuno/local-model-portfolio、正式v71 260登録・210有効。**

## 1. 発見と修正

v71正式追加は先行の別作業で実行され、Aurum-2B-UncensoredとQJev-1.5B-AbliteratedがCONDITIONAL選定済みとなった。これを新しい重複overlayで再登録せず、正式v71の履歴を保持した。

公開版を新規チェックアウトした当初、792テスト中38件が失敗した。主要原因は、CURRENTがv71を示す一方、条件付きアクセス評価の参照がv70の152件のままで、v71の154件と結合していなかったこと、readiness/CURRENTとestimates/CURRENTがv70を参照したこと、現行CURRENTのbudget_statusと物化済みv71のbudget_statusが文字列だけ不一致だったこと、過去v58～v70のテストが新しいv71を受け入れなかったこと。正式登録された2件の学習状態や旧258件の判断を変更する必要はなかった。

**修正**：v71専用のアクセス台帳154件（公認されたGated例21件のまま）をCURRENTから参照する。readinessとestimatesはv71/260/210へ同期。予算台帳の一つの不一致フィールドだけを物化済み正本に合わせる。旧版の不変資産・旧revisionsは書き換えず、テストのlive-pointer判定をv71まで拡張する。

**結果**：公開版の取得後修復を施した状態で794件PASS・1件SKIP。v71の210件すべての取得実行ゲートはSTOP、queues/approved.jsonは空。これはPython stdlibのメタデータテストでありOwner HDD/モデル推論の測定ではない。

## 2. QJev parent-head SHA の追加一次検証

AnkitNayak-dev/QJev-1.5B（Aligned parent）のPublisher固定コミットは、2026-11-25のAPI参照時点で **42e4c9e69897d3924e208f938227c072b24a53fa**。その decision_head.safetensors のLFS SHA256は、編集後AnkitNayak-dev/QJev-1.5B-Abliterated のものと同一の **ec01a57a7e61c3ee052a5b7ea939cb4e5ae2cfacf2fe84f5e1d67d962805bebe** だった。

一方、元backbone model.safetensorsのLFS SHA256は **48fea648140195c0b5f38a9dc79c48ab63556f221166cc69edb5d15746a6fea7**、編集後backboneは **5272c8590c74528d5f8604a6a058ddc6a8908089bfb92c010fd73fabd36c796e** である。

**事実**：学習済みヘッドの公開重みは同一でバックボーンは異なる。**推論**：ヘッドへの隠れ状態入力の統計分布が変わりうるため、編集後の確率校正が維持されたと結論するのは誤り。**不確かさ**：編集前後のECE/Brier、選択肢順序不変性、見落とし率は同一入力・同一backendでの独立比較前で未測定。

一次ソース：[Aligned parentのファイル](https://huggingface.co/AnkitNayak-dev/QJev-1.5B/tree/42e4c9e69897d3924e208f938227c072b24a53fa)、[Abliterated編集原本](https://huggingface.co/AnkitNayak-dev/QJev-1.5B-Abliterated/tree/1df03fe639898580f53a984355b7cbf3cca24bf4)、[機械可読のSHA照合結果](../../catalog/research/2026-11-25-r165-qjev-parent-head-immutable-provenance.json)。

## 3. H / T / D / C / U

**H**：編集済みモデルが元ヘッドを再利用しても、校正された確率の性能を維持できるとは限らない。

**T**：今回、公開元parent/editedの重みSHAとhead SHAを別々に確認し、原本のID/ファイル数を変更せずメタデータを固定した。次は同じ正答ラベルを備えた最低200件の権利確認済み選択肢問題、同一tokenizer/前処理/量子化・backend/温度・batchでBrier・ECE・action abstentionを独立評価。レイテンシは同じCPU/GPU、クロック、バッチ1、文脈長で最低30試行以上の中央値とばらつきで比較する。

**D**：出版社SHA一致／不一致の再現と現在の210件取得STOP・承認0はSTATIC PASS。品質の非劣性・所有者現物SHA・LICENSE行為権・完全off-line復元・GPU ABIはUNCERTAIN/STOP。偽承認、SHA不一致、ライセンス不適合をFAILとする。

**C**：拒否編集が隠れ状態分布を変えずに元ヘッドの校正性能を保つ可能性は残るが、同じ重みSHAだけでは証明できない。逆に保存対象2原本が既存モデルと機能的に重複する可能性もある。

**U**：モデルのPublisherメタデータは取得済み利用者HDD内容ではない。モデル出力反復、ハードウェア/クロック/OS/ABI、独立ベンチマークの分散、ライセンスとステージング容量の不確かさが未測定であり、合成標準不確かさと包含係数を数値推定しない。

関連分野：暗号学的ソフトウェア供給網検証、統計的確率校正・意思決定、モデル圧縮/安全な重み編集、著作権・輸出管理。

## ERROR CHECK

本監査は正式v71選定の260資産を変更せず、条件付き154件へのアクセス台帳正確な紐付け、210 activeの取得STOP、旧116取得報告の重複禁止、正本budget一致、Aligned parentの新規SHA照合を検証した。ユーザー所有者HDDの独立再SHA、実行・削除、新規モデル重みダウンロード、無断承認、Gated回避は実施していない。

**次に考える問い**：ヘッドのSHA一致がモデル性能を保証しないなら、配布停止前に保存すべき最小単位は「モデル重量」か、それとも校正済み入力分布・前処理コード・検証用データも含む再現可能な研究パッケージか。
