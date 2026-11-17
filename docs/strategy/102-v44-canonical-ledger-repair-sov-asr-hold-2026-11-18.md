# R102｜v44正本台帳修復と新型ASRの実原本選定比較（2026-11-18）

## 1.〈本論〉現在の選定と発見した実害

正本`catalog/CURRENT.json`の有効選定は**v44・196登録（170モデル/26データ）、149有効（SELECT53/CONDITIONAL96）**。2026-11-18にmainを調べると、v44[実効選定](../../catalog/effective-portfolio-2026-11-15-v44.json)と[R101全149件readiness](../../catalog/readiness/v44-2026-11-15-r101-all149-gates.json)は正しいが、`CURRENT.json`のキュー・保全準備・Gated台帳の**3参照がv43の148/148/95件を指していた**。これを正すことを、盲目的な新規モデル追加に優先させた。

**修復の内容:** [有効149件の非実行キュー](../../queues/proposed-v44-2026-11-18.json)、[有効149件の保全依存準備](../../catalog/preparation/2026-11-18-insurance-bundles-v44.json)、[CONDITIONAL96件の公開メタデータと権利STOP](../../catalog/access/2026-11-18-v44-conditional-hub-gates.json)を作成し、`CURRENT.json`の参照を原子的に切り替え。前版v43の148/95レコードに`IFM/PAN2`の1件をappendし、**主モデル原本と既存選定全196件の決定を変更しない**。この修復は`v45`という新規選定revisionを増殖させない。v44の過去overlayも改変しない。

新規PAN2はHF[公式モデル](https://huggingface.co/IFM/PAN2)でpublisherが29.202BとApache-2.0メタデータを提示し、[既存R101](101-v44-pan2-original-world-model-selection.md)が35候補ファイル86,082,094,058byte（うち19学習済み重量）を固定。しかし本人の法律上の取得権限、外部Wan VAEとの実物ビット重複、HDDの実空き、PyTorch CUDA再現性、ローカルSHAは**確認していない**。取得承認0のまま。

## 2.〈応用・転用例〉Hugging Face新規ASRの原本審査と保留

調査対象：[Salesforce SOV-Transcribe-1](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1) と[独立学習のDFlash](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1-DFlash)。[固定revision全ファイル・公開SHA台帳](../../catalog/research/2026-11-18-r102-sov-transcribe-original-and-dflash.json)。

| 観測した別学習資産 | 固定40文字revision | 公開元ファイル数／容量 | 判断 |
| --- | --- | ---: | --- |
| ASR原本 SOV-Transcribe-1 | `505d8fae243924c0d8acdc622f7f0abab344eba3` | **37全file 53,317,410,780byte／選択研究34file 53315653534byte** | **正式選定は見送る（研究HOLD）** |
| 追加学習のDFlash助手 | `8c0b3f3a98507d2e3dd35b1bee0f147fa3bded05` | **6file 859412782byte** | 主モデル性能検証が済むまで付随研究。独立したモデルだが推論に必須でない |

Hugging Faceの[原著モデルconfig](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1/blob/505d8fae243924c0d8acdc622f7f0abab344eba3/config.json)ではWhisper-large-v3形式32層音声encoder、Gemma4 Text MoE30層・128 experts/層・top8、FP32 router。 [モデルの公開重みindex](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1/blob/505d8fae243924c0d8acdc622f7f0abab344eba3/model.safetensors.index.json)を直接テキストとして検査した結果、**1,147テンソル名前／16シャード・tensor payload metadata 53,283,115,580byte**、`model.audio_tower`と`model.language_model`の両方が同じ重み群に含まれる。別のWhisper-base weights repo丸ごとは**実行時の必須依存と判断しない**。ただしこれは索引と作者コードの静的読取りで、safetensors binaryのヘッダを開いたわけではなく、その重みの実物ハッシュ再計算もしていない。

[DFlash設定](https://huggingface.co/salesforce-sovereign-intelligence/SOV-Transcribe-1-DFlash/blob/8c0b3f3a98507d2e3dd35b1bee0f147fa3bded05/config.json)は5層・16-token block、target layer [1,6,11,17,22,27]。普通のASR必須重みではなくspeculative decodingを最適化した**別学習成果**。主モデルの4bit量子化コピーではない。いずれもHF現在public/ungated、ライセンスタグApache-2.0だが、モデルrepoはstandalone `LICENSE` を含まないので、Gemma4/Whisper学習系統の権利正文・用途別合法性を**未承認**とする。

**非採用理由:** 既存の`openai/whisper-large-v3-turbo`、`Qwen/Qwen3-ASR-1.7B`、IBM Granite Speech 2Bと470M CTCをSELECTとして保有。SOVは固有の命令型文字起こし・企業名バイアス能力を持つ可能性はあるが、追加**約53.316GB**の質の増分・再取得困難さ・音声処理/encoderの必要性を、同一HW/backend/audio長/batchで独立比較していない。原著[Salesforce公開ベンチ](https://huggingface.co/blog/salesforce-sovereign-intelligence/sov-transcribe-1)は作者値としてのみ扱う。現時点で新規CONDITIONALや重複したDFlashは追加しない。

新規Hugging Faceモデルが存在することと、今すぐ保存承認すべきことは同値ではない。今後(1)希少固有能力 (2)法的権利 (3)完全原本と依存 (4)実HDD余力、の非補償ゲートを経る。

## 3. 規制：実際の法律と将来ストレスシナリオ

- EU欧州委員会の[AI Act GPAI提供者ガイド](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)と[Article 53の公式FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は2026-08-02からGPAI執行が始まることと、条件付きのopen-source一部義務免除を定める。すべての公開重みを保管禁止とする法律ではない。著作権ポリシー・学習データ要約の義務は一部免除でも残る。
- 米国BISは[2026-11-15にリモート経由で高度な計算チップ/サーバへアクセスすることへの暫定規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)を公表。**クラウド計算/半導体輸出管理の事実**と、一般公開モデルweightsをすべて個人がローカルで保管することの禁止は別問題。2025旧Diffusion Ruleの説明文だけで現行法を推定しない。
- HFのアクセス状態(public/Gated/removed)、個別licenseとユーザー本人の権利は**異なる変数**。モデル別公開停止・未来の全面規制には確率をつけない。

## 4. 変数表、次元検査、H/T/D/C/U

| 記号 | 意味（日本語） | 単位（SI準拠） | 定義・範囲・前提条件 | 型 |
| --- | --- | --- | --- | --- |
| N | 管理モデル・データの総件数 | 1 | 196、非負整数 | 整数スカラー |
| A | 現行有効選定件数 | 1 | 149、SELECT53/CONDITIONAL96 | 整数スカラー |
| B_m | SOV新ASRの原本候補source容量 | byte | 53315653534、34publisher files、保存済みでない | 整数スカラー |
| B_d | 任意のDFlash source容量 | byte | 859412782、6publisher files、保存済みでない | 整数スカラー |
| B_c | 正本アーカイブ計画容量上限 | byte | 4,000,000,000,000、実HDD計測値ではない | 整数スカラー |
| F | 保存後の実空き下限 | byte | 200,000,000,000、未測定 | 整数スカラー |
| P | 主モデル公表総パラメータ | 1 | 約26,630,700,000、MoE全expert含むモデル表示 | 整数スカラー |

次元チェック：B_m,B_d,B_c,Fはbyteとして比較可能。Pは無次元パラメータ個数でbyteと単純加算不可。SOV+DFlashの出版社source両方をもし一緒に選ぶと **54175066316byte**だが、これは予約承認でも完全復元容量でもない。

**H:** v44選定と3業務台帳は同一の149/96集合にすべきであり、追加SOVは大容量と既存ASRとの増分性能の未検証により現時点で非採用。  
**T:** 195→196のPAN2差分と149/96の全ID集合を照合。SOV発行元37file/16重みSHA、独立DFlash6file/1SHA、索引1147名前を研究監査。候補比較評価は各選択ASR≥30 paired segmentsが必要で未実施。  
**D:** 台帳全ID一致・保存承認0ならPASS。実機HDD・各モデル完全rights・オフライン復元はUNCERTAIN。未許可の取得/コード実行はFAIL。  
**C:** 新規PAN2の外部依存欠落、SOVが既存ASRを同コストで大きく上回る証拠、親licenseの変化、Tensor indexの仕様変更。  
**U:** 発行元の掲載日時、個人のGated権限、カスタムコードとABI、4TB物理空き、OS/CPU/GPU/SSD staging。誤差分布や反復観測がないため合成u_cと包含係数kは数値化不能。

**ERROR CHECK:** `CURRENT`は引き続き正式v44・196登録／149有効、96 conditional/20 Gated観測/9総数未確定active/取得承認0。v43履歴を変更しない。修復対象は149候補+149依存+96アクセスの正本ポインタとREADME/AGENTSのみでモデル重量は取得しない。

## 5.〈次に考える問い〉

追加SOVの53.316GBを使う価値は、既存のWhisper/Qwen/IBMと比較して**希少な専門語・番号の厳密一致率**が実機でどれだけ改善すればあると判断できるか。
