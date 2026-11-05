# R19：画像追加学習・音声編集の限定調査（2026-11-04）

## 1. 正本・今回の反映範囲

調査基準は `main` の `c1872652a389b7d4c389beb55dfb689ea5c90af1`。`catalog/CURRENT.json` は v17、管理142件／有効研究選定97件／保留27件／除外6件／繰延12件。前回の `catalog/proposals/18-media-mechanism-selection-2026-11-04.json` は3件の推薦であり、実体化カタログには未反映だった。

今回は直近90日（2026-08-06〜2026-11-04）を優先し、**画像の学習済み差分と音声の編集・変換**の2領域に限定。8候補を比較し、研究台帳上で **CONDITIONAL 3／HOLD 3／REJECT 2／SELECT 0** と決定する。**これは取得許可でも、現行カタログに8件を足す操作でもない。** 全構成と実用品質の未確認を解消しないまま正式採用へ昇格しない。

[機械可読の判定・証拠台帳](../../catalog/research/2026-11-04-round19-decisions.json)と[非実行のファイル証拠](../../manifests/drafts/round19-media-evidence.candidate.json)を正本とする。既存のNanbeige維持・6件除外、CURRENT、取得キュー、ダウンローダー、実機HDDは変更しない。

## 2. 候補一覧：配布元・更新日・方式・規模・容量

更新日はHubメタデータで観測した日。初回公開日とは区別する。全行の確認日は2026-11-04。規模は特記しない限り主モデルのみで、codec/encoder等を含む完全総数は未確定。容量はbyte、GBは十進で記録し、作者の概数はそのまま概数として残す。

| 順 | repo ID／直接配布元 | 更新日 | 技術方式 | パラメータ情報と未確定範囲 | 保存容量の根拠 | 判定／信頼度 |
|---|---|---|---|---|---|---|
| 1 | [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | 10-16 | rank128・画像生成/編集LoRA、224modules/448tensors | アダプター全スカラー数未確認。基盤DiT約7B＋encoder約8B＋VAE | アダプター **671,151,136 B**。基盤/依存は別 | CONDITIONAL／出所中・品質低 |
| 2 | [fishaudio/drama-3-int4](https://huggingface.co/fishaudio/drama-3-int4) | 10-14 | AK製量子化をFish Audio配下へ複製。MoE音声編集・hybrid W4A16 | 元主モデル約**35.8996B**。Hubの6.8578B表示を論理総数としない。codecは別確認 | 作者22.1GB、tree約24GB、engine weights20.8GBは異なる範囲。全選択byte未確定 | CONDITIONAL／出所中・品質中 |
| 3 | [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | 10-30 | rank32、step1500の画像編集位置保持LoRA | アダプター全スカラー数未確認。基盤約7B＋encoder約8B＋VAE | LFS pointerで **159,436,496 B**。依存は別 | CONDITIONAL／出所高・品質中 |
| 4 | [laion/Humaneness-Voice-Converter](https://huggingface.co/laion/Humaneness-Voice-Converter) | 10-11 | score-conditioned flow-RL音声→音声変換 | 主部品264.1M、flow学習対象112.62M。Ears等を含む完全総数未確認 | 作者export証跡 **1,056,773,004 B**、推論一式ではない | **HOLDへ見直し**／出所中・品質低 |
| 5 | [laion/Humaneness-Voice-Large-1.6-Alpha](https://huggingface.co/laion/Humaneness-Voice-Large-1.6-Alpha) | 10-27 | 1.5＋RealSpeech rank4を一度マージしたFP32親モデル | 基盤 **4,129,990,144**、外部MOSS codec別 | 主重み約16.5GB、完全容量未確定 | HOLD／出所中・品質低 |
| 6 | [laion/Humaneness-Voice-Large-1.5-Alpha](https://huggingface.co/laion/Humaneness-Voice-Large-1.5-Alpha) | 10-27 | 未マージ1.3基盤＋累積rank128 RLアダプター | 基盤4,129,990,144＋adapter96,337,920、codec別 | 全一式未確定 | REJECT：今回は完全重みの重複保存をしない |
| 7 | [YueFong/Qwen-Image-2.1-Uncensored-GGUF](https://huggingface.co/YueFong/Qwen-Image-2.1-Uncensored-GGUF) | 10-10 | 元重みの量子化・再包装という作者説明 | 基盤約7B＋encoder約8B＋VAE。圧縮で論理総数が減るとは扱わない | Q4約4.60GB＋encoder約9.35GB＋VAE約676MB、選択byte未確定 | REJECT：独立した新能力枠として |
| 8 | [laion/Humaneness-Voice-Small](https://huggingface.co/laion/Humaneness-Voice-Small) | 10-12 | Qwen3-0.6B＋local Talker、演技後学習 | semantic約0.6B、Talker/codecを含む総数未確認 | 未確定 | HOLD：既存TTSとの重複 |

信頼度は出所・性能についての定性的な評価であり、将来規制の確率ではない。SELECTが0件なのは、名称や単一の良好なスコアだけで品質と実行条件を確認済みにしないため。

## 3. 性能・反証・既存との差・利用条件

| 対象 | 採る理由／既存との差 | 不採用にすべき理由・失敗例 | 独立評価／実装条件 | ライセンス・正規取得条件 | 次の判定 |
|---|---|---|---|---|---|
| ChatR Omni | 学習済みの生成/編集差分。既存Qwen-Image-2.1を再利用できる | 独立画質・成人向け対応の比較なし。「無フィルター」は能力改善の証明でない | 作者の2×RTX4090 24GB・BF16・25step・CFG4の単発動作確認。中央値や同条件品質比較ではない | 作者GitHub v0.1のLICENSEを読取。Qwen Research Licenseは研究/評価の非商用利用を条件付き許諾。LICENSE/Notice・親モデル条件を保存 | base-onlyと同seedで品質、指示追従、adapter key適用率を比較 |
| Drama3 INT4 | S2-Proにはない部分編集・再演出。FP8と別能力ではなく実行表現の選択 | タグ行の途切れ。共有expertの過度な量子化でゼロ音声フレームになった失敗も作者記録。原因仮説を確定原因としない | 作者H200同時8要求、Seed-TTS英語1088文。p95はFP8 1.902s／INT4 2.178s。WER1.99%／1.63%だが、WER50%超を除くと1.32%／1.42%に逆転。非劣性を証明したとは言わない | Fish Audio Community v1.0。研究・非商用、Hosted Service、声の同意、透かし、出力の追加学習等の条件を用途別記録 | 日本語、音声編集、長文を同条件比較。AK元版と配布コピー全hashを照合 |
| Consistency1500 | 未編集領域と構図を維持する特殊能力。普通の画質/NSFW学習とは別 | 新ポーズ・顔向き変更を妨げる。大きな削除で残像。step2000は色調がずれる | 作者のheld-out36編集、同prompt/seed、INT8 Qwen2.1・ComfyUI・25step・CFG1・euler/simple・約1MP。最大コーナーずれ中央値24.3→1.6px。評価GPU/クロック未記載、独立再現なし | Qwen Research License適用という作者説明。HFとCivitaiの同一ファイル性は未照合 | 構図維持とポーズ変更を別試験。Turbo/2MP試験記述が一次ページ間で食い違うため25stepだけを暫定条件とする |
| Humaneness VC | 既存Chatterboxを源流に、元音声の演技を保ちながら声質を変更 | speaker cosine **0.821→0.773**。感情MSE改善0.113→0.092は学習報酬judgeを再利用、学習UID重複もある | 作者の40音声×2声。GH200120GB・BF16・10steps、6.53秒入力で生成中央値0.558s/3runだが前処理・ランキング等を除外。日本語/MOS/WER未検証 | LAION追加CC BY4.0、Chatterbox由来MIT。権利不明を理由に下げたのではない | 前回の条件付き推薦を保留に変更。独立の明瞭度・感情・声一致試験が先 |
| Humaneness Large1.6 | 現行のマージ済み演技モデル。1.5より新しい親版 | 過去の未マージrank4のWERを1.6へ流用不可。日本語の保証なし、専門adapterは別/Gated | 作者GH200試験で約32GB peakだが全長の最大値ではない。4.13B主モデル＋外部codec、custom code | 追加CC BY4.0、依存条項別。公開親版から専門adapterの取得権限を推定しない | exact merged1.6とQwen TTS/Audio8を同条件で比較 |
| 1.5／Small／YueFong | 再現用祖先や別実行形式としての価値はあり得る | 重複基盤や根拠の乏しい新能力枠は増やさない | 新規の実用優位は今回確認できない | ライセンス制約だけで不採用にしていない | 新しい比較証拠が出たときのみ再審査 |

[Drama3論文 arXiv:2610.18010v2](https://arxiv.org/html/2610.18010v2)の編集能力と[Artificial Analysisのサービス評価ページ](https://artificialanalysis.ai/text-to-speech/providers/drama3)も確認した。ただしサービスの音声品質は、このINT4チェックポイント、ローカル設定、日本語編集能力の独立評価ではない。APIの点数や単一stream271frames/sを別設定の1088文比較に混ぜない。

## 4. 容量・実行性の訂正

**INT4の重み約22GBから24GB GPUでの実行可能性は導けない。** [配布者README](https://huggingface.co/fishaudio/drama-3-int4/blob/main/README.md)はA10080GB・メモリ割当比率0.62/0.2でstartup57.3GB、試験peak57.9GBを報告する。予約領域を含む試験値は最低必要量でもない。32/48GBでの実行は未検証と明記されている。

量子化はgroup128の対称4bit、RTN＋group clippingで、GPTQ形式/Marlin kernelを使うが、校正データを用いたGPTQ最適化ではない。shared expertと音声decoderはBF16を保持。compute capability8.0以上が必要という記述があるが、単に対応GPUであるだけで全構成が収まるとは言えない。

2つの画像LoRAのファイル合計は **830,587,632 B（十進約0.831GB）**。同じ固定版の基盤・encoder・VAEを既に保全している場合に追加される重みファイルの合計であり、設定・ライセンス資料や実行一式の容量ではない。各159,436,496 Bは十進約159.44MB、二進約152.05MiB。Civitaiの「152.05MB」とHFの約159MBを別モデルと早合点しない。

現行設定はアーカイブ3.8TB、独立した空き200GB条件、推論ピーク512GB未満、150B原則＋検証済み量子化例外。現地の全容量・空き・GPU/RAMは未確認。この回で数字を書き換えたり容量を予約したりしていない。

## 5. 原本・ミラー・ハッシュ

ChatRはHFに加え、作者GitHubのRelease asset `659921001`、サイズ、SHA256を再確認。`immutable:false`でありタグだけでは固定にならない。Consistency1500はHFの**LFS pointerだけ**を読み、159,436,496 BとSHA256 `4f44ada1be2189cc23b3d010f9603543403f48454e2f76842a3d30109b20bd63`を取得。重みそのものはダウンロードしていない。

Voice Converterは作者EXPORT_PROOFの1,056,773,004 BとSHA256を再確認。REPRODUCINGのmerge誤差記述とEXPORT_PROOFの値が一致しないため、bit再現性を保証しない。ローカルハッシュ、全依存、完全なrevision固定は別の作業。

CivitaiはConsistencyの作者ページと実験記述を対照に使った。Pirate Faceの現在Seeder数とModelScopeの同一重みは今回再確認していない。過去にSeeder0だった観測を現在値として再利用しない。正規配布元に同一ファイルの証跡がある場合、索引・ミラーを追加するだけで独立保存価値が増えたとは数えない。

## 6. 判断手順の追加

1. 能力単位と配布形式を分ける。同じDrama3のFP8とINT4は2能力ではなく代替ファイル候補。
2. モデル論理総数、量子化後の格納テンソル数、活性expert数を別フィールドにする。Hubの6.8578B表示は元の35.8996Bという論理規模を置換しない。
3. 型・形式検査と出力品質を分ける。「読み込めた」「誤差normが小さい」だけで音声が生成できるとはしない。
4. 平均、中央値、p95、標本数、切捨て規則を保存する。外れ値除外で優劣が逆転するなら強い改善主張をしない。
5. 1.5の結果を1.6へ、FP8をINT4へ、作者APIを公開重みへ転記しない。版・精度・前処理・言語・コンテキスト・batchが異なれば別実験。
6. 研究上のCONDITIONAL、実体化カタログ、取得承認、実際の取得、実機合格を独立した状態として記録する。

統計的評価、推論システム工学、デジタル保存・権利管理の3分野を合わせ、性能・再現性・保存コストを同じIDと版で追跡する。

## 7. H/T/D/C/U・終了条件

**H**：候補の学習済み差分や音声編集能力は、現行の近い基盤/モデルでは代替しにくく、実用品質の下限を満たす。

**T**：次の実験は同意済み素材と固定prompt/seed、用途を層別した比較。画像は構図維持と動作変更を分離。音声は日本語/英語・編集/通常生成・声一致/自然さを分離する。backend commit、量子化方式、zero-point、ABI、GPU/RAM、入力長、batch、clock不明を記録。現段階では計画のみで推論していない。

**D**：事前固定した用途別閾値・完全依存・権利・容量・実機速度を満たせばSELECTを再審査。明確な劣化・重複はREJECT、欠測・矛盾はHOLD/CONDITIONAL。欠測を0やPASSで埋めない。

**C**：位置保持の過学習、shared-expert量子化失敗、報酬judgeへの適合、声一致低下、未マージ/マージ版の取り違え、同名ミラーの別バイナリ。

**U**：judgeの系統誤差・訓練重複・試行分散・言語/機器差を主要誤差源とする。合成不確かさとカバレッジ係数は未算定。著者表だけから信頼区間や規制確率を創作しない。

**終了**：この回は2領域8候補で打ち切る。新しい有力候補を無限に追加せず、次は選ばれた3候補の未検証項目を解く。

## ERROR CHECK

新規の研究台帳・ファイル証拠に対する標準ライブラリのread-onlyテスト9件をローカル実行。全リポジトリの既存監査は当該コミットに対応するGitHub Actionsで確認する。CIはファイルの整合性検査であり、推論・ライセンスの法的認定・公開重みの品質保証ではない。

CURRENTと実体化カタログ、取得キューは無変更。既存142/97を維持し、ローカル取得/削除・Torrent・インストールは0件。
