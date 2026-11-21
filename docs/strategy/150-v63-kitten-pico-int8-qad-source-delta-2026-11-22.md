# R150／v63継続調査 — Kitten Pico INT8版の「変換重複」判定を訂正（2026-11-22）

## 1. 結論と作業範囲

現行の唯一の選定正本は [catalog/CURRENT.json](../../catalog/CURRENT.json) の **v63-20261122／235登録・188有効（SELECT55、CONDITIONAL133）**。取得履歴99モデル／1,478ファイル／1,879,994,309,866 byteは実行側のVERIFIED**報告**であって、今回の所有者Windows Dドライブ独立SHA・完全オフライン復元確認ではない。

[旧R143不変source](../../manifests/drafts/r143-2026-11-22-three-specialists-originals.candidate.json) は、[KittenML/kitten-tts-2-pico](https://huggingface.co/KittenML/kitten-tts-2-pico/tree/a5632deac7d92f6178db814d933eba746a97f2dc) のINT8 ONNX 8ファイルを「同一学習成果の変換」として除外していた。これは**作者の明示したquantization-aware distillation（量子化を考慮した蒸留学習）**と整合しない。作者の技術仕様では、INT8・INT4の出力重みが対応する量子化丸めを含めて学習されている。単なるFP32の事後量子化複製としてすべてを落とす理由は不十分である。

そのため、**INT8 8ファイル／63,628,208 byteを、既存Kitten Pico CONDITIONAL資産の追加source候補に再分類**した。[機械可読の差分マニフェスト](../../manifests/drafts/r150-2026-11-22-kitten-pico-int8-qad-source-delta.candidate.json) に既存R143が記録した全8path・byte・未取得SHAを分離して保持した。**既存R143やv63 canonical overlayは書き換えず、別のモデル1件として二重カウントしない。**

## 2. 一次資料・実装に基づく訂正

- [KittenML/KittenTTS技術文書の固定commit](https://github.com/KittenML/KittenTTS/blob/5802f6b956844919ecf210f4e55f4750a6ad7c6f/docs/kitten-tts-2-tiny.md)：INT8に対して量子化を考慮した蒸留学習を行い、INT4も同方式で学習した旨、量子化後品質の作者評価、INT4のONNX opset 21／ONNX Runtime 1.20以上を説明する。これは**配布者記述**であって、INT8/INT4独立学習時のoptimizer checkpointや実tensor差分をこちらで再現した証明ではない。
- [同commitのランタイム実装](https://github.com/KittenML/KittenTTS/blob/5802f6b956844919ecf210f4e55f4750a6ad7c6f/kittenml/kittentts2_tiny/model.py)：未指定時は`default_weights`（通常 `int8`）、明示 `weights="int4"` でINT4版を使い、`backend="torch"` でFP32版を使う。**INT8を全除外すると、公式のデフォルト推論経路で対応するファイルが不足する**。INT4を使えば必ず失敗するという主張ではない。
- [配布者モデルカード](https://huggingface.co/KittenML/kitten-tts-2-pico)：対応8言語はen/de/es/it/pt/ru/hi/fr、約7.2M学習パラメータ／言語、30音声、24 kHz、Apache-2.0表示。**日本語は非対応**。パイプラインは外部`espeak-ng`、英語用`spaCy`モデル等のコード・辞書・リソースに依存するため、モデル重量だけでは完全オフライン復元を保証しない。

### 追加対象ファイル（発行者のR143既存byte観測）

| ファイルの言語 | INT8 ONNXの名前 | Byte |
|---|---|---:|
| ドイツ語 | `kitten_tts_2_pico_de.onnx` | 7,953,526 |
| 英語 | `kitten_tts_2_pico_en.onnx` | 7,953,526 |
| スペイン語 | `kitten_tts_2_pico_es.onnx` | 7,953,526 |
| フランス語 | `kitten_tts_2_pico_fr.onnx` | 7,953,526 |
| ヒンディー語 | `kitten_tts_2_pico_hi.onnx` | 7,953,526 |
| イタリア語 | `kitten_tts_2_pico_it.onnx` | 7,953,526 |
| ポルトガル語 | `kitten_tts_2_pico_pt.onnx` | 7,953,526 |
| ロシア語 | `kitten_tts_2_pico_ru.onnx` | 7,953,526 |

| 変数 | 意味 | SI単位 | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_old` | R143で選定済みのPico公開元ファイル容量 | B（バイト） | 285,879,877 | 公開元40桁revisionの選定33ファイル、現物容量ではない | 非負整数スカラー |
| `B_delta` | 追加審査対象のINT8ファイル容量 | B（バイト） | 63,628,208 | 8ファイルの出版社reference byte、SHA未固定 | 非負整数スカラー |
| `B_new` | 追加が承認されれば対象となるPico公開元容量 | B（バイト） | `B_old + B_delta` | 同じ固定revision、追加前実取得は承認されていない | 非負整数スカラー |

定義より `B_new = B_old + B_delta = 349,508,085 B`。**単位検査**：byteとbyteの和はbyteであり、R143の公開元全41ファイル総byteと一致する。これはWindows Dの新規必要量ではなく、SHA同一既存ファイルの有無、外部辞書／ランタイム依存、stagingで変わる。

## 3. 依存と法的停止ゲート

1. R143記録の8ファイルbyteだけでは**LFS SHA256／Git OIDを未取得**。モデル重みを落とさない公開元APIの固定revision tree調査で8つのSHAを補完し、その後に明示ファイルマニフェストを再固定する。SHAを推測・偽造しない。
2. モデル配布タグはApache-2.0だが、利用者の予定行為についてLICENSE本文とデータ・音声関連権利は別審査。コードは固定commitの静的監査が必要で、未審査のPython／ONNX／torch pickle／wheelを自動実行しない。
3. 実際の保存先空き、残床200GB、キャッシュ・staging、既存INT8の実ファイルSHAを確認。既存99報告内外の**現物重複を除外**してから、個別に明示承認する。
4. 代表的な8言語・音声で、CPU命令セット／OS／`onnxruntime` backend、`weights=int8/int4`、必要G2P辞書の固定版、CPUクロック、batch、入力文と出力音声を記録し、少なくとも30例／モデルを同条件で比較する。初期段階で欠落SHA・権利・依存が見つかれば実行前に停止。

## 4. 残りの候補11件に対する交換・保留判断

[99件の取得報告後の研究キュー](../../queues/proposed-v63-r149-after99-11-research-only.json) は引き続き正本として扱う。P0のMirage 237,985,863B、Timestral-28M 111,307,038B、Pico 285,879,877B、Aurora2 1,599,571,502Bは既に別学習原本として採用判断済みであり、**新モデルとして重複追加しない**。R150のINT8再評価が実行可能になった場合のP0総Publisher参照は、旧2,234,744,280Bから2,298,372,488Bの条件付き候補へ変わる。

- **無検閲の優先審査**：`LiquidAI/LFM3-VL-2B`親と`saidutta69/LFM3-VL-2B-heretic`はPublisher BF16の重量SHAが実際に異なり、親と編集成果を対で残す価値がある。ただしLFM Open License v1.0の商用年商1,000万USD条件と学習・実装・本人行為別権利が未完了。Hereticを性能の高い無検閲実装と断定しない。
- **原本・小型の優先**：Timestral-28Mは極小の確率時系列学習成果だが重みはModified MIT、Aurora2は優れた汎用chatではなく英語中心・2,048文脈のBase、MirageはCactus 4.1.4 native engine未審査。P0をまとめて一律GOにしない。
- **動画／大規模の保留**：Apple FastFrames-SのWan親約17.567GBはモデル自身の約0.948GBと別途必要。OpenMOSS realtimeとCosmos Sim-TransferはGPU/driver/ABIを個別審査。Ripple-65Bの約129.573GBは既存P3 HOLD維持。実測品質と追加容量が未検証のまま大型へ交換しない。

### 規制の事実と仮説

[米BIS 2026-11-19発効の規則 §IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm) は旧ECCN 4E091のモデル重量規定を撤廃した。他の半導体・遠隔計算・仕向地／最終用途制限と、出版社LICENSE、各国の法令は別。現在の一律ローカルウェイト所持禁止はこの資料から導けない。[欧州委員会公式AI Act FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start) の2026年8月2日GPAI等執行も、個人研究目的のローカルモデル全般が即時禁止されたという記載ではない。将来のGated化・公開停止は**予測シナリオ**として取得先の観測事実と分ける。

## 5. H / T / D / C / U

- **H（反証可能仮説）**：作者がQADで学習したINT8 8重みはFP32からの単純な再量子化だけではbit-exactに再現できず、配布者の公式デフォルトONNX経路を完全オフライン保全するために追加価値がある。
- **T（最小検証）**：固定40桁revision、8pathのbyte・LFS SHA／OID、R143既存33path、公式コードcommitの`default_weights`実装を静的照合。使用者の固定HW、clock、ONNX Runtime（INT4は1.20以上）、入力文・言語・voiceを記録し、INT8とINT4をそれぞれ最低30文で比較。SHA不一致なら逐次停止、実行コード審査前に実行しない。
- **D（合否条件）**：公開元差分とハッシュ8/8一致、許された行為、ローカル全依存、現物ディスク残床、明示された個別承認が揃って初めて取得PASS。1ファイルのSHA不一致ならFAIL。不足中は**UNCERTAIN／取得STOP**。作者だけのQAD言及は技術機序の有力な資料だが、bit-exact不可の定量的実証ではない。
- **C（対立仮説）**：INT8重みが既存FP32やINT4からbit-exact再生成可能、既存のINT4経路で十分、あるいはINT8が特定CPU/音声品質で利得を示さない。該当時は追加約64MBを採用しない理由になる。
- **U（主要誤差源）**：作者のQAD再現ログ非公開、8 LFS SHA未取得、音声品質データの偏り、G2P外部資源、使用者CPU・ONNXカーネル、音声別ベンチマークの反復変動、保存先SHAと空き。独立の測定値が無いため合成標準不確かさ `u_c` と包含係数 `k` は算定不可。

学際領域：機械学習（量子化学習と蒸留）、エッジ音声処理（ONNX/G2P/CPU ABI）、デジタル保存（bit-exact再現とSHA256）、知的財産・輸出管理（許諾とアクセス分離）。

**ERROR CHECK**：今回新規学習モデル登録0、既存v63 235/188不変更、旧R143 source不変更、INT8候補8path／63,628,208B、全Pico条件付き41path／349,508,085B、承認0、モデル重量取得0、第三者コード実行0、所有者D現物再SHA0、既存削除0。
