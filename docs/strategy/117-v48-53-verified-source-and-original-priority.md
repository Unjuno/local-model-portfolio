# R117 — v48保存モデルの再選定・取得重複停止（2026-11-19）

## 1.〈本論〉確認済み状態と判断

唯一の正本は[CURRENT v48](../../catalog/CURRENT.json)：**201登録／154有効**（SELECT53、CONDITIONAL101）。このR117はソースと保存価値の比較に限定し、**有効201件の登録変更・既存ファイル削除・ダウンロードは行わない**。承認キューは0件。

[現行取得履歴](../../catalog/execution/2026-11-19-acquisition-ledger.json)には**54件中53件VERIFIED報告、579ファイル、270,835,576,267byte**が記録される。ユーザーのWindows Dドライブで今回実物とhashを再照合した数ではない。従来R116の「59のうち5件だけ重複」は更新前のledgerに基づくため、現行の[59候補](../../catalog/execution/2026-11-19-discovered-next-waves.json)と照合し直すと**既存スコープ36件、未報告23件**。未報告の選択source表記の合計は**1,386,933,535,900byte（十進1.387TB）**。これら23件は全154件の未取得数という意味ではない。

## 2.優先順位の確定（取得許可ではなくsource確定順）

| 段階 | 件数 | ソースGB（十進） | 保存判断 |
| --- | ---: | ---: | --- |
| A | 5 | 84.652 | 独自学習成果、構造・専門能力のためsource file/hash監査を先行 |
| B | 13 | 792.906 | 保存対象として維持、容量・代替・再現性の追加判定後にsourceを確定 |
| C | 5 | 509.376 | 汎用大型の重複可能性を優先検証。**新規取得を保留**、既存カタログ・保管物は削除しない |

| repo ID | 帯 | 上流source GB | ファイル数 | v48決定 | 実質的に保存する理由と疑問 |
| --- | --- | ---: | ---: | --- | --- |
| `RWKV/RWKV7-7.2B-20260805` | A | 14.402 | 12 | select | recurrent RWKV7 architecture and independently learned original |
| `microsoft/TRELLIS.2-4B` | A | 16.237 | 21 | select | independent 3D geometry and texturing, different from Idol 3DGS |
| `GSAI-ML/iLLaDA-8B-Base` | A | 16.513 | 12 | select | 12T-token fully bidirectional masked diffusion independent original, unlike prior ARLoop |
| `PrentisAI/GroundGUI-8B` | A | 17.550 | 16 | conditional | ScreenRef-derived precise GUI grounding, not equivalent to Fara full GUI agent |
| `ACE-Step/acestep-v15-xl-turbo` | A | 19.949 | 7 | conditional | original music generation, not an ASR/TTS quantized duplicate |
| `ResembleAI/chatterbox` | B | 10.681 | 12 | select | distinct TTS pipeline but multiple variants/codec need file allowlist |
| `OpenMOSS-Team/MOSS-TTS-v1.5` | B | 16.996 | 15 | select | separate TTS trained lineage, inspect learned codec and variants |
| `kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers` | B | 26.671 | 34 | conditional | Independent MIT-licensed 2026 synchronized 5-second video+44kHz audio generator, 3.178B Lite main DiT, distilled 10-step execution; distinct from Wan and LTX. |
| `HuggingFaceBio/Carbon-X` | B | 29.656 | 10 | select | DNA配列と自然言語を共同学習した約14.8B特殊モデル。独自DNAトークナイザーと学習工程が必要で、Qwen3-14Bだけでは同じ重みを戻せない。 |
| `microsoft/Fara1.5-27B` | B | 54.744 | 21 | select | full GUI workflow agent, not replaceable one-to-one with GroundGUI click-only |
| `Qwen/Qwen3.8-27B` | B | 55.586 | 30 | select | original parent for comparing uncensored checkpoints; not identical to post-trained edits |
| `meta-models/Muse-Glimmer-30B` | B | 59.582 | 11 | conditional | Muse Glimmer 30Bは29.7766BパラメータのMeta原本蒸留・画像統合重み。52層sliding/full混在と50層vision towerを含む独立アーキテクチャ、同一系列のGGUFコピーではない。 |
| `ibm-granite/granite-switch-4.1-30b` | B | 59.991 | 25 | select | 4.1.1で改訂された約30Bのモジュラーモデル。Decision aLoRA・Guardian aLoRA・日本語含む7言語音声Encoderという独特の専門部品の組合せを保存する。 |
| `tencent/Hy-Memory-30B-A3B` | B | 60.143 | 58 | select | 約30B総数/約3Bアクティブの長期エージェント記憶書き込み専門MoE。メモリ更新方針を専門的な蒸留・強化学習で学んでいる。 |
| `allenai/Olmo-3-1125-32B` | B | 64.477 | 23 | select | AllenAIによる公開度の高い32B級系列。学習過程と検証可能性を別系統の比較対象として残す。 |
| `EPFLiGHT/OLMo-2-32B-MeditronFO` | B | 64.477 | 23 | select | 臨床質問・ガイドライン用SFTを施した32B。公開されたMeditronコーパスとレシピを含めて再学習の検証に使える。 |
| `openai/gpt-oss-120b` | B | 130.526 | 34 | select | native MXFP4 released weights, architecturally different MoE, large resource cost |
| `Qwen/Qwen3-Coder-Next` | B | 159.376 | 49 | select | 80B total (not 3B active) coding-agent posttraining, resource-expensive specialist |
| `google/gemma-4-31B` | C | 62.579 | 9 | select | general foundation baseline with large source, need distinct use-case evidence |
| `Nanbeige/Nanbeige4.3-33B` | C | 66.257 | 22 | select | another ~33B general checkpoint, possible functional overlap |
| `OctoMed/OctoMed-32B` | C | 66.726 | 10 | select | medical posttraining may be useful but duplicates other biomedical portfolio missions |
| `Qwen/Qwen3.5-35B-A3B-Base` | C | 71.927 | 24 | select | same-family base source with overlapping Qwen coverage until learned delta proven |
| `mistralai/Mistral-Small-4-119B-2603` | C | 241.887 | 21 | select | ~242GB generic 119B-class source, need measured uniqueness vs existing large models |

**A群を最初の原本優先トランシェとして選定**。特にiLLaDAは[配布元](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base)・[arXiv:2606.25331](https://arxiv.org/abs/2606.25331)がfully bidirectional masked diffusionで12T tokenからの独立事前学習を記載。RWKV7の再帰型、GroundGUIのGUI画像→クリック座標（[配布元](https://huggingface.co/PrentisAI/GroundGUI-8B)）、TRELLIS.2の3D生成、ACE-Stepの音楽生成とは原理的に用途が異なる。性能の自己公表値は、同じ機械での独立比較がない限り優劣の証拠としない。

B群のQwen3-Coder-Nextは約80B総数・3B程度の活性MoEだが、大型sourceである。規制予測だけで高速実行可能としない。Fara GUIエージェントはGroundGUIのクリック座標モデルと同じではなく、無条件に交換しない。C群のMistral Small 4 119Bは約242GBのsource候補で、他大型汎用モデルとの差が未実証ならまず原本の独自価値・容量を再検討する。

## 3.高精度マスターと重複取得の停止

| モデル原本 | 保存優先source | 過去報告との関係 | 判断 |
| --- | ---: | --- | --- |
| [InterpreticAI v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | **55,586,056,799 byte** BF16 | GGUF Q4報告は別ファイル形式 | BF16高精度原本を固定候補、既存Q4は推論用に保持 |
| [0bserverx RVN](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | **53,808,326,934 byte** RVN F16と付属物 | RVN Q4報告は別 | F16が確認できる再構成元。派生Safetensorsと二重保存しない。元学習BF16とは呼ばない |
| [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | **15,345,816,226byte** LM/codec/heads | 台帳VERIFIEDは**775,728,152byte**のteacher中心部分スコープ | 同一SHAのteacherを重複せず、不足するLM・codec原本の補完を先に確定 |

**新候補 [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash)** は19ファイル1,385,998,807byte／publisher LFS SHA-256 2件の固定[source案](../../manifests/drafts/r115-v48-rumble2-flash-and-nemotron-sigma-original.candidate.json)があり、**CONDITIONAL追加の候補として採用提案**。0.5B級の独立音声認識を日本語／英語・ノイズのある実務ASRと比較する価値がある。ただし独立学習済みCTC headのパラメータ総数未集計、本人のLicense行為別許諾・完全実行ABIは未検証で**最終lockと本体取得は禁止**。[配布者の2026-11-18発表](https://huggingface.co/blog/rumble-2-flash)はNVIDIA H200/vLLMで英語WER 6.60%、複数言語平均6.96%と述べるがクロック・バッチ数の詳細不明、満バッチ時7000 RTFx超の値をユーザー実機速度としない。日本語の独立WER未測定。NVIDIA Sigmaはlicense:other/custom code、SenseNova Loop9BはGatedのためHOLD研究。

## 4. 配布規制の最新の反証

[米BIS 2026-11-19のFederal Register公開前原文](https://public-inspection.federalregister.gov/2026-23529.pdf)は、**AI Diffusion Ruleのモデル重み輸出管理（ECCN 4E091）の撤回**を明記。同時に半導体・クラウド遠隔計算の別の規制を新設している。公開前版と最終発行・有効日の区別は維持する。個人のオープンウェイト所持が一律禁止になる証拠ではなく、Gated・LICENSE/データ由来・将来のホスト変更は別の審査対象である。危険・悪用可能性だけを無許可の取得根拠にしない。

## 5. 実施上のSTOPゲート

取得作業は**固定revision・取得ファイル一式のpublisher SHA・全学習済み依存・LICENSE正文と本人権限・HDDの実容量/200GB床・code/ABI安全・明示承認**を満たすまで停止。150Bモデル総数はMoEの非活性expertを含む。現在の[limits](../../policies/limits.json)は150B以上の厳密な**実測比較付き量子化例外**を認めるが、PASS済み例外は0で、総数不明は最終lock停止。今回`queues/approved.json`は変更しない。

## 6. 変数表と次元チェック

| 記号 | 意味 | 単位（SIとの関係） | 定義 | 定義域/条件 | 型 |
| --- | --- | --- | --- | --- | --- |
| `N_d` | 発見資産数 | 1（無次元） | 対象発見台帳のrepo一意数 | 59 | 整数スカラー |
| `N_v` | 同一IDにVERIFIED報告のある発見資産 | 1（無次元） | GitHub履歴と照合 | 36、ローカル実体未検証 | 整数スカラー |
| `N_r` | 発見スコープの残資産 | 1（無次元） | 未報告source ID集合 | 23 | 整数スカラー |
| `B_r` | 未報告候補のバイト数 | byte（情報量） | 残レコードの選択source合計 | 1,386,933,535,900、依存不含 | 整数スカラー |
| `B_f` | 必要最低物理空き | byte（情報量） | policies/limits.json | 200,000,000,000 | 整数スカラー |
| `P_i` | 新priority帯 | 1（順序カテゴリ） | A/B/C | 取得許可ではない | カテゴリ |
| `M` | モデル総パラメータ数 | 1（個数/無次元） | inactive MoE、学習済み補助も含む | 未確認は最終lock不可 | 整数/欠損 |

**次元チェック**：`N_d`/`N_v`/`N_r`は件数として差分比較でき、`B_r`/`B_f`はともにbyteで比較できる。モデルパラメータ個数`M`をbyteへ直接置換しない。GGUFファイルサイズやactive MoE数は総パラメータ数の代わりにならない。

## 7. H / T / D / C / U と ERROR CHECK

**H**：独自原本・実際に未報告のsourceを優先すると、単なる量子化形式の追加より再現価値を維持し、重複取得を防ぐ。  
**T**：59件全数とGitHub54件の取得記録を突合（n_min=59）、未報告全件にA/B/Cを一意に付与、A群の固定SHA・依存を追跡。実機での独立SHA検証は別手順で必要。  
**D**：PASS_METADATAは`59=36+23`、ledger 54件でVERIFIED 53件、A/B/C件数合計23、ダウンロード承認0。FAILは同名異revisionを再取得不要とすること、正規Gated手順を迂回、未知総数を承認、容量床違反、無断削除。UNCERTAINは本人HDD・LICENSE/依存・性能実測。  
**C**：VERIFIEDの一部が部分スコープであった／ベンチマーク比較で大型独自モデルが必要になった場合、再評価する。  
**U**：過去ledgerと実ファイルの間の証拠差、未公開の依存、モデルの厳密再現、個人の利用行為、評価データ偏り。`u_c`と`k`は反復測定がないため算出不能。

**ERROR CHECK**：現行v48=201登録/154有効、source発見59件・重複36・未報告23、未報告source容量1,386,933,535,900byte、A5/B13/C5、承認キュー0件を計算で確認。重量ファイル取得・モデル実行・パーティション・削除操作は実施していない。

関連分野はアーカイブ工学、MLモデルの学習系譜、ソフトウェア供給網の来歴、ライセンス・データ権利法制。  

###〈次に考える問い〉

取得済み報告のある53件の**完全な依存込みオフライン再現率**を実機で測定すると、追加保存すべき原本の順位は何件変わるか。

**50字超要約**：v48の登録201／有効154を維持し、現在の53件VERIFIED報告と59件発見台帳を再照合した。発見候補のうち未報告23件をA/B/Cへ分け、A群の独立学習済みモデルを原本source優先とした。無検閲はBF16・RVN F16の高精度原本、ZONOSはteacherだけでなくLM/codecを含む完全bundleに優先転換。Rumbleは新たな条件付き候補、権利・総数・実機・承認未完了の取得は停止する。
