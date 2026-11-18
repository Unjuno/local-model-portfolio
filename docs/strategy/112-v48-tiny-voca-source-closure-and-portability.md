# R112｜v48：tiny-voca独立FP32原本の正式CONDITIONAL選定と取得前ゲート（2026-11-18）

## 1.〈本論〉採用・交換・除外の結果

対象GitHub [`Unjuno/local-model-portfolio`](https://github.com/Unjuno/local-model-portfolio)。v47の200登録/153有効を保ったまま、[n4ze3m/tiny-voca](https://huggingface.co/n4ze3m/tiny-voca)を**R2・CONDITIONALの独立学習済みTTSモデル原本として1件追加**する。v48は**201登録/154有効、SELECT53・CONDITIONAL101**。既存のPhonon-31M英語・Phonon-40M多言語・Kitten TTS Mini・Qwen TTSを取り消したり置換しない。

**追加理由**：原本は音声波形生成を含む4,537,291学習済みパラメータ、2英語固定音声・24kHz。元モデルを量子化した派生物ではなく、独立に合成音声17.6時間で訓練したsource-filter型テキスト音声生成器。既存のPhonon/Mimiに依存する潜在復号、Kitten多言語音声とは学習系統・出力形式が異なり、最小CPU TTSのアーキテクチャ比較・再現研究の**小容量対照原本**になる。

**否定的側面**：英語のみ、固定音声2種、音声クローニング・ストリーミングなし、外国人名等の発音が弱い。著者の内部WER検証は検証8クリップ・試験8クリップ、形式的聴取試験なし。外部Open TTS leaderboard 2026-11-16版の著者紹介値はtiny M2の平均WER0.733%／Phonon英語0.730%と近いが、同条件のユーザー実機で独立再試験していない。著者の『CPU四スレッドで実時間の約70倍』はCPU型式・クロック/メモリ・バッチ数の情報が不十分で一般性能保証ではない。著者の再学習コストはRTX4090で最終訓練7.7時間／プロジェクトGPU代9.56米ドルとの申告であり、すべての再構築成本を含む証明ではない。**高い消失リスクを断定せず、低コストの独自構造として採用する。**

**形式の取捨選択**：正式保全候補は*同一資産内のFP32 PyTorch原本1つ*と実行に必要なphonemizer辞書・権利・config。GGUF FP16/orig/Q4/Q8、デモ音声・費用画像、変換済ONNX FP32（21,386,372 bytes）は初回sourceには含めない。ONNXは既存学習結果の変換形式であり、CPU利用上の利点を実証した場合だけ同一資産のオプションとして再審査。モデル・データセット本体の取得は本作業で行わない。

## 2. 完全固定した一次ソース選択

| 項目 | 値 | 出典・意味 |
|---|---:|---|
| Hugging Face repo | `n4ze3m/tiny-voca` | [作者の公式カード](https://huggingface.co/n4ze3m/tiny-voca) |
| Publisher 40文字revision | `d94d2a0338fd1e0eab7dd896ec0ad23d8cdf7c14` | [公式API revision固定](https://huggingface.co/api/models/n4ze3m/tiny-voca/revision/d94d2a0338fd1e0eab7dd896ec0ad23d8cdf7c14?blobs=true) |
| 公開元の全ファイル数 | 28 | ソースデータAPI・自動取得しない |
| 推奨FP32モデル | `tiny-voca.pt`：18,209,221 bytes | LFS SHA-256 `ebb22871524c5732520fb1652e6aefcec708a7452e83bdd00adcf6181db5ef70` |
| 発音辞書G2Pデータ | `phonemizer/g2p.npz`：1,840,104 bytes | LFS SHA-256 `eb3fd519ff00e72d850928d2fccb968adc36134bca2f3bda09de7e794c2ed01b` |
| 固定必要ファイル | **14件** | FP32/metadata/LICENSE/phonemizer、一覧は[マニフェスト](../../manifests/drafts/v48-2026-11-18-tiny-voca-immutable-source.candidate.json) |
| 選択ファイル総量 | **23,626,858 bytes** | 公開元整数サイズの和。所有者の実ディスク実測ではない |
| Publisher LFS SHA-256 | 2件 | その他12ファイルにはGit blob SHA-1、ローカルSHA未計算 |
| 非選択ONNX FP32 | 21,386,372 bytes | 同じ学習済み重みの変換版で、原本として重複採用せず |

**権利本文・依存**：[固定モデルLICENSE](https://huggingface.co/n4ze3m/tiny-voca/blob/d94d2a0338fd1e0eab7dd896ec0ad23d8cdf7c14/LICENSE)はApache 2.0、[CMUdict辞書条項](https://huggingface.co/n4ze3m/tiny-voca/blob/d94d2a0338fd1e0eab7dd896ec0ad23d8cdf7c14/phonemizer/LICENSE.cmudict)は著作権・免責表示保存等を要求し、homograph-dataは別LICENSEで提供される。Pythonソースは[tiny-voca GitHub](https://github.com/n4ze3m/tiny-voca)で確認、推論に必要な[dizione](https://github.com/n4ze3m/dizione)の[固定コードLICENSE](https://github.com/n4ze3m/dizione/blob/8cd889e4de7be6bd1dd2e6891344a0729fa14dd4/LICENSE)もApache 2.0と確認した。ただし、当該Gitコード2リポジトリを保存・監査し、安全に実行できることまでは検証していない。モデルからの重み取得に本人権限・本人の利用行為の確認が必要である。

著者ソース参照はtiny-voca `9b6b0899e17a78a25bb3a9f8d9be36dc6c071619`、dizione `8cd889e4de7be6bd1dd2e6891344a0729fa14dd4`（2026-11-18時点観測）。後者のG2P fingerprint `c729f235e10daa1a08ce7711169c1cb93fb552b3c24eecb16527513d7b69d4da` はconfig記載。Git code commitとHub model revisionは異なる体系であり、同じハッシュでないことは矛盾ではない。Python>=3.10、torch>=2.4,<3、numpy>=1.24,<3、soundfile>=0.12,<1、dizione依存を固定しての復元は未実施。

## 3. モデル総数・実行安全・ライセンスの停止境界

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| N_core | 作者報告のtiny-vocaコア学習済みパラメータ総数 | 1（無次元の個数） | 6モジュールの相互重複がない和 | 0以上整数、作者の当該revisionへの記載 | 整数スカラー |
| N_g2p | 別学習済み音素辞書G2Pデータ内のパラメータ数 | 1（無次元） | g2p.npz内部のテンソル要素数 | **未計数**、pickle読み込みせず静的検査 | 整数スカラー（未確定） |
| N_cap | 現行規則の基準パラメータ数 | 1（無次元） | 150×10^9 | 全expertと独立学習済み依存含む、量子化による減数は不許可 | 整数スカラー |

**次元検査**：N_coreとN_g2pの加算は同じ無次元の個数であり、バイトと直接比較しない。コア `N_core=4,537,291` は出版社の6成分合計（16,704＋1,588,864＋123,906＋795,971＋1,985,984＋25,862）。`N_g2p`は未測定なので、コア総数の確認を完全な依存総数の確定とは混同しない。現行v48では**150B未満の研究スクリーン通過**にとどめ、最終lock・承認・ダウンロードには別途完全に静的なテンソル計数が必要。既存の150B超量子化例外審査2件を、この追加で自動許諾することもない。

未審査の`.pt`はpickle系形式としてコード実行の可能性があるので**一切自動ロードしない**。`g2p.npz`は`allow_pickle=False`を用いる静的調査から始める。ONNXの演算子opset17・CPU backend・配布された依存パッケージABI・VRAM/RAM・phonemizerの入力一致は未実証。実行ベンチはモデルカード値と実機を分け、測定する際はCPU/GPU型番、クロック、スレッド数、quantization、バッチ、音声長、反復回数を揃える。

## 4. 規制予測の扱いと既存ポートフォリオ

米NTIAの[open-weight報告](https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations/recommendations)は能力別アクセス制限を将来の政策オプションとして提示したが、tiny-vocaが将来禁止対象になる確率は提示しない。現行公開モデルの検閲/無検閲・画像/音声特化のラベルから法的規制予定を断定しない。v47の無検閲独立編集2系列・OrcaRouter Gated原本を変えずに維持。R111で大型重複のPantheonとDavidAUを品質差保留とした判断も維持する。

Exaへの新規検索は**2026-11-18にAPI 402クレジット上限で失敗**。このR112で一次性を確認したのはHugging Face公式リポジトリ/API、配布者GitHubの固定URLとライセンス本文であり、Exaで検索が完了したかのような表示はしない。

## 5.〈応用・転用例〉H/T/D/C/Uと次の作業

**H**：tiny-vocaが既存のPhonon・Kittenと学習済み/音響方式に違いがあり、追加23.6MBで極小TTS再現研究の比較原本を確保できるという仮説。**T**：本人の正規ファイル取得・コード依存の適法性確認後、同じ32文・各モデル2話者相当以上の発話試験、CPU環境・クロック・バッチ1・試験n_min=32 utterancesを揃える。最初はpublisher情報のみを照合し、モデル実行と本体取得はまだ行わない。**D**：PASSは独自FP32原本と必要なG2P/codeが完全に復元でき、英語TTSとして独立に再現した場合。FAILは無許可・依存欠落・同一チェックポイント・再現不能が確定した場合。UNCERTAINは実機・個人許諾・データ不足（現状）。**C**：既存31Mモデルと同一の能力で代替可能と判定される、または独立実行に高いコスト/未知の問題が現れる場合。**U**：モデルカードの主張、元重みとONNXの未照合、G2Pの内部構成、リアルCPU未測定、法域・保存権限の未確認。繰返し実測分散がないので合成標準不確かさ`u_c`と包含係数`k`は数値化しない。

### ERROR CHECK

- v48：201 unique `asset_kind+repo_id` / 154有効、53 SELECT・101 CONDITIONAL、Gated20・有効な総数未確定9を保持。過去モデルの採否と順位は変更していない。
- 新規原本は14選択ファイル23,626,858byte、そのうち2件Publisher LFS SHA。GGUF通常量子化・ONNXを余分なモデルとして加えず、代替圧縮・その他の推論ランタイムはオプションのまま。
- 承認済みダウンロード0、重量ファイルの実取得0、モデルコード実行0、所有者4TB HDD実測0、完全オフライン復元0。承認キューに追加なし。

## 6.〈次に考える問い〉

**将来の配布制限に備えた原本保全では、再学習しやすい23.6MBの独立モデルを先に実行環境ごと固定する価値と、希少な無検閲17GB級の独立編集結果を優先する価値のどちらが、合法な再取得経路の喪失をより減らせるか。**
