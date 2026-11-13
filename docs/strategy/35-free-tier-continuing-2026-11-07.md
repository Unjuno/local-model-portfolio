# 35 — 無料tier継続調査：一次資料に基づく訂正・新規サービス（2026-11-07）

## 正本
GitHub CURRENT.json は v26-20261106、172資産・有効125件。重複排除後の既知一次ファイル容量は3,403,245,899,240バイト、一次ファイル総和3,406,271,632,830バイト。34資産の外部依存等は未解決で、所有者の物理ディスク空きと完全オフライン復元容量はUNKNOWN。4,000,000,000,000バイト計画枠との差額596,754,100,760バイトを実際の空きとは扱わない。

## 公式照合した無料サービスの差分

| サービス | 2026-11-07の公式確認結果 | 無料tier判定 | 出典 |
|---|---|---|---|
| Hugging Face Inference Providers | Free Users は月 $0.10 クレジット、変更可能。旧Deep Researchの $0 と矛盾。ウェイト取得権はない | B | https://huggingface.co/docs/inference-providers/pricing |
| SambaNova Cloud | Freeプランの初回API使用には支払方法の追加とクレジット購入が必要 | HOLD / 無課金API不適 | https://cloud.sambanova.ai/plans |
| Mistral | Free ModeはVibe・Studio用。APIにはbilling activation が必要 | HOLD / 無料API対象外 | https://docs.mistral.ai/admin/billing-usage/usage-limits |
| GitHub Models | 2026-07-30にplayground・API・BYOKも全面終了 | 終了 | https://github.blog/changelog/2026-07-30-github-models-is-now-retired/ |
| Modal Starter | 月$30の無料compute credits。Shared Endpointsには使えない | A / computeのみ | https://modal.com/pricing |
| Lightning AI Free | 初回5 credits＋カード登録で25 credits。12か月で失効し毎月30追加ではない。無料ストレージは10GB | B / 初回のみ | https://lightning.ai/pricing |
| OpenRouter :free | 50 req/日・20 req/分。$10購入後の日次上限増は無料登録枠とは別 | A / 無料推論 | https://openrouter.ai/collections/free-models |
| Cloudflare Workers AI | 10,000 Neurons/日・0:00 UTCリセット、一部大型モデルはPaidのみ | A / 無料推論 | https://developers.cloudflare.com/workers-ai/platform/pricing/ |
| IteraCompute | 30M tokens/月、Qwen3.8-27B無料プロモは11月24日 0:00 PT 終了予告 | C / 期限付き | https://iteracompute.com/pricing/?lang=en ; https://iteracompute.com/?lang=en |
| Venice Free | UIでは10 text prompts/日と15 image prompts/日。APIは支払クレジットが必要 | C / UI無料のみ | https://venice.ai/pricing |
| Scaleway Generative APIs | 新規顧客1M tokensと60分の音声文字起こしが無料。更新周期UNKNOWN、カード/KYC必要 | C / 初回または期限不明 | https://www.scaleway.com/en/generative-apis/ |
| Infomaniak AI Services | 初回1M credits、以降は従量課金。カード本人確認あり | C / 初回のみ | https://www.infomaniak.com/en/hosting/ai-services |
| AI Horde | ボランティアによる無料生成。可用性・SLA保証なし、重みは利用者に残らない | B / デモ向け | https://aihorde.net/mission/ |
| LLM7.io | 旧レポートの100K tokens/24hは今回の一次ページで再確認できず | HOLD / UNKNOWN | https://llm7.io/ |

## 重要な誤記と保全判断
過去のDeep Researchが記載したHF Free Inference Providers月額$0という値は、現在の公式価格表の月額$0.10と矛盾するため訂正する。無料プランとカード必須を併記するSambaNova、Mistral Free UIとAPI、Lightining初回クレジットと毎月補充、GitHub ModelsとGitHub LFSを混同しない。
これらの無料枠はクラウド上の推論・短期計算・少量のメタデータ複製に限られ、3.403TBの独立かつ合法・永続的なウェイト保全には使えない。無料GPU/APIは配布・取得・再配布に必要なモデルごとの権利を付与しない。
モデル保全Tierは以前のdocs/strategy/34-free-tier-factcheck-2026-11-07.mdに維持。ERNIE5.5 Flash BaseやOrcaRouter GLM-5.3 Flash量子化例外は実測RAM・許諾条件が揃うまでHOLDであり、既存v26選定数を更新しない。

## H/T/D/C/U
- H：各公式無料枠が本人の国・プラン・課金設定で利用できることは検証可能だが、永続性は未証明。
- T：公式料金表と利用規約を確認し、本人による課金のない範囲でサービス内実際のクォータを再照合する。第三者のモデルウェイトは移動しない。
- D：PASS=公式と本人条件が一致。FAIL=料金・契約に不適。UNCERTAIN=本人ダッシュボード、リセット周期、無料枠の維持が不明。
- C：UI無料とAPI無料を混同、期間限定を永続扱い、実行環境を物理保管容量扱い。
- U：価格・地域・クォータ・モデル別制限・契約変更が主要不確かさ。経験分散不足で合成u_c・係数kは算出しない。

## 実行履歴
この文書は専用ブランチの証拠追補のみ。取得承認変更なし、重みダウンロードなし、クラウド課金なし、所有者HDDアクセスなし、main変更なし。今回の追補について新規CIは未実行。従前v26のCIを今回の実行と称さない。
