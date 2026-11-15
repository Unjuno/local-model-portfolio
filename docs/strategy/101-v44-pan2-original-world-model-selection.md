# R101 — v44: IFM/PAN2原本の条件付き保存選定（2026-11-15）

## 1.〈本論〉実際の原本・独自性による追加決定
v43の195資産を変えず、`IFM/PAN2`を**研究段階conditional**として1件追加。v44は196資産・149 active（model170、dataset26）。[公式HF原本](https://huggingface.co/IFM/PAN2)は独立学習の29.202B双流MMDiT。Wan2.2通常T2V、Cosmos3自動運転・双腕世界モデル、Praxis DROIDアクションとは異なる、時間・行動・構造化世界状態→視覚未来予測という別の学習成果を保全する。単なる量子化複製ではない。一方、作者ベンチ300単一動作・200複数計画プロンプト・140人間評価プロンプトは第三者独立検証でない。

[immutable HF API](https://huggingface.co/api/models/IFM/PAN2/revision/82f54c6cea3e20a9c451b61d7360016e5970503d?blobs=true)から52ファイル **86,174,243,428 byte**を照合。[固定35ファイルマニフェスト](../../manifests/drafts/v43-2026-11-15-pan2-original-source.candidate.json)は**86,082,094,058 byte**。除外はデモassets17ファイル92,149,370 byte。学習済み原本19ファイルの配布元LFS SHA256を固定：
- Transformer原本14 shard **67,369,648,792 byte**
- 凍結Qwen3.5-9B encoder4 shard **15,873,415,904 byte**
- Wan2.2 VAE原本1 shard **2,818,777,808 byte**

Wan VAE SHA256 `62cd18f19438e35b32ac63020e2852f566e9b02f46b6cdbd87972a356e3c6f4b` は公式[Wan2.2 Diffusers版](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B-Diffusers)と一致するが、**既保存計画にあるWan2.2 native .pthのSHAは異なる**。したがって現地HDD重複控除は未確認・0とする。Qwen3.5encoder重みは当該PAN2 HFスナップショット内にあり、他repoの二重取得は不要。

コードは[IFM PAN2 固定コミット](https://github.com/ifm-ai/PAN2/tree/0fb907b6e16a82ead6d691d1de2eef6299c71e9a)、[Apache-2.0](https://github.com/ifm-ai/PAN2/blob/0fb907b6e16a82ead6d691d1de2eef6299c71e9a/LICENSE)、[Wan/Qwen第三者ライセンス](https://github.com/ifm-ai/PAN2/blob/0fb907b6e16a82ead6d691d1de2eef6299c71e9a/THIRD_PARTY_LICENSES)を保全対象とする。別系統の概念reasoner LLM、推奨Qwen3Guard/Q16 safety checker、コード環境PyTorch2.12/CUDA13.2は完全offline再現の前に追加検証する。本人実機は未検証。

## 2.〈応用・転用例〉保存交換の却下・保留判断
| モデル | 今回判定 | 原因 |
| --- | --- | --- |
| **IFM/PAN2** | conditional追加1 | 原本29.2B独立汎用行動シミュレータ、固定35ファイル |
| [Edge0/Edge0-145B-q3k](https://huggingface.co/Edge0/Edge0-145B-q3k) | HOLD | 145Bの別学習済みlatent-MoEは興味深いが、原本約105GBと必須学習済みPLE、Edge0/Qwen複合ライセンス、CUDA13/SSDストリーム実測、主family120Bとの重複が未解決 |
| [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | HOLD | 204GB原repoの2表現重複と27B prompt enhancer、地域・AUP契約条件とPruna P-H3既採用版との増分が未検証 |

単一の量子化形式を並列採用せず、原本と独立学習成果を優先。将来の規制拡大は仮説で、open weights一般禁止が確定したとする証拠ではない。[豪州ASDの2026-11-05公式open-weightガイド](https://www.cyber.gov.au/publication/open-weight-ai-models-opportunities-and-cyber-security-risks)は出自・hash・隔離・安全運用を推奨するが禁止法ではない。>=150Bは正式方針に厳格な量子化実測例外があり、当該PAN2はそれを使わない。

## 3. H/T/D/C/UとERROR CHECK
H: PAN2は既存世界モデルと違う構造化行動シミュレーション原本。T: 独立HF 52元ファイル35 selected＋19publisher SHA、公式ライセンス、現在の195件を保持して静的検算。D: 非重複のconditional選定PASS、本人の取得承認・容量・SHA/ABI・offline restoreはUNCERTAINとして停止。C: 重み同一、親の権利不適合、他の選定済みモデルへの実質重複が後に立証されればHOLD。U: 本人HDD実測・派生ベンチ・guardrail・source code/wheelの完全なオフライン依存、端末HWでのレイテンシ/品質は未測定。u_cや拡大規制の確率は推定しない。
ERROR CHECK: **196 unique/149 active/95→96 conditional/53 select/20 observed gated/unknown total active9/approved0**。byte数は整数byteで集計し4,000,000,000,000byte計画枠と200,000,000,000byte最低空きも同一単位。ただし現在の使用済み・空きHDDは未測定のため容量合格と判定していない。

## 4.〈次に考える問い〉
次の追加モデルより、PAN2と既登録Cosmos/Praxisの依存ウェイトをSHA単位で共通化して、正確な空き容量をどれだけ確保できるか。
