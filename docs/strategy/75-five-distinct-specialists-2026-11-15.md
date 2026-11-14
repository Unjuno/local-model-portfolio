# R75｜専門モデル5件の追加選定研究（2026-11-15）

## 1.〈本論〉

現行v32＝182登録・135有効。別学習済み状態の保存価値、本人アクセス権限、モデルの一次ファイルの同一性を独立に審査した。[R75機械可読一次ファイル台帳](../../catalog/proposals/07-rare-specialist-2026-11-15.json)は、Hugging Face公式APIから再照会した5件の固定40桁revision、公開ファイルサイズ、LFS SHA256とGit blob SHA1を記録する。正式なv33選定は作成せず、ダウンロード承認・実行は0。

| 対象モデル | 公開元の参考選択ファイル | 判断 |
|---|---:|---|
| [Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) | 243,656,960 byte／7ファイル | 次期CONDITIONAL候補。異なる学習済み分類器（119,862,733 byte）と回帰器（123,786,699 byte） |
| [Kumo-Anomaly](https://huggingface.co/nvidia/Kumo-Anomaly) | 29,612,151 byte／4ファイル | 次期CONDITIONAL候補。約8M parametersの時系列拡散異常検知、予測TTMの単純な代替ではない |
| [Ising ColorCode Fast](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | 5,899,248 byte／重み1本 | P0：Gated個人権利を先に確認。三角色符号predecoder、公開元は2,936,580 parametersと主張 |
| [Ising SurfaceCode Fast](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | 1,826,360 byte／重み1本 | P0：Gated個人権利を先に確認。回転表面符号向け、約913k parameters。ColorCodeとは異なる |
| [Nemotron 3.5 Parse](https://huggingface.co/nvidia/Nemotron-3.5-Parse) | 2,524,008,942 byte／不完全な6ファイル | HOLD：既存LightOnOCR-3-0.8BとPaddleOCR-VL-1.5への相対的な新規性と実行環境を先に比較 |

### 一次法務根拠と限界

**Kumo Relational**：[固定版モデルカード](https://huggingface.co/nvidia/Kumo-Relational/blob/efdbb110daea5aae123447864a64612e8a3dc6be/README.md)にはTabICLv2の関係表向け後学習を明記。[OpenMDW-1.1ライセンス本文](https://huggingface.co/nvidia/Kumo-Relational/blob/efdbb110daea5aae123447864a64612e8a3dc6be/LICENSE)と[TabICLv2のBSD-3-Clause第三者告知](https://huggingface.co/nvidia/Kumo-Relational/blob/efdbb110daea5aae123447864a64612e8a3dc6be/THIRD-PARTY-NOTICES.txt)を確認。ただし学習済み重みはPython .pt形式で、未信頼pickleを実行してはいけない。NVIDIA structured-data-modelsのコード/ABIと親モデル参照の必要性は未閉包。

**Kumo Anomaly**：[固定版モデルカード](https://huggingface.co/nvidia/Kumo-Anomaly/blob/369ccba38a105736c6c9e4b5788a330c7e22112e/README.md)はモデルのApache-2.0、約8M parametersと拡散異常検知の用途を明示。[NV-Tesseract-AD原論文](https://arxiv.org/abs/2610.12754)の能力と独立。単一final_model.pthはpickle形式の可能性があり、安全な静的監査・正確なKumo-TSソースと自動Hub取得を無効化したoffline版の確認が必要。原本コードの第三者ライセンスは未確認。

**Ising 2件**：公開APIは双方ともGated auto。公開元ハッシュが見えても個別アカウントによる取得承認を意味しない。ColorCodeはOpenMDW-1.1、SurfaceCodeはライセンスタグotherでモデルカードがNVIDIA Open Model Licenseを指定しており、同一条件とみなしてはならない。[ColorCode論文](https://arxiv.org/abs/2607.10058)と[SurfaceCode論文](https://arxiv.org/abs/2604.12841)は各々異なるノイズモデルと符号の結果であり、報告の誤り率改善は作者環境に限定。P0は合法的なアクセス調査順位であって、回避DLの推奨ではない。

**Nemotron Parse**：固定版は2026-11-14の評価追加コミット。主重み2,523,266,640 byte、オプションのDFlash2別学習重み178,657,376 byteを別の目的として記録。全repo217ファイル・約730kBの第三者告知とカスタム実行コードがあり、同条件ベンチマークも未確認なので保存候補に重複追加しない。

## 2.〈応用・転用例〉採用ゲート

Kumo 2件は、次期選定を判断する際に、公開元の全必須重み・ライセンス/NOTICE・依存コード・Python/torch/driver/ABI・セキュリティ・owner HDDと将来のオフライン復元条件を検査。Ising 2件は本人Gated許諾が得られない限り研究記録だけに留める。Parseは既存2つのSELECT OCRと同一文書・同一CPU/GPU・同一batch・同一precisionで比較し、利点がなければ追加しない。

## 3. 変数表・次元/単位チェック

| 記号 | 日本語の意味 | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| BR | Kumo Relational候補ファイル容量 | byte | 243,656,960、7公開元ファイル | 整数スカラー |
| BA | Kumo Anomaly候補ファイル容量 | byte | 29,612,151、4公開元ファイル | 整数スカラー |
| BI | Ising2件Gated重み参照合計 | byte | 7,725,608、取得許諾なし | 整数スカラー |
| BN | Parseの不完全参考スコープ | byte | 2,524,008,942、ランタイム未含有 | 整数スカラー |
| BT | 候補5件の公開元参照合計 | byte | BR+BA+BI+BN=2,805,003,661 | 整数スカラー |
| N | 正式採用の有効資産数 | 1（件） | 135、変更なし | 整数スカラー |

次元チェック：BR、BA、BI、BN、BTはbyteで加算可能。ファイル件数・モデルパラメータ数・実機VRAM/ディスク空きは異なる測度であり、この試算からは導けない。

## 4. H/T/D/C/U・ERROR CHECK

H：汎用LLMだけでは代替できない独立学習済み専門タスクが少容量で存在する。
T：5repoの固定publisher API、公開ハッシュ、Gated、ライセンス表示、既存v32とのID非重複を全数確認（n_min=5）。
D：5件のrevision・file bytes・公開元SHAの形式、未取得・未承認はPASS。正式採用・権利・依存閉包・ハードウェア実行はUNCERTAIN。
C：後学習でなく単純コピー、必要な外部学習済み親重み欠損、作者のベンチマーク条件から別ノイズへ転移不可、文書解析で独自性不足。
U：本人の権限、pickle安全性、runtimeとCUDA ABI、現物SHA、実HDDが未測定。合成標準不確かさu_c・包含係数kは確率分布未定義のため数値化不可。

ERROR CHECK：5候補の固定repo ID・ハッシュ・ファイルbytes一意。全5候補のbyte単純和2,805,003,661。既存182/135と取得承認0を維持。モデル実行0・本体取得0。

学際性：時系列統計、リレーショナル学習、量子誤り訂正、ソフトウェア供給網、著作権/アクセス制御。

## 5.〈次に考える問い〉

数MBの希少な科学モデルと数百GBの一般モデルを、再取得可能性・独立の訓練コスト・非代替性という指標で比較すると、どちらの保存優先順位が合理的か？
