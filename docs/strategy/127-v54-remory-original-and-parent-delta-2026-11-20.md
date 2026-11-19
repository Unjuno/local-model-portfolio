# R127 / v54：REMORY残差学習メモリの原本採用とQwen元親リビジョン差分（2026-11-20）

**v53の206資産を不変に維持し、v54は207登録／160有効（SELECT53／CONDITIONAL107）へ。** 新規1件の正式CONDITIONALは [`fudan-generative-ai/Qwen3.8-27B-REMORY-1.9B`](https://huggingface.co/fudan-generative-ai/Qwen3.8-27B-REMORY-1.9B)。これは原本取得の選定であり実ダウンロード許可ではない。[Publisher20-file source](../../manifests/drafts/r127-2026-11-20-remory-20file-online250-and-parent-delta.candidate.json) / [判断台帳](../../catalog/decisions/2026-11-20-r127-v54-remory-source-adoption.json) / [v54修正](../../catalog/revisions/v54-2026-11-20.json)。

## 1.〈本論〉実際のモデルの中身と固有性

REMORYは単なるQwen量子化や自然言語履歴の保存ではなく、**Qwen3.8-27Bを凍結し、要約と補完的に推論コンテキスト内へ入れる残差soft-memoryを独立学習した**成果。記憶を書き込む`tencent/Hy-Memory-30B-A3B`や、エージェント・コーディング行動を後学習するpi RL LoRAと学習目的が異なる。モデル側の正しい名前は2B級（repo名の1.9Bではなく、最新原本の正確な要素数は**2,005,757,188**）。

元publisher SHA `5ada60e61d5425012b92a7c2b2796fc0b0f29241`、**20 sourceファイル総8,023,113,280byte**。重みファイル`model.safetensors`だけで **8,023,041,444byte / SHA256 `59d36bcec81c44bb314b63afea4dae79d8cda53a8918a5364143d8ecb2a499e5`**、原本は117のFP32テンソル（online continuation step250）。モデル配布者の`release.json`と`manifest.json`、20全ファイルメタデータと`SHA256SUMS`を照合し、**19の小型ソースファイルを実際に読み出しGit blob SHA1とファイルSHA256を再計算した**。重み8GBはダウンロードしておらず、そのローカルSHAは未確認。

**重要な評価訂正**：online250は旧Stage II step14925（Hub rev `f24de2ac3996da36678cd5d196a7dc0dbbc3aa34`）から継続学習した**別の重みSHA**。原論文 [arXiv:2610.11287](https://arxiv.org/abs/2610.11287) の数値はonline250に再測定されていないと作者が明記しており、今回の採否根拠に最新checkpointの実測性能と偽って利用しない。

## 2. 親Qwen3.8-27Bの元訓練版を解決

REMORY配布`config.json.target_revision`は`Qwen/Qwen3.8-27B@1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`。ポートフォリオで使っている親比較`37561816e66b5b9153b1b64c10968c18c1e6f4a0`と元publisherの32ファイル全件をハッシュ比較し、**29件は同じ、18の重量BF16 shardは全一致**。異なるのは次の3メタデータファイルだけ。

| ファイル | 元訓練親バイト | Git blob SHA1 |
|---|---:|---|
| `README.md` | 65,012 | `bc8aa0e396cd029c21cd773cca21830d0ded28ec` |
| `chat_template.jinja` | 8,952 | `c0c686f9c38d70d179fb7b5f5aa7530bc913dda3` |
| `tokenizer_config.json` | 17,928 | `5de744b3fca2129d7186979ae47c06be33903243` |

差分は合計**91,892byte**。同じ重みを二重保存するのではなく、**元親版のchat template・tokenizer config・READMEを別ファイルとして保存**し、必要な復元versionを守る。現在の所有者HDDで親18重量が存在/ハッシュ一致するかは未検証で、REMORYの8GBだけで完全offline動作が保証されるわけではない。

## 3. 実行依存・費用・代替選定

作者公式コードは[GitHub Remory](https://github.com/fudan-generative-vision/Remory) commit `683b7ba648fe91fa063291380cd107c1d836cd6c`。配布モデルの`requirements.txt`は**PyTorch≥2.9／Transformers==5.3／Safetensors≥0.6／Hub≥0.34**、公式例はSGLang hookとCUDAコンパイルを含み、作者は**80GB GPUを最低2枚**推奨。所有者の実機での速度、完全ピークRAM、実行可否は未実測。ローカルコード/torch pickle/custom backendを未審査で実行しない。

`mocoV3/Qwen3.8-27B-REMORY-1.9B`はpublisher APIでこの正規fudan repoへリダイレクトし同じrev/重みを返すため二重登録不可。Hy-Memory30Bは記憶書込方針、pi RL LoRAはコーディング方策、REMORYは要約後の潜在メモリ表現であり、3種類を「記憶モデル」という名だけで機械的に交換しない。ML実験で必要な長期タスクを比較してから選定を見直す。

保存政策：4TB（ユーザーが許容する計画上限）、**実ドライブ最低空き200GB**、別途ステージング/キャッシュ。MITタグと第三者MIT表示だけで本人の取得・再配布/商業利用全てを許可しない。今回の`queues/approved.json`は空、実重量取得0。公開停止や規制は将来の可能性であり、いま公開非GatedなREMORYに差し迫った規制を断定する証拠はない。米BIS2026-11-16の[公式遠隔計算規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)を公開weightsの私的保管一律禁止と混同しない。

## 4. 変数表と次元・論理チェック


| 変数 | 意味（日本語） | SI単位 | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| `N_Q` | Qwen親の学習済み格納要素数 | 1（無次元） | 27,781,427,952 | 訓練親revisionのPublisher Safetensors総数 | 整数スカラー |
| `N_M` | REMORY残差memory学習済み要素数 | 1（無次元） | 2,005,757,188 | online250のrelease.jsonのテンソル総数 | 整数スカラー |
| `N_T` | 親＋memoryの合計格納要素数 | 1（無次元） | 29,787,185,140 = `N_Q + N_M` | 別の未計数の学習済みruntime依存なしの場合 | 整数スカラー |
| `B_M` | 原本20ファイルの論理source容量 | byte（非SI単位） | 8,023,113,280 | 親重量・runtime付属ファイルは別 | 整数スカラー |
| `B_D` | 元訓練親の差分ファイル容量 | byte（非SI単位） | 91,892 | 親32のうち異なる3ファイルの合計 | 整数スカラー |
| `B_F` | HDD最低確保空き | byte（非SI単位） | 200,000,000,000 | Owner媒体で実測が必要 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 対象測度の単位 | 未算出 | 実機反復標本不足 | 非負実数スカラー／未推定 |
| `k` | 包含係数 | 1（無次元） | 未設定 | 信頼水準・誤差モデル未指定 | 正実数スカラー／未設定 |

**算術導出**：Publisher親`27,781,427,952`個＋別学習済みmemory`2,005,757,188`個＝**`29,787,185,140`個**。学習済み要素の無次元数同士の加算で整合し、150B基準未満の研究スクリーンにPASS。ただし追加実行時に使われる外部learned moduleの完全閉包は別確認。sourceの`8,023,113,280byte`と親版3差分`91,892byte`の加算はどちらも情報量単位で可能だが、Qwen親重量全体とruntimeの実保存容量は別。

## 5. H/T/D/C/UとERROR CHECK

**H**：同じQwen親と圧縮token予算で、online250 REMORYは文字列要約のみより長期タスク成功率が高い。**T**：長期セッション最低30ペア、同一GPU/clock/OS/driver/SGLang ABI/quant zero-point/context/batch、元親revとtokenizer版も固定。事前停止ルールは違法/誤SHA/残床割れで即STOP、結果有利での逐次終了禁止。**D**：PASS＝事前登録した品質改善と所有者の原本SHA、LICENSE/親/復元全て成立。FAIL＝ハッシュ違反・権利違反・原本からの復元失敗。UNCERTAIN＝実機評価・権利・所有者HDDは未検証の現状。**C**：新online250の汎化が旧Stage IIを下回る、custom SGLang復元不能、元Qwenテンプレ差による不整合。**U**：出版社性能が異なるstepの公表、所有者環境/メモリ/ABI/法的範囲未測定なので合成標準不確かさ`u_c`と包含係数`k`を数値化しない。

**ERROR CHECK**：Publisher original20 source files 8,023,113,280byte、親32files中29同一・3差分、記憶2,005,757,188/親27,781,427,952、v53 206資産保護→v54 207／160、承認0・新重量DL0、Owner物理現物/実機Python試験未実施。関連分野：深層学習の圧縮記憶、アーカイブの内容アドレス、推論システム/SGLang-ABI、知財・モデル配布政策。

## 6.〈次に考える問い〉

親Qwenを再保管せずにREMORYを復元するには、**同じ18 BF16シャードと旧chat template/tokenizer設定**の組をどこまで保全・SHA確認する必要があるか。重量の名前だけではなく原本のファイル内容と実際の再起動試験が答えになる。
