# R143 / v60：小型独立学習モデル3件の正式選定と96件取得報告の反映（2026-11-22）

## 目的と結論

本リポジトリは、将来の公開終了・Gated化・利用条件変更に備え、**消えると再現が困難な学習成果とローカル実行能力**を重複なしで保存する。モデル名の「uncensored」・話題性・出版社ベンチマークだけでは採用しない。v59の221件を一切変更せず、新たに小型3独立学習成果を **conditional（研究用、実取得不可）** として追加する。現行 **224登録／177有効（SELECT53・CONDITIONAL124）**。

正式ソース：[v60差分](../../catalog/revisions/v60-2026-11-22.json)、[59ファイル不変publisher参照](../../manifests/drafts/r143-2026-11-22-three-specialists-originals.candidate.json)、[機械可読の採否・反証可能性](../../catalog/decisions/2026-11-22-r143-v60-three-small-specialists.json)、[177件readiness](../../catalog/readiness/v60-2026-11-22-r143-all177-gates.json)。取得を承認するものではない。

## 選定の具体的な判断

| 対象・Publisher一次元データ | 正式判定 | 独立能力と代替比較 | 停止理由 |
|---|---|---|---|
| [mistralai/Timestral-28M](https://huggingface.co/mistralai/Timestral-28M/tree/49b26409ac87b5935539a5d8ffe7f397b720db47) | CONDITIONAL、F32原本6ファイル111,307,038byte | 27,821,184 F32学習済み要素、patch-based Transformer、欠測・共変量対応、21分位点。既存IBM TTMとは違う確率時系列成果。発行者のGIFT-Eval MASEは28Mが0.678、209Mが0.658。約7.5倍大きい209Mは品質が有意に必要と確認できるまでHOLD | Modified MIT：前月の会社・雇用主の連結月商が2,000万USDを超えると本ライセンスの権利を行使できない。対象の利用者・行為の確認、固定コード・実機精度は未検証 |
| [internlm/Intern-Decision-0.8B](https://huggingface.co/internlm/Intern-Decision-0.8B/tree/42457fafd13d10d0b0d9be46cb30a23caa409994) | CONDITIONAL、BF16原本20ファイル1,734,731,370byte | 852,985,920要素のQwen3.5派生、言語・視覚・projector重みを含む。単一forwardで複数choice/score/noulの確率を読む別の学習成果。既存Kanana3.665Bと対照し、小型である点を独立保存理由とする | upstream LICENSE-QWEN、作者inference.pyのtoken位置取り、温度較正、PyTorch/transformers ABI、親の通知と学習データ権利は使用者環境未検証 |
| [KittenML/kitten-tts-2-pico](https://huggingface.co/KittenML/kitten-tts-2-pico/tree/a5632deac7d92f6178db814d933eba746a97f2dc) | CONDITIONAL、F32＋INT4 ONNX 33ファイル285,879,877byte | 8言語それぞれ約7.2Mの別重み、30音声、24kHz。既存Mini82Mより端末制約が厳しい用途用。**F32原本8件、INT4 ONNX8件、音声パック・G2Pを一資産に同居**させ、同じ成果のINT8 ONNX8件（計63,628,208byte）は追加保存対象から除く | 総学習済み要素を言語別重み・G2P・音声埋め込み込みで一意に数え終わっていないためパラメータ最終ロック不可。ONNXRuntime 1.20+とG2P動作／本人権利・32bit原本の復元未検証。日本語はPicoの対象外 |

## 出版社ファイルの厳密な容量

全3配布元の全67ファイルは **2,195,546,493byte**。そのうち採用する **59ファイルは2,131,918,285byte**、作者のSHA256（LFS）参照は**30件**。選択しないのはPicoの8個のINT8 ONNX形式のみ。正確なimmutable revision（40 hex）、選択path、サイズ、LFS SHA256とGit blob OIDはマニフェストに固定した。

**この数値は公開元ファイル集合の容量であり、所有者HDDの保存量や依存を含む推論メモリではない。** Timestral本体には [mistralai/timestral@a534bdbd](https://github.com/mistralai/timestral/tree/a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff)、Internには [internlm/Intern-Decision@a7b01e2](https://github.com/internlm/Intern-Decision/tree/a7b01e276cd5e18bae640be925e685ba6f5159ad)、Kittenには [KittenML/KittenTTS@5802f6b](https://github.com/KittenML/KittenTTS/tree/5802f6b956844919ecf210f4e55f4750a6ad7c6f) のコードを指定。依存閉包、配布許諾・コード安全性、オフライン復元は未確認。

## 別の能力は調べたが正式選定しない

- [apple/FastFrames-S](https://huggingface.co/apple/FastFrames-S)：新しいKV refinement / pixel-decoderは独立価値がある。ただし公開repo約1.788GBの補助重みだけではWan2.1-T2V-1.3B基盤・Causal Forcing++依存が揃わず、Apple研究用ライセンス、Linux x86-64/CUDA12.8と著者のB200での35.4ms/frame条件は本人ハードで再現未確認。研究HOLD。[一次論文 arXiv:2611.23226](https://arxiv.org/abs/2611.23226)。
- [Cactus-Compute/mirage](https://huggingface.co/Cactus-Compute/mirage)：画像理解重み216MB・専用cact runtime約21MBは小型で価値があるが、実行エンジンのバイナリ完全保全とライセンス・品質を静的に閉じられないためHOLD。
- [LG-AI-Research/EXAONE-Tabular](https://huggingface.co/LG-AI-Research/EXAONE-Tabular)：20〜21M classifier/regressor ensemblesは小さいが、重みは非商用条件、既存Kumo/Tabular系との比較と全複数重みの独立性が未検証のためHOLD。
- [mistralai/Timestral-209M](https://huggingface.co/mistralai/Timestral-209M)：28Mとは別の学習済み重みだが、今は28Mの低容量・広い確率予測を先行させ、209Mの実用的な品質差を独立試験までHOLD。

## 既存の96件を無駄に再取得しない

取得台帳 [2026-11-19-acquisition-ledger.json](../../catalog/execution/2026-11-19-acquisition-ledger.json) は**96モデル／1,370ファイル／1,752,033,357,565byte**のVERIFIEDを**報告**し、1件Gated HOLDも記載。研究側は今回、保有者のWindows Dを独立再ハッシュしておらず、実行報告＝ユーザーの全権利・offline restoreの証明ではない。新3対象は取得台帳の既存repo一覧に無く、まずP0でTimestral28MとPicoの事前審査、P1でInternDecisionを審査する。旧R140の「76件時点の次21source計画」は履歴であり現在の取得済み件数と誤認しない。

## 法的事実と将来仮説を分離

2026-11-19の [米BIS最終暫定規則・§IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm) は旧AI Diffusion Ruleのモデル重みECCN 4E091を撤廃した。**モデルの一律ローカル所有禁止や、今回3対象の削除予定を意味する一次資料は確認できない**。配布規約の制限、Gatedの本人同意、別の輸出先・最終用途規制は独立した現実のSTOP。将来の公開停止シナリオを政策事実と混同しない。

## H / T / D / C / U（反証可能な検証）

- **H**：3新系統により確率時系列・非生成型判断・超小型音声を追加し、公開元参照2.2GB未満で同一学習成果のINT8複製を排除できる。
- **T**：公式3つの40桁不変SHAと59件のpath/bytes/OIDを全件静的照合。旧221件の完全一致、sidecar有効177件と条件付き124件、取得承認ゼロをオフラインテスト。実機品質比較はHW、ドライバ、backend/ABI、zero-point、context、batchとタスク集合を固定し各モデル最低30試行。最初の不変SHA、利用条件、親モデル不一致で逐次停止。
- **D**：静的整合が全一致なら選定PASS。1件でもSHA/ファイル不一致はFAIL。使用者の権利・HDD・ABI・品質・オフライン復元は未確認ならUNCERTAIN、取得判定はFAIL-CLOSED。
- **C**：Timestral209Mの精度差が用途上大きい、Internのtoken位置・校正が壊れる、Picoの音質/言語範囲/推論速度がMiniに劣る、という対立仮説を残す。
- **U**：原作者のみのベンチマーク、データリーク・使用権利、所有者HDD・全依存・CPU/GPU差、int4 zero-point/ONNXバージョンが主要因。独立反復誤差を取得していないため合成標準不確かさ u_c および包含係数 k は未算出。

## 結果と関連分野

研究領域：①機械学習（独立学習成果・確率較正）、②ソフトウェアサプライチェーン（immutable SHA・runtime）、③法政策・知的財産（行為別権利・輸出）、④エッジシステム工学（CPU推論・メモリ・容量）。

取得前停止：モデル/ライセンスごとの本人権利、全trained components、ソフトウェアABI、実HDD最低空き200GBとstage/cache、取得後の現物SHA/オフライン復元、そして [queues/approved.json](../../queues/approved.json) の明示承認が必要。**今回は取得承認0、モデル重量ダウンロード0、既存削除0、未審査モデルコード実行0**。保全の有効性は現物のオフライン再構築確認後にのみ判定する。
