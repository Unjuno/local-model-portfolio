# 150B以上の特殊量子化モデルの例外調査（v9補足）

**調査日:** 2026-11-04 JST。**対象:** `Unjuno/local-model-portfolio` / `strategy/2026-11-03-01-risk`（基準コミット `6e9389c97d24528df97e4b14a6bc772780141fd3`）。対になる[全候補のJSON](../../catalog/proposals/03-quantized-over150-candidates.json)。

> これは**非実行の採用審査資料**。既存`policies/limits.json`は現在も総150B以上を除外しており、本ファイルでは規則変更・例外の取得承認・新しいダウンロード・既存ダウンロードへの介入をしない。ユーザーは既にダウンロード開始と申告したが、個別の実機進捗・保存量は未確認。GitHub承認キューが空であることは、外部手段によるダウンロードが行われていない証拠ではない。

## 1. 〈本論〉見つかった重要な修正点

- **元の総数と配布物の表示を混同しない。** AtomicChatのモデルカードに表示される`79.5M`や`0.1B`、GLM-5.3 EXL3に表示される`165B`は、元の180B/約1.05T/753Bという総パラメータ数の代わりにならない。元モデルのパラメータ、保存するcheckpoint tensorの総数、取り外したMoE expertやMTPを別に数える。
- **2026年11月4日現在の公式元ライセンス:** [Qwen3.8-Flash-NextのLICENSE](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/LICENSE)は**Qwen Community License 1.0**。OrcaRouterのFlash-Next-UncensoredのモデルカードはApache 2.0表示で不一致。`Qwen3.8-27B`のライセンスをFlash-Nextに誤適用しない。ライセンス正文と派生配布物の同意条件が未整理のため、OrcaRouter版は法的再確認が先。
- **量子化で性能が上がるわけではない。** 圧縮性能、特化用途の性能、汎用精度の保存は異なる。例：200B REAPの元checkpoint平均81.02%、200B REAMは78.10%、基準284Bは81.68%（4タスク平均、作者測定）。後段Q3量子化版はこの測定の対象ではない。
- **境界値の取り違え:** [DeepSeek-V4-Flash-0731-reap-150b](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b)は名前が150Bだが、Hubは150.1285Bと表示。厳密な従来の「150B以上除外」に該当し、150B未満の通常枠と誤認しない。
- **ベースを持たないアダプターは単体で動かない。** Mistral Large4の0.45GB LoRAは別の完全な元モデルGGUFを必要とする。0.45GBだけを『1Tモデル保存済み』としない。

## 2. 原本ごとの例外候補評価

| 候補repo | 元モデル総数 | 対象変換・配布者記載の選択容量 | 品質について確認できた数値 | 判定 |
|---|---:|---|---|---|
| [AtomicChat/Qwen3.8-Flash-Next-Uncensored-GGUF](https://huggingface.co/AtomicChat/Qwen3.8-Flash-Next-Uncensored-GGUF) | 180.0B | AD-4.25bpw-Q4_K_M；93.9GB | Author measured MMLU 87.3% base vs 86.8% edited BF16 on 2000 questions (delta -0.5 pp); baked Q4 ~91.1% same top-1 vs ~89.2% of old similarly sized base quant plus adapter | **A_PRIORITY_RESEARCH_NOT_APPROVAL** |
| [orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF) | 180.0B | Q4_K_M；110.0GB | Publisher reports original BF16 ablation within ±2 points on selected general benchmarks; no rigorous independent per-Q4-head-to-head is established | **B_RIGHTS_HOLD_ALTERNATIVE_COMPARE** |
| [AtomicChat/Mistral-Large-4-1T-A52B-Uncensored-GGUF](https://huggingface.co/AtomicChat/Mistral-Large-4-1T-A52B-Uncensored-GGUF) | 1050B | IQ2_XXS, 2.31bpw baked GGUF；302.0GB | Author MMLU 81.6% baseline vs 80.6% edited n=500, reported p=0.13; baked 2-bit top-1 match 82.5%, occasional degeneration; LoRA top-1 90.2% (not standalone checkpoint) | **B_QUALITY_HOLD_HIGH_BUDGET** |
| [dealignai/Qwen3.5-VL-397B-A17B-UNCENSORED-JANG_1L](https://huggingface.co/dealignai/Qwen3.5-VL-397B-A17B-UNCENSORED-JANG_1L) | 397.0B | JANG_1L mixed 8-bit attention +2-bit experts；112.0GB | Author MMLU 88.9% (185/208) vs baseline 87.0%; ~4-answer difference in a 208 question test, insufficient standalone evidence of general quality improvement | **C_PLATFORM_AND_QUALITY_HOLD** |
| [puwaer/DeepSeek-V4-Flash-0731-reap-150b-gguf](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b-gguf) | 284.0B | Q3_K_M；70.9GB | SGLang checkpoint (pre-further-quantization) 4-test mean 82.48% vs original 81.68%; difference +0.80 pp; Q3_K_M quality untested | **C_BOUNDARY_REVIEW_ONLY** |
| [puwaer/DeepSeek-V4-Flash-0731-reap-200b-gguf](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-200b-gguf) | 284.0B | Q3_K_M；92.9GB | SGLang upstream pruned checkpoint mean 81.02% vs original 81.68% across four reported tasks, -0.66 pp; quantized Q3 not separately evaluated | **D_TECH_INTEREST_NOT_PRIORITY** |
| [puwaer/DeepSeek-V4-Flash-0731-ream-200b-gguf](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-ream-200b-gguf) | 284.0B | Q3_K_M；92.9GB | Mean 78.10% vs original 81.68%, -3.58 pp across four suite average; source checkpoint, quantized Q3 performance unknown | **D_REJECT_CURRENT_PRIORITY** |
| [drowzeys/keys-GLM-5.3-EXL3-Abliterated](https://huggingface.co/drowzeys/keys-GLM-5.3-EXL3-Abliterated) | 753.0B | EXL3 routed-experts-only 3-bit, other modules bf16/fp16；308.0GB | No adequate independently comparable held-out specialist/general benchmark established in this review | **D_HIGH_COMPLEXITY_HOLD** |
| [OpenYourMind/Kimi-K2.7-Code-ablated](https://huggingface.co/OpenYourMind/Kimi-K2.7-Code-ablated) | 1059B | INT4；容量未確定 | No suitably controlled baseline/edited quality benchmark found in this research | **D_NO_EVIDENCE_HOLD** |

**調査上の第1候補:** [AtomicChat Qwen3.8 Flash Next Uncensored（93.9GB、Q4）](https://huggingface.co/AtomicChat/Qwen3.8-Flash-Next-Uncensored-GGUF)。作者の2000問MMLUでは元87.30%・改変86.80%（-0.5pt）。同程度サイズの従来の量子化＋LoRAより、同一元モデルへのtop-1一致率が高いと作者が報告（91.1%対89.2%）。これは量子化配列の改善であって一般的な知能向上の証明ではない。ベンチは作者測定：8×RTX PRO 6000、CUDA13、llama.cpp `980aef8c`、87×4096長の比較。強い思考モードでの停止問題・視覚未検証が残る。

**サイズの大きい比較候補:** [AtomicChat Mistral Large4 Uncensored](https://huggingface.co/AtomicChat/Mistral-Large-4-1T-A52B-Uncensored-GGUF)は302GB、2.31bpw。MMLU500問は81.6→80.6%で、モデルカード自体が一部の出力劣化を認める。0.45GBのLoRAは単体では動かない。大容量消費、ベースの別量子化版との重複、RAM/依存の見積もりを解決するまでは承認しない。

**特殊形式の保留:** [dealignai Qwen3.5-VL 397B JANG](https://huggingface.co/dealignai/Qwen3.5-VL-397B-A17B-UNCENSORED-JANG_1L)の112GB版はHub上のテンソル統計に約428.6Bと表示。MMLU185/208=88.9%対baseline87.0%は**約4問の差**であり、独立再現や統計的優位を確証できない。M3 Ultra 256GBで33tok/sという作者報告はclock/batchを固定した実機ベンチではなく、MLX/JANG依存が強い。

**圧縮手法の反例:** [DeepSeek REAP 200B](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-200b)は0.66ポイント平均低下で、[REAM 200B](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-ream-200b)は3.58ポイント低下。さらにそのGGUF Q3等は個別の品質測定がなく、量子化したから品質を維持したとしない。これらは専門的な圧縮研究に価値があっても、例外の『特化モデルとして明確に有益』という条件とは区別する。

## 3. 新規例外の正式判断ルール（提案、未適用）

まず**元モデルと変換後モデルの総学習済みパラメータ数を別々に確定**し、150B境界の通常枠／例外枠を決める。例外に進むには①目的を持った量子化と固有改変・専門学習、②同条件の対照評価による特化性能と汎用品質の維持、③非重複・正規ライセンスとgating承認、④本体・補助Encoder・LoRA・MTP・imatrix・実行コードの版と必要バイト、⑤ユーザー側の保存先/HDD実空きとRAM/バックエンド確認が必要。

**注意:** 規制が近いというモデル個別の確率は算出していない。安全解除系のような行動制御変更は、通常の数学/コードの性能改善と同じ評価ではない。本人への無許可アクセス、第三者権利侵害、違法データの復元を認めない。意図や用途と取得権限を別に扱う。

### ストレージと実機の前提

ユーザーは約3.95TBの保存目標と、既に外部でダウンロードを開始したことを申告している。現行GitHub `policies/limits.json`は3.8TB予算／空き200GBのままであり、どのダウンロード処理でどの機種のディスクに保存されているかは未観測。容量に関する現行の数字を勝手に差し替えたり、既存ファイルを削除・停止・上書きしたりしない。

## 4. 変数表・次元チェック

| 記号 | 意味（日本語） | SI単位 | 定義・定義域 | 型 |
|---|---|---|---|---|
| `N_original` | 元モデル総パラメータ数 | 1（無次元） | 全MoE expert/embedding/MTP等を含む元の学習済み総数。非負整数／unknown | 整数スカラー/null |
| `N_artifact` | 配布された変換後モデルの総パラメータ数 | 1（無次元） | pruningで減少可能、量子化単独では減少しない。非負整数／unknown | 整数スカラー/null |
| `B_store` | 選択する全ファイルの保存量 | byte（十進） | 固定revisionの全シャード・依存を含む、nullを0としない | 非負整数スカラー/null |
| `Q_general` | 一般能力評価スコア | 1（無次元） | 同一テスト・同条件で測定した割合、0〜1 | 実数スカラー |
| `Q_special` | 特化タスク評価スコア | 1（無次元） | 事前固定の正当な課題での成功率、0〜1 | 実数スカラー |
| `R_runtime` | 推論時のピークRAM | byte（十進） | OS/重み/KV/allocator/依存込み、実機・backend・context・batch次第 | 非負整数スカラー/null |

**次元チェック:** パラメータ個数をbyteと比較しない。圧縮によるbyte減少は総パラメータが150B以下になった証明ではない。単に高いtoken top-1一致率も、別の元モデルより能力が優れることを意味しない。

## 5. H/T/D/C/UとERROR CHECK

**H:** 150B以上の例外候補は、元モデルに対して固有の合法な特化能力を保ち、汎用テストにおける品質劣化を適切に評価できる。**T:** 元モデル・特殊版・同サイズの標準量子化版を同一合法データ、固定seed、backend/ABI/quant/zero-point/context/batch/HWで比較する。最低200独立課題（専門/汎用別、可能ならそれ以上）、95%区間を対比較で評価。欠測時は停止。**D:** 特化能力の改善を繰り返し確認し、一般能力が許容損失範囲内、依存・権利・実容量のゲートを満たす場合だけPASS。明らかな一般能力劣化や契約不適合はFAIL。比較未完はUNCERTAIN。**C:** 改善がベンチマーク過適合、単なる量子化記法、バックエンドバグ、偶然のサンプル変動という対立仮説。**U:** ライセンス改訂、サンプル変動、GPU/CPU測定ばらつき、依存互換、容量変動。一般化した予測確率がないため合成不確かさの`u_c`と包含係数`k`は未算出。

**ERROR CHECK:** 全候補についてrepo ID・元総数・配布形式・公開元一次URL・基準品質・原本と派生の独自性・制約を記録。高パラメータ候補を従来の通常PASSへ自動移行しない。取得承認・ダウンロード・ユーザー側の進行中タスクへの介入なし。

**〈次に考える問い〉** 元モデルより一般タスクが少し劣っても、代替不能な特化能力と品質保持の強い証拠があれば、その例外モデルを高価な完全原本より優先保存する価値があるか。
