# R116｜v48の固定原本取得・Dドライブ重複回避（2026-11-19）

## 1.〈本論〉今回の事実と実行判断

現行[正本](../../catalog/CURRENT.json)はv48：**201登録／154有効**。新たな学習済み資産を無造作に増やさず、既存登録モデルの保存ファイルを確定する。今回の[R115 16原本ソース・選定キュー](../../queues/proposed-v48-r115-master-sources-16.json)はpublisher固定ファイル237件・publisher LFS SHA256計102件（非LFSはGit blob SHA1）・source総量301,848,275,578 byteを記録した。

取得候補を10件 **132,430,668,414 byte**、新規取得を保留する6件 **169,417,607,164 byte** に分離する。前者でも別々の推論用量子化やWebGPU版は追加しない。

**重要な既存取得履歴**：[2026-11-19取得実行台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**23件実行、22件VERIFIED・1件Gated HOLD、227ファイル・162,325,501,646 byteを検証したと報告**。今回の研究環境から所有者のWindows Dドライブを独立に読み直したものではない。取得報告の22件と新キューを照合すると、10件中7件（7,690,468,455 byte）はrepo ID・revision・ファイル件数・sourceバイト数が一致する。再ダウンロード回避優先。

**新たなソース3件**：

| 取得の目的 | 現行登録 | 出典固定 | 正確なsource bytes | 備考 |
|---|---|---|---:|---|
| 43言語/話者制御とcodecを保全 | Zyphra/ZONOS3-Mini | [source manifest](../../manifests/drafts/r115-v48-zonos3-mini-original-source-with-codec.candidate.json) | 15,345,816,226 | source24ファイル。HF repo全342ファイル・30.918GBからGGUF/WebGPUを省く |
| 無検閲v2のBF16を保全 | InterpreticAI v2 | [source manifest](../../manifests/drafts/r113-v48-two-uncensored-original-fp16-parents.candidate.json) | 55,586,056,799 | BF16 weights18 shard＋関連config、MTP head保持 |
| RVNの既知最良の元形式を保全 | 0bserverx RVN | [R114 source](../../catalog/decisions/2026-11-19-r114-uncensored-lineage-correction.json) | 53,808,326,934 | RVN-F16.gguf＋README＋gitattributes。Safetensorsはこれからの再構成物 |

**合計124,740,199,959 byte（124.740GB）**。新規物理増加の見積もり上限ではなくpublisher固定source論理量。過去に同じファイルが別場所で保存されていれば正味増分は小さくなる。外部依存、ファイルシステム、stage、cacheは別。

**6件保留**：Nemotron-3-Diarizationはopenmdw-1.1の権利/実行条件、DSpineは親27Bとの正確なABI、画像LoRAは親と非商用ライセンス、大型Gryphe/DavidAUは独自性能差・重複評価、OrcaRouterはGated本人権限。なお過去の取得台帳ではこれらの一部も取得済みと報告されるが、**新規取得保留と既存ファイルの削除は別**。既存ファイルは削除しない。

InterpreticAI v3（Arete-27B親・MTPなし、作者公表の中国語政治評価でv2 3.5%対v3 2.6%）は別学習結果であるが、汎用性能改善の実証と容量の根拠が足りないので**新規登録せずHOLD**。詳細はR115の`v3_comparison`。

## 2. Windows Dドライブ上でOpenCodeが行う作業

このリポジトリに[実行器](../../scripts/download_r115_windows.py)と[ネットワークを使わない整合性テスト](../../tests/test_r115_download_manifest.py)を追加した。**最初のモデル前のユーザー再確認は不要**。ただし必ずユーザーがこの保存処理を指示したOpenCodeセッションで`--execute`を付けて起動する。既定はread-only計画表示。

Windows PowerShellで（GitHubを既にcloneしている場合はそのディレクトリを利用し、既存作業を無断上書きしない）：

```powershell
git clone https://github.com/Unjuno/local-model-portfolio.git
cd local-model-portfolio
py -3 -m pip install --upgrade huggingface_hub
py -3 -m unittest discover -s tests -p "test_r115_*.py"
py -3 scripts/download_r115_windows.py --root "D:\AI-Models"
py -3 scripts/download_r115_windows.py --execute --root "D:\AI-Models"
```

**既存モデル保存先が`D:\AI-Models`以外であれば、OpenCodeはDドライブを読取で探索し、既存保存階層のルートを`--root`に指定**。重複ダウンロードを避けるため、R115実行器は`models/author/repo`、`author/repo`、`downloads/author/repo`などを検査して既存ファイルの実SHAを確認。GitHubの過去台帳で同一scopeがVERIFIEDと報告される7件について、ユーザーのDドライブ上で未発見なら**再取得せず`SKIP_PRIOR_REPORTED_UNLOCATED`を記録**。不足していることを現物確認した場合に限り`--recover-prior`を使う。追加確認質問は不要。

`--execute`はその場でユーザーが開始を指示した実行に限る。必要なら追加的に`--approval-file <file>`で個別のsource-scope approvalを厳格検査できるが、一般の公開Apache-2.0 first-waveで逐一確認を要求しない。**GitHubの`queues/approved.json`は空のままであり、正式な保存完了やアクセス権確定と混同しない。**

実行器の保護：
- 固定40桁revision、sourceファイルをすべて検証、実D容量を計測し、200,000,000,000 byte以上の空きを維持。
- HF temporary/cacheをDドライブ内に置き、ファイル1個単位で途中再開。原則3回まで失敗リトライ。
- publisher LFS SHA256を優先。LFSのGit blob SHA1は**LFSポインタ**なので、展開されたweightsの内容ハッシュとして誤用しない。小ファイルはGit `blob <size>\0<content>` のblob SHA1と照合。実ローカルSHA256を追加記録。
- 既存ファイルが公開元hashと違う場合は**上書きせず競合として停止**。未知のモデルコードやpickle形式重みは実行しない。
- `D:\AI-Models\logs\r115-download-ledger.jsonl`にファイルごと検証結果を追記。パスとログをGitHubに公開しない。

## 3. 数値と次元チェック

| 記号 | 日本語での意味 | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| B | 実ストレージ空き容量 | bit（表示はbyte） | `shutil.disk_usage(root).free` | 0以上の整数、Windowsの当該volumeを実測 | 整数スカラー |
| F | 最低空き床 | bit（表示はbyte） | 200,000,000,000 byte | 固定方針 | 整数スカラー |
| S | まだない対象sourceファイルの必要量 | bit（表示はbyte） | 選択固定file bytesの合計 | 0以上、報告済みと現存一致なら0に減少 | 整数スカラー |
| O | 一時ファイル・追加余裕 | bit（表示はbyte） | `max(2GB, 最大片file/4)`の保守見積 | 0以上、未測定 | 整数スカラー |

ダウンロード開始条件：`B >= F + S + O`。各項ともbyte単位へ統一した容量なので次元一致。上の3件で最初に見積もる`S`は124,740,199,959 byteであるが、`B`はDドライブの未観測値であり、台帳上の別環境での最小空き量を流用しない。

## 4. H/T/D/C/U

- **H**：原本差し替え・元の訓練成果単位での重複排除・過去台帳との照合によって、同じ保存容量でより多くの独自能力を保全できる。
- **T**：固定source全16モデルのサイズ・hash・revision検査、10件GOと6件HOLD、旧台帳23件との一致比較。Windows側でユニットテスト実行後、Dドライブで全ファイルSHA・中断再開・offline restoreを検証。
- **D**：静的sourceと旧台帳照合はPASS_METADATA。物理同定／依存復元／ライセンス行為確定はUNCERTAIN。publisher不一致・Gated回避・200GB floor割れはFAIL。
- **C**：以前の22件の報告が誤っている、または別パスに実体がある場合は新規転送量の見積が変化。ZONOS3で推論依存に未収録学習済み重みが見つかれば追加して再評価。
- **U**：保存場所の同定、実自由容量、外部decoder/ABI、親sourceと著作権、量子化誤差。独立反復実測がないため合成標準不確かさ`u_c`と包含係数`k`は数値未算出。

関連分野：**デジタル保存工学**（内容同一性・誤消去防止）、**機械学習**（原本・訓練系譜・依存重み）、**ソフトウェア供給網**（固定revisionとABI）、**情報法**（公開メタデータ・権利・将来規制の区別）。

### ERROR CHECK

- v48登録201／有効154不変更。新学習成果登録0、既存削除0、Gated回避0。
- 16件のpublisher source合計301,848,275,578 byte ＝ GO10件132,430,668,414＋HOLD6件169,417,607,164。
- GO10件のうち旧台帳一致7件7,690,468,455 byte＋未報告ソース3件124,740,199,959 byte＝132,430,668,414 byte。
- 旧台帳22VERIFIED報告の物理的な独立再ハッシュは**今回未実施**。この回で新たな重みファイル取得0。GitHubの静的単体テストは作成したがWindows上での実行結果は未取得。

## 5.〈次に考える問い〉

Dドライブ内で実体があると報告された旧7ファイル集合を**再取得する前に**場所とSHAを確定し、それから新たな124.740GBの原本を追加できるか。R116の答えは「先に実体確認、重複回避、次に新原本」である。
