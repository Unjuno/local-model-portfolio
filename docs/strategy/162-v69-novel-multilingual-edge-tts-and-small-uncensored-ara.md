# R162/v69: 多言語7.88M・ベトナム語100K TTSとInkling別編集LoRAを条件付き追加（2026-11-25）

## 1.〈本論〉保存目的・採否

**正本 v68の252件は完全不変、v69で新規3モデルIDをCONDITIONAL登録：255登録／206有効、SELECT56、CONDITIONAL150、HOLD30。** 最新116件のVERIFIED取得報告に新3件は存在しない。いずれも**新規ダウンロード許可ではなく保存対象の選定**。既存116再取得0、approved queue0、Owner D現物再SHA0、実重量転送0、未審査任意コード実行0。

[小型音声2source SHA資料](../../manifests/drafts/r162-2026-11-25-paradee13-tihon100k-core-weight-pins.candidate.json)と[独立低拒否編集LoRA原本](../../manifests/drafts/r162-2026-11-25-electroglyph-inkling-heretic-v22-adapter-core.candidate.json)に、Publisher 40桁immutable commit、**5 weight file 92,138,387 byte**とSHA256を固定。しかし全非重みファイルと依存を個別SHA/byteで列挙し尽くしたものではない。**全取得対象のimmutable source scope未閉包→取得STOP**。これを完了したかのように誤った`fully_pinned_revision_sha`/承認フラグを生成しない。

## 2. 3モデルの独立性と負の証拠

| Publisher original / edited-state | 不変出典・固定コア | 決定・価値 | 未解決点 |
| --- | ---: | --- | --- |
| [sahilmahendrakar/Paradee-8M-v1.3](https://huggingface.co/sahilmahendrakar/Paradee-8M-v1.3/tree/b569f5efb789af5ba643a44af348427242ceb784) | INT8 ONNX 8,462,503 B＋学習済みPyTorch text/decoder各16,991,179/14,656,297 B＝**40,109,979B** | **CONDITIONAL**：Kokoro-82M教師から**別学習した**7.88Mモデルをv1.2から追加学習、8 voicesで英/ヒンディー/仏/西の4言語。3種ファイルは別モデルIDでなく、同学習成果の推論と訓練表現 | 発行者200文/voice、Hindi WER21.6～21.7%。M4 Pro CPU1threadの約62×RTFxは主にv1.2で、v1.3は2%以内との作者値。Python>=3.10/onnxruntime>=1.17/misaki/spacy、非英語はeSpeak NG系（GPL3別コンポーネント）。PyTorch .pt pickleは非信頼ロード禁止 |
| [ngocthien/tihon-tts](https://huggingface.co/ngocthien/tihon-tts/tree/bc71174f68651e7ff32a90f1ffd5e7528288d403) | F32 safetensors **411,224 B**, SHA256固定 | **CONDITIONAL**：独立10万118パラメータ、ベトナム語4声、音響を調波＋雑音で合成、24kHz。小型マイコン/NPUの別設計 | **CC BY-NC 4.0、商用利用不可**。作者のCER1.0～2.3%は36文/voice、主観MOSなし、Cortex-M55+Ethos-U55数値はシミュレーションのみ。trust_remote_codeのモデルコード、本人法的権利と実MCUテストを未検証 |
| [electroglyph/Inkling-2-Mini-uncensored-LoRA](https://huggingface.co/electroglyph/Inkling-2-Mini-uncensored-LoRA/tree/4d81722b2e939460d5b544e5319b80e9b960236b) | `adapter_model.safetensors` **51,617,184B**（repo全体52,406,603B、他9fileは個別SHA未固定） | **CONDITIONAL**：Heretic v2.2.0.dev0 ARA edited-state。既取得original Inkling親を再取得せず、既登録OpenUncensored rank2・satellitedownとは異なる設定を保存し研究比較する。**training-free重み編集であり「別の事前学習」ではない** | 作者refusal keyword 3/100対親100/100、KL0.0883、neutral MMLU/日本語/画像の独立成績なし。parent SHA、LoRAマージABI、rights、完全source未閉包 |

[Paradee原作者コード](https://github.com/sahilmahendrakar/paradee/tree/2de547e45da92840a636c499eb0782e988be1e47)の`pyproject.toml`はv1.3.1、numpy/onnxruntime/misaki/spacyなど。eSpeak NGはオプションだが非英語前処理に使われる。PyTorchとONNXは学習成果を2/3個と数えるものではなく、正本学習状態と推論形態のセット。

## 3. 研究HOLD・却下する交換

- **[Aion-1.0-Instruct-2.3B-Abliterated](https://huggingface.co/OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated)**：既取得済みMicrosoft/Aion 2.3B親からのfull-weight 4,577,698,688 B編集版。作者refusal 5/100と曖昧なvery-low KLのみ、既存重み編集資産に対する品質増分不明。**HOLD**、元重みとのシリアライズ差分と実機品質評価を先行。
- **[MC7ever/Dory4B-heretic](https://huggingface.co/MC7ever/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16-heretic)**：独立ARA編集のlooped Dory、Publisher約7,968,035,453B、refusal 8/100対親100/100、KL0.0664（作者測定）。**OpenMDW-1.1はApacheではない**。親取得状態と再現レシピ・利用許諾未閉包、全量の保存はHOLD。
- **[Peymandc/Qwen3.5-0.8B-Heretic-Uncensored](https://huggingface.co/Peymandc/Qwen3.5-0.8B-Heretic-Uncensored)**：訓練なしARA再現可能版1,726,760,416B。取得済みQwen原本とnchapman約6MB二編集LoRAに比べフル重量重複。refusal keyword 8/100、KL0.0675も作者100文。正式追加を保留、必要なら再現config・patchだけ選ぶ。形式変換は別trained outcomeと数えない。

## 4. 取得実行に進まない理由

ユーザー個別の利用権・法人収益条件・モデルカードAUP・CC BY-NC/音声源、Publisher全path/bytes/SHAの閉包、phonemizerとeSpeakバイナリ/音声前処理/Gitリビジョン、owner実ディスクSHA/4TB budget/200GB残床/キャッシュ、CUDA/ONNX Runtime/Transformers/PEFTループモデルABI、実ハードウェアピークRAM、完全オフライン復元と明示ファイル別承認がない。これらのどれかが閉じない限りモデル重量転送を行わない。米国BISの[2026-11-19告示](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)のモデルウェイトECCN4E091撤回を、将来の全モデル所持禁止の確証と誤読しない。

## 5. H/T/D/C/U・変数表・ERROR CHECK

**H**：既存Kokoro/TinyVocaと同じtrained成果を重複せず、4言語8声の新蒸留状態、10万ベトナム語独立状態、Heretic 2.2 ARA別編集を少量core weightで保全できる。

**T**：公開SHAを5file照合、旧252行JSON完全同一、全116既取得ID保持、205ではなく**206有効のqueue/prep/readiness** ID同集合、150 CONDITIONAL access同集合、承認0。実機の別途最低100文/言語・最低30同条件反復、速度・WER/CER/MOSをCPU型/クロック/OS/ONNX ABI/バッチ1・音声長・sample rate 24kHzで測る。低拒否モデルは安全/中立/拒否の独立50～100タスクと信頼区間で評価。

**D**：Publisher weight SHA5/5、整合/重複0がPASS。owner実SHA、ライセンス行為、全依存コードレビュー、音質/安全はUNCERTAIN→**取得STOP**。勝手な承認、存在しない受給資格、pickleの未監査ロードはFAIL。

**C**：多言語G2Pが再現不能、TiHonのNC権利で用途不適合、Hereticの低拒否化が中立能力を損なう、量子化/実行ABIが不整合。

**U**：作者ベンチの小サンプル/発音差、実機速度条件差、原本とowner媒体の未照合、Python/FFmpeg/runtimeの版差。標準不確かさu_cと包含係数kは繰返しの実測がないため評価不能。

| 記号 | 日本語の意味 | SI単位 | 定義 | 定義域/前提 | 型 |
|---|---|---|---|---|---|
| `B_core` | 新3原本のweight-only core参照総量 | byte (B) | 5正確なPublisher LFS重みの総和92,138,387 | >0、非重み/依存/owner実容量を含まない | 整数スカラー |
| `B_full` | 完全オフライン復元に必要な原本と依存の総量 | byte (B) | 全選定ファイル・codec・wheelhouse・runtime | 未確定、>B_core | 非負整数スカラー |
| `B_owner` | 所有者媒体への純増容量 | byte (B) | owner hash/共有/キャッシュ後の実量 | 未計測、>=0 | 非負整数スカラー |
| `N` | 音声テスト文数 | 1（無次元） | 各言語100以上で固定 | >=100/言語、未実施 | 整数スカラー |
| `u_c` | 合成標準不確かさ | 測定対象同単位 | 誤差源を分散合成 | 未計測 | 非負実数 |
| `k` | 包含係数 | 1（無次元） | 信頼領域を指定 | 被覆未定 | 正実数 |

次元チェック：重量の足し算はすべて10進byte、同次元。B_coreとB_fullを混同しない。Mbps/MB/s・GB/GiB・RTFxの定義、GPUバッチとtoken数を固定して比較する。

学際：①音声信号処理/蒸留、②越言語音韻学・G2P、③エッジMCU/NPU・量子化、④安全性アラインメント/モデル編集、⑤暗号ハッシュとソフトウェア供給網、⑥CC-BY-NC・GPL/輸出管理。

**ERROR CHECK**：v69 255登録／206有効／SELECT56・CONDITIONAL150・HOLD30、旧252行完全不変、116 ledger ID all included、5重量file SHA all 64 hex and exact bytes、approved0、owner D編集0、third-party code実行0。
