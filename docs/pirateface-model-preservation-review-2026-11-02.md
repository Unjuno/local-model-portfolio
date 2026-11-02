# Pirate Faceの2026年11月2日投稿：モデル保全の代替索引と小型モデル選定

> **2026-11-02調査、保存・取得未承認。** [Xの元投稿](https://x.com/thepirateface/status/2117074235965215181)は「新規1000件のモデルTorrent」と述べ、[ユーザー共有の続報](https://x.com/thepirateface/status/2117074347752149358)はAEON Qwen、MOSS LoRA、Mango、Huihui等を紹介する。1000件の申告は**配布者の主張**であり、当方で全1000件・完全シード・原本同一性を確認したわけではない。

## 1. Pirate Faceの適切な位置づけ

[公式説明](https://pirateface.co/how-it-works)および[掲載ポリシー](https://pirateface.co/policy)を確認。サービスは、Hugging Face原本のrepo ID/完全revision/ハッシュとコミュニティTorrentを関連づける**二次取得先の索引**。モデルの実体ファイル自体はホストしないと説明する。

- **価値**：Hugging Faceが配布を停止した場合にも、権利ある完全なコピーを保持するpeerがいれば補助経路になり得る。原本のチェックサムと独立に照合するという発想は、ポートフォリオの保存証跡に合う。
- **限界**：Torrentの登録、BitTorrent piece check、公開Seeder数は、必要なモデル全ファイルを最後まで取得できる保証ではない。登録Torrentは元repoの**一部ファイルだけ**の場合もある。配布元のSHA-256との独立照合、指定revの完全性、使用許諾が必要。
- **ライセンス**：サービスはMIT/Apache-2.0/OpenMDWなどの再配布可能なモデルを中心にし、Gemmaなど特別条件には個別の規約同意を要求すると説明。**Gatedのアクセス・配布制限や非商用・第三者データの権利を回避できるという意味ではない**。削除済みリポジトリは独立審査対象。
- **安全・プライバシー**：P2Pは参加peerの公開IPを他peerへ知らせる。匿名性やホストの安全を保証しない。配布サイトが提供する`pip install pirateface`、`skill.md`、シェルスクリプト、自動フックの導入をこのレビューでは実施・承認しない。

## 2. 投稿のモデルをそのまま採用してはいけない

| 配布元ID | 公開原本の観測 | 判定 |
| --- | --- | --- |
| [AEON NVFP4 MIXED](https://huggingface.co/AEON-7/Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED-NVFP4-MIXED) | 約24.717GB。配布者がAEON BF16からのNVFP4派生と明記 | 同一系列の量子化を二重採用せず監視 |
| [AEON BF16](https://huggingface.co/AEON-7/Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED-BF16) | 約55.585GB。Qwen3.8-27Bの独自改変重み | 既存Qwen3.8/Orcarouter Gated派生と容量・独立性を比較するまで保留 |
| [MOSS Beauty LoRA](https://huggingface.co/axiomofmind/Moss-image-beauty-lora) | 主adapter約74.377MB、ただし依存[OpenMOSS MOSS-Image-SFT](https://huggingface.co/OpenMOSS-Team/MOSS-Image-SFT)全repo約27.229GB | 小容量単体で実行できない。基盤モデルと肖像権確認まで保留 |
| [mango FlashNext IQ4XS](https://huggingface.co/isilicon/mango-qwen38-flashnext-iq4xs) | GGUF重み約98.422GB。配布カードは別GGUFからの量子化・mirrorとタグ付け | 高容量・派生重複。優先せず監視 |
| [Huihui Qwythos abliterated](https://huggingface.co/huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated) | 約19.333GB、元モデルは`empero-ai/Qwythos-9B-Claude-Mythos-5-1M` | 別のabliteration派生。名前の`Claude-Mythos`はAnthropicの原本重みである証拠ではない |
| [EfficientViT B1](https://huggingface.co/timm/efficientvit_b1.r288_in1k) | 主Safetensors約36.495MB、Apache-2.0 | 分野が一般ImageNet分類で既存Visionと重複しやすいため監視 |

全例のrepo ID・改訂版・公開メタデータを確認したが、Pirate Faceがこれら全リポジトリの**全ファイルを提供し、現在peerが完走可能な状態か**までは確認していない。

## 3. 今回の新しい小型候補2件（いずれもR2調査、取得未承認）

| 原本 | 独自の能力 | 選択内容 | 保存バイト数（十進） |
| --- | --- | --- | ---: |
| [tue-mps EoMT Small](https://huggingface.co/tue-mps/coco_panoptic_eomt_small_640_2x) | Semantic・Instance・Panoptic領域分割。SAM2のプロンプト領域分割と異なる | Safetensors＋config＋processor＋README＋.gitattributes、5ファイル | **95,939,145 B** |
| [cm93 ResNet18 EuroSAT](https://huggingface.co/cm93/resnet18-eurosat) | Sentinel-2 RGB衛星画像の土地利用分類10種類。地球科学の軽量比較原本 | Safetensors＋config＋README＋.gitattributes、4ファイル | **44,780,208 B** |
| **計** | — | **9ファイル** | **140,719,353 B（約0.140719GB）** |

公式Hugging Faceの完全コミットと、2つの`model.safetensors`の配布元SHA-256を[JSON選定記録](../catalog/reviews/pirateface-2026-11-02-source-and-compact-selection.json)へ格納した。旧`.bin`やTensorBoardログは不要形式として選択案から除いたが、元Safetensorsとの値の同一性は未検証。

両モデルは公開・MITの配布表示で、[EoMT公式コード](https://github.com/tue-mps/eomt)・[EuroSAT分類器コード](https://github.com/chathumal93/EuroSat-RGB-Classifiers)のGitHub LICENSEメタデータもMIT。一方、**元の学習データ全体の権利、性能、推論ランタイムと実機要件は別途確認する**。どちらも現時点で提供終了/政府規制が近いという証拠はない。

## 4. ポートフォリオに統合する際の停止ゲート

Pirate Faceを**候補発見と再取得先監視**に限定する。モデル候補の原本IDと固定rev、選択ファイルと完全SHA、原本利用規約、重要な依存物を先に定義する。必要な法的条件が許すときのみ、実際のTorrent内容が同じファイル全量を提供していることと、その時点の接続性を検証対象にできる。今回、Torrent接続・ダウンロード・seeding・第三者ソフトウェアの導入はしていない。

## H / T / D / C / U

| 項目 | 判定 |
| --- | --- |
| H | 二次索引は配布元停止時の再取得選択肢になり得る。小型専門モデル2件は既存Visionモデルと異なるアウトプットを少容量で提供する |
| T | 一次ソース8件をモデルカードと正確なrevにより照合。EoMT・EuroSATの9対象ファイルの容量、Git blob IDとLFS SHA-256をチェック。Torrent実在シードや利用権は未評価なので別ゲートで逐次停止 |
| D | 一次ソースのメタデータは条件付き候補としてPASS。Torrentの現在の完全取得可能性はUNCERTAIN。配布条件・Torrent使用・取得は未承認 |
| C | Torrentが部分ファイルのみ、Seederが0、ネットワーク上の実体が元revと異なる、LoRAの基盤が入手不可、量子化が元原本を代替できない |
| U | Seeder・peer可用性、ライセンスと個々の依存、実機HDD残量、推論性能は未測定。不確かさの統計分布がないので合成標準不確かさ・包含係数は未算定 |

## ERROR CHECK

このレビューは既存の110資産や前回の次期台帳差分に新たな取得許可を与えない。対象モデルはHugging Face上の正規配布ページを一次情報源として選別し、Pirate Face側の公開ファイル一致・Peer接続性については検証済みと記述しない。
