# SteerTTS 原本・Edge/Nano分岐と権利整合性監査（2026-11-15）

調査開始時点の正本は `v37-20261115`、登録191／有効144。**正式選定の入れ替え0、新規採用0、取得承認0**。既存の `WhissleAI/steer-tts` は **CONDITIONAL研究維持・最終取得ロックSTOP**。派生Edge/Nanoは現状**研究HOLD（正本に追加しない）**。将来の重み配布規制は仮説であり、権利条件の観測とは区別する。

## 1. 確認された一次ソースと権利衝突

- Hugging Face [SteerTTS作者カード](https://huggingface.co/WhissleAI/steer-tts)は **重みCC BY-NC 4.0／付属コードMIT**と説明。Hubのメタデータでは`WhissleAI/steer-tts`、[edge](https://huggingface.co/WhissleAI/steer-tts-edge)、[nano](https://huggingface.co/WhissleAI/steer-tts-nano)の3repoとも**Gated**。この観測は本人の許諾取得を意味しない。
- 配布元のGitHub [commit固定LICENSE](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/LICENSE)と[同版pyproject](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/pyproject.toml)は**コード・重み・音声ともCC BY-NC 4.0およびWhissle独自条件**。GitHubのライセンス本文blob `ed3a683cabd0a740cc2ae5e21896946caccdae1a`、README blob `a23107815cdf5bb6a54929d68e4ded82084ba27f`。第三者依存には別ライセンスが残る。
- このGitHub条件は[最初に検証できる2026-10-31付commit](https://github.com/WhissleAI/steer-tts/blob/989b6ce6006f/LICENSE)でもCC BY-NC 4.0であった。**MITから最近変更された、とは断定しない**。別ホスト文言の衝突であり、同一HF revisionの`LICENSE.md`本文と発行元の確認が必要。安全側では「MITコードとして取得・再配布可能」とみなさない。
- コード固定commit `5008f8e032f69266c3f37788825cfda3112eab55`、対応Python依存の例は`torch>=2.4,<2.12`、`safetensors==0.8.0`、`transformers==5.19.0`（任意）。インストール・任意コード実行・モデル取得は実施していない。モデル重みのrevision/ローカルSHAは未確認。

## 2. 実学習状態・重複の判定

| repo | 配布元の具体的機構 | 現行判断 |
|---|---|---|
| [SteerTTS原本](https://huggingface.co/WhissleAI/steer-tts) | 12種類の数値音声制御、2,825声、独立refiner・cloning flow・外部話者/テキストencoder | 既存CONDITIONAL維持、本人Gated権利と全依存未確認 |
| [SteerTTS Edge](https://huggingface.co/WhissleAI/steer-tts-edge) | 作者[固定models文書](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/docs/models.md)はv2学習済みacousticを搭載し、約9.25M acoustic・約6.2M vocoderをint4化、200声。HFには`base_model:quantized`タグもある | **追加保留**。新学習成果か単なる表現違いか、同じ版のテンソル・重みSHAで決める。派生ONNX/PyTorch/Cを別々にカウントしない |
| [SteerTTS Nano](https://huggingface.co/WhissleAI/steer-tts-nano) | ESP32-S3向け2声・int8、著者は約2.97MB重み＋1.8MB前処理と122KB動作RAMを報告。HFは`base_model:finetune` | **追加保留**。学習済み差分とマイコン動作の必然性を未証明のまま別資産にしない |

原本に対して作者カードが明示する学習済み構成要素は、約9.59M acoustic、13.53M Vocos、17.64M refiner、24.67M cloning flow、101M WavLM、22.7M MiniLM、0.5M prompt adapter。これらを単純加算した**約189.63Mは構成要素名の概算**であり、パイプラインの完全な総パラメータ確定値ではない。両flowは推論経路によって代替使用され、声埋め込み2,825×512要素やG2P由来の学習済み前処理を完全に照合していない。したがって既存`UNVERIFIED_BLOCK_FINAL_LOCK`は維持する。

作者の[同一ソース測定](https://github.com/WhissleAI/steer-tts/blob/5008f8e032f69266c3f37788825cfda3112eab55/docs/models.md)ではEdge2.0のSeed-TTS-eval 1,088文WER=0.93%、CV3-Eval 500文WER=2.44%、音質指標UTMOSはそれぞれ4.17/4.15。ただし独立測定ではない。著者ベンチのThreadripper 2970WX・1スレッド・20文でEdgeのnative peak RSS 98MB、Python ONNX 127MB、PyTorch 369MB。測定時ホスト高負荷かつ反復約2–3回で、ユーザーのHW・クロック・batch/ABI再現と精度の信頼区間は未確認。**エッジ版は低容量ゆえ新規採用する、という判断をしない**。

## 3. 制度的な制約と予測を分離

[欧州委員会のGPAIガイドライン](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)は提供者義務の2025-08-02適用と2026-08-02の執行開始を説明。オープンソース義務免除には条件がある。[欧州委員会のAI Act執行説明](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act)は、非同意の親密画像等に関する新たな禁止規定の適用日を2026-12-02とする。これは**対象となる行為・システムに関する法規制**であり、SteerTTSや一般ウェイトの保存禁止を意味しない。S1→S2→S3波及は検証対象仮説のままとする。

## 4. 変数表・検算・反証可能条件

| 変数 | 日本語の意味 | 単位（SI準拠） | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| `P_i` | 作者が公表した各学習済み構成要素の概算パラメータ数 | 1（個） | 非負、M=10⁶個、7要素。各値は概数 | 実数スカラー |
| `P_s` | 7要素概算の加算結果 | 1（個） | 約189.63×10⁶、G2P/声ベクトル等は別、完全pipeline総数ではない | 実数スカラー |
| `V` | 内蔵声の個数 | 1（声） | 2,825 | 整数スカラー |
| `d` | 1声あたりベクトル要素数 | 1（個/声） | 512、作者カードの記載 | 整数スカラー |
| `B` | Edge配布元による装置上の重み等の参考量 | byte | 約12.6×10⁶、同版実バイト未固定 | 非負実数スカラー |
| `R` | Raspberry Pi等実機推論時のメモリ | byte | 実環境未測定、作者値のみ | 非負実数スカラー |

数値例：7要素の約9.59＋13.53＋17.64＋24.67＋101＋22.7＋0.5＝**189.63M個**。声ベクトルは2,825声×512個/声＝**1,446,400要素**。次元確認：個/声×声＝個、モデル要素数とバイト数を直接加算しない。著者の数値は丸められているので厳密な総パラメータ証明ではない。

**H**：原本は制御可能な音声合成学習成果で独自性があるが、派生Edge/Nanoの完全別採用とコードMIT扱いは現状検証不足。  
**T**：n_min=3の公式モデルページ、固定GitHubコード/ライセンス/アーキテクチャを照合。正式昇格には異なる2 checkpointの固定revision・同一テンソル比較、権利、必要依存、ベンチ同一HW/OS/backend/context/batchで各30回以上の反復、物理容量を要求。  
**D**：GitHub作者コードのCC BY-NCとHFカードMITの記載不整合はPASS（観測済み）。法的優先順位・全モデル原本SHA・パラメータ・本人権利・独立品質はUNCERTAIN。無許可の取得・実行はFAIL/STOP。  
**C**：HFの実`LICENSE.md`が特定版のMIT付属コードを区別している、Edge2は独立v2訓練で重み変換では再現できない、Nanoの特化fine-tuneが独自ハードウェア能力を作る場合は判定を再検討。  
**U**：現在のHFページ表示と固定revisionの差、配布先別の契約・著作権、外部encoder/runtime、測定温度/負荷に不確かさが残る。分布・反復不足につき合成標準不確かさ`u_c`と包含係数`k`は算定しない。

**ERROR CHECK**：3repo区別／既存SteerTTS conditional維持／Edge/Nanoは研究HOLD／全取得承認0／重みDL0／任意コード実行0／コード最初期からNC確認／将来禁止確率の捏造なし。機械可読[監査JSON](../../catalog/research/2026-11-15-steertts-3build-source-license-risks.json)。

関連分野：音声機械学習、組込みシステム、知的財産・ライセンス、デジタルアーカイブ、サプライチェーンセキュリティ。

## 5.〈次に考える問い〉

**限られた保存容量で優先するのは、ライセンス条件の固まらない追加派生モデルか、それとも権利と必要依存が明確な異なる学習済み原本か。**
