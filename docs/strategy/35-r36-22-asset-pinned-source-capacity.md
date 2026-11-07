# R36｜容量不明だった22資産を固定コミット・実ファイル単位で監査（2026-11-08）

**結論：v19で全repo容量不明だった有効資産22件を追跡し、21モデルrepoの完全ファイルツリーと容量を固定リビジョンで確認した。** 残るFineWeb-Eduは巨大なデータセット全体を無理に集計せず、固定版の`sample/10BT`14 Parquet＝**28,518,193,415 bytes**に保存対象を限定する研究案とした。これらは正規配布元のメタデータによる調査であり、実際のユーザーHDDの容量、モデル実行、内容の再ハッシュ、ダウンロード承認とは別。[機械可読の22件台帳](../../catalog/research/2026-11-08-r36-22-asset-source-closure.json)。

## 1. 22件の再調査結果

| モデル・データセット／固定版へのリンク | 現行選定 | 全repo公開ファイル容量 | 選択ファイル構成の研究例 | 残る取得条件 |
|---|---|---:|---:|---|
| [`0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/tree/ab8d7bd81d03117501e4da60cccdff4c80f0eea0) | CONDITIONAL | 1645.27 GB | 17.18 GB | 依存・権利未完 |
| [`Lightricks/LTX-2.5`](https://huggingface.co/Lightricks/LTX-2.5/tree/49b093a39c19169a8a81721dcc541e07e945232f) | CONDITIONAL | 200.85 GB | 38.69 GB | Gated：検討構成のみ |
| [`Stuubs/Stubelius_Remix_Ltx2.5`](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/tree/829cf2f7cbdf79872ff365787ba50f80006efe76) | CONDITIONAL | 195.94 GB | 42.01 GB | 依存・権利未完 |
| [`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8/tree/592aaa11f13a7e480169455aa885f58c42d89766) | CONDITIONAL | 166.92 GB | 36.47 GB | 依存・権利未完 |
| [`Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2`](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2/tree/6af1278a92223c717ccea671e4571a5cc135f5d8) | CONDITIONAL | 53.12 GB | 53.09 GB | 依存・権利未完 |
| [`kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers`](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers/tree/4c487e8b4aeeb9059e5a77905aa2ddb59ec28f81) | CONDITIONAL | 26.68 GB | 26.64 GB | 依存・権利未完 |
| [`InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF`](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF/tree/f1a9272aaee6178ff598e3d025dd6709800db968) | CONDITIONAL | 17.74 GB | 17.74 GB | 依存・権利未完 |
| [`OpenMOSS-Team/MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5/tree/cdd3b911b1585e3f2dbc7775ef10f9926f58850a) | SELECT | 17.00 GB | 16.98 GB | 依存・権利未完 |
| [`ResembleAI/chatterbox`](https://huggingface.co/ResembleAI/chatterbox/tree/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18) | SELECT | 13.87 GB | 未選定 | 選択保留 |
| [`LiquidAI/LFM2.5-VL-3B`](https://huggingface.co/LiquidAI/LFM2.5-VL-3B/tree/35a118d938ce6d123ac2d371649f24a8efb69058) | CONDITIONAL | 6.27 GB | 6.25 GB | 依存・権利未完 |
| [`boltz-community/boltz-2`](https://huggingface.co/boltz-community/boltz-2/tree/6fdef46d763fee7fbb83ca5501ccceff43b85607) | CONDITIONAL | 6.20 GB | 6.20 GB | 依存・権利未完 |
| [`Qwen/Qwen3-TTS-12Hz-1.7B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base/tree/fd4b254389122332181a7c3db7f27e918eec64e3) | SELECT | 4.54 GB | 4.54 GB | 依存・権利未完 |
| [`LiquidAI/LFM3-1.7B`](https://huggingface.co/LiquidAI/LFM3-1.7B/tree/0dc4268b561499c648c7ba7c9466bf3d8d01517a) | CONDITIONAL | 3.48 GB | 3.46 GB | 依存・権利未完 |
| [`Edge0/Audio8-TTS-Realistic-Air`](https://huggingface.co/Edge0/Audio8-TTS-Realistic-Air/tree/23c305cc013fde378edb459f538317043c993a74) | CONDITIONAL | 2.57 GB | 2.55 GB | 依存・権利未完 |
| [`IFM/K2-Horizon-0.9B`](https://huggingface.co/IFM/K2-Horizon-0.9B/tree/c4f92a0d66e2ec6685ed9fff4f6c33e2a217f23b) | CONDITIONAL | 2.16 GB | 2.16 GB | 依存・権利未完 |
| [`KlingTeam/LivePortrait`](https://huggingface.co/KlingTeam/LivePortrait/tree/82a4fa6735ca58432b6ce39301b4b9ee066dea47) | SELECT | 2.14 GB | 0.66 GB | 依存・権利未完 |
| [`usezn/Galvanize-3`](https://huggingface.co/usezn/Galvanize-3/tree/597237be3b0fabbf5d70ff16ce95fad14a591f20) | SELECT | 1.16 GB | 0.56 GB | 依存・権利未完 |
| [`chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1`](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1/tree/aa213272180d6ad0d03f5fb3d597f0f0322647c5) | CONDITIONAL | 0.67 GB | 0.67 GB | 依存・権利未完 |
| [`LiquidAI/LFM2.5-VL-3B-DSpark`](https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark/tree/af77e9306a26e8625fde74d2a3051ab6d21bd955) | CONDITIONAL | 0.56 GB | 0.56 GB | 依存・権利未完 |
| [`udgamlabs/Lilavati`](https://huggingface.co/udgamlabs/Lilavati/tree/59004a9b6f75bc39e78790d7aca6b1adb6e4b7ac) | CONDITIONAL | 0.19 GB | 0.19 GB | 依存・権利未完 |
| [`udgamlabs/Lilavati-Checker`](https://huggingface.co/udgamlabs/Lilavati-Checker/tree/206b53c0e491ff1d88dbc48862332b7e63200303) | CONDITIONAL | 0.19 GB | 0.19 GB | 依存・権利未完 |
| [`HuggingFaceFW/fineweb-edu`](https://huggingface.co/HuggingFaceFW/fineweb-edu/tree/87f09149ef4734204d70ed1d046ddc9ca3f2b8f9) | CONDITIONAL | 全体不明 | 28.52 GB | 10BTサンプルのみ |

**数値の意味**：公開モデル21件は同じ40文字commitのHFファイルツリーから全ファイルbyteを集計。選択ファイル列はモデル本体、Codec、VAE等の**候補ファイルだけ**を選んだ概算ではなくファイル単位の正確なサイズだが、コード/追加権利/実行時構成を含む最終アーカイブ容量ではない。Chatterboxは複数系統のT3/S3Genが同居しており、正しい実行一式が特定できないため選択サイズはnull。FineWeb-Eduはデータセットの全容量が不明であることを保持する。

## 2. 最優先の重複改善：Heretic RVN

[0bserverx Heretic RVN](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/tree/ab8d7bd81d03117501e4da60cccdff4c80f0eea0)は配布元全体が**1,645,270,647,302 bytes**。通常の量子化、多言語chat template、MTP、GSQ分割、旧ALA/Heretic系の別版が同居している。**全repoをそのままミラーしない**。

現行の研究用代表形式は`RVN-Q4_K_M-multilingual.gguf`（16,547,400,224 bytes、LFS SHA256はR36に記録）と`mmproj-Qwen3.8-27B-Q8_0.gguf`（629,247,008 bytes）で、暫定合計**17,176,647,232 bytes**。全repoとの差は**1,628,093,000,070 bytes**。これは実際に容量を回収した値ではなく、もし全repoを取得する案と選択形式を取得する案を比較した場合の差である。

Hereticの反復ARA特殊学習は保存検討価値がある。旧Hereticと新版RVNは必ずしも同じ重みではないため、『旧版も通常量子化』と誤って消さない。多言語chat templateとMTP/vision組込版が本当に同じtensorかはヘッダ/対応SHAの比較が別途必要で、ファイル名のみで完全な同一性は主張しない。実用性能の独立検証と取得承認は未了。

## 3. LTX 2.5・Chris・Stubeliusの容量とアクセス権を区別

| 別学習済み状態 | 全repoバイト | 特定の研究用ファイル例 | 注意点 |
|---|---:|---:|---|
| [LTX 2.5公式](https://huggingface.co/Lightricks/LTX-2.5) | 200,853,702,264 | 38,694,140,060 byte | Gated=auto、公式ツリーのLFSハッシュはマスク。蒸留INT8 Transformer/Gemma INT8/音声VAE/映像ConvVAEの4ファイル例で、最終取得可能とは言えない |
| [ChrisColeTech特殊マージ](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | 166,915,795,579 | 36,468,259,016 byte | FP8 scaled Transformer＋カスタムGemma4＋両VAE。frtertaerミラーと15重みSHA一致、重複保存しない |
| [Stubelius v1特殊マージ](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | 195,942,118,539 | 42,008,732,600 byte | v1 BF16の一つの表現。beta1/beta2は別の学習成果なので一律除外しない |

**重要**：公式LTX 2.5のDev、Distilled、各量子化が同居するのは、学習段階と実行形式の両方があるため。単純な量子化を別モデルに数えず、一方でDevと蒸留済みを証拠なく同一重みとみなさない。公式モデルはGatedで、配布元APIのハッシュが伏せられている。フルSHA/権利/ユーザーの利用許諾が揃うまで最終保存ロックは禁止。

## 4. 小型でも重要な親・補助ファイルを削らない

| 資産群 | 選択例の重み総量 | 重複でない理由 |
|---|---:|---|
| [LiquidAI VLM本体](https://huggingface.co/LiquidAI/LFM2.5-VL-3B) ＋ [DSparkドラフター](https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark) | 6,806,008,386 byte | ドラフターはtargetの代わりにならず、別に学習された推測デコード用コンポーネント |
| [Lilavati](https://huggingface.co/udgamlabs/Lilavati) ＋ [Checker](https://huggingface.co/udgamlabs/Lilavati-Checker) | 378,968,896 byte | 両方とも189,484,448 byteだがSHA-256は違う。ソルバーと検証器は独立学習済み重み |
| [Audio8 Realistic Air](https://huggingface.co/Edge0/Audio8-TTS-Realistic-Air) | 2,552,200,087 byte | 音声生成本体だけでは不十分。Codecが本体より大きくても必要な補助学習成果 |
| [Galvanize-3](https://huggingface.co/usezn/Galvanize-3) | 562,583,392 byte（Safetensors本体） | ONNXは同じ分類器の別実行表現として扱う。ただしONNXと原重みの数学的同等性は未検証 |

**Chatterboxの保留理由**：リポジトリに12個の重み形式と複数のT3/S3Gen世代が混在。単純に最小容量の組合せを選ぶと、世代が違う部品の混合や、日本語対応の欠落が生じ得る。v2/v3などが新たな学習成果か純粋な圧縮かを原作者の対応表で確認するまで、保存対象を勝手に1ファイルへ削らない。LivePortraitも人物・動物・動物v1.1は改変目的や学習版が異なり、通常量子化と同じ扱いにしない。

## 5. FineWeb-Eduは全体ミラーでなく公開サンプルを識別

[FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu/tree/87f09149ef4734204d70ed1d046ddc9ca3f2b8f9/sample/10BT)の`sample/10BT`14 Parquetを固定commitで列挙し、**28,518,193,415 bytes**および各ファイルのSHA-256を記録した。その他の`sample/100BT`、`sample/350BT`などが存在するが、それぞれの収録データが重なるかは未検証。10BTを保存しても全FineWeb-Eduの学習再現ができると主張しない。ODC-BY条件の適用範囲、データの出典と削除要求、サンプルの独立性も取得前に監査する。

## 6. H/T/D/C/U・変数表・単位検査

| 記号 | 日本語の意味 | SI単位 | 定義・範囲・型 |
|---|---|---|---|
| R_i | 第i配布元の全repo容量 | byte | 固定40桁commitの公開ファイル合計。データ全体未集計はnull、非負整数または欠損 |
| S_i | 第i資産の候補ファイル総量 | byte | 必要候補の選択ファイル和、ランタイム依存不足時もある。非負整数またはnull |
| N_f | 固定サンプルのファイル数 | 1 | FineWeb-Edu sample/10BTは14、非負整数 |
| C | 計画予算 | byte | 4,000,000,000,000、ユーザー申告に基づく非負整数スカラー |
| F | 実機安全空き | byte | 200,000,000,000、非負整数スカラー |
| M | 推論実機のピークRAM | byte | OS・driver・Codec・KV・VAE等込み、未計測はnull |

**H**：公開元をリビジョン固定し、同一学習状態の余分な表現を整理することで、4TB予算の中で異なる専門訓練成果を保持できる。**T**：22件の固定APIファイルツリーとSHAを読み取り、音声/動画/データに独自学習と単なる圧縮形式を分ける。実機の許可が得られた場合は固定HW/clock、backend/ABI、quant zero-point、batch/context、Codec/VAE、stagingと選択SHAを検証する。**D**：元学習状態と依存の権利・品質・完全byte・実機容量を満たすときだけSELECT/取得審査PASS。既存の部分集合だけでは最終取得UNCERTAIN。無根拠な複数量子化を別学習モデルとして数えるのはFAIL。**C**：巨大な全repoを必要保存容量と勘違い、同じバイト数の別重みを重複と誤認、Gatedハッシュの存在を仮定、モデル構成とCodecを別にしたまま実行可能と判断する。**U**：ユーザーの実機空き、未完成Chatterbox一式、FineWeb-Edu全体容量、LTX公式の権利・ハッシュ、ベンチマーク品質が未計測。合成標準不確かさu_cと包含係数kは未定義。**次元チェック**：R_i、S_i、C、F、Mはbyte、N_fは無次元。HDDの保存byteとRAMのbyteは別の観測対象。

## 7. ERROR CHECK／関連分野／次に考える問い

**ERROR CHECK**：22件の既存有効資産に40文字SHAを固定、21件のmodel source repo全ファイルbytes、FineWebサンプル14 SHA、R21 Interpretic二重コピーSHA一致、Heretic代表Q4＋projector 17,176,647,232byte、Lilavati/Checker同サイズ異SHAを再計算で照合。推論・転送・ユーザーHDD検査なし。v19の150管理・105有効、Nanbeige SELECT、4TB計画、空の取得承認キューは不変。

**学際性**：デジタルアーカイブ（重み同一性）、数値計算/コンパイラ（量子化・ONNX）、音声/映像システム（Codecと生成スタック）、学習データ研究（FineWebの部分集合と著作権・来歴）に応用する。

### 〈次に考える問い〉

全体4TBの保全価値を最大化するには、次にChatterboxの世代別パイプラインを特定することと、既存の高容量モデル8件を各1学習状態に絞る作業のどちらが確実な容量改善につながるか。
