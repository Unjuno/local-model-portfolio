# R117｜v48・53件の取得報告を重複排除し、実際に保存すべき原本を次の5件へ絞る

**2026年11月19日 / 正本 main v48**。現行 `Unjuno/local-model-portfolio` は **201登録／154有効（SELECT53＋CONDITIONAL101）**。今回の対象はカタログの新モデル数を増やすことより、既に報告された取得原本・別精度・不足する学習済みCodec・権利の判定を、次に再現できる保全成果へつなげること。

[全154資産の再照合とR115固定16sourceの機械可読R117判定](../../catalog/decisions/2026-11-19-r117-v48-reported-acquisition-and-next-originals.json)／[現行R115固定source候補](../../queues/proposed-v48-r115-master-sources-16.json)／[取得履歴台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)を同時に基準とした。`queues/approved.json` は引き続き空。**ユーザーのWindows Dをこの調査セッションから独立に読み直したわけではない。**

## 1.〈本論〉— 台帳の53件の意味を限定する

2026-11-19取得台帳は、**54件報告のうち53件がPublisher SHA-256またはGit blob SHA-1によるファイル一致としてVERIFIED**、1件OrcaRouterはGated HOLDと報告する。**579ファイル／270,835,576,267byte**、過去のDドライブ最小残空き**2,710,260,613,120byte**。これらは**履歴に記録された実行結果**であり、現在この場で再取得・現物SHA・オフライン推論・所有者の利用契約を独立監査した意味ではない。

古い[R116 report](116-v48-r115-windows-d-unattended-acquisition-and-reconciliation.md)にある「22 VERIFIED／227ファイル／162.326GB」は、取得台帳の更新によって**現状の全件数としては古い**。削除せず履歴値として残す。53件の報告済み原本から、同じrevisionのファイルを重複して再取得してはいけない。

**有効154資産の排他的区分**：モデルのPublisherファイル検証済みとの実行報告53件、Gated HOLD報告1件、モデルの該当実行記録なし82件、選定されたデータセット18件。合計154。**53件≠54件の完全オフライン推論再現ではない**。`maya2-native`や`Kumo-Relational/Anomaly`のように学習済み総数・codecが未確認のものもsource検証報告として現れるが、従来のモデル単位の取得STOPを自動解除しない。

## 2. ダウンロードすべき原本の取得判断：R115 16候補中の10件

R115は10件を`GO_AFTER_LOCAL_PREFLIGHT`、6件をHOLDに区別した。このGOは**ダウンロード承認ではない**。今回、repo・正確な40文字revision・選択ファイル数・選択source整数byteの全てを古い取得台帳と照合し、**7件は完全一致、3件は別ソースのため未完了**と確定。

| Publisher固定source | 選択source bytes | 現在の扱い |
|---|---:|---|
| `ibm-granite/granite-timeseries-ttm-r3` | 5,748,963 | 過去報告と原本scope完全一致・再取得不要 |
| `robbyant/lingbot-touch-tiny` | 21,873,479 | 過去報告と原本scope完全一致・再取得不要 |
| `n4ze3m/tiny-voca` | 23,626,858 | 過去報告と原本scope完全一致・再取得不要 |
| `KittenML/kitten-tts-2-mini` | 477,936,075 | 過去報告と原本scope完全一致・再取得不要 |
| `usezn/Galvanize-3` | 597,001,839 | 過去報告と原本scope完全一致・再取得不要 |
| `qvac/BotPsy-0.8B` | 1,726,201,481 | 過去報告と原本scope完全一致・再取得不要 |
| `osunlp/ARLoop-1.2B` | 4,838,079,760 | 過去報告と原本scope完全一致・再取得不要 |
| `Zyphra/ZONOS3-Mini` | 15,345,816,226 | 異なる取得sourceまたは未報告。現物未検証 |
| `InterpreticAI/Qwen3.8-27B-Uncensored-v2` | 55,586,056,799 | 異なる取得sourceまたは未報告。現物未検証 |
| `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` | 53,808,326,934 | 異なる取得sourceまたは未報告。現物未検証 |

**新たに取得する必要がある原本候補の3件**（過去に同等の重みを別形式で保存したかもしれないが、現在の固定source scopeとしては未検証）：

1. **`Zyphra/ZONOS3-Mini` 15,345,816,226byte**：元音声LMに加え、ZAC-1 Codec、学習済みdecoderやspeaker encoder等を含む24ファイル。過去の`VERIFIED`は同版66ファイル・775,728,152byteという**別の保存集合**。完全な音声パイプラインを保存したとは認定できない。
2. **`InterpreticAI/Qwen3.8-27B-Uncensored-v2` 55,586,056,799byte**：作者のフルBF16、MTP維持、18 Safetensors shard。過去の`VERIFIED`は**量子化GGUF-v2の17,738,327,225byte**であり同じsource repo/file setではない。元の学習結果を高精度で研究・再量子化できる将来価値を優先。
3. **`0bserverx/...-GGUF` RVN-F16 53,808,326,934byte**：作者がSafetensorsへ再構成する際の既知のF16 GGUF元。過去`VERIFIED`は**Q4＋vision projector 17,176,692,278byte**であり別のsourceスコープ。学習時BF16ではない。公開者の13-shard Safetensors再構成物や別のGGUF量子化をデフォルト二重取得しない。RVN-F16はテキスト用途が基本で、旧Q4＋projectorのvision同等性は**未証明**。

上記3件の固定source合計は**124,740,199,959byte（124.740GB）**。7件の既報告一致source合計は **7,690,468,455byte（7.690GB）**。旧source重みを誤消去しない。ZONOS3のファイル・RVN形式などは実HDDで1パスずつ存在／SHA検証するまで**新規物理増分を断定できない**。

6件のHOLDはNemotron Diarization（OpenMDW＋推論ABI）、DSpine（親Qwen27B依存）、ChatR Labs Qwen Image LoRA（非商用親契約）、Gryphe Pantheon／DavidAU（大容量で独立能力増分未証明）、OrcaRouter（Gated本人権限）。台帳に報告済みのファイルがあっても**削除しない**。

## 3. 取得候補3件の次に残すべき2つの独立学習成果

先に単一Sourceを固定し、既存の53件取得報告にはない**2件**を追加で優先評価する。いずれもv48の既存`conditional`であり、原本を新資産として二重登録しない。

| 公式Publisher原本 | 保存file refs | source bytes | 上流LFS SHA | 必須の未解決事項 |
|---|---:|---:|---:|---|
| [`KRAFTON/Raon-1-nano`](https://huggingface.co/KRAFTON/Raon-1-nano/tree/39f897a1f835c723ec633c6c905dca7312bd9fd7) | 17 | 7,182,126,657 | 5 | Custom modeling/config source and separate MTP head required; published 3.2B rounded count versus 3.5299B serialized main tensors, inspect exact count before final lock |
| [`abel-lab/Simons-297M`](https://huggingface.co/abel-lab/Simons-297M/tree/335dc22e4ce26ca0a8bc567de9e93dbb1bd2ce3a) | 6 | 1,188,951,960 | 1 | OpenMDW-1.1 model weight license not identical to training dataset licenses; independent source and code/runtime verification needed |
| **合計** | **23** | **8,371,078,617** | **6** | **取得未承認** |

- **Raon-1 nano**：Delta Attention＋Gated MLAなど異なる小型ハイブリッド言語モデル。BF16元checkpointと専用MTP、`configuration_raon1_nano.py`と`modeling_raon1_nano.py`を保存し、未審査のコードをその場で実行しない。著者公称3.2BとHF main serialized3.5299Bの差は修正済みの証拠がないため正確な一意総数と称しない。
- **Simons-297M**：時系列の確率予測と共変量attentionという別の学習済み成果。Chronos/TTMとの学習済み重み同一性なし。OpenMDW-1.1本体とNOTICE、訓練データの別契約、再現環境を分離して確認する。

次の原本群として、**LFM3-1.7B-Base**（独自ハイブリッド事前学習原本だがHFライセンスタグ`other`）、**iLLaDA-8B-Base**（独立拡散言語アーキテクチャ、約16.5GB）、**NVIDIA Ising量子誤り訂正Color/Surface 2件**（互いに別の学習成果だがGated）を研究優先とする。一方、`m-a-p/SheetSage2`と`MERT-v2-FullSong`はCC BY-NC-4.0、`pfnet/plamo-3-translate-0.8b`は独自ライセンスなので用途別権利確認を先にする。単にサイズが小さいからと無条件取得しない。

## 4. 取得器の安全条件を実装修正

既存の[Windows取得器](../../scripts/download_r115_windows.py)を**main上で修正済み**。改修前は`--execute`に対し`--approval-file`が任意であり、[運用方針](../../policies/limits.json)の`require_user_approved_manifest=true`と矛盾した。

**修正後は`--execute`に必ず`--approval-file`を要求**し、各選択元repo／40桁revision／ファイル名・byte・SHAから構成した`source_scope_sha256`が、本人が承認したライセンス審査・本人HDD確認の記録と一致することを、外部通信・ディレクトリ作成より前に検査する。現状の`queues/approved.json`は空なので、**研究段階の自動取得は許可されない**。

また、`HF_HOME`や`local_dir`へのLFSキャッシュ・書き込み時には、最大ファイルの4分の1では足りない可能性がある。ファイル転送時の一時領域見積もりを**最大ファイル2個分または最低2GB**へ強化した。これは実際の全部のランタイム／Codec／圧縮展開まで保証しない。安全性を確認する[追加テスト](../../tests/test_r115_download_manifest.py)は3件作成したが、**この回答環境ではPythonユニットテスト自体は実行できていない**（コード・設定の静的監査のみ）。

`py -3 scripts/download_r115_windows.py --root "D:\AI-Models"` は読み取り中心の計画表示。実際の`--execute`は、そのWindows端末で本人が作成・審査した**正確なマニフェスト承認ファイル**があり、Dの実空き・再ダウンロード回避・ライセンスに合格したときに限る。今回こちらからダウンロードを起動していない。

## 5. 規制の一次根拠と誇張の排除

2026-11-19公開予定の米BIS公式[Interim Final Rule 2026-23529](https://public-inspection.federalregister.gov/2026-23529.pdf)のIV.A節は、2025年AI Diffusion Rule由来の**AIモデル重み固有のECCN 4E091を撤廃**すると明記。一方、先端半導体と遠隔データセンター計算資源の別の輸出・用途規制は存在する。したがって「米国で公開重みをすべて禁止する方向がすでに法制化された」という前提は**事実誤認**。ライセンス、地域、Gated、個別削除が将来変化する可能性は別の監視項目。全モデルの規制確率や期限を創作しない。

モデル有効選定154件はそのまま。**既存有効9件の学習済み総数不明、Gated20件、150B超の量子化例外2件**の強制STOPは解除しない。

## 6. 変数表と必要容量の保守的な判定

以下はR115次の3原本およびRaon・Simonsの**5 sourceを全量新規**と仮定し、最大1ファイルのステージングを二重に数える感度分析。既存内容と重複すれば実増分は小さく、外部依存を含めれば大きくなるため、**物理サイズの実測や取得GO判定ではない**。

| 記号 | 意味（日本語） | SI単位 | 定義・条件 | 範囲・前提 | 型 |
|---|---|---|---|---|---|
| `S_3` | 別sourceとして未完了の3原本 | byte | 124,740,199,959 | 0以上・publisherの選択file計 | 整数スカラー |
| `S_2` | RaonとSimonsの2原本 | byte | 8,371,078,617 | 0以上・source固定済 | 整数スカラー |
| `S_5` | 次の5原本のsource合計 | byte | `S_3+S_2` | 0以上・実増分ではない | 整数スカラー |
| `P` | 選択5原本の最大1ファイル | byte | 53,808,281,888（RVN F16） | 正の整数・上流ファイルbytes | 整数スカラー |
| `O` | 保守的な一時ファイル余裕 | byte | `max(2GB,2P)` | Runtime/外部依存の大きさは含まない | 整数スカラー |
| `F` | 保存後の最低空き床 | byte | 200,000,000,000 | 現行方針 | 整数スカラー |
| `B` | 仮定のもとでの取得前必要空き | byte | `F+S_5+O` | Dドライブ実空きとは別 | 整数スカラー |
| `D_{free}` | Windows Dの**現在**の実空き | byte | 未測定、null | 0以上または未知 | 整数/nullスカラー |

`S_5=124,740,199,959+8,371,078,617=133,111,278,576 byte`。`O=2×53,808,281,888=107,616,563,776 byte`。従って`B=200,000,000,000+133,111,278,576+107,616,563,776=440,727,842,352 byte`。すべてbyte単位の加減と倍率のみで**次元チェックPASS**。選択ファイルは合計**82 refs／Publisher SHA-256 38件**。Dドライブの履歴上の2.710TB最小残空きを現時点の`D_{free}`に代入しない。

## 7. H/T/D/C/U・ERROR CHECK

**H（仮説）**：原本を「学習成果＋依存＋正確な版」に固定し、既取得sourceを再ハッシュして再取得を避けることで、保存可能な独自能力を容量あたり増やせる。**T（最小検証）**：154全件のID、54取得実行記録、R115の16固定sourceをJOIN（n_min=154）。文字列だけでなくrepo・40桁revision・ファイル数・整数byteが全一致のものだけをスキップ候補とする。WindowsではSHAと完全オフライン推論を別々に検証。品質評価は同型HW・backend・clock・batch/context固定の独立試験30件以上。

**D（判定）**：静的JOINで53報告VERIFIED・1 Gate HOLD・GO10中7完全一致・3別sourceはPASS。本人Dの独立実SHAと依存再現・権利承認はUNCERTAIN。Gated回避、許諾なし取得、未知の学習総数をPASS、元ソース差分を無視するダウンロードはFAIL。**C（対立仮説）**：台帳報告済みファイルが移動・破損した、外部Codec・学習済み依存が足りない、同じrepoの別trained checkpointを同一原本と誤分類した場合。**U（不確かさ）**：ログの検証時刻、実ディスク位置、Git LFS指紋、権利全文、ソフト供給網と外部依存が主要。反復分布がないので合成標準不確かさ`u_c`と包含係数`k`を数値化しない。

### ERROR CHECK

- 最新正本v48：201資産、154有効。**登録・採否変更0、新たな重み取得0、approved0**。
- 実行台帳54件のうち53件でPublisher整合を**報告**、総579ファイル／270,835,576,267byte。Dの現物独立再計測は未実施。
- R115：GO10件のうち7件の一致、別source3件124,740,199,959byte、保留6件を分けた。Raon+Simons 23ファイル8,371,078,617byteを次に固定。
- 新規の厳格な実行条件により、空の承認台帳のまま`--execute`する経路を閉じた。追加テストは**作成済・未実行**。
- 米BIS 4E091の撤廃は公式公開文書の確認。公開ウェイトの日本国内個人保管が一律に違法になったという主張は行わない。

## 8.〈次に考える問い〉

**現物で確認できた原本だけを『保存済み』と扱う運用に移したとき、まず53件の既報告SHAを再検証することと、3件の高精度・Codec原本を新たに転送することのどちらが情報損失を最も速く減らすか。**
