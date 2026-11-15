# R94：正式v42／Gated親を持つLTX-2.5系3件の依存・権利・政策停止条件

**2026-11-15調査。** [HF一次・中国MOFCOM輸出登録・Kimi特例原本](../../catalog/research/2026-11-15-r93-hf-ltx-parent-gated-china-interim-kimi-review.json)と[現行正本](../../catalog/effective-portfolio-2026-11-15-v42.json)に基づく。旧v41の195資産・有効148、SELECT53、CONDITIONAL95、Gated20、総数不明の有効9を**変更しない**。新規追加・降格・DL承認・自動実行すべて0。

## 1.〈本論〉追加した学習済み依存・ライセンスの正式停止ゲート
対象はLightricks/LTX-2.5、ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8、Stuubs/Stubelius_Remix_Ltx2.5の3件。HFの一次観測では**本家はGated、子2件はHub非Gated**。子modelが公開でも親モデルファイルの本人認可・Gemma4 12B学習済みtext encoder・映像/音声VAE・派生ドナーNOTICEが揃ったという意味にはならない。逆にChrisColeTechが自己完結の異なるencoder/VAEを配布している場合、追加のGated原本が常に必要と仮定するのも誤り。**選択したworkflowで必要な各ファイルの不変revisionとpublisher SHAが一致するか、個別に判定**。
本家22Bは主DiTの数であり、完全pipeline総数ではない。従来の150B未満screen PASSを変更していないが、**外部learned成分は別に未確定**で最終取得は禁止。Stuubsは元マージBF16ファイルSHA候補6e0ff9c9d8a1d0747579f1f50d10a9c3822a5edd476044b0fbf4fを一原本候補とする。INT8、NVFP4、GGUFとbeta stageを全自動追加しない。ChrisColeTechは作者が変更したGemma4/Audio VAE/Video VAEを含むため、元LTXと同一SHAと仮定して無断共用しない。
[固定公式LTX2.x LICENSE](https://github.com/Lightricks/LTX-2/blob/f0f2f8607189c78a72420b2b63cb1975b5eca179/LICENSE-2_x)は2026-10-29改訂で、派生物の権利を含む。年商1000万USD以上の企業の多くの商用利用は別契約要件を満たす必要がある。個人・非商用の例外や各ドナーlicenseを保持。『Hub非Gated』と『誰でも再配布可能』を混同しない。

## 2. 現在の国際法規制を正確に表現
[中国商務部・科技部の公告2026年第48号](https://www.mofcom.gov.cn/zfxxgk/fdzdgknr/ztfl/blgg/art/2026/art_718071a95e6948cdb652e2f08f422673.html)は40技術/AI23技術の**最終輸出管理目録の改定案**に意見募集（2026-10-16～2026-11-15）する一方、対象技術の海外への所有権移転・ライセンス・実質支配変更等には**公布日から暫定的な事前登録**をすでに導入している。全件を『まだ単なる草案』とするのは誤り。公開・発表済み技術の取り扱い除外や、将来想定する自動ライセンス等を無視して『あらゆるHFモデルの個人DLが違法化』と一般化するのも誤り。
[EU公式AI Act 53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)のGPAI提供者義務・条件付きopen-source例外と[2026-08-02執行開始](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start)も、一般のウェイト所有禁止とは分ける。S1→S2→S3の規制拡大は反証可能なストレス仮説として残す。

## 3. 新規候補の採否
HF配布中のLTX2.5 Pre-Trainedは本家SFT前の独立重み・バンドルVAEを持つが、Gatedで約43GiB＋Gemma encoderが必要、同族追加価値と4TB余白が未確認につき研究HOLD。Kimi K3.1 ProはMXFP4 QATの**2.8兆 total**・約1040億 activeで、活性数を150B baseline判定に使わない。同じHW/backend/context/batchで150B未満モデル以下の完全ピークRAMと品質・速度を30回以上実測していないため、量子化例外の新規採用・取得は禁止。無断Gated回避や未公開の別安全強度版の存在を推定しない。

## 4.〈変数表〉・次元検査
| 記号 | 意味（日本語） | SI単位 | 定義／定義域・前提条件 | 型 |
|---|---|---|---|---|
| P_k | Kimi K3.1 Pro公称全総数 | 1（個） | 約2.8×10¹²、MoEの全expertを含む | 正実数スカラー |
| P_a | 同モデルのactive数 | 1（個） | 約1.04×10¹¹、推論時選択expertのみ | 正実数スカラー |
| P_0 | 通常の総数基準 | 1（個） | 1.5×10¹¹、base/quant無関係 | 正実数スカラー |
| C | 物理保存の計画枠 | byte | 4,000,000,000,000、HDD空き未計測 | 非負整数スカラー |
| F | 実HDD最低空き床 | byte | 200,000,000,000、実測前 | 非負整数スカラー |
P_k/P_0≈18.67は無次元比で、量子化後もパラメータ個数は減らない。P_aとP_kは別量で、RAM・byte・GPU条件と直接比較不可。C/Fは同じbyte単位だが、推論RAM/実際の保存済み容量ではない。

## 5. H/T/D/C/U・ERROR CHECK
H：本家Gated・子2件非Gatedという観測と、それぞれの学習済み外部依存の未固定を別途表現することが適切。T：既存3モデル・HF親2リポジトリ・2子repo、公式LICENSE/Notice、MOFCOM告示を静的照合し、148件全資産ID、95件CONDITIONAL accessを検証。D：一次資料アクセス状態・ライセンス制度の区分と全ID一致はPASS。親Gated個人権限、learned SHA・合法再配布/実機HDD/benchmarkはUNCERTAIN。C：子に完全な同等学習済みパーツが独立配布され、SHA・権利が確定すれば親の別ファイル取得不要になる。U：ファイル版・ドナー権利・定量的な速度/品質・所有者の資格が未確定。u_c/kは校正した分布なしで算定不能。
**ERROR CHECK**：同一195 ID／148 active／95 CONDITIONAL／Gated20／不明total9／新規取得承認0。学際：生成モデル、供給網ハッシュ、著作権/輸出管制、デジタル保存。

## 6.〈次に考える問い〉
複数の派生が同じGemma/VAEsを必要とするなら、配布元のSHAが本当に一致するかを次の固定原本調査に優先すべきではないか。
