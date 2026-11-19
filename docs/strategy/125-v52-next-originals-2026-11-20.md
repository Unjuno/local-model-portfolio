# R125｜v52・158有効資産の取得候補とOrcaRouter監査（2026-11-20）

## 1.〈本論〉現行正本と取得状態
基準main `64013428c7b4eb607faf46930134b6e4a8f401db` のCURRENT v52は205管理・158有効（179モデル・26データセット）。既存の取得実行ledgerは61モデル／708ファイル／409,835,119,252 byteのVERIFIEDを報告。ただし本研究では所有者Windows Dドライブの現物SHAと完全offline restoreを独立検証していない。正式承認キュー0件、今回の重量取得0件。

## 2. 保存すべき原本の調査順（取得承認ではない）
| 優先 | repo ID・一次URL | source byte | 取得前の障害 |
|---:|---|---:|---|
| 1 | [Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 1,385,998,807 | CTC head tensor/ABI、本人の利用許可、物理SHA |
| 2 | [harness-hub/Qwen3.8-27B-pi-adapted](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) | 657,633,248 | 学習時親revision・tokenizer互換性 |
| 3 | [RadixArk/DaisyRose-27B](https://huggingface.co/RadixArk/DaisyRose-27B) | 55,586,309,473 | 独立RL原本、source固定済み、実機復元未検証 |
| 4 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | 55,586,056,799 | 既取得Q4と異なるBF16、親/利用権利と現物容量 |
| 5 | [orcarouter/LFM3-1.7B-abliterated](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated) | 未確定 | Gated本人権限・LFM独自ライセンス・custom code |
| 6 | [orcarouter/Nex-N2.5-mini-Uncensored](https://huggingface.co/orcarouter/Nex-N2.5-mini-Uncensored) | 未確定 | Gated本人権限・全MoEパラメータ・固定SHA |

既存Rumble、DaisyRose、pi adapterはすでに正本選定済み。無検閲LFM/Nexは今回の研究上の候補であり、正式選定追加はしていない。量子化派生を別学習成果として二重計上しない。

## 3. 15 sourceと61取得報告の差分
[R122非実行15 source案](../../queues/proposed-v50-r122-deduplicated-next15-sources.json)は332ファイル、135 Publisher SHA、374,701,109,177 byte。v51/v52の新規2資産は含まれない。既報告61件とのrepo ID・revision・ファイル数・総byteの完全一致は0件、同repoの取得報告はあるがsource scope相違が5件、未報告が10件。これは**取得成功が0件**という意味ではなく、同一原本sourceの完全一致を証明できなかったという意味。
RWKV7・iLLaDA・TRELLIS.2は取得報告とsource scopeに小差があり、重みの重複転送を避けてメタファイルを比較する。ZONOS3-Miniは既報告775,728,152 byteに対し新原本source15,345,816,226 byte。0bserverx RVNは既報告17,176,692,278 byteのQ4系に対しF16 source53,808,326,934 byte。これらは単純なbyte差を必要追加転送量とみなさず、ファイルごとのSHAで決める。既存ファイルは削除しない。

## 4. 配布政策と新規OrcaRouter
[LFM3-1.7B-abliterated](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated)はHub表示1,728.8M・Gated・license other。独立の編集済み重みとして小型保存価値があるが、本人許諾は未確認。[Nex-N2.5-mini-Uncensored](https://huggingface.co/orcarouter/Nex-N2.5-mini-Uncensored)はHub総数35,107.2M（MoE全数）・Gated・Apache-2.0表示。モデルカードの拒否低下・性能維持は作者主張であり独立実測ではない。OrcaCyber Nanoは2B主モデルと誤認せず、draft/vision/本体の学習済み総数が不明なまま最終取得準備を止める。
現在のGatedは事実だが、政府が将来当該モデルを禁止するという予測は仮説であり、確率を捏造しない。規制リスクは無許可取得を正当化しない。ExaはHTTP402で利用不可。Hugging Face公式HubメタデータとGitHub固定sourceに基づく研究。

## 5. H/T/D/C/Uと検証
**H**：小型の独立編集済み重みと学習済みadapterを優先すると、同容量で独立能力を増やせる。**T**：158有効の一意性、15 sourceの照合、所有者Dドライブの全ファイルSHA。実機ベンチは同一HW/clock/OS/backend/ABI/zero-point/context/batchで30反復以上。**D**：PASS=158件一意・承認0・全未許諾STOP。FAIL=無許可取得、量子化重複の別学習計上、総数不明モデルの最終lock。UNCERTAIN=物理現物・本人権利・性能。**C**：重み同一性、現物欠損、契約変更。**U**：媒体容量・ハッシュ・ライセンス・品質誤差。分布不明のため合成標準不確かさu_c、包含係数kの数値化不可。

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| N_total | 全学習済みパラメータ数 | 1（無次元） | MoE非活性expert、MTP込み | 未知null、基準150B | 非負整数/null |
| B_source | 選択sourceファイル長 | byte（SI基本単位外） | 固定sourceの合計 | 非負整数、物理追加量とは別 | スカラー整数 |
| R_peak | 実機全ピークRAM | byte（SI基本単位外） | OS/KV/runtime/CPU/GPU（UMA二重計上なし） | 未測定null、512GB未満を審査 | スカラー整数/null |

**次元チェック**：パラメータ数は無次元、source容量とRAMはbyte。GGUFの量子化でMoE総数は減らない。150B超の量子化実測例外は現行policies/limits.jsonの同一HW参照モデル・品質・速度・権利・個別承認を全て満たすまで取得停止。

**ERROR CHECK**：205登録・158有効、旧取得報告61件・708ファイル、15 source＝同repo異scope5＋未報告10、取得承認0、新規重量取得0。法律・ML再現性・供給網フォレンジック・ストレージ工学の4領域を横断。

## 6.〈次に考える問い〉
既存61モデルを実機でハッシュ検査した後、最も少ない増分byteで保全できる独立した学習成果はどれか？
