# 43 — 新たな学習成果3件の条件付き選定提案（2026-11-08）

## 1. 〈本論〉結論と正本

現在の`catalog/CURRENT.json`は**v27／173資産／有効126資産／承認取得0件**である。本書は新規の訓練成果を三件**v28条件付き追加候補として採用する判断案**であり、`CURRENT.json`、有効126資産、キュー、権利状態を**この段階で変更しない**。正式v28化は一意性・総数・保存範囲・依存・CIの機械検査を通す別工程とする。詳細と各停止条件は[構造化提案JSON](../../catalog/proposals/03-v28-original-models-2026-11-08.json)を正とする。

**判定：3件追加提案／4件HOLD／同系統の余分な量子化・Base・checkpoint重複追加0件。**

| 優先 | 候補（配布元一次URL） | 独立の学習成果と既存の比較 | 対象範囲、容量上限（計画値） | 判定 |
| --- | --- | --- | ---: | --- |
| 1 | [`beipo-ai/NorthCUA-Mini`](https://huggingface.co/beipo-ai/NorthCUA-Mini) | Qwen3.5-35B-A3BからGUI長期タスクへの追加学習。既存Fara/Holo4とは別checkpoint。NorthCUA-Nanoは同族重複なので保存しない | BF16全16 shard＋Harness等、**75GB** | v28 conditionalを提案 |
| 2 | [`qiyuan-robot/PrimeSim`](https://huggingface.co/qiyuan-robot/PrimeSim) | 22プラットフォーム・30,110時間の行動付き複数視点学習。Cosmos3 Bimanual/Sim-Autoとは**学習データと時間条件付けが異なる**。Wan2.2 baseを再度保存しない | **`primesim_posttrain_g2.safetensors`1つ**＋再利用未確定のWan2.2必須部品。**26GB** | v28 conditionalを提案、完全総数/固定SHA未確定 |
| 3 | [`meta-models/Muse-Glimmer-30B`](https://huggingface.co/meta-models/Muse-Glimmer-30B) | Muse Spark蒸留の視覚対応エージェントと独立DFlash支援。既存Qwen/Gemma/Holo4とは別訓練系統 | **BF16原本1系統**＋DFlash支援モデルを精査。GGUF二形式・ExecuTorch全量は重複させない。**70GB** | v28 conditionalを提案 |

## 2. 現在の一次事実・評価限界

### NorthCUA Mini（2026-11-03までの固定公開情報）

[開発者モデルカード](https://huggingface.co/beipo-ai/NorthCUA-Mini)／[公式GitHubのモデル・固定SHA対応表](https://github.com/beipo-ai/NorthCUA/blob/main/docs/models.md)／[技術報告 arXiv:2611.02102](https://arxiv.org/abs/2611.02102)。**総約35.107B**（HF metadata、全MoE experts）、推論時活性約3B。16 shardのtensor payloadは開発元**70,214,363,872 B**、repoは約70.23GB。公式GitHubがチェックしたHF版 `cafee9af6a950bffea2a4a17544f253abf80d44b`、Apache-2.0、NOTICE、SHA256 manifest、`Qwen3_5MoeForConditionalGeneration`、Transformers 5.20.2出力。**総パラメータと活性パラメータを混同しない**。配布元の`beipo-ai`名と`china-beipo`の転送関係は固定URLを再照合する。

開発元報告：OSWorld-Verified **85.30%（361タスク）**、WebArena-Verified **70.43%（812タスク）**、最大100ステップ。NanoのOSWorld 78.90%より開発元同系列評価で優れる。ただしモデルカード自身が「このエクスポートのcheckpoint975と報告書の個別成績を同一視しない」と明記。**独立測定値ではない**。Harnessは`normalized_1000`座標を画面ピクセルへ変換する契約。**GUIの画面情報を命令源として信用しない**ことも必要。

### PrimeSim（2026-11-06に公開された重みと実装）

[公開元重み](https://huggingface.co/qiyuan-robot/PrimeSim)／[公開元コード](https://github.com/PrimebotTech/PrimeSim)／[一次論文 arXiv:2611.04870](https://arxiv.org/abs/2611.04870)／[著者プロジェクト説明](https://primebottech.github.io/PrimeSim-website/)。
別々の`primesim_base.safetensors`と`primesim_posttrain_g2.safetensors`から、**4-step推論の後学習G2のみ選定**。親Wan2.2-TI2V-5Bはv27で既選定済み。公式ソース参照Git commitは`b1e92466184da1bf3c55cc1a555dc4c2a06a597a`。本体は約5B、重み約10.1GB。ただし**全学習済みpipelineのtensor総数、HF原本の完全revisionとSHA、依存SHAは未検査**であり最終取得lockは禁止。親のT5 encoder/VAE/tokenizer約14GBは別部品であり、既保存分と同一SHAの確認前にゼロ増分とはしない。

開発者報告の生成速度は約**10.1 frames/s**、**単体NVIDIA A100 80GB・BF16・3視点・各288×384・4 denoise step**。GPUクロック・バッチは不明。機種の異なる所有者PCでは未測定。モデルは行動から未来映像を作るものであり、既存の行動ポリシーや映像生成APIと同じ成果物ではない。

### Muse Glimmer 30B（2026年8月公開・2026年10月まで資料更新）

[Meta公式モデルカード](https://huggingface.co/meta-models/Muse-Glimmer-30B)／[配布と構成の公式解説](https://dev.meta.ai/docs/muse-glimmer/get-the-model)／[投機デコードの公式解説](https://dev.meta.ai/docs/muse-glimmer/spec-decode)。原本は約**29.8Bパラメータ、BF16約59.6GB**、Apache-2.0表示＋`USAGE_POLICY.md`。推論用GPU常駐は公式が約72GBと説明。BF16固定元候補`f84ecc3a0ea984a4c04542a84269e3d065350a6e`と公式別レシピの`a4e59da52a7bc87ae7251dd5545c0dd437c44b68`の差分は最終lock前に確認。DFlash別repoを独立した速度改善学習部品として扱い、単なる同じ本体の量子化と混同しない。

Metaの**RTX 5090／llama.cpp／batch=1／greedy／K-QuantとDFlash**の報告は、標準74.9 tok/s、DFlash 233.4 tok/s。この値は**BF16原本の測定値ではない**。同条件で本体＋drafterの品質、RAM/VRAM、ABIを実機で照合する。

## 3. 今回採用しない4件

| 研究対象 | 判断 | 根拠 |
| --- | --- | --- |
| [Verne V0.5 base](https://huggingface.co/vernerobotics/v0.5-base) | **HOLD（権利）** | 独自world-action学習、約8.2B。ただし手動Gated、独自ライセンス、本人許諾未確認。1つの原本・LIBERO版・RoboTwin版を無条件に3重保存しない |
| [Base Labs Joey-1](https://huggingface.co/baselabs/joey-1) | **HOLD（重複比較）** | MIT・2.72Bの独立確率判断学習。ただし直近選定Kananaのchoice/noul/scoreと用途重複。較正精度・応答コストを同条件で比較するまでは追加しない |
| [NorthCUA Nano](https://huggingface.co/beipo-ai/NorthCUA-Nano) | **HOLD（同族）** | 同一学習系統。Miniがサイズ・推論制約で失格なら置換候補。両方を当然には保存しない |
| [NorthCUA Pro](https://huggingface.co/beipo-ai/NorthCUA-Pro) | **HOLD（総数/RAM）** | 約397B総数・17B活性。v27の150B超量子化例外について同一環境の実測証拠なし。取得不可 |

## 4. 容量 — 4TBを「埋めるため」に選ばない

| 容量項目 | 値 | 証拠範囲 |
| --- | ---: | --- |
| v27既知選択コンテンツ集合 | 3,417,685,712,585 B | [v27容量監査](../../catalog/capacity/2026-11-07/v27/capacity-summary.json) |
| 今回3件の政策上の追加予約上限 | 171,000,000,000 B | NorthCUA 75GB + Muse 70GB + PrimeSim依存込26GB。**測定した追加容量ではない** |
| v27既知集合＋予約枠（机上計算） | 3,588,685,712,585 B | 重複がない保守的仮定、その他の未解決依存は別 |
| 4TB計画上限との差 | 411,314,287,415 B | **実ディスク空きではない** |
| 最低物理空き | 200,000,000,000 B | 物理ストレージ実測は**未実施** |
| 完全オフライン復元・ピークstaging | **UNKNOWN** | source code、tokenizer、codec、cache、environmentを別途固定 |

**単位表（式を伴う場合の変数）：**

| 記号 | 意味（日本語） | 単位(SI) | 定義 | 定義域・範囲・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| B | v27既知論理容量 | byte（情報量） | v27 source scopeのSHA考慮集合 | 3,417,685,712,585 B、完全復元容量ではない | 非負整数 |
| R | 新3件の予約上限 | byte（情報量） | 三件の政策枠の合計 | 171,000,000,000 B、実測値ではない | 非負整数 |
| C | 計画上限 | byte（情報量） | 保存計画で使う上限 | 4,000,000,000,000 B | 非負整数 |
| U | 机上差額 | byte（情報量） | CからBとRを差し引く算術差 | 実容量Fと同一視禁止 | 整数 |
| F | 所有者の物理空き | byte（情報量） | 実機で読み出す空き | 未測定、最低200GBを要求 | 非負整数またはnull |

次元検査：B・R・C・Uはいずれもbyteで加減算可能。UとFは**同じ単位だが異なる定義対象**であり等置できない。総パラメータ数（個数）と容量（byte）も混同しない。

## 5. H/T/D/C/U・検証

- **H**：同一群の多形式重複を除き独立した訓練結果3件に絞ると、同予算で異なるGUI/ロボット映像/エージェント学習を保全できる。予測であり検証待ち。
- **T**：最少3モデルの元配布元、全shardとindex、権利、3系統の実行ABI、500GBを超えない合計総数などを確認。別に173基準IDとの重複全件検査、150B以上の有資格化は別検査。計測前にdownload/実行しない。
- **D**：PASS＝v28昇格前に三件の固定版・LICENSE・正確な増分bytes・依存closure・総学習パラメータ・同族非重複を検証し、承認キュー0を維持。FAIL＝同じ量子化の二重保存、著作権/Gated侵害、150B上限例外誤用、暗黙のダウンロード。UNCERTAIN＝実HDD空き、性能・codec・hashなどが未解決。
- **C**：Museが既選定と能力重複し学習成果の差が薄い、PrimeSimの依存復元が不可、NorthCUA Harnessの制御契約が合わず長期GUI操作が再現できない。
- **U**：主要誤差源は配布元の丸めサイズ、未確定の増分bytesと追加部品、本人利用権限、必要実行時メモリ。分布を仮定していないため合成u_cと係数kは算出しない。

学際連関：**機械学習**（独立した追加学習・蒸留）、**ソフトウェア供給網**（source SHA、Harness、ABI）、**デジタル保存**（依存closure、復元テスト）、**ライセンス・ガバナンス**（Gated/地域/用途条件）がいずれも必要。

## 6. ERROR CHECK と〈次に考える問い〉

今の提案ファイルに対して静的に、元173件に新3 IDが無いこと、提案3件一意、総150B未満の開発元数値、新規取得承認0、政策枠171GBを確認する。**GitHub Actionsによるv28適用・実際のモデル実行・重みファイルhash一致・物理容量実測は未実施**。

次の問い：モデルの原本そのものと、学習済みの投機ドラフターや復元必須encoderを、どの条件で「親に付く依存」と「別個の保存資産」に分類するべきか。
