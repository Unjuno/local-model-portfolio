# R161／v68（2026-11-25）：並行選定の統合監査・4独立原本を維持・203取得停止

## 1.〈本論〉正本の修復方針

2026-11-25の研究作業で、旧v67 **248件／199有効**から先に**3原本の条件付き保全（251件／202有効）**を記録した直後、別の更新で**IVE-4B**を含む4原本の正本v68が作成された。このリポジトリの唯一の現行正本は [catalog/CURRENT.json](../../catalog/CURRENT.json) の **v68-20261125／252登録・203有効、SELECT56／CONDITIONAL147**である。研究の並行更新を理由に251件へ巻き戻してはならない。

**一次確認済み**：[現行4モデル正式overlay](../../catalog/revisions/v68-2026-11-25.json)、[4原本75ファイル完全Publisher SHA](../../manifests/drafts/r160-2026-11-25-four-small-trained-states-75file-publisher-frozen.candidate.json)、[派生252件](../../catalog/effective-portfolio-2026-11-25-v68.json)、[全203 STOP](../../catalog/readiness/v68-2026-11-25-r160-all203-gates.json)、[監査機械可読JSON](../../catalog/audits/2026-11-25-r161-v68-four-model-concurrency-reconciliation.json)。

**3原本先行版の位置付け**：[52件の先行原本source](../../manifests/drafts/r160-2026-11-25-three-edge-trained-originals-source-freeze.candidate.json)と[旧202件readiness](../../catalog/readiness/v68-2026-11-25-r160-all202-gates.json)は履歴・部分集合である。現行取得可否判断には使わない。先行3件に関する**全52ファイルのpath、bytes、Git blob SHA1、LFS SHA256、40桁revisionは、4原本版に完全一致**。矛盾は第4原本の追加に伴う件数だけであり、既保存モデル・重量SHAを置換する必要は無い。

## 2. 決定済み4原本（条件付き採用、実取得未承認）

| 保存原本と凍結コミット | 元の独立学習成果・保全価値 | Publisher全source |
|---|---|---:|
| [openbmb/MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B/tree/42433e90dad95123ab87729fd7011e7110629556) | SFT→領域RL教師→OPD最終蒸留による2.517B汎用/agent/コード原本。Base/SFT/Midtrainの別状態やGGUF変換を無条件追加しない。公式HubのApache2タグとは別にモデルrepo内に独立LICENSEが無い。 | 11 files／**5,043,807,977 byte** |
| [illuin/Ivonnet-0.8B](https://huggingface.co/illuin/Ivonnet-0.8B/tree/6a6a979489d262861ad3c34faaa1a763d1ce4baf) | Qwen3.5-0.8B系、4B教師から蒸留した独立した小型文書画像decision確率readout。1,044,560Bの**readout.safetensors**が必須、モデルweightだけでは復元不可。 | 21 files／**1,728,496,331 byte** |
| [illuin/IVE-4B](https://huggingface.co/illuin/IVE-4B/tree/1e65613dfd83ba6949883325fc5f4791dae56a46) | Qwen3.5-4Bの別full fine-tuningと学習済みreadout。Ivonnetの単なる量子化・重み形式の別コピーではない。作者のDecision Index/校正結果は独立したOwner試験ではない。 | 23 files／**9,102,712,961 byte** |
| [tencent/WeMM-Ecom-0.8B](https://huggingface.co/tencent/WeMM-Ecom-0.8B/tree/b40297975d72386f1c53103371d80ae0e5a9bd58) | Qwen3.5-0.8Bから異なるEC画像属性、商品動画、OCR、複数画像とhybrid推論への後学習。既取得のWeMM-Video音声同期モデルと用途を分離する。 | 20 files／**1,733,044,450 byte** |

公開元全75ファイルの論理合計は**17,608,061,719 byte**。学習原本同士の共有情報を誤って二重に数えないよう、出版社のGit/LFS SHAとbyteで確認した**12組の補助ファイル一致**について、重複20,076,087byteを差し引いた理論ソース参照量が**17,587,985,632byte**になる。ただし実際のユーザー媒体のハードリンク、すでに取得済みの親tokenizer、cache/staging、物理容量との一致は検査されていない。

## 3. 変更禁止と安全ゲート

- 旧v67の**248資産レコードの完全一致**を確認。v68では4独立モデルを追加し、すでに登録済みのSmaug DPO無検閲、Qwen Heretic LoRA、Aratako日本語TTS原本、Studioの別KL蒸留を削除・置換しない。
- 現[全203実行停止台帳](../../catalog/readiness/v68-2026-11-25-r160-all203-gates.json)、[全203研究キュー](../../queues/proposed-v68-2026-11-25.json)、[全203依存準備](../../catalog/preparation/2026-11-25-insurance-bundles-v68.json)、[147条件付きHubアクセス](../../catalog/access/2026-11-25-v68-conditional-hub-gates.json)のID集合が一致。全件`download_approved=false`、`ready_to_acquire=false`。
- 実モデル取得を始める条件は**所有者の具体的利用行為別LICENSE/NOTICE確認、正確な取得原本ファイルscopeの承認、Owner Dの現物SHA256と実空き200GB維持、staging/cache、推論コード審査、backend CUDA/torch/Transformers/codec/FFmpeg/モデルヘッドと量子化のABI、完全offline復元**。いずれか未解決でSTOP。
- 既取得116モデル・1,758ファイル／2,021,784,002,725byteは取得器の過去VERIFIED報告であり、今回所有者ディスクを再ハッシュした証明ではない。**モデル重みDL0、承認0、未審査コード実行0、既存削除0、Gated回避0**。

## 4. 2026年の規制事実

米国BISの[2026-11-19 91 FR 74970 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion Ruleのモデル重量管理ECCN4E091を撤回。これを**今後の全面公開禁止の証拠と解釈してはいけない**。仕向地・最終用途、出版社固有の商用/再配布ライセンスやGated化、個人情報・画像著作権は別に審査する。公開消滅は将来のストレスシナリオであり、日付や確率は未検証。

## 5. 変数表と次元検査

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 前提・定義域 | 型 |
|---|---|---|---|---|---|
| `B_3` | 先行3Publisher原本の論理bytes | byte（B） | 8,505,348,758 | 52件、所有者追加量ではない | 非負整数スカラー |
| `B_IVE` | 追加IVE-4B原本bytes | byte（B） | 9,102,712,961 | 23件、所有者追加量ではない | 非負整数スカラー |
| `B_4` | 統合4原本の論理bytes | byte（B） | `B_3+B_IVE` | 75件 | 非負整数スカラー |
| `B_dup` | Publisher完全同一ハッシュで二重に数えたbytes | byte（B） | 20,076,087 | 12組、owner実共有は未検証 | 非負整数スカラー |
| `B_unique` | 出版社ファイル単位の一意参照bytes | byte（B） | `B_4-B_dup` | ファイル内部分テンソル重複は含まない | 非負整数スカラー |
| `D_free` | 所有者媒体の現空きbytes | byte（B） | null／未測定 | 十進で200GB床を必須 | 非負整数又はnull |
| `n` | 実機性能の独立反復数 | 1（無次元） | 同HW・条件の反復 | 事前登録する最低30、現在0 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 測定量に準じる | 複合誤差分散 | 未計測でnull | 非負実数又はnull |
| `k` | 包含係数 | 1（無次元） | 不確かさの区間拡大 | 覆域モデル未定 | 正実数又はnull |

`B_4=8,505,348,758+9,102,712,961=17,608,061,719byte`、`B_unique=17,608,061,719-20,076,087=17,587,985,632byte`。**次元検査**：byte加算・byte減算のみで全て同じ単位。MiB/GiBと十進GB、推論ピークVRAMとディスク原本bytes、モデル名のactive/totalパラメータを混同しない。

## 6. H/T/D/C/UとERROR CHECK

- **H（反証可能）**：2つの独立decision状態、小型EC理解、RL+OPD一般agent原本を、過去248件を変更せずに条件付き保存登録すると、利用可能な別学習結果が増える。モデル品質優位は別仮説。
- **T（最小検証）**：原本4×75ファイルのコミット・byte・Git/LFS SHA照合、先行3原本52件と統合版の全パス完全一致、旧v67の248行完全同一、203全件停止と147アクセス・owner承認0を静的検査。実機ではEC・文書decision・コードagent各100件以上のholdout、同じCPU/GPU/driver/clock/backend/context/batch/量子化zero-point/入力長で各30回以上の速度・ピークRAM反復。
- **D（合否）**：静的来歴・数値・ID集合は**PASS**。使用者契約、D現物、リアルGPU、モデル品質、完全offline復元は**UNCERTAIN→取得STOP**。他方のIVE-4Bを消したり251件版に巻き戻す、未承認取得を生むなら**FAIL**。
- **C（対立仮説）**：IvonnetとIVEが同用途で余分な9GB分の独立価値を持たない、WeMM内部ECベンチの改善が独立画像で成立しない、MiniCPMの作者ベンチが再現しない、カスタムloaderにコード/ABIリスクがある。
- **U（不確かさ）**：Owner実SHA・HDD残量/依存・ライセンス、ベンチの訓練重複、CUDA/PEFT/推論コード、出版社ソースの将来版ドリフト。実測分布なしで`u_c`や`k`を数値化しない。

**ERROR CHECK**：R161監査では4モデルの原本rev、75文件、17,608,061,719byte、重複20,076,087byte、canonical252/203、116報告非重複、全203 STOP、147 access、approved0を照合した。旧先行3原本を最終正本と誤認しない。

学際性：①モデル知識蒸留と確率校正、②EC視覚情報検索、③コードagentと後学習RL、④ファイル同定・暗号学的供給網、⑤GPU/コーデックABI、⑥著作権／輸出管理／データ保全。

## 7.〈次に考える問い〉

**IVE-4BをIvonnet-0.8Bの約5.3倍の保存容量で並行確保することに、同条件の未知ドメインで校正誤差・誤判定率の統計的に有意な差が認められるか。その差が確認できなければ、教師側は研究HOLDへ戻すべきか。**
