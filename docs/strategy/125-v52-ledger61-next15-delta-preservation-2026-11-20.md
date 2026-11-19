# R125｜v52・取得報告61件を反映した差分保存計画と15配布元の原本確定

**2026年11月20日、日本時間。** 対象：Unjuno/local-model-portfolio `main`。現行v52は205登録／158有効（SELECT53、CONDITIONAL105）。選定の重複調査を続ける代わりに、GitHubの最新取得実績を**現物再確認前の報告**として扱い、次に転送が必要そうなsource fileだけに絞る。新たなモデル資産の追加・削除は行わない。

## 1.〈本論〉取得報告の更新と現物の区別

[取得台帳](../../catalog/execution/2026-11-19-acquisition-ledger.json)は、**61モデルのpublisher-hash照合が完了したとの報告**、全708ファイル、計409,835,119,252byte（論理）。1 Gated HOLD。最小空き2,445,946,363,904byte・200GB床維持の記録は**当時の実行元が報告した過去観測**であり、今回の所有者Dドライブの実測値ではない。

[現行158資産の一意判定台帳](../../catalog/decisions/2026-11-20-r125-all158-ledger61-reconciliation.json)は**取得済み報告61、Gated保留1、取得報告なし96**に分類。61/158を『全て完全オフライン実行可能』とみなさず、weight byte hashと全依存の復元を別検証とする。

## 2. R122から実際の候補をさらに縮約

[R125差分15配布元・全ファイルscope](../../queues/proposed-v52-r125-ledger61-delta-next15.json)は、[従来のR122](../../queues/proposed-v50-r122-deduplicated-next15-sources.json)の**同一15元repo、同一revision**を維持。3モデルの重みファイルは最新ledgerで同じpublisher SHA256と報告済みなので、もう一度丸ごと取得せず、ファイル数・bytes差を満たす唯一の付属ファイル集合だけを選択。

| 既報告モデル | R125で残す付属ファイル | 選択source bytes | 前提のSHA照合 |
|---|---:|---:|---|
| RWKV7-7.2B | 7 | 337,813 | 既保存の3 weight shards |
| iLLaDA-8B Base | 4 | 28,506 | 既保存の4 weight shards＋tokenizer.json |
| TRELLIS.2-4B | 1 | 1,519 | 既保存の9 trained tensor files |
| **計** | **12** | **367,838** | **17個の既保存LFS hash照合** |

RWKV7は`inference/generate.py`、`kernel.py`、`model_loader.py`、`requirements.txt`、`runtime.py`、`.gitattributes`、`NOTICE`の7件。iLLaDAは`modeling_illada.py`、`configuration_illada.py`、`SECURITY.md`、`.gitattributes`の4件。TRELLIS.2は`.gitattributes`の1件。

**推論と事実を区別する**：上記の12件は『配布元の固定ファイル一覧の部分集合』という前提のもと、(a)旧取得台帳のrepo/revision、(b)検証報告済み重みSHA、(c)新旧ファイル件数差、(d)byte差の条件を満たす組合せが**各モデル一意**となることから導いた。旧台帳が全ファイル名を一覧表示しておらず、Dドライブ現物を独立再観測していないため、**物理的な欠落はまだ証明されていない**。大きい重みがあるかを実際にSHAで検査するまで、コードや付属ファイルを自動ダウンロードしない。

## 3. 入れ替え後の必要sourceとモデル選定

| 区分 | R122（旧） | R125（新） |
|---|---:|---:|
| 配布元 | 15 | 15 |
| 選択ファイル | 332 | **287** |
| Publisher SHA256参照 | 135 | **118** |
| 上流ファイルの論理量 | 374,701,109,177byte | **327,549,073,014byte** |

差分47,152,036,163byteはRWKV/iLLaDA/TRELLIS原本のうち既に検証したと報告される重量ファイル等に対応し、**二重転送候補から除外**した値である。物理HDDの47GB削減を確認したという意味ではない。

残る12 sourceは従来の選定ファイルを保持：少容量の[ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100)／[Aya Dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset)、独立した[Reson8 Rumble-2-Flash](https://huggingface.co/Reson8/Rumble-2-Flash)、公開版[SenseNova-Loop-9B GGUF](https://huggingface.co/sensenova/SenseNova-Loop-9B-GGUF)と一致コード2ファイル、ZONOS3-Mini原本、Z-Image-Turbo、Wan2.2 TI2V、Fara1.5、Hy-Memory、無検閲のInterpretic v2 BF16と0bserverx RVN-F16。**SenseNovaの作者BF16 SafetensorsはGated**であり、公開GGUFをその完全な訓練時原本と表現しない。F16 RVNはSafetensors再構成元でありpre-GGUF学習時checkpointとは断定しない。

今のv52で別途条件付き登録されている[harness-hub pi coding RL LoRA](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted)（publisher source657.633MB）は、訓練時の親Qwen3.8-27B revisionが未特定のため**今回のR125取得枠へ黙って追加しない**。DaisyRose-27B BF16（約55.586GB）も独立RL後学習の実益と全体4TB容量の追加評価まで別のHOLD順位とする。既存v52登録・CONDITIONAL状態は変更しない。

## 4. 実装・非破壊テスト

更新した[Windows取得器](../../scripts/download_r115_windows.py)はR125候補も理解する。3件の差分scopeでは17個の**既存のweightファイルのpublisher SHA256**を、実際のDドライブでファイルを開いて検算する。1つでも欠損・不一致、symlink、別ディレクトリ、版違いなら`SKIP_PREREQUISITE_SHA`としてネットワーク転送せず停止する。既存のモデル全体が実行可能かは別審査。**認可scopeのfingerprintには前提のweight SHA一覧も含める**ため、差分ファイルの対象が改変されたら旧承認を流用できない。

Python3.12/Linuxの別テスト環境で、R125新規13件・R122旧12件・R115旧10件・R119旧6件・認可7件、**合計48回帰テスト全件PASS**。テストは数byteの模擬ファイルを使用し、実重み・モデルコードはロードしていない。古いmanifestの後方互換性も確認。

Windows所有者ディスクが接続された端末での**読み取り専用dry-run**：

```powershell
py -3 scripts/download_r115_windows.py --manifest "queues/proposed-v52-r125-ledger61-delta-next15.json" --dry-run --root "D:\AI-Models"
```

実際の保存実行は、**本人が目的別の使用権とDドライブ200GB空き床／staging／snapshot固定を確認して、その15sourceの正確なファイルscopeを明示承認した**場合のみ`--execute --approval-file <user-approved-json>`を使用。現時点で`queues/approved.json`は空であり、モデルの重量取得・実行・依存のoffline restoreはこの作業で行っていない。

## 5. 法規・予測を混同しない

米国官報2026年11月19日付[91 FR 74970–74999 / Doc 2026-23529](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf)は同日発効。旧AI Diffusion Ruleの**model weights用ECCN 4E091を撤廃**し、先端チップ・遠隔計算資源への規制は別途設けている。したがって『全公開ローカルウェイトが一律禁止へ向かう』という単一の予測に依存して取得順位を決めない。実際のHub Gated・ライセンスタグ・作者のモデル削除や変更は、個別に観測可能なアクセスリスクである。

## 6. 変数表・次元確認

| 記号 | 意味（日本語） | 単位（SI換算） | 定義 | 定義域・前提 | 型 |
|---|---|---|---|---|---|
| `B_full` | R122の旧15source | byte（8bit） | 374,701,109,177 | 旧publisher scope、実空きではない | 非負整数スカラー |
| `B_saved` | 重複転送を避けたsource量 | byte（8bit） | 47,152,036,163 | 3モデルの既報告重量scope | 非負整数スカラー |
| `B_delta` | R125の修正後15source | byte（8bit） | `B_full-B_saved` | publisher固定source、物理純増ではない | 非負整数スカラー |
| `B_side` | 12付属ファイルの候補量 | byte（8bit） | 367,838 | 既報告weight SHA照合が前提 | 非負整数スカラー |
| `B_other` | 残る通常／高精度原本のsource | byte（8bit） | 327,548,705,176 | 全依存とstageを含まず | 非負整数スカラー |
| `F_min` | 取得中も残す最低空き | byte（8bit） | 200,000,000,000 | 保存媒体・staging・cacheに共通 | 非負整数スカラー |

**次元・整数計算**：374,701,109,177byte − 47,152,036,163byte = 327,549,073,014byte = 367,838byte + 327,548,705,176byte。メタデータのbyteを用いた正確な算術であり、現在のHDDの空き値や重複排除実効量の誤差区間を推定していない。

## 7. H/T/D/C/U・ERROR CHECK

**H**：重みが既に保存された3モデルについて推論関連の付属ファイルだけを補完すると、実ダウンロード量を抑えながら原本復元可能性を増やす。

**T**：v52全158有効資産と実行台帳62報告を一意突合。3モデルの同一revision／重みSHA／subset件数／byteの全組合せを検査し、一意解を確認。R125 15source、287ファイル、118 publisher SHA。模擬fileを用いる48回帰テスト、破損・権利未承認・リンク・hash不一致で逐次停止。

**D**：PASS＝catalogとpublisher metadata整合、模擬ファイルのfail-closed unit tests48/48。FAIL＝SHA欠損／不一致、ライセンス権限違反、D空き床割れ。UNCERTAIN＝実Dファイル物理存在・推論依存・offline restore。

**C**：61 VERIFIED報告が別ディスクに帰属していた、学習済み重みはあるがその他のコードが非互換、内部のQ4だけでは元BF16再生不能などの場合、取得順位と必要ファイルは変動。

**U**：台帳と物理ディスクの同一性、OSパス差、モデルカードの権利解釈、依存Python/CPU/GPU/ABIと量子化zero-pointが主要不確かさ。確率分布と反復標本が無いため`u_c`と包含係数`k`は数値化しない。

**ERROR CHECK**：v52 205登録/158有効、報告61＋Gated保留1＋未報告96＝158。R125の15sourceは元のv50 R122の15repoと同一、3sourceから12 sidecarsのみ抽出。287ファイル/118 LFS SHA/327,549,073,014byte。旧manifestへの影響なし。48/48 tests PASS。実重み新取得0、承認0、GitHub mainのみ。

関連分野：機械学習・アダプター互換性、デジタル保存・SHA内容同一性、OSファイルシステム、ソフトウェアサプライチェーン、モデル配布政策。

### 〈次に考える問い〉

**Dドライブで61モデルの重み・付属ファイルを実SHA照合し、最初に7.607MBの日本語評価データを保存できる環境を整えた後でも、57GB級の高精度派生チェックポイントを優先すべきか。**
