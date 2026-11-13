# 2026-11-09：Sophon-Realtime v1 — 3ビルド差分監査・候補選定（非実行）
> 投入元：https://x.com/nahid_pro09/status/2119427620643418296。v27（173件）は非変更。全て `acquisition: false`。ソースモデル本体は取得せずHub APIの公開メタデータのみを読み取った。

## 1. 保存上の判断
**Tag = P0研究候補、Flash = Tagとの学習済み音声生成差分P1研究候補、E2E = 新機構のP1研究HOLD。** モデル総数・第三者権利・ABI・個人の実機容量が未確定のため**v27へ自動昇格しない**。タグ版とフラッシュ版は同じFP8 32B音声対話brainを共有し、実際のTTS stageは別の学習済みパラメータである。単純量子化の重複ではない。

[Tag](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-Tag)、[Flash](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-Flash)、[E2E](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-E2E)、[開発者コード](https://github.com/adventists-ai/sophon-realtime/tree/3585943e8f6ea33ebfc4d077d24b4b59bbde924c)。Xで示された[親repo](https://huggingface.co/adventists-ai/Sophon-Realtime-v1)はシリーズ案内ページであり、実用重みは上記個別repo。

## 2. 公開ファイル検証（固定40桁リビジョン）

| ビルド | 固定revision | ファイル件数 | 公開ファイルの合計（B） | 機能 | ハードウェア |
|---|---|---:|---:|---|---|
| Tag | `20e03f35c2b2c6f45691e1a1108e1e0635ba6f1a` | 68 | 44,614,285,749 | expressive Tag TTS | 1×80GB H100/A100/H800 reference |
| Flash | `8d8d5d8a13ca0120042f1d7ac445e47dba68de7c` | 55 | 40,888,822,749 | lower-latency Flash speech | 1×80GB H100/A100/H800 reference |
| E2E | `7a701a25a8f746aae8cd4cc4f85deec883d4801c` | 37 | 79,003,893,156 | continuous vector E2E | 2×80GB GPUs |

- 同一SHA-256のLFSファイルはTag/Flash間で**19件・36,339,946,112B**。
- TagとFlashの重複排除後source-only上限（非LFS同一blob未控除）= **49,163,162,386B**。別々に保存すると 85,503,108,498B。
- E2EとTag/Flash間で同一SHA256のLFSオブジェクト = 1件／11,422,840B。3つのsource-only合算上限 = **128,155,632,702B**。
- v27の既知3,417,685,712,585Bに仮に3つ全て足すと **3,545,841,345,287B**（追加と重複の仮定、v27既存の物理バイト重複/学習依存は除外）。200GB空き実測がないので適用・承認不可。
- **本体のファイルをダウンロードしていない**。source LFS SHA-256はHub API登録値であり、ローカルハッシュ実測は0件。非LFSのGit blob SHA-1はSHA-256と異なるので区別。

## 3. 総パラメータと法律上の注意

- 開発元は「共通32B brain」と説明。TagはDuplexJev音声理解モデルに、Fun-CosyVoice3由来の訓練済み表現豊かな音声合成を結合。Flashはv27既存選定にもあるQwen3-TTS-1.7B-Baseを出発点に別の音声出力stageを学習。E2Eはtalker+4step decoderを利用。
- **完全な学習済みパラメータ総数は検証できていない**。32Bに外部話者/codec/音声トークナイザや音声ステージの合算が必要。150B基準の最終ゲートはUNKNOWN/HOLD。
- Tag/Flash/E2Eのmodel cardはApache-2.0を掲げる。一方で同じ開発元の中間モデル[DuplexJev-32B-Para](https://huggingface.co/adventists-ai/DuplexJev-32B-Para)のモデルメタデータはCC BY-NC 4.0。**同一権利者は再ライセンスできる可能性があるため直ちに侵害と断定できない**が、権利の連続性・変換履歴・再配布用途は原文とNOTICEで審査する。
- vLLM v0.30/vLLM-Omni v0.30・Python3.12/CUDA、E2Eはdriver>=580。セットアップは取得・インストール・モデル実行を伴うため一切実行しない。
- 開発元自らのVoiceBench 82.8（GPT-4o-mini-Audio 82.8と同値）・他指標は独立比較ではない。VoiceBenchのgpt-4o-mini評価ジャッジ、Big Bench AudioのGPT-4.1評価ジャッジなど再現条件を固定してから主張を受理する。
- 元投稿の「無料・no gate」は公開HF APIメタデータと整合するが「契約適法・全依存再現・使い物になること」は別。

## 4. 品質/重複の反証条件

H: Tag/Flashは共通推論中枢を使っても、音声生成の独立学習結果がある。E2Eは音声対話の別機構として残存価値がある。
T: 公開Hubの固定revision、全ファイルのLFS SHA256で同一性を見る。取得後のローカル試験は別途承認されてから。
D: 重複ファイルのhash一致はPASS。独立した音声品質差・実機高速性はUNKNOWN。本人許諾未確認で取得許可FAIL。
C: 作者のBENCHが他所で再現不能、speech stageが同一ハッシュ、OSS契約と中間モデルの条項が両立しない、必要runtime depsが閉じないときはHOLDに据え置く。
U: 最大誤差源＝開発元ベンチの非独立性、稼働環境、互換ABI、モデルと第三者コード条項。計測分布が無く標準合成不確かさ/u_cや包含係数kの数値化は不可。

**最短の次工程**：LICENSE/NOTICEとCC BY-NC中間モデルの権利源を確認 → 全checkpoint学習済みパラメータのテンソル総数確定 → 想定保存ファイルだけのハッシュ表固定 → 物理ディスク空き容量確認 → 改訂版（v28以降）への条件付き採否判断。データ移送/アプリ実行は別承認まで停止。

## ERROR CHECK
3種類の公開スコープ、commit40文字、ファイル件数68/55/37、Tag/Flash共有LFS 19件とSHA256一致byteを検査済み。個人の権限、実容量、実行、独立の品質試験は検証していない。
