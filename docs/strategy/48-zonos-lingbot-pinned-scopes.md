# R48｜ZONOS3・LingBotの固定ファイル監査と編集GGUFの誤分類訂正

2026-11-12。基準ブランチ `strategy/2026-11-03-01-risk`、親コミット `fada626a6f77438814c8f1a23fc3afa2874105c2`。
**研究証拠の追記だけを行う。v29の177資産・有効130件、CURRENT、採否、承認キューは変更しない。重み取得・推論実行・規約への代理同意は行わない。**

## 1. 結論と前回R47の訂正

**「GGUFは通常量子化の重複なので省略できる」「編集は非公開部品が必要なので公開版では保存できない」という一括判断は不正確だった。** 公式コードの固定版には、非公開の元PyTorch編集LoRAとは別に、公式公開Hubの `gguf/backbone-ptq-edit.gguf` と `gguf/edit/accents.gguf` を使う編集経路が記載されている。今回その2ファイルの公開ツリー、固定revision、サイズ、LFS SHA256を確認した。

編集用backboneには追加語彙・編集マーカー等があり、`accents.gguf` は学習済み編集アダプタのバンクである。**通常版PTQと編集用部品を同じ学習状態の別精度として廃棄しない。** これは公開元の正規配布を調査する話であり、非公開の元LoRAを取得する指示ではない。元の高精度LoRAの完全復元、全機能の同等性、ユーザー環境の動作までは確認していない。

固定一次資料：
- [ZONOS3公式ggml説明・固定コード](https://github.com/Zyphra/ZONOS3-Mini/blob/3a294675a06dd496242e8dbdf2232116a874f67a/servers/ggml/README.md)
- [公式ggufファイル情報](https://huggingface.co/api/models/Zyphra/ZONOS3-Mini/tree/7146a686b62bcb0661528fa300984e815e10152b/gguf?recursive=false)
- [公式編集アダプタ情報](https://huggingface.co/api/models/Zyphra/ZONOS3-Mini/tree/7146a686b62bcb0661528fa300984e815e10152b/gguf/edit?recursive=false)

**前版への適用範囲**：本報告はR47の「PyTorch原本一構成のみ」「編集機能は非公開依存」という技術判断を、実行形式・機能単位へ限定する補正である。既存カタログの保存対象や取得許可を自動的に書き換えない。追加編集部品は同じ資産の構成再審査対象とし、新規モデルとして二重登録しない。

## 2. 固定できた公開ソース

| repo ID | 確認したモデルrevision | 公開API観測 | 確認範囲 |
| --- | --- | --- | --- |
| Zyphra/ZONOS3-Mini | `7146a686b62bcb0661528fa300984e815e10152b` | public、gated=false | 対象26ファイル。全repoの全ファイル調査ではない |
| robbyant/lingbot-touch-tiny | `f23969ccd4b6bba2163e69cc05a577455a075fe9` | public、gated=false | 全5ファイルのモデルrepo |
| Zyphra/fusealign | `59f266809e743bbc2ae25bff45e738406090bc50` | public、gated=false | 全5ファイル。編集経路にはsafetensors原本1つを採る構成案 |

コードの参照固定はZyphra `3a294675a06dd496242e8dbdf2232116a874f67a`、Robbyant `dec8025b212e7099b235cc2ef13a4921a7e59545`。**コードのSHAとHF重みのSHAは別物**。APIの `usedStorage` を現在の選択ファイル合計と読み替えない。

[36ファイルの機械可読台帳](../../catalog/research/2026-11-12-r48-pinned-scopes.json)は、19件の公開元LFS SHA256と17件のGit blob SHA1を区別する。LFS SHA256は提供元メタデータであってローカル実体の再ハッシュ結果ではない。Git blob SHA1は生ファイルのSHA256ではない。

## 3. 機能別の必要ファイル小計

**以下は固定ファイルの「確認済みソース小計」であり、完全な実行環境・物理ディスク占有・取得許可を意味しない。構成同士は重なるので単純加算しない。**

| 調査構成 | ファイル数 | ソース小計（byte） | 概数 | 含む範囲と限界 |
| --- | ---: | ---: | ---: | --- |
| LingBot-Tinyモデルrepo全体 | 5 | 21,873,479 | 21.87 MB | encoder、config、README、LICENSE、gitattributes。推論コード・センサー試料・環境は別 |
| ZONOS3 PyTorch keep2参照構成 | 14 | 11,076,560,635 | 11.077 GB | LM、generator、keep2 head、teacher、speaker encoder、設定。keep2を明示選択。最小構成や全依存完備は未証明 |
| ZONOS3 GGUF話者埋め込みTTS | 4 | 1,160,870,026 | 1.161 GB | 通常PTQ backbone、keep2 decoder、speaker encoder、README。raw-reference・編集なし |
| 同TTS＋steering | 5 | 1,161,074,986 | 1.161 GB | さらにsteer.gguf。コード・配布文書・環境等は別 |
| 公開編集用2ファイルだけ | 2 | 920,073,472 | 0.920 GB | edit backboneと編集adapter。**単独で編集は動かない** |
| GGUF編集＋FuseAlign原本の構成案 | 10 | 8,345,326,125 | 8.345 GB | edit＋speaker＋keep2＋ZAC encoder＋SSL teacher＋steering＋FuseAlign。手入力の文字起こしを前提。任意ASR、worker環境等は別 |

ZONOS3の原PyTorchファイルは `lm/zonos3_mini/model.pth`（1,772,391,535 byte）であり、safetensorsと誤記しない。`autoencoder/generator.pt` だけで7,960,647,220 byteある。READMEの「約9GB」を確定した選択容量と扱わず、**今回列挙した14ファイルでは11,076,560,635 byte**と記録する。必要部品・保存精度・原本のセーブ内容が異なるので、サイズ差から性能やパラメータ数を推測しない。

全サイズ・元SHAの出典は固定APIの [lm](https://huggingface.co/api/models/Zyphra/ZONOS3-Mini/tree/7146a686b62bcb0661528fa300984e815e10152b/lm?recursive=true)、[autoencoder](https://huggingface.co/api/models/Zyphra/ZONOS3-Mini/tree/7146a686b62bcb0661528fa300984e815e10152b/autoencoder?recursive=true)、[speaker](https://huggingface.co/api/models/Zyphra/ZONOS3-Mini/tree/7146a686b62bcb0661528fa300984e815e10152b/speaker_encoders?recursive=true)、[registries](https://huggingface.co/api/models/Zyphra/ZONOS3-Mini/tree/7146a686b62bcb0661528fa300984e815e10152b/registries?recursive=true)、[LingBot](https://huggingface.co/api/models/robbyant/lingbot-touch-tiny/tree/f23969ccd4b6bba2163e69cc05a577455a075fe9?recursive=true)、[FuseAlign](https://huggingface.co/api/models/Zyphra/fusealign/tree/59f266809e743bbc2ae25bff45e738406090bc50?recursive=true)。

## 4. ライセンス・パラメータ・実行境界

**LingBotの事実**：固定版の[LICENSE全文](https://huggingface.co/robbyant/lingbot-touch-tiny/raw/f23969ccd4b6bba2163e69cc05a577455a075fe9/LICENSE)はApache-2.0。configはdepth12、embed192、heads3、tubelet2。固定READMEは、重みが凍結Encoderのみで、予測head・下流タスクhead・optimizer・訓練ログや推論コードを含まないと明示。生のRGB画像は入力ではない。センサー値と位置・左右の対応が必要で、保存だけで自律操作が再現できるわけではない。

**アクセスの訂正**：GitHub READMEの一般的な「permissionが必要」という記述だけで現在Gatedだと断定しない。今回の3repoはAPI上gated=false。ただしこれはメタデータの公開観測であり、ユーザーの取得承認や全利用条件の適法性の証明ではない。

**ZONOS3の権利**：固定モデルカード本文は重みをApache-2.0で公開すると明記。rootに独立LICENSEファイルは見当たらない。コードMIT、依存の別ライセンス、同意済み話者入力、再配布時noticeなどを別々に審査する。カードの宣言を否定もしないが、全依存の権利が完了したとも扱わない。

**総パラメータ**：ZONOS3 HubのGGUF metadataに886,337,384という値があるが、Codec、teacher、speaker、編集adapter、aligner込みの全体総数ではない。LingBotも実checkpointの厳密テンソル総数は未検算。今回の調査で新しい完全総数PASSを発行しない。未知の総数を0とせず、上位ゲートが未確定なら最終取得lockを作らない。

**実装前提**：ZONOS3通常GGUFはQ4_0 expert／Q8_0 mixer、固定C++/ggml実装と一致する名前・schemaが必要。固定コードには旧 `zonos3-*.gguf` から `backbone-*.gguf` への改名注意がある。編集adapterは `gguf/edit/accents.gguf` のまま扱い、通常PTQが自動読込する `gguf/accents.gguf` へ誤配置しない。文字起こしを渡す編集とQwen3-ASRを追加する編集では依存が異なる。LingBotの`.pt`は取得時に実行しない。PyTorchのweights_only経路も別の明示実行審査に置く。

## 5. H/T/D/C/Uと検証

**H**：独自の追加学習を持つ編集部品を通常量子化から区別すれば、不要な形式多重保存を抑えつつ編集能力の保全候補を落とさずに済む。
**T**：固定3モデルrepo、36ファイル、6構成を対象にファイルIDの一意性、ハッシュ種別・桁数、全小計をPythonで再集計した。モデル取得・torch.load・推論・実機HDD操作は0。
**D**：メタデータ整合検査PASS。復元全体の権利・全学習済み総数・ABI・実機空き・ユーザー承認はUNCERTAIN。別版混入、許諾不適合、容量不足はFAIL。今回のPASSはダウンロードGOではない。
**C**：公開編集GGUFが必要な機能と一致しない、元高精度LoRAの復元不能、外部worker未保全、センサー正規化違い、キャッシュ二重占有。
**U**：ネットワークで確認したメタデータと未取得実体の不一致、全依存数、実機RAM・ディスク、品質再現、契約適用範囲。統計標本がないため合成標準不確かさと包含係数は数値化しない。

| 記号 | 意味（日本語） | 単位 | 定義 | 範囲・型・条件 |
| --- | --- | --- | --- | --- |
| b | 個々の固定ファイルの公開サイズ | byte | APIのsize | 正整数スカラー、実体未取得 |
| B | ある構成の既知ソース小計 | byte | その構成内の重複しないファイルのbを加算 | 非負整数スカラー、runtime等の欠測を除く |
| C | アーカイブ計画上限 | byte | 4,000,000,000,000 | 整数スカラー、実HDD空きではない |
| F | 実機に残す最低空き | byte | 200,000,000,000 | 整数スカラー、独立に実測が必要 |

**単位チェック**：小計はbyteのみを加算。十進GBは10億byte、MBは100万byte。パラメータ数やactive数を容量へ直接加算しない。構成同士の共有ファイルを再度加算せず、未測定runtime/cacheは0と扱わない。

**ERROR CHECK**：36一意ファイル＝LFS SHA256 19＋Git blob SHA1 17、6構成の全小計を再計算。ローカルの重みハッシュ確認0、実機速度測定0、リポジトリ全テスト実行0。現行177件／有効130件は変更しない。Exaは402、コンテナの直接ネットワークはDNS不可だったため、公開一次APIと文書をFirecrawlで取得。制限回避や認証情報利用はしていない。

## 6. 応用と次に考える問い

音声工学では基盤・Codec・編集adapterを別々に評価し、ロボティクスではEncoderと行動policyを区別し、デジタル保存・供給網ではrevision、hash、ライセンス、ABIの対応を保つ。
**問い：失うと再作成できない編集adapterと、公開原本から再変換できる通常量子化では、どちらに保存容量を優先配分すべきか。**
