# v55取得候補の確定・小型無検閲原本のsource固定・親モデル復元性の再監査（2026-11-20）

> **用途：調査と選定の更新。モデル本体の新規取得・Gated突破・ライセンス同意・実行権限付与ではない。**
> 今回のGitHub書込は `strategy/2026-11-03-01-risk` の本資料、[全件判断JSON](../../catalog/proposals/2026-11-20-v55-preservation-priority-and-parent-proof.json)、[未承認固定source](../../manifests/drafts/2026-11-20-frostwolf-phala-immutable-source.candidate.json) の3ファイルのみ。mainのCURRENT・承認キューは更新しない。

## 1. 〈本論〉まず現行の正本と取得台帳を固定

- 本調査時にmainの正本が **v54（207資産/160有効）からv55（209資産/162有効）へ更新**された。以後は `catalog/CURRENT.json` が示す **v55-20261120**、`catalog/effective-portfolio-2026-11-20-v55.json` を比較基準とする。v55で新たに登録された `OVHaiLLM/Olala-v1.0-mini-7A1B` と `-base` は本件の追加候補と重複させない。
- 過去の[61モデル・708ファイル・409,835,119,252 byte取得報告](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**台帳上の報告**であって、今回所有者Dドライブの全ファイルを独立再ハッシュした事実ではない。
- `queues/approved.json`は**0件**。実物ドライブ容量、今の空き、ユーザー個別のライセンス適用、モデルコード/ABI、完全オフライン復元の全条件を未承認とする。
- 目的は**独立した学習済み状態と依存・評価データを再取得困難化に備えて合法的に保全すること**。モデル数だけ増やす、同じ量子化版を重複する、公開停止確率を創作する方針は取らない。

## 2. 既存R128の4配布元はsource確定を維持

既存[4件の非実行キュー](../../queues/proposed-v54-r128-first-four-delta-source.json)に記録された**101ファイル・6,127,042,272 byte**について、2026-11-20にHugging Face公開APIの**固定40桁revision**へ読み取り専用照会を行い、全選択ファイルのパス・バイト数、該当するGit blob SHA-1およびLFS SHA-256参照が一致した（4配布元ともPASS）。ELYZAは公開元66ファイルのうちNTFS非互換旧CSVを除く65件。Aionは公開元12件のうち指定11件。無差別にリポジトリ全体をmirrorしたとは呼ばない。

| 研究上の保存順 | source repo ID | 原本の固有価値 | 固定publisher source（十進byte） | 選択ファイル | 判定 |
|---:|---|---|---:|---:|---|
| 1 | [elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | 日本語能力・過去モデルの評価原本 | 7,606,817 | 65 | 源同一性PASS、権利とD媒体は未承認 |
| 2 | [CohereLabs/aya_dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 多言語・人手注釈データ | 140,160,376 | 6 | 源同一性PASS、データ利用目的は別審査 |
| 3 | [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 0.5B級多言語ASRと独立CTC head | 1,385,998,807 | 19 | 源同一性PASS、runtimeと再現精度未実測 |
| 4 | [microsoft/Aion-1.0-Instruct-2.3B](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B) | 独立2.3B小型SLMの後学習原本 | 4,593,276,272 | 11 | 源同一性PASS、custom code/ABI未承認 |
| 合計 | 2モデル＋2データセット | 評価に必要な多様性も確保 | **6,127,042,272** | **101** | **正式取得承認0** |

**確定の意味を限定**：remote metadataで固定済みファイルの存在と元のhash参照を再照合した。重み/データ本体を新たに読み込んでローカルSHA-256を照合したわけではなく、本人の正規取得許可の証明ではない。R128より大きい旧R125/R126や62件目以降の原本を勝手に初回バッチへ混ぜない。

## 3. FrostWolf／Phalaを直接調査して保存候補を再分類

### 3.1 第5候補：FrostWolfの小型無検閲BF16学習結果

- 配布元：[FrostWolfAI/LFM3-1.7B-abliterated](https://huggingface.co/FrostWolfAI/LFM3-1.7B-abliterated)。HF公開・非Gated、約**1.7288B**パラメータ。固定rev `fc0f808655210ef891515bad9b5195b03d89f11b`。
- 配布元公開ツリーの**13ファイル・3,475,637,066 byte**を、[全ファイル固定の未承認候補](../../manifests/drafts/2026-11-20-frostwolf-phala-immutable-source.candidate.json)に保存。重み`model.safetensors`は3,457,635,448 byte、配布元LFS SHA-256は`4064371dcfed8660f03d688dd7688aad48cce630fd3117ec30572a976352f165`。**重量ファイル本体は転送していない**。
- 元の`LiquidAI/LFM3-1.7B`と別の拒否方向編集済み学習結果。現行の`orcarouter/LFM3-1.7B-abliterated`は別作者・別重みでGated。FrostWolfをその同一SHA正規ミラーと扱わず、OrcaのGatedも回避しない。FrostWolf同作者のGGUFは**別学習資産ではなく同じ結果の変換形式**なので重複保存しない。
- AUTHORモデルカードの**120試行後の拒否1/100・KL=0.0555**は作者の選択済み評価であり、客観的な総合性能、無害性、制限予定を証明しない。日本語・ツール呼び出し・推論能力の独立比較は未実施。
- [当該revisionのLICENSE](https://huggingface.co/FrostWolfAI/LFM3-1.7B-abliterated/blob/fc0f808655210ef891515bad9b5195b03d89f11b/LICENSE)は**LFM Open License 1.0**。Section 5に年商1,000万USD以上の法人の商用利用条件があり、本人がどの行為を行うかの契約審査は未了。`configuration_lfm3.py`、`lfm3_conv.py`、`modeling_lfm3.py`のカスタムコードを無許可でimportしない。作者のreproduce環境はRTX 4090 / 24GB、CUDA 13.2、ドライバ621.14、Transformers 5.22.2、Torch 2.15.0だが、**ユーザー実機での動作・速度は未測定**。

**判定**：別系統の原本価値と小容量から**追加CONDITIONALの推薦を確定**。ただし今回の提案はmainへの正式登録ではない。本人の行為別ライセンス/静的コード/実機空き/40桁source指定の明示承認を終えるまでは**取得キューへ入れない**。

### 3.2 第6候補：Phalaの13MB LoRAは親と学習データを先に閉包

- 配布元：[PhalaCloud/Qwen3.8-27B-Uncensored-LoRA](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA)。公開・非Gated、固定rev `588752bc181b999247f0e7df578bbc55d2b920e9`。**7ファイル・13,034,727 byte**、うちAdapter重み`adapter_model.safetensors`は13,014,120 byte、配布元LFS SHA-256は`1abf13b2191c9973a4dc4d978448512d3ce2efabfd1e671edd5956b6aebfa5ac`。
- 重要な**親参照の違い**：固定`adapter_config.json`は `Qwen/Qwen3.8-27B@37561816e66b5b9153b1b64c10968c18c1e6f4a0` を記載。作者READMEでFP8推論に用いたのは `Qwen/Qwen3.8-27B-FP8@017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`。両revision自体は現在の公開APIで200だが、**量子化・実装・学習親が互換であるとは未証明**。
- LoRAのREADME/A​​dapterはApache-2.0でも、作成データ`mlabonne/harmless_alpaca`は[Stanford Alpaca由来のCC BY-NC 4.0](https://github.com/tatsu-lab/stanford_alpaca)を含む。元データ・派生重み・本人利用目的にまたがる権利審査は別。作者のStrongREJECT、GSM8K、IFEvalはH200・専用SGLang/FP8 KV等に限定される作者値であり、8GB GPUの性能を保証しない。

**判定**：13MBでも**親Qwen 27Bがなければモデルとして完成しない**。学習済みAdapterの研究価値は高いが、親の正しいバージョン・SHA・ライセンス・ABIとデータ権利が閉じるまで**HOLD**。マージ済み27B重みを別資産に増やさない。

## 4. 見落としやすい既存の復元阻害：REMORY親の現在の照合

[REMORY原本](https://huggingface.co/fudan-generative-ai/Qwen3.8-27B-REMORY-1.9B)は約2.006Bの学習済みメモリを含むが、通常のQwen親27Bがなければ学習済み機能を再現できない。既存[R127の20ファイル計画](../../manifests/drafts/r127-2026-11-20-remory-20file-online250-and-parent-delta.candidate.json)は訓練親を`Qwen/Qwen3.8-27B@1d4bf0f2ff6012fd82039d0dd7c60c0`と明記している。

2026-11-20に公開Hub APIの該当revisionと`config.json`へのHEADを照合したところ**双方404**。一方、旧基準`37561816e66b5b9153b1b64c10968c18c1e6f4a0`は双方**200**。これは現在の公開経路の不一致であって、**学習済み重みが削除されたと断定する証拠ではない**。

R127は過去のスナップショットで**29ファイルのSHA一致、README/chat template/tokenizer configの3差分**を記録している。したがって再取得は①歴史的なsha一覧と旧固定revisionの18重量シャードを照合、②差分の3ファイルの正規取得権を確認、③ユーザーDドライブ現物の有無とSHAを確認、の順。①〜③未完了の現状では「REMORYを8GBだけ保存すれば完全オフライン復元できる」は**FAIL**。REMORYのCONDITIONAL選定自体は削除しない。

## 5. 交換・重複排除・容量の明示

1. 既存61モデルの重みは**再転送しない**。特に取得台帳に記録されたInterpretic-v2 Q4と0bserverx RVN-Q4を再要求しない。異なるBF16原本/RVN-F16の追加は、同一学習結果の非可逆量子化差・HDD容量を別途評価して判断。
2. 第5候補FrostWolfは元LFM3やOrcaRouterモデルの完全置換ではない。**独立した編集済み重みのオプション**として追加し、変換GGUFを二重計上しない。
3. PhalaはQwen親の取得・復元性を確保できたときだけLoRAの少ない増分容量を活かす。親を保管しないまま「13MBで無検閲27Bが動く」と書かない。
4. v55のOlala Baseと後学習版はモデル系譜上別重みであるため既存選定を維持。本提案のFrostWolfとPhalaだけが**v55登録外の学習結果**。他の大量候補を追加せず、依存の整合を優先。

### 変数表（容量と条件）

| 記号 | 意味（日本語） | 単位（SI等） | 定義・値 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `B_4` | R128初回4source合計 | byte（SI情報量補助単位） | 6,127,042,272 | 101ファイルのpublisher source、未承認 | 非負整数スカラー |
| `B_F` | FrostWolf原本source全量 | byte | 3,475,637,066 | 13ファイル固定、実D保存量でない | 非負整数スカラー |
| `B_L` | Phala Adapter source全量 | byte | 13,034,727 | 親Qwenは含まない | 非負整数スカラー |
| `B_5` | 初回4＋FrostWolf候補容量 | byte | `B_4 + B_F` = 9,602,679,338 | 全件未承認・未取得 | 非負整数スカラー |
| `B_{peak}` | 選択scope最大単一ファイル | byte | 4,577,698,688（Aion） | この5候補のみ | 非負整数スカラー |
| `F` | HDD必須維持空き | byte | 200,000,000,000 | 取得中も維持 | 非負整数スカラー |
| `D` | 本人HDD現在の空き | byte | 未計測 | 正しい物理ボリューム特定後 | 非負整数またはnull |
| `N` | モデル全パラメータ数 | 1（無次元） | MoEの全expert含む総数 | 不明時は取得準備STOP。150B未満のみ本提案の取得候補 | 非負整数またはnull |

**単位・次元チェック**：`B_4`、`B_F`、`B_L`はbyteなので加算可能。候補5件で `B_5=9,602,679,338 byte`（約9.603十進GB）。予備2倍最大ファイルを仮定する最小限の保守的容量例は `D ≥ F + B_5 + 2 B_{peak}=218,758,076,714 byte`。これは依存・他プロセス・追加cache等を含まないため、実行承認の十分条件ではない。`N`はパラメータ個数であり、ファイルbyteや量子化後の保存容量と混同しない。

**150B政策の衝突**：本依頼で指定されていた **150B以上絶対除外** を本調査の新規候補には適用する。一方main v55は、厳格な比較実測を条件とする「150B超量子化例外審査」を過去の改訂で採用している。**同一ルールではない**ため、本提案では例外の採否や既存v55正本を自動改変しない。いずれの新候補も150Bに達しない。

## 6. 公開制限の事実と反証可能な見通し

2026-11-19の米BISの[Interim Final Rule（連邦官報一次資料）](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は、AI Diffusion Ruleによるモデル重み向け**ECCN 4E091を撤廃**した。一方、遠隔計算・半導体・特定輸出先/用途への別規則と各配布元Gated・利用契約は残る。「公開ウェイト全体が直ちに禁止される」とは現在の事実から導けない。

Exaは今回の検索で**HTTP 402（利用枠超過）**となったため、新たなExa調査成功を称さない。補完したのはHugging Face出版社の固定ファイルAPI、README・LICENSE正文、政府一次資料、既存固定manifestの再照合。将来の削除・Gated化は**予測**でありモデル別確率を創作しない。

## 7. H / T / D / C / U

- **H（反証可能仮説）**：v55で未登録の小型FrostWolf原本は、同じ編集系列のGGUF追加より少ない重複で、合法な保存の独自性を増やす。Phalaは親Qwenの同一性と学習データ権利を閉じない限り、容量が小さくてもオフライン再現性を増やさない。
- **T（最小検証）**：R128固定4ソースの101ファイルに加え、FrostWolf13＋Phala7ファイルを公式40桁revisionのHubツリーと照合（最小n=6配布元、121ファイル）。公開元のパス・byte・上流LFS SHA256・Git blob SHA1が一致しない時点で停止。本人承認後の独立性能試験は同一GPU/clock・CPU/RAM・Transformers/PyTorch/量子化zero-point・batch・context・temperature条件で合法的な日本語・多言語・tool tasksから最低100件のpaired held-out入力と事前登録の品質閾値を用いる。
- **D（PASS/FAIL/UNCERTAIN）**：**PASS_SOURCE**＝4＋2配布元のメタデータ照合は一致。**FAIL_ACQUISITION**＝個別ライセンス不適合、親SHA不一致、未審査コード実行、HDD空き不足。**UNCERTAIN**＝本人HDDの全ファイル実在と再ハッシュ、第三者コード実行安全性、親版互換、独立品質。Phala/REMORYは復元準備HOLD。
- **C（対立仮説）**：作者の拒否率選択試行は一般能力に過適合している可能性、Phalaの親revision差が実際には同一実行で互換な可能性、配布条件は規制強化ではなく緩和される可能性もある。
- **U（不確かさ）**：選択済み評価バイアス、元データ権利、GPU/ABI未測定、Hubの過去revisionの公開可否、現在のHDD、取得作業領域。規制停止頻度や独立測定分布がないため、合成標準不確かさ `u_c` と包含係数 `k` の数値化はできず未適用。

## 8. ERROR CHECK／次のステップ

- mainの調査基準は**v55:209登録/162有効**。FrostWolfとPhalaの既存登録有無はいずれもfalse。v55 Olala系既存2資産の重複追加0。
- 配布元の新規固定20ファイル＝FrostWolf13＋Phala7。publisher LFS SHA256は合計3参照、重みの**ローカルSHA検証は0件**。
- 従来の4件101ファイルと新規13ファイルを合わせた**5配布元114ファイル・9,602,679,338 byte**が今後の調査上の第一候補。Phala7ファイルは別のHOLDでありこの114ファイルには含まない。
- **実際の取得／ユーザーGated承認の代理実施／コードのimport／承認キュー変更／main改変は0件**。モデルのパラメータ絶対上限と本人の権利を優先度で上書きしない。

学際的な転用：①法制・ライセンス（行為別許諾、データ由来）②ML再現性（親checkpoint・量子化互換、編集の独自性）③デジタル保存（完全revision、LFS SHA、来歴）④信頼性工学（空き容量・実機ABI・失敗時停止）。

## 9.〈次に考える問い〉

**保存済みと報告された61モデルのうち、原本・親checkpoint・tokenizer・実行時コードを揃えて実際にオフライン復元できる割合は何％か。** 次の段階では新規モデル数ではなく、独立再ハッシュで復元可能と確認された学習済み状態の数を成果指標にすべきである。

## 10. 【2026-11-20追補】main v56への同時採択と二重登録防止

調査・専用ブランチへの記録中に**mainの正本がv55（209/162）からv56（211登録・164有効）へ更新**された。新規に登録された `FrostWolfAI/LFM3-1.7B-abliterated` と `PhalaCloud/Qwen3.8-27B-Uncensored-LoRA` は両方とも研究上の **CONDITIONAL**。前節「v55に未登録」「今後の正式追加候補」は**v55観測時点に限った履歴**であり、**2026-11-20最終のv56では登録済み**。他ブランチに追加コミットせず、[v56差分](../../catalog/revisions/v56-2026-11-20.json)と[正式v56ビュー](../../catalog/effective-portfolio-2026-11-20-v56.json)の採否を尊重し重複計上しない。

- mainの[先行固定source](../../manifests/drafts/r130-2026-11-20-frostwolf-and-phala-originals-fixed.candidate.json) と、今回の[本ブランチ固定source](../../manifests/drafts/2026-11-20-frostwolf-phala-immutable-source.candidate.json)を全20ファイルで照合。**2つのrepo ID、各40桁revision、ファイルpath、bytes、非null Git blob SHA-1とLFS SHA-256に不一致0**。両者は同じsourceを別の監査様式で記述しており、追加で3.4887GBを二重に予約しない。
- FrostWolf：v56で**正式CONDITIONAL採択済み**、研究第5候補として原本BF16を維持。権利適用・コード・owner D容量・ローカルハッシュに未完了があるため**取得承認ではない**。
- Phala：v56で**正式CONDITIONAL採択済み**、ただし13MB Adapterの**単体モデル性・親互換性・Alpaca由来データの使用権は未証明**。本報告のHOLDは**取得準備／offline-restore readinessに対する保留**であり、v56の採用判断を差し戻す意味ではない。
- v56の[CURRENT](../../catalog/CURRENT.json)は211件のうち有効164件、モデル185件／データセット26件を記録。既存[承認キュー](../../queues/approved.json)は0件。今回の追加取得/モデル実行/所有者媒体のre-hashも0。

**誤りの防止**：正式選定を研究候補として何度も「新規追加」しない。v55スナップショットとv56の確定済み意思決定、固定sourceと物理保存、CONDITIONAL選定と取得許可を混ぜない。
