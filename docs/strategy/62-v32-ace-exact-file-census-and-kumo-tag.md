# R62｜ACE-Step XL 34ファイルの正確な容量とKumo Relational v1.0.1固定監査

調査日：2026-11-14。GitHub `main`、調査開始HEAD `3bc471f3c43dacb8f167646c67fa998ca1ac3a90`、現行v32（182管理・135有効）。**保存対象の追加、ダウンロード承認、モデル実行は一切行わない。**

## 1. 一次資料と判定

- [ACE XL公式API](https://huggingface.co/api/models/ACE-Step/acestep-v15-xl-turbo/revision/d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee?blobs=true)：11ファイル、**19,953,378,268 byte**。F32 indexのtensor payload19,949,242,904 byteとは異なる。
- [ACE共有元公式API](https://huggingface.co/api/models/ACE-Step/Ace-Step1.5/revision/19671f406d603126926c1b7e2adc169acbcade22?blobs=true)：通常版2B DiTの5ファイルを除く23ファイルで**5,300,324,640 byte**。1.7B音楽LM、Qwen3-Embedding、VAEとrootメタデータを含む。root configは通常版由来なのでXLのconfigとして流用しない。
- 既存[Qwen source](../../catalog/capacity/2026-11-06/sources/model--Qwen--Qwen3-Embedding-0.6B.json)との同一LFS SHA-256／Git blob識別子の一致：**4種類・延べ6参照、1,211,907,493 byte**。一致するのはmodel.safetensors、tokenizer.json、merges.txt、vocab.json。LM/Embeddingの語彙重複も再度引かず、1度だけ控除。
- **ACE新規既知ソース増分24,041,795,415 byte**、v27＋後続8件の既知部分3,442,028,436,758 byteに加えた**見積り上のソーススコープ算術3,466,070,232,173 byte**。これは全135件の完全オフライン復元に必要な総量ではない。

## 2. ソース34ファイル

Git blob SHA-1とLFS SHA-256を同じ種類のハッシュとして扱わず、配布元の識別子でのみ比較する。ローカルSHAは未測定。

| No. | 区分 | ファイル | byte（正確） | 公開元識別子 | 容量処理 |
|---:|---|---|---:|---|---|
| 1 | XL | `.gitattributes` | 1,519 | `a6344aac8c09253b3b630fb776ae94478aa0275b` | NEW_SOURCE_ID |
| 2 | XL | `README.md` | 4,106 | `1a0e8752fe0703c9fecd900dbb9a49b82c57c998` | NEW_SOURCE_ID |
| 3 | XL | `config.json` | 2,407 | `0b360602d32112044b2c6f761b07ed8c06f2fba6` | NEW_SOURCE_ID |
| 4 | XL | `configuration_acestep_v15.py` | 13,225 | `e54e1c82f004851d356a0589c8ea94227ed61274` | NEW_SOURCE_ID |
| 5 | XL | `model-00001-of-00004.safetensors` | 4,986,971,456 | `e54a8413c981797312f53d512dec9944023d03f42f0740cbe86f62582cc27bdc` | NEW_SOURCE_ID |
| 6 | XL | `model-00002-of-00004.safetensors` | 4,986,942,776 | `b45f788b6dc9f15957cfa3d9b403f25f3f64c5211ecaf18dda45b67ea6470664` | NEW_SOURCE_ID |
| 7 | XL | `model-00003-of-00004.safetensors` | 4,986,942,808 | `a4f6bd572eab79cf5f3e4678796f904c6d6c33680a3e6ed09034d6de7cabea4d` | NEW_SOURCE_ID |
| 8 | XL | `model-00004-of-00004.safetensors` | 4,988,483,464 | `a868b05493c73808408f58b33a903371bb2846b53c8b19bd7476991bc8837259` | NEW_SOURCE_ID |
| 9 | XL | `model.safetensors.index.json` | 71,471 | `d383f21e424f222cf9af0677ca983d71ffac34b5` | NEW_SOURCE_ID |
| 10 | XL | `modeling_acestep_v15_xl_turbo.py` | 103,821 | `0c1ae8cad0365849a99e894c483316ebf4760b1a` | NEW_SOURCE_ID |
| 11 | XL | `silence_latent.pt` | 3,841,215 | `a778e9dd942f5e8b2c09c55370782d318834432b03dabbcdf70e6ed49ad6358b` | NEW_SOURCE_ID |
| 12 | 共通 | `.gitattributes` | 1,740 | `a8d4cbb214bda0ce6b6e4453c02ca1a826b9f08a` | NEW_SOURCE_ID |
| 13 | 共通 | `Qwen3-Embedding-0.6B/added_tokens.json` | 707 | `b54f9135e44c1e81047e8d05cb027af8bc039eed` | NEW_SOURCE_ID |
| 14 | 共通 | `Qwen3-Embedding-0.6B/chat_template.jinja` | 4,116 | `699ff8df401fe4788525e9c1f9b86a99eadd6230` | NEW_SOURCE_ID |
| 15 | 共通 | `Qwen3-Embedding-0.6B/config.json` | 1,359 | `21bd712c76114dc22587c6eeb84ab64186c9d245` | NEW_SOURCE_ID |
| 16 | 共通 | `Qwen3-Embedding-0.6B/merges.txt` | 1,671,853 | `31349551d90c7606f325fe0f11bbb8bd5fa0d7c7` | REUSE_QWEN_V27 |
| 17 | 共通 | `Qwen3-Embedding-0.6B/model.safetensors` | 1,191,586,416 | `0437e45c94563b09e13cb7a64478fc406947a93cb34a7e05870fc8dcd48e23fd` | REUSE_QWEN_V27 |
| 18 | 共通 | `Qwen3-Embedding-0.6B/special_tokens_map.json` | 613 | `ac23c0aaa2434523c494330aeb79c58395378103` | NEW_SOURCE_ID |
| 19 | 共通 | `Qwen3-Embedding-0.6B/tokenizer.json` | 11,423,705 | `def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a` | REUSE_QWEN_V27 |
| 20 | 共通 | `Qwen3-Embedding-0.6B/tokenizer_config.json` | 5,404 | `ddaf69808214a44fdd26d3785b66c1367c78277a` | NEW_SOURCE_ID |
| 21 | 共通 | `Qwen3-Embedding-0.6B/vocab.json` | 2,776,833 | `4783fe10ac3adce15ac8f358ef5462739852c569` | REUSE_QWEN_V27 |
| 22 | 共通 | `README.md` | 5,496 | `a3115cec283fbdc2d500aa50fdffac3c87e6689a` | NEW_SOURCE_ID |
| 23 | 共通 | `acestep-5Hz-lm-1.7B/added_tokens.json` | 2,217,787 | `584075018edeacd6dcc031b3e2cbbf90836eba41` | NEW_SOURCE_ID |
| 24 | 共通 | `acestep-5Hz-lm-1.7B/chat_template.jinja` | 4,168 | `01be9b307daa2d425f7c168c9fb145a286e0afb4` | NEW_SOURCE_ID |
| 25 | 共通 | `acestep-5Hz-lm-1.7B/config.json` | 1,385 | `1325891e0f2cb06ea22906f9c89047d09d0dac1f` | NEW_SOURCE_ID |
| 26 | 共通 | `acestep-5Hz-lm-1.7B/merges.txt` | 1,671,853 | `31349551d90c7606f325fe0f11bbb8bd5fa0d7c7` | REUSE_QWEN_V27 |
| 27 | 共通 | `acestep-5Hz-lm-1.7B/model.safetensors` | 3,708,521,528 | `f161689da73e5ecefa28ff780d51c2d92a00f056d021d7933c779ed5c6cd7db8` | NEW_SOURCE_ID |
| 28 | 共通 | `acestep-5Hz-lm-1.7B/special_tokens_map.json` | 1,824,199 | `aa26266349a0f38be608e07138c9047356309551` | NEW_SOURCE_ID |
| 29 | 共通 | `acestep-5Hz-lm-1.7B/tokenizer.json` | 24,321,939 | `35af56c3f5cb3ea2cc578aa28a8937770981d504f183ac5c8c38baf4bbd4af4d` | NEW_SOURCE_ID |
| 30 | 共通 | `acestep-5Hz-lm-1.7B/tokenizer_config.json` | 14,072,925 | `6cd70cdd89425971794f5235562edcc608b0629a6c4686ae51a8b8c8b8ba5e95` | NEW_SOURCE_ID |
| 31 | 共通 | `acestep-5Hz-lm-1.7B/vocab.json` | 2,776,833 | `4783fe10ac3adce15ac8f358ef5462739852c569` | REUSE_QWEN_V27 |
| 32 | 共通 | `config.json` | 1,968 | `6a0b5c09a654614302947fd1d7041f7ed0764d8c` | NEW_SOURCE_ID |
| 33 | 共通 | `vae/config.json` | 425 | `f49eb7b261dde15ed29c0fa1e790251dcecbd280` | NEW_SOURCE_ID |
| 34 | 共通 | `vae/diffusion_pytorch_model.safetensors` | 337,431,388 | `da17edb604c40deaf09e9b24974e590d1ca83a374070e5d0884cfa4bed9a99b0` | NEW_SOURCE_ID |

## 3. 容量見積り（十進byte）

| 項目 | byte |
|---|---:|
| v27＋8ソース参考範囲 | 3,442,028,436,758 |
| ACE XL 11 + 共通23の生合計 | 25,253,702,908 |
| 元Qwenへの6参照と一致する重複 | −1,211,907,493 |
| ACEの既知内容識別子増分 | **24,041,795,415** |
| **更新後の参考容量** | **3,466,070,232,173** |
| 空の4TBかつ保存後200GBを残す仮定上の差額 | **333,929,767,827** |

注意：上記は一部ソースのSHA-aware比較と既存参照スコープの算術合計。外部Codec、環境、実HDD空き、cache/staging、ライセンスは未確定。特定のモデルが削除されるとの予言でも、取得許可でもない。

## 4. NVIDIA Kumo Relational：タグと旧版の差分

- [v1.0.1公式API](https://huggingface.co/api/models/nvidia/Kumo-Relational/revision/v1.0.1?blobs=true) はコミット `2bd603d3d8f25f67a7aaa8579908595e20567e22`、7ファイル**243,656,960 byte**。旧観測版 `3d5176e4e713d734b71c2846fc9cd19e49e4c7d1` は6ファイルで、追加のconfig.json 139 byte以外は同一。**classifier.ptとregressor.ptは両版でSHA-256・サイズ一致**。
- 用途は異なる関係表の分類／回帰であり、単純な量子化重複とは扱わない。ただしv32に未選定なので、今回の135件の保存予算へは加算しない。
- `LICENSE`と`THIRD-PARTY-NOTICES.txt`は保存監査対象。`.pt`をこの調査で読み込み・unpickleしない。

| Kumo v1.0.1ファイル | byte（正確） | 公開元識別子 |
|---|---:|---|
| `.gitattributes` | 1,519 | `a6344aac8c09253b3b630fb776ae94478aa0275b` |
| `LICENSE` | 2,693 | `161a8f01c0e68899bf4175a5c641c5fa0e9b11db` |
| `README.md` | 1,294 | `54b830a9415bf4d578e5d5af7940134940fc35c1` |
| `THIRD-PARTY-NOTICES.txt` | 1,883 | `28215aee453d02bec3fc22ac534197b7665bc7f2` |
| `classifier.pt` | 119,862,733 | `0c2e35cc18303f0d3ddeaf04e9cab6ca3a8bd6ea17195ac0e42d47af4bcb2a2d` |
| `config.json` | 139 | `5aa62853e46843ea417d3c8dd930c3e7bf976b8f` |
| `regressor.pt` | 123,786,699 | `f863b3632f738e1444fb83a8cea5746f298889b5c96953a000c4720d202ae4cf` |

## 5. 変数表・単位検証

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| B0 | 既存部分スコープ算術 | byte | 3,442,028,436,758、全件の依存閉包でない | 非負整数スカラー |
| A | ACEの34ソースファイル生合計 | byte | 25,253,702,908、公式メタデータに基づく | 非負整数スカラー |
| D | 既存Qwenと一致した重複参照の合計 | byte | 1,211,907,493、同じSHA/サイズだけ | 非負整数スカラー |
| N | 新しいACEソース増分 | byte | N=A−D=24,041,795,415 | 非負整数スカラー |
| C | 計画上限 | byte | 4,000,000,000,000、実物HDDと別 | 非負整数スカラー |
| F | 最低空き床 | byte | 200,000,000,000、実機未測定 | 非負整数スカラー |
| T | 算術的な既知ソース見積り | byte | T=B0+N=3,466,070,232,173 | 非負整数スカラー |
| H | 仮想4TB差額 | byte | H=C−F−T=333,929,767,827 | 整数スカラー |

**単位チェック**：すべてbyte同士の加減算。パラメータ数（無次元）は重みファイルbyteと同一でない。推論RAM・VRAM上限512GBは保存容量上限4TBとは別。

## 6. H/T/D/C/U・ERROR CHECK

- H: 独立に学習したXL+LM+VAEを保全し、SHAが同じQwen原本・トークナイザー/語彙を二重計上せずに復元できる。反証は同一ハッシュの欠落、誤った版構成、非公開依存、権利不適合。
- T: ACEの34ファイルを全数、Kumoのv1.0.1の7ファイルと旧版の2重みを全数静的照合。ハッシュは配布元の値、モデル自体の取得・実行は未実施。
- D: 源メタデータ上のbyte・内容重複はPASS、全体系の復元・実ディスク・許可はUNCERTAIN。違うハッシュの重みを同一と見なす、未承認取得を始めるならFAIL。
- C: 共有依存のABI・音声の利用許諾・custom Pythonのコード版・stagingにより計算が破れる。
- U: ファイルのsizeメタデータ誤りと未確定の環境/依存/権利。分布がないため合成標準不確かさu_c・包含係数kは定量化不能。
- **ERROR CHECK**：34=11+23、同一Qwen6参照、25,253,702,908−1,211,907,493=24,041,795,415、3,442,028,436,758+24,041,795,415=3,466,070,232,173、仮想差額333,929,767,827 byte。正本v32 182/135、承認0、取得0。

機械学習（学習成果の異同）、デジタル保存（ハッシュ再利用）、ソフト供給網（Git blob/LFS/ABI）、知財法務（同意・利用条件）の4分野に関連する。

## 7.〈次に考える問い〉

公開元ファイルが固定できた後、実際のオフライン再現に不足する依存・ランタイムをどの最小パッケージで検証すべきか。
