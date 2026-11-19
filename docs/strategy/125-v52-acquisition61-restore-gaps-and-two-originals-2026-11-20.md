# R125｜61取得報告と照合し、次に残すのは「不足コード16ファイル」と「独立原本2件」

**確認日2026年11月20日（JST）／正本v52＝205資産・158有効。** 現行v52のモデル選定は追加／削除0。取得の既報告・実験的保存・本人の正規承認を混同せず、無検閲の原本、再帰・拡散・音楽・生命科学という異なる学習結果の完全再現性を重視。

## 1.〈本論〉実際の取得台帳により作業対象を修正

[取得履歴](../../catalog/execution/2026-11-19-acquisition-ledger.json)の**ファイルblob `5a5de85e8e0fdc1ac2bbb7f61b369df005e63b79`**は62件のモデル試行、**61 VERIFIED・1 Gated HOLD／708ファイル／409,835,119,252byte**を記録する。従来の「53 VERIFIED」は過去時点の履歴であり最新全件数ではない。ただしこれは**取得実行ログの自己申告**で、本調査から所有者のWindows Dを独立再ハッシュ・完全offline復元していない。

| repo | 公式固定revision | Publisher全source／取得ログ | 新たな**論理source**必要部分 | 取得判断 |
|---|---|---|---|---|
| [RWKV/RWKV7-7.2B-20260805](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | `9e47155004fe9df0f2a8015efa9152595c9065be` | 19files／報告12files | **7files、337,813byte** | 元重み3shardsは取得報告済み、推論コード・NOTICEを現物で確認 |
| [GSAI-ML/iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | `a1b5b5f8a31a3854a46205ee584178c04b45ec9a` | 16files／報告12files | **4files、28,506byte** | `configuration_illada.py`・`modeling_illada.py`未報告 |
| [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | `af44b45f2e35a493886929c6d786e563ec68364d` | 22files／報告21files | **1file、1,519byte** | `.gitattributes`の差分。外部CUDA依存/ライセンス別 |
| [ACE-Step/acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) | `d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee` | 11files／報告7files | **4files、3,959,780byte** | 約20GB元重みの再取得は避け、XLコード・silence latentを確認 |
| [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | `37561816e66b5b9153b1b64c10968c18c1e6f4a0` | 32files／該当報告なし | **32files、55,586,107,015byte** | 無検閲派生・RL LoRAの比較親として原本source固定 |
| [HuggingFaceBio/Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | `17de89165e25c49e7de4f845d0e5d464469de359` | 19files／該当報告なし | **19files、29,656,358,078byte** | DNA×自然言語14.82B原本、`tokenizer.py`を必須とする |

**6 source合計**：出版社の最新repo固定ファイルから**67論理ファイル、85,246,792,711byte（25件Publisher LFS SHA256）**。このうち**16ファイル・4,327,618byte**が4件の取得ログに含まれないと推定されるメタデータ／コード補完、**51ファイル・85,242,465,093byte**がモデルの取得報告に載っていない2原本の全source。両方とも本人Dの物理不足確定値ではない。

完全なPath/bytes/Git blob SHA1/LFS SHA256は[研究専用R125明細](../../queues/proposed-v52-r125-post61-gap66plus-2026-11-20.json)、R122既存15sourceの現在との照合状況も全15件記録した。

## 2. 重複ダウンロードを避けるための証拠レベル

この差分は「旧取得ログが記載した**同じrepo・同じ40桁revision・ファイル数・整数byte**がPublisher sourceの真部分集合である」という仮定の下で、候補ファイル集合の全組合せから**該当件数と差分byteを同時に満たす唯一の集合**として推定。実際に`D:\AI-Models`のどのpathが未保存かを検査したわけではない。従って端末で確認後にのみ不足ファイルを選び、既にある重みは再転送しない。

4件に対する主な不足推定：
- **RWKV7**：`inference/generate.py`、`kernel.py`、`runtime.py`、`model_loader.py`、requirements、NOTICE、.gitattributes。重み3シャードはログに報告済み。作者の`auto`バックエンドやTileLangは固定環境・数値parityが必要。
- **iLLaDA**：`configuration_illada.py`と`modeling_illada.py`、SECURITY、.gitattributes。`trust_remote_code=True`は安易に実行しない。作者公称7.62BとHub serialized8.25Bの不一致は未解決。
- **TRELLIS.2**：.gitattributesのみのsource差分だが、[GitHub公式実装](https://github.com/microsoft/TRELLIS.2)はLinux＋NVIDIA、CUDA Toolkit 12.4推奨、nvdiffrast/nvdiffrecは別ライセンス。512と1024の異なる重みSHAを同一成果として物理削除しない。
- **ACE-Step**：`configuration_acestep_v15.py`、`modeling_acestep_v15_xl_turbo.py`、`silence_latent.pt`、.gitattributes。作者の[公式インストール案内](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INSTALL.md)は別VAE、Qwen3 embedding、5Hz LMを必要に応じて使用。`.pt`はpickle実行なしで不活性に保管。HubにLICENSE独立ファイルはなくMITタグとコード上流全文を本人行為別審査。

**未報告2原本**：QwenはLICENSE/重み/vision/processor/tokenizerを含む32-file完全source、Carbon-XはDNA専用`tokenizer.py`と二つの大きな学習済みshardを含む19-file source。Carbon-XはモデルカードApache 2.0（単独LICENSE不在）、`trust_remote_code`での専用tokenizer実行前にコード監査が必要。R119がCarbon-Xを10fileとしていた事実を「全原本」とは解釈しない。

## 3. R122の既存15sourceとの統合判定

既存[R122の15元source](../../queues/proposed-v50-r122-deduplicated-next15-sources.json)の内容は変更しない。新61件ログではRWKV/iLLaDA/TRELLISについて**原本重みは検証済みと報告**、ZONOS3の既取得0.776GBとR122の15.346GBは異なるfile scope、RVNの既取得Q4とR122 F16は**異なる形式**。ソース容量から既取得byteを無条件に引くことを禁止する。R122の取得指示は、依然として個別LICENSE・実D容量・200GB安全床・同一SHAスキップ・本人承認が必要である。

**成果優先**：①既報告ファイルの現物ハッシュと不足16メタデータの確認、②未報告の公式Qwen27B原本sourceを固定して親/派生比較、③Carbon-X専門モデルの権利・custom tokenizer・環境を確認して保存、④その他R122の非重複sourceを検討。無検閲BF16/Hereticの既存R122保存候補は維持するが、同じチェックポイントの量子化形式を別資産として増やさない。

## 4. 規制の事実、予測と保全

2026-11-19 [米Federal Register 2026-23529](https://www.federalregister.gov/d/2026-23529)は旧AI Diffusion Rule由来ECCN 4E091のモデルweight区分を撤廃。遠隔計算資源・高度半導体・用途別の規則とは別。公開重みが一律に個人所持禁止になったとは主張しない。配布者Gated、ライセンス、目的/国、配布削除と独立して監視する。今回の6モデル固有の強制削除日や規制確率を創作しない。

## 5. 変数表と次元チェック

| 記号 | 意味（日本語） | 単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `S_4` | 既取得報告4repoとPublisher sourceの差分 | byte（情報量単位） | 4327618 | 内容の現物不存在は未検証 | 非負整数スカラー |
| `S_2` | 取得ログ未記載の2原本のPublisher source合計 | byte | 85242465093 | 未報告≠物理未取得 | 非負整数スカラー |
| `S_6` | 新たに研究固定した追加候補ファイル量 | byte | `S_4+S_2` | 学習済み依存/ランタイム容量外 | 非負整数スカラー |
| `F` | 残すべき物理最低空き | byte | 200000000000 | 転送中、キャッシュ含む | 非負整数スカラー |
| `D` | Dドライブの**現在の**実空き | byte | null（未測定） | 履歴ログの空きとは違う | 非負整数/nullスカラー |

`S_6=4327618+85242465093=85246792711 byte`。byte同士の加算なので次元整合PASS。この見積もりから実機の余剰空き、OS/VRAM、実用性は証明できない。型/単位を混同せず4TB論理保存枠・200GB物理床・<512GB完全実測ピークRAMの別規則を維持する。

## 6. H / T / D / C / U、ERROR CHECK

**H**：モデルごとにPublisherの必須ソースと取得ログをファイル水準で比較することで、重複DLを減らし、コード欠落によるoffline復元失敗を回避できる。**T**：今回6repoの同revision全ファイル集合の件数/byteを再検証し、4repoについて必要差分の組合せ一意性を全探索（n_min＝6モデル、論理file選択67）。ownerでは該当ファイルをsha比較してから段階停止。**D**：PASS_METADATA＝6ID全てv52 active、4repoは同revisionの差分集合唯一、67 logical refs/sha全件検査、R122重複把握。FAIL＝偽りのHDD空き・異なる版・LICENSE違反・未承認転送。UNCERTAIN＝保存済みファイルの実HDD SHA、本人権利、依存/ABI/オフライン復元。
**C**：古い取得アプリがこの16メタデータを別階層に保存済み、または外部環境が不足を補い旧file subsetでも動く場合、追加物理増分は小さくなる。**U**：ログの時差、HDD実ファイル、別学習済み依存、ライセンス正文、実機backend/zero-point/context/batchが主誤差源。統計反復なしのため合成標準不確かさ`u_c`と包含係数`k`の数値推定はしない。

**ERROR CHECK**：v52 205/158（旧採否不変）／取得報告61 VERIFIED・708files・409835119252byte／本R125候補6repo・67論理files・85246792711byte／owner現物独立再ハッシュ0、正式ダウンロード承認0、今回の重量取得0、既存ファイル削除0。

関連分野：AIモデル学習と推論アーキテクチャ、デジタル長期保全とハッシュ、ソフトウェアサプライチェーン、ライセンス・輸出管理、Windows/Unixファイルシステム。

## 7.〈次に考える問い〉

**「取得台帳で61モデルVERIFIED」という指標よりも、依存・実コード・hashを含む完全offline再現の合格数を増やすには、どの不足16ファイルを優先して物理再照合すべきか。**

