# R153／v64：112件取得報告後の重複停止・小型無検閲差分・特殊学習原本5件の再選定

**基準日：2026-11-22（日本時間）**。唯一の正式正本は [catalog/CURRENT.json](../../catalog/CURRENT.json) の**v64、236登録／189有効（SELECT55・CONDITIONAL134）**。本報告はPublisher原本の選定・研究用source固定・取得済み重複排除であり、**新たな正式v65登録・所有者のダウンロード承認・実モデル重量転送を行わない**。

一次資料・検査可能な生成物：
- [新5個別原本の全Publisher tree・選択source hash台帳](../../manifests/drafts/r153-2026-11-22-post112-five-distinct-origins-source-frozen.candidate.json)
- [正本v64を保持した次の研究専用キュー](../../queues/proposed-v64-r153-after112-next-originals-UNAPPROVED.json)
- [全13取得済報告との一致／5候補採否](../../catalog/decisions/2026-11-22-r153-post112-reconciliation-and-next-originals.json)
- [取得側の履歴報告](../../catalog/execution/2026-11-19-acquisition-ledger.json)
- [R152（99件時点の古い候補一覧）](../../queues/proposed-v64-r152-post99-13-plus-bison-research-only.json)

## 1. 今回の最優先判断：すでに取得報告済みの13原本を旧キューから取り除く

最新台帳は**112 VERIFY／1 Gated HOLD、1,714ファイル、2,020,548,143,087byte**。旧R152キューに記された99報告からの増分13配布元について、**13/13のrepo ID、40桁revision、取得files、整数bytesが台帳と完全一致**した。したがって、**取得報告済み13件は次の新規取得キューに一切再投入しない**。しかし、全件のowner Windows Dドライブ現物SHA・LICENSE・完全offline復元を本研究で検査したわけではない。履歴上の最低空き1,026,731,790,336byteは現在の空きではない。

旧99→112の差分は13リポジトリ／236ファイル／**140,553,833,221byte**であり、R152の非HOLD13全source合計と厳密に一致。旧1 Gated HOLDは未許諾であり勝手に再取得・回避しない。旧R152キューは履歴として残し、最新研究キューをR153へ移す。

**すでに取得報告済みだがv64に未登録の別学習結果（正式カタログbackfill審査）**：
- [mistralai/Timestral-5M](https://huggingface.co/mistralai/Timestral-5M/tree/bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f)：6 file／**20,854,471byte**。Timestral-28Mとは異なる学習済み5.2M時系列予測。Modified MITの利用者の月商条件がある。**現物を重複取得せず**次revisionで個別CONDITIONAL選定を審査。
- [tencent/WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B/tree/821690998399cac0f55bb7f7f805ebafa650c3a4)：27 file／**6,590,699,556byte**。2つのBF16 shardと時間同期映像音声用processor。作者発行のSHA256SUMS 25/25一致は[R150先行監査](150-v63-post99-wemm-video2b-uncensored-and-armenian-evidence.md)を参照。未登録でも112取得報告済みなので二度取得しない。custom Python、パッチ済みvLLM/SGLang、全音声/映像依存のoffline復元未検証。正式選定は別途。

新v64選定の[baselabs/bison-1](https://huggingface.co/baselabs/bison-1)も**16file／65,398,108,261byte**で112取得報告に含まれる。兄弟の[groundhog-1](https://huggingface.co/baselabs/groundhog-1) 53.121GBを同時自動採用・取得しない。<https://github.com/Unjuno/local-model-portfolio/blob/main/docs/strategy/151-v64-baseten-decision-original-selection-and-drift.md>

## 2. 次に保存すべき独立原本（研究選定確定、ダウンロードはSTOP）

| 順位／公開元（40桁revision固定） | 採用する正味Publisher参照source | 根拠・重複排除・権利上の限界 |
|---|---:|---|
| **P0：無検閲小型差分** [nchapman/Qwen3.5-0.8B-Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA/tree/92e2ae29c379d7378c696511ec9c70ace8be1434) | **12 file／2,031,005byte** | Heretic v2.1 rank-3を適用した別の2学習／編集重みSHAを保存。rootとPareto trial_002は同一SHAなので二重保存しない。3 GGUFは同編集結果の派生形式として保存対象外。親[Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B)は112取得報告のSELECT原本にあるが、**owner現物の同SHA・PEFT/vLLM/llama.cpp ABI、量子化zero-point等は未検証**。作者拒否測定4/100、6/100は独立再現なし。 |
| **P0：3独立制御ポリシー** [GetCartwheelInc/cartwheel-control](https://huggingface.co/GetCartwheelInc/cartwheel-control/tree/24fc279af8f70097f503767b81db5384d779aae5) | **154 file／304,057,444byte** | RP1、G1、Asimov-1の3別 `policy.safetensors` + 物理シミュレータ用模型/mesh/MJCF、モーションを一組として保全。**simulation only**であり実機の安全な制御は立証なし。独自Cartwheel Open Model Licenseの改定・通知・第三者権利を個別確認。 |
| **P0：生理信号16.7M原本** [inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0/tree/51582cc8487ab0e0f48d866bfc0124afbaf6562a) | **7 file／66,946,541byte** | ECG等の多チャネル信号学習済み特徴抽出器F32＋学習/構成済みchannels.npz、channels.json。MIT。**医療診断器ではない**。別の `lingsante_pulse` 推論codeパッケージをコミット固定しないとfull offline restore不完全。入力128Hz、物理channel同定、利用者のデータ同意も独立ゲート。 |
| **P1：画像潜在空間3成果** [ostris/primal_vae](https://huggingface.co/ostris/primal_vae/tree/dc3e96c879e8cf4247c9474c3109bc2847099b50) | **8 file／1,132,162,841byte** | 2×1、2×2、4×1の三つの異なるFP32学習済みVAE原本＋custom modeling Python/config/LICENSE。比較画像6個を除外した最小復元scope。Apache-2.0。構造上のlatent次元がFlux/SD VAEと等しくても**無学習交換可能と断定不可**。作者3画像PSNRは統計的代表性なし。 |
| **P2 HOLD：非商用30.9M URL台帳** [Octen/Octen-WebGR-0.6B](https://huggingface.co/Octen/Octen-WebGR-0.6B/tree/5c062c8ff81eb36f05b66e2fcd8652060d9b8960) | **34 file／1,980,313,007byte** | 0.73B学習済み生成検索と**16分割Parquet・30,931,888 URL対応表**が不可分。モデル重みだけではURLに復号不能。weights/table **CC BY-NC 4.0**・code Apache-2.0、過去URL表のプライバシー/削除申請・利用目的を先に審査。取得自動承認なし。 |

最初の4件は**新たな正式カタログ収録を推薦する研究候補**であるが、今回のv64にレコードを勝手に追加していない。内部の個々のadapter/robot/VAEを通常の量子化違いと混同しない。

独立性・再構築性：
- 無検閲QwenLoRAのroot SHA `269cee632d7b2dc1cb5163d6f1b2a378df3b2130e51c8b08c686709997c28679` とPareto trial_004 SHA `26836a1374eb43aef39f04970b558f347a62558ebce8c0e00388ff217146ba6e` は異なる。trial_002はrootと同一。**最低2 distinct weight states**。
- CartwheelのRP1/G1/Asimov1は別weights。リアルロボットの安全性/適法運用は未検証。
- LingSante sourceのモデルweight `model.safetensors` と別の固定channel vectors `channels.npz` は異なる役割。上流BAAI bge-smallはchannels vector生成に使われたものの、**固定ベクトルによる現在の推論実行で再ダウンロード必須とはカードは記載していない**。
- Primal VAEの3原本は別checkpoint（学習済み状態差）でありGGUF/FP8変換ではない。モデル作者自身も形状交換=下流性能互換と断定していない。

## 3. 計数・単位と保管増分の境界

| 記号 | 意味（日本語） | 単位（SI/情報単位） | 定義 | 定義域/前提 | 型 |
|---|---|---|---|---|---|
| `B_99` | 旧取得台帳の照合済容量 | byte | 1,879,994,309,866 | 99報告値、owner SHA未再検査 | 非負整数スカラー |
| `B_112` | 現取得台帳の照合済容量 | byte | 2,020,548,143,087 | 112報告値、owner SHA未再検査 | 非負整数スカラー |
| `B_Δ` | 新13件の報告済み増分 | byte | `B_112-B_99` | 重複DL対象外 | 非負整数スカラー |
| `B_H` | Qwen Heretic LoRA最小原本source | byte | 2,031,005 | 固定12file、親コピーなし | 非負整数スカラー |
| `B_C` | Cartwheel3制御policy全scope | byte | 304,057,444 | 固定154file | 非負整数スカラー |
| `B_L` | LingSanteモデル一式 | byte | 66,946,541 | 固定7file、別codeは除外 | 非負整数スカラー |
| `B_V` | Primal VAE3原本+code | byte | 1,132,162,841 | 固定8file、比較画像除外 | 非負整数スカラー |
| `B_P` | 新4系統の論理Publisher合計 | byte | `B_H+B_C+B_L+B_V` | owner重複SHA/実空きと別 | 非負整数スカラー |
| `F` | 取得処理中の最低残空き安全床 | byte | 200,000,000,000 | 実media上、staging/cacheは別 | 非負整数スカラー |
| `D` | 所有者媒体の現在の利用可能空き | byte | null | この研究環境からは未測定 | 非負整数またはnull |

容量計算：`B_Δ = 2,020,548,143,087 - 1,879,994,309,866 = 140,553,833,221byte`、`B_P=2,031,005+304,057,444+66,946,541+1,132,162,841=1,505,197,831byte`（十進約1.505GB）。**次元チェック**：すべてのB系列はbyteで加減算可能。LFS SHAは識別子、学習パラメータ数は個数でありbyte加算には直接使えない。4TB予算残を現在の2.021TBだけから断定できず、同一SHAの共有・データセット・未報告保存物・cache/staging・現在Dを調査する必要がある。

## 4. 権利と2026年の規制観測を区別

[米BISの2026-11-19 Federal Register 91 FR 74970 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は従前のモデル重みECCN 4E091を撤廃している。**すべてのオープンウェイトの合法所持が近日一律禁止される事実は立証されない**。別の仕向地/用途規制、配布元のGated、NC、モデルコードの権利、音声/生理信号・URL等の個人情報権利は別に保持する。将来Gated化・公開終了・ライセンス改定は保存戦略の**反証可能なシナリオ**であり、発生確率や日時を作らない。

## 5. H／T／D／C／UとERROR CHECK

**H（反証可能仮説）**：取得済み13と新4原本scopeを分離し、通常GGUF派生/同一SHA重みだけ削れば、既存の取得結果を重複させず追加4種の学習成果・能力が1.506GB未満のモデルPublisher原本選択で保存可能となる（ただし外部コード、親、実staging/権利は除く）。

**T（最小検証）**：①旧13repoのID／40hex rev／files／bytesを最新112ledgerに全件joinし、13/13・236/236・byte差分を検証。②新5 repo（全**225file／3,502,502,625byte**、うち新P0/P1推薦4件**181 selected files／1,505,197,831byte**）を上流immutable treeで全数参照。③nchapman2固有SHA、Cartwheel3 weights、Ling2補助学習・構成ファイル、Primal3 weightを全数列挙し、販売用同意やlocal SHAを自動trueにしない。④ owner許諾のもとなら同一HW/clock/backend commit/dtype、量子化scale+zero-point、context、batch、seedで、少なくとも各30合法なheld-out事例を計測し、次段階で予登録した誤差・許容条件により停止。

**D（合否）**：公開元のファイル形式/上流SHA/13差分はSTATIC PASS。**実ダウンロードGO条件＝本人の取得行為別利用権+固定scopeの個別明示承認+所有者HDDの実SHA/現空き200GB床とstaging+親/codec/全runtime ABI+再生可能なoffline構成**。現在不成立なので、新モデル本体の取得可否は**UNCERTAIN/STOP**。無承認取得・Gated迂回・既存の同一重量削除・コード無審査実行をFAIL。

**C（対立仮説）**：小型LoRAがparent版と非互換で効果を再現できない／Cartwheelの別モデル/mesh権利が衝突／LingSanteの波形特徴が実タスクで役立たない／Primal latentを元Flux/SDへ代入すると品質が崩れる／Octen NC・古いWeb URIや個人情報が研究目的と抵触する。

**U（主要不確かさ）**：owner実SHA・ディスク/キャッシュ/依存、Python ABI、ユーザーの利用目的とLicense帰属、作者の小標本評価、モデルの量子化数値表現。反復測定が未実施なので合成標準不確かさ `u_c`・係数 `k`は算定不能。

**ERROR CHECK**：v64正本236/189（SELECT55/CONDITIONAL134）は変更なし。13/13一致、+236 files、+140,553,833,221byteはinteger一致。新5repo225 files、P0/P1 4repo181 selected referencesと2,031,005+304,057,444+66,946,541+1,132,162,841の合計一致。approved queue 0、owner D現在の検証0、モデル重量新規DL0、Gated回避0、既存削除0。

**学際性**：①重み編集と低ランク行列（可逆LoRA・Pareto分岐）、②ロボティクス/制御とシミュレーション、③臨床信号処理とプライバシー、④画像潜在圧縮・生成、⑤生成検索/URLデータ管理、⑥暗号学的供給網、国際法務。

###〈次に考える問い〉

**独立学習済み4系統約1.505GBを保存する前に、取得済み112件のどれがユーザー媒体で実際に復元可能かを先に測定すると、追加の親/ランタイム取得量はどれだけ削減されるか。**
