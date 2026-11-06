# 33 — Cosmos Sim-Auto・Phonon端末内音声の独自学習成果とERNIE配布条件（2026-11-06、v26）

## 1. 対象・判断

公開ウェイトの学習成果が将来入手できなくなっても独自の訓練済み能力を保全する。何を残すかは学習成果の非重複性、取得の順序は実際のGated/契約制限と仮説的な先行制限で決める。v25・169資産／有効122件の一次ファイル範囲は122/122で既知、論理SHA dedup **3,372,065,984,104 byte**。31資産の外部依存・実機空き・計測RAMは未確定。

今回、**独立重み3件をconditionalとして採用**。v26は172資産／125有効になる。Gated多言語Phononは**研究専用かつ個人承認まで取得キュー不可**。Baidu ERNIE 5.5 Flash Baseは**総150B超・契約地域制限・RAM同等性未実測のため研究HOLD**。音声話者潜在とVibeVoiceのTokenizerは独立新モデルとして数えず、既存再現依存に加える。

2026-11-05公開のGradium記事は10月20日発売済みPhononの詳説であり、モデル自体が11月5日に初公開されたわけではない。Cosmos3 Sim-Autoもモデルカードは初回2026-10-20、HFの解説が11月5日。ERNIEの公開は11月5日。日付の違いを混同しない。

## 2. 新しい条件付き選定3件

| 候補・固定revision | 独自性／既存との差分 | 配布元全repo公称バイト | 計画上限 | 主な負の証拠 |
|---|---|---:|---:|---|
| [nvidia/Cosmos3-Nano-Sim-Auto](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto) `e289a50a4049614eaa62c9edc10b1e8d6cc1a6c1` | Transfer-Autoからの自動運転WSM+11カメラ+LiDARを同期する4-step因果蒸留世界モデル。既存Sim-Bimanualと**変換器6shard全て異なるSHA256**、VAEは同一SHAで共有 | 32,364,133,043 | 35GB | LiDAR制御映像・参照リグ、FA4/CUDA版、品質・実行RAM未測定。OpenMDW1.1本文/ソフトライセンス別審査 |
| [gradium/phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en) `92741c5b07d085ff840e26fea8ce43110b87852f` | 30.8M本体＋約10.3M decoderの独立flow-latent TTSで英語端末内発話。高B級音声モデルと別学習成果 | 223,333,254 | 0.3GB | q8/q4は同じ重みの量子化形式、別採用しない。話者encoder非公開、新規任意声の作成は再現不能 |
| [gradium/phonon-40m-multilingual](https://huggingface.co/gradium/phonon-40m-multilingual) `1537ce46c64f42903e0d608b132ccb073dac46d2` | 英仏独西葡の5言語独立学習版、英語31Mとは重みも言語能力も異なる | 257,581,010 | 0.3GB | **Gated auto**＋CC BY-NC4.0。本人許諾未確認で元重みSHA256も匿名APIでは伏字。**研究専用で取得禁止** |

総数は販売名の31M/40MではなくHF Safetensors集計の**41,096,035／50,539,363要素**を全モデルのスクリーンに使う。製作者の本体数とdecoder込みの値が違うが、数億未満で150B境界には影響しない。作者による品質/遅延は各自社発表であり、HW/clock/context/batchを揃えたユーザー実機比較を行っていない。

## 3. 同一学習成果の重複排除と欠落しやすい依存

Phononの各原本について`model.safetensors`と`default-voice.safetensors`、config/processor/tokenizerを保存範囲に指定し、`model.q4k.gguf`と`model.q8.gguf`を別原本として重複登録しない。固定配布元の選定一次ファイルは31M版**103,745,734 B**、40M多言語版**122,629,650 B**。

**共有の話者潜在：** `gradium/phonon-voices@0ee17205f254b5abc43b266c8a0f215565c352f7`には102件の`voices/*.safetensors`で**26,125,872 B**の学習済み話者潜在がある。カタログ`voices.jsonl`/README/.gitattributesを含む**26,183,423 B**を追加共有依存に計上し、デモ音声ファイルの約43MBをデフォルトの実行依存とはみなさない。repoのApache 2.0タグが個別声の同意を保証するとは推定しない。**話者の未公開speaker codec**がないため、新規録音からの任意声生成はできず、失われる前にこの事前潜在を保全する価値がある。

**VibeVoice用のモデル原本ではないTokenizer依存：** Hugging Faceの公式Transformers-native変換提案が指定する`Qwen/Qwen2.5-1.5B@8faed761d45a263340a0528343f099c05c9a4323`の`tokenizer.json`、merges、vocab、config、ライセンス等**9ファイル計11,505,079 B**を新規共有依存として記録。Qwen本体`model.safetensors`約3.087GBはこの依存のために再取得しない。実行コード版は`huggingface/transformers@640a08a597034221ca1c4fc0c129cf0118179225`がコミュニティ議論で提案された**候補版**であり、Microsoft公式に採択されたことは未確認。

**Cosmos同一VAE：** Sim-Autoと既選定Sim-Bimanualの`vae/diffusion_pytorch_model.safetensors`は**1,409,400,600 B**で同一の配布元SHA256 `230496cb59ff85bc9c040487737c4062480cb61c71e697b197b4c30142f2a0da`。システム上の論理重複を減らせるが所有者HDDの物理重複排除が存在するとは断定しない。

## 4. 150B以上の先行制限候補：Baidu ERNIE 5.5 Flash Base

[公式Baiduモデル](https://huggingface.co/baidu/ERNIE-5.5-Flash-Base)は事前学習だけで33.5T tokenを消費した**280B名義／HFメタデータ286,245,697,882要素**の独自MoE baseで、学習後のRLHF/Instructとは別の研究価値がある。固定revision`028544b2ffceea189b2d8768ed2b9d09b06f2343`、全repo**288,464,891,869 B**。モデルカードの14B activeは総パラメータではなく、元FP8容量がそのまま実行RAM以下を保証するわけではない。

[正式LICENSE](https://huggingface.co/baidu/ERNIE-5.5-Flash-Base/blob/main/LICENSE)は日本などを原則対象地域に含み、EU・英国・韓国を明示的に除外する独自契約。本人の法的主体・取得地・使用地・配布対象・売上条件・更新版の権利を確認する必要がある。**現実の提供元契約制限**であって行政の削除命令ではない。

このモデルの重要度は高い。しかし、量子化後の**150B未満比較モデルと同HW/backend/context/batchでのピークRAM同等以下**、512GB未満、品質維持、合法性の確認がないためv26で**active選定に昇格しない**。同一能力を持つより低ビットの正規派生と計測根拠が得られたら再審査する。今後の登録数と約4TBとの差額を、この288GBの元全repoを追加して算出してはいけない。

## 5. 4TB・残容量・不確かさ

| 記号 | 意味（日本語） | SI単位 | 定義 | 範囲・前提条件 | 型 |
|---|---|---|---|---|---|
| `B_prev` | v25一次ファイルSHAに基づく既知の論理容量 | B（byte） | 3,372,065,984,104 | 配布元API metadataによる計算 | 非負整数スカラー |
| `B_new_repo` | 追加3件の全repo容量 | B（byte） | 32,845,047,307 | 実際に選ぶファイル容量とは別 | 非負整数スカラー |
| `B_budget` | 保存枠 | B（byte） | 4,000,000,000,000 | 十進4TB | 非負整数スカラー |
| `B_floor` | HDDの最低空き余白 | B（byte） | 200,000,000,000 | 実機未接続 | 非負整数スカラー |

**次元チェック：** 全バイト数同士の足算は単位上妥当だが、全repo・選定ファイル・実行RAM・ディスク実使用量を同じものとして扱わない。v26選定ファイル、公開ハッシュが一致するVAE、重複しない音声依存とQwen tokenizerは`scripts/capacity_selection_v26.py`で別々に検査し、再計算後の`capacity-summary.json`を採用する。

## 6. H/T/D/C/U／ERROR CHECK

- **H:** Cosmos Sim-AutoとBimanualは訓練成果が異なり、Phonon 31M/40Mは各原本と既存大型TTSでは代替できない小型学習成果を持つ。Gatedかつ未公開speaker codecの制約で潜在声の取得機会には実際の限界がある。
- **T:** 既存169資産を完全保持し、3repoの固定source SHA・完全weights・codec・voice metadata・共有依存・LICENSE/HW条件を検査。CIで125/125一次ファイル、重複排除、承認0を検証。実機の計算はユーザー承認後のみHW/clock/backend/context/batchを記録。
- **D:** 選定PASS=独立重み／公式配布元SHA／個別理由。完全取得PASS=権利・実空き・依存・合法性・最終SHA・明示承認。多言語Gatedは**research-onlyかつapproved lock不可**。ERNIEは150B超RAM条件未実証でHOLD。
- **C:** 未公開speaker codecの喪失、声に関する権利、CosmosのLiDAR control例・FA4環境の欠落、HCA/MoE計測偏り。性能が元モデルに及ばない場合も保険価値と日常実用を分ける。
- **U:** 配布元のファイルバイトは正整数で固定、現物SHA・OS/backend外部部品・HDD空き・ローカル重複・stagingは未計測。確率分布不足により合成標準不確かさ`u_c`と係数`k`は推定不可。

**ERROR CHECK:** 169→172資産、122→125有効。追加は3件だけ、取得許可0。Phonon音声潜在とQwen tokenizerは共有依存のみ、BaIDU大規模原本は研究HOLD。4TB・200GB・150B超量子化の同等RAM条件は変更しない。推論本体のダウンロード・クラウド計算・実機操作・mainブランチ更新を行わない。デジタルアーカイブ、機械学習、ソフトウェア供給網、ライセンス・ガバナンスの少なくとも4分野にまたがる。
