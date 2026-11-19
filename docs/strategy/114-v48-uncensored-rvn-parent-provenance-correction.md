# R114 — 無検閲27B原本への交換に必要な同一性の検証（2026-11-19）

## 1. 〈本論〉今回の選定判断

v48 201登録／154有効を維持。直前R113の『GGUFの代わりにFP16系原本を優先』は、**2系統で同じ証拠強度ではない**。Hugging Face公式Hubの各repoの`base_model`タグを再確認した。

| 系統 | 公開元の関係 | 現時点の判断 |
|---|---|---|
| InterpreticAI v2 | GGUFの`base_model:quantized`が`InterpreticAI/Qwen3.8-27B-Uncensored-v2`を明示 | 55.586GB Safetensors原本をマスター候補、17.738GB GGUFは実行用オプション。変換品質と依存は別途検証 |
| 0bserverx Heretic RVN | Safetensors側の`base_model`がGGUF repoを参照する逆向きタグ。GGUF側は`Qwen/Qwen3.8-27B`をbaseと表記 | **RVN-Q4をSafetensors原本に無条件交換しない**。RVNが13 shard原本から変換されたことの証拠が必要 |

0bserverx RVN multilingual GGUF（16,547,400,224 byte本体、projector別）は、旧Heretic GGUFとは別の後処理結果として作者が説明する。別Safetensors 13 shardがこのRVNの正確な変換前学習済み状態であるかは不明。**似た名前・同一モデル系列・両方Apacheタグ**だけではチェックポイント同一性の証明にならない。誤交換により唯一のRVN版を保存対象から落とすことを避ける。

新しい[機械可読の同一性停止判定](../../catalog/decisions/2026-11-19-r114-uncensored-provenance-stop.json)をmainに追加。前回の[FP16原本source候補](../../manifests/drafts/r113-v48-two-uncensored-original-fp16-parents.candidate.json)は候補として維持し、GGUF選択キューや承認キューを勝手に書き換えない。

## 2. 証拠・残る最小検証

公式モデルカード：[Interpretic FP16](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2)、[Interpretic GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF)、[0bserverx Safetensors](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored)、[0bserverx GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)。公開元revisionとLFS SHAは既存の固定マニフェストにあるが、**同一性のtensor比較は未実施**。

0bserverxでは固定版の`artifact-manifest.json`と`export-receipt.json`、README、量子化元のモデル識別子、GGUF metadataを照合し、正確なRVN学習成果と13 shard原本の変換経路を特定する。証拠が不足した場合は両方を『独立成果かもしれない』として研究保持し、両方の重量ダウンロードはしない。本人の権利・4TB容量・ABIを先に満たす。

## 3.〈応用・転用例〉

機械学習：量子化前後の同一性を作者名ではなくtensor provenanceと変換再現性で判断。デジタルアーカイブ：重みの内容アドレス・revision・由来を保存。ソフトウェア供給網：メタデータの逆参照や誤登録を検出。情報法：モデルカードのライセンスタグと取得・再配布許可を別管理。

## 4. H/T/D/C/U と ERROR CHECK

- H：0bserverx RVN-Q4は13 shard Safetensorsと同一編集結果である、という仮説は未立証。
- T：固定版README、export receipt、GGUF内部メタデータ、原本shardのtensor identityを検証。モデルpayloadを伴う比較は本人の正規アクセス・容量・承認後に実施。
- D：PASSは作者の具体的変換元SHAと再現変換・量子化誤差範囲を確認した場合。FAILは別の学習済み編集結果が明示された場合。現時点はUNCERTAIN。
- C：作者のHub`base_model`タグが誤っていて、実際にはRVNと原本が同一の可能性。
- U：GGUF量子化の丸め・zero-point、backend、runtime ABI、原本tensor同一性。実測標本なしのため合成標準不確かさu_c・包含係数kは算定しない。

**ERROR CHECK**：v48 201/154、正式入替0、approved0、重み取得0。既存R113の109.397GBは候補sourceであり、RVN-Q4を削除できる証明ではない。

### 〈次に考える問い〉

『FP16だから原本』という形式上の分類より、**そのFP16が保存したい編集済み重みの正確な元データか**を確認する方が、長期保全では優先されるべきではないか。
