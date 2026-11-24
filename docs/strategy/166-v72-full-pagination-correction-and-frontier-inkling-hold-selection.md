# R166／v72（2026-11-25）：Inkling Small系の「原本不完全」誤判定を訂正し、4独立保存状態を正式研究HOLD登録

## 1.〈本論〉最優先の監査結果

**以前のR164研究マニフェストは、5配布元の完全ファイル一覧ではなかった。** Hugging Faceのモデル`/tree/<sha>?recursive=true&expand=true` APIは、`expand=true`の場合**50ノード／ページ**となる。ページ末のHTTP `Link: <...cursor=...>; rel="next"` をたどらなかったため、原本の後方にある重みシャード・MTP・Tokenizerなどを欠落させた。**R164の「完全」の表現は撤回し、R166のページ送り後データのみを不変原本一覧の現行根拠とする。** 一次仕様：[Hugging Face `list_repo_tree`](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api)。

| 凍結したPublisher原本 | R164旧ファイル／byte（不完全） | R166訂正済み完全ファイル／byte | 追加で発見したファイル |
|---|---:|---:|---:|
| [Inkling Small](https://huggingface.co/thinkingmachines/Inkling-Small) | 48／531,916,781,513 | **50／531,944,669,421** | +2 |
| [Inkling Small Abliterated](https://huggingface.co/distributedcognition/Inkling-Small-abliterated) | 47／698,246,149,596 | **48／698,246,151,509** | +1、Gated-auto・SHA26件マスク |
| [Inkling 2 Small NVFP4](https://huggingface.co/thinkingmachines/Inkling-2-Small) | 43／393,510,050,371 | **43／393,510,050,371** | 0 |
| [Inkling 2 Small MXFP8](https://huggingface.co/thinkingmachines/Inkling-2-Small-MXFP8) | 49／553,004,791,314 | **61／622,833,459,732** | +12、約69.83GB |
| [Inkling 2 Small Uncensored](https://huggingface.co/OpenUncensored/Inkling-2-Small-Uncensored) | 49／553,004,704,928 | **61／622,833,373,184** | +12、約69.83GB |

**5配布元総計263ファイル／2,869,367,704,217byte、公開元LFS SHA256参照165件、GatedでマスクされたLFS SHA26件**。R164の236ファイルから**27ファイル増加**。研究目的のPublisher原本メタデータ取得のみで、モデル重量ペイロードは一切転送していない。

根拠：[ページ送りした5原本の全SHA・サイズ](../../manifests/drafts/r166-2026-11-25-inkling-small-five-complete-paginated-original-sources.candidate.json)。この修正を残さないと、モデルが完全であるという虚偽の判定から保存・復元失敗につながる。

## 2. 原本と無検閲の独立状態を区別した正式v72

v71の**260資産・210有効・SELECT56／CONDITIONAL154／HOLD31**から、旧260件を完全に維持したまま、**4件の異なる学習済み原本または重み編集状態を正式HOLD**に追加する。**v72は264資産・210有効・HOLD35**。新規有効資産・ダウンロード承認はゼロ。

- **HOLD／原版**：`thinkingmachines/Inkling-Small`（276B総・12B活性、別学習成果）。
- **HOLD／旧版の独立重み編集**：`distributedcognition/Inkling-Small-abliterated`（Gated-auto・Publisher SHA26件マスク、独立編集された状態。ただし別の事前学習モデルではない）。権限のないGated取得を禁ずる。
- **HOLD／新原版**：`thinkingmachines/Inkling-2-Small`（594B総・17B活性、NVFP4、393.510GB）。**Mini系とは別のモデル**。
- **HOLD／新無検閲編集状態**：`OpenUncensored/Inkling-2-Small-Uncensored`（594B原版から独立に拒否方向編集されたMXFP8重み、622.833GB）。作者の拒否評価は独立ベンチマーク未実施。単体39KB編集情報の存在をもってオフライン復元成功とはしない。

**`thinkingmachines/Inkling-2-Small-MXFP8`は後者の必須親表現だが、追加学習済みの別モデルではないため、**正式モデルIDとして二重計上しない。量子化や編集済みの容量を、アーキテクチャ総パラメータ数と混同しない。登録上の2つの594B model IDのうち、無検閲編集は新しい事前学習ではなく**別の保存すべき学習後の編集結果**である。

### 無検閲編集での原本再利用の実測前提

公式MXFP8親と無検閲編集済みMXFP8を、同一パスとPublisher Git Blob OID/SHAが完全一致するファイルで比較すると、**11ファイル・56,755,370,428byte**が共通する。無検閲編集後の残り**566,078,002,756byte**は単純なPublisherファイルSHA同一性が証明されていない。これは**実機ディスク追加量ではなく、Publisherの参考値**。

編集者が公開する`edit.pt`の参照サイズは**39,174byte**、LFS SHA256は`58554a71aedb111f48cced364c035f102ccfd114e250dba6e165b929d356301a`。再現には**正確な親MXFP8**と編集演算・scale/zero-point・確率的丸め・PyTorchコンポーネントの審査が必要であり、**NVFP4親と39KB差分だけで無検閲MXFP8を完全再現できるとは断定できない**。作者[編集手順・試験](https://huggingface.co/blog/OpenUncensored/inkling-2-small-uncensored)も個別実機の再現性を保証するものではない。未審査のpickle `.pt`をロード・実行しない。

## 3. 大型原本のHOLDと、容量を抑えた互換形式の研究

4新HOLD資産の原本4repoのPublisher参照量は**2,246,534,244,485byte（十進約2.247TB）**。この数値に、編集MXFP8再適用の親MXFP8重みを二重で加えて自動DL計画にしてはいけない。ownerの歴史的取得報告は**116資産／約2.022TB**だが、現HDDの容量・重複領域・実空き・ステージングは独立確認されていない。最大4TB・最低200GB空きの制約を満たす証拠は**ない**。したがって本版で実取得は認めない。

比較研究として、[UnslothのInkling 2 Small GGUF](https://huggingface.co/unsloth/Inkling-2-Small-GGUF/tree/42593c63926d23380ea03d643ab2cde742427608)の**原本と同一学習結果から変換した**3形式の不変ソースを別に固定した。全repoを取得すると4.7TB超の複数形式が入り予算を破るため、**必要なフォルダだけが選択単位**となる：

| 研究用の代替形式 | GGUF分割ファイル合計（十進） | 状態 |
|---|---:|---|
| `UD-IQ2_XXS` | 190,584,243,104byte／5ファイル | 低容量・大きな精度損失の可能性。未実測 |
| `UD-Q3_K_XL` | 285,128,587,168byte／7ファイル | 品質と容量の中間。未実測 |
| `UD-Q4_K_XL` | 354,150,001,600byte／9ファイル | より高忠実度を期待する候補。未実測 |

画像入力用`mmproj-F16.gguf`の公開元参照サイズは**658,223,328byte**。GGUFは別学習済み重みではないため、**正式な4個の新HOLD学習状態に数えない**。また元のNVFP4／MXFP8の編集効果が量子化に自動継承されると推定しない。モデルカードに挙げられた速度・品質は同一条件で独立再測定していない。[形式別ソース・SHA](../../manifests/drafts/r166-2026-11-25-inkling2-small-three-gguf-format-alternatives-UNAPPROVED.candidate.json)。

## 4. 容量計算の変数表と次元検査

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| \(B_O\) | 旧Inkling Small原本のPublisher参照容量 | byte | R166完全Treeの50ファイル合計 | 非負整数、本人実占有量ではない | 整数スカラー |
| \(B_E\) | 旧Inkling Small編集版参照容量 | byte | R166の48ファイル合計 | SHA26件マスク、本人権利不明 | 整数スカラー |
| \(B_N\) | 新Inkling 2 Small NVFP4原本参照容量 | byte | R166の43ファイル合計 | 実VRAMではない | 整数スカラー |
| \(B_U\) | Inkling 2 Small無検閲MXFP8の参照容量 | byte | R166の61ファイル合計 | `edit.pt`含む。親再利用は未実証 | 整数スカラー |
| \(B_H\) | 新規正式HOLD4個のPublisher原本参照量 | byte | \(B_O+B_E+B_N+B_U\) | 重複除去前／実HDD新規バイトではない | 整数スカラー |

\[
B_H=531,944,669,421+698,246,151,509+393,510,050,371+622,833,373,184
=2,246,534,244,485\ \mathrm{byte}.
\]

**次元検査**：各項は十進byteであり、加算結果もbyte。2.247TBは物理空きの測定値ではない。MXFP8依存・一時ファイル、完全オフラインruntime wheelhouseのサイズを除いて計算した単なるPublisher source参照量であり、4TB収容PASSを意味しない。

## 5. H／T／D／C／U・ERROR CHECK

- **H（反証可能）**：Publisher原本のページ送りを完全に扱い、実行可能性と独立保存価値を分ければ、後方シャードの欠損と大型の独立編集結果の見落としが再発しない。
- **T（最小検証）**：Hugging Face固定40桁SHA・`Link rel=next`を最後までたどり、5repo263件とSHA165件・マスク26件、前R164との差分27件を確認。v71の260資産完全一致、v72の264登録・210有効、HOLD35、全210取得STOP、`queues/approved.json`0、量子化非重複を静的試験。将来実機は同一GPU/clock/backend/batch/context/量子化scale・zero-pointで最低30回の推論ピーク測定と100件以上の固定課題を行う。
- **D（PASS/FAIL/UNCERTAIN）**：原本全ファイルと各台帳の集合一致・無承認はPASS。Gatedマスクを発行者SHAとして使用、初ページを完全と誤認、GGUFを新学習、`edit.pt`単独を完成モデル、未計測の512GBメモリ例外を承認する行為はFAIL。owner実媒体・権利・再現性・性能はUNCERTAIN→STOP。
- **C（破れ方）**：配布元変更／Gated無許諾、MXFP8編集のbit-exact再適用不可、低精度GGUFで能力劣化、他の巨大モデルとの4TB容量競合、実行GPUの不足。
- **U（不確かさ）**：Publisherメタデータ、未許諾のGated SHA、保存媒体とCAS、実行ABI、編集の確率的丸め、メーカーのみの品質報告。測定がないので合成標準不確かさ\(u_c\)と包含係数\(k\)は数値化不能。

**ERROR CHECK**：旧260資産を不変に保持。大型4原本・編集状態はHOLDのみ、独立した2Small MXFP8やGGUFを別の学習結果に数えない。v72**264資産／210有効／SELECT56／CONDITIONAL154／HOLD35**、過去116取得報告の再DL0、今回の重量転送0、承認0、オーナー媒体ハッシュ検証0、未審査モデルコード実行0、Gated迂回0。

学際：機械学習のMoE/編集方向、GPU混合精度・量子化、コンテンツアドレス型原本保全とHTTPページネーション、ライセンス／輸出管理、不確かさ評価と再現性検証。

###〈次に考える問い〉

**復元可能性を重視するなら、594Bの原本1式を確保することと、独立編集方向39KB・実行可能な小型GGUFのどちらを優先すべきか。** 現段階では原本の役割を明確に維持しつつ、実容量・権利・再現できる編集手順が揃うまで追加取得は停止する。
