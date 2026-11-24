# R160／v68（2026-11-25）：独立した小型3学習成果の正式条件付き追加と全202件取得停止

## 1.〈本論〉目的・現状・採否

唯一の正本は [catalog/CURRENT.json](../../catalog/CURRENT.json) の **v68-20261125／251登録・202有効（SELECT56／CONDITIONAL146、HOLD30）**。旧v67の248件について`asset_kind`＋`repo_id`を含む**行全体を変更せず**、3件を末尾追加した。既取得報告の116モデル／1,758ファイル／**2,021,784,002,725byte**は取得器が報告したVERIFIEDであり、本作業から所有者Windows D媒体を独立再SHAしたことや再構築が成功した証拠ではない。

本作業で確定したのは**独立学習済みモデルの正式CONDITIONAL選定＋凍結Publisherファイルscope**。権利・本人承認・実機HDD・完全ランタイムの閉包に到達していないため、**モデル重量取得は0バイト、`queues/approved.json`は空、旧モデル削除0**。

一次・検査可能なリポジトリ成果：

- [v68正式追加overlay](../../catalog/revisions/v68-2026-11-25.json)
- [旧248を保存した251資産の派生実体](../../catalog/effective-portfolio-2026-11-25-v68.json)
- [3原本52Publisher file／整数bytes／LFS SHA](../../manifests/drafts/r160-2026-11-25-three-edge-trained-originals-source-freeze.candidate.json)
- [202件全件の研究用キュー](../../queues/proposed-v68-2026-11-25.json)／[146条件付きアクセス](../../catalog/access/2026-11-25-v68-conditional-hub-gates.json)
- [202件取得・権利STOP](../../catalog/readiness/v68-2026-11-25-r160-all202-gates.json)／[202件依存アーカイブ準備](../../catalog/preparation/2026-11-25-insurance-bundles-v68.json)
- [新3件の未承認取得候補](../../queues/proposed-v68-r160-next3-UNAPPROVED.json)／[採否証拠](../../catalog/decisions/2026-11-25-r160-v68-three-compact-distinct-originals.json)
- [回帰テスト](../../tests/test_r160_v68_three_small_originals.py)

## 2. 小型3原本の選択根拠

| 正式CONDITIONAL選定（公開元40桁revision） | 原本全ファイル／容量（十進） | 凍結重量SHA256 | 資産の独自性・悪い点 |
|---|---:|---|---|
| **[tencent/WeMM-Ecom-0.8B](https://huggingface.co/tencent/WeMM-Ecom-0.8B/tree/b40297975d72386f1c53103371d80ae0e5a9bd58)** | **20／1,733,044,450byte** | `5a84c44f4e3beaf16ab0b6aa8238c66a6033291d77b13b81d934098a02d68bf4` | Qwen3.5-0.8Bから**別学習されたEC商品画像・マルチ画像・動画・思考分岐**。原本BF16 single safetensors 1,706,030,496byte。作者28 EC/64一般ベンチ、EC平均+16.43ptを公表するが、独立試験なし。モデル動画実行は`transformers>=5.2.0`、PyTorch、TorchCodec、互換FFmpeg必要。 |
| **[openbmb/MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B/tree/42433e90dad95123ab87729fd7011e7110629556)** | **11／5,043,807,977byte** | `14fb8e7f0a18d53d1f239773758bf581cee7e456a4523a54622c3a245b64402c` | 2,516,756,480要素の事前学習→中間→SFT→**RL+OPD統合最終状態**。5,033,557,096byteの原本single shard。Base/Midtrain/SFTは別学習だが今回追加せず。作者複合平均53.9は異なるタスク/条件が混ざる。**11ファイルに独立LICENSEなし**（HubのApache2タグとGitHubコードLICENSEから重みの本人許諾を自動推論しない）。 |
| **[illuin/Ivonnet-0.8B](https://huggingface.co/illuin/Ivonnet-0.8B/tree/6a6a979489d262861ad3c34faaa1a763d1ce4baf)** | **21／1,728,496,331byte** | backbone `efa1c618389747c10cac685d832788fe0a147e3a0058c30643f9f7c3c7bd164c` + readout `b8edc7c99b4c03e706c537a3a0ae96763ea33bb7d1e9bebebb615e1a6994b08f` | Qwen3.5-0.8Bから**画像・文書の選択肢確率判定**用full微調整＋1,044,560byteの独立学習readout。生成型VLMや既存のInternDecisionとは異なる観測インターフェイス。作者vision index47.6などはowner未再現。Python3.10+、Torch2.6+、Transformers5.7〜6未満、`source/src/decision_model/*.py`のコード審査が必要。 |

凍結原本は計**3repo／52files／8,505,348,758byte／LFS SHA256 13参照／学習済み重量4ファイル**。出版社の完全ファイル参照であって、Owner HDDの将来占有増分・cache・staging・重みの暗号学的現物SHAを証明しない。

### モデル独自性の厳密な境界

- WeMM-Ecom0.8BとIvonnet0.8Bはどちらも元のQwen3.5-0.8Bに由来するが、**Publisher原本重量SHAが異なり、前者はEC視覚・後者は非生成decision readoutの異なる学習成果**。元モデルや既存のQwen-LoRAと同一資産にしない。
- Ivonnetを`model.safetensors`だけで保存するのは不完全。**readout.safetensors＋decision_config＋推論コード＋processor/tokenizer**を全て同一凍結範囲へ入れた。推論時に親Qwen重みをもう一式取得する必要があるとはPublisherは指定していない。来歴の親revisionと実行の自己完結性は別に扱う。
- MiniCPM5 Finalだけをまず保存対象とし、以前に研究固定したBase・Midtrain・SFTを全て同時自動取得しない。別段階の独立性があっても**保存価値/GBや利用目的の確認まではHOLD**。
- TTS StudioYebisu別蒸留、Smaug27B無検閲DPO、nchapman0.8B LoRA、既取得116件は今回の採用で**交換・削除・再取得しない**。多重配布GGUF/FP8/GPTQは他の学習stateではない。

## 3. 実装・権利・媒体の停止境界

3repoは現在Publisherでpublic ungatedとして観測されたが、誰のどの行為にも法的な許可が付与されたわけではない。

| 課題 | 必要条件 | 今回 |
|---|---|---|
| 権利 | 利用、改変、商用提供、再配布、モデル出力利用の**各行為別**LICENSE/NOTICE＋親/データ系譜 | 未確認・STOP |
| 取得原本 | 40桁revision、モデルごとの52ファイルscope、Publisher LFS SHA、Git blob／Owner現物SHA | Publisher静的PASS・Owner SHA未確認 |
| 依存 | WeMMのTorchCodec/FFmpeg/視覚processor、MiniCPMのLlama backendと131k KV、Ivonnet専用readout・ソースcodeとPyTorch ABI | 実機未テスト・STOP |
| 容量 | 保存予算4,000,000,000,000byte、実ディスク空き**常時200,000,000,000byte以上**、cache＋stagingピーク含む | owner現在空き不明・STOP |
| CPU/GPU | 実HW型、driver、クロック、VRAM/RAM、OS、backend commit、context、batch、量子化scale/zero-point、AVX/CUDA/ROCm | 未測定・STOP |
| 個別承認 | 利用者本人が**選択ファイルと取得行為**に明示的に承認し、承認をシステムが勝手に合成しない | 0件・STOP |

旧v67への研究source追加は、既存v67の全件取得ゲート、所有者のLICENSE承認やHDD検査をPASSに昇格する理由にならない。新v68は[202件readiness](../../catalog/readiness/v68-2026-11-25-r160-all202-gates.json)で全件`ready_to_acquire=false`。

## 4. 米国政策の一次資料と予測の分離

[米BIS 91 FR 74970、2026年11月19日発効 IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion Ruleで作られたモデル重量のECCN 4E091を**撤廃**した。一方、半導体、最終用途・仕向地、配布元ライセンス等の制約がすべて消えたという意味ではない。**今後一律のローカルモデル禁止が何月何日に起きるという根拠はない**。公開停止・Gated化・LICENSE変更は、定量確率を仮定しない保全ストレスシナリオとする。

## 5. H／T／D／C／Uと変数・単位

### 変数表

| 記号 | 意味（日本語） | 単位（SI/情報単位） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_W` | WeMM-Ecom0.8原本bytes | byte（B） | 1,733,044,450 | >0、publisher全20file | 整数スカラー |
| `B_M` | MiniCPM5 Final bytes | byte（B） | 5,043,807,977 | >0、publisher全11file | 整数スカラー |
| `B_I` | Ivonnet0.8原本＋readout bytes | byte（B） | 1,728,496,331 | >0、publisher全21file | 整数スカラー |
| `B_Σ` | 3repoの出版社論理原本合計 | byte（B） | `B_W+B_M+B_I` | owner占有ではない | 整数スカラー |
| `D_free` | 所有者実媒体の現在の空きbyte | byte（B） | null | 取得器の履歴値からは推定不可 | 非負整数／null |
| `D_floor` | 必須の最低空きbyte | byte（B） | 200,000,000,000 | stagingも含め全取得過程で維持 | 非負整数スカラー |
| `n` | 同条件性能反復数 | 1（無次元） | 課題群別の独立測定回数 | 将来>=30、今0 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 測定対象と同単位 | 誤差源の分散合成 | 実測なし未算定 | 非負実数又はnull |
| `k` | 包含係数 | 1（無次元） | 区間構成に用いる係数 | 統計モデル未設定 | 実数又はnull |

`B_Σ=1,733,044,450+5,043,807,977+1,728,496,331=8,505,348,758byte`（十進**8.505GB**）。**次元チェック**：byte+byte+byte=byte。VRAMピークやパラメータ数（個数）をこの出版社原本サイズと同一に扱う誤りはしない。

### H/T/D/C/U

- **H**：新3独立学習済みstateを「通常の量子化format追加」から除外して別々に保存すれば、既存の無検閲／小型／特殊能力とは異なるEC視覚・推論agent・文書decision機能を固定できる。品質が有意に増えるかは未実証。
- **T**：①3repo 52 files／Publisher SHA／同一重みではないことを照合。②元248件の行単位不変、現251資産／202 active／146条件付きと旧116取得報告との非重複、全202STOP、承認0を検査。③将来実機で各100以上の学習外課題、各30回以上の速度・メモリ反復を同一GPU/CPU clock・batch・input/context・backend/quant設定で計測する。Ivonnetは既存InternDecisionと同じ画像と文書を使い、非生成確率の校正誤差・棄権率と正答を測る。WeMMは商品属性・OCR・比較、MiniCPMはコードと道具呼出しを評価。
- **D**：immutable source一致／同一ID重複無し／全承認STOPなら**STATIC PASS**。品質差の95%CI下限>0と使用条件・owner SHA・完全offline復元・空き200GBを全て満たす場合のみ次段階を検討。本人権利や形式指定が不明な今は**DOWNLOAD UNCERTAIN→STOP**。自動許諾や未審査custom code実行は**FAIL**。
- **C**：WeMM EC作者データ偏りで一般化しない、MiniCPMの作者の複数指標集計が実機で反転する、Ivonnetの小型decisionが既存InternDecisionより劣る、外部LICENSEやreadout ABIに不適合がある。
- **U**：主な誤差はPublisher評価の代表性・訓練/テスト汚染、実HW clock/context、モデルコード、法務・親NOTICE、owner実ファイル欠損。反復実測がないので`u_c`と`k`は数値化不能。

**ERROR CHECK（静的）**：prev248全行を保護、3新IDを重複なしで追加。現251資産・202有効、SELECT56、CONDITIONAL146、R0 19／R1 141／R2 42／HOLD30／BACKLOG13／EXCLUDED6、モデル225・データ26。ソース3repo52file／8,505,348,758byte／LFS13、全202`ready_to_acquire=false`、approved queue空。取得重量0、owner現物SHA0、Gated回避0、未審査code実行0、削除0。

関連分野：**①小型マルチモーダルEC／視覚言語、②強化学習と小型LLM蒸留、③非生成分類と確率校正、④ソフトウェア供給網の暗号ハッシュ、⑤GPU実装・メモリ工学、⑥輸出管理とソフトウェア利用許諾**。

## 6.〈次に考える問い〉

**無検閲系のSmaug（約55.6GB）と、新規独立3系統（約8.5GB）について、法的アクセス・実機再現可能性・新規訓練成果の希少性を分けて得点化したとき、最初のOWNER実機SHA再確認に割くべき工数をどちらへ優先すべきか。**
