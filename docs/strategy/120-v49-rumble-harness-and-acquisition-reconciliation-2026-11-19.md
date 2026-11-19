# R120｜v49最新監査：取得報告53件・Rumble小型ASR次期原本・無検閲保全方針（2026-11-19）

## 1.〈本論〉— 現行正本と新規候補の確定

**現行はv49（202登録／155有効、SELECT53/CONDITIONAL102）。** v49ではすでに[SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B)が、Gated原本に対するCONDITIONALとして登録されている。Rumbleを同じv49の別追加として上書きせず、**次版の独立原本として採用提案を確定**する。正式v50への反映・取得承認はこの調査段階では行わない。

[Reson8/Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash)は出版社が2026年11月18日に公開した45言語ASR。主重みと別の学習済みCTC補助headを含む、固定revision `a0c34287229103b706c670d70791683e34379732` の**19ファイル・1,385,998,807 byte**、LFS SHA256が2件。Publisher [release blog](https://huggingface.co/blog/rumble-2-flash)には英語WER6.60%/多言語9評価言語平均6.96%、大バッチ7,000倍実時間が示される。ただし**H200/vLLMの著者条件**であって本人PC・batch1の達成値ではない。既存Whisper Turbo、Qwen3-ASRからの実際の精度増分は未検証。

| 学習成果 | 固定ファイル | Publisher SHA-256 |
|---|---|---|
| ASR本体 | `model.safetensors`（1,017,318,776 byte） | `6dc35af40ad150e50767382a9d401eb9af9c3a1ad4e915c61fe05aecfa79a3e1` |
| 学習済みCTC head | `ctc/ctc_head.safetensors`（357,476,284 byte） | `c13befc1c60a8410185a730cdccefc825df12ac8af75d4411fdff8106291ede7` |

[19ファイルの全publisher SHAと依存一覧](../../manifests/drafts/r115-v48-rumble2-flash-and-nemotron-sigma-original.candidate.json)でモデル構成を確定し、同一学習重みの追加GGUF/ONNXを無造作に別資産登録しない。

## 2.〈応用・転用例〉新規比較と優先順位

| モデル | 判定 | 理由 |
|---|---|---|
| Rumble-2-Flash | **次版正式選定の第一候補** | 小型・多言語・独立CTC学習済み原本、1.386GB |
| [harness-hub/pi coding LoRA](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) | **P1 原本の版固定** | 既存Qwen27Bに適用する別RL学習結果。出版社はTerminal/SWE-bench改善を報告。親revision・adapter byte/SHAとREADME内別名の照合が必要 |
| [SenseNova-Loop-9B](https://huggingface.co/sensenova/SenseNova-Loop-9B) | **既存v49選定維持、Gated権利P0** | 32物理/56実効decoder層、two-stream mHC・画像。Gated個人アクセス・MTP/vision・custom runtimeの閉包が未完 |
| [NVIDIA Sigma](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B) | HOLD | 独立diffusion/AR、8.495GB固定済みだがライセンスotherとcustom code |
| [Apple FastFrames-S/L](https://huggingface.co/apple/FastFrames-S) | HOLD | 独立後学習動画。Apple/親Wan/LingBot条件、Lの約174GB sourceから必要原本だけ選択する課題 |
| [LongCat Avatar 1.6](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6) | HOLD | 音声動画DMD/OPSD LoRAは独自結果だがparent/codec/任意量子化重複を解消してから |

[8候補の機械可読判断](../../catalog/decisions/2026-11-19-r120-v49-rumble-harness-specialists.json)に残る未解決条件を保存した。既存の無検閲0bserverx RVN、InterpreticAI v2、OrcaRouter Gatedは異なる学習済み成果として維持し、量子化同士やGGUF→Safetensors再構成物を独立学習成果として二重計上しない。

## 3. 実際に取得したと報告されたモデルの監査

GitHubの[取得実行ledger](../../catalog/execution/2026-11-19-acquisition-ledger.json)は**53モデル・579ファイル・270,835,576,267 byteをVERIFIEDと報告**する。しかし、この調査回は実Dドライブへの直接アクセス・独立SHA256再計算をしておらず、本人のLICENSE行為別・依存・offline復元が完了したとは認定できない。既存ファイルを無条件に再取得せず、実際の保存先を特定しハッシュ比較する。現在の`queues/approved.json`は0件であり、次の取得実行承認は別の条件。

**規制の事実と予測を分離**：[米BIS 2026-11-16遠隔高度計算アクセス規則](https://www.bis.gov/press-release/bis-issues-rule-addressing-remote-access-american-super-intelligence-technology)は公開weightsの一律所有禁止とは別。[EU AI Act GPAIオープンソースFAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)は提供者義務・例外について。個別将来禁止確率は根拠不足のため推定しない。ExaはHTTP402で利用不可。

## 4. 変数表と誤差・単位

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・範囲・前提 | 型 |
|---|---|---|---|---|---|
| `N_main` | 主ASR学習済み格納要素数 | 1（無次元） | 508,631,552 | Publisher SAFETENSORS値。別CTC含まず | 非負整数スカラー |
| `B_ctc` | CTC原本ファイル容量 | byte（非SI） | 357,476,284 | Publisher固定、本体CTCの厳密テンソル計数未実施 | 非負整数スカラー |
| `N_upper` | CTCを含む条件付き要素数上界 | 1（無次元） | `N_main + 8 × B_ctc` | 各学習要素が1bit以上を占有、外部学習済み重みは別審査 | 非負整数スカラー |

**数値・単位チェック**：508,631,552＋8×357,476,284＝3,368,441,824要素で150B未満。ただし厳密なCTC要素数ではない。byte×8bit/byte÷1bit/要素＝要素数となり、N_mainと加算可能。runtime RAM/VRAM、context、KV/cacheの上界を示す計算ではない。

## 5. H/T/D/C/U・ERROR CHECK

**H**：新規の学習済みCTC ASRは、既存量子化の重複保存より高い独自価値を持つ。**T**：19ファイル、完全Publisher SHA・40桁revision、元コード、完全LICENSEと依存を検査。次に同一HW・クロック・backend・batch・量子化/zero-point・音声長で各30発話以上の日本語CER/英語雑音WERをWhisper・Qwen ASRと比較。**D**：source metadata PASS、本人権利/実HDD/復元UNCERTAIN、無承認取得FAIL。**C**：旧ASRで同性能以上を再現できるか、CTC ABI不整合。**U**：著者H200大バッチ・端末差、契約、復元依存。実測分散がないため合成不確かさu_cとkは数値化できない。

**ERROR CHECK**：公式v49の202/155を不変更。新規正式追加0、削除0、今回のモデル重量DL0、承認キュー0。固定Rumble19ファイル/2SHA/1,385,998,807byte。GitHubの取得台帳53件は自己報告のまま扱う。関連分野は音声認識/ML、保存工学、ソフトウェア供給網・ABI、情報法。

## 6.〈次に考える問い〉

既存モデル53件の現物を再ハッシュ・復元する作業と、Rumble・pi LoRAを次に追加する作業のどちらが、失われる可能性のある**独立学習済み能力の保全率**を高めるか。
