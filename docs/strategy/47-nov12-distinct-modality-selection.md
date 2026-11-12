# R47｜11月12日の新しい学習成果・非重複選定（v29）

## 1.〈本論〉正式判断と事実・推論の分離

指定ブランチ `strategy/2026-11-03-01-risk`、前版 `v28-20261112`、親コミット `79a533807da1337387612132a5745060e77caeb0`。2026-11-12確認の一次資料と公式HFメタデータを根拠に**独自の学習成果2件のみ**を研究用`conditional`追加。前版175件／有効128件→**v29 177資産／有効130件**（モデル151／データ26、SELECT53／CONDITIONAL77／HOLD28／延期13／EXCLUDED6）。機能だけが似ている重みは通常の量子化と同一視しないが、不要な形式多重保存も行わない。

**事実（publisher/HF）**：ZONOS3-Miniは2026-11-09公開の43言語TTS、独自ZAC-1音声Codec、Gated DeltaNet＋Attentionの潜在MoE、DPO/GRPO、話者複製と語単位の条件付き制御。開発元の技術記事は主要LM「総800M/活性100M」、[公式モデル情報](https://www.zyphra.com/models/zonos3-mini)は「総886M/活性100M」と報告。活性数を150B上限比較に流用しない。ZONOS3の公開Hub全repoは**約30.7GB**で、PyTorch原本/GGUF/WebGPUの複数表現が入る。[公式推論実装](https://github.com/Zyphra/ZONOS3-Mini)はPyTorch標準構成 `lm/`+`autoencoder/`+`speaker_encoders/` を**約9GB**と説明。**完全に再現可能な「全機能編集システム」ではない**：語単位編集の一部は非公開の編集用LoRA、別のFuseAlign・Qwen3-ASRなどが必要。原本の公開TTSだけを選定し、非公開編集部品にはアクセスしない。

**事実（publisher/paper）**：LingBot-Touch-Tinyは同月9日公開の約**5.46M**の凍結JEPA触覚Encoder。3つのセンサー技術の触覚token表現を学習し、26現実ロボットタスクの研究はTinyで実施。Tinyは`encoder.pt`＋`config.json`の約22MB級で、[公式推論コード](https://github.com/Robbyant/lingbot-touch)を別保全する必要。これは**触覚アダプタであり動作ポリシーや再訓練用全データではない**。センサー較正、5指の順序、形式・正規化・実機が重要。TinyとSmallは別重みだが、Tinyで26件を評価しているためSmallを自動採用しない。コードはPython3.12.13／PyTorch2.11.0／NumPy2.4.4（公式のテスト条件）、モデルは`torch.load(weights_only=True)`を前提とする`.pt`でありダウンロード時にimport/executeしない。

一次資料（原論文含む）：[Zyphra技術記事](https://www.zyphra.com/our-work/zonos3-mini) ／ [Zyphra公開Hub](https://huggingface.co/Zyphra/ZONOS3-Mini) ／ [Robbyant公式プロジェクト](https://technology.robbyant.com/lingbot-touch) ／ [LingBot公式コード](https://github.com/Robbyant/lingbot-touch) ／ [LingBot論文arXiv:2611.12806](https://arxiv.org/abs/2611.12806)。Zyphra公式実装コードの観測SHA `3a294675a06dd496242e8dbdf2232116a874f67a`、LingBotコード `dec8025b212e7099b235cc2ef13a4921a7e59545`（2026-11-12 GitHub公開参照）；**HFモデル重み自体のコミットではない**。

## 2. 比較した他の候補と見送り理由

| repo ID・一次URL | 総数・容量の一次情報 | 他モデルからの独立性 | 判断と反証 |
| --- | --- | --- | --- |
| [nvidia/Alpamayo2-Edge](https://huggingface.co/nvidia/Alpamayo2-Edge) | HF総2.6512B。2.45B基盤（LM1.96B、SigLIP2 0.41B、投影0.08B）＋行動expert0.2B | Cosmos3 Sim-Autoの動画/LiDAR生成と異なり、カメラ＋車両状態→**走行軌道・理由文**を出す | **優先研究HOLD**：重みOpenMDW1.1、コードApache。H100 80GB、BF16、22画像・batch1・6軌道でプロセス12.06GiBピークは開発元値。実機・権利・外部評価データ未確認 |
| [runwayml/praxis-1-droid](https://huggingface.co/runwayml/praxis-1-droid) | 27.2024B総数、発表BF16約54.4GB。NVFP4量子化学習の別版17.5GBは原稿の別モデル形式 | joint video+action DROID調整。YAM・baseは**別学習状態**なので普通の量子化と同一視しない | **比較研究HOLD**：既存Cosmos/π0/Puffin/GR00Tとの用途重複、メーカーRoboLab120の46.2%を独立実測として採用しない。DROID/YAM/Base/NVFP4全取得しない |
| [abel-lab/Simons-297M](https://huggingface.co/abel-lab/Simons-297M) | 297.2M総数、OpenMDW1.1、学習ソース一部公開 | 9分位点予測と未来既知共変量、TinyTimeMixer R3とは異なるが時系列領域で重複 | **比較HOLD**：v28でTiny TTM、既存Chronos2をすでに選定。GIFT-Eval/fevを同条件で比較。学習データ別ライセンスにも留意 |
| [IFM/PAN2](https://huggingface.co/IFM/PAN2) | 29.202B、Apacheタグ、画像＋行動テキストから最大20秒の将来動画 | 既存のCosmos/Puffinや提案PrimeSimと同じ世界シミュレーション分野だが独立学習済み | **HOLD**：selected sharding、動画評価・復元依存・実機性能未確定 |
| [robbyant/lingbot-touch-small](https://huggingface.co/robbyant/lingbot-touch-small) | 近似87MB repo（独立非一次情報）、**Small総数は一次資料から未確定** | Tinyより大きい別encoderだが実ロボット26タスク検証はTiny | **HOLD**：両方は過剰。Smallのみの明確な追加精度を確認してから。総数不明で取得準備STOP |

**能力宣伝と保全判断の違い**：ZyphraのH100/8並列でTTFA中央値80ms、最適並列457秒音声/秒、メーカー評価のZTTS2優位性は独立実測でない。Robbyantの26実機タスクも開発者実験。NVIDIA H100ピークは別モデル・別ハードの実機値ではない。全モデルの現実の規制確率は作らない。

## 3. 容量・ハードゲートの変数表

| 記号 | 意味（日本語） | SI単位 | 定義 | 型／定義域・条件 |
| --- | --- | --- | --- | --- |
| `C` | ユーザー申告の計画保存上限 | byte | 4,000,000,000,000 | 非負整数スカラー。実HDD空き未測定 |
| `F_min` | 実機の最低空き | byte | 200,000,000,000 | 非負整数スカラー。独立の物理制約 |
| `B_v27` | 以前の126件に関する既知SHA重複控除ソース | byte | 3,417,685,712,585 | 非負整数。完全な復元バイトではない |
| `R_{28}` | v28小型2件の研究予約 | byte | 2,700,000,000 | 非負整数、未実測 |
| `R_{29}` | 新2件の研究予約 | byte | 16,300,000,000 | 非負整数。ZONOS3の全repoと違う想定、最終ファイル量でない |
| `P_{Z}` | ZONOS3-Miniの公表モデル総パラメータ | 1 | 886,000,000（製品画面概数）、活性100,000,000は比較対象外 | 非負整数、構成厳密センサス保留 |
| `P_{T}` | LingBot Tiny凍結Encoderの公表総パラメータ | 1 | 5,460,000（作者概数） | 非負整数、モデル実体テンソル未計数 |
| `M_{peak}` | OS/KV/backend/全学習済み部品込み推論ピーク | byte | null | 実機・backend/zero-point/context/batch未測定 |

**次元検査**：`B_v27`、`R_{28}`、`R_{29}`、`C`と`F_min`はいずれもbyteで算術比較できる。**ただし予約と測定値を足した結果は実際の残容量ではない**。モデル総数は無次元で、活性expert数と重みbytesも混同しない。ユーザー実機が4TB容量・200GB空き安全床を同時に保てるか、payload/cache/staging/独立依存の実ファイルSHAとバイトを確定するまで取得承認不可。150B超のモデル量子化例外は現行の同HW/同条件での実測比較HOLDを維持。

## 4. H / T / D / C / U と ERROR CHECK

- **H**：触覚JEPAとZAC-1基盤TTSは既存v28の学習済み状態と同じ単なる量子化ではなく、比較不可能な独自機能を少ないモデル個数で保存する価値がある。
- **T**：HF2リポジトリの40文字SHA、対応する重み＋codec/encoder/付属license、README/noticeとbyte/上流SHA256、GitHub参照コード・ABIを固定。安全な静的メタデータ検査のみ。この後ユーザー取得・実行を別途許諾した場合だけ、日本語TTS（短文・長文・同意済み話者）と触覚各センサーの代表サンプルを各30例以上で同HW/clock/backend/条件を合わせて比較。
- **D**：PASS＝独立重みと一意repo ID、非実行conditional採用、モデル数の公表上限内。FAIL＝法的許諾違反、必須依存入手不可、総数/容量の硬い制約未達。UNCERTAIN＝ファイルSHA、本人権限、実機速度や品質未実証。
- **C**：語単位編集に必要な非公開LoRAを持たず本来狙う用途が欠落する、ZONOS3日本語に競合モデルとの差がない、Tinyの凍結Encoderを実ロボットの自律制御モデルと誤認する、センサー較正が異なる。
- **U**：元モデルの更新、主重みとcodec総数、推論ABI、外部権利、実機空き、性能独立評価に欠測。繰返し測定に基づく合成標準不確かさ`u_c`と包含係数`k`は未算定。

**ERROR CHECK**：既存175件の判断/順序はすべて維持。全177件一意、151モデル/26データ、有効130、SELECT53/CONDITIONAL77/EXCLUDED6/HOLD28/延期13、PASS総129/総数不明20/超150B例外2。取得承認0、モデル本体取得/実行0。CI単体テストはこの報告作成時に実行したとは主張しない。

**学際転用**：音声工学（Codec/話者・同意）、ロボティクス（触覚・視覚・行動条件付け）、時系列・シミュレーション（異なる予測対象）、デジタル保存と供給網（SHA/ABI/権利）に共通する保全方法。

###〈次に考える問い〉
同じ4TB枠に収めるため、重み配布形式の多様性よりも、触覚・非生成判断・行動軌道・音声制御といった**異なる学習済み情報の復元可能性**を何件保全できるかで次の順位を決めるべきではないか。
