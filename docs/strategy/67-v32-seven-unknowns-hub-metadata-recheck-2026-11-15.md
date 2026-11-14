# R67｜v32 有効7モデルの配布元メタデータ再照合（2026-11-15）

## 1.〈本論〉対象と結論

正本 `main` v32（182登録／135有効）の[前回R66](66-seven-parameter-unknowns-source-bound-audit.md)で総数未確定とされた**7件**を、接続済みHugging Faceの`hub_repo_details`で一次配布者メタデータ再照合した。メタデータ表示の「Parameters」は主モデルや表示対象の一部であり、外部Codec・Encoder・VAEを含む完全な学習済み依存グラフを証明しない。したがって**7件の総数UNKNOWN・最終lock停止を変更しない**。今回モデル重みやpickle、依存コードは取得・実行していない。

| repo ID（一次配布元） | 今回確認した表示・ライセンスメタデータ | 未解決の完全性・取得ゲート | 判断 |
|---|---|---|---|
| [PrunaAI/P-H3-Image](https://huggingface.co/PrunaAI/P-H3-Image) | 公開メタデータ33,123.0M、`license:other`。R66の15 safetensorsヘッダー合計49,635,347,496要素とは測定対象が異なる | 15ファイルの外部学習済み依存閉包・MiniMax H3関連の契約、実機ABI | **HOLD**：表示33.123Bを完全総数としない |
| [maya-research/maya2-native](https://huggingface.co/maya-research/maya2-native) | 公開メタデータ2,502.4M、Apache-2.0タグ、Mimiタグ | ECAPA学習済みspeaker encoderの原本revision・テンソル数・ライセンスと必須性 | **HOLD**：主モデル2.502Bは全依存総数ではない |
| [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3) | 公開メタデータ35,899.6M、`license:other` | `codec.pth`はpickle形式。コードを実行せずに静的に安全に確認できる依存総数とFish Audio Research License本文 | **HOLD** |
| [WhissleAI/steer-tts](https://huggingface.co/WhissleAI/steer-tts) | **Gated**、表示9.6M、CC-BY-NC-4.0タグ | 外部Vocos/WavLM/MiniLM、本人Gated許可、商用利用制限、実行版の固定 | **HOLD** |
| [ausboss/Qwen-Image-2.1-Consistency-LoRA](https://huggingface.co/ausboss/Qwen-Image-2.1-Consistency-LoRA) | LoRA・親`Qwen/Qwen-Image-2.1`タグ、`license:other`、モデル全総数の表示なし | LoRA別SHAと親・Encoder・VAEの完全依存、各利用条件 | **HOLD** |
| [ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | `gguf`・`base_model:quantized:Lightricks/LTX-2.5`タグ、**`license:unknown`** | 実際の派生学習差分と単なる量子化の区別、元LTX・Gemma encoder・VAE・ライセンス | **HOLD**：量子化タグは独立学習済み原本の証拠ではない |
| [Stuubs/Stubelius_Remix_Ltx2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5) | `gguf`・`base_model:quantized:Lightricks/LTX-2.5`タグ、`license:other` | 元LTXとの差分学習の一次証拠、学習済みEncoder/VAEの総数と許諾 | **HOLD** |

**重要な反証:** ChrisColeTechとStuubsの両モデルは配布元の現行タグで`base_model:quantized`と表示される。これだけで特殊な独立学習済み版と認定して保存枠を二重配分してはいけない。一方、同一重み・単純量子化とも未証明なので、証拠なく削除しない。最短の次工程は親と派生の**固定リビジョン・テンソル構成・モデルカードの変更履歴**を突き合わせ、通常量子化か新たな学習成果かを判定すること。

## 2. ソースの限界と最新性

このラウンドの一次情報は2026-11-15に接続済みHugging Faceアプリで照会したモデル一覧メタデータであり、各カードの更新表示は主に2026-10-15〜11-08。取得権限、repo内全ファイル、最終ライセンス本文、実機動作の確認は**未実施**。Exa検索はクレジット上限エラー（402）のため本ラウンドでは取得できず、Exaで新たに検証したとは主張しない。政策変更の一次出典は既存の[01調査](01-regulation-risk.md)を参照。今回の照会はR66の結論を反転させる新証拠を与えていない。

## 3. 完成判定の非補償型ゲート

1. 7件の**全学習済み構成要素**（MoEは非活性expertも含む）と選択形式を固定し、総パラメータを一次証拠で確定。超150B量子化例外は現行方針に従い、同一条件・実測の同等RAM比較なしに承認しない。
2. Gated本人権限、第三者の個人データ・音声同意、ライセンス正文・親モデル条件を確認。表示がpublicでも無条件の利用許可ではない。
3. 完全40桁revision、必要シャード・外部Codec/Encoder/VAE・SHA-256、増分容量、cache/staging、実HDDの空き200GBを確認。
4. 固定manifestごとに利用者の明示承認を取得。現時点で`queues/approved.json`は空。**調査完了≠取得可能≠オフライン復元可能**。

## 4. H/T/D/C/Uと変数表

| 記号 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| N | 対象の総数未確定モデル | 1（件） | 7件、v32 active | 整数スカラー |
| L | 標準の全モデルパラメータ判定境界 | 1（個） | 150,000,000,000。例外には別途量子化RAM実測が必要 | 整数スカラー |
| S | Pruna15ファイルの保存テンソル要素数 | 1（個） | 49,635,347,496、R66ヘッダー検査値 | 整数スカラー |
| E | 外部必須学習済み部品の要素数 | 1（個） | 未確定、非負整数またはnull | 整数スカラー/null |
| P | 完全パイプライン要素数 | 1（個） | S+E。EがnullならPも未確定 | 整数スカラー/null |

次元チェック：SとEは無次元の要素数なので加算可能。Hubの`Parameters`表示とモデル重みbytes、実行時RAMは異なる測度で、直接比較しない。

**H:** 配布元メタデータの主モデル数だけでは7件の全依存総数を確定できない。**T:** 7/7のrepoを照会、固定revisionと外部学習済み部品を次回1件ずつ照合、最小n=7。**D:** 全数・権利・SHA・容量・実機・承認が揃うまで取得FAIL/UNCERTAIN。**C:** 別学習済みCodecが存在する、量子化を特殊学習と誤認する。**U:** 未知の依存と本人許諾が主要誤差源、分布不明のため合成u_cと包含係数kは数値化不能。

**ERROR CHECK:** 対象7/7のIDをR66と照合。総数unknownからPASSへの昇格0、選定変更0、承認0、モデル本体ダウンロード0、コード実行0。

関連分野：機械学習（パラメータ総数）、ソフトウェア供給網（依存閉包とSHA）、知的財産法（派生元の許諾）、デジタルアーカイブ（重複を避けた長期復元）。

## 5.〈次に考える問い〉

7件のうち、固定ファイルの静的ヘッダーと公開ソースの参照グラフだけで、追加の外部学習済み依存を最初に閉包できるのはどれか？
