# R153 — v65: 112件取得報告との照合と独立無検閲DPO原本の追加 (2026-11-22)

## 結果
ユーザー取得側の台帳 [ledger](catalog/execution/2026-11-19-acquisition-ledger.json) は**112 VERIFIEDモデル／1,714ファイル／2,020,548,143,087byte**を報告。旧v64の236正本とID突合すると未登録は**Timestral-5M、WeMM-Video-2Bの2件のみ**。両原本のpublisher SHA、固定rev、全33file **6,611,554,027byte**は台帳のrevision/bytesに一致。新たに転送せず正式CONDITIONALとして記録した。

追加選定する [Smaug-Uncensored](https://huggingface.co/abacusai/Smaug-Uncensored/tree/e4bbcf7aec54ab72f4ce720569f3b3dc7b973087) はQwen3.8-27Bの**独立DPO+NLL微調整済みBF16**原本。ハッシュ調査[原資料](manifests/drafts/r153-2026-11-22-smaug-qwen-hash-reuse-and-atomic-lora.candidate.json)で、公式Qwen親18 shardと比べ**2 shard (5,934,994,296byte)はSHA完全一致、16 shard (49,628,012,480byte)は異なる**。Smaug32全file55,586,070,091byte。16個の異なるファイルにも同一tensorはあり得るため、異なるbyteの全量を「独立情報量」とは見なさない。作者OR-Bench-Hard1,309件で過剰拒否45.2%→2.3%の報告。独立評価なし。可逆な独立DPOアダプターは検証できない。

これら3モデルを **CONDITIONAL**。旧236件の記録/判定を一切変更しない。現在**239登録／192有効、SELECT55/CONDITIONAL137**。AtomicChat Inkling LoRA43.805MBは別編集だが作者MMLU2,000問80.65%→79.15%（McNemar p=.006）を報告し、GGUFのPR#32694互換性不明のため研究HOLD。

## 取得停止と実機要件
`queues/approved.json`は0件。ユーザー媒体Dの本回の実ハッシュ再検査なし。前記112件は取得ツール側VERIFIED報告であり、本人個別ライセンス行為の認可や全依存オフライン復元の検証ではない。Modified MIT (Timestral5Mの雇用主/企業月商USD20m制限)、Tencent第三者ライセンス、Smaug Apache2とNOTICEの権利・現物SHA・4TB/残床200GB/staging・backend/zero-point/adapter/KV cache/context/batch・モデル推論コード監査・明示モデルmanifest承認を満たさなければ、**新規DL停止**。許可を合成しない。既存モデル削除なし。

将来のモデル規制は予測シナリオであり、米BIS [2026-11-19 Federal Register IV.A](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm) のECCN4E091撤回と一般open weights所持禁止を混同しない。

**H**：正本に未登録だった取得報告2件は無転送で整合可能、Smaug独立DPO成果はシャードSHA16件が親と異なる。**T**：112台帳を正本IDに突合、各ファイルSHA/byte、旧236件不変、192 activeのqueue/prep/readinessと137 conditionalのaccess集合一致、承認0。性能の検証は固定HW/driver/backend/context/batchで≥30ケース。**D**：メタデータPASS、実媒体/許諾/復元/速度 UNCERTAIN。**C**：保存親の現物SHA違い、Smaug性能劣化、WeMM patch incompatibility。**U**：owner実体とPublisherメタの差、モデル作者ベンチの偏り、未計測RAM/VRAM。合成標準不確かさu_c・包含係数kは算定不可。

関連：DPOモデル学習、時系列予測、映像音声統合、サプライチェーン検証、輸出・著作権法、GPU実行コスト。

**ERROR CHECK**：既存236件保持・239 unique・旧112 VERIFIED IDすべて対応・192 active・137 conditional・approved0。今回モデル本体取得・コード実行・D媒体変更0。
