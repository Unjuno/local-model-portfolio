**R35最新訂正（2026-11-08）**：Chris本家とfrtertaer複製先のモデル・補助重み15ファイルを公開APIのLFS SHA-256＋byteで照合し、全件一致した。R32時点の『一致未確認』は現在の固定revisionでは解決。ただしライセンス・実機ハッシュ・推論品質は未検証。[R35固定ファイル監査](34-r35-ltx-source-vs-mirror-file-identity.md)。

**R33重要訂正（2026-11-07）**：R32が追跡した`TenStrip/LTX2.3-10Eros`のv1 BF16は、Stubeliusが指定する実際の10Eros donorではない。作者`NOTICE.txt`は**10Eros v1.5**を指定。正しい原本は`10Eros_v1.5_bf16.safetensors`（46,139,886,366 byte、SHA-256 `2383d87bc1eea4fc00b73a52eb177bea868c2c46da621511acf9e54b92309f24`、Git commit `99be68b2b6a3f68cde86b3b70e6f71bc26e726fb`）。加えて、[R33台帳](../../catalog/research/2026-11-07-r33-ltx-exact-donor-and-adapter-conversion.json)はOmniNFT元FP32とKijai BF16変換を**同一RL学習状態の異なる表現**として整理。旧v1のハッシュと容量は歴史比較のみとして保持。[R33訂正報告](32-r33-correct-donor-and-adapter-representations.md)が現行判断。

# R32 — LTX 2.5特殊版の元学習成果・権利・公開ハッシュの追跡（2026-11-07）

**結論**：特殊マージは保存候補として残す。量子化を別モデルとして積み上げない。完成済み重みだけでなく**小容量の元RLアダプター**を独立の学習成果として調査する。今回はモデルの保存・実行・取得承認を一切行っていない。[機械可読の6ファイルSHA台帳](../../catalog/research/2026-11-07-r32-ltx-donor-chain.json)。

## 1. ChrisColeTech LTX 2.5 — R31で過小評価した来歴の訂正

[Hugging Face複製先](https://huggingface.co/frtertaer/LTX-2.5-uncensored-v1.1-FP8)には`Duplicated from ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`と表示され、[公開README](https://huggingface.co/frtertaer/LTX-2.5-uncensored-v1.1-FP8/blob/main/README.md)には**5つのマージ元と重み**が書かれている。

| マージ元（配布者の説明） | 相対強度 | 独自の目的 |
|---|---:|---|
| 10Eros NSFW LoRA | 0.70 | 成人向け・スタイル学習 |
| DMD Distilled LoRA | 1.00 | 蒸留済み低ステップ生成 |
| LTX Video IC-LoRA | 0.70 | 参照画像に従う制御 |
| LTX Video IC-LoRA Detailer | 0.45 | 動画からの細部制御 |
| Img2Vid LoRA | 0.45 | 画像→動画の整合性 |

**事実**：配布者のマージ方法が文書で主張されている。複製先のREADMEが取得でき、元のリポジトリはHFメタデータ上`license:unknown`。`base_model:quantized`タグだけで普通の量子化と決められない。

**未確認**：Chris原本と複製先の重み同一性（SHA/Xet）、実際にマージした元リビジョン・再現コード、性能差、許諾の整合。**この不明点が残るため取得を許可しない**。複製先の例示構成は動画重み21.5GB、独自Gemma4 text encoder13.2GB、audio VAE0.365GB、video VAE1.47GB、合計約36.535GB（表示丸めの合計、実ファイル差分や全構成容量ではない）。特に変更済みtext encoderは別学習成果か単なる量子化か確認する。

## 2. Stubelius Remix v1 — 原本と通常量子化の対応が前進

[作者README](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)と[NOTICE](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/NOTICE.txt)は、10Eros・Sulphurのタスクベクトル移植、LTX 2.5蒸留LoRA、OmniNFTのRL-LoRA（rank32／alpha64）という来歴を明示する。

- **BF16 v1（42GB）**：高精度の学習済みマージ状態を残す候補。作者が公開したSHA-256を以下の表へ記録。
- **INT8 ConvRot v1（21.5GB）**：同一v1の実行形式。BF16と独立の学習成果ではない。
- **NVFP4（14.4GB）／GGUF Q4（12.5GB）**：作者がINT8との生成品質比較未完と説明する実験形式。容量のために全形式を保存しない。

作者のbeta2対v1比較は48例、AI評価29勝／9敗／10引分で、第三者独立評価ではない。BF16本体だけで動作せず、Gemma4投影付きencoder・音声VAE・映像VAE・ComfyUIの互換性が必要。フルリポジトリのimmutable commitはまだ未確定。

## 3. 後学習の元ソースを新規発見：OmniNFTの原本LoRA

[論文 arXiv:2605.12480](https://arxiv.org/abs/2605.12480)（DOI:10.48550/arXiv.2605.12480）は音声・動画同時生成における3点、**モダリティ別Advantage routing、層別Gradient surgery、領域別Loss reweighting**を記述。原論文はLTX-2系の作者ベンチであり、StubeliusのLTX2.5統合版の直接の性能証拠ではない。

[OmniNFTの元リポジトリ](https://huggingface.co/zghhui/OmniNFT)には、LTX-2用とLTX-2.3用で**別々に訓練されたアダプター**がある。両ファイルのSHA-256が異なり、各約1.23GB。LTX-2.3用は設定JSON885バイトにrank32とalpha64が明記され、StubeliusのNOTICEと系譜が整合する。**移植により同じ性能が再現されるとの証明ではない**。未決定だが容量効率が高い新しい研究候補にする。

**権利条件の不一致**：Hugging FaceカードはApache-2.0だが、[OmniNFT作者のGitHub master README](https://github.com/zghhui/OmniNFT/blob/master/README.md)末尾は`Research use only`と明記。LoRAの元となるLTX-2/2.3/2.5の権利は別途[LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x)の制約を受ける。同ライセンスの2026-10-29改訂版では、派生重みも明示的な適用対象で、商用企業の利用と非商用研究を区分している。**Apacheラベルだけで商用・再配布可とは判断しない**。

## 4. 6ファイルの公開SHA256・モデル原本を記録

以下はHF/Xetの公開ポインターから読んだ**配布者提示のハッシュ**。実ファイルを取得して再計算したものではない。容量は公開画面の丸め表示であり、最終的な総bytesではない。

| ファイル | 公開配布元 | サイズ表示 | SHA-256（配布元提示） | 保存上の判断 |
|---|---|---:|---|---|
| [ltx2.5-Stubelius_remix_v1_bf16.safetensors](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/ltx2.5-Stubelius_remix_v1_bf16.safetensors) | Stuubs/Stubelius_Remix_Ltx2.5 | 42 GB | `6e0ff9c9d8a1d0747579f1f50d10a9c3822a9a8f265322a5edd476044b0fbf4f` | MERGED_SPECIAL_STATE_MASTER_BF16／CONDITIONAL_PRIMARY_EXACT_SHA_METADATA |
| [ltx2.5-Stubelius_remix_v1_int8_convrot.safetensors](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/ltx2.5-Stubelius_remix_v1_int8_convrot.safetensors) | Stuubs/Stubelius_Remix_Ltx2.5 | 21.5 GB | `ab4f2c731a34550337b14a9e9bdeafb85ef4a4f8b265d7c53503400b1d281fc6` | SAME_STUUBS_V1_COMPRESSED_RUNTIME_REPRESENTATION／ALTERNATIVE_FORMAT_NOT_ANOTHER_SPECIAL_MODEL |
| [LTX-2.3-RL-Lora/adapter_model.safetensors](https://huggingface.co/zghhui/OmniNFT/blob/main/LTX-2.3-RL-Lora/adapter_model.safetensors) | zghhui/OmniNFT | 1.23 GB | `c8e59836f28a6a7d2660f2652a156e77493ba82fb53a1e1e84f258fdf94ac608` | ORIGINAL_RL_LORA_FOR_LTX_2_3／NEW_CONDITIONAL_RESEARCH_SOURCE_CHECKPOINT |
| [LTX-2-RL-Lora/adapter_model.safetensors](https://huggingface.co/zghhui/OmniNFT/blob/main/LTX-2-RL-Lora/adapter_model.safetensors) | zghhui/OmniNFT | 1.23 GB | `61c579f3c1de0dfc8aed1bf34dd92e1f54d4f55bb0abfcb260f19ba95a4fc975` | DIFFERENT_RL_LORA_FOR_LTX_2／CONDITIONAL_OPTIONAL_RESEARCH_DIFFERENT_PARENT |
| [LTX2.3_DMD_hybrid_v2.safetensors](https://huggingface.co/TenStrip/LTX2.3_DMD_Lora/blob/main/LTX2.3_DMD_hybrid_v2.safetensors) | TenStrip/LTX2.3_DMD_Lora | 5.1 GB | `db418249c95eba25ed7d7d24f74a17e7cdc82c03b0ef34a477abdccb1d7a2915` | ORIGINAL_DISTILLATION_DONOR_UNKNOWN_IF_USED／HOLD_WHICH_DMD_VERSION_USED_UNCONFIRMED |
| [10Eros_v1_bf16.safetensors](https://huggingface.co/TenStrip/LTX2.3-10Eros/blob/main/10Eros_v1_bf16.safetensors) | TenStrip/LTX2.3-10Eros | 46.1 GB | `b4b3498eeafa4d52fab5222776e4fe8821787d11fff39de867b919c83e916d35` | FULL_10EROS_LTX23_SOURCE_SNAPSHOT_NOT_SMALL_DELTA／HOLD_DONOR_VERSION_AND_REDUNDANCY_UNCONFIRMED |

**元Donorの過剰取得を防ぐ**：TenStrip DMDにはv1/v2/reshapedの約5.1GBファイルが計3本あり、Chrisがどれを移植したか未確定。10Erosにはv1からv1.5など複数のフルチェックポイントがあり、v1 BF16は約46.1GB。いずれもマージ済み完成物とは異なる学習済み状態になり得るが、元の版が特定できない限り全形式・全世代の取得をしない。

## 5. 次に実行する検証と判定条件

**H**：Chrisの5方向マージとStubeliusのRL・スタイル移植は、同じNSFW動画基盤でも異なる制御機能を持ち、OmniNFTオリジナルLoRAは融合済み42GBから失われる学習来歴を独立して保持する。

**T**：まず元作者の完全40文字HFコミット、全ファイル正確byte、SHA256、NOTICE、元donor版、Gatedアクセス権を確認する。その後、実行許可された同一GPU・クロック・driver・ComfyUI/backend版・量子化方式・CFG・denoise steps・seedで、20の同一プロンプトを各3seedで評価し、映像の動作・参照人物保持・発話と画面の同期・動画/音声の破綻をブラインド比較する。

**D**：形式だけ変わったファイルを別の学習済みモデルと数える場合はFAIL。変更された学習状態と異なる制御性能、依存・権利・実行条件を確認して初めて正式保存候補PASS。現時点は**UNCERTAIN/CONDITIONAL**。

**C**：実はChrisの配布先が通常量子化、旧版のmirrorで重みが違う、LTX2.3用のLoRAがLTX2.5で直接再現不能、量子化で映像の品質が落ちる、Gated/再配布権利が成立しない。

**U**：主要な不確かさは元commit未固定、作者以外の性能評価欠測、実行RAM、ライセンス本文の範囲。実測誤差がないため合成標準不確かさu_cと包含係数kは算出しない。

### 変数表

| 記号 | 意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| N_p | 対応評価プロンプト数 | 1 | 20以上、異なる動画制御入力、整数スカラー |
| N_s | 各プロンプトのseed数 | 1 | 3以上、整数スカラー |
| B_i | 選択ファイルの容量 | byte | ファイル本体＋依存の正確byte、未知はnull、非負整数スカラー |
| R_peak | 実行時ピークRAM | byte | OS/GPU/encoder等込み。未測定、非負実数スカラーまたはnull |

**次元確認**：プロンプト数とseed数は無次元。ディスク容量とピークRAMはともにbyteだが、同じ必要容量とはみなさない。

## 6. ERROR CHECKと学際的転用

- **ERROR CHECK**：6レコードのファイル名が一意、6個の公開SHA256は全て64桁の十六進表記。2件のStubelius形式は同一学習状態、2件のOmniNFT LoRAは別親、DMDと10Erosは元donor候補のまま。正式150資産とNanbeige SELECT、4TB枠、取得キューは変更していない。モデル重みの取得・実行0。
- **関連分野**：機械学習（RL・LoRA転移）、映像/音声信号処理（同期・視覚品質）、デジタル保存（同一学習状態とハッシュ証跡）、ソフトウェア法務/供給網（親モデル・マージ元の利用条件）。

### 〈次に考える問い〉

高精度マージ済みの巨大checkpointと、再学習成果を独立して再利用できる小さな元LoRAでは、どちらを先に保存すべきか。その判断は、**元親モデルへのアクセスを将来維持できるか**でどう変わるか。
