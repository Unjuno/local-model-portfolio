# v14：Nanbeige維持・低優先6件を選定除外（2026-11-04）

## ユーザー指示の反映

- **維持・正式selectへ変更**：`Nanbeige/Nanbeige4.3-33B`。33B級Denseの独立した研究価値を優先。大容量・推論負担は認識したうえで保持。**取得承認ではない**。
- **有効選定から除外**：下表6件。選定カタログに履歴を保持し、取得候補キューから取り除いた。X:ドライブの既存ファイルや実行中ダウンロードには触れていない。

| repo ID | 旧状態 | v14 | 判断 |
|---|---|---|---|
| `nvidia/nemotron-labs-unified-asr-0.6b` | conditional | **excluded** | ユーザー指定の選定除外 |
| `PerceptronAI/Isaac-0.2-2B-Preview` | conditional | **excluded** | ユーザー指定の選定除外 |
| `qvac/TranscribePsy-250M-EU` | conditional | **excluded** | ユーザー指定の選定除外 |
| `state-spaces/mamba-2.8b` | select | **excluded** | ユーザー指定の選定除外 |
| `Wigtn/KoGovDoc-Bench` | conditional | **excluded** | ユーザー指定の選定除外 |
| `Wigtn/Qwen3-VL-2B-WigtnOCR` | conditional | **excluded** | ユーザー指定の選定除外 |

## 範囲と未解決
この操作は直前に提示した**第1表の7件**に対するもの。第2表の大型モデル（Llama 4 Scout、Meditron3-70B、FLUX.2-dev、Mistral Small 4等）は別途「悩む」対象だったため、**この変更で一括削除しない**。またRWKV/iLLaDA等の異なる技術系列は維持。

現行134件、選定92件、HOLD24件、EXCLUDED6件、deferred12件。150B超の量子化例外2件はHOLDのまま。モデル総数未確認12件は取得準備禁止。ライセンス・固定SHA・選択ファイル容量・実機性能・明示承認の条件を維持。

## ERROR CHECK
- 134件ID一意、選定92件、取得候補92件、ID集合一致。
- 除外6件は取得候補0件。
- Nanbeigeは`select`、パラメータ数33.119B（Hub由来）、Denseの実機性能は未測定。
- ダウンロード承認0件、実ファイル削除0件。
