# R158 / v66（2026-11-24）—116取得報告後に本当に差分となる保存順

[正本](../catalog/CURRENT.json)はv66 **246登録・197有効**、[新5原本134files・306,537,688,378byte](../manifests/drafts/r157-2026-11-24-post116-five-originals-medical-moe.candidate.json)と結合。**既取得と報告されたToto4m・LingSante-Pulse・Primal VAEは再取得しない**。最新116件は取得実行側の報告でありOwner D現物SHAを独立検証した証拠ではない。

## 推奨する未承認調査順位
1. **P0 [Smaug-Uncensored](https://huggingface.co/abacusai/Smaug-Uncensored/tree/e4bbcf7aec54ab72f4ce720569f3b3dc7b973087)**：公開元全32file **55,586,070,091byte**。うち親Qwen重みとPublisher SHA同一2file **5,934,994,296byte**。この2ファイルを実際のOwner媒体でSHA照合し、可能なら親をそのまま参照する。この2ファイルだけを差し引いた公開元残余は**49,651,075,795byte**だが、これはOwner追加保存量ではない。16シャードのSHA差異は別DPO学習の証拠だが内部共通tensorまで含む。作者の拒否率低下と中立性能は独立実機評価がない。本人ライセンス行為と容量・復元・品質・明示承認でSTOP。
2. **P1 [LingSante-3.1-air-VL](https://huggingface.co/inclusionAI/LingSante-3.1-air-VL/tree/1f398c937d6069994a156689636832c47d8c09be)**：Publisher74files・**249,721,924,398byte**。医療画像理解とエビデンス検索の別学習原本で高い保存価値。ただし250GB級負担とPublisher推奨4×141GB GPU、custom code/patch ABI、患者情報・臨床監督、実HDD空きとstagingは未検証。取得は承認されていない。
3. **P2 [Kitten Pico INT8 QAD](../manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json)**：同じrepoの8追加ONNX **63,628,208byte**。以前の33fileは既取得報告なので再取得しない。独立QADと単純変換か、音質改善・速度改善を固定HW/ONNX runtime/音声バッチ下で検証できるまで追加取得の優先度は低い。

**HOLD**：LingSante Flash MXFP4（元560B、packed elements294Bはモデル総数ではない、同HWの150B未満参考ピーク実測および完全file scope未確認）、AtomicChat Inkling rank1 LoRA（別編集だが作者MMLU品質低下・GGUF ABI不明）、Cartwheelロボットpolicy（三系統の第三者権利とsimulation-only未検証）。これらは優先候補へ自動昇格しない。

この研究順は配布禁止確率の予測値ではない。米BISの[2026-11-19 91 FR 74970 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)でモデルウェイトECCN4E091は撤回、個別のライセンスと仕向け・最終用途制限は別。容量最大4TB（十進）、最低空き200GB、所有者本人のSHA確認、依存の完全offline復元、Python/推論Backend/zero-point/context/batchの安全性、個別ファイルマニフェスト承認が閉じるまで**新規重量DL0・承認0**。

## H/T/D/C/U
**H**：同一Publisher重みSHAの重複回避を先行すれば、既取得112→116で報告された学習成果を重複取得せず、Smaugの独立DPOを将来保存できる。**T**：116報告ID結合、Smaug18Shard中2同一5.935GB、原本30+パスのSHAと個別LICENSE、P0/P1の総Publisher参照305,307,994,489byte、Owner現物再hash、固定HWにおける代表各30例の速度/品質測定。**D**：Publisher不変SHAが一致なら研究PASS、本人SHA・権利・バックエンド・許可はUNCERTAINでSTOP、偽承認はFAIL。**C**：Smaugの差分圧縮不可、医療モデルの実機不適合、音声QADの不成立。**U**：実ディスク・作者ベンチ・CLI ABIの未測定により合成標準不確かさu_c/kは算定不可。

関連分野はデジタル保存/ハッシュ、DPO/低拒否モデル、医療マルチモーダル、音声圧縮、GPU資源工学、ライセンス。
