# 37 — 新規の型付きマルチモーダル判断モデルとMOSS必須音声Codec：v27選定（2026-11-07）

## 1. 結論と基準

[CURRENT.json](../../catalog/CURRENT.json) v26の**172資産／有効125件**の全判断履歴を保存したまま、**Kakaoの別途学習済み判断モデル1件**を`conditional`（研究専用、ダウンロード承認不可）に追加する。結果はv27 **173資産／有効126件**。他の2つの新公開`Ripple-65B`の事前学習原本・指示調整版は、独立学習成果と認めるが容量・再現性・実品質評価前の**研究HOLD**とする。先行規制の確率を捏造しない。

既存の`OpenMOSS-Team/MOSS-TTS-v1.5`用24kHz音声コーデック（`OpenMOSS-Team/MOSS-Audio-Tokenizer`）は独立の保全対象モデルとして件数を追加せず、**親の必須外部依存ファイル**として復元容量を再計算する。作者の別48kHzステレオ`MOSS-Audio-Tokenizer-v2`で置き換えない。

[新規候補の固定版容量・ライセンス・ハッシュ（読取専用R30研究）](../../catalog/research/2026-11-07-r30/research.json)／[MOSS source-only重複排除計算](../../catalog/research/2026-11-07-r30/codec-capacity.json)を先行検証した。容量は**配布元のGit/HF metadata整数値**で、利用者の所有物理ディスクの実測ではない。

## 2. 今回採用した独自の学習成果

[開発元Kakao公式発表（2026-11-06）](https://www.kakaocorp.com/page/detail/12193)／[公式HFモデルカード](https://huggingface.co/kakaocorp/kanana-2-v-decide-3b-2611)。

| 項目 | 監査値／評価 |
|---|---|
| 資産 | `kakaocorp/kanana-2-v-decide-3b-2611` |
| 固定配布元revision | `1489062def4145ae3a0a9261fbac4f4d88a8c6d1` |
| 配布元全repo | **7,341,213,499 B** |
| 元のBF16重み | **7,330,945,212 B**／`model.safetensors` |
| 提案する17ファイル一式 | **7,341,102,234 B** |
| serializeした総tensor要素 | **3,665,430,640**（150B未満スクリーニング通過） |
| 現行公開状態 | ungated、Kanana Open License（Apache/MITではない） |
| 推論動作 | 選択肢、はい/いいえ（`noul`）、順序付きスコアの確率分布。テキスト/JSON/画像入力、文字生成とは異なる |
| 今回の正式判断 | `conditional`研究専用、取得承認しない |

**学習成果の非重複性**：`Kanana-2-v-3b`の言語・視覚エンコーダを基盤にした、質問・状態と候補の埋め込み類似度から確率を出す独立した判定学習。既存の汎用生成LLM、GUIアクション、音声生成モデルの量子化では得られない。17ファイルには推論カスタムコード（`configuration_kanana_v_decide.py`, `modeling_kanana_v_decide.py`, `decision_kanana_v_decide.py`, `processing_kanana_v_decide.py`, `image_processing_kanana_v.py`）、Tokenizer、config、LICENSEを含め、デモ画像とサンプルは原本重み一式の必要部品から除外した。

**品質の負の証拠**：社内韓国語評価72.50／公開Decision Index61.34、Vision61.12、公開2指標平均61.23は**Kakao自身の結果**で独立再評価ではない。例えば公開Decision Index単独では比較対象のJoey-1が63.31を報告している。開発元のH200 1枚で平均0.04秒以内という発表は**HWクロック、backend、batch/同一入力条件を固定した第三者測定ではない**。動画非対応、入力最大10画像・20,480 tokens、長文は先頭/末尾を残して短縮、極端な縦横比不可という制限がある。重みサイズはGPUピークRAMの実測ではない。

**利用条件**：[固定版LICENSE](https://huggingface.co/kakaocorp/kanana-2-v-decide-3b-2611/blob/1489062def4145ae3a0a9261fbac4f4d88a8c6d1/LICENSE)（配布元SHA256 `3c13f0cf41c4d49f6d3885bffb27c39431826f9886cacac75349b4ffb58361c4`）にはKananaのResponsible AI方針準拠と、再配布時LICENSE/NOTICE、`Powered by Kanana`表示、派生名称等の義務がある。第三者へのAPI/cloudアクセス再販、システムインテグレーション・オンプレ提供、機器組み込み販売には**別途商用ライセンス**が必要。ライセンスが公表されていることと、利用者の将来の提供形態が合法と確認されたことは違うため、選定キューの`can_enter_approved_queue=false`を維持する。

## 3. 既選定MOSS-TTS v1.5の復元依存に必須Codecを計上

`OpenMOSS-Team/MOSS-TTS-v1.5@cdd3b911b1585e3f2dbc7775ef10f9926f58850a`の固定版`processing_moss_tts.py`は、明示された`codec_path`がない場合`OpenMOSS-Team/MOSS-Audio-Tokenizer`を別途読み込む。したがって本体重みを保全するだけでは完全なオフライン音声生成はできない可能性がある。[ソースコード](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5/raw/cdd3b911b1585e3f2dbc7775ef10f9926f58850a/processing_moss_tts.py)。

固定版Codec `OpenMOSS-Team/MOSS-Audio-Tokenizer@3cd226ba2947efa357ef453bcad111b6eafba782` の必須8ファイルは **7,098,711,111 B**。2つのsafetensors shard、index、config、音声Tokenizer実装、READMEを含む。既存125件と共通SHAがあるか検査し、今回の**新規論理容量増分も7,098,711,111 B**と確認できた。Codec v2の8.49GB重み群はこの親の必須復元依存として算入しない。

*注意*：MOSSのソースrepoはApache-2.0のメタデータ表示だが、保存候補8ファイルに独立のLICENSE原文が同梱されているとは限らない。権利原文、`trust_remote_code`のソース監査、Transformers/Torch/Codec ABI、音声出力の再現性は引き続き未検証。従ってMOSSを「完全復元可能」へ昇格させない。

## 4. 保存容量（B：十進バイト）

| 指標 | v26基準／追加の計算結果 |
|---|---:|
| v26既知SHA-aware論理重複排除容量 | 3,403,245,899,240 B |
| MOSS必須Codecの新たなSHA-aware論理増分 | 7,098,711,111 B |
| Kanana選定17ファイルの追加一次容量 | 7,341,102,234 B |
| **v27新規計算により検証すべき論理総容量** | **3,417,685,712,585 B**（ハッシュ重複がなければこの値） |
| 4TBとの数値差 | 582,314,287,415 B（上記シナリオが一致した場合） |
| 最低物理空き床 | 200,000,000,000 B |
| 完全オフライン復元＋環境込み容量 | **UNKNOWN** |
| 所有者HDD実空き／取得時のピーク実使用量 | **UNKNOWN／UNKNOWN** |

実際のv27は全126件とMOSS依存を同一ハッシュルールで再計算して`catalog/capacity/2026-11-07/v27/capacity-summary.json`へ出力する。**重みファイルサイズとピークRAMは別量**。一時キャッシュ、staging、第三者依存、OS/driver、同一内容のハードリンクの実効可用性は未測定なので、上表の差額を残容量と呼ばない。

## 5. 採用しなかった新規の65B原本・後学習

| 資産 | 固定SHA | 全repo配布元公称 | 決定 |
|---|---|---:|---|
| [Ripple-65B Base Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Base-Preview) | `6187d1108a25fcc31681ec942ec3c581721b9fe1` | 129,569,923,434 B | 研究HOLD |
| [Ripple-65B Instruct Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | `4f872a1ef1376a1962c56bab6d874d017be7eb96` | 129,572,880,240 B | 研究HOLD |

Ricursiveの[公式発表](https://www.ricursive.com/ripple)は65B密結合事前学習12T tokensとagentic coding品質を主張。BaseとInstructは独立の学習段階であり、同一重みの単純形式違いではない。一方、**BF16 instructとそのNVFP4派生は重複形式**として両方を自動採用しない。約129.6GBの各repoを今すぐ追加すると、実ディスク不明・依存が35件残る状況で4TBの物理的保全余地を過剰予約し得る。独立評価、親コードの固定、実RAM測定、重複モデルとの品質比較後に再審査する。独立学習成果だからといって無条件で容量枠を割り当てない。

## 6. 検証計画H/T/D/C/U（多分野）

- **H（反証可能仮説）**：Kananaの型付き判断に既存選定にはない独自学習能力があり、7.341GBの元ソース一式で特定の決定ベンチを再現できる。MOSSのv1 Codec保存候補を加えると親TTSの音声復元欠損が少なくとも1段階解消される。
- **T（最小検証）**：source tree固定SHA、17ファイルのbyte・LICENSE、MOSS Codec8ファイル、索引と全重みSHA、126件のread-only capacity union、履歴保持・承認0をCI検査。後続の本人環境で許諾・CUDA/Python/Transformers版を固定して、可能なら30試行の判断精度・出力再現と実ピークRAMを測る。試験機HW/clock/batch/contextはまだUNKNOWN。
- **D（合否条件）**：条件付き選定PASS＝独立重みと公開版・容量・否定的証拠あり。取得PASS＝利用者の権利・実空き・必要依存・正規ダウンロード承認とオフライン復元が完備。今は**取得UNCERTAIN**。
- **C（破れ方）**：Kanana判定が既存と学習的に同一、商用API再販が許可されない、カスタムPython不互換、音声Codecの正規indexはあるが実際のdecoderとMOSSモデルが不一致、Ripple独自価値が他と大幅重複。
- **U（誤差源）**：配布元byteは固定revisionから再現可能だが、現物ペイロードとownerの空き、実行VM／Python ABIの変動、別licenseや再配布履行は未評価。観測分布がないため標準不確かさ`u_c`と包含係数`k`は算出せずUNKNOWN。

**ERROR CHECK**：ユーザーの永続保全の最上位目的は変えない。法規制発効確率は未推定。MLの訓練成果、デジタルアーカイブの完全復元、ソフトウェア供給網の版固定、権利・法律の四分野から独立検査。モデルウェイト取得・クラウド課金・main更新・approved queue変更を行わない。
