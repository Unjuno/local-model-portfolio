# R122｜v50：取得候補3系統を重複排除し、Windows Dドライブ用の15固定sourceへ統合

調査日：2026-11-19。正本v50（登録203、active156、SELECT53＋CONDITIONAL103）に変更を加えず、次に物理保存すべき学習済み原本・評価データの実装上の取得候補だけを再整理した。**今回新たな重み取得は行わず、過去の取得台帳をWindows Dで独立再ハッシュしたとは報告しない。**

## 1.〈本論〉重複排除後の保存対象を確定

一次ソース：過去の[R121 v50 17source](../../queues/proposed-v50-r121-master-sources-17.json)、[R119 v49 7source](../../queues/proposed-v49-r119-next7-public-source-entries.json)、[R117 v48 8source](../../queues/proposed-v48-r117-next-wave-eight-source-pinned.json)、および[2026-11-19取得報告台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)。R121 GO11のうち**同一revision／全sourceファイル個数／bytesが53モデルのVERIFIED報告に一致する7件を除外**。その後、R121とR119のZONOS3、Interpretic BF16、RVN F16が同一source scopeで重複し、R119とR117のFara1.5が同一source scopeで重複したことを確認した。

| 重複源の除外対象 | 取り除けた二重計上byte |
|---|---:|
| ZONOS3-Mini | 15,345,816,226 |
| Interpretic v2 BF16 | 55,586,056,799 |
| 0bserverx RVN F16 | 53,808,326,934 |
| Fara1.5-27B | 54,743,814,229 |
| **計** | **179,484,014,188** |

この179.484GBは**将来の同一sourceの二重ダウンロードを避ける効果**であり、ユーザーHDDで179GBの物理ファイルを削除して空けたという意味ではない。各sourceの40桁revision、ファイルパス・byte・LFS SHA256またはGit blob SHA1を全件突き合わせ、4件はいずれも同一だった。

## 2. 初回実行優先・15source（12独立学習済み成果＋2データ、SenseNova補助コード1source）

| 順 | Source | 固定選択byte | 役割 |
|---:|---|---:|---|
| 1 | [ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | 7,606,817 | 日本語の外部評価 |
| 2 | [Aya Dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 140,160,376 | 多言語評価・指示学習 |
| 3 | [Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash) | 1,385,998,807 | 独立CTC ASR後学習 |
| 4 | [RWKV7-7.2B](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14,402,000,339 | 再帰型言語モデル |
| 5 | [iLLaDA-8B](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 16,512,918,618 | 拡散型言語モデル |
| 6 | [TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16,237,485,044 | 3D形状・材質モデル |
| 7 | [SenseNova-Loop-9B GGUF](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF) | 19,338,124,279 | 本人Gated許可が未確認のSafetensorsに対する同一配布元の公開重み |
| 8 | [SenseNova Previewの一致コードのみ](https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview) | 26,724 | 別学習成果ではない。正確なコード2ファイルのみ |
| 9 | [ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | 15,345,816,226 | 既報告0.776GBとは違うBF16原本＋codecスコープ |
| 10 | [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | 32,848,321,404 | 高速画像生成、encoder/VAE含む |
| 11 | [Wan2.2 TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | 34,201,539,556 | Video DiT、UMT5 encoder、VAE含む |
| 12 | [Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | 54,743,814,229 | GUI操作エージェントの独立後学習 |
| 13 | [Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) | 60,142,913,025 | 長期記憶書き込みモデル |
| 14 | [InterpreticAI v2 BF16](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) | 55,586,056,799 | 選択的拒否編集・高精度学習済みマスター |
| 15 | [0bserverx RVN-F16](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 53,808,326,934 | RVN再構成元GGUF。事前学習時BF16ではない |
| **合計** | **15公開source** | **374,701,109,177** | **重複形式なし、保存先未実測** |

完全なallowlist、publisher revisionとSHA、各sourceの`repository_type`（model/dataset）は[R122統合非実行マニフェスト](../../queues/proposed-v50-r122-deduplicated-next15-sources.json)に固定。**15sourceは13モデル配布repo＋2データrepo、ただしSenseNova Previewはコードだけなので独立した重み成果は12件**。既存v50カタログを増やさず、既存53モデルの局所archive scopeとの重複を避ける。R121の6 HOLDや本人Gated原本はこの15件の自動候補へ混入しない。

## 3. Windows安全性・実際に検出したバグ

R117のELYZA原配布には`baseline/preds/anthropic.claude-v2:1.csv`（181,663byte）という**Windows NTFSでは使用できないコロン入りの原path**があり、そのままDドライブ用取得器に投入すると失敗した。R122では初期選択からこの1ファイルのみ除外して配布元revision・Git blob SHA1を`nonportable_source_exclusions`に記録。評価問題本体の`test.csv`は保持。**この1ファイルが復元できていない以上、ELYZAリポジトリ全ファイルの完全コピーを達成したとは呼ばない。** 後日POSIX名の原本を必要とする場合はreversible filename mappingまたはPOSIX対応媒体へ移して別途再取得する。

[Windows downloader](../../scripts/download_r115_windows.py)もモデルとdatasetを分離し、`hf_hub_download(repo_type='dataset')`を用い、モデルはモデル名前空間、データは`datasets/author/repo`へ保存するよう変更。NTFSの無効名・Windows予約名・大小文字折り畳み衝突も拒否。Hugging Face公式[Hub download guide](https://huggingface.co/docs/huggingface_hub/main/guides/download)ではrevisionとlocal_dirによる固定ファイル保存が可能。モデルコード・pickle・評価スクリプトはダウンロード時に自動実行しない。

既存R115選択モデルKitten／ARLoopの`apache-2.0 author/model card no standalone LICENSE`注記が、以前の形式validatorで例外となる問題も修正。**注記は入力に保存し、validator返却値のライセンスタグ正規化だけを行う。独立LICENSE未確認の利用権は自動承認しない**。現在も実転送は`--execute`に加え、本人の適法な行為・物理ドライブ・全source scopeが固定された`--approval-file`が無い限り起動できない。

## 4. 反証可能な最小検証と実行手順

Python 3.12/Linux上でR122テスト**12件、既存R115テスト10件、R119テスト6件、承認ポリシーテスト7件の計35件がPASS**。これはコードとpublisher snapshotの検証結果で、Windows Dの実転送試験やoffline model restoreの代用ではない。

Windowsの所有者PC（Dドライブが実際にマウント済み）で読み取り専用のplan表示を行い、既存保存領域を特定してから検証する。

```powershell
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v50-r122-deduplicated-next15-sources.json" --dry-run --root "D:\AI-Models"
```

取得はユーザーが実機で同一source単位の合法な利用権と実HDD空き／一時cacheを確認し、適法な正本scopeを明示承認した**後に限り**次を実行する。承認ファイルは今回作成・署名していない。

```powershell
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v50-r122-deduplicated-next15-sources.json" --execute --approval-file "owner-approved-r122.json" --root "D:\AI-Models"
```

## 5. 容量変数表・次元チェック

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域/範囲/前提 | 型 |
|---|---|---|---|---|---|
| `B_g` | 7既報告scopeを除外した3研究queueの額面合計 | byte | 554,185,305,028 | 重複あり・NTFS非互換あり・実diskではない | 非負整数スカラー |
| `B_d` | 4重複したsource scope | byte | 179,484,014,188 | 各publisher SHA/revision/file set一致 | 非負整数スカラー |
| `B_n` | 1件Windows非互換CSV | byte | 181,663 | この初回取得scopeからのみ除外 | 非負整数スカラー |
| `B_u` | 15sourceの修正後論理量 | byte | `B_g - B_d - B_n` | publisher固定scope、外部依存別 | 非負整数スカラー |
| `F` | 保存後の最低物理空き | byte | 200,000,000,000 | 転送一時cache中も維持 | 非負整数スカラー |
| `H` | 現在の実Dドライブ空き | byte | 未測定 | 同時処理/時刻で変化 | 非負整数スカラー/不明 |

**計算**：554,185,305,028 − 179,484,014,188 − 181,663 = 374,701,109,177byte。すべてbyte単位なので減算は次元整合。過去の実行台帳では観測当時最小2,710,260,613,120byte空きとの報告があるが、これは`H`の現在値ではない。実際の転送増分は過去ファイルとcacheのハッシュ重複・最大ステージング消費を加味して再計算する。

## 6. H/T/D/C/U・ERROR CHECK

**H**：同一publisher source重複を排除し、既保存の53scopeを再取得しないことで、同じディスク容量内で独立機能の保全件数を増やせる。

**T**：R121/R119/R117の同一repo SHA+全ファイルpath/size/hashを比較、既取得報告53件中同一scope7件を除外、15sourceへ統合。検証最小件数は全15、ファイル検査は332件。R122・既存テスト35件を実行、停止条件はパス不正・SHA/版の不一致・未承認・残容量床割れ。

**D**：source重複とWindows安全性、テスト35/35はPASS_METADATA。Dの現物hashとライセンス・全依存・offline復元はUNCERTAIN。未承認/Gated回避や容量床割れはFAIL。

**C**：元ファイルが既取得台帳から消失、異なるモデルの未検証学習済み依存が隠れている、画像/動画モデルのVAE/encoderやハードウェアABIが互換でない場合。

**U**：現在のD残空き、実FS上の重複、publisher SHAと現物ハッシュ差、CLI/HF Hubバージョン、Windows長パス・ディスク故障、モデル本体推論品質。統計分布の観測がないため合成標準不確かさ`u_c`と包含係数`k`は未算定。

**ERROR CHECK**：v50登録203／有効156不変更。旧報告53モデル/579ファイル/270.836GBは報告のまま。4repo exact source scope重複179.484GB、NTFS1ファイル181,663byte除外、15source＝13モデルrepo＋2データrepo、332ファイル・135publisher SHA256・374,701,109,177byte。R122 12件＋後方互換23件、合計35/35PASS。正式取得承認0、今回実モデル重みDL0。GitHub mainのみ。

関連分野：機械学習、デジタルアーカイブ、サプライチェーン・ハッシュ、ファイルシステム互換性、国際的なデータ・ライセンス法。

###〈次に考える問い〉

**今のDドライブで過去53scopeと新15sourceの存在/不在をハッシュ照合して、最初の日本語評価データから合法的に差分取得するための正確な保存先と最大ステージング容量を確定できるか。**
