# R21：探索を止め、既存2候補の保存ファイルを固定する

確認日：2026-11-05。基準main：`bb20725940694ca85548b3bad8ed10fa663d78e6`。

## 1. 今回完了した範囲

新候補の拡大は行わず、R19/R20で条件付き推薦した2件について、4リポジトリの固定コミット、47ファイルの正確な配布元表示バイト数、重み10ファイルすべての配布元SHA-256、設定・ライセンス等のGit blob IDを記録した。主目的は、消える前の保存に必要な具体的なファイル構成を詰めること。

[準備順位台帳](../../catalog/preparation/2026-11-05-priority-packages.json)と[固定ファイル候補台帳](../../manifests/drafts/round21-pinned-preservation.candidate.json)を追加した。**後者は最終lockでもダウンロード承認でもない。** CURRENTはv17、142資産・有効97件のまま。Nanbeigeと除外6件、approvedキュー、実機HDD・進行中ダウンロードは変更していない。

## 2. 固定した保存構成

| 順 | 保存対象 | 固定版 | 選択ファイル容量 | 今回の到達点 |
|---|---|---|---:|---|
| 1 | ChatR Omni画像LoRA＋Qwen-Image-2.1原本 | adapter `aa213272180d6ad0d03f5fb3d597f0f0322647c5`、base `790c92633540aa0cb11d9abf19eb46d861714758` | **33,802,789,787 B**（35ファイル） | adapter、DiT2シャード、encoder4シャード、VAE、processor、scheduler、index、利用条件・使用例まで列挙 |
| 2 | Interpretic Qwen3.8-27B-Uncensored-v2 Q4＋画像projector＋元モデル資料 | GGUF `e6924b3a08765341e01546308ccf2683d43e880b`、source `69227901b022d2a039fe52e220383f0b79517063` | **17,738,357,352 B**（12ファイル） | GGUF2ファイルとREADME/SHA256SUMS、元LICENSE・config等7資料を列挙。BF16重みの重複取得はしない |

2組をどちらも新規保存するモデル・資料分は **51,541,147,139 B（十進約51.541GB）**。OS、推論ランタイム、Pythonパッケージ、ダウンロード一時領域、キャッシュはこの値に含まれない。

ChatR内訳：base **33,131,616,412 B**、adapterリポジトリ一式 **671,173,375 B**。adapter重み単体は **671,151,136 B**。baseの全選択ファイルが同じ固定版・ハッシュで既に存在する場合だけ、増分を671,173,375 Bとして扱える。既存ディスクを検査していないため実増分はnull。

Interpretic内訳：重み2件 **17,738,321,536 B**、GGUF側の補助資料5,689 B、元モデル側の資料30,127 B。画像を使わないテキスト用途ならprojectorは実行時必須ではないが、今回は視覚能力の保存用として含めた。別の量子化レベルや元BF1618シャードを同時取得する計画にはしていない。

## 3. 新しく閉じた確認事項・未解決事項

### ChatR

[作者カード](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/blob/aa213272180d6ad0d03f5fb3d597f0f0322647c5/README.md)は本日更新。**推奨35ステップ／CFG5.0**へ変更された。掲載されている2×RTX4090 24GBの時間は旧25ステップ／CFG4.0の単発チェックであり、新設定の実測として使わない。GPUクロック、性能の独立再現なし。

固定[requirements](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/raw/aa213272180d6ad0d03f5fb3d597f0f0322647c5/requirements.txt)：Diffusers `80c7ed262aeffbeb43ef13ae04baeb9b84515a69`、Transformers5.12.1、PEFT0.20.0、Accelerate1.14.0、safetensors0.8.0。作者参考PyTorch2.11.0/CUDA12.8。Pillow>=10やCUDA対応バイナリまで固定した環境lockではない。negative_promptは空文字ではなく1個の空白、VAE tilingは無効という作者条件を残す。取得時にinference.pyを実行しない。

[baseのmodel_index](https://huggingface.co/Qwen/Qwen-Image-2.1/raw/790c92633540aa0cb11d9abf19eb46d861714758/model_index.json)はprocessor、scheduler、text_encoder、transformer、vaeを指定。全部を候補台帳に含めた。Hubの7,115,124,736パラメータは主transformerの表示で、encoder/VAE/LoRA込み総数ではない。完全なテンソル総数は未確定のままにする。

[Qwen Research License本文](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/blob/aa213272180d6ad0d03f5fb3d597f0f0322647c5/LICENSE)の研究・評価目的の許諾を読み、LICENSE/Noticeを選択した。otherタグだけを理由に排除しない。ユーザー本人の承諾・再配布・商用使用を代行または推定したわけではない。

### Interpretic

[GGUFカード](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF/blob/e6924b3a08765341e01546308ccf2683d43e880b/README.md)で政治質問のQ4評価を確認。一方、有害依頼の拒否・一般能力はBF16測定。Q4で一般能力も同じと見なさない。GPU型番・クロック・バッチ・実行ピークは未確認。

API原本のBF16全数は**27,781,427,952**、GGUF言語部の表示は**27,320,697,856**。どちらも約27Bだが範囲が違う。視覚projectorを含む変換後の全テンソル照合は未実施。[元LICENSE](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2/blob/69227901b022d2a039fe52e220383f0b79517063/LICENSE)のApache-2.0本文を確認し、GGUF側にない本文を同梱する構成にした。

READMEの65536 context例はRAM適合の保証ではない。固定llama.cpp版、ユーザー機器、KV精度、context、batch、量子化実装の確認が残る。Q4_K_Mを任意の固定zero-point方式と同一視しない。

## 4. 誤った完了扱いを防ぐ

- 今回はHugging Faceの公開APIが返したcommit・サイズ・LFS SHA256を保存した。HTTP200のメタデータ取得はモデル本体を取得できた証拠ではない。
- LFS SHA256は重み本体の照合値。Git blob IDはLFSポインターまたは通常ファイルのGit IDであり、重み本体SHA256ではない。
- 小さな資料のSHA256SUMSは、更新後の本文と照合するまで全面的な検証済みとしない。commit＋Git blobも併記した。モデル本体のローカルハッシュ確認は0件。
- 完全オフライン復元に必要なソフトウェア一式の容量はnull。モデルファイル一式の確定と、環境の再現性を分離する。
- 保存予算は現行policies/limits.jsonの3.8TBと空き200GBを記録するが、ユーザーの実際の容量報告は実測と単位確認が必要。古い予算シナリオから空き容量を推定しない。
- どちらについても新たな公開停止予告・規制時期を確認したわけではない。優先度は独自学習成果の保全シナリオであって規制確率ではない。

## 5. 次に必要な作業を限定

画像は**完全テンソル総数と既存baseの照合**、テキストは**変換後の構成照合とruntime固定**。両者共通で実機の空き・保存先・一時領域を確認し、最後に対象ファイルを固定した取得承認を受ける。新しいモデル名を増やしてこの確認を先延ばしにしない。

**単位チェック**：すべての容量はbyteで合算し、GBは十進表示。ディスクの保存容量と推論RAMは別量。Git SHA1・LFS SHA256・モデルのパラメータ数を混同しない。

## ERROR CHECK

47ファイル一意、4固定commit、10重みすべて配布元SHA256あり、明示byte合算。本文を読んだ利用条件2系列。モデル本体取得0、推論0、HDD操作0、承認追加0。ローカルでは新規10件の読み取り専用テストを実行し、GitHub上の既存監査も更新commitを対象に確認する。CI成功をモデル品質保証とはしない。
