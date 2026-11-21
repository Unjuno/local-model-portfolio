# R146／v62 — 小型MoE・極小視覚・無検閲VLMの独立原本選定（2026-11-22）

## 1. 目的と判断の範囲

現行ポートフォリオの目的は、公開方針・Gated化・商用ライセンス・供給消失の変化に備え、**再現困難な別学習成果をローカルで再構築できるように保存**すること。単に「無検閲」「小さい」「人気」だけで採用しない。今回はv61の227資産を完全保持し、4件を**CONDITIONAL研究選定**。正本は **v62／231登録・184有効（SELECT53・CONDITIONAL131）**。今回の重量モデルDL／ユーザーDドライブ再SHA／個別取得承認／未審査コード実行は**いずれも0**。

対象の[正本](../../catalog/CURRENT.json)・[正式overlay](../../catalog/revisions/v62-2026-11-22.json)・[58ファイルとCactusランタイム5参照の不変source](../../manifests/drafts/r146-2026-11-22-aurora-mirage-lfm3-paired-source.candidate.json)・[機械可読決定とH/T/D/C/U](../../catalog/decisions/2026-11-22-r146-v62-original-and-heretic-selection.json)・[全184件readiness](../../catalog/readiness/v62-2026-11-22-r146-all184-gates.json)を一貫して参照する。

## 2. 4モデルの採用・代替比較

| 新しい原本（Publisher） | 採否／選択したファイル | 明確な独立学習成果 | 未解消の条件 |
|---|---|---|---|
| [AuroraAI-Research/Aurora2-400M-A20M](https://huggingface.co/AuroraAI-Research/Aurora2-400M-A20M/tree/f2e561d38b0c0c35e910c8a519f553b2831ffad4) | **CONDITIONAL**。FP32 master主体10ファイル**1,599,571,502byte** | 399,597,454総学習済み要素、作者19,050,382活性/token。1層につき32 routed expert＋shared 1、top1 MoE、100B token scratch pretrain（作者発表）。LFM系hybridや短いdraftモデルとは独立したルータ学習成果 | SFT/RLHFなしのBaseで実用会話能力は低い可能性が高い。2,048 token context、訓練データセットの再利用権、FlexAttention/custom PythonのABI、実機評価未確認 |
| [Cactus-Compute/mirage](https://huggingface.co/Cactus-Compute/mirage/tree/3d03cee88c0acbe4e71b94b567ab14e6e55f40c9) | **CONDITIONAL**。safetensors＋cact 2形式／関連5ファイル**237,985,863byte** | 作者公称51.3MのOCR・物体検出・セグメンテーション・場面記述・構造化判断を統合する極小視覚成果。既存PaddleOCR等の大型言語統合モデルと独立したワンパス端末処理 | 公式の完全tensor総数を独立に確定できず **UNVERIFIED_BLOCK_FINAL_LOCK**。端末性能はSamsung Galaxy S26（NPU 74ms／CPU 107ms）の**作者値**で、clock、batch、推論条件の独立検証なし。Cactusネイティブエンジンは未審査実行禁止 |
| [LiquidAI/LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B/tree/f83d2b0a2296aaa277f394990a9b8b949ddf9691) | **CONDITIONAL**。学習時親BF16の18ファイル**3,854,651,108byte** | 1,918,181,888 BF16要素、内訳：language 1,728,801,536、vision 164,206,336、projector 25,174,016。Hereticの再現レシピが指定する厳密な親commit `f83d2b0a…` を保存（現行HFの異なる最新commitと元重みSHAは一致） | LFM Open License v1.0、年商1,000万米ドル以上企業の商用利用制限、動画tokenizer・Python custom code・Transformers ABI／owner権利／GPUの実測未完了 |
| [saidutta69/LFM3-VL-2B-heretic](https://huggingface.co/saidutta69/LFM3-VL-2B-heretic/tree/f4cf2cfb5b1289ca4ca10c6c71eb17d147c8c795) | **CONDITIONAL**。改変済みBF16、Q4_K_M GGUF＋F16 mmproj、一式25ファイル**5,334,098,126byte** | 親と異なるBF16 SHA256を持つ実際の拒否方向編集後の学習済み成果。モダリティ実装・tokenizerは親とPublisher SHA一致。BF16マスターを保持しつつ、エッジで画像入力できるGGUFとmmprojを同一モデル資産内に同梱する | 同族GGUF別量子化14ファイルは**別モデルとして不採用**。作者100問のrefusal 98→3、MMLU 14,042問34.37→34.44%（標準誤差0.40ポイント）は独立検証されず、言語以外の品質・実機互換性を証明しない。LFM商用条件と編集用データ出所審査が必要 |

**原本と編集成果の判断**：Hereticの`reproduce/config.toml`にある親は`LiquidAI/LFM3-VL-2B@f83d2b0a2296aaa277f394990a9b8b949ddf9691`。出版社BF16の元重みSHA256は`a9bb8b1c159c9d6c3007bc1c7ad8018b599f759d97da2701714e37426283e131`、改変後は`91d527edb09f1e382172c9bf4028247676f92b6c1545f1e4d6b8920b4eba906a`で**異なる**。同一の学習結果の単純量子化ではない。tokenizerといくつかのコードが一致するものの、所有者HDD上の同一SHAは今回照合していない。作者の`reproduce/config.toml`・`reproduce/reproduce.json`・Heretic v1.4.0／CUDA13／RTX PRO 6000 Blackwell 94.97GB VRAMなどは**作者記録**であり、こちらの実測と混同しない。

## 3. 重複排除と取得前の確定仕様

選定対象は**4 repo／58 source files／11,026,306,599 byte／9 publisher LFS SHA256参照**。Auroraの別BF16/FP16変換16ファイル、Hereticの14別GGUF変換は不要と判断。BF16原本＋GGUF Q4_K_M＋mmprojは**一つの編集成果の保存・可搬実行用表現**であって3モデルと数えない。

Cactus Mirageの`mirage.cact`は通常のPyTorch Safetensorsから再構成できるとは断定できないため、同じ論理モデル内の圧縮されたデプロイ成果として保全。必須のCactus Compute engineは[公式Cactus runtime repo](https://huggingface.co/Cactus-Compute/cactus/tree/f4ab2741203a282c6e7b89983de2b5e5b2e805a8)の**4.1.4**からWindows x86_64、Linux x86_64実行体、Windows Python wheel、LICENSE、manifestの**5ファイル／4,137,947byte**を別途固定。GitHubコードは[cactus-compute/cactus@bb822a3](https://github.com/cactus-compute/cactus/tree/bb822a35983cf0ff942d67d46b8b79b535773b02)。Publisher source固定やバイナリ存在は、ABIの動作・コード安全性・権利合格ではない。

LFM Open Licenseに関しては[Liquid AI原文](https://www.liquid.ai/lfm-license)を参照。年間収入の閾値は**商用利用**の利用許諾上の制限で、個人研究と同一には扱わない。MirageのApache2とCactus実行環境の利用行為も別々に確認する。

## 4. 最新96件の重複済み取得台帳から次候補を選び直す

[取得実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)の**96モデル／1,370files／1,752,033,357,565byte**は実行側のVERIFIED**報告**。所有者Dの今回独立再SHA・ローカル復元・正規取得許諾の代替ではない。旧R140「21候補」うち20repoの同IDが最新ledgerに記録され、新たにその20の全重量を取得するのは重複リスクが高い。

新しい[次期11sourceの非実行審査キュー](../../queues/proposed-v62-r147-post96-next-research-sources.json)は、P0小型端末／時系列群**2,234,744,280byte**、P1マルチモーダル親・無検閲・意思決定群**11,871,408,047byte**、P2映像／シミュレーション**54,438,018,606byte**、P3 Ripple65B **129,572,889,973byte HOLD**。P0〜P2は10repoのPublisher source参照**68,544,170,933byte**。FastFramesのCF++＋Wan親17.567GBやMirage runtime4.138MBはその10repo sourceに含まれない。全て未承認の調査順序であり、本人HDD容量の現在値ではない。

## 5. 規制の事実と予想を区別する

米BIS[2026-11-19 Federal Register §IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は旧AI Diffusion RuleのECCN4E091モデル重み規定を撤廃。オープンウェイト全般や無検閲系のローカル所持が直近に一律禁止されるという一次資料は確認していない。モデル固有の未来takedownは**反証可能なストレス仮説**として研究順位に利用し、現実のGated・利用権利・著作権・国際移転条件とは独立に停止させる。

## 6. H / T / D / C / U

- **H：仮説**。4学習済み成果の保全で、既存227モデル資産から復元できない小型MoEの独立ルーティング、tiny視覚、LFM公式親、Heretic別編集状態が増える。量子化とpublisher同一SHAコードを別モデルとして重複計上しない。
- **T：検証計画**。Publisher不変40桁revisionを前提に、全58選択パス・byte・Git OID/LFS9件を静的検証。旧227件の完全一致、v62有効184件・CONDITIONAL131件と承認0をオフライン試験。本人の実機再構築にはWindows/Linux・CPU/GPU・ドライバ・backend版・quantization/zero-point・context・batchを固定し、モデルごとに代表入力最低30件、事前閾値と逐次停止ルールを定義。
- **D：合否**。選定メタデータ一致・旧227不変・承認0で **PASS**、Publisher SHA不一致やモデルの二重カウントで **FAIL**。本人権利・保存先実空き200GB・全重み/local SHA・依存閉包・安全実装・明示的manifest承認が一つでも欠ければ、**実取得はFAIL-CLOSED**。性能はUNCERTAIN。
- **C：反証ケース**。Auroraの小型活性MoEが汎用能力で著しく劣る、Mirageの専用engineに実機互換性が無い、Hereticのテキスト拒否改善が視覚性能を損ねる、親・派生を二重保存する価値が実用上小さい場合。
- **U：主要不確かさ**。出版社ベンチマークの選別、Heretic評価100例の偏り、専門モデルの外部trained component総数、Cactus4.1.4 Windows wheel/CPU ISA/ABI、本人HDDの実容量・一時領域・実SHA、LFM商用権利、未審査Pythonコードなど。独立反復観測が無く、合成標準不確かさ `u_c` と包含係数 `k` の定量値は未算出。

学際的転用：機械学習（MoE・拒否編集・VLM）、エッジロボティクス（小型画像理解）、ソフトウェアサプライチェーン（SHA・同一trained output・実行ABI）、知的財産・輸出政策（LFMとApache、現行BIS）を共通の保存ポートフォリオで評価する。

**実行境界**：4追加は全て研究用`conditional`、旧227の採否変更・削除0。承認キュー0、今回の重量取得0、未審査ランタイム実行0、本人Dドライブ現物再ハッシュ0。
