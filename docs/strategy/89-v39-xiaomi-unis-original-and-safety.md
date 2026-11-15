# R89：v39 Xiaomi U0-4B 世界モデル原本の正式研究選定、18ファイル固定（2026-11-15）

## 1.〈本論〉選定結果と目的

将来の公開停止・Gated化・ライセンス変更があっても、実際に学習された異なる能力とその必須依存を**適法かつオフライン復元可能に保存すること**が目的。2026-11-15の正本v38 **193資産・有効146**から、[XiaomiRobotics/Xiaomi-Robotics-U0-4B](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B)を条件付き研究選定に**1件追加**し、v39 **194資産（168モデル／26データ）・有効147（SELECT53／CONDITIONAL94）**へ更新。旧193件の選定は無変更。取得・実行・承認0。

**学習目的：** ロボット複数視点の`Scene Gen`と、物理状態・ロボット姿勢を維持する`Transfer`を学習したUNISの離散視覚トークン自己回帰。既存のWan／Cosmos／Praxisとは原本重みや出力目的が異なるため追加価値はあるが、**性能優位は独立未測定**。[公式技術報告](https://arxiv.org/abs/2607.11643)の38B主モデルの結果を4Bの結果へ外挿しない。

## 2.〈応用・転用例〉学習済み原本・必須部品の固定

| 選定内容 | 固定配布元revision | 原本選択ファイル | 出典と重要事項 |
| --- | --- | ---: | --- |
| Xiaomi 4B原本 | `c1a4e9c9c3cf52dd3617d3c9c974e16e6e88b3cd` | **12ファイル・10,170,001,048 byte** | [公式API](https://huggingface.co/api/models/XiaomiRobotics/Xiaomi-Robotics-U0-4B/revision/c1a4e9c9c3cf52dd3617d3c9c974e16e6e88b3cd?blobs=true)、本体BF16重み2本、5,336,406,336＋4,827,825,824 byte。LFS SHA256を両方固定。見本PNGは除外 |
| 必須VisionTokenizer | `a5c45bdb8084763048e094ae124778bfeca7d5ee` | **6ファイル・1,821,439,140 byte** | [BAAI公式API](https://huggingface.co/api/models/BAAI/Emu3.5-VisionTokenizer/revision/a5c45bdb8084763048e094ae124778bfeca7d5ee?blobs=true)。1,821,405,084byteの`model.safetensors`を選定。別ポートフォリオモデルとしてカウントしない |
| 合計 | 2固定repo | **18ファイル・11,991,440,188 byte** | [全ファイルSHA／bytes監査JSON](../../catalog/research/2026-11-15-r89-xiaomi-u0-4b-immutable-selected-source.json)、モデル実体は未取得 |

新規研究枠は**16,000,000,000 byte**。公式repo全量、VQの`model.ckpt`別形式、`config.yaml`、主モデルの見本PNGを無理由に保管しない。作者[固定コード](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/tree/e722003980958f242203af265718ee980b834deb)はPython3.10のAR eagerで4Bを指定する経路。**重大な互換性注意：** [VQ loader](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/blob/e722003980958f242203af265718ee980b834deb/inference/xr_u0_ar/vision_tokenizer/__init__.py)には`config.yaml+model.ckpt`が揃うと`torch.load`する経路と、なければ`AutoModel.from_pretrained(...trust_remote_code=True)`へ進む分岐がある。今回のSafetensors選択は後者を意図したが**安全かつ完全に復元可能かは未検証**。ネットワーク自動取得、任意コード、ABIも確定前に実行しない。

### 保存しない同族

[Xiaomi-U0-4B-Sequence](https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-U0-4B-Sequence)は別チェックポイントで、2重みSHAは原本4Bと異なる。**単純量子化複製ではない**。しかし`interleave_video/subtask`に追加10.16GBを投じる独立利点は未検証のため今回は非採用。34Bと38B FlashARも同様にサイズ・作者ベンチマークだけでは追加しない。

### 規制事実と仮説

**現状の観測:** 公開元APIでU0-4BとVQとも`private:false, gated:false`、Apache-2.0モデルカードタグ。重みrepoには独立`LICENSE`本文がなく、[作者GitHubコードのLICENSE](https://github.com/XiaomiRobotics/Xiaomi-Robotics-U0/blob/e722003980958f242203af265718ee980b834deb/LICENSE)と重み・外部VQの別権利を**未承認**のまま扱う。

**規制の事実:** EUの[AI Act執行](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start)が2026-08-02に始まったが、[オープンソースの一部義務免除](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)がある。米国の2025 AI Diffusion Ruleは特定のclosed weightモデル制御に関するもので、[GAO 2026判断](https://www.gao.gov/products/b-337935)は不執行・形式的な効力を区別。**公開モデルの全面禁止は確認した事実ではない**。将来のホスティング廃止・規制拡張は未確率化の仮説。今回モデル固有の公開停止予定は未確認。

## 3. 変数表・検証

| 記号 | 日本語の意味 | 単位(SI準拠) | 定義／範囲／前提 | 型 |
| --- | --- | --- | --- | --- |
| N | 管理資産数 | 1 | 194、非負整数 | 整数スカラー |
| A | 選定有効数 | 1 | 147、0以上N以下 | 整数スカラー |
| B_m | U0原本の参照選択量 | byte | 10,170,001,048、12出版社ファイル | 整数スカラー |
| B_v | 必須VQの参照選択量 | byte | 1,821,439,140、6出版社ファイル | 整数スカラー |
| B | 参照候補量 | byte | B_m+B_v=11,991,440,188 | 整数スカラー |
| C | HDD計画上限 | byte | 4,000,000,000,000、実容量ではない | 整数スカラー |
| F | 実空き下限 | byte | 200,000,000,000、未実測 | 整数スカラー |
| P_m | 主モデル公開パラメータ | 1 | 約5,082,100,000、Hub概数 | 整数スカラー |
| P_v | VQパラメータ | 1 | 約455,300,000、Hub概数 | 整数スカラー |

次元チェック：B_mとB_vはbyte同士で加算可能。モデル要素数P_m/P_v（無次元）と保存byte、VRAM、HDD空きは別測度。

**H** 新規原本は既存から重み一致で復元不能な多視点ロボット編集の別学習成果。**T** 固定APIの原本2repo・全18ファイルについてモデルID/sha/bytesを全数照合（n_min=18）、他のfamily重みSHA相違を再照合。**D** 原本source固定と重複防止はPASS、取得権利/外部VQ安全実行/オフライン復元/容量はUNCERTAIN、無承認取得はFAIL/STOP。**C** 権利・VQ loaderの危険や既存モデルの代替性能が反証。**U** 主要未確定は実体SHA・パッケージABI・本人HDD・Gatedでない場合の合法性。実測誤差分布がないためu_cと包含係数kは算定不能。

**ERROR CHECK:** v38の193件と採否を保存し+1、v39は194件／有効147、168モデル/26データ、Gated20、未確定全パラメータ有効9、承認・モデル重量DL・復元0。約11.991GBは出版社参照ファイル和、完全復元容量ではない。

〈次に考える問い〉: 多視点ロボット状態の保持誤差を同じ入力/HW・30反復で比較した場合、U0原本と現在のCosmos/Praxisは代替可能か。
