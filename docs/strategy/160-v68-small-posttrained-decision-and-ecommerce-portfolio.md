# R160／v68（2026-11-25）—小型4つの独立trained originalsを正式CONDITIONAL選定

## 1. 結論・正本不変保証

**v67（248登録／199有効）からv68（252登録／203有効：SELECT56、CONDITIONAL147、HOLD30）へ、既存248 assetのJSON行を完全不変で4原本追加**。既取得報告116モデルは全repo IDを維持し、二重再取得しない。正式CONDITIONALは原本の保存価値についての研究判断であり、モデルの実際の取得承認ではない。現行`queues/approved.json`は空のまま、追加ペイロード・ユーザー媒体変更・未審査コード実行0。

4Publisher full repository sourceを[固定リビジョン・全75file・Git SHA1/LFS SHA256](../../manifests/drafts/r160-2026-11-25-four-small-trained-states-75file-publisher-frozen.candidate.json)で照合。全ソース合計 **17,608,061,719 byte**。12組の出版社完全一致補助ファイルは **20,076,087 byte**、Publisher SHAベースのユニークファイル参照合計は **17,587,985,632 byte**（user所有媒体では確認未実施）。

## 2. 正式CONDITIONALにした4種類

| 原本 | First-party scope | 既存との差・用途 | 重要な負の証拠 |
| --- | ---: | --- | --- |
| [openbmb/MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B/tree/42433e90dad95123ab87729fd7011e7110629556) | 11 files・5,043,807,977 B | 2,516,756,480 backbone要素、Llama42層、131,072文脈、コード/数学/Agentに対してRL+OPDで学習した最終原本。別学習段階Base/SFT/Midtrainと量子化GGUF/MLXは別保全優先度に分ける | 出版者の平均53.9（比較セット内最高51.1）は評価者HWで再現なし。131kのピークKV/ABI・日本語性能未証明 |
| [illuin/Ivonnet-0.8B](https://huggingface.co/illuin/Ivonnet-0.8B/tree/6a6a979489d262861ad3c34faaa1a763d1ce4baf) | 21 files・1,728,496,331 B | Qwen3.5-0.8B `2fc063...` をIVE-4Bから蒸留した**独立学習済み判定モデル**。BF16 backbone＋別FP32 `readout.safetensors`、255選択肢/非生成型、画像判定用途で非常に小さい | 出版者Decision Index vision 47.6（<=1Bの10モデル中2位）、ECE2.3%、英語中心。文章判定は#14/73。FLASH Linear Attention/CUDA/Python runtime未評価 |
| [illuin/IVE-4B](https://huggingface.co/illuin/IVE-4B/tree/1e65613dfd83ba6949883325fc5f4791dae56a46) | 23 files・9,102,712,961 B | Qwen3.5-4Bの**別フルfine-tune**と255 codeの学習済みreadout。ページ画像から直接確率判定、文書・図表・リランキング。Ivonnetとはteacher/studentで異なる重み | 作者公開結果はnew-domain private taskで5B以下166モデル中1位、vision65.5、ECE1.6%（2026-11-21）。独立実測なし・日本語未知。RTX PRO 6000のベンチを所有者HWへ外挿しない |
| [tencent/WeMM-Ecom-0.8B](https://huggingface.co/tencent/WeMM-Ecom-0.8B/tree/b40297975d72386f1c53103371d80ae0e5a9bd58) | 20 files・1,733,044,450 B | Qwen3.5-0.8BをEC商品画像/動画・OCR・属性理解に後学習した別trained state。一般的なWeMM-Video-2Bや0.8B decision型とは異なる目的 | 作者の28 EC+64一般ベンチ比較でQwen親にEC平均+16.43pt、general平均+6.93pt。検証独立性不足。TorchCodec/FFmpeg/video ABI未審査 |

Ivonnetの学習元であるQwen3.5-0.8Bは最新の取得レシート116で記録された**同じ親リビジョン**。しかしIvonnetは単純な親への量子化ではなく蒸留済み単独モデル。IVE-4BのQwen3.5-4B訓練親は明記されているが、**推論のため親重みを別ダウンロードする必要はない**（公開元のfull backbone + readoutが揃う）。商用/学術の行為別Apache2と作者NOTICEは別途所有者の確認を要する。

## 3. 入れ替え・保留・容量

既登録のHeretic-LoRA Qwen0.8B、Smaug DPO、OpenUncensored Inkling編集は保全し、今回のテキスト性能未比較の新モデルを理由に**勝手に置換・削除しない**。MiniCPM5のBase/SFT/Midtrainは異なる学習段階だが今回正式追加せず、特殊な学習史研究に対し追加約5GBずつの価値が証明されるまで研究HOLD。GGUF/MLX/GPTQ/FP8の同重み形式は別trained stateに数えない。DSpark draftなど別学習された加速補助重みは量子化変換と区別し、別ゲート評価。

新規4源の公開元ハッシュ一致12組は補助ファイルの共有可能性を示すが、**所有者実HDDのSHAを確認するまで実削減容量ではない**。親重みとの共通tensorに関する実測も無い。全有効203資産を閉包してから4TB archive上限／実空き200GB floor/キャッシュ/部分転送領域・実GPU RAM<512GBと照らす。116取得台帳の報告2.022TBと現在実ドライブ容量は同義ではない。

規制：米BIS [2026-11-19 91 FR 74970 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion RuleモデルウェイトECCN4E091を**撤回**。将来の一律open weights禁止は未確定。LICENSE/Gated/輸出先・最終用途・配布元の公開撤回の可否は独立の法的事実・仮説として分類する。ユーザーの特定モデル/ファイルscopeの明示承認が無ければ実取得しない。

## 4. 実測設計、変数表、誤差管理

```text
H 反証可能仮説：これら4つの別trained outcomeは1) 既存登録重複でない 2) 小容量か専門能力を持つ 3) 正式条件付き保全に価値がある
T 最小検証：75 Publisher source SHA/bytes全照合；既存248行完全保存；116報告済みsource-ID重複0；203 active queue/readiness/prepと147 conditional access ID一致；approved0。
  本人HW推論：同CPU/GPU/driver/clock/backend/quant zero-point/context/batchと課題集合を固定し各モデル最低n=30、中央値・分布・95%CIを記録。
D メタデータPASS、Owner実媒体SHA・全依存offline復元・本人LICENSE/権利・品質はUNCERTAIN/STOP。未承認モデルDL/未監査任意codeの実行はFAIL。
C 編集済みtrainedモデルが一般品質を損なう／decision student 0.8Bの分類正確度が4Bに及ばない／EC領域に過適合／親依存が失われる。
U 出版社評価のバイアス、実機性能とモデル名の乖離、tokenizer/vision processor/FLA ABI、Owner現物SHAの不確実性。u_c・kは実測繰返しが無いため数値化できない。
```

**容量の変数表**：

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域/前提 | 型 |
|---|---|---|---|---|---|
| `B_sum` | 4原本publisher参照容量 | byte (B) | 固定75file総和17,608,061,719 | 非負整数、物理ディスク使用量ではない | スカラー整数 |
| `B_dup` | 配布元ハッシュ完全一致の重複ファイル容量 | byte (B) | 12組20,076,087 | Git SHA1/LFS SHA256と整数byte一致 | スカラー整数 |
| `B_unique` | Publisherファイル単位のハッシュ一意参照容量 | byte (B) | 17,587,985,632 | ファイル単位のみ、内部tensorの差分なし | スカラー整数 |
| `B_owner` | 所有者の実追加保管量 | byte (B) | 現物SHA+staging/parent共有後 | 未測定、0以上 | スカラー整数 |
| `n` | 同条件の実測反復数 | 1（無次元） | 各指定条件で最低30 | 環境と課題固定 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 対象測定量のSI単位 | 統合誤差 | 未測定 | 非負実数 |
| `k` | 包含係数 | 1（無次元） | 被覆範囲規定 | 未確定 | 正実数 |

容量の差分を用いる場合の次元検査：十進byteから十進byteを引くため、結果もbyteで整合する。SIのGB（10進）とGiB（2進）、FP32/BF16 tensor数と実VRAMピークを混同しない。

関連分野：**低資源LLM・RL/OPD、知覚と文書判定の知識蒸留、マルチモーダル商用文書理解、サプライチェーンの内容ハッシュ、GPU推論システム、AIライセンス・輸出管理**。これらはソフトウェア保存上の再現性と将来利用可能性を分離して評価する。

**ERROR CHECK（目標）**：正式追加4モデルでv68 252登録・203有効（SELECT56/CONDITIONAL147/HOLD30）、旧248全記録不変。全116取得台帳IDを維持。75Publisher referencesのSHA一致、承認0、owner D実SHA測定0、重み転送0。
