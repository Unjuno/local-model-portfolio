# v16: 先行的な配布制限に備えるモデル選定法と追加調査（2026-11-04）

## 1. 結論と変更

v15の139資産・有効94件を基準に、**2026年公開の3モデルを台帳追加**。用途を分けて評価し、[Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2)を**条件付き選定**、NSFW動画の[ChrisColeTech LTX-2.5 v1.1](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8)と[Stuubs Remix LTX2.5](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5)を**HOLD**とする。v16は**142管理資産、95有効選定**。取得承認0。

**最重要変更は判定方法の制度化**：モデル年式・人気・名前の「uncensored」・拒否率だけでは採用しない。セーフティ制御の技術機序ごとに1つの有力代表を比較し、現状の公開制限の観測事実と、今後先に規制対象になる仮説を分離する。シナリオS1は予測確率ではなく調査順序。

## 2. 性能・負の証拠

| 候補 | 独自性 | 有利な観測 | 反証・未解決 | 判定 |
|---|---|---|---|---|
| Pantheon-Reasoning-26B-A4B-1.1-V2 | 単なる拒否方向編集でない、推論トレース付きRP SFT。Gemma4系MoE総26.5441B | [第三者Caliper](https://caliperbench.com/m/pantheon-reasoning-26b-a4b-1.1-v2/)：RP総合64.0/100・95/777位、50ターンRP72.4/100 | 創作文章58.4/100・555/777位で弱い。ベンチ提供者と実機条件を再現していない。モデル元との同条件比較不足 | **conditional** |
| ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8 | NSFW＋蒸留＋I2V改良をLTX2.5へ統合 | 作者はFP8主重み21.5GB、int8 encoder13.2GB、audio/video VAEを明記 | **license:unknown**。権利・独立画質・全学習済みパラメータ未確定 | **HOLD** |
| Stuubs/Stubelius_Remix_Ltx2.5 | NSFW＋OmniNFT RLマージ＋蒸留LoRA、Comfy/int8/Q4 | 作者のblind AI-judgeで旧beta2に**29勝・9敗・10分** | 作者主導、公式LTX2.5と直接比較なし。Q4レンダ比較未実施。派生元の複数ライセンス | **HOLD** |
| [CyberRealistic ZImage Turbo v10](https://cyberdelia.nl/models/cyberrealistic-z-image-turbo) | Civitai原版の写実写真特化重み | **作者公式**がFP8 6.41GiB・SHA256 `F74F5E7144B7922B57210EE223F37279CE9D6BBAF8724DD0F4B5412858A99A8A`を提示 | Civitai Early Access、モデル版別許諾と選択ファイル本体のSHA実測未確認。作者画像は客観ベンチでない | 研究保留、HF IDを偽装しない |
| [JonathanColetti Qwen3.8-27B Uncensored](https://huggingface.co/JonathanColetti/Qwen3.8-27B-Uncensored) | 他の拒否方向編集版と比較対象 | [第三者spicysharkco試験](https://huggingface.co/datasets/spicysharkco/uncensored-leaderboard/blob/main/README.md)：有害300中拒否27、無害350中過剰拒否0。GSM8K 94.0%、stock94.0%、MMLU-Pro57.2%、stock57.6% | 既存OrcaRouter派生等と機構が重複し得る。測定はQ6条件、独立の他ベンチは未確認 | 研究保留、重複登録しない |

### サイバー能力関連
OrcaCyber Zero 1.5は公開APIサービスであり、保存可能な同一ウェイトを確認できていない。**ベンチマークはハーネスの実績とモデル単体を混同しない**。安全性評価器[Galvanize-3](https://huggingface.co/usezn/Galvanize-3)は既に有効、Jailbreak検出用[Opus Neo](https://huggingface.co/opus-research/opus-moderation-4-neo)は保留のまま。

## 3. 非補償型判定プロトコル

機械可読の[policies/selection-decision-v16.json](../../policies/selection-decision-v16.json)と静的監査で実施。

1. **存在・権利・原本同一性**：HFのrepo+不変commit、Civitai model/version/file、完全ファイルのSHA256。権利が不明なら取得不可。Pirate Faceのmagnetは一次許諾を代替しない。
2. **技術機序の分類**：重みの拒否方向編集／SFT／DPOなどの選好学習／プロンプト式Jailbreak（重み資産ではなく安全評価）／守備型検出器／画像／動画／声・顔・自律操作、別枠で扱う。**原則1機序1代表、独自機能が実証された場合だけ追加**。
3. **能力と性能維持**：同一ハード・モデルを固定して一般能力、指示追従、出力完了率、拒否率、過剰拒否、創作・生成品質を**別々に測る**。負の証拠を消さない。author-only=上限B/C、無条件にA扱い禁止。
4. **先行規制仮説と観測事実**：現在のGated・権利・削除・期間を一次資料で測り、将来規制の**架空の確率は付けない**。
5. **実行と予算**：全MoE expert・補助学習済みモジュールの総数、150B原則、量子化超過例外は実機ピークRAM512GB未満と品質/速度が必須。HDD全選択byteと空き200GB、作者ライセンス、個別承認は独立ゲート。
6. **最終決定**：PASS=対象タスクで有意な差別化と必須実証を確認、FAIL=重複・不適格・性能不足が明確、UNCERTAIN=証拠不足。**SELECT/CONDITIONALはダウンロード権限ではない**。

## 4. H/T/D/C/Uと測定前提

- **H**（反証可能仮説）：対象モデルは既存で最も近い有効モデルより特定タスクで実用上価値があり、他の主要性能で重大な品質低下がない。閾値を測定前に決める。
- **T**（最小検証）：LLMは無害200・安全性200・命令追従200・一般能力200の事前分割比較を目安とし、画像40プロンプト×各3seed、動画20×3seed、音声各言語30文×同意済み話者5人、実行速度30反復以上。実機／ドライバ／CUDA/Metal／量子化zero-point／context／batch／KV・ABIを固定する。
- **D**（判定）：同一タスク・同一設定で事前宣言した品質閾値と95%区間が満たされ、権利・マニフェスト・容量・実行可能性を満たす場合PASS。欠落・矛盾はUNCERTAIN=保留。法的不可、著しい品質不足や代替可能な重複はFAIL。ダウンロードはPASS後も個別承認。
- **C**（破れ方）：データ汚染、作者と第三者の結果不一致、NSFWを名乗るだけ、長文で思考が閉じない、量子化劣化、VRAM↔RAMオフロード過多、Civitaiの有料/権利条件、Pirate FaceのSeederなし。
- **U**（不確かさ）：二値性能はWilson 95%CI、連続差はpaired bootstrap 95%CIを推奨。誤差の主要源はjudgeの系統誤差、試行間変動、プロンプト汚染、ベンチ選択、量子化による差異。実測なしでは合成標準不確かさ`u_c`は推定不能、拡張係数`k=2`は測定計画上の参考値。探索的な多数比較では多重検定補正し、成功しそうな時点での恣意的な逐次停止は禁止。

### 変数表・次元チェック

| 記号 | 意味（日本語） | SI単位 | 定義 | 前提/範囲 | 型 |
|---|---|---|---|---|---|
| N | モデル総パラメータ数 | 1（個数） | MoE全expert・encoder等を含む | 0以上の整数、未確定はnull | 整数 |
| B | 全選定ファイル | byte | 最終lockの必須ファイルバイトの合計 | 0以上、未選定はnull | 整数 |
| M | 完全な推論ピークRAM | byte | 実機OS＋weight＋KV＋依存・runtimeのピーク | 0以上、未知はnull | 整数 |
| r | 二値成功率 | 1（無次元） | n回中の成功割合 | 0〜1 | 確率スカラー |
| n | 独立評価件数 | 1（個数） | 固定したテスト件数 | 正整数 | 整数 |
| t | 実行所要時間 | s | 生成の実測経過時間 | 非負 | スカラー |
| v | LLM生成速度 | token/s | 単一ストリームの出力token数/秒 | 非負 | スカラー |
| u_c | 合成標準不確かさ | 評価量と同じ | 主要誤差源を合成した不確かさ | 未評価ならnull | スカラー |
| k | 拡張係数 | 1（無次元） | 測定計画の参考値2 | 正 | スカラー |

**次元チェック**：重みバイトBは実機ピークメモリMと同じbyteだが同一量ではない。量子化でBは減少してもNは維持される。token/sとsは混同しない。作者の単発測定値を中央値・区間と書かない。

## 5. 外部一次・研究根拠
- [JailbreakBench原著・共通評価](https://jailbreakbench.github.io/)
- [WildBench原論文 arXiv:2406.04770](https://arxiv.org/abs/2406.04770)
- [BenchMIRT（安全性と推論を分離）](https://huggingface.co/blog/allenai/benchmirt)
- モデル配布者のリンクは上の表。**ここでのモデル別将来規制時期・確率は未実証**。

## ERROR CHECK
管理142件、選定95件、保留29件、deferred12件、excluded6件。モデル119件/データ23件。正常パラメータゲート103件、全総数未確認14件、超150B量子化審査2件。ダウンロード承認0、Torrent・ローカルHDD操作0件。
