# 2026-11-11: v27高価値モデルWave 2 — exact source scope監査と新v3比較
> **非実行・未承認**。GitHub Unjuno/local-model-portfolio、ブランチ strategy/2026-11-03-01-risk、基準 ddc48f03bfc7dca1d7d2665a43a36618bf77818b。現行v27/173件、有効126件、承認キュー0件は変更しない。

## 1.〈本論〉選定4件と実際の取得範囲

| 優先 | Repo | v27実際の選定files | 選定bytes | 配布repo全体bytes | 扱い |
|---|---|---:|---:|---:|---|
| W2-1 | [usezn/Galvanize-3](https://huggingface.co/usezn/Galvanize-3) | 11 | 597,573,024 | 1,160,571,956 | ONNXだけ |
| W2-2 | [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | 8 | 671,173,375 | 671,173,375 | LoRA + metadata |
| W2-3 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | 5 | 17,738,327,225 | 17,738,327,225 | Q4+mmproj |
| W2-4 | [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 11 | 16,560,392,734 | 1,645,270,647,302 | RVN-Q4_K_M-multilingualだけ |

**小型2件合計 1,268,746,399 B、全4件 35,567,466,358 B**。4件はすでにv27選定済み126資産の**部分集合**であり、v27の3.417TBへ再度足してはいけない。

### 1) usezn/Galvanize-3
選定は約597.57MB、ONNX 563,102,066 B + tokenizer.json 34,387,721 B と小さな設定・規約等。モデルSafetensors 562,583,392 Bをさらに取得しない。CPU ONNXのopset, thresholds, tokenizerの適合性は本番実行前の別監査。Apache-2.0メタデータは本人利用権限の確定ではない。

### 2) chatrlabs Qwen-Image-2.1 LoRA
本体671,151,136BのBF16 rank128 448-tensor LoRAを、README、LICENSE、Notice、SHA256SUMSと保存する独立の追加学習成果。**Qwen Research Licenseによる非商用研究/評価限定**で、商用・再配布を無制限にできない。親モデル Qwen/Qwen-Image-2.1の実体はこのリポに含まれない。公開作者モデルカードは訓練基盤revision `790c92633540aa0cb11d9abf19eb46d861714758`、Diffusers `80c7ed262aeffbeb43ef13ae04baeb9b84515a69` を明記。パイプライン復元は親とABI両方の固定が必要。作者による2xRTX4090 24GB/25step/CFG4の時間は独立性能検証ではない。

### 3) InterpreticAI v2 Q4
選定はQ4_K_M GGUF 16,810,714,592 B、F16 vision projector 927,606,944 B、README、SHA256SUMSなど合計17.738GB。政治的な質問での応答スタイルを調整した派生で、万能低拒否とは異なる。v27固定revision `e6924b3a08765341e01546308ccf2683d43e880b` は11/6観測。**11/11のHub mainは7057fd1...と表示され、最新版へ無断追従できない**。旧固定版がまだ配布可能か、ファイル名・旧SHAが一致するか本人の承認前dry-runで再確認が必要。

### 4) 0bserverx Heretic
配布repo全体は 1,645,270,647,302B（量子化群182ファイル）なのに、v27で選択しているのは 16,560,392,734B（11ファイル）である。選択の主重みは `RVN-Q4_K_M-multilingual.gguf`（16,547,400,224 B）**だけ**。GSQ-3bitの設定/トークナイザも現行manifestに入っているため、GGUF単独での復元確認後に縮約を検討するなら任意4ファイル案 16,547,454,222B（節減 12,938,512B）。**これは未採用の提案であり、元v27を勝手に書き換えない**。

## 2. 最新の別後学習 v3 は研究候補、v2の自動置換は却下
[InterpreticAI/Qwen3.8-27B-Uncensored-v3-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v3-GGUF) は2026-11-10公開。v2はQwen3.8-27B直接派生でMTPを保持、v3はNousResearch/Arete-27Bからの別後学習でMTP非搭載。作者報告の検閲率v2 3.5%/v3 2.6%は対象質問・採点等が異なる可能性があり、独立比較ではない。**性能が高いからv2を捨てる判断はしない**。v3の固定40字revisionとLFS SHAが未監査なので取得禁止。

## 3. 完全な事前承認と公式Hugging Face CLI
公式CLIは `--revision`（commit SHA）、`--include`（選択ファイル名）、`--dry-run`（本体を取得せず見積もり）、`--max-workers 1` を提供。ダウンロード時に無指定`main`と`--local-dir`でリビジョンを混ぜない。HF Hubの`cache_dir`共有blobと`--local-dir`のメタデータcacheは別の配置方式なので、容量は同一HDDで一つずつ実測し、フルcache+最終ファイルの二重保管を避ける。

**現時点でCLIは一切実行していない。** 以下は、既にCLIがある場合の管理者向け *未実行* metadata dry-run の例。

```bash
hf download usezn/Galvanize-3 --revision 597237be3b0fabbf5d70ff16ce95fad14a591f20 --include 'onnx/model.onnx' --include 'tokenizer.json' --include 'thresholds.json' --include 'config.json' --dry-run --max-workers 1
hf download InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF --revision e6924b3a08765341e01546308ccf2683d43e880b --include '*.gguf' --include 'SHA256SUMS' --dry-run --max-workers 1
```

上の例は主ファイルのメタデータ確認であり、全規約・小ファイル等の承認済み完全スコープを意味しない。正確な11/8/5ファイル名リストはJSONを使用。決してドライラン結果だけで『本体のローカルhashを実証済み』とはしない。配布元の条件や取得先の現物空きは必ず別判定する。

## 4. 容量と取得時ピーク

| 記号 | 意味 | SI単位 | 定義域/型と条件 |
|---|---|---|---|
| `B_W` | Wave2選択4件総量（重複なし） | B | 35,567,466,358、非負整数スカラー、v27既存内数 |
| `B_2` | W2前半小型2件 | B | 1,268,746,399、非負整数スカラー |
| `B_F` | Wave2最大単一重みの追加コピー | B | 16,810,714,592, 非負整数スカラー |
| `F_0` | W2開始時保存先実測空き | B | 未測定の非負整数スカラー |
| `F_min` | 取得後に残す最低空き | B | 200,000,000,000、定数スカラー |

W2を空の保存先に格納する単純コピーの上界例は `B_W + B_F = 52,378,180,950 B`（キャッシュ全量保持や実行依存なし）。B同士の加算なので単位整合。既存バイト重複と実機空き不明のため取得GOには使えない。本人が確認すべき条件は `F_0 - 実際の増分 - 同時コピーとキャッシュ >= F_min`。

## 5. H/T/D/C/U・ERROR CHECK

H: v27選定の4件は独立学習価値・圧縮・権利が異なり、全repoを無差別に取らず原本ファイルだけを取得すれば、選択した目的と容量を両立できる。T: まずsource 4repo・実際の選択35ファイルのrevision, LFS SHA/size, parent provenanceを静的検査。取得試験は別途本人承認後にone-asset workerで比較。D: 固定ソース内整合PASS、実体取得はNO。C: 古いリビジョンが削除/変更、用途非商用違反、量子化選択過多、親モデル欠落、backend不適合。U: Hubライブ再確認・実機空き・cache・実行性能・法的適用未測定なのでu_cとkは算定不能。
ERROR CHECK: 静的バリデーション 17件PASS、失敗0。v27/承認0維持。モデル本体取得/インストール/実行なし。

## 6.〈次に考える問い〉

容量を埋めることを目的にせず、取得できなくなる可能性がある独立後学習重みと、その使用権利を示す証拠をどの順で確保するか。まず小型高価値のファイル固定、次に大きい派生Q4を別承認する。
