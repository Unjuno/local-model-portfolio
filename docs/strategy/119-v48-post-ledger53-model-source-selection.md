# R119｜取得報告済み53件を除外した非重複モデル原本の確定調査

調査日：2026-11-19。正本：[CURRENT v48](../../catalog/CURRENT.json)（201登録・154有効）。[機械可読の全23件判断](../../catalog/decisions/2026-11-19-r119-post-ledger53-source-selection.json)。**今回、モデル本体の取得・Gated認証申請・実行・既存ファイル削除・承認キューの変更は行っていない。**

## 1.〈本論〉まず最新の取得報告との二重計上を解消

[2026-11-19の最新取得実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は **53モデル・579ファイル・270,835,576,267 byte（270.836GB）VERIFIEDと報告**する。別に1件がGated HOLD。これは実行台帳の報告で、今回ユーザーの現物4TB HDDを独立再マウントし全ファイルをSHA-256再検査した証明ではない。

[旧59件の次波探索](../../catalog/execution/2026-11-19-discovered-next-waves.json)について最新ledgerのrepo IDと結合し、**36件はすでに取得済みと報告され、まだ報告に現れない候補は23件**と判明した。従って古い「次54件」をそのまま再実行するのは誤り。23件の出版社source観測合計は **1,386,933,535,900 byte（1.387TB）**。これは実際にDドライブへ追加で必要な空き量でも、全てが合法かつ再現可能な重み構成でもない。

## 2. 独立性を最大化する先行6原本 — ソース調査対象として決定

| 調査順 | モデル・一次リンク | 既知のpublisher source（十進GB） | 主な保全理由 |
|---:|---|---:|---|
| 1 | [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) | 55.586 | 公式原本を保持し、すでに報告されたInterpretic/RVNの無検閲派生との正確な重み差分を将来検証する |
| 2 | [`RWKV/RWKV7-7.2B-20260805`](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14.402 | 定サイズ再帰stateの独自モデルで通常Transformerとは異なる計算体系を維持する |
| 3 | [`GSAI-ML/iLLaDA-8B-Base`](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 16.513 | 双方向マスク拡散言語モデルの独立原本を確保し自己回帰ベースへの集中を避ける |
| 4 | [`microsoft/TRELLIS.2-4B`](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16.237 | 画像から3D形状とPBR材質を生成する独立の学習済み重みを保全する |
| 5 | [`ACE-Step/acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 19.949 | 一般TTS・LLMと違う音楽生成拡散モデルの学習成果を保全する |
| 6 | [`HuggingFaceBio/Carbon-X`](https://huggingface.co/HuggingFaceBio/Carbon-X) | 29.656 | DNA配列と自然言語の専門学習済み重みを保全する |

**先行6件のpublisher source合計は152,343,191,968 byte（152.343GB）**。重要なのは原本6件を必ず取得することではなく、固定ファイル・LICENSE・補助学習部品・本人承認を順に閉包すること。各モデルはv48で既にSELECTまたはCONDITIONALなので、追加登録で水増ししない。

保存価値を具体化する一次資料：
- [RWKV7作者モデルカード](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) は7,199,932,416総パラメータ、BF16と定サイズ再帰stateを記載。基準Transformerと異なる計算構造を保存する。ただし専用Transformers/TileLangなどのABI適合や原PTHとの重複は未評価。
- [iLLaDA作者カード](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base)は双方向マスク拡散、12T token事前学習を説明。ただしカードの7.62BとHF serialized metadata 8,250.5Mの差があるため、**完全重み数はさらに検証する**。`trust_remote_code`を実行して数える方法は禁止。
- [Qwen公式重み](https://huggingface.co/Qwen/Qwen3.8-27B)は無検閲派生との比較に不可欠。単なる形式変換と別の後学習成果を分離し、親重みを重複して取得しない。
- [Microsoft TRELLIS.2](https://huggingface.co/microsoft/TRELLIS.2-4B)は3D形状・材質、[ACE-Step](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo)は音楽生成、[Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X)はDNA配列と言語の学習済み融合。これらは別タスクだが、ライセンス表示だけでruntime/dependencyの権利は確認できない。

## 3. 無検閲を重視した高精度マスター整理

既に取得済みと報告された`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`と`0bserverx/...-Uncensored-GGUF`のQ4は**実用形式**。追加のマスター候補として[Interpretic v2 BF16](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) **55,586,056,799 byte**、[0bserverx RVN F16 GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) **53,808,281,888 byte**を既存R115方針で維持する。合計 **109,394,338,687 byte**の候補増分であり、現行4TBアーカイブ枠への適合・権利・Dドライブ余裕は未確認。

重要な証拠上の区別：RVN-F16は作者の公開した再構成元で、**学習直後の元BF16が存在したとの証明ではない**。同一RVN学習結果のF16と別sharded safetensorsを、二つの独立学習済みモデルとして数えない。Q4も本人の承認なく削除しない。OrcaRouter公式Gated原本は本人の利用権が未確認のため取得保留を継続する。

## 4. 新モデル3件の採否（本回は正式な追加0件）

| モデル | 一次資料 | 判断 |
|---|---|---|
| **Reson8/Rumble-2-Flash** | [作者の11月18日公開記事](https://huggingface.co/blog/rumble-2-flash)、[公式model card](https://huggingface.co/Reson8/Rumble-2-Flash) | **新規研究候補、正式SELECTにはしない**。0.5B本体＋CTC head、19ファイル1.386GB、Apache 2.0表示。Publisherの英語WER6.60%・多言語6.96%は既取得報告のWhisper/Qwen3-ASRとの独立した日本語/英語30以上の同条件試験ではない。完全な追加学習部品数を静的に数える。 |
| **nvidia/Nemotron-Labs-Sigma-distill-spec-3B** | [公式モデル](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B) | **HOLD**。自律連続拡散/AR検証は固有だが他社runtimeでcustom codeの安全・ABIが未確認、LICENSE表示`other`。 |
| **sensenova/SenseNova-Loop-9B** | [公式モデル](https://huggingface.co/sensenova/SenseNova-Loop-9B) | **HOLD**。Gatedで本人承認未確認。既取得報告のARLoopと別学習成果かもしれないが先に権利・重み・runtimeを確認する。 |

多くの同サイズのTTS/汎用LLM、通常のQ4/Q5/Q6/Q8、元と違いのないGGUF/ONNXを大量収集する方針は採らない。原本の再生成可能性・学習の独立性・必要な実務品質が確認できない派生は保存に格上げしない。

## 5. 残り23モデルの正確なsource-ID・revision・研究帯

| # | repo IDと一次リンク | source GB | 帯 | v48判断 | 観測source commit（40桁） |
|---:|---|---:|---|---|---|
| 1 | [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) | 55.586 | A | select | `37561816e66b5b9153b1b64c10968c18c1e6f4a0` |
| 2 | [`RWKV/RWKV7-7.2B-20260805`](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14.402 | A | select | `9e47155004fe9df0f2a8015efa9152595c9065be` |
| 3 | [`GSAI-ML/iLLaDA-8B-Base`](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 16.513 | A | select | `a1b5b5f8a31a3854a46205ee584178c04b45ec9a` |
| 4 | [`microsoft/TRELLIS.2-4B`](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16.237 | A | select | `af44b45f2e35a493886929c6d786e563ec68364d` |
| 5 | [`ACE-Step/acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 19.949 | A | conditional | `d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee` |
| 6 | [`HuggingFaceBio/Carbon-X`](https://huggingface.co/HuggingFaceBio/Carbon-X) | 29.656 | A | select | `17de89165e25c49e7de4f845d0e5d464469de359` |
| 7 | [`ResembleAI/chatterbox`](https://huggingface.co/ResembleAI/chatterbox) | 10.681 | B | select | `5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18` |
| 8 | [`OpenMOSS-Team/MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | 16.996 | B | select | `cdd3b911b1585e3f2dbc7775ef10f9926f58850a` |
| 9 | [`PrentisAI/GroundGUI-8B`](https://huggingface.co/PrentisAI/GroundGUI-8B) | 17.550 | B | conditional | `9db378189fddaabb5f6e347b9053858a392022ac` |
| 10 | [`kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers`](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers) | 26.671 | B | conditional | `4c487e8b4aeeb9059e5a77905aa2ddb59ec28f81` |
| 11 | [`microsoft/Fara1.5-27B`](https://huggingface.co/microsoft/Fara1.5-27B) | 54.744 | B | select | `299c8406a6c6256d45ec200d1ac12b34c5599d9b` |
| 12 | [`meta-models/Muse-Glimmer-30B`](https://huggingface.co/meta-models/Muse-Glimmer-30B) | 59.582 | B | conditional | `1297fd7dfeac4598948a5d15886968435c81c2b7` |
| 13 | [`ibm-granite/granite-switch-4.1-30b`](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) | 59.991 | B | select | `eb206725d03c0f1c409ce3aa512afe325fdf8731` |
| 14 | [`tencent/Hy-Memory-30B-A3B`](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | 60.143 | B | select | `64a460a94d5498b7316fb02395c72d01c47a7347` |
| 15 | [`google/gemma-4-31B`](https://huggingface.co/google/gemma-4-31B) | 62.579 | B | select | `5bbc2fb1c1b2c611d06e3d9f23c170ba21659d89` |
| 16 | [`allenai/Olmo-3-1125-32B`](https://huggingface.co/allenai/Olmo-3-1125-32B) | 64.477 | B | select | `c2b61dae89a1ad10e4ad5653d0e46b590902607b` |
| 17 | [`EPFLiGHT/OLMo-2-32B-MeditronFO`](https://huggingface.co/EPFLiGHT/OLMo-2-32B-MeditronFO) | 64.477 | B | select | `04c6953977c3a9f913e3d08a6c23edaae6bd6459` |
| 18 | [`Nanbeige/Nanbeige4.3-33B`](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | 66.257 | B | select | `df919e1e2cf077a22204c78b6c826bf3db18bc08` |
| 19 | [`OctoMed/OctoMed-32B`](https://huggingface.co/OctoMed/OctoMed-32B) | 66.726 | B | select | `7b480e62a0f59139aa504e67d62974b83e360200` |
| 20 | [`Qwen/Qwen3.5-35B-A3B-Base`](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base) | 71.927 | B | select | `0f0813072d2358973511097385626f21fcb6d422` |
| 21 | [`openai/gpt-oss-120b`](https://huggingface.co/openai/gpt-oss-120b) | 130.526 | B | select | `b5c939de8f754692c1647ca79fbf85e8c1e70f8a` |
| 22 | [`Qwen/Qwen3-Coder-Next`](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 159.376 | B | select | `a7fbcb5c0e12d62a448eaa0e260346bf5dcc0feb` |
| 23 | [`mistralai/Mistral-Small-4-119B-2603`](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 241.887 | B | select | `a11f36bebf709121056b1dbcc943d1c6afbe494d` |

表の`source GB`は出版社から観測した対象sourceファイル数と容量に依拠する。今回の完全な`files[]`・個別LFS SHA-256・親`LICENSE`・ファイル抜け・重複・tokenizer/codecは再照合していない。**形式だけでダウンロードキューに投入せず、不明を0 byteとして予算計算しない。**

## 6. 政策上の事実と仮説

[米BISの2026年11月16日公式発表](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は高度半導体と遠隔計算資源へのアクセスを対象とする。米Federal Registerの[公開検査文書2026-23529](https://public-inspection.federalregister.gov/2026-23529.pdf) IV.Aには旧AI Diffusion Rule由来のモデルウェイト輸出分類ECCN 4E091を撤廃する内容がある。正式公布日・発効日は官報掲載後に再検証する。**公開ウェイトの私的保管全般が法的に禁止されたとの断定は誤り**。一方、個別のライセンス・人格同意・Gated・輸出先・配布元の公開停止はそれぞれ独立して確認する。

規制の具体的発生確率、個別の強制削除時期は不明。無検閲・強力な小型・高度専門モデルが将来制約される可能性をストレスシナリオとするが、その不確かな予測は無許可アクセスの理由にならない。Exaは本日時点で402（枠超過）で取得不能のため、**今回Exaを利用して一次検証したとは記録しない**。

## 7. H / T / D / C / U、単位・実装前提

**H（反証可能仮説）**：旧59候補を現行取得報告53件と突合して重複除外すれば、元の能力とは異なる6モデルの原本を先に研究し、不要な二重取得を避けられる。測度は完全repo ID一致、現在台帳に記載のsource bytes、独立用途数。

**T（最小検証）**：全59 IDとVERIFIED 53 IDを完全一致照合、重複件数36、残り23を列挙。原本6件の40桁commit・sourceサイズ・総数上限を一次資料と比べる。利用可能になった実機でモデルごとに30件以上の固定課題、同CPU/GPUクロック・driver・backend・dtype/zero-point・batch・context/KVでメモリ、精度、中央値速度を測る。実機試験は本回未実施。

**D（合否）**：PASS_METADATA＝残23件と6先行IDが完全一致、v48既存SELECT/CONDITIONALで、取得承認ゼロ。FAIL＝未許可Gated取得・LICENSE違反・必要学習部品の総数未確認で最終lock・不正hash・承認なし実行。UNCERTAIN＝物理Dドライブ同定・独立SHA・完全offline復元・実測モデル性能と実容量。

**C（破れ方）**：機能的には異なるが再現性利益が低い、同SHA原本が既に存在した、元LICENSEで用途を許可されない場合は優先順位を下げる。反例が出れば優先順位を修正する。

**U（不確かさ）**：モデルカードの数値、外部codec、稼働環境、報告済み取得の自己申告、将来の配布先条件。実測分布がないため合成標準不確かさ`u_c`と包含係数`k`は算定できない。

### 変数表

| 記号 | 意味 | 単位（SI） | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| `n_s` | 前回次波候補数 | 1（無次元） | 59 | 固定旧source wave | 整数スカラー |
| `n_v` | 次波中の既報告数 | 1（無次元） | 36 | repo ID完全一致 | 整数スカラー |
| `n_r` | 今回の未報告数 | 1（無次元） | `n_s-n_v` | 物理未保存と同義ではない | 整数スカラー |
| `B_r` | 未報告source容量 | byte（SI単位ではない） | 1,386,933,535,900 | 外部依存は除外 | 非負整数スカラー |
| `B_A` | 先行6source合計 | byte（SI単位ではない） | 152,343,191,968 | 出版社の対象source合計 | 非負整数スカラー |
| `F_{min}` | 取得後維持する空き | byte（SI単位ではない） | 200,000,000,000 | 全stageでも維持 | 非負整数スカラー |
| `P_{total}` | 総学習済みパラメータ | 1（無次元） | 全expert/encoder/learned head | 不明なら最終lock停止 | 非負整数スカラーまたはnull |

**導出と次元チェック**：`n_r=59−36=23` は件数同士の差。 `B_r`と`B_A`はbyteを同じbyte単位で足した結果であり、総パラメータ数（無次元個数）やGPU RAMと混同しない。v48は150Bを超える量子化モデルの例外を非常に厳しい同条件実測で判定する制度に更新済みであり、本回新規に例外承認したモデルはない。

## 8.〈応用・転用例〉・ERROR CHECK

関連分野：**モデルアーキテクチャ比較**（自己回帰／拡散／再帰）、**情報保存・ハッシュ同一性**（親・マスター・圧縮版）、**法とデータガバナンス**（許諾・Gated）、**実行システム工学**（HDD/SSD、backend/ABI、zero-point、KV cacheと物理RAM）。

**ERROR CHECK**：v48 201登録・154有効を維持。53 VERIFIED報告（579ファイル・約270.836GB）、次波59=36既報告＋23未報告。先行6件約152.343GB、無検閲高精度source提案約109.394GB。全23件の元repo ID・40桁revision・source容量をJSONで残し、承認・実取得・実行・既存削除はいずれも0件。実機の再ハッシュと完全オフライン再現、権利承認は**未完了**でありPASSとしない。

## 9.〈次に考える問い〉

**不足する200GBの物理安全余裕を守りながら、汎用大型原本1件の代わりに、法的に保存可能な再帰・拡散・3D・音楽・科学の6原本を完全復元できるか。** 実際の選択byteと依存/障害率で決め、能力が高いという宣伝だけで決めない。
