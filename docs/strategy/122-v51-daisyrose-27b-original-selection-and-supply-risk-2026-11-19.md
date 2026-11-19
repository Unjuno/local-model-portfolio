# R122｜DaisyRose 27BのBF16原本を1件正式追加、派生量子化を重複採用しない

**2026年11月19日／main v51／204登録・157有効（SELECT53、CONDITIONAL104）**。旧203資産の採否変更0。取得承認・重量ダウンロード・既存削除0。

## 1.〈本論〉原本内部と採否

2026-11-18公開の出版社[RadixArk/DaisyRose-27B](https://huggingface.co/RadixArk/DaisyRose-27B)は[Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)を長期エージェント課題約1200件でRL後学習した別チェックポイント。出版社記載の訓練条件は**144 NVIDIA H200、18日間**（推論速度のユーザー実測ではない）。出版社の[技術解説](https://huggingface.co/blog/RadixArk/daisyrose-27b-pushing-the-frontier-of-post-trainin)はTerminal Bench 4.1 12.0対5.6を報告するが、ベースラインとの完全に同一harness・推論設定かを独立検証できないので優位性は暫定。

2026-11-19にhttps://huggingface.co/api/models/RadixArk/DaisyRose-27B/revision/293a7a2ab54aaea78098ee917c546390667521dc?blobs=trueから34個のPublisherファイルメタデータを検査。固定コミット`293a7a2ab54aaea78098ee917c546390667521dc`、**34files、55586309473byte、LFS SHA256 20件、学習済みweight18シャード**。公式Qwen親`37561816e66b5b9153b1b64c10968c18c1e6f4a0`との重み同名18ファイルをSHA256完全一致比較し、一致**0/18**。異なる重みの別RL学習成果とする十分なファイル同一性上の証拠。ただし出力行動差や業務性能差の実測ではない。内部構成は`config.json`、18 weight shard、`model.safetensors.index.json`、tokenizer、vision processor、MTP学習重みを含み、公式Hub safetensors総要素数27781427952。全学習済みpipeline要素のowner独立再計数は未了。

**CONDITIONAL/R1を1資産追加**：[v51 overlay](../../catalog/revisions/v51-2026-11-19.json)、[原本ファイル34件の固定source](../../manifests/drafts/v51-2026-11-19-daisyrose-27b-bf16-original.candidate.json)。同一学習成果の[FP8](https://huggingface.co/RadixArk/DaisyRose-27B-FP8)、[NVFP4](https://huggingface.co/RadixArk/DaisyRose-27B-NVFP4)は**別資産として不採用**。NVFP4 Hubのtensor element数がBF16より小さく表示されても総学習済みモデル数の別訓練を意味しない。既存のQwen親、無検閲Interpretic/0bserverx、[harness-hubの独立RL LoRA](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted)は別研究用に残す。DaisyRose自体が無検閲版という根拠はない。

## 2. 保存順位と規制の事実

[取得報告ledger](../../catalog/execution/2026-11-19-acquisition-ledger.json)には53モデル・579file・270,835,576,267byteがPublisher一致と記録されるが、今回の調査は所有者Dの現物再ハッシュではない。まず53件の再照合と重複回避。続いて既存R117のZONOS3 Codec／Interpretic BF16／0bserverx F16、R119のRWKV7・iLLaDA・TRELLIS.2等の独立型を優先審査。DaisyRoseは保存対象を確定しても**転送優先順が全候補に優越するとは限らない**。

**確認済み法制度**：[米BISの2026-11-19 IFR IV.A](https://public-inspection.federalregister.gov/2026-23529.pdf)は旧AI Diffusion Ruleのウェイト輸出分類4E091を撤廃。高度半導体・遠隔計算の規制は別に存在する。ローカルの全公開重み保管が一律禁止と決まったという主張は誤り。DaisyRoseの公開Hubは`gated:false`で、近い将来の消失は**仮説**。LICENSE全文の行為別審査、権利と地域、外部依存が独立STOPゲート。ExaはHTTP402のため調査不能で、今回は出版社公式Hub APIと政府一次資料による。

## 3. 変数表と容量の次元チェック

|記号|意味（日本語）|単位（SI）|定義|定義域・前提|型|
|---|---|---|---|---|---|
|`S`|Publisher BF16原本34ファイル長|byte|55586309473|非負、現物実増分ではない|整数スカラー|
|`P`|Publisher原本最大単一ファイル|byte|3988973152|正、固定source|整数スカラー|
|`F`|取得後最低安全空き|byte|200000000000|現行policy|整数スカラー|
|`H`|全ファイル新規取得と二重stage時に必要な参考空き|byte|`S+2P+F`|依存/ランタイム/重複を未考慮|整数スカラー|

`H = 55586309473 + 2×3988973152 + 200000000000 = 263564255777 byte`。byte同士を足すため**単位整合PASS**。Owner Dの現在の空き容量は不明で、これは取得可否の実測ではない。コンテキスト長・batch・GPU VRAM・backend/ABI・zero-point/KVと実測速度を別途確認する。

## 4. H/T/D/C/U・ERROR CHECK

**H**：独立RL後学習成果は既存Qwen親と無検閲編集、LoRAからの単純な変換では再現できない。**T**：Pub SHA18件の同一性比較（本回完了）と、同一HW/driver/backend/clock/batch/context/ハーネスでエージェント30件以上・成功率/中央値時間/ピークRAMを測定（未実施）。**D**：選定PASS＝18SHA非一致、source固定、元203件不変。取得条件＝個人権利・SHA・実HDD空き200GB床・依存・明示承認全て必要。未検証はUNCERTAIN。無断転送はFAIL。**C**：実測で親や軽量adapterとの差が小さければ55.586GBの優先を下げる。**U**：benchハーネス差、owner推論環境、法的行為、ファイル実SHA/外部runtimeが主要不確実性。独立反復がないため合成標準不確かさ`u_c`と包含係数`k`は数値化できない。

**ERROR CHECK**：v51 204登録／157有効／CONDITIONAL104、20 Publisher LFS SHA、34 files 55586309473 bytes、18 weightシャードの親とのSHA一致0、旧203件の採否変更0、新規重量DL/承認/実行/削除0。

関連分野：**強化学習・エージェント評価、デジタル長期保全、ソフトウェア供給網、輸出管理・利用許諾**。

## 5.〈次に考える問い〉

**同条件のエージェント評価でDaisyRoseの実益が既存親・0.638GB級LoRAに対して小さければ、55.586GBの原本を優先保持するべきか。**

