# R149／v63 — 99件取得報告後の11原本：固定scopeの再検証・優先順位の確定（2026-11-22）

## 1. 結論と変更境界

対象：[`catalog/CURRENT.json`](../../catalog/CURRENT.json) の **v63-20261122／235資産・188有効（SELECT55／CONDITIONAL133）**。既存の取得報告は **99モデル／1,478ファイル／1,879,994,309,866byte**。本研究は所有者Windows Dドライブの実ファイルを再ハッシュしていない。取得済み重量とこれから確保するべき重量を混同しない。

前ラウンドの [11ソース非実行キュー](../../queues/proposed-v63-r149-after99-11-research-only.json) を、[今回の機械可読の採否・証拠・STOP](../../catalog/decisions/2026-11-22-r149-v63-next-source-finalization.json) に整理し、**全11repoの40桁revision、219選択ファイル、合計198,117,060,906byteについて、前回Publisher manifestのpath/byte件数・合計・revisionが11/11一致**することをコードで照合した。これはPublisher記録どうしの静的整合であり、今回Hubの全ファイルを再SHAした検査でも所有者ディスク検査でもない。

**確定したのは「次に個別審査する原本とその保存候補scope・優先順位」**である。取得承認・ライセンス行為別許諾・完全依存・実機disk/GPU/ABI・オフライン復元の完了を意味しない。**既存235資産の決定は1件も変更せず、追加モデル0、取得承認0、重量ダウンロード0、既存削除0、未審査コード実行0**。

## 2. 候補11件の確定順位（選択scopeのPublisher参照byte）

| 審査順位 | 原本 | 固定Publisher範囲 | 状態／結論 | 非代替性と停止理由 |
|---:|---|---:|---|---|
| 1 | [mistralai/Timestral-28M](https://huggingface.co/mistralai/Timestral-28M) | **111,307,038 B** | P0・次回個別審査 | 27.8M・21分位点を出力する時系列予測。Modified MITの売上高条件を利用行為別に審査 |
| 2 | [KittenML/kitten-tts-2-pico](https://huggingface.co/KittenML/kitten-tts-2-pico) | **285,879,877 B** | P0・次回個別審査 | 8言語・30声の独立TTS；8言語F32 master、INT4 ONNX、声・G2Pの選択。既定INT8は含まず明示的INT4選択が必要 |
| 3 | [Cactus-Compute/mirage](https://huggingface.co/Cactus-Compute/mirage) | **237,985,863 B** | P0・次回個別審査 | 小型多機能visionの`.cact`と`.safetensors`原本。別のCactus engine・Windows ABIと自動download挙動が未検証 |
| 4 | [AuroraAI-Research/Aurora2-400M-A20M](https://huggingface.co/AuroraAI-Research/Aurora2-400M-A20M) | **1,599,571,502 B** | P0・次回個別審査 | 独立pretrain、FP32 master、400M級total／19M級activeの希少MoE。custom PythonとBaseの品質は別審査 |
| 5 | [internlm/Intern-Decision-0.8B](https://huggingface.co/internlm/Intern-Decision-0.8B) | **1,734,731,370 B** | P1・維持 | マルチモーダル判断の別学習成果。vision／projector・Qwen通知・推論コード審査 |
| 6 | [LiquidAI/LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B) | **3,854,651,108 B** | P1・親として維持 | 後掲Hereticの正確な親。LFM licenseとprocessor/model custom code |
| 7 | [saidutta69/LFM3-VL-2B-heretic](https://huggingface.co/saidutta69/LFM3-VL-2B-heretic) | **5,334,098,126 B** | P1・親と組で維持 | 親とBF16の重みSHAが異なる独立編集成果。Q4+mmprojは同じ学習成果の別実行形態で別資産にしない |
| 8 | [apple/FastFrames-S](https://huggingface.co/apple/FastFrames-S) | **947,927,443 B** | P1・親条件で延期 | Sのcheckpointだけでは不完全。CF++／Wan親**17,567,235,949 B**を別に参照し、Apple AMLRと親の利用権確認 |
| 9 | [OpenMOSS-Team/MOSS-VL-Realtime](https://huggingface.co/OpenMOSS-Team/MOSS-VL-Realtime) | **22,687,497,344 B** | P2・延期 | 動画ストリームの別モデル。実GPU／レイテンシ／custom decoder未検証 |
| 10 | [nvidia/Cosmos3-Nano-Sim-Transfer](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Transfer) | **31,750,521,262 B** | P2・延期 | 世界モデルSim-Transfer；OpenMDW1.1・共有VAE・Cosmos runtime・GPUゲート |
| 11 | [ricursiveAI/Ripple-65B-Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | **129,572,889,973 B** | **P3 HOLD継続** | 65B級の独立原本だが容量・GPU・比較効用・コード安全性の確認不足。取得を承認しない |

P0の4repoは **2,234,744,280 B**。P0～P2の10repoのPublisher参照は **68,544,170,933 B**。上記以外にFastFramesの親 **17,567,235,949 B**、Mirageの4.1.4 runtime選択5ファイル **4,137,947 B** が必要候補。共有ファイルの**所有者現物SHAでの再利用は未証明**なので、この参照サイズを実増分転送量に変換しない。Rippleの129.573GBはP0～P2 68.544GBに含まない。

## 3. 一次情報で確認した技術的罠

### Timestralのライセンスは「MIT」と単純化できない

[配布元モデルカード](https://huggingface.co/mistralai/Timestral-28M)のタグは `other` で、[公式LICENSE](https://huggingface.co/mistralai/Timestral-28M/blob/main/LICENSE)は **Modified MIT License**。前月の世界連結**月次売上高がUSD20 millionを超える会社／雇用主には、このライセンスに基づく権利行使を認めない**条件を含む。個人・組織にとって合法な利用かは別途判断する。作者のGIFT-Eval MASE 0.678とCRPS 0.461は同作者の公表比較値であり、本作業の同一環境測定ではない。

### Kitten Picoの量子化除外とオフライン復元は別問題

[公式モデルカード](https://huggingface.co/KittenML/kitten-tts-2-pico)によれば、`KittenTTS(...)`のデフォルトONNXはINT8。保存候補は**FP32 safetensorsとINT4 ONNX、voice pack・G2P**で、INT8 ONNXを重複変換として除外した。これ自体は訓練成果の重複排除に妥当。ただしINT4の使用には `weights="int4"`、`onnxruntime>=1.20` が必要と公式に明記される。通常のデフォルト起動がINT8ファイルを求めれば、**重み選択が正しくても復元FAIL**。既存manifestを勝手に拡大せず、明示INT4プロファイルでoffline testする。声パックとG2Pの権利はApache2.0との公式声明があるが、利用行為・音声の個別権利を別確認する。

### Mirageは重み単体では動かない

[Mirage card](https://huggingface.co/Cactus-Compute/mirage)はエンジンと重みの初回自動DLを記載する。[Cactusの公式runtime card](https://huggingface.co/Cactus-Compute/cactus)はWindows x64/ARM64を含む対応プラットフォームを列挙。v62では **runtime 4.1.4 revision `f4ab2741203a282c6e7b89983de2b5e5b2e805a8`** のWindows/Linux選択5件を固定しているが、今回のHubカードに例示される4.0.0と**版が違う**。4.0.0の対応を根拠に4.1.4とMirageを動作検証済みとは言わない。ネットワークを止めた実装・DLL/ABI/バイナリ審査・隔離実行が必要。

### AuroraのFP32原本とHereticの別重み

Auroraは公式記述で **399,597,454 total／19,050,382 active**、元はFP32 master。従来manifestのFP16/BF16変換を別学習資産として二重選択しない。モデルカードの `trust_remote_code=True` 例を**信用済み実行許可とはみなさない**。

Heretic編集版のPublisher LFSのBF16重みSHAは `91d527edb09f1e382172c9bf4028247676f92b6c1545f1e4d6b8920b4eba906a`、親LFM3-VL重みは `a9bb8b1c159c9d6c3007bc1c7ad8018b599f759d97da2701714e37426283e131`。異なる学習済み／編集後成果として2つの原本を保つが、親子間の品質・拒否率・危険性は**未測定**。量子化版Q4は別の学習済み成果ではない。

## 4. 法規の事実と仮説を分離

[米国BIS 2026-11-19 Federal Register（一次資料）](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)は2025 AI Diffusion Ruleで導入したモデル重みの **ECCN 4E091を撤廃**した。一方、先端半導体・遠隔計算・エンドユーザ等への規制は別に規定されている。**今後ローカルモデル一般が全面禁止されることは、この資料からは導けない**。

事実：Timestral Modified MIT、Liquid LFM1.0、Apple AMLR、NVIDIA OpenMDW1.1など、モデル単位で権利条件が違う。推論：再配布・改変利用・二次配布の条件変化は技術保存の障害になり得る。仮説：「将来の強力なopen-weight一律禁止で対象repoが削除される」は現時点で**対象・時期・確率を裏付ける一次資料が無く順位に数値化しない**。Gated repoの非正規回避は行わない。

## 5. 次回の検証順序と取得STOP

先に[RFD4-Proteinaの旧catalog revisionと99取得報告の**重みSHAが異なる1件**](../../catalog/research/2026-11-22-r148-ledger99-immutable-revision-drift.json)を、base/root/adapterごとのパス・ハッシュ・用途へ分解する。所有者D現物の読み取り専用SHA結果無しに同一学習成果だと推定したり、削除・上書きしたりしない。

続いてP0 **Timestral → Kitten Pico → Mirage → Aurora2** を「owner個別審査で次に取得するべきsource scope」として確定。選択source pathは既存不変manifestを使用し、該当ライセンスの行為別許諾、実ディスク空き200GB残床・ステージング、SHA／親・codec・runtime、未審査の任意コード実行禁止、明示的なrepo+revision+file+checksum単位の取得承認の全条件が揃わなければ **STOP**。既取得99件の再ダウンロードも禁止。

P1のLFM親＋Hereticは別編集結果を保存する価値があるが、両者を独立に「無検閲だから最優先」とするのは不適切。性能・拒否率・合法性を明確に別々に比較する。FastFramesのS重量の小ささで親source費用を過小評価しない。P2大型2件は実GPU/ABIの前に重みDLしない。P3 RippleはHOLD。

## 6. H / T / D / C / U

- **H（反証可能仮説）**：上記11repoのPublisher選択ファイルと固定revisionが既存4つのmanifestに一致し、99既取得repoとID重複なしで調査の優先順位を付けられる。2026-11-22時点、source metadata11件・219pathを対象とする。
- **T（最小検証）**：4manifest＋R149キューをファイル読み取りだけで比較。11/11 revision、file count、合計byte、git blob/LFS証拠の有無、approved queue0件をassert。実機n_minは別セッションで各対象1ローカル復元（8言語Kittenは8言語ごと動作）と、ローカルSHA検査。逐次停止は最初のハッシュ差異・権利未確定・オフライン依存の未閉包。
- **D（合否）**：11件の静的結合は **PASS**。取得承認とowner実ファイル一致・rights・runtime・offline restoreは **UNCERTAIN／STOP**。重みを同一視する・暗黙承認を生成する・不明runtimeを実行した場合 **FAIL**。
- **C（破れ方）**：配布元mutable cardのライセンス変化、同名別重み、親差分、デフォルトINT8要求によるKitten復元失敗、CactusバイナリABIの非互換、FastFramesの親を既取得と誤認、予測ベンチマーク不再現。
- **U（不確かさ）**：Hub公開可視性≠個別許諾、Publisher Git OID≠owner重量SHA、共有VAE/codec未検証、GPU条件（メーカー・VRAM・ドライバ・batch・context・quant backend・zero-point）未確定。測定系列が無いので合成標準不確かさ `u_c` と包含係数 `k` は算定しない。

学際的な転用：①MLアーキテクチャと希少な独立学習原本の保全、②音声・動画のofflineシステム設計、③ソフトウェア供給網のimmutable SHA追跡、④契約法・輸出管理と権利の個別検証。

**本ラウンドの唯一の本番変更**：静的な意思決定台帳と研究・検証資料。重みデータ、承認キュー、正式v63の235件の採否、owner媒体には変更を加えない。
