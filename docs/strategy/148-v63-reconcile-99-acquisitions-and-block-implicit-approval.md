# R148／v63 — 取得済み99件の正本照合と誤った自動承認の停止（2026-11-22）

## 1. 結論：追加ダウンロードではなく、保存済みモデルの選定を完成させる

ユーザーは確定済み対象のダウンロードが完了したと申告。現行の[取得実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)も**99モデルVERIFIED／1,478ファイル／1,879,994,309,866byte**、1件Gated HOLD、履歴の最低空き1,167,311,646,720byteを報告する。この研究は**所有者Windows Dドライブの現物SHAを再計算していない**ため、ledger VERIFIEDを「全依存・LICENSE・完全オフライン復元済み」と宣言しない。

v62の231登録／184有効の中に、99件のVERIFIEDモデルのうち**95件だけが存在**。4件は技術価値があり、報告上すでに全ファイル検証済みなのに正式ポートフォリオ未登録だった。**不要な再取得を禁止したまま4件を登録**し、v63を**235登録／188有効（SELECT55・CONDITIONAL133）**とする。旧231の全判定・原本情報は変更なし。

[新4モデル全49ファイル・固定SHA](../../manifests/drafts/r148-2026-11-22-ledger99-four-untracked-trained-sources.candidate.json)／[8件メタデータ差分・RFD4別重量を区別した9件監査](../../catalog/research/2026-11-22-r148-ledger99-immutable-revision-drift.json)／[機械可読の決定と検証](../../catalog/decisions/2026-11-22-r148-v63-ledger99-selection-and-approval-gates.json)／[v63 overlay](../../catalog/revisions/v63-2026-11-22.json)。

## 2. 追加ではなく取得済みから正式選定する4資産

| 99件の既取得報告に含まれていた未登録モデル | 固定した全Publisherファイル | v63判定 | 価値・限界 |
|---|---:|---|---|
| [RikiyaT/Qwen3.5-0.8B-weight-space-programming](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming/tree/d1671a178705bcab7644806d23c535517f35723b) | 17件／**1,779,420,899byte** | **SELECT** | Qwen3.5-0.8B親は既存SELECT。作者の[重み編集ログ](https://github.com/RikiyaT/lm_understand-logs)でMLP 15/19層のdown_proj重み合計131,072要素を勾配なしで直接編集。Publisher full BF16 weightと親のSHA・byteは異なる。作者MATH-500評価（7.9%→48.1%）と500問×4試行の編集版51.0%は本人実機再現なし。比較に使われたbase smoke 25問と編集2000回答は標本設計が異なり独立同条件の優越証明にはならない。 |
| [JetBrains/Mellum2.1-12B-A2.5B-Thinking-MTP](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-MTP/tree/d55846102dd1c047e95d4841070f88290227c3b7) | 17件／**25,165,148,781byte** | **SELECT** | 思考・コーディングMoE原本5シャードは[通常Thinking](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking)のPublisher重みSHAと全5件一致。MTP予測ヘッド**856,767,160byteだけが独立追加**。通常Thinkingを二重取得・別資産化しない。作者報告1.4〜1.8倍のMTP投機生成と約90%draft受理は、vLLM 0.33+／Transformers 5.20+の特定ABI条件で、ユーザーHW再測定なし。モデルメタのBF16総要素12,578,294,528、`total`12,149,923,072との差428,371,456はMTP頭に対応すると推測されるがローカルtensor censusはしていない。 |
| [speechbrain/spkrec-ecapa-voxceleb](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/tree/0f99f2d0ebe89ac095bcc5903c4dd8f72b367286) | 10件／**89,133,738byte** | **CONDITIONAL** | VoxCeleb学習済みECAPA話者埋め込み・分類器。外部音声モデルの別学習依存として高価値だが、既存モデルへの必須依存と断定しない。顔・声の本人同一性を扱うため、利用権・プライバシーおよびSpeechBrain/.ckpt実行安全性の審査を残す。 |
| [kyutai/mimi](https://huggingface.co/kyutai/mimi/tree/89091b3e466eb6a9d11e537bf26b144f194978f7) | 5件／**384,657,055byte** | **CONDITIONAL** | F32**96,151,393要素**の12.5Hzストリーミング音声codec。音声生成・音声理解の学習済み補助原本として登録し、CC BY 4.0の帰属表示、音声データ権利、入力・出力codec ABIとオフライン復元を別確認。 |

4配布元計**49ファイル／27,418,360,473byte**、公開元LFS SHA256**12参照**。これは**新規取得量0byte**であり、全て既存99件VERIFIED報告の一部。採用に伴ってHDDへ追加コピー・重み削除・再量子化はしていない。

## 3. 既取得99件とカタログrevisionの不一致9件

照合基準は**Hubの40桁immutable revision毎の全Publisherファイル集合とLFS SHA256／Git object OID**。旧選定時の`upstream_revision_sha_observed`と99件ledger内`revision_sha`が異なるrepoは9件。

**8件は重みファイル集合・重量SHAが一致**。gradium/phonon-31m-en、ibm-granite/speech-5.0 470m/2b、PaddleOCR-VL-1.5、meta Muse Glimmer 30B/assistant、Qwen3.8-27B、OLMo Meditron。README／tokenizer_config／chat_template／Paddleの`modeling_paddleocr_vl.py`など非重みファイルが変更されたケースがある。**学習済み重みが同じでも、推論テンプレートやカスタムコードを無条件に同じ挙動とみなさない**。取得済みrevisionを保全し、必要に応じその時点のコードを同梱する。

**1件は重みそのものが異なる**：[nvidia/RFD4-Proteina](https://huggingface.co/nvidia/RFD4-Proteina)。v62旧観測 `cf31b93509df5af854c7f6ad704f5c83c77c0698` に対して、ledger取得報告は `5ec66c399bf0b48727ab24e6b298dcf33864fa07`、**17ファイル／5,236,405,470byte**。前者の`transformers/model.safetensors`と取得側はSHAが変化し、後者には`adapter/adapter_model.safetensors`、`base/model.safetensors`、新`antibody/*.ckpt`が追加されている。**同じ学習済み結果を取得したとの推定を禁止**。当該資産は既存CONDITIONALを維持し、どのmerged/root/adapter/抗体重みが復元の正本かを将来の個別検証対象にする。既存取得側を削除せず、変更された原本を勝手に再取得しない。

## 4. 高リスク：取得計画をユーザー承認に自動変換していたコードを修正

最新mainの`scripts/build_v62_plan.py`を調べたところ、**非実行の研究キュー**から`approved_by_user: true`、`license_text_reviewed: true`、`parent_dependency_rights_reviewed: true`を自動生成していた。同種の誤りが`build_v59_plan.py`、`build_repair_plan.py`、`prepare_session_approvals.py`にもあった。

**対処**：将来の計画生成は全件**UNAPPROVED（承認・license review・親依存権利のすべてfalse）**とし、`approved-vXX.json`や既存ユーザーの所有者側の承認ファイルを上書きせず`review-*-UNAPPROVED.json`へ書き出す。また`preserve_execute.approval_for()`では、2026-11-19の一般的な取得意向をモデル毎の許諾確認にすり替えた旧自動承認`approval_ref`を拒否する。合法な所有者の新しい明示的なファイル別承認を妨げず、無断取得を止める。

この修正はGitHubのソース更新であり、所有者Dドライブ上にある旧approvalファイルを遠隔削除・修正・再ハッシュした事実ではない。旧承認ファイルを更新済み実行器へ渡しても、既知の自動承認refは拒否されることをテストする。リポジトリ`queues/approved.json`は**空**。

## 5. 今後の追加取得候補は99件との差分だけ

[正本から再作成した99件取得後の非実行キュー](../../queues/proposed-v63-r149-after99-11-research-only.json)では、残る11 sourceのうちP0〜P2は**10repo／68,544,170,933byte**のPublisher参照、P3 Ripple65B **129,572,889,973byte HOLD**。この数字を「今すぐ取得するべきリスト」やユーザーDの空き容量と混同しない。

ユーザー申告どおり取得済みは再取得しない。次に優先するのは、RFD4別revisionの依存と、既存の99件のowner現物SHA・ライセンス・実行環境・完全オフライン復元。**99/99のrepo IDの台帳照合は完了しても、184→188件の全件オフライン復元が完了したわけではない。** 出版社の公開停止の可能性は反証不能な確率として数値化しない。輸出管理上の主張は別途最新法令を一次資料で確認し、既存の一般的禁止断定を継承しない。

## 6. H／T／D／C／U

- **H**：99件VERIFIEDの既存repo IDについて、未登録4件を独立したtrained/edit成果として収録すれば新規ダウンロード無しでカタログ照合漏れは0になる。また歴史的な一括許可を個別許可に変換する危険なコードを停止できる。
- **T**：repo IDで99報告をjoinし4欠落を検出。4モデルの全49 Publisher path、bytes、Git OIDとLFS12件を同一40桁revで検証。9つの旧rev→取得revのモデル重みSHA・非重み差分を検出。旧231行不変、188有効、133条件付き、SELECT55、approved0をテスト。承認器の旧自動許可refは正確なファイルSHA・flagsがtrueでも拒否する。
- **D**：静的台帳・SHA・参照が一致ならメタデータのPASS。RFD4相違を同一と扱う、4件の二重取得、旧参照のsilent rewrite、自動許可trueを発生させた場合FAIL。owner HDD実ファイル、各ライセンス行為別承認、runtime ABI、実装ピークRAM／完全復元は未測定のためUNCERTAINで、追加取得はSTOP。
- **C**：一部依存sourceが実際に必要ない、改変モデル品質が再現しない、JetBrains MTP速度が所有者GPUに載らない、RFD4の別rootが意味的に同等だが本研究では未確認である可能性。
- **U**：第三者ledgerのみの現物検証、作者の不均等な数学ベンチ、旧メタデータと現runtimeの差、音声本人権利、ownerのドライブ空き・cache/staging・GPU・CPU・KV cache/量子化/zero-point・コンテキスト・バッチに不確かさが残る。独立測定が無く、合成標準不確かさ`u_c`および包含係数`k`は算定不可。

連携分野：①機械学習・モデル編集と投機復号、②音声認識・生体情報保護、③ソフトウェアサプライチェーン・ハッシュ、④ライセンス・取得と管理的承認の分離。

**作業の境界**：新規重量ダウンロード0、新規取得承認0、所有者Dドライブ現物更新0、未審査モデルコード実行0、既存231の改変・削除0。

