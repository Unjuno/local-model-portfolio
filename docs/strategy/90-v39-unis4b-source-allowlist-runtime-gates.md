# R90 — Xiaomi UNIS-4Bと必須VQの18ファイル原本計画・安全ゲート（2026-11-15）

## 1.〈本論〉選定した中身・未完成の境界

現行v39・194資産／有効147件の採否を変えず、[Xiaomi UNIS4B原本](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B)と必須[BAAI VisionTokenizer](https://huggingface.co/BAAI/Emu3.5-VisionTokenizer)を、**2配布repo・18ファイル・11,991,440,188 byteの固定ソース候補**として整理した。成果物は[非実行マニフェスト](../../manifests/drafts/v39-unis4b-and-vq-source.candidate.json)、[オフライン静的検証器](../../scripts/verify_v39_unis_source_draft.py)、[負例を含むテスト](../../tests/test_verify_v39_unis_source_draft.py)である。

| 原本 | 不変revision | 選択ファイル | 選定理由 |
|---|---|---:|---|
| Xiaomi U0-4B | c1a4e9c9c3cf52dd3617d3c9c974e16e6e88b3cd | 12本・10,170,001,048 byte | BF16学習済み2シャード＋設定・tokenizer・作者独自コード参照、見本画像2件は非取得 |
| BAAI Emu3.5 VisionTokenizer | a5c45bdb8084763048e094ae124778bfeca7d5ee | 6本・1,821,439,140 byte | 必須学習済みVQのsafetensorsを選び、別形式pickleチェックポイントを排除 |
| **合計** | 配布元2件 | **18本・11,991,440,188 byte** | **3学習済みsafetensorsファイル**、著作権や推論コード権限は未確定 |

固定ソースの一次メタデータは[R89の研究JSON](../../catalog/research/2026-11-15-r89-xiaomi-u0-4b-immutable-selected-source.json)。各ファイルについてpath、byte、Git blob SHA1、該当する学習済み重みのLFS SHA256を照合する。**Git blob SHA1と学習済み重みのSHA256を同一視しない**。この出版社メタデータの固定は**本人HDDにファイルがある・ローカルSHA一致・権利がある・オフライン復元可能の証明ではない**。利用者の明示承認なしに取得しない。

## 2. 危険な実行分岐の発見と遮断

固定作者コード[vision_tokenizer builder](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/blob/e722003980958f242203af265718ee980b834deb/inference/xr_u0_ar/vision_tokenizer/__init__.py)の文字列を直接検査した。

| 条件 | 実際の処理 | 本候補の判断 |
|---|---|---|
| config.yaml と model.ckpt が揃う | torch.load(ckpt_path, map_location="cpu")。weights_only引数の明記なし | **取得対象からpickle形式を外す**。コード実行は未承認。PyTorch既定値やリスクはABI別に確認 |
| pickle側の組を選ばない | AutoModel.from_pretrained(model_path, trust_remote_code=True) | **safetensorsでもremote code許可が残るため実行停止**。第三者コード・ライセンス・動作の独立確認が必要 |
| VisionTokenizerを主モデルに結合 | 必須VQの学習済み本体と対応processorが必要 | VQも独立固定revisionと原本ハッシュを記録。別モデルの重複採用として数えない |

**安全なsafetensorsを選択しても、ランタイム安全性は証明されない。** 将来の実行は最低権限・ネットワーク遮断・固定済みソフトウェア・安全なモデル読み込み・ローカルSHA検証・本人承認が独立に必要。作者のH20上の大型FlashAR速度値を4B eagerモデルへ流用しない。4B-Sequence/34B/38Bは増分価値未測定で選定外を維持する。

## 3. 公開リスクの事実と仮説

[EU AI ActのオープンソースGPAI例外](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は特定義務を限定免除する規定であり、全ての重みが無制限に配布できると認定するものではない。[日本内閣府AI法](https://www8.cao.go.jp/cstp/ai/ai_act/ai_act.html)も一律ウェイト保有禁止の証拠にはならない。今のモデルはHubのpublic記録だが、LICENSE正文・外部VQの使用許諾・適法な再配布権は未精査。将来のGated化や配布停止は反証可能な仮説であり、確率や禁止予定日は作らない。

## 4. 変数表と単位

| 記号 | 意味（日本語） | SI/情報単位 | 定義 | 定義域・範囲・前提 | 型 |
|---|---|---|---|---|---|
| n | 配布repo数 | 1（件） | 2 | 固定repo ID | 整数スカラー |
| f | source選定ファイル数 | 1（件） | 18 | 各repo内でpath一意 | 整数スカラー |
| Bm | 原本source容量 | byte | 10,170,001,048 | 固定publisher SHAに紐づく計画 | 整数スカラー |
| Bv | VQ source容量 | byte | 1,821,439,140 | 固定publisher SHAに紐づく計画 | 整数スカラー |
| Bs | 合計選定source容量 | byte | Bm+Bv=11,991,440,188 | 実HDD必要量ではない | 整数スカラー |
| Bh | 安全空き容量床 | byte | 200,000,000,000 | 所有者HDDで未検証 | 整数スカラー |
| Pm | 主モデルの公表学習済みパラメータ | 1（無次元、個） | 5,082,100,000 | Hub概数・完全tensor監査前 | 整数スカラー |
| Pv | VQの公表学習済みパラメータ | 1（無次元、個） | 455,300,000 | Hub概数・完全tensor監査前 | 整数スカラー |

**単位確認**：Bsはbyte同士の和であり、パラメータ数Pm/Pvとは比較も加算もしない。重み・OS・KV cache・ABI・CPU RAM・GPU VRAM・stagingの実測がなければ4TB計画への物理適合は未確認。

## 5. H/T/D/C/U・ERROR CHECK

- **H**：全18ファイルについて不変revision・選択path・出版社byte・LFS SHAをR89研究JSONと一致させ、pickle系の代替を取得対象に入れず、実行フラグを閉じたマニフェストを維持できる。
- **T**：n_min=18のsource全件を静的検証器で照合。異なるrevision/重みSHA/byte、未承認実行、絶対パスや親ディレクトリ参照、pickle代替を負例テストにする。ネットワーク・モデルimportは不要。
- **D**：PASSはソースメタデータの整合と非実行状態のみ。FAILは選択SHA・容量・権限フラグの不一致。UNCERTAINはモデル本体の独立SHA、ソフトウェアABI、ライセンス・本人権限・安全なVQロード・完全オフライン復元・実機精度。
- **C**：VQをsafetensorsに切り替えた分岐が原本互換でない、作者コードの未監査実行が不可避、実重みやライセンスの不一致、同族の重複費用。
- **U**：Publisherメタデータ、第三者コード/ライセンス、実機RAMとHDD、選択以外の依存。誤差分布がないので合成標準不確かさu_cと包含係数kは算定不可。

**ERROR CHECK**：v39の194資産・147有効・承認0を変更しない。今回追加したのは**非実行ファイル候補とソース整合検証**であり、モデル本体取得、復元、実機ベンチ、ライセンス承認ではない。

## 6.〈次に考える問い〉

作者が提供するVQ safetensorsを、trust_remote_codeの実行を安全に制御した完全オフライン環境で、同一の画像トークン表現として再現できるか。その証明がない限り「復元可能」と認定しない。
