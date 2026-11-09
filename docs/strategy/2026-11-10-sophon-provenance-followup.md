# Sophon-Realtime — 2026-11-10 一次資料による保存選定追補（非実行）

**参照コミット**：`c67c9598af3678b2c0b3f6a31f19ad20f62d9c87`（`strategy/2026-11-03-01-risk`）。v27 173件、承認キュー0件は変更しない。ソースコード・Hub公開ツリー・ライセンス表示のみを確認し、重みの取得・インストール・実行は行っていない。

## 1. 〈本論〉優先順位：保存価値と取得可能性を区分

| 候補 | 研究順 | 保存上の独自性 | 推奨 |
|---|---|---|---|
| [`adventists-ai/Sophon-Realtime-32B-Tag`](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-Tag) | P0 | Audio interruption-aware and expressive speech with learned Tag TTS; most feature-complete one-GPU version. Different from current standalone ASR/TTS models. | HOLD |
| [`adventists-ai/Sophon-Realtime-32B-Flash`](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-Flash) | P1 | Same 32B thinker but independently fine-tuned Qwen3-TTS-based streaming talker. Of 40.889GB files, 36.340GB LFS exactly shared with Tag and 0.682GB tokenizer exactly shared with v27 Qwen3 TTS. Not merely quantization. | HOLD |
| [`adventists-ai/Sophon-Realtime-32B-E2E`](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-E2E) | P2 | Separate continuous-vector and E2 decoder mechanism. High unshared source bytes and 2×80GB GPU requirement, preview status. | HOLD |
| [`adventists-ai/DuplexJev-4B-Para`](https://huggingface.co/adventists-ai/DuplexJev-4B-Para) | P1 | 4.2197088B in published safetensors metadata, 8.455528999GB pinned repo; learned speech-turn decisions and paralinguistics. CC BY-NC 4.0, not general commercial successor to Sophon. | HOLD |
| [`adventists-ai/tag-tts`](https://huggingface.co/adventists-ai/tag-tts) | P2 | 7.725543570GB standalone source; 6 same-LFS objects shared with Tag, but llm.pt and flow.pt have DIFFERENT LFS SHA256 from Tag, thus not a byte-identical duplicate. Standalone speech component useful if independent. | HOLD |

**重要**：Tag/Flash/E2Eの正式総パラメータ・本人権利・完全復元ABIは検証されていない。Tagを最優先するのはまず証拠を閉じるためで、取得承認ではない。

## 2. 法的継承の一次資料に不整合

- [DuplexJev開発元README](https://github.com/adventists-ai/duplexjev/blob/b851ea57ba48b351bb9381d6c16d6d10619a9d6b/README.md) は、DuplexJev-32B/4Bの完成モデルを **CC BY-NC 4.0** とし、その理由をESDの研究限定利用や非商用データセットに求める。 [DuplexJev-32B-Paraモデルカード](https://huggingface.co/adventists-ai/DuplexJev-32B-Para) はESD・EARS・Expressoなどを列記。
- [Tag/NOTICE](https://github.com/adventists-ai/sophon-realtime/blob/3585943e8f6ea33ebfc4d077d24b4b59bbde924c/tag/NOTICE) と [Flash/NOTICE](https://github.com/adventists-ai/sophon-realtime/blob/3585943e8f6ea33ebfc4d077d24b4b59bbde924c/flash/NOTICE) はそのDuplexJevから派生したと記載する一方、Sophonは重みとコードを**Apache-2.0**と表示。
- 同一権利者による二重ライセンス、再学習、別途取得した商用データ利用許諾の可能性があるので、現時点で違法・侵害と断定しない。ただし、**第三者に由来する契約制約は開発者の表示変更だけでは消えない可能性がある**。適用関係は法務確認が必要。
- 実行用スナップショットには、Tagは`talker/LICENSE`のみ、E2EはrootのLICENSE/NOTICE無し（Flashは双方あり）。保全時は同じ固定コミットのコード・第三者通知・派生条件も束ねる。

## 3. バックエンド互換性：4%末尾欠落の再発リスク（未実測）

- Sophon Tag/Flashの[install.sh](https://github.com/adventists-ai/sophon-realtime/blob/3585943e8f6ea33ebfc4d077d24b4b59bbde924c/tag/install.sh) は `duplexjev-vllm==0.3.0`、`vllm==0.30.0`、`vllm-omni==0.30.0` を指定。
- 上流[DuplexJev v1.5リリース記録](https://github.com/adventists-ai/duplexjev/blob/b851ea57ba48b351bb9381d6c16d6d10619a9d6b/docs/news.md) は `duplexjev-vllm>=0.4` が `audio_full_length` 対応に必要とし、旧実装では約30秒音声チャンク末尾の約4%を欠いたと説明。
- [DuplexJev v1.5 config](https://huggingface.co/adventists-ai/DuplexJev-32B-Para/raw/757f9df3bf72ffc5b7a708696d47982c39d48d8c/config.json) には `audio_full_length:true`。Sophon `thinker/config.json` は別の `qwen3_vl` 構成で同名のトップレベル設定は確認できなかった。
- **これは差分監査であり、Sophonの実行失敗を証明していない。** 専用のフレーム処理が独立して修正している可能性もある。原実行コマンドの自動起動は禁止。静的なトークン化・フレームレート監査、承認後の30秒試験が必要。

## 4. v27とのハッシュ同一性・容量（10進SIバイト）

| 変数 | 意味（日本語）/定義 | 単位 | 定義域/型 |
|---|---|---|---|
| `B_v27` | v27既知重複排除済source-only容量 | B | 非負整数・スカラー、実機の使用量ではない |
| `B_TF` | Tag+FlashのLFS共有ハッシュを一度だけ数えたsource-onlyバイト | B | 非負整数・スカラー |
| `B_TFE` | Tag+Flash+E2Eの既知同一LFSを重複排除したバイト | B | 非負整数・スカラー |
| `B_Q` | Flashとv27 Qwen3-TTSが共有する音声トークナイザ | B | 非負整数・スカラー、両方のハッシュ一致のみ |
| `B_add` | v27と比較した**確認できた**SHA重複を控除した追加source-only上界 | B | 非負整数・スカラー、他の重複未照合 |
| `F_min` | 取得後最低維持すべき物理空き | B | 200,000,000,000・スカラー |

数値：`B_v27=3,417,685,712,585 B`、`B_TF=49,163,162,386 B`、`B_TFE=128,155,632,702 B`、`B_Q=682,293,092 B`。

`B_add` を `B_TF-B_Q` と定義すると **48,480,869,294 B（約48.48GB）**。3版すべてなら `B_TFE-B_Q` = **127,473,339,610 B（約127.47GB）**。どちらの減算も**B−B=B**で次元は整合する。

- 両版Tag/Flashの **19個・36,339,946,112 B** の共通LFS重みは前回確認済み。
- 今回新しく **`Flash/talker/speech_tokenizer/model.safetensors`（682,293,092 B）** とv27の **`Qwen/Qwen3-TTS-12Hz-1.7B-Base/speech_tokenizer/model.safetensors`** が**LFS payload SHA-256一致**と確認。v27保存済み候補と完全に同一の学習済み部品である。
- まだ他の全v27ファイルとはハッシュ照合していないため、これは保存候補間で確認済みのsource-only上界であり**物理増分の計測値ではない**。
- Tag+Flashの既知部分をv27に加えると **3,466,166,581,879 B**。E2Eも加えると **3,545,159,052,195 B**。完全な依存・作業領域・現地HDDは未測定。4TB/200GB床を満たしたとは判断しない。

## 5. 別学習成果・小型代替の追加確認

- [DuplexJev-4B-Para](https://huggingface.co/adventists-ai/DuplexJev-4B-Para/tree/a0aea2e705b2503695d61629f543d0fc9d30f8a7)：Hugging Faceのsafetensorsメタデータは **4,219,708,800 parameters**、固定snapshotは **8,455,528,999 B/16ファイル**。音声決定・発話終了・抑揚理解の小型フォールバック。ただしTTSを内蔵せず**Sophon自体の代替ではない**。CC BY-NCと音声依存を別途審査。
- [tag-tts独立版](https://huggingface.co/adventists-ai/tag-tts/tree/3a125cba1a24a14e308f410f0d51bea0ba6a03ce)：固定snapshotは **7,725,543,570 B/33ファイル**。Tag内包版とLFS SHA一致は6件計 **3,038,629,775 B**だが、`llm.pt` と `flow.pt` は**別のハッシュ**。従って「同一名だから完全重複」と断定せず、差分の独立学習価値と小型推論の有用性を検査してから採否判断。
- E2Eの古い重みが残るという案内に対し、公開[HFのSophon-Realtime-v1](https://huggingface.co/api/models/adventists-ai/Sophon-Realtime-v1) は固定revision `2e52bd4ade5ab9353a387de0b8930d305b1aff88` で**重みファイル0件**。ModelScopeか過去revisionでの存在は未確認であり、今は削除の事実とはしない。

## 6. 論文・ベンチマークの独立性

- [arXiv:2610.02638](https://arxiv.org/abs/2610.02638) は**DuplexJev**の一次プレプリント（査読採択未確認）。[arXiv:2609.21967](https://arxiv.org/abs/2609.21967) は**NVIDIA NemotronLabs VoiceChat**の論文で、Sophon固有の性能を証明する論文ではない。
- SophonのVoiceBench 82.8 / Big Bench Audio 81.8 / Tag発声F1 / Flash約0.31秒などは開発元の測定。H100 80GBとvLLM-Omni指定・同時アクセス数を固定し、出版社の比較表だけで優位を確定しない。
- 追加試験の標準案：同一音声集合で割り込み終了、相づち誤切断、笑いとため息の実現率、WER・遅延P50/P90、推論RAMピークを両buildで測定。少なくとも30例/条件を独立に計測し、逐次停止・しきい値は採用前に指定する。

## 7. H/T/D/C/U・ERROR CHECK

**H**：Tag/Flashは同一32B brainでも音声生成stageの学習結果が異なり、一般的なTTS/ASRの保存と異なる価値がある。両buildの差が品質/遅延試験とハッシュ差分で確認可能。  
**T**：先に静的にroot license、依存、40桁revision、LFS SHAを確認。実行・データ取得試験は明示承認後のみ。  
**D**：Tag/Flash/Qwenの同一SHA照合はPASS。商用権利・完全依存・実機容量・動作/品質はUNCERTAIN、取得許可はNO。  
**C**：CC BY-NC制約の継承、vLLM音声末尾の切断、GPU/ABI不整合、特定モデルのH100依存、モデルカードベンチ非再現。  
**U**：主要未測定は実機容量・学習済み総数・契約権・ABI・音声品質。統計的合成標準不確かさ `u_c` と包含係数 `k` は測定標本不足により数値化できない。

**ERROR CHECK**：v27=173資産、承認キュー=0、当該4件（Tag/Flash/E2E/4B）は現行v27に存在しない。保存・承認・モデル実行なし。源データSHA検証（Flash声tokenizer一致）成立。別モデルの"同一性"をファイル名だけで推測しない。

## 8.〈次に考える問い〉

CC BY-NCで商用利用が曖昧なモデルを保存する場合、**私的な研究目的での適法性**と将来の**再配布可能性**のどちらをアーカイブ取得の必須条件にすべきか。別軸で記録し、契約確認までHOLDするのが安全。
