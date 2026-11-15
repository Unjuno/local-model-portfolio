# R93｜Hugging Face 全148有効資産の現行アクセス・ライセンス・独自原本監査（2026-11-15）

**主張できる範囲**：GitHub `main`／正本 `catalog/CURRENT.json` → **v41、195登録・148有効（130モデル・18データ）**。Connected Hugging Face `hub_repo_details`で**148/148件の現在のリポジトリ要約メタデータを取得**、うち**Gated表示20件／過去のGated記録20件／表示上の不一致0件**。これは2026-11-15時点の**公開情報の照合**であり、重みの可読・同意済み・合法的な保存許可を確認したものではない。

[機械可読・全148行のrepo別証拠と4件のライセンス判定](../../catalog/research/2026-11-15-r93-v41-hf148-live-repo-metadata.json)／[現行effective v41](../../catalog/effective-portfolio-2026-11-15-v41.json)／[148件取得前停止ゲート](../../catalog/readiness/v41-2026-11-15-r92-all148-gates.json)。

## 1.〈本論〉— 公開元を直接調べて何が確定したか

| 分類 | 2026-11-15の実証 | 残る不確かさ |
|---|---|---|
| HF個別repo IDのメタデータ取得 | 130モデル＋18データ＝**148件すべての表示にアクセス**。取得応答なし0。 | 情報はHubの要約メタデータ。README本文・固定revision／LFS・Xet全blob・権利の本人口座許可までの検証ではない。 |
| 現在のGated表示 | **20件**、既存v41の履歴フラグ20件とID単位で完全一致。 | 古い個別承認・失効や実際のファイル取得権限は確認できていない。今回「Gated変更が1件も起きていない」ことを歴史的に証明したのではなく、**2時点の表示レコードが一致**したという意味。 |
| 現行HFメタデータのライセンス | 大半は既存カタログと表記互換。3件で文字列の不一致、1件でHubライセンス欄に表示なし。 | LICENSE本文・派生元・データサブセットの権利、国・用途制限は個別審査。 |
| モデル総学習済み構成 | 過去に未知とされた9件は**9件のまま**。モデルカードの本体パラメータ表示は取得。 | MoE全expert、モデル外codecs/VAE/text encoder/adapterの完全合算は未確認。取得前の総数ゲートを解除してはならない。 |
| 保存の前提条件 | 有効148件全件でreadiness未通過、重み取得・ローカルSHA・オフライン復元・取得承認**0件**。 | 最終files/byte・HDD空き・runtime wheelhouse/driver・cache/staging未測定。 |

**非同一事項**：HFの `region:us` 等のタグは**配布ライセンスの利用可能地域を証明しない**。出版社のLICENSE原文が優先であり、`private:false`や非Gated表示も商用・再配布・保存の権利を付与しない。Connected accountのOAuth `read-repos`も、Gatedモデルについて特定ユーザーが承認されているという証拠ではない。

## 2. 4件のライセンス異常を原文で判定

| repo | HFメタデータ／過去カタログ | 原著作権者の一次記録・判断 | 採否・停止 |
|---|---|---|---|
| [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) | カタログ `[openmdw-1.1,cc-by-sa-4.0]`、HF `openmdw-1.1, cc-by-sa-4.0` | **同じ2種の識別子**をarrayと文字列で表示しているだけ。各元音声データや派生ラベルが一律に同条件という証明ではない。 | 現行CONDITIONAL維持。取得元ごとの権利と再配布条件を精査。 |
| [nvidia/Nemotron-Cascade-2-30B-A3B](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B) | 要約APIの `other`、カタログ `nvidia-open-model-license` | 出版社model cardが**NVIDIA Open Model License**を明記。ラベル形式の差だけで契約変更とみなさない。実行例の `trust_remote_code` は未監査コード実行を要請するので安全なABIが別条件。 | 既存CONDITIONAL維持・モデル本文契約と固定runtime確認。 |
| [nvidia/Nemotron-Cascade-2-SFT-Data](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) | 要約APIの `other`、カタログ `nvidia-open-model-license` | 作者dataset cardにNVIDIA Open Model Licenseとあるが、別のベースデータ・生成モデル由来のprompt/responseが混在。**大元の著作権まで単一ラベルで確定しない**。 | 現行CONDITIONAL維持、原データ由来の権利監査が必要。 |
| [nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B) | HF要約のLICENSE欄なし、カタログ `unknown` | [配布元のLICENSE原文](https://huggingface.co/nvidia/GR00T-N1.6-3B/blame/main/LICENSE)の**NVIDIA License §3.3は非商用の研究・評価のみ**。§3.1はLICENSEと著作権表示を含む再配布要件。 | **権利メタデータを研究台帳で確定**。現行CONDITIONAL維持。ただし商用利用可とは扱わない・ダウンロード未承認。 |

**OpenMDWを誤外挿しない**：[Linux Foundation公式（2026-05-28）](https://www.linuxfoundation.org/press/linux-foundation-releases-openmdw-1.1-nvidia-adopts-openmdw-for-cosmos-isaac-gr00t-ising-and-nemotron-ai-model-families)はNVIDIAの**今後のモデルファミリーへの採用方針**を発表した。これは個別に`NVIDIA License §3.3`が置かれたGR00T版の利用条件を遡及変更した証拠ではない。契約は**モデル×固定revision×ファイルごと**に適用条件を照合する。

## 3. 総数未確定9件の再優先調査

| モデル | 今回観察した本体表示／課題 | 次に取るべき非実行の最短確認 |
|---|---|---|
| [ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | 本体総数の表示なし。LICENSEタグはunknown。 | 元LTX 2.5と編集後の学習済み重みの関係、FP8/その他形式、外部text encoder/VAEの総構成。 |
| [Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | 本体総数の表示なし。LICENSEタグはother。 | 上記と**学習済み差分の同一性**・作者ライセンス原文・full pipelineを比較。名前が同じだけで「重複」認定しない。 |
| [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts) | HFは9.6M、**GatedかつCC BY-NC 4.0**。 | 音響本体＋Vocos／flow／WavLM／MiniLM等を同一固定snapshotで合算。本人の許可と追加音声同意規約。 |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | HFは2,502.4M、Apache 2.0。 | Mimi・ECAPAを含む全外部学習済みcodec／encoderとlicenseを固定。 |
| [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3) | HFは35,899.6M、LICENSEタグother。 | MoE全expert、音声decoder／codecなど全学習済み部品、独自LICENSE正文と固定revision。 |
| [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | LoRA単体で親の学習済み総数は表さない。 | v41で作者推奨step1500のみ固定済み。基盤Qwen・encoder・VAEと同一SHA共有の可否、研究ライセンス。 |
| [PrunaAI/P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image) | HFの33.123Bは主transformer表示のみ。既知3部は46,970,622,448、VAEとconnector未計数。 | [v41一次資料](92-v41-source-and-license-corrections.md)にあるMiniMax派生の地域除外（EU・UK・韓国・米国）、全コンポーネント固定、必要な私的許諾。 |
| [nvidia/Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) | HFの総数表示なし。OpenMDW-1.1。 | ソースからの保守的な上限見積りと**実ウェイト全tensor数の一致**。README上のサイズだけでは確定しない。 |
| [nvidia/Kumo-Anomaly](https://huggingface.co/nvidia/Kumo-Anomaly) | HF総数表示なし。Apache 2.0。 | 8MとSDK別値の相違を原本headerで閉包。安全な公式 `weights_only=True` ローダーの存在と実行安全性は別問題。 |

判定：上記9件は**「取得準備停止／研究候補維持」**。上限150B、例外審査条件、学習済み全構成、本人権利などのゲートを一切緩めない。

## 4. 制限強化という仮説への反証可能な対応

**観測事実**：[EU AI Act公式ガイド](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)では2026-08-02からGPAI提供者義務を執行。[OSS部分免除](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は条件付きで残り、システミックリスクや著作権関連義務は免除されない。[HF自身の2026年公開ウェイト調査](https://huggingface.co/blog/state-of-open-models-summer-2026)はApache/MIT等での公開モデル増加と、一部巨大モデルでの別条件導入を報告。実際には**オープン化と利用制限の分化が併存**する。

**仮説**：T1（対象別制限）→T2（高能力モデル）→T3（全公開ウェイトの広域規制）は将来のストレスシナリオ。150Bモデル総数という個人用ルールはEUの学習計算量・systemic-risk判定とは無関係である。今回の148件メタデータ照合だけで、全体規制を裏付ける削除・Gated化の因果を認定しない。

**保存戦略の修正**：「規制されそうなモデルを片端から増やす」より、少なくとも**Gated20件の本人権利・9件の総数未確定・LICENSE差異4件・保存容量の測定**に作業を優先する。現行有効モデルは既に自然言語、音声、画像／動画、ロボティクス、量子誤り訂正、科学、時系列、表構造を広くカバー。新規採用は**独立学習成果と必要bytesの純増価値**を立証した候補に限定し、主に同族量子化を増やさない。

**選定判断（今回確定）**：
- **維持**：既存v41の195件登録・148件有効。Gatedの20件は高消失確率とみなさず、**合法的アクセスを最初に調べる候補**として維持。
- **研究台帳の権利補正**：GR00T N1.6-3Bを非商用研究・評価のNVIDIA Licenseとして明記。
- **交換・追加は0**：HF要約データだけで同一重みの重複や新たな性能優位を認定できない。LTX系の特殊学習成果を未検証のまま棄却せず、LoRA親重みを重複取得しない。
- **保留**：9件の完全総数不明、Prunaの地域／追加コンポーネント、Granaryの原データ単位の権利等。**承認キューとCURRENTの更新なし**。

## 5. 変数表と次元確認

静的監査における件数の検算式：

\[
N_{\mathrm{active}}=N_{\mathrm{model}}+N_{\mathrm{dataset}}=130+18=148.
\]

| 変数 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| \(N_{\mathrm{active}}\) | 有効保全候補の総登録数 | 1（件） | v41でSELECTまたはCONDITIONAL。0以上195以下 | 非負整数スカラー |
| \(N_{\mathrm{model}}\) | 上記中のモデル件数 | 1（件） | 上記をasset_kind=modelで分類 | 非負整数スカラー |
| \(N_{\mathrm{dataset}}\) | 上記中のデータ件数 | 1（件） | 上記をasset_kind=datasetで分類 | 非負整数スカラー |

次元確認：130件＋18件は次元1の同種の登録数で、148件と整合。Gated数20は**別の重複可能な属性**なので右辺に加えてはならない。

## 6. H / T / D / C / U・ERROR CHECK

**H（反証可能仮説）**：現行配布元の認証・LICENSE・依存元を一意に確認することで、根拠のない新規採用より多くの合法的なオフライン復元可能候補を確定できる。評価指標は、次回監査までに全停止ゲートを通過したasset数、偽陽性のlicence change判定数、実復元成功数。

**T（最小検証）**：公式HF `hub_repo_details`を10 repo以下／呼出しで15回、130モデル・18データを全件照合（n=148）。raw metadataを保存し、要約ライセンス差分3件・ライセンス表示欠損1件を**作者の一次カード／LICENSE**で別途検証。停止条件はID欠損・本人承認不可・complete tensor count不明・unsafe loaderで実行しようとした場合。

**D（合否）**：PASS＝148 ID一意・全meta応答148・観測Gated20・履歴20との表示不一致0・LICENSE問題4件を一次情報で分類・無許可DL0。UNCERTAIN＝本人の重みへのアクセス、LICENSE行為別承認、完全MoE数、実ディスクとoffline復元。FAIL＝要約API `other` を無条件に全利用許諾とみなす、GR00Tを商用利用可と誤表記、承認なく重量・codecを取得。

**C（破れ方）**：HF要約が遅延・改変済み、実repoのimmutable snapshotが変更、LICENSE違反や権利第三者請求、未申告の学習済み依存、類似モデルに本当に優越的な非代替性能が認められる場合。

**U（不確かさ）**：Hubキャッシュ、model card metadataの過小計数、本人のGated状態、元データ著作権、地域利用規約、実ハードの容量・実行差。統計的誤差分布と反復測定がないため合成標準不確かさ `u_c` と包含係数 `k` は数値化不能。報告されたモデル評価は本監査で再計測していない。

**ERROR CHECK**：148/148のHFメタデータ取得PASS、130モデル＋18データ、Gated20、偽のGated変化主張0、要約差異3／欠損1を一次原文で分類、新規ライセンス改定と証明されたもの0、総数未確認9、合法的取得許可0、重量DL0、コード実行0、本人HDD実測0。**正式v41のselectionは変更なし**。

関連学際領域：AI法・国際契約／デジタルアーカイブ・記録管理／AI/ロボティクス／ソフトウェア供給網・安全なABI／統計的モデル比較。

## 7.〈次に考える問い〉

**今あるGated20件のうち、本人の明示アクセス承認とLICENSE・全原本sourceの閉包を最短で証明できる資産はどれか？** データを増やす前に、その1件を真に再現できる保存対象へ進められるかが次の合否指標となる。
