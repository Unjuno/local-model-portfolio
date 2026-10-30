# 第3次AIモデル選定案 — 2026-10-30

> **レビュー用。現行台帳には未適用、ダウンロード承認ではない。** 2026-10-30時点でGitHub接続経由の現行v2台帳と、配布元の公式HFページ/公式GitHub実装を照合した。

## 目的と前提

- 正本は `catalog/CURRENT.json` が指定する初期97件 + v2差分。**現行は110件追跡・94件有効**。この文書と `catalog/revisions/v3-proposals-2026-10-30.json` は提案であり、`CURRENT`を変更しない。
- [選定基準](../policies/selection.md)の優先順位は、(1)観測済みアクセス制限、(2)専門学習成果の再現困難性、(3)異なる能力、(4)容量と実行可能性。モデルの人気だけでは採用しない。
- 取得予算は十進 **3,800,000,000,000 B**、空き容量原則 **200,000,000,000 B以上**、想定ピークRAM **512,000,000,000 B未満**。3/4bit量子化時にもOS・バックエンド・KVキャッシュ・バッチ・コンテキストを含める。
- 選定候補は既存97件、v2追加13件、旧一括レビュー119件、リスク監視29件と正確なrepo IDで照合。下記7件に一致はなかった。

## 今回の追加7件

| 優先度・案 | 公式資産 | 配布元表示の全repo容量（概数） | 保存固有価値・代替との比較 |
| --- | --- | ---: | --- |
| R0・条件付き | [pyannote Community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) | Gatedのため未確定 | ASRとは別の話者分離。segment/embedding/PLDAを含む完成済みのローカル処理系 |
| R0・条件付き | [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) | Gatedのため未確定 | 音楽生成・TTS以外の効果音/環境音をテキストから生成するDiT系 |
| R1・選定案 | [Microsoft Aurora](https://huggingface.co/microsoft/aurora) | 約41.2 GB（複数版合算） | 地球物理予測。Chronos-2の一般時系列予測とは別の入力と専門学習 |
| R1・条件付き | [Boltz-2](https://huggingface.co/boltz-community/boltz-2) | 約6.2 GB | 生体分子複合体構造・結合親和性。既存ESM2の配列Encoderとは別能力 |
| R1・選定案 | [Prithvi-EO-2.0-300M-TL](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL) | 約1.34 GB | 6波長帯・時間・位置を使う衛星観測モデル。RGBモデルの単純代替不可 |
| R2・選定案 | [SAM2.1 Hiera Small](https://huggingface.co/facebook/sam2.1-hiera-small) | 約0.369 GB | GatedのSAM3に対する独立した公開セグメンテーション基準 |
| R1・選定案 | [Depth Anything V2 Small](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) | 約0.0992 GB | 相対深度推定（24.8M）。3Dアセット生成やVLMの代替ではない |

分類は **R0 2件、R1 4件、R2 1件**。4件の`select`案と3件の`conditional`案。適用した場合の単純件数は117件追跡・101件有効だが、まだ現行確定値ではない。

## 観測事実と未検証の問題

1. **pyannote Community-1**: [公式カード](https://huggingface.co/pyannote/speaker-diarization-community-1)にGated・利用条件同意・CC-BY-4.0・offline useの記載。話者分離エラー率の比較は配布者報告であり、ユーザーの日本語音声・実機での独立再試験ではない。権利同意はユーザーが行う。
2. **Stable Audio Open 1.0**: [公式カード](https://huggingface.co/stabilityai/stable-audio-open-1.0)、[LICENSE](https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md)。Gated・独自コミュニティライセンス。商用利用について別途案内あり。safetensors約4.85GBとckpt約4.85GBは同一モデルの代替形式の可能性があり、取得前に照合する。
3. **Aurora**: [公式HFファイル一覧](https://huggingface.co/microsoft/aurora/tree/main)は多数のモデル版を含む。例として`aurora-0.25-v1.5.ckpt`約5.03GBと対応static約0.15GBを検討するが、選択ファイルは未固定。[公式実装](https://github.com/microsoft/aurora)はMITで、商用について問い合わせ案内がある。科学的性能を運用保証としない（原論文 DOI: [10.1038/s41586-025-09005-y](https://doi.org/10.1038/s41586-025-09005-y)）。
4. **Boltz-2**: [HFファイル一覧](https://huggingface.co/boltz-community/boltz-2/tree/main)には`boltz2_aff.ckpt`、`boltz2_conf.ckpt`、`mols.tar`。公式[実装・利用条件](https://github.com/jwohlwend/boltz)はMIT。MSAサーバーを使う実行例をそのまま『完全オフライン』と呼ばず、ローカルMSAの用意と隔離されたckptの検証が必要。
5. **Prithvi**: [公式ファイル一覧](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL/tree/main)に`Prithvi_EO_V2_300M_TL.pt`約1.33GB。Apache-2.0。TerraTorch・6バンドHLS入力・位置/時間前処理が必要。`.pt`にはpickle由来の読み込みリスクがある（[論文](https://arxiv.org/abs/2412.02732)）。
6. **SAM2.1**: [公式ファイル一覧](https://huggingface.co/facebook/sam2.1-hiera-small/tree/main)はApache-2.0、safetensorsとptがそれぞれ約184MB。両形式を必ず両方保存する前提にしない。SAM3はGatedだが、代替モデルの同等品質は未検証。
7. **Depth Anything**: [公式ファイル一覧](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf/tree/main)はApache-2.0、safetensors約99.2MB。単眼の**相対深度**を推定するもので、実世界メートル単位の校正済み測距ではない（[論文](https://arxiv.org/abs/2406.09414)）。

## 冗長性による今回の見送り

- `facebook/musicgen-small`: YuE2等と音楽生成が重なる。CC-BY-NC-4.0条件もあり、音楽生成ベンチを事前に定義するまでは追加しない。
- `biohub/esm3-sm-open-v1`: 既存ESM2とは異なる生成機能があるが、上流配布条件の本文・正式配布元・実行依存をこのラウンドで確証できないため追加しない。
- 既存のFLUX3蒸留版/Baseや医療モデルは学習成果が異なる可能性があるため、容量の大きさだけで機械的に降格しない。

## 選定から取得承認へ進むための検証手順

| 項目 | H: 検証仮説 | T: 最小試験 | D: 合否 | C: 破れ方と対立仮説 | U: 主な不確かさ |
| --- | --- | --- | --- | --- | --- |
| 正規取得 | 現行の権利と供給が有効 | 固定40桁revision、選択ファイル全件、利用条件本文を取得・照合 | PASS=リンク/権利/依存が整合、FAIL=拒否/禁止、UNCERTAIN=情報不足 | Gatedの同意が不成立、非商用条件と利用目的が衝突 | ライセンス解釈、配布者の将来変更 |
| 容量・再現 | 選んだ構成が保管・再現可能 | 正確なバイト、全ファイルSHA-256、必要ランタイム、3/4bit量子化の実装可否を検査 | PASS=3.8TB枠内・実空き200GB以上、推定ピークRAM512GB未満、再現環境が固定。UNCERTAIN=未知 | 全repo表示が重複版を含む、依存が別repo、pickleを安全にロードできない | 依存容量、backend/コンテキスト/バッチによるRAM変動 |
| 専門性能 | 少なくとも一つの新たな利用機能を既存モデルより提供する | 用途別データを事前に固定し、各機能少なくとも30独立例で対照比較（条件によって増量） | PASS=事前登録した機能別基準を満たす。FAIL=明確な劣位・機能未成立。UNCERTAIN=少数例/未測定 | 入力形式やモデル間の公平な比較不能、計測環境差 | 標本偏り、バッチ、言語、GPU/CPU、精度、測定誤差（合成値未推定） |

性能試験の実施条件（CPU/GPU、クロック、バッチ、コンテキスト、OS、推論器版、データ権利）と閾値は**試験前**に固定する。30例は最低のスクリーニング設計値であって、統計的な精度保証ではない。

## 容量評価で断定しないこと

v2の`catalog/CURRENT.json`には `provisional_active_repo_bytes_plus_fineweb_sample` = **3,234,067,678,260 B**、暫定余裕 **565,932,321,740 B** とある。どちらも**旧v2の上流全repo概算を用いた仮計算**であり、選択ファイルの精算でもv3追加分を含んだ収容保証でもない。

今回7件の `upstream_all_files_bytes_observed`、`selected_file_bytes`、`fully_pinned_revision_sha` は全てnull。UIの丸められた表示値を確定バイトやSHAに読み替えない。

## 次の安全な操作

1. ユーザーが同意条件を判断できるよう、R0の2件の配布条件とGated状態を再照合する（同意操作やダウンロードは行わない）。
2. 公開・小型のPrithvi/SAM2.1/Depth Anythingについて1件ずつ完全revision・単一の採用表現・依存物のバイト数を固定した**未承認**マニフェスト案を作る。
3. Auroraは複数checkpointから代表1版、Boltz-2はMSAを含む完結構成を確定して保存予算を再計算する。
4. 上記ゲートを通過した項目のみ、別PRで`catalog/CURRENT.json`に追加する。このレビューだけでは `queues/approved.json`、HDD実機、モデル本体は変更しない。
