# R66 — v32有効モデルの総数未確定7件：2026-11-15配布元メタデータ再照合

**状態：非実行の一次資料監査。現行v32の選定・総数ゲート・取得承認を変更しない。** 基準：[R64全135件](../../catalog/readiness/v32-2026-11-15-r64-all-active.json)と[現行v32](../../catalog/effective-portfolio-2026-11-14-v32.json)。確認日2026-11-15。Hugging Face接続アプリの`hub_repo_details`による配布元モデルメタデータ（当日照合）。Exaの検索は**クレジット上限(402)**により実施できなかった。したがって新しい論文・法規・削除事例をExaで確認したと主張しない。

## 1. 〈本論〉— 7件の監査結果

| repo ID（一次URL） | 2026-11-15に確認したHubメタデータ | 確定できないこと | 次の安全な検証 | 判定 |
|---|---|---|---|---|
| [ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | GGUF／quantized、親Lightricks/LTX-2.5、license:unknown、更新2026-10-15 | 正確な対象revisionの全tensor、親の全学習済み依存、実際の使用許諾 | 公開config・全checkpointメタデータ・ライセンス正文・親との同一性を静的照合 | **UNCERTAIN・取得準備停止** |
| [Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | GGUF／ComfyUI、親Lightricks/LTX-2.5、license:other、更新2026-11-08 | 独自に学習した差分と単なる形式変換の区別、完全総数・親依存 | 版固定、配布元説明・元checkpoint tensor形状と親との差分 | **UNCERTAIN・取得準備停止** |
| [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts) | **Gated**、CC-BY-NC-4.0タグ、Hub表示**9.6M**、Vocos関連タグ、更新2026-11-03 | Hubの9.6Mが音声復元に必要な全学習済みモデルを含むか、本人のGated許諾 | モデル・Vocos/その他vocoderを個別列挙、正規許諾とライセンス本文を確認 | **UNCERTAIN・取得準備停止** |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | Hub表示**2,502.4M**、Maya3アーキテクチャ、Mimi関連タグ、Apache-2.0タグ、更新2026-11-03 | 2,502.4MにMimiと話者encoderが含まれるか、外部依存の固定版 | 元のMaya重み・Mimi・話者encoderを分離して総数と利用権限を検証 | **UNCERTAIN・取得準備停止** |
| [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3) | Hub表示**35,899.6M**、fish_omni、license:other、更新2026-10-29 | MoE全expertを含む値か、codec・推論に必須な別重み・権利正文 | 公式config・全シャード/codecの静的総数、license原文を照合 | **UNCERTAIN・取得準備停止** |
| [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | LoRA adapter、親Qwen/Qwen-Image-2.1、license:other、更新2026-10-30 | LoRAの独自学習済みtensor数と親・encoder・VAEの総数、使用権限 | LoRAのsafetensorsヘッダと親固定revision、共有親のSHAを比較 | **UNCERTAIN・取得準備停止** |
| [PrunaAI/P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image) | Hub表示**33,123.0M**、diffusers、MiniMax H3由来、license:other、更新2026-11-03 | 33.123Bが全pipeline（text encoder/VAE/prompt-upsampler等）を含むか、地域・使用条件 | モジュールごとの総数、原本15重みと依存、MiniMaxライセンスの適用主体を照合 | **UNCERTAIN・取得準備停止** |

**重要な訂正：** Hubが「Parameters: 35,899.6M」等と表示しても、これだけで**全学習済み依存を含むエンドツーエンドの総数**や、厳密なMoE全expert総数を証明したことにはならない。R64の7件を`PASS`に変更しない。モデル名のB表記や量子化ファイルのbyteを総数に読み替えない。

## 2. 保存可能な状態へ至る優先ゲート

1. **メタデータの一次照合**：上記7件のHub表示・親/ライセンスタグを再確認。**完了したのはこの範囲のみ**。
2. **全tensor総数・依存**：公開済みの固定revisionと`safetensors`のヘッダ等、非実行で確認できる情報から計数。pickleや未監査コードの実行、モデル本体の無許可取得はしない。親モデル、音声codec、encoder、VAEは別依存として権利と容量を検証する。
3. **ライセンスと許諾**：`license:other`・`unknown`・Gatedを利用許可と見なさない。本人の許諾は公開Gitに記録せず、許諾が確認できない場合はSTOP。
4. **固定ファイル/容量/復元性**：全シャード・完全revision・選択byte・ファイルSHAと親の重複排除を確定し、実HDD空き・staging・4TB上限/200GB空き床を検証。実機が見えないため現時点では全件未実施。
5. **実行可能性**：保存とは別にbackend/version、CPU/GPU/VRAM、RAM、量子化zero-point、ABI、KV cache、context、batchと外部ネットワーク自動取得を検査。特にMayaのMimi、SteerのVocos、ACE-Stepの暗黙2B自動取得を防ぐ。

### 変数表

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域/前提 | 型 |
|---|---|---|---|---|---|
| `N` | 対象の総数未確定モデル | 1（個数） | 7 | v32有効135件のうちR64で未確定 | 整数スカラー |
| `P_hub` | Hubに表示された主モデルのパラメータ数 | 1（個数） | 当日表示値。非表示ならnull | モジュール範囲が未確定 | 非負実数スカラー／null |
| `P_full` | 全必要学習済み構成の総数 | 1（個数） | 全expertと必要な別学習済み部品の合計 | 版と依存を固定するまでnull | 非負整数スカラー／null |
| `B_source` | 配布元の選択ファイル容量 | byte | 全選択ファイルのbyte和 | 現時点では未確定、0にしない | 非負整数スカラー／null |
| `B_disk` | 実HDDの使用可能空き | byte | 実機の容量と既存保存物から確認 | 未測定 | 非負整数スカラー／null |

**単位チェック**：`P_hub`と`P_full`は無次元のパラメータ個数であり、`B_source`・`B_disk`はbyte。量子化によってbyteが減ってもパラメータ個数は減らない。MoEのactivated countは`P_full`ではない。

## 3. H / T / D / C / U

- **H**：固定revisionの静的メタデータと一次権利文書を追加確認すれば、7件のうち少なくとも1件の総数・全依存を決定できる。
- **T**：対象7件全数（`n_min=7`）、各repoの全学習済みコンポーネント・親・ライセンス・revisionを固定。未承認の重量ファイル取得と実行を行わない。7件の評価完了または権利上の停止を逐次記録。
- **D**：PASS＝1件以上で完全総数・依存の出典と権利を確定。FAIL＝7件すべてに権利/資料上の確定不能が確認。UNCERTAIN＝一部資料未取得・依存不明（**現状**）。
- **C**：Hub表示値が主モデルだけを示し、外部音声codec等が省かれている。GGUFは別学習成果ではなく量子化形式のみの場合がある。
- **U**：元revisionとHub表示の時間差、構成の省略、MoEの活性/総数、ライセンスの地域差。校正済み誤差分布がないため合成標準不確かさ`u_c`と拡張係数`k`は算定不可。

## 4. ERROR CHECK

- 対象7件すべてをHubで照合し、正式なパラメータゲートは**7件ともUNCHANGED/UNCERTAIN**。
- `catalog/CURRENT.json`、`queues/approved.json`、モデル本体、ローカルHDDは変更していない。
- Exaの検索は402エラー。**この調査はExa成功と記載しない**。
- 本書は135件の選定の完成、ダウンロード可能性、実行復元性を保証しない。

## 5.〈次に考える問い〉

**全学習済み依存の構成が固定され、かつ合法的な再取得可能性が低いモデルを、7件の中からどれだけ実証できるか。** 実証できない限り、希少性だけを根拠に容量を予約しない。
