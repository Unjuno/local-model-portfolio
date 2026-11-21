# R150／2026-11-22 — 99件取得報告後の新小型原本・無検閲候補の実物調査（非実行）

**現行の正式正本は依然 `catalog/CURRENT.json` → v63・235資産／188有効（SELECT55／CONDITIONAL133）。本調査では正式選定数・既取得99件・承認キューを変更しない。** 新規追加は公開元の研究用ソース固定と採否の次期改訂案であり、今すぐ重量を取得する許可ではない。

## 1. 結論と順位

| 対象 | 今回の研究判定 | 公開元の完全ソース容量（decimal byte） | 非重複価値／反証 |
| --- | --- | ---: | --- |
| [mistralai/Timestral-5M](https://huggingface.co/mistralai/Timestral-5M/tree/bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f) | **P0／次期CONDITIONAL推奨** | **20,854,471**／6files | 5,208,960学習要素の独立事前学習版。既存Timestral-28Mを置換せず、超小型zero-shot予測を補完。 |
| [tencent/WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B/tree/821690998399cac0f55bb7f7f805ebafa650c3a4) | **P1／次期CONDITIONAL推奨** | **6,590,699,556**／27files | 動画と原音声の同時理解＋単独音声／画像／文字。MOSS-VL-Realtime等とは別の学習済み成果で、音声統合が保存価値。 |
| [abacusai/Smaug-Uncensored](https://huggingface.co/abacusai/Smaug-Uncensored/tree/e4bbcf7aec54ab72f4ce720569f3b3dc7b973087) | **研究HOLD** | 観測Hub使用容量 **55,575,816,096** | 本物のDPO後学習差分とされるが、Qwen3.8-27B本体との多量重複・追加保存費用がある。 |
| [IndrasMirror/Inkling-2-Mini-XQ-Uncensored](https://huggingface.co/IndrasMirror/Inkling-2-Mini-XQ-Uncensored/tree/629e214bd67315f6faaa45274f253f0cc6ac561b) | **研究HOLD** | 観測Hub使用容量 **15,221,549,728** | 拒否方向ARA＋XQ特殊量子化。ただし既存のInkling原本や無検閲編集との重複、専用エンジンABIと作者評価の再現性が不明。 |

**不変ソース**: [2原本33files／6,611,554,027byte](../../manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json)。[従来11件を無変更保持した次期13配布元非実行キュー](../../queues/proposed-v63-r150-after99-13-research-only.json)は、P0=5件2,255,598,751byte、P1=5件18,462,107,603byte、P2=2件54,438,018,606byte、P3=Ripple1件129,572,889,973byte（HOLD）。P0〜P2は合計**75,155,724,960byteの公開元参考値**。共有依存・既取得ファイルと突合していないので、そのまま残HDD容量から差し引くことはできない。

## 2. 本当にソースを確認した内容

### WeMM-Video-2B

- 2026-11-22にHub API 40桁revision `821690998399cac0f55bb7f7f805ebafa650c3a4`を観測。public・ungated。27filesの **パス／整数byte／Git blob SHA1** を固定し、5件のLFS SHA256と公開元 `SHA256SUMS` の**25 SHA256**を一致検証（publisher対publisher検証で、所有者媒体のSHA検証ではない）。
- BF16 `model-00001-of-00002.safetensors` **4,296,516,368byte** と `model-00002-of-00002.safetensors` **2,270,879,536byte** の合計 **6,567,395,904byte**。すべてのメタデータを含む完全repo scopeは上表の6,590,699,556byte。
- **名称の2Bを全パラメータ数だと誤認しない。** HFの重みメタデータはBF16が3,283,621,448、F32が2,304、I64が512で計3,283,624,264要素（約3.284B）。混合dtypeの単純合計であり、ローカルの完全tensor censusは未実施。
- モデルカードはTencent独自の`configuration_wemm.py`／`modeling_wemm.py`／`processing_wemm.py`等のPythonを必要とし、`trust_remote_code=True`の例を示す。**このコードを未審査で実行しない。** Publisherはpatched vLLM 0.18.0/0.31.0、patched SGLang 0.5.16/0.5.19、L20/H20での動作を記載。ユーザーのCPU/GPU・クロック・ドライバー・KV cache・画像/音声入力・バッチ・ゼロ点等は未測定。
- Apache-2.0のTencent配布条項は`LICENSE`内の**第三者コンポーネント固有の原ライセンスを除外**している。本人利用行為別確認を要する。公式論文 [Tang et al., *WeMM-Video*, arXiv:2611.26409](https://arxiv.org/abs/2611.26409) の優越主張は主として35B級・9B級の評価であり、2B級に自動転用しない。

### Timestral-5M

- Hub固定revision `bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f`、6files／20,854,471byte、F32 `model.safetensors` 20,843,960byte、LFS `7ace108c4987e7f2a99a75a445240019d1d31c2117139d1bd05ffdfd25aca738`。モデル全学習済み要素5,208,960をPublisher safetensors metadataで確認。
- 作者公開GIFT-Eval MASE（低いほど良い）は**5M 0.705、28M 0.678**。約4.0%の相対悪化を伴う、サイズ／予測精度のトレードオフ。28Mを削除・置換しない。実機CPU latencyと消費電力の優劣は未測定。
- ソース`LICENSE`は通常MITではなく**Modified MIT**。帰属義務のほか、直前月の企業／雇用主の連結グローバル月商が **2,000万USD超**の場合には当該ライセンス下の利用権がない（別商用ライセンス可能）。商用/非商用の一般論や個人・勤務先の属性を推測しない。

## 3. 無検閲2候補をなぜ即取得にしないか

**Smaug-Uncensored**: 公開元はrank16 LoRA＋DPOを本体にmergeし、1,199 tensorのうち400を変更、799はベースとbitwise同一と報告する。自己評価のOR-Bench-Hardはbenignだがリスクに見える入力1,309件、thinking-on、temperature1.0/top-p0.95、外部LLM審査器で拒否率45.2%→2.3%。独立再現ではない。55.58GBの丸ごと保存より、既取得のQwen3.8-27B親をSHA検証し、**可逆な独立変更分だけで復元可能か**を調べる。親の完全一致を検証せず「差分だけで復元可能」と断定しない。著者の安全制御解除はサービス用途で安全層を別途要求する。

**Inkling XQ**: 作者はRTX4090、Xolotl `2bd4b5d77`、2.8K入力＋256 greedy出力で113 tokens/s、DSparkで136 tokens/sと報告。MMLU 100問では元73%対XQ76%だが標本が小さく統計的優越は示せない。13.93GB GGUF＋別DSpark・mmproj、既存OpenUncensored編集と学習差分の相違が未監査。作者専用XQ変換レシピは非公開部分を含むため、現時点の適切な判断は研究HOLD。

## 4. 取得と規制の停止条件

現行`queues/approved.json`は空。99件VERIFIED／1,478files／1,879,994,309,866byteは**取得台帳の報告**であり、今回の所有者Windows D現物再SHAではない。新規sourceに関しても**重みダウンロード0、ユーザー承認0、既存削除0、未審査モデルコード実行0、Gated回避0**。

取得昇格の必須関門は (i) 著作権・LICENSE・第三者部品／勤務先月商など本人の行為別権利、(ii) immutable SHAとファイル単位範囲とローカルSHA、(iii) 親・codec・patch・実装依存の完全閉包、(iv) 実フォーマット後空き、4TB設定と最低200GB余裕＋staging、(v) 本人実機のHW/driver/backend/quant/zero-point/context/batch下での速度・品質、(vi) **明示された個別ファイルマニフェスト承認**のすべて。量子化容量とピークRAMは別指標。

**現行法の一次根拠**：米BIS [91 FR 74970 (2026-11-19), IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm) はAI Diffusion RuleのウェイトECCN4E091を撤回している。残存する仕向け・最終用途・遠隔計算・ライセンスを無視できない。「全オープンウェイトは間もなく禁止」は根拠のない予測。保存優先度は配布政策変更への**耐性シナリオ**であり、規制される確率の観測値ではない。

## 5. H／T／D／C／Uと実装・次の一手

- **H（反証可能仮説）**：固定済みのTimestral5MとWeMMは既取得99件・現行188有効モデルにない独立学習済み成果であり、2原本33ファイルの上流メタデータを完全な整合性でアーカイブ候補に追加できる。
- **T（最小検証）**：GitHub候補IDを99台帳・235現行資産とjoinし重複0、HF 40桁revision固定、33 path・整数byte・Git OID検証、WeMM 25 publisher checksum／5 LFS一致、Timestral1 LFS確認、13候補への11件不変埋込。実行価値はデータセットとHWを固定し、双方の性能を**各30件以上**の paired trial で中央値・分布・精度を測る。未計測では逐次停止を早期PASS扱いにしない。
- **D（判断）**：メタデータ整合なら **PASS（source研究のみ）**。重量やowner diskの実ハッシュ不一致・自動承認・他人権利侵害は **FAIL**。ライセンス解釈、実機性能、完全offline restore、個別取得許可は **UNCERTAIN→STOP**。
- **C（破れ方）**：5Mは28Mより単位仕事量効率が悪い可能性、WeMMはパッチ／権利が閉じない可能性、Smaugは差分再現が不完全／既存同等、XQはエンジン依存測定偏り。
- **U（不確かさ）**：PublisherのGit/sha参照とowner実体SHAの隔たり、媒体空き、GPU ABI、テンプレート更新、作者評価の標本偏り。測定系列がないため合成標準不確かさ `u_c` と包含係数 `k` は**算定不可**、架空の信頼区間を出さない。byteはdecimal（1GB=10億byte）、KiB/GiBや仮想RSSと混同しない。

関連する専門分野は、(1) 時系列予測と決定理論、(2) マルチモーダル認識とモデル学習、(3) ハッシュによるソフトウェア供給網監査、(4) 著作権・輸出管理、(5) GPUメモリ／推論実装。次の昇格の鍵は**現行モデルの差分学習成果を重複取得しないこと**と**実機計測／個別権利に偽のPASSを作らないこと**。

**ERROR CHECK**: Publisher SHA refs & bytes source-frozen、11→13件で旧11の属性は全保持、99報告済み対象の再取得なし、CURRENT v63の235件／188有効・approved0不変、所有者媒体への変更なし。実際のテストの結果は別途記録する。
