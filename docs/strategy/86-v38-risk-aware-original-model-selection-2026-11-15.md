# R86／正式v38：公開制限リスクに備えた独立学習済み原本2件の選定見直し

調査日：**2026-11-15**。対象：GitHub `Unjuno/local-model-portfolio` の `main`、v37の191資産／有効144件からの判断。**結論：新2資産をCONDITIONALで選定、v38で193資産（167モデル・26データセット）／有効146件、SELECT53／CONDITIONAL93。** 旧191資産を不合理に削除しない。**実ファイル取得・自動実行・Gated許諾・ダウンロード承認0件**。

[正式選定差分](../../catalog/revisions/v38-2026-11-15.json)／[v38全193資産](../../catalog/effective-portfolio-2026-11-15-v38.json)／[有効146非実行キュー](../../queues/proposed-v38-2026-11-15.json)／[有効146保全依存](../../catalog/preparation/2026-11-15-insurance-bundles-v38.json)／[R84実物構造と全メタデータ](../../catalog/research/2026-11-15-r84-haru-praxis-original-source-and-dependencies.json)／[43選択ファイルの固定一次原本候補](../../manifests/drafts/v38-haru-praxis-original-selected-source.candidate.json)。

## 1.〈本論〉— 目的と実際の学習済みモデル

**目的は、将来のGated化・削除・配布条件変更があっても、法令・ライセンスとアクセス条件に従って独自モデルを再取得困難となる前に保存できるよう、選定対象と復元に必要な依存物を決めること。** 単純にパラメータ数やダウンロード数を増やさない。既存と同一学習済み重みの別量子化、同族の不要なサイズ違いを自動で追加しない。逆に異なる学習済み能力があれば、同じタスク系統でも独立性を検証する。

### 今回の正式追加：2種類

| 配布元（原本） | モデル中身を実際に照合した結果 | 採否 |
|---|---|---|
| [higurashi-ai/Haru-4B](https://huggingface.co/higurashi-ai/Haru-4B) | 公開元SHA`8d6e83bcd3701a76fc27a764965665da1df7da78`。**7ファイル・10,560,190,159 byte**。Qwen3.5系32層＋入力/出力音声投影＋one-step MeanFlow音声head＋VibeVoice式音声codecを**一体に学習・1 checkpointに内包**。24kHz/3,200 samples×7.5Hzの全二重speech-to-speech。Hub総パラメータ約5.27B、Apache-2.0、現在public ungated。 | **CONDITIONAL追加**、S1仮説、重み原本1系統 |
| [runwayml/praxis-1-droid](https://huggingface.co/runwayml/praxis-1-droid) | 公開元SHA`6bb70750663e53592cc38f46e531a5a01a12d291`。**23ファイル・54,404,890,103 byte**、17個のBF16 shardと`SHA256SUMS`。総パラメータ約27.2024BはMoE**全expertを含む**。動画生成DiTのchunk-causal状態＋学習済みaction expertが、DROIDアームの動画・動作を一緒に予測。現在Hub **Gated auto**、匿名`config.json`は401。 | **過去のHOLDからCONDITIONAL研究選定**、S2仮説、合法アクセス確認前の取得禁止 |

### 原本と外部学習済み依存の確定

Haruの唯一の重み本体`model.safetensors`は**10,540,113,510 byte**、配布元Xet SHA256 `ad2c3534ef6bd88525e22e5da3ac4fb739368406bf3b1c852cbafbade647c0fa`。モデル本体の`config.json`は`model_type=haru`、`sample_rate=24000`、`frame_samples=3200`、`frame_rate=7.5`、`latent_dim=64`、`head.num_steps=1`。作者の[固定コード](https://github.com/higurashi-ai/Haru/tree/7fe6b7665f8bf035998f401f8cb779fbe53f2751)の`pyproject.toml`はPython≥3.10、torch≥2.6、transformers≥5.16。他社の[VibeVoice MIT等の第三者通知](https://github.com/higurashi-ai/Haru/blob/7fe6b7665f8bf035998f401f8cb779fbe53f2751/THIRD_PARTY_NOTICES.md)がある。**学習済みcodecはこの原本に含まれ、別VibeVoice原本をモデル依存として二重選定しない**。音声の参照クリップは本人の同意済み・権利を有する素材のみ。

Praxisの一次計算構造は[Runway技術報告](https://runway.com/research/praxis-1-video-pretraining-to-robot-control)と[固定推論コード](https://github.com/runwayml/praxis-1-oss/tree/afef2e18a0af22b2e9926e9f743dc4694ab8b6b5)に基づく。**全17個の分割重みの公開SHAをR84で記録**した。ただしGatedのため実ペイロードのtensor headerを匿名で閲覧・実行したとは主張しない。Python≥3.12、torch≥2.13、transformers**5.2.0固定**、CUDA13、作者想定GPU VRAM≥80GB。**保存**と**この環境での実行可否**は別判定。

Praxisの必須外部学習済み依存は以下のとおり。
- [Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) の`Wan2.2_VAE.pth`：旧ポートフォリオで選択済み。公開元固定rev`921dbaf3f1674a56f47e83fb80a34bac8a8f203e`、**2,818,839,170 byte**、SHA256 `20eb789667fa5e60e7516bf509512f6cb61f01b0aa0695eadaea930c13892b36`。現時点では同じ公開元ファイルとして**追加source計上しない**。実HDDに同一物があることは未検証。
- [Qwen/Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B)：学習済みテキストencoderの**追加依存**。固定rev`15852e8c16360a2fea060d615a32b45270f8a8fc`、**13ファイル・4,571,274,023 byte**。**ポートフォリオの独立148番目の有効資産として数えず**、Praxisに紐づく必須依存として固定。選択対象とモデル評価を混同しない。

### 重複・入替の判断

- **Praxis-1 Baseは追加しない**：身体化専用action headがなく、選定目的は実行可能なDROIDのjoint video-action学習済み重み。**YAMは別学習版**だが、別ロボットの実験が未確定の間に約54GBの同系統重みを二重保存しない。NVFP4 QATも通常の量子化複製と異なる再学習成果を持つが、BF16原本を置き換える同条件品質・エラー/ABI比較がない。
- **現在のCosmos3 Sim-Bimanual・Sim-Auto、GR00T、Alpamayoは保持**：それぞれ世界シミュレーション、車両行動、汎用ロボットVLAの学習済み対象・出力定義が異なる。作者報告のRoboLab-120 **46.2%（1,200 episodes）対Cosmos3 Nano36.8%**は同一課題の作者比較だが、学習セット汚染・ハード・クロック・独立再現が未確認であり、既存モデルを除外する十分な根拠ではない。
- **Haru vs Qwen Omni/ZONOS3**：Haruは入出力音声の**同時生成**、Omniは多モーダル、ZONOS3はTTS。実際に同等品質の全二重対応が証明できない限り、別原本として保持。
- **GLM-5.3-Flash**：公式公開総数**320B**、活性**18B**。150B判定には活性ではなく全expertを計数。ユーザーの150B超量子化例外条件（実測peak RAM、同一HWでの品質・速度）未充足につき通常選定に追加しない。
- **Underdog Woof**：英語の固定少数話者TTS約38.24M。既存TTS原本と役割が重複するうえ独自非商用条項・再学習制限があるため、今回の追加選定の利益は弱い。

## 2. 規制リスクの事実と仮説の分離

**事実**：[欧州委員会AI Act執行概要](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act)では**2026-08-02**からGPAI提供者への義務執行が始まり、重大な不履行にモデルの市場提供制限・撤回・リコールもあり得る。一方、[Article 53](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53)では一定のオープンソース例外があり、**全公開ウェイトの一律禁止ではない**。[Australian Cyber Security Centreの2026年報告](https://www.cyber.gov.au/publication/open-weight-ai-models-opportunities-and-cyber-security-risks)は公開重みのセキュリティリスクと適切な統制を説明するが、対象モデルの将来の法的禁止を宣告していない。**Runway Praxis-1のGated autoは現行配布事実**、Haruは現在public。Gatedは直ちに政府規制が原因だという証拠ではない。

**仮説**：S1＝音声・顔・安全制御変更／S2＝高度自律ロボット・科学／S3＝公開ウェイト全般への提供制限波及。観測期間・無作為サンプル・分布がなく「1年以内に規制される確率」等は推定できない。選定調査順位には用いるが、合法アクセス権を上書きしない。今後同じrepo revision/公開状態/Licenseを差分観測する際は「Hub管理者によるGated化」と「法律の施行」を別事象として符号化する。

## 3. 完全保存に必要な検査

[新規43参照候補](../../manifests/drafts/v38-haru-praxis-original-selected-source.candidate.json)は**コードを実行せず全pathを選定**。新2原本は7＋23＝30件、別依存Qwenは13件。既存Wan VAEは選定済みのため増分のsource単純加算から除く。**重みの公開元SHAが得られていてもローカルSHA・端末空き・ユーザー固有のGated権利は全件未検証**。単純な`hf download`全repo実行や、モデルコードをimportすることでの暗黙取得は禁止。

| 記号 | 意味（日本語） | SI単位 | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| `B_h` | Haru原本公開元容量 | byte | 10,560,190,159 | 固定rev7ファイル・未実測 | 非負整数スカラー |
| `B_p` | Praxis DROID原本公開元容量 | byte | 54,404,890,103 | 固定rev23ファイル・Gated | 非負整数スカラー |
| `B_q` | Qwen3.5-2B必須依存の公開元容量 | byte | 4,571,274,023 | 固定rev13ファイル | 非負整数スカラー |
| `B_w` | 既存Wan VAEの共有候補容量 | byte | 2,818,839,170 | 旧選定source同一SHA、実HDD未照合 | 非負整数スカラー |
| `B_{Δ}` | 重複VAEを除く新たなsource候補容量 | byte | `B_h + B_p + B_q = 69,536,354,285` | 所有者HDD上の真の増分ではない | 非負整数スカラー |
| `C` | アーカイブ計画容量上限 | byte | 4,000,000,000,000 | 実HDD空きではない | 非負整数スカラー |
| `F` | 最低限の必要実空き床 | byte | 200,000,000,000 | 実機上で検証 | 非負整数スカラー |
| `N` | 現行の有効選定 | 1（件） | 146 | v38正式選定 | 整数スカラー |

**次元チェック**：`B_h`、`B_p`、`B_q`はbyteなので加算可能。全expert総パラメータ数、ファイル件数、GB VRAMと混同しない。`B_w`は別モデルとの共有候補であり、現物SHAが一致しなければ実HDDから減算できない。**4TBに収まる証拠はまだない**（既存モデルの外部コード・新規runtime・キャッシュ・staging未測定）。

## 4. H / T / D / C / U と ERROR CHECK

- **H**：Haruの全二重会話とPraxisの動画＋ロボット動作共同生成は、既存141?種類の汎用モデルだけでは重み同一性・タスクが再現できない独自学習成果である。
- **T**：HF固定revisionで**2原本30ファイル＋Qwen依存13ファイルの全43件**を全数検査、公式GitHubコード2 commit、他に既存Wan VAEのSHA照合。最小`n_min=43`。出典・権利・パラメータ・依存が確定しなければ取得停止。
- **D**：非実行の原本source scope・distinct task研究選定はPASS。HDD・ローカルhash・個別Gated許諾・実機復元はUNCERTAIN（全件承認0）。保存不可の法的条件やSHA不一致はFAIL/STOP。
- **C**：Haruの全二重特性が既存Qwen Omniと独立評価で同等、Praxisの学習済みactionが既存のロボットVLAを上回らず保存価値不足、必要依存が欠ける。
- **U**：Publisher性能値、Gated本人権限、第三者wheelとdriver、Wan VAE実物、ロボット評価環境・ハードクロック。確率分布・誤差予算が無いため合成標準不確かさ`u_c`・包含係数`k`は算定しない。

**ERROR CHECK**：旧v37 **191→v38 193**、有効**144→146**、モデル**165→167**、S1追加1/S2追加1、各原本path/bytes/revision確定（ローカル値ではない）、追加版のsource43、同族追加形式0、取得承認0。過去版v37のKumo元ファイル訂正は改変せず保持する。

## 5.〈次に考える問い〉

**最初の保存対象をHaru単体とし、実HDDの残容量・外部依存・合法な原本取得の再現性を確かめたうえで、GatedなPraxisの43ファイル群へ段階的に進める方がよいか。**
