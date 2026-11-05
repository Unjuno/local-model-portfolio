# 配布制限リスクと選定の続報：2026-11-06

## 1. 結論

**全面禁止の予言ではなく、実際の配布条件の変更と、失うと再現しにくい能力に備える。** 今回は12件を重点確認し、新規能力モデル1件、学習データ2件、任意のクラウド形式1件を審査対象として提案した。105件の既存有効選定を丸ごと置き換える提案ではない。

正本はv9ではなく **v19・150資産・有効105件**。読取基準は `29529656ac9af944e37c1a803d7271d045860a44`。元戦略の基準は `6e9389c97d24528df97e4b14a6bc772780141fd3`。現在mainには150B超の条件付き例外審査規定があるが、この会話の明示条件を優先し、**本提案では総150B以上を絶対除外**する。main側の規定やCURRENT、承認キューは変更しない。

本体取得・クラウド契約・課金・モデル実行・自動監視の設定は行っていない。対象HDDの状態は不明。これは調査提案であり、取得承認でも実機検証でもない。

## 2. 現在の事実と将来予測

| 事象・発生日 | 確認した一次資料 | 結論の限界 |
|---|---|---|
| 中国CACの整治方針、2026-04-30 | [公式通知](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm)は重大リスクのある公開モデル・データセットを適切に管理・除去しない問題を対象に含める | 公開コミュニティへの管理圧力は具体的。ただし日本の個人による全公開重みの保有を一律禁止する文書ではない |
| CACの執行報告、2026-07-06 | [公式報告](https://www.cac.gov.cn/2026-07/06/c_1785081384384987.htm)は公開データセット9件の下架を報告 | 9件のモデル重み禁止ではなく、データセットの処分実績 |
| 中国商務部・科技部第48号、2026-10-16 | [公告](https://www.mofcom.gov.cn/zfxxgk/fdzdgknr/ztfl/blgg/art/2026/art_718071a95e6948cdb652e2f08f422673.html)はAI技術等の目録改訂案と暫定的な輸出前登録を示す。意見募集は11月15日まで | 既に公開・開源等で公共領域にある技術の対象外規定もある。草案の全措置が施行済み、またはすべての重み輸出が禁止済みとはしない |
| Kimi K3.1 Proの公開方針、2026-10-24の発表 | [開発者ブログ](https://www.kimi.ai/blog/kimi-k3-1-pro)は公開前に一部サイバー関連の訓練内容を調整したと説明 | 提供者の選択的な能力調整の実例。法律による全面禁止でも、未調整版が公開されている証拠でもない |
| VibeVoiceの過去の公式repo無効化、2025-09-05 | [開発者コメント](https://github.com/microsoft/VibeVoice/issues/100#issuecomment-3268563653)が想定外利用とrepo無効化を説明 | 2026-11-06の重み停止予告ではない。現在のHubモデル表示は別途確認した |

**推論：** 制限は、法律による禁止だけでなく、提供者の公開判断、Gated、地域・契約条件、コードやデータの撤回として現れ得る。これは個別の停止確率を推定したものではない。S1→S2→S3は反証可能な想定として残すが、すべての候補に同じ緊急度を与えない。

**未確認：** OrcaRouter 27Bの個別削除予定・規制期限は確認できなかった。提示されたX投稿はwebとExaで本文を取得できず、投稿の内容は判断根拠に使っていない。本人のGated承認、全150件の当日ライブ状態、完全な依存・権利は確認していない。

## 3. 選定をどう進めるか

**既存のOrca 27B原本と対応する公式Qwenを優先審査する。** 改変版だけを保存しても、変わった能力を比較できない。親モデルは最新mainで代用せず、改変時のrevisionとの対応を確認する。Gatedは実在する取得条件だが、許諾済みとも削除予定とも解釈しない。

**Interpretic v2は別目的として残す。** [作者カード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)は政治的な回答抑制の変更と、有害要求への拒否を区別している。一般的な拒否低減と同じ能力として数えない。[Q4カード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)の政治質問評価はQ4だが、一般能力と有害要求拒否の評価はBF16である。精度をまたいだ性能保証は禁止する。

**0bserverxはrepoではなく成果物の同一性を確認する。** [現行カード](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)はlegacyとRVNの併存、一部パスの修正を説明している。同じrepo IDであるだけでは、以前選んだ原本と同じとは限らない。作者が複数GPUで測定したことを、独立研究者による追試と読み替えない。

**クラウド実行形式は一つずつ検討する。** [Orca公式実装説明](https://www.orcarouter.ai/blog/qwen-uncensored-explained)にはFP8とvLLMの経路がある。BF16原本とFP8を異なる能力として数えず、FP8・NVFP4・GGUF・MLXを全収集しない。[APIと配布物の区別](https://www.orcarouter.ai/blog/uncensored-model-leaderboard)に従い、クラウドAPIが使えることを保存したファイルと同一revisionの実行証拠にもしない。クラウドの利用規約・地域・費用、backendの版、GPU、KV、context、batch、量子化、ABIは別審査である。

**新規能力候補：Nemotron-Cascade 2。** [モデル](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B)は総約31.6BのMoEで、3Bは活性数の呼称。[原論文 arXiv:2603.19220v2](https://arxiv.org/abs/2603.19220v2)はCascade RLと多領域on-policy蒸留を説明する。数学・競技プログラミングの後学習成果を保存する候補として条件付き提案する。ただし作者表では一般知識、多言語、複数のエージェント課題でQwen3.5-35B-A3Bに劣る。万能な置換モデルでも、独立検証済みの最良モデルでもない。2026年3月公開であり、今週の新発売ではない。

**重みと学習来歴を分けて審査する。** [公式コレクション](https://huggingface.co/collections/nvidia/nemotron-cascade-2)でSFTとRLデータの存在を確認した。既存データとの重複、素材の権利、必要subsetの容量が未確定のため2件は研究候補に留める。全データの一括取得や完全な訓練再現性は承認しない。

## 4. 重点12件の判断表

全件の確認日は2026-11-06。以下のアクセスは公開メタデータの観測で、本人許諾ではない。優先順位は調査順であり取得順ではない。数値は総パラメータの概数・一次スクリーニングで、完全テンソル監査ではない。各行の完全な反証条件・否定的根拠は提案JSONに格納した。

| 調査順 | repo ID・一次URL | 確認済み配布表示／ライセンス表示 | 想定 | 独自性と判断 | 反証・再評価条件 | 未解決事項 |
|---|---|---|---|---|---|---|
| 1 | [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | gated / apache-2.0 | S1（仮説） | RETAIN_PRIORITY_REVIEW：拒否機構比較用の改変原本。公式Qwenと対にする。無検閲という名称自体は品質証拠にしない。 | 固定版の一般品質で重大な劣化、または合法な同一原本の再取得経路と再構成手順が実証されれば優先度を下げる。 | 個別の削除予告は未確認。現在Gated。本人許諾は未確認。作者の研究限定説明とLICENSE正文の関係を精査。 |
| 2 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | public_listing / apache-2.0 | S2（仮説） | RETAIN_PAIRED_CONTROL：改変版の品質・過剰拒否を比較する対照原本。最新mainではなく改変元と対応する版が必要。 | 改変元revisionとの対応が立証されない限り対照実験を開始しない。 | 当日Hub更新日は2026-11-05。既存派生と同じ親revisionか不明。ModelScopeの存在と同一ハッシュは別問題。 |
| 3 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | public_listing / apache-2.0 | S1（仮説） | RETAIN_DISTINCT_PURPOSE：政治的な回答抑制の変更を調べる別目的。一般的な有害要求への拒否低減モデルと同一視しない。 | 未見の日本語・中国語質問と同一精度の対照で改善せず、または事実誤答が増えるなら優先度を下げる。 | Q4の政治質問評価は作者報告。一般能力と有害要求拒否の結果はBF16でありQ4へ移せない。 |
| 4 | [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | public_listing / apache-2.0 | S1（仮説） | VERIFY_EXISTING_FILE_IDENTITY：Orcaとは異なる改変の研究対象。ただし同じrepo内でlegacyとRVNが併存し、ファイル名だけで同一原本とはできない。 | 既存候補が旧版のままなら同一性を再審査。一般品質と差別化が再現しなければ比較対象を絞る。 | 作者は旧ファイル維持と一部パスの修正を説明。複数GPUでの作者測定を独立研究者の追試と扱わない。 |
| 5 | [orcarouter/Qwen3.8-27B-Uncensored-FP8](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8) | gated / apache-2.0 | S1（仮説） | OPTIONAL_CLOUD_FORMAT：既存Orca原本のクラウド実行形式候補。新しい能力資産として二重計上しない。 | 予定クラウドの固定backendで一般品質・費用・メモリ上の利点が確認できなければ原本のみを保存候補とする。 | 作者はvLLM/H100・H200経路を公開。約30.9GBは公開時の概数で最終取得bytesではない。こちらでは未実行。 |
| 6 | [orcarouter/Qwen3.8-27B-Uncensored-NVFP4](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-NVFP4) | gated / apache-2.0 | S1（仮説） | DEFER_DUPLICATE_FORMAT：同一改変系列の別形式。FP8・GGUFと同時に追加する独自能力の根拠は不足。 | 対応GPU・backendの固定条件で品質非劣性と実用的な節約が示された場合のみ実行形式を再検討する。 | Hubの21.2321B表示と親27.7814Bが不一致。量子化によるパラメータ削減とは認定しない。packing等の原因は未検証。 |
| 7 | [microsoft/VibeVoice-1.5B](https://huggingface.co/microsoft/VibeVoice-1.5B) | public_listing / mit | S1（仮説） | RETAIN_DEPENDENCY_PRESERVATION：長時間・複数話者音声の既存選定。過去の公式repo無効化を踏まえ、権利確認済み実行コード・音声部品も一体で評価する。 | 正規の完全実行依存が安定配布され、別の既存TTSが目的を満たすなら緊急度を下げる。 | 2025-09-05のrepo無効化は開発者コメントで確認。現在の重み停止予告ではない。1.5Bは全体総数ではなくHubでは約2.704B。 |
| 8 | [nvidia/Nemotron-Cascade-2-30B-A3B](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B) | public_listing / nvidia-open-model-license | S2（仮説） | NEW_CONDITIONAL_RESEARCH：Cascade RLと多領域on-policy蒸留による独立した後学習。数学・競技プログラミングの比較原本として追加提案。 | 現行候補との未見問題・同一推論予算の比較で補完価値がなければ不採用。公開停止の証拠がないため緊急救出扱いしない。 | 2026-03公開であり今週の新発売ではない。作者評価では一般知識・多言語・一部エージェント課題に劣る。独立追試なし。 |
| 9 | [nvidia/Nemotron-Cascade-2-SFT-Data](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) | public_listing / other | S3（仮説） | DATASET_RESEARCH_ONLY：Cascade2の後学習データ。重みだけでは残せない学習来歴の検証に役立つ候補。 | 既存保存予定データと完全重複、または個別保存の適法な根拠を確保できなければ対象subsetを縮小・除外する。 | 複数出典・生成モデルが混在。個別権利、既存学習データとの重複、必要subset、bytesは未確定。 |
| 10 | [nvidia/Nemotron-Cascade-2-RL-data](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) | public_listing / odc-by | S3（仮説） | DATASET_RESEARCH_ONLY：RL・蒸留・指示追従の学習構成を残す候補。公開されたデータだけで全訓練が再現できるとは断定しない。 | 実行環境や必要データが欠けて比較に利用できない場合、メタデータ保全に限定する。 | ライセンス本文・元データ・環境依存・subset別容量・重複は未確定。自動一括保存しない。 |
| 11 | [orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) | gated / apache-2.0 | S1（仮説） | EXCLUDE_SCOPE_GE150B：今回の150B絶対除外条件により重み候補から除外。量子化やクラウド実行は例外にしない。 | 全学習済み部品を含む公式総数が150B未満と訂正・検証された場合以外は除外を維持する。 | 全expert等を含む総数約180B。上流・派生ライセンス整合性は別問題として残る。 |
| 12 | [moonshotai/Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) | public_listing / other | S2（仮説） | EXCLUDE_SCOPE_GE150B：3T級で対象外。公開前の能力調整という政策事例として資料のみ参照する。 | 別の150B未満の正規公開モデルが出た場合は別repoとして審査し、この巨大モデルの例外にはしない。 | 作者は公開前のサイバー関連訓練内容調整を説明。未調整版が一般公開されたことは未確認。 |

**共通の未解決ゲート：** 本人の正規アクセス許諾、LICENSE正文と親・派生条件の整合、固定revision、選択ファイルの整数bytes・SHA-256、依存コードと学習済み部品、HDD実空き、必要な実行資源、取得に対する個別承認。代替元は全12件で同一revision・全ファイルSHA-256が一致する正規配布先としては未立証。別モデル、API、第三者ミラーの存在だけでは代替完了としない。

## 5. パラメータ・実装前提

| 記号 | 意味 | 単位 | 定義 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| P_total | 元モデルの総学習済みパラメータ | 1（無次元の個数） | 休止expert、embedding、MTP等も数える | 非負整数または未確認。量子化のpacked要素数で代用しない | 整数スカラー／欠測 |
| P_cap | 今回の絶対除外境界 | 1 | 150,000,000,000個 | 境界値を含めて除外 | 整数スカラー |
| B_selected | 最終選択するファイルの容量 | byte（SI外の情報量単位） | 固定ファイル一覧の整数bytes | 今回は未確定。repo全体表示とは異なる | 整数スカラー／欠測 |
| M_peak | 推論時ピークメモリ | byte | OS・runtime・重み・KV・作業領域 | GPU/CPU、backend、量子化、zero-point、ABI、batch、contextを固定して評価 | 数値スカラー／欠測 |
| R | 調査順 | 1 | 本報告の1～12 | 取得許可や規制確率ではない | 順序整数 |

**単位チェック：** 180B個のパラメータと150B個の境界は比較できる。30.9GBという重み容量をパラメータ数や必要VRAMそのものとして比較してはいけない。VibeVoiceの名称1.5BとHub全体表示約2.704Bは区別する。NVFP4のHub表示21.2321Bを、親27.7814Bから構造的に縮小した証拠として扱わない。差の原因は未検証である。

## 6. 最小検証と停止条件

H：既存候補と同一条件で比較したとき、新規Cascade2は数学・コードの少なくとも一つの目的で補完価値を持つ。Orcaの別形式は、同じ能力を保存するコストまたは実行互換性に検証可能な利点を持つ。いずれも未検証仮説。

T：権利・固定版の審査後、未見の通常課題と指示追従を各200件以上、実行資源測定を固定条件で30反復する設計。日本語を含め、原本と量子化版の評価を分ける。研究用の外部コードやモデル出力を自動実行しない。現段階でこの実験を実施していない。

D：PASSは事前に固定した品質・資源基準を満たし、権利とmanifestが揃った場合のみ。FAILは重大な品質劣化、無価値な重複、150B以上、または許されない取得。UNCERTAINは総数・権利・版・評価の不足。総数不明なら取得準備を止め、公開仕様の調査に留める。成功らしい中間結果だけで逐次停止しない。

C：拒否率の低下は知識・正確性の改善ではない。クラウドのAPIサービスは同じ重みの実行証拠とは限らない。新しい形式は新しい能力とは限らない。取り下げが起きても法令以外の原因を区別する。

U：主な不確かさは作者評価、基準モデルの異なる版、量子化、観測日の差、未確認の本人許諾と依存。規制確率を数値化していない。合成標準不確かさu_cと包含係数kは、本件の定性的な政策予測に計測モデルがないため数値未設定。

学際的な転用は、法学・技術ガバナンス（何が禁止・契約条件か）、機械学習評価（能力の差の再現）、ソフトウェア供給網（版・コード・依存の保存）、アーカイブ設計（重複排除と増分容量）の4分野で行う。

## 7. ERROR CHECKと実施範囲

JSONをローカルで解析し、12件の一意ID、総数境界、追加モデル1件・データ調査2件・除外2件・承認0件を検査した。これは選定提案の整合性検査であって、モデルの安全性・速度・法的権利のPASSではない。全150件の当日ライブ監査は未実施。

GitHubの現行CURRENT、有効候補キュー、R26、選定プロトコルを参照した。Nemotron-Cascadeの既存記録はGitHub検索では見つからなかったが、全履歴の拒否理由を網羅したとは主張しない。学習データ2件は審査のみで、元データを収集していない。成果物は専用ブランチへの追記用であり、既存の2つのv9報告を上書きしない。

## 次に考える問い

保存対象を増やすより先に、どの独立した能力について「正規に取得できる固定版・必要コード・依存・評価結果」の一組を完成させるべきか。
