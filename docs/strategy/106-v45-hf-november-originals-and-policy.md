# R106｜2026年11月18日：Hugging Face新規原本・規制と権利条件の再監査

**対象**：GitHub `Unjuno/local-model-portfolio`、現行 `v45-20261118`（登録198・有効151）。[8件の正式ID・一次根拠・非実行採否JSON](../../catalog/research/2026-11-18-r106-hf-originals-license-and-policy.json)を作成。調査のみで、**新規正式登録0、取得承認0、実重みダウンロード0、モデル実行0**。読み取り確認済みのHugging Face認証は、各Gatedモデルの利用許諾を意味しない。

## 1. 〈本論〉目的から逆算した選定

目的は、規制の発生確率を当てることではなく、**将来、合法的に再入手しにくくなる独自の学習済み原本を、限られた4TBに重複なく長期保全すること**である。必要能力は、①出版社とファイルの一意性識別、②独立学習結果/構造の認定、③利用契約・依存・必要バイトの閉包、④固定版の安全な復元。現在、v45の151有効件にはすべて未解決取得前ゲートがあり、学習済み総数の不明な有効モデルは9件、本人承認・物理HDDの実測・復元確認は0。この前提を隠して新規モデルを`CURRENT`へ無条件登録しない。

最優先は [**osunlp/ARLoop-1.2B**](https://huggingface.co/osunlp/ARLoop-1.2B)。公式[実装](https://github.com/OSU-NLP-Group/ARLoop)と[論文（arXiv:2611.05234）](https://arxiv.org/abs/2611.05234)に基づく独立事前学習原本。**24物理層・3反復・500B学習tokens**の構成で、Attention Residualが残差履歴を深さ方向に選択する。Hubの約1.2087B個は150B基準未満。既存RWKV/Mamba/Raonと異なる学習済み構造のため、同系列量子化を集めるより原本の研究価値が高い。**モデルカードApache-2.0表示とソースコードMITは別ライセンス**。実装は`trust_remote_code=True`を含み、実行/インストールせず固定ソースとABIをまず監査する。

次点は [**KittenML/kitten-tts-2-mini**](https://huggingface.co/KittenML/kitten-tts-2-mini)。メーカーは82M、16言語、118音声（日本語を含む）、INT8 ONNX単体82.7MBと記載。Hubの全repo表示約478MBはほかの重み形式等を含むため、**82.7MBを完成した選択ファイルbundle容量と同一視しない**。ONNX Runtime・voice packs/G2P・使用言語での再現性と、Haru/ZONOS/Mayaなど既存TTSの増分価値を確認した後に正式追加を判断する。

| 新規repo ID／一次資料 | 学習済み総数（Hub/公開者） | ライセンス・アクセス表示 | この調査の判断 | 原本独自性の仮説 | 主要停止条件 |
|---|---:|---|---|---|---|
| [osunlp/ARLoop-1.2B](https://huggingface.co/osunlp/ARLoop-1.2B) | 1.2087B | apache-2.0 | 優先採用候補・不変source照合待ち | 独立事前学習500B tokenのAttention Residual反復Transformer。24物理層・3反復、既存RWKV/Mamba/R… | モデルカードのApacheタグとGitHubコードMITは別個。trust_remote_code=Trueを自動実行しない |
| [KittenML/kitten-tts-2-mini](https://huggingface.co/KittenML/kitten-tts-2-mini) | 0.0820B | apache-2.0 | 条件付き採用候補・ONNX依存固定待ち | 作者記載の16言語・118音声、82M学習済み多言語TTS、日本語含む。CPU用int8 ONNX単体82.7MB。元重みと声資産の独自性が期待さ… | Hub約478MBはリポジトリ全量表示で、INT8 ONNXと声packs/G2Pを含む選択bundleのbyteとは異なる |
| [ConwayResearch/Underdog-Woof](https://huggingface.co/ConwayResearch/Underdog-Woof) | 0.0382B | underdog-non-commercial-1.0 | 契約制限HOLD | 音声本体22.95M＋Mimi派生decoder15.3M＝38.24M。メーカーのCPU/numpy原本は40.6MBで小型ローカルTTSとして… | 独自非商用LICENSEは表示義務、商用ライセンス別途、モデル及び生成音声を用いた音声AI追加学習・蒸留禁止 |
| [speakleash/Bielik-11B-v3.1-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.1-Instruct) | 11.1688B | apache-2.0（Gated） | Gated・容量HOLD | ポーランド語/欧州語中心56言語、作者独自追加学習とSFT/RL成果。特化多言語の復元困難な学習原本。 | HF gatedで個人の実アクセス許可不明 |
| [salesforce-sovereign-intelligence/SOV-Transcribe-1](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1) | 26.6307B | apache-2.0 | 既存R105 HOLD維持 | Whisper-large-v3 encoder＋Gemma4 MoE由来の音声表記制御と固有名詞のcontext biasing。学習済み総数2… | v45 R105に同モデルの研究HOLD既存、二重登録禁止 |
| [osunlp/ARLoop-0.6B](https://huggingface.co/osunlp/ARLoop-0.6B) | 0.5831B | apache-2.0 | 同系列重複により延期 | 同作者の180B-token独立学習の小型Attention Residual反復版。1.2Bの構造と強く重なる。 | 1.2B版で代替できない比較実験目的が未立証 |
| [osunlp/PreNormLoop-0.6B](https://huggingface.co/osunlp/PreNormLoop-0.6B) | 0.5828B | apache-2.0 | 論文対照用として延期 | ARLoop論文の対照recurrent-depth PreNorm学習重み。論文再現での価値はあるが保存先の独立能力は限定的。 | 研究の比較実験を必須目標とするときのみ再審査 |
| [n4ze3m/tiny-voca](https://huggingface.co/n4ze3m/tiny-voca) | 総数不明 | apache-2.0 | 総数不明と重複でHOLD | 英語向け小型TTS。ONNX/GGUF表示、原本trained-totalについて今回のHub照会は数値を返していない。 | 総パラメータ不明なので重みlock準備停止 |

**採否のポイント**：同作者の[ARLoop-0.6B](https://huggingface.co/osunlp/ARLoop-0.6B)と[PreNormLoop-0.6B](https://huggingface.co/osunlp/PreNormLoop-0.6B)は研究対照/スケーリング価値はあるが、1.2B原本に追加して保存するだけの独立目的が未特定で延期。新規8件はv45の198件には存在しないことを実台帳の完全一致で確認した。

[**Underdog Woof**](https://huggingface.co/ConwayResearch/Underdog-Woof)は音声モデル22.95M＋Mimi派生decoder15.3M＝総38.24Mで、作者のCPU/numpy二声版約40.6MBという特色がある。しかし[原文LICENSEとNOTICE](https://huggingface.co/ConwayResearch/Underdog-Woof/blob/main/NOTICE)に基づく**非商用、帰属表示、音声生成モデルへの学習/蒸留用途禁止**があり、ポートフォリオの追加学習目的への利用を無条件には認められない。作者が示す13.8倍リアルタイムは**Apple M5 Max、CPU 1スレッド、numpy/Juno声**の条件であり、独立実機測定ではない。今は契約HOLDが妥当。

[**Bielik-11B-v3.1-Instruct**](https://huggingface.co/speakleash/Bielik-11B-v3.1-Instruct)はポーランド語を重点に56言語のSFT/RL原本。Hub上の**Gated**を確認し、本人承認は未確認。配布repo約22GBに対しv45の仮想予算残余約27.409GBと競合し、依存容量を加えると増分費用が大きい。

[**SOV-Transcribe-1**](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1)はWhisper音声encoder＋Gemma 4 MoE由来の26.63B**総数**（活性約4.6B）で、音声の表記制御とcontext biasingという独自学習結果がある。ただし既存[R105](105-v45-raon-simons-original-preservation-2026-11-18.md)で53,317,410,780byteの**上流repo全量**と容量・重複のHOLDが記録済み。追加候補として二重登録しない。公開者のベンチ優位を同条件独立測定としない。

[**tiny-voca**](https://huggingface.co/n4ze3m/tiny-voca)はONNX/GGUF表示があるが、今回のHubレスポンスは原本の**学習済み総数を返していない**。サイズをパラメータ数と誤認せず、重みlock準備停止。

既存登録のHaru-4B、PAN2、Praxis-1 Droid、ZONOS3-Mini、Raon-1 nano、Simons-297Mは**v45実台帳と照合して重複追加しない**。

## 2. 配布規制：現行事実・予想・誤認の分離

[**中国商務部・科学技術部2026年第48号公告（2026-10-16）**](https://www.mofcom.gov.cn/zfxxgk/gkml/art/2026/art_ccd0391072a94c809ae7e820abe2536b.html-322)は2要素を明確に区別する。(a)輸出禁止・制限技術目録への追加は**意見募集案**（2026-11-15締切）であり、11月18日時点で正式改訂施行済みと証明できていない。(b)公告から正式改訂施行まで、所定の**技術輸出、技術ライセンス移転、所有権移転等**に臨時の**輸出前登録**が設定されている。したがって「全部未施行」も「日本の全ローカルモデルの保有が直ちに違法」も誤り。実行者・地域・移転行為を特定して判断する。[中国商務部公式解説](https://www.mofcom.gov.cn/xwfb/xwfyrth/art/2026/art_d7661dbf62794345a221404f82a25959.html)を併記。

[EU AI Act公式FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)はGPAIのオープンソースに一定免除とシステミックリスク例外を置くが全公開ウェイトを一律禁止しない。[米GAO 2026判断](https://www.gao.gov/products/b-337935)はAI Diffusion Ruleの不執行/正式撤回の手続きを区別。米中EUの制度は**具体的な法域と活動範囲**が違い、特定repoの将来削除日・規制確率は根拠なく設定しない。

## 3. 取得前の条件・停止境界

既存4TB予算と200GB最低空き条件、量子化済み150B超の厳格な同一HW/バックエンド/コンテキスト/バッチ・30試行以上の例外は[現行limits.json](../../policies/limits.json)に従う。今回の追加候補はいずれも新しい重みの取得承認対象になっていない。本人のGated許可、元/親モデルや声・decoderの権利、完全40文字revision、全シャードの正確なbyte/上流SHA256、OS/Python ABI/backend、量子化zero-point、KV/context/batch、実HDD/ステージング、ローカルSHA、オフライン復元の**独立ゲート**を満たすこと。

| 記号 | 意味（日本語） | 単位（SI） | 定義・値 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `P_total` | 学習済み総パラメータ | 1（無次元） | 全expert・必要学習済み部品を数える | 0以上の整数、未知ならnull | 整数 |
| `P_baseline` | 総数の通常審査基準 | 1（無次元） | 150,000,000,000 | 以上は同条件実測の量子化例外が必要 | 整数 |
| `B_repo` | 公開repo全ファイル容量 | byte | 不要な精度や画像を含む上流表示 | 未知ならnull、選択容量ではない | 整数/null |
| `B_selected` | 必須固定ファイルの増分容量 | byte | 完全SHAに結び付く必要ファイルの合計 | 今回は全件null | 整数/null |
| `B_budget` | 計画アーカイブ容量上限 | byte | 4,000,000,000,000 | 実HDDの利用可能バイトと異なる | 整数 |
| `B_floor` | 必要な物理安全空き | byte | 200,000,000,000 | cache/staging・既存保存容量を加味する | 整数 |

**次元チェック**：パラメータ数は個数（無次元）、ファイル/保存枠はbyte。量子化ファイルサイズが小さいことは全MoE学習済み総数が小さい証拠にならない。例えばARLoop 1.2087Bは150B未満のモデル総数画面審査を通過し得るが、モデルを実行する権限や安全性、必要バイトは未確定のまま。

## 4. H / T / D / C / U と次工程

- **H**：ARLoop-1.2Bの反復深さ原本とKitten MiniのCPU多言語TTSは、同系列小型版や用途重複モデルより独立研究/運用価値を合法的に低容量で保存できる可能性がある。規制確率は仮説に組み込まない。
- **T**：新規8件の一次情報/既存198件のID照合を実施。次は優先2件の固定revision、全必須shard/codec/voice、SHA256、親/LICENSE、ABIを確認。**重み実行・取得なし**。資料欠損時は逐次停止。
- **D**：PASS＝同一原本が既存に存在せず、正式ライセンス・固定byte/sha・依存・本人許諾と物理予算を満たす。FAIL＝既存原本の重複・予定用途の契約禁止・必要容量の不成立。UNCERTAIN＝今回のように固定sourceと実機/権利が未閉包。
- **C**：既存のHaru/ZONOSがKittenを完全代替、ARLoopの特殊ABIが保存可能な実装にならない、作者が別の正規同一ハッシュ配布元を用意する、Bielikへの個人許可が得られる可能性。
- **U**：公開者のパラメータ丸め、Hub update/revision変動、親依存と再配布条件、実機資源・品質評価なし。分布が未定義のため合成標準不確かさ`u_c`と拡張係数`k`は未適用。

**転用分野**：計算機アーキテクチャ（反復深さモデルの復元）、音響処理（日本語を含む小型TTS）、情報保全・ソフトウェア供給網（SHA/ABI/第三者ライセンス）、AI配布政策（モデル規制と実際の輸出・技術移転の区別）。

### ERROR CHECK

- 候補8件、v45の198正規IDと一致重複0。既存Haru/PAN2/Praxis/ZONOS/Raon/Simonsの二重登録なし。
- v45の198/151、`queues/approved.json`空を維持。**候補採用・固定lock・個別権利承認・ダウンロード/実行を一切捏造していない**。
- ARLoopソースMIT/重みApache表示、Underdog独自非商用とMimi、BielikのGated、SOV上流53.317GBと仮想容量残、tiny-voca総数不明を別々に記録。
- 8候補すべて最終SHA/完全選択byte/ハード性能・実空き不明。今回の研究成果はモデルを「正式選定済み」に書き換えない。

### 〈次に考える問い〉

**規制を予測して同系モデルを大量保管する代わりに、異なる学習済み原本と依存/runtimeのオフライン復元を検証した少数の代表モデルへ容量を集中できるか。**
