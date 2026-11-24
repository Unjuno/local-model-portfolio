# R166／v71：極小TTS・無検閲LoRAの全ソースSHA閉包と親重み重複回避（2026-11-25）

## 1.〈本論〉正式採否と検証の結論

**唯一の正本はv71／260登録・210有効（SELECT56、CONDITIONAL154、HOLD31）のまま。** 3件ともv69以前からCONDITIONALに登録済みなので今回の新規正式モデルID、取得承認、モデル重量DL、ユーザーWindows D変更はいずれも0。

R162では3件の学習済みコア重み5ファイル計92,138,387 byteだけが発行者SHAで固定され、非重みファイルのbytesとGit OIDが未閉包だった。今回は各repoの不変コミットで**全89ファイル**のパス、正確なサイズ、Git blob OID、LFS SHA256（存在する場合）を記録した。

[全Publisher原本と外部GitHubコードの機械可読固定](../../manifests/drafts/r166-2026-11-25-tiny-tts-inkling-adapter-complete-publisher-scope.candidate.json)／[取得未承認の32ファイル研究キュー](../../queues/proposed-v71-r166-three-small-complete-source-UNAPPROVED.json)／[採否とSTOP条件](../../catalog/decisions/2026-11-25-r166-v71-three-small-source-finalization-and-stop.json)。

| Publisher不変原本 | 全repoファイル・byte | 優先保存source scope | 採否 |
|---|---:|---:|---|
| [Paradee-8M-v1.3](https://huggingface.co/sahilmahendrakar/Paradee-8M-v1.3/tree/b569f5efb789af5ba643a44af348427242ceb784) | **59ファイル／87,606,314 B** | **9ファイル／74,922,992 B** | P0 CONDITION維持。異なる蒸留学習状態。FP32/INT8 ONNX、PyTorchのtext/decoder、tokenizer・設定・LICENSEを一組で |
| [TiHon-TTS](https://huggingface.co/ngocthien/tihon-tts/tree/bc71174f68651e7ff32a90f1ffd5e7528288d403) | **20ファイル／1,862,130 B** | **13ファイル／480,266 B** | P2 CONDITIONAL研究維持。CC BY-NC 4.0、音声元の権利、未完のTFLite実装で実取得STOP |
| [Inkling-2-Mini-uncensored-LoRA](https://huggingface.co/electroglyph/Inkling-2-Mini-uncensored-LoRA/tree/4d81722b2e939460d5b544e5319b80e9b960236b) | **10ファイル／52,406,603 B** | **10ファイル／52,406,603 B** | P1 CONDITIONAL維持。ARA v2.2による51.617 MBの別重み編集状態と再現情報9ファイル |

Paradeeでは最初の公開API応答が50項目で切られ、ファイルを46件と誤認する危険があった。limit=100で再要求すると全59ファイルを取得し、Model siblingsと全パス一致が確認できた。**デフォルト表示を全ファイルと思い込む取得計画は誤りである。**

### Paradee：推論形式、G2Pコード、Python pickle

4言語（英・ヒンディー・仏・西）、8声の約7.88M独立蒸留結果。FP32 ONNXとINT8 ONNXは同じ学習結果の異形式なので、モデルIDを二重にしない。ただしPyTorch native重みが未監査のpickleデシリアライズを伴いうるため、比較用のFP32 ONNXを追加保全する価値がある。PTファイルのロードと第三者コード実行は未実施。

原作者の[別GitHubコードリポジトリ](https://github.com/sahilmahendrakar/paradee/tree/2de547e45da92840a636c499eb0782e988be1e47)のコミット 2de547e45da92840a636c499eb0782e988be1e47 も固定し、**38 Git blob、4,678,996byte**の個別SHA1/サイズを凍結した。G2P ONNXとG2P辞書、phoneme前処理コード、training/uv.lockが存在することを静的に確認。実装前提は作者Python3.10+、onnxruntime 1.17+、numpy、misaki、spacy、num2words等。非英語発音に関わるeSpeak NGのライセンス・配布範囲・実行ABI、追加wheelhouse・辞書を所有者環境で閉包できるまでは実用可としない。

49の音声デモWAVと図版は出典SHAだけ保存し、最小scopeから除外する。第三者の音声権利・復元目的の必要性を明らかにしないままサンプルを全量コピーする必要はない。

### TiHon：学習済み重みの極小性と欠けている実行物

[一次技術記事](https://huggingface.co/blog/ngocthien/tihon-tts)はベトナム語4声、**100,118学習パラメータ**と公表する。しかしHub Safetensorsの保存要素集計は**F32 100,125要素**で、差の7要素が学習対象・バッファかは現時点で不明。差を無言で丸めず、今後のテンソルセンサスで検証する。

[公開NOTICE](https://huggingface.co/ngocthien/tihon-tts/blob/bc71174f68651e7ff32a90f1ffd5e7528288d403/NOTICE)によればモデル重量・コードには**CC BY-NC 4.0**が適用され、学習元のNgọc Huyền音声データに非商用制約がある。本人の利用行為・声素材の同意と再配布権は未確認であり、用途によっては不適合。

重要な否定的事実として、tihon_tts/tflite_runner.pyはrepoにあるものの、**TFLiteグラフファイルは1件も含まれない**。実MCUでそのまま動作する完成パッケージとは呼べない。作者記事のCortex-M55+Ethos-U55性能はシミュレータ結果で実ボード測定ではない。作者CER1.0〜2.3%は36文/声の小標本、MOS人手聴感なし。custom Pythonのtrust_remote_code実行も行わない。

### Inkling：違う親コミットだが重みは同一

Heretic v2.2.0.dev0 ARA LoRAの再現設定は親 thinkingmachines/Inkling-2-Mini を **ed40e7da625f594fc9c4990f5f66be24873c22d7** に固定している。しかし116件取得台帳でVERIFIEDとして報告された親は **1fb4134b9a74f9681054f4ef82e4bf1f458a2337** で、SHA文字列は異なる。

今回、両固定リビジョンの14ファイルのPublisher OIDを比較すると、**13件が完全一致**し、残る差分はconfig.jsonのみ。編集設定側のconfigには23byte分の dtype: bfloat16 キーが追加されているだけだった。本体19.526 GB、MTP、tokenizer関係4つのLFS SHAは両revisionで一致し、**取得台帳内の報告SHAとも一致**。[機械可読の親比較](../../catalog/research/2026-11-25-r166-inkling-heretic-parent-source-parity-no-redownload.json)。

よって**学習済み原本が変化したという理由で20GB親を再取得する根拠はない**。ただしadapter_configのrevisionはnull、PEFT 0.22・rank100・o_proj.linear対象と、Inklingのloop/modelopt/runtime・dtype指定差・GPU ABIはオーナー実機で未検証。LoRAアダプタ単独では実行可能なフルモデルにならない。作者の拒否3/100・KL0.0883は同条件の独立性能試験ではなく、既存の別編集LoRAに対する品質優位も未証明。

## 2.〈応用・転用例〉容量と重複排除

\[
B_{\mathrm{selected}}
= B_{\mathrm{Paradee}} + B_{\mathrm{TiHon}} + B_{\mathrm{ARA}}
= 74{,}922{,}992 + 480{,}266 + 52{,}406{,}603
= 127{,}809{,}861\ \mathrm{B}.
\]

\[
B_{\mathrm{excluded}}
= B_{\mathrm{all}}-B_{\mathrm{selected}}
= 141{,}875{,}047-127{,}809{,}861
= 14{,}065{,}186\ \mathrm{B}.
\]

\[
B_{\mathrm{selected+code}}
=B_{\mathrm{selected}}+B_{\mathrm{code}}
=127{,}809{,}861+4{,}678{,}996
=132{,}488{,}857\ \mathrm{B}.
\]

| 変数 | 意味（日本語） | 単位（SI・情報単位） | 定義 | 定義域／前提条件 | 型 |
|---|---|---|---|---|---|
| \(B_{\mathrm{Paradee}}\) | Paradee優先9ファイルの出版社参照容量 | B（byte） | 74,922,992 | 非負整数、Owner媒体の純増量ではない | 整数スカラー |
| \(B_{\mathrm{TiHon}}\) | TiHon優先13ファイルの出版社参照容量 | B | 480,266 | CC BY-NC行為許諾は未確認 | 整数スカラー |
| \(B_{\mathrm{ARA}}\) | Inkling編集LoRA原本10ファイル参照容量 | B | 52,406,603 | 親20GBは含まない | 整数スカラー |
| \(B_{\mathrm{selected}}\) | 3原本の優先32ファイル参照合計 | B | 上記3項の和 | 取得未承認の静的研究scope | 整数スカラー |
| \(B_{\mathrm{all}}\) | 公開元3repoの全89ファイル参照容量 | B | 141,875,047 | WAVデモ等も含む | 整数スカラー |
| \(B_{\mathrm{excluded}}\) | 優先scopeから除外した57ファイル参照容量 | B | 全参照から優先分を減算 | 学習済みコアは除外していない | 整数スカラー |
| \(B_{\mathrm{code}}\) | Paradee別GitHub38 blobの参照容量 | B | 4,678,996 | 外部依存wheel・辞書は未含有 | 整数スカラー |
| \(B_{\mathrm{selected+code}}\) | 優先原本＋静的ソースコード参照容量 | B | 132,488,857 | Owner実際の純増・完全復元量とは異なる | 整数スカラー |

**次元チェック**：全項がbyteであり、byteの加算と減算なので左辺・右辺の次元はすべてbyte。4TB総計画と200GB最低空き床、staging/cacheやOwner実媒体SHAとの整合は現時点で未測定。

保全の学際的意味は、**音声信号処理・多言語音韻学・エッジCPU/NPU・低拒否モデル編集・Git/LFSデジタルアーカイブ・CC BY-NC／GPLライセンス**の六領域にある。

## 3. H / T / D / C / U

**H（反証可能仮説）**：異なる2つの小型音声学習結果と、既取得親から再生可能な別ARA編集を、二重原本・デモファイルを省いた32ファイルで保存できる。ただし完全offline復元可能とはまだ断定しない。

**T（最小検証）**：Publisher3repo全89ファイルのpath/byte/OID/LFS SHA、別GitHubの38blob、Inkling親14ファイルと取得報告の4 SHAを今回静的検査。次は許諾済み各言語100文以上のWER/CER・人手MOS、同一CPU/GPU/クロック/OS/量子化scale・zero-point/音長/バッチ1で最低30回の速度反復、最小n未到達の逐次停止なし。

**D（合否）**：発行者ソース範囲、選別32件と旧5コアSHA、重複親回避はSTATIC PASS。本人用途別LICENSE、Owner現HDD空き＋200GB床・cache/staging、実SHA、PyTorch pickle安全性、G2P/Wheelhouse、PEFT/MCU/TFLite再現、完全offline復元、モデルファイル単位の明示承認はUNCERTAIN＝**DOWNLOAD STOP**。SHA不一致・NC用途違反・偽承認・Gated回避はFAIL。

**C（破れ方）**：Paradee G2Pの辞書またはABI不足、TiHonで未公開TFLiteグラフを復元できない、InklingのPEFT layer指定/loop dtype差でモデルが動かない、低拒否率のため他の能力が悪化する可能性。

**U（主な不確かさ）**：出版社自己評価、TiHon100125/100118の7要素差、各種外部コードとライセンス、Owner GPU/ディスクと音声品質試験の未実施。合成標準不確かさ \(u_c\)、包含係数 \(k\) は実測分散がないため数値を主張しない。

米BIS 2026-11-19旧ECCN4E091撤回は、将来の全モデル所持禁止の証拠ではない。別個のライセンス・輸出用途・アクセス権は引き続き個別確認する。

### ERROR CHECK

- 正本v71の260登録／210有効、過去116取得台帳と全210取得STOP、approved queue空は不変更。
- R162旧5重量ファイルのSHAを今回の公開元repoで照合。全89ファイル／優先32ファイル／除外57ファイルと追加GitHub38blobの整数byteを照合。
- 未審査第三者コード実行、モデル重みの実転送、所有者D変更、承認捏造は**0**。
- オフライン回帰テストと公開mainの再取得後検証結果を別途記録する。

## 4.〈次に考える問い〉

極小モデルであっても保存後の完全再現には、重みのほかにG2Pコードや専用NPU形式が必要になる。**「原本重みが存在すること」と「将来その原本を利用できること」を、どの検証ゲートで区別すべきか。**
