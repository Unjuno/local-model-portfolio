# R90｜v40正式選定：GroundingPI原本採用、Thinker-WM保留（2026-11-15）

## 1.〈本論〉選定変更
**v40＝195登録（169モデル・26データ）／148有効（SELECT53＋CONDITIONAL95）**。旧v39の194レコードは完全一致で保持。[GroundingPI](https://huggingface.co/GroundingPI/GroundingPI)を独立後学習したBF16原本1件としてCONDITIONAL研究採用。Qwen3-4B 36層とKimi由来MoonViT視覚27層を統合、点・矩形・OCR/GUI位置を0～999の座標トークンとして生成。一般OCR、SAM3のマスク、Fara GUI、Praxisのロボット行動とは異なる学習済み原本であり量子化複製ではない。性能優位は著者報告で独立測定なし。[原論文](https://arxiv.org/abs/2609.39601)。

[HF固定revision](https://huggingface.co/api/models/GroundingPI/GroundingPI/revision/afe658ba07cc47168371d69cc66b40ae9dcede7c?blobs=true)で、全4,843,664,384 BF16パラメータ、2重み9,687,403,168byte、[28ファイルの候補source](../../manifests/drafts/v39-groundingpi-source28.candidate.json)合計9,704,102,624byteを確認。9デモ媒体101,805,168byteは候補除外。SHA-256（配布元）第1重み`2ff67831e10766e557311324b3ed5b31864baeb8363a5aef07e876c69afa6de1`、第2`08137c2be794e4932acfca2adac89e290f5ec0b3bb60d63ee7fb1ddc6a9501d2`。local保存を検証した数値ではない。[全source及びThinker比較](../../catalog/research/2026-11-15-r88-groundingpi-thinker-original-license-comparison.json)。

**ライセンス**：[GroundingPI原文](https://huggingface.co/GroundingPI/GroundingPI/raw/afe658ba07cc47168371d69cc66b40ae9dcede7c/LICENSE)のApache-2.0は作者原著部分であり、[Kimi-K3原文](https://huggingface.co/GroundingPI/GroundingPI/raw/afe658ba07cc47168371d69cc66b40ae9dcede7c/LICENSE-Kimi-K3)由来モデル部分に条件（notice、一定MaaS商用売上で別途契約、一定規模製品の表示）が残る。HFはprivate:false gated:falseだが個別権利の最終承認ではない。

**再現ABI**：[作者コード](https://github.com/groundingpi/GroundingPI/tree/98641f0b8ed94a091f1457e0e624c49c0ebf3876)はLinux x86_64、Python3.12、独自Transformers5.7.0 fork、vLLM0.18.x、BF16/context16384・単画像batch相当1、検証GPUはB300/B200/H200/H800等。ユーザーHW、ドライバ、ピークRAM、zero-point、外部ライブラリ・オフライン復元の完全性は未検証。モデル本体・任意コードDL/実行なし。

**Thinker-WMは研究HOLD**：RGB＋metric-depth＋ロボットactionの独立学習価値があるが、主重み25,022,451,471byteのpickle .bin、CC BY-NC-SA4.0、Praxis/Cosmosと比較した実測の増分・実機容量が未確認。Wan2.2 VAEの公開SHAは既存Wanモデルと一致し論理上は二重保管を不要とするが、所有者のHDD同一性未確認。

## 2. 規制上の位置づけ
[EU AI Act執行ガイド](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act)は一定条件でモデルの公開制限を求める制度を説明する。ただし**公開ウェイト全体のローカル保存禁止ではない**。S1→S2→S3配布制限の拡大はストレス仮説、個別モデル禁止確率と実際のGated・LICENSE改定は区別する。

## 3. 変数表・次元チェック
| 記号 | 意味（日本語） | SI準拠単位 | 定義／範囲と前提 | 型 |
|---|---|---|---|---|
| P | 全BF16パラメータ | 1（個） | 4,843,664,384、公式索引 | 非負整数 |
| B1 | 第1重みファイル | byte | 4,995,018,360、配布元 | 非負整数 |
| B2 | 第2重みファイル | byte | 4,692,384,808、配布元 | 非負整数 |
| Bt | indexのtensor payload | byte | 9,687,328,768、配布元 | 非負整数 |
| Bs | 28原本候補ファイル | byte | 9,704,102,624、配布元 | 非負整数 |
| Bd | 除外デモ媒体 | byte | 101,805,168、配布元 | 非負整数 |

BF16は2byte/paramなのでP×2byte＝Bt。B1+B2＝9,687,403,168byte、差74,400byteはヘッダ等。Bs+Bd＝9,805,907,792byteで37ファイル合計と整合。4TB計画と最低200GB物理空きへの適合は**実測なし**。

## 4. H/T/D/C/U・ERROR CHECK
**H**：独立座標トークン学習成果の保存は同一学習済みモデルの量子化重複より固有能力を維持。**T**：固定repo37ファイル/28候補、2重み、3 LICENSE、v39 194旧レコードとv40の148 activeの一意性と4台帳を静的照合。**D**：選定1件・publisher sourceとID整合PASS、完全権利/HDD/local SHA/復元UNCERTAIN、無許可DLはFAIL。**C**：既存SAM/OCR等と同等位置定位、またはThinker-WMが明確な優位と安全実装を示す場合再評価。**U**：作者バイアス、ハード・runtime/ABI、ライセンス権限、ディスク実容量は未知でu_cとkの算定は不能。

**ERROR CHECK**：旧194件完全維持、新1件＝195／148有効（SELECT53/CONDITIONAL95）、Gated20、総数不明の有効9、取得承認0、重みDL0、unsafe実行0。学際領域：VLM、ロボット知覚、デジタル保存、ソフトウェア供給網・AI政策。

## 5.〈次に考える問い〉
**候補を増やすより、既存選定の所有者HDD・権利・完全runtimeの停止条件を何件解消すべきか？**
