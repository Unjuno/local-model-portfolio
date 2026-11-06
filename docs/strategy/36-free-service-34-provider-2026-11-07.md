# 36 — 無料tier34サービスとモデル保全Tier16資産（2026-11-07）

## 設計と出典
- 調査対象: 事業者の無料GPU・CPU・推論API・小容量クラウド保存。新規5社は2026-11-07に公式一次資料で確認。
- [34サービス機械可読CSV](../../catalog/research/2026-11-07-free-services.csv) ／ [16資産保全優先度CSV](../../catalog/research/2026-11-07-preservation-tiers.csv)
- 元の監査：[34版](34-free-tier-factcheck-2026-11-07.md)／[35版](35-free-tier-continuing-2026-11-07.md)。
- CURRENT v26=172管理・125有効、既知の論理重複排除後3,403,245,899,240 B、外部依存34資産。完備オフライン容量・本人の実ディスク空きはUNKNOWN。

## 新規5サービス：無料枠、条件、正確な出典
|事業者|無料枠（公式）|制限|無料tier|根拠|
|---|---|---|---|---|
|Requesty|無料モデル200 requests/日|カード不要。ただしモデル集合変更可能、推論のみ|A|https://www.requesty.ai/pricing |
|Speka|$1/月の推論割当・10RPM|超過分は従量料金、API推論のみ|B|https://speka.me/ |
|Aion Labs|20,000 tokens/日・15RPM|日次クォータはトークン数。モデルウェイト保有権は付与しない|B|https://www.aionlabs.ai/docs/rate-limits/ |
|Typhoon|研究用API無料。例: typhoon-v2.5-30b-a3b-instruct 200RPM|日次/月次トークン上限UNKNOWN。利用データ改善利用あり|B|https://docs.opentyphoon.ai/en/faq/ |
|OVHcloud AI Endpoints|匿名Playground 2RPM/IP/モデル。Public Cloud trial $200は1か月|本番APIのキーはカード/クラウドプロジェクト必要。継続無料の証明なし|C|https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-endpoints-getting-started |

## 公開停止事例の厳格な分類
OVHcloud公式ライフサイクル台帳は **BGE-Multilingual-Gemma2** の提供APIについて 2026-10-21の退役通知、2027-01-21終了予定を記載する。**これはホスト型APIの退役であり、オープンウェイト原本が削除されたことを意味しない**。
公式: https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-endpoints-billing

## 結論・不確定事項
- 今回確認した無料枠の集合に、約3.403TBの重みと依存を独立・継続・権利適合の状態で無料保存できるサービスは**確認できない**。
- free trial・初回クレジットと定期更新を区別。APIへのアクセスは学習済み重みの保存・再配布権とは異なる。
- 同じ登録者でも地域、利用契約、無料対象モデル、決済設定、終了日で利用条件が変わる。本人の契約とダッシュボードを見ていないためUNKNOWN部分を残す。
- S/A/B/C/HOLDの無料サービスtierと、学習済み独自能力の保全tierは別の評価軸。

## H/T/D/C/U
- H: 公式無料枠の記載が無料アカウントの現在条件に一致する。
- T: 各行の公式URLに再訪、本人が承認する場合のみ実際のアカウント上限を無課金で確認。変更履歴を保存。
- D: PASS=公式＋本人条件一致、FAIL=カード/課金/地域不適合、UNCERTAIN=未ログイン・上限変更・ソース曖昧。
- C: trialの継続無料扱い、匿名Playgroundを有料APIの無料枠と混同、モデルAPI停止をウェイト削除と混同。
- U: ライセンス・サービス運用・地域・カード条件・クォータ可用性。実測分散不足で合成標準不確かさは未算定。

## ERROR CHECK
上記は公開情報の静的監査であり、利用者のクラウド課金、モデル重量のダウンロード、Gated回避、実ディスク容量測定を行っていない。モデル選定はv26のまま、172資産/有効125件、main/承認キューを変更しない。今回追加するファイルは調査資料とCSVのみ。
