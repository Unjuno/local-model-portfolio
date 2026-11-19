# R117｜v48・取得報告53件の再照合と次に保存する原本8資産の確定

調査日2026-11-19。GitHub正本v48、201登録・154有効。**今回行ったのは既存台帳の全件突合とHugging Face一次APIによる新たな選択ファイル固定であり、Windows Dドライブの再マウント・モデル重み転送ではない。**

## 1.〈本論〉既存ダウンロードを二重実施しない

[取得台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は2026-11-19T08:54:46Z作成。**全54報告のうち53モデルをVERIFIED、1モデルはGated HOLD**と記録。53モデル・579ファイル・270,835,576,267byteについて公開元とローカルSHAが一致したと報告し、計測期間の最小空き2,710,260,613,120byte、200GB床を維持したとの記録がある。これは**その実行元が報告した結果であり、本研究セッションがDドライブを独立に再ハッシュした証明ではない**。

旧[R116文書](116-v48-r115-windows-d-unattended-acquisition-and-reconciliation.md)内の22 VERIFIED/162.326GBは新台帳より古い状態。旧報告を現状と誤認して再取得しない。53モデルは全て現行154有効資産に含まれ、重複ID0。未報告100件、Gated HOLD1件。

[154全件・一意の取得状態と次アクション](../../catalog/decisions/2026-11-19-r117-all154-acquisition-gap-and-next-wave.json)に、公開元revisionとreported source容量、正式portfolio判断、本人アクセス・取得未報告を突合した。Gryphe/PantheonとDavidAU等、現行R115で「新規取得HOLD」でも歴史台帳にはVERIFIED報告がある資産を**削除・再取得しない**。

R115の保存版アップグレード3件は別スコープ：ZONOS3-Miniの原本＋codec 15,345,816,226byte（旧取得報告775,728,152byte）、Interpretic v2 BF16 55,586,056,799byte（旧GGUF Q4 17,738,327,225byte）、0bserverx RVN-F16 53,808,326,934byte（旧Q4＋projector 17,176,692,278byte）。**同repo取得済みという理由だけで高精度原本まで取得済みと判断しない**。3件のpublisher source計124,740,199,959byte。容量・hash unionと各用途差はWindows実データで再確認する。

## 2.〈本論〉次回8原本を不変ソースで固定

以下は153有効SELECT/CONDITIONALの既存登録から、取得台帳に存在しないモデル6件／データ2件を選定した。通常のquant siblingsとdemo imageを落とし、各repoのauthor SHA、ファイルサイズ、LFS sha256もしくは通常Git blob sha1を原配布元APIから記録した。

| 次順位 | 保存対象 | 独立保全価値 | 固定source bytes | ファイル件数 |
|---:|---|---|---:|---:|
| 1 | [ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100) | 日本語の外部評価と過去対照回答 | 7,788,480 | 66 |
| 2 | [Aya Dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 多言語人手指示・評価 | 140,160,376 | 6 |
| 3 | [iLLaDA-8B-Base](https://huggingface.co/GSAI-ML/iLLaDA-8B-Base) | 非自己回帰・拡散言語モデルの学習結果 | 16,512,918,618 | 16 |
| 4 | [RWKV7-7.2B](https://huggingface.co/RWKV/RWKV7-7.2B-20260805) | 独立再帰型言語モデルの原本とコード | 14,402,000,339 | 19 |
| 5 | [TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) | 3D形状・材質を生成する複数学習済み成分 | 16,237,485,044 | 22 |
| 6 | [Wan2.2 TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | 動画DiT、専用VAEとUMT5 encoder | 34,201,539,556 | 16 |
| 7 | [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | 高速画像生成原本とtext encoder/VAE | 32,848,321,404 | 21 |
| 8 | [Fara1.5-27B](https://huggingface.co/microsoft/Fara1.5-27B) | GUI画面操作・browser agentの異なる後学習成果 | 54,743,814,229 | 22 |
| **計** | **6モデル＋2データ** | **重複登録0** | **169,094,028,046** | **188** |

source単位で48件のpublisher LFS SHA256、残りはGit blob SHA1を保管。詳細revisionとallowlistは[R117次期選定ソース](../../queues/proposed-v48-r117-next-wave-eight-source-pinned.json)。動画/画像のデモassetは除外したが、VAEとtext encoderは必要な学習済み依存として残した。**TRELLIS.2の512/1024段階は異なる学習済み重みであり、単なる量子化の重複とは認定しない**。

8件には公開表示のMIT、Apache-2.0、CC-BY-SA-4.0のタグがあり、全て非Gated。ただしモデルカードのタグだけで本人の意図した利用・再配布・外部依存の契約審査が完了したとは言えない。特にiLLaDAの独自`modeling_illada.py`、RWKV kernelコード、Wanの`.pth`は**無審査のコードロードやpickle実行を行わない**。データセットの配布・二次利用はライセンスとプライバシー条件を別途監査。

## 3.〈応用・転用例〉4TBの段階的保全

既存R115で報告外の別ソース3件と新R117次期8件を合算すると、上流選択sourceは**293,834,228,005byte（293.834GB）**。これは実物の重複を差し引く前の比較用であり、新しい物理予約の確定値ではない。旧取得台帳の最小空き2.710TBを仮にそのまま使えば約2.416TBが残るが、**現在のDドライブの空きをこの値と仮定することは禁止**。stage/cache、依存、他プロセス、ローカル重複を実測後に判断。

まずDドライブ上の53報告済みモデルを再発見し、ファイル実SHAと実使用容量を確認する。その後、既存R115の原本拡張3件を個別に処理し、次にR117の少容量データ2件から順に取得・ローカルSHA照合・オフライン復元を進める。**本研究用キューは非実行。正式`queues/approved.json`は空であり、このターンは新モデル重みを転送していない。**

## 4. 規制リスクの根拠

米国BISの[2026-11-19公開検査文書](https://public-inspection.federalregister.gov/2026-23529.pdf)はAI Diffusion RuleのECCN 4E091によるモデル重み統制を撤廃し、先端半導体と遠隔計算アクセス規制を別途扱う。したがって『モデル重量の一般的配布が直ちに一律禁止される』という予測は現在の法的事実ではない。一方、Hugging FaceのGatedアクセス、モデル配布者の個別削除やライセンス変更は別の観測リスク。重みの保存価値は独立学習結果・復元困難性・既存保存状況に基づいて判断する。

## 5. 変数表・次元/誤差

| 記号 | 意味（日本語） | SI単位 | 定義 | 範囲・条件 | 型 |
|---|---|---|---|---|---|
| `B_old` | 既存R115未報告3source | byte | 124,740,199,959 | publisher source、正味増分でない | 非負整数スカラー |
| `B_new` | R117新選定8source | byte | 169,094,028,046 | publisher source、正味増分でない | 非負整数スカラー |
| `B_sum` | 両候補源の論理合計 | byte | `B_old+B_new` | 重複・stage未反映 | 非負整数スカラー |
| `F_report` | 過去取得台帳の最小空き報告 | byte | 2,710,260,613,120 | 今のWindows実測ではない | 非負整数スカラー |
| `F_floor` | 常時維持すべき空き床 | byte | 200,000,000,000 | 現行archive policy | 非負整数スカラー |

算術と次元チェック：124,740,199,959byte＋169,094,028,046byte＝293,834,228,005byte。全てbyteで比較可能。物理HDD・キャッシュ・転送時ピークの不確かさは未計量のため安全な合計誤差推定がなく、`u_c`/`k`を数値化できない。

## 6. H/T/D/C/U、ERROR CHECK

**H**：既存検証台帳の確認を先行し、異なる独立学習成果に限定してファイルを選ぶと、二重転送が減り4TB内で機能カバレッジが増える。

**T**：現行154件を台帳54件と全件突合し、8資産188ファイルのpublisher immutable revision/byte/hashを実査。オフラインの10回帰テストは10/10 PASS。未知のfile/hashや重複IDが1件でも見つかれば停止。

**D**：154件の一意分類、8原本のsourceメタデータ整合はPASS。本人現物再ハッシュ・契約・runtime閉包・オフラインrestoreはUNCERTAIN。容量超過や法的アクセス欠如はFAIL。

**C**：既存53報告に欠落がある、配布元の版が異なる、非量子化の特殊学習済み部品がまだ依存先として抜けている場合に判断は崩れる。

**U**：台帳の帰属と保存先現物、publisher SHAの転送後再測定、未知データのlicenseとコンポーネントABI。分布・標本独立性の未確認により合成標準不確かさと包含係数は設定しない。

**ERROR CHECK**：v48 201登録／154有効、報告53＋Gated保留1＋未報告100＝154。次期8は現行154の内数、53報告済みとのID重複0。6モデル2データ＝8。188ファイル／48上流SHA256参照／169,094,028,046byte。研究テスト10/10 PASS。データ変更はGitHubの研究メタデータとテストのみ、重量DL0、正式承認0。

**関連分野**：機械学習の学習系統・モデル依存、デジタルアーカイブとハッシュ証明、ソフトウェア供給網、言語データ評価と輸出/著作権法。

###〈次に考える問い〉

今ある53件の実SHAを最短で独立再確認し、3件の原本拡張と次期8件を失敗なく順次保存するために、Windows Dドライブ上でどの既存ダウンロードログを正本とするべきか。
