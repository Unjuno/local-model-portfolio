# R122｜v50独自原本5件の公開元ファイル固定・依存ゲート再設計（2026-11-19）

## 1.〈本論〉確定したのは取得元と保存範囲であり、ダウンロード許可ではない

対象正本：`catalog/CURRENT.json` → **v50（203登録、156有効）**。旧R117で最優先A群に入れた5モデルについて、Hugging Face**完全40桁revision**の`/tree/{revision}?recursive=true`を再照合し、重み・索引・トークナイザー・パイプライン設定・配布者コード等のファイル名とbyte、LFS SHA256、非LFS Git blob SHA1を[全85ファイルの研究用候補](../../manifests/drafts/r122-v50-five-originals-and-dependency-sources.candidate.json)に記録した。

| 保存対象原本 | publisher full source (byte) | ファイル／LFS SHA256件数 | source判断とSTOP |
| --- | ---: | ---: | --- |
| [`RWKV/RWKV7-7.2B-20260805`](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 14,402,000,339 | 19／3 | **A0**：SOURCE_PINNED_RIGHTS_RUNTIME_UNVERIFIED |
| [`GSAI-ML/iLLaDA-8B-Base`](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 16,512,918,618 | 16／5 | **A1**：SOURCE_PINNED_PARAMETER_AND_CODE_DISCREPANCY |
| [`PrentisAI/GroundGUI-8B`](https://huggingface.co/PrentisAI/GroundGUI-8B) | 17,550,250,270 | 17／2 | **A1**：SOURCE_PINNED_MODEL_DATA_RIGHTS_SEPARATE |
| [`ACE-Step/acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | 19,953,378,268 | 11／5 | **H_DEP**：ROOT_PINNED_PUBLIC_DEPENDENCIES_SOURCE_ONLY |
| [`microsoft/TRELLIS.2-4B`](https://huggingface.co/microsoft/TRELLIS.2-4B) | 16,237,485,044 | 22／9 | **H_GATE**：ROOT_PINNED_GATED_DEPS_BLOCK_OFFLINE |
| **合計** | **84,656,032,539** | **85／24** | 五つのmodel repoだけのサイズ、外部依存なし |

旧R117のsource対象選択合計84,651,703,351 byteと比べ、publisherリポジトリ**全件**の和は**4,329,188byte多い**。特にACE-Stepの`silence_latent.pt`が含まれる。これは一部のファイルがR117の「選択source」から外れていた差であり、意図的に除いた任意ファイルと漏れを区別しなければならない。

### 各原本の競合・独自性・次の判定

**1. `RWKV/RWKV7-7.2B-20260805`（A0）** — 公式RWKV-7の反復状態モデル。7,199,932,416要素BF16。旧来のTransformer系や量子化派生で代替不可。

次段：publisher release-manifest（個々のSHA256）とSOURCE SHA整合を検証し、runtime/kernel.pyのコード監査。

**2. `GSAI-ML/iLLaDA-8B-Base`（A1）** — 12T tokens事前学習の双方向masked diffusion Base。ARLoop/RWKVとは生成機構が異なる。

次段：publisherカード7.62B対HF実serialized 8.250462208Bの計数範囲とLICENSE/remote codeを監査。

**3. `PrentisAI/GroundGUI-8B`（A1）** — Qwen3-VL-8BからScreenRefで学習したGUI指示→クリック座標特化フル重み。Faraの全操作agentとは違う。

次段：モデルApache2本文・元Qwenとの再配布権の一致とSYSTEM prompt/eval ABIを確認。ScreenRef画像は取得対象外。

**4. `ACE-Step/acestep-v15-xl-turbo`（H_DEP）** — F32シリアライズ4,987,310,726要素の4B級音楽生成XL蒸留モデル。システム全体はVAE/LM/Embeddingの追加学習済み部品が必要。

次段：独立main repoのVAE/LM/Embeddingを固定。既存Qwen-Embedding同一SHAなら物理重複排除。torch pickle/ABI・ライセンスを確認。

**5. `microsoft/TRELLIS.2-4B`（H_GATE）** — 形状とPBR材質を作る3D生成/1024 cascade。512・1024 checkpoint双方をpipeline.jsonが参照。

次段：外部公開sparse decoderを固定済み。DINOv3 vitl（manual）/RMBG2.0（auto）の本人許可・使用条件を先に確定。


**iLLaDAの注意**：[作者カード](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base)では7.62B、固定repoのHugging Face `safetensors` APIでは**8,250,462,208個のBF16要素**。同一の「厳密全総数」として混ぜず、重み共有・パラメータの数え方を別検証する。どちらも現行150B基準を大幅に下回るが、正確な構成全体の監査を完了した意味にはならない。iLLaDAは`trust_remote_code`を前提とするため、コードを取得しても自動実行しない。

## 2.〈応用・転用例〉依存部品・重複排除の具体的な交換

**ACE-Step** — [公式導入ガイド](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INSTALL.md)が必要とするVAE、1.7B LM、Qwen3 Embeddingを、同じ公式`ACE-Step/Ace-Step1.5`の固定revision `19671f406d603126926c1b7e2adc169acbcade22`から**23ファイル、5,300,324,640byte**として選択。別の2B Turbo DiTを5ファイル丸ごと除外し、XL Turboの別学習成果だけを対象にする。親側の`Qwen3-Embedding-0.6B/model.safetensors`と`tokenizer.json`は既存履歴にある`Qwen/Qwen3-Embedding-0.6B`のPublisher SHA256と完全一致（対象合計**1,203,010,121byte**）。**物理ファイルが既に存在しlocal SHA一致なら再取得せず、復元に必要な二つの論理パスを保持**する。過去台帳のVERIFIEDは今回のDドライブ再ハッシュではないため、重複削減済みと断定しない。

**TRELLIS.2** — 公式[ソース](https://github.com/microsoft/TRELLIS.2)の`pipeline.json`は既定`1024_cascade`で512と1024のモデル両方を参照する。大容量を減らす目的だけで512を不要な量子化版と誤認して削除しない。別の公式`microsoft/TRELLIS-image-large`固定revision `25e0d31ffbebe4b5a97464dd851910efc3002d96`から必要なsparse decoder 2ファイル**147,592,217byte**を研究sourceに限定した。ただし以下の2依存は別配布元で現在Gatedであり、本体repoの署名やMITタグでは取得資格を得られない。

| 外部学習済み依存 | Hub観測 | 判断 |
| --- | --- | --- |
| [facebook/dinov3-vitl16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m) | **manual Gated**、ライセンスタグother | 本人の正規承認・LICENSE正文未確認：**完全bundleの取得停止** |
| [briaai/RMBG-2.0](https://huggingface.co/briaai/RMBG-2.0) | **auto Gated**、ライセンスタグother | 同じく正規条件が成立するまで停止 |

モデルを保存しても、**完全オフライン動作や権利を証明しない**。TRELLISはLinux+CUDA専用コード、公式READMEではNVIDIA 24GB以上でテストと記載し、これはユーザーの機種での実測ではない。<escape><</escape>16GB VRAM等で確実に動くと主張しない。

### 容量の下限ではなく「source論理量」としての比較

5モデル全repoと、上記の公開依存2repoの**選択済み部分**の総量は**90,103,949,396byte（十進90.104GB）**。既存Qwen Embeddingの同一SHA2ファイルがユーザーHDDで本当に存在・一致したと仮定すれば**88,900,939,275byte**の論理容量に減らせる可能性がある。ただしTRELLISのGated2依存、OS/ABI runtime、実staging/cacheと物理HDD実測はこれに含まない。

**新しい量子化形式を追加して保存枠を埋めるのではなく、既存の無検閲Interpretic v2 BF16とRVN F16のマスター方針を維持**する。すでに取得報告されるQ4を削除せず、同じ学習成果のQ4/Q5/Q8やF16派生を別の資産として重複登録しない。

## 3. 配布政策と停止ゲート

米BISの[2026-11-16遠隔計算資源に関する公式発表](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は、半導体・海外データセンターの遠隔計算アクセスに関する規制であり、個人のローカル公開ウェイト所有を一律禁止する根拠ではない。公開停止・Gated化・権利条件の変更はあり得るが、発生確率や施行日を勝手に数値化しない。

モデルの取得を許可する条件は**(a)全モデル総学習済みパラメータ数（MoEの全expert）、(b)モデルと依存ごとの利用条件、(c)不変revisionと全選択ファイルSHA、(d)ユーザーの現在のDドライブ空きと200GB残床、(e)明示的な対象ファイル承認**。本調査では各source metaを固定したが、権利/本人Gated/実機/コード監査のゲートは未完了。既存v50/156選定、`queues/approved.json`、重み実体は変更しない。

## 4. 変数表と単位確認

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・範囲・前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `N` | 今回の原本モデル数 | 1（無次元） | 固定Publisher repoのユニーク数 | 5 | 整数スカラー |
| `F` | 固定ファイル数 | 1（無次元） | 5repoの重み・設定等のファイル総数 | 85 | 整数スカラー |
| `S` | 5repo全ソース論理容量 | byte（情報量） | 5repoのsource file bytes和 | 84,656,032,539byte | 非負整数スカラー |
| `E` | 公開依存sourceの選択容量 | byte（情報量） | ACE親の23ファイルとTRELLIS decoder2ファイル | 5,447,916,857byte | 非負整数スカラー |
| `D` | 他資産と完全ハッシュ一致した容量 | byte（情報量） | ACE parent中のQwen Embedding重み+tokenizer | 1,203,010,121byte、実体未再ハッシュ | 非負整数スカラー |
| `R` | 実行環境のピークRAM | byte（情報量） | OS/モデル/エンコーダー/KV/ランタイム等の実測合計 | 未測定、512GB未満の個別審査要 | 非負実数/欠損 |
| `P` | モデルの学習済み総パラメータ数 | 1（個数／無次元） | 非活性MoE expertを含む | 未確認なら最終lock停止、150B以上は実測付き例外審査 | 整数/欠損 |

**次元チェック**：ソース容量、共有ハッシュ容量、RAMはすべてbyteで記録できるが、ディスク容量が小さいこととRAMに収まることは別の命題。パラメータ総数`P`は個数で、byteと直接比較できない。登録容量4TBは十進byte、物理ドライブ使用可能値と一時領域は未計測。

## 5. H / T / D / C / U・ERROR CHECK

- **H**：5モデルの元revisionの重み/設定ファイルを固定し、同一SHAのQwen Embeddingを共有すれば、単なる量子化版の多重取得を減らしながら差異のある学習済み原本を維持できる。
- **T**：5repo全85ファイル、公開SHA24件、ACE親23ファイル、TRELLIS decoder2ファイルをPublisher APIで照合（全数）。ユーザー実機では改めて対象ファイルのSHA256と残容量・同一source revisionを検証。技術品質の独立評価には同一HW/clock/backend・context・batch条件で最低30試行し中央値/範囲を報告。STOP条件はGated許可なし、ファイルハッシュ不一致、権利不明、200GB床違反。
- **D**：PASS_METADATA＝5repoの一意な固定revision、85ファイル全数、24 SHA参照、元のpublisher source総量の再集計、ACE Qwen重み・tokenizer2ハッシュ一致。FAIL＝Gated依存を許可済みと見なす、重複の逆変換を元学習原本と誤認、未承認の取得・既存削除。UNCERTAIN＝Dドライブ物理存在、ライセンス行為別許可、完全オフライン復元、実機品質。
- **C**：将来、TRELLISが権利明確な新たなdecoder/DINOなし構成を公式公開すれば依存版の優先順位を変更。iLLaDAの作者表記とシリアライズ総数の差が重要な学習部品の違いを示す場合、サイズ計数をやり直す。
- **U**：物理ファイル未確認、モデルカードとシリアライズ要素数のスコープ差、LICENSE正文、OSS code ABI、GPU/CPU、世代・driver、品質測定なし。合成標準不確かさ`u_c`、包含係数`k`は反復評価未実施で算定不能。

**ERROR CHECK**：5repo、85ファイル、24公開SHA、固定ソース84,656,032,539byte。学習済み異なる重みを機械的に「規制される」とは分類しない。**ダウンロード承認0、本体DL0、実行・インストール0、既存ファイル削除0**。

**関連分野**：アーカイブ工学（参照内容一致・重複排除）、ニューラルアーキテクチャ研究（独立学習結果・共有依存）、供給網セキュリティ（code/SHA/ABI）、著作権と配布政策（Gatedと正規許諾）。

### 6.〈次に考える問い〉

**「固定ファイルが完備」より厳しい「許可された本人環境で復元可能」を満たすため、RWKV・iLLaDA・GroundGUIのうち先に実機検証する1件はどれか。**

**50字超要約**：v50の元選定5モデルをHugging Faceの不変revisionで全ファイルとSHAを固定した。ACE-Stepは独立LM/VAEの追加が必須で既存Qwen Embeddingの同一SHAにより将来重複排除が可能。TRELLISは別公開decoderに加えGatedのDINOv3とRMBGが必要なので取得停止を維持する。モデル本体の完全復元、権利、所有者HDD容量、実機性能は未検証であり、今回の全ファイル台帳は実行可能な取得キューではない。
