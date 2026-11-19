# R119｜v49：取得報告53モデルと未保存6学習成果の確定（2026-11-19）

## 1.〈本論〉成果

[GitHub正本](../../catalog/CURRENT.json)をv49へ更新する研究判断。現行v48の201資産を**全件無変更**で保存した上で、2026-11-17公開の独立した9BマルチモーダルLoopモデルを1件条件付き追加（R1）。v49 **202登録／155有効、SELECT 53・CONDITIONAL 102**。他の量子化違いを新資産として計上しない。

[固定配布者ファイル7ソース、6独立学習成果・258,965,078,216 bytes](../../queues/proposed-v49-r119-next7-public-source-entries.json)を次の取得候補に確定。publisherの40桁revision、各ファイルbyteとSHA（LFSはSHA-256、非LFSはGit blob SHA-1）を付与。Owner Windows Dドライブの再測定、ローカルSHAと完全復元はこの回に未実施。新しいモデル重みダウンロード0。Gatedダウンロード0。

### 取得報告の更新を反映

[2026-11-19実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は、**54件中53件VERIFIED・1件HOLD、579ファイル、270,835,576,267 bytes、過去実行で観測した最小残容量2,710,260,613,120 bytes**と報告している。R115/R116の「22件VERIFIED」の記述は当時の台帳版であり、現在の最新版として繰り返してはいけない。今回の研究環境からユーザーのWindows Dドライブをマウントし再ハッシュしたのではなく、実行台帳の**報告値**である。

取得済みとの報告があるZONOS3-Miniは66ファイル775,728,152 byteの**別の実行用source scope**であり、今回固定するLM・codec等の原本24ファイル15,345,816,226 byteを取得済みと認定してはいけない。同様に、Interpretic v2/0bserverx RVNで取得済み報告されているのは量子化GGUFであり、今回のBF16/F16マスターとは重みファイルが別である。

## 2. 結論を伴う取得順位

| 順位 | 学習成果／固定配布元source | Source bytes（byte、decimal） | 決定と根拠 |
|---|---|---:|---|
| 1 | [sensenova/SenseNova-Loop-9B-GGUF](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF) BF16+mmproj（同公式学習結果） | 19,338,124,279 | 公式[Safetensors](https://huggingface.co/sensenova/SenseNova-Loop-9B)が**gated:auto**、公式GGUFはpublic。9.413B/32物理層・56演算層・2-stream mHC。削除予測ではなく観測されたアクセス差を優先。GGUFはMTP原本の完全保全とは言えない |
| 1a | 公開Previewリポジトリの同一blobを確認したmodeling code/chat template | 26,724 | 公式配布と**Git blob SHA-1一致**の2ファイルのみ。Preview固有のconfig/indexは異なるため混ぜない。**別学習成果ではない** |
| 2 | [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) BF16 LM、音声generator/codec、heads、speaker encoder/teacher | 15,345,816,226 | 43言語/voice cloning/可制御TTS（出版社仕様）。GGUF/WebGPU派生群を除外。既存の0.776GB実行用版を重複保全マスターと誤認しない |
| 3 | [InterpreticAI/Qwen3.8-27B-Uncensored-v2](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2) BF16 | 55,586,056,799 | 元の後学習済みフルBF16とMTPを保存。既存Q4とは異なる保存精度、作者政治抑制評価は独立再現されていない |
| 4 | [0bserverx/RVN-F16.gguf](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 53,808,326,934 | 配布者SafetensorsがこのF16 GGUFから再構成されたため、再構成元F16を優先。元の学習直後BF16ではない。多量のGSQ/IQ派生を除外 |
| 5 | [microsoft/Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) BF16 | 54,743,814,229 | **ブラウザー操作専門の学習済みCUA**。Qwen基本モデルでは代替できない後学習。MITモデルカード、操作エージェントは隔離ブラウザーと人間の重要操作管理が必須 |
| 6 | [tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) BF16 | 60,142,913,025 | **外部長期メモリー書き込み専用学習済みモデル**。汎用会話モデルとはタスクが異なる。Apache 2.0。Mem0/MemOS/Hy-Memory/未学習系への転移は出版社評価、独立検証未実施 |
| **総計** | **6学習結果、7 public ungated source repos** | **258,965,078,216** | **本人Dドライブの実空き、既存file SHA、streaming stagingを再計測して段階取得** |

SenseNova公式Safetensors原本はPublisher APIで `gated:"auto"`、previewとpublisher GGUFは `gated:false`、全てApache 2.0メタデータ。第三者 mirror ではなく**同一 publisherの公開形式を保管**。公式原本へ本人が正式アクセスできる場合はfull BF16を優先再検討するが、アクセスを回避しない。

### 既存候補の交換／保留

- **無検閲Q4を新規原本として追加しない**：R114系譜訂正を採用。高精度マスターに優先順位を交換するが、過去に取得報告されたQ4は削除しない。
- **LiquidAI LFM3 1.7B Base / Instruct**：[一次LICENSE全文](https://huggingface.co/LiquidAI/LFM3-1.7B/raw/1da06bec6a819da10b54c67e5c90972b46d81871/LICENSE)を確認。出版社のLFM Open License v1.0は**商用利用する法人の年間収益10,000,000 USD以上を許諾対象外**とする。単なるApache-2.0ではない。BaseとSFTは別重みハッシュ（3,457,635,448 byteの異なる学習済み重み各1件）であり単なる量子化重複ではない。両原本のpublisher scope合計6,951,324,903 byteは[固定マニフェスト](../../manifests/drafts/r118-2026-11-19-unreported-fara-hymemory-lfm3-moss-source.candidate.json)に保存したが、用途・権利条件を明示するまでこの最初のpublic Apache/MIT取得リストへは入れない。
- **MOSS-TTS-v1.5**：同マニフェストに16,995,761,910 byteの主repo原本を固定。外部の学習済み音声codec（過去v27依存調査7.099GB）、ユーザーWindows ABIと実行コード閉包が未確定なので依存完了までHOLD。
- **Interpretic v3/Nous Arete 27B**：v2との同条件の独立能力差が不十分なので追加登録しない。v3は別の後学習成果であり単なる量子化コピーではないが、現時点で約55GBの増分を正当化できる検証不足。
- **SenseNova Preview**：旧学習checkpointは正式版とは別だが、正式公開BF16 GGUFが取得できる間はPreviewの約19GB重みを重複確保しない。Previewからは公式版とGit blob SHAが一致するcode2件だけを記録する。

## 3. 配布政策：現在の一次事実と将来仮説を分離

- 米国BISの[2026-11-19予定Federal Register IFR原文](https://public-inspection.federalregister.gov/2026-23529.pdf) IV.Aは、旧AI Diffusion Ruleの**AIモデル重みECCN 4E091指定を廃止**し、モデル重みFDP rule等を除去すると明記。半導体・データセンターへの目的地/最終用途による規制は別途強化される。これを「公開モデルウェイト一般の近日禁止」と解釈するのは誤り。
- モデルごとのGated化/削除/ライセンス条件変更は提供者の行動として個別に実測する。SenseNova `gated:auto`はアクセス条件の事実、将来の禁止確率ではない。
- 日本の個人Dドライブで保有する行為、国境を越える配布/転送、商業サービスで推論提供する行為は法的分類が異なる。日本の個別ライセンス条件/輸出・利用目的に合わせて判断。**無検閲というラベルは無条件無害・無条件合法を保証しない。**
- ExaはHTTP402で新規検索できず、Hugging Face publisher API・モデルカード・米BISの公文書とGitHubの取得台帳を使用。

## 4. Windows取得・検証と単位表

この研究環境は所有者のDドライブを直接操作していない。主repoの[Windows原本取得器](../../scripts/download_r115_windows.py)は、少なくとも`--execute`と、現在のrepository policyでは**明示的な正本scope-承認ファイル**が必要。許可済みのファイルだけの一括処理にすれば「モデルごとの再確認質問」は不要。現在の[Windows原本取得器](../../scripts/download_r115_windows.py)は **R115の16件ソースとR119の7件ソースを両方受け付けるよう更新済み**。既定では読み取り計画だけを表示し、実取得は固定sourceスコープの事前承認を記載した `--approval-file` と `--execute` を同時に指定する。承認ファイルは1回のバッチ実行単位で用意でき、モデルごとの対話確認を繰り返す必要はない。以前のREADMEの`--execute`だけのコマンドは現行の承認ゲートで失敗する。未承認ファイルやGated原本を自動取得しない。


Windows PowerShellからの読み取り計画・取得コマンド（保存ルートは実際のDドライブ格納先に置き換える）：

```powershell
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v49-r119-next7-public-source-entries.json" --dry-run --root "D:\AI-Models"
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v49-r119-next7-public-source-entries.json" --execute --approval-file "owner-approved-r119.json" --root "D:\AI-Models"
```

実行器は固定リビジョン、公開元SHA、200GB残容量床、既存ファイル競合回避を検証する。単体テストは[ R119無通信検証](../../tests/test_r119_public_firstwave.py)に記述済みだが、**Windows Dドライブ上の実行結果はこの調査では未取得**。

| 記号 | 日本語の意味 | 単位（SI次元） | 定義 | 範囲／前提 | 型 |
|---|---|---|---|---|---|
| `B` | Dドライブ実空き容量 | byte（SIのbit換算可） | 実機で `shutil.disk_usage(root).free` | 非負整数、今回未観測 | 整数スカラー |
| `F` | 常時維持する空き床 | byte（SIのbit換算可） | 200,000,000,000 | 固定値 | 整数スカラー |
| `S` | 新規必要source | byte（SIのbit換算可） | R119の全file bytes合計258,965,078,216 | 正確な既存物理hash一致で減る、外部依存除外 | 整数スカラー |
| `O` | キャッシュ/一時書込・file system予備 | byte（SIのbit換算可） | 実装と同時ダウンロード量による | 非負整数、今回未測定 | 整数スカラー |

全件の取得条件：`B >= F + S + O`。全項ともbyteで次元整合。**過去台帳の2.710TB観測値は現在の本人Windows Dドライブの`B`とみなさない**。

## 5.〈応用・転用例〉H/T/D/C/U

**学際分野**：機械学習（学習済み成果と量子化、再帰層）、ソフトウェア供給網（SHA/リビジョンとruntime ABI）、デジタル保存工学（リカバリー・media failure・重複排除）、情報法（現在の公開/Gatedと使用目的別権利）。

- **H**：新たな6独立学習済み成果の高精度sourceは、既存Q4/派生形式だけの保存より将来の再利用可能性と能力カバレッジを増やす。
- **T**：固定メタデータで全publisherファイルをSHA照合し、前の53 reported scopesとrepo/revision/fileごとの重複を検出。本人Dドライブは初回実測、原本の復元試験にはWindows OS/NTFS or exFAT、GPU/backend/version/seed/context/バッチ1を記録。同じ30件以上の比較タスクで同一settingの品質差を記録。
- **D**：v49の202一意/155 active、旧201完全一致、R119 7ソースと2個コードfileが固定ならPASS_METADATA。新規ファイルの現物SHA・オフライン復元・ライセンスの本人使用目的は未実施につきUNCERTAIN。誤SHA/Gated越え/空き200GB割れはFAIL。
- **C**：正式版SenseNovaが本人承認でSafetensorsを取得できるならGGUFを本来原本と誤認せず更新。Faraで外部依存が未収録なら同sourceだけでは実行不能。既存53件の物理状態が台帳と違えば再取得範囲が変化。
- **U**：出版社自己申告ベンチマーク、モデルのcheckpoint欠損、学習系譜、ライセンス、所有者ディスク実際の空き、復元するframework ABI。ランダム反復実測なしにつき合成標準不確かさ `u_c` と包含係数 `k` は未算出。

### ERROR CHECK

- v49 202資産、155 active = 53 SELECT + 102 CONDITIONAL。旧201レコードをJSONで全件一致確認。新規R1 CONDITIONAL 1件のみ。正式原本 gated:auto、公開同publisher GGUF Gated:false。
- R119 7公開source（6学習結果＋1モデルcode dependency）、取得候補source合計 **258,965,078,216 bytes**。過去54モデル記録中53 VERIFIED報告（ユーザーDドライブ現物未照合）。
- 既存原本削除0、派生GGUFを別学習成果と計上0、Gated無断取得0、モデル実行0、今回の実weights取得0。すべて検証すべき外部実装依存は明示保留。

## 6.〈次に考える問い〉

**モデル数の増加ではなく、独立した学習済み能力・正確な原本復元・失われやすい公開経路を満たす追加1GBあたりの価値を、現物ディスクの残容量を維持してどれだけ増やせるか。** 今回は既存選定を削らず、変換版の増殖を抑え、6独立結果の固定sourceに絞った。
