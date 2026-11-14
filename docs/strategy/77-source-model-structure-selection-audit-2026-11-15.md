# R77 | 実モデル構成に基づく選定差分監査（2026-11-15）

対象: main / v32 / 182資産。今回の変更は**既存モデル2件の実体照合と取得スコープ修正指示**であり、モデル本体の取得・実行・承認ではない。

## 1. Tencent Qwen3.8-27B-DSpine-b16 — CONDITIONAL維持、設定整合性ゲート追加

一次資料:
- https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/tree/main
- https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/main/config.json
- https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/main/model.safetensors
- https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/main/README.md

2026-11-15に公開ページを確認。配布元repoの実ファイルは `.gitattributes`, `LICENSE`, `README.md`, `config.json`, `model.safetensors` の5件（4.05GB表示）。重みの公開Xet SHA256は `ac90f1df842ea66b23e4224f3e86624add547526f689ffe9e9c6b7a5937116b1`。公開ツリーの最新コミット表示は `260a6c2`（短縮表示であり、固定40桁revisionではない）。

重要: 公開検索で取得された `config.json` の版には `architectures: [\"DFlashDraftModel\"]` がある一方、ツリーには `Set architectures to DSpineDraftModel` という後続コミットが表示される。**検索キャッシュの設定内容を最新固定版と混同してはいけない**。旧configと新重みを混在させない。配布元の実行例は `--speculative-algorithm DSPINE`, SGLang/FA3、`--trust-remote-code` を要求する。これは安全な自動実行許可ではない。

**判定:** 学習済みドラフターとしてCONDITIONAL維持。追加モデル数0。最終取得LOCKはHOLD（固定40桁commitのconfig/weights同一版照合、コードcommit、ターゲットQwenのrevision、必要な独自実行コードの静的監査まで）。通常のDFlashやQwen本体の重複保存は行わない。

## 2. NVIDIA RFD4-Proteina — 統合済みrootのみ選択、Base/LoRAは別目的

一次資料:
- https://huggingface.co/nvidia/RFD4-Proteina/blob/main/release-checkpoints.json
- https://huggingface.co/nvidia/RFD4-Proteina/blob/main/README.md
- https://huggingface.co/nvidia/RFD4-Proteina/blob/main/provenance.json
- https://huggingface.co/nvidia/RFD4-Proteina/tree/main

公開release manifestの `model.safetensors` は**1,742,660,596 byte / 435,622,465 stored parameters**、SHA256 `5b549dd61adb2f6c6b5cb95bda13f40f5e31556b4e6c755edc0ca6f011c68fb0`。これはflowと互換autoencoderを含むLoRAマージ済みbundle。 `base/model.safetensors` は別の事前学習状態（同サイズ）、`adapter/adapter_model.safetensors` は8,264,360 byteのLoRA。base＋adapterの機能的再構成とrootを**別々の独立モデルとして数えない**。ただし、学習過程・差分研究が保存目的ならbase＋adapterを独立追加する理由はあり得る（今回未採用）。

releaseはlatent dimension=32、residue vocabulary=147。旧版の16/33と混用不可。配布元はoptimizer/scheduler/loop stateが除かれた推論・fine-tune初期化用EMA exportであり、**中断学習を完全再開できるcheckpointではない**と明記。

**判定:** 既存CONDITIONAL維持、root `model.safetensors` と対応 `config.json`, `LICENSE`, `README.md`, `release-checkpoints.json`, `provenance.json`, `inference.yaml` を優先範囲とする。全repo（現行表示約107GB）、旧checkpoint、base/adapter、oracle、runtime container、学習データは一括取得しない。公開provenanceにコードrevision `5248e9a15` の短縮表記があるため、完全commitと依存環境の確定は未完了。

## 3. 変更判定と残余リスク

| 資産 | 採否 | 取得範囲変更 | 新規資産 |
|---|---|---|---:|
| tencent/Qwen3.8-27B-DSpine-b16 | CONDITIONAL維持 | config/weightの同一revision、実行コード互換性をLOCK条件に追加 | 0 |
| nvidia/RFD4-Proteina | CONDITIONAL維持 | root統合bundle優先、base/adapter/旧checkpoint/全repoを選択外に明示 | 0 |

これらは**公開元のモデル構成とmanifestを読む監査**。重みファイルをローカル取得してテンソル内容を再計算したものではない。公開SHAは発行者提示値でありローカルSHA検証ではない。v32全182件の最終入替監査完了を意味しない。実HDDの保存済み状態は不明。

### 検証ゲート
- H: 既存2件は独立した学習成果として残す価値があり、同一成果の派生形式を重複採用しない。
- T: 公式README、config、release manifest、公開重みSHA、ファイルツリーを比較。n=2モデル。
- D: RFD4のroot統合関係はPASS（配布元宣言）。DSpineの最新同一commit設定整合性はUNCERTAIN。両者の実機再現・権利・取得承認はUNCERTAIN。
- C: HF検索キャッシュが旧版configを示す、重みと設定の異版混在、LoRA統合済み重みとBase＋adapterを重複計上する。
- U: API観測時点、固定revision、実機環境の不確かさは未定量。測定反復がないためu_cとkは算出しない。

ERROR CHECK: v32の182資産・135有効選定を変更していない。新規資産0、除外0、承認0。重みSHAは配布元提示値のみ。

関連領域: 機械学習アーキテクチャ、デジタルアーカイブ、ソフトウェア供給網、ライセンス管理。
