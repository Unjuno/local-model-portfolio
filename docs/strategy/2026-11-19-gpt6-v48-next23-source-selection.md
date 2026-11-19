# v48・未収載23モデルの保存原本確定：取得履歴の重複排除と次段階

**実施日：2026-11-19。対象：Unjuno/local-model-portfolio。提案は専用ブランチ上のみ。** 現行正本は`catalog/CURRENT.json` → v48で、201登録／154有効。前回のv9（132資産）や旧S1→S2→S3の仮説順位へ巻き戻さない。

[全件JSON決定表](../../catalog/decisions/2026-11-19-gpt6-v48-next23-source-selection.json) に23件すべての固定配布元revision（発見台帳の情報）、選択ファイル件数・容量、モデル総パラメータ、根拠、保留条件を記録した。**本書は研究上の「保存すべき原本」順位の確定であり、取得承認・実行・既存ファイル削除は行わない。**

## 1. 取得済み報告との再突合

2026-11-19の[取得履歴JSON](../../catalog/execution/2026-11-19-acquisition-ledger.json)では、**53件VERIFIED報告、1件Gated HOLD、579ファイル／270,835,576,267 byte**。この報告をWindows Dドライブで今回独立再ハッシュしたわけではないため、現物同定の成功と誤記しない。

[次候補59件](../../catalog/execution/2026-11-19-discovered-next-waves.json)から、取得報告のrepo IDと一致した36件を**再ダウンロード対象から除外して調査**する。残り23件・publisher候補source 1,386,933,535,900 byte。2026-11-19の古いR116で「59候補の残り54」と記された状態は、取得報告更新により古くなった。

| 判断 | 件数 | publisher選択source合計（十進） | 状態 |
| --- | ---: | ---: | --- |
| 新規発見候補 | 59 | 1,496,201,864,921 byte | 出典ファイル・revisionの研究台帳 |
| 取得報告と重複 | 36 | 109,268,329,021 byte | 既存ファイルの所在・ハッシュを最初に再照合 |
| 取得報告に未収載 | 23 | 1,386,933,535,900 byte | **未取得と断定せず**現物照合 |
| A1：最初に原本sourceを閉じる | 5 | 122,687,559,858 byte | 次の監査最優先。承認なし |
| A2：独自能力の次群 | 5 | 368,396,117,962 byte | 専門原本を確保する候補。承認なし |
| B：比較・延期 | 13 | 895,849,858,080 byte | 重複・容量・品質比較待ち |

**判断**：有効ポートフォリオの外にむやみに新しい量子化を増やさず、現在の201資産の独立学習済み原本を優先する。保存枠4TB・物理残床200GBの条件を満たすことを実機で再検証するまでは、これらの数字を実際の残容量や転送量とみなさない。

## 2. 未収載23件の個別選定

- **A1（5件）**：RWKV7の再帰構造、iLLaDAの非自己回帰拡散言語、TRELLIS.2の編集可能な3D、ACE-Stepの音楽生成、Qwen3.8公式原本（既存無検閲派生の比較対照）。いずれも名称・一般Q4コピーでは代替できない独立学習済み状態の保全を優先する。
- **A2（5件）**：Carbon-XのDNA専門学習、FaraのGUI行動方策、Hy-Memoryの記憶更新MoE、MeditronFOの医学SFT、Qwen3-Coder-Nextのコードエージェント事後学習。高性能だから規制されると断定して順位を決めていない。
- **B（13件）**：一般Base重複、音声TTSの多重保管、画像・医療派生の差分未測定、大型119B/120B原本の容量負荷を理由として**取得調査の後順位**とする。現行SELECTの正式削除・降格を意味しない。

| repo ID（配布元一次URL） | 分類 | 選択source GB | 総パラメータ B | 表示licenseタグ | 独自性・次の反証条件 |
| --- | --- | ---: | ---: | --- | --- |
| [RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | A1 | 14.402 | 7.200 | apache-2.0 | 再帰型RWKV7原本。保存済みARLoopと構造比較 |
| [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | A1 | 16.237 | 4.000 | mit | 編集可能3Dメッシュと材質。保存済みIdolの3DGSと非同一 |
| [GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | A1 | 16.513 | 8.251 | apache-2.0 | 拡散言語モデルの事前学習原本。custom code監査要 |
| [ACE-Step/acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | A1 | 19.949 | 4.987 | mit_publisher_tag_and_code_mit | 楽曲・歌声生成の独立重み。音声Codec/権利を要照合 |
| [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | A1 | 55.586 | 27.781 | apache-2.0 | 無検閲Interpretic/RVN派生と比較する公式親原本 |
| [HuggingFaceBio/Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | A2 | 29.656 | 14.822 | apache-2.0 | DNAと言語の専門学習。構造系モデルの代替ではない |
| [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | A2 | 54.744 | 27.357 | mit | GUI行動方策の専用後学習。操作コードは別審査 |
| [tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | A2 | 60.143 | 30.065 | apache-2.0 | 長期記憶更新に特化したMoE学習済み状態 |
| [EPFLiGHT/OLMo-2-32B-MeditronFO](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | A2 | 64.477 | 32.234 | apache-2.0 | 臨床言語SFT独立原本。実臨床使用の認可ではない |
| [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | A2 | 159.376 | 79.674 | apache-2.0 | 約80B総数のコードエージェント専用学習成果 |
| [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) | B | 10.681 | 0.500 | mit | 既取得のZONOS/Qwen/KittenとTTS比較後に具体版を選ぶ |
| [OpenMOSS-Team/MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | B | 16.996 | 8.490 | apache-2.0 | 日本語長文韻律の差分を同条件試験で確認 |
| [PrentisAI/GroundGUI-8B](https://huggingface.co/PrentisAI/GroundGUI-8B) | B | 17.550 | 8.767 | apache-2.0 | Faraとは異なる画面座標特化。定位精度差を検証 |
| [kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers) | B | 26.671 | 3.178 | mit | 音声同期動画の差分と依存Codec、容量を監査 |
| [meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | B | 59.582 | 29.777 | apache-2.0 | 独立マルチモーダルだが大型。重複と性能差を比較 |
| [ibm-granite/granite-switch-4.1-30b](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | B | 59.991 | 29.990 | apache-2.0 | aLoRA/Guardian/音声Encoderの全学習済み依存を確認 |
| [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) | B | 62.579 | 31.273 | apache-2.0 | 別系統の一般Base。実需要と容量対効果を比較 |
| [allenai/Olmo-3-1125-32B](https://huggingface.co/allenai/Olmo-3-1125-32B) | B | 64.477 | 32.233 | apache-2.0 | 公開訓練過程の再現価値と保存容量を比較 |
| [Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | B | 66.257 | 33.119 | apache-2.0 | コード・エージェント系でQwen Coderとの差分を比較 |
| [OctoMed/OctoMed-32B](https://huggingface.co/OctoMed/OctoMed-32B) | B | 66.726 | 33.357 | apache-2.0 | Meditronと別の画像・臨床タスクで重複評価 |
| [Qwen/Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | B | 71.927 | 35.952 | apache-2.0 | MoE事前学習Base、Qwen3.8比較原本との役割整理 |
| [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | B | 130.526 | 116.829 | apache-2.0 | MXFP4 MoE独自形式。130GBと別配布経路の比較 |
| [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | B | 241.887 | 119.401 | apache-2.0 | 242GB級。独立性能・有用性が実証されるまで延期 |

B群でも、既存にない学習済み構造・公開停止の具体的予告・実用上の性能差が一次資料または対照試験で示された場合は、A2より前に再選定する。サイズが大きいという理由**だけ**では削除しない。逆にA群でモデル親、Codec、encoder、権利を完全に閉じられなければ取得を進めない。

## 3. 新たに浮上した4モデルの結論

| モデル | 2026-11-19の一次資料・事実 | 研究上の判断 |
| --- | --- | --- |
| [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 2026-11-18公開、Hub約508.6M、Apache-2.0表示。配布者の[Open ASR報告](https://huggingface.co/blog/rumble-2-flash)はH200/vLLMで英語WER6.60%、多言語平均6.96%、フルバッチ>7000RTFxを報告 | **CONDITIONAL採用提案**。auxiliary CTC headの学習済み総数、固定ファイル全SHA、日本語実測・権利が未完了のためダウンロード準備は停止 |
| [sensenova/SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B) | 元SafetensorsはGated、Hub約9.413B。一方、同じ出版社の[GGUF](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF)は公開表示、Previewは約9.656Bと規模も異なる | **元Safetensorsは権限確認HOLD**。GGUFは別の正規公開sourceとして同一性・mmproj・licenseを比較し、Gatedへの無許可アクセス経路とみなさない |
| [nvidia/Nemotron-Labs-Sigma-distill-spec-3B](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B) | Hub約4.237B・license tag`other`・custom codeを含む | **HOLD／ライセンス正文とcustom code静的検査**。iLLaDAと別の推論機構だが比較品質は未実証 |
| `Empero/Quark-150M-128K-Zero` | 二次情報に掲載されるが、正確なHub repo IDの照合では未発見 | **取得対象外**。出版社の正確なURL・コミット・学習済み原本を一次確認するまで追加しない |

※これらは既存23件の外側。現行201件の登録数は変更せず、Rumbleの正式追加・取得承認を先取りしない。

## 4. 無検閲モデルの原本・交換方針

[R115原本保存案](../../queues/proposed-v48-r115-master-sources-16.json)を引き継ぐ。**InterpreticAI/Qwen3.8-27B-Uncensored-v2はBF16の配布者学習済み原本**、**0bserverx RVNは確認できる最も上流に近い公開RVN-F16.gguf**を高精度マスターとする。後者のsafetensors 13シャードはF16 GGUFを変換した二次物であり、pre-GGUFの学習時オリジナルBF16とは認定しない。

過去のQ4 VERIFIED記録は実行用比較コピーとして残し、無断削除・過剰なQ4/Q5/Q6/Q8追加を行わない。OrcaRouterのGated原本を権利未確認のまま取得せず、無検閲のラベルだけで性能や安全性を断定しない。別学習成果であっても現行の要件を満たさない派生は比較待ちへ移す。

## 5. 現在の法制度と取得停止ゲート

一次法令：BIS [2026-11-19掲載予定の暫定最終規則](https://public-inspection.federalregister.gov/2026-23529.pdf)（2026-23529）。2025年AI Diffusion Ruleからのモデル重み輸出管理`ECCN 4E091`の撤廃と、先端半導体・遠隔計算資源・提供先/用途への規律を明確に区別する。**公開重み全般が現に禁止されるという根拠にはならない**。配布停止・Gated・license変更・private dataの権利は異なるリスクである。Exaは**HTTP402（credits exhausted）**のため今回検索できなかった。政府公文書と一次Hub・配布者カードで代替し、Exa取得済みと虚偽記録しない。

現在の`policies/limits.json`は総パラメータ150B以上の量子化例外を**同一実機条件・各30回以上・ピーク512GB未満・厳密な比較メモリ証拠**がある場合だけ個別審査する。今回の23候補の総学習済みモデル数はすべて150B未満なので例外は使っていない。MoE活性数を総数に置換せず、総数不明はlock停止。

各資産の必須STOPは、完全利用許諾（親とデータを含む）、本人Gated権限、immutable revision＋必要全ファイルSHA256、外部学習済みEncoder/Codec、ローカルハッシュ、Dドライブの正確なボリュームと残床200GB＋cache/staging、OS/backend/ABI/量子化zero-point/KV/context/batch、明示的な承認manifest。**研究上のGOはダウンロードの許可ではない。**

### 変数表（単位・条件・型）

| 記号 | 意味 | SI単位 | 定義 | 定義域・範囲・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `N` | 次候補数 | 1（無次元） | 台帳に列挙された件数 | 今回59 | 整数スカラー |
| `V` | 過去報告と重複する件数 | 1（無次元） | 対象repo IDの交差 | 今回36、現物再ハッシュ前 | 整数スカラー |
| `U` | 重複報告のない件数 | 1（無次元） | `N−V` | 今回23 | 整数スカラー |
| `b_i` | repoごとに提示された選択source | byte（8bit） | 選択候補ファイル合計 | 非負整数、依存・最終承認で変わる | 整数スカラー |
| `p_i` | 学習済み総パラメータ | 1（無次元） | MoE全expertなどを含む | 今回の23件は150B未満 | 整数スカラー |
| `f` | 保存後の物理的空き容量 | byte（8bit） | 本人HDDでの実測 | 2×10¹¹byte以上必須、今回未再確認 | 整数スカラー |
| `a_i` | 本体取得承認 | 1（無次元） | 固定manifestに対する明示承認 | 現時点でfalse | 真偽値 |

**単位チェック**：59=36+23はすべて件数であり次元一致。A1とA2の各source合計を合わせると491,083,677,820byte。バイト数とパラメータ総数を直接比較せず、元の学習済みパラメータ数を量子化で減ったと判定しない。

## 6. H / T / D / C / U — 次の最小検証

- **H**：同一学習成果の量子化を増やすより、A1の5異系統原本を固定した方が同容量当たりの独自な再現能力が増す。これは研究仮説であり測定済み効用ではない。
- **T**：次候補59行の全照合（`n_min=59`）。A1はsource SHAと全学習済み部品の完全閉包、著作権、所有Dの容量確認。runtime・品質は同一ハードウェア、クロック、batch、context、backendと量子化条件で最低30課題ずつ比較。不一致や権利不明ではその資産を停止。
- **D**：**PASS_METADATA**＝59=36+23、23=10+13、モデル150B未満、無許可取得0。**PASS_DOWNLOAD**はなし。**UNCERTAIN**＝現物の所在・権利・依存・実運用性能・将来規制。**FAIL**＝総数不明のlock、Gated回避、SHA不一致、残床200GB割れ、未承認取得。
- **C**：B群が同条件評価で代替不能な能力を示す、A1の外部モデル依存が保全不能、報告済み53件が別ボリュームに存在・欠損、出版社の原本が変更された場合、順位を再度変更。
- **U**：取得履歴は本人HDDの独立照合ではなく、source候補はオフライン一式でない。規制発生確率と測定分散がないため、合成標準不確かさ`u_c`と包含係数`k`は未算定。

**学際的転用**：アーカイブ工学（原本同一性・重複排除）、機械学習（独立学習済み構造と再現性）、ソフトウェア供給網（依存・固定版・ABI）、情報法（配布・データ権利・Gated）を一つのsource lock設計で接続する。

### ERROR CHECK

上記判断の機械可読JSONは23件一意、A1=5・A2=5・B=13。A群491,083,677,820byte、B群895,849,858,080byte、合計1,386,933,535,900byte。既存`CURRENT.json`の201/154および`queues/approved.json`の0件は不変。モデル本体の新規取得、サードパーティコード実行、既存ファイルの削除は行っていない。

## 7.〈次に考える問い〉

**A1の5資産について、出版社SHA・元重み全ファイル・依存の権利・Dドライブの実測を同時に満たす最初の1件はどれか。** この条件を満たしたものだけを正式なダウンロード承認対象に進める。
