# R131｜v56無検閲原本の独立全SHA再照合と正本ポインタ修復（2026-11-20）

**対象**：`Unjuno/local-model-portfolio`の現行正本v56（211登録／164有効、SELECT53＋CONDITIONAL111）。本研究は新規選定モデルを増やさない。配布元モデル原本と取得判断の整合性を高める。

## 1.〈本論〉独立した20ファイルの完全一致

既存の[正式v56固定源](../../manifests/drafts/r130-2026-11-20-frostwolf-and-phala-originals-fixed.candidate.json)と、この調査で新たに公式Hub API`?blobs=true`から取得した[別のpublisher SHA調査結果](../../manifests/drafts/r130-2026-11-20-frostwolf-and-phala-uncensored-originals.candidate.json)を照合。**FrostWolf 13/13、Phala 7/7、合計20/20のパス・整数byte・Git blob SHA-1／LFS SHA-256が一致**した。これは二つの証跡の**同一情報照合**であって、所有者Dドライブ上のmodel weight SHAの独立測定ではない。

| 正規保存候補 | 公開元固定revision | ファイル・論理容量 | ライセンス／依存を含む停止理由 |
|---|---|---|---|
| [FrostWolf LFM3-1.7B-abliterated](https://huggingface.co/FrostWolfAI/LFM3-1.7B-abliterated) | `fc0f808655210ef891515bad9b5195b03d89f11b` | **13ファイル／3,475,637,066byte** | LFM Open License v1.0 第5条の年商1,000万USD商用制約、custom LFM3 code／Owner CPU・GPU ABI |
| [Phala Qwen3.8-27B-Uncensored-LoRA](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA) | `588752bc181b999247f0e7df578bbc55d2b920e9` | **7ファイル／13,034,727byte** | 独立LoRAは親Qwen約27.78Bと実用版SGLangが必要。Adapter Apache-2.0と学習元のStanford Alpaca由来CC BY-NC4.0を別審査 |

FrostWolfの重みSHA`4064371dcfed8660f03d688dd7688aad48cce630fd3117ec30572a976352f165`はLiquidAI親`135922caef64e81e52af88ede8b7c3ddaa9d6da220a9737fb3065275dbfb4330`とも、GatedのOrcaRouter版`a11f80c25e8d70ead520fa8e686442d3807cbee12a6286182f40174d5ef34bf5`とも異なる。元親から独立して編集された重み成果であり、OrcaへのGatedアクセスを回避するためのミラーではない。

Phala`adapter_config.json`は`Qwen/Qwen3.8-27B@37561816e66b5b9153b1b64c10968c18c1e6f4a0`、rank=3/alpha=3を指定。PublisherはH200・専用SGLangと別のFP8 parentで拒否判定を示しており、同一ベンチでの再現や日本語性能を保証しない。**LoRAの13MBとフルモデルの再現可能容量を混同しない**。前回の61モデル／708file取得一致報告には親Qwenの取得一致は含まれていないが、現物不存在と断定しない。

法の事実：[米BIS 2026-11-19 IFR](https://public-inspection.federalregister.gov/2026-23529.pdf)は旧ECCN4E091モデルweight分類を撤廃。モデルごとの将来削除・全面禁止は観測されていない。実際に検証が必要なのは各モデルの現在のHub Gated状態、LICENSE正文、モデル/データ依存と所有者の使用目的。拒否率の研究一次文献は[Arditiら、arXiv:2406.11717](https://arxiv.org/abs/2406.11717)と[複数拒否方向の2026年反証、arXiv:2602.02132](https://arxiv.org/abs/2602.02132)を参照。実用性の外挿は行わない。

## 2.〈応用・転用例〉正本参照の世代ずれを修復

v56は採用済みなのに`CURRENT.priority_worklist_path`、`insurance_preparation_worklist_path`、`latest_adopted_selection_path`、`latest_selection_report_path`、`latest_manifest_draft`、`latest_active_readiness_audit`、`latest_conditional_access_audit`が**v55を指していた**。v56の実ファイルを確認し、[164研究キュー](../../queues/proposed-v56-2026-11-20.json)、[164 readiness](../../catalog/readiness/v56-2026-11-20-r130-all164-gates.json)、[111条件付きaccess](../../catalog/access/2026-11-20-v56-conditional-hub-gates.json)、[164依存準備](../../catalog/preparation/2026-11-20-insurance-bundles-v56.json)、[v56 overlay](../../catalog/revisions/v56-2026-11-20.json)、[R130判定](../../docs/strategy/130-v56-public-uncensored-selection-source-and-rights.md)へ参照を更新。旧209件とv56の2追加を含む211件の採否・重要度・sourceハッシュ・既存取得状況は変更なし。正式`queues/approved.json`は空。

## 3. 変数表と単位／整合条件

| 記号 | 意味（日本語） | 単位（SI/備考） | 定義 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `B_F` | Frost元publisher全ファイル量 | byte | 3,475,637,066 | 十進byte、Owner実増分でない | 非負整数スカラー |
| `B_P` | Phala LoRA Publisher全ファイル量 | byte | 13,034,727 | 親Qwen重量なし | 非負整数スカラー |
| `B_S` | 今回比較したsource合計 | byte | `B_F+B_P` | 2出版社20ファイル | 非負整数スカラー |
| `n_F` | Frost照合したパス数 | 1（無次元） | 13 | 件数整数 | 非負整数スカラー |
| `n_P` | Phala照合したパス数 | 1（無次元） | 7 | 件数整数 | 非負整数スカラー |
| `F_{min}` | 安全に残す物理空き | byte | 200,000,000,000 | 現物Owner HDD未観測 | 非負整数スカラー |

`B_S=3,475,637,066+13,034,727=3,488,671,793 byte`。ファイル一致数`n_F+n_P=13+7=20`。byte同士、件数同士の加算なので**次元チェックPASS**。両者を合わせても3.489GBは「Publisher版ファイルの額面」であり、親Qwen・キャッシュ・一時領域・ドライブ現在空きを含まない。容量4TB／200GB残床は別の実機STOP条件。

## 4. H/T/D/C/U・ERROR CHECK

**H**：独立Publisher証跡をファイル単位で照合し正本のv56参照先を修正すれば、誤って旧v55候補を転送する事故とハッシュ誤分類を防止できる。**T**：固定2repo・20全ファイル（n_min=20）で名前、byte、LFS/Git SHAを検査。テストは回帰静的解析のみ。Ownerで実際のファイルSHAを読み直し、同GPU/backend/clock/batch/context/量子化・zero-pointで各30以上のタスク評価を別途行う。**D**：PASS_METADATAは20/20一致・現行参照先統一・211登録164有効・approved0。FAILは単一SHA不整合・未承認重量転送・不適切なGated回避・ライセンス逸脱。UNCERTAINは本人の用途別許諾、物理HDDと完全offline復元。**C**：同じ上流API証拠に依存しているためPublisherの誤情報を二重計上している、モデル重みが変更/破損している、親Qwen配布とLoRA runtimeが非互換の場合。**U**：Publisherメタデータの信頼性、モデル学習元権利、ソフト実行ABI、Owner HDD/ファイルハッシュが主要。合成不確かさ`u_c`と係数`k`は反復測定がないので数値化しない。

**ERROR CHECK**：v56＝211登録／164有効（185モデル＋26データ）、source20／20一致、Publisher3 LFS重みSHA、全学習元許諾未確定、approved0、重量取得／既存ファイル削除0。今回の編集は**報告・参照修正・退行テストのみ**。

関連分野：計算機科学の暗号学的ハッシュ／デジタル保全、MLアラインメント研究、モデルと学習データの知的財産権、推論ソフトウェア供給網、統計品質評価。

## 5.〈次に考える問い〉

**SHAが20件すべて一致してもモデル復元を立証できないとき、次に取得すべき一次証拠は所有者HDDの実ハッシュか、親QwenとLoRAの同一ABI実行ログか。**

