# 全二重・音声マルチモーダル模型の候補監査（2026-11-10）
> GitHub `Unjuno/local-model-portfolio` / `strategy/2026-11-03-01-risk` / 基準 `16d198a01aa669d8b7d6abed21fbe2e0630ff91f`。**v27の173件と承認キュー0件は維持**。公開配布元メタデータのみ。モデル重み・依存ソフトウェアは取得/実行していない。

## 1. 〈本論〉保存選定
- **P0研究候補**：`openbmb/MiniCPM-o-4_5`（音声・映像の時間軸統合、独自学習結果）、Sophon Tag（CC BY-NC由来権利とABIを先に解消）、`nvidia/personaplex-7b-v1`（本人Gated同意確認優先）。
- **P1研究候補**：`kyutai/moshiko-pytorch-bf16`（Moshi基礎checkpoint原本）、`HIT-TMG/Lychee-FD`（階層音響・意味分離の独立学習成果）、Sophon Flash（Tagと32B中枢を重複排除し独立の音声生成部を保全）。
- **P2研究候補**：Sophon E2E（連続音声表現のプレビュー、2×80GB GPU）。`PranavHarshan/SmolDuplex`は重みが**0件**なのでHOLD、実在するチェックポイントとしては数えない。
- 新しく候補にしたモデルは全て現行v27に未登録。ユーザーの承認権を越えて採用・取得しない。

| 候補 | 固定revision | ソース全ファイル（B） | Hub報告param | 権利/状態 |
|---|---|---:|---:|---|
| [openbmb/MiniCPM-o-4_5](https://huggingface.co/openbmb/MiniCPM-o-4_5) | `fb09628e98b1f55d8d5b863e0eccfcdd11bff499` | 20,048,635,820 | 9,371,787,666 | apache-2.0, PUBLIC |
| [kyutai/moshiko-pytorch-bf16](https://huggingface.co/kyutai/moshiko-pytorch-bf16) | `2bfc9ae6e89079a5cc7ed2a68436010d91a3d289` | 15,760,704,992 | 7,687,729,152 | cc-by-4.0, PUBLIC |
| [nvidia/personaplex-7b-v1](https://huggingface.co/nvidia/personaplex-7b-v1) | `fdaf4090a61cb315c138a1faee287ffd6c716309` | 17,135,667,560 | 8,371,408,896 | nvidia-open-model-license, GATED_AUTO_USER_CONSENT_MISSING |
| [HIT-TMG/Lychee-FD](https://huggingface.co/HIT-TMG/Lychee-FD) | `ac06087bef70b33d4dfebf63a3eadadb4e024f33` | 25,630,746,830 | 12,812,043,520 | apache-2.0, PUBLIC |
| [PranavHarshan/SmolDuplex](https://huggingface.co/PranavHarshan/SmolDuplex) | `cca4a5e1ed0703650b97cb4beee480a726672be3` | 12,430 | MODEL_WEIGHT_MISSING | LICENSE UNKNOWN, PUBLIC_DOCUMENTATION_ONLY |
| [stepfun-ai/Step-Audio-2-mini](https://huggingface.co/stepfun-ai/Step-Audio-2-mini) | `e36fdd5d71e0ea22f09dd94bbab9bfc544ca1e36` | 1,231,244,352（token2wav限定） | 外部decoderの個別全学習済み数未確証 | Apache-2.0表示／外部依存のみ |

- MiniCPM-o [一次論文](https://arxiv.org/abs/2604.27393) はOmni-Flowのfull-duplex音声映像同時入出力を説明。Hugging Face全体のsafetensors総数9.37Bはreported、完全な外部学習済み総数は未確定。開発元の全二重Webデモは**28GB以上のNVIDIA GPU**を要求。推論一般の「bf16 19GB」と同条件の保証はない。
- Moshi [一次実装](https://github.com/kyutai-labs/moshi) はMimiと同時音声出力の元祖。PyTorch推奨約24GB GPU、PythonとRust/MLXは異なるruntime前提。原本1版を優先し普通の量子化複製はしない。
- PersonaPlex [配布元](https://huggingface.co/nvidia/personaplex-7b-v1) はGated自動受付。匿名APIでは重みのsha256が伏せられるため、正しい完全ロックは不可能。使途は[NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/)に従い個人受諾が必要。
- Lychee-FD [一次論文](https://arxiv.org/abs/2607.06540) は独立のnative full-duplex階層分離モデル。カスタムvLLMと外部token2wavが必要、開発元はGPUを分離する構成を基本例とする。
- `SmolDuplex`の当該リポジトリは文書3件合計12,430B、学習済みファイルは0件。単なる宣伝文を保存候補として採択しない。

## 2. 外部trained依存・重複の確定範囲
- Lychee-FDの必須token2wav外部依存5ファイル、**1,231,244,352 B**を[Step-Audio-2-mini](https://huggingface.co/stepfun-ai/Step-Audio-2-mini)の固定revisionで検査した。
- MiniCPM-oの`assets/token2wav/`と**4ファイル1,231,243,253BのLFS payload SHA-256が一致**：`campplus.onnx`、`flow.pt`、`hift.pt`、`speech_tokenizer_v2_25hz.onnx`。追加メタデータ`flow.yaml` **1,099B** のみ。JSONに両ソースパスと64桁SHAを収録。
- これは**同じ学習済みコンテンツの同一性**のみを証明する。学習元の再配布条件と2実行環境が実際に互換かは未確認。
- Sophon Tag+Flashのv27に対する**確認済みハッシュのみ控除した**追加ソース上界=48,480,869,294B。Sophon E2E差分上界=78,992,470,316B。Sophon CC BY-NC→ApacheとDuplexJev audio_length ABIに未解決事項あり。前回調査 `catalog/research/2026-11-10-sophon-provenance-followup.json`。

## 3. 容量・選定の反証可能性

| 記号 | 意味 | SI単位 | 定義、範囲、型 |
|---|---|---|---|
| `B_0` | v27で分かっている選択ソースの重複排除バイト | B | 3,417,685,712,585、非負整数スカラー |
| `B_i` | 新規候補の固定スナップショットのバイト | B | 0以上の整数スカラー |
| `B_s` | SHA-256一致により控除する重複データ | B | 0以上の整数スカラー、原データ同一性のみ |
| `B_case` | 候補組合せごとのsource-only上界 | B | `B_0+sum(B_i)-B_s`、非負整数スカラー |
| `C_real` | 実機のフォーマット後の物理容量 | B | 現時点は不明の非負整数スカラー |
| `C_extra` | ソフトウェア、キャッシュ、既存ファイルと一時領域 | B | 現時点は不明の非負整数スカラー |
| `F_min` | 最低維持すべき空き | B | 200,000,000,000、スカラー |

**必要条件**：`B_case+C_extra+F_min<=C_real`。各項Bなので次元は整合。ただし最終実行計画では**開始時実測空き容量**と実際の追加ファイル量が必要で、この式は空ボリューム仮定の容量計画のみ。

| 仮定の保存組合せ | 既知source-only上界（B） | 空・フォーマット済3.8TBと200GB維持の場合のソースのみの余裕（B） |
|---|---:|---:|
| v27_only | 3,417,685,712,585 | 182,314,287,415 |
| v27+MiniCPM+Moshi | 3,453,495,053,397 | 146,504,946,603 |
| previous+Lychee_and_step_dependency | 3,479,125,801,326 | 120,874,198,674 |
| previous+SophonTagFlash | 3,527,606,670,620 | 72,393,329,380 |
| previous+GatedPersonaHypothetical | 3,544,742,338,180 | 55,257,661,820 |
| previous+SophonE2EHypothetical | 3,623,734,808,496 | -23,734,808,496 |

- 上記の3.8TBは**仮説の物理容量**。持ち主のHDD実測値でも、現在の空きでもない。余裕が正でも必要な学習済み外部部品・ABI・Python環境・キャッシュを引く必要があるためどれも正式な容量PASSではない。
- 4.0TBは現行ポリシーの選定上限で、空き200GBを維持するなら完全保存の合計が物理ボリュームに入るか別途測定する。提案v28の追加約145GBと全候補を無条件で重ねない。

## 4. セキュリティ・権利ブロッカー（事実と仮説）

- Sophonの**オプションLiveバックオフィス**は`SOPHON_LIVE_BACKEND`を有効にした場合、`SOPHON_LIVE_BACKEND_URL`のデフォルトが[Alibaba DashScope](https://github.com/adventists-ai/sophon-realtime/blob/3585943e8f6ea33ebfc4d077d24b4b59bbde924c/live/sophon_live/backend.py)。対話タスク・蓄積した会話文脈がそのURLにPOSTされ得る。**外部バックオフィスを使わないコア音声処理まで外部通信すると断定しない**。オフラインで使う場合は明示的に無効化し、ネットワーク監査を行う。
- Sophonの派生元DuplexJev完成モデルはCC BY-NCとデータ制約を明示する一方、SophonのLICENSE/NOTICEはApache-2.0を記載。同じ配布者の二重ライセンス等もあり得るので違反認定はしないが、権利の連続性が証明されるまではHOLD。
- `duplexjev-vllm==0.3`と上流の`>=0.4`に関する音声末尾処理互換性は静的な疑義であり、Sophonの実際の故障ではない。
- NVIDIA PersonaPlex Gatedのユーザー同意状態は確認不能。**公開ファイル一覧・許諾を取得できたとは扱わない**。Gatedモデルの認証・利用規約を回避しない。
- model cardの公称ベンチマークは開発元報告。MiniCPM/Moshi/Sophonの比較は公開された評価手法・日本語入力・長時間・相づち・割り込み・GPU/driver/clock/context/batchを固定した独立追試が不可欠。

## 5. H/T/D/C/U、ERROR CHECK

**H**：機構の異なる音声対話モデルは、通常量子化のみを多重保持するより高い保全価値を持つ。独立重み・訓練由来・同時音声処理を確認することで反証可能。  
**T**：現行v27と独立に公開6repo全件を固定revisionで走査、別途GPU/メモリとライセンスが承認されてから同一条件で最低30試料/条件を計測。  
**D**：ツリー整合、ハッシュ差分、明示的に無い重みの検出=PASS。配布権・Gated本人承認・完全パラメータ・実行・実機容量=UNCERTAIN/NOT APPROVED。  
**C**：公開IDが実行不可・コード依存欠落、音声コーデック互換性不成立、音声の長時間割り込み品質不十分、校正不良、ライセンス不一致。  
**U**：数値標準不確かさ `u_c` と包含係数`k`は、モデル本体を実測しておらず未知。容量の主誤差源は物理容量/外部trained依存/ステージング、性能は測定HW/負荷。

ERROR CHECK：**13項目PASS**。変更は専用ブランチの新規非実行調査資料だけとし、元カタログ/承認キュー/本体重みは改変しない。

## 6.〈応用・転用例〉・次に考える問い

機械学習：独立訓練の結果と全二重処理機構を保存。法務：CC BY4／NVIDIA Open Model License／CC BY-NC継承を分離。デジタルアーカイブ：同一LFS重みを1回保存し、復元時に原パスを再生成。運用・プライバシー：GPU/ABI、外部HTTP送信既定値を監査。

**問い**：3.8TB程度の実容量が確定した際に、Sophonの一式を後回しにしてでも、MiniCPM-oとMoshiの別機構を先に確保する方が保存リスク分散につながるか。実機容量と権利の確定後に決定する。
