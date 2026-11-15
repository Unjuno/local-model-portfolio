# 規制連鎖シナリオを主軸にした保存優先度と安全審査（v5・2026-11-03）

## 2026-11-15追補（main／調査当時v37、最新はCURRENT参照）

- **歴史と現行の分離**：この文書のS1/S2/S3はv5時点からの*仮説的な保全順序*であり、実際に成立した禁止の順序ではない。唯一の正式選定正本は`catalog/CURRENT.json`。現行の150B以上は量子化後の同一条件実測・RAM・品質・権利等の非補償ゲートを満たす場合に限り個別審査を許し、v8の歴史的な絶対除外を現在の規則へ持ち込まない。
- **確認済み制度**：[EU AI Act Article 53](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)と[欧州委員会のGPAIガイドライン](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)は提供者への義務と条件付きのopen-source例外を定める。**一般の公開ウェイト保有・ローカル保存が一律禁止されたことを示す規定ではない**。Gated、ライセンス、提供者義務、用途禁止、将来の配布停止予測を別々に記録する。
- **モデル別の現在の事実**：`WhissleAI/steer-tts`の[HF作者カード](https://huggingface.co/WhissleAI/steer-tts)がコードMIT／重みCC BY-NCと述べる一方、発行元[固定GitHub LICENSE](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/LICENSE)はコード・重み・音声ともCC BY-NC 4.0＋Whissle独自条件。古いGitHub LICENSEにも同条件があり、**変更日時の確証ではなく配布元間の矛盾**として扱う。保守的な取得権利判断ではコードMITを推定しない。3モデルrepoのGated本人権限は不明。
- **同一学習成果の重複防止**：SteerTTS originalは既存CONDITIONAL研究選定を保持。Edgeは作者が別v2音響学習を主張するがHF量子化タグもあり、Nanoは微調整タグがある。両者の新規登録は同一revisionの重み/テンソル差・独自能力・ライセンスが確定するまで**研究HOLD**。通常のint8/int4形式違い、ONNX/C/PyTorch実装差は新しい学習済み資産としない。
- **安全条件**：[全3版の一次ソース調査](../docs/strategy/2026-11-15-steertts-source-license-and-duplicate-weights-decision.md)と[機械可読根拠](../catalog/research/2026-11-15-steertts-3build-source-license-risks.json)。本人Gated許可、全構成の総数、固定40文字revisionとSHA、必須依存、ライセンス本文、実HDD空き、明示的取得承認が揃うまでは本体取得・実行・承認済みキュー投入をしない。本追補によるSELECT/CONDITIONALの変更・ダウンロード権限の追加は0。


## 予測主導の目的

保全の第一の判断軸は、ユーザーの「悪用されやすい能力が先に制限され、その後強力なAI一般、最後に公開ウェイト全体へ制限が波及する」という**3段階の仮説**である。これは現在のGatedリストを機械的に先に取得する方針ではない。将来の規制日程・発生確率を観測できていないため、モデル単位の「禁止予定」は表明しない。

- **S1（想定する先行制限）**：無検閲・安全制御変更、強い自律操作、顔や声の合成、画像・動画生成、権利や個人情報に関連する学習データ
- **S2（高性能モデルへ拡大）**：汎用LLM/Omni、医療・科学、ロボット、世界モデル、高度な3D
- **S3（全面化）**：Base、学習・評価データ、実行環境、一般のモデルウェイト・依存

## 別軸で記録するもの

**A. 規制シナリオ上の消失順位**は[v5予測オーバーレイ](../catalog/revisions/v5-2026-11-03.json)の132件すべてに記録する。各レコードにはS1/S2/S3、用途/想定される制限理由、現在の観測情報、調査順位を明示する。性能に関する出版社の主張は独立測定から区別する。R0/R1/R2は履歴区分とし、調査順を統制しない。

**B. 現時点の法的・技術的な取得資格**は完全に独立した必須条件。公開URL、Gated/手動許諾、LICENSEの正文、親モデル・Codec/依存、取得ファイルのバイト数と完全revision、RAM/HDD、安全性と本人同意、ユーザー承認を満たすまでは取得しない。S1のHOLD/BACKLOGは**優先的な権利/代替/重複調査対象**だが、選定・ダウンロード可に格上げしない。

**C. 確定事実と仮説**：観測したGated/Removed/利用条件/公式法令は事実、S1からS3への波及と未検証の悪用可能性は仮説。将来「すべての重みが禁止される」は最悪ケースへの備えであって法的な現状説明ではない。これにより「危険だから今すぐ無条件取得」とは判断しない。

## 正式制度との区別

EU AI Act第51条は特定の汎用AIモデルについて、高影響能力や訓練計算量に基づき**システミックリスクの規律**を設ける。一律に「高性能な重みの所有・公開をすべて禁止する法律」ではない。システミックリスクのGPAIには評価・リスク低減・報告・セキュリティ措置等の義務がある。すべての特化モデルが同じ法的区分に該当するわけではない。

一次法令： https://eur-lex.europa.eu/eli/reg/2024/1689/oj
EU当局の解説： https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-general-purpose-ai-model-one-systemic-risk

## 今回の実例：Idol（物体の単一画像→3DGS）

- SNS由来の問題提起：[2026-11-02 X投稿](https://x.com/TaroKichijo/status/2117218974404620414)。投稿者の「8GB VRAM程度でも動く」は推測であり性能検証ではない。
- [公式SDK](https://github.com/speridlabs/idol-sdk)と[Hugging Faceモデル本体](https://huggingface.co/speridlabs/idol)に一次資料がある。モデル本体はpublic・Apache-2.0表示。SDKのGitHub LICENSE本文はApache-2.0。2026-11-03確認。
- モデル本体のHub SHA：`2731c2291fc65a797c5cb627a5e5526fc1490902`。全ファイル16件・3,128,391,338バイト。必要7ファイルは3,078,990,585バイトで、4つの重みには上流完全ファイルSHA-256がある（[候補マニフェスト](../manifests/drafts/idol-core-2026-11-03.candidate.json)）。
- SDKの固定コードSHA：`4702a7f00850e34b6e83a2170cc123c3e9570744`。インストール前にコード/依存/OS/ABI安全性を別途評価。
- **必須の別モデル**：`facebook/dinov3-vith16plus-pretrain-lvd1689m`（manual Gated、独自利用条件、3,362,457,679バイト全repo）。既存の`facebook/dinov3-vit7b16-pretrain-lvd1689m`と同一ではない。さらに`black-forest-labs/FLUX.2-dev`のVAEはGatedで、v3で別資産として既に選定済み。アクセス許可のない依存はスキップして「実行可能」としない。
- 配布者によるVRAMピークは**7.2GB**。50ステップ、262,144 Gaussians、1GPU、8画像の中央値はH100（80GB VRAM）で6.7秒、RTX 3080（10GB）で46.2秒。短い「2秒以下」という宣伝値と直接比較せず、リクエスト時間の測定条件を採用。独立測定なし。
- 安全上の仮説：写真を3D化する技術が個人や機微対象に悪用される可能性。ただしモデルカードは**物体の3D再構成**を主目的としており、本人なりすましや規制予定は実証されていない。
- **判断**：IdolはR1/conditional、必須DINOv3 ViT-H+はR0/conditional（すでにmanual Gated）。どちらもダウンロード・実行承認0件。

## H / T / D / C / U：シナリオの反証

- **H（仮説）**：2026-11-03から12か月に新しく観測される配布制限は、S1に先行し、S2・S3へ広がる。既存Gatedは新規イベントに加えない。法的な改正以外に配布者の変更も別カテゴリーで記録する。
- **T（検証）**：全132件を週次で観測し、初回12週間で中間検討、12か月で本評価する設計（各回 n=132）。公開配布元API・LICENSE・配布者の変更告知・法令原文を比較。現段階で定期チェックの実装・実施はしていない。
- **D（判定）**：PASS＝S1先行・S2/S3への波及を複数の独立配布元の一次資料で確認。FAIL＝S2/S3が先行、または初めから一律の制限となる。UNCERTAIN＝事例不足/原因不明/観測期間不足。現在UNCERTAIN。予測確率ではない。
- **C（対立仮説）**：Gatedは商用契約やプライバシー対応であり規制ではない、全面的な制限が来ない、またはS1より先に高性能一般を制限する可能性がある。重み配布でなく用途/APIを規制する場合もある。
- **U（不確かさ）**：各国制度、公開履歴、配布者の非公開理由、データの偏り、モデル性能の独立評価欠如。校正された確率モデルはなく、合成標準不確かさ`u_c`と係数`k`は現時点で算定不可。

一次根拠：[米NTIAオープンウェイト報告](https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations/recommendations)、[Hugging Face Gated](https://huggingface.co/docs/hub/models-gated)、[International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026)。これらは特定モデルの近い将来の禁止を証明しない。

## 禁止する近道

- 無許可のGated・Private取得、配布元の制限回避、匿名ミラーへの無条件依存。
- 実在人物の無同意の顔・声複製/なりすまし、非同意の性的合成、未成年の性的生成、機微データの無断取扱い。
- 自動モデル実行/任意コードimport/依存自動インストール。モデルを「保存した」ことと「安全に実行した」ことの混同。
