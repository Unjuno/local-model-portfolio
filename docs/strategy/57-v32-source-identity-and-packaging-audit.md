# R57 — v32原本3件の固定ファイル・重複・権利監査（2026-11-14）

**mainの現行v32（182資産・有効135件）は維持**。通常の追加発見を繰り返す代わりに、前回採用した3件の源ファイル全リストのうち必要な部分を、公開元の完全40文字コミット・正確なbyte・主重みSHA256に固定。

[機械可読監査](../../catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json)／[取得未承認の固定ソース部分](../../manifests/drafts/r57-v32-three-source-scopes.candidate.json)。すべて読み取り専用の研究成果。**承認済みロック、完全オフライン復元、取得済みモデルではない**。

| リポジトリ | 不変リビジョン | ファイル参照 | 公開元選択部分（十進byte） | 候補パッケージ |
| --- | --- | ---: | ---: | --- |
| [Tencent DSpine](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | `5f54174d301dbca65d9aa4448dc47e56732d9a12` | 5 | **4,051,857,976** | 5ファイル全件。親Qwenは別の既存SELECTを参照 |
| [Nemotron 3 Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization) | `52a432672732425e4c19765b9fec9b5810e6f4ba` | 11 | **397,030,277** | F32 Safetensors・config・processor・権利/評価/プライバシー説明。NeMo nativeとGGUFは独立価値未確認 |
| [RFD4-Proteína](https://huggingface.co/nvidia/RFD4-Proteina) | `a06e2509c7033b010fc43614e9fd840303588502` | 7 | **1,742,698,063** | 統合済み2026-10-19 Flow+AE重みと設定・LICENSE・来歴。全repoや学習データを取らない |
| **合計（3資産の部分のみ）** | — | **23** | **6,191,586,316** | 外部依存・staging・実機空き未算入 |

## 同一性と重複の修正

- **Qwen3.8-27B**は既存SELECT。2026年10月30日版`1d4bf0f2...`と11月7日版`37561816...`の重み18シャード＋tokenizer.jsonが、**全19ファイルで公開元SHA256と正確なbyteとも一致**。DSpineのために元重みを再取得する意味はない。ただしドラフターと親の実際の受理率・backend互換は未実測。[元Qwen](https://huggingface.co/Qwen/Qwen3.8-27B)／[Tencent実装固定版](https://github.com/Tencent/DSpine/tree/d211869ac168b756e197f7607ff37cd342b50fb2)
- **RFD4**はv32に記録されていた`cf31b935...`、実行サンプルの参照コミット`a06e2509...`、公開元の11月照会時`621b785a...`が異なる。**主重みとconfigは同一ハッシュ・byteだが、README、provenance、inference.yamlは異なる**。同じ重みを版ごとに多重保存せず、今回は実行設定が参照した`a06e...`を固定。ソフトウェアの別GitHubソース`RosettaCommons/RFD4-Proteina`、ソースコミット`834392d06fd78883edb2b4ef358abdbbc39f3dd6`は固定したが未実行。
- **PAN2**の最新固定版`82f54c6...`は全repo **86,173,925,584 byte**、14 Transformer shardと4 text encoder shard、VAE **2,818,777,808 byte**。公開SHA`62cd18f...`はR40のWan Animate/LongCat共有VAE`d6e524b...`と異なるので重複排除しない。Wan・Qwen依存と権利を調査してから採否再評価。
- **MiniMax H3 Image**の最新固定版`5f904730...`はrepo **203,981,781,880 byte**。複数重み形式を全取得しない。独自地域条件付き[正式LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image/blob/5f90473023975e6271b0ed1dd84c4e88e4bbc6d3/LICENSE)、text encoderとPruna版との比較を待つ。HOLDを維持。

## 残る停止条件

1. **権利**：DSpineは[Apache-2.0原LICENSE](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16/blob/5f54174d301dbca65d9aa4448dc47e56732d9a12/LICENSE)。Nemotronは[OpenMDW-1.1正式全文](https://openmdw.ai/license/)（別名のNVIDIA Open Model Agreementとは異なる）。RFD4は[BSD-3-Clause原LICENSE](https://huggingface.co/nvidia/RFD4-Proteina/blob/a06e2509c7033b010fc43614e9fd840303588502/LICENSE)。ラベルと本人の利用目的への適用は別検証。
2. **ABI**：Tencent DSpineはSGLang0.5.22/FlashAttention3/ReplaySSM、NemotronはNeMoまたはTransformers（F32対native形式の同等性未試験）、RFD4はPython3.12/CUDA12/13等。CPU/GPU/clock、backend/commit、batch、context、quant/zero-point、KVなどの前提を固定してから速度・品質を評価。
3. **完全依存**：モデルの源主重みSHAは公式Xet/LFSデータ。**モデル本体は未ダウンロード**。非LFS小ファイルのSHA256をGit blob SHA1から捏造せず、固定コミットとbyteだけ記録。外部コード・学習済み依存・ライセンス・実HDDの空き200GBとユーザーの最終ロック承認は未完了。

## 検証 H/T/D/C/U

- **H**：既存Qwenのtrained state同一性と、RFD4の主重み再版同一性は公開元のSHA一致で検証できる。
- **T**：3 repoの23ソースファイル部分、Qwenの18シャード＋Tokenizer計19公開元ファイル、RFD4の2固定版主重み・config・metadataを静的に比較。モデル本体/コード実行ゼロ。
- **D**：PASSは今回の公開元ファイルID・SHA256・byte、及び重複を許可せず正本v32を維持したこと。FAILは公開元SHAが衝突/不一致、承認キューの無許可変更、異なる学習済み状態の不適切な削減。権利・実機・完全依存・ローカルSHAはUNCERTAIN。
- **C**：公表ファイルの取り下げ、相違するNeMoネイティブ状態、異なるコード版のABI不整合、RFD4のモデルとAE不適合、各権利の適用範囲の不一致。
- **U**：配布元公開メタデータを信頼した静的評価。ローカルハッシュ・実HW測定・法的確認と誤差収支がないため合成標準不確かさ`u_c`と包含係数`k`の数値は未定義。

| 記号 | 意味（日本語） | SI単位 | 定義／定義域・前提 | 型 |
| --- | --- | --- | --- | --- |
| B | 取得候補の源ソース部分サイズ | byte | 3固定rev内の23ファイルのsize合計、非負整数。外部依存は含まない | スカラー |
| C | 保存上限 | byte | 4,000,000,000,000。ユーザー実HDD計測ではない | スカラー |
| F | 保存後最低空き | byte | 200,000,000,000。既存ファイル/staging別 | スカラー |
| N | 対象ファイル参照数 | 1 | 23。重複ハッシュ不明のテキストは統合しない | 整数スカラー |

**単位チェック**：B/C/Fはいずれもbyte、Nは無次元。異なる単位の加算はしない。

**ERROR CHECK**：v32の182資産・有効135件、3特殊モデルの既存CONDITIONAL判定を不変更。外部親は容量再加算せず、通常の量子化違いを選定増分としない。取得承認0・実機操作0・モデル実行0・ブランチmainのみ。

**次に考える問い**：この3モデルのどの依存を正確に固定すれば、余計なファイル形式を増やさず実際のオフライン再現性まで検証できるか。
