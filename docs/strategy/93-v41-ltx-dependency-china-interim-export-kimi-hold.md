# R93：LTX-2.5のGated親・未固定音声映像依存と、中国の暫定輸出前登録を正式区別する

## 1.〈本論〉
調査日2026-11-15。Hugging Face接続で現行v41のLTX3有効候補と、別研究候補のLTX2.5 Pre-Trained/Kimi K3.1 Proを一次照合。**採用済みLTX3件の採否を変えず、依存原本・派生権利の追加停止条件を付す。** model weightの取得や実行はしない。

### 実在するGatedと親からの学習済み依存の区別
[Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5)と[LTX-2.5-Pre-Trained](https://huggingface.co/Lightricks/LTX-2.5-Pre-Trained)はHFでGated。前者のmain22B DiT以外にGemma4 12B、動画・音声decoder、特定workflowの追加head/LoRAがある。Pre-Trainedの別stageはVAE/Vocoder等を一体に抱える独立の学習済みチェックポイントだが、追加43GiB級＋encoder・アクセス権と追加価値が未確認で今回はHOLD研究。
[Stuubs Remix](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)と[ChrisColeTech](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8)は公開メタデータで非Gated。しかしこれはLightricksのGatedファイルにアクセスできる証明ではない。Stuubs v1は作者の異なる学習済みタスクベクトル＋OmniNFT RL-LoRAマージ。BF16原本SHA候補6e0ff9c9d8a1d0747579f1f50d10a9c3822a9a8f265322a5edd476044b0fbf4fを一つ保持し、int8/nvfp4/GGUFやbetaを量子化と学習stageの区別なしに重複取得しない。作者はINT8を実行用に推奨するが、BF16は元マージ検証に向いたアーカイブ候補。厳密byte/40桁revisionはまだ未確定。
ChrisColeTechはカスタムGemma4/映像VAE/音声VAEを含めた4部材の作者パッケージを記載する。『すべて本家と同じだから共有できる』とは判定しない。各部材のSHAを比較して同じ公開原本なら共有、違うなら独立学習済み内容とライセンスを精査。派生元の権利があるから公開元の許諾を迂回してよいとは扱わない。
元の[LTX2.x LICENSE-2_x](https://github.com/Lightricks/LTX-2/blob/f0f2f8607189c78a72420b2b63cb1975b5eca179/LICENSE-2_x)は2026-10-29改訂、派生も含む。年商USD1000万以上の企業の商用利用には原則別契約が必要で、非商用例外やドナーNOTICEを確認する。MIT/Apache2ソースコードの権利を重みの無条件利用許可と混同しない。

### 現在の法的規制と未成立の目録改定を区別
中国MOFCOM/MOSTの[2026年第48号公告](https://www.mofcom.gov.cn/zfxxgk/fdzdgknr/ztfl/blgg/art/2026/art_718071a95e6948cdb652e2f08f422673.html)は、40技術（AI23件）の**輸出管理目録の改定案**への意見募集（10月16日～11月15日）である。同時に、対象になる特定技術の海外への所有権移転・使用許諾・海外主体への支配変更などに**正式改定までの暫定的輸出前登録**を既に導入している。[MOFCOMの説明](https://english.mofcom.gov.cn/News/SpokesmansRemarks/art/2026/art_74bf283f105a4b19a11f7430df3671ae.html)は、公開済み技術の例外と自動許諾等の緩和にも言及する。最終目録はこの公告をもって全件確定したわけではない。**全公開ウェイトの個人保存・Hugging Faceからの一般DLを一律禁止した法令ではない**。
EUは[AI Act 53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)のGPAI提供者義務と一部open-source例外、[2026-08-02執行](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start)を区別する。S1→S2→S3配布制限連鎖は未計測ストレス仮説であり、特定repoの削除予定を創作しない。

### 超150B特例の新調査候補
[moonshotai/Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro)は作者表示**約2.8Tの全パラメータ**、活性104B、MXFP4 QAT、100万token context、視覚401M。2.8T＞150Bであり、活性104Bが閾値判定の代わりにならない。作者が安全対策を講じた公開モデルという評価は、同一学習済み未公開版が取得可能だという意味ではない。全ファイル選択と現機材・SSD expert streamingの実測ピークRAM、150B未満モデルとの同条件品質/速度、ライセンス・本人許可が未完のため、今回の新資産には追加せず研究HOLD。

## 2. 変数表・次元
| 記号 | 意味（日本語） | SI単位 | 定義・定義域/前提 | 型 |
|---|---|---|---|---|
| P_k | Kimi K3.1 Proの出版社全パラメータ数 | 1（個） | 約2.8×10^12、MoE非活性expert含む | 正実数スカラー |
| P_a | 同モデルの活性パラメータ数 | 1（個） | 約104×10^9、前向き推論使用部 | 正実数スカラー |
| P_t | ポートフォリオ標準の全数スクリーニング閾値 | 1（個） | 150×10^9、全学習済み数 | 正実数スカラー |
| C | アーカイブ選定上限 | byte | 4,000,000,000,000、物理実測ではない | 非負整数スカラー |
| F | 最低実空き容量 | byte | 200,000,000,000、現物HDD未測定 | 非負整数スカラー |
次元検査：P_k/P_t ≈18.67（無次元）で明らかに標準を超過。P_aはP_kの代替ではない。C/Fはbyteで、パラメータ数とは比較できない。MoE 4bitのモデル重量からRSS/VRAMの実測値を推測しない。

## 3. H/T/D/C/U・ERROR CHECK
H：子modelのpublic listingだけでは完全復元できず、学習済みGemma/VAEsとLTX2.x派生権利の個別確認が必要。T：HF5 repoアクセス観測、3有効モデルID、一つの固定公式LICENSEの権利、MOFCOM公式原文とEU53条を静的照合。D：Gated親／子非Gatedと登録案＋暫定制度の区別はPASS。本人の実重み・権利/全依存とlocal SHAはUNCERTAIN。C：子配布に完結する独立Gemma/VAEsが同一版で含まれ、親Gated本体に依存しない場合は個別ゲートを解消できる。U：作者カード・モデル断面・元ライセンス版、実験HDDとCPU/GPU/driver/環境が不確か。反復のないためu_c/kは算定不能。
ERROR CHECK：新モデル採用0・状態変更0、Gated表示はparentとchildで混同しない、所有者本人承認0。機械学習アーキテクチャ／デジタル保存／国際輸出規制／ソフト供給網の4分野に関連。

## 4.〈次に考える問い〉
二つのLTX派生に必要な外部Gemma/VAEsの現物SHAが一致するなら、その共有を先に実証すべきではないか。
