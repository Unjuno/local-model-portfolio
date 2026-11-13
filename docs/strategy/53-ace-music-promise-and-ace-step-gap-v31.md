# R53・v31｜ACE Musicの公開予告とACE-Step楽曲生成能力の欠落補完（2026-11-13）

指定ブランチ `strategy/2026-11-03-01-risk`、基準コミット `19f68aaeb5a04acd3d2d1c71325c97bfc9c8bdc4`、[元投稿](https://x.com/acemusicai/status/2120945723005166053)。X元投稿本文は直接取得できなかったため、出版社の[公式ACE Music v1製品ページ](https://acemusic.ai/acemusic-v1/)、[AI Audio評価](https://x.com/ArtificialAnlys/status/2120337324898992298)、[公式ACE-Step 1.5 GitHub](https://github.com/ace-step/ACE-Step-1.5)、[一次論文 arXiv:2602.00744](https://arxiv.org/abs/2602.00744)で照合。

## 1.〈本論〉同一企業に関わるが重みが異なる3系統

| 対象 | 公開状況 | 現段階のアーカイブ判断 |
| --- | --- | --- |
| **ACE Music v1** | [公式サイト](https://acemusic.ai/acemusic-v1/)上の楽曲生成サービス。公開ウェイトrepo、SHA、配布ライセンスは未確認 | **非採用研究HOLD**。無料楽曲生成・商用有料出力権は重み再配布の許諾ではない |
| **ACE Music v1 Flash** | 同サイトに**2026年末のオープンソース化計画**が明記。ただしモデル総数、重み、LICENSE、日付未公表 | **公開待ち監視（NOT YET ARCHIVABLE）**。v1旗艦重み自体が公開されるとの推測は禁止 |
| **ACE-Step 1.5 / XL** | 別のACE Studio＋StepFun共著系列でコード・原重みがすでにHF一般公開、公式MITタグ | **独立した楽曲生成モデル**として現行との差分を評価 |

2026-11-12のSNS投稿を説明する二次報道には「数週間以内にv1の重み」と記載があるが、出版社の公式製品ページでは**v1 Flash**と明記。モデル名の違いは大きい。**main v1、Flash、ACE-Step、1.1 Previewの重み同一性は一切確認できていない**ため、異なるrepoを仮に同一物として登録しない。ACE Music 1.1 PreviewのABC記譜から音声生成も現在サービス提供のみ。

[Artificial Analysis発表](https://x.com/ArtificialAnlys/status/2120337324898992298)では音楽・歌声のblind-vote AA-Music-Vocal v1.1でACE Music v1の1160 Elo対Suno v6 1144 Elo（差16）。二次掲載の区間はACE[1139,1181]対Suno[1126,1162]と重なっている。これは**歌声カテゴリの観測上の先行**であり、全音楽ジャンルへの品質優越や統計的確定を意味しない。ACE Music v1の主ウェイトが公開済みである根拠にもならない。Suno/ACE Step双方の価格/商用出力権と学習済み重みの権利は異なる。

## 2. なぜXL Turboを条件付き研究選定するのか

現行v30の178件で[**MERT v2 FullSong**](https://huggingface.co/m-a-p/MERT-v2-FullSong)は音楽表現抽出モデルだが、完成楽曲と歌声の生成器を保全していない。GPTやTTS、動画生成から簡単に戻せる学習状態でもない。原音楽生成能力の明白な空白を補うため、[ACE-Step/acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo)を**R1/S2のCONDITIONAL1件**として選定。原版のACE-Step 1.5（2026年2月）、XL系追加2026年4月2日、XL Turboは**別蒸留・8ステップ・CFGなし**の学習済みモデル。出版社の比較では2Bより音質が良いとされるが**独立の同一条件テスト未実施**。

**重要なパラメータ表示差**：作者は「4B XL」と呼ぶが、HF safetensorsは**約4,987.3M学習済み要素・F32で約20GB**を表示。公式カードの「BF16約18.8GB」という説明と実際の公開スナップショットを混同しない。計画保存量は**原XL F32 4 shard＋別の楽曲構成LMとVAE等**。所要本体と外部依存の重複排除後の正確なバイト数はまだnull。出版社はVRAM12GB（INT8＋オフロード）、16GB（オフロード）、20GB（オフロードなし）、24GB（4B LM追加品質）を公表するが、ユーザー実機・backend/cuda/clock/batch条件での実測ではない。

HFモデルの現在公開画面に示された40字ソースrevision：
- XL Turbo重み原本: `d4a0b288b83ebb7e25a8c0b32c573c22e134e8ee`
- ACE-Step 1.5共有LM/VAE/embedding配布元: `19671f406d603126926c1b7e2adc169acbcade22`
- [公式コード固定](https://github.com/ace-step/ACE-Step-1.5/tree/ca1e85fe9430179831e6bc6be790c332190a3866): `ca1e85fe9430179831e6bc6be790c332190a3866`

後者の共通repoは約10.1GBだが、2B Turbo重みも含む。**丸ごと採らず**、1.7B計画LM、Qwen3 Embedding 0.6B、音声VAE、metadata/tokenizer/configの必要分を依存として固定する。4B XL Turbo独立重み（F32約20GB）、1.7B計画LM、Embedding、VAEの各SHAとLICENSEは将来の最終manifestで明示。XL repoの`silence_latent.pt`はpickleの可能性があるため保全中に`torch.load`しない。HFの`trust_remote_code=True`提示は、コード安全審査済みを意味しない。

**別の価値を持つXL Baseは保留**：[XL Base](https://huggingface.co/ACE-Step/acestep-v15-xl-base)は50 step/CFG付きのpretrained重みで、Turboでは対象外のextract/lego/completeも提供する。従って単なる量子化を除外する論理は適用できないが、約20GB追加の保存価値を同条件の用途比較前に勝手に認定しない。XL SFT、2B Turbo、3サイズのLM、普通のGGUF/INT8/MLX派生も自動追加しない。[MERT]や既存TTSとの「歌声/楽曲生成」と「音楽分析・読上げ」のタスク違いを重視する。

**ライセンス**：[出版社モデルカード](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo)はMIT、[固定ランタイムLICENSE](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/LICENSE)はMITの全文確認済み。ただし独立音楽原盤・人物の声などのデータの適法性は出版社による「 licensed/public-domain/synthetic 」の自己説明であり、第三者監査ではない。原モデルの音楽成果物の商用ライセンスと、ACE Music hostedの有料プランの権利を混同しない。

## 3. 容量・変数表・H/T/D/C/U

| 記号 | 意味（日本語） | 単位（SI） | 定義・型/定義域・前提 |
| --- | --- | --- | --- |
| `C` | 4TB保存計画上限 | byte | 4,000,000,000,000、非負整数、所有者実HDD未確認 |
| `F` | 最低物理空き | byte | 200,000,000,000、非負整数、ユーザーPC未測定 |
| `B_{XL}` | 公開XL Turbo原本repo規模 | byte | 約20,000,000,000、近似非負、**正確なselected bytesではない** |
| `B_{shared}` | ACE-Step 1.5共有元repo規模 | byte | 約10,100,000,000、近似非負、2B DiT重複含む |
| `R_{budget}` | 研究予約上限 | byte | 40,000,000,000、非負整数、環境全依存を含む実測ではない |
| `P_{XL}` | XL Turbo原本の公表学習済み要素 | 1 | 約4,987,300,000、非負整数、HFの四捨五入表示 |
| `P_{full}` | 依存を含む完全学習済み要素 | 1 | null、推論構成別に未計数、独立符号化器等を含む |
| `M_{peak}` | 推論実機RAM+VRAMピーク | byte | null、実機/OS/backend/context/batch未測定 |

**次元検査**：B/R/C/Fはbyteだが、全repo展示量・選択実体・物理残量は別物。Pは無次元でありbytesをそのまま足さない。4TBの過去126件既知SHA配布元3,417,685,712,585byteにこれまでの後続依存・cache・stagingが含まれないため、新40GB予約で最終安全空きが保証されたとは言わない。150B等の上限超例外を根拠なく軽くしない。

**H**：音楽解析のみのv30に対し、独立楽曲生成DiT＋composer LMは新能力。公開予定Flashも現在は未取得不能。
**T**：ACE-Step XL/HF shared/公式Gitの固定40字revision、原テンソルSHA/bytes・license全文・最小復元コードのABIで静的審査し、本人が取得/実行を個別許可した後に日本語/英語・8ステップ固定、最低30曲・同HW/context/batch、歌詞/音源一致、音声品質を比較。
**D**：研究上の独立学習資産としてCONDITIONALはPASS、実際の取得準備・ユーザー権限・完全復元はUNCERTAIN。原本解放されていないACE Music v1/Flashの実ウェイトを取得できるとみなすのはFAIL。
**C**：Flashが公開後実は同系譜で、XLの重複代替となる；XLのpublisher音質上振れが独立評価で再現しない；VAEまたはモデルカードのMITで配布権利未解決。
**U**：根HFメタデータと正確な重みSHA、分割subsetのbyte、推論実機メモリと出力評価、不確かさの共分散未観測。u_c/kは算定不可。

**ERROR CHECK**：旧178資産を不変保持し、正式追加XL Turboのみ1モデル、管理179件/有効132件（モデル153/データ26、SELECT53/CONDITIONAL79/HOLD28/延期13/EXCLUDED6）。総数不明20（有効7）、150B超例外HOLD2、ダウンロード承認0。Python全CI・実モデル動作・実payload SHA・実HDD未検証。音響・音楽情報検索、生成モデル、知財法務・デジタル保存、ソフト供給網の4分野で評価。

## 4.〈次に考える問い〉

リリース予告だけのACE Music Flashを「今日バックアップできる」と誤認することなく、すでにオープンなACE-Step XLの**独自DiT＋音楽計画LM＋VAEという学習済み依存**を確定するほうが先ではないか。
