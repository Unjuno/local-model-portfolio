# R137｜v58：Inkling 2 MiniとDettato四段音楽転写原本の選定・ソース保全

基準日：2026-11-21。正本案は **v58／218登録・171有効（SELECT53、CONDITIONAL118）**。過去のv57 **213登録／166有効**を完全保持し、5つの独立した学習済みモデル状態だけをCONDITIONAL追加する。[選定overlay](../../catalog/revisions/v58-2026-11-21.json)、[5原本の固定source](../../manifests/drafts/r137-2026-11-21-inkling2mini-and-dettato-four-publisher-sources.candidate.json)、[機械可読の根拠と停止条件](../../catalog/decisions/2026-11-21-r137-v58-inkling2mini-dettato-original-selection.json)。これは**weight取得・本人ライセンス承諾・モデルコード実行・完全オフライン復元の承認ではない**。

## 1.〈本論〉なぜ今選び、何を保存するか

選定基準はモデルの単なる人気/パラメータ効率ではなく、**①独立した学習済み機能、②取得経路の来歴と固定可能性、③小型モデルの代替困難性、④復元に必要な依存グラフ、⑤合法利用、⑥実保存容量**の6条件。将来の一律禁止日や確率は推定できない。ユーザーのモデルポートフォリオに以前はなかった looped multimodal MoE checkpoint と、polyphonic MIDI instrument-track transcription pipeline を追加する。

| 正式CONDITIONAL選定 | 固定40桁revision | 出版社repo source容量 | 出版社の総パラメータ数 | 固有の保存対象 |
|---|---|---:|---:|---|
| [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) | `1fb4134b9a74f9681054f4ef82e4bf1f458a2337` | **20,191,643,271 byte**（14 files） | 本体Hub **26,388,646,440**＋別MTPヘッダ **317,897,872** | Native NVFP4/MXFP8を持つループ型128-expert MoE、画像入力と別MTP学習結果 |
| [kobimusic/dettato](https://huggingface.co/kobimusic/dettato) | `a0d1e354d282c4ed458b83b287065587979b053e` | 64,794,996 byte（8 files） | 15,299,474 | 88鍵の複声音高、音符onset/frame/offset学習 |
| [kobimusic/dettato-evidence](https://huggingface.co/kobimusic/dettato-evidence) | `5633f28ee330a48bc31bdd3f9f98bb1a71206141` | 21,234,165 byte（6 files） | 4,930,929 | 学習済み音符修正・欠落補完 |
| [kobimusic/dettato-grouper](https://huggingface.co/kobimusic/dettato-grouper) | `5a94cea2329f53228d7bcf1fd6a9f8d9778cc75b` | 12,460,661 byte（5 files） | 2,896,613 | 楽器ID・トラック割当の独立学習結果 |
| [kobimusic/dettato-drums](https://huggingface.co/kobimusic/dettato-drums) | `97801f2328e32e4c87b12586aa81121f62cacacb` | 21,976,775 byte（6 files） | 5,017,049（Hub表示） | ドラムキット・管弦楽打楽器のモデルとrouter |
| **選定計5repo** | | **20,312,109,868 byte（39 files）** | Dettato四段 **28,144,065** | 全39 path/byte/Git SHA1／17 LFS SHA256参照の公開固定source |

**四段全体の原本重み合計は112,758,556 byte**。全配布repoの120,466,597byteとの差にはcard、configuration、benchmark figuresなどが含まれる。後続のコード実行版・音声前処理依存は別途固定が必要。既存カタログの[SheetSage2](https://huggingface.co/m-a-p/SheetSage2)は旋律・コード推定や楽曲構造であり、Dettatoの88鍵多声音符の楽器別performance MIDIとドラム検出を完全に代替しない。

## 2. Dettatoの「20M」・ベンチマーク・学習権利を正確に分類

出典：[kobi.music作者記事](https://kobi.music/research/dettato)、[github/kobimusic/dettato](https://github.com/kobimusic/dettato)、[出版社4モデルカード](https://huggingface.co/collections/kobimusic/dettato)。作者の**20.3M**は大部分の公開転写比較を計算した**transcriberとdrumsの2段**。公式CLIが実行するのはtranscriber、evidence repairer、grouper、drumsの**4段＝約28.1M**。この違いを「20Mで全システムの性能が検証済み」と混同しない。

- **作者値（未独立再実験）**：9ベンチマーク集合のtranscriber+drums composite F1は59.2（作者の95％区間57.9～60.6）、MuScriptor 1.3Bは45.1。Mireloが公表した3セットに限るとDettato60.8、Mirelo56.1。ただしセット・音源・評価方法の差が残り、上位互換を全音楽ジャンルへ外挿できない。
- **決定的な限界**：出版社READMEは**4段の統合end-to-end F1をまだ計測していない**と明記。evidence単独+0.30F1は古いtranscriberが入力。grouperは楽器同定が弱く、jazzでsax/lead guitarの音がpiano trackへ紛れる例がある。音符長は演奏由来の時刻を保持し、小節へ量子化した読みやすい楽譜とは異なる。
- **入力要件**：drumsの検出には元録音サンプルレート40,000Hz以上が必要。Python3.10+、PyTorch2.2+、音声デコードに`soundfile`と場合により`ffmpeg`が必要。配布コード[固定Git commit](https://github.com/kobimusic/dettato/commit/9b724251794f2bbd5eaa43e54734e5a251829130)は**`9b724251794f2bbd5eaa43e54734e5a251829130`**。全4モデルを`DETTATO_WEIGHTS`で局所フォルダ指定してロードするオフライン設計を作者は提示しているが、本人機材での実証はまだない。
- **出版社の速度例**：RTX 5060 8GB、4分曲約15秒、6分曲約25秒、VRAMピーク4GB未満との作者値。GPUクロック・CUDAドライバ・バッチ制御・実測反復分布は未公表、ユーザー機材での性能保証ではない。
- **ライセンスの注意**：コードとweightはGitHub固定LICENSE/NOTICEとHF cardでApache-2.0。ただしGrouperとDrumsの学習に使った公開研究データには非商用ライセンスが一部存在すると作者自身が説明。**CCライセンス付き録音は著作権が消滅した録音ではない**。作者記事の「著作権付き録音を使わなかった」は法務検証済み事実と断定しない。学習データを再配布するか、生成したMIDIを商用利用するか等の行為ごとに権利を確認。

## 3. Inkling 2 Miniは「26B相当の4bit量子化」とは違う

出典：[Thinking Machines公式モデルカード](https://huggingface.co/thinkingmachines/Inkling-2-Mini)／[Acceptable Use Policy](https://thinkingmachines.ai/model-acceptable-use-policy/)。独立学習済みnativeのMoEで、**24物理層の中間12層を3回反復**、128 expert中各トークン8 expertを使用。出版社の物理activated約3.4B、3pass時のeffective activated約5.4Bは、保存する全expert個数約26.4Bとは異なる。量子化はModelOpt native NVFP4/MXFP8。1M contextや高性能は出版社説明であり、ユーザーHW上の実証ではない。必要HWとして**32GB以上のGPU/Apple unified memory**をメーカーは推奨し、8GB GPU単体での高速ローカル実行は保証されない。

**重み本体を転送せず静的検査**：公開Hubの固定revisionに対するHTTP Range206で、主safetensorsのヘッダ148,408byte（1,244 tensor）、別`mtp.safetensors`ヘッダ5,664byte（54 tensor、BF16合計317,897,872個）を読み取った。Hub表示の主モデル論理総数は26,388,646,440で、主重みの物理的シリアライズ要素は17,597,909,544。ModelOpt NVFP4のU8値はパック済みのため、両者は同じ意味のスカラーではない。研究上の暫定名目値として主+MTP=**26,706,544,312**を記録するが、厳密な物理学習パラメータのreconstructionには`hf_quant_config.json`とbackendの静的解析が要る。150B以上の上限には十分小さいという出版社の根拠で**PASS候補**とするが、実行許諾やメモリ適合PASSとは独立。

**研究上の代替**：[thinkingmachines/TML-d24-varloop-research](https://huggingface.co/thinkingmachines/TML-d24-varloop-research)はvarloopフラグを有し、midtrainingで1～5passを変化させた**異なる学習済み重み**で、主とMTPのSHAは通常版と異なる。通常版の量子化変換ではないため独自の研究価値はあるが、追加20,191,620,855byteを使い、出版社自身はproduction非推奨。現在の正式v58には追加せず**研究HOLD**として機能比較・保存容量の再判断を後回しにする。

## 4. 変数表・総数と容量の次元チェック

| 記号 | 意味（日本語） | 単位 | 定義・値 | 定義域と前提 | 型 |
|---|---|---|---|---|---|
| `P_d` | Dettato4段のHub公称パラメータ数合計 | 1（個・無次元） | 28,144,065 | 4repo独立訓練済み、drums headerとの差104個は注記 | 非負整数スカラー |
| `P_i` | Inkling主モデルの公称総パラメータ | 1（個） | 26,388,646,440 | ModelOpt packed表現に対するHub算定値 | 非負整数スカラー |
| `P_m` | Inkling追加MTPヘッダBF16要素 | 1（個） | 317,897,872 | 別safetensors、54 tensor | 非負整数スカラー |
| `P_nom` | Inkling名目総数 | 1（個） | `P_i+P_m`＝26,706,544,312 | Packed logical countの詳細検証前。主MTP別ファイル | 非負整数スカラー |
| `P_limit` | 新規取得候補のハード上限 | 1（個） | 150,000,000,000 | 全inactive expertsも含め150B以上は取得対象外 | 非負整数スカラー |
| `B_d` | Dettato4repo固定原本source | byte（情報量単位） | 120,466,597 | 25ファイル、weight以外も含む | 非負整数スカラー |
| `B_i` | Inkling固定repo source | byte | 20,191,643,271 | 14ファイル、native混合精度原本 | 非負整数スカラー |
| `B_total` | 5repoのPublisher論理source | byte | `B_d+B_i` | Owner HDD占有や差分転送量ではない | 非負整数スカラー |
| `F_min` | 容量安全床 | byte | 200,000,000,000 | 処理中も維持する条件 | 非負整数スカラー |
| `D_free` | Owner実媒体の現時点の空き | byte | null（未観測） | 正しいDドライブ容量計測が必要 | 非負整数またはnull |

**確認**：`P_i+P_m=26,706,544,312` は150B未満。Dettatoは`15,299,474+4,930,929+2,896,613+5,017,049=28,144,065`。音声stageのヘッダではDrumsのF32=5,016,945＋I64バッファ208があり、Hub表示とは104個の差がある。これを未説明の学習重み増分とみなさず、数値不整合を保全する。`B_d+B_i=120,466,597+20,191,643,271=20,312,109,868byte`。**次元検査**：P系は個数、B系はbyteのため同じ種類でのみ加算可能。量子化されたbyte長から全学習済みパラメータ数やVRAM性能を推定しない。

## 5. H / T / D / C / U・ERROR CHECK

**H（反証可能仮説）**：v58に保存した5独立学習結果は旧v57の音楽生成/音声ASR/SheetSage2だけでは復元できない機能を増やす。Dettato全4段を保存しコード固定なら楽器別MIDIへのoffline推論が可能になる。Inklingは同容量の一般量子化配布版と異なりnative looped-MoEを保全する。

**T（最小検証）**：5 repoの計39ファイル・元LFS SHA256 17件とGit OIDを固定40桁revisionの公式APIで全照合（n_min=39、初回不一致で停止）。safetensorsヘッダのみを読む静的検査でDettato4つ・Inkling主+MTPを調べた。所有者D実機は未接続。承認後の独立比較は、原音源・楽器別正解MIDIを有する合法な公知テスト最低30録音、全4段系とSheetSage2やMuScriptorを同一分割・F1/onset/offsetとトラック一致で比較。測定HW、clock、backend、batch、PyTorch/CUDA/quant zero-pointとモデルコードcommitを固定し、逐次停止条件はライセンス違反・SHA不一致・容量床割れ。

**D（合否）**：PASS_SOURCE＝5repo39件Publisher固定metadata一致／原作者ソースコードコミット記録／新たな五つのCONDITIONAL登録。PASS_OFFLINE＝Ownerに実SHAが揃い、権利・ソフトウェアABI・同じモデル復元・正常推論と独立検証が完了した場合（**現時点UNCERTAIN**）。FAIL＝無許諾Gated迂回、他人のLICENSEを勝手に同意、全モデルを20Mと誤記、2段F1を4段F1と解釈、モデル重みのローカルhash偽装。

**C（破れ方）**：インストーラが想定以外の依存を取得する、本人Windows環境で音声ライブラリが不整合、4段の楽器分類でF1が低下、Inklingが32GBを要求し一般8GB GPUで速度不十分、非商用学習データの利用目的でライセンス義務が発生しうる。

**U（主要不確かさ）**：原音源の著作権・dataset利用区分、4段ベンチの未実施、作者RTX5060のclock/バッチ不明、ModelOpt packed schema、ユーザー実ドライブ未検証。再実験分布がないため合成標準不確かさ`u_c`と係数`k`の数値は未設定。

**ERROR CHECK**：旧v57の213登録／166有効を不変更で継承し、v58では+5モデル⇒**218登録／171有効、モデル192・dataset26**。HF固定原本5repo39files20,312,109,868byte・LFS SHA参照17件。Dettato4段のdistinct checkpointは各1つずつで量子化重複なし。TML可変loopは未採用で二重追加なし。approved queue0、実モデルweight DL0、ユーザーDハッシュ0、未審査コード実行0。

関連分野：①音楽情報検索・自動採譜（MIDI/複数楽器分離）②モデル設計・量子化（再帰型MoEとnative ModelOpt）③長期デジタル保存（40桁snapshotとSHA）④ライセンス・著作権（Creative Commons録音と学習済みweightの権利）⑤実験計画・不確かさ（統合品質の独立測定）。

###〈次に考える問い〉

**Inkling 20.19GBのオフライン原本確保と、Dettato 120.47MBのコードを含む完全再現テストでは、ユーザーの実機環境でどちらがより少ない未解決依存と費用で完了できるか。** 実HDDの再ハッシュとライセンス審査で次の取得順を確定する。
