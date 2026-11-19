# R128｜v54 160有効資産の次回原本選定・OrcaRouter規制リスク再評価（2026-11-20）

## 1.〈本論〉
正本 `main` `e31ba6c48658b95e72682c1ca89d57620651b824` はv54・207登録／160有効（181モデル／26データセット）。取得実行ledgerは61モデル／708ファイル／409,835,119,252byteのVERIFIEDを報告するが、今回Windows Dの現物を独立に再hashしていない。全160 readinessはSTOP、`queues/approved.json`は0件。**研究上の選定とダウンロード許可は別**。

## 2. 独立学習済み原本の次の優先順位

| 優先 | モデル・一次URL | 研究source bytes | 判定 |
|---:|---|---:|---|
| 1 | [`Reson8/Rumble-2-Flash`](https://huggingface.co/Reson8/Rumble-2-Flash) | 1,385,998,807 | SOURCE_PINNED_OWNER_PREFLIGHT |
| 2 | [`microsoft/Aion-1.0-Instruct-2.3B`](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B) | 4,593,276,272 | SOURCE_PINNED_CUSTOM_CODE_ABI_HOLD |
| 3 | [`harness-hub/Qwen3.8-27B-pi-adapted`](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) | 657,633,248 | PARENT_TRAINING_REVISION_HOLD |
| 4 | [`fudan-generative-ai/Qwen3.8-27B-REMORY-1.9B`](https://huggingface.co/fudan-generative-ai/Qwen3.8-27B-REMORY-1.9B) | 8,023,113,280 | PARENT_ABI_HOLD |
| 5 | [`RadixArk/DaisyRose-27B`](https://huggingface.co/RadixArk/DaisyRose-27B) | 55,586,309,473 | SOURCE_PINNED_LARGE_BYTES_PREFLIGHT |
| 6 | [`InterpreticAI/Qwen3.8-27B-Uncensored-v2`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | 55,586,056,799 | SOURCE_PINNED_NOT_PREVIOUS_Q4 |
| 7 | [`orcarouter/LFM3-1.7B-abliterated`](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated) | 未固定 | GATED_LICENSE_HOLD |
| 8 | [`orcarouter/Nex-N2.5-mini-Uncensored`](https://huggingface.co/orcarouter/Nex-N2.5-mini-Uncensored) | 未固定 | GATED_RIGHTS_HOLD |
| 9 | [`Zyphra/ZONOS3-Mini`](https://huggingface.co/Zyphra/ZONOS3-Mini) | 15,345,816,226 | DIFFERENT_SCOPE_REHASH_FIRST |
| 10 | [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 53,808,326,934 | DIFFERENT_SCOPE_REHASH_FIRST |

RumbleのCTC head、AIONの小型Windows向け原本、pi RL LoRA、REMORY残差記憶器は、単純な量子化複製と異なる学習成果を少ない追加容量で確保するための上位候補。AIONの`custom_code`、REMORYのSGLang/CUDA依存、pi adapterの訓練時親revisionは未閉包。REMORYは作者の元親revisionと比較版で18重量shardが同一とする一次照合があるが、**所有者の実HDDにその親があると確認したわけではない**。

Interpretic v2 BF16と0bserverx RVN F16は無検閲高精度原本として残す。ただし旧Q4の取得報告を高精度原本の保存完了と誤認しない。ZONOSの旧775,728,152byteと新15,345,816,226byte、RVN旧17,176,692,278byteと新53,808,326,934byteの差は**単純なsource集合の差**で、実際の追加転送byteではない。重複ファイルをSHAで調べてから判断。

## 3. 小型無検閲モデルと政策の観測事実

[OrcaRouter LFM3-1.7B Abliterated](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated)はHF一次メタデータで1,728.8M、Gated、license:other、custom_code。小型で独自の安全制御変更済み重みを残す意義はあるが、本人Gated許可・ライセンス正文・正確なsource revisionが未確認のため**新規CONDITIONAL追加ではなく研究HOLD**。[Nex-N2.5-mini Uncensored](https://huggingface.co/orcarouter/Nex-N2.5-mini-Uncensored)は35,107.2Mの全MoEモデル、Gated、Apache-2.0メタデータ。モデル作者の低拒否・能力維持は独立測定でなく、品質を断定しない。

クラウドAPIが稼働することはウェイトを正規取得できる証拠ではない。現時点のGatedは事実、将来の政府規制・削除は未確定の仮説。根拠のない規制確率を付けない。150B以上のMoEは総expertを含め、量子化例外の同条件30回以上の実機RAM/品質/速度検証と権利が未完ならSTOP。

## 4. 既存15ソースの照合
[旧15-source差分キュー](../../queues/proposed-v52-r125-ledger61-delta-next15.json)は287論理ファイル・118 Publisher SHA・327,549,073,014byte。これはv52時点の非実行研究キューで、v53 AIONとv54 REMORYを含まない。61件の取得成功報告は現物ハッシュ/オフライン復元の証明ではない。次の物理作業は**所有者の現物SHA照合→不足する固定ファイルの特定→個別利用許可→承認マニフェスト**の順であり、旧重みの削除・Gated回避・custom code自動実行はしない。

## 5. H/T/D/C/U・検算
**H**：独立学習済みの小型モデルとadapterを優先すると、4TB内の保存多様性が増す。**T**：160件全ての一意性と15ソースの静的照合、本人環境で全選択ファイルのSHA確認。実機性能は同一HW/clock/OS/backend/ABI/量子化zero-point/context/batchで30反復以上。**D**：PASS=160一意、承認0、Gated/未知総数STOP。FAIL=無許可取得、Q4をF16と偽称、MoE活性数を総数と混同。UNCERTAIN=本人HDD、権利、依存、品質。**C**：既報告ファイル欠損、原本の独自性が低い、契約条件の変化。**U**：容量・ハッシュ・ライセンス・実機品質の主要誤差源、分布未推定のため合成標準不確かさu_cと係数kは算定不可。

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `N_total` | 全学習済みパラメータ数 | 1（無次元） | 非活性MoE、MTP等含む | 未知null、150B基準 | 整数/null |
| `B_source` | 選択source容量 | byte（SI基本単位外） | 固定ファイル長合計 | 非負整数、物理差分とは別 | スカラー |
| `R_peak` | 実行全ピークメモリ | byte（SI基本単位外） | OS/KV/runtime/CPU/GPU（UMA重複なし） | 未測定null、512GB未満条件 | スカラー/null |

**次元チェック**：`N_total`は無次元で、byteの`B_source`や`R_peak`と直接比較できない。量子化は総パラメータ数を減らさない。

**ERROR CHECK**：207登録・160有効、160件一意、15ソース研究キュー、61件既存報告、承認0、新規重量取得0。ExaはHTTP402のため利用不能。政策・機械学習・ソフトウェア供給網・ストレージ工学の4分野を統合。

## 6.〈次に考える問い〉
所有者のDドライブで既存61モデルのハッシュを照合した後、追加保存byte当たりの独立学習成果が最大なのはRumble、AION、pi LoRA、REMORYのどれか？
