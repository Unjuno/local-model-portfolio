# R167／v72 — 17Mロボット点追跡の独立原本をP0候補に確定、1B WarpはHOLD（2026-11-25）

## 1.〈本論〉採否と現行の正本

**本研究で正式登録は変更しない。現行v72は264登録／210有効（SELECT56、CONDITIONAL154、HOLD35）を保持。** 116モデルVERIFIED取得台帳報告の再ダウンロード、取得承認の追加、Owner Windows DのSHA・容量再測定、未審査コード実行、実ロボット操作はすべて0。将来の配布規制は未確定のシナリオとして扱い、独立学習状態・用途・容量・権利・依存を根拠に選定する。

2026-11-23にAi2が公開した[原作者RoboTrack記事](https://allenai.org/blog/robotrack)は、点追跡モデルを実ロボット操作動画向けに追加学習したと報告。今回の2原本は既存264資産と取得116台帳にID重複なし。

| Publisher原本と固定SHA | 原本サイズと重量SHA | 今回の選定 |
|---|---|---|
| [allenai/RoboTracker](https://huggingface.co/allenai/RoboTracker/tree/3bda363815dca4395b855ba0e7737517300f937f) 3bda363815dca4395b855ba0e7737517300f937f | **3ファイル／66,011,293 byte**。学習済みrobotracker.pth 66,004,399 byte／LFS SHA256 d846b841b698a772bff681b7c1d5446f11ff5e9c4e0371bfa171190b1c7805b8 | **P0・次期CONDITIONAL正式選定を推薦**。AllTracker約17Mを実操作追跡向けに追加学習した独立チェックポイント。コード復元や本人権利なしで重量DL許可にはしない |
| [allenai/RoboTracker-Warp](https://huggingface.co/allenai/RoboTracker-Warp/tree/6cf4ddd90571b5e5bb269cf6cfb6112b91e66ec8) 6cf4ddd90571b5e5bb269cf6cfb6112b91e66ec8 | **3ファイル／3,898,587,949 byte**。robotracker_warp.pth 3,898,580,646 byte／LFS SHA256 6a45fc269a227dbb87f9aab8cc8efc43eba77113ac891f6156db9834b1b3830c | **P2・HOLD**。約1BのCoWTracker/VGGT系を別fine-tuneした原本。CC BY-NC4.0と専用非商用コード、GPU・ABI・利用権が未充足 |

原本証拠：[2モデル全6ファイルのPublisher Git OID・LFS SHA、原作者コード56 blob、Leanコード19 blob、評価datasetの権利タグ](../../manifests/drafts/r167-2026-11-25-robotracker17m-vs-warp-nc-publisher-source-frozen.candidate.json)／[機械可読採否と反証可能な停止条件](../../catalog/decisions/2026-11-25-r167-v72-robotracker-small-vs-warp-source-adjudication.json)／[ダウンロード未承認の研究キュー](../../queues/proposed-v72-r167-robotrack-two-independent-specialists-UNAPPROVED.json)。

### 元AllTrackerとの差と品質の負の証拠

[元AllTrackerモデル](https://huggingface.co/aharley/alltracker/tree/c8ba31225828cab9ec512d0627f0f826e641a877)の全学習済み重みのPublisher SHA256は ffd9ebcfb6d206d594b646999a150540f92c049cf9b2bf940facf7123f62aa1d で、RoboTrackerの重量SHAと異なる。作者はRoboTrack-15M合成データとKubricを50%ずつ混ぜて10,000ステップfine-tuneしたと記載。したがって単なるGGUF量子化ではなく、別学習済み状態として記録する。フル学習済みcheckpointなので元AllTrackerを別に再取得しない。

RoboTrackerと元AllTrackerの著者同条件比較は、TAP-Vid first、384×512画像、4回refinement、visibility×confidence 0.6しきい値、FP32/TF32。RoboTrack-BenchのAverage Jaccard（AJ）は**62.56→63.40、+0.84ポイント**だが、RoboTAPのAJは**68.48→68.41、−0.07ポイント**で悪化。全面的性能向上という評価は不適切。WarpのRoboTrack-Bench AJはCoWTracker **63.87→65.98、+2.11ポイント**だが入力336×560であり、RoboTrackerの384×512との直接性能比較にはしない。著者のWarp H200約18 frames/s・GPUメモリ約47GBは利用者実機の測定値ではなく、クロック・バッチなどは未検証。独立測定と信頼区間がないので有意差を断定できない。

作者はピペットロボット実験20配置で点追跡17成功、マスク8、光学流5と報告するが小標本の特定装置結果。危険な実ロボットの自律実行許可ではない。遮蔽からの再追跡や小物体の難しさも残る。

## 2.〈応用・転用例〉モデル重みのほかに必要な復元ソース

両方のモデルHub repoにはLICENSE実ファイルがなく、ライセンスタグはそれぞれApache2とCC BY-NC4.0。**配布ページのタグは所有者の用途別利用権審査の代替ではない**。

[原作者の公開ソース](https://github.com/allenai/robotrack/tree/fc5cd87f60fad57c7cbc48c3d09e9aa7b45061a3)をcommit fc5cd87f60fad57c7cbc48c3d09e9aa7b45061a3、Git tree 4d44877a3a9c127ce0089a1d2acd0022d8184bedで固定。全56 Git blob／1,907,536 byteの個別サイズ・OIDを記録した。RoboTracker用の最小コード19 blob／164,989 byteは、AllTracker net/blocks/basic等、eval_alltracker、hub、evaluate、metrics、LICENSEとpyprojectを含む。元repo全体には別にCowtrackerのFAIR Noncommercial Research License部分があるため、コード全体を一般商用Apacheライセンスと誤認しない。小型用のlean runtimeにcowtracker部分を含めていないが、元repo全体をそのままpip installする行為や配布行為の権利は別途審査する。

**実装前提**：作者pyprojectはPython3.10以上、Torch2.1以上、torchvision、einops、numpy、opencv-python、huggingface_hubを要求。小型を読み込む原作者ソースには torch.load(weights_only=True) が存在することを静的に確認したが、.pthの未審査デシリアライズ、CUDAドライバやtorchvision ABIが安全かどうかを実行で確認していない。標準チェックポイント名はモデルHubのmainを自動参照しうる。完全オフライン復元は**固定済みローカルの.pthファイルパス**を用いて、外部通信禁止下で別途検証する。

Warpは別にFAIR Noncommercial Research LicenseのCoWTrackerとVGGT等、依存パッケージの固定Torch2.10.0、torchvision0.25.0、xformers0.0.34を前提とする。非商用利用条件を個別確認し、所有者GPU/ピークVRAM、外部ソースのGIT/submodule、元モデルの許諾が閉包するまでHOLD。

データは別資産：[RoboTrack-Bench](https://huggingface.co/datasets/allenai/RoboTrack-Bench)は307動画・2,522手動追跡点、複数の実動画元を含みLICENSEはotherで約921 MBの出版社ストレージ参照。[RoboTrack-15M](https://huggingface.co/datasets/allenai/RoboTrack-15M)は3000合成動画・15M点、ODC-BYで約18.78 GBの出版社参照。両datasetは独立した権利・プライバシー審査なしに原本モデルと共に自動取得しない。

## 3. 容量計算・変数表・次元確認

\[
B_{\mathrm{minimal}}=B_{\mathrm{weightsrepo}}+B_{\mathrm{code}}
=66{,}011{,}293+164{,}989
=66{,}176{,}282\ \mathrm{B}.
\]

| 変数 | 意味（日本語） | 単位（SI／情報単位） | 定義 | 定義域／前提 | 型 |
|---|---|---|---|---|---|
| \(B_{\mathrm{weightsrepo}}\) | 小型RoboTracker全3Publisherファイルの容量 | B（byte） | 66,011,293 | 非負整数。Owner保存媒体の純増量ではない | 整数スカラー |
| \(B_{\mathrm{code}}\) | 小型用の優先19 Git blobのPublisher参照量 | B | 164,989 | 非負整数。Torch等のwheelhouse除外 | 整数スカラー |
| \(B_{\mathrm{minimal}}\) | 小型モデルとLeanコードのPublisher参照容量 | B | 2項の和 | 外部依存・GPU・動画datasetとcache/stagingを除外 | 整数スカラー |

単位検査：byte＋byte＝byteで左辺と右辺が一致。保存容量66.18 MBから実GPUピークや4TB／最低200GB残床の適合可否を推定してはならない。

## 4. H / T / D / C / U

**H**：17Mパラメータのロボット点追跡は、既存VLM/ロボットpolicyと別機能の独立fine-tuneを66MBで保全できる。大きなWarpも別fine-tuneだが、非商用制約、依存・GPU負担から小型を先行させる。

**T**：Hub2repo全6ファイルの固定SHA／OID／サイズ、AllTracker元重みとの相違、GitHubコード全56 blobと選定19 blob、評価データrepoのライセンス・コミットを静的照合。次に所有者の個別権利と媒体SHA・200GB残床＋staging、Python/torch/driver ABI、weights_only安全ロード、完全offline復元を検証。品質は同一基準の最低100動画、同一HW/clock/batch/resolution/context、最低30反復のAJとlatencyを事前登録する。最小n未達で逐次停止しない。

**D**：Publisher原本SHA／コードGit OID、116取得台帳IDの非重複、空approvedキューはSTATIC PASS。所有者の用途別LICENSE、物理SHA、CUDA/torch ABI、完全offline restore、個別file-scope明示許可がない状態ではDOWNLOAD STOP。PTH危険ロード、NC権利違反、偽承認、無断ロボット制御はFAIL。

**C**：作者報告の小型＋0.84 AJ改善が統計的に有意でない、RoboTAP−0.07悪化、既存videoモデルで実用的に代替可能、PTHと周辺コードのABI不一致、データ権利未閉包。Warpが実機ではより効率的な可能性も未反証。

**U**：自己申告17MはTensor Census未実施、独立bench不明、実HW・GPU clock・バッチ・動画分布・保存媒体実空き・ライセンス未測定。合成標準不確かさ \(u_c\) と包含係数 \(k\) は反復測定前で数値化しない。

関連分野はロボット知覚、動画追跡・コンピュータビジョン、統計実験計画、安全なモデルシリアライズと供給網、GPU実装、動画データの知財／プライバシー。

### ERROR CHECK

正式v72の264資産／210有効、116件取得報告、全210取得STOPとapprovedキュー空は改変しない。RoboTracker/ Warpは現在の正本・台帳にIDが存在せず、二重登録を防止した。未承認の研究queueにPublisher原本6ファイルとコード・評価出典を固定し、実重量・実Datasetのダウンロードや未審査コード実行は行わない。

## 5.〈次に考える問い〉

すでにロボット制御や動画理解のモデルがあっても、「視覚点追跡」という別機能を小型原本で保全する意義はあるか。モデルの汎用ベンチではなく、遮蔽・追従・再認識の独立タスクで比較すべきである。
