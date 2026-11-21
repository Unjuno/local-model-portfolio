# R150／v63 — 99件取得報告後の11原本再選定と未承認の先頭4件（2026-11-22）

## 0. 結論と正本

- 正本は `catalog/CURRENT.json` の **v63-20261122：235登録、188有効（SELECT55、CONDITIONAL133）**。R150は研究・取得順の確定であり、235レコードへの追加・入替はまだしない。
- 過去の `catalog/execution/2026-11-19-acquisition-ledger.json` は **99モデル／1,478ファイル／1,879,994,309,866バイトのVERIFIED報告**。現物Windows Dドライブの今回の再ハッシュではない。前回の報告による物理空きも現在の空きではない。
- `queues/proposed-v63-r149-after99-11-research-only.json` に11件の未取得とみなす研究ソースがある。11件とも `repo_id + 40桁revision` を固定しているが、ユーザー現物のSHAと必要な利用権を裏付ける証明はない。
- **小型・独自学習4件を初回の所有者審査対象に確定**し、厳密な54ファイルの未承認キューを作成：[`queues/proposed-v63-r150-first-four-UNAPPROVED.json`](../../queues/proposed-v63-r150-first-four-UNAPPROVED.json)。
- その次に**無検閲VLMのオリジナル＋編集重みのペア**をセットで審査する。単純に「無検閲で強い」とは扱わない。
- 別系列の大規模音声モデル **KittenML/kitten-tts-2（1.7B ternary）** を新たに発見。声質複製能力と独自学習成果には研究価値があるが、Apache-2.0はGitHubコードの条件であり、**モデル本体は別のStellon Labs Community License**。この版では研究HOLDで、未確定の原本を正本に追加しない。
- **今回の重量ダウンロード・コード実行・実HDD変更・承認数はいずれも0**。法的判断や取得実行を自動化しない。

機械可読の全11件判断：[`catalog/decisions/2026-11-22-r150-v63-post99-reselection.json`](../../catalog/decisions/2026-11-22-r150-v63-post99-reselection.json)。

## 1. 新しい審査順位：学習済み原本を単位にする

下表のバイトは **Publisherの固定済み選択ファイル参照サイズ** であり、実HDDに必要な重複除外後の増分容量ではない。

| 新審査順 | 既選定の配布元 | 選択ファイル／バイト | 判定と主な根拠 |
|---:|---|---:|---|
| 1 | [Cactus-Compute/mirage](https://huggingface.co/Cactus-Compute/mirage) | 5件／237,985,863 | **A・維持**：小型画像理解。 `mirage.cact` 約21.61MBと`mirage.safetensors` 約216.37MBは同じ学習成果の別表現であって別学習済みモデルではない。Cactus 4.1.4は別依存 |
| 2 | [mistralai/Timestral-28M](https://huggingface.co/mistralai/Timestral-28M) | 6件／111,307,038 | **A・維持**：27.82M時系列確率予測。既存TTMと独立学習。Modified MITの特定収益条件を審査 |
| 3 | [KittenML/kitten-tts-2-pico](https://huggingface.co/KittenML/kitten-tts-2-pico) | 33件／285,879,877 | **A・維持**：約7.2M/言語のエッジTTS。既選定Kitten 2 Mini 82Mと重複原本ではない。4MB/言語INT4広告を全原本容量と混同しない |
| 4 | [AuroraAI-Research/Aurora2-400M-A20M](https://huggingface.co/AuroraAI-Research/Aurora2-400M-A20M) | 10件／1,599,571,502 | **A・維持**：総399.6M／活性約19.05Mのスクラッチ学習MoEのFP32原本のみ。指示追従品質を主張しない |
| 5 | [saidutta69/LFM3-VL-2B-heretic](https://huggingface.co/saidutta69/LFM3-VL-2B-heretic) | 25件／5,334,098,126 | **B・審査繰上げ**：無検閲方向編集を受けた別のBF16重み。元モデルとはPublisher重量SHAが異なる。1種類のQ4_K_MとFP16 projectorを携帯復元用に残す |
| 6 | [LiquidAI/LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B) | 18件／3,854,651,108 | **B・親の対保存**：編集前のVLMを巻き戻し・比較・依存分析に使う。差分ではない独立の親学習済み原本 |
| 7 | [internlm/Intern-Decision-0.8B](https://huggingface.co/internlm/Intern-Decision-0.8B) | 20件／1,734,731,370 | **C・維持**：Qwen3.5の構造化確率意思決定用の別学習成果。Qwen親権利、実行Python・校正を審査 |
| 8 | [apple/FastFrames-S](https://huggingface.co/apple/FastFrames-S) | 6件／947,927,443 | **D・依存閉包HOLD**：0.948GBの二つの追加訓練原本だけで動画生成器は再現できない |
| 9 | [OpenMOSS-Team/MOSS-VL-Realtime](https://huggingface.co/OpenMOSS-Team/MOSS-VL-Realtime) | 20件／22,687,497,344 | **E・維持**：ストリーミング映像理解11.34B原本。カスタムmodeling/processing・GPU検証が必要 |
| 10 | [nvidia/Cosmos3-Nano-Sim-Transfer](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Transfer) | 44件／31,750,521,262 | **E・維持**：ワールドモデル系15.16Bの別学習成果。VAE 1,409,400,600byteは既選定Cosmos2件とPublisher重量SHAが同じ、所有者媒体の実再利用は未検証 |
| 11 | [ricursiveAI/Ripple-65B-Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | 32件／129,572,889,973 | **F・大型HOLD**：64.78B BF16独立学習原本として価値を維持。実験的NVFP4派生は原本の代替にしない |

A群合計 **4配布元・54ファイル・2,234,744,280byte・Publisher LFS SHA-256参照29件**。固定参照は既存の `r143` と `r146` マニフェストをそのまま照合し、現所有者媒体での追加必要量は未確定。

A〜E（Rippleを除いた10配布元）の既存source参照は **68,544,170,933byte**。これは必要依存を完全加算した量ではない。Ripple HOLDは**別枠129,572,889,973byte**で、自動的に4TB予算を予約しない。

## 2. 差分保存で守るべきポイント

**無検閲ペア**：LFM3-VL-2B原本とheretic別重量は同じ1.918B構造でも、Publisher `model.safetensors` LFS SHA256が一致しない。親と編集版の保存ソース計 **9,188,749,234byte**。ただし10件の共有コード／tokenizer参照は18,072,853byte相当の同一Publisher SHAで、owner HDDで確認した重複削減ではない。hereticの作者自身による拒否率実験は性能向上の独立証明ではない。テキストGGUFのみでは画像入力が復元できず、vision projectorも必要。Transformers custom code とLFM3対応 llama.cpp のバージョン・ABIを固定する。LFM Open Licenseと用途に応じた条件を確認。

**FastFramesの依存**：作者のKV refinerとpixel decoder計約0.948GBに加え、Causal-Forcing++ checkpoint **5,676,220,819byte**、Wan VAE／UMT5 source **11,891,015,130byte** が別途必要。ローカル既存重みのSHA再利用が未確定ならセット約 **18,515,163,392byte** が参照される。Apple `apple-amlr`研究条件、Linux CUDA 12.8、`.pt`／`.pth`の安全な静的監査が未済。依存のない0.95GB単体取得をoffline-readyとするのは禁止。

**Mirage実行依存**：モデル原本の他に Cactus runtime 4.1.4のWindows/Linux計 **4,137,947byte** が別管理。未審査の.exeや.whlを取得後に起動しない。

**Cosmos VAE**：Publisher SHA256一致は正本相当の重み参照再利用候補であり、実際の所有者HDD内のファイル存在、パス、同一SHAの証明ではない。フォーマット変換で再現できる派生を新規訓練原本として数えない。

**RFD4 Proteina**：前回R148で観測した別revisionの重量差分が残っている。既取得revisionとcatalog旧revisionを勝手に同一視・差替えしない。owner媒体上の依存閉包も未確定。

## 3. 新規発見：Kitten 1.7Bをなぜ即時確定しないか

一次資料：[モデルリポジトリ](https://huggingface.co/KittenML/kitten-tts-2)、[モデルLICENSE本文](https://huggingface.co/KittenML/kitten-tts-2/blob/main/LICENSE.md)、[公式実装README](https://github.com/KittenML/KittenTTS)。

Publisherは **1.7B ternary、約492MBのコンパクト実行形、音声クローン／表現付きTTS** を提示。しかしHubの`main`全リポジトリ表示は **約8.24GB** で、492MBを全学習済み音声生成・codec・話者/音声素材の完全保存量とはしない。現時点で固定コミットごとの要保存ファイルとLFS SHA256/完全復元依存は閉包していない。

GitHub実装のApache 2.0を**モデル重みの利用許諾と取り違えてはいけない**。重みのStellon Labs Community Licenseは研究・非商用利用を規定し、権利はrevocable。商用は登録が必要で、年間売上・累計資金調達100万米ドル超に別許諾条件を課す。AUP、帰属、蒸留・別基盤モデルへの能力転移制限、違反時の停止・削除条項を含む。ユーザー個別の利用行為・収益・音声利用同意は本研究では判定不能。よって **新登録なし／研究HOLD／取得承認なし**。合法な研究保存を一律に禁止する趣旨ではない。

## 4. 配布規制について、事実と仮説を分離

**事実**：米国BISの2026-11-19施行 [91 FR 74970-74999、Section IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm) は旧AI Diffusion Ruleの重量ECCN 4E091を撤廃した。これは仕向地・最終用途による輸出管理、個別PublisherのLICENSE、Gated条件や個人情報処理を撤廃する規則ではない。

**仮説**：無検閲、安全制御変更、小型高能力・音声クローン・映像・ロボット等の公開経路に将来の変更が起き得るので、今存在する**独立学習成果を正規の範囲で先に保存する**。個別モデルの削除予定日・Gated化確率は確認されておらず、数値を創作しない。

## 5. 実行ゲート／H・T・D・C・U

- **H（反証可能仮説）**：異なる学習済み重みと復元必須なcodec／親／ABIを優先し、同一重みの多種量子化は増やさなければ、原本保存可能性とモデル系列の分散が改善する。
- **T（最小検証）**：11件の固定repo＋revision＋file SHA＋bytesを静的突合。先頭4件54ファイルを比較し、実機で対象Dの既存99モデル分の原本と差分だけを読み取りでSHA-256照合。個別LICENSE・依存・完全offline restore・GPU/CPU/ランタイム検証はそれぞれ別ゲート。性能を比較する時はHW、クロック、OS/driver、backend commit、context、batch、量子化と同一入力を記録し、少なくとも30回の反復を行う。ここでは反復測定未実施。
- **D（合否）**：先頭4件が54ファイル／2,234,744,280byte、10非HOLDが68,544,170,933byte、既存99報告とのrepo一致、重み差分と親依存明示、`queues/approved.json`空なら **静的PASS**。ファイル不一致や承認偽造なら **FAIL**。実媒体のSHA・権利・full restore・推論品質は現物未測定のため **UNCERTAIN**、取得と新原本の最終lockは停止。
- **C（反例・破れ方）**：作者の性能再現に失敗する／意図した利用行為が契約上認められない／親が未保存で実行不能／共有ファイルが媒体に見つからない／GPUに実装が載らない。そのとき該当原本をHOLDに戻し、重みを削除せず審査順を修正する。
- **U（不確かさ）**：出版社メタデータと作者ベンチ、ローカルパス・hash・ドライブ空き・GPU等未測定、ライセンス適用とABIが支配的な誤差源。独立反復測定と誤差分散がないため合成標準不確かさ `u_c`、包含係数 `k` は算定不能。

**連携分野**：機械学習の重み編集と推論、音声・時系列のエッジ処理、視覚・ロボット基盤モデル、ソフトウェア供給網・著作権／個人情報法。

## 6. 誰が何を進められるか

研究者側で確定できたもの：既存99報告との差分11件、先頭4件の原本ファイル・固定revision・Publisherハッシュ参照、ヘリティック＋親の重みが異なる証拠、11件の順序、FastFramesの復元依存、Kitten 1.7Bの権利上の停止条件。

所有者側でしか閉じられないもの：Windows Dの実ファイルSHA-256と空き容量（最低200GB安全余白・staging込み）、用途別LICENSE確認、本人の個別source承認。これらを暗黙承認にはしない。

**今回の操作**：GitHub `main` に審査キュー・決定・調査文書を追加。新重量取得0、モデル実行0、`queues/approved.json`の変更0、所有者媒体変更0。既存の235正式資産の判定は維持。
