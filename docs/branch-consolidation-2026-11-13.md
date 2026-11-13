# ブランチをmainへ統合（2026-11-13）

目的：GitHub `Unjuno/local-model-portfolio` を今後 `main` 一本で運用する。古い調査ブランチのファイルを消さず履歴としてマージする。

- 元main `0e0dabe7ded9f775b91d860856051ce425ab4c09` (v19)
- 現行v31 `4ee1eaf6052f3ac97f83c001e3e0a04331b8554f` (`strategy/2026-11-03-01-risk`)
- 旧レビュー `3b12ec6bfe6979a3c9d371d5854f22e11d46276b` (`review/ai-model-selection-v3-2026-10-30`)
- 旧監査 `6e9389c97d24528df97e4b14a6bc772780141fd3` (`audit/specialized-tss-rights-2026-11-02`、既にmain/strategyの履歴に含まれる)
- マージ方法：元main・現行戦略・旧レビューを親に持つ複数親Gitコミット。フォースプッシュしない。
- ファイル：戦略側616件、main専有40件、レビュー専有45件を統合。旧ブランチにだけ存在した調査資料はすべて残した。
- 同名変更17件：v31の正式カタログ・判定ロジック・最新ポリシーを優先し、旧mainからR40〜R29の調査記録を補完。AGENTS/README/selection policyは両方の内容を統合した。
- 旧main側の重要な改善：`scripts/archive_preflight.py` は固定3.8TBではなく `policies/limits.json` の現行4TBを読み込む版、`tests/test_archive_preflight.py` と監視ワークフローを保持。
- 正本：`catalog/CURRENT.json` v31、179資産、有効132件、4TB計画・最低空き200GB。
- `queues/approved.json` は空。本マージでモデル重みの取得・同意・実行は行わない。
- 旧文書に残るv19等の集計は歴史値。以後の通常作業では `main` だけを更新する。

元ブランチはGit履歴で復元可能。不要参照の削除は全ブランチの取り込みを確認してからのみ行う。
