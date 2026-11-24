# R163／v71（2026-11-25）— 無検閲・独立編集原本2系統のPublisher全ファイルSHA確定と210件取得STOP

## 1.〈本論〉正本の変化と保存目的

従前の唯一の正本 **v70（258登録、208有効、SELECT56／CONDITIONAL152、HOLD31）** の全258行を不変のまま、[v71正式overlay](../../catalog/revisions/v71-2026-11-25.json)で2モデルを追加し、**v71-20261125（260登録、210有効、SELECT56／CONDITIONAL154、HOLD31）**に進める。新たな重みペイロードの取得や本人のライセンス行為許諾が成立したという意味ではなく、**研究上のCONDITIONAL正式選定**である。

目的は、既取得116報告と既選定258資産を重複取得せず、将来の公開終了・利用条件変更に備えて**独立した編集済み学習済み原本を完全に同定**し、オフラインで復元できる素材・実装依存を研究管理すること。公開終了・規制発生の具体的確率や期限を実証したものではない。

一次根拠・コミット済み実物：

- [全5Publisher固定リビジョン／66ファイルのpath・整数bytes・Git blob SHA1・LFS SHA256](../../manifests/drafts/r163-2026-11-25-five-uncensored-source-complete-publisher-OID-SHA.candidate.json)（公開元APIの**メタデータのみ**。重みの本人ダウンロード・実物SHA再検証ではない）
- [正式CONDITIONAL選定の2資産追加](../../catalog/revisions/v71-2026-11-25.json)、[既存258を不変とした派生260資産](../../catalog/effective-portfolio-2026-11-25-v71.json)
- [全210 STOP](../../catalog/readiness/v71-2026-11-25-r163-all210-gates.json)、[全210 research queue](../../queues/proposed-v71-2026-11-25.json)、[154 conditional rights](../../catalog/access/2026-11-25-v71-conditional-hub-gates.json)、[210 dependency bundles](../../catalog/preparation/2026-11-25-insurance-bundles-v71.json)
- [次の新2件だけの未承認レビュー](../../queues/proposed-v71-r163-next2-uncensored-full-source-UNAPPROVED.json)、[正式決定](../../catalog/decisions/2026-11-25-r163-v71-source-complete-uncensored-and-decision.json)、[オフライン回帰試験](../../tests/test_r163_v71_complete_uncensored_source_and_all210_stops.py)

従前[R162の5repo調査](162-v68-post116-uncensored-vision-and-decision-originals-no-approval.md)で未完成だった**全非重みファイルの個別Git OID／byteの凍結**を今回完了した。旧R162は当時の「未完成」履歴として残し、現行の根拠はR163に切り替える。

## 2. 研究で確定した2つの別編集学習済み原本

| 完全Publisher原本と固定SHA | 公開元ファイル | 個別重量SHA、学習済み改変の意味 |
|---|---:|---|
| [2Beyes/Aurum-2B-Uncensored](https://huggingface.co/2Beyes/Aurum-2B-Uncensored/tree/56c735e8dc8efb82d81ad8db95e9eefb2ae7129d) | **23 file、4,572,557,909byte、LFS6 SHA参照** | BF16`model.safetensors-00001-of-00001.safetensors`は**4,548,221,520byte**、Publisher SHA256`54b60b4e66348f40d9672dbd245407d85a19189e586aab5b06cb635304371c1c`。Qwen3.5-2Bの41テンソル拒否方向を編集した独立パラメータ状態。編集は**追加勾配学習と同義ではない**。画像/動画前処理、tokenizer、chat_template、Model Index、LICENSE、build_logを含めて固定。 |
| [AnkitNayak-dev/QJev-1.5B-Abliterated](https://huggingface.co/AnkitNayak-dev/QJev-1.5B-Abliterated/tree/1df03fe639898580f53a984355b7cbf3cca24bf4) | **15 file、3,102,137,211byte、LFS3 SHA参照** | 編集済みBF16`model.safetensors` **3,087,467,144byte**／SHA`5272c8590c74528d5f8604a6a058ddc6a8908089bfb92c010fd73fabd36c796e`と、学習済み`decision_head.safetensors` **3,183,276byte**／SHA`ec01a57a7e61c3ee052a5b7ea939cb4e5ae2cfacf2fe84f5e1d67d962805bebe`。別の非生成選択肢確率判定器。 `decision_config.json`・`qjev.py`・`handler.py`・`serve.py`を**任意コードの実行なしで静的源として保全**。 |

両者の公開元全原本計**38ファイル、7,674,695,120byte、LFS SHA参照9件**、学習済み重み3件の総byte数は**7,638,871,940byte**。この正確なSourceのバイト数は**Owner HDDで追加消費する容量を測定したものではない**。ローカル重複排除、staging/cache、既取得parent/Tokenizerの物理的存在は今回未確認。

**編集品質の負面を保存判断に必ず入れる**：
- Aurum作者の拒否0/1,113問はモデル側手動・親側自動という判定系の相違あり。**BFCL「適用可能なツールなし」への対応は親87.9→Aurum62.5と悪化**。長文GPQAの回答予算切れ増加や画像数学の負面を作者自身が記載している。拒否率改善≠一般品質改善。作者の111tokens/sは**RX6600 8GB、Vulkan、llama.cpp build 12289、Q4_K_M**であり、owner BF16の性能と同一視しない。
- QJev通常版との比較では、**本体重量SHAは異なるがdecision_headのSHAは同一**。教師あり学習ヘッドが同じでも入力隠れ表現が編集によって変わるので、**確率校正・順位・信頼度が不変とは証明できない**。作者のJevBench62.53%（240評価例・1468試行、strict tolerance0.05）や約31msはowner独立測定でなく、危険なサイバー・産業制御の自律実行に使える証明ではない。

オリジナルの完全weight状態は独立であり、元のQwen3.5/Qwen2.5や他のHeretic派生と同一のGGUF変換ではない。他方、*量子化だけ*の別形式は独立資産と数えない。既存v68のIvonnet/IVEの**画像判定機能**もQJevの選択肢確率・校正インターフェイスとは同義ではない。

## 3. 2系統保留・重みゼロ排除

| 原本 | Publisher確認scope | 処置 |
|---|---:|---|
| [OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated](https://huggingface.co/OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated/tree/266067bc254dbf72d76154016023d1687cc0e3d5) | 11file／**4,593,269,888byte**、LFS2 | HOLD。編集本体SHAは既取得報告済みMicrosoft Aionと異なる。著者拒否5/100とKL定性的「very low」は独立比較証拠に乏しく、別4.593GBの機能増分要再検証。 |
| [MC7ever/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16-heretic](https://huggingface.co/MC7ever/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16-heretic/tree/9a9220a20924249e07d782fc0cd912345858728e) | 16file／**7,968,035,453byte**、LFS3 | HOLD。OpenMDW v1.1モデル利用権・専用looped推論器、KV-cacheの`last_loop`／`per_loop`の意味、vLLM/llama.cpp PR依存・owner再生環境を閉包できていない。 |
| [electroglyph/Spark-X2.6-4B-uncensored-experimental-LoRA](https://huggingface.co/electroglyph/Spark-X2.6-4B-uncensored-experimental-LoRA/tree/82fd1a8d83837c35164c958404dce198bf43fe94) | 1file／**1,519byte**、LFS0 | REJECT。publisher Gitツリーに`.gitattributes`のみで、`adapter_model.safetensors`等の学習済みファイルが無い。「LoRA」の名前のみでは保存可能な学習成果は存在しない。 |

5Publisher固定原本全66files／20,236,001,980byte・LFS14参照を資料化。ただし正式選定を変更したのはP0/P1の2件だけで、Aion/Dory/Sparkをv71正式資産に追加していない。

## 4. ゲート・正確な実装前提

新2資産はpublic ungatedと観測されたが、Apache-2.0タグ/LICENSEが存在するだけで本人のすべての行為を許諾済みと見なさない。個別の改変、転載/商用提供、学習元・出力・データ/コードのNOTICEを審査する。

- **Aurum**：Qwen3.5向けTransformersの`AutoModelForImageTextToText`、PyTorch、BF16、`AutoProcessor`、vision/video config、長文262144文脈のKV容量、CPU/GPUとOSのABIを固定。作者のQ4_K_M測定速度をBF16原本の速度へ外挿しない。
- **QJev**：PyTorch/Transformers・決定専用MLP・`qjev.py`/handler/serveのカスタムコード、`decision_config.json`、readoutとtokenizerを全て固定。任意Pythonコードをサンドボックスなしで実行しない。高リスクなネットワーク操作・工業制御・医療判断にモデルを自律接続しない。
- **物理保存**：最大4TB（十進）計画上限、現物HDD残床200GB（十進）以上、staging/cache、完全オフライン再現に必要なwheelhouseとcodec、全ファイル現物SHA256を本人環境で読取専用検証。取得レシート116VERIFIEDは別セッションの過去取得器の報告。
- **権限**：ファイル単位のmanifest/権利/リソースを確認したうえでユーザーが**明示的に承認**するまで`queues/approved.json`空、全210のreadinessは`ready_to_acquire=false`で維持。公開元全ファイルの個別SHA固定は取得権限を生成しない。

法律事実と予測を区別：米BISの[2026-11-19 Federal Register](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)が旧AI Diffusion RuleのECCN4E091を撤回。これをもって輸出用途制限・公開元のLICENSE制限が全消滅したとはいえない。「近い将来一律にローカルモデル所持が禁止」とする規制日程や確率を捏造しない。

## 5. 変数表／計算／次元検査

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 範囲／前提 | 型 |
|---|---|---|---|---|---|
| `B_A` | Aurum publisher原本参照byte | byte (B) | 4,572,557,909 | 全23file、Owner増分ではない | 非負整数スカラー |
| `B_Q` | QJev publisher原本参照byte | byte (B) | 3,102,137,211 | 全15file、Owner増分ではない | 非負整数スカラー |
| `B_new` | 追加2原本の論理参照総量 | byte (B) | `B_A+B_Q` | 重複排除前の公開元scope | 非負整数スカラー |
| `B_weight` | 両原本の重み3ファイル合計 | byte (B) | 7,638,871,940 | Publisher LFS参照 | 非負整数スカラー |
| `B_aux` | 非重量35ファイルの参照bytes | byte (B) | `B_new-B_weight` | 元ファイル別Git OID固定済み | 非負整数スカラー |
| `D_free` | 所有者の現在保存先空き | byte (B) | null | 0以上、未測定 | 非負整数／null |
| `D_floor` | 保持すべき最低空き | byte (B) | 200,000,000,000 | staging/cache込み | 非負整数スカラー |
| `M_peak` | 実機推論GPU+CPU構成のピークメモリ | byte (B) | null | HW/quant/zero-point/context/batch依存、未測定 | 非負実数／null |
| `n` | 同条件計測反復数 | 1（無次元） | 最小30回を計画 | 今回実機実行0 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 測定量の単位 | 独立誤差源の合成 | 実測なし未算定 | 非負実数／null |
| `k` | 包含係数 | 1（無次元） | 区間の拡大係数 | 分布・被覆率未定 | 正実数／null |

算術は整数のまま実施：
`B_new = 4,572,557,909 + 3,102,137,211 = 7,674,695,120 byte`。
`B_aux = 7,674,695,120 - 7,638,871,940 = 35,823,180 byte`。

**次元検査**：全加算・減算の項の単位はbyteで一致。publisherファイルbyteとVRAMピークや学習パラメータ要素数（無次元個数）の混同を禁止。リポジトリの差分はユーザー媒体への実書込み量ではない。

## 6. H／T／D／C／UとERROR CHECK

- **H**：訓練不要の拒否方向モデル編集による独立パラメータ状態が、既存v70の一般モデル・微小LoRAとは異なる研究保存価値を与える。拒否率低下は品質改善の証明ではない。
- **T**：公開元5repo、66ファイル全パスの整数byte/Git OID/LFS SHAを一致させ、追加2repo全38file・9LFS SHAを照合。v70旧258行完全不変、新v71 260登録/210有効/154CONDITIONAL、全210 STOP、承認0を静的回帰試験。将来の本人実機評価は100以上のholdout合法課題、各モデル30反復以上、HW/driver/clock/backend/quant scale・zero-point/context/batch固定、精度・拒否・ツール不必要時の過剰呼出し・decision ECE/確信度の95%CIを記録する。
- **D**：公開元identity完全凍結・重複なし・203+2 STOPなら**STATIC PASS**。品質優位、Owner権利・実媒体SHA・実空き/staging・依存コード閉包・復元は現時点 **UNCERTAIN→取得STOP**。無承認の重み転送／未審査コード起動／状態IDの二重取得は**FAIL**。
- **C**：AurumのTool abstentionが既存編集モデルより悪い、QJevの同一readoutが編集後表現に対して確率校正を失う、公開源に訓練基底や権利の不整合、CPU/GPU backendが非互換。
- **U**：出版社試験の評価バイアス、コード供給安全性、owner独立SHA・実測電力/clock、学習データ重複、licenseの本人行為適用。実機統計系列がないので合成標準不確かさ`u_c`と係数`k`は数字にできない。

**ERROR CHECK**：旧258同一、現260/210/154、追加2repo 38 file／7,674,695,120byte／9 LFS参照、5repo原本66files・LFS14参照、取得報告116モデル重複なし。承認0／重量DL0／ユーザー物理ドライブ変更0／未審査コード実行0。

学際性：**①モデルの重み編集・表現幾何、②確率校正と意思決定、③マルチモーダルモデル/ツールの信頼性、④暗号学的ハッシュと再現可能なデジタル保存、⑤GPU実装・量子化/ABI、⑥輸出管理・知財とAI倫理**。

## 7.〈次に考える問い〉

**Aurumによる低拒否率とBFCLのツール不必要時の不正確な選択増加をどの尺度で評価し、QJevのECE校正破壊が独立測定で判明した場合にどのモデルを優先保全するべきか。**
