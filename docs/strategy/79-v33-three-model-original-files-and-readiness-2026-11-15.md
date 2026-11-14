# R79｜v33追加3モデルの公開元ファイル原本・候補44ファイル・全138件レディネス統合

監査日：2026-11-15。対象：`main`の正式v33（185資産、138有効）。**追加取得承認・モデルダウンロード・実行・Gated同意は0件**。モデルカードの表示だけでなく、配布元の**固定revisionの完全ファイル一覧、byte数、LFS SHA256、config、独自学習済み部品**を確認した。

証拠：[一次モデルファイルの一覧](../../catalog/research/2026-11-15-v33-llmon-decider-immutable-file-audit.json)／[3モデル44ファイルの非実行候補](../../manifests/drafts/v33-three-trained-state-source-scopes.candidate.json)／[有効138件の取得前条件](../../catalog/readiness/v33-2026-11-15-r79-all138-selection-gates.json)。旧v32のR64、R73、R74は当時の135件についての履歴であり、v33現行版の全件証明と混同しない。

## 1.〈本論〉— 実際のファイル構成と独自性

| 資産 | 固定配布元revision | 公開元ファイル数 | 公開元ファイルの総byte | 判定・固有学習成果 |
|---|---|---:|---:|---|
| [IBM Granite4.1-3B-LLMON](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview) | `55a14cac002854bb64c7f465c30da29209b170c8` | 8 | **7,326,711,067** | CONDITIONAL。LLMONの命令・データ境界を学習 |
| [Perplexity Decider Flash v1.3](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3) | `d06fb3f2d97e0a52325a0d463c450cf0338f44fe` | 29 | **9,626,212,554** | CONDITIONAL。専用確率判定ヘッド、Locate追加学習 |
| [NVIDIA Kumo Relational](https://huggingface.co/nvidia/Kumo-Relational) | `efdbb110daea5aae123447864a64612e8a3dc6be` | 7 | **243,656,960** | CONDITIONAL研究専用。関係表の分類・回帰、総パラメータ未確定 |
| **新規3件合計** | | **44** | **17,196,580,581** | 元データの公開元scope。全依存・HDD実測ではない |

IBMの`model.safetensors`は**7,319,517,272 byte**、公開元SHA256は`1b3bca7852237cd0d23d0b71c3e809231568425f66ce4005b3cdad1e992af3dc`。[固定重み](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview/blob/55a14cac002854bb64c7f465c30da29209b170c8/model.safetensors)。実際の40層・hidden2560の別SFT成果であり、通常chat用モデルとは異なるchat_template・LLMON構造化が必要。モデル配布repoには専用LICENSEファイルがなく、公開カード上のApache-2.0タグを本人の利用許可確認と同一視しない。

Perplexityの5種類の**学習済み**重量ファイルは、主重み2分割、255種類の判断readout、Locate adapter、Locate head。公開元SHAは以下を固定。[主重み1](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/model-00001-of-00002.safetensors) `0048d1ddf2c5754fc05540fccdbc4ac50407e5cf14a35326be01cac0756b4de6`。[主重み2](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/model-00002-of-00002.safetensors) `40e0c0ccb3248a59db0724ffd1ad1c81fc935d9f474e6fd52e9df32af4690608`。[readout](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/readout.safetensors) `46358a2e2639f1956561687ba261dd9b37506f878e90eb5eabc15f114532bec3`。量子化複製と異なり、専用コードの**非因果full-attention＋質問ごとの判定位置**が不可欠。

Kumoの`classifier.pt`と`regressor.pt`は別タスクの学習済み重みで、2重の同一量子化ではない。ただし`.pt`は未監査のpickleを含む可能性があるため、**本体デシリアライズ禁止・総数未確定による最終取得ロック停止**。前段の[一次調査](../../catalog/proposals/07-rare-specialist-2026-11-15.json)を再利用し、同じrepoを再取得したとは主張しない。

### 配布元内部マニフェストの不一致：Perplexity

固定revisionの[公式Hub API](https://huggingface.co/api/models/perplexity-ai/pplx-decider-flash-v1.3/revision/d06fb3f2d97e0a52325a0d463c450cf0338f44fe?blobs=true)は**`private:false`、`gated:false`、29ファイル**と応答した。しかし同じrevisionの[配布者作成のrelease-manifest.json](https://huggingface.co/perplexity-ai/pplx-decider-flash-v1.3/blob/d06fb3f2d97e0a52325a0d463c450cf0338f44fe/release-manifest.json)には**`private:true`、27ファイル**と記載される。差分は`.gitattributes`と`release-manifest.json`の自己登録漏れ、さらにNOTICEがmanifest127/Hub API132 byte、READMEが12024/12031 byte。主重み2シャードと専用headの公開元SHA256には矛盾なし。

この差は、**作者が残した内部マニフェストだけで現行のアクセス制御状態を断定してはいけない**という実例。現在の公開APIがungatedと応答しても、所有者個人の合法利用許諾・ライセンス全文・ファイル現物のハッシュは**別途確認**する。正式v33のCONDITIONAL研究選定は維持し、取得承認に昇格しない。

## 2.〈応用・転用例〉— 完成に向けた更新後の状態

[R79全138件台帳](../../catalog/readiness/v33-2026-11-15-r79-all138-selection-gates.json)は旧135件をその時点の根拠のまま保持し、新3件の**全44公開元ファイル・revision・許諾/依存の不足**を追加。全資産は一意で、取得承認とオフライン復元合格は0。**総パラメータ未確定の有効モデルは旧7件＋Kumo1件＝8件**。個別Gatedの旧v32観測17件は引き継ぐが、Perplexityの旧内部privateフラグを「新たなGated1件」とは数えない。

同族大型版を余分に追加せず、IBM LLMON 8B／Perplexity Decider 26B／Duoの全依存未閉包版は非採用のまま。既存Galvanize、Kanana、Chronos、TTMを優劣未実証で削除しない。既存の公開元SHA再利用効果を全資産でローカル実測したとは主張しない。

### 変数表

| 変数 | 意味（日本語） | SI単位 | 定義 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `B_{32}` | v32のSHA調整済み参考source | byte | 3,466,070,232,173 | 完全アーカイブではない、非負 | 整数スカラー |
| `B_{33,new}` | v33の新3モデルの公開元ファイル和 | byte | 17,196,580,581 | 未重複排除、外部実行依存除外 | 整数スカラー |
| `B_{scenario}` | v33の参考source合計 | byte | `B_{32}+B_{33,new}=3,483,266,812,754` | 参考算術、非負 | 整数スカラー |
| `C` | 計画保存上限 | byte | 4,000,000,000,000 | 実HDD測定値ではない | 整数スカラー |
| `F` | 実空き床 | byte | 200,000,000,000 | 計画条件 | 整数スカラー |
| `N` | 有効選定資産数 | 1（個） | 138 | v33現行正本 | 整数スカラー |

**次元チェック**：source容量3量と`C,F`はすべてbyteで算術可能。仮の`C−F−B_{scenario}=316,733,187,246 byte`は**ユーザーHDDの実際の残量ではない**。パラメータ数も別の無次元数であり、byteへ直接換算しない。

**H/T/D/C/U**：H＝新3モデルは既存と同一でない学習済み表現を持つ。T＝固定revision3・公開元ファイル44を全件（`n_min=44`）照合し、失敗時は取得STOP。D＝ファイルscopeの同一性・採否の研究判定はPASS、法的許諾／全依存／端末復元はUNCERTAIN、権利不足やSHA不一致ならFAIL。C＝LLMONの実効果が外形フォーマットだけ、DeciderのLocateが他の既存モデルで同品質代替できる、Kumoの片方が同一重みという対立仮説。U＝公開元revision変化、Hub内のprivateフラグ相違、必要wheel/ABI、実機、許諾。不確かさの分布がないため合成`u_c`と係数`k`は算定しない。

**ERROR CHECK**：モデル3／44ファイル／17,196,580,581byte、旧135＋新3＝138、一意ID、Kumoの総数未確定、承認0、実体DL0、オフライン復元PASS0。

## 3.〈次に考える問い〉

**Kumoの全学習済みパラメータ総数と、Deciderの非因果専用runtimeを、モデルを実行せず安全に固定するには何が不足しているか。**
