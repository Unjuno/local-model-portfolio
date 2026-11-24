# R159 / v66 — 116取得報告の再照合、文書判定0.8B・4Bの原本確定、v65偽承認経路修正（2026-11-24）

## 1. 結論：既取得は再転送しない、独立学習成果は復元可能な原本で評価する

唯一の正式正本は現時点では **v66／246登録・197有効（SELECT56・CONDITIONAL141）** のまま。新たな正式overlay・ユーザー取得承認・所有者Windows Dの変更を行っていない。

最新の[取得台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**116モデルVERIFIED報告、1,758ファイル、2,021,784,002,725 byte**、1 Gated HOLD、歴史的最小空き1,022,413,893,632 byteを記載。これは今回所有者Dの実物を再SHAした事実ではなく、実行コード/親/codec/権利/完全オフライン復元の証明でもない。旧112モデル報告に比べ追加4モデル、44ファイル、1,235,859,638 byte。追加4件は **nchapman Qwen3.5-0.8B Heretic LoRA、Datadog Toto 4M、LingSante Pulse、Primal VAE**。同repo・rev・source byteの取得報告済みscopeは再取得しない。

**歴史的v65時点では取得済み116件と正式カタログの差分**は3repoだったが、現行v66の追加overlayで以下の3件はすべて正式登録済み。[機械可読監査](../../catalog/research/2026-11-24-r159-ledger116-reconciliation.json)にIDと取得コミットを残した。

| 取得済み報告にある未登録repo | 台帳報告byte | 正本対応の判断 |
|---|---:|---|
| [Datadog/Toto-2.0-4m](https://huggingface.co/Datadog/Toto-2.0-4m) | 17,727,464 | **v66に既取得として登録済み**。4.144M独立時系列原本、以前のTimestral5Mと別学習結果 |
| [inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0) | 66,946,541 | **v66に既取得として登録済み**。16.7M生理信号表現、channels.npzと128Hz preprocessing、privacy/医学的validityは未検証 |
| [ostris/primal_vae](https://huggingface.co/ostris/primal_vae) | 1,145,019,884 | **v66に条件付き既取得登録済み**。複数の独立VAE学習済み状態・latent互換とライセンスを個別評価。モデル総学習パラメータ数と復元依存を閉包するまで最終ロック保留 |

上記は**新規重みダウンロード対象ではない**。現行v66ではこれら3repoは追加ダウンロードなしで正式登録済み。ただし、同一原本の所有者現物SHA、外部ランタイム・個人の行為別ライセンス審査は未完了であり、取得台帳VERIFIEDだけで完全復元可能と断定しない。

## 2. 新規に研究用保存原本を確定した2モデル

2026年11月23日公開、[Illuinの作者一次技術説明](https://huggingface.co/blog/QuentinJG/ive-release)とHub本家immutable APIでモデル原本を調査。元のQwen 3.5を単に量子化したモデルではなく、別々のfull fine-tune/蒸留学習成果で、専用の小さな`readout.safetensors`を伴う選択肢確率判定器。共通コード・tokenizerのSHA一致は重複排除の手掛かりであり、別の重みチェックポイントの同一性を示す証拠ではない。

| 正式Publisher原本 | 不変コミット | 全ファイル＋Publisher正確byte | 研究判断 |
|---|---|---:|---|
| [illuin/Ivonnet-0.8B](https://huggingface.co/illuin/Ivonnet-0.8B/tree/6a6a979489d262861ad3c34faaa1a763d1ce4baf) | `6a6a979489d262861ad3c34faaa1a763d1ce4baf` | **21ファイル／1,728,496,331byte** | **P0／CONDITIONAL研究用source固定**。852,985,920 BF16要素。Qwen3.5-0.8Bから独立に蒸留・full fine-tuneされた軽量vision/document判定器。既存Intern-Decision 0.8B/元Qwenにはないドキュメント・画像に対する専用読出し学習結果。作者のvision index 47.6は本人環境未再現 |
| [illuin/IVE-4B](https://huggingface.co/illuin/IVE-4B/tree/1e65613dfd83ba6949883325fc5f4791dae56a46) | `1e65613dfd83ba6949883325fc5f4791dae56a46` | **23ファイル／9,102,712,961byte** | **P1／CONDITIONAL研究用source固定**。4,539,265,536 BF16要素、非生成の文書関連性・再ランキング・表／画像の確率判定を行う独立学習状態。作者はprivate new-domain score 40.3、vision index 65.5、ECE 1.6%を公表、実機第三者の独立再現なし |

[両者の44全ファイル不変パス・Git OID・LFS SHA256原本仕様](../../manifests/drafts/r159-2026-11-24-ive-ivonnet-ccore-immutable-publisher-source.candidate.json)。リリースの`release-manifest.json`記載のweight/readout/tokenizer SHAをPublisher treeのLFS SHAと重み別に照合し一致を確認。ただし所有者D現物の重量SHAチェックではない。

**依存を含めて保全する**：`readout.safetensors`、`decision_config.json`、`model.safetensors`または重み2shard、`tokenizer.json`、`source/src/decision_model/*.py`、`source/pyproject.toml`、LICENSE/NOTICE、実行テンプレートを必須範囲とする。ParentのQwen3.5重みを丸ごと重複取得する必要は、出版社のfull checkpointを復元する限りない。学習系譜の元のparent revisionは各`decision_config.json`で固定済みだが、使用者D親SHAは未測定。

**ソフトウェア実装前提**：作者の`source/pyproject.toml`はPython3.10+、PyTorch2.6+、Transformers 5.7以上6未満、safetensors0.4+、Pillow10+、高速化のための任意`flash-linear-attention==0.5.2`を明記。作者のテスト環境はH100/torch2.11等で、Windowsや利用者GPU対応、量子化zero-point/attention、推論ピーク・バッチは未検証。**custom Pythonがあるため静的保存のみ・ユーザー環境に未審査コードをインポート/インストールしない**。

出版社ブログの49ms（テキスト）・128ms（画像）はRTX PRO 6000での作者引用値。実GPUクロック、バッチ条件などが不明なのでユーザー環境性能として推論しない。また、作者のText Decision Index全体52.8は比較対象Perplexity Flash v1.3の55.1より低い。選定の理由は「全面的な最高性能」ではなく、**未知ドメインへの一般化を作者が報告した異なる訓練成果**および小型版の独立価値である。

## 3. 新規リリースを即採用しない候補・無検閲の保全

- [ccore/CCORE-Web-Coder-4B](https://huggingface.co/ccore/CCORE-Web-Coder-4B)：2026-11-23公開。コミット`b3b7eff06af48b7d850402fc8e85ea7f9aa2a9b9`に **30ファイル／33,809,262,632byte**。そのうちnative 5 Safetensors shardが **17,490,122,528byte**、他にF16/Q8/Q4 GGUF＋mmprojがある。同じ学習成果の配布フォーマットを複数の独立モデルとして数えない。ウェブHTML生成という価値はあるが、既存の強いコードモデルと同一条件の未学習・HTML品質評価がなく、大容量全形式保全の優先度は低い。**HOLD**。必要なら将来、native Safetensors＋必須config/tokenizerだけを選択し、GGUFの重複は除外する。
- **無検閲0.8Bの真の別学習結果は既に保有**：`nchapman/Qwen3.5-0.8B-Heretic-LoRA`は116件台帳で原本16ファイルをVERIFIED報告済み。rootとtrial002の重みSHAは同じ、trial004は別重みSHA。親`Qwen/Qwen3.5-0.8B`も取得報告済み。今回は再転送対象にしない。作者の拒否率主張は実機独立計測せず、実行可能性/親revision ABIを今後検証。
- **重み直接編集の評価に対する負の対照研究**：2026-11-22公開の[Filipinoに関する検証ブログ](https://huggingface.co/blog/Neurips-2026-MLIntern-Repro/the-weight-space-programming-illusion-gradient-fre)はQwen3-1.7B、Llama3.2-1B、Gemma3-1Bで構造と編集強度を揃えたランダム重み編集と狙いを定めた勾配なし編集の差が出なかったと報告。ただしコミュニティ記事（査読済み論文と断定しない）であり、既取得のRikiyaT Qwen0.8B/MATH500の別課題にそのまま外挿して選定を取り消さない。**少なくとも同じ編集範囲・サンプル・seedのrandom-edit対照を用いて再評価すべき**。
- **Pico QAD追加8 INT8 ONNX**：公式Publisher SHA8件は固定済みだが、取得台帳のPicoは33ファイルだけを報告。QADの学習成果が単なる変換と異なるという作者主張はあるが、重み差・音質・修復性は独立未検証。研究HOLDに保ち、**既存33ファイル再取得禁止**。
- **保留**：`GetCartwheelInc/cartwheel-control`はRP1ロボットの第三者メッシュ権利、`ricursiveAI/Ripple-65B-Preview`は容量・増分性能、`Metric-AI/OhanTTS`はGated/CC BY-NC/話者同意が未充足。Gated回避や無断利用をしない。

## 4. 最新の危険な承認経路を停止

**発見**：`scripts/build_v65_plan.py`は取得済みになった4 repoを古いowner store検知だけでスキップし、研究sourceから `approved-v65.json` に`approved:true`、`approved_by_user:true`、`license_text_reviewed:true`、`parent_dependency_rights_reviewed:true`という**根拠のない本人・権利確認**を書き出す設計だった。更に`preserve_execute.approval_for()`はその自動生成`v65-post112-exact-source-files-*`を一般に拒否していなかった。

**修正**：`build_v65_plan.py`は116件の正本実行台帳と照合した上でIVE/Ivonnet2件だけの非実行sourceレビューを作り、`review-v65-r159-UNAPPROVED.json`に全フラグfalse、`approval_ref:null`を出力。既存`approved-v65.json`を決して上書きしない。`preserve_execute.py`は過去のv65 synthetic approval_refの識別子を強制拒否する。新しい真正の所有者による固定file-scope別承認の仕組みまで禁止しない。

この修正は**GitHubの実装ソースのみ**。ユーザーのWindows D上に旧自動生成済みapproved JSONがある場合、そのファイルを今回削除・修正した事実はない。更新実行器を導入するまで旧承認JSONを実行に使ってはならない。

## 5. 追加原本容量、変数表、次元チェック

\[
B_{\rm new} = B_{\rm Ivonnet} + B_{\rm IVE}
             = 1{,}728{,}496{,}331 + 9{,}102{,}712{,}961
             = 10{,}831{,}209{,}292\ \mathrm{B}.
\]

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域/範囲/前提 | 型 |
|---|---|---|---|---|---|
| \(B_{\rm Ivonnet}\) | Ivonnetの出版社原本参照量 | B（byte） | 1,728,496,331 | 非負整数、21 Publisher files | スカラー・整数 |
| \(B_{\rm IVE}\) | IVEの出版社原本参照量 | B | 9,102,712,961 | 非負整数、23 Publisher files | スカラー・整数 |
| \(B_{\rm new}\) | 2原本の単純参照量 | B | 前2項の和 | 物理HDD増分、cache、依存量ではない | スカラー・整数 |

単位検査：右辺はいずれもbyteであり、和の左辺もbyteで整合。2repoで同じPublisher tokenizer SHAがあるが、物理D上の重複排除・一時領域の必要量は未測定。計画上の4TB総量・200GB空き安全床も元HDDの現時点での実測ではない。

## 6. H / T / D / C / U と反証計画

**H**：独立の非生成文書/視覚意思決定4B原本と0.8B蒸留原本は、116件報告済みの汎用LLMと異なる学習済み能力を復元できる。作者主張に関係なく、比べるべきは同条件の実際の文書決定品質。

**T**：一次Publisherの固定44ファイルSHA・byte・release-manifest照合を今回実行。次に各モデル最小200件の権利確認済み文書/画像選択問題を使用し、正答率・ECE/Brier・未知ドメイン低下・推論レイテンシを個別測定。同じ実機GPU/CPU型・clock、batch=1、画像解像度、context、Torch/Transformers/flash attention版、quant zero-point、各選択肢数、温度校正方式を事前登録。逐次停止はこの最小数まで禁止し、その後は事前規定の不確かさと検証条件に従う。Pico/無検閲など別用途を同一スコアに混ぜない。

**D**：Publisher metadataについては一致をSTATIC PASS。本人の利用行為許諾、実モデル重みSHA、オフライン再現、確定したWindows/GPU ABI、空き200GBの床とcache/staging、明示的ファイル単位承認のいずれも未完成なら**DOWNLOAD STOP／UNCERTAIN**。誤ったSHA/ライセンス不適合/偽承認は**FAIL**。

**C**：ベースQwenや既存のPerplexity/InternDecisionが現実タスクで十分、作者の新ドメイン性能が再現せず、Python/DeltaNet CUDA依存がowner環境に合わない、未取得のreadoutやlicenseで復元不能。

**U**：作者ベンチは独立再現なし、GPU clock、batch/context、文書分布、映像解像度・言語、依存APIバージョン、物理容量・権利は未確認。反復測定による分散がないため合成標準不確かさ \(u_c\)・包含係数 \(k\) は数値を捏造しない。

**学際的応用**：機械学習（確率校正・OOD評価）、情報検索・文書解析（再ランキング/KIE）、暗号学・デジタルアーカイブ（immutable provenance/Git OIDとLFS SHA）、法務・ソフトウェア安全保障（配布権・モデルコード供給網）。

## 7. 規制の事実と将来仮説

[米国BIS連邦官報2026年11月19日](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧モデルウェイトECCN 4E091を撤廃。これは個別ライセンス・輸出用途・Gatedの管理をなくす意味ではなく、将来すべてのopen weightsが一律禁止されるという証明でもない。したがって保全優先は、禁止の憶測より**現在公開されている独立原本の権利・不変ID・保存効率・独立再現性**で決める。

## ERROR CHECK

静的テストでは最新版116取得レポートの正確な件数/byte、v65で未登録だった3件がv66に正確にbackfillされたこと、44 publisher filesのSHA/byte、readout/トークナイザ必須、CCOREの多重形式HOLD、承認キュー空、旧v65 synthetic approval拒否を確認。またv66の有効未知総数15件／全未知29件に更新し、150B超研究HOLDにLingSante 560Bを追加して合計3件の安全ゲート一致を確認。オフラインunittestの全結果を記録してからコミットする。**新規重量DL・Gated回避・第三者コード実行・既存モデル削除はいずれも0。**

### 次に考える問い

許容できるストレージ量が同じなら、未知ドメインでの正答率が向上した4B原本と、バッチ1・低消費電力で運用できる0.8B蒸留原本のどちらが将来の自律性を高めるか。本人の実機と文書分布で測定する。
