# R124 / v52｜pi Coding Agent RL-LoRA原本の追加とDaisyRose v51保護

**2026年11月19日、正式選定をv52へ更新：205登録／158有効（SELECT53＋CONDITIONAL105）。** 直前のv51で採用済み[`RadixArk/DaisyRose-27B`](https://huggingface.co/RadixArk/DaisyRose-27B)を含め、旧204件のID・採否を一切変更せず、新しい学習済み[`harness-hub/Qwen3.8-27B-pi-adapted`](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted)1件のみCONDITIONAL/R1追加した。原本7ファイルの[不変Publisher Hash台帳](../../manifests/drafts/r122-v50-pi-adapter-and-nvidia-draft.candidate.json)、[rev overlay](../../catalog/revisions/v52-2026-11-19.json)、[機械可読判断](../../catalog/decisions/2026-11-19-r124-v52-pi-rl-adapter-original.json)。

## 1.〈本論〉モデル中身と保存理由

`pi-adapted`は単なる量子化GGUFやフルマージではなく、Qwen3.8-27Bに端末・コーディング課題をAsyncGRPOで学習した**rank32/alpha64 LoRA**である。publisher revision `80d05c9051dfd2ae464e1daf4329cb15524caf60`、独立重み`adapter_model.safetensors` **637,610,624 byte**、Publisher SHA-256 `869b2a089882c0dac4683993f11081bd70edc30b32c64a988c688d6ac26b792a`。選択元sourceは**7ファイル657,633,248 byte**。親モデル全量を再取得し、別のマージ本体として登録することはしない。

[モデルカード固定版](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted/blob/80d05c9051dfd2ae464e1daf4329cb15524caf60/README.md)の出版社比較では、同一pi harness・thinking OFF、Terminal-Bench2.1 **39.5→55.8%**（86課題）とSWE-bench Pro hard51 **39.2→64.7%**（51課題）。選択checkpoint160が一部の評価課題を見ているため**独立な将来精度・実機速度を保証しない**。

**厳格な復元停止**：`adapter_config.json`の元モデルはQwen3.8-27Bだが`revision=null`。親の訓練時commitは検証できていない。参考用親`Qwen/Qwen3.8-27B@37561816e66b5b9153b1b64c10968c18c1e6f4a0`の`tokenizer.json` SHA-256とAdapter公開tokenizer SHAが違うため、独立ファイルを保存候補にする。配布元のApache-2.0タグだけで適法な用途と他の依存LICENSEを承認しない。

## 2. 採用・交換・保留を区別

| 系統 | 判断 | 理由 |
|---|---|---|
| v51 DaisyRose 27B | **維持** | 同じ親QwenをRLした別の全原本であり、本LoRAと同一SHA・同一後学習ではない。BF16/FP8/NVFP4など量子化は一学習成果の形式 |
| pi coding RL LoRA | **新規CONDITIONAL** | 既存Qwen親を共有して追加0.658GBの独立学習済みcoding政策を保持 |
| [OpenCode LoRA](https://huggingface.co/harness-hub/Qwen3.8-27B-opencode-adapted) | **HOLD** | 別ハーネスのモデルであり、運用者のOpenCode有用性は未実測 |
| [NVIDIA 4B draft](https://huggingface.co/nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft) | **HOLD** | 現有Tencent DSpineと内蔵MTP比較がないまま8.43GB追加しない |
| [NVIDIA 0.8B draft](https://huggingface.co/nvidia/Qwen3.5-0.8B-Qwen3.8-27B-Draft) | **後順位** | 著者の長文受理長3.60で内蔵MTP3.86より小さく実速度も不明 |
| [PhalaCloud Uncensored LoRA](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA) | **HOLD** | 既存Interpretic/0bserverxとの独自性能差が不足 |

## 3. 変数表と次元検査

| 記号 | 意味（日本語） | SI単位 | 定義 | 範囲と前提 | 型 |
|---|---|---|---|---|---|
| `B_a` | LoRA重量原本 | byte（非SI） | 637,610,624 | publisher完全sourceの当該重み | 整数スカラー |
| `B_s` | 7選択source | byte（非SI） | 657,633,248 | 外部親モデルを含まず | 整数スカラー |
| `P_p` | 参考親モデルの総パラメータ数の切上げスクリーン | 1（無次元） | 28,000,000,000 | 出版社約27.7814B、訓練親別版未確認 | 整数スカラー |
| `P_u` | 親＋Adapterの条件付き数の上界 | 1（無次元） | `P_p + 8×B_a` | 別学習済み部品なし・最低1bit/要素と仮定 | 整数スカラー |
| `B_f` | HDD最低残床 | byte（非SI） | 200,000,000,000 | 所有者媒体で独立確認 | 整数スカラー |
| `u_c,k` | 合成不確かさ・包含係数 | 対象測度依存／1 | 未推定 | 独立計測なし | 実数・未設定 |

計算：**28,000,000,000＋8×637,610,624＝33,100,884,992**個。bit/byte換算で学習済み要素の個数に戻すため次元一致。ただし条件付き上界であり正確な重みテンソル数や親版を証明していない。150Bスクリーンと本当の適法取得・復元は別。

## 4. 仮説・検証・権利（H/T/D/C/U）

**H**：同一の正式親とpi harnessで、新規100コーディング課題の成功率を5パーセントポイント以上改善。**T**：最低100 paired課題、固定GPU/clock/driver、PEFT/vLLM/OS・モデル版・quant/zero-point、context/batch1、thinking OFFで盲検評価。**D**：差分5pp以上かつpaired 95%区間下限正と完全権利・SHA・実機復元成立のみPASS。未確認・信頼区間交差はUNCERTAIN。無許可取得/版不一致はFAIL。**C**：チェックポイント選択による上振れ、親SHA違い、ハーネス差。**U**：出版社結果のサンプル偏りと所有者HW/法的状態未確定、独立実測がなく`u_c,k`数値化不可。

制度上の公開モデル規制はストレス仮説であり、米BIS[2026-11-16発表](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は越境計算資源規制で公開weights全般の私的保管禁止ではない。**取得承認0・重量転送0**。正確な訓練親のrev、LICENSE正文と本人許諾、owner HDD空き4TB/200GB・staging/cache、ハッシュ/完全offline復元、実行ABIを満たすまでSTOP。

**ERROR CHECK**：v51の204件維持、v52追加1件→205資産・158有効。157ではなく158に合わせた研究キュー・readinessと106条件付きアクセスを機械整合。既存53モデル取得報告は実物再ハッシュ済みとは呼ばない。今回の実機推論/Pythonテスト未実行。

関連分野：**ML/PEFT、長期アーカイブ・内容アドレス、サプライチェーン/ABI、情報法**。

**〈次に考える問い〉** 親の訓練時版が不明な派生LoRAを先に保存する場合、どの証拠を追加すれば後日のオフライン復元失敗を最も減らせるか。親コミット特定とtokenizer互換検証が先行する。
