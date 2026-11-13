# R50・v30｜Alpamayo 2 Edge原本の保存選定と版差分監査（2026年11月12日）

> 専用ブランチ `strategy/2026-11-03-01-risk` 親 `accfc1a592697941365d10c045097c826330cfb2`。**正式選定は旧177資産を保持したまま追加1モデルのCONDITIONALのみ**。利用・運転・ダウンロードの承認ではない。現行**178資産、131有効、152モデル/26データ、SELECT53/CONDITIONAL78/HOLD28/延期13/EXCLUDED6**。

## 1.〈本論〉モデルの独立性と選定判断

[公式原本](https://huggingface.co/nvidia/Alpamayo2-Edge)、[NVIDIA技術記事（2026-11-10）](https://developer.nvidia.com/blog/running-av-reasoning-models-within-onboard-compute-and-latency-limits/)、[固定推論コード](https://github.com/NVlabs/alpamayo2-edge/tree/02f55a7aeabc1a2b9f7a80445c08e40bddc89f5e)を確認。**2,651,163,378個の総学習済みパラメータ**をモデルrepoのsafetensorsメタデータで観測。内訳はNVIDIAの丸め値でVLM基盤2.45B（LLM1.96B＋画像SigLIP2 0.41B＋投影0.08B）＋拡散action expert0.2B。活性パラメータやモデル名2Bを完全総数と混同しない。

既存`nvidia/Cosmos3-Nano-Sim-Auto`は**将来の動画・LiDAR等の世界状態**を生成する。Alpamayo2-Edgeは**周辺6台カメラの22フレーム＋自車履歴20姿勢＋ナビテキスト→将来64点の運転軌道と因果説明**を出す別のVLA訓練成果。Alpamayo2-SuperからのCoC蒸留とAlpaGym閉ループ強化学習による差分は元のCosmos3-Edge基盤や単純量子化では再現できない。NVIDIAによるclosed-loop RLの「従来最良学習状態比48.9%改善」は**出版社測定**であり、独立評価ではない。

**判定**：**R1 / S2でCONDITIONAL追加、BF16の元公開checkpoint1つ**。別の量子化エンジン/DFlash2/AlpaJudgeを追加重みとして機械的に数えない。初回試験には実カメラ・実車運転を使わずシミュレーションと権利を得たサンプルを想定し、実際の実行前には本人の別途承認が必要。

## 2. 固定版とライセンス：「公式コードの旧版」対「LICENSEのある現行版」

| 出典 | HFモデルrevision | ファイル | 全公開ファイルbyte | 内容 |
| --- | --- | ---: | ---: | --- |
| [公式コードREADME指定のモデル版](https://huggingface.co/api/models/nvidia/Alpamayo2-Edge/tree/f8951d095de3589b3face1dec3f4394c8ecedb38?recursive=true) | `f8951d095de3589b3face1dec3f4394c8ecedb38` | 11 | 5,320,369,777 B | **LICENSEファイルなし** |
| [今回の採用調査固定版](https://huggingface.co/api/models/nvidia/Alpamayo2-Edge/tree/b92b6aa326bd3e2235db28f248ad5a30b5890e64?recursive=true) | `b92b6aa326bd3e2235db28f248ad5a30b5890e64` | 12 | **5,320,375,887 B** | LICENSE 2,619Bと更新README |
| 差分 | — | 1増 | **6,110 B** | **共通10ファイルの提供元hashは全一致**、2 shard・tokenizer・index・configは同一 |

モデル重み2 shardの正確なbyteは4,275,716,192＋1,026,726,076＝**5,302,442,268 byte**。新しいrevisionを選ぶ理由は重み能力向上ではなく、**原本の完全LICENSEが含まれること**。既に公開された同一重みの旧・新revisionを二重保存する必要はない。GitHubモデル実装のコードcommitは`02f55a7aeabc1a2b9f7a80445c08e40bddc89f5e`。別の管理対象であるソースコードとモデルウェイトのSHAを混同しない。

[原LICENSE全文](https://huggingface.co/nvidia/Alpamayo2-Edge/raw/b92b6aa326bd3e2235db28f248ad5a30b5890e64/LICENSE)を今回読取確認し、**ウェイトはOpenMDW-1.1**、別の[GitHubソース](https://github.com/NVlabs/alpamayo2-edge/blob/02f55a7aeabc1a2b9f7a80445c08e40bddc89f5e/LICENSE)はApache-2.0。OpenMDWは配布時の契約正文・通知保持、第三者の権利・同意の個別確認を要求。これはNVIDIAの学習用データの自由取得を保証しない。例示[PhysicalAI-AVデータ](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles)は**別のGated利用規約**で、権限未確認なら外部例示をDLしない。

## 3. ハードウェア・ABIと性能、変数表

**開発元の固定参照環境**はLinux/Python3.12、torch2.8.0、torchvision0.23.0、Transformers5.17.0、通常PyTorch SDPA、任意でFlashAttention2.8.3、uv.lock。NVIDIA H100 80GB、BF16、22画像・3,236 prompt tokens、batch1、独立6軌道で**GPUプロセス12.06GiBピーク**（torch割当8.40GiB、予約11.38GiB）。GPU 16GB以上をメーカー推奨するが、他のGPU/CPUでの挙動は未検証。**評価条件を混同しない**：技術カードの875シナリオ×3回ロールアウトで事故まで平均15.15±0.04km、1,392サンプルの5s minADE6 0.52mは**メーカー実験**。安全性・自動車認証・現実走行を保証しない。NVIDIAの学習データ規模約115,000時間/3.7M CoCは重みと別保存項目。

| 記号 | 意味（日本語） | 単位(SI) | 定義 | 定義域・型・前提 |
| --- | --- | --- | --- | --- |
| `C` | 保存計画上限 | byte | 4,000,000,000,000 | 非負整数スカラー、物理実機未測定 |
| `F` | 必要な物理空き最低値 | byte | 200,000,000,000 | 非負整数スカラー、実機の空き別確認 |
| `B_src` | 今回固定した12ファイル | byte | 5,320,375,887 | 非負整数、runtime/data/staging除く |
| `B_shard` | 2重みシャード | byte | 5,302,442,268 | 非負整数、BF16原重み |
| `R` | v30新原本の計画予約枠 | byte | 8,000,000,000 | 非負整数、取得ファイル実測ではない |
| `N_param` | 元モデル全テンソル数 | 1（無次元） | 2,651,163,378 | 正整数、HF safetensors metadataから観測 |
| `M_peak` | 実測GPUプロセスメモリ | byte | 12.06 GiB（開発元H100測定） | プラットフォーム条件付き、所有者実機の測定ではない |
| `B_v27` | 旧126件に関するソースの論理集合 | byte | 3,417,685,712,585 | 非負整数、外部学習済み依存・本体未完 |

**次元検査**：C/F/B_src/B_shard/R/B_v27はbyte、N_paramは無次元。12.06GiB=12.06×1,073,741,824 byteであり、4TB十進枠・512GB十進RAM上限と同じ単位に換算可能。ただしGPUだけの数値がOSや別依存込みの完全実機RAMではない。保存スコープ5.320GBを8GB予約枠内と確認できても**実ディスクに入る、権利がある、実行できる**ことの証明にはならない。

## 4. H/T/D/C/U・ERROR CHECK

H：Alpamayo2の蒸留/閉ループRL走行軌道ポリシーは、既存の動画世界モデル・一般VLAと異なる独立保存価値を持つ。T：公開元12ファイルのsha/byte、LICENSE全文と固定コードのABI、全2,651B総数をまずメタデータだけで検証。実機試験は権利とユーザー個別承認が揃ってからシミュレーション上で30条件以上。D：**条件付き採用の一意性、提供元SHA整合、権利原文の取得は静的PASS**。本人の取得、PhysicalAI-AV、実行・リアル運転、実機HDDはUNCERTAIN、未承認で取得すればFAIL。C：取得権利未確認、必要補助部品欠落、実機RAM過大、ベンチが独立追試で不成立。U：他HW・自治体道路・カメラ個人情報やソースの将来更新、不確実性の共分散は未測定でu_c/kは数値化しない。

**ERROR CHECK**：旧177件の判断を無変更維持、v30 178ユニークID・131有効・152モデル/26データ、20総数未確認・150B超例外2HOLD、EXCLUDED6維持、承認キュー0。既存大容量形式を削除せず、追加するのは元VLA学習状態1つ。GitHub Actionsテスト・モデル本体DL・ランタイムテストは未実施。学際性：強化学習、ロボット・車両運動学、ML供給網、ソフトウェア保全・法務で同じ原本/依存照合を活用できる。

###〈次に考える問い〉
約5.32GBの未圧縮原本を保全する場合、量子化の多形式よりも、**学習済みの軌道・理由生成という不可逆な訓練成果**に容量を優先すべきではないか。
