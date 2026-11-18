# R111 — v47原本ポートフォリオの確定範囲と新候補の重複回避（2026-11-18）

## 1.〈本論〉— 判定

**現行正本はv47（200登録・153有効、SELECT53／CONDITIONAL100）。今ここで新しい重みを登録しない。** 理由は最新候補の中核が既存v47に既に採用済みで、さらに増やせば同じタスクや同じ学習成果の二重化につながるため。**これは調査と選択の判断であり、153件の取得許可ではない。**

[機械可読のR111比較・14原本一覧](../../catalog/research/2026-11-18-r111-v47-continuity-small-model-and-uncensored-review.json)に、確認できた事実・競合候補・残課題・反証条件を保存した。既存CURRENT・正式選定・承認キューは変更しない。

- **重複で新規追加しない**：[`perplexity-ai/pplx-decider-flash-v1.3`](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3)はv47の184番目として**CONDITIONAL登録済み**。約4.5393Bの独自後学習チェックポイントで、同じ27B系列の大型版とは別の蒸留成果。非因果Attention・255行の特殊readout・Locate用独立adapterが必要で、通常の言語生成モデルへ単純変換して保存するものではない。既存の著者原本revisionは`d06fb3f2d97e0a52325a0d463c450cf0338f44fe`だが、固定ファイル一式の最終lock・本人行為別許諾・offline再現は未完了。
- **小型で既に保全対象**：[`kakaocorp/kanana-2-v-decide-3b-2611`](https://huggingface.co/kakaocorp/kanana-2-v-decide-3b-2611)、[`LiquidAI/d1-omni-600M`](https://huggingface.co/LiquidAI/d1-omni-600M)、[`pfnet/plamo-3-translate-0.8b`](https://huggingface.co/pfnet/plamo-3-translate-0.8b)、[`KittenML/kitten-tts-2-mini`](https://huggingface.co/KittenML/kitten-tts-2-mini)もv47に存在。これらを最新ニュースだけで重複登録しない。

### 新候補の実際の採否

| repo ID | 観測事実と区別点 | 判断 | 決定を変える証拠 |
|---|---|---|---|
| [`perplexity-ai/pplx-decider-v1.3`](https://huggingface.co/perplexity-ai/pplx-decider-v1.3) | Hugging Face表示約26.0853B、Apache-2.0メタデータ。公式開発報告ではQwen3.8-27Bから独立後学習した決定モデル。v1.3はTyped Decision/Locateを提供し、既存4B Flashと同族。 | **HOLD・新規採用しない**。大型という理由より、FlashとKananaに対する作業別性能差と追加容量の正当化が不足。 | 必須readout・Locate adapterを含む固定ファイル一式、法的条件、同一HW・同じバッチ/入力でFlashより明確な精度増分（事前に定めた測度・閾値）。 |
| [`ConwayResearch/Underdog-Woof`](https://huggingface.co/ConwayResearch/Underdog-Woof) | 作者公表は音声22.95M+decoder15.3M=約38.24M、二話者の**英語限定**24kHz CPU TTS。約40.6MBのモデル・単一CPUスレッド13.8倍実時間・402MB RSSは作者実測主張。Hubタグは`other`、本文では独自非商用ライセンス・訓練用途制限を掲げる。 | **HOLD・新規採用しない**。既存Kittenは日本語含む多言語TTS原本。極小サイズだけでは取替不可。 | 原本revisionとMimi由来decoder/NOTICEの権利、ライセンス正文、Kitten同一CPU・clock・backend・batch条件の30件以上の品質/速度/ピークRAM比較。 |

Perplexityの[2026-11-12公式技術報告](https://www.perplexity.ai/hub/blog/perplexity-decider)は分類/抽出/マルチモーダル判断の作者評価を提示するが、全値は**利用者実機での独立再測定ではない**。大型版をFlashへ単純に量子化したものと誤認することも、Flashの成績を大型版に移すことも禁じる。Woofの性能主張もKittenと同条件の独立比較ではない。

## 2. 既に取得対象ファイルを選択した14原本

[現在のpublisher source候補キュー](../../queues/proposed-v47-r110-source-pinned-14.json)には以下の14原本、**173論理ファイル、211,999,468,264 byte** が計上される。この値は発行者側で観測・選定したソースの合計で、実HDDへ既に保存された容量ではない。複数の同一学習済み重みをQ4/Q5/Q6/Q8やONNX等で別資産として重複させない。

| 順 | repo ID | 調査レーン | 原本候補ファイル数 | Publisher source bytes | アクセス |
|---:|---|---|---:|---:|---|
| 1 | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | A:独立派生・特殊LoRA | 5 | 17.738 GB | Public表示（権利別） |
| 2 | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | A:独立派生・特殊LoRA | 4 | 17.177 GB | Public表示（権利別） |
| 3 | [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | A:独立派生・特殊LoRA | 8 | 0.671 GB | Public表示（権利別） |
| 4 | [`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | B:小型専門/原本 | 5 | 0.006 GB | Public表示（権利別） |
| 5 | [`usezn/Galvanize-3`](https://huggingface.co/usezn/Galvanize-3) | B:小型専門/原本 | 9 | 0.597 GB | Public表示（権利別） |
| 6 | [`qvac/BotPsy-0.8B`](https://huggingface.co/qvac/BotPsy-0.8B) | B:小型専門/原本 | 11 | 1.726 GB | Public表示（権利別） |
| 7 | [`nvidia/Nemotron-3-Diarization`](https://huggingface.co/nvidia/Nemotron-3-Diarization) | B:小型専門/原本 | 11 | 0.397 GB | Public表示（権利別） |
| 8 | [`robbyant/lingbot-touch-tiny`](https://huggingface.co/robbyant/lingbot-touch-tiny) | B:小型専門/原本 | 5 | 0.022 GB | Public表示（権利別） |
| 9 | [`tencent/Qwen3.8-27B-DSpine-b16`](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | B:小型専門/原本 | 5 | 4.052 GB | Public表示（権利別） |
| 10 | [`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2) | C:大型・権利先行 | 12 | 53.122 GB | Public表示（権利別） |
| 11 | [`DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU`](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | C:大型・権利先行 | 25 | 55.590 GB | Public表示（権利別） |
| 12 | [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | C:大型・権利先行 | 31 | 55.586 GB | Gated（個別許可未検証） |
| 13 | [`osunlp/ARLoop-1.2B`](https://huggingface.co/osunlp/ARLoop-1.2B) | D:追加小型原本 | 15 | 4.838 GB | Public表示（権利別） |
| 14 | [`KittenML/kitten-tts-2-mini`](https://huggingface.co/KittenML/kitten-tts-2-mini) | D:追加小型原本 | 27 | 0.478 GB | Public表示（権利別） |

**重み・学習済み全構成の最終化は未完了。** データ型変換の重複排除と、別のSFT/RL/拒否制御編集に由来する独立学習済み重みの保存を区別する。例えば0bserverx RVNとInterpreticの政治的制御編集は独立の研究対象で、モデル名の類似だけで削除しない。一方、RVN自身のQ4/Q5/Q6/Q8バリエーションを無条件で全取得しない。

上記には約55.59GBのDavidAU原本とGatedのOrcaRouter原本を含む。**固定Publisher URLが存在することと個人の適法取得資格があることは別。** この14件のsource-only集合を一括承認するのではなく、原本ごとのLICENSE・許諾・親依存・前処理・ファイルハッシュを先に確定する。

## 3. 段階的な確定計画と停止条件

**第一段階（取得指定ファイルの選定）**：14件について原本の学習済み構成、必要decoder/adapterとモデル本体を分離し、各ファイルについて完全40桁revision、path、byte、公開されている完全SHA-256を参照表に固定する。同一物理SHAで複数論理パスを復元する場合はパス意味を保持する。メタデータ検証はモデルロード・コード実行を行わない。

**第二段階（法的資格）**：個人のGated許可、モデルLICENSE正文、ベース/LoRA/decoderの依存条件、個人が行う保存・内部解析・将来の利用行為への許諾を分ける。2026年11月時点のモデル公開条件の変化は一次情報で監視するが、特定モデルの削除や法的禁止確率を捏造しない。

**第三段階（本人のHDD・復元）**：実際の4TB対象HDDの物理識別、フォーマット後容量、現在の空き、cache/staging使用ピーク、200GB安全残床を測る。メーカー容量4TBは実測ではない。CPU/GPU・VRAM・OS・driver・PyTorch/Transformers/ONNXRuntime/llama.cppのversion・ABI・quantization scheme/zero-point・KV/cache・context・batchを固定。モデルファイルを取得してもcustom codeは自動実行しない。

**第四段階（最終承認）**：モデル一式のexact lock、総容量、権利と復元試験内容、原本差異を提示したうえで利用者が**個別の固定manifestを承認して初めて**取得キューへ移す。現状`queues/approved.json`は0件、152件でも14件でも自動実行不可。高リスク予測、無検閲、量子化、MoEの活性パラメータ数によって例外取得を正当化しない。現行`policies/limits.json`の**150B baseline + 厳密実測を要する量子化例外**を適用し、完全総数不明ならlock停止。

## 4. H / T / D / C / U とERROR CHECK

**H**：既存v47の独自原本を正しく完成させる方が、重複し得る大型Deciderや英語限定TTSを今直ちに追加するより、保存上の独自能力/適法な増分byteが大きい。

**T**：v47の200 IDと153有効、原本選択14 IDを完全照合。候補についてHub一次ページを確認し、独自学習成果・原本の公開状態・契約・一式の欠落を検査。最終比較には同一HW/clock/backend/context/batch、各タスク30試行以上、性能中央値と誤差範囲、事前定義した合格閾値を要求。今回実機試験なし。

**D**：PASS＝既採用候補を二重登録せず、新候補2件をHOLD研究に残し、全153の取得STOPを維持。FAIL＝未確認重みの取得承認、権利回避、source値を所有者の実HDD測定値と扱う。UNCERTAIN＝性能、外部依存の完全復元、実機空き、本人Gated許可。

**C**：Woofが非商用研究で許容されるうえ同一CPUでKittenより相当に高品質・低負荷となる、または大型DeciderがFlashより大幅な独自仕事を生む場合、両モデルの採否を再審査する。

**U**：作者ベンチマーク、ハードウェアクロックとbatch差、真の学習済み部品総数、モデルカードとLICENSE正文の不一致、パラメータとファイルbyteの混同が主な不確かさ。独立観測系列と誤差相関がないので合成標準不確かさ`u_c`と包含係数`k`は算出不可。

### 変数表・単位検査

| 記号 | 日本語の意味 | 単位（SI） | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| `N` | 発行者sourceで選択した論理ファイル数 | 1 | 14原本から173件。重複論理パスを含みうる | 非負整数スカラー |
| `B_s` | Publisher側で選択したソース総量 | byte（情報量、SI単位ではない） | 211,999,468,264。キャッシュ・外部依存を含まない | 非負整数スカラー |
| `B_h` | 本人HDDの実空き | byte | 未実測。200,000,000,000以上の安全残床要求 | 非負整数/未確認 |
| `P_t` | モデル全学習済みパラメータ数 | 1（無次元） | MoE全expert・補助学習済み構成含む。未確定ならlock停止 | 非負整数/未確認 |

**次元チェック**：ファイル数`N`とパラメータ数`P_t`は無次元、`B_s`と`B_h`はbyte。重みのbit化で`P_t`は減らない。Publisher sourceのbyteと実HDD空きのbyteは同次元でも、実測前に大小比較して実行可能と判断できない。

**ERROR CHECK**：v47 200登録/153有効、SELECT53/CONDITIONAL100、14原本/173選択sourceファイル/211,999,468,264byte、現存Flash・Kanana・PLaMo・Kitten・Liquid d1を二重登録せず、候補2件HOLD、正式選定追加0・削除0・取得承認0。**Exaの検索4回はHTTP402で結果なし**。Hugging Faceの公開メタデータ及び一次ページを使ったが、取得ファイルSHAのローカル再計算や完全offline復元・本人HDD検査は未実施。

**次に考える問い**：同じ保存予算で、別の独立学習済み能力を追加するのと、既存14原本を安全に完全復元可能な状態へ仕上げるのとでは、どちらが一つの障害解消あたりの価値を増やすか。
