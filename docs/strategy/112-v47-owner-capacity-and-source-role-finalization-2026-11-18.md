# R112｜v47・保存原本14件の取得順とHDD容量停止条件の確定

2026-11-18 JST／`Unjuno/local-model-portfolio`・専用ブランチ `strategy/2026-11-03-01-risk`。**正本mainはv47（200登録／153有効）**。今回の成果は [14原本・173ファイル・Publisher SHA72件の機械可読判定](../../catalog/decisions/2026-11-18-r112-v47-source-role-and-owner-capacity-gates.json)。**モデル重み取得・本人Gated承認・モデルコード実行・選定変更はいずれも0**。旧R109の6件案ではなく、v47の最新14原本を基準とする。

## 1.〈本論〉— 保存する原本をどう確定したか

目的は、希少な独立訓練済み重み（無検閲編集、専門小型モデル、音声、触覚、画像LoRA）を、適法に再取得・オフライン復元できる状態にすること。単なる量子化形式の追加や規制されるという憶測を選定の根拠にしない。

- **最初の1件**：`ibm-granite/granite-timeseries-ttm-r3` を取得・復元手順の検証候補に確定。小型原本なので出版社SHA・権利・オフライン環境検証の失敗原因を切り分けられる。
- **小型原本6件**：Galvanize／BotPsy／Nemotron Diarization／LingBot Touch／ARLoop／Kittenを保全候補に維持。ただし`.pt`やカスタムコードを無審査で実行しない。
- **無検閲2件**：0bserverx RVN Q4とInterpretic Q4は異なる編集成果として現行選定を維持。同一27Bの多数の通常量子化を重複保存しない。OrcaRouter BF16はGated本人許諾確認を先行。
- **親依存1件**：Qwen3.8 DSpineは単体4GBで成立するモデルではなく、親Qwen 27B原本と対応backendの閉包が必要。
- **権利制限1件**：ChatR Labs画像LoRAは親Qwen-Imageと非商用研究の契約を別審査。大型PantheonとDavidAUは容量と独立品質の証拠が不足し、初期転送は延期する（正式除外ではない）。

### 保存上の誤りを訂正

[BotPsy-0.8B](https://huggingface.co/qvac/BotPsy-0.8B)は**ツール利用に後学習された小型エージェント**であり、セキュリティ分類器ではない。[Galvanize-3](https://huggingface.co/usezn/Galvanize-3)は**プロンプト注入とjailbreakの専用分類器**。過去R109のBotPsy「行動リスク判定モデル」という説明は誤りであり、今回の機械可読原本台帳に訂正を記録した。

## 2. 全14モデルの必要ファイル容量と試算

「最低空き」は**取得する全ファイルの出版社容量＋最大単一ファイル1個分のステージ領域＋200GB空き床**の仮定下での値。追加の学習済み外部部品／キャッシュ／ランタイムを未計上であり、実際の取得可能性の十分条件ではない。GBは十進。

| 研究帯 | 不変Publisher原本 | 候補source (GB) | 条件付き最低空き (GB) | 第一停止ゲート |
|---|---|---:|---:|---|
| 最小復元試験 | [`ibm-granite/granite-timeseries-ttm-r3`](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/tree/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa) | 0.006 | 200.011 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 小型独自成果 | [`robbyant/lingbot-touch-tiny`](https://huggingface.co/robbyant/lingbot-touch-tiny/tree/f23969ccd4b6bba2163e69cc05a577455a075fe9) | 0.022 | 200.044 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 小型独自成果 | [`nvidia/Nemotron-3-Diarization`](https://huggingface.co/nvidia/Nemotron-3-Diarization/tree/52a432672732425e4c19765b9fec9b5810e6f4ba) | 0.397 | 200.794 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 小型独自成果 | [`KittenML/kitten-tts-2-mini`](https://huggingface.co/KittenML/kitten-tts-2-mini/tree/c01797caec3967b400da457656e011eb81f530a4) | 0.478 | 200.805 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 小型独自成果 | [`usezn/Galvanize-3`](https://huggingface.co/usezn/Galvanize-3/tree/597237be3b0fabbf5d70ff16ce95fad14a591f20) | 0.597 | 201.160 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 小型独自成果 | [`qvac/BotPsy-0.8B`](https://huggingface.co/qvac/BotPsy-0.8B/tree/24561e9681643eaf807fc28b0875210cb17f89c1) | 1.726 | 203.432 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 小型独自成果 | [`osunlp/ARLoop-1.2B`](https://huggingface.co/osunlp/ARLoop-1.2B/tree/a29f310ac46646edf5c462425dc546b2ce7ea985) | 4.838 | 206.822 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 無検閲・品質比較 | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/tree/ab8d7bd81d03117501e4da60cccdff4c80f0eea0) | 17.177 | 233.724 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 無検閲・品質比較 | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF/tree/e6924b3a08765341e01546308ccf2683d43e880b) | 17.738 | 234.549 | OWNER_HDD_ACTUAL_CAPACITY_AND_STAGING |
| 親依存 | [`tencent/Qwen3.8-27B-DSpine-b16`](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/tree/260a6c23070ca873ff1a5f33b7119ac3f6a245ee) | 4.052 | 208.104 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 非商用親LICENSE | [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/tree/aa213272180d6ad0d03f5fb3d597f0f0322647c5) | 0.671 | 201.342 | OWNER_HDD_ACTUAL_CAPACITY_AND_STAGING |
| 大型後学習・延期 | [`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2/tree/6af1278a92223c717ccea671e4571a5cc135f5d8) | 53.122 | 302.293 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| 大型後学習・延期 | [`DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU`](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU/tree/079b2b268c637b77f2fb4ab6a5ca1edc47d462a5) | 55.590 | 260.555 | SINGLE_IMMUTABLE_SOURCE_FILE_SET |
| Gated権限先行 | [`orcarouter/Qwen3.8-27B-Uncensored`](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored/tree/0f639a9bde23fe229a7b064b40a5153c5bec0b48) | 55.586 | 259.575 | OWNER_SPECIFIC_GATED_ENTITLEMENT |

*SHA監査*：14モデル・173論理ファイルのうちPublisher SHA-256記録は**72件**。同一SHA-256の重複は**0件**。SHAのないファイル、別量子化形式、モデル能力が異なるかどうかまで証明したわけではない。

## 3. 最小取得試験の具体的な判定

**Phase 0** は [TTM R3の固定revision](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3/tree/ea17cfd2e3edcaea21eb8dcecd18bf88971482fa) のsource **5,748,963 byte**、最大単一ファイル **5,729,424 byte**。仮定した必要空きは **200,011,478,387 byte**。

**Phase 1** は TTM R3／Galvanize-3／Kitten TTS Mini。source **1,080,686,877 byte**、最大単一ファイル **562,583,392 byte**、条件付き最低空き **201,643,270,269 byte**。KittenのFP32原本とINT8 ONNX、16言語voice packsは同じモデルの異なる保存形態・必要依存であり、2モデルとして数えない。

既存R109では接続されたLinux filesystem容量**50,884,108,288 byte**、空き **29,520,904,192 byte**を観測。**ユーザーの別の4TB HDDを測った結果ではない**。そのLinuxでは最低200GB床が満たせず、Phase 0でも容量FAIL。ユーザーの4TBディスクの実空きは未測定であるため、**現在の取得可能性はUNCERTAIN、取得承認は0**。

モデル取得前に、既存の[読取専用事前検証ツール](../../scripts/verify_v46_download_preflight.py)と正式な`policies/limits.json`を照合する。権利正文・本人Gated・ライセンス適用行為・学習済み依存・完全SHA・loader/ABIと復元条件は独立の強制停止条件である。

## 4. 新規候補を無条件に採用しない理由

[9B Heretic](https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic) はQwen3.5由来の別編集だが親JackrongとのHugging Face表示パラメータ数に差があり、Vision/MTP含む全保存範囲と通常性能を未検証。**研究HOLD**。

[tiny-voca](https://huggingface.co/n4ze3m/tiny-voca)は英語2声・極小4.537M原本だが、既存Phonon/Kittenと重なる。作者の速さの数字は使用HWやbatchを統一した独立実測ではないため、今回の正式追加は延期。[Underdog Woof Japanese](https://huggingface.co/ConwayResearch/Underdog-Woof-Japanese)は英語版と異なる日本語独自性があるが、独自非商用と音声学習制限の版ごとの適用を確認するまでHOLD。

**規制事実と仮説**：個別Gatedや著作権・派生ライセンスは観測事実。他方「まず無検閲、次に高性能、最後に全open-weightが禁止される」は反証可能なシナリオであり、禁止予定日・確率は設定できない。参考：[Hugging Face Gated公式文書](https://huggingface.co/docs/hub/models-gated)、[EU AI Act第53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)。今回のExaは402利用枠超過で新たな検索根拠を得られなかった。

## 5. 変数表・次元チェック

| 記号 | 意味（日本語） | 単位（SI） | 定義・条件 | 定義域・範囲 | 型 |
|---|---|---|---|---|---|
| `B_s` | 固定した選択source容量 | byte | 各選択ファイル容量の和 | 0以上の整数 | スカラー |
| `B_m` | 最大単一ファイル | byte | 一時領域を1最大ファイル分使用する仮定 | 0以上の整数 | スカラー |
| `B_f` | 保存後最低空き | byte | 200,000,000,000 | 固定 | スカラー |
| `F_req` | 仮定下の取得前必要空き | byte | `B_s+B_m+B_f` | 0以上 | スカラー |
| `F_linux` | 過去の接続Linux実空き | byte | 29,520,904,192（ユーザー4TBとは異なる） | 観測時のみ | スカラー |
| `N_total` | モデル総学習済みパラメータ | 無次元（1） | MoE全expertと補助学習済み要素を含む、未知ならnull | 0以上／null | 整数スカラー |

Phase 0の`F_req`は **5,748,963 + 5,729,424 + 200,000,000,000 = 200,011,478,387 byte**、Phase 1は **1,080,686,877 + 562,583,392 + 200,000,000,000 = 201,643,270,269 byte**。**次元チェックPASS**：加算項はbyteで統一。`N_total`をファイルbyteへ直接流用しない。現行150B通常境界と厳格な量子化例外は正式`limits.json`を尊重する。

## 6.〈応用・転用例〉・H/T/D/C/U

- **保存情報学**：固定Git/LFS SHA、重複排除、復元パス整合。
- **機械学習・音声／ロボット**：時系列・触覚・TTS・ツール使用SFTの独立した訓練成果を保全。
- **ソフトウェア供給網**：pickle/remote code、wheelhouse、OS/ドライバ/量子化ABIと完全復元。
- **情報法・AI配布政策**：モデル別Gated、非商用利用、親ライセンスと配布規制の区分。

**H**：最小TTM原本の合法な復元を確認してから大型27Bへ進める方が、取得の失敗原因を切り分けやすい。**T**：14固定source・173ファイル・72ハッシュ全件比較（n_min=14）後、ユーザーの4TB HDDを指定して実空きとcache/stagingを読取専用検査。権利やSHAの不一致時には逐次停止。**D**：静的原本・ハッシュ照合PASS、既存Linuxの容量FAIL、ユーザーHDDと取得適格性UNCERTAIN。**C**：外部Codec、LICENSEやGated権限、古いPublisher情報、モデル互換性が計画を破る可能性。**U**：HDD測定時刻、モデル作者メタデータ、権利・ランタイムが主な系統不確かさ。誤差標本がなく`u_c`と`k`は数値化できない。

### ERROR CHECK

- **200登録・153有効**を正式正本のまま維持。
- **14原本・173ファイル・72個の上流SHA-256（重複0）・source合計211,999,468,264 byte**を機械検算。
- 取得承認0。ユーザーHDDと依存・localSHA/復元・性能評価は未実施。
- 専用ブランチに判断と容量ゲートの資料のみ追加。`main`と`queues/approved.json`は変更しない。

## 7.〈次に考える問い〉

**最初の5.75MB時系列原本を本当に再現できる状態にする際、モデル重みのSHAだけでなく、どのLICENSE・Python/torch/ABI・訓練済み依存を必ず一緒に固定するべきか。**
