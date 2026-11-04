# 先行的な配布制限シナリオの能力別分類（v11補助調査）

**目的**：テキスト無検閲だけでなく、画像・動画・音声・顔ID・エージェント・専門用途を別々の仕組みとして調べ、**各仕組みから代表候補を原則1件ずつ**選ぶ。これは「規制確率が高い順」ではなく、先行制限の**検証優先度**を作るための分類である。

| 区分 | 仕組み | 既存/調査例 | 判定に必要な証拠 |
|---|---|---|---|
| WEIGHT_REFUSAL_EDIT | 推論前のモデル重みを改変して拒否挙動を変更する。単なるプロンプト注入とは別。 | `orcarouter/Qwen3.8-27B-Uncensored`、`orcarouter/Qwen3.8-Flash-Next-Uncensored`、`knoveleng/Qwen3.5-9B-Uncensored` | 作者の手法・元モデルとの重み差・同条件拒否率/一般能力比較 |
| POST_TRAIN_LOW_REFUSAL | SFT/DPO/RLなどの追加学習で指示追従や拒否挙動が変化。重み直交化とは区別。 | `dphn/Dolphin3.0-Llama3.1-8B` | 学習工程の一次資料、ベースとの制御比較 |
| PROMPT_JAILBREAK | 重みを変えず入力・会話・ツール応答によって安全動作を迂回する試み。原則モデル資産ではなく評価データ・手法として管理。 | 評価手法として管理（モデル重みの自動追加なし） | 安全な評価用データセット、脆弱性再現の測定と許可されたテスト環境 |
| SYSTEM_GUARDRAIL_BYPASS | API・UI・後処理フィルターの差を調査。モデル重みの低拒否性とは別。 | 評価手法として管理（モデル重みの自動追加なし） | サービス規約、システム構成、許可された評価条件 |
| ADULT_IMAGE_FINETUNE | 画像モデルの成人向け微調整・LoRA・マージ。品質と許諾を別に測る。 | `OnomaAIResearch/Illustrious-XL-v1.1` | 正確なチェックポイントと版、元モデルライセンス、総数、画像品質と権利 |
| ADULT_VIDEO_AV_FINETUNE | 動画拡散モデルへのNSFW LoRA・蒸留・マージなど。ベース重みと区別。 | `Lightricks/LTX-2.3`、`Wan-AI/Wan2.2-TI2V-5B` | 特化派生の正確なrepo、ライセンス、総数、動き/同期/VRAMの比較 |
| VOICE_IDENTITY | TTS/VCで特定話者や感情を再現。無検閲という宣伝と声の同意を分ける。 | `Plachta/Seed-VC`、`Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`、`ResembleAI/chatterbox` | 話者同意、話者類似性・自然性・透かし、総数と依存 |
| FACE_IDENTITY | 顔ID/表情/動画の転写。画像生成一般のNSFWとは別の能力。 | `InstantX/InstantID`、`KlingTeam/LivePortrait` | 被写体同意・本人確認、依存、顔保持品質 |
| AUTONOMOUS_AGENT | 外部ツールやOSを操作できるモデル。テキスト拒否率では測れない。 | `microsoft/Fara1.5-27B` | 権限境界、タスク成功率、失敗時の影響、隔離評価 |
| SPECIALIZED_DUAL_USE | 特定用途での危険性や提供条件の変化を調査。汎用モデルの能力だけで推定しない。 | `google/medgemma-4b-it` | 用途・権利・評価環境の明示、実証された提供制限 |

## 重要な区別

1. **重み改変（abliterationなど）**と**後学習による低拒否**は別。元モデルとの差分・拒否率・一般性能を同条件で比較しない限り、「無検閲」のラベルだけで採用しない。
2. **プロンプト・ジェイルブレイク**は重みを変更しない場合があり、原則としてモデル保存枠ではなく許可された安全性評価手法・データに分類する。
3. **外部サービスのコンテンツフィルター**とモデル自体の学習済み能力は別。サービス上の規制を重みの削除確率に転写しない。
4. **成人向け画像・動画**はテキストLLMと別の性能評価。本人同意・著作権・配布者の許諾・依存モデルを個別に確認する。
5. **声・顔の同一性**は成人向け機能と重複し得るが、なりすまし・同意の論点として別に監査する。
6. **安全・法的制限の証拠**は配布者のGated化・ライセンス変更・削除履歴・実効法規を一次URLで示す。今後の拡大は反証可能な仮説であり確率を捏造しない。

## 新たに確認した動画派生

- [ChrisColeTech LTX-2.3 Uncensored v1.4 FP8](https://huggingface.co/ChrisColeTech/LTX-2.3-uncensored-v1.4-FP8)：配布者はNSFW LoRA、蒸留LoRA、参照詳細LoRAを統合したと説明。**license:unknown、総パラメータ数未確定**のため調査のみ。
- [Phr00t LTX2 Rapid Merges](https://huggingface.co/Phr00t/LTX2-Rapid-Merges)：作者がNSFW版の旧版化と保守縮小を説明。現時点で採用しない。
- 画像の[WAI Illustrious公式コレクション](https://huggingface.co/collections/IbarakiDouji/wai-illustrious)は候補系列を示すが、**個別repo ID・バージョン・ライセンス・総数を固定できていないため採用しない**。

## 選定ゲートとERROR CHECK

分類10種、v11既存モデル/資産14件の重複可能な能力例、外部調査候補2件。新規取得承認0件。150B以上のモデルは絶対除外、MoEは全パラメータ総数、総数不明は取得準備停止。権利・本人のGated承認・容量・依存・正確なrevisionを別途検証する。

**次に考える問い**：同じ仕組みのモデル2件について、実際の制限変更と固有能力のどちらの証拠があれば代表を入れ替えるか。
