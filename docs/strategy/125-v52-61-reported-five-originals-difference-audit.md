# R125 — v52／61件VERIFIED報告から原本5件の不足ファイルを一意同定（2026-11-20）

## 1.〈本論〉現在の主張と精度

現行正本 `catalog/CURRENT.json` はこの調査時点で **v52-20261119、登録205／有効158**。新しい取得台帳は62件中61件VERIFIED報告・708ファイル・409,835,119,252 byte。ユーザーが管理するDドライブをこの会話で再ハッシュしたものではない。

旧[R122全原本マニフェスト](../../manifests/drafts/r122-v50-five-originals-and-dependency-sources.candidate.json)は5モデル85ファイル、84,656,032,539byteを公開元固定40字revisionで保存候補としたが、歴史的取得台帳の「VERIFIED」を原本全ファイルがそろったという意味に誤読できる危険があった。R125では個々のsource revisionが完全一致し、**公開元の大容量weight/content SHA-256 23件は台帳の記録と全て一致**することを確認。次に全ファイル数とbyte差から未収録候補を組合せ全探索し、5モデルで各**一意の組合せ**を得た。よって大容量5repoを丸ごと取得し直す合理性はない。

| Publisher model | 公開元SHA一致 | 未収録候補ファイル数 | 欠落候補 byte | 未収録と一意推定したパス |
| --- | ---: | ---: | ---: | --- |
| `RWKV/RWKV7-7.2B-20260805` | 3 | 7 | 337,813 | `.gitattributes`, `inference/generate.py`, `inference/kernel.py`, `inference/model_loader.py`, `inference/requirements.txt`, `inference/runtime.py`, `NOTICE` |
| `GSAI-ML/iLLaDA-8B-Base` | 5 | 4 | 28,506 | `.gitattributes`, `configuration_illada.py`, `modeling_illada.py`, `SECURITY.md` |
| `PrentisAI/GroundGUI-8B` | 2 | 1 | 1,570 | `.gitattributes` |
| `ACE-Step/acestep-v15-xl-turbo` | 4 | 4 | 3,959,780 | `.gitattributes`, `configuration_acestep_v15.py`, `modeling_acestep_v15_xl_turbo.py`, `silence_latent.pt` |
| `microsoft/TRELLIS.2-4B` | 9 | 1 | 1,519 | `.gitattributes` |
| **合計** | **23** | **17** | **4,329,188** | 85ファイルに対し履歴の68ファイル |

**注意**：実際にユーザーHDDから消失しているという証明ではない。GitHub過去台帳の選択file_count・source_bytesと元リポジトリの定量的一致で逆算した**メタデータ上の未収録候補**。対象小ファイルの物理有無、SHA・版を本人Dドライブで照合し、確認できた欠損だけを取得候補にする。

### 1.1 実装・再現性に基づく優先順

- **ACE-Step**：大容量4重量シャードはPublisher SHAと合致。未収録は`silence_latent.pt` 3,841,215 byte、`configuration_acestep_v15.py`、`modeling_acestep_v15_xl_turbo.py`、`.gitattributes`。重要なのは前3者で、.ptを無検証pickleとしてロード・デシリアライズしない。
- **iLLaDA**：5 SHA一致（4重量＋tokenizer）。未収録`configuration_illada.py`、`modeling_illada.py`、`SECURITY.md`、`.gitattributes`。前2者は非標準アーキテクチャ復元のために重要だが、`trust_remote_code`で自動実行しない。
- **RWKV7**：3 BF16重量シャードは全一致。未収録は`inference/`内のkernel/generate/loader/requirements/runtimeと`NOTICE`、`.gitattributes`。標準Transformersルートと最適化推論コードは別。オフライン研究用コードは静的保存候補、GPU/TileLang/ABI検証まで実行しない。
- **GroundGUI**／**TRELLIS.2**：公開元重み全LFS SHAは一致。差分は`.gitattributes`のみで、それぞれ1,570／1,519 byte。これらは推論重みではなく来歴メタデータ。ただし**TRELLISの外部DINOv3・RMBG Gated依存は依然未解決**。

## 2. 交換・追加・保留の決定

**維持確定**：5件は現行のモデル選定をすべて維持し、公開元の大容量重みシャードの再取得を次の通常キューから除く。ただし現物が未発見、ローカルSHA不一致、改訂違いなら、即取得せず別途復旧判断。削除・上書きは行わない。

**具体的な取得前候補**：[差分17ファイルの非実行manifest](../../queues/proposed-v52-r125-five-root-small-deltas.json)にパス・バイト・上流Git blob SHA1/LFS SHA256・実装上の注意を記録。暫定の論理byte総量は4,329,188、同一Git blobを内容重複排除する場合の最小参照量は4,326,099。既存HDDに同一内容がある場合の実増分はもっと小さくなる可能性がある。

**保留**：ACEの外部VAE/LM/Embedding、TRELLIS公開decoder・2 Gated依存は別repoであり、今回の差分17ファイルには含めない。全モデル完全オフライン復元とユーザーの合法的取得資格を確認するまでは、元の`queues/approved.json`を変更しない。

**無検閲の原本**：Interpretic v2の発行者BF16、0bserverx RVNのF16、v51 DaisyRose全BF16、v52 pi RL-LoRAは別学習結果。Q4/Q5/Q8など通常の追加量子化を独立モデルに数えない。pi adapterはQwen親の学習時revisionが明示されないこと、独立tokenizerのSHAが親と異なることが既存調査で確認され、親版の不一致を許可せず修正対象に残す。将来の一律禁止確率は不明であり無許可取得根拠にしない。

## 3. H／T／D／C／Uと変数表

| 記号 | 意味（日本語） | 単位・SI | 定義 | 定義域／前提条件 | 型 |
| --- | --- | --- | --- | --- | --- |
| `N_f` | 公開元原本ファイル総数 | 1（無次元） | 今回5repoのfile path総数 | 85 | 整数スカラー |
| `N_v` | 過去台帳の選択ファイル件数 | 1（無次元） | 同一revisionで当時報告された件数 | 68 | 整数スカラー |
| `N_u` | メタデータ上の未収録ファイル件数 | 1（無次元） | 5repoそれぞれのcount差の和 | 17、物理的欠損ではない | 整数スカラー |
| `S_f` | 公開元5repo容量 | byte（情報量） | 5repoの固定source全ファイル和 | 84,656,032,539 | 整数スカラー |
| `S_v` | 過去台帳の当該5repo選択容量 | byte（情報量） | 当該repo source_bytes和 | 84,651,703,351 | 整数スカラー |
| `S_u` | メタデータ上の未収録source量 | byte（情報量） | 元repoと報告容量の差 | 4,329,188 | 整数スカラー |
| `P_i` | 元モデル学習済み総数 | 1（パラメータの個数、無次元） | MoE inactive expertと外部学習部品を範囲を明記して数える | unknownなら最終lock不可 | 整数／欠損 |
| `H_{k}` | 取得元とのSHA一致状態 | 1（無次元） | 全桁一致の必要条件 | True/False/未観測 | カテゴリ |

**次元チェック**：ファイル件数同士、バイト量同士のみ差が取れる。SHAはハッシュ値であり、容量やモデル総パラメータ数ではない。5モデルの未収録ソース総量は**84,656,032,539 byte − 84,651,703,351 byte ＝ 4,329,188 byte**。オーナーHDDの空き、RAM、実行時間はこの差分から推定できない。

**H（反証可能仮説）**：履歴が同じ固定revision・全重量SHAで正しいなら、欠落しているpublisher原本の相違は17小ファイルに限定される。  
**T（最小検証）**：5repoの公開全85ファイルと履歴68ファイルを照合。各repoで未収録数とbyte数を組合せ探索（n_min=5repo、85files）。Owner Dで全85論理パスとlocal SHAを読み取り照合。STOPはrepo/版/本人権限・sha・残床違反。  
**D（合否）**：PASS_METADATA＝5repo各1解、23重みSHA一致、欠落17ファイル/4,329,188 byte。FAIL＝独立owner再ハッシュで重み不一致、別revision、実装不可能な依存を黙って除外。UNCERTAIN＝ユーザーの現物・LICENSE・実行ABI・Gated権限。  
**C（破れ方）**：台帳が意図的に別の軽量ファイル集合を選択した、同じファイル数とバイトで別の組合せが存在する、現物が別ドライブにある。今回同一revと候補集合について2番目の同数同バイト解は見つからなかったが、物理認定とは別。  
**U（不確かさ）**：公開元metadata時点、過去台帳の信頼性、ローカル実体と保存場所、実装ABI、権利・Gatedの個人差。反復測定結果の統計分散がないため合成標準不確かさ`u_c`と包含係数`k`は数値化不能。

**ERROR CHECK**：5repo、85 publisher files、68 ledger files、17 unique missing files、4,329,188 byte、重量とtokenizerなどpublisher SHA23件一致・衝突0。原本の本体ダウンロードは行わず、現行v52 selection／正式承認キュー不変更。

**転用分野**：デジタルアーカイブ（コンテンツアドレス・論理パス復元）、ML再現性（原本と推論カーネル・ABI）、ソフトウェア供給網（不変revisionとSHA）、情報法（保存できる事実と正規アクセスを区分）。

## 4.〈次に考える問い〉

**実機Dドライブ上で、現在の報告SHA一致23ファイルが本当に存在するなら、次に17の小さな差分を補完することで、外部依存のないRWKV/iLLaDAの完全再現率をどこまで上げられるか。**
