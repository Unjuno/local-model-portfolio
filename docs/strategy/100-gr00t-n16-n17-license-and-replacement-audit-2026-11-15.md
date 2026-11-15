# R100 — NVIDIA GR00T N1.6/N1.7の学習済み差分、ライセンス改訂と交換判断（2026-11-15）

## 1.〈本論〉評価対象と決定

GitHub `Unjuno/local-model-portfolio`の**v42（195登録・148有効）**を基準に、既存`nvidia/GR00T-N1.6-3B`の権利情報と新候補`nvidia/GR00T-N1.7-3B`をNVIDIAの一次資料で比較する。

**判断（2026-11-15）：N1.6はCONDITIONALのまま研究保持、ライセンス表記を非商用に修正。N1.7は新規HOLD研究（正本への資産追加0）とし、N1.6との交換は見送る。** 販売数・評判・後継版という名前だけで唯一の学習済み原本を消さない。権利確認・本人のアクセス権限・完全な重み／依存・実機/HDD実測が未完成なため、どちらも取得承認はしない。

| 項目 | 既存のN1.6 | 新候補N1.7 |
|---|---|---|
| 公式原本 | [nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B) | [nvidia/GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B) |
| 主モデル（Hub概数） | 3,286.6Mパラメータ | 3,144.0Mパラメータ |
| 学習済み視覚言語バックボーン | Eagle-Block2A-2B-v2 | Cosmos-Reason2-2B／Qwen3-VL系列 |
| 動作状態表現 | N1.6の従来のend-effector形式 | 相対EEF形式、人間・ロボットで共通 |
| action state dimension・horizon | 29・16 | 132・40 |
| Flow-matching DiT action head | 32層 | 16層 |
| 追加された訓練経験 | 当時の多種類ロボット学習 | 作者報告20,000時間のEgoScale人間映像事前学習を含む |
| 推論ABIの参考 | Transformers 4.51.3 | Transformers 4.57.3、Python3.12、CUDA12.8（dGPU作者系） |
| モデルLICENSE | **非商用のNVIDIA License §3.3** | NVIDIAが**NVIDIA Open Model License**適用を2026-11-10明言、11-11にHFファイルの訂正を報告 |
| 保存上の判断 | **CONDITIONAL維持、権利・復元ゲート** | **HOLD研究、同族重複と必要依存の実証待ち** |

構造の一次資料は[NVIDIA公式コードREADME（2026-11-10時点の固定commit）](https://github.com/NVIDIA/Isaac-GR00T/blob/3b49067943eb1ab2eb2203b93d461c4390c78da3/README.md)。原モデル論文は[arXiv:2503.14734](https://arxiv.org/abs/2503.14734)。上記は設計と作者実装に関する説明で、両モデルを利用者実機で比較したものではない。

## 2. 最重要の確認事項：**LICENSEの違いを「単なるタグ差」とみなさない**

### N1.6：固定revisionの原本非商用ライセンスが現実に存在

既存v42はN1.6の`license_metadata=unknown`と記録していた。しかし、台帳が記録する同一配布元revision `d0814e7ecb19202e7c8468b46098b0b7ef3a6d61`の[LICENSE本文](https://huggingface.co/nvidia/GR00T-N1.6-3B/blob/d0814e7ecb19202e7c8468b46098b0b7ef3a6d61/LICENSE)を確認すると、表題はNVIDIA Licenseで、**3.3条は研究・評価目的に限る非商用利用**と規定する。Hubのライセンスタグが空欄でも、**原本LICENSEファイルがないことにはならない**。今後の正式正本にこの区別を反映する必要がある。

### N1.7：作者は新ライセンス適用を明言。ただし必ず固定ファイルを照合する

[NVIDIA公式GitHub issue #803](https://github.com/NVIDIA/Isaac-GR00T/issues/803)では2026-11-05に「モデルカードは商用可、repo内LICENSEは非商用」という矛盾が報告され、**NVIDIAメンテナーが11-10にNVIDIA Open Model License適用を回答し、issueをclose**した。[NVIDIA公式開発者フォーラム](https://forums.developer.nvidia.com/t/gr00t-n1-7-license-clarification-model-card-says-commercial-use-but-license-file-in-hf-repo-says-non-commercial/387959)でも11-11に旧LICENSEは訂正済み、DROID/LIBERO/Bridge/Fractalも同契約と説明。さらに[NVIDIAがHFに提出した変更PR](https://huggingface.co/nvidia/GR00T-N1.7-3B/discussions/5)は、LICENSE差替えと`NOTICE`、`Built on NVIDIA Cosmos`表記を説明する。

ただし、**現行N1.7の採用候補となる「不変40文字重みrevision」と、その同一revisionのLICENSE・NOTICE・全SHA/bytesをまだ確定していない**。古いWebキャッシュが非商用LICENSEを表示していても、現在の正式条項を旧版と混同しない一方、出版社の訂正報告をもって全ファイル監査を省略しない。

正式な[2025-10-24版NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/)は、商用利用許可に加えて、ガードレール条件、NVIDIA Cosmosの帰属表示、別コンポーネントの権利、輸出入規制遵守等を含む。**Open Model License適用モデルにも無制限の権利があるわけではない。**

## 3. 学習済み依存と容量・実行の確認

N1.7は`nvidia/Cosmos-Reason2-2B`を視覚言語バックボーンとする。現在[Cosmos Reason2-2B](https://huggingface.co/nvidia/Cosmos-Reason2-2B)はHubで**Gated**である。ただしN1.7のシャードに必要重みがすべて含まれるか、独立repoからの追加取得が要るかは固定manifest・作者ロードコードの監査前には断定しない。**Gated外部依存が必須なら本人の正規権限を確認するまで取得停止**。

NVIDIA公式はN1.7実行にGPU VRAM 16GB以上を参考提示し、TensorRTでRTX PRO 6000 Blackwell Server Edition約40Hz、Jetson AGX Thor約28Hz（LIBERO・batch=1、後者はMAXN＋jetson_clocks）を報告。ただしN1.6を同一HW/backend/context/batchで比較した数値ではなく、**旧モデルを性能で支配した証拠として使わない**。N1.7はn1d7 package、state/action 132次元、action horizon 40、Python3.12/CUDA環境を要求するためN1.6用のwheelhouse/ABIを流用しない。

保存計画4TBと最低空き200GBは**計画条件**。新候補repo約6.93GBというHubの概数から、全ソフト依存・staging・安全な実行環境の総容量を確定しない。複数の実体版と量子化を無差別に取得せず、追加が必要なら**N1.7の原本1系統＋最低限の学習済み依存**を最初の評価候補とする。

### 具体的な交換条件

N1.6（旧Eagle原本）とN1.7（新Cosmos系原本）は学習経路・表現が異なるため、単純に片方のコピーとはみなさない。N1.7を正式採用・N1.6をHOLDへ移すには次の非補償ゲートが必要。

- 同一revisionのモデル全shard、SHA256、LICENSE、NOTICE、config/tokenizer、学習済みencoder、コードcommit、第三者ライセンスを固定。
- 本人の許された取得と保存・再配布行為をモデル別、外部Cosmos別に確認。
- 同一ロボットタスク、同一HW/クロック・backend・精度/zero-point・コンテキスト・バッチ、各30試行以上で成功率・軌道安定性・median遅延／peak memoryを比較。
- N1.6だけが保持する旧Eagle系の独立挙動が用途に不要と立証できるときだけ交換し、元記録を削除しない。N1.7-DROID/LIBEROや通常量子化を自動的に新資産と数えない。

## 4. 法規制・配布制限の事実と仮説

N1.7のNVIDIAによる公開LICENSE訂正は**現実の配布契約変更**であり、政府がモデルを禁止した証拠ではない。参考に[EU AI Act第53条](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)はGPAI提供者義務と一部のopen-source例外を区別し、[中国商務省2026年第48号説明](https://english.mofcom.gov.cn/News/SpokesmansRemarks/art/2026/art_74bf283f105a4b19a11f7430df3671ae.html)も輸出技術の暫定登録と公開技術例外を区別する。公開ウェイト全般の日本国内保有禁止は今回確認していない。将来のS1→S2→S3配布制限はストレス仮説であり、N1.6/N1.7固有の公開終了予定日や確率を捏造しない。

## 5.〈変数表〉および次元確認

| 記号 | 日本語の意味 | SI単位 | 定義 | 定義域・条件 | 型 |
|---|---|---|---|---|---|
| `P_{16}` | N1.6単体の公表パラメータ | 1（個） | 3,286,600,000 | Hub公表概数、学習済み全依存の厳密総数ではない | 非負整数スカラー |
| `P_{17}` | N1.7単体の公表パラメータ | 1（個） | 3,144,000,000 | 同上 | 非負整数スカラー |
| `D_{16}` | N1.6動作状態次元 | 1（成分数） | 29 | 固定NVIDIAコードの既定値 | 非負整数スカラー |
| `D_{17}` | N1.7動作状態次元 | 1（成分数） | 132 | 同上 | 非負整数スカラー |
| `H_{16}` | N1.6動作予測horizon | 1（ステップ数） | 16 | 同上 | 非負整数スカラー |
| `H_{17}` | N1.7動作予測horizon | 1（ステップ数） | 40 | 同上 | 非負整数スカラー |
| `B_{lim}` | 計画保存予算 | byte | 4,000,000,000,000 | 物理HDD計測値ではない | 非負整数スカラー |
| `B_{floor}` | 必須空き容量余白 | byte | 200,000,000,000 | 実HDDで確保すべき値 | 非負整数スカラー |

**次元チェック：**両モデルのパラメータ数は無次元の「個」、horizonはステップ数、動作状態次元は成分数、保存byteとは直接加減算できない。N1.7の次元132がN1.6の29より大きくても、**成功率や汎化性能が高い数学的証明にはならない**。

## 6. H/T/D/C/U・ERROR CHECK

**H：**N1.6とN1.7のライセンス正文・アーキテクチャ・学習結果は異なり、N1.7は単純な量子化複製ではない。**T：**N1.6固定LICENSE 1件、N1.7版権確認（issuer issue/forum/HF PR）3件、固定コードN1.6/N1.7、各モデルメタデータ、Cosmos配布statusを比較。将来評価は同一HW・各30反復。**D：**旧LICENSE非商用・新作者訂正報告・構造差の文書照合PASS。新しいN1.7特定revisionのLICENSE+NOTICE完全一致、依存閉包と性能による交換の可否はUNCERTAIN、本人権利なしの取得はFAIL/STOP。**C：**本体シャード中身が同一、外部Cosmos Gated原本が取得不可、またはN1.7の実測品質が著しく劣る場合は採用を見直す。**U：**修正済みLICENSEの不変commit・モデル重みhash・本人権利・全依存・実行HWとばらつき。未測定につき合成標準不確かさ`u_c`と包含係数`k`は算定不可。

**ERROR CHECK：**正本v42の195登録／148有効を基準とする。新規採用0・削除0・承認0・重みDL0。N1.6の既存権利ラベルを実ファイルから具体化し、N1.7は明示的な研究HOLDとする。研究報告はNVIDIAの発行した新LICENSEの一般条項を確認するもので、独立の法的助言や所有者の権限認証を代替しない。

関連分野：ロボティクスのVLA制御、機械学習モデルアーキテクチャ、AI重みライセンス・輸出管理、ソフトウェア供給網のSHA同一性、デジタルアーカイブ。

## 7.〈次に考える問い〉

**N1.7が同一タスクでN1.6に勝っても、旧Eagle系チェックポイントが再現できない歴史的学習成果なら、数GBの保存費用で双方を保持すべきか。**その判断は同条件の品質・復元性・目的適合性から導く。
